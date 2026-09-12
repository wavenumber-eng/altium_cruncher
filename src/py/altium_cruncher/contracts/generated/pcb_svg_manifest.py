"""Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

PcbSvgManifest = TypedDict("PcbSvgManifest", {
    "schema": "Literal[\"pcb.svg.manifest.a0\"]",
    "board": "str",
    "source_input": "str",
    "layer_outputs": "RecordSvgLayerOutput",
    "views": "RecordSvgViewOutput",
}, closed=True)

SvgLayerOutput = TypedDict("SvgLayerOutput", {
    "file": "str",
    "layers": "list[str]",
    "group_id": "str",
}, closed=True)

SvgViewOutput = TypedDict("SvgViewOutput", {
    "file": "str",
    "group_id": "str",
    "layers": "list[str]",
    "mirrored": "bool",
    "assembly_hlr_mode": "str",
}, closed=True)

RecordSvgLayerOutput = dict[str, SvgLayerOutput]
RecordSvgViewOutput = dict[str, SvgViewOutput]
