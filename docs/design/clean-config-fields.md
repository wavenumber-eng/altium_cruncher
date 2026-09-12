# Clean configuration fields

Generated from src/tsp/altium_cruncher/config/clean-config.tsp. Do not edit.

Required paths/sections are checked at loading. Defaults describe generated templates or adapter fallbacks; codecs do not insert them.

Path resolution, normalization and native CAD semantics remain Python adapter behavior.

## SchematicCleanConfig

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | No | — |  |
| `normalize_pin_fonts` | No | — |  |
| `normalize_symbol_body_rectangles` | No | — |  |
| `normalize_power_symbols` | No | — |  |
| `normalize_net_labels` | No | — |  |
| `normalize_component_designators` | No | — |  |
| `normalize_component_parameters` | No | — |  |
| `normalize_component_free_text` | No | — |  |
| `normalize_wires` | No | — |  |
| `normalize_no_erc` | No | — |  |
| `normalize_sheet_style` | No | — |  |
| `normalize_symbol_internal_graphics_monochrome` | No | — |  |

## PcblibCleanConfig

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | No | — |  |
| `profile` | No | — |  |
| `remove_mechanical_primitives` | No | — |  |
| `remove_text_strings` | No | — |  |
| `remove_regions` | No | — |  |

## PinFonts

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | — |  |
| `name_font` | No | — |  |
| `name` | No | — |  |
| `designator_font` | No | — |  |
| `designator` | No | — |  |

## SymbolBodyRectangles

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | — |  |
| `min_width_mils` | No | — |  |
| `min_height_mils` | No | — |  |
| `outline_color_win32` | No | — |  |
| `outline_color` | No | — |  |
| `color` | No | — |  |
| `line_width` | No | — |  |
| `fill_color_win32` | No | — |  |
| `fill_color` | No | — |  |
| `area_color` | No | — |  |
| `is_solid` | No | — |  |
| `transparent` | No | — |  |

## FontAndColorRule

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | — |  |
| `color_win32` | No | — |  |
| `color` | No | — |  |
| `font_name` | No | — |  |
| `size_pt` | No | — |  |
| `bold` | No | — |  |
| `italic` | No | — |  |
| `font` | No | — |  |

## ComponentFontRule

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | — |  |
| `font` | No | — |  |

## ComponentFreeText

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | — |  |
| `font_name` | No | — |  |
| `font` | No | — |  |
| `color_win32` | No | — |  |
| `color` | No | — |  |

## ColorRule

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | — |  |
| `color_win32` | No | — |  |
| `color` | No | — |  |

## NoErcRule

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | — |  |
| `color_win32` | No | — |  |
| `color` | No | — |  |
| `symbol` | No | — |  |
| `style` | No | — |  |

## SheetStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | — |  |
| `line_color_win32` | No | — |  |
| `line_color` | No | — |  |
| `color` | No | — |  |
| `area_color_win32` | No | — |  |
| `area_color` | No | — |  |
| `document_font` | No | — |  |
| `font` | No | — |  |

## InternalGraphics

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | — |  |
| `saturation` | No | — |  |

## PcblibMechanicalPrimitives

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | — |  |
| `primitive_types` | No | — |  |
| `layers` | No | — | Layer name filters. Accepts legacy PcbLayer names, display names such as 'Mechanical 17', and V7 semantic tokens such as 'MECHANICAL17' when the installed altium-monkey exposes the V7-aware layer API; token and display forms match the same layer. |
| `preserve_regions` | No | — |  |
| `preserve_component_bodies` | No | — |  |

## PcblibTextStrings

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | — |  |
| `layers` | No | — | Layer name filters. Accepts legacy PcbLayer names, display names such as 'Mechanical 17', and V7 semantic tokens such as 'MECHANICAL17' when the installed altium-monkey exposes the V7-aware layer API; token and display forms match the same layer. |
| `match` | No | — |  |
| `patterns` | No | — |  |

## PcblibRegions

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | — |  |
| `layers` | No | — | Layer name filters. Accepts legacy PcbLayer names, display names such as 'Mechanical 17', and V7 semantic tokens such as 'MECHANICAL17' when the installed altium-monkey exposes the V7-aware layer API; token and display forms match the same layer. |
| `preserve_component_linked` | No | — |  |
| `preserve_model_associated` | No | — |  |
| `preserve_keepouts` | No | — |  |
| `preserve_board_cutouts` | No | — |  |
| `preserve_custom_pad_regions` | No | — |  |

## FontSpec

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `font_name` | No | — |  |
| `font` | No | — |  |
| `size_pt` | No | — |  |
| `size` | No | — |  |
| `bold` | No | — |  |
| `italic` | No | — |  |
| `color_win32` | No | — |  |
| `color` | No | — |  |
