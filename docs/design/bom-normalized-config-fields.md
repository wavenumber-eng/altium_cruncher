# Normalized BOM output fields

Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit.

Wire fields emitted by Cruncher. Validation preserves the payload without inserting defaults.

See the contract authority inventory for producer locations and delegated upstream data boundaries.

## BomNormalized

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — |  |
| `source` | Yes | — |  |
| `variant` | Yes | — |  |
| `component_count` | Yes | — |  |
| `dnp_count` | Yes | — |  |
| `components` | Yes | — |  |

## Source

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `path` | Yes | — |  |
| `name` | Yes | — |  |
| `stem` | Yes | — |  |

## NormalizedBomComponent

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `designator` | Yes | — |  |
| `value` | Yes | — |  |
| `footprint` | Yes | — |  |
| `library_ref` | Yes | — |  |
| `description` | Yes | — |  |
| `sheet` | Yes | — |  |
| `dnp` | Yes | — |  |
| `parameters` | Yes | — |  |
| `canonical_fields` | Yes | — |  |
| `field_sources` | Yes | — |  |

## RecordString

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
