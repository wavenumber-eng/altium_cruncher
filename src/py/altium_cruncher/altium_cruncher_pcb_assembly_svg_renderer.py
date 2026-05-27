"""Altium Cruncher assembly SVG renderer with Geometer-backed HLR."""

from __future__ import annotations

import html
from typing import TYPE_CHECKING, Any

from altium_monkey.altium_pcb_surface import (
    PCB_SurfaceRole,
    PCB_SurfaceSide,
    pcb_surface_layers,
)
from altium_monkey.altium_record_types import PcbLayer
from altium_cruncher.altium_cruncher_pcb_assembly_svg_base import (
    CruncherPcbAssemblySvgRenderer as _BaseCruncherPcbAssemblySvgRenderer,
    CruncherPcbAssemblySvgRenderOptions,
)
from altium_cruncher.altium_cruncher_pcb_workflow import iter_pcb_render_inputs

from altium_cruncher.altium_cruncher_pcb_svg_assembly_projection import (
    AssemblyProjectionOptions,
    get_assembly_projection_cache,
)

if TYPE_CHECKING:
    from altium_monkey.altium_design import AltiumDesign
    from altium_monkey.altium_pcb_svg_renderer import PcbSvgRenderContext


_ASSEMBLY_CONNECTING_COPPER_COLOR = "#C8C8C8"
_ASSEMBLY_PAD_COLOR = "#707070"
_ASSEMBLY_SILKSCREEN_COLOR = "#8C8C8C"


class CruncherPcbAssemblySvgRenderer(_BaseCruncherPcbAssemblySvgRenderer):
    """Assembly renderer that resolves STEP HLR through Altium Cruncher."""

    @staticmethod
    def _assembly_projection_types():
        return AssemblyProjectionOptions, get_assembly_projection_cache

    def _collect_layer_primitives(
        self,
        ctx: "PcbSvgRenderContext",
        pcbdoc: Any,
        layer: PcbLayer,
        layer_color_override: str | None = None,
    ) -> tuple[str, list[str], list[str]]:
        if not layer.is_copper():
            layer_color = (
                _ASSEMBLY_SILKSCREEN_COLOR
                if layer in {PcbLayer.TOP_OVERLAY, PcbLayer.BOTTOM_OVERLAY}
                else layer_color_override or ctx.layer_color(layer)
            )
            return super()._collect_layer_primitives(  # noqa: SLF001
                ctx,
                pcbdoc,
                layer,
                layer_color,
            )

        connecting_color = _ASSEMBLY_CONNECTING_COPPER_COLOR
        pad_color = _ASSEMBLY_PAD_COLOR
        base_primitives: list[str] = []
        base_primitives.extend(self._render_fills_for_layer(ctx, pcbdoc, layer, connecting_color))  # noqa: SLF001
        base_primitives.extend(self._render_vias_for_layer(ctx, pcbdoc, layer, connecting_color))  # noqa: SLF001
        base_primitives.extend(self._render_tracks_for_layer(ctx, pcbdoc, layer, connecting_color))  # noqa: SLF001
        base_primitives.extend(self._render_arcs_for_layer(ctx, pcbdoc, layer, connecting_color))  # noqa: SLF001
        base_primitives.extend(self._render_texts_for_layer(ctx, pcbdoc, layer, connecting_color))  # noqa: SLF001
        # Linked polygon regions use polygon_overlay_color; unlinked region
        # shapes are commonly custom pads and stay in the pad color.
        base_primitives.extend(self._render_regions_for_layer(ctx, pcbdoc, layer, pad_color))  # noqa: SLF001
        base_primitives.extend(self._render_pads_for_layer(ctx, pcbdoc, layer, pad_color))  # noqa: SLF001

        drill_primitives = self._render_drill_holes_for_layer(ctx, pcbdoc, layer)  # noqa: SLF001
        return connecting_color, base_primitives, drill_primitives

    def _build_assembly_symbol_defs(
        self,
        *,
        simple_id: str,
        detail_id: str,
        projected: Any,
    ) -> list[str]:
        lines: list[str] = []
        if self.options.assembly_include_simple:
            lines.append(
                "    "
                + (
                    f'<g id="{html.escape(simple_id)}" data-assembly-symbol="simple" '
                    'stroke-width="0.12">'
                )
            )
            lines.extend(
                self._assembly_geometry_elements_local(  # noqa: SLF001
                    line_segments=tuple(projected.simple_line_segments),
                    arcs=tuple(projected.simple_arcs),
                )
            )
            lines.append("    </g>")

        if self.options.assembly_include_detail:
            lines.append(
                "    "
                + (
                    f'<g id="{html.escape(detail_id)}" data-assembly-symbol="detail" '
                    'stroke-width="0.08">'
                )
            )
            lines.extend(
                self._assembly_geometry_elements_local(  # noqa: SLF001
                    line_segments=tuple(projected.detail_line_segments),
                    arcs=tuple(projected.detail_arcs),
                )
            )
            lines.append("    </g>")

        return lines


def _surface_role_order_from_tokens(
    order_tokens: list[str] | tuple[str, ...] | None,
    *,
    include_missing_roles: bool,
) -> list[PCB_SurfaceRole]:
    ordered_roles: list[PCB_SurfaceRole] = []
    for token in list(order_tokens or []):
        normalized = str(token or "").strip().lower()
        if not normalized:
            continue
        role = PCB_SurfaceRole(normalized)
        if role not in ordered_roles:
            ordered_roles.append(role)
    if include_missing_roles:
        for role in (PCB_SurfaceRole.COPPER, PCB_SurfaceRole.SILKSCREEN):
            if role not in ordered_roles:
                ordered_roles.append(role)
    return ordered_roles


def _assembly_mode_outputs(
    *,
    primary_key: str,
    simple_key: str,
    include_simple: bool,
    include_detail: bool,
) -> list[tuple[str, bool, bool, bool]]:
    outputs: list[tuple[str, bool, bool, bool]] = []
    if include_detail:
        outputs.append((primary_key, False, True, True))
    elif include_simple:
        outputs.append((primary_key, True, False, False))
    if include_simple and include_detail:
        outputs.append((simple_key, True, False, False))
    return outputs


def render_pcb_assembly_svg_views(
    design: "AltiumDesign",
    *,
    pcbdoc_selector: str | None = None,
    views: set[str] | None = None,
    layer_filter: set[PcbLayer] | None = None,
    monochrome_color: str = "#000000",
    plated_drill_color: str = "#90EE90",
    non_plated_drill_color: str = "#ADD8E6",
    drill_mode: str = "overlay",
    drill_overlay_opacity: float = 1.0,
    include_metadata: bool = True,
    include_board_outline: bool = True,
    show_empty_layers: bool = False,
    include_polygon_definition_overlays: bool = False,
    polygon_overlay_color: str = "#000000",
    board_cutout_color: str = "#FF0000",
    mirror_bottom_view: bool = True,
    clip_to_outline: bool = True,
    clip_holes_from_copper: bool = True,
    assembly_enabled: bool = False,
    assembly_include_simple: bool = True,
    assembly_include_detail: bool = True,
    assembly_curve_mode: str = "native_arcs",
    assembly_samples_per_curve: int = 24,
    assembly_round_digits: int = 3,
    assembly_include_visible: bool = True,
    assembly_include_outline: bool = True,
    assembly_union_polygons: bool = True,
    assembly_overlay_color: str = "#F59E0B",
    svg_display_scale: float = 1.0,
    svg_size_unit: str = "",
    top_board_outline_color: str | None = None,
    top_board_cutout_color: str | None = None,
    top_copper_color: str | None = None,
    top_silkscreen_color: str | None = None,
    top_plated_drill_color: str | None = None,
    top_non_plated_drill_color: str | None = None,
    top_polygon_overlay_color: str | None = None,
    top_layer_order: list[str] | tuple[str, ...] | None = None,
    bottom_board_outline_color: str | None = None,
    bottom_board_cutout_color: str | None = None,
    bottom_copper_color: str | None = None,
    bottom_silkscreen_color: str | None = None,
    bottom_plated_drill_color: str | None = None,
    bottom_non_plated_drill_color: str | None = None,
    bottom_polygon_overlay_color: str | None = None,
    bottom_layer_order: list[str] | tuple[str, ...] | None = None,
    assembly_top_layer_order: list[str] | tuple[str, ...] | None = None,
    assembly_bottom_layer_order: list[str] | tuple[str, ...] | None = None,
    **_ignored: Any,
) -> dict[str, dict[str, str]]:
    del (
        layer_filter,
        show_empty_layers,
        include_polygon_definition_overlays,
        polygon_overlay_color,
        top_polygon_overlay_color,
        top_layer_order,
        bottom_polygon_overlay_color,
        bottom_layer_order,
    )
    normalized_views = {v.strip().lower() for v in (views or set()) if v and v.strip()}
    if not normalized_views:
        return {}
    unsupported = normalized_views - {"assembly-top", "assembly-bottom"}
    if unsupported:
        raise ValueError(
            "render_pcb_assembly_svg_views() only supports assembly surface views; "
            f"got {sorted(unsupported)}"
        )
    rendered: dict[str, dict[str, str]] = {}

    for render_input in iter_pcb_render_inputs(design, pcbdoc_selector=pcbdoc_selector):
        pcbdoc = render_input.pcbdoc
        board_key = render_input.board_key
        board_views: dict[str, str] = {}

        if "assembly-top" in normalized_views:
            top_role_order = _surface_role_order_from_tokens(
                assembly_top_layer_order or ["copper"],
                include_missing_roles=False,
            )
            top_layers_in_order = pcb_surface_layers(
                PCB_SurfaceSide.TOP,
                role_order=top_role_order,
                include_missing_roles=False,
            )
            top_options = dict(
                visible_layers=set(top_layers_in_order),
                layer_render_order=top_layers_in_order,
                layer_colors={
                    PcbLayer.TOP: _ASSEMBLY_CONNECTING_COPPER_COLOR,
                    PcbLayer.TOP_OVERLAY: _ASSEMBLY_SILKSCREEN_COLOR,
                },
                show_empty_layers=True,
                include_metadata=include_metadata,
                show_board_outline=include_board_outline,
                board_outline_color=top_board_outline_color or monochrome_color,
                board_cutout_color=top_board_cutout_color or board_cutout_color,
                drill_hole_mode=drill_mode,
                drill_hole_overlay_plated_color=top_plated_drill_color
                or plated_drill_color,
                drill_hole_overlay_non_plated_color=top_non_plated_drill_color
                or non_plated_drill_color,
                drill_hole_overlay_opacity=drill_overlay_opacity,
                clip_copper_to_board_outline=clip_to_outline,
                clip_all_layers_to_board_outline=clip_to_outline,
                clip_holes_from_copper=clip_holes_from_copper,
                polygon_overlay_color=_ASSEMBLY_CONNECTING_COPPER_COLOR,
                include_assembly_overlay=assembly_enabled,
                assembly_view_side="top",
                assembly_curve_mode=assembly_curve_mode,
                assembly_samples_per_curve=assembly_samples_per_curve,
                assembly_round_digits=assembly_round_digits,
                assembly_include_outline=assembly_include_outline,
                assembly_union_polygons=assembly_union_polygons,
                assembly_overlay_color=assembly_overlay_color,
                svg_display_scale=svg_display_scale,
                svg_size_unit=svg_size_unit,
            )
            for view_key, include_simple, include_detail, include_visible in _assembly_mode_outputs(
                primary_key="assembly_top_view",
                simple_key="assembly_top_simple_view",
                include_simple=assembly_include_simple,
                include_detail=assembly_include_detail,
            ):
                top_renderer = CruncherPcbAssemblySvgRenderer(
                    CruncherPcbAssemblySvgRenderOptions(
                        **top_options,
                        assembly_include_simple=include_simple,
                        assembly_include_detail=include_detail,
                        assembly_include_visible=assembly_include_visible
                        if include_visible
                        else False,
                    )
                )
                board_views[view_key] = top_renderer.render_board(
                    pcbdoc,
                    project_parameters=render_input.project_parameters,
                )

        if "assembly-bottom" in normalized_views:
            bottom_role_order = _surface_role_order_from_tokens(
                assembly_bottom_layer_order or ["copper"],
                include_missing_roles=False,
            )
            bottom_layers_in_order = pcb_surface_layers(
                PCB_SurfaceSide.BOTTOM,
                role_order=bottom_role_order,
                include_missing_roles=False,
            )
            bottom_options = dict(
                visible_layers=set(bottom_layers_in_order),
                layer_render_order=bottom_layers_in_order,
                layer_colors={
                    PcbLayer.BOTTOM: _ASSEMBLY_CONNECTING_COPPER_COLOR,
                    PcbLayer.BOTTOM_OVERLAY: _ASSEMBLY_SILKSCREEN_COLOR,
                },
                show_empty_layers=True,
                include_metadata=include_metadata,
                show_board_outline=include_board_outline,
                board_outline_color=bottom_board_outline_color or monochrome_color,
                board_cutout_color=bottom_board_cutout_color or board_cutout_color,
                drill_hole_mode=drill_mode,
                drill_hole_overlay_plated_color=bottom_plated_drill_color
                or plated_drill_color,
                drill_hole_overlay_non_plated_color=bottom_non_plated_drill_color
                or non_plated_drill_color,
                drill_hole_overlay_opacity=drill_overlay_opacity,
                clip_copper_to_board_outline=clip_to_outline,
                clip_all_layers_to_board_outline=clip_to_outline,
                clip_holes_from_copper=clip_holes_from_copper,
                polygon_overlay_color=_ASSEMBLY_CONNECTING_COPPER_COLOR,
                include_assembly_overlay=assembly_enabled,
                assembly_view_side="bottom",
                assembly_curve_mode=assembly_curve_mode,
                assembly_samples_per_curve=assembly_samples_per_curve,
                assembly_round_digits=assembly_round_digits,
                assembly_include_outline=assembly_include_outline,
                assembly_union_polygons=assembly_union_polygons,
                assembly_overlay_color=assembly_overlay_color,
                mirror_x=mirror_bottom_view,
                svg_display_scale=svg_display_scale,
                svg_size_unit=svg_size_unit,
            )
            for view_key, include_simple, include_detail, include_visible in _assembly_mode_outputs(
                primary_key="assembly_bottom_view",
                simple_key="assembly_bottom_simple_view",
                include_simple=assembly_include_simple,
                include_detail=assembly_include_detail,
            ):
                bottom_renderer = CruncherPcbAssemblySvgRenderer(
                    CruncherPcbAssemblySvgRenderOptions(
                        **bottom_options,
                        assembly_include_simple=include_simple,
                        assembly_include_detail=include_detail,
                        assembly_include_visible=assembly_include_visible
                        if include_visible
                        else False,
                    )
                )
                board_views[view_key] = bottom_renderer.render_board(
                    pcbdoc,
                    project_parameters=render_input.project_parameters,
                )

        rendered[board_key] = board_views

    return rendered


__all__ = [
    "CruncherPcbAssemblySvgRenderOptions",
    "CruncherPcbAssemblySvgRenderer",
    "render_pcb_assembly_svg_views",
]
