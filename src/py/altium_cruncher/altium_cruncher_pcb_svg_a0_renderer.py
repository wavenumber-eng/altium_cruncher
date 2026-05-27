"""Explicit A0 PCB SVG compositor."""

from __future__ import annotations

import html
import json
import logging
import xml.etree.ElementTree as ET
from dataclasses import replace
from pathlib import Path
from typing import TYPE_CHECKING

from altium_monkey.altium_pcb_svg_renderer import (
    _MIL_TO_MM,
    PcbSvgRenderContext,
    PcbSvgRenderOptions,
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
from altium_cruncher.altium_cruncher_pcb_svg_cutout_layer import (
    CruncherPcbCutoutLayerRenderer,
    PCB_SVG_BOARD_CUTOUTS_LAYER_ID,
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

_HLR_TOKENS = {"ASSEMBLY_HLR_TOP", "ASSEMBLY_HLR_BOTTOM"}
_HOLE_TOKENS = {"DRILLS", "SLOTS"}
_SVG_NS = "http://www.w3.org/2000/svg"


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
        mode = view.assembly_hlr_mode
        style = styles.get("assembly_hlr", {})
        options = CruncherPcbAssemblySvgRenderOptions(
            visible_layers=set(source_layers),
            layer_render_order=source_layers,
            include_metadata=self.options.include_metadata,
            show_board_outline=False,
            mirror_x=False,
            include_assembly_overlay=True,
            assembly_view_side=side,
            assembly_include_simple=mode == "simple",
            assembly_include_detail=mode == "detail",
            assembly_curve_mode=str(style.get("curve_mode") or "native_arcs"),
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
            assembly_include_visible=bool(style.get("include_visible", True)),
            assembly_include_outline=bool(style.get("include_outline", True)),
            assembly_union_polygons=bool(style.get("union_polygons", True)),
            assembly_overlay_color=str(style.get("color") or "#F59E0B"),
        )
        renderer = CruncherPcbAssemblySvgRenderer(options)
        try:
            return renderer._render_overlay_defs_scene(ctx, pcbdoc)  # noqa: SLF001
        except Exception as exc:
            log.warning("Skipping %s HLR overlay for %s: %s", side, view.name, exc)
            return [], []

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
            width_iu, height_iu = pad._layer_size(layer)  # noqa: SLF001
            if width_iu <= 0 or height_iu <= 0:
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


def _replace_group_in_svg(existing_svg: str, new_svg: str, group_id: str) -> str:
    ET.register_namespace("", _SVG_NS)
    existing_root = ET.fromstring(existing_svg)
    new_group = _extract_svg_group(new_svg, group_id)
    old_group = _find_element_by_id(existing_root, group_id)
    if old_group is None:
        raise ValueError(f"Existing SVG does not contain durable group {group_id!r}")
    else:
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
