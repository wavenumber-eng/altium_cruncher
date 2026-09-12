# Project skeleton configuration fields

Generated from src/tsp/altium_cruncher/config/creation.tsp. Do not edit.

Required paths/sections are checked at loading. Defaults describe generated templates or adapter fallbacks; codecs do not insert them.

Path resolution, normalization and native CAD semantics remain Python adapter behavior.

## ProjectSkeletonConfigInput

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — | Project skeleton config contract id. |
| `project` | Yes | — | PrjPcb output and project-level parameters. |
| `schematics` | Yes | — | SchDoc sheets to create and add to the project. Empty creates no sheets. |
| `pcb` | No | — | Optional PcbDoc output; null creates no board. |

## ProjectOutput

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — | PrjPcb file to create, relative to this config file unless absolute. |
| `name` | No | — | Project display name; omission, null or empty derives it from the file. |
| `parameters` | No | — | Project parameters; the Python adapter converts authored values to strings. |

## SchdocChild

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — | SchDoc file to create, relative to this config file unless absolute. |
| `sheet_style` | No | `"D"` | Altium SheetStyle enum name or native integer id. Falsy input uses D. |
| `template` | No | — | Optional SchDot template file to copy settings from. |
| `apply_template_visual_sheet_settings` | No | `false` | Whether to copy visual sheet settings from the template; legacy JSON truthiness is preserved. Prefer true or false. |
| `custom_sheet_mils` | No | — | Optional explicit sheet size in mils. |

## PcbdocChild

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `file` | Yes | — | PcbDoc file to create, relative to this config file unless absolute. |
| `board_outline_mils` | No | — | Optional rectangular board outline in mils. |
| `layer_stack` | No | — | Generated rigid stack; use only one layer-stack input. |
| `layer_stack_template` | No | `"2-layer"` | Named layer-stack template; defaults to 2-layer when no stack input is supplied. |
| `stackupx_file` | No | — | Optional .stackupx path to import as the PcbDoc layer-stack document. |
| `mechanical_layer_profile` | No | `"none"` | Optional profile; case, surrounding whitespace and hyphen aliases are accepted. |
| `mechanical_layers` | No | — |  |
| `mechanical_layer_pairs` | No | — |  |
| `mechanical_layer_kinds` | No | — |  |

## RecordUnknown

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## CustomSheetMils

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `width` | Yes | — | Custom sheet width in mils. |
| `height` | Yes | — | Custom sheet height in mils. |

## BoardOutlineMils

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `left` | Yes | `0` |  |
| `bottom` | Yes | `0` |  |
| `right` | Yes | `3000` |  |
| `top` | Yes | `2000` |  |

## RigidLayerStack

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `mode` | No | `"generated_rigid"` | Layer-stack generation mode. Omission or null uses generated_rigid. |
| `name` | No | — |  |
| `copper_layers` | Yes | — | Copper layers in top-to-bottom order. |
| `dielectrics_between` | Yes | — | Dielectric layers between adjacent copper layers. |

## MechanicalLayer

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `layer` | Yes | — |  |
| `name` | No | — |  |
| `enabled` | No | — |  |
| `kind` | No | — |  |

## GroupedMechanicalPair

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `top` | Yes | — |  |
| `bottom` | Yes | — |  |

## FlatMechanicalPair

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `layer_1` | Yes | — |  |
| `layer_2` | Yes | — |  |
| `pair_index` | No | — |  |
| `top` | No | — |  |
| `bottom` | No | — |  |

## MechanicalKind

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `layer` | Yes | — |  |
| `kind` | Yes | — |  |

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

## MechanicalPairSide

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `layer` | Yes | — |  |
| `name` | No | — |  |
| `enabled` | No | — |  |
| `kind` | Yes | — |  |
