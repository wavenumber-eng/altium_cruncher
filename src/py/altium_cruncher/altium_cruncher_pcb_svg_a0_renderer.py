"""Explicit A0 PCB SVG compositor."""

from __future__ import annotations

import html
import json
import logging
import math
import xml.etree.ElementTree as ET
from dataclasses import replace
from pathlib import Path
from typing import TYPE_CHECKING

from altium_monkey.altium_pcb_svg_renderer import (
    _MIL_TO_MM,
    PcbSvgRenderContext,
    PcbSvgRenderOptions,
    SVG_ENRICHMENT_METADATA_ID,
    SVG_ENRICHMENT_SCHEMA_ID,
    should_render_via_drill_hole,
)
from altium_monkey.altium_record_types import PcbLayer

from altium_cruncher.altium_cruncher_pcb_assembly_svg_base import (
    CruncherPcbAssemblySvgRenderOptions,
)
from altium_cruncher.altium_cruncher_pcb_assembly_svg_renderer import (
    CruncherPcbAssemblySvgRenderer,
)
from altium_cruncher.altium_cruncher_pcb_svg_config import (
    PCB_SVG_SPECIAL_LAYERS,
    PcbSvgConfig,
    PcbSvgViewConfig,
    pcb_svg_physical_layer_from_token,
    resolve_config_output_path,
)
from altium_cruncher.altium_cruncher_pcb_svg_assembly_projection import (
    AssemblyProjectionOptions,
)
from altium_cruncher.altium_cruncher_pcb_svg_cutout_layer import (
    CruncherPcbCutoutLayerRenderer,
    PCB_SVG_BOARD_CUTOUTS_LAYER_ID,
)
from altium_cruncher.altium_cruncher_pcb_svg_pin1 import (
    choose_pin1_pad_designator,
    is_grid_pad_designator,
)
from altium_cruncher.altium_cruncher_pcb_workflow import (
    CruncherPcbRenderInput,
    iter_pcb_render_inputs,
    load_design_for_pcb_input,
)

if TYPE_CHECKING:
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc

log = logging.getLogger(__name__)

PCB_SVG_BOARD_OUTLINE_LAYER_ID = 9000
PCB_SVG_DRILLS_LAYER_ID = 9001
PCB_SVG_SLOTS_LAYER_ID = 9003
PCB_SVG_ASSEMBLY_HLR_TOP_LAYER_ID = 9004
PCB_SVG_ASSEMBLY_HLR_BOTTOM_LAYER_ID = 9005
PCB_SVG_PIN1_TOP_LAYER_ID = 9006
PCB_SVG_PIN1_BOTTOM_LAYER_ID = 9007
PCB_SVG_ASSEMBLY_DESIGNATORS_TOP_LAYER_ID = 9008
PCB_SVG_ASSEMBLY_DESIGNATORS_BOTTOM_LAYER_ID = 9009

_HLR_TOKENS = {"ASSEMBLY_HLR_TOP", "ASSEMBLY_HLR_BOTTOM"}
_HOLE_TOKENS = {"DRILLS", "SLOTS"}
_PIN1_TOKENS = {"PIN1_TOP", "PIN1_BOTTOM"}
_SVG_NS = "http://www.w3.org/2000/svg"
_MM_TO_MIL = 1.0 / _MIL_TO_MM
_ASSEMBLY_HLR_EDGE_FLAG_KEYS = {
    "edge_v_sharp",
    "edge_v_outline",
    "edge_v_smooth",
    "edge_v_sewn",
    "edge_v_iso",
    "edge_h_sharp",
    "edge_h_outline",
    "edge_h_smooth",
    "edge_h_sewn",
    "edge_h_iso",
}


def _style_enabled(styles: dict[str, dict[str, object]], name: str) -> bool:
    return bool(styles.get(name, {}).get("enabled", True))


def _style_color(styles: dict[str, dict[str, object]], name: str, default: str) -> str:
    return str(styles.get(name, {}).get("color") or default)


def _style_float(
    styles: dict[str, dict[str, object]],
    name: str,
    key: str,
    default: float,
) -> float:
    value = styles.get(name, {}).get(key, default)
    if not isinstance(value, (int, float, str)):
        raise ValueError(f"Invalid pcb-svg style value {name}.{key}")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid pcb-svg style value {name}.{key}") from exc


def _style_int(
    styles: dict[str, dict[str, object]],
    name: str,
    key: str,
    default: int,
) -> int:
    value = styles.get(name, {}).get(key, default)
    if not isinstance(value, (int, float, str)):
        raise ValueError(f"Invalid pcb-svg style value {name}.{key}")
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid pcb-svg style value {name}.{key}") from exc


def _style_bool(
    styles: dict[str, dict[str, object]],
    name: str,
    key: str,
    default: bool,
) -> bool:
    value = styles.get(name, {}).get(key, default)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.lower().strip()
        if normalized in {"1", "true", "yes", "on"}:
            return True
        if normalized in {"0", "false", "no", "off"}:
            return False
    return bool(value)


def _style_plating_color(
    styles: dict[str, dict[str, object]],
    name: str,
    *,
    plated: bool,
) -> str:
    style = styles.get(name, {})
    key = "plated_color" if plated else "non_plated_color"
    return str(style.get(key) or ("#90EE90" if plated else "#ADD8E6"))


def _is_component_linked(primitive: object) -> bool:
    try:
        component_index = int(getattr(primitive, "component_index", -1))
    except (TypeError, ValueError):
        return False
    return component_index >= 0 and component_index not in {0xFFFF, 65535}


def _pad_has_hole(pad: object) -> bool:
    try:
        return int(getattr(pad, "hole_size", 0) or 0) > 0
    except (TypeError, ValueError):
        return False


def _pad_is_slot(pad: object) -> bool:
    try:
        hole_shape = int(getattr(pad, "hole_shape", 0) or 0)
        hole_size = int(getattr(pad, "hole_size", 0) or 0)
        slot_size = int(getattr(pad, "slot_size", 0) or 0)
    except (TypeError, ValueError):
        return False
    return hole_shape == 2 and hole_size > 0 and slot_size > hole_size


def _object_float(value: object, default: float = 0.0) -> float:
    if isinstance(value, (int, float, str)):
        try:
            return float(value)
        except (TypeError, ValueError):
            return default
    return default


def _pad_center_mils(pad: object) -> tuple[float, float]:
    center = getattr(pad, "pad_center_mils", None)
    if callable(center):
        try:
            result = center()
            if isinstance(result, (list, tuple)) and len(result) >= 2:
                return (_object_float(result[0]), _object_float(result[1]))
        except (TypeError, ValueError):
            pass
    x_value = getattr(pad, "x_mils", 0.0)
    y_value = getattr(pad, "y_mils", 0.0)
    return (_object_float(x_value), _object_float(y_value))


def _pad_size_mils(pad: object, layer: PcbLayer) -> tuple[float, float]:
    layer_size = getattr(pad, "_layer_size", None)
    if callable(layer_size):
        try:
            result = layer_size(layer)
            if isinstance(result, (list, tuple)) and len(result) >= 2:
                return (
                    _object_float(result[0]) / 10000.0,
                    _object_float(result[1]) / 10000.0,
                )
        except (TypeError, ValueError):
            pass
    width = getattr(pad, "width_mils", 0.0)
    height = getattr(pad, "height", 0.0)
    return (_object_float(width), _object_float(height) / 10000.0)


def _pad_renders_on_layer(pad: object, layer: PcbLayer) -> bool:
    should_render = getattr(pad, "_should_render_on_layer", None)
    if callable(should_render):
        try:
            return bool(should_render(layer))
        except (TypeError, ValueError):
            return False
    return True


def _component_side(component: object) -> str:
    normalized = getattr(component, "get_layer_normalized", None)
    if callable(normalized):
        try:
            side = str(normalized()).strip().lower()
            if side:
                return side
        except (TypeError, ValueError):
            pass
    raw_layer = str(getattr(component, "layer", "") or "").strip().lower()
    if "bottom" in raw_layer:
        return "bottom"
    if "top" in raw_layer:
        return "top"
    return raw_layer


def _component_designator(component: object) -> str:
    return str(getattr(component, "designator", "") or "").strip()


def _reference_designator_prefix(designator: str) -> str:
    text = str(designator or "").strip().upper()
    index = 0
    while index < len(text) and text[index].isalpha():
        index += 1
    return text[:index] if index > 0 else text


def _normalize_draw_order(tokens: list[str]) -> list[str]:
    body: list[str] = []
    holes: list[str] = []
    hlr: list[str] = []
    for token in tokens:
        if token in _HLR_TOKENS:
            if token not in hlr:
                hlr.append(token)
        elif token in _HOLE_TOKENS:
            if token not in holes:
                holes.append(token)
        elif token not in body:
            body.append(token)
    return body + holes + hlr


def _safe_svg_id(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "._-" else "-" for ch in value).strip("-")


def _synthetic_layer_metadata_attrs(
    layer_id: int,
    *,
    key: str,
    display_name: str,
    role: str = "annotation",
) -> list[str]:
    return [
        f'data-layer-id="{int(layer_id)}"',
        f'data-layer-key="{html.escape(key)}"',
        f'data-layer-name="{html.escape(key)}"',
        f'data-layer-display-name="{html.escape(display_name)}"',
        f'data-layer-role="{html.escape(role)}"',
    ]


class PcbSvgA0Renderer(CruncherPcbCutoutLayerRenderer):
    """Render explicit A0 PCB SVG layer and composed view outputs."""

    def __init__(self, config: PcbSvgConfig) -> None:
        self.config = config
        options = PcbSvgRenderOptions(
            include_metadata=config.global_options.include_metadata,
            show_empty_layers=config.global_options.show_empty_layers,
            show_board_outline=True,
            board_outline_color="#000000",
            board_cutout_color="#FF0000",
            clip_copper_to_board_outline=config.global_options.clip_to_outline,
            clip_all_layers_to_board_outline=config.global_options.clip_to_outline,
            clip_holes_from_copper=config.global_options.clip_holes_from_copper,
            svg_display_scale=config.global_options.svg_scale,
            svg_size_unit=config.global_options.svg_size_unit,
            drill_hole_mode="overlay",
            drill_holes_as_layer_group=False,
        )
        super().__init__(options=options)

    def _compute_bounds_mils(
        self,
        pcbdoc: "AltiumPcbDoc",
    ) -> tuple[float, float, float, float]:
        canvas = self.config.global_options.canvas
        if canvas.bounds != "board_outline":
            return super()._compute_bounds_mils(pcbdoc)  # noqa: SLF001

        outline_bounds = self._compute_board_outline_canvas_bounds_mils(pcbdoc)
        if outline_bounds is None:
            return super()._compute_bounds_mils(pcbdoc)  # noqa: SLF001

        margin_mils = canvas.margin_mm * _MM_TO_MIL
        min_x, min_y, max_x, max_y = outline_bounds
        return (
            min_x - margin_mils,
            min_y - margin_mils,
            max_x + margin_mils,
            max_y + margin_mils,
        )

    def _compute_board_outline_canvas_bounds_mils(
        self,
        pcbdoc: "AltiumPcbDoc",
    ) -> tuple[float, float, float, float] | None:
        outline = getattr(getattr(pcbdoc, "board", None), "outline", None)
        if outline is None or not getattr(outline, "vertices", None):
            return None
        try:
            min_x, min_y, max_x, max_y = outline.bounding_box
        except (TypeError, ValueError, AttributeError):
            return None
        return (float(min_x), float(min_y), float(max_x), float(max_y))

    def _canvas_metadata_attrs(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: "AltiumPcbDoc",
    ) -> list[str]:
        origin_x, origin_y = self._board_origin_mils(pcbdoc)
        return [
            f'data-canvas-bounds-mode="{html.escape(self.config.global_options.canvas.bounds)}"',
            f'data-canvas-min-x-mils="{ctx.fmt(ctx.min_x_mils)}"',
            f'data-canvas-min-y-mils="{ctx.fmt(ctx.min_y_mils)}"',
            f'data-canvas-max-x-mils="{ctx.fmt(ctx.max_x_mils)}"',
            f'data-canvas-max-y-mils="{ctx.fmt(ctx.max_y_mils)}"',
            f'data-altium-origin-x-mils="{ctx.fmt(origin_x)}"',
            f'data-altium-origin-y-mils="{ctx.fmt(origin_y)}"',
        ]

    def _canvas_metadata_payload(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: "AltiumPcbDoc",
    ) -> dict[str, object]:
        origin_x, origin_y = self._board_origin_mils(pcbdoc)
        return {
            "bounds_mode": self.config.global_options.canvas.bounds,
            "bounds_mils": [
                ctx.min_x_mils,
                ctx.min_y_mils,
                ctx.max_x_mils,
                ctx.max_y_mils,
            ],
            "margin_mm": self.config.global_options.canvas.margin_mm,
            "altium_origin_mils": [origin_x, origin_y],
            "svg_units": "mm",
            "geometry_transform": {
                "x_svg_mm": "(x_absolute_mils - canvas_min_x_mils) * 0.0254",
                "y_svg_mm": "(canvas_max_y_mils - y_absolute_mils) * 0.0254",
            },
            "metadata_coordinate_policy": (
                "component x_mils/y_mils are source absolute mils; "
                "x_origin_relative_mils/y_origin_relative_mils subtract the Altium origin"
            ),
        }

    @staticmethod
    def _board_origin_mils(pcbdoc: "AltiumPcbDoc") -> tuple[float, float]:
        board = getattr(pcbdoc, "board", None)
        if board is None:
            return (0.0, 0.0)
        try:
            return (float(getattr(board, "origin_x", 0.0)), float(getattr(board, "origin_y", 0.0)))
        except (TypeError, ValueError):
            return (0.0, 0.0)

    def _append_svg_metadata(
        self,
        lines: list[str],
        ctx: PcbSvgRenderContext,
        view_kind: str,
        active_layer_ids: list[int],
        *,
        include_board_outline: bool,
        pcbdoc: "AltiumPcbDoc",
    ) -> None:
        if not self.options.include_metadata:
            return

        enrichment_payload = ctx.enrichment_metadata_payload(
            view_kind=view_kind,
            included_layer_ids=active_layer_ids,
            includes_board_outline=bool(
                include_board_outline and self.options.show_board_outline
            ),
            pcbdoc_filename=pcbdoc.filepath.name if pcbdoc.filepath else None,
        )
        enrichment_payload["canvas"] = self._canvas_metadata_payload(ctx, pcbdoc)
        payload_json = json.dumps(
            enrichment_payload,
            sort_keys=True,
            separators=(",", ":"),
        )
        lines.append(
            f'  <metadata id="{SVG_ENRICHMENT_METADATA_ID}" '
            f'data-schema="{SVG_ENRICHMENT_SCHEMA_ID}">'
        )
        lines.append(f"    {html.escape(payload_json, quote=False)}")
        lines.append("  </metadata>")

    def _build_component_metadata(
        self,
        pcbdoc: "AltiumPcbDoc",
    ) -> tuple[dict[int, str], dict[int, str], dict[int, dict[str, object]]]:
        designators, uids, components = super()._build_component_metadata(pcbdoc)  # noqa: SLF001
        origin_x, origin_y = self._board_origin_mils(pcbdoc)
        for entry in components.values():
            x_value = entry.get("x_mils")
            y_value = entry.get("y_mils")
            if isinstance(x_value, (int, float)) and isinstance(y_value, (int, float)):
                entry["x_absolute_mils"] = float(x_value)
                entry["y_absolute_mils"] = float(y_value)
                entry["x_origin_relative_mils"] = float(x_value) - origin_x
                entry["y_origin_relative_mils"] = float(y_value) - origin_y
        return designators, uids, components

    def render_view_svg(
        self,
        pcbdoc: AltiumPcbDoc,
        view: PcbSvgViewConfig,
        *,
        project_parameters: dict[str, str] | None,
        layers: list[str],
        group_id: str,
        mirror: bool,
        styles: dict[str, dict[str, object]],
    ) -> str:
        """Render one explicit view into a complete SVG document."""
        tokens = _normalize_draw_order([token for token in layers if token])
        physical_layers = self._physical_layers_from_tokens(tokens)
        options = replace(
            self.options,
            visible_layers=set(physical_layers),
            layer_render_order=physical_layers,
            mirror_x=mirror,
            board_outline_color=_style_color(styles, "board_outline", "#000000"),
            board_cutout_color=_style_color(styles, "board_cutouts", "#FF0000"),
            polygon_overlay_color=_style_color(styles, "copper_polygons", "#888888"),
        )
        self.options = options

        ctx = self._build_context(pcbdoc, project_parameters=project_parameters)  # noqa: SLF001
        board_clip_id, board_clip_path_d = self._resolve_board_clip_definition(  # noqa: SLF001
            ctx,
            pcbdoc,
            physical_layers,
            None,
        )
        layer_hole_masks = self._collect_layer_hole_masks(  # noqa: SLF001
            ctx,
            pcbdoc,
            physical_layers,
            None,
        )
        extra_defs, extra_scene = self._collect_a0_overlays(
            ctx,
            pcbdoc,
            tokens,
            view=view,
            styles=styles,
            source_layers=physical_layers,
        )
        active_layer_ids = self._active_layer_ids(tokens)
        svg_attrs = self._build_svg_document_attrs(ctx, pcbdoc, view.name)  # noqa: SLF001
        svg_attrs.extend(self._canvas_metadata_attrs(ctx, pcbdoc))

        lines = [f"<svg {' '.join(svg_attrs)}>"]
        self._append_svg_metadata(  # noqa: SLF001
            lines,
            ctx,
            view.name,
            active_layer_ids,
            include_board_outline="BOARD_OUTLINE" in tokens,
            pcbdoc=pcbdoc,
        )
        lines.append(f"  <g {' '.join(self._build_scene_attrs(ctx))}>")  # noqa: SLF001
        safe_group_id = html.escape(group_id)
        lines.append(
            f'    <g id="{safe_group_id}" data-pcb-svg-group="view" '
            f'data-pcb-svg-view="{html.escape(view.name)}">'
        )

        defs_lines: list[str] = []
        self._append_svg_defs(  # noqa: SLF001
            defs_lines,
            ctx,
            board_clip_id,
            board_clip_path_d,
            layer_hole_masks,
            extra_defs,
        )
        for line in defs_lines:
            lines.append(f"    {line}")

        for token in tokens:
            lines.extend(
                self._render_a0_token(
                    ctx,
                    pcbdoc,
                    token,
                    styles,
                    source_layers=physical_layers,
                    board_clip_id=board_clip_id,
                    layer_hole_masks=layer_hole_masks,
                )
            )

        if extra_scene:
            lines.extend(f"      {line}" for line in extra_scene)
        lines.append("    </g>")
        lines.append("  </g>")
        lines.append("</svg>")
        return "\n".join(lines)

    def _render_a0_token(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        token: str,
        styles: dict[str, dict[str, object]],
        *,
        source_layers: list[PcbLayer],
        board_clip_id: str,
        layer_hole_masks: dict[int, tuple[str, list[str]]],
    ) -> list[str]:
        if token in _HLR_TOKENS:
            return []
        if token == "BOARD_OUTLINE":
            return self._render_a0_board_outline(ctx, pcbdoc, styles)
        if token == "BOARD_CUTOUTS":
            return self._render_a0_board_cutouts(ctx, pcbdoc, styles)
        if token in _HOLE_TOKENS:
            return self._render_a0_hole_group(
                ctx,
                pcbdoc,
                source_layers=source_layers,
                styles=styles,
                slot=token == "SLOTS",
            )
        if token in _PIN1_TOKENS:
            return self._render_a0_pin1_layer(ctx, pcbdoc, token, styles)
        layer = pcb_svg_physical_layer_from_token(token)
        if layer is None:
            return []
        return self._render_a0_physical_layer(
            ctx,
            pcbdoc,
            layer,
            styles,
            clip_path_id=self._layer_clip_id(board_clip_id, layer),
            mask_id=layer_hole_masks.get(layer.value, (None, []))[0],
        )

    def _layer_clip_id(self, board_clip_id: str, layer: PcbLayer) -> str | None:
        if not board_clip_id:
            return None
        if self.options.clip_all_layers_to_board_outline or layer.is_copper():
            return board_clip_id
        return None

    def _physical_layers_from_tokens(self, tokens: list[str]) -> list[PcbLayer]:
        layers: list[PcbLayer] = []
        for token in tokens:
            if token in PCB_SVG_SPECIAL_LAYERS:
                continue
            layer = pcb_svg_physical_layer_from_token(token)
            if layer is not None and layer not in layers:
                layers.append(layer)
        return layers

    def _active_layer_ids(self, tokens: list[str]) -> list[int]:
        ids: list[int] = []
        synthetic_ids = {
            "BOARD_OUTLINE": PCB_SVG_BOARD_OUTLINE_LAYER_ID,
            "BOARD_CUTOUTS": PCB_SVG_BOARD_CUTOUTS_LAYER_ID,
            "DRILLS": PCB_SVG_DRILLS_LAYER_ID,
            "SLOTS": PCB_SVG_SLOTS_LAYER_ID,
            "ASSEMBLY_HLR_TOP": PCB_SVG_ASSEMBLY_HLR_TOP_LAYER_ID,
            "ASSEMBLY_HLR_BOTTOM": PCB_SVG_ASSEMBLY_HLR_BOTTOM_LAYER_ID,
            "PIN1_TOP": PCB_SVG_PIN1_TOP_LAYER_ID,
            "PIN1_BOTTOM": PCB_SVG_PIN1_BOTTOM_LAYER_ID,
            "ASSEMBLY_DESIGNATORS_TOP": PCB_SVG_ASSEMBLY_DESIGNATORS_TOP_LAYER_ID,
            "ASSEMBLY_DESIGNATORS_BOTTOM": PCB_SVG_ASSEMBLY_DESIGNATORS_BOTTOM_LAYER_ID,
        }
        for token in tokens:
            if token in synthetic_ids:
                ids.append(synthetic_ids[token])
                continue
            layer = pcb_svg_physical_layer_from_token(token)
            if layer is not None:
                ids.append(int(layer.value))
        return sorted(set(ids))

    def _collect_a0_overlays(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        tokens: list[str],
        *,
        view: PcbSvgViewConfig,
        styles: dict[str, dict[str, object]],
        source_layers: list[PcbLayer],
    ) -> tuple[list[str], list[str]]:
        defs: list[str] = []
        scene: list[str] = []
        if "BOARD_CUTOUTS" in tokens and self._cutouts_enabled(styles):
            cutout_style = styles.get("board_cutouts", {})
            if bool(cutout_style.get("hatch", False)):
                defs.extend(
                    self._cutout_hatch_defs(  # noqa: SLF001
                        hatch_spacing_mm=_style_float(
                            styles, "board_cutouts", "hatch_spacing_mm", 2.0
                        ),
                        hatch_angle_deg=_style_float(
                            styles, "board_cutouts", "hatch_angle_deg", 45.0
                        ),
                        hatch_line_width_mm=_style_float(
                            styles, "board_cutouts", "hatch_line_width_mm", 0.08
                        ),
                    )
                )
        for token in tokens:
            if token not in _HLR_TOKENS:
                continue
            overlay_defs, overlay_scene = self._render_a0_hlr(
                ctx,
                pcbdoc,
                token=token,
                view=view,
                styles=styles,
                source_layers=source_layers,
            )
            defs.extend(overlay_defs)
            scene.extend(overlay_scene)
        return defs, scene

    def _render_a0_hlr(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        *,
        token: str,
        view: PcbSvgViewConfig,
        styles: dict[str, dict[str, object]],
        source_layers: list[PcbLayer],
    ) -> tuple[list[str], list[str]]:
        if not _style_enabled(styles, "assembly_hlr"):
            return [], []
        side = "top" if token == "ASSEMBLY_HLR_TOP" else "bottom"
        mode = self._resolved_hlr_projection_mode(view)
        if mode == "none":
            return [], []
        override_modes = self._component_projection_overrides_for_side(pcbdoc, side)
        component_styles = self._component_assembly_hlr_styles_for_side(
            pcbdoc,
            side,
            styles,
        )
        if mode == "bounding_box":
            return self._render_hlr_bounding_box_mode(
                ctx,
                pcbdoc,
                side=side,
                styles=styles,
                override_modes=override_modes,
                component_styles=component_styles,
            )
        options = self._build_hlr_render_options(
            side=side,
            mode=mode,
            styles=styles,
            source_layers=source_layers,
            override_modes=override_modes,
            component_styles=component_styles,
        )
        renderer = CruncherPcbAssemblySvgRenderer(options)
        try:
            defs, scene = renderer._render_overlay_defs_scene(ctx, pcbdoc)  # noqa: SLF001
            scene = self._apply_hlr_component_projection_overrides(
                ctx,
                pcbdoc,
                side,
                scene,
                styles,
                override_modes,
                component_styles,
            )
            return defs, scene
        except Exception as exc:
            log.warning("Skipping %s HLR overlay for %s: %s", side, view.name, exc)
            return [], []

    def _render_hlr_bounding_box_mode(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        *,
        side: str,
        styles: dict[str, dict[str, object]],
        override_modes: dict[str, str],
        component_styles: dict[str, dict[str, object]],
    ) -> tuple[list[str], list[str]]:
        excluded = {
            designator
            for designator, projection in override_modes.items()
            if projection == "none"
        }
        return [], self._render_a0_assembly_bounding_boxes(
            ctx,
            pcbdoc,
            side,
            styles,
            exclude_designators=excluded,
            component_styles=component_styles,
        )

    def _build_hlr_render_options(
        self,
        *,
        side: str,
        mode: str,
        styles: dict[str, dict[str, object]],
        source_layers: list[PcbLayer],
        override_modes: dict[str, str],
        component_styles: dict[str, dict[str, object]],
    ) -> CruncherPcbAssemblySvgRenderOptions:
        style = styles.get("assembly_hlr", {})
        emitted_modes = self._hlr_emitted_modes(mode, override_modes)
        component_projection_options = {
            designator: self._assembly_projection_options_from_style(
                side=side,
                style=component_style,
            )
            for designator, component_style in component_styles.items()
        }
        component_stroke_styles = {
            designator: {
                "color": _style_color(
                    {"assembly_hlr": component_style},
                    "assembly_hlr",
                    "#F59E0B",
                ),
                "line_width_mm": _style_float(
                    {"assembly_hlr": component_style},
                    "assembly_hlr",
                    "line_width_mm",
                    0.12,
                ),
            }
            for designator, component_style in component_styles.items()
        }
        options = CruncherPcbAssemblySvgRenderOptions(
            visible_layers=set(source_layers),
            layer_render_order=source_layers,
            include_metadata=self.options.include_metadata,
            show_board_outline=False,
            mirror_x=False,
            include_assembly_overlay=True,
            assembly_view_side=side,
            assembly_include_simple="simple" in emitted_modes,
            assembly_include_detail="detail" in emitted_modes,
            assembly_curve_mode=str(style.get("curve_mode") or "native_arcs"),
            assembly_projection_algorithm=self._optional_assembly_hlr_str(
                style,
                "projection_algorithm",
            ),
            assembly_samples_per_curve=_style_int(
                styles,
                "assembly_hlr",
                "samples_per_curve",
                24,
            ),
            assembly_round_digits=_style_int(
                styles,
                "assembly_hlr",
                "round_digits",
                3,
            ),
            assembly_mesh_linear_deflection=self._optional_assembly_hlr_float(
                style,
                "mesh_linear_deflection",
            ),
            assembly_mesh_angular_deflection=self._optional_assembly_hlr_float(
                style,
                "mesh_angular_deflection",
            ),
            assembly_mesh_relative=self._optional_assembly_hlr_bool(
                style,
                "mesh_relative",
            ),
            assembly_hlr_angle_tolerance=self._optional_assembly_hlr_float(
                style,
                "hlr_angle_tolerance",
            ),
            assembly_edge_flags={
                key: _style_bool({"assembly_hlr": style}, "assembly_hlr", key, False)
                for key in _ASSEMBLY_HLR_EDGE_FLAG_KEYS
                if key in style
            }
            or None,
            assembly_include_visible=_style_bool(
                {"assembly_hlr": style},
                "assembly_hlr",
                "include_visible",
                True,
            ),
            assembly_include_outline=_style_bool(
                {"assembly_hlr": style},
                "assembly_hlr",
                "include_outline",
                True,
            ),
            assembly_union_polygons=_style_bool(
                {"assembly_hlr": style},
                "assembly_hlr",
                "union_polygons",
                True,
            ),
            assembly_overlay_color=str(style.get("color") or "#F59E0B"),
            assembly_line_width_mm=_style_float(
                {"assembly_hlr": style},
                "assembly_hlr",
                "line_width_mm",
                0.12,
            ),
            assembly_component_projection_options=component_projection_options or None,
            assembly_component_stroke_styles=component_stroke_styles or None,
        )
        return options

    def _assembly_projection_options_from_style(
        self,
        *,
        side: str,
        style: dict[str, object],
    ) -> AssemblyProjectionOptions:
        projection_side = "bottom" if side == "bottom" else "top"
        curve_mode = str(style.get("curve_mode") or "native_arcs").strip().lower()
        if curve_mode not in {"native_arcs", "polyline"}:
            curve_mode = "native_arcs"
        style_table = {"assembly_hlr": style}
        return AssemblyProjectionOptions(
            side=projection_side,
            projection_algorithm=self._optional_assembly_hlr_str(
                style,
                "projection_algorithm",
            ),
            curve_mode="polyline" if curve_mode == "polyline" else "native_arcs",
            samples_per_curve=_style_int(
                style_table,
                "assembly_hlr",
                "samples_per_curve",
                24,
            ),
            round_digits=_style_int(
                style_table,
                "assembly_hlr",
                "round_digits",
                3,
            ),
            include_visible=_style_bool(
                style_table,
                "assembly_hlr",
                "include_visible",
                True,
            ),
            include_outline=_style_bool(
                style_table,
                "assembly_hlr",
                "include_outline",
                True,
            ),
            union_polygons=_style_bool(
                style_table,
                "assembly_hlr",
                "union_polygons",
                True,
            ),
            mesh_linear_deflection=self._optional_assembly_hlr_float(
                style,
                "mesh_linear_deflection",
            ),
            mesh_angular_deflection=self._optional_assembly_hlr_float(
                style,
                "mesh_angular_deflection",
            ),
            mesh_relative=self._optional_assembly_hlr_bool(
                style,
                "mesh_relative",
            ),
            hlr_angle_tolerance=self._optional_assembly_hlr_float(
                style,
                "hlr_angle_tolerance",
            ),
            edge_flags={
                key: _style_bool(style_table, "assembly_hlr", key, False)
                for key in _ASSEMBLY_HLR_EDGE_FLAG_KEYS
                if key in style
            }
            or None,
        )

    @staticmethod
    def _hlr_emitted_modes(mode: str, override_modes: dict[str, str]) -> set[str]:
        emitted_modes = {mode}
        emitted_modes.update(
            projection
            for projection in override_modes.values()
            if projection in {"simple", "detail"}
        )
        return emitted_modes

    @staticmethod
    def _optional_assembly_hlr_str(
        style: dict[str, object],
        key: str,
    ) -> str | None:
        value = style.get(key)
        if value is None:
            return None
        text = str(value).strip()
        return text or None

    @staticmethod
    def _optional_assembly_hlr_float(
        style: dict[str, object],
        key: str,
    ) -> float | None:
        value = style.get(key)
        if value is None:
            return None
        if not isinstance(value, (int, float, str)):
            raise ValueError(f"Invalid pcb-svg assembly_hlr.{key}")
        try:
            return float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid pcb-svg assembly_hlr.{key}") from exc

    @staticmethod
    def _optional_assembly_hlr_bool(
        style: dict[str, object],
        key: str,
    ) -> bool | None:
        if key not in style:
            return None
        return _style_bool({"assembly_hlr": style}, "assembly_hlr", key, False)

    def _resolved_hlr_projection_mode(self, view: PcbSvgViewConfig) -> str:
        mode = str(view.assembly_hlr_mode or "detail").strip().lower()
        if mode == "detail" and self.config.assembly != type(self.config.assembly)():
            return self.config.assembly.default_projection
        return mode

    def _render_a0_assembly_bounding_boxes(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        side: str,
        styles: dict[str, dict[str, object]],
        *,
        include_designators: set[str] | None = None,
        exclude_designators: set[str] | None = None,
        component_styles: dict[str, dict[str, object]] | None = None,
    ) -> list[str]:
        layer = PcbLayer.TOP if side == "top" else PcbLayer.BOTTOM
        color = _style_color(styles, "assembly_hlr", "#F59E0B")
        stroke_width = _style_float(styles, "assembly_hlr", "line_width_mm", 0.12)
        boxes = self._component_pad_bounds_by_side(
            pcbdoc,
            layer,
            include_designators=include_designators,
            exclude_designators=exclude_designators,
        )
        if not boxes:
            return []

        layer_id = (
            PCB_SVG_ASSEMBLY_HLR_TOP_LAYER_ID
            if side == "top"
            else PCB_SVG_ASSEMBLY_HLR_BOTTOM_LAYER_ID
        )
        attrs = [
            f'id="assembly-hlr-bounding-boxes-{side}"',
            'data-projection-mode="bounding_box"',
        ]
        if self.options.include_metadata:
            attrs.extend(
                _synthetic_layer_metadata_attrs(
                    layer_id,
                    key=f"ASSEMBLY_HLR_{side.upper()}",
                    display_name=f"Assembly HLR {side.title()}",
                )
            )

        lines = [f"      <g {' '.join(attrs)}>"]
        for designator, bounds in boxes:
            box_color = color
            box_stroke_width = stroke_width
            component_style = (component_styles or {}).get(designator)
            if component_style:
                component_style_table = {"assembly_hlr": component_style}
                box_color = _style_color(
                    component_style_table,
                    "assembly_hlr",
                    color,
                )
                box_stroke_width = _style_float(
                    component_style_table,
                    "assembly_hlr",
                    "line_width_mm",
                    stroke_width,
                )
            lines.append(
                "        "
                + self._component_bounds_rect_svg(
                    ctx,
                    bounds,
                    color=box_color,
                    stroke_width_mm=box_stroke_width,
                    designator=designator,
                )
            )
        lines.append("      </g>")
        return lines

    def _component_pad_bounds_by_side(
        self,
        pcbdoc: AltiumPcbDoc,
        layer: PcbLayer,
        *,
        include_designators: set[str] | None = None,
        exclude_designators: set[str] | None = None,
    ) -> list[tuple[str, tuple[float, float, float, float]]]:
        result: list[tuple[str, tuple[float, float, float, float]]] = []
        for component_index, component in enumerate(getattr(pcbdoc, "components", []) or []):
            if _component_side(component) != ("top" if layer == PcbLayer.TOP else "bottom"):
                continue
            designator = _component_designator(component)
            if include_designators is not None and designator not in include_designators:
                continue
            if exclude_designators is not None and designator in exclude_designators:
                continue
            pads = self._component_layer_pads(pcbdoc, component_index, layer)
            bounds = self._pad_bounds_mils(pads, layer)
            if bounds is None:
                continue
            result.append((designator, bounds))
        return result

    def _component_projection_overrides_for_side(
        self,
        pcbdoc: AltiumPcbDoc,
        side: str,
    ) -> dict[str, str]:
        result: dict[str, str] = {}
        components = getattr(pcbdoc, "components", []) or []
        sides_by_designator = {
            _component_designator(component): _component_side(component)
            for component in components
            if _component_designator(component)
        }
        for designator, override in self.config.components.items():
            if override.projection is None:
                continue
            override_side = override.side or sides_by_designator.get(designator)
            if override_side == side:
                result[designator] = override.projection
        return result

    def _component_assembly_hlr_styles_for_side(
        self,
        pcbdoc: AltiumPcbDoc,
        side: str,
        styles: dict[str, dict[str, object]],
    ) -> dict[str, dict[str, object]]:
        result: dict[str, dict[str, object]] = {}
        components = getattr(pcbdoc, "components", []) or []
        sides_by_designator = {
            _component_designator(component): _component_side(component)
            for component in components
            if _component_designator(component)
        }
        base_style = dict(styles.get("assembly_hlr", {}))
        for designator, override in self.config.components.items():
            if not override.assembly_hlr:
                continue
            override_side = override.side or sides_by_designator.get(designator)
            if override_side == side:
                merged = dict(base_style)
                merged.update(override.assembly_hlr)
                result[designator] = merged
        return result

    def _apply_hlr_component_projection_overrides(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        side: str,
        scene: list[str],
        styles: dict[str, dict[str, object]],
        overrides: dict[str, str],
        component_styles: dict[str, dict[str, object]],
    ) -> list[str]:
        if not overrides:
            return scene
        filtered = self._filter_hlr_component_scene(scene, overrides)
        bounding_designators = {
            designator
            for designator, projection in overrides.items()
            if projection == "bounding_box"
        }
        if bounding_designators:
            filtered.extend(
                self._render_a0_assembly_bounding_boxes(
                    ctx,
                    pcbdoc,
                    side,
                    styles,
                    include_designators=bounding_designators,
                    component_styles=component_styles,
                )
            )
        return filtered

    def _filter_hlr_component_scene(
        self,
        scene: list[str],
        overrides: dict[str, str],
    ) -> list[str]:
        filtered: list[str] = []
        active_projection: str | None = None
        skip_component_depth = 0
        for line in scene:
            if skip_component_depth > 0:
                skip_component_depth += line.count("<g ")
                skip_component_depth -= line.count("</g>")
                continue
            projection = self._override_projection_for_hlr_line(line, overrides)
            if projection in {"none", "bounding_box"}:
                skip_component_depth = max(line.count("<g ") - line.count("</g>"), 1)
                continue
            if projection in {"simple", "detail"}:
                active_projection = projection
            elif line.startswith("    </g>"):
                active_projection = None
            if (
                active_projection in {"simple", "detail"}
                and 'data-assembly-mode="' in line
                and f'data-assembly-mode="{active_projection}"' not in line
            ):
                continue
            filtered.append(line)
        return filtered

    def _override_projection_for_hlr_line(
        self,
        line: str,
        overrides: dict[str, str],
    ) -> str | None:
        for designator, projection in overrides.items():
            escaped = html.escape(designator)
            token = _safe_svg_id(designator)
            if f'data-component="{escaped}"' in line or f"assembly-comp-{token}-" in line:
                return projection
        return None

    def _component_layer_pads(
        self,
        pcbdoc: AltiumPcbDoc,
        component_index: int,
        layer: PcbLayer,
    ) -> list[object]:
        return [
            pad
            for pad in getattr(pcbdoc, "pads", []) or []
            if getattr(pad, "component_index", None) == component_index
            and _pad_renders_on_layer(pad, layer)
        ]

    def _pad_bounds_mils(
        self,
        pads: list[object],
        layer: PcbLayer,
    ) -> tuple[float, float, float, float] | None:
        bounds: list[tuple[float, float, float, float]] = []
        for pad in pads:
            x_mils, y_mils = _pad_center_mils(pad)
            width_mils, height_mils = _pad_size_mils(pad, layer)
            half_width = max(width_mils, 1.0) / 2.0
            half_height = max(height_mils, 1.0) / 2.0
            rotation = math.radians(_object_float(getattr(pad, "rotation", 0.0)))
            cos_v = abs(math.cos(rotation))
            sin_v = abs(math.sin(rotation))
            rotated_half_width = half_width * cos_v + half_height * sin_v
            rotated_half_height = half_width * sin_v + half_height * cos_v
            bounds.append(
                (
                    x_mils - rotated_half_width,
                    y_mils - rotated_half_height,
                    x_mils + rotated_half_width,
                    y_mils + rotated_half_height,
                )
            )
        if not bounds:
            return None
        return (
            min(item[0] for item in bounds),
            min(item[1] for item in bounds),
            max(item[2] for item in bounds),
            max(item[3] for item in bounds),
        )

    def _component_bounds_rect_svg(
        self,
        ctx: PcbSvgRenderContext,
        bounds: tuple[float, float, float, float],
        *,
        color: str,
        stroke_width_mm: float,
        designator: str,
    ) -> str:
        left, bottom, right, top = bounds
        x_svg = ctx.x_to_svg(left)
        y_svg = ctx.y_to_svg(top)
        width = max((right - left) * _MIL_TO_MM, 0.01)
        height = max((top - bottom) * _MIL_TO_MM, 0.01)
        return (
            f'<rect x="{ctx.fmt(x_svg)}" y="{ctx.fmt(y_svg)}" '
            f'width="{ctx.fmt(width)}" height="{ctx.fmt(height)}" '
            'fill="none" '
            f'stroke="{html.escape(color)}" '
            f'stroke-width="{ctx.fmt(stroke_width_mm)}" '
            f'data-component-designator="{html.escape(designator)}" '
            'data-feature="assembly-bounding-box"/>'
        )

    def _render_a0_pin1_layer(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        token: str,
        styles: dict[str, dict[str, object]],
    ) -> list[str]:
        if not _style_enabled(styles, "pin1_marker"):
            return []
        layer = PcbLayer.TOP if token == "PIN1_TOP" else PcbLayer.BOTTOM
        side = "top" if layer == PcbLayer.TOP else "bottom"
        marker_elements = self._pin1_marker_elements(ctx, pcbdoc, layer, styles)
        if not marker_elements and not self.options.show_empty_layers:
            return []

        layer_id = PCB_SVG_PIN1_TOP_LAYER_ID if token == "PIN1_TOP" else PCB_SVG_PIN1_BOTTOM_LAYER_ID
        attrs = [f'id="pin1-markers-{side}"']
        if self.options.include_metadata:
            attrs.extend(
                _synthetic_layer_metadata_attrs(
                    layer_id,
                    key=token,
                    display_name=f"Pin 1 {side.title()}",
                )
            )
            attrs.append(f'data-primitive-count="{len(marker_elements)}"')

        lines = [f"      <g {' '.join(attrs)}>"]
        lines.extend(f"        {element}" for element in marker_elements)
        lines.append("      </g>")
        return lines

    def _pin1_marker_elements(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        layer: PcbLayer,
        styles: dict[str, dict[str, object]],
    ) -> list[str]:
        side = "top" if layer == PcbLayer.TOP else "bottom"
        marker_elements: list[str] = []
        for component_index, component in enumerate(getattr(pcbdoc, "components", []) or []):
            if _component_side(component) != side:
                continue
            designator = _component_designator(component)
            if not self._pin1_component_enabled(designator):
                continue
            if self._component_pad_designator_count(pcbdoc, component_index) <= 1:
                continue
            pad = self._pin1_pad_for_component(pcbdoc, component_index, component, layer)
            if pad is not None:
                marker_elements.extend(
                    self._pin1_marker_svg(ctx, component, pad, layer, styles)
                )
        return marker_elements

    def _pin1_component_enabled(self, designator: str) -> bool:
        override = self.config.components.get(designator)
        if override is not None and override.pin1_enabled is not None:
            return bool(override.pin1_enabled)
        return not self._pin1_designator_excluded(designator)

    def _pin1_designator_excluded(self, designator: str) -> bool:
        prefix = _reference_designator_prefix(designator)
        if not prefix:
            return False
        excluded = {
            str(item or "").strip().upper()
            for item in self.config.pin1.exclude_designator_prefixes
            if str(item or "").strip()
        }
        return prefix in excluded

    def _component_pad_designator_count(
        self,
        pcbdoc: AltiumPcbDoc,
        component_index: int,
    ) -> int:
        designators = {
            str(getattr(pad, "designator", "") or "").strip().upper()
            for pad in getattr(pcbdoc, "pads", []) or []
            if getattr(pad, "component_index", None) == component_index
            and str(getattr(pad, "designator", "") or "").strip()
        }
        return len(designators)

    def _pin1_pad_for_component(
        self,
        pcbdoc: AltiumPcbDoc,
        component_index: int,
        component: object,
        layer: PcbLayer,
    ) -> object | None:
        pads = self._component_layer_pads(pcbdoc, component_index, layer)
        if not pads:
            return None

        override = self.config.components.get(_component_designator(component))
        selected = choose_pin1_pad_designator(
            [
                str(getattr(pad, "designator", "") or "").strip()
                for pad in pads
                if str(getattr(pad, "designator", "") or "").strip()
            ],
            override=override.pin1_pad if override is not None else None,
        )
        if selected is None:
            return None
        by_designator = {
            str(getattr(pad, "designator", "") or "").strip().upper(): pad for pad in pads
        }
        return by_designator.get(selected.upper())

    def _pin1_marker_svg(
        self,
        ctx: PcbSvgRenderContext,
        component: object,
        pad: object,
        layer: PcbLayer,
        styles: dict[str, dict[str, object]],
    ) -> list[str]:
        designator = _component_designator(component)
        pad_designator = str(getattr(pad, "designator", "") or "").strip()
        color = _style_color(styles, "pin1_marker", "#2563EB")
        group_attrs = [
            f'id="pin1-{_safe_svg_id(designator or "component")}-{_safe_svg_id(pad_designator or "pad")}"',
            'data-feature="pin1-marker"',
            f'data-component-designator="{html.escape(designator)}"',
            f'data-pad-designator="{html.escape(pad_designator)}"',
        ]

        should_fill_pad = _pad_has_hole(pad) or is_grid_pad_designator(pad_designator)
        if should_fill_pad:
            to_svg = getattr(pad, "to_svg", None)
            rendered: list[str] = []
            render_holes = _pad_has_hole(pad)
            if callable(to_svg):
                raw_rendered = to_svg(
                    ctx,
                    stroke=color,
                    include_metadata=self.options.include_metadata,
                    for_layer=layer,
                    render_holes=render_holes,
                )
                if isinstance(raw_rendered, (list, tuple)):
                    rendered = [str(element) for element in raw_rendered]
            if rendered:
                return [f"<g {' '.join(group_attrs)}>"] + [
                    f"  {element}" for element in rendered
                ] + ["</g>"]

        x_mils, y_mils = _pad_center_mils(pad)
        width_mils, height_mils = _pad_size_mils(pad, layer)
        max_dot_mm = max(min(width_mils, height_mils) * _MIL_TO_MM * 0.80, 0.01)
        requested_dot_mm = _style_float(styles, "pin1_marker", "dot_diameter_mm", 0.55)
        min_dot_mm = _style_float(styles, "pin1_marker", "min_dot_diameter_mm", 0.25)
        dot_diameter_mm = max(min(requested_dot_mm, max_dot_mm), min_dot_mm)
        cx = ctx.x_to_svg(x_mils)
        cy = ctx.y_to_svg(y_mils)
        return [
            (
                f'<circle cx="{ctx.fmt(cx)}" cy="{ctx.fmt(cy)}" '
                f'r="{ctx.fmt(dot_diameter_mm / 2.0)}" '
                f'fill="{html.escape(color)}" stroke="none" {" ".join(group_attrs)}/>'
            )
        ]

    def _render_a0_board_outline(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        styles: dict[str, dict[str, object]],
    ) -> list[str]:
        if not _style_enabled(styles, "board_outline"):
            return []
        outline = getattr(getattr(pcbdoc, "board", None), "outline", None)
        vertices = getattr(outline, "vertices", None)
        if not vertices:
            return []
        path_d = self._path_from_vertices(ctx, vertices)  # noqa: SLF001
        if not path_d:
            return []
        attrs = [
            f'd="{path_d}"',
            'fill="none"',
            f'stroke="{html.escape(_style_color(styles, "board_outline", "#000000"))}"',
            f'stroke-width="{ctx.fmt(_style_float(styles, "board_outline", "line_width_mm", 0.10))}"',
            'stroke-linejoin="round"',
            'vector-effect="non-scaling-stroke"',
        ]
        if self.options.include_metadata:
            attrs.extend(
                [
                    'data-feature="board-outline"',
                    'data-element-key="board-outline"',
                ]
            )
        return [
            '      <g id="board-outline">',
            "        " + f"<path {' '.join(attrs)}/>",
            "      </g>",
        ]

    def _cutouts_enabled(self, styles: dict[str, dict[str, object]]) -> bool:
        return _style_enabled(styles, "board_cutouts")

    def _render_a0_board_cutouts(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        styles: dict[str, dict[str, object]],
    ) -> list[str]:
        if not self._cutouts_enabled(styles):
            return []
        outline = getattr(getattr(pcbdoc, "board", None), "outline", None)
        cutouts = list(getattr(outline, "cutouts", []) or [])
        if not cutouts:
            return []
        return [
            f"      {line}"
            for line in self._render_cutout_paths(  # noqa: SLF001
                ctx,
                cutouts,
                include_hatch=_style_bool(styles, "board_cutouts", "hatch", True),
                include_label=False,
                label_text="",
                outline_style=str(
                    styles.get("board_cutouts", {}).get("outline_style") or "solid"
                ),
                outline_dash_mm=_style_float(
                    styles, "board_cutouts", "outline_dash_mm", 1.5
                ),
                outline_width_mm=_style_float(
                    styles, "board_cutouts", "outline_width_mm", 0.15
                ),
            )
        ]

    def _render_a0_physical_layer(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        layer: PcbLayer,
        styles: dict[str, dict[str, object]],
        *,
        clip_path_id: str | None,
        mask_id: str | None,
    ) -> list[str]:
        if layer.is_copper():
            primitives = self._a0_copper_primitives(ctx, pcbdoc, layer, styles)
            color = _style_color(styles, "copper_traces", ctx.layer_color(layer))
        elif layer.is_overlay():
            primitives = self._a0_silkscreen_primitives(ctx, pcbdoc, layer, styles)
            color = _style_color(
                styles, "silkscreen_component_graphics", ctx.layer_color(layer)
            )
        elif layer == PcbLayer.KEEPOUT:
            primitives = (
                self._render_layer_primitives_default(
                    ctx, pcbdoc, layer, _style_color(styles, "keepout", "#CC00CC")
                )
                if _style_enabled(styles, "keepout")
                else []
            )
            color = _style_color(styles, "keepout", "#CC00CC")
        else:
            primitives = self._render_layer_primitives_default(
                ctx, pcbdoc, layer, ctx.layer_color(layer)
            )
            color = ctx.layer_color(layer)

        if not primitives and not self.options.show_empty_layers:
            return []
        return self._render_layer_group_from_primitives(  # noqa: SLF001
            ctx,
            layer,
            color,
            primitives,
            [],
            clip_path_id=clip_path_id,
            mask_id=mask_id,
        )

    def _a0_copper_primitives(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        layer: PcbLayer,
        styles: dict[str, dict[str, object]],
    ) -> list[str]:
        primitives: list[str] = []
        if _style_enabled(styles, "copper_traces"):
            trace_color = _style_color(styles, "copper_traces", ctx.layer_color(layer))
            primitives.extend(self._render_tracks_for_layer(ctx, pcbdoc, layer, trace_color))  # noqa: SLF001
            primitives.extend(self._render_arcs_for_layer(ctx, pcbdoc, layer, trace_color))  # noqa: SLF001
        if _style_enabled(styles, "vias"):
            primitives.extend(
                self._render_vias_for_layer(
                    ctx,
                    pcbdoc,
                    layer,
                    _style_color(styles, "vias", ctx.layer_color(layer)),
                )
            )
        if _style_enabled(styles, "copper_polygons"):
            polygon_color = _style_color(styles, "copper_polygons", ctx.layer_color(layer))
            primitives.extend(self._render_fills_for_layer(ctx, pcbdoc, layer, polygon_color))  # noqa: SLF001
            primitives.extend(self._render_regions_for_layer(ctx, pcbdoc, layer, polygon_color))  # noqa: SLF001
        primitives.extend(self._render_a0_pads(ctx, pcbdoc, layer, styles))
        return primitives

    def _render_a0_pads(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        layer: PcbLayer,
        styles: dict[str, dict[str, object]],
    ) -> list[str]:
        primitives: list[str] = []
        if _style_enabled(styles, "smd_pads"):
            smd_pads: list[object] = [
                pad for pad in pcbdoc.pads if not _pad_has_hole(pad)
            ]
            primitives.extend(
                self._render_primitive_collection(  # noqa: SLF001
                    ctx,
                    smd_pads,
                    layer,
                    _style_color(styles, "smd_pads", ctx.layer_color(layer)),
                    render_holes=False,
                )
            )
        if _style_enabled(styles, "through_hole_pads"):
            through_pads: list[object] = [
                pad for pad in pcbdoc.pads if _pad_has_hole(pad)
            ]
            primitives.extend(
                self._render_primitive_collection(  # noqa: SLF001
                    ctx,
                    through_pads,
                    layer,
                    _style_color(styles, "through_hole_pads", ctx.layer_color(layer)),
                    render_holes=False,
                )
            )
        return primitives

    def _a0_silkscreen_primitives(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        layer: PcbLayer,
        styles: dict[str, dict[str, object]],
    ) -> list[str]:
        primitives: list[str] = []
        graphics_collections = (
            pcbdoc.regions,
            pcbdoc.shapebased_regions,
            pcbdoc.fills,
            pcbdoc.pads,
            pcbdoc.vias,
            pcbdoc.tracks,
            pcbdoc.arcs,
        )
        if _style_enabled(styles, "silkscreen_component_graphics"):
            comp_graphics: list[object] = []
            for collection in graphics_collections:
                comp_graphics.extend(item for item in collection if _is_component_linked(item))
            primitives.extend(
                self._render_primitive_collection(  # noqa: SLF001
                    ctx,
                    comp_graphics,
                    layer,
                    _style_color(
                        styles,
                        "silkscreen_component_graphics",
                        ctx.layer_color(layer),
                    ),
                )
            )
        if _style_enabled(styles, "silkscreen_board_graphics"):
            board_graphics: list[object] = []
            for collection in graphics_collections:
                board_graphics.extend(
                    item for item in collection if not _is_component_linked(item)
                )
            primitives.extend(
                self._render_primitive_collection(  # noqa: SLF001
                    ctx,
                    board_graphics,
                    layer,
                    _style_color(styles, "silkscreen_board_graphics", ctx.layer_color(layer)),
                )
            )
        primitives.extend(self._render_a0_silkscreen_texts(ctx, pcbdoc, layer, styles))
        return primitives

    def _render_a0_silkscreen_texts(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        layer: PcbLayer,
        styles: dict[str, dict[str, object]],
    ) -> list[str]:
        tt_renderer, stroke_renderer, barcode_renderer = self._text_renderers()  # noqa: SLF001
        font_resolver = self._embedded_font_resolver(pcbdoc)  # noqa: SLF001
        texts = [
            text
            for text in pcbdoc.texts
            if self._should_render_component_linked_text(pcbdoc, text)  # noqa: SLF001
        ]
        groups: list[tuple[str, list[object]]] = [
            (
                "silkscreen_designators",
                [
                    text
                    for text in texts
                    if _is_component_linked(text) and bool(getattr(text, "is_designator", False))
                ],
            ),
            (
                "silkscreen_component_graphics",
                [
                    text
                    for text in texts
                    if _is_component_linked(text)
                    and not bool(getattr(text, "is_designator", False))
                ],
            ),
            (
                "silkscreen_board_graphics",
                [text for text in texts if not _is_component_linked(text)],
            ),
        ]
        rendered: list[str] = []
        for style_name, items in groups:
            if not items or not _style_enabled(styles, style_name):
                continue
            rendered.extend(
                self._render_primitive_collection(  # noqa: SLF001
                    ctx,
                    items,
                    layer,
                    _style_color(styles, style_name, ctx.layer_color(layer)),
                    text_as_polygons=self.options.text_as_polygons,
                    truetype_renderer=tt_renderer,
                    stroke_renderer=stroke_renderer,
                    barcode_renderer=barcode_renderer,
                    font_resolver=font_resolver,
                )
            )
        return rendered

    def _render_layer_primitives_default(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        layer: PcbLayer,
        color: str,
    ) -> list[str]:
        primitives: list[str] = []
        primitives.extend(self._render_tracks_for_layer(ctx, pcbdoc, layer, color))  # noqa: SLF001
        primitives.extend(self._render_arcs_for_layer(ctx, pcbdoc, layer, color))  # noqa: SLF001
        primitives.extend(self._render_vias_for_layer(ctx, pcbdoc, layer, color))  # noqa: SLF001
        primitives.extend(self._render_fills_for_layer(ctx, pcbdoc, layer, color))  # noqa: SLF001
        primitives.extend(self._render_regions_for_layer(ctx, pcbdoc, layer, color))  # noqa: SLF001
        primitives.extend(self._render_pads_for_layer(ctx, pcbdoc, layer, color))  # noqa: SLF001
        primitives.extend(self._render_texts_for_layer(ctx, pcbdoc, layer, color))  # noqa: SLF001
        return primitives

    def _render_a0_hole_group(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        *,
        source_layers: list[PcbLayer],
        styles: dict[str, dict[str, object]],
        slot: bool,
    ) -> list[str]:
        style_name = "slots" if slot else "drills"
        if not _style_enabled(styles, style_name):
            return []
        copper_layers = [layer for layer in source_layers if layer.is_copper()]
        elements: list[str] = []
        for layer in copper_layers:
            elements.extend(
                self._collect_a0_pad_holes(ctx, pcbdoc, layer, styles, slot=slot)
            )
            if not slot:
                elements.extend(self._collect_a0_via_holes(ctx, pcbdoc, layer, styles))
        if not elements:
            return []
        layer_id = PCB_SVG_SLOTS_LAYER_ID if slot else PCB_SVG_DRILLS_LAYER_ID
        layer_key = "SLOTS" if slot else "DRILLS"
        attrs = [f'id="layer-{layer_key}"']
        if self.options.include_metadata:
            attrs.extend(
                [
                    f'data-layer-id="{layer_id}"',
                    f'data-layer-key="{layer_key}"',
                    f'data-layer-name="{layer_key}"',
                    f'data-layer-display-name="{layer_key.title()}"',
                    f'data-primitive-count="{len(elements)}"',
                    'data-layer-origin="synthetic-hole-aggregate"',
                ]
            )
        lines = [f"      <g {' '.join(attrs)}>"]
        lines.extend(f"        {element}" for element in elements)
        lines.append("      </g>")
        return lines

    def _collect_a0_pad_holes(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        layer: PcbLayer,
        styles: dict[str, dict[str, object]],
        *,
        slot: bool,
    ) -> list[str]:
        style_name = "slots" if slot else "drills"
        opacity = max(0.0, min(1.0, _style_float(styles, style_name, "opacity", 1.0)))
        elements: list[str] = []
        for pad in pcbdoc.pads:
            if self._should_skip_primitive_for_svg(pad):  # noqa: SLF001
                continue
            if not _pad_has_hole(pad) or _pad_is_slot(pad) != slot:
                continue
            if not pad._should_render_on_layer(layer):  # noqa: SLF001
                continue
            color = _style_plating_color(
                styles,
                style_name,
                plated=bool(getattr(pad, "is_plated", True)),
            )
            elements.extend(
                pad._hole_knockout_svg_elements(  # noqa: SLF001
                    ctx,
                    layer,
                    include_metadata=self.options.include_metadata,
                    hole_color=color,
                    hole_opacity=opacity,
                    hole_outline=False,
                    hole_outline_width_mm=0.10,
                )
            )
        return elements

    def _collect_a0_via_holes(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        layer: PcbLayer,
        styles: dict[str, dict[str, object]],
    ) -> list[str]:
        opacity = max(0.0, min(1.0, _style_float(styles, "drills", "opacity", 1.0)))
        elements: list[str] = []
        for via in pcbdoc.vias:
            if self._should_skip_primitive_for_svg(via):  # noqa: SLF001
                continue
            if not via._spans_layer(layer):  # noqa: SLF001
                continue
            if not should_render_via_drill_hole(via):
                continue
            hole_radius_mm = max(via.hole_size_mils * _MIL_TO_MM / 2.0, 0.0)
            if hole_radius_mm <= 0:
                continue
            plated = bool(getattr(via, "is_plated", True))
            color = _style_plating_color(styles, "drills", plated=plated)
            attrs = [
                f'cx="{ctx.fmt(ctx.x_to_svg(via.x_mils))}"',
                f'cy="{ctx.fmt(ctx.y_to_svg(via.y_mils))}"',
                f'r="{ctx.fmt(hole_radius_mm)}"',
                f'fill="{html.escape(color)}"',
            ]
            if opacity < 1.0:
                attrs.append(f'fill-opacity="{ctx.fmt(opacity)}"')
            if self.options.include_metadata:
                attrs.extend(
                    [
                        'data-primitive="via-hole"',
                        'data-hole-owner="via"',
                        'data-hole-kind="round"',
                        f'data-hole-plating="{"plated" if plated else "non-plated"}"',
                        'data-hole-render="fill"',
                    ]
                )
                attrs.extend(ctx.layer_metadata_attrs(layer.value))
                attrs.extend(
                    ctx.relationship_metadata_attrs(
                        net_index=getattr(via, "net_index", None),
                    )
                )
                hole_id_attr = ctx.primitive_id_attr(
                    "via",
                    via,
                    layer_id=layer.value,
                    role="hole",
                )
                if hole_id_attr:
                    attrs.append(hole_id_attr)
            elements.append(f"<circle {' '.join(attrs)}/>")
        return elements


def _extract_svg_group(svg_text: str, group_id: str) -> ET.Element:
    root = ET.fromstring(svg_text)
    result = _find_element_by_id(root, group_id)
    if result is None:
        raise ValueError(f"Generated SVG does not contain expected group id {group_id!r}")
    return result


def _find_element_by_id(root: ET.Element, group_id: str) -> ET.Element | None:
    for elem in root.iter():
        if elem.attrib.get("id") == group_id:
            return elem
    return None


def _is_svg_group(elem: ET.Element) -> bool:
    return elem.tag in {"g", f"{{{_SVG_NS}}}g"}


def _is_legacy_generated_view_artifact(elem: ET.Element) -> bool:
    if elem.attrib.get("data-feature") == "board-cutout-label":
        return True
    if not _is_svg_group(elem):
        return False
    return elem.attrib.get("data-layer-key") is not None or elem.attrib.get("id") == "board-outline"


def _remove_legacy_generated_view_artifacts(root: ET.Element, protected_group_id: str) -> None:
    protected_group = _find_element_by_id(root, protected_group_id)
    protected_descendant_ids = (
        {id(elem) for elem in protected_group.iter()} if protected_group is not None else set()
    )
    parent_map = {child: parent for parent in root.iter() for child in parent}
    removals: list[tuple[ET.Element, ET.Element]] = []
    for elem in root.iter():
        if id(elem) in protected_descendant_ids:
            continue
        if _is_legacy_generated_view_artifact(elem):
            parent = parent_map.get(elem)
            if parent is not None:
                removals.append((parent, elem))
    for parent, elem in removals:
        try:
            parent.remove(elem)
        except ValueError:
            continue


def _replace_generated_metadata(existing_root: ET.Element, new_root: ET.Element) -> None:
    new_metadata = _find_element_by_id(new_root, SVG_ENRICHMENT_METADATA_ID)
    old_metadata = _find_element_by_id(existing_root, SVG_ENRICHMENT_METADATA_ID)
    parent_map = {child: parent for parent in existing_root.iter() for child in parent}
    if new_metadata is None:
        if old_metadata is not None:
            parent = parent_map.get(old_metadata)
            if parent is not None:
                parent.remove(old_metadata)
        return
    if old_metadata is None:
        existing_root.insert(0, new_metadata)
        return
    parent = parent_map.get(old_metadata)
    if parent is None:
        return
    index = list(parent).index(old_metadata)
    parent.remove(old_metadata)
    parent.insert(index, new_metadata)


def _replace_group_in_svg(existing_svg: str, new_svg: str, group_id: str) -> str:
    ET.register_namespace("", _SVG_NS)
    existing_root = ET.fromstring(existing_svg)
    new_root = ET.fromstring(new_svg)
    new_group = _find_element_by_id(new_root, group_id)
    if new_group is None:
        raise ValueError(f"Generated SVG does not contain expected group id {group_id!r}")
    old_group = _find_element_by_id(existing_root, group_id)
    if old_group is None:
        raise ValueError(f"Existing SVG does not contain durable group {group_id!r}")
    else:
        existing_root.attrib.clear()
        existing_root.attrib.update(new_root.attrib)
        _replace_generated_metadata(existing_root, new_root)
        _remove_legacy_generated_view_artifacts(existing_root, group_id)
        parent_map = {child: parent for parent in existing_root.iter() for child in parent}
        parent = parent_map.get(old_group)
        if parent is None:
            raise ValueError(f"Existing SVG group {group_id!r} has no parent")
        index = list(parent).index(old_group)
        parent.remove(old_group)
        parent.insert(index, new_group)
    return ET.tostring(existing_root, encoding="unicode")


def write_or_update_view_svg(path: Path, svg_text: str, *, group_id: str) -> None:
    """Write a new SVG or replace an existing durable view group."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        try:
            updated = _replace_group_in_svg(path.read_text(encoding="utf-8"), svg_text, group_id)
            path.write_text(updated, encoding="utf-8")
            return
        except Exception as exc:
            log.warning("Replacing whole SVG after group update failed for %s: %s", path, exc)
    path.write_text(svg_text, encoding="utf-8")


def _auto_layer_tokens(renderer: PcbSvgA0Renderer, pcbdoc: AltiumPcbDoc) -> list[str]:
    layers = renderer._collect_visible_layers(pcbdoc)  # noqa: SLF001
    return [layer.to_json_name() for layer in layers]


def _layer_output_tokens(
    config: PcbSvgConfig,
    renderer: PcbSvgA0Renderer,
    pcbdoc: AltiumPcbDoc,
) -> list[str]:
    configured = config.layer_outputs.get("layers", "auto")
    if configured == "auto":
        return _auto_layer_tokens(renderer, pcbdoc)
    if not isinstance(configured, list):
        return []
    return [str(token) for token in configured]


def _layer_output_special_tokens(config: PcbSvgConfig) -> list[str]:
    raw_include_special = config.layer_outputs.get("include_special_layers", [])
    if not isinstance(raw_include_special, list):
        return []
    return [str(token) for token in raw_include_special]


def _render_a0_layer_outputs(
    config: PcbSvgConfig,
    renderer: PcbSvgA0Renderer,
    render_input: CruncherPcbRenderInput,
    *,
    output_dir: Path,
    board_name: str,
    layer_manifest: dict[str, object],
) -> int:
    if not bool(config.layer_outputs.get("enabled", True)):
        return 0

    layer_dir = output_dir / str(config.layer_outputs.get("output_dir") or "layers")
    include_special = _layer_output_special_tokens(config)
    written = 0
    for layer_token in _layer_output_tokens(config, renderer, render_input.pcbdoc):
        group_id = f"pcb-svg-layer-{_safe_svg_id(layer_token.lower())}"
        view = PcbSvgViewConfig(
            name=f"layer_{layer_token}",
            group_id=group_id,
            layers=[layer_token, *include_special],
            mirror=False,
        )
        styles = config.resolved_styles_for_view(view)
        svg_text = renderer.render_view_svg(
            render_input.pcbdoc,
            view,
            project_parameters=render_input.project_parameters,
            layers=view.layers,
            group_id=group_id,
            mirror=False,
            styles=styles,
        )
        layer_path = layer_dir / f"{board_name}__{layer_token}.svg"
        layer_path.parent.mkdir(parents=True, exist_ok=True)
        layer_path.write_text(svg_text, encoding="utf-8")
        layer_manifest[layer_token] = {
            "file": str(layer_path.relative_to(output_dir)).replace("\\", "/"),
            "layers": view.layers,
            "group_id": group_id,
        }
        written += 1
    return written


def _view_mirror(config: PcbSvgConfig, view: PcbSvgViewConfig) -> bool:
    if view.mirror is not None:
        return bool(view.mirror)
    return bool(
        config.global_options.mirror_bottom_view
        and any("BOTTOM" in token for token in view.layers)
    )


def _render_a0_configured_views(
    config: PcbSvgConfig,
    renderer: PcbSvgA0Renderer,
    render_input: CruncherPcbRenderInput,
    *,
    output_dir: Path,
    board_name: str,
    view_manifest: dict[str, object],
) -> int:
    written = 0
    for view in config.enabled_views():
        styles = config.resolved_styles_for_view(view)
        mirror = _view_mirror(config, view)
        group_id = view.resolved_group_id()
        svg_text = renderer.render_view_svg(
            render_input.pcbdoc,
            view,
            project_parameters=render_input.project_parameters,
            layers=view.layers,
            group_id=group_id,
            mirror=mirror,
            styles=styles,
        )
        view_path = resolve_config_output_path(
            output_dir,
            view.resolved_output_svg(),
            board=board_name,
            view=view.name,
        )
        write_or_update_view_svg(view_path, svg_text, group_id=group_id)
        view_manifest[view.name] = {
            "file": str(view_path.relative_to(output_dir)).replace("\\", "/"),
            "group_id": group_id,
            "layers": view.layers,
            "mirrored": mirror,
            "assembly_hlr_mode": view.assembly_hlr_mode,
        }
        written += 1
    return written


def _render_a0_board_outputs(
    config: PcbSvgConfig,
    render_input: CruncherPcbRenderInput,
    *,
    input_file: Path,
    output_dir: Path,
) -> int:
    renderer = PcbSvgA0Renderer(config)
    board_name = render_input.board_key
    layer_manifest: dict[str, object] = {}
    view_manifest: dict[str, object] = {}
    manifest: dict[str, object] = {
        "schema": "pcb.svg.manifest.a0",
        "board": board_name,
        "source_input": input_file.name,
        "layer_outputs": layer_manifest,
        "views": view_manifest,
    }

    written = _render_a0_layer_outputs(
        config,
        renderer,
        render_input,
        output_dir=output_dir,
        board_name=board_name,
        layer_manifest=layer_manifest,
    )
    written += _render_a0_configured_views(
        config,
        renderer,
        render_input,
        output_dir=output_dir,
        board_name=board_name,
        view_manifest=view_manifest,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / f"{board_name}__views.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    log.info("Rendered PCB SVG A0 outputs for %s into %s", board_name, output_dir)
    return written + 1


def render_pcb_svg_a0_to_output(
    args: object,
    input_files: list[Path],
    output_dir: Path,
    config_by_input: dict[Path, PcbSvgConfig],
) -> int:
    """Render all configured A0 PCB SVG layer outputs and views."""
    del args
    total_written = 0
    for input_file in input_files:
        resolved_input = input_file.resolve()
        config = config_by_input.get(resolved_input)
        if config is None:
            log.error("No pcb-svg config resolved for input: %s", resolved_input)
            return 1
        try:
            design, design_source = load_design_for_pcb_input(input_file)
        except Exception as exc:
            log.error("Error loading design context for %s: %s", input_file.name, exc)
            return 1
        if input_file.suffix.lower() == ".pcbdoc":
            log.info("pcb-svg design context for %s: %s", input_file.name, design_source)

        for render_input in iter_pcb_render_inputs(
            design,
            pcbdoc_selector=config.global_options.pcbdoc,
        ):
            total_written += _render_a0_board_outputs(
                config,
                render_input,
                input_file=input_file,
                output_dir=output_dir,
            )

    log.info("Successfully generated %s PCB SVG artifact file(s)", total_written)
    return 0


__all__ = [
    "PcbSvgA0Renderer",
    "render_pcb_svg_a0_to_output",
    "write_or_update_view_svg",
]
