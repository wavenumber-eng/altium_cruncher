import "@typespec/json-schema";
import "./mate-config-defaults.tsp";
import "./pcb-layer-step-config.tsp";
import "../outputs/mate.tsp";
using TypeSpec.JsonSchema;
using Wavenumber.AltiumCruncher.MateGeometry;
namespace Wavenumber.AltiumCruncher.MateConfigInputContract;

model NumberArray is Pair;
model StringArray is string[];
alias Names = string | StringArray | null;
@minValue(0)
scalar Nonnegative extends float64;
@minItems(4)
@maxItems(4)
model BoundsArray is float64[];
model MilRange extends Record<unknown> {
  min?: float64 | null;
  max?: float64 | null;
}
model Margins extends Record<unknown> {
  @minValue(0) left?: float64;
  @minValue(0) bottom?: float64;
  @minValue(0) right?: float64;
  @minValue(0) top?: float64;
}
model OutputOutline extends Record<unknown> {
  mode?:
    | "source_bounds"
    | "match_source_bounds"
    | "match_bounds"
    | "source_bounds_with_margin"
    | "source_bounds_plus_margin"
    | "padded_rectangle"
    | "padded_source_bounds"
    | null;
  margin_mils?: Nonnegative | Margins;
}
model Output extends Record<unknown> {
  backend?: "altium" | null;
  output_dir?: string | null;
  project_name?: string | null;
  schematic_filename?: string | null;
  schematic_sheet_style?: string | null;
  board_filename?: string | null;
  project_filename?: string | null;
  origin?: string | null;
  overwrite?: boolean | null;
  layer_stack_template?: string | null;
  board_outline?: OutputOutline | null;
  board_outline_mils?: Bounds | null;
  board_origin_mils?: Point | null;
}
model Libraries extends Record<unknown> {
  roots?: Names;
  recursive?: boolean | null;
}
model KnownParts extends Record<unknown> {
  manifest?: string | null;
  cache_dir?: string | null;
}
model TextStyle extends Record<unknown> {
  height_mils?: float64 | null;
  layer?: string | integer | null;

  @doc("Text-kind aliases are normalized by the shared MCO text adapter, including True Type and BARCODE.")
  font_kind?: string | null;

  font_name?: string | null;
  bold?: boolean | null;
  italic?: boolean | null;
  stroke_width_mils?: float64 | null;
  text_justification?: string | integer | null;
  is_inverted?: boolean | null;
  inverted_margin_mils?: float64 | null;
  use_inverted_rectangle?: boolean | null;
  is_frame?: boolean | null;
  header_height_mils?: float64 | null;
  header_stroke_width_mils?: float64 | null;
  rotation_degrees?: float64 | null;
  stroke_font_type?: string | integer | null;
  is_comment?: boolean | null;
  is_designator?: boolean | null;
  is_mirrored?: boolean | null;
  barcode_kind?: string | integer | null;
  barcode_render_mode?: string | integer | null;
  barcode_full_size_mils?: Pair | null;
  barcode_margin_mils?: Pair | null;
  barcode_min_width_mils?: float64 | null;
  barcode_show_text?: boolean | null;
  barcode_inverted?: boolean | null;
}
model LabelPlacement extends Record<unknown> {
  side?: "left" | "right" | "board_left" | "board_right" | null;
  offset_mils?: Pair | null;
  box_size_mils?: Pair | null;
  center_box_on_target?: boolean | null;
  row_spacing_mils?: float64 | null;
  column_spacing_mils?: float64 | null;
  auto_width_padding_mils?: float64 | null;
}
model Labels extends Record<unknown> {
  ...LabelPlacement;
  enabled?: boolean | null;
  style?: TextStyle;
}
model Designators extends Record<unknown> {
  enabled?: boolean | null;
  placement?: "above_component" | null;
  offset_mils?: Pair | null;
  width_factor?: float64 | null;
  style?: TextStyle;
}
model ReferenceStyle extends Record<unknown> {
  mode?: string | null;
  @extension("minimum", 1) outline_count?: integer | null;
  clearance_mils?: float64;
  outline_spacing_mils?: float64;
  stroke_width_mils?: float64;
}
model ReferenceGraphics extends Record<unknown> {
  enabled?: boolean | null;
  layer?: string | null;
  shape?: "source_pad_outline" | "destination_pad_outline" | null;
  style?: ReferenceStyle;
}
model Graphics extends Record<unknown> {
  enabled?: boolean | null;
  layer?: string | null;
  stroke_width_mils?: float64;
}
model BoardProjection extends Record<unknown> {
  outline?: {
    graphics?: Graphics;
  };
  cutouts?: {
    graphics?: Graphics;
    scope?: "all" | "interior" | null;
    actual_cutouts?: boolean | null;
    layer?: string | null;
  };
}
model Highlight extends Record<unknown> {
  `projection`: string;
  name?: string | null;
  color?: string | null;
  z_offset_mm?: float64 | null;
  thickness_mm?: float64 | null;
}
model InsertArtifact extends Record<unknown> {
  enabled?: boolean | null;
  name?: string | null;
  layer?: string | null;
  side?: string | null;
  location_mils?: Pair | null;
  z_mm?: float64 | null;
  rotation_z_degrees?: float64 | null;
  opacity?: float64 | null;
  bounds_mils?: Bounds | BoundsArray | null;
}
model LayerStepArtifact extends Record<unknown> {
  ...Wavenumber.AltiumCruncher.PcbLayerStepConfigInputContract.ExportOptions;

  @doc("Omitted or false disables the artifact, independently of generated template defaults.")
  enabled?: boolean | null;

  source_layer?: string | null;

  @doc("true enables insertion; an empty object retains disabled-by-default semantics.")
  insert_in_output?: boolean | InsertArtifact | null;

  highlights?: Highlight[] | null;
}
model Artifacts extends Record<unknown> {
  pcb_layer_step?: LayerStepArtifact | null;
}
model SourceSelector extends Record<unknown> {
  @doc("Case/hyphen-normalized component(s), free_pad(s), pad(s), or drill(s).")
  object?: string | null;

  type?: string | null;
  kind?: Names;
  kinds?: Names;
  designators?: Names;
  hole_size_mils?: MilRange | null;
  plated?: boolean | null;
}
model MateComponentSettings extends Record<unknown> {
  kind?: "mate_component";
  part?: string | null;
  role?: string | null;
  description?: string | null;
  symbol_name?: string | null;
  footprint_name?: string | null;
  designator_prefix?: string | null;
  signal_pad_designator?: string | null;
}
model ComponentAction extends Record<unknown> {
  ...OmitProperties<MateComponentSettings, "kind">;
  kind: "mate_component";
}
model ReferenceAction extends Record<unknown> {
  kind: "reference_graphics";
  shape?: "source_pad_outline" | "destination_pad_outline" | null;
  layer?: string | null;
  enabled?: boolean | null;
  style?: ReferenceStyle;
}
model LabelAction extends Record<unknown> {
  kind: "label";
  enabled?: boolean | null;
  style?: TextStyle | null;
  @doc("Retained input; current label generation uses source nets.") text?:
    | string
    | null;
  value?: string | null;
  placement?: LabelPlacement | null;
}
union ProjectionAction {
  ComponentAction,
  ReferenceAction,
  LabelAction,
}
model Projection extends Record<unknown> {
  id?: string | null;
  source?: SourceSelector | null;
  select?: {
    components?: SourceSelector;
    free_pads?: SourceSelector;
  };
  actions?: ProjectionAction[];
}
model Validation extends Record<unknown> {
  source_side?: "infer_single_side" | "any" | "none" | "top" | "bottom" | null;

  @doc("Retained template field; the current parser does not consult it.")
  allow_side_agnostic_through_hole?: boolean | null;

  side_agnostic_kinds?: StringArray | null;
}
model Shared extends Record<unknown> {
  output?: Output;
  libraries?: Libraries | null;
  known_parts?: KnownParts | null;
  pcb_designators?: Designators | null;
  artifacts?: Artifacts;
}
model CurrentMate extends Record<unknown> {
  ...Shared;
  schema: "altium_cruncher.mate.config.a0";
  source?: {
    board?: string | null;
    pcbdoc?: string | null;
    project_context?: "auto" | "none" | "schematic" | null;
  };
  validation?: Validation;
  projections?: Projection[];
  board_projection?: BoardProjection;
}
model SelectionExtras extends Record<unknown> {
  mate_projection_id?: string | null;
  mate_part_role?: string | null;
  mate_component?: MateComponentSettings | null;
  mate_pcb_label?: Labels | null;
  mate_reference_graphics?: ReferenceGraphics | null;
  source_power_port?: InputPowerPort | null;
  source_pad_geometries?: InputPadGeometry[] | null;
}
model SelectedComponent extends Record<unknown> {
  ...SelectionExtras;
  designator?: string;
  kind?: string;
  layer?: string;
  footprint?: string;
  x_mils?: float64;
  y_mils?: float64;
  net_name?: string | null;
}
model SelectedPad extends Record<unknown> {
  ...SelectionExtras;
  designator?: string;
  kind?: string;
  x_mils?: float64;
  y_mils?: float64;
  net_name?: string | null;
  width_mils?: float64;
  height_mils?: float64;
  hole_size_mils?: float64;
  shape?: integer;
  layer?: integer;
  rotation_degrees?: float64;
}
model InputPowerPort extends Record<unknown> {
  text?: string | null;
  style?: string | null;
  show_net_name?: boolean;
}
model InputPadGeometry extends Record<unknown> {
  x_mils?: float64;
  y_mils?: float64;
  width_mils?: float64;
  height_mils?: float64;
  shape?: integer;
  layer?: integer;
  rotation_degrees?: float64;
  corner_radius_mils?: float64;
}
model InputVertex extends Record<unknown> {
  x_mils: float64;
  y_mils: float64;
  segment?: "line" | "arc" | null;
  center_mils?: Pair;
  radius_mils?: float64;
  start_angle_degrees?: float64;
  end_angle_degrees?: float64;
}
model InputOutline extends Record<unknown> {
  vertices: InputVertex[];
  closed?: boolean;
  cutouts?: (InputOutline | InputVertex[])[] | null;
}
model SelectedBoard extends Record<unknown> {
  board_key?: string;
  pcb_path?: string;
  components?: SelectedComponent[];
  free_pads?: SelectedPad[];
  board_outline_mils?: Bounds | null;
  board_outline?: InputOutline | null;
}
model LegacyMate extends Record<unknown> {
  ...Shared;
  schema?: "altium_cruncher.mate.legacy.a0" | null;
  source?: {
    dut?: string | null;
  };
  marker?: {
    enabled?: boolean | null;
    text?: string | null;
    position_mils?: Pair | null;
    height_mils?: float64 | null;
    layer?: string | null;
  };
  placement?: {
    source_mount_side?: string | null;
    offset_mils?: Pair | null;
    mirror_x?: boolean | null;
    mirror_y?: boolean | null;
    mirror_origin_mils?: Pair | null;
  };
  pcb_labels?: Labels | null;
  selection?: {
    boards?: SelectedBoard[];
  };
  board_projection?: BoardProjection | null;
}
@jsonSchema
@id("https://github.com/wavenumber-eng/altium_cruncher/docs/contracts/mate_config.a0.schema.json")
@doc("Current and supported legacy authored Mate inputs. Template values are not inserted by decoding.")
union MateConfigInput {
  CurrentMate,
  LegacyMate,
}

model AuthoredKnownPart extends Record<unknown> {
  role?: string;
  description?: string | null;
  symbol_name?: string;
  symbol_library?: string;
  footprint_name?: string;
  footprint_library?: string;
  target_kinds?: Names;
  designator_prefix?: string;
  signal_pad_designator?: string | null;
}
@jsonSchema
@id("altium_cruncher.mate.parts_cache.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "mate_parts_input",
    title: "Editable mate parts",
    source: "mate-config",
    kind: "config",
  }
)
model MatePartsInput extends Record<unknown> {
  schema: "altium_cruncher.mate.parts_cache.a0";
  parts: AuthoredKnownPart[];
  source?: PartSource;
  designator_normalization?: Record<Record<string>>;
}
