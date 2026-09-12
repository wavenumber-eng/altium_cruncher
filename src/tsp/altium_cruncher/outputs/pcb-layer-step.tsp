import "@typespec/json-schema";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.PcbLayerStepOutput;

@minItems(2)
@maxItems(2)
model Point is float64[];
model CoordinateOrigin {
  mode: "board_origin";
  origin_mils: Point;
  origin_mm: Point;
  geometry: string;
}
model Layer {
  id: integer;
  json_name: string;
  display_name: string;
}
model FeatureSwitches {
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
model FeatureStyle {
  color: string | null;
  step_body_name: string | null;
}
model FeatureStyles {
  tracks: FeatureStyle;
  arcs: FeatureStyle;
  fills: FeatureStyle;
  polygons: FeatureStyle;
  regions: FeatureStyle;
  vias: FeatureStyle;
  component_pads: FeatureStyle;
  free_pads: FeatureStyle;
}
model ThicknessBias {
  tracks: float64;
  arcs: float64;
  fills: float64;
  polygons: float64;
  regions: float64;
  vias: float64;
  component_pads: float64;
  free_pads: float64;
}
model PadColorRule {
  designators: string[];
  color: string;
  step_body_name: string | null;
}
model Options {
  thickness_mm: float64;
  z_mm: float64;
  copper_color: string;
  outline_width_mm: float64;
  outline_color: string;
  board_cutout_color: string;
  include_copper: boolean;
  include_board_outline: boolean;
  include_board_cutouts: boolean;
  include_poured_polygons: boolean;
  cut_holes: boolean;
  drill_hole_mode: string;
  effective_drill_hole_mode: string;
  max_boolean_drill_cuts: integer;
  drill_hole_color: string;
  drill_plated_hole_color: string;
  drill_non_plated_hole_color: string;
  drill_overlay_thickness_mm: float64;
  drill_minimum_diameter_mm: float64;
  drill_hole_shape: string;
  drill_ring_width_mm: float64;
  drill_plated_ring_shape: string;
  drill_selected_component_mode: string;
  drill_other_component_mode: string;
  drill_free_pad_mode: string;
  drill_via_mode: string;
  fuse_copper: boolean;
  fuse_board_outline: boolean;
  arc_segments: integer;
  features: FeatureSwitches;
  pad_color_rules: PadColorRule[];
  feature_color_rules: FeatureStyles;
  thickness_bias_mm: ThicknessBias;
  highlight_count: integer;
}
@jsonSchema
@id("altium_cruncher.pcb_layer_step.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "pcb_layer_step",
    slug: "pcb-layer-step-output",
    title: "PCB layer STEP sidecar",
    source: "../outputs/pcb-layer-step",
    kind: "output",
  }
)
model PcbLayerStepManifest {
  schema: "altium_cruncher.pcb_layer_step.a0";
  backend: "geometer.planar_step";
  board: string;
  source_input: string | null;
  step_file: string;
  coordinate_origin: CoordinateOrigin;
  layer: Layer;
  options: Options;
  counts: Record<integer>;
  bytes: integer;
}
