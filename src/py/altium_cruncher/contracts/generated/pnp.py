"""Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

Pnp = TypedDict("Pnp", {
    "schema": "Literal[\"altium_cruncher.pnp.a0\"]",
    "source": "Source",
    "variant": "str | None",
    "units": "Literal[\"mm\"] | Literal[\"mils\"]",
    "position_mode": "Literal[\"altium-pick-place\"] | Literal[\"component-origin\"]",
    "placement_count": "Count",
    "placements": "list[Placement]",
}, closed=True)

Source = TypedDict("Source", {
    "path": "str",
    "name": "str",
    "stem": "str",
}, closed=True)

Placement = TypedDict("Placement", {
    "designator": "str",
    "comment": "str",
    "layer": "str",
    "footprint": "str",
    "center_x": "float",
    "center_y": "float",
    "rotation": "float",
    "units": "str",
    "description": "str",
    "parameters": "RecordString",
    "canonical_fields": "RecordString",
    "field_sources": "RecordString",
}, closed=True)

Count = int
RecordString = dict[str, str]
