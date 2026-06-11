"""Generate a STEP alignment model for one PCB layer."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field, replace
import fnmatch
import json
import logging
import math
from pathlib import Path
from typing import Any

from altium_monkey.altium_board import BoardOutlineVertex, resolve_outline_arc_segment
from altium_monkey.altium_pcb_enums import PadShape
from altium_monkey.altium_record_types import PcbLayer
from altium_monkey.altium_svg_arc_helpers import choose_svg_sweep_flag_for_center

from altium_cruncher.config_json import load_json_config
from altium_cruncher.altium_cruncher_pcb_layer_step_config import (
    pcb_layer_step_default_config_text,
    resolve_pcb_layer_selector,
)
from altium_cruncher.altium_cruncher_pcb_layer_step_highlights import (
    PcbLayerStepHighlight,
    highlight_bodies_from_geometries,
)
from altium_cruncher.altium_cruncher_pcb_layer_step_utils import (
    _board_name_from_pcbdoc,
    _dedupe_closed_points,
    _iu_to_mils,
    _mils_to_mm,
    _octagon_points,
    _points_close,
    _step_name,
    layer_step_output_name as layer_step_output_name,
)
from altium_cruncher import altium_cruncher_pcb_layer_step_origin as step_origin

log = logging.getLogger(__name__)

DEFAULT_COPPER_COLOR = "#B87333"
DEFAULT_OUTLINE_COLOR = "#FFFF00"
DEFAULT_BOARD_CUTOUT_COLOR = "#FFFF00"
DEFAULT_DRILL_HOLE_COLOR = "#FFFFFF"
DEFAULT_MAX_BOOLEAN_DRILL_CUTS = 128
PCB_LAYER_STEP_CONFIG_FILENAME = "pcb-layer-step.jsonc"
PCB_LAYER_STEP_LEGACY_CONFIG_FILENAME = "pcb-layer-step.json"
PCB_LAYER_STEP_CONFIG_SCHEMA = "wn.altium_cruncher.pcb_layer_step.config.v1"
PCB_LAYER_STEP_CONFIG_SCHEMA_V2 = "wn.altium_cruncher.pcb_layer_step.config.v2"
DEFAULT_PAD_THICKNESS_BIAS_MM = 0.010
DEFAULT_VIA_THICKNESS_BIAS_MM = 0.006
DEFAULT_POLYGON_THICKNESS_BIAS_MM = 0.003
DEFAULT_TRACE_THICKNESS_BIAS_MM = 0.0
DRILL_HOLE_MODE_AUTO = "auto"
DRILL_HOLE_MODE_CUT = "cut"
DRILL_HOLE_MODE_OVERLAY = "overlay"
DRILL_HOLE_MODE_NONE = "none"
DRILL_SCOPE_MODE_INHERIT = "inherit"
DRILL_HOLE_SHAPE_SOLID = "solid"
DRILL_HOLE_SHAPE_RING = "ring"
DRILL_HOLE_SHAPES = frozenset({DRILL_HOLE_SHAPE_SOLID, DRILL_HOLE_SHAPE_RING})
DRILL_PLATED_RING_SHAPE_ANNULUS = "annulus"
DRILL_PLATED_RING_SHAPES = frozenset(("annulus",))
_NON_COPPER_BODY_IDS = frozenset(
    {
        "board_outline",
        "board_cutouts",
        "drill_holes",
        "plated_drill_holes",
        "non_plated_drill_holes",
    }
)
DRILL_HOLE_MODES = frozenset(
    {
        DRILL_HOLE_MODE_AUTO,
        DRILL_HOLE_MODE_CUT,
        DRILL_HOLE_MODE_OVERLAY,
        DRILL_HOLE_MODE_NONE,
    }
)
DRILL_SCOPE_MODES = frozenset(
    {
        DRILL_SCOPE_MODE_INHERIT,
        DRILL_HOLE_MODE_CUT,
        DRILL_HOLE_MODE_OVERLAY,
        DRILL_HOLE_MODE_NONE,
    }
)
_COLOR_NAMES = {
    "black": "#000000",
    "blue": "#0000FF",
    "brown": "#A52A2A",
    "copper": DEFAULT_COPPER_COLOR,
    "gray": "#808080",
    "green": "#008000",
    "grey": "#808080",
    "orange": "#FFA500",
    "purple": "#800080",
    "red": "#FF0000",
    "white": "#FFFFFF",
    "yellow": "#FFFF00",
}


@dataclass(frozen=True, slots=True)
class _PadColorRule:
    designators: tuple[str, ...]
    color: str
    step_body_name: str = "matched_pads"


@dataclass(frozen=True, slots=True)
class PcbLayerStepOptions:
    """Options for one-layer PCB STEP export."""

    layer: PcbLayer = PcbLayer.BOTTOM
    thickness_mm: float = 0.035
    z_mm: float = 0.0
    copper_color: str = DEFAULT_COPPER_COLOR
    outline_width_mm: float = 0.2
    outline_color: str = DEFAULT_OUTLINE_COLOR
    board_cutout_color: str = DEFAULT_BOARD_CUTOUT_COLOR
    include_board_cutouts: bool = True
    include_copper: bool = True
    include_board_outline: bool = True
    include_poured_polygons: bool = True
    cut_holes: bool = True
    drill_hole_mode: str = DRILL_HOLE_MODE_AUTO
    max_boolean_drill_cuts: int = DEFAULT_MAX_BOOLEAN_DRILL_CUTS
    drill_hole_color: str = DEFAULT_DRILL_HOLE_COLOR
    drill_plated_hole_color: str = DEFAULT_DRILL_HOLE_COLOR
    drill_non_plated_hole_color: str = DEFAULT_DRILL_HOLE_COLOR
    drill_overlay_thickness_mm: float = 0.001
    drill_minimum_diameter_mm: float = 0.0
    drill_hole_shape: str = DRILL_HOLE_SHAPE_SOLID
    drill_ring_width_mm: float = 0.12
    drill_plated_ring_shape: str = DRILL_PLATED_RING_SHAPE_ANNULUS
    drill_selected_component_mode: str = DRILL_SCOPE_MODE_INHERIT
    drill_other_component_mode: str = DRILL_SCOPE_MODE_INHERIT
    drill_free_pad_mode: str = DRILL_SCOPE_MODE_INHERIT
    drill_via_mode: str = DRILL_SCOPE_MODE_INHERIT
    fuse_copper: bool = True
    fuse_board_outline: bool = True
    arc_segments: int = 32
    include_tracks: bool = True
    include_arcs: bool = True
    include_fills: bool = True
    include_regions: bool = True
    include_vias: bool = True
    include_component_pads: bool = True
    include_free_pads: bool = True
    include_designators: tuple[str, ...] = ()
    pad_color_rules: tuple[_PadColorRule, ...] = ()
    track_color: str | None = None
    track_body: str = "tracks"
    arc_color: str | None = None
    arc_body: str = "arcs"
    fill_color: str | None = None
    fill_body: str = "fills"
    polygon_color: str | None = None
    polygon_body: str = "polygons"
    region_color: str | None = None
    region_body: str = "regions"
    via_color: str | None = None
    via_body: str = "vias"
    component_pad_color: str | None = None
    component_pad_body: str = "component_pads"
    free_pad_color: str | None = None
    free_pad_body: str = "free_pads"
    track_thickness_bias_mm: float = DEFAULT_TRACE_THICKNESS_BIAS_MM
    arc_thickness_bias_mm: float = DEFAULT_TRACE_THICKNESS_BIAS_MM
    fill_thickness_bias_mm: float = DEFAULT_TRACE_THICKNESS_BIAS_MM
    polygon_thickness_bias_mm: float = DEFAULT_POLYGON_THICKNESS_BIAS_MM
    region_thickness_bias_mm: float = DEFAULT_POLYGON_THICKNESS_BIAS_MM
    via_thickness_bias_mm: float = DEFAULT_VIA_THICKNESS_BIAS_MM
    component_pad_thickness_bias_mm: float = DEFAULT_PAD_THICKNESS_BIAS_MM
    free_pad_thickness_bias_mm: float = DEFAULT_PAD_THICKNESS_BIAS_MM
    highlights: tuple["PcbLayerStepHighlight", ...] = ()


@dataclass(frozen=True, slots=True)
class PcbLayerStepResult:
    """Summary of a generated one-layer PCB STEP export."""

    output_path: Path
    manifest_path: Path
    board_name: str
    layer: str
    copper_body_count: int
    outline_body_count: int
    drill_cut_count: int
    source_input: str | None


def _coerce_optional_str(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _coerce_str(value: object, default: str) -> str:
    if value is None:
        return default
    return str(value)


def _coerce_color(value: object, default: str) -> str:
    text = _coerce_str(value, default).strip()
    named = _COLOR_NAMES.get(text.casefold())
    return named or text


def _coerce_optional_color(value: object) -> str | None:
    if value is None:
        return None
    return _coerce_color(value, DEFAULT_COPPER_COLOR)


def _coerce_str_tuple(value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        text = value.strip()
        return (text,) if text else ()
    if isinstance(value, Iterable):
        return tuple(text for item in value if (text := str(item).strip()))
    raise ValueError(f"Invalid string list in pcb-layer-step config: {value!r}")


def _coerce_float(value: object, default: float) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"Invalid numeric value in pcb-layer-step config: {value!r}"
        ) from exc


def _coerce_bool(value: object, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, int | float):
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "y", "on"}:
            return True
        if normalized in {"0", "false", "no", "n", "off"}:
            return False
    raise ValueError(f"Invalid boolean value in pcb-layer-step config: {value!r}")


def _coerce_drill_hole_mode(value: object, *, cut_holes: bool) -> str:
    """Return the configured drill-hole rendering strategy."""
    if value is None:
        return DRILL_HOLE_MODE_AUTO if cut_holes else DRILL_HOLE_MODE_NONE
    normalized = str(value).strip().casefold().replace("-", "_")
    aliases = {
        "boolean": DRILL_HOLE_MODE_CUT,
        "boolean_cut": DRILL_HOLE_MODE_CUT,
        "cutout": DRILL_HOLE_MODE_CUT,
        "cutouts": DRILL_HOLE_MODE_CUT,
        "cuts": DRILL_HOLE_MODE_CUT,
        "off": DRILL_HOLE_MODE_NONE,
        "omit": DRILL_HOLE_MODE_NONE,
    }
    mode = aliases.get(normalized, normalized)
    if mode not in DRILL_HOLE_MODES:
        raise ValueError(f"Invalid drill_hole_mode in pcb-layer-step config: {value!r}")
    return mode


def _coerce_drill_hole_shape(value: object, default: str) -> str:
    if value is None:
        return default
    shape = str(value).strip().casefold().replace("-", "_")
    if shape not in DRILL_HOLE_SHAPES:
        raise ValueError(
            f"Invalid drill_hole_shape in pcb-layer-step config: {value!r}"
        )
    return shape


def _coerce_drill_plated_ring_shape(value: object, default: str) -> str:
    if value is None:
        return default
    normalized = str(value).strip().casefold().replace("-", "_")
    aliases = {
        "hole": DRILL_PLATED_RING_SHAPE_ANNULUS,
        "drill": DRILL_PLATED_RING_SHAPE_ANNULUS,
    }
    shape = aliases.get(normalized, normalized)
    if shape not in DRILL_PLATED_RING_SHAPES:
        raise ValueError(
            f"Invalid drill plated ring shape in pcb-layer-step config: {value!r}"
        )
    return shape


def _coerce_drill_scope_mode(value: object, default: str) -> str:
    if value is None:
        return default
    normalized = str(value).strip().casefold().replace("-", "_")
    aliases = {
        "default": DRILL_SCOPE_MODE_INHERIT,
        "global": DRILL_SCOPE_MODE_INHERIT,
        "off": DRILL_HOLE_MODE_NONE,
        "omit": DRILL_HOLE_MODE_NONE,
        "boolean": DRILL_HOLE_MODE_CUT,
        "boolean_cut": DRILL_HOLE_MODE_CUT,
        "cutout": DRILL_HOLE_MODE_CUT,
        "cutouts": DRILL_HOLE_MODE_CUT,
        "cuts": DRILL_HOLE_MODE_CUT,
    }
    mode = aliases.get(normalized, normalized)
    if mode not in DRILL_SCOPE_MODES:
        raise ValueError(
            f"Invalid scoped drill mode in pcb-layer-step config: {value!r}"
        )
    return mode


def _coerce_pad_highlight_rules(value: object) -> tuple[_PadColorRule, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ValueError(
            "pcb-layer-step config field "
            "'features.component_pads.highlight_rules' must be a list"
        )
    rules: list[_PadColorRule] = []
    for index, raw_rule in enumerate(value):
        if not isinstance(raw_rule, dict):
            raise ValueError(
                "pcb-layer-step features.component_pads.highlight_rules"
                f"[{index}] must be an object"
            )
        designators = _coerce_str_tuple(raw_rule.get("designators"))
        if not designators:
            raise ValueError(
                "pcb-layer-step features.component_pads.highlight_rules"
                f"[{index}] requires designators"
            )
        rules.append(
            _PadColorRule(
                designators=designators,
                color=_coerce_color(raw_rule.get("color"), DEFAULT_COPPER_COLOR),
                step_body_name=str(raw_rule.get("step_body_name") or "matched_pads"),
            )
        )
    return tuple(rules)


def _config_mapping(value: object, field_name: str) -> Mapping[str, object]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise ValueError(
            f"pcb-layer-step config field '{field_name}' must be an object"
        )
    return value


def _feature_value(
    features: Mapping[str, object],
    name: str,
    *aliases: str,
) -> object:
    for key in (name, *aliases):
        if key in features:
            return features[key]
    return None


def _feature_enabled(
    *,
    features: Mapping[str, object],
    merged: Mapping[str, object],
    name: str,
    default: bool,
    legacy_key: str,
    aliases: tuple[str, ...] = (),
) -> bool:
    value = _feature_value(features, name, *aliases)
    if isinstance(value, Mapping):
        return _coerce_bool(value.get("enabled"), default)
    if value is not None:
        return _coerce_bool(value, default)
    return _coerce_bool(merged.get(legacy_key), default)


def _feature_color_and_body(
    *,
    features: Mapping[str, object],
    merged: Mapping[str, object],
    name: str,
    body_default: str,
    color_key: str,
    body_key: str,
    aliases: tuple[str, ...] = (),
) -> tuple[str | None, str]:
    color_value = None
    body_value = None
    candidate = _feature_value(features, name, *aliases)
    if isinstance(candidate, Mapping):
        color_value = candidate.get("color", color_value)
        body_value = candidate.get("step_body_name", body_value)
    elif candidate is not None and not isinstance(candidate, bool):
        color_value = candidate
    return (
        _coerce_optional_color(color_value),
        str(body_value or body_default),
    )


def _feature_thickness_bias(
    *,
    features: Mapping[str, object],
    merged: Mapping[str, object],
    name: str,
    default: float,
    legacy_key: str,
    aliases: tuple[str, ...] = (),
) -> float:
    value = None
    candidate = _feature_value(features, name, *aliases)
    if isinstance(candidate, Mapping):
        value = candidate.get("thickness_bias_mm", value)
    return _coerce_float(value, default)


def _reject_removed_config_fields(
    *,
    merged: Mapping[str, object],
    features: Mapping[str, object],
) -> None:
    _reject_removed_root_fields(merged)
    _reject_removed_feature_body_fields(features)


def _reject_removed_root_fields(merged: Mapping[str, object]) -> None:
    removed_root_fields = {
        "colors": "use features.defaults, feature color fields, and "
        "features.component_pads.highlight_rules",
        "pad_color_rules": "use features.component_pads.highlight_rules",
        "pad_rules": "use features.component_pads.highlight_rules",
        "thickness_bias": "put thickness_bias_mm on each feature entry",
        "thickness_bias_mm": "put thickness_bias_mm on each feature entry",
    }
    for field_name, replacement in removed_root_fields.items():
        if field_name in merged:
            raise ValueError(
                f"pcb-layer-step config field '{field_name}' was removed; {replacement}"
            )


def _reject_removed_feature_body_fields(features: Mapping[str, object]) -> None:
    for feature_name, raw_feature in features.items():
        if isinstance(raw_feature, Mapping) and "body" in raw_feature:
            raise ValueError(
                f"pcb-layer-step config field 'features.{feature_name}.body' "
                "was removed; use step_body_name"
            )
        if feature_name == "component_pads" and isinstance(raw_feature, Mapping):
            _reject_removed_highlight_rule_body_fields(raw_feature)


def _reject_removed_highlight_rule_body_fields(
    component_pads: Mapping[str, object],
) -> None:
    highlight_rules = component_pads.get("highlight_rules")
    if not isinstance(highlight_rules, list):
        return
    for index, rule in enumerate(highlight_rules):
        if isinstance(rule, Mapping) and "body" in rule:
            raise ValueError(
                "pcb-layer-step config field "
                f"'features.component_pads.highlight_rules[{index}].body' "
                "was removed; use step_body_name"
            )


def _merge_options(data: Mapping[str, object]) -> dict[str, object]:
    options = data.get("options")
    if options is None:
        return dict(data)
    if not isinstance(options, Mapping):
        raise ValueError("pcb-layer-step config field 'options' must be an object")
    return {**dict(data), **dict(options)}


def _root_config_defaults(data: Mapping[str, object]) -> dict[str, object]:
    return {
        key: value for key, value in data.items() if key not in {"defaults", "outputs"}
    }


def _output_config_dicts(
    data: Mapping[str, object],
) -> tuple[Mapping[str, object], ...]:
    raw_outputs = data.get("outputs")
    if not isinstance(raw_outputs, list) or not raw_outputs:
        raise ValueError(
            "pcb-layer-step config field 'outputs' must be a non-empty list"
        )
    outputs: list[Mapping[str, object]] = []
    for index, raw_output in enumerate(raw_outputs):
        if not isinstance(raw_output, Mapping):
            raise ValueError(
                f"pcb-layer-step config outputs[{index}] must be an object"
            )
        outputs.append(raw_output)
    return tuple(outputs)


def _component_pad_settings(
    *,
    features: Mapping[str, object],
    merged: Mapping[str, object],
    default: "PcbLayerStepConfig",
) -> tuple[bool, object]:
    component_pads = features.get("component_pads")
    component_pad_designators = merged.get("include_designators")
    include_component_pads = default.include_component_pads
    if isinstance(component_pads, Mapping):
        mode = str(component_pads.get("mode") or "all").strip().casefold()
        include_component_pads = mode != "none"
        if "enabled" in component_pads:
            include_component_pads = _coerce_bool(
                component_pads.get("enabled"),
                include_component_pads,
            )
        component_pad_designators = component_pads.get(
            "include_designators",
            component_pad_designators,
        )
    elif component_pads is not None:
        include_component_pads = _coerce_bool(
            component_pads,
            default.include_component_pads,
        )
    else:
        include_component_pads = _coerce_bool(
            merged.get("include_component_pads"),
            default.include_component_pads,
        )
    return include_component_pads, component_pad_designators


def _component_pad_highlight_rules(
    features: Mapping[str, object],
) -> tuple[_PadColorRule, ...]:
    component_pads = features.get("component_pads")
    if not isinstance(component_pads, Mapping):
        return ()
    return _coerce_pad_highlight_rules(component_pads.get("highlight_rules"))


def _drill_color_source(
    *,
    drills: Mapping[str, object],
    merged: Mapping[str, object],
) -> object:
    return drills.get("color", merged.get("drill_hole_color"))


def _drill_plated_color_source(
    *,
    drills: Mapping[str, object],
    merged: Mapping[str, object],
    drill_color: object,
) -> object:
    return drills.get(
        "plated_color",
        merged.get("drill_plated_hole_color", drill_color),
    )


def _drill_non_plated_color_source(
    *,
    drills: Mapping[str, object],
    merged: Mapping[str, object],
    drill_color: object,
) -> object:
    return drills.get(
        "non_plated_color",
        merged.get("drill_non_plated_hole_color", drill_color),
    )


@dataclass(frozen=True, slots=True)
class PcbLayerStepConfig:
    """JSON config for one-layer PCB STEP export."""

    schema: str = PCB_LAYER_STEP_CONFIG_SCHEMA
    name: str | None = None
    output_step: str | None = None
    pcbdoc: str | None = None
    layer: str = "bottom"
    thickness_mm: float = 0.035
    z_mm: float = 0.0
    copper_color: str = DEFAULT_COPPER_COLOR
    outline_width_mm: float = 0.2
    outline_color: str = DEFAULT_OUTLINE_COLOR
    board_cutout_color: str = DEFAULT_BOARD_CUTOUT_COLOR
    include_board_cutouts: bool = True
    include_copper: bool = True
    include_board_outline: bool = True
    include_poured_polygons: bool = True
    cut_holes: bool = True
    drill_hole_mode: str = DRILL_HOLE_MODE_AUTO
    max_boolean_drill_cuts: int = DEFAULT_MAX_BOOLEAN_DRILL_CUTS
    drill_hole_color: str = DEFAULT_DRILL_HOLE_COLOR
    drill_plated_hole_color: str = DEFAULT_DRILL_HOLE_COLOR
    drill_non_plated_hole_color: str = DEFAULT_DRILL_HOLE_COLOR
    drill_overlay_thickness_mm: float = 0.001
    drill_minimum_diameter_mm: float = 0.0
    drill_hole_shape: str = DRILL_HOLE_SHAPE_SOLID
    drill_ring_width_mm: float = 0.12
    drill_plated_ring_shape: str = DRILL_PLATED_RING_SHAPE_ANNULUS
    drill_selected_component_mode: str = DRILL_SCOPE_MODE_INHERIT
    drill_other_component_mode: str = DRILL_SCOPE_MODE_INHERIT
    drill_free_pad_mode: str = DRILL_SCOPE_MODE_INHERIT
    drill_via_mode: str = DRILL_SCOPE_MODE_INHERIT
    fuse_copper: bool = True
    fuse_board_outline: bool = True
    arc_segments: int = 32
    include_tracks: bool = True
    include_arcs: bool = True
    include_fills: bool = True
    include_regions: bool = True
    include_vias: bool = True
    include_component_pads: bool = True
    include_free_pads: bool = True
    include_designators: tuple[str, ...] = ()
    pad_color_rules: tuple[_PadColorRule, ...] = ()
    track_color: str | None = None
    track_body: str = "tracks"
    arc_color: str | None = None
    arc_body: str = "arcs"
    fill_color: str | None = None
    fill_body: str = "fills"
    polygon_color: str | None = None
    polygon_body: str = "polygons"
    region_color: str | None = None
    region_body: str = "regions"
    via_color: str | None = None
    via_body: str = "vias"
    component_pad_color: str | None = None
    component_pad_body: str = "component_pads"
    free_pad_color: str | None = None
    free_pad_body: str = "free_pads"
    track_thickness_bias_mm: float = DEFAULT_TRACE_THICKNESS_BIAS_MM
    arc_thickness_bias_mm: float = DEFAULT_TRACE_THICKNESS_BIAS_MM
    fill_thickness_bias_mm: float = DEFAULT_TRACE_THICKNESS_BIAS_MM
    polygon_thickness_bias_mm: float = DEFAULT_POLYGON_THICKNESS_BIAS_MM
    region_thickness_bias_mm: float = DEFAULT_POLYGON_THICKNESS_BIAS_MM
    via_thickness_bias_mm: float = DEFAULT_VIA_THICKNESS_BIAS_MM
    component_pad_thickness_bias_mm: float = DEFAULT_PAD_THICKNESS_BIAS_MM
    free_pad_thickness_bias_mm: float = DEFAULT_PAD_THICKNESS_BIAS_MM
    outputs: tuple["PcbLayerStepConfig", ...] = ()

    @classmethod
    def default(cls) -> "PcbLayerStepConfig":
        return cls()

    @classmethod
    def from_dict(cls, data: object) -> "PcbLayerStepConfig":
        if not isinstance(data, Mapping):
            raise ValueError("pcb-layer-step config root must be a JSON object")
        if "outputs" in data:
            return cls._from_outputs_dict(data)
        return cls._from_merged_dict(data)

    @classmethod
    def _from_outputs_dict(
        cls,
        data: Mapping[str, object],
    ) -> "PcbLayerStepConfig":
        defaults = _config_mapping(data.get("defaults"), "defaults")
        merged_defaults = {**_root_config_defaults(data), **dict(defaults)}
        schema = str(data.get("schema") or PCB_LAYER_STEP_CONFIG_SCHEMA_V2)
        outputs = tuple(
            cls._from_merged_dict(
                {**merged_defaults, **dict(raw_output)}, schema=schema
            )
            for raw_output in _output_config_dicts(data)
        )
        defaults_config = cls._from_merged_dict(merged_defaults, schema=schema)
        return replace(defaults_config, outputs=outputs)

    @classmethod
    def _from_merged_dict(
        cls,
        data: Mapping[str, object],
        *,
        schema: str | None = None,
    ) -> "PcbLayerStepConfig":
        merged = _merge_options(data)
        default = cls()
        board_outline = _config_mapping(merged.get("board_outline"), "board_outline")
        features = _config_mapping(merged.get("features"), "features")
        _reject_removed_config_fields(merged=merged, features=features)
        feature_defaults = _config_mapping(
            features.get("defaults"),
            "features.defaults",
        )
        drills = _config_mapping(merged.get("drills"), "drills")
        include_component_pads, component_pad_designators = _component_pad_settings(
            features=features,
            merged=merged,
            default=default,
        )
        track_color, track_body = _feature_color_and_body(
            features=features,
            merged=merged,
            name="tracks",
            aliases=("traces",),
            body_default="tracks",
            color_key="track_color",
            body_key="track_body",
        )
        arc_color, arc_body = _feature_color_and_body(
            features=features,
            merged=merged,
            name="arcs",
            body_default="arcs",
            color_key="arc_color",
            body_key="arc_body",
        )
        fill_color, fill_body = _feature_color_and_body(
            features=features,
            merged=merged,
            name="fills",
            body_default="fills",
            color_key="fill_color",
            body_key="fill_body",
        )
        polygon_color, polygon_body = _feature_color_and_body(
            features=features,
            merged=merged,
            name="polygons",
            aliases=("poured_polygons",),
            body_default="polygons",
            color_key="polygon_color",
            body_key="polygon_body",
        )
        region_color, region_body = _feature_color_and_body(
            features=features,
            merged=merged,
            name="regions",
            aliases=("shapebased_regions",),
            body_default="regions",
            color_key="region_color",
            body_key="region_body",
        )
        via_color, via_body = _feature_color_and_body(
            features=features,
            merged=merged,
            name="vias",
            body_default="vias",
            color_key="via_color",
            body_key="via_body",
        )
        component_pad_color, component_pad_body = _feature_color_and_body(
            features=features,
            merged=merged,
            name="component_pads",
            aliases=("pads",),
            body_default="component_pads",
            color_key="component_pad_color",
            body_key="component_pad_body",
        )
        free_pad_color, free_pad_body = _feature_color_and_body(
            features=features,
            merged=merged,
            name="free_pads",
            body_default="free_pads",
            color_key="free_pad_color",
            body_key="free_pad_body",
        )
        cut_holes = _coerce_bool(merged.get("cut_holes"), default.cut_holes)
        drill_color = _drill_color_source(drills=drills, merged=merged)
        return cls(
            schema=str(schema or merged.get("schema") or default.schema),
            name=_coerce_optional_str(merged.get("name")),
            output_step=_coerce_optional_str(merged.get("output_step")),
            pcbdoc=_coerce_optional_str(merged.get("pcbdoc")),
            layer=_coerce_str(merged.get("layer"), default.layer),
            thickness_mm=_coerce_float(
                merged.get("thickness_mm"), default.thickness_mm
            ),
            z_mm=_coerce_float(merged.get("z_mm"), default.z_mm),
            copper_color=_coerce_color(
                feature_defaults.get("color", merged.get("copper_color")),
                default.copper_color,
            ),
            outline_width_mm=_coerce_float(
                board_outline.get("width_mm", merged.get("outline_width_mm")),
                default.outline_width_mm,
            ),
            outline_color=_coerce_color(
                board_outline.get("color", merged.get("outline_color")),
                default.outline_color,
            ),
            board_cutout_color=_coerce_color(
                board_outline.get(
                    "cutout_color",
                    board_outline.get(
                        "cutouts_color",
                        merged.get("board_cutout_color"),
                    ),
                ),
                default.board_cutout_color,
            ),
            include_board_cutouts=_coerce_bool(
                board_outline.get("cutouts", merged.get("include_board_cutouts")),
                default.include_board_cutouts,
            ),
            include_copper=_coerce_bool(
                merged.get("include_copper"), default.include_copper
            ),
            include_board_outline=_coerce_bool(
                merged.get("include_board_outline"), default.include_board_outline
            ),
            include_poured_polygons=_feature_enabled(
                features=features,
                merged=merged,
                name="polygons",
                aliases=("poured_polygons",),
                legacy_key="include_poured_polygons",
                default=default.include_poured_polygons,
            ),
            cut_holes=cut_holes,
            drill_hole_mode=_coerce_drill_hole_mode(
                drills.get("mode", merged.get("drill_hole_mode")),
                cut_holes=cut_holes,
            ),
            max_boolean_drill_cuts=int(
                _coerce_float(
                    merged.get("max_boolean_drill_cuts"),
                    default.max_boolean_drill_cuts,
                )
            ),
            drill_hole_color=_coerce_color(
                drill_color,
                default.drill_hole_color,
            ),
            drill_plated_hole_color=_coerce_color(
                _drill_plated_color_source(
                    drills=drills,
                    merged=merged,
                    drill_color=drill_color,
                ),
                default.drill_plated_hole_color,
            ),
            drill_non_plated_hole_color=_coerce_color(
                _drill_non_plated_color_source(
                    drills=drills,
                    merged=merged,
                    drill_color=drill_color,
                ),
                default.drill_non_plated_hole_color,
            ),
            drill_overlay_thickness_mm=_coerce_float(
                drills.get(
                    "overlay_thickness_mm",
                    merged.get("drill_overlay_thickness_mm"),
                ),
                default.drill_overlay_thickness_mm,
            ),
            drill_minimum_diameter_mm=_coerce_float(
                drills.get(
                    "minimum_diameter_mm",
                    merged.get("drill_minimum_diameter_mm"),
                ),
                default.drill_minimum_diameter_mm,
            ),
            drill_hole_shape=_coerce_drill_hole_shape(
                drills.get("shape", merged.get("drill_hole_shape")),
                default.drill_hole_shape,
            ),
            drill_ring_width_mm=_coerce_float(
                drills.get("ring_width_mm", merged.get("drill_ring_width_mm")),
                default.drill_ring_width_mm,
            ),
            drill_plated_ring_shape=_coerce_drill_plated_ring_shape(
                drills.get(
                    "plated_ring_shape",
                    merged.get("drill_plated_ring_shape"),
                ),
                default.drill_plated_ring_shape,
            ),
            drill_selected_component_mode=_coerce_drill_scope_mode(
                drills.get(
                    "selected_component_mode",
                    merged.get("drill_selected_component_mode"),
                ),
                default.drill_selected_component_mode,
            ),
            drill_other_component_mode=_coerce_drill_scope_mode(
                drills.get(
                    "other_component_mode",
                    merged.get("drill_other_component_mode"),
                ),
                default.drill_other_component_mode,
            ),
            drill_free_pad_mode=_coerce_drill_scope_mode(
                drills.get("free_pad_mode", merged.get("drill_free_pad_mode")),
                default.drill_free_pad_mode,
            ),
            drill_via_mode=_coerce_drill_scope_mode(
                drills.get("via_mode", merged.get("drill_via_mode")),
                default.drill_via_mode,
            ),
            fuse_copper=_coerce_bool(merged.get("fuse_copper"), default.fuse_copper),
            fuse_board_outline=_coerce_bool(
                board_outline.get("fuse", merged.get("fuse_board_outline")),
                default.fuse_board_outline,
            ),
            arc_segments=int(
                _coerce_float(merged.get("arc_segments"), default.arc_segments)
            ),
            include_tracks=_feature_enabled(
                features=features,
                merged=merged,
                name="tracks",
                aliases=("traces",),
                legacy_key="include_tracks",
                default=default.include_tracks,
            ),
            include_arcs=_feature_enabled(
                features=features,
                merged=merged,
                name="arcs",
                legacy_key="include_arcs",
                default=default.include_arcs,
            ),
            include_fills=_feature_enabled(
                features=features,
                merged=merged,
                name="fills",
                legacy_key="include_fills",
                default=default.include_fills,
            ),
            include_regions=_feature_enabled(
                features=features,
                merged=merged,
                name="regions",
                aliases=("shapebased_regions",),
                legacy_key="include_regions",
                default=default.include_regions,
            ),
            include_vias=_feature_enabled(
                features=features,
                merged=merged,
                name="vias",
                legacy_key="include_vias",
                default=default.include_vias,
            ),
            include_component_pads=include_component_pads,
            include_free_pads=_feature_enabled(
                features=features,
                merged=merged,
                name="free_pads",
                legacy_key="include_free_pads",
                default=default.include_free_pads,
            ),
            include_designators=_coerce_str_tuple(component_pad_designators),
            pad_color_rules=_component_pad_highlight_rules(features),
            track_color=track_color,
            track_body=track_body,
            arc_color=arc_color,
            arc_body=arc_body,
            fill_color=fill_color,
            fill_body=fill_body,
            polygon_color=polygon_color,
            polygon_body=polygon_body,
            region_color=region_color,
            region_body=region_body,
            via_color=via_color,
            via_body=via_body,
            component_pad_color=component_pad_color,
            component_pad_body=component_pad_body,
            free_pad_color=free_pad_color,
            free_pad_body=free_pad_body,
            track_thickness_bias_mm=_feature_thickness_bias(
                features=features,
                merged=merged,
                name="tracks",
                aliases=("traces",),
                legacy_key="track_thickness_bias_mm",
                default=default.track_thickness_bias_mm,
            ),
            arc_thickness_bias_mm=_feature_thickness_bias(
                features=features,
                merged=merged,
                name="arcs",
                legacy_key="arc_thickness_bias_mm",
                default=default.arc_thickness_bias_mm,
            ),
            fill_thickness_bias_mm=_feature_thickness_bias(
                features=features,
                merged=merged,
                name="fills",
                legacy_key="fill_thickness_bias_mm",
                default=default.fill_thickness_bias_mm,
            ),
            polygon_thickness_bias_mm=_feature_thickness_bias(
                features=features,
                merged=merged,
                name="polygons",
                aliases=("poured_polygons",),
                legacy_key="polygon_thickness_bias_mm",
                default=default.polygon_thickness_bias_mm,
            ),
            region_thickness_bias_mm=_feature_thickness_bias(
                features=features,
                merged=merged,
                name="regions",
                aliases=("shapebased_regions",),
                legacy_key="region_thickness_bias_mm",
                default=default.region_thickness_bias_mm,
            ),
            via_thickness_bias_mm=_feature_thickness_bias(
                features=features,
                merged=merged,
                name="vias",
                legacy_key="via_thickness_bias_mm",
                default=default.via_thickness_bias_mm,
            ),
            component_pad_thickness_bias_mm=_feature_thickness_bias(
                features=features,
                merged=merged,
                name="component_pads",
                aliases=("pads",),
                legacy_key="component_pad_thickness_bias_mm",
                default=default.component_pad_thickness_bias_mm,
            ),
            free_pad_thickness_bias_mm=_feature_thickness_bias(
                features=features,
                merged=merged,
                name="free_pads",
                legacy_key="free_pad_thickness_bias_mm",
                default=default.free_pad_thickness_bias_mm,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "name": self.name,
            "output_step": self.output_step,
            "pcbdoc": self.pcbdoc,
            "layer": self.layer,
            "thickness_mm": self.thickness_mm,
            "z_mm": self.z_mm,
            "outline_width_mm": self.outline_width_mm,
            "outline_color": self.outline_color,
            "board_cutout_color": self.board_cutout_color,
            "include_copper": self.include_copper,
            "include_board_outline": self.include_board_outline,
            "include_board_cutouts": self.include_board_cutouts,
            "include_poured_polygons": self.include_poured_polygons,
            "cut_holes": self.cut_holes,
            "max_boolean_drill_cuts": self.max_boolean_drill_cuts,
            "fuse_copper": self.fuse_copper,
            "fuse_board_outline": self.fuse_board_outline,
            "arc_segments": self.arc_segments,
            "features": {
                "defaults": {"color": self.copper_color},
                "tracks": {
                    "enabled": self.include_tracks,
                    "color": self.track_color or self.copper_color,
                    "step_body_name": self.track_body,
                    "thickness_bias_mm": self.track_thickness_bias_mm,
                },
                "arcs": {
                    "enabled": self.include_arcs,
                    "color": self.arc_color or self.copper_color,
                    "step_body_name": self.arc_body,
                    "thickness_bias_mm": self.arc_thickness_bias_mm,
                },
                "fills": {
                    "enabled": self.include_fills,
                    "color": self.fill_color or self.copper_color,
                    "step_body_name": self.fill_body,
                    "thickness_bias_mm": self.fill_thickness_bias_mm,
                },
                "polygons": {
                    "enabled": self.include_poured_polygons,
                    "color": self.polygon_color or self.copper_color,
                    "step_body_name": self.polygon_body,
                    "thickness_bias_mm": self.polygon_thickness_bias_mm,
                },
                "regions": {
                    "enabled": self.include_regions,
                    "color": self.region_color or self.copper_color,
                    "step_body_name": self.region_body,
                    "thickness_bias_mm": self.region_thickness_bias_mm,
                },
                "vias": {
                    "enabled": self.include_vias,
                    "color": self.via_color or self.copper_color,
                    "step_body_name": self.via_body,
                    "thickness_bias_mm": self.via_thickness_bias_mm,
                },
                "component_pads": {
                    "enabled": self.include_component_pads,
                    "mode": "matching_designators"
                    if self.include_designators
                    else "all",
                    "include_designators": list(self.include_designators),
                    "color": self.component_pad_color or self.copper_color,
                    "step_body_name": self.component_pad_body,
                    "thickness_bias_mm": self.component_pad_thickness_bias_mm,
                    "highlight_rules": [
                        {
                            "designators": list(rule.designators),
                            "color": rule.color,
                            "step_body_name": rule.step_body_name,
                        }
                        for rule in self.pad_color_rules
                    ],
                },
                "free_pads": {
                    "enabled": self.include_free_pads,
                    "color": self.free_pad_color or self.copper_color,
                    "step_body_name": self.free_pad_body,
                    "thickness_bias_mm": self.free_pad_thickness_bias_mm,
                },
            },
            "drills": {
                "mode": self.drill_hole_mode,
                "minimum_diameter_mm": self.drill_minimum_diameter_mm,
                "shape": self.drill_hole_shape,
                "color": self.drill_hole_color,
                "plated_color": self.drill_plated_hole_color,
                "non_plated_color": self.drill_non_plated_hole_color,
                "ring_width_mm": self.drill_ring_width_mm,
                "plated_ring_shape": self.drill_plated_ring_shape,
                "selected_component_mode": self.drill_selected_component_mode,
                "other_component_mode": self.drill_other_component_mode,
                "free_pad_mode": self.drill_free_pad_mode,
                "via_mode": self.drill_via_mode,
                "overlay_thickness_mm": self.drill_overlay_thickness_mm,
            },
        }

    def to_options(self) -> PcbLayerStepOptions:
        return PcbLayerStepOptions(
            layer=resolve_pcb_layer_selector(self.layer),
            thickness_mm=self.thickness_mm,
            z_mm=self.z_mm,
            copper_color=self.copper_color,
            outline_width_mm=self.outline_width_mm,
            outline_color=self.outline_color,
            board_cutout_color=self.board_cutout_color,
            include_copper=self.include_copper,
            include_board_outline=self.include_board_outline,
            include_board_cutouts=self.include_board_cutouts,
            include_poured_polygons=self.include_poured_polygons,
            cut_holes=self.cut_holes,
            drill_hole_mode=self.drill_hole_mode,
            max_boolean_drill_cuts=self.max_boolean_drill_cuts,
            drill_hole_color=self.drill_hole_color,
            drill_plated_hole_color=self.drill_plated_hole_color,
            drill_non_plated_hole_color=self.drill_non_plated_hole_color,
            drill_overlay_thickness_mm=self.drill_overlay_thickness_mm,
            drill_minimum_diameter_mm=self.drill_minimum_diameter_mm,
            drill_hole_shape=self.drill_hole_shape,
            drill_ring_width_mm=self.drill_ring_width_mm,
            drill_plated_ring_shape=self.drill_plated_ring_shape,
            drill_selected_component_mode=self.drill_selected_component_mode,
            drill_other_component_mode=self.drill_other_component_mode,
            drill_free_pad_mode=self.drill_free_pad_mode,
            drill_via_mode=self.drill_via_mode,
            fuse_copper=self.fuse_copper,
            fuse_board_outline=self.fuse_board_outline,
            arc_segments=self.arc_segments,
            include_tracks=self.include_tracks,
            include_arcs=self.include_arcs,
            include_fills=self.include_fills,
            include_regions=self.include_regions,
            include_vias=self.include_vias,
            include_component_pads=self.include_component_pads,
            include_free_pads=self.include_free_pads,
            include_designators=self.include_designators,
            pad_color_rules=self.pad_color_rules,
            track_color=self.track_color,
            track_body=self.track_body,
            arc_color=self.arc_color,
            arc_body=self.arc_body,
            fill_color=self.fill_color,
            fill_body=self.fill_body,
            polygon_color=self.polygon_color,
            polygon_body=self.polygon_body,
            region_color=self.region_color,
            region_body=self.region_body,
            via_color=self.via_color,
            via_body=self.via_body,
            component_pad_color=self.component_pad_color,
            component_pad_body=self.component_pad_body,
            free_pad_color=self.free_pad_color,
            free_pad_body=self.free_pad_body,
            track_thickness_bias_mm=self.track_thickness_bias_mm,
            arc_thickness_bias_mm=self.arc_thickness_bias_mm,
            fill_thickness_bias_mm=self.fill_thickness_bias_mm,
            polygon_thickness_bias_mm=self.polygon_thickness_bias_mm,
            region_thickness_bias_mm=self.region_thickness_bias_mm,
            via_thickness_bias_mm=self.via_thickness_bias_mm,
            component_pad_thickness_bias_mm=self.component_pad_thickness_bias_mm,
            free_pad_thickness_bias_mm=self.free_pad_thickness_bias_mm,
        )


@dataclass(slots=True)
class _Segment:
    kind: str = "line"
    center: tuple[float, float] | None = None
    sweep: str | None = None

    def to_json(self) -> dict[str, Any]:
        data: dict[str, Any] = {"kind": self.kind}
        if self.center is not None:
            data["center"] = [self.center[0], self.center[1]]
        if self.sweep is not None:
            data["sweep"] = self.sweep
        return data


@dataclass(slots=True)
class _Ring:
    points: list[tuple[float, float]]
    segments: list[_Segment] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.points = _dedupe_closed_points(self.points)
        if not self.segments:
            self.segments = [_Segment() for _ in self.points]
        if len(self.segments) != len(self.points):
            raise ValueError("ring segments must match ring points")

    def to_json(self) -> dict[str, Any]:
        return {
            "points": [[x, y] for x, y in self.points],
            "segments": [segment.to_json() for segment in self.segments],
        }


@dataclass(slots=True)
class _Region:
    outer: _Ring
    holes: list[_Ring] = field(default_factory=list)

    def to_json(self) -> dict[str, Any]:
        data: dict[str, Any] = {"outer": self.outer.to_json()}
        if self.holes:
            data["holes"] = [hole.to_json() for hole in self.holes]
        return data


@dataclass(frozen=True, slots=True)
class _SourceFeature:
    kind: str
    region: _Region
    component_designator: str | None = None
    pad_designator: str | None = None


@dataclass(frozen=True, slots=True)
class _DrillFeature:
    region: _Region
    center: tuple[float, float]
    diameter_mm: float
    slot_length_mm: float | None = None
    rotation_degrees: float = 0.0
    plated: bool = True
    pad_region: _Region | None = None
    source_kind: str = "pad"
    component_designator: str | None = None
    pad_designator: str | None = None


def write_default_pcb_layer_step_config(config_path: Path) -> None:
    """Write a default editable pcb-layer-step JSONC config."""
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        pcb_layer_step_default_config_text(),
        encoding="utf-8",
    )


def load_pcb_layer_step_config(config_path: Path) -> PcbLayerStepConfig:
    """Load a pcb-layer-step JSON or JSONC config."""
    try:
        raw_data = load_json_config(config_path)
    except Exception as exc:
        raise ValueError(
            f"Failed to parse pcb-layer-step config '{config_path}': {exc}"
        ) from exc
    return PcbLayerStepConfig.from_dict(raw_data)


def export_pcb_layer_step(
    pcbdoc: Any,
    output_path: Path,
    *,
    options: PcbLayerStepOptions | None = None,
    board_name: str | None = None,
    source_input: str | None = None,
) -> PcbLayerStepResult:
    """Export a selected PCB layer as a colored STEP alignment model."""
    opts = options or PcbLayerStepOptions()
    _validate_options(opts)
    geometer = _load_geometer()
    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    layer = opts.layer
    resolved_board_name = board_name or _board_name_from_pcbdoc(pcbdoc)

    layer_name = layer.to_json_name()
    log.info("Collecting %s layer geometry for %s", layer_name, resolved_board_name)
    features = _collect_layer_features(pcbdoc, layer, opts)
    drill_features = _collect_drill_features(pcbdoc, layer, opts)
    drill_hole_mode = _effective_drill_hole_mode(opts, len(drill_features))
    feature_counts = (len(features), len(drill_features), drill_hole_mode)
    log.info("Collected features: layer=%d drill=%d mode=%s", *feature_counts)
    bodies, counts = _build_step_bodies(
        pcbdoc=pcbdoc,
        opts=opts,
        features=features,
        drill_features=drill_features,
        drill_hole_mode=drill_hole_mode,
    )
    if not bodies:
        raise ValueError(f"No geometry found for layer {layer.to_display_name()}")
    origin_mils = step_origin.board_origin_mils(pcbdoc)
    step_origin.apply_origin_relative_geometry(bodies, origin_mils)

    request = {
        "schema": "geometry.planar_step.request.a0",
        "units": "mm",
        "name": _step_name(resolved_board_name),
        "bodies": bodies,
    }
    log.info("Writing STEP with %d bodies: %s", len(bodies), output_path.name)
    geometer.write_planar_step(request, output_path)

    manifest_path = output_path.with_suffix(".json")
    manifest = _build_manifest(
        opts=opts,
        output_path=output_path,
        board_name=resolved_board_name,
        source_input=source_input,
        layer=layer,
        drill_hole_mode=drill_hole_mode,
        counts=counts,
        coordinate_origin=step_origin.coordinate_origin_payload(origin_mils),
    )
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    return PcbLayerStepResult(
        output_path=output_path,
        manifest_path=manifest_path,
        board_name=resolved_board_name,
        layer=layer.to_json_name(),
        copper_body_count=counts["copper_bodies"],
        outline_body_count=counts["outline_bodies"],
        drill_cut_count=counts["drill_cut_geometries"],
        source_input=source_input,
    )


def _validate_options(opts: PcbLayerStepOptions) -> None:
    if opts.thickness_mm <= 0.0:
        raise ValueError("STEP layer thickness must be positive")
    if opts.outline_width_mm < 0.0:
        raise ValueError("Board outline width must be non-negative")
    if opts.drill_ring_width_mm < 0.0:
        raise ValueError("Drill ring width must be non-negative")
    if opts.drill_plated_ring_shape not in DRILL_PLATED_RING_SHAPES:
        raise ValueError("Drill plated ring shape must be 'annulus'")
    scoped_modes = {
        "selected_component": opts.drill_selected_component_mode,
        "other_component": opts.drill_other_component_mode,
        "free_pad": opts.drill_free_pad_mode,
        "via": opts.drill_via_mode,
    }
    invalid_modes = [
        name for name, value in scoped_modes.items() if value not in DRILL_SCOPE_MODES
    ]
    if invalid_modes:
        joined = ", ".join(invalid_modes)
        raise ValueError(f"STEP scoped drill modes are invalid: {joined}")
    bias_values = {
        "track": opts.track_thickness_bias_mm,
        "arc": opts.arc_thickness_bias_mm,
        "fill": opts.fill_thickness_bias_mm,
        "polygon": opts.polygon_thickness_bias_mm,
        "region": opts.region_thickness_bias_mm,
        "via": opts.via_thickness_bias_mm,
        "component_pad": opts.component_pad_thickness_bias_mm,
        "free_pad": opts.free_pad_thickness_bias_mm,
    }
    invalid_biases = [name for name, value in bias_values.items() if value < 0.0]
    if invalid_biases:
        joined = ", ".join(invalid_biases)
        raise ValueError(f"STEP thickness bias values must be non-negative: {joined}")


def _load_geometer() -> Any:
    try:
        import geometer
    except Exception as exc:  # pragma: no cover - import failure depends on environment
        raise RuntimeError(
            "PCB layer STEP export requires wn-geometer with planar_step support"
        ) from exc
    if not hasattr(geometer, "write_planar_step"):
        raise RuntimeError(
            "PCB layer STEP export requires wn-geometer write_planar_step support"
        )
    return geometer


def _build_manifest(
    *,
    opts: PcbLayerStepOptions,
    output_path: Path,
    board_name: str,
    source_input: str | None,
    layer: PcbLayer,
    drill_hole_mode: str,
    counts: dict[str, int],
    coordinate_origin: dict[str, object],
) -> dict[str, Any]:
    return {
        "schema": "wn.altium_cruncher.pcb_layer_step.v1",
        "backend": "geometer.planar_step",
        "board": board_name,
        "source_input": source_input,
        "step_file": output_path.name,
        "coordinate_origin": coordinate_origin,
        "layer": {
            "id": int(layer.value),
            "json_name": layer.to_json_name(),
            "display_name": layer.to_display_name(),
        },
        "options": {
            "thickness_mm": float(opts.thickness_mm),
            "z_mm": float(opts.z_mm),
            "copper_color": opts.copper_color,
            "outline_width_mm": float(opts.outline_width_mm),
            "outline_color": opts.outline_color,
            "board_cutout_color": opts.board_cutout_color,
            "include_copper": bool(opts.include_copper),
            "include_board_outline": bool(opts.include_board_outline),
            "include_board_cutouts": bool(opts.include_board_cutouts),
            "include_poured_polygons": bool(opts.include_poured_polygons),
            "cut_holes": bool(opts.cut_holes),
            "drill_hole_mode": opts.drill_hole_mode,
            "effective_drill_hole_mode": drill_hole_mode,
            "max_boolean_drill_cuts": int(opts.max_boolean_drill_cuts),
            "drill_hole_color": opts.drill_hole_color,
            "drill_plated_hole_color": opts.drill_plated_hole_color,
            "drill_non_plated_hole_color": opts.drill_non_plated_hole_color,
            "drill_overlay_thickness_mm": float(opts.drill_overlay_thickness_mm),
            "drill_minimum_diameter_mm": float(opts.drill_minimum_diameter_mm),
            "drill_hole_shape": opts.drill_hole_shape,
            "drill_ring_width_mm": float(opts.drill_ring_width_mm),
            "drill_plated_ring_shape": opts.drill_plated_ring_shape,
            "drill_selected_component_mode": opts.drill_selected_component_mode,
            "drill_other_component_mode": opts.drill_other_component_mode,
            "drill_free_pad_mode": opts.drill_free_pad_mode,
            "drill_via_mode": opts.drill_via_mode,
            "fuse_copper": bool(opts.fuse_copper),
            "fuse_board_outline": bool(opts.fuse_board_outline),
            "arc_segments": int(opts.arc_segments),
            "features": {
                "tracks": bool(opts.include_tracks),
                "arcs": bool(opts.include_arcs),
                "fills": bool(opts.include_fills),
                "polygons": bool(opts.include_poured_polygons),
                "regions": bool(opts.include_regions),
                "vias": bool(opts.include_vias),
                "component_pads": bool(opts.include_component_pads),
                "free_pads": bool(opts.include_free_pads),
                "include_designators": list(opts.include_designators),
            },
            "pad_color_rules": [
                {
                    "designators": list(rule.designators),
                    "color": rule.color,
                    "step_body_name": rule.step_body_name,
                }
                for rule in opts.pad_color_rules
            ],
            "feature_color_rules": {
                "tracks": {
                    "color": opts.track_color,
                    "step_body_name": opts.track_body,
                },
                "arcs": {
                    "color": opts.arc_color,
                    "step_body_name": opts.arc_body,
                },
                "fills": {
                    "color": opts.fill_color,
                    "step_body_name": opts.fill_body,
                },
                "polygons": {
                    "color": opts.polygon_color,
                    "step_body_name": opts.polygon_body,
                },
                "regions": {
                    "color": opts.region_color,
                    "step_body_name": opts.region_body,
                },
                "vias": {
                    "color": opts.via_color,
                    "step_body_name": opts.via_body,
                },
                "component_pads": {
                    "color": opts.component_pad_color,
                    "step_body_name": opts.component_pad_body,
                },
                "free_pads": {
                    "color": opts.free_pad_color,
                    "step_body_name": opts.free_pad_body,
                },
            },
            "thickness_bias_mm": {
                "tracks": float(opts.track_thickness_bias_mm),
                "arcs": float(opts.arc_thickness_bias_mm),
                "fills": float(opts.fill_thickness_bias_mm),
                "polygons": float(opts.polygon_thickness_bias_mm),
                "regions": float(opts.region_thickness_bias_mm),
                "vias": float(opts.via_thickness_bias_mm),
                "component_pads": float(opts.component_pad_thickness_bias_mm),
                "free_pads": float(opts.free_pad_thickness_bias_mm),
            },
            "highlight_count": len(opts.highlights),
        },
        "counts": counts,
        "bytes": output_path.stat().st_size,
    }


def _build_step_bodies(
    *,
    pcbdoc: Any,
    opts: PcbLayerStepOptions,
    features: list[_SourceFeature],
    drill_features: list[_DrillFeature],
    drill_hole_mode: str,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    board_cutouts = _collect_board_cutout_regions(pcbdoc)
    drill_mode_by_feature = _drill_modes_for_features(
        drill_features,
        opts,
        drill_hole_mode,
    )
    boolean_drill_cutouts = [
        feature.region
        for feature, mode in drill_mode_by_feature
        if mode == DRILL_HOLE_MODE_CUT
    ]
    drill_copper_cutouts = [
        feature.region
        for feature, mode in drill_mode_by_feature
        if mode in {DRILL_HOLE_MODE_CUT, DRILL_HOLE_MODE_OVERLAY}
    ]
    overlay_drill_features = [
        feature
        for feature, mode in drill_mode_by_feature
        if mode == DRILL_HOLE_MODE_OVERLAY
    ]
    pad_clip_regions = _pad_clip_regions(features)
    shared_cutouts = [*drill_copper_cutouts, *board_cutouts]
    bodies = [
        *_copper_bodies_from_features(
            features,
            opts,
            shared_cutouts,
            pad_clip_regions,
        ),
        *_highlight_bodies(opts),
        *_drill_overlay_bodies(overlay_drill_features, DRILL_HOLE_MODE_OVERLAY, opts),
        *_outline_bodies(pcbdoc, opts),
    ]
    counts = _build_counts(
        features=features,
        drill_features=drill_features,
        overlay_drill_features=overlay_drill_features,
        boolean_drill_cutouts=boolean_drill_cutouts,
        drill_copper_cutouts=drill_copper_cutouts,
        board_cutouts=board_cutouts,
        bodies=bodies,
    )
    return bodies, counts


def _copper_bodies_from_features(
    features: list[_SourceFeature],
    opts: PcbLayerStepOptions,
    cutouts: list[_Region],
    pad_clip_regions: list[_Region],
) -> list[dict[str, Any]]:
    if not opts.include_copper:
        return []
    grouped: dict[tuple[str, str, float, bool], list[_Region]] = {}
    for feature in features:
        body_id, color, thickness_bias_mm = _body_style_for_feature(feature, opts)
        clip_to_pads = _feature_clips_to_pad_shapes(feature)
        grouped.setdefault(
            (body_id, color, thickness_bias_mm, clip_to_pads), []
        ).append(feature.region)
    return [
        _body_from_regions(
            body_id=body_id,
            color=color,
            regions=regions,
            z_mm=_biased_z_mm(opts.z_mm, thickness_bias_mm),
            thickness_mm=_biased_thickness_mm(opts.thickness_mm, thickness_bias_mm),
            fuse_regions=opts.fuse_copper,
            cutouts=[
                *cutouts,
                *(pad_clip_regions if clip_to_pads else []),
            ],
        )
        for (
            body_id,
            color,
            thickness_bias_mm,
            clip_to_pads,
        ), regions in grouped.items()
        if regions
    ]


def _body_style_for_feature(
    feature: _SourceFeature,
    opts: PcbLayerStepOptions,
) -> tuple[str, str, float]:
    thickness_bias_mm = _thickness_bias_for_feature(feature, opts)
    body_id, color = _configured_body_style(feature, opts)
    body_id, color = _apply_pad_color_rules(feature, opts, body_id, color)
    if body_id == "copper" and thickness_bias_mm > 0.0:
        body_id = f"copper_{_feature_body_suffix(feature.kind)}"
    return body_id, color, thickness_bias_mm


def _configured_body_style(
    feature: _SourceFeature,
    opts: PcbLayerStepOptions,
) -> tuple[str, str]:
    style = _feature_style_options(opts).get(feature.kind)
    if style is None:
        return "copper", opts.copper_color
    body_template, default_body_id, color = style
    if color is None and body_template == default_body_id:
        return "copper", opts.copper_color
    return (
        _format_step_body_name(body_template, feature, default_body_id),
        color or opts.copper_color,
    )


def _feature_style_options(
    opts: PcbLayerStepOptions,
) -> dict[str, tuple[str, str, str | None]]:
    region_style = (opts.region_body, "regions", opts.region_color)
    return {
        "track": (opts.track_body, "tracks", opts.track_color),
        "arc": (opts.arc_body, "arcs", opts.arc_color),
        "fill": (opts.fill_body, "fills", opts.fill_color),
        "polygon": (opts.polygon_body, "polygons", opts.polygon_color),
        "region": region_style,
        "shapebased_region": region_style,
        "via": (opts.via_body, "vias", opts.via_color),
        "component_pad": (
            opts.component_pad_body,
            "component_pads",
            opts.component_pad_color,
        ),
        "free_pad": (opts.free_pad_body, "free_pads", opts.free_pad_color),
    }


def _apply_pad_color_rules(
    feature: _SourceFeature,
    opts: PcbLayerStepOptions,
    body_id: str,
    color: str,
) -> tuple[str, str]:
    if feature.kind not in {"component_pad", "free_pad"}:
        return body_id, color
    designator = feature.component_designator or feature.pad_designator or ""
    for rule in opts.pad_color_rules:
        if _matches_any_pattern(designator, rule.designators):
            return (
                _format_step_body_name(
                    rule.step_body_name,
                    feature,
                    "matched_pads",
                ),
                rule.color,
            )
    return body_id, color


def _format_step_body_name(
    template: str,
    feature: _SourceFeature,
    fallback: str,
) -> str:
    values = {
        "component": feature.component_designator or "",
        "pad": feature.pad_designator or "",
        "feature": _feature_body_suffix(feature.kind),
    }
    text = str(template)
    for key, value in values.items():
        text = text.replace(f"{{{key}}}", value)
    name = _step_name(text)
    return name if name != "board" or text.strip() else _step_name(fallback)


def _biased_z_mm(z_mm: float, thickness_bias_mm: float) -> float:
    return z_mm - max(0.0, thickness_bias_mm)


def _biased_thickness_mm(thickness_mm: float, thickness_bias_mm: float) -> float:
    bias = max(0.0, thickness_bias_mm)
    return thickness_mm + (2.0 * bias)


def _feature_body_suffix(kind: str) -> str:
    return {
        "track": "tracks",
        "arc": "arcs",
        "fill": "fills",
        "polygon": "polygons",
        "region": "regions",
        "shapebased_region": "regions",
        "via": "vias",
        "component_pad": "pads",
        "free_pad": "pads",
    }.get(kind, kind)


def _pad_clip_regions(features: list[_SourceFeature]) -> list[_Region]:
    return [
        feature.region
        for feature in features
        if feature.kind in {"component_pad", "free_pad", "via"}
    ]


def _feature_clips_to_pad_shapes(feature: _SourceFeature) -> bool:
    return feature.kind in {
        "track",
        "arc",
        "fill",
        "polygon",
        "region",
        "shapebased_region",
    }


def _thickness_bias_for_feature(
    feature: _SourceFeature,
    opts: PcbLayerStepOptions,
) -> float:
    return {
        "track": opts.track_thickness_bias_mm,
        "arc": opts.arc_thickness_bias_mm,
        "fill": opts.fill_thickness_bias_mm,
        "polygon": opts.polygon_thickness_bias_mm,
        "region": opts.region_thickness_bias_mm,
        "shapebased_region": opts.region_thickness_bias_mm,
        "via": opts.via_thickness_bias_mm,
        "component_pad": opts.component_pad_thickness_bias_mm,
        "free_pad": opts.free_pad_thickness_bias_mm,
    }.get(feature.kind, 0.0)


def _highlight_bodies(opts: PcbLayerStepOptions) -> list[dict[str, Any]]:
    return highlight_bodies_from_geometries(
        highlights=opts.highlights,
        layer=opts.layer,
        z_mm=opts.z_mm,
        copper_thickness_mm=opts.thickness_mm,
        pad_shape_region=_pad_shape_region,
        step_name=_step_name,
    )


def _drill_overlay_bodies(
    drill_features: list[_DrillFeature],
    drill_hole_mode: str,
    opts: PcbLayerStepOptions,
) -> list[dict[str, Any]]:
    if drill_hole_mode != DRILL_HOLE_MODE_OVERLAY or not drill_features:
        return []
    grouped: dict[tuple[str, str], list[_DrillFeature]] = {}
    for feature in drill_features:
        body_id, color = _drill_body_style(feature, opts)
        grouped.setdefault((body_id, color), []).append(feature)
    return [
        _body_from_regions(
            body_id=body_id,
            color=color,
            regions=[_drill_overlay_region(feature, opts) for feature in features],
            z_mm=opts.z_mm + opts.thickness_mm,
            thickness_mm=max(0.0001, opts.drill_overlay_thickness_mm),
            fuse_regions=False,
            cutouts=[],
        )
        for (body_id, color), features in grouped.items()
    ]


def _drill_body_style(
    feature: _DrillFeature,
    opts: PcbLayerStepOptions,
) -> tuple[str, str]:
    if _drill_overlay_uses_single_color(opts):
        return "drill_holes", opts.drill_hole_color
    if feature.plated:
        return "plated_drill_holes", opts.drill_plated_hole_color
    return "non_plated_drill_holes", opts.drill_non_plated_hole_color


def _drill_overlay_uses_single_color(opts: PcbLayerStepOptions) -> bool:
    return (
        opts.drill_plated_hole_color == opts.drill_hole_color
        and opts.drill_non_plated_hole_color == opts.drill_hole_color
    )


def _outline_bodies(pcbdoc: Any, opts: PcbLayerStepOptions) -> list[dict[str, Any]]:
    if not opts.include_board_outline or opts.outline_width_mm <= 0.0:
        return []
    bodies: list[dict[str, Any]] = []
    outline_regions = _collect_board_outline_regions(pcbdoc, opts)
    if outline_regions:
        bodies.append(
            _body_from_regions(
                body_id="board_outline",
                color=opts.outline_color,
                regions=outline_regions,
                z_mm=opts.z_mm,
                thickness_mm=opts.thickness_mm,
                fuse_regions=opts.fuse_board_outline,
                cutouts=[],
            )
        )
    cutout_regions = _collect_board_cutout_outline_regions(pcbdoc, opts)
    if opts.include_board_cutouts and cutout_regions:
        bodies.append(
            _body_from_regions(
                body_id="board_cutouts",
                color=opts.board_cutout_color,
                regions=cutout_regions,
                z_mm=opts.z_mm,
                thickness_mm=opts.thickness_mm,
                fuse_regions=opts.fuse_board_outline,
                cutouts=[],
            )
        )
    return bodies


def _body_from_regions(
    *,
    body_id: str,
    color: str,
    regions: list[_Region],
    z_mm: float,
    thickness_mm: float,
    fuse_regions: bool,
    cutouts: list[_Region],
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "id": body_id,
        "name": body_id,
        "color": color,
        "z_mm": z_mm,
        "thickness_mm": thickness_mm,
        "regions": [region.to_json() for region in regions],
    }
    if fuse_regions:
        body["fuse_regions"] = True
    if cutouts:
        body["cutouts"] = [cutout.to_json() for cutout in cutouts]
    return body


def _build_counts(
    *,
    features: list[_SourceFeature],
    drill_features: list[_DrillFeature],
    overlay_drill_features: list[_DrillFeature],
    boolean_drill_cutouts: list[_Region],
    drill_copper_cutouts: list[_Region],
    board_cutouts: list[_Region],
    bodies: list[dict[str, Any]],
) -> dict[str, int]:
    drill_overlay_count, plated_overlay_count, non_plated_overlay_count = (
        _drill_overlay_counts(overlay_drill_features)
    )
    return {
        "source_layer_geometries": len(features),
        "drill_cut_geometries": len(drill_features),
        "drill_boolean_cut_geometries": len(boolean_drill_cutouts),
        "drill_copper_cutout_geometries": len(drill_copper_cutouts),
        "drill_overlay_geometries": drill_overlay_count,
        "drill_plated_overlay_geometries": plated_overlay_count,
        "drill_non_plated_overlay_geometries": non_plated_overlay_count,
        "board_cutout_geometries": len(board_cutouts),
        "board_cutout_outline_geometries": sum(
            len(body.get("regions", []))
            for body in bodies
            if str(body.get("id")) == "board_cutouts"
        ),
        "copper_bodies": sum(1 for body in bodies if _is_step_copper_body(body)),
        "highlight_bodies": sum(
            1 for body in bodies if str(body.get("kind")) == "highlight"
        ),
        "outline_bodies": sum(
            1 for body in bodies if str(body.get("id")) == "board_outline"
        ),
        "board_cutout_outline_bodies": sum(
            1 for body in bodies if str(body.get("id")) == "board_cutouts"
        ),
        "body_count": len(bodies),
    }


def _drill_overlay_counts(
    drill_features: list[_DrillFeature],
) -> tuple[int, int, int]:
    plated_count = sum(1 for feature in drill_features if feature.plated)
    return (len(drill_features), plated_count, len(drill_features) - plated_count)


def _is_step_copper_body(body: Mapping[str, Any]) -> bool:
    return (
        str(body.get("id")) not in _NON_COPPER_BODY_IDS
        and str(body.get("kind")) != "highlight"
    )


def _effective_drill_hole_mode(opts: PcbLayerStepOptions, drill_count: int) -> str:
    """Choose the drill-hole strategy for this board."""
    if not opts.cut_holes:
        return DRILL_HOLE_MODE_NONE
    requested = _coerce_drill_hole_mode(opts.drill_hole_mode, cut_holes=True)
    if requested != DRILL_HOLE_MODE_AUTO:
        return requested
    if drill_count <= max(0, int(opts.max_boolean_drill_cuts)):
        return DRILL_HOLE_MODE_CUT
    log.info(
        "Using drill overlay instead of boolean drill cuts for %d holes "
        "(threshold: %d)",
        drill_count,
        int(opts.max_boolean_drill_cuts),
    )
    return DRILL_HOLE_MODE_OVERLAY


def _drill_modes_for_features(
    drill_features: list[_DrillFeature],
    opts: PcbLayerStepOptions,
    global_mode: str,
) -> list[tuple[_DrillFeature, str]]:
    if global_mode == DRILL_HOLE_MODE_NONE:
        return [(feature, DRILL_HOLE_MODE_NONE) for feature in drill_features]
    return [
        (feature, _effective_drill_feature_mode(feature, opts, global_mode))
        for feature in drill_features
    ]


def _effective_drill_feature_mode(
    feature: _DrillFeature,
    opts: PcbLayerStepOptions,
    global_mode: str,
) -> str:
    scoped_mode = _configured_drill_scope_mode(feature, opts)
    return global_mode if scoped_mode == DRILL_SCOPE_MODE_INHERIT else scoped_mode


def _configured_drill_scope_mode(
    feature: _DrillFeature,
    opts: PcbLayerStepOptions,
) -> str:
    if feature.source_kind == "via":
        return opts.drill_via_mode
    if feature.component_designator:
        if _include_pad_feature(feature.component_designator, opts):
            return opts.drill_selected_component_mode
        return opts.drill_other_component_mode
    return opts.drill_free_pad_mode


def _collect_layer_features(
    pcbdoc: Any,
    layer: PcbLayer,
    opts: PcbLayerStepOptions,
) -> list[_SourceFeature]:
    features: list[_SourceFeature] = []
    if opts.include_tracks or opts.include_poured_polygons:
        features.extend(_track_features(pcbdoc, layer, opts))
    if opts.include_arcs or opts.include_poured_polygons:
        features.extend(_arc_features(pcbdoc, layer, opts))
    if opts.include_fills or opts.include_poured_polygons:
        features.extend(_fill_features(pcbdoc, layer, opts))
    if layer.is_copper():
        features.extend(_pad_features(pcbdoc, layer, opts))
        if opts.include_vias:
            features.extend(_via_features(pcbdoc, layer))
    if opts.include_regions or opts.include_poured_polygons:
        features.extend(_region_features(pcbdoc, layer, opts))
    return features


def _track_features(
    pcbdoc: Any,
    layer: PcbLayer,
    opts: PcbLayerStepOptions,
) -> list[_SourceFeature]:
    features: list[_SourceFeature] = []
    for track in getattr(pcbdoc, "tracks", []) or []:
        if int(getattr(track, "layer", 0) or 0) != layer.value:
            continue
        is_polygon = _is_poured_polygon_primitive(track)
        if is_polygon and not opts.include_poured_polygons:
            continue
        if not is_polygon and not opts.include_tracks:
            continue
        region = _track_region(track)
        if region is not None:
            features.append(
                _SourceFeature("polygon" if is_polygon else "track", region)
            )
    return features


def _arc_features(
    pcbdoc: Any,
    layer: PcbLayer,
    opts: PcbLayerStepOptions,
) -> list[_SourceFeature]:
    features: list[_SourceFeature] = []
    for arc in getattr(pcbdoc, "arcs", []) or []:
        if int(getattr(arc, "layer", 0) or 0) != layer.value:
            continue
        is_polygon = _is_poured_polygon_primitive(arc)
        if is_polygon and not opts.include_poured_polygons:
            continue
        if not is_polygon and not opts.include_arcs:
            continue
        region = _arc_region(arc)
        if region is not None:
            features.append(_SourceFeature("polygon" if is_polygon else "arc", region))
    return features


def _fill_features(
    pcbdoc: Any,
    layer: PcbLayer,
    opts: PcbLayerStepOptions,
) -> list[_SourceFeature]:
    features: list[_SourceFeature] = []
    for fill in getattr(pcbdoc, "fills", []) or []:
        if int(getattr(fill, "layer", 0) or 0) != layer.value:
            continue
        is_polygon = _is_poured_polygon_primitive(fill)
        if is_polygon and not opts.include_poured_polygons:
            continue
        if not is_polygon and not opts.include_fills:
            continue
        region = _fill_region(fill)
        if region is not None:
            features.append(_SourceFeature("polygon" if is_polygon else "fill", region))
    return features


def _pad_features(
    pcbdoc: Any,
    layer: PcbLayer,
    opts: PcbLayerStepOptions,
) -> list[_SourceFeature]:
    features: list[_SourceFeature] = []
    for pad in getattr(pcbdoc, "pads", []) or []:
        component_designator = _pad_component_designator(pcbdoc, pad)
        if not _include_pad_feature(component_designator, opts):
            continue
        region = _pad_region(pad, layer)
        if region is None:
            continue
        features.append(
            _SourceFeature(
                "component_pad" if component_designator else "free_pad",
                region,
                component_designator=component_designator,
                pad_designator=str(getattr(pad, "designator", "") or "").strip()
                or None,
            )
        )
    return features


def _via_features(pcbdoc: Any, layer: PcbLayer) -> list[_SourceFeature]:
    features: list[_SourceFeature] = []
    for via in getattr(pcbdoc, "vias", []) or []:
        region = _via_region(via, layer)
        if region is not None:
            features.append(_SourceFeature("via", region))
    return features


def _region_features(
    pcbdoc: Any,
    layer: PcbLayer,
    opts: PcbLayerStepOptions,
) -> list[_SourceFeature]:
    features: list[_SourceFeature] = []
    for region in getattr(pcbdoc, "regions", []) or []:
        feature = _normal_region_feature(region, layer, opts)
        if feature is not None:
            features.append(feature)
    for region in getattr(pcbdoc, "shapebased_regions", []) or []:
        feature = _shapebased_region_feature(region, layer, opts)
        if feature is not None:
            features.append(feature)
    return features


def _normal_region_feature(
    region: Any,
    layer: PcbLayer,
    opts: PcbLayerStepOptions,
) -> _SourceFeature | None:
    if int(getattr(region, "layer", 0) or 0) != layer.value:
        return None
    if bool(getattr(region, "is_board_cutout", False)) or bool(
        getattr(region, "is_keepout", False)
    ):
        return None
    is_polygon = _is_poured_polygon_primitive(region)
    if is_polygon and not opts.include_poured_polygons:
        return None
    if not is_polygon and not opts.include_regions:
        return None
    converted = _region_from_outline_vertices(region)
    return (
        _SourceFeature("polygon" if is_polygon else "region", converted)
        if converted is not None
        else None
    )


def _shapebased_region_feature(
    region: Any,
    layer: PcbLayer,
    opts: PcbLayerStepOptions,
) -> _SourceFeature | None:
    if int(getattr(region, "layer", 0) or 0) != layer.value:
        return None
    if bool(getattr(region, "is_keepout", False)):
        return None
    is_polygon = _is_poured_polygon_primitive(region)
    if is_polygon and not opts.include_poured_polygons:
        return None
    if not is_polygon and not opts.include_regions:
        return None
    converted = _shapebased_region(region)
    return (
        _SourceFeature("polygon" if is_polygon else "shapebased_region", converted)
        if converted is not None
        else None
    )


def _include_pad_feature(
    component_designator: str | None,
    opts: PcbLayerStepOptions,
) -> bool:
    if component_designator:
        return opts.include_component_pads and _matches_designator_filter(
            component_designator,
            opts.include_designators,
        )
    return opts.include_free_pads


def _matches_designator_filter(value: str, patterns: tuple[str, ...]) -> bool:
    return not patterns or _matches_any_pattern(value, patterns)


def _matches_any_pattern(value: str, patterns: Iterable[str]) -> bool:
    normalized = value.casefold()
    return any(
        fnmatch.fnmatchcase(normalized, pattern.casefold()) for pattern in patterns
    )


def _pad_component_designator(pcbdoc: Any, pad: Any) -> str | None:
    raw_index = getattr(pad, "component_index", None)
    try:
        index = int(raw_index)
    except (TypeError, ValueError):
        return None
    components = list(getattr(pcbdoc, "components", []) or [])
    if not 0 <= index < len(components):
        return None
    designator = str(getattr(components[index], "designator", "") or "").strip()
    return designator or None


def _collect_drill_features(
    pcbdoc: Any,
    layer: PcbLayer,
    opts: PcbLayerStepOptions,
) -> list[_DrillFeature]:
    if not layer.is_copper():
        return []
    drills = [
        *_pad_drill_features(pcbdoc, layer, opts),
        *_via_drill_features(pcbdoc, layer),
    ]
    return [
        drill
        for drill in drills
        if drill.diameter_mm > max(0.0, opts.drill_minimum_diameter_mm)
    ]


def _pad_drill_features(
    pcbdoc: Any,
    layer: PcbLayer,
    opts: PcbLayerStepOptions,
) -> list[_DrillFeature]:
    features: list[_DrillFeature] = []
    for pad in getattr(pcbdoc, "pads", []) or []:
        if not _pad_should_render_on_layer(pad, layer):
            continue
        component_designator = _pad_component_designator(pcbdoc, pad)
        feature = _pad_hole_feature(
            pad,
            layer,
            opts.arc_segments,
            component_designator=component_designator,
        )
        if feature is not None:
            features.append(feature)
    return features


def _via_drill_features(pcbdoc: Any, layer: PcbLayer) -> list[_DrillFeature]:
    features: list[_DrillFeature] = []
    for via in getattr(pcbdoc, "vias", []) or []:
        if not _via_spans_layer(via, layer):
            continue
        feature = _via_hole_feature(via)
        if feature is not None:
            features.append(feature)
    return features


def _collect_drill_cutout_regions(
    pcbdoc: Any,
    layer: PcbLayer,
    opts: PcbLayerStepOptions,
) -> list[_Region]:
    if not layer.is_copper():
        return []
    cutouts: list[_Region] = []
    for pad in getattr(pcbdoc, "pads", []) or []:
        if not _pad_should_render_on_layer(pad, layer):
            continue
        cutout = _pad_hole_region(pad, layer, opts.arc_segments)
        if cutout is not None:
            cutouts.append(cutout)
    for via in getattr(pcbdoc, "vias", []) or []:
        if not _via_spans_layer(via, layer):
            continue
        cutout = _via_hole_region(via)
        if cutout is not None:
            cutouts.append(cutout)
    return cutouts


def _collect_board_outline_regions(
    pcbdoc: Any, opts: PcbLayerStepOptions
) -> list[_Region]:
    board = getattr(pcbdoc, "board", None)
    outline = getattr(board, "outline", None) if board is not None else None
    if outline is None:
        return []

    regions: list[_Region] = []
    regions.extend(
        _outline_stroke_regions(
            getattr(outline, "vertices", []) or [], opts.outline_width_mm
        )
    )
    return regions


def _collect_board_cutout_outline_regions(
    pcbdoc: Any, opts: PcbLayerStepOptions
) -> list[_Region]:
    board = getattr(pcbdoc, "board", None)
    outline = getattr(board, "outline", None) if board is not None else None
    regions: list[_Region] = []
    for cutout in getattr(outline, "cutouts", []) or []:
        regions.extend(_outline_stroke_regions(cutout, opts.outline_width_mm))
    for region in getattr(pcbdoc, "regions", []) or []:
        if bool(getattr(region, "is_board_cutout", False)):
            regions.extend(
                _outline_stroke_regions(
                    getattr(region, "outline_vertices", []) or [],
                    opts.outline_width_mm,
                )
            )
    return regions


def _collect_board_cutout_regions(pcbdoc: Any) -> list[_Region]:
    cutouts: list[_Region] = []
    board = getattr(pcbdoc, "board", None)
    outline = getattr(board, "outline", None) if board is not None else None
    for cutout in getattr(outline, "cutouts", []) or []:
        ring = _outline_ring(cutout)
        if ring is not None:
            cutouts.append(_Region(ring))

    for region in getattr(pcbdoc, "regions", []) or []:
        if not bool(getattr(region, "is_board_cutout", False)):
            continue
        converted = _region_from_outline_vertices(region)
        if converted is not None:
            cutouts.append(converted)
    return cutouts


def _track_region(track: Any) -> _Region | None:
    width_mm = max(_mils_to_mm(float(getattr(track, "width_mils", 0.0) or 0.0)), 0.0)
    if width_mm <= 0.0:
        return None
    start = (
        _mils_to_mm(float(getattr(track, "start_x_mils", 0.0))),
        _mils_to_mm(float(getattr(track, "start_y_mils", 0.0))),
    )
    end = (
        _mils_to_mm(float(getattr(track, "end_x_mils", 0.0))),
        _mils_to_mm(float(getattr(track, "end_y_mils", 0.0))),
    )
    return _line_capsule_region(start, end, width_mm)


def _arc_region(arc: Any) -> _Region | None:
    width_mm = max(_mils_to_mm(_iu_to_mils(getattr(arc, "width", 0))), 0.0)
    radius_mils = float(getattr(arc, "radius_mils", 0.0) or 0.0)
    if width_mm <= 0.0 or radius_mils <= 0.0:
        return None
    center_mils = (float(arc.center_x_mils), float(arc.center_y_mils))
    start_degrees = float(getattr(arc, "start_angle", 0.0) or 0.0)
    end_degrees = float(getattr(arc, "end_angle", 0.0) or 0.0)
    start_point = _arc_point_from_angle_mils(center_mils, radius_mils, start_degrees)
    end_point = _arc_point_from_angle_mils(center_mils, radius_mils, end_degrees)
    sweep = _svg_like_board_sweep_degrees(
        center_mils=center_mils,
        radius_mils=radius_mils,
        start_point_mils=start_point,
        end_point_mils=end_point,
        start_degrees=start_degrees,
        end_degrees=end_degrees,
        default_sweep_flag=1,
    )
    return _arc_stroke_region(
        center=(_mils_to_mm(center_mils[0]), _mils_to_mm(center_mils[1])),
        radius_mm=_mils_to_mm(radius_mils),
        start_degrees=math.degrees(
            math.atan2(start_point[1] - center_mils[1], start_point[0] - center_mils[0])
        ),
        sweep_degrees=sweep,
        width_mm=width_mm,
    )


def _fill_region(fill: Any) -> _Region | None:
    x1 = _mils_to_mm(_iu_to_mils(getattr(fill, "pos1_x", 0)))
    y1 = _mils_to_mm(_iu_to_mils(getattr(fill, "pos1_y", 0)))
    x2 = _mils_to_mm(_iu_to_mils(getattr(fill, "pos2_x", 0)))
    y2 = _mils_to_mm(_iu_to_mils(getattr(fill, "pos2_y", 0)))
    if math.isclose(x1, x2, abs_tol=1e-9) or math.isclose(y1, y2, abs_tol=1e-9):
        return None
    cx = (x1 + x2) / 2.0
    cy = (y1 + y2) / 2.0
    return _rectangle_region(
        center=(cx, cy),
        width_mm=abs(x2 - x1),
        height_mm=abs(y2 - y1),
        rotation_degrees=float(getattr(fill, "rotation", 0.0) or 0.0),
    )


def _pad_region(pad: Any, layer: PcbLayer) -> _Region | None:
    if not _pad_should_render_on_layer(pad, layer):
        return None
    try:
        width_iu, height_iu = pad._layer_size(layer)
        shape = int(pad._layer_shape(layer))
        cx_mils, cy_mils = pad.pad_center_mils(layer)
    except Exception:
        width_iu = int(getattr(pad, "top_width", 0) or getattr(pad, "width", 0) or 0)
        height_iu = int(getattr(pad, "top_height", 0) or getattr(pad, "height", 0) or 0)
        shape = int(getattr(pad, "shape", PadShape.CIRCLE) or PadShape.CIRCLE)
        cx_mils = _iu_to_mils(getattr(pad, "x", 0))
        cy_mils = _iu_to_mils(getattr(pad, "y", 0))

    width_mm = _mils_to_mm(_iu_to_mils(width_iu))
    height_mm = _mils_to_mm(_iu_to_mils(height_iu))
    if width_mm <= 0.0 or height_mm <= 0.0:
        return None
    center = (_mils_to_mm(cx_mils), _mils_to_mm(cy_mils))
    rotation = float(getattr(pad, "rotation", 0.0) or 0.0)
    corner_pct = _pad_corner_radius_percent(pad, layer)
    region = _pad_shape_region(
        center=center,
        width_mm=width_mm,
        height_mm=height_mm,
        shape=shape,
        rotation_degrees=rotation,
        corner_radius_percent=corner_pct,
        corner_radius_mm=None,
    )
    return region


def _via_region(via: Any, layer: PcbLayer) -> _Region | None:
    if not _via_spans_layer(via, layer) or _via_pad_removed_on_layer(via, layer):
        return None
    diameter_iu = _via_diameter_iu(via, layer)
    diameter_mm = _mils_to_mm(_iu_to_mils(diameter_iu))
    if diameter_mm <= 0.0:
        return None
    center = (_mils_to_mm(via.x_mils), _mils_to_mm(via.y_mils))
    return _circle_region(center, diameter_mm / 2.0)


def _region_from_outline_vertices(region: Any) -> _Region | None:
    outline = [
        (_mils_to_mm(vertex.x_mils), _mils_to_mm(vertex.y_mils))
        for vertex in (getattr(region, "outline_vertices", []) or [])
    ]
    holes = [
        _Ring(
            [
                (_mils_to_mm(vertex.x_mils), _mils_to_mm(vertex.y_mils))
                for vertex in hole
            ]
        )
        for hole in (getattr(region, "hole_vertices", []) or [])
        if len(hole) >= 3
    ]
    if len(_dedupe_closed_points(outline)) < 3:
        return None
    return _Region(_Ring(outline), holes)


def _shapebased_region(region: Any) -> _Region | None:
    outline_vertices = list(getattr(region, "outline", []) or [])
    if hasattr(region, "_outline_vertices_without_closing_duplicate"):
        outline_vertices = region._outline_vertices_without_closing_duplicate(
            outline_vertices
        )
    outer = _extended_vertices_ring(outline_vertices)
    if outer is None:
        return None
    holes = [
        _Ring(
            [
                (_mils_to_mm(vertex.x_mils), _mils_to_mm(vertex.y_mils))
                for vertex in hole
            ]
        )
        for hole in (getattr(region, "holes", []) or [])
        if len(hole) >= 3
    ]
    return _Region(outer, holes)


def _pad_hole_region(pad: Any, layer: PcbLayer, arc_segments: int) -> _Region | None:
    feature = _pad_hole_feature(pad, layer, arc_segments)
    return feature.region if feature is not None else None


def _pad_hole_center_mm(pad: object, layer: PcbLayer) -> tuple[float, float]:
    try:
        cx_mils, cy_mils = pad.hole_center_mils(layer)
    except Exception:
        cx_mils = _iu_to_mils(getattr(pad, "x", 0))
        cy_mils = _iu_to_mils(getattr(pad, "y", 0))
    return (_mils_to_mm(cx_mils), _mils_to_mm(cy_mils))


def _pad_hole_is_slot(
    pad: object, hole_size_mils: float, slot_size_mils: float
) -> bool:
    hole_shape = int(getattr(pad, "hole_shape", 0) or 0)
    return hole_shape == 2 and slot_size_mils > hole_size_mils


def _pad_drill_feature(
    pad: object,
    layer: PcbLayer,
    *,
    region: _Region,
    center: tuple[float, float],
    diameter_mm: float,
    component_designator: str | None,
    slot_length_mm: float | None = None,
    rotation_degrees: float = 0.0,
) -> _DrillFeature:
    return _DrillFeature(
        region=region,
        center=center,
        diameter_mm=diameter_mm,
        slot_length_mm=slot_length_mm,
        rotation_degrees=rotation_degrees,
        plated=bool(getattr(pad, "is_plated", True)),
        pad_region=_pad_region(pad, layer),
        source_kind="pad",
        component_designator=component_designator,
        pad_designator=str(getattr(pad, "designator", "") or "").strip() or None,
    )


def _pad_hole_feature(
    pad: Any,
    layer: PcbLayer,
    arc_segments: int,
    *,
    component_designator: str | None = None,
) -> _DrillFeature | None:
    hole_size_mils = float(getattr(pad, "hole_size_mils", 0.0) or 0.0)
    if hole_size_mils <= 0.0:
        return None
    center = _pad_hole_center_mm(pad, layer)
    diameter_mm = _mils_to_mm(hole_size_mils)
    slot_size_mils = _iu_to_mils(getattr(pad, "slot_size", 0))
    if not _pad_hole_is_slot(pad, hole_size_mils, slot_size_mils):
        return _pad_drill_feature(
            pad,
            layer,
            region=_circle_region(center, diameter_mm / 2.0),
            center=center,
            diameter_mm=diameter_mm,
            component_designator=component_designator,
        )
    slot_length_mm = _mils_to_mm(slot_size_mils)
    rotation = float(getattr(pad, "slot_rotation", 0.0) or 0.0) + float(
        getattr(pad, "rotation", 0.0) or 0.0
    )
    region = _capsule_region(
        center, slot_length_mm, diameter_mm, rotation, arc_segments
    )
    if region is None:
        return None
    return _pad_drill_feature(
        pad,
        layer,
        region=region,
        center=center,
        diameter_mm=diameter_mm,
        slot_length_mm=slot_length_mm,
        rotation_degrees=rotation,
        component_designator=component_designator,
    )


def _via_hole_region(via: Any) -> _Region | None:
    feature = _via_hole_feature(via)
    return feature.region if feature is not None else None


def _via_hole_feature(via: Any) -> _DrillFeature | None:
    hole_size_mils = float(getattr(via, "hole_size_mils", 0.0) or 0.0)
    if hole_size_mils <= 0.0:
        return None
    center = (_mils_to_mm(via.x_mils), _mils_to_mm(via.y_mils))
    diameter_mm = _mils_to_mm(hole_size_mils)
    return _DrillFeature(
        region=_circle_region(center, diameter_mm / 2.0),
        center=center,
        diameter_mm=diameter_mm,
        plated=bool(getattr(via, "is_plated", True)),
        source_kind="via",
    )


def _drill_overlay_region(
    feature: _DrillFeature,
    opts: PcbLayerStepOptions,
) -> _Region:
    if opts.drill_hole_shape != DRILL_HOLE_SHAPE_RING:
        return feature.region
    if opts.drill_ring_width_mm <= 0.0:
        return feature.region
    outer_diameter = feature.diameter_mm + (2.0 * opts.drill_ring_width_mm)
    if feature.slot_length_mm is not None:
        outer = _capsule_region(
            feature.center,
            feature.slot_length_mm + (2.0 * opts.drill_ring_width_mm),
            outer_diameter,
            feature.rotation_degrees,
            opts.arc_segments,
        )
        if outer is None:
            return feature.region
        return _Region(outer.outer, [feature.region.outer])
    outer = _circle_region(feature.center, outer_diameter / 2.0)
    return _Region(outer.outer, [feature.region.outer])


def _line_capsule_region(
    start: tuple[float, float], end: tuple[float, float], width_mm: float
) -> _Region | None:
    radius = width_mm / 2.0
    if radius <= 0.0:
        return None
    if _points_close(start, end):
        return _circle_region(start, radius)
    sx, sy = start
    ex, ey = end
    dx = ex - sx
    dy = ey - sy
    length = math.hypot(dx, dy)
    if length <= 1e-12:
        return _circle_region(start, radius)
    nx = -dy / length
    ny = dx / length
    points = [
        (sx + nx * radius, sy + ny * radius),
        (ex + nx * radius, ey + ny * radius),
        (ex - nx * radius, ey - ny * radius),
        (sx - nx * radius, sy - ny * radius),
    ]
    segments = [
        _Segment("line"),
        _Segment("arc", center=end, sweep="cw"),
        _Segment("line"),
        _Segment("arc", center=start, sweep="cw"),
    ]
    return _Region(_Ring(points, segments))


def _arc_stroke_region(
    *,
    center: tuple[float, float],
    radius_mm: float,
    start_degrees: float,
    sweep_degrees: float,
    width_mm: float,
) -> _Region | None:
    half_width = width_mm / 2.0
    outer_radius = radius_mm + half_width
    inner_radius = radius_mm - half_width
    if (
        outer_radius <= 0.0
        or inner_radius <= 0.0
        or math.isclose(sweep_degrees, 0.0, abs_tol=1e-9)
    ):
        return None
    end_degrees = start_degrees + sweep_degrees
    outer_start = _arc_point_from_angle_mm(center, outer_radius, start_degrees)
    outer_end = _arc_point_from_angle_mm(center, outer_radius, end_degrees)
    inner_end = _arc_point_from_angle_mm(center, inner_radius, end_degrees)
    inner_start = _arc_point_from_angle_mm(center, inner_radius, start_degrees)
    end_center = _arc_point_from_angle_mm(center, radius_mm, end_degrees)
    start_center = _arc_point_from_angle_mm(center, radius_mm, start_degrees)
    sweep = "ccw" if sweep_degrees > 0.0 else "cw"
    opposite = "cw" if sweep == "ccw" else "ccw"
    return _Region(
        _Ring(
            [outer_start, outer_end, inner_end, inner_start],
            [
                _Segment("arc", center=center, sweep=sweep),
                _Segment("arc", center=end_center, sweep=sweep),
                _Segment("arc", center=center, sweep=opposite),
                _Segment("arc", center=start_center, sweep=sweep),
            ],
        )
    )


def _capsule_region(
    center: tuple[float, float],
    length_mm: float,
    diameter_mm: float,
    rotation_degrees: float,
    arc_segments: int,
) -> _Region | None:
    del arc_segments
    straight = max(0.0, length_mm - diameter_mm)
    dx = (straight / 2.0) * math.cos(math.radians(rotation_degrees))
    dy = (straight / 2.0) * math.sin(math.radians(rotation_degrees))
    start = (center[0] - dx, center[1] - dy)
    end = (center[0] + dx, center[1] + dy)
    return _line_capsule_region(start, end, diameter_mm)


def _circle_region(center: tuple[float, float], radius_mm: float) -> _Region:
    cx, cy = center
    points = [
        (cx + radius_mm, cy),
        (cx, cy + radius_mm),
        (cx - radius_mm, cy),
        (cx, cy - radius_mm),
    ]
    segments = [_Segment("arc", center=center, sweep="ccw") for _ in range(4)]
    return _Region(_Ring(points, segments))


def _ellipse_region(
    center: tuple[float, float],
    radius_x_mm: float,
    radius_y_mm: float,
    rotation_degrees: float,
    samples: int,
) -> _Region:
    count = max(16, int(samples))
    points = [
        _rotate_point(
            (
                center[0] + radius_x_mm * math.cos(2.0 * math.pi * idx / count),
                center[1] + radius_y_mm * math.sin(2.0 * math.pi * idx / count),
            ),
            center,
            rotation_degrees,
        )
        for idx in range(count)
    ]
    return _Region(_Ring(points))


def _rectangle_region(
    *,
    center: tuple[float, float],
    width_mm: float,
    height_mm: float,
    rotation_degrees: float,
) -> _Region:
    cx, cy = center
    half_w = width_mm / 2.0
    half_h = height_mm / 2.0
    points = [
        (cx - half_w, cy - half_h),
        (cx + half_w, cy - half_h),
        (cx + half_w, cy + half_h),
        (cx - half_w, cy + half_h),
    ]
    if not math.isclose(rotation_degrees, 0.0, abs_tol=1e-9):
        points = [_rotate_point(point, center, rotation_degrees) for point in points]
    return _Region(_Ring(points))


def _rounded_rectangle_region(
    center: tuple[float, float],
    width_mm: float,
    height_mm: float,
    radius_mm: float,
    rotation_degrees: float,
) -> _Region:
    radius = max(0.0, min(radius_mm, width_mm / 2.0, height_mm / 2.0))
    if radius <= 1e-9:
        return _rectangle_region(
            center=center,
            width_mm=width_mm,
            height_mm=height_mm,
            rotation_degrees=rotation_degrees,
        )
    cx, cy = center
    half_w = width_mm / 2.0
    half_h = height_mm / 2.0
    centers = [
        (cx + half_w - radius, cy + half_h - radius),
        (cx - half_w + radius, cy + half_h - radius),
        (cx - half_w + radius, cy - half_h + radius),
        (cx + half_w - radius, cy - half_h + radius),
    ]
    points = [
        (cx + half_w, cy - half_h + radius),
        (cx + half_w, cy + half_h - radius),
        (cx + half_w - radius, cy + half_h),
        (cx - half_w + radius, cy + half_h),
        (cx - half_w, cy + half_h - radius),
        (cx - half_w, cy - half_h + radius),
        (cx - half_w + radius, cy - half_h),
        (cx + half_w - radius, cy - half_h),
    ]
    segments = [
        _Segment("line"),
        _Segment("arc", center=centers[0], sweep="ccw"),
        _Segment("line"),
        _Segment("arc", center=centers[1], sweep="ccw"),
        _Segment("line"),
        _Segment("arc", center=centers[2], sweep="ccw"),
        _Segment("line"),
        _Segment("arc", center=centers[3], sweep="ccw"),
    ]
    ring = _Ring(points, segments)
    if not math.isclose(rotation_degrees, 0.0, abs_tol=1e-9):
        ring = _rotate_ring(ring, center, rotation_degrees)
    return _Region(ring)


def _pad_shape_region(
    *,
    center: tuple[float, float],
    width_mm: float,
    height_mm: float,
    shape: int,
    rotation_degrees: float,
    corner_radius_percent: int,
    corner_radius_mm: float | None = None,
) -> _Region:
    if shape == int(PadShape.CIRCLE):
        if math.isclose(width_mm, height_mm, rel_tol=1e-9, abs_tol=1e-9):
            return _circle_region(center, width_mm / 2.0)
        length_mm = max(width_mm, height_mm)
        diameter_mm = min(width_mm, height_mm)
        axis_rotation = (
            rotation_degrees if width_mm >= height_mm else rotation_degrees + 90.0
        )
        region = _capsule_region(
            center,
            length_mm,
            diameter_mm,
            axis_rotation,
            arc_segments=32,
        )
        if region is not None:
            return region
        return _circle_region(center, diameter_mm / 2.0)
    if shape == int(PadShape.OCTAGONAL):
        points = _octagon_points(center[0], center[1], width_mm / 2.0, height_mm / 2.0)
        if not math.isclose(rotation_degrees, 0.0, abs_tol=1e-9):
            points = [
                _rotate_point(point, center, rotation_degrees) for point in points
            ]
        return _Region(_Ring(points))
    if shape == int(PadShape.ROUNDED_RECTANGLE):
        radius = (
            max(0.0, corner_radius_mm)
            if corner_radius_mm is not None
            else (max(0, corner_radius_percent) / 100.0)
            * min(width_mm, height_mm)
            / 2.0
        )
        return _rounded_rectangle_region(
            center, width_mm, height_mm, radius, rotation_degrees
        )
    return _rectangle_region(
        center=center,
        width_mm=width_mm,
        height_mm=height_mm,
        rotation_degrees=rotation_degrees,
    )


def _outline_stroke_regions(
    vertices: list[BoardOutlineVertex], width_mm: float
) -> list[_Region]:
    if len(vertices) < 2 or width_mm <= 0.0:
        return []
    regions: list[_Region] = []
    count = len(vertices)
    for idx, current in enumerate(vertices):
        nxt = vertices[(idx + 1) % count]
        start = (_mils_to_mm(current.x_mils), _mils_to_mm(current.y_mils))
        end = (_mils_to_mm(nxt.x_mils), _mils_to_mm(nxt.y_mils))
        if (
            bool(getattr(current, "is_arc", False))
            and float(getattr(current, "radius_mils", 0.0) or 0.0) > 0.0
        ):
            clockwise, sweep = resolve_outline_arc_segment(current, nxt)
            start_angle = math.degrees(
                math.atan2(
                    current.y_mils - current.center_y_mils,
                    current.x_mils - current.center_x_mils,
                )
            )
            region = _arc_stroke_region(
                center=(
                    _mils_to_mm(current.center_x_mils),
                    _mils_to_mm(current.center_y_mils),
                ),
                radius_mm=_mils_to_mm(current.radius_mils),
                start_degrees=start_angle,
                sweep_degrees=-sweep if clockwise else sweep,
                width_mm=width_mm,
            )
        else:
            region = _line_capsule_region(start, end, width_mm)
        if region is not None:
            regions.append(region)
    return regions


def _outline_ring(vertices: list[BoardOutlineVertex]) -> _Ring | None:
    if len(vertices) < 3:
        return None
    points: list[tuple[float, float]] = []
    segments: list[_Segment] = []
    count = len(vertices)
    for idx, current in enumerate(vertices):
        nxt = vertices[(idx + 1) % count]
        points.append((_mils_to_mm(current.x_mils), _mils_to_mm(current.y_mils)))
        if (
            bool(getattr(current, "is_arc", False))
            and float(getattr(current, "radius_mils", 0.0) or 0.0) > 0.0
        ):
            clockwise, _sweep = resolve_outline_arc_segment(current, nxt)
            segments.append(
                _Segment(
                    "arc",
                    center=(
                        _mils_to_mm(current.center_x_mils),
                        _mils_to_mm(current.center_y_mils),
                    ),
                    sweep="cw" if clockwise else "ccw",
                )
            )
        else:
            segments.append(_Segment("line"))
    return _Ring(points, segments)


def _extended_vertices_ring(vertices: list[Any]) -> _Ring | None:
    if len(vertices) < 3:
        return None
    points: list[tuple[float, float]] = []
    segments: list[_Segment] = []
    count = len(vertices)
    for idx, current in enumerate(vertices):
        nxt = vertices[(idx + 1) % count]
        points.append(
            (_mils_to_mm(float(current.x_mils)), _mils_to_mm(float(current.y_mils)))
        )
        if (
            bool(getattr(current, "is_round", False))
            and float(getattr(current, "radius_mils", 0.0) or 0.0) > 0.0
        ):
            raw_delta = float(getattr(current, "end_angle", 0.0) or 0.0) - float(
                getattr(current, "start_angle", 0.0) or 0.0
            )
            current_point = (float(current.x_mils), float(current.y_mils))
            next_point = (float(nxt.x_mils), float(nxt.y_mils))
            sweep = _svg_like_board_sweep_degrees(
                center_mils=(
                    float(current.center_x_mils),
                    float(current.center_y_mils),
                ),
                radius_mils=float(current.radius_mils),
                start_point_mils=current_point,
                end_point_mils=next_point,
                start_degrees=float(getattr(current, "start_angle", 0.0) or 0.0),
                end_degrees=float(getattr(current, "end_angle", 0.0) or 0.0),
                default_sweep_flag=1 if raw_delta >= 0.0 else 0,
            )
            segments.append(
                _Segment(
                    "arc",
                    center=(
                        _mils_to_mm(float(current.center_x_mils)),
                        _mils_to_mm(float(current.center_y_mils)),
                    ),
                    sweep="ccw" if sweep > 0.0 else "cw",
                )
            )
        else:
            segments.append(_Segment("line"))
    return _Ring(points, segments)


def _rotate_point(
    point: tuple[float, float],
    origin: tuple[float, float],
    rotation_degrees: float,
) -> tuple[float, float]:
    if math.isclose(rotation_degrees, 0.0, abs_tol=1e-12):
        return point
    angle = math.radians(rotation_degrees)
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    px, py = point
    ox, oy = origin
    dx = px - ox
    dy = py - oy
    return (ox + dx * cos_a - dy * sin_a, oy + dx * sin_a + dy * cos_a)


def _rotate_ring(
    ring: _Ring, origin: tuple[float, float], rotation_degrees: float
) -> _Ring:
    segments = [
        _Segment(
            kind=segment.kind,
            center=_rotate_point(segment.center, origin, rotation_degrees)
            if segment.center is not None
            else None,
            sweep=segment.sweep,
        )
        for segment in ring.segments
    ]
    return _Ring(
        [_rotate_point(point, origin, rotation_degrees) for point in ring.points],
        segments,
    )


def _sample_arc_points_mils(
    *,
    center_mils: tuple[float, float],
    radius_mils: float,
    start_degrees: float,
    end_degrees: float,
    arc_segments: int,
) -> list[tuple[float, float]]:
    if radius_mils <= 0.0:
        return []
    raw_delta = end_degrees - start_degrees
    sweep = _normalize_signed_sweep(raw_delta)
    return _sample_arc_points_for_sweep_mils(
        center_mils=center_mils,
        radius_mils=radius_mils,
        start_degrees=start_degrees,
        sweep_degrees=sweep,
        raw_delta_degrees=raw_delta,
        arc_segments=arc_segments,
    )


def _sample_svg_arc_points_mils(
    *,
    center_mils: tuple[float, float],
    radius_mils: float,
    start_point_mils: tuple[float, float],
    end_point_mils: tuple[float, float],
    start_degrees: float,
    end_degrees: float,
    default_sweep_flag: int,
    arc_segments: int,
) -> list[tuple[float, float]]:
    if radius_mils <= 0.0:
        return []
    raw_delta = end_degrees - start_degrees
    sweep = _svg_like_board_sweep_degrees(
        center_mils=center_mils,
        radius_mils=radius_mils,
        start_point_mils=start_point_mils,
        end_point_mils=end_point_mils,
        start_degrees=start_degrees,
        end_degrees=end_degrees,
        default_sweep_flag=default_sweep_flag,
    )
    start_angle = math.degrees(
        math.atan2(
            start_point_mils[1] - center_mils[1],
            start_point_mils[0] - center_mils[0],
        )
    )
    points = _sample_arc_points_for_sweep_mils(
        center_mils=center_mils,
        radius_mils=radius_mils,
        start_degrees=start_angle,
        sweep_degrees=sweep,
        raw_delta_degrees=raw_delta,
        arc_segments=arc_segments,
    )
    if not points:
        return []
    points[0] = start_point_mils
    points[-1] = end_point_mils
    return points


def _svg_like_board_sweep_degrees(
    *,
    center_mils: tuple[float, float],
    radius_mils: float,
    start_point_mils: tuple[float, float],
    end_point_mils: tuple[float, float],
    start_degrees: float,
    end_degrees: float,
    default_sweep_flag: int,
) -> float:
    raw_delta = end_degrees - start_degrees
    sweep_ccw = (end_degrees - start_degrees) % 360.0
    if math.isclose(sweep_ccw, 0.0, abs_tol=1e-9) and not math.isclose(
        raw_delta, 0.0, abs_tol=1e-9
    ):
        return 360.0 if raw_delta >= 0.0 else -360.0
    large_arc_int = 1 if sweep_ccw > 180.0 else 0

    sx, sy = start_point_mils
    ex, ey = end_point_mils
    cx, cy = center_mils
    sweep_flag = choose_svg_sweep_flag_for_center(
        sx,
        -sy,
        ex,
        -ey,
        radius_mils,
        large_arc_int,
        cx,
        -cy,
        default_sweep_flag=default_sweep_flag,
    )
    svg_sweep = _signed_svg_sweep_degrees(
        start_point=(sx, -sy),
        end_point=(ex, -ey),
        center=(cx, -cy),
        sweep_flag=sweep_flag,
    )
    return -svg_sweep


def _signed_svg_sweep_degrees(
    *,
    start_point: tuple[float, float],
    end_point: tuple[float, float],
    center: tuple[float, float],
    sweep_flag: int,
) -> float:
    sx, sy = start_point
    ex, ey = end_point
    cx, cy = center
    start = math.degrees(math.atan2(sy - cy, sx - cx))
    end = math.degrees(math.atan2(ey - cy, ex - cx))
    delta = (end - start) % 360.0
    if int(sweep_flag):
        return 360.0 if math.isclose(delta, 0.0, abs_tol=1e-9) else delta
    return -360.0 if math.isclose(delta, 0.0, abs_tol=1e-9) else delta - 360.0


def _sample_arc_points_for_sweep_mils(
    *,
    center_mils: tuple[float, float],
    radius_mils: float,
    start_degrees: float,
    sweep_degrees: float,
    raw_delta_degrees: float,
    arc_segments: int,
) -> list[tuple[float, float]]:
    sweep = sweep_degrees
    if math.isclose(sweep, 0.0, abs_tol=1e-9) and not math.isclose(
        raw_delta_degrees, 0.0, abs_tol=1e-9
    ):
        sweep = 360.0 if raw_delta_degrees >= 0.0 else -360.0
    samples = max(
        2, int(math.ceil(max(abs(sweep), 1.0) / 360.0 * max(8, arc_segments))) + 1
    )
    cx, cy = center_mils
    return [
        (
            cx
            + radius_mils
            * math.cos(math.radians(start_degrees + sweep * idx / (samples - 1))),
            cy
            + radius_mils
            * math.sin(math.radians(start_degrees + sweep * idx / (samples - 1))),
        )
        for idx in range(samples)
    ]


def _normalize_signed_sweep(raw_delta: float) -> float:
    if raw_delta >= 0.0:
        return raw_delta % 360.0
    return -((-raw_delta) % 360.0)


def _arc_point_from_angle_mils(
    center_mils: tuple[float, float], radius_mils: float, angle_degrees: float
) -> tuple[float, float]:
    cx, cy = center_mils
    return (
        cx + radius_mils * math.cos(math.radians(angle_degrees)),
        cy + radius_mils * math.sin(math.radians(angle_degrees)),
    )


def _arc_point_from_angle_mm(
    center_mm: tuple[float, float], radius_mm: float, angle_degrees: float
) -> tuple[float, float]:
    cx, cy = center_mm
    return (
        cx + radius_mm * math.cos(math.radians(angle_degrees)),
        cy + radius_mm * math.sin(math.radians(angle_degrees)),
    )


def _pad_should_render_on_layer(pad: Any, layer: PcbLayer) -> bool:
    try:
        return bool(pad._should_render_on_layer(layer)) or bool(
            pad._should_force_svg_copper_render(layer)
        )
    except Exception:
        source_layer = int(getattr(pad, "layer", 0) or 0)
        if source_layer == PcbLayer.MULTI_LAYER.value and layer.is_copper():
            return True
        return source_layer == layer.value


def _via_spans_layer(via: Any, layer: PcbLayer) -> bool:
    start = int(getattr(via, "layer_start", PcbLayer.TOP.value) or PcbLayer.TOP.value)
    end = int(getattr(via, "layer_end", PcbLayer.BOTTOM.value) or PcbLayer.BOTTOM.value)
    low = min(start, end)
    high = max(start, end)
    return low <= layer.value <= high


def _via_pad_removed_on_layer(via: Any, layer: PcbLayer) -> bool:
    idx = layer.value - 1
    removed = getattr(via, "is_pad_removed", []) or []
    return 0 <= idx < len(removed) and bool(removed[idx])


def _via_diameter_iu(via: Any, layer: PcbLayer) -> int:
    idx = layer.value - 1
    diameters = getattr(via, "diameter_by_layer", []) or []
    if 0 <= idx < len(diameters) and int(diameters[idx] or 0) > 0:
        return int(diameters[idx])
    return int(getattr(via, "diameter", 0) or 0)


def _pad_corner_radius_percent(pad: Any, layer: PcbLayer) -> int:
    idx = layer.value - 1
    corner_radius = getattr(pad, "corner_radius", []) or []
    corner_value = 0
    if 0 <= idx < len(corner_radius):
        raw_corner = corner_radius[idx]
        corner_value = int(0 if raw_corner is None else raw_corner)
    if corner_value > 0:
        return corner_value
    raw_percentage = getattr(pad, "corner_radius_percentage", 0)
    return int(0 if raw_percentage is None else raw_percentage)


def _is_poured_polygon_primitive(primitive: Any) -> bool:
    if bool(getattr(primitive, "is_polygon_outline", False)):
        return True
    polygon_index = getattr(primitive, "polygon_index", None)
    if polygon_index is None:
        return False
    try:
        polygon_index_int = int(polygon_index)
    except (TypeError, ValueError):
        return False
    return polygon_index_int not in {0, 0xFFFF}
