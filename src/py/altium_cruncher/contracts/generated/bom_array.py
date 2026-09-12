"""Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

RawBomComponent = TypedDict("RawBomComponent", {
    "designator": NotRequired["str"],
    "value": NotRequired["str"],
    "footprint": NotRequired["str"],
    "library_ref": NotRequired["str"],
    "description": NotRequired["str"],
    "sheet": NotRequired["str"],
    "dnp": NotRequired["bool"],
    "parameters": NotRequired["RecordUnknown"],
}, extra_items="object")

BomArray = list[RawBomComponent]
RecordUnknown = dict[str, object]
