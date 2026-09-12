# PCB layer STEP sidecar output fields

Generated from src/tsp/altium_cruncher/outputs/pcb-layer-step.tsp. Do not edit.

Wire fields emitted by Cruncher. Validation preserves the payload without inserting defaults.

See the contract authority inventory for producer locations and delegated upstream data boundaries.

## PcbLayerStepManifest

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — |  |
| `backend` | Yes | — |  |
| `board` | Yes | — |  |
| `source_input` | Yes | — |  |
| `step_file` | Yes | — |  |
| `coordinate_origin` | Yes | — |  |
| `layer` | Yes | — |  |
| `options` | Yes | — |  |
| `counts` | Yes | — |  |
| `bytes` | Yes | — |  |

## CoordinateOrigin

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `mode` | Yes | — |  |
| `origin_mils` | Yes | — |  |
| `origin_mm` | Yes | — |  |
| `geometry` | Yes | — |  |

## Layer

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | Yes | — |  |
| `json_name` | Yes | — |  |
| `display_name` | Yes | — |  |

## Options

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `thickness_mm` | Yes | — |  |
| `z_mm` | Yes | — |  |
| `copper_color` | Yes | — |  |
| `outline_width_mm` | Yes | — |  |
| `outline_color` | Yes | — |  |
| `board_cutout_color` | Yes | — |  |
| `include_copper` | Yes | — |  |
| `include_board_outline` | Yes | — |  |
| `include_board_cutouts` | Yes | — |  |
| `include_poured_polygons` | Yes | — |  |
| `cut_holes` | Yes | — |  |
| `drill_hole_mode` | Yes | — |  |
| `effective_drill_hole_mode` | Yes | — |  |
| `max_boolean_drill_cuts` | Yes | — |  |
| `drill_hole_color` | Yes | — |  |
| `drill_plated_hole_color` | Yes | — |  |
| `drill_non_plated_hole_color` | Yes | — |  |
| `drill_overlay_thickness_mm` | Yes | — |  |
| `drill_minimum_diameter_mm` | Yes | — |  |
| `drill_hole_shape` | Yes | — |  |
| `drill_ring_width_mm` | Yes | — |  |
| `drill_plated_ring_shape` | Yes | — |  |
| `drill_selected_component_mode` | Yes | — |  |
| `drill_other_component_mode` | Yes | — |  |
| `drill_free_pad_mode` | Yes | — |  |
| `drill_via_mode` | Yes | — |  |
| `fuse_copper` | Yes | — |  |
| `fuse_board_outline` | Yes | — |  |
| `arc_segments` | Yes | — |  |
| `features` | Yes | — |  |
| `pad_color_rules` | Yes | — |  |
| `feature_color_rules` | Yes | — |  |
| `thickness_bias_mm` | Yes | — |  |
| `highlight_count` | Yes | — |  |

## RecordInteger

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## FeatureSwitches

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `tracks` | Yes | — |  |
| `arcs` | Yes | — |  |
| `fills` | Yes | — |  |
| `polygons` | Yes | — |  |
| `regions` | Yes | — |  |
| `vias` | Yes | — |  |
| `component_pads` | Yes | — |  |
| `free_pads` | Yes | — |  |
| `include_designators` | Yes | — |  |

## PadColorRule

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `designators` | Yes | — |  |
| `color` | Yes | — |  |
| `step_body_name` | Yes | — |  |

## FeatureStyles

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `tracks` | Yes | — |  |
| `arcs` | Yes | — |  |
| `fills` | Yes | — |  |
| `polygons` | Yes | — |  |
| `regions` | Yes | — |  |
| `vias` | Yes | — |  |
| `component_pads` | Yes | — |  |
| `free_pads` | Yes | — |  |

## ThicknessBias

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `tracks` | Yes | — |  |
| `arcs` | Yes | — |  |
| `fills` | Yes | — |  |
| `polygons` | Yes | — |  |
| `regions` | Yes | — |  |
| `vias` | Yes | — |  |
| `component_pads` | Yes | — |  |
| `free_pads` | Yes | — |  |

## FeatureStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `color` | Yes | — |  |
| `step_body_name` | Yes | — |  |
