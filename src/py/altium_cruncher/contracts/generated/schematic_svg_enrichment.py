"""Generated from src/tsp/altium_cruncher/outputs/schematic-svg-enrichment.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

SchematicSvgEnrichment = TypedDict("SchematicSvgEnrichment", {
    "schema": "Literal[\"altium_cruncher.schematic.svg.enrichment.b0\"]",
    "source": "SchematicSvgEnrichmentSource",
    "view": "SchematicSvgEnrichmentView",
}, closed=True)

SchematicSvgEnrichmentSource = TypedDict("SchematicSvgEnrichmentSource", {
    "altium_schdoc_file": "str",
    "page_occurrence_ref": "str",
    "artifact_key": "Literal[\"sch.dwg_scene\"]",
}, closed=True)

SchematicSvgEnrichmentView = TypedDict("SchematicSvgEnrichmentView", {
    "kind": "Literal[\"compiled_schematic_page\"]",
    "profile": "Literal[\"design_review\"]",
    "sheet_name": "str",
    "sheet_file": "str",
    "page_occurrence_ref": "str",
    "artifact_key": "Literal[\"sch.dwg_scene\"]",
    "physical_page_metadata": "SchematicSvgEnrichmentViewPhysicalPageMetadata",
}, closed=True)

SchematicSvgEnrichmentViewPhysicalPageMetadata = dict[str, Never]
RecordUnknown = dict[str, object]
