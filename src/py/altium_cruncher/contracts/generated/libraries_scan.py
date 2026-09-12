"""Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

LibrariesScan = TypedDict("LibrariesScan", {
    "schema": "Literal[\"altium_cruncher.libraries.scan.a0\"]",
    "roots": "list[str]",
    "recursive": "bool",
    "symbols": "list[LibraryEntry]",
    "footprints": "list[LibraryEntry]",
    "warnings": "list[str]",
}, closed=True)

LibraryEntry = TypedDict("LibraryEntry", {
    "name": "str",
    "library": "str",
}, closed=True)
