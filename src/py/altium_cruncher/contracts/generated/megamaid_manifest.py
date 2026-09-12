"""Generated from src/tsp/altium_cruncher/outputs/megamaid-manifest.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

MegamaidManifest = TypedDict("MegamaidManifest", {
    "schema": "Literal[\"altium_cruncher.megamaid_manifest.b0\"]",
    "kind": "Literal[\"megamaid\"]",
    "input_project": "str",
    "output_root": "str",
    "variants": "list[str]",
    "bom_pnp_config": "str | None",
    "schdoc_count": "int",
    "pcbdoc_count": "int",
    "bom": "MegamaidManifestBom",
    "pnp": "MegamaidManifestPnp",
    "netlist": "Netlist",
    "document_jsons": "list[MegamaidManifestDocumentJsonsItem]",
    "library_jsons": "MegamaidManifestLibraryJsons",
    "notes": "MegamaidManifestNotes",
    "schlib": "list[MegamaidManifestSchlibItem]",
    "pcblib": "list[MegamaidManifestPcblibItem]",
    "embedded_assets": "MegamaidManifestEmbeddedAssets",
    "sch_images": "MegamaidManifestSchImages",
}, closed=True)

MegamaidManifestBom = TypedDict("MegamaidManifestBom", {
    "output_kinds": NotRequired["list[str]"],
    "outputs": NotRequired["list[BomOutput]"],
}, extra_items="object")

MegamaidManifestPnp = TypedDict("MegamaidManifestPnp", {
    "output_kinds": NotRequired["list[str]"],
    "outputs": NotRequired["list[PnpOutput]"],
    "skipped": NotRequired["str"],
}, extra_items="object")

Netlist = TypedDict("Netlist", {
    "design_json": "str",
    "design_schema": "Literal[\"altium_monkey.design.b0\"]",
    "compiled_schematic_graph_schema": "Literal[\"altium_monkey.compiled_schematic_graph.a0\"]",
    "component_count": "int",
    "net_count": "int",
    "page_occurrence_count": "int",
    "graphical_artifact_link_count": "int",
}, closed=True)

MegamaidManifestDocumentJsonsItem = TypedDict("MegamaidManifestDocumentJsonsItem", {
    "source": NotRequired["str"],
    "kind": NotRequired["str"],
    "json": NotRequired["str"],
}, extra_items="object")

MegamaidManifestLibraryJsons = TypedDict("MegamaidManifestLibraryJsons", {
    "schlib": NotRequired["list[LibraryJsonEntry]"],
    "pcblib": NotRequired["list[LibraryJsonEntry]"],
}, extra_items="object")

MegamaidManifestNotes = TypedDict("MegamaidManifestNotes", {
    "notes_json": NotRequired["str"],
}, extra_items="object")

MegamaidManifestSchlibItem = TypedDict("MegamaidManifestSchlibItem", {
    "source_schdocs": NotRequired["list[str]"],
    "combined_schlib": NotRequired["str"],
    "split_dir": NotRequired["str"],
    "symbol_count": NotRequired["int"],
    "split_file_count": NotRequired["int"],
    "split_files": NotRequired["list[str]"],
    "split_results_by_schdoc": NotRequired["list[SchdocSplitResult]"],
}, extra_items="object")

MegamaidManifestPcblibItem = TypedDict("MegamaidManifestPcblibItem", {
    "source_pcbdoc": NotRequired["str"],
    "combined_pcblib": NotRequired["str"],
    "split_dir": NotRequired["str"],
    "footprint_count": NotRequired["int"],
    "split_file_count": NotRequired["int"],
    "split_files": NotRequired["list[str]"],
}, extra_items="object")

MegamaidManifestEmbeddedAssets = TypedDict("MegamaidManifestEmbeddedAssets", {
    "fonts": NotRequired["list[EmbeddedAsset]"],
    "models": NotRequired["list[EmbeddedAsset]"],
    "font_file_count": NotRequired["int"],
    "model_file_count": NotRequired["int"],
}, extra_items="object")

MegamaidManifestSchImages = TypedDict("MegamaidManifestSchImages", {
    "images": NotRequired["list[SchematicImage]"],
    "image_file_count": NotRequired["int"],
}, extra_items="object")

BomOutput = TypedDict("BomOutput", {
    "variant": "str",
    "component_count": "int",
    "artifacts": "list[str]",
}, closed=True)

PnpOutput = TypedDict("PnpOutput", {
    "variant": "str",
    "placement_count": "int",
    "artifacts": "list[str]",
}, closed=True)

LibraryJsonEntry = TypedDict("LibraryJsonEntry", {
    "source": "str",
    "kind": "str",
    "json": "str",
    "scope": "Literal[\"combined\"] | Literal[\"split\"]",
}, closed=True)

SchdocSplitResult = TypedDict("SchdocSplitResult", {
    "source_schdoc": "str",
    "split_results": "RecordBoolean",
}, closed=True)

EmbeddedAsset = TypedDict("EmbeddedAsset", {
    "source_pcbdoc": "str",
    "source_name": "str",
    "output_file": "str",
    "deduplicated": "bool",
}, closed=True)

SchematicImage = TypedDict("SchematicImage", {
    "source_schdoc": "str",
    "source_name": "str",
    "output_file": "str",
    "deduplicated": "bool",
}, closed=True)

RecordUnknown = dict[str, object]
RecordBoolean = dict[str, bool]
