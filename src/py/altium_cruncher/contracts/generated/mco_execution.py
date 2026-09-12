"""Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

McoExecution = TypedDict("McoExecution", {
    "schema": "Literal[\"altium_cruncher.mco.a0\"]",
    "ok": "bool",
    "dry_run": "bool",
    "results": "list[McoOperationResult]",
}, closed=True)

McoOperationResult = TypedDict("McoOperationResult", {
    "op": "str",
    "id": "str",
    "status": "Literal[\"ok\"] | Literal[\"fail\"]",
    "message": "str",
    "outputs": "RecordUnknown",
    "error": NotRequired["str"],
}, closed=True)

RecordUnknown = dict[str, object]
