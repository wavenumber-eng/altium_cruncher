"""Generated from src/tsp/altium_cruncher/outputs/mate.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

MatePartsManifest = TypedDict("MatePartsManifest", {
    "schema": "Literal[\"altium_cruncher.mate.parts_cache.a0\"]",
    "source": "PartSource",
    "parts": "list[KnownPart]",
    "designator_normalization": "RecordRecordString",
}, closed=True)

PartSource = TypedDict("PartSource", {
    "kind": "str",
    "project": "str",
}, closed=True)

KnownPart = TypedDict("KnownPart", {
    "role": "str",
    "description": "str",
    "symbol_name": "str",
    "symbol_library": "str",
    "footprint_name": "str",
    "footprint_library": "str",
    "target_kinds": "list[str]",
    "designator_prefix": "str",
    "signal_pad_designator": "str | None",
}, closed=True)

RecordString = dict[str, str]
RecordRecordString = dict[str, RecordString]
