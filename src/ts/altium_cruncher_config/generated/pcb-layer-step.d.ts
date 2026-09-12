/** Generated from src/tsp/altium_cruncher/config/pcb-layer-step-config.tsp. Do not edit. */

/**
 * JSON/JSONC configuration contract for fixture-alignment PCB layer STEP exports.
 */
export type PcbLayerStepConfigInput = {
  [k: string]: unknown;
} & {
  schema?: "altium_cruncher.pcb_layer_step.config.a0" | null;
  defaults?: OutputOptions;
  /**
   * @minItems 1
   */
  outputs?: [OutputOptions, ...OutputOptions[]];
  options?: OutputOptions;
  name?: string | null;
  output_step?: string | null;
  pcbdoc?: string | null;
  layer?: LayerSelector;
  thickness_mm?: number;
  z_mm?: number;
  copper_color?: Color;
  outline_width_mm?: number;
  outline_color?: Color;
  board_cutout_color?: Color;
  include_board_cutouts?: boolean;
  include_copper?: boolean;
  include_board_outline?: boolean;
  include_poured_polygons?: boolean;
  cut_holes?: boolean;
  drill_hole_mode?: DrillMode;
  max_boolean_drill_cuts?: number;
  drill_hole_color?: Color;
  drill_plated_hole_color?: Color;
  drill_non_plated_hole_color?: Color;
  drill_overlay_thickness_mm?: number;
  drill_minimum_diameter_mm?: number;
  drill_hole_shape?: DrillShape;
  drill_ring_width_mm?: number;
  drill_plated_ring_shape?: PlatedRingShape;
  drill_selected_component_mode?: DrillScopedMode;
  drill_other_component_mode?: DrillScopedMode;
  drill_free_pad_mode?: DrillScopedMode;
  drill_via_mode?: DrillScopedMode;
  fuse_copper?: boolean;
  fuse_board_outline?: boolean;
  arc_segments?: number;
  include_tracks?: boolean;
  include_arcs?: boolean;
  include_fills?: boolean;
  include_regions?: boolean;
  include_vias?: boolean;
  include_component_pads?: boolean;
  include_free_pads?: boolean;
  include_designators?: StringList;
  board_outline?: BoardOutline;
  features?: Features;
  drills?: Drills;
};
export type Color = string;
export type DrillMode = "auto" | "cut" | "overlay" | "none";
export type DrillShape = "solid" | "ring";
export type PlatedRingShape = "annulus";
export type DrillScopedMode = "inherit" | "cut" | "overlay" | "none";
export type StringList = string | string[];
export type FeatureSwitch = boolean | FeatureSwitchOption2;
export type FeaturesComponentPads = boolean | ComponentPads;
export type HighlightRules = HighlightRulesValueItem[];
/**
 * PCB layer selector: legacy PcbLayer name (for example 'TOP_OVERLAY'), display name (for example 'Mechanical 13'), legacy integer layer id, or a V7 semantic token such as 'MECHANICAL33' when the installed altium-monkey exposes the V7-aware layer API. Layer-step rendering writes legacy layer bytes, so V7-only layers (Mechanical17+, Mid31+) are rejected with an actionable error.
 */
export type LayerSelector = string | number | null;

export interface OutputOptions {
  options?: OutputOptions;
  name?: string | null;
  output_step?: string | null;
  pcbdoc?: string | null;
  /**
   * PCB layer selector: legacy PcbLayer name (for example 'TOP_OVERLAY'), display name (for example 'Mechanical 13'), legacy integer layer id, or a V7 semantic token such as 'MECHANICAL33' when the installed altium-monkey exposes the V7-aware layer API. Layer-step rendering writes legacy layer bytes, so V7-only layers (Mechanical17+, Mid31+) are rejected with an actionable error.
   */
  layer?: string | number | null;
  thickness_mm?: number;
  z_mm?: number;
  copper_color?: Color;
  outline_width_mm?: number;
  outline_color?: Color;
  board_cutout_color?: Color;
  include_board_cutouts?: boolean;
  include_copper?: boolean;
  include_board_outline?: boolean;
  include_poured_polygons?: boolean;
  cut_holes?: boolean;
  drill_hole_mode?: DrillMode;
  max_boolean_drill_cuts?: number;
  drill_hole_color?: Color;
  drill_plated_hole_color?: Color;
  drill_non_plated_hole_color?: Color;
  drill_overlay_thickness_mm?: number;
  drill_minimum_diameter_mm?: number;
  drill_hole_shape?: DrillShape;
  drill_ring_width_mm?: number;
  drill_plated_ring_shape?: PlatedRingShape;
  drill_selected_component_mode?: DrillScopedMode;
  drill_other_component_mode?: DrillScopedMode;
  drill_free_pad_mode?: DrillScopedMode;
  drill_via_mode?: DrillScopedMode;
  fuse_copper?: boolean;
  fuse_board_outline?: boolean;
  arc_segments?: number;
  include_tracks?: boolean;
  include_arcs?: boolean;
  include_fills?: boolean;
  include_regions?: boolean;
  include_vias?: boolean;
  include_component_pads?: boolean;
  include_free_pads?: boolean;
  include_designators?: StringList;
  board_outline?: BoardOutline;
  features?: Features;
  drills?: Drills;
}
export interface BoardOutline {
  color?: string;
  cutout_color?: string;
  cutouts_color?: Color;
  cutouts?: boolean;
  width_mm?: number;
  fuse?: boolean;
}
export interface Features {
  defaults?: FeatureDefaults;
  tracks?: FeatureSwitch;
  traces?: FeatureSwitch;
  arcs?: FeatureSwitch;
  fills?: FeatureSwitch;
  polygons?: FeatureSwitch;
  poured_polygons?: FeatureSwitch;
  regions?: FeatureSwitch;
  shapebased_regions?: FeatureSwitch;
  vias?: FeatureSwitch;
  component_pads?: FeaturesComponentPads;
  free_pads?: FeatureSwitch;
}
export interface FeatureDefaults {
  color?: Color;
}
export interface FeatureSwitchOption2 {
  enabled?: boolean;
  color?: Color;
  step_body_name?: string;
  thickness_bias_mm?: number;
}
export interface ComponentPads {
  enabled?: boolean;
  mode?: "none" | "all" | "matching_designators";
  include_designators?: StringList;
  color?: Color;
  step_body_name?: string;
  thickness_bias_mm?: number;
  highlight_rules?: HighlightRules;
}
export interface HighlightRulesValueItem {
  designators: StringList;
  color: Color;
  step_body_name?: string;
}
export interface Drills {
  mode?: DrillMode;
  minimum_diameter_mm?: number;
  shape?: DrillShape;
  color?: Color;
  plated_color?: Color;
  non_plated_color?: Color;
  ring_width_mm?: number;
  plated_ring_shape?: PlatedRingShape;
  selected_component_mode?: DrillScopedMode;
  other_component_mode?: DrillScopedMode;
  free_pad_mode?: DrillScopedMode;
  via_mode?: DrillScopedMode;
  overlay_thickness_mm?: number;
}
