# PcbSvgTimings output fields

Generated from src/tsp/altium_cruncher/outputs/pcb-svg-timings.tsp. Do not edit.

Wire fields emitted by Cruncher. Validation preserves the payload without inserting defaults.

See the contract authority inventory for producer locations and delegated upstream data boundaries.

## PcbSvgTimings

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — |  |
| `clock` | Yes | — |  |
| `workers` | No | — |  |
| `notes` | Yes | — |  |
| `model_cache` | No | — |  |
| `events` | Yes | — |  |

## PcbSvgTimingsModelCacheObject

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `directory` | Yes | — |  |
| `counts` | Yes | — |  |
| `read_seconds` | Yes | — |  |
| `write_seconds` | Yes | — |  |

## PcbSvgTimingsEventsItem

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | Yes | — |  |
| `parent_id` | Yes | — |  |
| `stage` | Yes | — |  |
| `command` | No | — |  |
| `board` | No | — |  |
| `variant` | No | — |  |
| `view` | No | — |  |
| `side` | No | — |  |
| `layer` | No | — |  |
| `part` | No | — |  |
| `cache` | Yes | — |  |
| `failed` | Yes | — |  |
| `seconds` | Yes | — |  |
| `exclusive_seconds` | Yes | — |  |

## PcbSvgTimingsModelCacheObjectCounts

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `hits` | Yes | — |  |
| `misses` | Yes | — |  |
| `writes` | Yes | — |  |
| `invalid` | Yes | — |  |
| `evictions` | Yes | — |  |
