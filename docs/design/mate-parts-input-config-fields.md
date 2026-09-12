# Editable mate parts configuration fields

Generated from src/tsp/altium_cruncher/config/mate-config.tsp. Do not edit.

Required paths/sections are checked at loading. Defaults describe generated templates or adapter fallbacks; codecs do not insert them.

Path resolution, normalization and native CAD semantics remain Python adapter behavior.

## MatePartsInput

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — |  |
| `parts` | Yes | — |  |
| `source` | No | — |  |
| `designator_normalization` | No | — |  |

## AuthoredKnownPart

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `role` | No | — |  |
| `description` | No | — |  |
| `symbol_name` | No | — |  |
| `symbol_library` | No | — |  |
| `footprint_name` | No | — |  |
| `footprint_library` | No | — |  |
| `target_kinds` | No | — |  |
| `designator_prefix` | No | — |  |
| `signal_pad_designator` | No | — |  |

## PartSource

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `kind` | Yes | — |  |
| `project` | Yes | — |  |

## RecordRecordString

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## RecordUnknown

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## RecordString

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
