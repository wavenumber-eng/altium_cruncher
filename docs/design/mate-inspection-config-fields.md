# Mate inspection output fields

Generated from src/tsp/altium_cruncher/outputs/mate.tsp. Do not edit.

Wire fields emitted by Cruncher. Validation preserves the payload without inserting defaults.

See the contract authority inventory for producer locations and delegated upstream data boundaries.

## MateInspection

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — |  |
| `source` | Yes | — |  |
| `source_tag` | Yes | — |  |
| `boards` | Yes | — |  |

## Board

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `board_key` | Yes | — |  |
| `pcb_path` | Yes | — |  |
| `components` | Yes | — |  |
| `free_pads` | Yes | — |  |
| `board_outline_mils` | No | — |  |
| `board_outline` | No | — |  |
| `board_origin_mils` | No | — |  |

## Component

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `designator` | Yes | — |  |
| `kind` | Yes | — |  |
| `layer` | Yes | — |  |
| `footprint` | Yes | — |  |
| `x_mils` | Yes | — |  |
| `y_mils` | Yes | — |  |
| `net_name` | No | — |  |
| `source_power_port` | No | — |  |
| `source_pad_geometries` | No | — |  |

## FreePad

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `designator` | Yes | — |  |
| `kind` | Yes | — |  |
| `layer` | Yes | — |  |
| `x_mils` | Yes | — |  |
| `y_mils` | Yes | — |  |
| `width_mils` | Yes | — |  |
| `height_mils` | Yes | — |  |
| `hole_size_mils` | Yes | — |  |
| `plated` | Yes | — |  |
| `shape` | Yes | — |  |
| `net_name` | No | — |  |
| `source_power_port` | No | — |  |

## Bounds

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `left` | Yes | — |  |
| `bottom` | Yes | — |  |
| `right` | Yes | — |  |
| `top` | Yes | — |  |

## Outline

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `vertices` | Yes | — |  |
| `closed` | Yes | — |  |
| `cutouts` | No | — |  |

## Point

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `x` | Yes | — |  |
| `y` | Yes | — |  |

## PowerPort

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `text` | Yes | — |  |
| `style` | Yes | — |  |
| `show_net_name` | Yes | — |  |

## PadGeometry

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `x_mils` | Yes | — |  |
| `y_mils` | Yes | — |  |
| `width_mils` | Yes | — |  |
| `height_mils` | Yes | — |  |
| `shape` | Yes | — |  |
| `layer` | Yes | — |  |
| `rotation_degrees` | Yes | — |  |
| `corner_radius_mils` | No | — |  |

## LineVertex

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `x_mils` | Yes | — |  |
| `y_mils` | Yes | — |  |
| `segment` | Yes | — |  |

## ArcVertex

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `x_mils` | Yes | — |  |
| `y_mils` | Yes | — |  |
| `segment` | Yes | — |  |
| `center_mils` | Yes | — |  |
| `radius_mils` | Yes | — |  |
| `start_angle_degrees` | Yes | — |  |
| `end_angle_degrees` | Yes | — |  |
