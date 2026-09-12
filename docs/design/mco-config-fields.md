# MCO operations configuration fields

Generated from src/tsp/altium_cruncher/mco/main.tsp. Do not edit.

Authored MCO codecs preserve input fields and defaults; the execution envelope defers argument checks until a built-in operation is reached.

Execution, failure branches, custom registry behavior, dry-run checks and native CAD semantics remain Python behavior.

## McoDocument

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | No | — |  |
| `operations` | Yes | — |  |

## CustomOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — | Custom registry operation name; built-in names are excluded during generation. |
| `args` | No | — |  |

## RecordUnknown

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## FileCopyOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## McoFailOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | No | — |  |

## McoMessageOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | No | — |  |

## PcbdocAddArcOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## PcbdocAddComponentOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## PcbdocAddEmbedded3dModelOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## PcbdocAddFillOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## PcbdocAddPadOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## PcbdocAddRegionOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## PcbdocAddTextOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## PcbdocAddTrackOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## PcbdocAddViaOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## PcbdocArrangeDesignatorsOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## PcbdocCreateOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## PcbdocCreateUserUnionOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## PcbdocExportLayerStepOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## PcblibAddFootprintOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## PcblibCreateOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## ProjectAddDocumentOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## ProjectAddParameterOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## ProjectAddVariantOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## ProjectAddVariantDnpOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## ProjectCloneVariantOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## ProjectCreateOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## ProjectDeleteVariantOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## ProjectListVariantsOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## ProjectRenameVariantOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## ProjectToggleVariantDnpOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## SchdocAddComponentOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## SchdocAddNetLabelOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## SchdocAddPowerPortOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## SchdocAddWireOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## SchdocCreateOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## SchlibAddSymbolOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## SchlibCreateOperation

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | No | — | Stable operation ID; omission, null or empty generates opN in source order. |
| `message` | No | — | Optional human-readable operation message. |
| `on_fail` | No | — | Operation ID to jump to on failure. Null/omission stops on failure. |
| `op` | Yes | — |  |
| `args` | Yes | — |  |

## FileCopyArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `source` | Yes | — |  |
| `destination` | Yes | — |  |
| `overwrite` | No | `false` |  |

## McoFailArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `message` | No | — |  |

## McoMessageArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `text` | No | — |  |

## PcbdocAddArcArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — | Input Altium document path, relative to the MCO file directory. |
| `output_file` | No | — | Optional output document; otherwise overwrite=true is required. |
| `overwrite` | No | `false` | Allow overwriting the input or existing output document. |
| `center_mils` | Yes | — |  |
| `radius_mils` | Yes | — |  |
| `start_angle_degrees` | Yes | — |  |
| `end_angle_degrees` | Yes | — |  |
| `width_mils` | Yes | — |  |
| `layer` | No | `"TOP"` |  |
| `net` | No | `null` |  |

## PcbdocAddComponentArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — | Input Altium document path, relative to the MCO file directory. |
| `output_file` | No | — | Optional output document; otherwise overwrite=true is required. |
| `overwrite` | No | `false` | Allow overwriting the input or existing output document. |
| `library` | Yes | — |  |
| `footprint` | Yes | — |  |
| `designator` | Yes | — |  |
| `position_mils` | Yes | — |  |
| `layer` | No | `"TOP"` |  |
| `source_unique_id` | No | — |  |
| `source_hierarchical_path` | No | — |  |
| `source_component_library` | No | — |  |
| `source_lib_reference` | No | — |  |
| `source_description` | No | — |  |
| `channel_offset` | No | — |  |
| `comment_text` | No | `null` |  |
| `component_parameters` | No | — |  |
| `pad_nets` | No | — |  |
| `rotation_degrees` | No | `0` |  |
| `source_footprint_library` | No | — |  |
| `comment_visible` | No | `false` |  |
| `source_designator` | No | — |  |

## PcbdocAddEmbedded3dModelArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — | Input Altium document path, relative to the MCO file directory. |
| `output_file` | No | — | Optional output document; otherwise overwrite=true is required. |
| `overwrite` | No | `false` | Allow overwriting the input or existing output document. |
| `model_file` | Yes | — |  |
| `model_name` | No | — |  |
| `name` | No | — |  |
| `layer` | No | `"MECHANICAL_13"` |  |
| `side` | No | `"TOP"` |  |
| `location_mils` | No | `[0,0]` |  |
| `rotation_x_degrees` | No | `0` |  |
| `rotation_y_degrees` | No | `0` |  |
| `rotation_z_degrees` | No | `0` |  |
| `z_mm` | No | `0` |  |
| `bounds_mils` | No | — |  |
| `projection_outline_mils` | No | — |  |
| `overall_height_mils` | No | — |  |
| `opacity` | No | `1` |  |
| `z_mils` | No | — | Takes precedence over z_mm when supplied. |

## PcbdocAddFillArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — | Input Altium document path, relative to the MCO file directory. |
| `output_file` | No | — | Optional output document; otherwise overwrite=true is required. |
| `overwrite` | No | `false` | Allow overwriting the input or existing output document. |
| `corner1_mils` | Yes | — |  |
| `corner2_mils` | Yes | — |  |
| `rotation_degrees` | No | `0` |  |
| `layer` | No | `"TOP"` |  |
| `net` | No | `null` |  |

## PcbdocAddPadArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — | Input Altium document path, relative to the MCO file directory. |
| `output_file` | No | — | Optional output document; otherwise overwrite=true is required. |
| `overwrite` | No | `false` | Allow overwriting the input or existing output document. |
| `designator` | Yes | — |  |
| `position_mils` | Yes | — |  |
| `width_mils` | Yes | — |  |
| `height_mils` | Yes | — |  |
| `shape` | No | — |  |
| `corner_radius_percent` | No | — |  |
| `rotation_degrees` | No | `0` |  |
| `hole_size_mils` | No | `0` |  |
| `plated` | No | — |  |
| `layer` | No | `"TOP"` |  |
| `net` | No | `null` |  |
| `solder_mask_expansion_mils` | No | — |  |
| `paste_mask_expansion_mils` | No | — |  |
| `tenting_top` | No | — |  |
| `tenting_bottom` | No | — |  |
| `solder_mask_expansion_mode` | No | — |  |
| `paste_mask_expansion_mode` | No | — |  |

## PcbdocAddRegionArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — | Input Altium document path, relative to the MCO file directory. |
| `output_file` | No | — | Optional output document; otherwise overwrite=true is required. |
| `overwrite` | No | `false` | Allow overwriting the input or existing output document. |
| `outline_points_mils` | Yes | — |  |
| `layer` | No | `"TOP"` |  |
| `hole_points_mils` | No | — |  |
| `is_keepout` | No | `false` |  |
| `keepout_restrictions` | No | `0` |  |
| `net` | No | `null` |  |
| `is_board_cutout` | No | `false` |  |

## PcbdocAddTextArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — | Input Altium document path, relative to the MCO file directory. |
| `output_file` | No | — | Optional output document; otherwise overwrite=true is required. |
| `overwrite` | No | `false` | Allow overwriting the input or existing output document. |
| `text` | Yes | — |  |
| `position_mils` | Yes | — |  |
| `layer` | No | `"TOP_OVERLAY"` |  |
| `height_mils` | Yes | — |  |
| `font_kind` | No | `"stroke"` |  |
| `font_name` | No | `"Arial"` |  |
| `bold` | No | `false` |  |
| `italic` | No | `false` |  |
| `rotation_degrees` | No | `0` |  |
| `stroke_width_mils` | No | `10` |  |
| `is_comment` | No | `false` |  |
| `is_designator` | No | `false` |  |
| `is_mirrored` | No | `false` |  |
| `is_inverted` | No | `false` |  |
| `inverted_margin_mils` | No | `0` |  |
| `use_inverted_rectangle` | No | `false` |  |
| `inverted_rectangle_size_mils` | No | — |  |
| `is_frame` | No | `false` |  |
| `frame_size_mils` | No | — |  |
| `barcode_full_size_mils` | No | — |  |
| `barcode_margin_mils` | No | `[20,20]` |  |
| `barcode_min_width_mils` | No | `0` |  |
| `barcode_show_text` | No | `true` |  |
| `barcode_inverted` | No | `true` |  |
| `text_justification` | No | — |  |
| `barcode_kind` | No | — |  |
| `barcode_render_mode` | No | — |  |

## PcbdocAddTrackArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — | Input Altium document path, relative to the MCO file directory. |
| `output_file` | No | — | Optional output document; otherwise overwrite=true is required. |
| `overwrite` | No | `false` | Allow overwriting the input or existing output document. |
| `start_mils` | Yes | — |  |
| `end_mils` | Yes | — |  |
| `width_mils` | Yes | — |  |
| `layer` | No | `"TOP"` |  |
| `net` | No | `null` |  |

## PcbdocAddViaArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — | Input Altium document path, relative to the MCO file directory. |
| `output_file` | No | — | Optional output document; otherwise overwrite=true is required. |
| `overwrite` | No | `false` | Allow overwriting the input or existing output document. |
| `position_mils` | Yes | — |  |
| `diameter_mils` | Yes | — |  |
| `hole_size_mils` | Yes | — |  |
| `layer_start` | No | `"TOP"` |  |
| `layer_end` | No | `"BOTTOM"` |  |
| `net` | No | `null` |  |

## PcbdocArrangeDesignatorsArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — | Input Altium document path, relative to the MCO file directory. |
| `output_file` | No | — | Optional output document; otherwise overwrite=true is required. |
| `overwrite` | No | `false` | Allow overwriting the input or existing output document. |
| `designators` | No | — |  |
| `placement` | No | `"above_component"` |  |
| `offset_mils` | No | `[0,10]` |  |
| `height_mils` | No | `40` |  |
| `layer` | No | `"TOP_OVERLAY"` |  |
| `stroke_width_mils` | No | `8` |  |
| `width_factor` | No | `0.6` |  |
| `bold` | No | `true` |  |
| `italic` | No | `false` |  |
| `font_name` | No | `"Arial"` |  |
| `font_kind` | No | `"truetype"` |  |

## PcbdocCreateArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `layer_stack_template` | No | — |  |
| `rigid_stack` | No | — |  |
| `stackupx_file` | No | — |  |
| `board_outline_mils` | No | — |  |
| `board_origin_mils` | No | — |  |
| `sheet_frame_mils` | No | — |  |
| `mechanical_layer_profile` | No | — |  |
| `mechanical_layers` | No | — |  |
| `mechanical_layer_pairs` | No | — |  |
| `mechanical_layer_kinds` | No | — |  |
| `overwrite` | No | `false` |  |

## PcbdocCreateUserUnionArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — | Input Altium document path, relative to the MCO file directory. |
| `output_file` | No | — | Optional output document; otherwise overwrite=true is required. |
| `overwrite` | No | `false` | Allow overwriting the input or existing output document. |
| `name` | Yes | — |  |
| `members` | No | `"all"` |  |

## PcbdocExportLayerStepArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `output_file` | Yes | — |  |
| `layer` | No | — | Delegated to PcbLayerStepConfig along with additional fixture options; see pcb-layer-step configuration. |
| `board_name` | No | — |  |
| `highlights` | No | — |  |
| `overwrite` | No | `false` |  |

## PcblibAddFootprintArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — | Input Altium document path, relative to the MCO file directory. |
| `output_file` | No | — | Optional output document; otherwise overwrite=true is required. |
| `overwrite` | No | `false` | Allow overwriting the input or existing output document. |
| `name` | Yes | — |  |
| `height` | No | `"0mil"` |  |
| `description` | No | `""` |  |
| `item_guid` | No | `""` |  |
| `revision_guid` | No | `""` |  |
| `parameters` | No | — |  |
| `primitive_parameters` | No | — |  |

## PcblibCreateArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `overwrite` | No | `false` |  |

## ProjectAddDocumentArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `document` | Yes | — |  |
| `unique_id` | No | `null` |  |

## ProjectAddParameterArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `name` | Yes | — |  |
| `value` | Yes | — |  |

## ProjectAddVariantArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `name` | Yes | — |  |
| `unique_id` | No | `null` |  |
| `allow_fabrication` | No | `true` |  |
| `current` | No | `false` |  |

## ProjectAddVariantDnpArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `variant` | Yes | — |  |
| `designator` | Yes | — |  |
| `unique_id` | No | `null` |  |
| `alternate_part` | No | `""` |  |

## ProjectCloneVariantArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `source_name` | Yes | — |  |
| `name` | Yes | — |  |
| `unique_id` | No | `null` |  |
| `allow_fabrication` | No | — |  |
| `current` | No | `false` |  |

## ProjectCreateArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `name` | No | `null` |  |
| `project_name` | No | `null` |  |
| `overwrite` | No | `false` |  |

## ProjectDeleteVariantArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `name` | Yes | — |  |

## ProjectListVariantsArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |

## ProjectRenameVariantArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `name` | Yes | — |  |
| `new_name` | Yes | — |  |

## ProjectToggleVariantDnpArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `variant` | Yes | — |  |
| `designator` | Yes | — |  |
| `unique_id` | No | `null` |  |
| `alternate_part` | No | `""` |  |

## SchdocAddComponentArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — | Input Altium document path, relative to the MCO file directory. |
| `output_file` | No | — | Optional output document; otherwise overwrite=true is required. |
| `overwrite` | No | `false` | Allow overwriting the input or existing output document. |
| `library` | Yes | — |  |
| `symbol` | Yes | — |  |
| `designator` | Yes | — |  |
| `position_mils` | Yes | — |  |
| `unique_id` | No | `null` |  |
| `design_item_id` | No | `null` |  |
| `footprint_model` | No | `null` |  |
| `footprint_library` | No | `""` |  |
| `parameters` | No | — |  |
| `orientation` | No | `0` |  |
| `mirrored` | No | `false` |  |
| `part_id` | No | `1` |  |
| `display_mode` | No | `0` |  |
| `designator_style` | No | — |  |
| `comment_style` | No | — |  |
| `footprint_description` | No | `""` |  |

## SchdocAddNetLabelArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — | Input Altium document path, relative to the MCO file directory. |
| `output_file` | No | — | Optional output document; otherwise overwrite=true is required. |
| `overwrite` | No | `false` | Allow overwriting the input or existing output document. |
| `text` | Yes | — |  |
| `location_mils` | Yes | — |  |
| `orientation` | No | — |  |
| `justification` | No | `"BOTTOM_LEFT"` |  |

## SchdocAddPowerPortArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — | Input Altium document path, relative to the MCO file directory. |
| `output_file` | No | — | Optional output document; otherwise overwrite=true is required. |
| `overwrite` | No | `false` | Allow overwriting the input or existing output document. |
| `text` | Yes | — |  |
| `location_mils` | Yes | — |  |
| `style` | No | `"BAR"` |  |
| `orientation` | No | — |  |
| `show_net_name` | No | `true` |  |

## SchdocAddWireArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — | Input Altium document path, relative to the MCO file directory. |
| `output_file` | No | — | Optional output document; otherwise overwrite=true is required. |
| `overwrite` | No | `false` | Allow overwriting the input or existing output document. |
| `points_mils` | Yes | — |  |

## SchdocCreateArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `template` | No | — |  |
| `sheet_style` | No | `"D"` |  |
| `apply_template_visual_sheet_settings` | No | `false` |  |
| `custom_sheet_mils` | No | — |  |
| `overwrite` | No | `false` |  |

## SchlibAddSymbolArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `name` | Yes | — |  |
| `description` | No | `""` |  |

## SchlibCreateArgs

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — |  |
| `overwrite` | No | `false` |  |

## RecordString

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## BoundsObject

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `left` | Yes | — |  |
| `bottom` | Yes | — |  |
| `right` | Yes | — |  |
| `top` | Yes | — |  |

## RigidLayerStack

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `mode` | No | — | Layer-stack generation mode. Omission or null uses generated_rigid. |
| `name` | No | — |  |
| `copper_layers` | Yes | — | Copper layers in top-to-bottom order. |
| `dielectrics_between` | Yes | — | Dielectric layers between adjacent copper layers. |

## BoardOutlineMils

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `left` | Yes | — |  |
| `bottom` | Yes | — |  |
| `right` | Yes | — |  |
| `top` | Yes | — |  |

## OriginMils

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `x` | Yes | — |  |
| `y` | Yes | — |  |

## SheetFrameMils

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `x` | Yes | — |  |
| `y` | Yes | — |  |
| `width` | Yes | — |  |
| `height` | Yes | — |  |

## McoMechanicalLayer

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `layer` | Yes | — |  |
| `name` | No | — |  |
| `enabled` | No | `true` |  |

## McoMechanicalPair

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `layer_1` | Yes | — |  |
| `layer_2` | Yes | — |  |
| `pair_index` | No | — | Defaults to the row's zero-based source index. |

## McoMechanicalKind

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `layer` | Yes | — |  |
| `kind` | Yes | — |  |

## LayerStepHighlight

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `id` | Yes | — |  |
| `name` | No | — |  |
| `color` | Yes | — |  |
| `pad_geometries` | No | — | Geometry records consumed by the existing STEP exporter; non-object entries are ignored. |
| `z_offset_mm` | No | `0.001` |  |
| `thickness_mm` | No | `0.01` |  |

## SchematicTextStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `position_mils` | No | — |  |
| `font_name` | No | `"Arial"` |  |
| `font_size` | No | `12` |  |
| `bold` | No | — | Default is true for designator style and false for comment style. |
| `justification` | No | — |  |
| `hidden` | No | — | Explicit hidden takes precedence over visible. |
| `visible` | No | — |  |

## CustomSheetMils

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `width` | Yes | — | Custom sheet width in mils. |
| `height` | Yes | — | Custom sheet height in mils. |

## CopperLayer

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `name` | Yes | — | Copper layer display name. |
| `copper_thickness_mils` | No | — | Copper thickness in mils. |
| `thickness_mils` | No | — | Historical extension field; ignored by creation. Use copper_thickness_mils. |
| `component_placement` | No | — | Optional native component-placement enum id. |
| `copper_orientation` | No | — | Optional native copper-orientation enum id. |

## DielectricLayer

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `name` | Yes | — |  |
| `material` | Yes | — |  |
| `thickness_mils` | Yes | — |  |
| `dielectric_constant` | Yes | — |  |
| `dk` | No | — | Historical extension field; ignored by creation. Use dielectric_constant. |
| `dielectric_type` | No | — |  |
| `type_code` | No | — | Historical extension field; ignored by creation. Use dielectric_type. |
| `loss_tangent` | No | — |  |
