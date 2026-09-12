"""Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

Profiles = TypedDict("Profiles", {
    "schema": "Literal[\"altium_cruncher.profiles.a0\"]",
    "profiles": "list[Profile]",
}, closed=True)

Profile = TypedDict("Profile", {
    "name": "str",
    "guid": "str",
    "path": "str",
    "extensions_root": "str",
    "registry_path": "str",
    "registry_exists": "bool",
    "module_name": "str",
    "module_dir": "str",
    "module_dir_exists": "bool",
    "registered": "bool",
    "registry_version": "str | None",
    "dll_path": "str",
    "dll_exists": "bool",
    "last_write_time_utc": "str | None",
}, closed=True)
