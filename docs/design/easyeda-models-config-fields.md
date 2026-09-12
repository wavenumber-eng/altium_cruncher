# EasyEDA model downloads output fields

Generated from src/tsp/altium_cruncher/outputs/easyeda.tsp. Do not edit.

Wire fields emitted by Cruncher. Validation preserves the payload without inserting defaults.

See the contract authority inventory for producer locations and delegated upstream data boundaries.

## EasyedaModels

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — |  |
| `lcsc_id` | Yes | — |  |
| `placement_implemented` | Yes | — |  |
| `placement_note` | Yes | — |  |
| `models` | Yes | — |  |
| `placement_verdict` | No | — |  |
| `placement_check` | No | — |  |

## ModelReference

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `uuid` | Yes | — |  |
| `title` | Yes | — |  |
| `origin` | Yes | — |  |
| `z` | Yes | — |  |
| `rotation` | Yes | — |  |
| `files` | Yes | — |  |
| `errors` | Yes | — |  |
| `placement_status` | Yes | — |  |

## PlacementCheck

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `verdict` | No | — |  |
| `checked` | No | — |  |
| `reason` | No | — |  |
| `center_distance_mils` | No | — |  |
| `distance_ratio` | No | — |  |
| `model_bounds_mils` | No | — |  |
| `pad_bounds_mils` | No | — |  |

## RecordString

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
