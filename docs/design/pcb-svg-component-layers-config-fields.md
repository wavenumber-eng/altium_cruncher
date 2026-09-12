# PcbSvgComponentLayers output fields

Generated from src/tsp/altium_cruncher/outputs/pcb-svg-component-layers.tsp. Do not edit.

Wire fields emitted by Cruncher. Validation preserves the payload without inserting defaults.

See the contract authority inventory for producer locations and delegated upstream data boundaries.

## PcbSvgComponentLayers

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — |  |
| `coordinate_policy` | Yes | — |  |
| `layers` | Yes | — |  |

## PcbSvgComponentLayersLayersItem

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `token` | Yes | — |  |
| `group_id` | Yes | — |  |
| `side` | Yes | — |  |
| `instances` | Yes | — |  |
| `unique_symbols` | No | — |  |

## RecordUnknown

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## PcbSvgComponentLayersLayersItemInstancesItem

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `group_id` | Yes | — |  |
| `component_index` | Yes | — |  |
| `designator` | Yes | — |  |
| `side` | No | — |  |
| `symbol_id` | No | — |  |
| `anchor_svg_mm` | No | — |  |
| `anchor_board_mm` | No | — |  |
| `bounds_local_xyz_mm` | No | — |  |
| `bodies` | No | — |  |
| `paint_order` | No | — |  |
| `geometry_source` | No | — |  |
| `center_view_mm` | No | — |  |
| `font_size_mm` | No | — |  |
| `rotation_degrees` | No | — |  |

## PcbSvgComponentLayersLayersItemInstancesItemBodiesItem

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `index` | Yes | — |  |
| `kind` | Yes | — |  |
| `lower_z_mm` | Yes | — |  |
| `upper_z_mm` | Yes | — |  |
| `color` | Yes | — |  |
| `opacity` | Yes | — |  |
