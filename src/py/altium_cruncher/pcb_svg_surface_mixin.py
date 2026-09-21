"""Region-aware synthetic surfaces and silkscreen clipping for PCB SVG."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Protocol, cast

from altium_monkey.altium_pcb_svg_renderer import (
    PcbSvgRenderContext,
    PcbSvgRenderOptions,
)
from altium_monkey.altium_record_types import PcbLayer

from .altium_cruncher_pcb_svg_bend_lines import (
    BendLinesRenderer,
    bend_line_view_bounds,
)
from .altium_cruncher_pcb_svg_soldermask_film import (
    SOLDERMASK_FILM_LAYER_IDS,
    SoldermaskFilmRenderer,
    contrasting_silkscreen_color,
)
from .altium_cruncher_pcb_svg_substrate import BoardSubstrateRenderer
from .pcb_svg_render_job import PcbSvgRenderJob

if TYPE_CHECKING:
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc


class _MaskDomain(Protocol):
    def mask_lines(self, ctx: PcbSvgRenderContext, mask_id: str) -> list[str]: ...


class PcbSvgSurfaceMixin:
    """Render synthetic surface tokens and clip completed overlay groups."""

    options: PcbSvgRenderOptions
    render_job: PcbSvgRenderJob

    def _resolved_silkscreen_styles(
        self,
        pcbdoc: AltiumPcbDoc,
        layer: PcbLayer,
        styles: dict[str, dict[str, object]],
    ) -> dict[str, dict[str, object]]:
        names = (
            "silkscreen_component_graphics",
            "silkscreen_designators",
            "silkscreen_board_graphics",
        )
        automatic = tuple(
            name
            for name in names
            if str(styles.get(name, {}).get("color", "")).strip().casefold()
            == "auto"
        )
        if not automatic:
            return styles
        side: Literal["top", "bottom"] = (
            "top" if layer == PcbLayer.TOP_OVERLAY else "bottom"
        )
        color = contrasting_silkscreen_color(
            pcbdoc,
            side,
            styles.get("soldermask_film", {}),
            self.render_job.board_surface_appearances(pcbdoc),
        )
        resolved = dict(styles)
        for name in automatic:
            resolved[name] = {**styles.get(name, {}), "color": color}
        return resolved

    def _bend_line_bounds(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        tokens: list[str],
        styles: dict[str, dict[str, object]],
        mirror: bool,
    ) -> tuple[tuple[float, float, float, float], ...]:
        if "BEND_LINES" not in tokens:
            return ()
        return bend_line_view_bounds(
            ctx,
            self.render_job.layer_stack_document(pcbdoc),
            styles.get("bend_lines", {}),
            requested=True,
            mirror=mirror,
        )

    def _render_surface_token(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        token: str,
        styles: dict[str, dict[str, object]],
        source_layers: list[PcbLayer],
        board_clip_id: str,
        layer_hole_masks: dict[int, tuple[str, list[str]]],
    ) -> list[str] | None:
        surface_copper = self._render_surface_copper(
            ctx,
            pcbdoc,
            token,
            styles,
            board_clip_id,
            layer_hole_masks,
        )
        if surface_copper is not None:
            return surface_copper
        appearance_index = (
            self.render_job.board_surface_appearances(pcbdoc)
            if pcbdoc.board is not None
            else None
        )
        if token in SOLDERMASK_FILM_LAYER_IDS:
            renderer = SoldermaskFilmRenderer(
                self.options,
                primitive_index=self.render_job.primitive_index,
            )
            return renderer.render_film(
                ctx,
                pcbdoc,
                token,
                styles.get("soldermask_film", {}),
                appearance_index,
            )
        if token == "BOARD_SUBSTRATE":
            return BoardSubstrateRenderer(self.options).render_substrate(
                ctx,
                pcbdoc,
                styles.get("board_substrate", {}),
                source_layers,
                appearance_index,
            )
        if token == "BEND_LINES":
            return BendLinesRenderer().render(
                ctx,
                self.render_job.layer_stack_document(pcbdoc),
                styles.get("bend_lines", {}),
                on_invalid=lambda region_index, region_name, source_index, reason: (
                    self._diagnose_invalid_bend_line(
                        pcbdoc, region_index, region_name, source_index, reason
                    )
                ),
            )
        return None

    def _diagnose_invalid_bend_line(
        self,
        pcbdoc: AltiumPcbDoc,
        region_index: int,
        region_name: str,
        source_index: int,
        reason: str,
    ) -> None:
        source = self.render_job.geometry_source(pcbdoc)
        self.render_job.diagnose(
            code="invalid-bend-line",
            category="region_resolution",
            producer="altium-cruncher",
            message=f"{region_name} bend line {source_index}: {reason}; omitted",
            detail={
                "region_index": region_index,
                "region_name": region_name,
                "source_index": source_index,
                "reason": reason,
            },
            occurrence_key=(
                f"bend-line:{self.render_job.identity(source)}:"
                f"{region_index}:{source_index}"
            ),
            source_scoped=True,
        )

    def _clip_silkscreen_to_surface(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        layer: PcbLayer,
        styles: dict[str, dict[str, object]],
        lines: list[str],
    ) -> list[str]:
        if layer not in {PcbLayer.TOP_OVERLAY, PcbLayer.BOTTOM_OVERLAY}:
            return lines
        mode = (
            str(styles.get("silkscreen_surface", {}).get("clip_mode", "none"))
            .strip()
            .casefold()
        )
        if mode == "none":
            return lines
        if mode not in {"board", "film"}:
            raise ValueError(
                "silkscreen_surface.clip_mode must be none, board, or film"
            )
        side = "top" if layer == PcbLayer.TOP_OVERLAY else "bottom"
        mask_id = f"silkscreen-surface-{mode}-{side}"
        domain = self._silkscreen_domain(
            ctx,
            pcbdoc,
            side,
            cast(Literal["board", "film"], mode),
        )
        metadata = (
            ' data-feature="silkscreen-surface-clip"'
            f' data-clip-mode="{mode}" data-side="{side}"'
            if ctx.options.include_metadata
            else ""
        )
        return [
            "<defs>",
            *domain.mask_lines(ctx, mask_id),
            "</defs>",
            f'<g mask="url(#{mask_id})"{metadata}>',
            *lines,
            "</g>",
        ]

    def _silkscreen_domain(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        side: Literal["top", "bottom"],
        mode: Literal["board", "film"],
    ) -> _MaskDomain:
        if mode == "film":
            renderer = SoldermaskFilmRenderer(
                self.options,
                primitive_index=self.render_job.primitive_index,
            )
            return renderer.surface_domain(
                ctx,
                pcbdoc,
                side,
                self.render_job.board_surface_appearances(pcbdoc),
            )
        surface_layer = PcbLayer.TOP if side == "top" else PcbLayer.BOTTOM
        return BoardSubstrateRenderer(self.options).material_domain(
            ctx,
            pcbdoc,
            (surface_layer,),
        )


__all__ = ["PcbSvgSurfaceMixin"]
