"""Generate a STEP alignment model for one PCB layer."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field, replace
import fnmatch
import json
import logging
import math
from pathlib import Path
import re
from typing import Any

from altium_monkey.altium_board import BoardOutlineVertex, resolve_outline_arc_segment
from altium_monkey.altium_pcb_enums import PadShape
from altium_monkey.altium_record_types import PcbLayer
from altium_monkey.altium_svg_arc_helpers import choose_svg_sweep_flag_for_center

from altium_cruncher.config_json import load_json_config

log = logging.getLogger(__name__)

MIL_TO_MM = 0.0254
INTERNAL_UNITS_PER_MIL = 10000.0
DEFAULT_COPPER_COLOR = "#B87333"
DEFAULT_OUTLINE_COLOR = "#111111"
DEFAULT_DRILL_HOLE_COLOR = "#FFFFFF"
DEFAULT_MAX_BOOLEAN_DRILL_CUTS = 128
PCB_LAYER_STEP_CONFIG_FILENAME = "pcb-layer-step.json"
PCB_LAYER_STEP_CONFIG_SCHEMA = "wn.altium_cruncher.pcb_layer_step.config.v1"
PCB_LAYER_STEP_CONFIG_SCHEMA_V2 = "wn.altium_cruncher.pcb_layer_step.config.v2"
DRILL_HOLE_MODE_AUTO = "auto"
DRILL_HOLE_MODE_CUT = "cut"
DRILL_HOLE_MODE_OVERLAY = "overlay"
DRILL_HOLE_MODE_NONE = "none"
DRILL_HOLE_SHAPE_SOLID = "solid"
DRILL_HOLE_SHAPE_RING = "ring"
DRILL_HOLE_SHAPES = frozenset({DRILL_HOLE_SHAPE_SOLID, DRILL_HOLE_SHAPE_RING})
DRILL_HOLE_MODES = frozenset(
    {
        DRILL_HOLE_MODE_AUTO,
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
    body: str = "matched_pads"


@dataclass(frozen=True, slots=True)
class PcbLayerStepOptions:
    """Options for one-layer PCB STEP export."""

    layer: PcbLayer = PcbLayer.BOTTOM
    thickness_mm: float = 0.035
    z_mm: float = 0.0
    copper_color: str = DEFAULT_COPPER_COLOR
    outline_width_mm: float = 0.2
    outline_color: str = DEFAULT_OUTLINE_COLOR
    include_copper: bool = True
    include_board_outline: bool = True
    include_poured_polygons: bool = True
    cut_holes: bool = True
    drill_hole_mode: str = DRILL_HOLE_MODE_AUTO
    max_boolean_drill_cuts: int = DEFAULT_MAX_BOOLEAN_DRILL_CUTS
    drill_hole_color: str = DEFAULT_DRILL_HOLE_COLOR
    drill_overlay_thickness_mm: float = 0.001
    drill_minimum_diameter_mm: float = 0.0
    drill_hole_shape: str = DRILL_HOLE_SHAPE_SOLID
    drill_ring_width_mm: float = 0.12
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


def _coerce_pad_color_rules(value: object) -> tuple[_PadColorRule, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ValueError(
            "pcb-layer-step config field 'colors.pad_rules' must be a list"
        )
    rules: list[_PadColorRule] = []
    for index, raw_rule in enumerate(value):
        if not isinstance(raw_rule, dict):
            raise ValueError(
                f"pcb-layer-step colors.pad_rules[{index}] must be an object"
            )
        designators = _coerce_str_tuple(raw_rule.get("designators"))
        if not designators:
            raise ValueError(
                f"pcb-layer-step colors.pad_rules[{index}] requires designators"
            )
        rules.append(
            _PadColorRule(
                designators=designators,
                color=_coerce_color(raw_rule.get("color"), DEFAULT_COPPER_COLOR),
                body=_step_name(str(raw_rule.get("body") or "matched_pads")),
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
        include_component_pads = str(component_pads.get("mode") or "all") != "none"
        component_pad_designators = component_pads.get(
            "include_designators",
            component_pad_designators,
        )
    elif component_pads is not None:
        include_component_pads = _coerce_bool(
            component_pads,
            default.include_component_pads,
        )
    return include_component_pads, component_pad_designators


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
    include_copper: bool = True
    include_board_outline: bool = True
    include_poured_polygons: bool = True
    cut_holes: bool = True
    drill_hole_mode: str = DRILL_HOLE_MODE_AUTO
    max_boolean_drill_cuts: int = DEFAULT_MAX_BOOLEAN_DRILL_CUTS
    drill_hole_color: str = DEFAULT_DRILL_HOLE_COLOR
    drill_overlay_thickness_mm: float = 0.001
    drill_minimum_diameter_mm: float = 0.0
    drill_hole_shape: str = DRILL_HOLE_SHAPE_SOLID
    drill_ring_width_mm: float = 0.12
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
        colors = _config_mapping(merged.get("colors"), "colors")
        drills = _config_mapping(merged.get("drills"), "drills")
        include_component_pads, component_pad_designators = _component_pad_settings(
            features=features,
            merged=merged,
            default=default,
        )
        cut_holes = _coerce_bool(merged.get("cut_holes"), default.cut_holes)
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
                colors.get("default_copper", merged.get("copper_color")),
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
            include_copper=_coerce_bool(
                merged.get("include_copper"), default.include_copper
            ),
            include_board_outline=_coerce_bool(
                merged.get("include_board_outline"), default.include_board_outline
            ),
            include_poured_polygons=_coerce_bool(
                features.get("polygons", merged.get("include_poured_polygons")),
                default.include_poured_polygons,
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
                drills.get("color", merged.get("drill_hole_color")),
                default.drill_hole_color,
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
            fuse_copper=_coerce_bool(merged.get("fuse_copper"), default.fuse_copper),
            fuse_board_outline=_coerce_bool(
                board_outline.get("fuse", merged.get("fuse_board_outline")),
                default.fuse_board_outline,
            ),
            arc_segments=int(
                _coerce_float(merged.get("arc_segments"), default.arc_segments)
            ),
            include_tracks=_coerce_bool(
                features.get("tracks", merged.get("include_tracks")),
                default.include_tracks,
            ),
            include_arcs=_coerce_bool(
                features.get("arcs", merged.get("include_arcs")),
                default.include_arcs,
            ),
            include_fills=_coerce_bool(
                features.get("fills", merged.get("include_fills")),
                default.include_fills,
            ),
            include_regions=_coerce_bool(
                features.get("regions", merged.get("include_regions")),
                default.include_regions,
            ),
            include_vias=_coerce_bool(
                features.get("vias", merged.get("include_vias")),
                default.include_vias,
            ),
            include_component_pads=include_component_pads,
            include_free_pads=_coerce_bool(
                features.get("free_pads", merged.get("include_free_pads")),
                default.include_free_pads,
            ),
            include_designators=_coerce_str_tuple(component_pad_designators),
            pad_color_rules=_coerce_pad_color_rules(colors.get("pad_rules")),
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
            "copper_color": self.copper_color,
            "outline_width_mm": self.outline_width_mm,
            "outline_color": self.outline_color,
            "include_copper": self.include_copper,
            "include_board_outline": self.include_board_outline,
            "include_poured_polygons": self.include_poured_polygons,
            "cut_holes": self.cut_holes,
            "drill_hole_mode": self.drill_hole_mode,
            "max_boolean_drill_cuts": self.max_boolean_drill_cuts,
            "drill_hole_color": self.drill_hole_color,
            "drill_overlay_thickness_mm": self.drill_overlay_thickness_mm,
            "drill_minimum_diameter_mm": self.drill_minimum_diameter_mm,
            "drill_hole_shape": self.drill_hole_shape,
            "drill_ring_width_mm": self.drill_ring_width_mm,
            "fuse_copper": self.fuse_copper,
            "fuse_board_outline": self.fuse_board_outline,
            "arc_segments": self.arc_segments,
            "include_tracks": self.include_tracks,
            "include_arcs": self.include_arcs,
            "include_fills": self.include_fills,
            "include_regions": self.include_regions,
            "include_vias": self.include_vias,
            "include_component_pads": self.include_component_pads,
            "include_free_pads": self.include_free_pads,
            "include_designators": list(self.include_designators),
            "pad_color_rules": [
                {
                    "designators": list(rule.designators),
                    "color": rule.color,
                    "body": rule.body,
                }
                for rule in self.pad_color_rules
            ],
        }

    def to_options(self) -> PcbLayerStepOptions:
        return PcbLayerStepOptions(
            layer=resolve_pcb_layer_selector(self.layer),
            thickness_mm=self.thickness_mm,
            z_mm=self.z_mm,
            copper_color=self.copper_color,
            outline_width_mm=self.outline_width_mm,
            outline_color=self.outline_color,
            include_copper=self.include_copper,
            include_board_outline=self.include_board_outline,
            include_poured_polygons=self.include_poured_polygons,
            cut_holes=self.cut_holes,
            drill_hole_mode=self.drill_hole_mode,
            max_boolean_drill_cuts=self.max_boolean_drill_cuts,
            drill_hole_color=self.drill_hole_color,
            drill_overlay_thickness_mm=self.drill_overlay_thickness_mm,
            drill_minimum_diameter_mm=self.drill_minimum_diameter_mm,
            drill_hole_shape=self.drill_hole_shape,
            drill_ring_width_mm=self.drill_ring_width_mm,
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


def resolve_pcb_layer_selector(selector: str | int | PcbLayer | None) -> PcbLayer:
    """Resolve CLI/user layer selectors to a native Altium PCB layer enum."""
    if selector is None:
        return PcbLayer.BOTTOM
    if isinstance(selector, PcbLayer):
        return selector
    if isinstance(selector, int):
        return PcbLayer(selector)

    text = str(selector).strip()
    if not text:
        return PcbLayer.BOTTOM
    if text.isdigit():
        return PcbLayer(int(text))

    normalized = re.sub(r"[\s_\-]+", "", text).upper()
    if normalized.startswith("L") and normalized[1:].isdigit():
        return PcbLayer(int(normalized[1:]))

    aliases = {
        "TOP": PcbLayer.TOP,
        "TOPLAYER": PcbLayer.TOP,
        "FRONT": PcbLayer.TOP,
        "BOTTOM": PcbLayer.BOTTOM,
        "BOTTOMLAYER": PcbLayer.BOTTOM,
        "BOT": PcbLayer.BOTTOM,
        "BACK": PcbLayer.BOTTOM,
        "MULTILAYER": PcbLayer.MULTI_LAYER,
    }
    if normalized in aliases:
        return aliases[normalized]

    for layer in PcbLayer:
        names = {
            re.sub(r"[\s_\-]+", "", layer.name).upper(),
            re.sub(r"[\s_\-]+", "", layer.to_json_name()).upper(),
            re.sub(r"[\s_\-]+", "", layer.to_display_name()).upper(),
        }
        if normalized in names:
            return layer

    raise ValueError(f"Unknown PCB layer selector: {selector!r}")


def write_default_pcb_layer_step_config(config_path: Path) -> None:
    """Write a default editable pcb-layer-step JSON config."""
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        _default_pcb_layer_step_config_text(),
        encoding="utf-8",
    )


def _default_pcb_layer_step_config_text() -> str:
    return """{
  /* pcb-layer-step creates compact fixture-alignment models, not full
     fabrication STEP exports. Keep only the features that help verify pogo-pin
     alignment against DUT pads. */
  "schema": "wn.altium_cruncher.pcb_layer_step.config.v2",
  "defaults": {
    "pcbdoc": null,
    "layer": "bottom",
    "z_mm": 0.0,
    "thickness_mm": 0.035,
    "include_board_outline": true,
    "board_outline": {
      "color": "#111111",
      "width_mm": 0.2,
      "fuse": true
    }
  },
  "outputs": [
    {
      "name": "fixture_alignment",
      "output_step": "{board}__fixture_alignment.step",
      "features": {
        /* Use include_designators for component-owned pads. Examples:
           ["TP*"] or ["TP*", "J*", "U1", "U2"]. */
        "component_pads": {
          "mode": "matching_designators",
          "include_designators": ["TP*"]
        },
        "free_pads": false,
        "tracks": true,
        "arcs": true,
        "fills": false,
        "polygons": false,
        "regions": false,
        "vias": false
      },
      "colors": {
        "default_copper": "#B87333",
        "pad_rules": [
          {
            "designators": ["TP*"],
            "color": "red",
            "body": "test_points"
          }
        ]
      },
      "drills": {
        /* none omits drills, cut performs boolean holes, overlay draws a
           separate drill-reference body. */
        "mode": "overlay",
        "minimum_diameter_mm": 0.85,
        "shape": "ring",
        "color": "#666666",
        "ring_width_mm": 0.12,
        "overlay_thickness_mm": 0.001
      },
      "fuse_copper": false
    }
  ]
}
"""


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

    features = _collect_layer_features(pcbdoc, layer, opts)
    drill_features = _collect_drill_features(pcbdoc, layer, opts)
    drill_hole_mode = _effective_drill_hole_mode(opts, len(drill_features))
    bodies, counts = _build_step_bodies(
        pcbdoc=pcbdoc,
        opts=opts,
        features=features,
        drill_features=drill_features,
        drill_hole_mode=drill_hole_mode,
    )
    if not bodies:
        raise ValueError(f"No geometry found for layer {layer.to_display_name()}")

    request = {
        "schema": "geometry.planar_step.request.a0",
        "units": "mm",
        "name": _step_name(resolved_board_name),
        "bodies": bodies,
    }
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
) -> dict[str, Any]:
    return {
        "schema": "wn.altium_cruncher.pcb_layer_step.v1",
        "backend": "geometer.planar_step",
        "board": board_name,
        "source_input": source_input,
        "step_file": output_path.name,
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
            "include_copper": bool(opts.include_copper),
            "include_board_outline": bool(opts.include_board_outline),
            "include_poured_polygons": bool(opts.include_poured_polygons),
            "cut_holes": bool(opts.cut_holes),
            "drill_hole_mode": opts.drill_hole_mode,
            "effective_drill_hole_mode": drill_hole_mode,
            "max_boolean_drill_cuts": int(opts.max_boolean_drill_cuts),
            "drill_hole_color": opts.drill_hole_color,
            "drill_overlay_thickness_mm": float(opts.drill_overlay_thickness_mm),
            "drill_minimum_diameter_mm": float(opts.drill_minimum_diameter_mm),
            "drill_hole_shape": opts.drill_hole_shape,
            "drill_ring_width_mm": float(opts.drill_ring_width_mm),
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
                    "body": rule.body,
                }
                for rule in opts.pad_color_rules
            ],
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
    boolean_drill_cutouts = [
        feature.region
        for feature in drill_features
        if drill_hole_mode == DRILL_HOLE_MODE_CUT
    ]
    shared_cutouts = [*boolean_drill_cutouts, *board_cutouts]
    bodies = [
        *_copper_bodies_from_features(features, opts, shared_cutouts),
        *_drill_overlay_bodies(drill_features, drill_hole_mode, opts),
        *_outline_bodies(pcbdoc, opts),
    ]
    counts = _build_counts(
        features=features,
        drill_features=drill_features,
        boolean_drill_cutouts=boolean_drill_cutouts,
        drill_hole_mode=drill_hole_mode,
        board_cutouts=board_cutouts,
        bodies=bodies,
    )
    return bodies, counts


def _copper_bodies_from_features(
    features: list[_SourceFeature],
    opts: PcbLayerStepOptions,
    cutouts: list[_Region],
) -> list[dict[str, Any]]:
    if not opts.include_copper:
        return []
    grouped: dict[tuple[str, str], list[_Region]] = {}
    for feature in features:
        body_id, color = _body_style_for_feature(feature, opts)
        grouped.setdefault((body_id, color), []).append(feature.region)
    return [
        _body_from_regions(
            body_id=body_id,
            color=color,
            regions=regions,
            z_mm=opts.z_mm,
            thickness_mm=opts.thickness_mm,
            fuse_regions=opts.fuse_copper,
            cutouts=cutouts,
        )
        for (body_id, color), regions in grouped.items()
        if regions
    ]


def _body_style_for_feature(
    feature: _SourceFeature,
    opts: PcbLayerStepOptions,
) -> tuple[str, str]:
    if feature.kind in {"component_pad", "free_pad"}:
        designator = feature.component_designator or feature.pad_designator or ""
        for rule in opts.pad_color_rules:
            if _matches_any_pattern(designator, rule.designators):
                return rule.body, rule.color
    return "copper", opts.copper_color


def _drill_overlay_bodies(
    drill_features: list[_DrillFeature],
    drill_hole_mode: str,
    opts: PcbLayerStepOptions,
) -> list[dict[str, Any]]:
    if drill_hole_mode != DRILL_HOLE_MODE_OVERLAY or not drill_features:
        return []
    return [
        _body_from_regions(
            body_id="drill_holes",
            color=opts.drill_hole_color,
            regions=[
                _drill_overlay_region(feature, opts) for feature in drill_features
            ],
            z_mm=opts.z_mm + opts.thickness_mm,
            thickness_mm=max(0.0001, opts.drill_overlay_thickness_mm),
            fuse_regions=False,
            cutouts=[],
        )
    ]


def _outline_bodies(pcbdoc: Any, opts: PcbLayerStepOptions) -> list[dict[str, Any]]:
    outline_regions = (
        _collect_board_outline_regions(pcbdoc, opts)
        if opts.include_board_outline and opts.outline_width_mm > 0.0
        else []
    )
    if not outline_regions:
        return []
    return [
        _body_from_regions(
            body_id="board_outline",
            color=opts.outline_color,
            regions=outline_regions,
            z_mm=opts.z_mm,
            thickness_mm=opts.thickness_mm,
            fuse_regions=opts.fuse_board_outline,
            cutouts=[],
        )
    ]


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
    boolean_drill_cutouts: list[_Region],
    drill_hole_mode: str,
    board_cutouts: list[_Region],
    bodies: list[dict[str, Any]],
) -> dict[str, int]:
    return {
        "source_layer_geometries": len(features),
        "drill_cut_geometries": len(drill_features),
        "drill_boolean_cut_geometries": len(boolean_drill_cutouts),
        "drill_overlay_geometries": len(drill_features)
        if drill_hole_mode == DRILL_HOLE_MODE_OVERLAY
        else 0,
        "board_cutout_geometries": len(board_cutouts),
        "copper_bodies": sum(
            1
            for body in bodies
            if str(body.get("id")) not in {"board_outline", "drill_holes"}
        ),
        "outline_bodies": sum(
            1 for body in bodies if str(body.get("id")) == "board_outline"
        ),
        "body_count": len(bodies),
    }


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


def _collect_layer_features(
    pcbdoc: Any,
    layer: PcbLayer,
    opts: PcbLayerStepOptions,
) -> list[_SourceFeature]:
    features: list[_SourceFeature] = []
    if opts.include_tracks:
        features.extend(_track_features(pcbdoc, layer, opts))
    if opts.include_arcs:
        features.extend(_arc_features(pcbdoc, layer, opts))
    if opts.include_fills:
        features.extend(_fill_features(pcbdoc, layer, opts))
    if layer.is_copper():
        features.extend(_pad_features(pcbdoc, layer, opts))
        if opts.include_vias:
            features.extend(_via_features(pcbdoc, layer))
    if opts.include_regions:
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
        if _is_poured_polygon_primitive(track) and not opts.include_poured_polygons:
            continue
        region = _track_region(track)
        if region is not None:
            features.append(_SourceFeature("track", region))
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
        if _is_poured_polygon_primitive(arc) and not opts.include_poured_polygons:
            continue
        region = _arc_region(arc)
        if region is not None:
            features.append(_SourceFeature("arc", region))
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
        if _is_poured_polygon_primitive(fill) and not opts.include_poured_polygons:
            continue
        region = _fill_region(fill)
        if region is not None:
            features.append(_SourceFeature("fill", region))
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
    if _is_poured_polygon_primitive(region) and not opts.include_poured_polygons:
        return None
    converted = _region_from_outline_vertices(region)
    return _SourceFeature("region", converted) if converted is not None else None


def _shapebased_region_feature(
    region: Any,
    layer: PcbLayer,
    opts: PcbLayerStepOptions,
) -> _SourceFeature | None:
    if int(getattr(region, "layer", 0) or 0) != layer.value:
        return None
    if bool(getattr(region, "is_keepout", False)):
        return None
    if _is_poured_polygon_primitive(region) and not opts.include_poured_polygons:
        return None
    converted = _shapebased_region(region)
    return (
        _SourceFeature("shapebased_region", converted)
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
        feature = _pad_hole_feature(pad, layer, opts.arc_segments)
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


def _collect_layer_regions(
    pcbdoc: Any,
    layer: PcbLayer,
    opts: PcbLayerStepOptions,
) -> list[_Region]:
    regions: list[_Region] = []

    for track in getattr(pcbdoc, "tracks", []) or []:
        if int(getattr(track, "layer", 0) or 0) != layer.value:
            continue
        if _is_poured_polygon_primitive(track) and not opts.include_poured_polygons:
            continue
        region = _track_region(track)
        if region is not None:
            regions.append(region)

    for arc in getattr(pcbdoc, "arcs", []) or []:
        if int(getattr(arc, "layer", 0) or 0) != layer.value:
            continue
        if _is_poured_polygon_primitive(arc) and not opts.include_poured_polygons:
            continue
        region = _arc_region(arc)
        if region is not None:
            regions.append(region)

    for fill in getattr(pcbdoc, "fills", []) or []:
        if int(getattr(fill, "layer", 0) or 0) != layer.value:
            continue
        if _is_poured_polygon_primitive(fill) and not opts.include_poured_polygons:
            continue
        region = _fill_region(fill)
        if region is not None:
            regions.append(region)

    if layer.is_copper():
        for pad in getattr(pcbdoc, "pads", []) or []:
            region = _pad_region(pad, layer)
            if region is not None:
                regions.append(region)
        for via in getattr(pcbdoc, "vias", []) or []:
            region = _via_region(via, layer)
            if region is not None:
                regions.append(region)

    for region in getattr(pcbdoc, "regions", []) or []:
        if int(getattr(region, "layer", 0) or 0) != layer.value:
            continue
        if bool(getattr(region, "is_board_cutout", False)) or bool(
            getattr(region, "is_keepout", False)
        ):
            continue
        if _is_poured_polygon_primitive(region) and not opts.include_poured_polygons:
            continue
        converted = _region_from_outline_vertices(region)
        if converted is not None:
            regions.append(converted)

    for region in getattr(pcbdoc, "shapebased_regions", []) or []:
        if int(getattr(region, "layer", 0) or 0) != layer.value:
            continue
        if bool(getattr(region, "is_keepout", False)):
            continue
        if _is_poured_polygon_primitive(region) and not opts.include_poured_polygons:
            continue
        converted = _shapebased_region(region)
        if converted is not None:
            regions.append(converted)

    return [region for region in regions if len(region.outer.points) >= 3]


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
    for cutout in getattr(outline, "cutouts", []) or []:
        regions.extend(_outline_stroke_regions(cutout, opts.outline_width_mm))
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


def _pad_hole_feature(
    pad: Any,
    layer: PcbLayer,
    arc_segments: int,
) -> _DrillFeature | None:
    hole_size_mils = float(getattr(pad, "hole_size_mils", 0.0) or 0.0)
    if hole_size_mils <= 0.0:
        return None
    try:
        cx_mils, cy_mils = pad.hole_center_mils(layer)
    except Exception:
        cx_mils = _iu_to_mils(getattr(pad, "x", 0))
        cy_mils = _iu_to_mils(getattr(pad, "y", 0))
    center = (_mils_to_mm(cx_mils), _mils_to_mm(cy_mils))
    diameter_mm = _mils_to_mm(hole_size_mils)
    slot_size_mils = _iu_to_mils(getattr(pad, "slot_size", 0))
    is_slot = (
        int(getattr(pad, "hole_shape", 0) or 0) == 2 and slot_size_mils > hole_size_mils
    )
    if not is_slot:
        return _DrillFeature(
            region=_circle_region(center, diameter_mm / 2.0),
            center=center,
            diameter_mm=diameter_mm,
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
    return _DrillFeature(
        region=region,
        center=center,
        diameter_mm=diameter_mm,
        slot_length_mm=slot_length_mm,
        rotation_degrees=rotation,
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
    )


def _drill_overlay_region(
    feature: _DrillFeature,
    opts: PcbLayerStepOptions,
) -> _Region:
    if (
        opts.drill_hole_shape != DRILL_HOLE_SHAPE_RING
        or opts.drill_ring_width_mm <= 0.0
    ):
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
) -> _Region:
    if shape == int(PadShape.CIRCLE):
        if math.isclose(width_mm, height_mm, rel_tol=1e-9, abs_tol=1e-9):
            return _circle_region(center, width_mm / 2.0)
        return _ellipse_region(
            center, width_mm / 2.0, height_mm / 2.0, rotation_degrees, 48
        )
    if shape == int(PadShape.OCTAGONAL):
        points = _octagon_points(center[0], center[1], width_mm / 2.0, height_mm / 2.0)
        if not math.isclose(rotation_degrees, 0.0, abs_tol=1e-9):
            points = [
                _rotate_point(point, center, rotation_degrees) for point in points
            ]
        return _Region(_Ring(points))
    if shape == int(PadShape.ROUNDED_RECTANGLE):
        radius = (
            (max(0, corner_radius_percent) / 100.0) * min(width_mm, height_mm) / 2.0
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


def _octagon_points(
    cx: float, cy: float, half_w: float, half_h: float
) -> list[tuple[float, float]]:
    chamfer = min(half_w, half_h) / 2.0
    return [
        (cx + half_w, cy - (half_h - chamfer)),
        (cx + half_w, cy + half_h - chamfer),
        (cx + half_w - chamfer, cy + half_h),
        (cx - (half_w - chamfer), cy + half_h),
        (cx - half_w, cy + half_h - chamfer),
        (cx - half_w, cy - (half_h - chamfer)),
        (cx - (half_w - chamfer), cy - half_h),
        (cx + half_w - chamfer, cy - half_h),
    ]


def _mils_to_mm(value: float) -> float:
    return float(value) * MIL_TO_MM


def _iu_to_mils(value: Any) -> float:
    return float(value or 0.0) / INTERNAL_UNITS_PER_MIL


def _points_close(
    a: tuple[float, float], b: tuple[float, float], tol: float = 1e-9
) -> bool:
    return math.isclose(a[0], b[0], abs_tol=tol) and math.isclose(
        a[1], b[1], abs_tol=tol
    )


def _dedupe_closed_points(
    points: list[tuple[float, float]],
) -> list[tuple[float, float]]:
    deduped: list[tuple[float, float]] = []
    for x, y in points:
        point = (float(x), float(y))
        if deduped and _points_close(deduped[-1], point):
            continue
        deduped.append(point)
    if len(deduped) > 1 and _points_close(deduped[0], deduped[-1]):
        deduped.pop()
    return deduped


def _board_name_from_pcbdoc(pcbdoc: Any) -> str:
    filepath = getattr(pcbdoc, "filepath", None)
    if filepath:
        return Path(filepath).stem
    return "board"


def _step_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]+", "_", value).strip("_") or "board"


def layer_step_output_name(board_name: str, layer: PcbLayer) -> str:
    """Return the conventional filename for one generated layer STEP artifact."""
    layer_name = re.sub(r"[^A-Za-z0-9]+", "_", layer.to_json_name().lower()).strip("_")
    return f"{_step_name(board_name)}__{layer_name}_layer.step"
