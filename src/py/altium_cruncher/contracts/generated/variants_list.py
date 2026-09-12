"""Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

VariantsList = TypedDict("VariantsList", {
    "schema": "Literal[\"altium_cruncher.variants.list.a0\"]",
    "project": "str",
    "current_variant": "str | None",
    "variant_count": "Count",
    "variants": "list[Variant]",
    "rows": "list[VariantRow]",
    "index_errors": "list[str]",
}, closed=True)

Variant = TypedDict("Variant", {
    "name": "str",
    "unique_id": "str",
    "allow_fabrication": "bool",
    "current": "bool",
    "dnp": "list[str]",
    "variation_count": "Count",
    "parameter_count": "Count",
    "param_variation_count": "Count",
    "rows": "list[VariantRow]",
}, closed=True)

VariantRow = TypedDict("VariantRow", {
    "variant": "str",
    "sheet": "str",
    "designator": "str",
    "operation": "str",
    "detail": "str",
    "component_value": "str",
    "parameter_name": "str",
    "value": "str",
    "unique_id": "str",
    "alternate_part": NotRequired["str"],
    "alternate_part_resolved": NotRequired["str"],
}, closed=True)

Count = int
