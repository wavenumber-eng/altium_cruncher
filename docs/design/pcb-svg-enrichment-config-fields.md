# Cruncher PCB SVG metadata extensions output fields

Generated from src/tsp/altium_cruncher/outputs/pcb-svg-enrichment.tsp. Do not edit.

Wire fields emitted by Cruncher. Validation preserves the payload without inserting defaults.

See the contract authority inventory for producer locations and delegated upstream data boundaries.

## PcbSvgEnrichment

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `canvas` | Yes | — |  |
| `virtual_component_layers` | No | — |  |

## Canvas

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `bounds_mode` | Yes | — |  |
| `bounds_mils` | Yes | — |  |
| `margin_mm` | Yes | — |  |
| `altium_origin_mils` | Yes | — |  |
| `svg_units` | Yes | — |  |
| `geometry_transform` | Yes | — |  |
| `metadata_coordinate_policy` | Yes | — |  |
| `view_box_mm` | No | — |  |
| `scene_mirror_x` | No | — |  |
| `scene_mirror_width_mm` | No | — |  |

## RecordUnknown

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## ImportedPcbSvgComponentLayers

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — |  |
| `coordinate_policy` | Yes | — |  |
| `layers` | Yes | — |  |

## ImportedPcbSvgComponentLayers_PcbSvgComponentLayersLayersItem

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `token` | Yes | — |  |
| `group_id` | Yes | — |  |
| `side` | Yes | — |  |
| `instances` | Yes | — |  |
| `unique_symbols` | No | — |  |

## ImportedPcbSvgComponentLayers_RecordUnknown

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## ImportedPcbSvgComponentLayers_PcbSvgComponentLayersLayersItemInstancesItem

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

## ImportedPcbSvgComponentLayers_PcbSvgComponentLayersLayersItemInstancesItemBodiesItem

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `index` | Yes | — |  |
| `kind` | Yes | — |  |
| `lower_z_mm` | Yes | — |  |
| `upper_z_mm` | Yes | — |  |
| `color` | Yes | — |  |
| `opacity` | Yes | — |  |
