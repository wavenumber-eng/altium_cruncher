"""Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

OutjobRun = TypedDict("OutjobRun", {
    "schema": "Literal[\"altium_cruncher.outjob.run.a0\"]",
    "project": "str",
    "success": "bool",
    "results": "list[OutjobResult]",
}, closed=True)

OutjobResult = TypedDict("OutjobResult", {
    "project": "str",
    "outjob": "str",
    "success": "bool",
    "launch_code": "int",
    "timed_out": "bool",
    "error_count": "int",
    "marker_text": "str",
    "normalized_changed": "bool",
    "rebound_document_paths": "int",
    "marker_path": "str",
    "log_path": "str",
}, closed=True)
