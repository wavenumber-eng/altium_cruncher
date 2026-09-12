/** Generated from src/tsp/altium_cruncher/outputs/pcb-layer-step.tsp. Do not edit. */

/**
 * @minItems 2
 * @maxItems 2
 */
export type Point = [number, number];

export interface PcbLayerStepManifest {
  schema: "altium_cruncher.pcb_layer_step.a0";
  backend: "geometer.planar_step";
  board: string;
  source_input: string | null;
  step_file: string;
  coordinate_origin: CoordinateOrigin;
  layer: Layer;
  options: Options;
  counts: RecordInteger;
  bytes: number;
}
export interface CoordinateOrigin {
  mode: "board_origin";
  origin_mils: Point;
  origin_mm: Point;
  geometry: string;
}
export interface Layer {
  id: number;
  json_name: string;
  display_name: string;
}
export interface Options {
  thickness_mm: number;
  z_mm: number;
  copper_color: string;
  outline_width_mm: number;
  outline_color: string;
  board_cutout_color: string;
  include_copper: boolean;
  include_board_outline: boolean;
  include_board_cutouts: boolean;
  include_poured_polygons: boolean;
  cut_holes: boolean;
  drill_hole_mode: string;
  effective_drill_hole_mode: string;
  max_boolean_drill_cuts: number;
  drill_hole_color: string;
  drill_plated_hole_color: string;
  drill_non_plated_hole_color: string;
  drill_overlay_thickness_mm: number;
  drill_minimum_diameter_mm: number;
  drill_hole_shape: string;
  drill_ring_width_mm: number;
  drill_plated_ring_shape: string;
  drill_selected_component_mode: string;
  drill_other_component_mode: string;
  drill_free_pad_mode: string;
  drill_via_mode: string;
  fuse_copper: boolean;
  fuse_board_outline: boolean;
  arc_segments: number;
  features: FeatureSwitches;
  pad_color_rules: PadColorRule[];
  feature_color_rules: FeatureStyles;
  thickness_bias_mm: ThicknessBias;
  highlight_count: number;
}
export interface FeatureSwitches {
  tracks: boolean;
  arcs: boolean;
  fills: boolean;
  polygons: boolean;
  regions: boolean;
  vias: boolean;
  component_pads: boolean;
  free_pads: boolean;
  include_designators: string[];
}
export interface PadColorRule {
  designators: string[];
  color: string;
  step_body_name: string | null;
}
export interface FeatureStyles {
  tracks: FeatureStyle;
  arcs: FeatureStyle;
  fills: FeatureStyle;
  polygons: FeatureStyle;
  regions: FeatureStyle;
  vias: FeatureStyle;
  component_pads: FeatureStyle;
  free_pads: FeatureStyle;
}
export interface FeatureStyle {
  color: string | null;
  step_body_name: string | null;
}
export interface ThicknessBias {
  tracks: number;
  arcs: number;
  fills: number;
  polygons: number;
  regions: number;
  vias: number;
  component_pads: number;
  free_pads: number;
}
export interface RecordInteger {
  [k: string]: number;
}
