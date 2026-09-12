"""Generated from src/tsp/altium_cruncher/config/mate-config.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

MatePartsInput = TypedDict("MatePartsInput", {
    "schema": "Literal[\"altium_cruncher.mate.parts_cache.a0\"]",
    "parts": "list[AuthoredKnownPart]",
    "source": NotRequired["PartSource"],
    "designator_normalization": NotRequired["RecordRecordString"],
}, extra_items="object")

AuthoredKnownPart = TypedDict("AuthoredKnownPart", {
    "role": NotRequired["str"],
    "description": NotRequired["str | None"],
    "symbol_name": NotRequired["str"],
    "symbol_library": NotRequired["str"],
    "footprint_name": NotRequired["str"],
    "footprint_library": NotRequired["str"],
    "target_kinds": NotRequired["str | StringArray | None"],
    "designator_prefix": NotRequired["str"],
    "signal_pad_designator": NotRequired["str | None"],
}, extra_items="object")

PartSource = TypedDict("PartSource", {
    "kind": "str",
    "project": "str",
}, closed=True)

RecordString = dict[str, str]
RecordRecordString = dict[str, RecordString]
RecordUnknown = dict[str, object]
StringArray = list[str]
