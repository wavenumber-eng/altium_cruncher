# BOM / PnP configuration fields

Generated from src/tsp/altium_cruncher/config/bom-pnp-config.tsp. Do not edit.

Required paths/sections are checked at loading. Defaults describe generated templates or adapter fallbacks; codecs do not insert them.

Path resolution, normalization and native CAD semantics remain Python adapter behavior.

## BomPnpConfigInput

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | No | `"altium_cruncher.bom.config.a0"` |  |
| `field_aliases` | No | — |  |
| `variants` | No | — |  |
| `bom` | No | — |  |
| `pnp` | No | — |  |
| `output` | No | — |  |

## BomPnpConfigInputFieldAliases

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## BomPnpConfigInputVariants

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `mode` | No | `"all"` |  |
| `names` | No | — |  |
| `include_base` | No | `true` |  |

## BomPnpConfigInputBom

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `source_mode` | No | `"schematic"` |  |
| `outputs` | No | — |  |
| `group_fields` | No | — |  |
| `output_fields` | No | — |  |
| `include_dnp` | No | `true` |  |
| `split_dnp` | No | `true` |  |
| `dnp_placement` | No | `"inline"` |  |
| `highlight_dnp_rows` | No | `true` |  |
| `prefix_order` | No | — |  |
| `pcb_line_item` | No | — |  |

## BomPnpConfigInputPnp

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `outputs` | No | — |  |
| `output_fields` | No | — |  |
| `units` | No | `"mm"` |  |
| `position_mode` | No | `"altium-pick-place"` |  |
| `exclude_no_bom` | No | `false` |  |
| `layer_order` | No | — |  |
| `prefix_order` | No | — |  |

## BomPnpConfigInputOutput

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `dir_template` | No | `"{Command}"` |  |
| `name_template` | No | `"{SourceStem}_{VariantName}{OutputKindSuffix}"` |  |

## RecordArrayString

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## BomPnpConfigInputBomPcbLineItem

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | `false` |  |
| `designator` | No | `"PCB"` |  |
| `fields` | No | — |  |

## BomPnpConfigInputBomPcbLineItemFields

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## RecordString

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
