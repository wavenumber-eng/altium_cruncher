# Built-in MCO operation results output fields

Generated from src/tsp/altium_cruncher/outputs/mco-builtins.tsp. Do not edit.

Wire fields emitted by Cruncher. Validation preserves the payload without inserting defaults.

See the contract authority inventory for producer locations and delegated upstream data boundaries.

## Failure

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `op` | Yes | — |  |
| `id` | Yes | — |  |
| `status` | Yes | — |  |
| `message` | Yes | — |  |
| `outputs` | Yes | — |  |
| `error` | No | — |  |

## ProjectPath

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `project` | Yes | — |  |

## NamedProject

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `project` | Yes | — |  |
| `name` | Yes | — |  |

## SectionProject

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `project` | Yes | — |  |
| `name` | Yes | — |  |
| `section` | Yes | — |  |

## DnpAdded

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `project` | Yes | — |  |
| `variant` | Yes | — |  |
| `designator` | Yes | — |  |
| `unique_id` | Yes | — |  |
| `variation` | Yes | — |  |

## ToggleAdded

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `project` | Yes | — |  |
| `variant` | Yes | — |  |
| `designator` | Yes | — |  |
| `unique_id` | Yes | — |  |
| `variation` | Yes | — |  |
| `action` | Yes | — |  |
| `dnp` | Yes | — |  |

## ToggleRemoved

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `project` | Yes | — |  |
| `variant` | Yes | — |  |
| `designator` | Yes | — |  |
| `action` | Yes | — |  |
| `dnp` | Yes | — |  |

## TextOutput

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `text` | Yes | — |  |

## TextDryRun

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `text` | Yes | — |  |
| `font_kind` | Yes | — |  |
| `text_justification` | Yes | — |  |

## ArrangeDone

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `updated` | Yes | — |  |

## ArrangeDryRun

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `designators` | Yes | — |  |
| `placement` | Yes | — |  |

## UnionDone

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `name` | Yes | — |  |
| `union_index` | Yes | — |  |
| `member_count` | Yes | — |  |

## UnionDryRun

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `name` | Yes | — |  |

## StepExport

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `step_file` | Yes | — |  |
| `manifest_file` | Yes | — |  |
| `highlight_count` | Yes | — |  |
| `layer` | No | — |  |

## EmbeddedModel

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `model_file` | Yes | — |  |
| `name` | Yes | — |  |
| `z_mils` | No | — |  |

## ImportedVariantsList

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — |  |
| `project` | Yes | — |  |
| `current_variant` | Yes | — |  |
| `variant_count` | Yes | — |  |
| `variants` | Yes | — |  |
| `rows` | Yes | — |  |
| `index_errors` | Yes | — |  |

## ImportedVariantsList_Variant

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `name` | Yes | — |  |
| `unique_id` | Yes | — |  |
| `allow_fabrication` | Yes | — |  |
| `current` | Yes | — |  |
| `dnp` | Yes | — |  |
| `variation_count` | Yes | — |  |
| `parameter_count` | Yes | — |  |
| `param_variation_count` | Yes | — |  |
| `rows` | Yes | — |  |

## ImportedVariantsList_VariantRow

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `variant` | Yes | — |  |
| `sheet` | Yes | — |  |
| `designator` | Yes | — |  |
| `operation` | Yes | — |  |
| `detail` | Yes | — |  |
| `component_value` | Yes | — |  |
| `parameter_name` | Yes | — |  |
| `value` | Yes | — |  |
| `unique_id` | Yes | — |  |
| `alternate_part` | No | — |  |
| `alternate_part_resolved` | No | — |  |
