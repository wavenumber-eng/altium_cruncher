"""pcb-svg command for altium_cruncher.

The command emits contract SVG artifacts (geometry + metadata only). Any
presentation-only decoration belongs in downstream HTML/report consumers.

View config is array-driven: each `views[]` object defines a render `source`
(`layers`, `top`, `bottom`, `assembly-top`, `assembly-bottom`) and a
`name` that drives output folder/file naming.
"""

import argparse
import json
import logging
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from altium_monkey.altium_pcb_surface import PCB_SurfaceRole, PCB_SurfaceSide
from altium_monkey.altium_pcb_svg_renderer import PcbSvgRenderOptions, PcbSvgRenderer
from altium_monkey.altium_record_types import PcbLayer

from altium_cruncher.altium_cruncher_common import (
    _resolve_output_dir,
    find_pcbdocs_in_cwd,
    find_prjpcbs_in_cwd,
)
from altium_cruncher.svg_hatch_patterns import MIN_DASH_MM, MIN_HATCH_SPACING_MM

log = logging.getLogger(__name__)

PCB_SVG_CONFIG_FILENAME = "pcb-svg.json"
PCB_SVG_CONFIG_SCHEMA = "wn.pcb.svg.config.v1"
PCB_SVG_VIEW_SOURCES = {"layers", "top", "bottom", "assembly-top", "assembly-bottom"}
PCB_SVG_CONTENT_VIEW_SOURCES = {
    "layers",
    "top",
    "bottom",
    "assembly-top",
    "assembly-bottom",
}
PCB_SURFACE_LAYER_ORDER_TOKENS = {"copper", "silkscreen"}
ASSEMBLY_OVERLAY_KARASHI_YELLOW = "#F59E0B"
PCB_DEFAULT_SVG_SCALE = 10.0
PcbSvgResolvedSettings = dict[str, Any]


def _coerce_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "on"}:
            return True
        if normalized in {"0", "false", "no", "off"}:
            return False
    raise ValueError(f"Invalid boolean value in pcb-svg config: {value!r}")


def _coerce_float(value: Any, default: float) -> float:
    if value is None:
        return float(default)
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid numeric value in pcb-svg config: {value!r}") from exc


def _coerce_optional_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid numeric value in pcb-svg config: {value!r}") from exc


def _coerce_optional_bool(value: object, default: bool) -> bool | None:
    if value is None:
        return None
    return _coerce_bool(value, default)


def _coerce_optional_int(value: object, default: float) -> int | None:
    if value is None:
        return None
    return int(_coerce_float(value, default))


def _coerce_str(value: Any, default: str) -> str:
    if value is None:
        return default
    return str(value)


def _coerce_optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _normalize_view_source(value: Any) -> str:
    source = str(value or "").strip().lower()
    source_aliases = {
        "layers": "layers",
        "top": "top",
        "top_view": "top",
        "bottom": "bottom",
        "bottom_view": "bottom",
        "assembly-top": "assembly-top",
        "assembly_top": "assembly-top",
        "assembly_top_view": "assembly-top",
        "assembly-bottom": "assembly-bottom",
        "assembly_bottom": "assembly-bottom",
        "assembly_bottom_view": "assembly-bottom",
    }
    return source_aliases.get(source, source)


def _coerce_optional_str_list(value: Any) -> list[str] | None:
    if value is None:
        return None
    if not isinstance(value, list):
        raise ValueError(
            f"Expected a list value in pcb-svg config, got: {type(value).__name__}"
        )
    result: list[str] = []
    for item in value:
        text = str(item).strip()
        if text:
            result.append(text)
    return result


def _parse_hex_argb_to_svg_color(
    raw_color: str, *, field_name: str, view_name: str
) -> str:
    """
    Parse hex RGB/ARGB color into SVG-friendly CSS color.

    Accepts:
    - `#RRGGBB`
    - `#AARRGGBB`
    - `RRGGBB`
    - `AARRGGBB`
    - `0xRRGGBB`
    - `0xAARRGGBB`
    """
    text = str(raw_color or "").strip()
    if not text:
        raise ValueError(f"Missing {field_name} for view '{view_name}'")

    if text.lower().startswith("0x"):
        text = text[2:]
    if text.startswith("#"):
        text = text[1:]

    text = text.strip()
    if len(text) == 6:
        try:
            int(text, 16)
        except ValueError as exc:
            raise ValueError(
                f"Invalid {field_name} '{raw_color}' in view '{view_name}'. "
                "Expected hex RGB/ARGB."
            ) from exc
        return f"#{text.upper()}"

    if len(text) == 8:
        try:
            value = int(text, 16)
        except ValueError as exc:
            raise ValueError(
                f"Invalid {field_name} '{raw_color}' in view '{view_name}'. "
                "Expected hex RGB/ARGB."
            ) from exc
        a = (value >> 24) & 0xFF
        r = (value >> 16) & 0xFF
        g = (value >> 8) & 0xFF
        b = value & 0xFF
        if a == 0xFF:
            return f"#{r:02X}{g:02X}{b:02X}"
        alpha = a / 255.0
        alpha_text = f"{alpha:.4f}".rstrip("0").rstrip(".")
        return f"rgba({r},{g},{b},{alpha_text})"

    raise ValueError(
        f"Invalid {field_name} '{raw_color}' in view '{view_name}'. "
        "Expected 6 or 8 hex digits (RGB or ARGB)."
    )


def _normalize_surface_layer_order(
    raw_order: list[str] | None, *, view_name: str
) -> list[str] | None:
    if raw_order is None:
        return None
    normalized: list[str] = []
    for token in raw_order:
        name = str(token or "").strip().lower()
        if not name:
            continue
        if name not in PCB_SURFACE_LAYER_ORDER_TOKENS:
            raise ValueError(
                f"Unsupported layer_order token '{token}' in view '{view_name}'. "
                "Expected copper or silkscreen."
            )
        if name not in normalized:
            normalized.append(name)
    return normalized or None


@dataclass(slots=True)
class PcbSvgGlobalConfig:
    """
    Global pcb-svg rendering options applied to all views unless overridden.
    """

    pcbdoc: str | None = None
    mono_color: str = "#000000"
    board_cutout_color: str = "#FFFF0000"
    plated_drill_color: str = "#90EE90"
    non_plated_drill_color: str = "#ADD8E6"
    polygon_color: str = "#FF888888"
    drill_mode: str = "overlay"
    drill_overlay_opacity: float = 0.25
    include_metadata: bool = True
    include_board_outline: bool = True
    include_outline_in_layers: bool = True
    show_empty_layers: bool = False
    include_polygon_definition_overlays: bool = False
    mirror_bottom_view: bool = True
    clip_to_outline: bool = True
    clip_holes_from_copper: bool = True
    include_board_cutout_layer: bool = False
    board_cutout_layer_hatch: bool = False
    board_cutout_layer_hash_spacing_mm: float = 2.0
    board_cutout_layer_hash_angle_deg: float = 45.0
    board_cutout_layer_outline_style: str = "solid"
    board_cutout_layer_outline_dash_mm: float = 1.5
    board_cutout_layer_label: bool = False
    board_cutout_layer_label_text: str = "cutout"
    assembly_enabled: bool = False
    assembly_include_simple: bool = True
    assembly_include_detail: bool = True
    assembly_curve_mode: str = "native_arcs"
    assembly_samples_per_curve: int = 24
    assembly_round_digits: int = 3
    assembly_include_visible: bool = True
    assembly_include_outline: bool = True
    assembly_union_polygons: bool = True
    svg_scale: float = PCB_DEFAULT_SVG_SCALE
    svg_size_unit: str = ""
    clean_output: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "PcbSvgGlobalConfig":
        if data is None:
            return cls()
        if not isinstance(data, dict):
            raise ValueError("pcb-svg config field 'global' must be an object")

        default = cls()
        return cls(
            pcbdoc=_coerce_optional_str(data.get("pcbdoc")),
            mono_color=_coerce_str(data.get("mono_color"), default.mono_color),
            board_cutout_color=_coerce_str(
                data.get("board_cutout_color"), default.board_cutout_color
            ),
            plated_drill_color=_coerce_str(
                data.get("plated_drill_color"), default.plated_drill_color
            ),
            non_plated_drill_color=_coerce_str(
                data.get("non_plated_drill_color"), default.non_plated_drill_color
            ),
            polygon_color=_coerce_str(data.get("polygon_color"), default.polygon_color),
            drill_mode=_coerce_str(data.get("drill_mode"), default.drill_mode),
            drill_overlay_opacity=_coerce_float(
                data.get("drill_overlay_opacity"), default.drill_overlay_opacity
            ),
            include_metadata=_coerce_bool(
                data.get("include_metadata"), default.include_metadata
            ),
            include_board_outline=_coerce_bool(
                data.get("include_board_outline"), default.include_board_outline
            ),
            include_outline_in_layers=_coerce_bool(
                data.get("include_outline_in_layers"),
                default.include_outline_in_layers,
            ),
            show_empty_layers=_coerce_bool(
                data.get("show_empty_layers"), default.show_empty_layers
            ),
            include_polygon_definition_overlays=_coerce_bool(
                data.get("include_polygon_definition_overlays"),
                default.include_polygon_definition_overlays,
            ),
            mirror_bottom_view=_coerce_bool(
                data.get("mirror_bottom_view"), default.mirror_bottom_view
            ),
            clip_to_outline=_coerce_bool(
                data.get("clip_to_outline"), default.clip_to_outline
            ),
            clip_holes_from_copper=_coerce_bool(
                data.get("clip_holes_from_copper"), default.clip_holes_from_copper
            ),
            include_board_cutout_layer=_coerce_bool(
                data.get("include_board_cutout_layer"),
                default.include_board_cutout_layer,
            ),
            board_cutout_layer_hatch=_coerce_bool(
                data.get("board_cutout_layer_hatch"),
                default.board_cutout_layer_hatch,
            ),
            board_cutout_layer_hash_spacing_mm=_coerce_float(
                data.get("board_cutout_layer_hash_spacing_mm"),
                default.board_cutout_layer_hash_spacing_mm,
            ),
            board_cutout_layer_hash_angle_deg=_coerce_float(
                data.get("board_cutout_layer_hash_angle_deg"),
                default.board_cutout_layer_hash_angle_deg,
            ),
            board_cutout_layer_outline_style=_coerce_str(
                data.get("board_cutout_layer_outline_style"),
                default.board_cutout_layer_outline_style,
            ),
            board_cutout_layer_outline_dash_mm=_coerce_float(
                data.get("board_cutout_layer_outline_dash_mm"),
                default.board_cutout_layer_outline_dash_mm,
            ),
            board_cutout_layer_label=_coerce_bool(
                data.get("board_cutout_layer_label"),
                default.board_cutout_layer_label,
            ),
            board_cutout_layer_label_text=_coerce_str(
                data.get("board_cutout_layer_label_text"),
                default.board_cutout_layer_label_text,
            ),
            assembly_enabled=_coerce_bool(
                data.get("assembly_enabled"), default.assembly_enabled
            ),
            assembly_include_simple=_coerce_bool(
                data.get("assembly_include_simple"),
                default.assembly_include_simple,
            ),
            assembly_include_detail=_coerce_bool(
                data.get("assembly_include_detail"),
                default.assembly_include_detail,
            ),
            assembly_curve_mode=_coerce_str(
                data.get("assembly_curve_mode"), default.assembly_curve_mode
            ),
            assembly_samples_per_curve=int(
                _coerce_float(
                    data.get("assembly_samples_per_curve"),
                    float(default.assembly_samples_per_curve),
                )
            ),
            assembly_round_digits=int(
                _coerce_float(
                    data.get("assembly_round_digits"),
                    float(default.assembly_round_digits),
                )
            ),
            assembly_include_visible=_coerce_bool(
                data.get("assembly_include_visible"),
                default.assembly_include_visible,
            ),
            assembly_include_outline=_coerce_bool(
                data.get("assembly_include_outline"),
                default.assembly_include_outline,
            ),
            assembly_union_polygons=_coerce_bool(
                data.get("assembly_union_polygons"),
                default.assembly_union_polygons,
            ),
            svg_scale=_coerce_float(data.get("svg_scale"), default.svg_scale),
            svg_size_unit=_coerce_str(data.get("svg_size_unit"), default.svg_size_unit),
            clean_output=_coerce_bool(data.get("clean_output"), default.clean_output),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "pcbdoc": self.pcbdoc,
            "mono_color": self.mono_color,
            "board_cutout_color": self.board_cutout_color,
            "plated_drill_color": self.plated_drill_color,
            "non_plated_drill_color": self.non_plated_drill_color,
            "polygon_color": self.polygon_color,
            "drill_mode": self.drill_mode,
            "drill_overlay_opacity": self.drill_overlay_opacity,
            "include_metadata": self.include_metadata,
            "include_board_outline": self.include_board_outline,
            "include_outline_in_layers": self.include_outline_in_layers,
            "show_empty_layers": self.show_empty_layers,
            "include_polygon_definition_overlays": self.include_polygon_definition_overlays,
            "mirror_bottom_view": self.mirror_bottom_view,
            "clip_to_outline": self.clip_to_outline,
            "clip_holes_from_copper": self.clip_holes_from_copper,
            "include_board_cutout_layer": self.include_board_cutout_layer,
            "board_cutout_layer_hatch": self.board_cutout_layer_hatch,
            "board_cutout_layer_hash_spacing_mm": self.board_cutout_layer_hash_spacing_mm,
            "board_cutout_layer_hash_angle_deg": self.board_cutout_layer_hash_angle_deg,
            "board_cutout_layer_outline_style": self.board_cutout_layer_outline_style,
            "board_cutout_layer_outline_dash_mm": self.board_cutout_layer_outline_dash_mm,
            "board_cutout_layer_label": self.board_cutout_layer_label,
            "board_cutout_layer_label_text": self.board_cutout_layer_label_text,
            "assembly_enabled": self.assembly_enabled,
            "assembly_include_simple": self.assembly_include_simple,
            "assembly_include_detail": self.assembly_include_detail,
            "assembly_curve_mode": self.assembly_curve_mode,
            "assembly_samples_per_curve": self.assembly_samples_per_curve,
            "assembly_round_digits": self.assembly_round_digits,
            "assembly_include_visible": self.assembly_include_visible,
            "assembly_include_outline": self.assembly_include_outline,
            "assembly_union_polygons": self.assembly_union_polygons,
            "svg_scale": self.svg_scale,
            "svg_size_unit": self.svg_size_unit,
            "clean_output": self.clean_output,
        }


@dataclass(slots=True)
class PcbSvgViewConfig:
    """
    Per-view pcb-svg options. Any option set to None inherits from global.

    `source` selects the render pipeline (top/bottom/layers/assembly).
    `name` drives artifact folder/file naming.

    `description` is metadata-only and is emitted in sidecar manifests. It does
    not inject title/caption primitives into core SVG artifacts.
    """

    name: str
    source: str
    enabled: bool = True
    layers: list[str] | None = None
    source_views: list[str] | None = None
    board_outline_color: str | None = None
    board_cutout_color: str | None = None
    copper_color: str | None = None
    silkscreen_color: str | None = None
    description: str | None = None
    layer_order: list[str] | None = None
    mono_color: str | None = None
    plated_drill_color: str | None = None
    non_plated_drill_color: str | None = None
    polygon_color: str | None = None
    drill_mode: str | None = None
    drill_overlay_opacity: float | None = None
    include_metadata: bool | None = None
    include_board_outline: bool | None = None
    include_outline_in_layers: bool | None = None
    show_empty_layers: bool | None = None
    include_polygon_definition_overlays: bool | None = None
    mirror_bottom_view: bool | None = None
    clip_to_outline: bool | None = None
    clip_holes_from_copper: bool | None = None
    include_board_cutout_layer: bool | None = None
    board_cutout_layer_hatch: bool | None = None
    board_cutout_layer_hash_spacing_mm: float | None = None
    board_cutout_layer_hash_angle_deg: float | None = None
    board_cutout_layer_outline_style: str | None = None
    board_cutout_layer_outline_dash_mm: float | None = None
    board_cutout_layer_label: bool | None = None
    board_cutout_layer_label_text: str | None = None
    assembly_enabled: bool | None = None
    assembly_include_simple: bool | None = None
    assembly_include_detail: bool | None = None
    assembly_curve_mode: str | None = None
    assembly_samples_per_curve: int | None = None
    assembly_round_digits: int | None = None
    assembly_include_visible: bool | None = None
    assembly_include_outline: bool | None = None
    assembly_union_polygons: bool | None = None
    svg_scale: float | None = None
    svg_size_unit: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PcbSvgViewConfig":
        if not isinstance(data, dict):
            raise ValueError("Each item in pcb-svg config 'views' must be an object")
        raw_name = _coerce_optional_str(data.get("name"))
        if not raw_name:
            raise ValueError(
                "Each view in pcb-svg config must include a non-empty 'name'"
            )
        view_source = _normalize_view_source(data.get("source", raw_name))
        if view_source not in PCB_SVG_VIEW_SOURCES:
            raise ValueError(
                f"Unsupported pcb-svg view source '{view_source}'. "
                f"Expected one of: {', '.join(sorted(PCB_SVG_VIEW_SOURCES))}"
            )

        return cls(
            name=raw_name,
            source=view_source,
            enabled=_coerce_bool(data.get("enabled"), True),
            layers=_coerce_optional_str_list(data.get("layers")),
            source_views=_coerce_optional_str_list(data.get("source_views")),
            board_outline_color=_coerce_optional_str(data.get("board_outline_color")),
            board_cutout_color=_coerce_optional_str(data.get("board_cutout_color")),
            copper_color=_coerce_optional_str(data.get("copper_color")),
            silkscreen_color=_coerce_optional_str(data.get("silkscreen_color")),
            # Legacy `title_text` now maps to metadata-only description.
            description=_coerce_optional_str(
                data.get("description") or data.get("title_text")
            ),
            layer_order=_coerce_optional_str_list(data.get("layer_order")),
            mono_color=_coerce_optional_str(data.get("mono_color")),
            plated_drill_color=_coerce_optional_str(data.get("plated_drill_color")),
            non_plated_drill_color=_coerce_optional_str(
                data.get("non_plated_drill_color")
            ),
            polygon_color=_coerce_optional_str(data.get("polygon_color")),
            drill_mode=_coerce_optional_str(data.get("drill_mode")),
            drill_overlay_opacity=_coerce_optional_float(
                data.get("drill_overlay_opacity")
            ),
            include_metadata=_coerce_optional_bool(data.get("include_metadata"), True),
            include_board_outline=_coerce_optional_bool(
                data.get("include_board_outline"), True
            ),
            include_outline_in_layers=_coerce_optional_bool(
                data.get("include_outline_in_layers"), True
            ),
            show_empty_layers=_coerce_optional_bool(
                data.get("show_empty_layers"), False
            ),
            include_polygon_definition_overlays=_coerce_optional_bool(
                data.get("include_polygon_definition_overlays"), False
            ),
            mirror_bottom_view=_coerce_optional_bool(
                data.get("mirror_bottom_view"), True
            ),
            clip_to_outline=_coerce_optional_bool(data.get("clip_to_outline"), True),
            clip_holes_from_copper=_coerce_optional_bool(
                data.get("clip_holes_from_copper"), True
            ),
            include_board_cutout_layer=_coerce_optional_bool(
                data.get("include_board_cutout_layer"), False
            ),
            board_cutout_layer_hatch=_coerce_optional_bool(
                data.get("board_cutout_layer_hatch"), False
            ),
            board_cutout_layer_hash_spacing_mm=_coerce_optional_float(
                data.get("board_cutout_layer_hash_spacing_mm")
            ),
            board_cutout_layer_hash_angle_deg=_coerce_optional_float(
                data.get("board_cutout_layer_hash_angle_deg")
            ),
            board_cutout_layer_outline_style=_coerce_optional_str(
                data.get("board_cutout_layer_outline_style")
            ),
            board_cutout_layer_outline_dash_mm=_coerce_optional_float(
                data.get("board_cutout_layer_outline_dash_mm")
            ),
            board_cutout_layer_label=_coerce_optional_bool(
                data.get("board_cutout_layer_label"), False
            ),
            board_cutout_layer_label_text=_coerce_optional_str(
                data.get("board_cutout_layer_label_text")
            ),
            assembly_enabled=_coerce_optional_bool(
                data.get("assembly_enabled"), False
            ),
            assembly_include_simple=_coerce_optional_bool(
                data.get("assembly_include_simple"), True
            ),
            assembly_include_detail=_coerce_optional_bool(
                data.get("assembly_include_detail"), True
            ),
            assembly_curve_mode=_coerce_optional_str(data.get("assembly_curve_mode")),
            assembly_samples_per_curve=_coerce_optional_int(
                data.get("assembly_samples_per_curve"), 24.0
            ),
            assembly_round_digits=_coerce_optional_int(
                data.get("assembly_round_digits"), 3.0
            ),
            assembly_include_visible=_coerce_optional_bool(
                data.get("assembly_include_visible"), True
            ),
            assembly_include_outline=_coerce_optional_bool(
                data.get("assembly_include_outline"), True
            ),
            assembly_union_polygons=_coerce_optional_bool(
                data.get("assembly_union_polygons"), True
            ),
            svg_scale=_coerce_optional_float(data.get("svg_scale")),
            svg_size_unit=_coerce_optional_str(data.get("svg_size_unit")),
        )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "name": self.name,
            "source": self.source,
            "enabled": self.enabled,
        }
        optional_values = {
            "layers": self.layers,
            "source_views": self.source_views,
            "board_outline_color": self.board_outline_color,
            "board_cutout_color": self.board_cutout_color,
            "copper_color": self.copper_color,
            "silkscreen_color": self.silkscreen_color,
            "description": self.description,
            "layer_order": self.layer_order,
            "mono_color": self.mono_color,
            "plated_drill_color": self.plated_drill_color,
            "non_plated_drill_color": self.non_plated_drill_color,
            "polygon_color": self.polygon_color,
            "drill_mode": self.drill_mode,
            "drill_overlay_opacity": self.drill_overlay_opacity,
            "include_metadata": self.include_metadata,
            "include_board_outline": self.include_board_outline,
            "include_outline_in_layers": self.include_outline_in_layers,
            "show_empty_layers": self.show_empty_layers,
            "include_polygon_definition_overlays": self.include_polygon_definition_overlays,
            "mirror_bottom_view": self.mirror_bottom_view,
            "clip_to_outline": self.clip_to_outline,
            "clip_holes_from_copper": self.clip_holes_from_copper,
            "include_board_cutout_layer": self.include_board_cutout_layer,
            "board_cutout_layer_hatch": self.board_cutout_layer_hatch,
            "board_cutout_layer_hash_spacing_mm": self.board_cutout_layer_hash_spacing_mm,
            "board_cutout_layer_hash_angle_deg": self.board_cutout_layer_hash_angle_deg,
            "board_cutout_layer_outline_style": self.board_cutout_layer_outline_style,
            "board_cutout_layer_outline_dash_mm": self.board_cutout_layer_outline_dash_mm,
            "board_cutout_layer_label": self.board_cutout_layer_label,
            "board_cutout_layer_label_text": self.board_cutout_layer_label_text,
            "assembly_enabled": self.assembly_enabled,
            "assembly_include_simple": self.assembly_include_simple,
            "assembly_include_detail": self.assembly_include_detail,
            "assembly_curve_mode": self.assembly_curve_mode,
            "assembly_samples_per_curve": self.assembly_samples_per_curve,
            "assembly_round_digits": self.assembly_round_digits,
            "assembly_include_visible": self.assembly_include_visible,
            "assembly_include_outline": self.assembly_include_outline,
            "assembly_union_polygons": self.assembly_union_polygons,
            "svg_scale": self.svg_scale,
            "svg_size_unit": self.svg_size_unit,
        }
        for key, value in optional_values.items():
            if value is not None:
                result[key] = value
        return result


def _default_pcb_svg_views() -> list[PcbSvgViewConfig]:
    return [
        PcbSvgViewConfig(name="layers", source="layers"),
        PcbSvgViewConfig(
            name="top_view",
            source="top",
            board_outline_color="#FF000000",
            board_cutout_color="#FFFF0000",
            copper_color="#FF000000",
            silkscreen_color="#FF000000",
            plated_drill_color="#FF90EE90",
            non_plated_drill_color="#FFADD8E6",
            polygon_color="#FF888888",
            description="Top View",
            layer_order=["copper", "silkscreen"],
        ),
        PcbSvgViewConfig(
            name="bottom_view",
            source="bottom",
            board_outline_color="#FF000000",
            board_cutout_color="#FFFF0000",
            copper_color="#FF000000",
            silkscreen_color="#FF000000",
            plated_drill_color="#FF90EE90",
            non_plated_drill_color="#FFADD8E6",
            polygon_color="#FF888888",
            description="Bottom View",
            layer_order=["copper", "silkscreen"],
        ),
        PcbSvgViewConfig(
            name="assembly_top_view",
            source="assembly-top",
            enabled=False,
            assembly_enabled=True,
            board_outline_color="#FF000000",
            board_cutout_color="#FFFF0000",
            copper_color="#FF000000",
            silkscreen_color="#FF000000",
            description="Assembly Top View",
            layer_order=["copper"],
        ),
        PcbSvgViewConfig(
            name="assembly_bottom_view",
            source="assembly-bottom",
            enabled=False,
            assembly_enabled=True,
            board_outline_color="#FF000000",
            board_cutout_color="#FFFF0000",
            copper_color="#FF000000",
            silkscreen_color="#FF000000",
            description="Assembly Bottom View",
            layer_order=["copper"],
        ),
    ]


@dataclass(slots=True)
class PcbSvgConfig:
    """
    Config model for pcb-svg serialization/deserialization.
    """

    schema: str = PCB_SVG_CONFIG_SCHEMA
    global_options: PcbSvgGlobalConfig = field(default_factory=PcbSvgGlobalConfig)
    views: list[PcbSvgViewConfig] = field(default_factory=_default_pcb_svg_views)

    @classmethod
    def default(cls) -> "PcbSvgConfig":
        return cls()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PcbSvgConfig":
        if not isinstance(data, dict):
            raise ValueError("pcb-svg config root must be a JSON object")
        schema = str(data.get("schema") or PCB_SVG_CONFIG_SCHEMA)
        global_options = PcbSvgGlobalConfig.from_dict(data.get("global"))
        raw_views = data.get("views")
        if raw_views is None:
            views = _default_pcb_svg_views()
        else:
            if not isinstance(raw_views, list):
                raise ValueError("pcb-svg config field 'views' must be an array")
            views = [PcbSvgViewConfig.from_dict(item) for item in raw_views]
        return cls(schema=schema, global_options=global_options, views=views)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "global": self.global_options.to_dict(),
            "views": [view.to_dict() for view in self.views],
        }


def _write_default_pcb_svg_config(config_path: Path) -> None:
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config = PcbSvgConfig.default()
    config_path.write_text(json.dumps(config.to_dict(), indent=2), encoding="utf-8")


def _load_pcb_svg_config(config_path: Path) -> PcbSvgConfig:
    try:
        raw_data = json.loads(config_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(
            f"Failed to parse pcb-svg config '{config_path}': {exc}"
        ) from exc
    return PcbSvgConfig.from_dict(raw_data)


def _apply_pcb_view_selection(
    config: PcbSvgConfig, raw_views: str | None
) -> PcbSvgConfig:
    if raw_views is None:
        return config

    selected_sources = _parse_pcb_views(raw_views)
    for view in config.views:
        if view.source in PCB_SVG_CONTENT_VIEW_SOURCES:
            view.enabled = view.source in selected_sources
    return config


def _apply_pcb_layer_selection(
    config: PcbSvgConfig, raw_layers: str | None
) -> PcbSvgConfig:
    if raw_layers is None:
        return config

    selected_layers = _parse_pcb_visible_layers(raw_layers)
    normalized_layers = [
        layer.to_json_name()
        for layer in sorted(selected_layers or [], key=lambda item: int(item.value))
    ]
    for view in config.views:
        if view.source == "layers":
            view.layers = normalized_layers
    return config


def _resolve_pcb_svg_configs(
    args,
    input_files: list[Path],
) -> tuple[dict[Path, PcbSvgConfig], list[Path]]:
    """
    Resolve one effective pcb-svg config per input file.

    Returns:
        (config_by_input, created_paths)
        - created_paths contains any config templates that were created during
          resolution; callers may log them but should continue using the loaded
          default config in the same invocation.
    """
    resolved_input_files = [path.resolve() for path in input_files]
    created_paths: list[Path] = []
    config_by_input: dict[Path, PcbSvgConfig] = {}
    config_cache: dict[Path, PcbSvgConfig] = {}

    if getattr(args, "config", None):
        explicit_config_path = Path(args.config).resolve()
        if not explicit_config_path.exists():
            _write_default_pcb_svg_config(explicit_config_path)
            created_paths.append(explicit_config_path)
        loaded_config = _load_pcb_svg_config(explicit_config_path)
        _apply_pcb_view_selection(loaded_config, getattr(args, "pcb_views", None))
        _apply_pcb_layer_selection(loaded_config, getattr(args, "pcb_layers", None))
        for input_file in resolved_input_files:
            config_by_input[input_file] = loaded_config
        return config_by_input, created_paths

    for input_file in resolved_input_files:
        auto_config_path = input_file.parent / PCB_SVG_CONFIG_FILENAME
        if not auto_config_path.exists():
            _write_default_pcb_svg_config(auto_config_path)
            created_paths.append(auto_config_path)

    for input_file in resolved_input_files:
        auto_config_path = input_file.parent / PCB_SVG_CONFIG_FILENAME
        loaded = config_cache.get(auto_config_path)
        if loaded is None:
            loaded = _load_pcb_svg_config(auto_config_path)
            _apply_pcb_view_selection(loaded, getattr(args, "pcb_views", None))
            _apply_pcb_layer_selection(loaded, getattr(args, "pcb_layers", None))
            config_cache[auto_config_path] = loaded
        config_by_input[input_file] = loaded

    return config_by_input, sorted(set(created_paths))


def _view_option_value(view_value: Any, global_value: Any) -> Any:
    return global_value if view_value is None else view_value


def _parse_pcb_views(raw_views: str | None) -> set[str]:
    """
    Parse comma-separated EG-06 PCB view names.

    Supported names:
    - `layers`
    - `top`
    - `bottom`
    - `assembly-top`
    - `assembly-bottom`
    - `all` (alias for layers,top,bottom,assembly-top,assembly-bottom)
    - `none`
    """
    if raw_views is None:
        return {"layers", "top", "bottom"}

    values = [token.strip().lower() for token in raw_views.split(",") if token.strip()]
    if not values:
        return {"layers", "top", "bottom"}

    normalized: set[str] = set()
    for value in values:
        if value == "all":
            normalized.update(
                {"layers", "top", "bottom", "assembly-top", "assembly-bottom"}
            )
            continue
        if value == "none":
            continue
        if value not in {"layers", "top", "bottom", "assembly-top", "assembly-bottom"}:
            raise ValueError(
                f"Unknown --pcb-views token '{value}'. "
                "Expected layers, top, bottom, assembly-top, assembly-bottom, all, or none."
            )
        normalized.add(value)
    return normalized


def _sanitize_layer_output_name(layer_name: str) -> str:
    """Convert layer labels into stable filesystem-safe suffixes."""
    return layer_name.replace(" ", "_").replace("/", "_")


def _parse_pcb_visible_layers(raw_layers: str | None):
    """
    Parse a comma-separated PCB layer selector string.

    Supported tokens:
    - numeric IDs (`1`, `33`, `57`)
    - `L`-prefixed IDs (`L1`, `L33`)
    - JSON layer names (`TOP`, `BOTTOM`, `TOPOVERLAY`, `MECHANICAL1`, ...)
    - common aliases (`TOP_LAYER`, `BOTTOM_SILK`, `TOP_MASK`, ...)
    """
    if not raw_layers:
        return None

    from altium_monkey.altium_record_types import PcbLayer

    alias_map = {
        "TOPLAYER": "TOP",
        "BOTTOMLAYER": "BOTTOM",
        "TOPSILK": "TOPOVERLAY",
        "BOTTOMSILK": "BOTTOMOVERLAY",
        "TOPSILKSCREEN": "TOPOVERLAY",
        "BOTTOMSILKSCREEN": "BOTTOMOVERLAY",
        "TOPMASK": "TOPSOLDER",
        "BOTTOMMASK": "BOTTOMSOLDER",
        "TOPPASTEMASK": "TOPPASTE",
        "BOTTOMPASTEMASK": "BOTTOMPASTE",
    }

    selected_layers = set()
    tokens = [token.strip() for token in raw_layers.split(",") if token.strip()]
    if not tokens:
        raise ValueError(
            "--pcb-layers was provided but no valid layer tokens were found"
        )

    for token in tokens:
        normalized = token.upper().replace(" ", "").replace("_", "").replace("-", "")
        numeric_token = (
            normalized[1:]
            if normalized.startswith("L") and normalized[1:].isdigit()
            else normalized
        )

        if numeric_token.isdigit():
            layer_id = int(numeric_token)
            try:
                selected_layers.add(PcbLayer(layer_id))
            except ValueError as exc:
                raise ValueError(
                    f"Unknown PCB layer id in --pcb-layers: {token}"
                ) from exc
            continue

        canonical_name = alias_map.get(normalized, normalized)
        try:
            selected_layers.add(PcbLayer.from_json_name(canonical_name))
        except ValueError as exc:
            raise ValueError(
                f"Unknown PCB layer token in --pcb-layers: {token}"
            ) from exc

    return selected_layers


def _parse_pcb_visible_layers_from_list(raw_layers: list[str] | None):
    if raw_layers is None:
        return None
    joined = ",".join(str(token).strip() for token in raw_layers if str(token).strip())
    if not joined:
        return None
    return _parse_pcb_visible_layers(joined)


def _validate_board_cutout_outline_style(*, style: str, view_name: str) -> str:
    normalized = str(style or "solid").strip().lower()
    if normalized not in {"solid", "dashed"}:
        raise ValueError(
            f"Invalid board_cutout_layer_outline_style '{style}' for view "
            f"'{view_name}'. Expected solid or dashed."
        )
    return normalized


def _validate_positive_svg_mm(
    *,
    value: float,
    field_name: str,
    view_name: str,
    minimum: float,
) -> float:
    number = float(value)
    if not math.isfinite(number) or number < minimum:
        raise ValueError(
            f"Invalid {field_name} '{value}' for view '{view_name}'. "
            f"Expected a value >= {minimum}."
        )
    return number


def _merge_rendered_views(
    destination: dict[str, dict[str, str]],
    source: dict[str, dict[str, str]],
) -> None:
    for board_name, view_map in source.items():
        board_views = destination.setdefault(board_name, {})
        board_views.update(view_map)


def _resolve_view_render_settings(
    global_options: PcbSvgGlobalConfig,
    view: PcbSvgViewConfig,
    *,
    default_svg_scale: float | None = None,
    default_svg_size_unit: str | None = None,
) -> dict[str, Any]:
    view_source = view.source
    view_label = f"{view.name} ({view_source})"
    visible_layers = _parse_pcb_visible_layers_from_list(view.layers)

    mono_color = (
        str(_view_option_value(view.mono_color, global_options.mono_color)).strip()
        or "#000000"
    )
    board_cutout_color_raw = (
        str(
            _view_option_value(
                view.board_cutout_color, global_options.board_cutout_color
            )
        ).strip()
        or "#FFFF0000"
    )
    board_cutout_color = _parse_hex_argb_to_svg_color(
        board_cutout_color_raw,
        field_name="board_cutout_color",
        view_name=view_label,
    )
    board_cutout_hash_spacing_mm = _validate_positive_svg_mm(
        value=float(
            _view_option_value(
                view.board_cutout_layer_hash_spacing_mm,
                global_options.board_cutout_layer_hash_spacing_mm,
            )
        ),
        field_name="board_cutout_layer_hash_spacing_mm",
        view_name=view_label,
        minimum=MIN_HATCH_SPACING_MM,
    )
    board_cutout_outline_style = _validate_board_cutout_outline_style(
        style=str(
            _view_option_value(
                view.board_cutout_layer_outline_style,
                global_options.board_cutout_layer_outline_style,
            )
        ),
        view_name=view_label,
    )
    board_cutout_outline_dash_mm = _validate_positive_svg_mm(
        value=float(
            _view_option_value(
                view.board_cutout_layer_outline_dash_mm,
                global_options.board_cutout_layer_outline_dash_mm,
            )
        ),
        field_name="board_cutout_layer_outline_dash_mm",
        view_name=view_label,
        minimum=MIN_DASH_MM,
    )
    plated_color = (
        str(
            _view_option_value(
                view.plated_drill_color, global_options.plated_drill_color
            )
        ).strip()
        or "#90EE90"
    )
    non_plated_color = (
        str(
            _view_option_value(
                view.non_plated_drill_color, global_options.non_plated_drill_color
            )
        ).strip()
        or "#ADD8E6"
    )
    polygon_color_raw = (
        str(
            _view_option_value(view.polygon_color, global_options.polygon_color)
        ).strip()
        or "#FF888888"
    )
    polygon_color = _parse_hex_argb_to_svg_color(
        polygon_color_raw,
        field_name="polygon_color",
        view_name=view_label,
    )
    drill_mode = (
        str(_view_option_value(view.drill_mode, global_options.drill_mode))
        .strip()
        .lower()
        or "overlay"
    )
    if drill_mode not in {"knockout", "overlay", "none"}:
        raise ValueError(
            f"Invalid drill_mode '{drill_mode}' for view '{view_label}'. "
            "Expected knockout, overlay, or none."
        )

    drill_overlay_opacity = float(
        _view_option_value(
            view.drill_overlay_opacity, global_options.drill_overlay_opacity
        )
    )
    if not (0.0 <= drill_overlay_opacity <= 1.0):
        raise ValueError(
            f"Invalid drill_overlay_opacity '{drill_overlay_opacity}' for view '{view_label}'. "
            "Expected a value between 0 and 1."
        )

    assembly_curve_mode = (
        str(
            _view_option_value(
                view.assembly_curve_mode, global_options.assembly_curve_mode
            )
        )
        .strip()
        .lower()
        or "native_arcs"
    )
    if assembly_curve_mode not in {"native_arcs", "polyline"}:
        raise ValueError(
            f"Invalid assembly_curve_mode '{assembly_curve_mode}' for view '{view_label}'. "
            "Expected native_arcs or polyline."
        )
    assembly_samples_per_curve = int(
        _view_option_value(
            view.assembly_samples_per_curve, global_options.assembly_samples_per_curve
        )
    )
    if assembly_samples_per_curve < 2:
        raise ValueError(
            f"Invalid assembly_samples_per_curve '{assembly_samples_per_curve}' for view '{view_label}'. "
            "Expected an integer >= 2."
        )
    assembly_round_digits = int(
        _view_option_value(
            view.assembly_round_digits, global_options.assembly_round_digits
        )
    )
    if assembly_round_digits < 0:
        raise ValueError(
            f"Invalid assembly_round_digits '{assembly_round_digits}' for view '{view_label}'. "
            "Expected an integer >= 0."
        )

    base_scale = (
        global_options.svg_scale if default_svg_scale is None else default_svg_scale
    )
    svg_scale = float(_view_option_value(view.svg_scale, base_scale))
    if svg_scale <= 0.0:
        raise ValueError(
            f"Invalid svg_scale '{svg_scale}' for view '{view_label}'. "
            "Expected a value > 0."
        )

    base_size_unit = (
        global_options.svg_size_unit
        if default_svg_size_unit is None
        else default_svg_size_unit
    )
    svg_size_unit = str(_view_option_value(view.svg_size_unit, base_size_unit)).strip()

    board_outline_color: str | None = None
    copper_color: str | None = None
    silkscreen_color: str | None = None
    layer_order: list[str] | None = None
    description: str | None = _coerce_optional_str(view.description)
    if view_source in {"top", "bottom", "assembly-top", "assembly-bottom"}:
        board_outline_color_raw = (
            str(_view_option_value(view.board_outline_color, mono_color)).strip()
            or mono_color
        )
        board_outline_color = _parse_hex_argb_to_svg_color(
            board_outline_color_raw,
            field_name="board_outline_color",
            view_name=view_label,
        )

        copper_color_raw = (
            str(_view_option_value(view.copper_color, mono_color)).strip() or mono_color
        )
        copper_color = _parse_hex_argb_to_svg_color(
            copper_color_raw,
            field_name="copper_color",
            view_name=view_label,
        )

        silkscreen_color_raw = (
            str(_view_option_value(view.silkscreen_color, mono_color)).strip()
            or mono_color
        )
        silkscreen_color = _parse_hex_argb_to_svg_color(
            silkscreen_color_raw,
            field_name="silkscreen_color",
            view_name=view_label,
        )

        plated_color = _parse_hex_argb_to_svg_color(
            plated_color,
            field_name="plated_drill_color",
            view_name=view_label,
        )
        non_plated_color = _parse_hex_argb_to_svg_color(
            non_plated_color,
            field_name="non_plated_drill_color",
            view_name=view_label,
        )

        if view_source in {"top", "bottom", "assembly-top", "assembly-bottom"}:
            layer_order = _normalize_surface_layer_order(
                view.layer_order, view_name=view_label
            )
            if layer_order is None:
                if view_source in {"assembly-top", "assembly-bottom"}:
                    layer_order = ["copper"]
                else:
                    layer_order = ["copper", "silkscreen"]
        if view_source in {"top", "assembly-top"}:
            default_description = (
                "Top View" if view_source == "top" else "Assembly Top View"
            )
        else:
            default_description = (
                "Bottom View" if view_source == "bottom" else "Assembly Bottom View"
            )
        if description is None:
            description = default_description

    # Assembly-only views should render assembly overlays by default even if the
    # global default is disabled.
    assembly_enabled_default = global_options.assembly_enabled
    if (
        view_source in {"assembly-top", "assembly-bottom"}
        and view.assembly_enabled is None
    ):
        assembly_enabled_default = True
    assembly_enabled = bool(
        _view_option_value(view.assembly_enabled, assembly_enabled_default)
    )

    render_kwargs = dict(
        pcbdoc_selector=global_options.pcbdoc,
        layer_filter=visible_layers,
        monochrome_color=mono_color,
        plated_drill_color=plated_color,
        non_plated_drill_color=non_plated_color,
        drill_mode=drill_mode,
        drill_overlay_opacity=drill_overlay_opacity,
        polygon_overlay_color=polygon_color,
        board_cutout_color=board_cutout_color,
        include_metadata=bool(
            _view_option_value(view.include_metadata, global_options.include_metadata)
        ),
        include_board_outline=bool(
            _view_option_value(
                view.include_board_outline, global_options.include_board_outline
            )
        ),
        include_outline_in_layer_views=bool(
            _view_option_value(
                view.include_outline_in_layers, global_options.include_outline_in_layers
            )
        ),
        show_empty_layers=bool(
            _view_option_value(view.show_empty_layers, global_options.show_empty_layers)
        ),
        include_polygon_definition_overlays=bool(
            _view_option_value(
                view.include_polygon_definition_overlays,
                global_options.include_polygon_definition_overlays,
            )
        ),
        mirror_bottom_view=bool(
            _view_option_value(
                view.mirror_bottom_view, global_options.mirror_bottom_view
            )
        ),
        clip_to_outline=bool(
            _view_option_value(view.clip_to_outline, global_options.clip_to_outline)
        ),
        clip_holes_from_copper=bool(
            _view_option_value(
                view.clip_holes_from_copper, global_options.clip_holes_from_copper
            )
        ),
        include_board_cutout_layer=bool(
            _view_option_value(
                view.include_board_cutout_layer,
                global_options.include_board_cutout_layer,
            )
        ),
        board_cutout_layer_hatch=bool(
            _view_option_value(
                view.board_cutout_layer_hatch,
                global_options.board_cutout_layer_hatch,
            )
        ),
        board_cutout_layer_hash_spacing_mm=board_cutout_hash_spacing_mm,
        board_cutout_layer_hash_angle_deg=float(
            _view_option_value(
                view.board_cutout_layer_hash_angle_deg,
                global_options.board_cutout_layer_hash_angle_deg,
            )
        ),
        board_cutout_layer_outline_style=board_cutout_outline_style,
        board_cutout_layer_outline_dash_mm=board_cutout_outline_dash_mm,
        board_cutout_layer_label=bool(
            _view_option_value(
                view.board_cutout_layer_label,
                global_options.board_cutout_layer_label,
            )
        ),
        board_cutout_layer_label_text=str(
            _view_option_value(
                view.board_cutout_layer_label_text,
                global_options.board_cutout_layer_label_text,
            )
        ),
        assembly_enabled=assembly_enabled,
        assembly_include_simple=bool(
            _view_option_value(
                view.assembly_include_simple, global_options.assembly_include_simple
            )
        ),
        assembly_include_detail=bool(
            _view_option_value(
                view.assembly_include_detail, global_options.assembly_include_detail
            )
        ),
        assembly_curve_mode=assembly_curve_mode,
        assembly_samples_per_curve=assembly_samples_per_curve,
        assembly_round_digits=assembly_round_digits,
        assembly_include_visible=bool(
            _view_option_value(
                view.assembly_include_visible, global_options.assembly_include_visible
            )
        ),
        assembly_include_outline=bool(
            _view_option_value(
                view.assembly_include_outline, global_options.assembly_include_outline
            )
        ),
        assembly_union_polygons=bool(
            _view_option_value(
                view.assembly_union_polygons, global_options.assembly_union_polygons
            )
        ),
        assembly_overlay_color=ASSEMBLY_OVERLAY_KARASHI_YELLOW,
    )

    return {
        "visible_layers": visible_layers,
        "render_kwargs": render_kwargs,
        "svg_scale": svg_scale,
        "svg_size_unit": svg_size_unit,
        "board_outline_color": board_outline_color,
        "board_cutout_color": board_cutout_color,
        "copper_color": copper_color,
        "silkscreen_color": silkscreen_color,
        "layer_order": layer_order,
        "description": description,
    }


def _surface_roles_from_order_tokens(
    order_tokens: list[str] | tuple[str, ...] | None,
) -> list[PCB_SurfaceRole]:
    if not order_tokens:
        return [PCB_SurfaceRole.COPPER, PCB_SurfaceRole.SILKSCREEN]
    return [
        PCB_SurfaceRole(str(token).strip().lower())
        for token in order_tokens
        if str(token).strip()
    ]


def _select_core_layer_view_layers(
    pcbdoc,
    *,
    layer_filter: set[PcbLayer] | None,
) -> set[PcbLayer]:
    selected_layers = set(layer_filter or set())
    if selected_layers:
        return selected_layers

    layer_probe = PcbSvgRenderer(PcbSvgRenderOptions())
    discovered = layer_probe._collect_visible_layers(pcbdoc)  # noqa: SLF001
    selected_layers = {
        layer for layer in discovered if layer.is_copper() or layer.is_overlay()
    }
    if selected_layers:
        return selected_layers

    return {
        PcbLayer.TOP,
        PcbLayer.BOTTOM,
        PcbLayer.TOP_OVERLAY,
        PcbLayer.BOTTOM_OVERLAY,
    }


def _build_core_layer_view_options(
    *,
    pcbdoc,
    resolved: dict[str, Any],
) -> PcbSvgRenderOptions:
    render_kwargs = resolved["render_kwargs"]
    selected_layers = _select_core_layer_view_layers(
        pcbdoc,
        layer_filter=render_kwargs["layer_filter"],
    )
    return PcbSvgRenderOptions(
        visible_layers=selected_layers,
        show_empty_layers=render_kwargs["show_empty_layers"],
        include_metadata=render_kwargs["include_metadata"],
        show_board_outline=render_kwargs["include_board_outline"],
        all_layers_color_override=render_kwargs["monochrome_color"],
        layer_svg_color_override=render_kwargs["monochrome_color"],
        board_outline_color=render_kwargs["monochrome_color"],
        board_cutout_color=render_kwargs["board_cutout_color"],
        include_polygon_definition_overlays=render_kwargs[
            "include_polygon_definition_overlays"
        ],
        polygon_overlay_color=render_kwargs["polygon_overlay_color"],
        drill_hole_mode=render_kwargs["drill_mode"],
        drill_hole_overlay_plated_color=render_kwargs["plated_drill_color"],
        drill_hole_overlay_non_plated_color=render_kwargs["non_plated_drill_color"],
        drill_hole_overlay_opacity=render_kwargs["drill_overlay_opacity"],
        clip_copper_to_board_outline=render_kwargs["clip_to_outline"],
        clip_all_layers_to_board_outline=render_kwargs["clip_to_outline"],
        clip_holes_from_copper=render_kwargs["clip_holes_from_copper"],
        svg_display_scale=float(resolved["svg_scale"]),
        svg_size_unit=str(resolved["svg_size_unit"]),
    )


def _build_core_surface_view_options(
    *,
    resolved: dict[str, Any],
    side: PCB_SurfaceSide,
) -> tuple[PcbSvgRenderOptions, list[PCB_SurfaceRole], dict[PCB_SurfaceRole, str]]:
    render_kwargs = resolved["render_kwargs"]
    role_order = _surface_roles_from_order_tokens(resolved["layer_order"])
    role_colors = {
        PCB_SurfaceRole.COPPER: resolved["copper_color"]
        or render_kwargs["monochrome_color"],
        PCB_SurfaceRole.SILKSCREEN: resolved["silkscreen_color"]
        or render_kwargs["monochrome_color"],
    }
    options = PcbSvgRenderOptions(
        show_empty_layers=render_kwargs["show_empty_layers"],
        include_metadata=render_kwargs["include_metadata"],
        show_board_outline=render_kwargs["include_board_outline"],
        board_outline_color=resolved["board_outline_color"]
        or render_kwargs["monochrome_color"],
        board_cutout_color=resolved["board_cutout_color"]
        or render_kwargs["board_cutout_color"],
        include_polygon_definition_overlays=render_kwargs[
            "include_polygon_definition_overlays"
        ],
        polygon_overlay_color=render_kwargs["polygon_overlay_color"],
        drill_hole_mode=render_kwargs["drill_mode"],
        drill_hole_overlay_plated_color=render_kwargs["plated_drill_color"],
        drill_hole_overlay_non_plated_color=render_kwargs["non_plated_drill_color"],
        drill_hole_overlay_opacity=render_kwargs["drill_overlay_opacity"],
        clip_copper_to_board_outline=render_kwargs["clip_to_outline"],
        clip_all_layers_to_board_outline=render_kwargs["clip_to_outline"],
        clip_holes_from_copper=render_kwargs["clip_holes_from_copper"],
        svg_display_scale=float(resolved["svg_scale"]),
        svg_size_unit=str(resolved["svg_size_unit"]),
        mirror_x=(
            side == PCB_SurfaceSide.BOTTOM and bool(render_kwargs["mirror_bottom_view"])
        ),
    )
    return options, role_order, role_colors


def _palette_value(
    palette: PcbSvgResolvedSettings | None,
    resolved: PcbSvgResolvedSettings,
    key: str,
) -> Any:
    if palette is not None:
        return palette[key]
    return resolved[key]


def _view_color_kwargs_for_source(
    source: str,
    resolved: PcbSvgResolvedSettings,
    *,
    top_palette: PcbSvgResolvedSettings | None,
    bottom_palette: PcbSvgResolvedSettings | None,
) -> PcbSvgResolvedSettings:
    if source == "top":
        render_kwargs = dict(resolved["render_kwargs"])
        return {
            "top_board_outline_color": resolved["board_outline_color"],
            "top_board_cutout_color": resolved["board_cutout_color"],
            "top_copper_color": resolved["copper_color"],
            "top_silkscreen_color": resolved["silkscreen_color"],
            "top_plated_drill_color": render_kwargs["plated_drill_color"],
            "top_non_plated_drill_color": render_kwargs["non_plated_drill_color"],
            "top_polygon_overlay_color": render_kwargs["polygon_overlay_color"],
            "top_layer_order": resolved["layer_order"],
        }
    if source == "bottom":
        render_kwargs = dict(resolved["render_kwargs"])
        return {
            "bottom_board_outline_color": resolved["board_outline_color"],
            "bottom_board_cutout_color": resolved["board_cutout_color"],
            "bottom_copper_color": resolved["copper_color"],
            "bottom_silkscreen_color": resolved["silkscreen_color"],
            "bottom_plated_drill_color": render_kwargs["plated_drill_color"],
            "bottom_non_plated_drill_color": render_kwargs["non_plated_drill_color"],
            "bottom_polygon_overlay_color": render_kwargs["polygon_overlay_color"],
            "bottom_layer_order": resolved["layer_order"],
        }
    if source == "assembly-top":
        return {
            "top_board_outline_color": _palette_value(
                top_palette, resolved, "board_outline_color"
            ),
            "top_board_cutout_color": _palette_value(
                top_palette, resolved, "board_cutout_color"
            ),
            "top_copper_color": _palette_value(top_palette, resolved, "copper_color"),
            "top_silkscreen_color": _palette_value(
                top_palette, resolved, "silkscreen_color"
            ),
            "assembly_top_layer_order": resolved["layer_order"],
        }
    if source == "assembly-bottom":
        return {
            "bottom_board_outline_color": _palette_value(
                bottom_palette, resolved, "board_outline_color"
            ),
            "bottom_board_cutout_color": _palette_value(
                bottom_palette, resolved, "board_cutout_color"
            ),
            "bottom_copper_color": _palette_value(
                bottom_palette, resolved, "copper_color"
            ),
            "bottom_silkscreen_color": _palette_value(
                bottom_palette, resolved, "silkscreen_color"
            ),
            "assembly_bottom_layer_order": resolved["layer_order"],
        }
    return {}


def _render_core_pcb_svg_views(
    design,
    *,
    resolved_by_source: dict[str, dict[str, Any]],
) -> dict[str, dict[str, str]]:
    from altium_cruncher.altium_cruncher_pcb_svg_cutout_layer import (
        CruncherPcbCutoutLayerRenderer,
        PCB_SVG_BOARD_CUTOUTS_LAYER_NAME,
    )
    from altium_cruncher.altium_cruncher_pcb_workflow import iter_pcb_render_inputs

    rendered: dict[str, dict[str, str]] = {}
    pcbdoc_selector = next(
        (
            resolved["render_kwargs"].get("pcbdoc_selector")
            for resolved in resolved_by_source.values()
            if resolved["render_kwargs"].get("pcbdoc_selector")
        ),
        None,
    )
    for render_input in iter_pcb_render_inputs(design, pcbdoc_selector=pcbdoc_selector):
        board_views: dict[str, str] = {}

        layer_resolved = resolved_by_source.get("layers")
        if layer_resolved is not None:
            layer_options = _build_core_layer_view_options(
                pcbdoc=render_input.pcbdoc,
                resolved=layer_resolved,
            )
            layer_svgs = render_input.pcbdoc.to_layer_svgs(
                options=layer_options,
                project_parameters=render_input.project_parameters,
            )
            if layer_resolved["render_kwargs"]["include_board_cutout_layer"]:
                cutout_svg = CruncherPcbCutoutLayerRenderer(
                    layer_options
                ).render_board_cutout_layer(
                    render_input.pcbdoc,
                    project_parameters=render_input.project_parameters,
                    include_hatch=bool(
                        layer_resolved["render_kwargs"]["board_cutout_layer_hatch"]
                    ),
                    hatch_spacing_mm=float(
                        layer_resolved["render_kwargs"][
                            "board_cutout_layer_hash_spacing_mm"
                        ]
                    ),
                    hatch_angle_deg=float(
                        layer_resolved["render_kwargs"][
                            "board_cutout_layer_hash_angle_deg"
                        ]
                    ),
                    include_label=bool(
                        layer_resolved["render_kwargs"]["board_cutout_layer_label"]
                    ),
                    label_text=str(
                        layer_resolved["render_kwargs"][
                            "board_cutout_layer_label_text"
                        ]
                    ),
                    outline_style=str(
                        layer_resolved["render_kwargs"][
                            "board_cutout_layer_outline_style"
                        ]
                    ),
                    outline_dash_mm=float(
                        layer_resolved["render_kwargs"][
                            "board_cutout_layer_outline_dash_mm"
                        ]
                    ),
                )
                if cutout_svg is not None:
                    layer_svgs[PCB_SVG_BOARD_CUTOUTS_LAYER_NAME] = cutout_svg
            for layer_name, layer_svg in layer_svgs.items():
                board_views[f"layer_{layer_name}"] = layer_svg

        top_resolved = resolved_by_source.get("top")
        if top_resolved is not None:
            top_options, top_role_order, top_role_colors = (
                _build_core_surface_view_options(
                    resolved=top_resolved,
                    side=PCB_SurfaceSide.TOP,
                )
            )
            board_views["top_view"] = render_input.pcbdoc.to_surface_svg(
                PCB_SurfaceSide.TOP,
                role_order=top_role_order,
                role_colors=top_role_colors,
                options=top_options,
                project_parameters=render_input.project_parameters,
            )

        bottom_resolved = resolved_by_source.get("bottom")
        if bottom_resolved is not None:
            bottom_options, bottom_role_order, bottom_role_colors = (
                _build_core_surface_view_options(
                    resolved=bottom_resolved,
                    side=PCB_SurfaceSide.BOTTOM,
                )
            )
            board_views["bottom_view"] = render_input.pcbdoc.to_surface_svg(
                PCB_SurfaceSide.BOTTOM,
                role_order=bottom_role_order,
                role_colors=bottom_role_colors,
                options=bottom_options,
                project_parameters=render_input.project_parameters,
                mirror_bottom_view=bool(
                    bottom_resolved["render_kwargs"]["mirror_bottom_view"]
                ),
            )

        rendered[render_input.board_key] = board_views

    return rendered


def _cmd_pcb_svg_from_inputs(
    args,
    input_files: list[Path],
    output_dir: Path,
    config_by_input: dict[Path, PcbSvgConfig],
) -> int:
    """
    Handle EG-06 PCB SVG export workflows using config-driven view definitions.
    """
    from altium_cruncher.altium_cruncher_pcb_assembly_svg_renderer import (
        render_pcb_assembly_svg_views,
    )
    from altium_cruncher.altium_cruncher_pcb_workflow import (
        load_design_for_pcb_input,
    )

    total_written = 0
    for input_file in input_files:
        resolved_input = input_file.resolve()
        config = config_by_input.get(resolved_input)
        if config is None:
            log.error(f"No pcb-svg config resolved for input: {resolved_input}")
            return 1
        global_options = config.global_options

        enabled_views = [view for view in config.views if view.enabled]
        if not enabled_views:
            log.error(
                f"No enabled views configured in pcb-svg config for {input_file.name}"
            )
            return 1

        content_views = [
            view
            for view in enabled_views
            if view.source
            in {"layers", "top", "bottom", "assembly-top", "assembly-bottom"}
        ]
        if not content_views:
            log.error(
                f"No renderable views selected in pcb-svg config for {input_file.name}"
            )
            return 1

        suffix = input_file.suffix.lower()
        if suffix not in {".prjpcb", ".pcbdoc"}:
            log.error(f"Unsupported PCB SVG input type: {suffix}")
            log.info("Supported PCB SVG types: .PcbDoc, .PrjPcb")
            return 1
        try:
            design, design_source = load_design_for_pcb_input(input_file)
        except Exception as exc:
            log.error(f"Error loading design context for {input_file.name}: {exc}")
            return 1
        if suffix == ".pcbdoc":
            log.info(
                "pcb-svg design context for %s: %s",
                input_file.name,
                design_source,
            )

        rendered_for_files: dict[str, dict[str, str]] = {}
        layer_filter_manifest_value: list[str] | str = "auto:copper+silkscreen"
        view_mirror_by_source: dict[str, bool] = {
            "bottom": bool(global_options.mirror_bottom_view),
            "assembly-bottom": bool(global_options.mirror_bottom_view),
        }
        view_description_by_source: dict[str, str] = {}
        view_name_by_source: dict[str, str] = {}
        output_name_by_source: dict[str, str] = {
            "layers": "layers",
            "top": "top_view",
            "bottom": "bottom_view",
            "assembly-top": "assembly_top_view",
            "assembly-bottom": "assembly_bottom_view",
            "assembly-top-simple": "assembly_top_simple_view",
            "assembly-bottom-simple": "assembly_bottom_simple_view",
        }
        seen_sources: set[str] = set()
        view_key_to_source = {
            "top_view": "top",
            "bottom_view": "bottom",
            "assembly_top_view": "assembly-top",
            "assembly_bottom_view": "assembly-bottom",
            "assembly_top_simple_view": "assembly-top-simple",
            "assembly_bottom_simple_view": "assembly-bottom-simple",
        }
        manifest_source_by_source = {
            "assembly-top-simple": "assembly-top",
            "assembly-bottom-simple": "assembly-bottom",
        }
        top_palette_resolved: dict[str, Any] | None = None
        top_view_for_palette = next(
            (view for view in content_views if view.source == "top"), None
        )
        if top_view_for_palette is not None:
            try:
                top_palette_resolved = _resolve_view_render_settings(
                    global_options, top_view_for_palette
                )
            except ValueError as exc:
                log.error(f"Invalid pcb-svg config in {input_file.name}: {exc}")
                return 1
        bottom_palette_resolved: PcbSvgResolvedSettings | None = None
        bottom_view_for_palette = next(
            (view for view in content_views if view.source == "bottom"), None
        )
        if bottom_view_for_palette is not None:
            try:
                bottom_palette_resolved = _resolve_view_render_settings(
                    global_options, bottom_view_for_palette
                )
            except ValueError as exc:
                log.error(f"Invalid pcb-svg config in {input_file.name}: {exc}")
                return 1

        for view in content_views:
            source = view.source
            if source in seen_sources:
                log.error(
                    "pcb-svg config defines multiple enabled views for source "
                    f"'{source}' in {input_file.name}; keep one per source."
                )
                return 1
            seen_sources.add(source)
            try:
                resolved = _resolve_view_render_settings(
                    global_options,
                    view,
                    default_svg_scale=getattr(args, "pcb_svg_scale", None),
                )
            except ValueError as exc:
                log.error(f"Invalid pcb-svg config in {input_file.name}: {exc}")
                return 1

            view_name_by_source[source] = view.name
            output_name_by_source[source] = _sanitize_layer_output_name(view.name)
            if source == "assembly-top":
                detail_folder = output_name_by_source[source]
                output_name_by_source["assembly-top-simple"] = (
                    f"{detail_folder[:-5]}_simple_view"
                    if detail_folder.endswith("_view")
                    else f"{detail_folder}_simple"
                )
            elif source == "assembly-bottom":
                detail_folder = output_name_by_source[source]
                output_name_by_source["assembly-bottom-simple"] = (
                    f"{detail_folder[:-5]}_simple_view"
                    if detail_folder.endswith("_view")
                    else f"{detail_folder}_simple"
                )
            description = _coerce_optional_str(resolved.get("description"))
            if description:
                view_description_by_source[source] = description

            if source == "layers":
                resolved_layer_filter: list[str] | str = (
                    sorted(layer.name for layer in resolved["visible_layers"])
                    if resolved["visible_layers"] is not None
                    else "auto:copper+silkscreen"
                )
                if resolved["render_kwargs"]["include_board_cutout_layer"]:
                    if isinstance(resolved_layer_filter, list):
                        resolved_layer_filter.append("BOARD_CUTOUTS")
                    else:
                        resolved_layer_filter = f"{resolved_layer_filter}+BOARD_CUTOUTS"
                layer_filter_manifest_value = resolved_layer_filter
            if source in {"bottom", "assembly-bottom"}:
                view_mirror_by_source[source] = bool(
                    resolved["render_kwargs"]["mirror_bottom_view"]
                )

            try:
                view_color_kwargs = _view_color_kwargs_for_source(
                    source,
                    resolved,
                    top_palette=top_palette_resolved,
                    bottom_palette=bottom_palette_resolved,
                )
                render_kwargs = dict(resolved["render_kwargs"])
                if source in {"layers", "top", "bottom"}:
                    rendered_chunk = _render_core_pcb_svg_views(
                        design,
                        resolved_by_source={source: resolved},
                    )
                else:
                    rendered_chunk = render_pcb_assembly_svg_views(
                        design,
                        views={source},
                        svg_display_scale=float(resolved["svg_scale"]),
                        svg_size_unit=str(resolved["svg_size_unit"]),
                        **render_kwargs,
                        **view_color_kwargs,
                    )
            except Exception as exc:
                log.error(
                    f"Error rendering PCB view '{view.name}' ({source}) for {input_file.name}: {exc}"
                )
                return 1
            _merge_rendered_views(rendered_for_files, rendered_chunk)

        board_names = sorted(rendered_for_files.keys())
        if not board_names:
            log.warning(f"No PCB views were generated for input {input_file.name}")
            continue

        clean_output_enabled = bool(global_options.clean_output) or bool(
            getattr(args, "pcb_clean_output", False)
        )
        skip_sidecar_json = bool(getattr(args, "pcb_skip_sidecar_json", False))

        for board_name in board_names:
            view_map = rendered_for_files.get(board_name, {})
            stale_view_folders = {
                "layers",
                "top_view",
                "bottom_view",
                "assembly_top_view",
                "assembly_bottom_view",
                "assembly_top_simple_view",
                "assembly_bottom_simple_view",
                output_name_by_source["layers"],
                output_name_by_source["top"],
                output_name_by_source["bottom"],
                output_name_by_source["assembly-top"],
                output_name_by_source["assembly-bottom"],
                output_name_by_source["assembly-top-simple"],
                output_name_by_source["assembly-bottom-simple"],
            }
            sidecar_paths = [
                output_dir / f"{board_name}__views.json",
                output_dir / f"{board_name}__view.json",
            ]
            for folder in sorted(stale_view_folders):
                sidecar_paths.append(output_dir / folder / f"{board_name}__view.json")

            if clean_output_enabled:
                stale_paths = list(sidecar_paths)
                for folder in sorted(stale_view_folders):
                    stale_paths.append(
                        output_dir / folder / f"{board_name}__{folder}.svg"
                    )
                for stale in stale_paths:
                    stale.unlink(missing_ok=True)
                for folder in sorted(stale_view_folders):
                    for stale_layer in (output_dir / folder).glob(
                        f"{board_name}__*.svg"
                    ):
                        stale_layer.unlink(missing_ok=True)
            elif skip_sidecar_json:
                for stale in sidecar_paths:
                    stale.unlink(missing_ok=True)

            output_dir.mkdir(parents=True, exist_ok=True)

            view_manifest: dict[str, Any] = {
                "schema": "wn.pcb.svg.eg06.view_manifest.v1",
                "board": board_name,
                "source_input": input_file.name,
                "views": {},
            }

            def _enrich_view_entry(
                entry: dict[str, Any], *, source: str
            ) -> dict[str, Any]:
                configured_name = view_name_by_source.get(source)
                if configured_name:
                    entry["name"] = configured_name
                description = view_description_by_source.get(source)
                if description:
                    entry["description"] = description
                return entry

            layers_folder = output_name_by_source["layers"]
            layers_written: list[str] = []
            for view_key, svg_text in sorted(view_map.items()):
                if view_key.startswith("layer_"):
                    layer_name = view_key[len("layer_") :]
                    layer_safe = _sanitize_layer_output_name(layer_name)
                    layer_dir = output_dir / layers_folder
                    layer_dir.mkdir(parents=True, exist_ok=True)
                    layer_file = layer_dir / f"{board_name}__{layer_safe}.svg"
                    layer_file.write_text(svg_text, encoding="utf-8")
                    layers_written.append(layer_file.name)
                    total_written += 1
                    continue

                source = view_key_to_source.get(view_key)
                if source is not None:
                    view_folder = output_name_by_source[source]
                    view_dir = output_dir / view_folder
                    view_dir.mkdir(parents=True, exist_ok=True)
                    view_file = view_dir / f"{board_name}__{view_folder}.svg"
                    view_file.write_text(svg_text, encoding="utf-8")
                    manifest_source = manifest_source_by_source.get(source, source)
                    view_entry: dict[str, Any] = {
                        "folder": view_folder,
                        "file": view_file.name,
                    }
                    if source in {
                        "bottom",
                        "assembly-bottom",
                        "assembly-bottom-simple",
                    }:
                        view_entry["mirrored"] = bool(
                            view_mirror_by_source.get(
                                source, global_options.mirror_bottom_view
                            )
                        )
                    if source.endswith("-simple"):
                        view_entry["mode"] = "simple"
                    elif source in {"assembly-top", "assembly-bottom"}:
                        view_entry["mode"] = "detail"
                    view_manifest["views"][view_key] = _enrich_view_entry(
                        view_entry,
                        source=manifest_source,
                    )
                    total_written += 1
                    continue

            if layers_written:
                view_manifest["views"]["layers"] = _enrich_view_entry(
                    {
                        "folder": layers_folder,
                        "files": sorted(layers_written),
                        "layer_filter": layer_filter_manifest_value,
                    },
                    source="layers",
                )
                if not skip_sidecar_json:
                    (
                        output_dir / layers_folder / f"{board_name}__view.json"
                    ).write_text(
                        json.dumps(view_manifest["views"]["layers"], indent=2),
                        encoding="utf-8",
                    )
                    total_written += 1

            if not skip_sidecar_json:
                for key in (
                    "top_view",
                    "bottom_view",
                    "assembly_top_view",
                    "assembly_bottom_view",
                    "assembly_top_simple_view",
                    "assembly_bottom_simple_view",
                ):
                    info = view_manifest["views"].get(key)
                    if info:
                        folder = str(info.get("folder") or key)
                        (output_dir / folder / f"{board_name}__view.json").write_text(
                            json.dumps(info, indent=2),
                            encoding="utf-8",
                        )
                        total_written += 1

            if not skip_sidecar_json:
                (output_dir / f"{board_name}__views.json").write_text(
                    json.dumps(view_manifest, indent=2),
                    encoding="utf-8",
                )
                total_written += 1
            log.info(f"Rendered PCB views for {board_name} into {output_dir}")

    log.info(f"Successfully generated {total_written} PCB artifact file(s)")
    return 0


def resolve_pcb_svg_configs(
    args,
    input_files: list[Path],
) -> tuple[dict[Path, PcbSvgConfig], list[Path]]:
    """
    Public wrapper for resolving pcb-svg config payloads.
    """
    return _resolve_pcb_svg_configs(args, input_files)


def render_pcb_views_from_inputs(
    args,
    input_files: list[Path],
    output_dir: Path,
    config_by_input: dict[Path, PcbSvgConfig],
) -> int:
    """
    Public wrapper for executing PCB view rendering from resolved inputs/config.
    """
    return _cmd_pcb_svg_from_inputs(args, input_files, output_dir, config_by_input)


def cmd_pcb_svg(args) -> int:
    """
    Handle pcb-svg subcommand - generate PCB SVG views from PcbDoc/PrjPcb.
    """
    input_files: list[Path] = []
    if args.file:
        input_file = Path(args.file).resolve()
        if not input_file.exists():
            log.error(f"File not found: {input_file}")
            return 1
        suffix = input_file.suffix.lower()
        if suffix not in {".pcbdoc", ".prjpcb"}:
            log.error(f"Unsupported file type: {suffix}")
            log.info("Supported PCB SVG types: .PcbDoc, .PrjPcb")
            return 1
        input_files = [input_file]
    else:
        prjpcbs = find_prjpcbs_in_cwd()
        if prjpcbs:
            input_files = prjpcbs
            log.info(
                f"Auto-detected {len(prjpcbs)} project file(s) for PCB SVG generation"
            )
        else:
            pcbdocs = find_pcbdocs_in_cwd()
            if pcbdocs:
                input_files = pcbdocs
                log.info(
                    f"Auto-detected {len(pcbdocs)} standalone PcbDoc file(s) for PCB SVG generation"
                )
            else:
                log.error(
                    "No file specified and no .PrjPcb/.PcbDoc found in current directory"
                )
                log.info(
                    "Usage: altium-cruncher pcb-svg [project.PrjPcb | board.PcbDoc]"
                )
                return 1

    try:
        config_by_input, created_configs = resolve_pcb_svg_configs(args, input_files)
    except ValueError as exc:
        log.error(str(exc))
        return 1

    if created_configs:
        for config_path in created_configs:
            log.info(f"Created pcb-svg config template: {config_path}")
        log.info("pcb-svg config template created and defaulted for this invocation.")

    output_dir = _resolve_output_dir(args.output, "pcb-svg")
    return render_pcb_views_from_inputs(args, input_files, output_dir, config_by_input)


def add_pcb_svg_option_arguments(parser, *, include_legacy_pcb_flag: bool = False):
    """
    Add PCB SVG option flags to an argparse parser.

    This is shared by `pcb-svg` and legacy `svg`.
    """
    if include_legacy_pcb_flag:
        parser.add_argument(
            "--pcb",
            action="store_true",
            help="legacy compatibility flag for svg shortcut (no-op for pcb-svg)",
        )
    parser.add_argument(
        "--config",
        type=Path,
        help=(
            "path to pcb-svg JSON config. "
            "If omitted, pcb-svg looks for pcb-svg.json next to each input file; "
            "if missing, it creates a template and exits."
        ),
    )
    parser.add_argument(
        "--doc",
        "--pcbdoc",
        dest="pcbdoc",
        type=str,
        help="with .PrjPcb input, select a specific PcbDoc by filename, stem, or relative path",
    )
    parser.add_argument(
        "--views",
        "--pcb-views",
        dest="pcb_views",
        type=str,
        help=(
            "comma-separated PCB view set: "
            "layers,top,bottom,assembly-top,assembly-bottom "
            "(plus all/none aliases). Default: all"
        ),
    )
    parser.add_argument(
        "--export",
        "--pcb-export",
        dest="pcb_export",
        choices=["board", "layers", "bundle", "outline"],
        default="board",
        help="PCB export mode: board, layers, bundle (board+outline+layers), or outline (default: board)",
    )
    parser.add_argument(
        "--layers",
        "--pcb-layers",
        dest="pcb_layers",
        type=str,
        help="comma-separated PCB layer selectors (IDs, L-prefixed IDs, or names like TOP, BOTTOM, TOPOVERLAY)",
    )
    parser.add_argument(
        "--show-empty-layers",
        "--pcb-show-empty-layers",
        dest="pcb_show_empty_layers",
        action="store_true",
        help="include empty layer outputs for PCB layer exports",
    )
    parser.add_argument(
        "--no-board-outline",
        "--pcb-no-board-outline",
        dest="pcb_no_board_outline",
        action="store_true",
        help="omit board outline geometry from PCB board/layer SVG outputs",
    )
    parser.add_argument(
        "--include-outline-in-layers",
        "--pcb-include-outline-in-layers",
        dest="pcb_include_outline_in_layers",
        action="store_true",
        help="include board-outline geometry in per-layer PCB SVG outputs (default)",
    )
    parser.add_argument(
        "--no-outline-in-layers",
        "--pcb-no-outline-in-layers",
        dest="pcb_include_outline_in_layers",
        action="store_false",
        help="omit board-outline geometry from per-layer PCB SVG outputs",
    )
    parser.add_argument(
        "--no-metadata",
        "--no-pcb-metadata",
        dest="no_pcb_metadata",
        action="store_true",
        help="disable PCB SVG metadata enrichment attributes",
    )
    parser.add_argument(
        "--include-polygon-definitions",
        "--include-pcb-polygon-definitions",
        dest="include_pcb_polygon_definitions",
        action="store_true",
        help="include dashed polygon definition overlays from Polygons6 data",
    )
    parser.add_argument(
        "--mono-color",
        "--pcb-mono-color",
        dest="pcb_mono_color",
        type=str,
        help="set one color for all PCB geometry (also used for layer SVGs and board outline unless explicitly overridden)",
    )
    parser.add_argument(
        "--all-layers-color",
        "--pcb-all-layers-color",
        dest="pcb_all_layers_color",
        type=str,
        help="override composite-board PCB layer colors with a single color",
    )
    parser.add_argument(
        "--layer-svg-color",
        "--pcb-layer-svg-color",
        dest="pcb_layer_svg_color",
        type=str,
        help="override per-layer PCB SVG geometry color",
    )
    parser.add_argument(
        "--board-outline-color",
        "--pcb-board-outline-color",
        dest="pcb_board_outline_color",
        type=str,
        help="override PCB board-outline stroke color",
    )
    parser.add_argument(
        "--scale",
        dest="pcb_svg_scale",
        type=float,
        default=None,
        help=(
            "display scale multiplier for SVG width/height attrs for layer/top/bottom outputs "
            f"(default: {PCB_DEFAULT_SVG_SCALE})"
        ),
    )
    parser.add_argument(
        "--svg-size-unit",
        "--pcb-svg-size-unit",
        dest="pcb_svg_size_unit",
        type=str,
        default="",
        help="optional size unit suffix for SVG width/height attrs (e.g. mm, px)",
    )
    parser.add_argument(
        "--drill-mode",
        "--pcb-drill-mode",
        dest="pcb_drill_mode",
        choices=["knockout", "overlay", "none"],
        default="overlay",
        help="PCB drill hole rendering mode (default: overlay)",
    )
    parser.add_argument(
        "--drill-overlay-plated-color",
        "--pcb-drill-overlay-plated-color",
        dest="pcb_drill_overlay_plated_color",
        type=str,
        help="overlay color for plated drill holes when --pcb-drill-mode overlay",
    )
    parser.add_argument(
        "--drill-overlay-non-plated-color",
        "--pcb-drill-overlay-non-plated-color",
        dest="pcb_drill_overlay_non_plated_color",
        type=str,
        help="overlay color for non-plated drill holes when --pcb-drill-mode overlay",
    )
    parser.add_argument(
        "--drill-overlay-opacity",
        "--pcb-drill-overlay-opacity",
        dest="pcb_drill_overlay_opacity",
        type=float,
        default=0.25,
        help="overlay opacity for PCB drill holes (0-1, default: 0.25)",
    )
    parser.add_argument(
        "--no-mirror-bottom",
        "--pcb-no-mirror-bottom",
        dest="pcb_no_mirror_bottom",
        action="store_true",
        help="disable bottom-view mirroring (default is mirrored-for-view)",
    )
    parser.add_argument(
        "--clip-copper-to-outline",
        "--pcb-clip-copper-to-outline",
        dest="pcb_clip_copper_to_outline",
        action="store_true",
        help="legacy override: retained for compatibility (EG-06 clipping defaults are enabled)",
    )
    parser.add_argument(
        "--clip-holes-from-copper",
        "--pcb-clip-holes-from-copper",
        dest="pcb_clip_holes_from_copper",
        action="store_true",
        help="legacy override: retained for compatibility (EG-06 hole clipping defaults are enabled)",
    )
    parser.add_argument(
        "--no-clip-to-outline",
        "--pcb-no-clip-to-outline",
        dest="pcb_no_clip_to_outline",
        action="store_true",
        help="disable board-outline clipping (default: clip all exported layers to board outline)",
    )
    parser.add_argument(
        "--no-hole-clipping",
        "--pcb-no-hole-clipping",
        dest="pcb_no_hole_clipping",
        action="store_true",
        help="disable drill-hole clipping from copper (default: enabled)",
    )
    parser.add_argument(
        "--clean-output",
        "--pcb-clean-output",
        dest="pcb_clean_output",
        action="store_true",
        help="remove existing board output files in the output directory before writing PCB outputs",
    )
    parser.set_defaults(pcb_include_outline_in_layers=True)


def register_parser(subparsers):
    pcb_svg_parser = subparsers.add_parser(
        "pcb-svg",
        help="generate PCB SVG views from Altium PcbDoc/PrjPcb",
        description=(
            "Generate PCB SVG outputs from Altium PcbDoc or PrjPcb inputs. "
            "Rendering is driven by pcb-svg JSON config. "
            "SVG outputs are contract-only (geometry + metadata); "
            "presentation text should be added by downstream viewers/reports."
        ),
        epilog="Examples:\n"
        "  altium-cruncher pcb-svg board.PcbDoc\n"
        "  altium-cruncher pcb-svg project.PrjPcb --config pcb-svg.json\n"
        "  altium-cruncher pcb-svg board.PcbDoc --config custom_pcb_svg.json\n"
        "  altium-cruncher pcb-svg                              # Auto-detect PrjPcb/PcbDoc in CWD\n"
        "  altium-cruncher pcb-svg board.PcbDoc -o output_dir/",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    pcb_svg_parser.add_argument(
        "file",
        nargs="?",
        help="PcbDoc or PrjPcb file (optional if auto-detected in CWD)",
    )
    pcb_svg_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output directory (default: ./output/pcb-svg)",
    )
    add_pcb_svg_option_arguments(pcb_svg_parser, include_legacy_pcb_flag=False)
    pcb_svg_parser.set_defaults(handler=cmd_pcb_svg)
    return pcb_svg_parser
