# MCO execution result output fields

Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit.

Wire fields emitted by Cruncher. Validation preserves the payload without inserting defaults.

See the contract authority inventory for producer locations and delegated upstream data boundaries.

## McoExecution

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — | Existing execution reports reuse the input schema tag; the contract file distinguishes the result shape. |
| `ok` | Yes | — |  |
| `dry_run` | Yes | — |  |
| `results` | Yes | — |  |

## McoOperationResult

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `op` | Yes | — |  |
| `id` | Yes | — |  |
| `status` | Yes | — |  |
| `message` | Yes | — |  |
| `outputs` | Yes | — | Operation-specific results; custom registries own their output payloads. |
| `error` | No | — |  |

## RecordUnknown

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
