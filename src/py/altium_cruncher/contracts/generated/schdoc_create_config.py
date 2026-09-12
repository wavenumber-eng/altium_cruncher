"""Generated from src/tsp/altium_cruncher/config/creation.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

SchdocCreateConfigInput = TypedDict("SchdocCreateConfigInput", {
    "schema": "Literal[\"altium_cruncher.schdoc.create.config.a0\"]",
    "file": "NonemptyString",
    "sheet_style": NotRequired["str | int | bool | None"],
    "template": NotRequired["NonemptyString | None"],
    "apply_template_visual_sheet_settings": NotRequired["bool | str | float | None | list[object] | RecordUnknown"],
    "custom_sheet_mils": NotRequired["CustomSheetMils | None"],
}, extra_items="object")

CustomSheetMils = TypedDict("CustomSheetMils", {
    "width": "float | bool",
    "height": "float | bool",
}, extra_items="object")

NonemptyString = str
RecordUnknown = dict[str, object]
