"""Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

Installs = TypedDict("Installs", {
    "schema": "Literal[\"altium_cruncher.installs.a0\"]",
    "installs": "list[Install]",
}, closed=True)

Install = TypedDict("Install", {
    "name": "str",
    "label": "str",
    "major": "int | None",
    "root": "str",
    "x2_path": "str",
    "runtime_tfm": "str | None",
    "registry_version": "str | None",
    "unique_id": "str | None",
    "source": "str",
}, closed=True)
