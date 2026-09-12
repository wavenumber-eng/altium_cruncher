# Grouped BOM output fields

Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit.

Wire fields emitted by Cruncher. Validation preserves the payload without inserting defaults.

See the contract authority inventory for producer locations and delegated upstream data boundaries.

## BomGrouped

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — |  |
| `source` | Yes | — |  |
| `variant` | Yes | — |  |
| `line_count` | Yes | — |  |
| `component_count` | Yes | — |  |
| `dnp_line_count` | Yes | — |  |
| `lines` | Yes | — |  |

## Source

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `path` | Yes | — |  |
| `name` | Yes | — |  |
| `stem` | Yes | — |  |

## GroupedBomLine

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `item` | Yes | — |  |
| `quantity` | Yes | — |  |
| `designators` | Yes | — |  |
| `dnp` | Yes | — |  |
| `fields` | Yes | — |  |

## RecordString

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
