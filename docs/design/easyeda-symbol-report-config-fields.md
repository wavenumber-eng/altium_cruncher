# EasyEDA symbol mapping output fields

Generated from src/tsp/altium_cruncher/outputs/easyeda.tsp. Do not edit.

Wire fields emitted by Cruncher. Validation preserves the payload without inserting defaults.

See the contract authority inventory for producer locations and delegated upstream data boundaries.

## EasyedaSymbolReport

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `lcsc_id` | Yes | — |  |
| `symbol_name` | Yes | — |  |
| `designator` | Yes | — |  |
| `pin_count` | Yes | — |  |
| `rectangle_count` | Yes | — |  |
| `circle_count` | Yes | — |  |
| `ellipse_count` | Yes | — |  |
| `polyline_count` | Yes | — |  |
| `polygon_count` | Yes | — |  |
| `unsupported_count` | Yes | — |  |
| `unsupported_graphics` | Yes | — |  |
| `warnings` | Yes | — |  |
| `policy` | Yes | — |  |
| `grid` | Yes | — |  |

## SymbolPolicy

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `mils_per_easyeda_unit` | No | — |  |
| `invert_y` | No | — |  |
| `default_pin_length_mils` | No | — |  |
| `hotspot_grid_mils` | No | — |  |
| `align_hotspots_to_grid` | No | — |  |
| `body_color` | No | — |  |
| `body_fill_color` | No | — |  |
| `use_source_pin_electrical` | No | — |  |
| `use_source_pin_ieee_symbols` | No | — |  |
| `pin_name_visibility` | No | — |  |
| `pin_designator_visibility` | No | — |  |
| `pin_text_orientation` | No | — |  |
| `rotate_vertical_pin_text` | No | — |  |

## HotspotGrid

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `hotspot_grid_mils` | No | — |  |
| `align_hotspots_to_grid` | No | — |  |
| `anchor_adjusted_to_grid` | No | — |  |
| `source_grid_units` | No | — |  |
| `source_common_offset_possible` | No | — |  |
| `source_x_remainder` | No | — |  |
| `source_y_remainder` | No | — |  |
| `hotspot_count` | No | — |  |
| `off_grid_hotspot_count` | No | — |  |
| `max_hotspot_error_mils` | No | — |  |
| `off_grid_hotspots_sample` | No | — |  |

## OffGridHotspot

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `pin` | Yes | — |  |
| `name` | Yes | — |  |
| `x_mils` | Yes | — |  |
| `y_mils` | Yes | — |  |
| `x_error_mils` | Yes | — |  |
| `y_error_mils` | Yes | — |  |
