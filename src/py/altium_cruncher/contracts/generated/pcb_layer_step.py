"""Generated from src/tsp/altium_cruncher/outputs/pcb-layer-step.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

PcbLayerStepManifest = TypedDict("PcbLayerStepManifest", {
    "schema": "Literal[\"altium_cruncher.pcb_layer_step.a0\"]",
    "backend": "Literal[\"geometer.planar_step\"]",
    "board": "str",
    "source_input": "str | None",
    "step_file": "str",
    "coordinate_origin": "CoordinateOrigin",
    "layer": "Layer",
    "options": "Options",
    "counts": "RecordInteger",
    "bytes": "int",
}, closed=True)

CoordinateOrigin = TypedDict("CoordinateOrigin", {
    "mode": "Literal[\"board_origin\"]",
    "origin_mils": "Point",
    "origin_mm": "Point",
    "geometry": "str",
}, closed=True)

Layer = TypedDict("Layer", {
    "id": "int",
    "json_name": "str",
    "display_name": "str",
}, closed=True)

Options = TypedDict("Options", {
    "thickness_mm": "float",
    "z_mm": "float",
    "copper_color": "str",
    "outline_width_mm": "float",
    "outline_color": "str",
    "board_cutout_color": "str",
    "include_copper": "bool",
    "include_board_outline": "bool",
    "include_board_cutouts": "bool",
    "include_poured_polygons": "bool",
    "cut_holes": "bool",
    "drill_hole_mode": "str",
    "effective_drill_hole_mode": "str",
    "max_boolean_drill_cuts": "int",
    "drill_hole_color": "str",
    "drill_plated_hole_color": "str",
    "drill_non_plated_hole_color": "str",
    "drill_overlay_thickness_mm": "float",
    "drill_minimum_diameter_mm": "float",
    "drill_hole_shape": "str",
    "drill_ring_width_mm": "float",
    "drill_plated_ring_shape": "str",
    "drill_selected_component_mode": "str",
    "drill_other_component_mode": "str",
    "drill_free_pad_mode": "str",
    "drill_via_mode": "str",
    "fuse_copper": "bool",
    "fuse_board_outline": "bool",
    "arc_segments": "int",
    "features": "FeatureSwitches",
    "pad_color_rules": "list[PadColorRule]",
    "feature_color_rules": "FeatureStyles",
    "thickness_bias_mm": "ThicknessBias",
    "highlight_count": "int",
}, closed=True)

FeatureSwitches = TypedDict("FeatureSwitches", {
    "tracks": "bool",
    "arcs": "bool",
    "fills": "bool",
    "polygons": "bool",
    "regions": "bool",
    "vias": "bool",
    "component_pads": "bool",
    "free_pads": "bool",
    "include_designators": "list[str]",
}, closed=True)

PadColorRule = TypedDict("PadColorRule", {
    "designators": "list[str]",
    "color": "str",
    "step_body_name": "str | None",
}, closed=True)

FeatureStyles = TypedDict("FeatureStyles", {
    "tracks": "FeatureStyle",
    "arcs": "FeatureStyle",
    "fills": "FeatureStyle",
    "polygons": "FeatureStyle",
    "regions": "FeatureStyle",
    "vias": "FeatureStyle",
    "component_pads": "FeatureStyle",
    "free_pads": "FeatureStyle",
}, closed=True)

ThicknessBias = TypedDict("ThicknessBias", {
    "tracks": "float",
    "arcs": "float",
    "fills": "float",
    "polygons": "float",
    "regions": "float",
    "vias": "float",
    "component_pads": "float",
    "free_pads": "float",
}, closed=True)

FeatureStyle = TypedDict("FeatureStyle", {
    "color": "str | None",
    "step_body_name": "str | None",
}, closed=True)

RecordInteger = dict[str, int]
Point = list[float]
