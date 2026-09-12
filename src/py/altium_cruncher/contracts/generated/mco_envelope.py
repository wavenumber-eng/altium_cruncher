"""Generated from src/tsp/altium_cruncher/mco/main.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

McoEnvelopeDocument = TypedDict("McoEnvelopeDocument", {
    "schema": NotRequired["Literal[\"altium_cruncher.mco.a0\"] | None"],
    "operations": "list[OpenOperation]",
}, extra_items="object")

OpenOperation = TypedDict("OpenOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "McoString",
    "args": NotRequired["RecordUnknown"],
}, extra_items="object")

McoEnvelopeInput = McoEnvelopeDocument | list[OpenOperation]
RecordUnknown = dict[str, object]
McoString = str
