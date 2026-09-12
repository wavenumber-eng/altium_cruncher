"""Resolved STEP export options and rendering policy constants.

Defaults come from TypeSpec metadata. Config interpretation lives in the STEP
adapter; geometry generation consumes this immutable options record.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from altium_monkey.altium_record_types import PcbLayer
from .contracts.workflows import domain_default
from .altium_cruncher_pcb_layer_step_highlights import PcbLayerStepHighlight


DEFAULT_COPPER_COLOR = "#B87333"
DEFAULT_OUTLINE_COLOR = "#FFFF00"
DEFAULT_BOARD_CUTOUT_COLOR = "#FFFF00"
DEFAULT_DRILL_HOLE_COLOR = "#FFFFFF"
DEFAULT_MAX_BOOLEAN_DRILL_CUTS = 128
PCB_LAYER_STEP_CONFIG_FILENAME = "pcb-layer-step.jsonc"
PCB_LAYER_STEP_LEGACY_CONFIG_FILENAME = "pcb-layer-step.json"
PCB_LAYER_STEP_CONFIG_SCHEMA = "altium_cruncher.pcb_layer_step.config.a0"
PCB_LAYER_STEP_CONFIG_SCHEMA_V2 = "altium_cruncher.pcb_layer_step.config.a0"
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

    layer: PcbLayer = PcbLayer(
        domain_default("pcb_layer_step_config", "PcbLayerStepOptions", "layer")
    )
    thickness_mm: float = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "thickness_mm"
    )
    z_mm: float = domain_default("pcb_layer_step_config", "PcbLayerStepOptions", "z_mm")
    copper_color: str = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "copper_color"
    )
    outline_width_mm: float = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "outline_width_mm"
    )
    outline_color: str = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "outline_color"
    )
    board_cutout_color: str = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "board_cutout_color"
    )
    include_board_cutouts: bool = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "include_board_cutouts"
    )
    include_copper: bool = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "include_copper"
    )
    include_board_outline: bool = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "include_board_outline"
    )
    include_poured_polygons: bool = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "include_poured_polygons"
    )
    cut_holes: bool = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "cut_holes"
    )
    drill_hole_mode: str = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "drill_hole_mode"
    )
    max_boolean_drill_cuts: int = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "max_boolean_drill_cuts"
    )
    drill_hole_color: str = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "drill_hole_color"
    )
    drill_plated_hole_color: str = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "drill_plated_hole_color"
    )
    drill_non_plated_hole_color: str = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "drill_non_plated_hole_color"
    )
    drill_overlay_thickness_mm: float = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "drill_overlay_thickness_mm"
    )
    drill_minimum_diameter_mm: float = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "drill_minimum_diameter_mm"
    )
    drill_hole_shape: str = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "drill_hole_shape"
    )
    drill_ring_width_mm: float = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "drill_ring_width_mm"
    )
    drill_plated_ring_shape: str = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "drill_plated_ring_shape"
    )
    drill_selected_component_mode: str = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "drill_selected_component_mode"
    )
    drill_other_component_mode: str = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "drill_other_component_mode"
    )
    drill_free_pad_mode: str = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "drill_free_pad_mode"
    )
    drill_via_mode: str = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "drill_via_mode"
    )
    fuse_copper: bool = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "fuse_copper"
    )
    fuse_board_outline: bool = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "fuse_board_outline"
    )
    arc_segments: int = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "arc_segments"
    )
    include_tracks: bool = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "include_tracks"
    )
    include_arcs: bool = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "include_arcs"
    )
    include_fills: bool = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "include_fills"
    )
    include_regions: bool = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "include_regions"
    )
    include_vias: bool = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "include_vias"
    )
    include_component_pads: bool = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "include_component_pads"
    )
    include_free_pads: bool = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "include_free_pads"
    )
    include_designators: tuple[str, ...] = field(
        default_factory=lambda: tuple(
            domain_default(
                "pcb_layer_step_config", "PcbLayerStepOptions", "include_designators"
            )
        )
    )
    pad_color_rules: tuple[_PadColorRule, ...] = field(
        default_factory=lambda: tuple(
            domain_default(
                "pcb_layer_step_config", "PcbLayerStepOptions", "pad_color_rules"
            )
        )
    )
    track_color: str | None = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "track_color"
    )
    track_body: str = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "track_body"
    )
    arc_color: str | None = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "arc_color"
    )
    arc_body: str = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "arc_body"
    )
    fill_color: str | None = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "fill_color"
    )
    fill_body: str = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "fill_body"
    )
    polygon_color: str | None = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "polygon_color"
    )
    polygon_body: str = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "polygon_body"
    )
    region_color: str | None = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "region_color"
    )
    region_body: str = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "region_body"
    )
    via_color: str | None = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "via_color"
    )
    via_body: str = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "via_body"
    )
    component_pad_color: str | None = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "component_pad_color"
    )
    component_pad_body: str = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "component_pad_body"
    )
    free_pad_color: str | None = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "free_pad_color"
    )
    free_pad_body: str = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "free_pad_body"
    )
    track_thickness_bias_mm: float = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "track_thickness_bias_mm"
    )
    arc_thickness_bias_mm: float = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "arc_thickness_bias_mm"
    )
    fill_thickness_bias_mm: float = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "fill_thickness_bias_mm"
    )
    polygon_thickness_bias_mm: float = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "polygon_thickness_bias_mm"
    )
    region_thickness_bias_mm: float = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "region_thickness_bias_mm"
    )
    via_thickness_bias_mm: float = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "via_thickness_bias_mm"
    )
    component_pad_thickness_bias_mm: float = domain_default(
        "pcb_layer_step_config",
        "PcbLayerStepOptions",
        "component_pad_thickness_bias_mm",
    )
    free_pad_thickness_bias_mm: float = domain_default(
        "pcb_layer_step_config", "PcbLayerStepOptions", "free_pad_thickness_bias_mm"
    )
    highlights: tuple["PcbLayerStepHighlight", ...] = field(
        default_factory=lambda: tuple(
            domain_default("pcb_layer_step_config", "PcbLayerStepOptions", "highlights")
        )
    )
