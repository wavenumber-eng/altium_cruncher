# MegamaidManifest output fields

Generated from src/tsp/altium_cruncher/outputs/megamaid-manifest.tsp. Do not edit.

Wire fields emitted by Cruncher. Validation preserves the payload without inserting defaults.

See the contract authority inventory for producer locations and delegated upstream data boundaries.

## MegamaidManifest

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — |  |
| `kind` | Yes | — |  |
| `input_project` | Yes | — |  |
| `output_root` | Yes | — |  |
| `variants` | Yes | — |  |
| `bom_pnp_config` | Yes | — |  |
| `schdoc_count` | Yes | — |  |
| `pcbdoc_count` | Yes | — |  |
| `bom` | Yes | — |  |
| `pnp` | Yes | — |  |
| `netlist` | Yes | — |  |
| `document_jsons` | Yes | — |  |
| `library_jsons` | Yes | — |  |
| `notes` | Yes | — |  |
| `schlib` | Yes | — |  |
| `pcblib` | Yes | — |  |
| `embedded_assets` | Yes | — |  |
| `sch_images` | Yes | — |  |

## MegamaidManifestBom

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `output_kinds` | No | — |  |
| `outputs` | No | — |  |

## MegamaidManifestPnp

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `output_kinds` | No | — |  |
| `outputs` | No | — |  |
| `skipped` | No | — |  |

## Netlist

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `design_json` | Yes | — |  |
| `design_schema` | Yes | — |  |
| `compiled_schematic_graph_schema` | Yes | — |  |
| `component_count` | Yes | — |  |
| `net_count` | Yes | — |  |
| `page_occurrence_count` | Yes | — |  |
| `graphical_artifact_link_count` | Yes | — |  |

## MegamaidManifestDocumentJsonsItem

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `source` | No | — |  |
| `kind` | No | — |  |
| `json` | No | — |  |

## MegamaidManifestLibraryJsons

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schlib` | No | — |  |
| `pcblib` | No | — |  |

## MegamaidManifestNotes

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `notes_json` | No | — |  |

## MegamaidManifestSchlibItem

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `source_schdocs` | No | — |  |
| `combined_schlib` | No | — |  |
| `split_dir` | No | — |  |
| `symbol_count` | No | — |  |
| `split_file_count` | No | — |  |
| `split_files` | No | — |  |
| `split_results_by_schdoc` | No | — |  |

## MegamaidManifestPcblibItem

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `source_pcbdoc` | No | — |  |
| `combined_pcblib` | No | — |  |
| `split_dir` | No | — |  |
| `footprint_count` | No | — |  |
| `split_file_count` | No | — |  |
| `split_files` | No | — |  |

## MegamaidManifestEmbeddedAssets

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `fonts` | No | — |  |
| `models` | No | — |  |
| `font_file_count` | No | — |  |
| `model_file_count` | No | — |  |

## MegamaidManifestSchImages

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `images` | No | — |  |
| `image_file_count` | No | — |  |

## BomOutput

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `variant` | Yes | — |  |
| `component_count` | Yes | — |  |
| `artifacts` | Yes | — |  |

## RecordUnknown

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## PnpOutput

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `variant` | Yes | — |  |
| `placement_count` | Yes | — |  |
| `artifacts` | Yes | — |  |

## LibraryJsonEntry

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `source` | Yes | — |  |
| `kind` | Yes | — |  |
| `json` | Yes | — |  |
| `scope` | Yes | — |  |

## SchdocSplitResult

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `source_schdoc` | Yes | — |  |
| `split_results` | Yes | — |  |

## EmbeddedAsset

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `source_pcbdoc` | Yes | — |  |
| `source_name` | Yes | — |  |
| `output_file` | Yes | — |  |
| `deduplicated` | Yes | — |  |

## SchematicImage

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `source_schdoc` | Yes | — |  |
| `source_name` | Yes | — |  |
| `output_file` | Yes | — |  |
| `deduplicated` | Yes | — |  |

## RecordBoolean

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
