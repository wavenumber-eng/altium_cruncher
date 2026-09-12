# MCO execution envelope configuration fields

Generated from src/tsp/altium_cruncher/mco/main.tsp. Do not edit.

Authored MCO codecs preserve input fields and defaults; the execution envelope defers argument checks until a built-in operation is reached.

Execution, failure branches, custom registry behavior, dry-run checks and native CAD semantics remain Python behavior.

## McoEnvelopeDocument

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | No | — |  |
| `operations` | Yes | — |  |

## OpenOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | No | — |  |

## RecordUnknown

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
