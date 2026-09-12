"""Generated from src/tsp/altium_cruncher/outputs/json-dump.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

JsonDumpManifest = TypedDict("JsonDumpManifest", {
    "schema": "Literal[\"altium_cruncher.json_dump.manifest.a0\"]",
    "outputs": "list[DumpOutput]",
}, closed=True)

DumpOutput = TypedDict("DumpOutput", {
    "source_path": "str",
    "output_path": "str",
    "kind": "Literal[\"SchDoc\"] | Literal[\"SchLib\"] | Literal[\"PcbDoc\"] | Literal[\"PcbLib\"]",
}, closed=True)
