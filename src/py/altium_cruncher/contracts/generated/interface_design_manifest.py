"""Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

InterfaceDesignManifest = TypedDict("InterfaceDesignManifest", {
    "schema": "Literal[\"altium_cruncher.interface_design_manifest.a0\"]",
    "major_interfaces": "list[str | NamedInterface]",
}, closed=True)

NamedInterface = TypedDict("NamedInterface", {
    "name": "str",
}, extra_items="object")

RecordUnknown = dict[str, object]
