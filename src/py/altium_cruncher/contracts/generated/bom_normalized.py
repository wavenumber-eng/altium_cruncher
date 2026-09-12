"""Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

BomNormalized = TypedDict("BomNormalized", {
    "schema": "Literal[\"altium_cruncher.bom.raw.a0\"]",
    "source": "Source",
    "variant": "str | None",
    "component_count": "Count",
    "dnp_count": "Count",
    "components": "list[NormalizedBomComponent]",
}, closed=True)

Source = TypedDict("Source", {
    "path": "str",
    "name": "str",
    "stem": "str",
}, closed=True)

NormalizedBomComponent = TypedDict("NormalizedBomComponent", {
    "designator": "str",
    "value": "str",
    "footprint": "str",
    "library_ref": "str",
    "description": "str",
    "sheet": "str",
    "dnp": "bool",
    "parameters": "RecordString",
    "canonical_fields": "RecordString",
    "field_sources": "RecordString",
}, closed=True)

Count = int
RecordString = dict[str, str]
