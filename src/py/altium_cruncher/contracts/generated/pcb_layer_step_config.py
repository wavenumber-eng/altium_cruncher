"""Generated from src/tsp/altium_cruncher/config/pcb-layer-step-config.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

PcbLayerStepConfigInput = TypedDict("PcbLayerStepConfigInput", {
    "schema": NotRequired["Literal[\"altium_cruncher.pcb_layer_step.config.a0\"] | None"],
    "defaults": NotRequired["OutputOptions"],
    "outputs": NotRequired["list[OutputOptions]"],
    "options": NotRequired["OutputOptions"],
    "name": NotRequired["str | None"],
    "output_step": NotRequired["str | None"],
    "pcbdoc": NotRequired["str | None"],
    "layer": NotRequired["LayerSelector"],
    "thickness_mm": NotRequired["float"],
    "z_mm": NotRequired["float"],
    "copper_color": NotRequired["Color"],
    "outline_width_mm": NotRequired["float"],
    "outline_color": NotRequired["Color"],
    "board_cutout_color": NotRequired["Color"],
    "include_board_cutouts": NotRequired["bool"],
    "include_copper": NotRequired["bool"],
    "include_board_outline": NotRequired["bool"],
    "include_poured_polygons": NotRequired["bool"],
    "cut_holes": NotRequired["bool"],
    "drill_hole_mode": NotRequired["DrillMode"],
    "max_boolean_drill_cuts": NotRequired["int"],
    "drill_hole_color": NotRequired["Color"],
    "drill_plated_hole_color": NotRequired["Color"],
    "drill_non_plated_hole_color": NotRequired["Color"],
    "drill_overlay_thickness_mm": NotRequired["float"],
    "drill_minimum_diameter_mm": NotRequired["float"],
    "drill_hole_shape": NotRequired["DrillShape"],
    "drill_ring_width_mm": NotRequired["float"],
    "drill_plated_ring_shape": NotRequired["PlatedRingShape"],
    "drill_selected_component_mode": NotRequired["DrillScopedMode"],
    "drill_other_component_mode": NotRequired["DrillScopedMode"],
    "drill_free_pad_mode": NotRequired["DrillScopedMode"],
    "drill_via_mode": NotRequired["DrillScopedMode"],
    "fuse_copper": NotRequired["bool"],
    "fuse_board_outline": NotRequired["bool"],
    "arc_segments": NotRequired["int"],
    "include_tracks": NotRequired["bool"],
    "include_arcs": NotRequired["bool"],
    "include_fills": NotRequired["bool"],
    "include_regions": NotRequired["bool"],
    "include_vias": NotRequired["bool"],
    "include_component_pads": NotRequired["bool"],
    "include_free_pads": NotRequired["bool"],
    "include_designators": NotRequired["StringList"],
    "board_outline": NotRequired["BoardOutline"],
    "features": NotRequired["Features"],
    "drills": NotRequired["Drills"],
}, closed=True)

OutputOptions = TypedDict("OutputOptions", {
    "options": NotRequired["OutputOptions"],
    "name": NotRequired["str | None"],
    "output_step": NotRequired["str | None"],
    "pcbdoc": NotRequired["str | None"],
    "layer": NotRequired["LayerSelector"],
    "thickness_mm": NotRequired["float"],
    "z_mm": NotRequired["float"],
    "copper_color": NotRequired["Color"],
    "outline_width_mm": NotRequired["float"],
    "outline_color": NotRequired["Color"],
    "board_cutout_color": NotRequired["Color"],
    "include_board_cutouts": NotRequired["bool"],
    "include_copper": NotRequired["bool"],
    "include_board_outline": NotRequired["bool"],
    "include_poured_polygons": NotRequired["bool"],
    "cut_holes": NotRequired["bool"],
    "drill_hole_mode": NotRequired["DrillMode"],
    "max_boolean_drill_cuts": NotRequired["int"],
    "drill_hole_color": NotRequired["Color"],
    "drill_plated_hole_color": NotRequired["Color"],
    "drill_non_plated_hole_color": NotRequired["Color"],
    "drill_overlay_thickness_mm": NotRequired["float"],
    "drill_minimum_diameter_mm": NotRequired["float"],
    "drill_hole_shape": NotRequired["DrillShape"],
    "drill_ring_width_mm": NotRequired["float"],
    "drill_plated_ring_shape": NotRequired["PlatedRingShape"],
    "drill_selected_component_mode": NotRequired["DrillScopedMode"],
    "drill_other_component_mode": NotRequired["DrillScopedMode"],
    "drill_free_pad_mode": NotRequired["DrillScopedMode"],
    "drill_via_mode": NotRequired["DrillScopedMode"],
    "fuse_copper": NotRequired["bool"],
    "fuse_board_outline": NotRequired["bool"],
    "arc_segments": NotRequired["int"],
    "include_tracks": NotRequired["bool"],
    "include_arcs": NotRequired["bool"],
    "include_fills": NotRequired["bool"],
    "include_regions": NotRequired["bool"],
    "include_vias": NotRequired["bool"],
    "include_component_pads": NotRequired["bool"],
    "include_free_pads": NotRequired["bool"],
    "include_designators": NotRequired["StringList"],
    "board_outline": NotRequired["BoardOutline"],
    "features": NotRequired["Features"],
    "drills": NotRequired["Drills"],
}, closed=True)

BoardOutline = TypedDict("BoardOutline", {
    "color": NotRequired["Color"],
    "cutout_color": NotRequired["Color"],
    "cutouts_color": NotRequired["Color"],
    "cutouts": NotRequired["bool"],
    "width_mm": NotRequired["float"],
    "fuse": NotRequired["bool"],
}, closed=True)

Features = TypedDict("Features", {
    "defaults": NotRequired["FeatureDefaults"],
    "tracks": NotRequired["FeatureSwitch"],
    "traces": NotRequired["FeatureSwitch"],
    "arcs": NotRequired["FeatureSwitch"],
    "fills": NotRequired["FeatureSwitch"],
    "polygons": NotRequired["FeatureSwitch"],
    "poured_polygons": NotRequired["FeatureSwitch"],
    "regions": NotRequired["FeatureSwitch"],
    "shapebased_regions": NotRequired["FeatureSwitch"],
    "vias": NotRequired["FeatureSwitch"],
    "component_pads": NotRequired["FeaturesComponentPads"],
    "free_pads": NotRequired["FeatureSwitch"],
}, closed=True)

Drills = TypedDict("Drills", {
    "mode": NotRequired["DrillMode"],
    "minimum_diameter_mm": NotRequired["float"],
    "shape": NotRequired["DrillShape"],
    "color": NotRequired["Color"],
    "plated_color": NotRequired["Color"],
    "non_plated_color": NotRequired["Color"],
    "ring_width_mm": NotRequired["float"],
    "plated_ring_shape": NotRequired["PlatedRingShape"],
    "selected_component_mode": NotRequired["DrillScopedMode"],
    "other_component_mode": NotRequired["DrillScopedMode"],
    "free_pad_mode": NotRequired["DrillScopedMode"],
    "via_mode": NotRequired["DrillScopedMode"],
    "overlay_thickness_mm": NotRequired["float"],
}, closed=True)

FeatureDefaults = TypedDict("FeatureDefaults", {
    "color": NotRequired["Color"],
}, closed=True)

FeatureSwitchOption2 = TypedDict("FeatureSwitchOption2", {
    "enabled": NotRequired["bool"],
    "color": NotRequired["Color"],
    "step_body_name": NotRequired["str"],
    "thickness_bias_mm": NotRequired["float"],
}, closed=True)

ComponentPads = TypedDict("ComponentPads", {
    "enabled": NotRequired["bool"],
    "mode": NotRequired["Literal[\"none\"] | Literal[\"all\"] | Literal[\"matching_designators\"]"],
    "include_designators": NotRequired["StringList"],
    "color": NotRequired["Color"],
    "step_body_name": NotRequired["str"],
    "thickness_bias_mm": NotRequired["float"],
    "highlight_rules": NotRequired["HighlightRules"],
}, closed=True)

HighlightRulesValueItem = TypedDict("HighlightRulesValueItem", {
    "designators": "StringList",
    "color": "Color",
    "step_body_name": NotRequired["str"],
}, closed=True)

LayerSelector = str | int | None
Color = str
DrillMode = Literal["auto"] | Literal["cut"] | Literal["overlay"] | Literal["none"]
DrillShape = Literal["solid"] | Literal["ring"]
PlatedRingShape = Literal["annulus"]
DrillScopedMode = Literal["inherit"] | Literal["cut"] | Literal["overlay"] | Literal["none"]
StringList = str | list[str]
FeatureSwitch = bool | FeatureSwitchOption2
FeaturesComponentPads = bool | ComponentPads
HighlightRules = list[HighlightRulesValueItem]
