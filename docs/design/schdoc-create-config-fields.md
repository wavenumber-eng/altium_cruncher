# SchDoc creation configuration fields

Generated from src/tsp/altium_cruncher/config/creation.tsp. Do not edit.

Required paths/sections are checked at loading. Defaults describe generated templates or adapter fallbacks; codecs do not insert them.

Path resolution, normalization and native CAD semantics remain Python adapter behavior.

## SchdocCreateConfigInput

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — | SchDoc create config contract id. |
| `file` | Yes | — | SchDoc file to create, relative to this config file unless absolute. |
| `sheet_style` | No | `"D"` | Altium SheetStyle enum name or native integer id. Falsy input uses D. |
| `template` | No | — | Optional SchDot template file to copy settings from. |
| `apply_template_visual_sheet_settings` | No | `false` | Whether to copy visual sheet settings from the template; legacy JSON truthiness is preserved. Prefer true or false. |
| `custom_sheet_mils` | No | — | Optional explicit sheet size in mils. |

## RecordUnknown

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## CustomSheetMils

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `width` | Yes | — | Custom sheet width in mils. |
| `height` | Yes | — | Custom sheet height in mils. |
