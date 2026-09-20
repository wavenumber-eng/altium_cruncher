# PCB SVG / Toon configuration fields

Generated from src/tsp/altium_cruncher/config/pcb-svg.tsp. Do not edit.

Authored overrides stay partial. Defaults are annotations, not values inserted when reading a file.

The CLI applies presets, config overrides and explicit command choices afterward.

## PcbSvgConfigInput

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | No | `"pcb.svg.config.a1"` | PCB SVG config contract id. pcb.svg.config.a0 remains accepted as the additive predecessor. |
| `global` | No | — | Global settings applied to layer outputs and composed views. |
| `assembly` | No | — | Assembly projection defaults for component virtual layers. |
| `dnp` | No | — | DNP marker style. |
| `diodes` | No | — | Diode/cathode marker detection policy. |
| `pin1` | No | — | Pin-1 marker detection and display policy. |
| `components` | No | — | Per-designator overrides keyed by component designator. |
| `layer_outputs` | No | — | Config-driven physical layer SVG output policy. |
| `views` | No | — | Explicit composed SVG views. Each item has its own draw-order layer list. |

## GlobalOptions

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `pcbdoc` | No | `null` | Optional PcbDoc selector when a PrjPcb contains multiple boards. |
| `canvas` | No | — | SVG viewBox normalization policy. |
| `include_metadata` | No | `true` | Include Altium/source metadata in SVG data attributes. |
| `show_empty_layers` | No | `false` | Emit empty physical layers when no primitives are present. |
| `clip_to_outline` | No | `true` | Clip rendered geometry to the board outline. |
| `clip_holes_from_copper` | No | `true` | Clip drills and slots out of copper layers. |
| `mirror_bottom_view` | No | `true` | Mirror bottom-side views into assembly-view orientation. |
| `svg_scale` | No | `10` | Multiplier for SVG width and height attributes. |
| `svg_size_unit` | No | `""` | Optional SVG size unit suffix, such as mm or px. |
| `clean_output` | No | `false` | Reserved cleanup flag for generated output directories. |
| `styles` | No | — | Default style table for physical and synthetic layers. |

## AssemblyOptions

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `default_projection` | No | `"detail"` | Projection mode for fitted components. Options: bounding_box, detail, none, outline, simple. |
| `dnp_projection` | No | `"bounding_box"` | Projection mode for DNP components. Options: bounding_box, detail, none, outline, simple. |
| `designator_color` | No | `"#FF0000"` | Text color for fitted component designators. |
| `dnp_designator_color` | No | `"#FF0000"` | Text color for DNP component designators. |

## DnpOptions

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `color` | No | `"#FF0000"` | SVG color value, usually #RRGGBB. |
| `hatch` | No | `true` | Enable hatch fill for this layer/style. |
| `hatch_spacing_mm` | No | `1.5` | Hatch spacing in millimeters. |
| `hatch_angle_deg` | No | `45` | Hatch angle in degrees. |
| `hatch_line_width_mm` | No | `0.08` | Hatch stroke width in millimeters. |

## DiodeOptions

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | `true` | Enable diode/cathode marker detection. |
| `line_art` | No | `true` | Draw diode line art when possible. |
| `marker_color` | No | `"#FF0000"` | Cathode marker color. |
| `numeric_cathode_pad` | No | `"2"` | Default numeric cathode pad designator. |
| `cathode_pad_names` | No | — | Pad names treated as cathode pads. |
| `designator_prefixes` | No | — | Designator prefixes treated as diode-like parts. |
| `parameter_terms` | No | — | Parameter text terms treated as diode-like parts. |

## Pin1Options

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `exclude_designator_prefixes` | No | — | Component designator prefixes excluded from automatic pin-1 markers. |

## RecordComponentOverride

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## LayerOutputOptions

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | `true` | Enable individual physical layer SVG outputs. |
| `layers` | No | `"auto"` | Either 'auto' or a list of PCB layer names: legacy PcbLayer names, display names, or V7 semantic tokens such as 'MECHANICAL33' and 'MID31' when the installed altium-monkey exposes the V7-aware layer API. |
| `include_special_layers` | No | — | Synthetic layers also emitted with layer outputs. Options: BOARD_SUBSTRATE, BOARD_OUTLINE, BOARD_CUTOUTS, DRILLS, SLOTS, BEND_LINES, ASSEMBLY_HLR_TOP, ASSEMBLY_HLR_BOTTOM, ASSEMBLY_DESIGNATORS_TOP, ASSEMBLY_DESIGNATORS_BOTTOM, PIN1_TOP, PIN1_BOTTOM, SOLDERMASK_FILM_TOP, SOLDERMASK_FILM_BOTTOM, SURFACE_COPPER_TOP, SURFACE_COPPER_BOTTOM, ILLUSTRATION_TOP, and ILLUSTRATION_BOTTOM. |
| `output_dir` | No | `"layers"` | Output directory for physical layer SVG files. |

## ViewOptions

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `name` | Yes | — |  |
| `enabled` | No | `true` | Enable this rendering rule. |
| `group_id` | No | `null` |  |
| `output_svg` | No | `null` |  |
| `layers` | No | — | PCB layer names for this view: legacy PcbLayer names, display names, or V7 semantic tokens such as 'MECHANICAL33' and 'MID31' when the installed altium-monkey exposes the V7-aware layer API. |
| `mirror` | No | `null` |  |
| `assembly_hlr_mode` | No | `"detail"` |  |
| `styles` | No | — |  |
| `description` | No | `null` |  |

## RecordUnknown

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## CanvasOptions

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `bounds` | No | `"board_outline"` | Canvas bounds mode. Options: all_geometry, board_outline. |
| `margin_mm` | No | `1` | Canvas margin added around the chosen bounds. |

## StyleTable

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `illustration` | No | — |  |
| `assembly_designators` | No | — | Autodoc silhouette fitting; model-less parts use electrical pads first (including flagged testpoints), with mechanical holes as a fallback. |
| `board_substrate` | No | — | Bare PCB fill, clipped to the outline with physical bores and scoped cutouts removed. Place BOARD_SUBSTRATE before copper and film. Applies globally or per view. |
| `soldermask_film` | No | — | Board-clipped inverse solder mask using saved pad/via expansions. Applies globally or per view. |
| `bend_lines` | No | — | Flat, region-clipped rigid-flex bend-line annotations. This does not fold or deform the board. |
| `assembly_hlr` | No | — |  |
| `board_outline` | No | — |  |
| `board_cutouts` | No | — |  |
| `drills` | No | — |  |
| `slots` | No | — |  |
| `copper_traces` | No | — |  |
| `vias` | No | — |  |
| `copper_polygons` | No | — |  |
| `smd_pads` | No | — |  |
| `through_hole_pads` | No | — |  |
| `silkscreen_component_graphics` | No | — |  |
| `silkscreen_designators` | No | — |  |
| `silkscreen_board_graphics` | No | — |  |
| `silkscreen_surface` | No | — |  |
| `pin1_marker` | No | — |  |
| `keepout` | No | — |  |

## ComponentOverride

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `side` | No | `null` |  |
| `projection` | No | `null` |  |
| `assembly_hlr` | No | — |  |
| `pin1_enabled` | No | `null` |  |
| `pin1_pad` | No | `null` |  |
| `cathode_pad` | No | `null` |  |
| `diode` | No | `null` |  |
| `diode_line_art` | No | `null` |  |
| `show_designator` | No | `null` |  |

## IllustrationStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | `true` | Enable this rendering rule. |
| `line_width_mm` | No | `0.025` | Stroke width in millimeters. |
| `opacity` | No | `1` | Layer opacity from 0.0 to 1.0. |

## AssemblyDesignatorsStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | `true` | Enable this rendering rule. |
| `color` | No | — | SVG color value, usually #RRGGBB. |
| `stroke_color` | No | `"#FFFFFF"` | Text outline CSS color, drawn behind the fill. |
| `stroke_width_mm` | No | `0` | Full SVG stroke width in board millimetres. Zero disables the outline; fitting and placement are unchanged. |
| `fill_ratio` | No | `0.8` |  |
| `max_font_size_mm` | No | `2.5` |  |
| `opacity` | No | `1` | Layer opacity from 0.0 to 1.0. |

## BoardSubstrateStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | `true` | Enable this rendering rule. |
| `color` | No | `"auto"` | Global substrate CSS color override, or auto (default) for region-local authored/saved/palette resolution. |
| `rigid_color` | No | `"#B6A26B"` | Rigid-substrate fallback CSS color used when color=auto and no authored or saved board-core color is available. |
| `flex_color` | No | `"#D18B28"` | Flex-substrate fallback CSS color used when color=auto and no authored material color is available. |

## SoldermaskFilmStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | `true` | Enable this rendering rule. |
| `color` | No | `"auto"` | Global film CSS color override, or auto (default) for region-local authored material, saved Altium 3D solder-mask color, and configured surface-class fallback resolution. |
| `coverlay_color` | No | `"#D18B28"` | Coverlay fallback CSS color used when color=auto and the authored coverlay material has no color. |
| `opacity` | No | `1` | Layer opacity from 0.0 to 1.0. |

## BendLinesStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | `true` | Enable flat board bend-line annotations. |
| `color` | No | `"#D97706"` | SVG color for bend-line annotations. |
| `opacity` | No | `0.8` | Layer opacity from 0.0 to 1.0. |
| `line_width_mm` | No | `0.15` | Stroke width in millimeters. |
| `line_style` | No | `"dashed"` | Bend-line stroke style. Options: solid, dashed. |
| `dash_length_mm` | No | `0.5` | Dash and gap length in millimeters when line_style is dashed. |
| `dash_gap_mm` | No | `0.3` | Gap between dashes in millimeters when line_style is dashed. |
| `extension_mm` | No | `1` | Absolute distance each end extends beyond the owning-region chord, in millimeters. Zero stops at the region boundary. |

## AssemblyHlrStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `projection_algorithm` | No | — |  |
| `outline_algorithm` | No | — |  |
| `fast` | No | — | Geometer Fast candidate, tolerance and limit options. Legacy include/edge controls require an explicit poly/exact backend. |
| `enabled` | No | `true` | Enable this rendering rule. |
| `color` | No | `"#F59E0B"` | SVG color value, usually #RRGGBB. |
| `line_width_mm` | No | `0.12` | Stroke width in millimeters. |
| `curve_mode` | No | `"native_arcs"` | Legacy HLR curve serialization mode; Fast always emits polylines. Options: native_arcs, polyline. |
| `samples_per_curve` | No | `24` | Polyline sample count when curves are sampled. |
| `round_digits` | No | `3` | Decimal places retained in generated SVG path coordinates. |
| `include_visible` | No | `true` | Legacy poly/exact visible-edge control; leave true for Fast. |
| `include_outline` | No | `true` | Legacy poly/exact silhouette control; leave true for Fast. |
| `union_polygons` | No | `true` | Union projected polygons before converting to SVG paths. |

## BoardOutlineStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | `true` | Enable this rendering rule. |
| `color` | No | `"#000000"` | SVG color value, usually #RRGGBB. |
| `line_width_mm` | No | `0.1` | Stroke width in millimeters. |

## BoardCutoutsStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | `true` | Enable this rendering rule. |
| `scope` | No | `"all"` | Cutouts used by board clipping, film and cutout artwork. Interior uses the existing Mate containment filter to exclude touching/outside contours. |
| `outline_opacity` | No | `1` | Cutout outline opacity from 0.0 to 1.0. |
| `hatch_color` | No | — | Hatch color; omitted uses the cutout outline color. |
| `hatch_opacity` | No | `0.55` | Hatch opacity from 0.0 to 1.0, independent of the outline. |
| `label` | No | `""` | Cutout label text; an empty string disables labels. |
| `label_color` | No | — | Label color; omitted uses the cutout outline color. |
| `label_opacity` | No | `1` | Cutout label opacity from 0.0 to 1.0. |
| `label_max_font_size_mm` | No | `3` | Maximum fitted cutout label font size in millimeters. |
| `label_fill_ratio` | No | `0.72` | Fraction of cutout width/height available to the fitted label (0 to 1). |
| `label_rotation_min_gain` | No | `0.25` | Vertical cutout text must fit this fraction larger than horizontal after the size cap. |
| `color` | No | `"#FF0000"` | SVG color value, usually #RRGGBB. |
| `hatch` | No | `true` | Enable hatch fill for this layer/style. |
| `hatch_spacing_mm` | No | `2` | Hatch spacing in millimeters. |
| `hatch_angle_deg` | No | `45` | Hatch angle in degrees. |
| `hatch_line_width_mm` | No | `0.08` | Hatch stroke width in millimeters. |
| `outline_style` | No | `"solid"` | Outline stroke style. Options: solid, dashed. |
| `outline_dash_mm` | No | `1.5` | Dash length in millimeters when outline_style is dashed. |
| `outline_width_mm` | No | `0.15` | Outline stroke width in millimeters. |

## HoleStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | `true` | Enable this rendering rule. |
| `plated_color` | No | `"#90EE90"` | SVG color for plated drill/slot features. |
| `non_plated_color` | No | `"#ADD8E6"` | SVG color for non-plated drill/slot features. |
| `outline` | No | `false` | Draw drill/slot boundaries with unfilled centers instead of filled marks. |
| `outline_width_mm` | No | `0.1` | Outline stroke width in millimeters. |
| `respect_tenting` | No | `false` | Hide plated drill/slot marks covered by solder mask on the rendered side. |
| `opacity` | No | `1` | Layer opacity from 0.0 to 1.0. |

## CopperTracesStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | `true` | Enable this rendering rule. |
| `color` | No | `"#000000"` | SVG color value, usually #RRGGBB. |

## ViasStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | `true` | Enable this rendering rule. |
| `color` | No | `"#000000"` | SVG color value, usually #RRGGBB. |

## CopperPolygonsStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | `true` | Enable this rendering rule. |
| `color` | No | `"#888888"` | SVG color value, usually #RRGGBB. |

## SmdPadsStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | `true` | Enable this rendering rule. |
| `color` | No | `"#000000"` | SVG color value, usually #RRGGBB. |

## ThroughHolePadsStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | `true` | Enable this rendering rule. |
| `color` | No | `"#000000"` | SVG color value, usually #RRGGBB. |

## SilkscreenComponentGraphicsStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | `true` | Enable this rendering rule. |
| `color` | No | `"#000000"` | SVG color value, usually #RRGGBB. |

## SilkscreenDesignatorsStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | `true` | Enable this rendering rule. |
| `color` | No | `"#000000"` | SVG color value, usually #RRGGBB. |

## SilkscreenBoardGraphicsStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | `true` | Enable this rendering rule. |
| `color` | No | `"#000000"` | SVG color value, usually #RRGGBB. |

## SilkscreenSurfaceStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `clip_mode` | No | `"none"` | Silkscreen clipping domain. none preserves authored overlay; board clips to board material and physical holes; film clips to the resolved solder-mask/coverlay film after apertures. |

## Pin1MarkerStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | `true` | Enable this rendering rule. |
| `color` | No | `"#2563EB"` | SVG color value, usually #RRGGBB. |
| `dot_diameter_mm` | No | `0.55` | Pin-1 marker dot diameter in millimeters. |
| `min_dot_diameter_mm` | No | `0.25` | Minimum pin-1 marker dot diameter in millimeters. |

## KeepoutStyle

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `enabled` | No | `true` | Enable this rendering rule. |
| `color` | No | `"#CC00CC"` | SVG color value, usually #RRGGBB. |

## RecordStyleObject

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## FastHlrOptions

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `include_hidden` | No | — |  |
| `include_boundaries` | No | — |  |
| `include_creases` | No | — |  |
| `include_silhouettes` | No | — |  |
| `suppress_coplanar_seams` | No | — |  |

## StyleObject

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
