/** Generated from src/tsp/altium_cruncher/outputs/easyeda.tsp. Do not edit. */

/**
 * @minItems 4
 * @maxItems 4
 */
export type BoundsArray = [number, number, number, number];

/**
 * Existing unversioned mapping report: this schema adds no field to the emitted wire object.
 */
export interface EasyedaFootprintReport {
  lcsc_id: string;
  footprint_name: string;
  source_pad_count: number;
  generated_pad_count: number;
  generated_hole_pad_count: number;
  custom_pad_count: number;
  slotted_pad_count: number;
  track_count: number;
  track_segment_count: number;
  circle_count: number;
  arc_count: number;
  rectangle_count: number;
  region_count: number;
  text_count: number;
  unsupported_count: number;
  unsupported_graphics: string[];
  warnings: string[];
  layers: RecordInteger;
  policy: FootprintPolicy;
  transform: FootprintTransform;
  model_3d_attached: boolean;
  model_3d_centered_fallback: boolean;
  model_3d_placement_verdict: string;
  model_3d: ModelAttachment;
}
export interface RecordInteger {
  [k: string]: number;
}
export interface FootprintPolicy {
  mils_per_easyeda_unit?: number;
  invert_y?: boolean;
  include_source_graphics?: boolean;
  include_source_text?: boolean;
  include_non_pad_holes?: boolean;
  default_graphic_width_mils?: number;
  curve_approximation_segments?: number;
  arc_approximation_max_degrees?: number;
}
export interface FootprintTransform {
  anchor_x?: number;
  anchor_y?: number;
  mils_per_easyeda_unit?: number;
  invert_y?: boolean;
}
export interface ModelAttachment {
  name?: string;
  error?: string;
  location_mils?: number[];
  raw_location_mils?: number[];
  centered_fallback?: boolean;
  rotation_degrees?: number[];
  standoff_mils?: number;
  identifier?: string;
  placement_check?: PlacementCheck;
}
export interface PlacementCheck {
  verdict?: "ok" | "needs_checking";
  checked?: boolean;
  reason?: string;
  center_distance_mils?: number;
  distance_ratio?: number;
  model_bounds_mils?: BoundsArray;
  pad_bounds_mils?: BoundsArray;
}
