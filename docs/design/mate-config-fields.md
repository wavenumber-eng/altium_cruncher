# Mate configuration fields

Generated from src/tsp/altium_cruncher/config/mate-config.tsp. Do not edit.

Required paths/sections are checked at loading. Defaults describe generated templates or adapter fallbacks; codecs do not insert them.

Path resolution, normalization and native CAD semantics remain Python adapter behavior.

## CurrentMate

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `output` | No | — |  |
| `libraries` | No | — |  |
| `known_parts` | No | — |  |
| `pcb_designators` | No | — |  |
| `artifacts` | No | — |  |
| `schema` | Yes | — |  |
| `source` | No | — |  |
| `validation` | No | — |  |
| `projections` | No | — |  |
| `board_projection` | No | — |  |

## LegacyMate

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `output` | No | — |  |
| `libraries` | No | — |  |
| `known_parts` | No | — |  |
| `pcb_designators` | No | — |  |
| `artifacts` | No | — |  |
| `schema` | No | — |  |
| `source` | No | — |  |
| `marker` | No | — |  |
| `placement` | No | — |  |
| `pcb_labels` | No | — |  |
| `selection` | No | — |  |
| `board_projection` | No | — |  |

## Output

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `backend` | No | — |  |
| `output_dir` | No | — |  |
| `project_name` | No | — |  |
| `schematic_filename` | No | — |  |
| `schematic_sheet_style` | No | — |  |
| `board_filename` | No | — |  |
| `project_filename` | No | — |  |
| `origin` | No | — |  |
| `overwrite` | No | — |  |
| `layer_stack_template` | No | — |  |
| `board_outline` | No | — |  |
| `board_outline_mils` | No | — |  |
| `board_origin_mils` | No | — |  |

## Libraries

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `roots` | No | — |  |
| `recursive` | No | — |  |

## KnownParts

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `manifest` | No | — |  |
| `cache_dir` | No | — |  |

## Designators

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | — |  |
| `placement` | No | — |  |
| `offset_mils` | No | — |  |
| `width_factor` | No | — |  |
| `style` | No | — |  |

## Artifacts

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `pcb_layer_step` | No | — |  |

## Validation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `source_side` | No | — |  |
| `allow_side_agnostic_through_hole` | No | — | Retained template field; the current parser does not consult it. |
| `side_agnostic_kinds` | No | — |  |

## Projection

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — |  |
| `source` | No | — |  |
| `select` | No | — |  |
| `actions` | No | — |  |

## BoardProjection

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `outline` | No | — |  |
| `cutouts` | No | — |  |

## RecordUnknown

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## Labels

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `side` | No | — |  |
| `offset_mils` | No | — |  |
| `box_size_mils` | No | — |  |
| `center_box_on_target` | No | — |  |
| `row_spacing_mils` | No | — |  |
| `column_spacing_mils` | No | — |  |
| `auto_width_padding_mils` | No | — |  |
| `enabled` | No | — |  |
| `style` | No | — |  |

## SelectedBoard

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `board_key` | No | — |  |
| `pcb_path` | No | — |  |
| `components` | No | — |  |
| `free_pads` | No | — |  |
| `board_outline_mils` | No | — |  |
| `board_outline` | No | — |  |

## OutputOutline

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `mode` | No | — |  |
| `margin_mils` | No | — |  |

## Bounds

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `left` | Yes | — |  |
| `bottom` | Yes | — |  |
| `right` | Yes | — |  |
| `top` | Yes | — |  |

## Point

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `x` | Yes | — |  |
| `y` | Yes | — |  |

## TextStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `height_mils` | No | — |  |
| `layer` | No | — |  |
| `font_kind` | No | — | Text-kind aliases are normalized by the shared MCO text adapter, including True Type and BARCODE. |
| `font_name` | No | — |  |
| `bold` | No | — |  |
| `italic` | No | — |  |
| `stroke_width_mils` | No | — |  |
| `text_justification` | No | — |  |
| `is_inverted` | No | — |  |
| `inverted_margin_mils` | No | — |  |
| `use_inverted_rectangle` | No | — |  |
| `is_frame` | No | — |  |
| `header_height_mils` | No | — |  |
| `header_stroke_width_mils` | No | — |  |
| `rotation_degrees` | No | — |  |
| `stroke_font_type` | No | — |  |
| `is_comment` | No | — |  |
| `is_designator` | No | — |  |
| `is_mirrored` | No | — |  |
| `barcode_kind` | No | — |  |
| `barcode_render_mode` | No | — |  |
| `barcode_full_size_mils` | No | — |  |
| `barcode_margin_mils` | No | — |  |
| `barcode_min_width_mils` | No | — |  |
| `barcode_show_text` | No | — |  |
| `barcode_inverted` | No | — |  |

## LayerStepArtifact

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
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
| `enabled` | No | — | Omitted or false disables the artifact, independently of generated template defaults. |
| `source_layer` | No | — |  |
| `insert_in_output` | No | — | true enables insertion; an empty object retains disabled-by-default semantics. |
| `highlights` | No | — |  |

## SourceSelector

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `object` | No | — | Case/hyphen-normalized component(s), free_pad(s), pad(s), or drill(s). |
| `type` | No | — |  |
| `kind` | No | — |  |
| `kinds` | No | — |  |
| `designators` | No | — |  |
| `hole_size_mils` | No | — |  |
| `plated` | No | — |  |

## Graphics

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | — |  |
| `layer` | No | — |  |
| `stroke_width_mils` | No | — |  |

## SelectedComponent

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `mate_projection_id` | No | — |  |
| `mate_part_role` | No | — |  |
| `mate_component` | No | — |  |
| `mate_pcb_label` | No | — |  |
| `mate_reference_graphics` | No | — |  |
| `source_power_port` | No | — |  |
| `source_pad_geometries` | No | — |  |
| `designator` | No | — |  |
| `kind` | No | — |  |
| `layer` | No | — |  |
| `footprint` | No | — |  |
| `x_mils` | No | — |  |
| `y_mils` | No | — |  |
| `net_name` | No | — |  |

## SelectedPad

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `mate_projection_id` | No | — |  |
| `mate_part_role` | No | — |  |
| `mate_component` | No | — |  |
| `mate_pcb_label` | No | — |  |
| `mate_reference_graphics` | No | — |  |
| `source_power_port` | No | — |  |
| `source_pad_geometries` | No | — |  |
| `designator` | No | — |  |
| `kind` | No | — |  |
| `x_mils` | No | — |  |
| `y_mils` | No | — |  |
| `net_name` | No | — |  |
| `width_mils` | No | — |  |
| `height_mils` | No | — |  |
| `hole_size_mils` | No | — |  |
| `shape` | No | — |  |
| `layer` | No | — |  |
| `rotation_degrees` | No | — |  |

## InputOutline

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `vertices` | Yes | — |  |
| `closed` | No | — |  |
| `cutouts` | No | — |  |

## Margins

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `left` | No | — |  |
| `bottom` | No | — |  |
| `right` | No | — |  |
| `top` | No | — |  |

## BoardOutline

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `color` | No | — |  |
| `cutout_color` | No | — |  |
| `cutouts_color` | No | — |  |
| `cutouts` | No | — |  |
| `width_mm` | No | — |  |
| `fuse` | No | — |  |

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

## InsertArtifact

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | — |  |
| `name` | No | — |  |
| `layer` | No | — |  |
| `side` | No | — |  |
| `location_mils` | No | — |  |
| `z_mm` | No | — |  |
| `rotation_z_degrees` | No | — |  |
| `opacity` | No | — |  |
| `bounds_mils` | No | — |  |

## Highlight

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `projection` | Yes | — |  |
| `name` | No | — |  |
| `color` | No | — |  |
| `z_offset_mm` | No | — |  |
| `thickness_mm` | No | — |  |

## MilRange

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `min` | No | — |  |
| `max` | No | — |  |

## ComponentAction

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `part` | No | — |  |
| `role` | No | — |  |
| `description` | No | — |  |
| `symbol_name` | No | — |  |
| `footprint_name` | No | — |  |
| `designator_prefix` | No | — |  |
| `signal_pad_designator` | No | — |  |
| `kind` | Yes | — |  |

## ReferenceAction

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `kind` | Yes | — |  |
| `shape` | No | — |  |
| `layer` | No | — |  |
| `enabled` | No | — |  |
| `style` | No | — |  |

## LabelAction

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `kind` | Yes | — |  |
| `enabled` | No | — |  |
| `style` | No | — |  |
| `text` | No | — | Retained input; current label generation uses source nets. |
| `value` | No | — |  |
| `placement` | No | — |  |

## MateComponentSettings

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `kind` | No | — |  |
| `part` | No | — |  |
| `role` | No | — |  |
| `description` | No | — |  |
| `symbol_name` | No | — |  |
| `footprint_name` | No | — |  |
| `designator_prefix` | No | — |  |
| `signal_pad_designator` | No | — |  |

## ReferenceGraphics

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | — |  |
| `layer` | No | — |  |
| `shape` | No | — |  |
| `style` | No | — |  |

## InputPowerPort

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `text` | No | — |  |
| `style` | No | — |  |
| `show_net_name` | No | — |  |

## InputPadGeometry

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `x_mils` | No | — |  |
| `y_mils` | No | — |  |
| `width_mils` | No | — |  |
| `height_mils` | No | — |  |
| `shape` | No | — |  |
| `layer` | No | — |  |
| `rotation_degrees` | No | — |  |
| `corner_radius_mils` | No | — |  |

## InputVertex

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `x_mils` | Yes | — |  |
| `y_mils` | Yes | — |  |
| `segment` | No | — |  |
| `center_mils` | No | — |  |
| `radius_mils` | No | — |  |
| `start_angle_degrees` | No | — |  |
| `end_angle_degrees` | No | — |  |

## FeatureDefaults

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `color` | No | — |  |

## ReferenceStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `mode` | No | — |  |
| `outline_count` | No | — |  |
| `clearance_mils` | No | — |  |
| `outline_spacing_mils` | No | — |  |
| `stroke_width_mils` | No | — |  |

## LabelPlacement

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `side` | No | — |  |
| `offset_mils` | No | — |  |
| `box_size_mils` | No | — |  |
| `center_box_on_target` | No | — |  |
| `row_spacing_mils` | No | — |  |
| `column_spacing_mils` | No | — |  |
| `auto_width_padding_mils` | No | — |  |

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
