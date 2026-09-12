# SchematicSvgManifest output fields

Generated from src/tsp/altium_cruncher/outputs/schematic-svg-manifest.tsp. Do not edit.

Wire fields emitted by Cruncher. Validation preserves the payload without inserting defaults.

See the contract authority inventory for producer locations and delegated upstream data boundaries.

## SchematicSvgManifest

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — |  |
| `input` | Yes | — |  |
| `design_json` | Yes | — |  |
| `design_schema` | Yes | — |  |
| `compiled_schematic_graph_schema` | Yes | — |  |
| `svgs` | Yes | — |  |

## SvgArtifact

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `page_occurrence_ref` | Yes | — |  |
| `artifact_key` | Yes | — |  |
| `source` | Yes | — |  |
| `source_sheet` | Yes | — |  |
| `page_number` | Yes | — |  |
| `page_count` | Yes | — |  |
