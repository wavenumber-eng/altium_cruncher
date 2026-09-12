# DesignReviewManifest output fields

Generated from src/tsp/altium_cruncher/outputs/design-review-manifest.tsp. Do not edit.

Wire fields emitted by Cruncher. Validation preserves the payload without inserting defaults.

See the contract authority inventory for producer locations and delegated upstream data boundaries.

## DesignReviewManifest

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — |  |
| `input` | Yes | — |  |
| `design_json` | Yes | — |  |
| `document_jsons` | Yes | — |  |
| `notes_json` | Yes | — |  |
| `schematic_svgs` | Yes | — |  |
| `schematic_irs` | Yes | — |  |
| `pcb_svgs` | Yes | — |  |
| `readme` | Yes | — |  |

## DocumentArtifact

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `source` | Yes | — |  |
| `kind` | Yes | — |  |

## CompiledSchematicArtifact

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `page_occurrence_ref` | Yes | — |  |
| `artifact_key` | Yes | — |  |
| `source` | Yes | — |  |
| `source_sheet` | Yes | — |  |
| `page_number` | Yes | — |  |
| `page_count` | Yes | — |  |

## PcbArtifact

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `manifest` | Yes | — |  |
| `board` | Yes | — |  |
| `layer_outputs` | Yes | — |  |
| `views` | Yes | — |  |

## LogicalSchematicArtifact

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `source` | Yes | — |  |
| `page_number` | Yes | — |  |
| `page_count` | Yes | — |  |

## PcbOutput

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `name` | Yes | — |  |
| `file` | Yes | — |  |
| `layers` | Yes | — |  |
