import "@typespec/json-schema";
import "./defaults.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Config;

@extension("additionalProperties", true)
model StyleObject {}

alias SyntheticLayer =
  | "BOARD_SUBSTRATE"
  | "BOARD_OUTLINE"
  | "BOARD_CUTOUTS"
  | "DRILLS"
  | "SLOTS"
  | "ASSEMBLY_HLR_TOP"
  | "ASSEMBLY_HLR_BOTTOM"
  | "ASSEMBLY_DESIGNATORS_TOP"
  | "ASSEMBLY_DESIGNATORS_BOTTOM"
  | "PIN1_TOP"
  | "PIN1_BOTTOM"
  | "SOLDERMASK_FILM_TOP"
  | "SOLDERMASK_FILM_BOTTOM"
  | "SURFACE_COPPER_TOP"
  | "SURFACE_COPPER_BOTTOM"
  | "BEND_LINES"
  | "ILLUSTRATION_TOP"
  | "ILLUSTRATION_BOTTOM";

alias ProjectionMode =
  | "detail"
  | "outline"
  | "simple"
  | "bounding_box"
  | "none"
  | "silhouette"
  | "profile"
  | "bounding-box"
  | "bbox"
  | "box"
  | "bounds"
  | "off"
  | "disabled";

model ComponentOverride {
  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "enum")
  side?:
    | "top"
    | "bottom"
    | "toplayer"
    | "bottomlayer"
    | "top_layer"
    | "bottom_layer"
    | "top-layer"
    | "bottom-layer"
    | null;

  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "enum")
  `projection`?: ProjectionMode | null;

  assembly_hlr?: AssemblyHlrStyle | null;

  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "boolean")
  pin1_enabled?: boolean | null;

  pin1_pad?: string | null;
  cathode_pad?: string | null;

  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "boolean")
  diode?: boolean | null;

  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "boolean")
  diode_line_art?: boolean | null;

  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "boolean")
  show_designator?: boolean | null;
}

model IllustrationStyle extends Record<unknown> {
  @doc("Enable this rendering rule.")
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @doc("Stroke width in millimeters.")
  @minValueExclusive(0)
  @extension("x-acr-input", "number")
  line_width_mm?: float64;

  @doc("Layer opacity from 0.0 to 1.0.")
  @minValue(0)
  @maxValue(1)
  @extension("x-acr-input", "number")
  opacity?: float64;
}

model AssemblyDesignatorsStyle extends Record<unknown> {
  @doc("Enable this rendering rule.")
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @doc("SVG color value, usually #RRGGBB.")
  color?: string;

  @doc("Text outline CSS color, drawn behind the fill.")
  stroke_color?: string;

  @doc("Full SVG stroke width in board millimetres. Zero disables the outline; fitting and placement are unchanged.")
  @minValue(0)
  @extension("x-acr-input", "number")
  stroke_width_mm?: float64;

  @maxValue(1)
  @minValueExclusive(0)
  @extension("x-acr-input", "number")
  fill_ratio?: float64;

  @minValueExclusive(0)
  @extension("x-acr-input", "number")
  max_font_size_mm?: float64;

  @doc("Layer opacity from 0.0 to 1.0.")
  @minValue(0)
  @maxValue(1)
  @extension("x-acr-input", "number")
  opacity?: float64;
}

model BoardSubstrateStyle extends Record<unknown> {
  @doc("Enable this rendering rule.")
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @doc("Global substrate CSS color override, or auto (default) for region-local authored/saved/palette resolution.")
  color?: string;

  @doc("Rigid-substrate fallback CSS color used when color=auto and no authored or saved board-core color is available.")
  rigid_color?: string;

  @doc("Flex-substrate fallback CSS color used when color=auto and no authored material color is available.")
  flex_color?: string;
}

model SoldermaskFilmStyle extends Record<unknown> {
  @doc("Enable this rendering rule.")
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @doc("Global film CSS color override, or auto (default) for region-local authored material, saved Altium 3D solder-mask color, and configured surface-class fallback resolution.")
  color?: string;

  @doc("Coverlay fallback CSS color used when color=auto and the authored coverlay material has no color.")
  coverlay_color?: string;

  @doc("Layer opacity from 0.0 to 1.0.")
  @minValue(0)
  @maxValue(1)
  @extension("x-acr-input", "number")
  opacity?: float64;
}

model BendLinesStyle extends Record<unknown> {
  @doc("Enable flat board bend-line annotations.")
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @doc("SVG color for bend-line annotations.")
  color?: string;

  @doc("Layer opacity from 0.0 to 1.0.")
  @minValue(0)
  @maxValue(1)
  @extension("x-acr-input", "number")
  opacity?: float64;

  @doc("Stroke width in millimeters.")
  @minValueExclusive(0)
  @extension("x-acr-input", "number")
  line_width_mm?: float64;

  @doc("Bend-line stroke style. Options: solid, dashed.")
  @extension("x-acr-input", "enum")
  @extension("x-acr-trim", false)
  line_style?: "solid" | "dashed";

  @doc("Dash and gap length in millimeters when line_style is dashed.")
  @minValueExclusive(0)
  @extension("x-acr-input", "number")
  dash_length_mm?: float64;

  @doc("Gap between dashes in millimeters when line_style is dashed.")
  @minValueExclusive(0)
  @extension("x-acr-input", "number")
  dash_gap_mm?: float64;

  @doc("Absolute distance each end extends beyond the owning-region chord, in millimeters. Zero stops at the region boundary.")
  @minValue(0)
  @extension("x-acr-input", "number")
  extension_mm?: float64;
}

model BoardOutlineStyle extends Record<unknown> {
  @doc("Enable this rendering rule.")
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @doc("SVG color value, usually #RRGGBB.")
  color?: string;

  @doc("Stroke width in millimeters.")
  @minValueExclusive(0)
  @extension("x-acr-input", "number")
  line_width_mm?: float64;
}

model BoardCutoutsStyle extends Record<unknown> {
  @doc("Enable this rendering rule.")
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @doc("Cutouts used by board clipping, film and cutout artwork. Interior uses the existing Mate containment filter to exclude touching/outside contours.")
  scope?: "all" | "interior";

  @doc("Cutout outline opacity from 0.0 to 1.0.")
  @minValue(0)
  @maxValue(1)
  @extension("x-acr-input", "number")
  outline_opacity?: float64;

  @doc("Hatch color; omitted uses the cutout outline color.")
  hatch_color?: string;

  @doc("Hatch opacity from 0.0 to 1.0, independent of the outline.")
  @minValue(0)
  @maxValue(1)
  @extension("x-acr-input", "number")
  hatch_opacity?: float64;

  @doc("Cutout label text; an empty string disables labels.")
  label?: string;

  @doc("Label color; omitted uses the cutout outline color.")
  label_color?: string;

  @doc("Cutout label opacity from 0.0 to 1.0.")
  @minValue(0)
  @maxValue(1)
  @extension("x-acr-input", "number")
  label_opacity?: float64;

  @doc("Maximum fitted cutout label font size in millimeters.")
  @minValueExclusive(0)
  @extension("x-acr-input", "number")
  label_max_font_size_mm?: float64;

  @doc("Fraction of cutout width/height available to the fitted label (0 to 1).")
  @maxValue(1)
  @minValueExclusive(0)
  @extension("x-acr-input", "number")
  label_fill_ratio?: float64;

  @doc("Vertical cutout text must fit this fraction larger than horizontal after the size cap.")
  @minValue(0)
  @extension("x-acr-input", "number")
  label_rotation_min_gain?: float64;

  @doc("SVG color value, usually #RRGGBB.")
  color?: string;

  @doc("Enable hatch fill for this layer/style.")
  @extension("x-acr-input", "boolean")
  hatch?: boolean;

  @doc("Hatch spacing in millimeters.")
  @minValueExclusive(0)
  @extension("x-acr-input", "number")
  hatch_spacing_mm?: float64;

  @doc("Hatch angle in degrees.")
  @extension("x-acr-input", "number")
  hatch_angle_deg?: float64;

  @doc("Hatch stroke width in millimeters.")
  @minValueExclusive(0)
  @extension("x-acr-input", "number")
  hatch_line_width_mm?: float64;

  @doc("Outline stroke style. Options: solid, dashed.")
  @extension("x-acr-input", "enum")
  @extension("x-acr-trim", false)
  outline_style?: "solid" | "dashed";

  @doc("Dash length in millimeters when outline_style is dashed.")
  @minValueExclusive(0)
  @extension("x-acr-input", "number")
  outline_dash_mm?: float64;

  @doc("Outline stroke width in millimeters.")
  @minValueExclusive(0)
  @extension("x-acr-input", "number")
  outline_width_mm?: float64;
}

model CopperTracesStyle extends Record<unknown> {
  @doc("Enable this rendering rule.")
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @doc("SVG color value, usually #RRGGBB.")
  color?: string;
}

model ViasStyle extends Record<unknown> {
  @doc("Enable this rendering rule.")
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @doc("SVG color value, usually #RRGGBB.")
  color?: string;
}

model CopperPolygonsStyle extends Record<unknown> {
  @doc("Enable this rendering rule.")
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @doc("SVG color value, usually #RRGGBB.")
  color?: string;
}

model SmdPadsStyle extends Record<unknown> {
  @doc("Enable this rendering rule.")
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @doc("SVG color value, usually #RRGGBB.")
  color?: string;
}

model ThroughHolePadsStyle extends Record<unknown> {
  @doc("Enable this rendering rule.")
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @doc("SVG color value, usually #RRGGBB.")
  color?: string;
}

model SilkscreenComponentGraphicsStyle extends Record<unknown> {
  @doc("Enable this rendering rule.")
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @doc("SVG color value, usually #RRGGBB.")
  color?: string;
}

model SilkscreenDesignatorsStyle extends Record<unknown> {
  @doc("Enable this rendering rule.")
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @doc("SVG color value, usually #RRGGBB.")
  color?: string;
}

model SilkscreenBoardGraphicsStyle extends Record<unknown> {
  @doc("Enable this rendering rule.")
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @doc("SVG color value, usually #RRGGBB.")
  color?: string;
}

model SilkscreenSurfaceStyle extends Record<unknown> {
  @doc("Silkscreen clipping domain. none preserves authored overlay; board clips to board material and physical holes; film clips to the resolved solder-mask/coverlay film after apertures.")
  @extension("x-acr-input", "enum")
  clip_mode?: "none" | "board" | "film";
}

model Pin1MarkerStyle extends Record<unknown> {
  @doc("Enable this rendering rule.")
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @doc("SVG color value, usually #RRGGBB.")
  color?: string;

  @doc("Pin-1 marker dot diameter in millimeters.")
  @extension("x-acr-input", "number")
  dot_diameter_mm?: float64;

  @doc("Minimum pin-1 marker dot diameter in millimeters.")
  @extension("x-acr-input", "number")
  min_dot_diameter_mm?: float64;
}

model KeepoutStyle extends Record<unknown> {
  @doc("Enable this rendering rule.")
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @doc("SVG color value, usually #RRGGBB.")
  color?: string;
}

model StyleTable extends Record<StyleObject> {
  illustration?: IllustrationStyle;

  @doc("Autodoc silhouette fitting; model-less parts use electrical pads first (including flagged testpoints), with mechanical holes as a fallback.")
  assembly_designators?: AssemblyDesignatorsStyle;

  @doc("Bare PCB fill, clipped to the outline with physical bores and scoped cutouts removed. Place BOARD_SUBSTRATE before copper and film. Applies globally or per view.")
  board_substrate?: BoardSubstrateStyle;

  @doc("Board-clipped inverse solder mask using saved pad/via expansions. Applies globally or per view.")
  soldermask_film?: SoldermaskFilmStyle;

  @doc("Flat, region-clipped rigid-flex bend-line annotations. This does not fold or deform the board.")
  bend_lines?: BendLinesStyle;

  assembly_hlr?: AssemblyHlrStyle;
  board_outline?: BoardOutlineStyle;
  board_cutouts?: BoardCutoutsStyle;
  drills?: HoleStyle;
  slots?: HoleStyle;
  copper_traces?: CopperTracesStyle;
  vias?: ViasStyle;
  copper_polygons?: CopperPolygonsStyle;
  smd_pads?: SmdPadsStyle;
  through_hole_pads?: ThroughHolePadsStyle;
  silkscreen_component_graphics?: SilkscreenComponentGraphicsStyle;
  silkscreen_designators?: SilkscreenDesignatorsStyle;
  silkscreen_board_graphics?: SilkscreenBoardGraphicsStyle;
  silkscreen_surface?: SilkscreenSurfaceStyle;
  pin1_marker?: Pin1MarkerStyle;
  keepout?: KeepoutStyle;
}

model FastHlrOptions extends Record<unknown> {
  @extension("x-acr-input", "boolean")
  include_hidden?: boolean;

  @extension("x-acr-input", "boolean")
  include_boundaries?: boolean;

  @extension("x-acr-input", "boolean")
  include_creases?: boolean;

  @extension("x-acr-input", "boolean")
  include_silhouettes?: boolean;

  @extension("x-acr-input", "boolean")
  suppress_coplanar_seams?: boolean;
}

model AssemblyHlrStyle extends Record<unknown> {
  projection_algorithm?: "fast" | "poly" | "exact";
  outline_algorithm?: "fast-mesh-shadow" | "mesh-shadow" | "hlr-close";

  @doc("Geometer Fast candidate, tolerance and limit options. Legacy include/edge controls require an explicit poly/exact backend.")
  fast?: FastHlrOptions;

  @doc("Enable this rendering rule.")
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @doc("SVG color value, usually #RRGGBB.")
  color?: string;

  @doc("Stroke width in millimeters.")
  @extension("x-acr-input", "number")
  line_width_mm?: float64;

  @doc("Legacy HLR curve serialization mode; Fast always emits polylines. Options: native_arcs, polyline.")
  curve_mode?: string;

  @doc("Polyline sample count when curves are sampled.")
  @extension("x-acr-input", "number")
  samples_per_curve?: float64;

  @doc("Decimal places retained in generated SVG path coordinates.")
  @extension("x-acr-input", "number")
  round_digits?: float64;

  @doc("Legacy poly/exact visible-edge control; leave true for Fast.")
  @extension("x-acr-input", "boolean")
  include_visible?: boolean;

  @doc("Legacy poly/exact silhouette control; leave true for Fast.")
  @extension("x-acr-input", "boolean")
  include_outline?: boolean;

  @doc("Union projected polygons before converting to SVG paths.")
  @extension("x-acr-input", "boolean")
  union_polygons?: boolean;
}

model HoleStyle extends Record<unknown> {
  @doc("Enable this rendering rule.")
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @doc("SVG color for plated drill/slot features.")
  plated_color?: string;

  @doc("SVG color for non-plated drill/slot features.")
  non_plated_color?: string;

  @doc("Draw drill/slot boundaries with unfilled centers instead of filled marks.")
  @extension("x-acr-input", "boolean")
  outline?: boolean;

  @doc("Outline stroke width in millimeters.")
  @minValueExclusive(0)
  @extension("x-acr-input", "number")
  outline_width_mm?: float64;

  @doc("Hide plated drill/slot marks covered by solder mask on the rendered side.")
  @extension("x-acr-input", "boolean")
  respect_tenting?: boolean;

  @doc("Layer opacity from 0.0 to 1.0.")
  @minValue(0)
  @maxValue(1)
  @extension("x-acr-input", "number")
  opacity?: float64;
}

model CanvasOptions {
  @doc("Canvas bounds mode. Options: all_geometry, board_outline.")
  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "enum")
  bounds?:
    | "board_outline"
    | "all_geometry"
    | "board"
    | "outline"
    | "board_profile"
    | "legacy"
    | "all"
    | "rendered_view"
    | "rendered_geometry";

  @doc("Canvas margin added around the chosen bounds.")
  @minValue(0)
  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "number")
  margin_mm?: float64;
}

@extension("not", #{ required: #["png"] })
model GlobalOptions extends Record<unknown> {
  @doc("Optional PcbDoc selector when a PrjPcb contains multiple boards.")
  pcbdoc?: string | null;

  @doc("SVG viewBox normalization policy.")
  canvas?: CanvasOptions | null;

  @doc("Include Altium/source metadata in SVG data attributes.")
  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "boolean")
  include_metadata?: boolean;

  @doc("Emit empty physical layers when no primitives are present.")
  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "boolean")
  show_empty_layers?: boolean;

  @doc("Clip rendered geometry to the board outline.")
  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "boolean")
  clip_to_outline?: boolean;

  @doc("Clip drills and slots out of copper layers.")
  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "boolean")
  clip_holes_from_copper?: boolean;

  @doc("Mirror bottom-side views into assembly-view orientation.")
  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "boolean")
  mirror_bottom_view?: boolean;

  @doc("Multiplier for SVG width and height attributes.")
  @minValueExclusive(0)
  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "number")
  svg_scale?: float64;

  @doc("Optional SVG size unit suffix, such as mm or px.")
  svg_size_unit?: string | null;

  @doc("Reserved cleanup flag for generated output directories.")
  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "boolean")
  clean_output?: boolean;

  @doc("Default style table for physical and synthetic layers.")
  styles?: StyleTable | null;
}

model AssemblyOptions {
  @doc("Projection mode for fitted components. Options: bounding_box, detail, none, outline, simple.")
  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "enum")
  default_projection?: ProjectionMode;

  @doc("Projection mode for DNP components. Options: bounding_box, detail, none, outline, simple.")
  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "enum")
  dnp_projection?: ProjectionMode;

  @doc("Text color for fitted component designators.")
  designator_color?: string | null;

  @doc("Text color for DNP component designators.")
  dnp_designator_color?: string | null;
}

model DnpOptions {
  @doc("SVG color value, usually #RRGGBB.")
  color?: string | null;

  @doc("Enable hatch fill for this layer/style.")
  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "boolean")
  hatch?: boolean;

  @doc("Hatch spacing in millimeters.")
  @minValueExclusive(0)
  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "number")
  hatch_spacing_mm?: float64;

  @doc("Hatch angle in degrees.")
  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "number")
  hatch_angle_deg?: float64;

  @doc("Hatch stroke width in millimeters.")
  @minValueExclusive(0)
  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "number")
  hatch_line_width_mm?: float64;
}

model DiodeOptions {
  @doc("Enable diode/cathode marker detection.")
  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @doc("Draw diode line art when possible.")
  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "boolean")
  line_art?: boolean;

  @doc("Cathode marker color.")
  marker_color?: string | null;

  @doc("Default numeric cathode pad designator.")
  numeric_cathode_pad?: string | null;

  @doc("Pad names treated as cathode pads.")
  @extension("x-acr-nullable", true)
  cathode_pad_names?: string[];

  @doc("Designator prefixes treated as diode-like parts.")
  @extension("x-acr-nullable", true)
  designator_prefixes?: string[];

  @doc("Parameter text terms treated as diode-like parts.")
  @extension("x-acr-nullable", true)
  parameter_terms?: string[];
}

model Pin1Options {
  @doc("Component designator prefixes excluded from automatic pin-1 markers.")
  @extension("x-acr-nullable", true)
  exclude_designator_prefixes?: string[];
}

model LayerOutputOptions extends Record<unknown> {
  @doc("Enable individual physical layer SVG outputs.")
  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @doc("Either 'auto' or a list of PCB layer names: legacy PcbLayer names, display names, or V7 semantic tokens such as 'MECHANICAL33' and 'MID31' when the installed altium-monkey exposes the V7-aware layer API.")
  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "enum")
  layers?: "auto" | "AUTO" | string[];

  @doc("Synthetic layers also emitted with layer outputs. Options: BOARD_SUBSTRATE, BOARD_OUTLINE, BOARD_CUTOUTS, DRILLS, SLOTS, BEND_LINES, ASSEMBLY_HLR_TOP, ASSEMBLY_HLR_BOTTOM, ASSEMBLY_DESIGNATORS_TOP, ASSEMBLY_DESIGNATORS_BOTTOM, PIN1_TOP, PIN1_BOTTOM, SOLDERMASK_FILM_TOP, SOLDERMASK_FILM_BOTTOM, SURFACE_COPPER_TOP, SURFACE_COPPER_BOTTOM, ILLUSTRATION_TOP, and ILLUSTRATION_BOTTOM.")
  @extension("x-acr-nullable", true)
  include_special_layers?: (SyntheticLayer | string)[];

  @doc("Output directory for physical layer SVG files.")
  output_dir?: string | null;
}

model ViewOptions {
  @minLength(1)
  name: string;

  @doc("Enable this rendering rule.")
  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  group_id?: string | null;
  output_svg?: string | null;

  @doc("PCB layer names for this view: legacy PcbLayer names, display names, or V7 semantic tokens such as 'MECHANICAL33' and 'MID31' when the installed altium-monkey exposes the V7-aware layer API.")
  @extension("x-acr-nullable", true)
  layers?: string[];

  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "boolean")
  mirror?: boolean | null;

  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "enum")
  @extension("x-acr-trim", false)
  assembly_hlr_mode?:
    | "outline"
    | "simple"
    | "detail"
    | "detailed"
    | "bounding_box"
    | "none"
    | "silhouette"
    | "profile"
    | "bounding-box"
    | "bbox"
    | "box"
    | "off";

  styles?: StyleTable | null;
  description?: string | null;
}

@jsonSchema
@id("pcb_svg_config.a1.schema.json")
@extension("title", "pcb.svg.config.a1")
@extension("x-acr-jsonc-comments", configComments)
@extension("x-acr-jsonc-key-comments", styleComments)
@extension("x-acr-style-order", styleOrder)
@extension("x-acr-resolved-defaults", configDefaults)
@extension("x-acr-toon-preset", toonPreset)
@extension("x-acr-toon-themes", toonThemes)
model PcbSvgConfigInput extends Record<unknown> {
  @doc("PCB SVG config contract id. pcb.svg.config.a0 remains accepted as the additive predecessor.")
  schema?: "pcb.svg.config.a1" | "pcb.svg.config.a0" | null;

  @doc("Global settings applied to layer outputs and composed views.")
  global?: GlobalOptions | null;

  @doc("Assembly projection defaults for component virtual layers.")
  assembly?: AssemblyOptions | null;

  @doc("DNP marker style.")
  dnp?: DnpOptions | null;

  @doc("Diode/cathode marker detection policy.")
  diodes?: DiodeOptions | null;

  @doc("Pin-1 marker detection and display policy.")
  pin1?: Pin1Options | null;

  @doc("Per-designator overrides keyed by component designator.")
  components?: Record<ComponentOverride> | null;

  @doc("Config-driven physical layer SVG output policy.")
  layer_outputs?: LayerOutputOptions | null;

  @doc("Explicit composed SVG views. Each item has its own draw-order layer list.")
  views?: ViewOptions[] | null;
}

// Frozen additive predecessor. Its open records still permit extensions, but
// A1-only fields are not promoted into A0's typed/documented surface.
model BoardSubstrateStyleA0 extends Record<unknown> {
  @doc("Enable this rendering rule.")
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @doc("CSS color for exposed board substrate.")
  color?: string;
}

model SoldermaskFilmStyleA0 extends Record<unknown> {
  @doc("Enable this rendering rule.")
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @doc("CSS color or auto, which reads the side's saved Altium 3D solder-mask color and falls back to #176B3A.")
  color?: string;

  @doc("Layer opacity from 0.0 to 1.0.")
  @minValue(0)
  @maxValue(1)
  @extension("x-acr-input", "number")
  opacity?: float64;
}

model StyleTableA0 extends Record<StyleObject> {
  illustration?: IllustrationStyle;
  assembly_designators?: AssemblyDesignatorsStyle;
  board_substrate?: BoardSubstrateStyleA0;
  soldermask_film?: SoldermaskFilmStyleA0;
  assembly_hlr?: AssemblyHlrStyle;
  board_outline?: BoardOutlineStyle;
  board_cutouts?: BoardCutoutsStyle;
  drills?: HoleStyle;
  slots?: HoleStyle;
  copper_traces?: CopperTracesStyle;
  vias?: ViasStyle;
  copper_polygons?: CopperPolygonsStyle;
  smd_pads?: SmdPadsStyle;
  through_hole_pads?: ThroughHolePadsStyle;
  silkscreen_component_graphics?: SilkscreenComponentGraphicsStyle;
  silkscreen_designators?: SilkscreenDesignatorsStyle;
  silkscreen_board_graphics?: SilkscreenBoardGraphicsStyle;
  pin1_marker?: Pin1MarkerStyle;
  keepout?: KeepoutStyle;
}

@extension("not", #{ required: #["png"] })
model GlobalOptionsA0 extends Record<unknown> {
  ...OmitProperties<GlobalOptions, "styles">;
  styles?: StyleTableA0 | null;
}

model ViewOptionsA0 {
  ...OmitProperties<ViewOptions, "styles">;
  styles?: StyleTableA0 | null;
}

alias SyntheticLayerA0 =
  | "BOARD_SUBSTRATE"
  | "BOARD_OUTLINE"
  | "BOARD_CUTOUTS"
  | "DRILLS"
  | "SLOTS"
  | "ASSEMBLY_HLR_TOP"
  | "ASSEMBLY_HLR_BOTTOM"
  | "ASSEMBLY_DESIGNATORS_TOP"
  | "ASSEMBLY_DESIGNATORS_BOTTOM"
  | "PIN1_TOP"
  | "PIN1_BOTTOM"
  | "SOLDERMASK_FILM_TOP"
  | "SOLDERMASK_FILM_BOTTOM"
  | "ILLUSTRATION_TOP"
  | "ILLUSTRATION_BOTTOM";

model LayerOutputOptionsA0 extends Record<unknown> {
  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "boolean")
  enabled?: boolean;

  @extension("x-acr-nullable", true)
  @extension("x-acr-input", "enum")
  layers?: "auto" | "AUTO" | string[];

  @extension("x-acr-nullable", true)
  include_special_layers?: (SyntheticLayerA0 | string)[];

  output_dir?: string | null;
}

@jsonSchema
@id("pcb_svg_config.a0.schema.json")
@extension("title", "pcb.svg.config.a0")
model PcbSvgConfigA0Input extends Record<unknown> {
  @doc("PCB SVG config contract id.")
  schema?: "pcb.svg.config.a0" | null;
  global?: GlobalOptionsA0 | null;
  assembly?: AssemblyOptions | null;
  dnp?: DnpOptions | null;
  diodes?: DiodeOptions | null;
  pin1?: Pin1Options | null;
  components?: Record<ComponentOverride> | null;
  layer_outputs?: LayerOutputOptionsA0 | null;
  views?: ViewOptionsA0[] | null;
}
