"""Generated from src/tsp/altium_cruncher/outputs/easyeda.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

EasyedaModels = TypedDict("EasyedaModels", {
    "schema": "Literal[\"altium_cruncher.easyeda.3d_models.a0\"]",
    "lcsc_id": "str",
    "placement_implemented": "bool",
    "placement_note": "str",
    "models": "list[ModelReference]",
    "placement_verdict": NotRequired["str"],
    "placement_check": NotRequired["PlacementCheck"],
}, closed=True)

ModelReference = TypedDict("ModelReference", {
    "uuid": "str",
    "title": "str",
    "origin": "str",
    "z": "str",
    "rotation": "str",
    "files": "RecordString",
    "errors": "RecordString",
    "placement_status": "str",
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

RecordString = dict[str, str]
BoundsArray = list[float]
