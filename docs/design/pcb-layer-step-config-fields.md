# PCB layer STEP configuration fields

Generated from src/tsp/altium_cruncher/config/pcb-layer-step-config.tsp. Do not edit.

Required paths/sections are checked at loading. Defaults describe generated templates or adapter fallbacks; codecs do not insert them.

Path resolution, normalization and native CAD semantics remain Python adapter behavior.

## PcbLayerStepConfigInput

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | No | `"altium_cruncher.pcb_layer_step.config.a0"` |  |
| `defaults` | No | — |  |
| `outputs` | No | — |  |
| `options` | No | — |  |
| `name` | No | — |  |
| `output_step` | No | — |  |
| `pcbdoc` | No | — |  |
| `layer` | No | — |  |
| `thickness_mm` | No | — |  |
| `z_mm` | No | — |  |
| `copper_color` | No | — |  |
| `outline_width_mm` | No | — |  |
| `outline_color` | No | — |  |
| `board_cutout_color` | No | — |  |
| `include_board_cutouts` | No | — |  |
| `include_copper` | No | — |  |
| `include_board_outline` | No | — |  |
| `include_poured_polygons` | No | — |  |
| `cut_holes` | No | — |  |
| `drill_hole_mode` | No | — |  |
| `max_boolean_drill_cuts` | No | — |  |
| `drill_hole_color` | No | — |  |
| `drill_plated_hole_color` | No | — |  |
| `drill_non_plated_hole_color` | No | — |  |
| `drill_overlay_thickness_mm` | No | — |  |
| `drill_minimum_diameter_mm` | No | — |  |
| `drill_hole_shape` | No | — |  |
| `drill_ring_width_mm` | No | — |  |
| `drill_plated_ring_shape` | No | — |  |
| `drill_selected_component_mode` | No | — |  |
| `drill_other_component_mode` | No | — |  |
| `drill_free_pad_mode` | No | — |  |
| `drill_via_mode` | No | — |  |
| `fuse_copper` | No | — |  |
| `fuse_board_outline` | No | — |  |
| `arc_segments` | No | — |  |
| `include_tracks` | No | — |  |
| `include_arcs` | No | — |  |
| `include_fills` | No | — |  |
| `include_regions` | No | — |  |
| `include_vias` | No | — |  |
| `include_component_pads` | No | — |  |
| `include_free_pads` | No | — |  |
| `include_designators` | No | — |  |
| `board_outline` | No | — |  |
| `features` | No | — |  |
| `drills` | No | — |  |

## OutputOptions

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `options` | No | — |  |
| `name` | No | — |  |
| `output_step` | No | — |  |
| `pcbdoc` | No | `null` |  |
| `layer` | No | `"bottom"` |  |
| `thickness_mm` | No | `0.035` |  |
| `z_mm` | No | `0` |  |
| `copper_color` | No | — |  |
| `outline_width_mm` | No | — |  |
| `outline_color` | No | — |  |
| `board_cutout_color` | No | — |  |
| `include_board_cutouts` | No | — |  |
| `include_copper` | No | — |  |
| `include_board_outline` | No | `true` |  |
| `include_poured_polygons` | No | — |  |
| `cut_holes` | No | — |  |
| `drill_hole_mode` | No | — |  |
| `max_boolean_drill_cuts` | No | — |  |
| `drill_hole_color` | No | — |  |
| `drill_plated_hole_color` | No | — |  |
| `drill_non_plated_hole_color` | No | — |  |
| `drill_overlay_thickness_mm` | No | — |  |
| `drill_minimum_diameter_mm` | No | — |  |
| `drill_hole_shape` | No | — |  |
| `drill_ring_width_mm` | No | — |  |
| `drill_plated_ring_shape` | No | — |  |
| `drill_selected_component_mode` | No | — |  |
| `drill_other_component_mode` | No | — |  |
| `drill_free_pad_mode` | No | — |  |
| `drill_via_mode` | No | — |  |
| `fuse_copper` | No | — |  |
| `fuse_board_outline` | No | — |  |
| `arc_segments` | No | — |  |
| `include_tracks` | No | — |  |
| `include_arcs` | No | — |  |
| `include_fills` | No | — |  |
| `include_regions` | No | — |  |
| `include_vias` | No | — |  |
| `include_component_pads` | No | — |  |
| `include_free_pads` | No | — |  |
| `include_designators` | No | — |  |
| `board_outline` | No | — |  |
| `features` | No | — |  |
| `drills` | No | — |  |

## BoardOutline

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `color` | No | `"#FFFF00"` |  |
| `cutout_color` | No | `"#FFFF00"` |  |
| `cutouts_color` | No | — |  |
| `cutouts` | No | `true` |  |
| `width_mm` | No | `0.2` |  |
| `fuse` | No | `true` |  |

## Features

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `defaults` | No | — |  |
| `tracks` | No | — |  |
| `traces` | No | — |  |
| `arcs` | No | — |  |
| `fills` | No | — |  |
| `polygons` | No | — |  |
| `poured_polygons` | No | — |  |
| `regions` | No | — |  |
| `shapebased_regions` | No | — |  |
| `vias` | No | — |  |
| `component_pads` | No | — |  |
| `free_pads` | No | — |  |

## Drills

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `mode` | No | — |  |
| `minimum_diameter_mm` | No | — |  |
| `shape` | No | — |  |
| `color` | No | — |  |
| `plated_color` | No | — |  |
| `non_plated_color` | No | — |  |
| `ring_width_mm` | No | — |  |
| `plated_ring_shape` | No | — |  |
| `selected_component_mode` | No | — |  |
| `other_component_mode` | No | — |  |
| `free_pad_mode` | No | — |  |
| `via_mode` | No | — |  |
| `overlay_thickness_mm` | No | — |  |

## FeatureDefaults

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `color` | No | — |  |

## FeatureSwitchOption2

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | — |  |
| `color` | No | — |  |
| `step_body_name` | No | — |  |
| `thickness_bias_mm` | No | — |  |

## ComponentPads

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | — |  |
| `mode` | No | — |  |
| `include_designators` | No | — |  |
| `color` | No | — |  |
| `step_body_name` | No | — |  |
| `thickness_bias_mm` | No | — |  |
| `highlight_rules` | No | — |  |

## HighlightRulesValueItem

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `designators` | Yes | — |  |
| `color` | Yes | — |  |
| `step_body_name` | No | — |  |
