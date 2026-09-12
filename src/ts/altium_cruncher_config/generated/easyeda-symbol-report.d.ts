/** Generated from src/tsp/altium_cruncher/outputs/easyeda.tsp. Do not edit. */

/**
 * Existing unversioned mapping report: this schema adds no field to the emitted wire object.
 */
export interface EasyedaSymbolReport {
  lcsc_id: string;
  symbol_name: string;
  designator: string;
  pin_count: number;
  rectangle_count: number;
  circle_count: number;
  ellipse_count: number;
  polyline_count: number;
  polygon_count: number;
  unsupported_count: number;
  unsupported_graphics: string[];
  warnings: string[];
  policy: SymbolPolicy;
  grid: HotspotGrid;
}
export interface SymbolPolicy {
  mils_per_easyeda_unit?: number;
  invert_y?: boolean;
  default_pin_length_mils?: number;
  hotspot_grid_mils?: number;
  align_hotspots_to_grid?: boolean;
  body_color?: number;
  body_fill_color?: number;
  use_source_pin_electrical?: boolean;
  use_source_pin_ieee_symbols?: boolean;
  pin_name_visibility?: string;
  pin_designator_visibility?: string;
  pin_text_orientation?: string;
  rotate_vertical_pin_text?: boolean;
}
export interface HotspotGrid {
  hotspot_grid_mils?: number;
  align_hotspots_to_grid?: boolean;
  anchor_adjusted_to_grid?: boolean;
  source_grid_units?: number;
  source_common_offset_possible?: boolean;
  source_x_remainder?: number | null;
  source_y_remainder?: number | null;
  hotspot_count?: number;
  off_grid_hotspot_count?: number;
  max_hotspot_error_mils?: number;
  off_grid_hotspots_sample?: OffGridHotspot[];
}
export interface OffGridHotspot {
  pin: string;
  name: string;
  x_mils: number;
  y_mils: number;
  x_error_mils: number;
  y_error_mils: number;
}
