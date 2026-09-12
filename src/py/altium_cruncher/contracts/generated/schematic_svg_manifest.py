"""Generated from src/tsp/altium_cruncher/outputs/schematic-svg-manifest.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

SchematicSvgManifest = TypedDict("SchematicSvgManifest", {
    "schema": "Literal[\"altium_cruncher.schematic_svg_manifest.b0\"]",
    "input": "str",
    "design_json": "str",
    "design_schema": "Literal[\"altium_monkey.design.b0\"]",
    "compiled_schematic_graph_schema": "Literal[\"altium_monkey.compiled_schematic_graph.a0\"]",
    "svgs": "list[SvgArtifact]",
}, closed=True)

SvgArtifact = TypedDict("SvgArtifact", {
    "file": "str",
    "page_occurrence_ref": "str",
    "artifact_key": "Literal[\"sch.dwg_scene\"]",
    "source": "str",
    "source_sheet": "str",
    "page_number": "int",
    "page_count": "int",
}, closed=True)
