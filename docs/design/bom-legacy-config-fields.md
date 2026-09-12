# Generic / legacy BOM output fields

Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit.

Wire fields emitted by Cruncher. Validation preserves the payload without inserting defaults.

See the contract authority inventory for producer locations and delegated upstream data boundaries.

## BomLegacy

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — |  |
| `source` | Yes | — |  |
| `variant` | Yes | — |  |
| `component_count` | Yes | — |  |
| `dnp_count` | Yes | — |  |
| `columns` | Yes | — |  |
| `parameter_columns` | Yes | — |  |
| `components` | Yes | — |  |
| `raw_components` | Yes | — |  |
| `normalized` | Yes | — |  |

## Source

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `path` | Yes | — |  |
| `name` | Yes | — |  |
| `stem` | Yes | — |  |

## RecordString

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## RawBomComponent

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `designator` | No | — |  |
| `value` | No | — |  |
| `footprint` | No | — |  |
| `library_ref` | No | — |  |
| `description` | No | — |  |
| `sheet` | No | — |  |
| `dnp` | No | — |  |
| `parameters` | No | — |  |

## RecordUnknown

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## ImportedBomNormalized

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — |  |
| `source` | Yes | — |  |
| `variant` | Yes | — |  |
| `component_count` | Yes | — |  |
| `dnp_count` | Yes | — |  |
| `components` | Yes | — |  |

## ImportedBomNormalized_Source

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `path` | Yes | — |  |
| `name` | Yes | — |  |
| `stem` | Yes | — |  |

## ImportedBomNormalized_NormalizedBomComponent

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

## ImportedBomNormalized_RecordString

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
