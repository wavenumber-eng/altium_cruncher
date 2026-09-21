/** Generated from src/tsp/altium_cruncher/config/pcb-svg.tsp. Do not edit. */

export type PcbSvgConfigInput = RecordUnknown & {
  /**
   * PCB SVG config contract id. pcb.svg.config.a0 remains accepted as the additive predecessor.
   */
  schema?: "pcb.svg.config.a1" | "pcb.svg.config.a0" | null;
  /**
   * Global settings applied to layer outputs and composed views.
   */
  global?: GlobalOptions | null;
  /**
   * Assembly projection defaults for component virtual layers.
   */
  assembly?: AssemblyOptionsA1 | null;
  /**
   * DNP marker style.
   */
  dnp?: DnpOptions | null;
  /**
   * Diode/cathode marker detection policy.
   */
  diodes?: DiodeOptions | null;
  /**
   * Pin-1 marker detection and display policy.
   */
  pin1?: Pin1Options | null;
  /**
   * Per-designator overrides keyed by component designator.
   */
  components?: RecordComponentOverride | null;
  /**
   * Config-driven physical layer SVG output policy.
   */
  layer_outputs?: LayerOutputOptions | null;
  /**
   * Explicit composed SVG views. Each item has its own draw-order layer list.
   */
  views?: ViewOptions[] | null;
};
export type GlobalOptions = RecordUnknown & {
  /**
   * Optional PcbDoc selector when a PrjPcb contains multiple boards.
   */
  pcbdoc?: string | null;
  /**
   * SVG viewBox normalization policy.
   */
  canvas?: CanvasOptions | null;
  /**
   * Include Altium/source metadata in SVG data attributes.
   */
  include_metadata?: boolean | null | number | string;
  /**
   * Emit empty physical layers when no primitives are present.
   */
  show_empty_layers?: boolean | null | number | string;
  /**
   * Clip rendered geometry to the board outline.
   */
  clip_to_outline?: boolean | null | number | string;
  /**
   * Clip drills and slots out of copper layers.
   */
  clip_holes_from_copper?: boolean | null | number | string;
  /**
   * Mirror bottom-side views into assembly-view orientation.
   */
  mirror_bottom_view?: boolean | null | number | string;
  /**
   * Multiplier for SVG width and height attributes.
   */
  svg_scale?: number | null | boolean | string;
  /**
   * Optional SVG size unit suffix, such as mm or px.
   */
  svg_size_unit?: string | null;
  /**
   * Reserved cleanup flag for generated output directories.
   */
  clean_output?: boolean | null | number | string;
  /**
   * Default style table for physical and synthetic layers.
   */
  styles?: StyleTable | null;
};
export type StyleTable = RecordStyleObject & {
  illustration?: IllustrationStyle;
  assembly_designators?: AssemblyDesignatorsStyle;
  board_substrate?: BoardSubstrateStyle;
  soldermask_film?: SoldermaskFilmStyle;
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
};
export type IllustrationStyle = RecordUnknown & {
  /**
   * Enable this rendering rule.
   */
  enabled?: boolean | number | string;
  /**
   * Stroke width in millimeters.
   */
  line_width_mm?: number | boolean | string;
  /**
   * Layer opacity from 0.0 to 1.0.
   */
  opacity?: number | boolean | string;
};
/**
 * Autodoc silhouette fitting; model-less parts use electrical pads first (including flagged testpoints), with mechanical holes as a fallback.
 */
export type AssemblyDesignatorsStyle = RecordUnknown & {
  /**
   * Enable this rendering rule.
   */
  enabled?: boolean | number | string;
  /**
   * SVG color value, usually #RRGGBB.
   */
  color?: string;
  /**
   * Text outline CSS color, drawn behind the fill.
   */
  stroke_color?: string;
  /**
   * Full SVG stroke width in board millimetres. Zero disables the outline; fitting and placement are unchanged.
   */
  stroke_width_mm?: number | boolean | string;
  fill_ratio?: number | boolean | string;
  max_font_size_mm?: number | boolean | string;
  /**
   * Layer opacity from 0.0 to 1.0.
   */
  opacity?: number | boolean | string;
};
/**
 * Bare PCB fill, clipped to the outline with physical bores and scoped cutouts removed. Place BOARD_SUBSTRATE before copper and film. Applies globally or per view.
 */
export type BoardSubstrateStyle = RecordUnknown & {
  /**
   * Enable this rendering rule.
   */
  enabled?: boolean | number | string;
  /**
   * Global substrate CSS color override, or auto (default) for region-local authored/saved/palette resolution.
   */
  color?: string;
  /**
   * Rigid-substrate fallback CSS color used when color=auto and no authored or saved board-core color is available.
   */
  rigid_color?: string;
  /**
   * Flex-substrate fallback CSS color used when color=auto and no authored material color is available.
   */
  flex_color?: string;
};
/**
 * Board-clipped inverse solder mask using saved pad/via expansions. Applies globally or per view.
 */
export type SoldermaskFilmStyle = RecordUnknown & {
  /**
   * Enable this rendering rule.
   */
  enabled?: boolean | number | string;
  /**
   * Global film CSS color override, or auto (default) for region-local authored material, saved Altium 3D solder-mask color, and configured surface-class fallback resolution.
   */
  color?: string;
  /**
   * Coverlay fallback CSS color used when color=auto and the authored coverlay material has no color.
   */
  coverlay_color?: string;
  /**
   * Layer opacity from 0.0 to 1.0.
   */
  opacity?: number | boolean | string;
};
/**
 * Flat, region-clipped rigid-flex bend-line annotations. This does not fold or deform the board.
 */
export type BendLinesStyle = RecordUnknown & {
  /**
   * Enable flat board bend-line annotations.
   */
  enabled?: boolean | number | string;
  /**
   * SVG color for bend-line annotations.
   */
  color?: string;
  /**
   * Layer opacity from 0.0 to 1.0.
   */
  opacity?: number | boolean | string;
  /**
   * Stroke width in millimeters.
   */
  line_width_mm?: number | boolean | string;
  /**
   * Bend-line stroke style. Options: solid, dashed.
   */
  line_style?: ("solid" | "dashed") | string;
  /**
   * Dash and gap length in millimeters when line_style is dashed.
   */
  dash_length_mm?: number | boolean | string;
  /**
   * Gap between dashes in millimeters when line_style is dashed.
   */
  dash_gap_mm?: number | boolean | string;
  /**
   * Absolute distance each end extends beyond the owning-region chord, in millimeters. Zero stops at the region boundary.
   */
  extension_mm?: number | boolean | string;
};
export type AssemblyHlrStyle = RecordUnknown & {
  projection_algorithm?: "fast" | "poly" | "exact";
  outline_algorithm?: "fast-mesh-shadow" | "mesh-shadow" | "hlr-close";
  fast?: FastHlrOptions;
  /**
   * Enable this rendering rule.
   */
  enabled?: boolean | number | string;
  /**
   * SVG color value, usually #RRGGBB.
   */
  color?: string;
  /**
   * Stroke width in millimeters.
   */
  line_width_mm?: number | boolean | string;
  /**
   * Legacy HLR curve serialization mode; Fast always emits polylines. Options: native_arcs, polyline.
   */
  curve_mode?: string;
  /**
   * Polyline sample count when curves are sampled.
   */
  samples_per_curve?: number | boolean | string;
  /**
   * Decimal places retained in generated SVG path coordinates.
   */
  round_digits?: number | boolean | string;
  /**
   * Legacy poly/exact visible-edge control; leave true for Fast.
   */
  include_visible?: boolean | number | string;
  /**
   * Legacy poly/exact silhouette control; leave true for Fast.
   */
  include_outline?: boolean | number | string;
  /**
   * Union projected polygons before converting to SVG paths.
   */
  union_polygons?: boolean | number | string;
};
/**
 * Geometer Fast candidate, tolerance and limit options. Legacy include/edge controls require an explicit poly/exact backend.
 */
export type FastHlrOptions = RecordUnknown & {
  include_hidden?: boolean | number | string;
  include_boundaries?: boolean | number | string;
  include_creases?: boolean | number | string;
  include_silhouettes?: boolean | number | string;
  suppress_coplanar_seams?: boolean | number | string;
};
export type BoardOutlineStyle = RecordUnknown & {
  /**
   * Enable this rendering rule.
   */
  enabled?: boolean | number | string;
  /**
   * SVG color value, usually #RRGGBB.
   */
  color?: string;
  /**
   * Stroke width in millimeters.
   */
  line_width_mm?: number | boolean | string;
};
export type BoardCutoutsStyle = RecordUnknown & {
  /**
   * Enable this rendering rule.
   */
  enabled?: boolean | number | string;
  /**
   * Cutouts used by board clipping, film and cutout artwork. Interior uses the existing Mate containment filter to exclude touching/outside contours.
   */
  scope?: "all" | "interior";
  /**
   * Cutout outline opacity from 0.0 to 1.0.
   */
  outline_opacity?: number | boolean | string;
  /**
   * Hatch color; omitted uses the cutout outline color.
   */
  hatch_color?: string;
  /**
   * Hatch opacity from 0.0 to 1.0, independent of the outline.
   */
  hatch_opacity?: number | boolean | string;
  /**
   * Cutout label text; an empty string disables labels.
   */
  label?: string;
  /**
   * Label color; omitted uses the cutout outline color.
   */
  label_color?: string;
  /**
   * Cutout label opacity from 0.0 to 1.0.
   */
  label_opacity?: number | boolean | string;
  /**
   * Maximum fitted cutout label font size in millimeters.
   */
  label_max_font_size_mm?: number | boolean | string;
  /**
   * Fraction of cutout width/height available to the fitted label (0 to 1).
   */
  label_fill_ratio?: number | boolean | string;
  /**
   * Vertical cutout text must fit this fraction larger than horizontal after the size cap.
   */
  label_rotation_min_gain?: number | boolean | string;
  /**
   * SVG color value, usually #RRGGBB.
   */
  color?: string;
  /**
   * Enable hatch fill for this layer/style.
   */
  hatch?: boolean | number | string;
  /**
   * Hatch spacing in millimeters.
   */
  hatch_spacing_mm?: number | boolean | string;
  /**
   * Hatch angle in degrees.
   */
  hatch_angle_deg?: number | boolean | string;
  /**
   * Hatch stroke width in millimeters.
   */
  hatch_line_width_mm?: number | boolean | string;
  /**
   * Outline stroke style. Options: solid, dashed.
   */
  outline_style?: ("solid" | "dashed") | string;
  /**
   * Dash length in millimeters when outline_style is dashed.
   */
  outline_dash_mm?: number | boolean | string;
  /**
   * Outline stroke width in millimeters.
   */
  outline_width_mm?: number | boolean | string;
};
export type HoleStyle = RecordUnknown & {
  /**
   * Enable this rendering rule.
   */
  enabled?: boolean | number | string;
  /**
   * SVG color for plated drill/slot features.
   */
  plated_color?: string;
  /**
   * SVG color for non-plated drill/slot features.
   */
  non_plated_color?: string;
  /**
   * Draw drill/slot boundaries with unfilled centers instead of filled marks.
   */
  outline?: boolean | number | string;
  /**
   * Outline stroke width in millimeters.
   */
  outline_width_mm?: number | boolean | string;
  /**
   * Hide plated drill/slot marks covered by solder mask on the rendered side.
   */
  respect_tenting?: boolean | number | string;
  /**
   * Layer opacity from 0.0 to 1.0.
   */
  opacity?: number | boolean | string;
};
export type CopperTracesStyle = RecordUnknown & {
  /**
   * Enable this rendering rule.
   */
  enabled?: boolean | number | string;
  /**
   * SVG color value, usually #RRGGBB.
   */
  color?: string;
};
export type ViasStyle = RecordUnknown & {
  /**
   * Enable this rendering rule.
   */
  enabled?: boolean | number | string;
  /**
   * SVG color value, usually #RRGGBB.
   */
  color?: string;
};
export type CopperPolygonsStyle = RecordUnknown & {
  /**
   * Enable this rendering rule.
   */
  enabled?: boolean | number | string;
  /**
   * SVG color value, usually #RRGGBB.
   */
  color?: string;
};
export type SmdPadsStyle = RecordUnknown & {
  /**
   * Enable this rendering rule.
   */
  enabled?: boolean | number | string;
  /**
   * SVG color value, usually #RRGGBB.
   */
  color?: string;
};
export type ThroughHolePadsStyle = RecordUnknown & {
  /**
   * Enable this rendering rule.
   */
  enabled?: boolean | number | string;
  /**
   * SVG color value, usually #RRGGBB.
   */
  color?: string;
};
export type SilkscreenComponentGraphicsStyle = RecordUnknown & {
  /**
   * Enable this rendering rule.
   */
  enabled?: boolean | number | string;
  /**
   * SVG color value, usually #RRGGBB.
   */
  color?: string;
};
export type SilkscreenDesignatorsStyle = RecordUnknown & {
  /**
   * Enable this rendering rule.
   */
  enabled?: boolean | number | string;
  /**
   * SVG color value, usually #RRGGBB.
   */
  color?: string;
};
export type SilkscreenBoardGraphicsStyle = RecordUnknown & {
  /**
   * Enable this rendering rule.
   */
  enabled?: boolean | number | string;
  /**
   * SVG color value, usually #RRGGBB.
   */
  color?: string;
};
export type SilkscreenSurfaceStyle = RecordUnknown & {
  /**
   * Silkscreen clipping domain. none preserves authored overlay; board clips to board material and physical holes; film clips to the resolved solder-mask/coverlay film after apertures.
   */
  clip_mode?: ("none" | "board" | "film") | string;
};
export type Pin1MarkerStyle = RecordUnknown & {
  /**
   * Enable this rendering rule.
   */
  enabled?: boolean | number | string;
  /**
   * SVG color value, usually #RRGGBB.
   */
  color?: string;
  /**
   * Pin-1 marker dot diameter in millimeters.
   */
  dot_diameter_mm?: number | boolean | string;
  /**
   * Minimum pin-1 marker dot diameter in millimeters.
   */
  min_dot_diameter_mm?: number | boolean | string;
};
export type KeepoutStyle = RecordUnknown & {
  /**
   * Enable this rendering rule.
   */
  enabled?: boolean | number | string;
  /**
   * SVG color value, usually #RRGGBB.
   */
  color?: string;
};
export type LayerOutputOptions = RecordUnknown & {
  /**
   * Enable individual physical layer SVG outputs.
   */
  enabled?: boolean | null | number | string;
  /**
   * Either 'auto' or a list of PCB layer names: legacy PcbLayer names, display names, or V7 semantic tokens such as 'MECHANICAL33' and 'MID31' when the installed altium-monkey exposes the V7-aware layer API.
   */
  layers?: ("auto" | "AUTO" | string[]) | null | string;
  /**
   * Synthetic layers also emitted with layer outputs. Options: BOARD_SUBSTRATE, BOARD_OUTLINE, BOARD_CUTOUTS, DRILLS, SLOTS, BEND_LINES, ASSEMBLY_HLR_TOP, ASSEMBLY_HLR_BOTTOM, ASSEMBLY_DESIGNATORS_TOP, ASSEMBLY_DESIGNATORS_BOTTOM, PIN1_TOP, PIN1_BOTTOM, SOLDERMASK_FILM_TOP, SOLDERMASK_FILM_BOTTOM, SURFACE_COPPER_TOP, SURFACE_COPPER_BOTTOM, ILLUSTRATION_TOP, and ILLUSTRATION_BOTTOM.
   */
  include_special_layers?:
    | (
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
        | "ILLUSTRATION_BOTTOM"
        | string
      )[]
    | null;
  /**
   * Output directory for physical layer SVG files.
   */
  output_dir?: string | null;
};

export interface RecordUnknown {
  [k: string]: unknown;
}
export interface CanvasOptions {
  /**
   * Canvas bounds mode. Options: all_geometry, board_outline.
   */
  bounds?:
    | (
        | "board_outline"
        | "all_geometry"
        | "board"
        | "outline"
        | "board_profile"
        | "legacy"
        | "all"
        | "rendered_view"
        | "rendered_geometry"
      )
    | null
    | string;
  /**
   * Canvas margin added around the chosen bounds.
   */
  margin_mm?: number | null | boolean | string;
}
export interface RecordStyleObject {
  [k: string]: StyleObject;
}
export interface StyleObject {
  [k: string]: unknown;
}
export interface AssemblyOptionsA1 {
  /**
   * Projection mode for fitted components. Options: bounding_box, detail, none, outline, simple.
   */
  default_projection?:
    | (
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
        | "disabled"
      )
    | null
    | string;
  /**
   * Projection mode for DNP components. Options: bounding_box, detail, none, outline, simple.
   */
  dnp_projection?:
    | (
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
        | "disabled"
      )
    | null
    | string;
  /**
   * Text color for fitted component designators.
   */
  designator_color?: string | null;
  /**
   * Text color for DNP component designators.
   */
  dnp_designator_color?: string | null;
  /**
   * Hide authored physical silkscreen designators when projected assembly designators are requested. Defaults to false so --assembly preserves the board as authored.
   */
  hide_silkscreen_designators?: boolean | null | number | string;
}
export interface DnpOptions {
  /**
   * SVG color value, usually #RRGGBB.
   */
  color?: string | null;
  /**
   * Enable hatch fill for this layer/style.
   */
  hatch?: boolean | null | number | string;
  /**
   * Hatch spacing in millimeters.
   */
  hatch_spacing_mm?: number | null | boolean | string;
  /**
   * Hatch angle in degrees.
   */
  hatch_angle_deg?: number | null | boolean | string;
  /**
   * Hatch stroke width in millimeters.
   */
  hatch_line_width_mm?: number | null | boolean | string;
}
export interface DiodeOptions {
  /**
   * Enable diode/cathode marker detection.
   */
  enabled?: boolean | null | number | string;
  /**
   * Draw diode line art when possible.
   */
  line_art?: boolean | null | number | string;
  /**
   * Cathode marker color.
   */
  marker_color?: string | null;
  /**
   * Default numeric cathode pad designator.
   */
  numeric_cathode_pad?: string | null;
  /**
   * Pad names treated as cathode pads.
   */
  cathode_pad_names?: string[] | null;
  /**
   * Designator prefixes treated as diode-like parts.
   */
  designator_prefixes?: string[] | null;
  /**
   * Parameter text terms treated as diode-like parts.
   */
  parameter_terms?: string[] | null;
}
export interface Pin1Options {
  /**
   * Component designator prefixes excluded from automatic pin-1 markers.
   */
  exclude_designator_prefixes?: string[] | null;
}
export interface RecordComponentOverride {
  [k: string]: ComponentOverride;
}
export interface ComponentOverride {
  side?:
    | (
        | "top"
        | "bottom"
        | "toplayer"
        | "bottomlayer"
        | "top_layer"
        | "bottom_layer"
        | "top-layer"
        | "bottom-layer"
        | null
      )
    | null
    | string;
  projection?:
    | (
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
        | "disabled"
        | null
      )
    | null
    | string;
  assembly_hlr?: AssemblyHlrStyle | null;
  pin1_enabled?: (boolean | null) | null | number | string;
  pin1_pad?: string | null;
  cathode_pad?: string | null;
  diode?: (boolean | null) | null | number | string;
  diode_line_art?: (boolean | null) | null | number | string;
  show_designator?: (boolean | null) | null | number | string;
}
export interface ViewOptions {
  name: string;
  /**
   * Enable this rendering rule.
   */
  enabled?: boolean | null | number | string;
  group_id?: string | null;
  output_svg?: string | null;
  /**
   * PCB layer names for this view: legacy PcbLayer names, display names, or V7 semantic tokens such as 'MECHANICAL33' and 'MID31' when the installed altium-monkey exposes the V7-aware layer API.
   */
  layers?: string[] | null;
  mirror?: (boolean | null) | null | number | string;
  assembly_hlr_mode?:
    | (
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
        | "off"
      )
    | null
    | string;
  styles?: StyleTable | null;
  description?: string | null;
}
