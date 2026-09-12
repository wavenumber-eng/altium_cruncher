"""Generated from src/tsp/altium_cruncher/outputs/easyeda.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

EasyedaFootprintReport = TypedDict("EasyedaFootprintReport", {
    "lcsc_id": "str",
    "footprint_name": "str",
    "source_pad_count": "int",
    "generated_pad_count": "int",
    "generated_hole_pad_count": "int",
    "custom_pad_count": "int",
    "slotted_pad_count": "int",
    "track_count": "int",
    "track_segment_count": "int",
    "circle_count": "int",
    "arc_count": "int",
    "rectangle_count": "int",
    "region_count": "int",
    "text_count": "int",
    "unsupported_count": "int",
    "unsupported_graphics": "list[str]",
    "warnings": "list[str]",
    "layers": "RecordInteger",
    "policy": "FootprintPolicy",
    "transform": "FootprintTransform",
    "model_3d_attached": "bool",
    "model_3d_centered_fallback": "bool",
    "model_3d_placement_verdict": "str",
    "model_3d": "ModelAttachment",
}, closed=True)

FootprintPolicy = TypedDict("FootprintPolicy", {
    "mils_per_easyeda_unit": NotRequired["float"],
    "invert_y": NotRequired["bool"],
    "include_source_graphics": NotRequired["bool"],
    "include_source_text": NotRequired["bool"],
    "include_non_pad_holes": NotRequired["bool"],
    "default_graphic_width_mils": NotRequired["float"],
    "curve_approximation_segments": NotRequired["int"],
    "arc_approximation_max_degrees": NotRequired["float"],
}, closed=True)

FootprintTransform = TypedDict("FootprintTransform", {
    "anchor_x": NotRequired["float"],
    "anchor_y": NotRequired["float"],
    "mils_per_easyeda_unit": NotRequired["float"],
    "invert_y": NotRequired["bool"],
}, closed=True)

ModelAttachment = TypedDict("ModelAttachment", {
    "name": NotRequired["str"],
    "error": NotRequired["str"],
    "location_mils": NotRequired["list[float]"],
    "raw_location_mils": NotRequired["list[float]"],
    "centered_fallback": NotRequired["bool"],
    "rotation_degrees": NotRequired["list[float]"],
    "standoff_mils": NotRequired["float"],
    "identifier": NotRequired["str"],
    "placement_check": NotRequired["PlacementCheck"],
}, closed=True)

PlacementCheck = TypedDict("PlacementCheck", {
    "verdict": NotRequired["Literal[\"ok\"] | Literal[\"needs_checking\"]"],
    "checked": NotRequired["bool"],
    "reason": NotRequired["str"],
    "center_distance_mils": NotRequired["float"],
    "distance_ratio": NotRequired["float"],
    "model_bounds_mils": NotRequired["BoundsArray"],
    "pad_bounds_mils": NotRequired["BoundsArray"],
}, closed=True)

RecordInteger = dict[str, int]
BoundsArray = list[float]
