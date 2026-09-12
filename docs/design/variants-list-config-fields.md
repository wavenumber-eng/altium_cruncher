# Project variant listing output fields

Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit.

Wire fields emitted by Cruncher. Validation preserves the payload without inserting defaults.

See the contract authority inventory for producer locations and delegated upstream data boundaries.

## VariantsList

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — |  |
| `project` | Yes | — |  |
| `current_variant` | Yes | — |  |
| `variant_count` | Yes | — |  |
| `variants` | Yes | — |  |
| `rows` | Yes | — |  |
| `index_errors` | Yes | — |  |

## Variant

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

## VariantRow

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
