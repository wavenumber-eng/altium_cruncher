"""Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

McoOperations = TypedDict("McoOperations", {
    "schema": "Literal[\"altium_cruncher.mco.operations.a0\"]",
    "operations": "list[McoCatalogEntry]",
}, closed=True)

McoCatalogEntry = TypedDict("McoCatalogEntry", {
    "op": "str",
    "group": "str",
    "summary": "str",
    "required_args": "list[str]",
    "optional_args": "list[str]",
    "aliases": NotRequired["list[str]"],
}, closed=True)
