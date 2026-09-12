"""Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

BomLegacy = TypedDict("BomLegacy", {
    "schema": "Literal[\"altium_cruncher.bom.a0\"]",
    "source": "Source",
    "variant": "str | None",
    "component_count": "Count",
    "dnp_count": "Count",
    "columns": "list[str]",
    "parameter_columns": "list[str]",
    "components": "list[RecordString]",
    "raw_components": "list[RawBomComponent]",
    "normalized": "ImportedBomNormalized",
}, closed=True)

Source = TypedDict("Source", {
    "path": "str",
    "name": "str",
    "stem": "str",
}, closed=True)

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

ImportedBomNormalized = TypedDict("ImportedBomNormalized", {
    "schema": "Literal[\"altium_cruncher.bom.raw.a0\"]",
    "source": "ImportedBomNormalized_Source",
    "variant": "str | None",
    "component_count": "ImportedBomNormalized_Count",
    "dnp_count": "ImportedBomNormalized_Count",
    "components": "list[ImportedBomNormalized_NormalizedBomComponent]",
}, closed=True)

ImportedBomNormalized_Source = TypedDict("ImportedBomNormalized_Source", {
    "path": "str",
    "name": "str",
    "stem": "str",
}, closed=True)

ImportedBomNormalized_NormalizedBomComponent = TypedDict("ImportedBomNormalized_NormalizedBomComponent", {
    "designator": "str",
    "value": "str",
    "footprint": "str",
    "library_ref": "str",
    "description": "str",
    "sheet": "str",
    "dnp": "bool",
    "parameters": "ImportedBomNormalized_RecordString",
    "canonical_fields": "ImportedBomNormalized_RecordString",
    "field_sources": "ImportedBomNormalized_RecordString",
}, closed=True)

Count = int
RecordString = dict[str, str]
RecordUnknown = dict[str, object]
ImportedBomNormalized_Count = int
ImportedBomNormalized_RecordString = dict[str, str]
