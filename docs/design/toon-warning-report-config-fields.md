# ToonWarningReport output fields

Generated from src/tsp/altium_cruncher/outputs/toon-warning-report.tsp. Do not edit.

Wire fields emitted by Cruncher. Validation preserves the payload without inserting defaults.

See the contract authority inventory for producer locations and delegated upstream data boundaries.

## ToonWarningReport

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — |  |
| `summary` | Yes | — |  |
| `diagnostics` | Yes | — |  |

## ToonWarningSummary

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `unique_diagnostic_count` | Yes | — |  |
| `occurrence_count` | Yes | — |  |
| `groups` | Yes | — |  |

## ToonWarningDiagnostic

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `key` | Yes | — | Stable digest of the diagnostic's structured grouping identity. |
| `code` | Yes | — |  |
| `severity` | Yes | — |  |
| `category` | Yes | — |  |
| `producer` | Yes | — |  |
| `message` | Yes | — |  |
| `occurrence_count` | Yes | — |  |
| `input` | No | — |  |
| `board` | No | — |  |
| `variant` | No | — |  |
| `view` | No | — |  |
| `component_designator` | No | — |  |
| `body_index` | No | — |  |
| `model_identity` | No | — |  |
| `detail` | No | — |  |

## ToonWarningSummaryGroup

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `category` | Yes | — |  |
| `code` | Yes | — |  |
| `unique_diagnostic_count` | Yes | — |  |
| `occurrence_count` | Yes | — |  |
| `affected_component_count` | Yes | — |  |
| `affected_body_count` | Yes | — |  |
| `affected_model_count` | Yes | — |  |
| `sample_designators` | Yes | — |  |

## RecordUnknown

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
