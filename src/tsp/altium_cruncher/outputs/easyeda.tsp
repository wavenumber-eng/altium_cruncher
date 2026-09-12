import "@typespec/json-schema";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.EasyedaReports;

@minItems(4)
@maxItems(4)
model BoundsArray is float64[];
model PlacementCheck {
  verdict?: "ok" | "needs_checking";
  checked?: boolean;
  reason?: string;
  center_distance_mils?: float64;
  distance_ratio?: float64;
  model_bounds_mils?: BoundsArray;
  pad_bounds_mils?: BoundsArray;
}
model ModelAttachment {
  name?: string;
  error?: string;
  location_mils?: float64[];
  raw_location_mils?: float64[];
  centered_fallback?: boolean;
  rotation_degrees?: float64[];
  standoff_mils?: float64;
  identifier?: string;
  placement_check?: PlacementCheck;
}
model ModelReference {
  uuid: string;
  title: string;
  origin: string;
  z: string;
  rotation: string;
  files: Record<string>;
  errors: Record<string>;
  placement_status: string;
}
@jsonSchema
@id("altium_cruncher.easyeda.3d_models.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "easyeda_models",
    title: "EasyEDA model downloads",
    source: "../outputs/easyeda",
    kind: "output",
  }
)
model EasyedaModels {
  schema: "altium_cruncher.easyeda.3d_models.a0";
  lcsc_id: string;
  placement_implemented: boolean;
  placement_note: string;
  models: ModelReference[];
  placement_verdict?: string;
  placement_check?: PlacementCheck;
}
model FootprintPolicy {
  mils_per_easyeda_unit?: float64;
  invert_y?: boolean;
  include_source_graphics?: boolean;
  include_source_text?: boolean;
  include_non_pad_holes?: boolean;
  default_graphic_width_mils?: float64;
  curve_approximation_segments?: integer;
  arc_approximation_max_degrees?: float64;
}
model FootprintTransform {
  anchor_x?: float64;
  anchor_y?: float64;
  mils_per_easyeda_unit?: float64;
  invert_y?: boolean;
}
@jsonSchema
@id("altium_cruncher.easyeda.footprint_report.a0")
@doc("Existing unversioned mapping report: this schema adds no field to the emitted wire object.")
@extension(
  "x-acr-contract",
  #{
    stem: "easyeda_footprint_report",
    title: "EasyEDA footprint mapping",
    source: "../outputs/easyeda",
    kind: "output",
  }
)
model EasyedaFootprintReport {
  lcsc_id: string;
  footprint_name: string;
  source_pad_count: integer;
  generated_pad_count: integer;
  generated_hole_pad_count: integer;
  custom_pad_count: integer;
  slotted_pad_count: integer;
  track_count: integer;
  track_segment_count: integer;
  circle_count: integer;
  arc_count: integer;
  rectangle_count: integer;
  region_count: integer;
  text_count: integer;
  unsupported_count: integer;
  unsupported_graphics: string[];
  warnings: string[];
  layers: Record<integer>;
  policy: FootprintPolicy;
  transform: FootprintTransform;
  model_3d_attached: boolean;
  model_3d_centered_fallback: boolean;
  model_3d_placement_verdict: string;
  model_3d: ModelAttachment;
}
model SymbolPolicy {
  mils_per_easyeda_unit?: float64;
  invert_y?: boolean;
  default_pin_length_mils?: float64;
  hotspot_grid_mils?: float64;
  align_hotspots_to_grid?: boolean;
  body_color?: integer;
  body_fill_color?: integer;
  use_source_pin_electrical?: boolean;
  use_source_pin_ieee_symbols?: boolean;
  pin_name_visibility?: string;
  pin_designator_visibility?: string;
  pin_text_orientation?: string;
  rotate_vertical_pin_text?: boolean;
}
model OffGridHotspot {
  pin: string;
  name: string;
  x_mils: float64;
  y_mils: float64;
  x_error_mils: float64;
  y_error_mils: float64;
}
model HotspotGrid {
  hotspot_grid_mils?: float64;
  align_hotspots_to_grid?: boolean;
  anchor_adjusted_to_grid?: boolean;
  source_grid_units?: float64;
  source_common_offset_possible?: boolean;
  source_x_remainder?: float64 | null;
  source_y_remainder?: float64 | null;
  hotspot_count?: integer;
  off_grid_hotspot_count?: integer;
  max_hotspot_error_mils?: float64;
  off_grid_hotspots_sample?: OffGridHotspot[];
}
@jsonSchema
@id("altium_cruncher.easyeda.symbol_report.a0")
@doc("Existing unversioned mapping report: this schema adds no field to the emitted wire object.")
@extension(
  "x-acr-contract",
  #{
    stem: "easyeda_symbol_report",
    title: "EasyEDA symbol mapping",
    source: "../outputs/easyeda",
    kind: "output",
  }
)
model EasyedaSymbolReport {
  lcsc_id: string;
  symbol_name: string;
  designator: string;
  pin_count: integer;
  rectangle_count: integer;
  circle_count: integer;
  ellipse_count: integer;
  polyline_count: integer;
  polygon_count: integer;
  unsupported_count: integer;
  unsupported_graphics: string[];
  warnings: string[];
  policy: SymbolPolicy;
  grid: HotspotGrid;
}
