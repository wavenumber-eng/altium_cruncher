"""Region-aware outer copper composition for rigid-flex PCB views."""

from __future__ import annotations

import html
from collections import OrderedDict
from typing import TYPE_CHECKING, Literal

from altium_monkey.altium_pcb_layer_ref import PcbLayerRef
from altium_monkey.altium_pcb_svg_renderer import PcbSvgRenderContext
from altium_monkey.altium_record_types import PcbLayer

if TYPE_CHECKING:
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc

    from .pcb_board_region_envelope_index import BoardRegionEnvelope
    from .pcb_board_surface_appearance import BoardSurfaceAppearanceIndex
    from .pcb_svg_render_job import PcbSvgRenderJob


SURFACE_COPPER_LAYER_IDS = {
    "SURFACE_COPPER_TOP": 9016,
    "SURFACE_COPPER_BOTTOM": 9017,
}


class PcbSvgSurfaceCopperMixin:
    """Render each region's resolved outer copper without exposing inner layers."""

    render_job: PcbSvgRenderJob

    def _surface_copper_refs(
        self,
        pcbdoc: AltiumPcbDoc,
        tokens: list[str],
    ) -> list[PcbLayerRef]:
        refs: list[PcbLayerRef] = []
        for token, side in (
            ("SURFACE_COPPER_TOP", "top"),
            ("SURFACE_COPPER_BOTTOM", "bottom"),
        ):
            if token not in tokens:
                continue
            appearances = self.render_job.board_surface_appearances(pcbdoc)
            if appearances.invalid_regions or not appearances.regions:
                fallback = _nominal_ref(side)
                if fallback not in refs:
                    refs.append(fallback)
                continue
            for appearance in appearances.regions:
                ref = appearance.surface(side).copper_layer_ref
                if ref is not None and ref not in refs:
                    refs.append(ref)
        return refs

    def _render_surface_copper(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        token: str,
        styles: dict[str, dict[str, object]],
        board_clip_id: str,
        layer_hole_masks: dict[int, tuple[str, list[str]]],
    ) -> list[str] | None:
        if token not in SURFACE_COPPER_LAYER_IDS:
            return None
        side: Literal["top", "bottom"] = "top" if token.endswith("_TOP") else "bottom"
        appearances = self.render_job.board_surface_appearances(pcbdoc)
        groups = _surface_copper_groups(appearances, side)

        attrs = [
            f'id="layer-{token}"',
            f'data-layer-id="{SURFACE_COPPER_LAYER_IDS[token]}"',
            f'data-layer-key="{token}"',
            f'data-layer-name="{token}"',
            'data-layer-origin="synthetic-region-surface-copper"',
        ]
        lines = [f"<g {' '.join(attrs)}>"]
        for ref, layer_key, regions in groups:
            clip_id = board_clip_id
            if regions:
                clip_id = f"surface-copper-{side}-{_safe_id(layer_key)}"
                path = " ".join(_region_path(ctx, region) for region in regions)
                lines.extend(
                    (
                        "<defs>",
                        f'<clipPath id="{clip_id}"><path d="{path}" '
                        'fill-rule="evenodd" clip-rule="evenodd"/></clipPath>',
                        "</defs>",
                    )
                )
            rendered = self._render_surface_copper_ref(
                ctx,
                pcbdoc,
                ref,
                styles,
                clip_id,
                layer_hole_masks,
            )
            child_id = f"surface-copper-{side}-{_safe_id(layer_key or ref.token)}"
            lines.extend(_retag_group(rendered, child_id, layer_key))
        lines.append("</g>")
        return lines

    def _render_surface_copper_ref(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        ref: PcbLayerRef,
        styles: dict[str, dict[str, object]],
        clip_id: str,
        layer_hole_masks: dict[int, tuple[str, list[str]]],
    ) -> list[str]:
        layer = ref.legacy_layer
        if layer is None:
            return self._render_a0_v7_layer(
                ctx,
                pcbdoc,
                ref,
                board_clip_id=clip_id,
            )
        return self._render_a0_physical_layer(
            ctx,
            pcbdoc,
            layer,
            styles,
            clip_path_id=clip_id,
            mask_id=layer_hole_masks.get(layer.value, (None, []))[0],
        )


def _surface_copper_groups(
    appearances: BoardSurfaceAppearanceIndex,
    side: Literal["top", "bottom"],
) -> tuple[tuple[PcbLayerRef, str, tuple[BoardRegionEnvelope, ...]], ...]:
    if appearances.invalid_regions or not appearances.regions:
        return ((_nominal_ref(side), "", ()),)
    grouped: OrderedDict[PcbLayerRef, tuple[str, list[BoardRegionEnvelope]]] = (
        OrderedDict()
    )
    for appearance in appearances.regions:
        surface = appearance.surface(side)
        ref = surface.copper_layer_ref
        if ref is None:
            continue
        if ref not in grouped:
            grouped[ref] = (surface.copper_layer_key, [])
        grouped[ref][1].append(appearance.region)
    return tuple(
        (ref, layer_key, tuple(regions))
        for ref, (layer_key, regions) in grouped.items()
    )


def _nominal_ref(side: Literal["top", "bottom"]) -> PcbLayerRef:
    layer = PcbLayer.TOP if side == "top" else PcbLayer.BOTTOM
    return PcbLayerRef.from_legacy(layer)


def _region_path(ctx: PcbSvgRenderContext, region: BoardRegionEnvelope) -> str:
    rings = (region.outline_mils, *region.holes_mils)
    commands: list[str] = []
    for ring in rings:
        if len(ring) < 3:
            continue
        x, y = ring[0]
        commands.append(f"M {ctx.fmt(ctx.x_to_svg(x))} {ctx.fmt(ctx.y_to_svg(y))}")
        commands.extend(
            f"L {ctx.fmt(ctx.x_to_svg(px))} {ctx.fmt(ctx.y_to_svg(py))}"
            for px, py in ring[1:]
        )
        commands.append("Z")
    return " ".join(commands)


def _retag_group(lines: list[str], group_id: str, layer_key: str) -> list[str]:
    if not lines:
        return []
    result = list(lines)
    result[0] = result[0].replace('id="layer-', f'id="{html.escape(group_id)}-', 1)
    if layer_key and "<g " in result[0]:
        result[0] = result[0].replace(
            "<g ",
            f'<g data-surface-layer-key="{html.escape(layer_key)}" ',
            1,
        )
    return result


def _safe_id(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "._-" else "-" for ch in value)


__all__ = ["PcbSvgSurfaceCopperMixin", "SURFACE_COPPER_LAYER_IDS"]
