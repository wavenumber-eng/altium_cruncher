"""Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

BomGrouped = TypedDict("BomGrouped", {
    "schema": "Literal[\"altium_cruncher.bom.grouped.a0\"]",
    "source": "Source",
    "variant": "str | None",
    "line_count": "Count",
    "component_count": "Count",
    "dnp_line_count": "Count",
    "lines": "list[GroupedBomLine]",
}, closed=True)

Source = TypedDict("Source", {
    "path": "str",
    "name": "str",
    "stem": "str",
}, closed=True)

GroupedBomLine = TypedDict("GroupedBomLine", {
    "item": "int",
    "quantity": "Count",
    "designators": "list[str]",
    "dnp": "bool",
    "fields": "RecordString",
}, closed=True)

Count = int
RecordString = dict[str, str]
