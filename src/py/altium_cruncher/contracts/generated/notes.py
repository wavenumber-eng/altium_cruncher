"""Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

Notes = TypedDict("Notes", {
    "schema": "Literal[\"altium_cruncher.notes.a0\"]",
    "input": "str",
    "source_kind": "Literal[\"schdoc\"] | Literal[\"prjpcb\"]",
    "path_base": "Literal[\"input_directory\"]",
    "schdoc_count": "Count",
    "filters": "NoteFilters",
    "schdocs": "list[NotesPage]",
}, closed=True)

NoteFilters = TypedDict("NoteFilters", {
    "include_sheet_template_text": "bool",
    "default_suppression": "str",
}, closed=True)

NotesPage = TypedDict("NotesPage", {
    "file": "str",
    "notes": NotRequired["list[Note]"],
    "text_frames": NotRequired["list[Note]"],
    "free_text": NotRequired["list[Note]"],
}, closed=True)

Note = TypedDict("Note", {
    "text": "str",
    "position_mils": "Point | None",
    "unique_id": NotRequired["str"],
    "bounds_mils": NotRequired["Bounds"],
    "author": NotRequired["str | float | bool"],
}, closed=True)

Point = TypedDict("Point", {
    "x": "float",
    "y": "float",
}, closed=True)

Bounds = TypedDict("Bounds", {
    "x_min": "float",
    "y_min": "float",
    "x_max": "float",
    "y_max": "float",
}, closed=True)

Count = int
