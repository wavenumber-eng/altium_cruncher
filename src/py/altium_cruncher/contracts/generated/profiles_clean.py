"""Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

ProfilesClean = TypedDict("ProfilesClean", {
    "schema": "Literal[\"altium_cruncher.profiles.clean.a0\"]",
    "actions": "list[ProfileCleanAction]",
}, closed=True)

ProfileCleanAction = TypedDict("ProfileCleanAction", {
    "profile_guid": "str",
    "profile_name": "str",
    "profile_path": "str",
    "module_name": "str",
    "module_dir": "str",
    "removed_module_dir": "bool",
    "removed_registry_item": "bool",
    "dry_run": "bool",
}, closed=True)
