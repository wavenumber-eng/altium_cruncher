import "@typespec/json-schema";
import "./pcb-layer-step-config-defaults.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.PcbLayerStepConfigInputContract;

model OutputOptions {
  options?: OutputOptions;
  name?: string | null;
  output_step?: string | null;
  pcbdoc?: string | null;
  layer?: LayerSelector;
  ...ExportOptions;
}

@doc("Shared geometry/export settings also forwarded by Mate artifacts.")
model ExportOptions {
  @extension("exclusiveMinimum", 0)
  thickness_mm?: float64;

  z_mm?: float64;
  copper_color?: Color;

  @extension("minimum", 0)
  outline_width_mm?: float64;

  outline_color?: Color;
  board_cutout_color?: Color;
  include_board_cutouts?: boolean;
  include_copper?: boolean;
  include_board_outline?: boolean;
  include_poured_polygons?: boolean;
  cut_holes?: boolean;
  drill_hole_mode?: DrillMode;

  @extension("minimum", 0)
  max_boolean_drill_cuts?: integer;

  drill_hole_color?: Color;
  drill_plated_hole_color?: Color;
  drill_non_plated_hole_color?: Color;

  @extension("minimum", 0)
  drill_overlay_thickness_mm?: float64;

  @extension("minimum", 0)
  drill_minimum_diameter_mm?: float64;

  drill_hole_shape?: DrillShape;

  @extension("minimum", 0)
  drill_ring_width_mm?: float64;

  drill_plated_ring_shape?: PlatedRingShape;
  drill_selected_component_mode?: DrillScopedMode;
  drill_other_component_mode?: DrillScopedMode;
  drill_free_pad_mode?: DrillScopedMode;
  drill_via_mode?: DrillScopedMode;
  fuse_copper?: boolean;
  fuse_board_outline?: boolean;

  @extension("minimum", 1)
  arc_segments?: integer;

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

@doc("PCB layer selector: legacy PcbLayer name (for example 'TOP_OVERLAY'), display name (for example 'Mechanical 13'), legacy integer layer id, or a V7 semantic token such as 'MECHANICAL33' when the installed altium-monkey exposes the V7-aware layer API. Layer-step rendering writes legacy layer bytes, so V7-only layers (Mechanical17+, Mid31+) are rejected with an actionable error.")
union LayerSelector {
  string,
  integer,
  null,
}

@extension("minLength", 1)
scalar Color extends string;

@oneOf
union StringList {
  string,
  string[],
}

model BoardOutline {
  color?: Color;
  cutout_color?: Color;
  cutouts_color?: Color;
  cutouts?: boolean;

  @extension("minimum", 0)
  width_mm?: float64;

  fuse?: boolean;
}

@oneOf
union FeaturesComponentPads {
  boolean,
  ComponentPads,
}

model Features {
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

model FeatureDefaults {
  color?: Color;
}

model FeatureSwitchOption2 {
  enabled?: boolean;
  color?: Color;

  @extension("minLength", 1)
  step_body_name?: string;

  @extension("minimum", 0)
  thickness_bias_mm?: float64;
}

@oneOf
union FeatureSwitch {
  boolean,
  FeatureSwitchOption2,
}

model ComponentPads {
  enabled?: boolean;
  mode?: "none" | "all" | "matching_designators";
  include_designators?: StringList;
  color?: Color;

  @extension("minLength", 1)
  step_body_name?: string;

  @extension("minimum", 0)
  thickness_bias_mm?: float64;

  highlight_rules?: HighlightRules;
}

model HighlightRulesValueItem {
  designators: StringList;
  color: Color;

  @extension("minLength", 1)
  step_body_name?: string;
}

model HighlightRules is HighlightRulesValueItem[];

model Drills {
  mode?: DrillMode;

  @extension("minimum", 0)
  minimum_diameter_mm?: float64;

  shape?: DrillShape;
  color?: Color;
  plated_color?: Color;
  non_plated_color?: Color;

  @extension("minimum", 0)
  ring_width_mm?: float64;

  plated_ring_shape?: PlatedRingShape;
  selected_component_mode?: DrillScopedMode;
  other_component_mode?: DrillScopedMode;
  free_pad_mode?: DrillScopedMode;
  via_mode?: DrillScopedMode;

  @extension("minimum", 0)
  overlay_thickness_mm?: float64;
}

union DrillMode {
  "auto",
  "cut",
  "overlay",
  "none",
}

union DrillScopedMode {
  "inherit",
  "cut",
  "overlay",
  "none",
}

union DrillShape {
  "solid",
  "ring",
}

union PlatedRingShape {
  "annulus",
}

@jsonSchema
@id("https://github.com/wavenumber-eng/altium_cruncher/docs/contracts/pcb_layer_step_config.a0.schema.json")
@doc("JSON/JSONC configuration contract for fixture-alignment PCB layer STEP exports.")
@extension("title", "Altium Cruncher PCB Layer STEP Config")
@extension(
  "allOf",
  #[
    #{
      `if`: #{ required: #["outputs"] },
      then: #{
        properties: #{
          schema: #{ `const`: "altium_cruncher.pcb_layer_step.config.a0" },
        },
      },
    }
  ]
)
model PcbLayerStepConfigInput {
  schema?: "altium_cruncher.pcb_layer_step.config.a0" | null;
  defaults?: OutputOptions;

  @extension("minItems", 1)
  outputs?: OutputOptions[];

  options?: OutputOptions;
  name?: string | null;
  output_step?: string | null;
  pcbdoc?: string | null;
  layer?: LayerSelector;

  @extension("exclusiveMinimum", 0)
  thickness_mm?: float64;

  z_mm?: float64;
  copper_color?: Color;

  @extension("minimum", 0)
  outline_width_mm?: float64;

  outline_color?: Color;
  board_cutout_color?: Color;
  include_board_cutouts?: boolean;
  include_copper?: boolean;
  include_board_outline?: boolean;
  include_poured_polygons?: boolean;
  cut_holes?: boolean;
  drill_hole_mode?: DrillMode;

  @extension("minimum", 0)
  max_boolean_drill_cuts?: integer;

  drill_hole_color?: Color;
  drill_plated_hole_color?: Color;
  drill_non_plated_hole_color?: Color;

  @extension("minimum", 0)
  drill_overlay_thickness_mm?: float64;

  @extension("minimum", 0)
  drill_minimum_diameter_mm?: float64;

  drill_hole_shape?: DrillShape;

  @extension("minimum", 0)
  drill_ring_width_mm?: float64;

  drill_plated_ring_shape?: PlatedRingShape;
  drill_selected_component_mode?: DrillScopedMode;
  drill_other_component_mode?: DrillScopedMode;
  drill_free_pad_mode?: DrillScopedMode;
  drill_via_mode?: DrillScopedMode;
  fuse_copper?: boolean;
  fuse_board_outline?: boolean;

  @extension("minimum", 1)
  arc_segments?: integer;

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
