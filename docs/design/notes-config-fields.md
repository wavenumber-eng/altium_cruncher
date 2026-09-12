# Schematic notes output fields

Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit.

Wire fields emitted by Cruncher. Validation preserves the payload without inserting defaults.

See the contract authority inventory for producer locations and delegated upstream data boundaries.

## Notes

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — |  |
| `input` | Yes | — |  |
| `source_kind` | Yes | — |  |
| `path_base` | Yes | — |  |
| `schdoc_count` | Yes | — |  |
| `filters` | Yes | — |  |
| `schdocs` | Yes | — |  |

## NoteFilters

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `include_sheet_template_text` | Yes | — |  |
| `default_suppression` | Yes | — |  |

## NotesPage

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `notes` | No | — |  |
| `text_frames` | No | — |  |
| `free_text` | No | — |  |

## Note

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `text` | Yes | — |  |
| `position_mils` | Yes | — |  |
| `unique_id` | No | — |  |
| `bounds_mils` | No | — |  |
| `author` | No | — |  |

## Point

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `x` | Yes | — |  |
| `y` | Yes | — |  |

## Bounds

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `x_min` | Yes | — |  |
| `y_min` | Yes | — |  |
| `x_max` | Yes | — |  |
| `y_max` | Yes | — |  |
