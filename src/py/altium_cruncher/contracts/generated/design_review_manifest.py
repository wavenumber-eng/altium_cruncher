"""Generated from src/tsp/altium_cruncher/outputs/design-review-manifest.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

DesignReviewManifest = TypedDict("DesignReviewManifest", {
    "schema": "Literal[\"altium_cruncher.design_review_manifest.b0\"]",
    "input": "Path",
    "design_json": "Path",
    "document_jsons": "list[DocumentArtifact]",
    "notes_json": "Path",
    "schematic_svgs": "list[DesignReviewManifestSchematicSvgsItem]",
    "schematic_irs": "list[CompiledSchematicArtifact]",
    "pcb_svgs": "list[PcbArtifact]",
    "readme": "Path",
}, closed=True)

DocumentArtifact = TypedDict("DocumentArtifact", {
    "file": "Path",
    "source": "Path",
    "kind": "Literal[\"SchDoc\"] | Literal[\"PcbDoc\"]",
}, closed=True)

CompiledSchematicArtifact = TypedDict("CompiledSchematicArtifact", {
    "file": "Path",
    "page_occurrence_ref": "str",
    "artifact_key": "Literal[\"sch.dwg_scene\"]",
    "source": "Path",
    "source_sheet": "Path",
    "page_number": "PositiveInteger",
    "page_count": "PositiveInteger",
}, closed=True)

PcbArtifact = TypedDict("PcbArtifact", {
    "manifest": "Path",
    "board": "str | None",
    "layer_outputs": "list[PcbOutput]",
    "views": "list[PcbOutput]",
}, closed=True)

LogicalSchematicArtifact = TypedDict("LogicalSchematicArtifact", {
    "file": "Path",
    "source": "Path",
    "page_number": "PositiveInteger",
    "page_count": "PositiveInteger",
}, closed=True)

PcbOutput = TypedDict("PcbOutput", {
    "name": "str",
    "file": "Path",
    "layers": "list[str]",
}, closed=True)

Path = str
DesignReviewManifestSchematicSvgsItem = LogicalSchematicArtifact | CompiledSchematicArtifact
PositiveInteger = int
