# EasyEDA footprint mapping output fields

Generated from src/tsp/altium_cruncher/outputs/easyeda.tsp. Do not edit.

Wire fields emitted by Cruncher. Validation preserves the payload without inserting defaults.

See the contract authority inventory for producer locations and delegated upstream data boundaries.

## EasyedaFootprintReport

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `lcsc_id` | Yes | — |  |
| `footprint_name` | Yes | — |  |
| `source_pad_count` | Yes | — |  |
| `generated_pad_count` | Yes | — |  |
| `generated_hole_pad_count` | Yes | — |  |
| `custom_pad_count` | Yes | — |  |
| `slotted_pad_count` | Yes | — |  |
| `track_count` | Yes | — |  |
| `track_segment_count` | Yes | — |  |
| `circle_count` | Yes | — |  |
| `arc_count` | Yes | — |  |
| `rectangle_count` | Yes | — |  |
| `region_count` | Yes | — |  |
| `text_count` | Yes | — |  |
| `unsupported_count` | Yes | — |  |
| `unsupported_graphics` | Yes | — |  |
| `warnings` | Yes | — |  |
| `layers` | Yes | — |  |
| `policy` | Yes | — |  |
| `transform` | Yes | — |  |
| `model_3d_attached` | Yes | — |  |
| `model_3d_centered_fallback` | Yes | — |  |
| `model_3d_placement_verdict` | Yes | — |  |
| `model_3d` | Yes | — |  |

## RecordInteger

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## FootprintPolicy

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `mils_per_easyeda_unit` | No | — |  |
| `invert_y` | No | — |  |
| `include_source_graphics` | No | — |  |
| `include_source_text` | No | — |  |
| `include_non_pad_holes` | No | — |  |
| `default_graphic_width_mils` | No | — |  |
| `curve_approximation_segments` | No | — |  |
| `arc_approximation_max_degrees` | No | — |  |

## FootprintTransform

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `anchor_x` | No | — |  |
| `anchor_y` | No | — |  |
| `mils_per_easyeda_unit` | No | — |  |
| `invert_y` | No | — |  |

## ModelAttachment

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `name` | No | — |  |
| `error` | No | — |  |
| `location_mils` | No | — |  |
| `raw_location_mils` | No | — |  |
| `centered_fallback` | No | — |  |
| `rotation_degrees` | No | — |  |
| `standoff_mils` | No | — |  |
| `identifier` | No | — |  |
| `placement_check` | No | — |  |

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
