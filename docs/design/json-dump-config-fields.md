# Document JSON dump output fields

Generated from src/tsp/altium_cruncher/outputs/json-dump.tsp. Do not edit.

Wire fields emitted by Cruncher. Validation preserves the payload without inserting defaults.

See the contract authority inventory for producer locations and delegated upstream data boundaries.

## SchdocDump

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — |  |
| `kind` | Yes | — |  |
| `document` | Yes | — |  |

## SchlibDump

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — |  |
| `kind` | Yes | — |  |
| `document` | Yes | — |  |

## PcbdocDump

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — |  |
| `kind` | Yes | — |  |
| `document` | Yes | — |  |

## PcblibDump

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — |  |
| `kind` | Yes | — |  |
| `document` | Yes | — |  |

## SchDoc

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `format` | Yes | — |  |

## SchLib

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `format` | Yes | — |  |

## PcbDoc

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `pads` | Yes | — |  |
| `vias` | Yes | — |  |
| `tracks` | Yes | — |  |
| `arcs` | Yes | — |  |
| `texts` | Yes | — |  |
| `fills` | Yes | — |  |
| `regions` | Yes | — |  |
| `shapebased_regions` | Yes | — |  |
| `component_bodies` | Yes | — |  |
| `models` | Yes | — |  |
| `format` | Yes | — |  |
| `counts` | Yes | — |  |
| `raw_streams` | Yes | — |  |
| `board` | Yes | — |  |
| `union_name_records` | Yes | — |  |
| `smart_unions` | Yes | — |  |
| `user_unions` | Yes | — |  |
| `components` | Yes | — |  |
| `nets` | Yes | — |  |
| `net_classes` | Yes | — |  |
| `differential_pairs` | Yes | — |  |
| `polygons` | Yes | — |  |
| `rules` | Yes | — |  |
| `dimensions` | Yes | — |  |
| `extended_primitive_information` | Yes | — |  |
| `custom_shapes` | Yes | — |  |
| `via_structures` | Yes | — |  |
| `via_structure_links` | Yes | — |  |
| `board_regions` | Yes | — |  |
| `shapebased_component_bodies` | Yes | — |  |
| `embedded_fonts` | Yes | — |  |
| `embedded_models` | Yes | — |  |

## PcbLib

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `format` | Yes | — |  |
| `footprint_count` | Yes | — |  |
| `footprints` | Yes | — |  |
| `models_3d` | Yes | — |  |
| `raw_streams` | Yes | — |  |

## RecordUnknown

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## RecordCount

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## RawStream

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `name` | Yes | — |  |
| `byte_count` | Yes | — |  |
| `sha256` | Yes | — |  |

## UserUnion

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `union_index` | Yes | — |  |
| `name` | Yes | — |  |
| `member_count` | Yes | — |  |
| `members` | Yes | — |  |

## UnionError

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `error` | Yes | — |  |

## Footprint

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `pads` | Yes | — |  |
| `vias` | Yes | — |  |
| `tracks` | Yes | — |  |
| `arcs` | Yes | — |  |
| `texts` | Yes | — |  |
| `fills` | Yes | — |  |
| `regions` | Yes | — |  |
| `shapebased_regions` | Yes | — |  |
| `component_bodies` | Yes | — |  |
| `models` | Yes | — |  |
| `name` | Yes | — |  |
| `counts` | Yes | — |  |

## UnionMember

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `collection` | Yes | — |  |
| `object_index` | Yes | — |  |
| `union_index` | Yes | — |  |
| `object_summary` | Yes | — |  |

## MemberSummary

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `class` | No | — |  |
| `designator` | No | — |  |
| `name` | No | — |  |
| `text_content` | No | — |  |
| `footprint` | No | — |  |
| `comment` | No | — |  |
| `x_mils` | No | — |  |
| `y_mils` | No | — |  |
| `start_x_mils` | No | — |  |
| `start_y_mils` | No | — |  |
| `end_x_mils` | No | — |  |
| `end_y_mils` | No | — |  |
| `center_x_mils` | No | — |  |
| `center_y_mils` | No | — |  |
