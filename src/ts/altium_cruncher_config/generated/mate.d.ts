/** Generated from src/tsp/altium_cruncher/config/mate-config.tsp. Do not edit. */

/**
 * Current and supported legacy authored Mate inputs. Template values are not inserted by decoding.
 */
export type MateConfigInput = CurrentMate | LegacyMate;
export type CurrentMate = RecordUnknown & {
  output?: Output;
  libraries?: Libraries | null;
  known_parts?: KnownParts | null;
  pcb_designators?: Designators | null;
  artifacts?: Artifacts;
  schema: "altium_cruncher.mate.config.a0";
  source?: {
    board?: string | null;
    pcbdoc?: string | null;
    project_context?: "auto" | "none" | "schematic" | null;
  };
  validation?: Validation;
  projections?: Projection[];
  board_projection?: BoardProjection;
};
export type Output = RecordUnknown & {
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
};
export type OutputOutline = RecordUnknown & {
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
};
export type Nonnegative = number;
export type Margins = RecordUnknown & {
  left?: number;
  bottom?: number;
  right?: number;
  top?: number;
};
export type Libraries = RecordUnknown & {
  roots?: string | StringArray | null;
  recursive?: boolean | null;
};
export type StringArray = string[];
export type KnownParts = RecordUnknown & {
  manifest?: string | null;
  cache_dir?: string | null;
};
export type Designators = RecordUnknown & {
  enabled?: boolean | null;
  placement?: "above_component" | null;
  offset_mils?: Pair | null;
  width_factor?: number | null;
  style?: TextStyle;
};
/**
 * @minItems 2
 * @maxItems 2
 */
export type Pair = [number, number];
export type TextStyle = RecordUnknown & {
  height_mils?: number | null;
  layer?: string | number | null;
  /**
   * Text-kind aliases are normalized by the shared MCO text adapter, including True Type and BARCODE.
   */
  font_kind?: string | null;
  font_name?: string | null;
  bold?: boolean | null;
  italic?: boolean | null;
  stroke_width_mils?: number | null;
  text_justification?: string | number | null;
  is_inverted?: boolean | null;
  inverted_margin_mils?: number | null;
  use_inverted_rectangle?: boolean | null;
  is_frame?: boolean | null;
  header_height_mils?: number | null;
  header_stroke_width_mils?: number | null;
  rotation_degrees?: number | null;
  stroke_font_type?: string | number | null;
  is_comment?: boolean | null;
  is_designator?: boolean | null;
  is_mirrored?: boolean | null;
  barcode_kind?: string | number | null;
  barcode_render_mode?: string | number | null;
  barcode_full_size_mils?: Pair | null;
  barcode_margin_mils?: Pair | null;
  barcode_min_width_mils?: number | null;
  barcode_show_text?: boolean | null;
  barcode_inverted?: boolean | null;
};
export type Artifacts = RecordUnknown & {
  pcb_layer_step?: LayerStepArtifact | null;
};
export type LayerStepArtifact = RecordUnknown & {
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
  /**
   * Omitted or false disables the artifact, independently of generated template defaults.
   */
  enabled?: boolean | null;
  source_layer?: string | null;
  /**
   * true enables insertion; an empty object retains disabled-by-default semantics.
   */
  insert_in_output?: boolean | InsertArtifact | null;
  highlights?: Highlight[] | null;
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
export type InsertArtifact = RecordUnknown & {
  enabled?: boolean | null;
  name?: string | null;
  layer?: string | null;
  side?: string | null;
  location_mils?: Pair | null;
  z_mm?: number | null;
  rotation_z_degrees?: number | null;
  opacity?: number | null;
  bounds_mils?: Bounds | BoundsArray | null;
};
/**
 * @minItems 4
 * @maxItems 4
 */
export type BoundsArray = [number, number, number, number];
export type Highlight = RecordUnknown & {
  projection: string;
  name?: string | null;
  color?: string | null;
  z_offset_mm?: number | null;
  thickness_mm?: number | null;
};
export type Validation = RecordUnknown & {
  source_side?: "infer_single_side" | "any" | "none" | "top" | "bottom" | null;
  /**
   * Retained template field; the current parser does not consult it.
   */
  allow_side_agnostic_through_hole?: boolean | null;
  side_agnostic_kinds?: StringArray | null;
};
export type Projection = RecordUnknown & {
  id?: string | null;
  source?: SourceSelector | null;
  select?: {
    components?: SourceSelector;
    free_pads?: SourceSelector;
  };
  actions?: ProjectionAction[];
};
export type SourceSelector = RecordUnknown & {
  /**
   * Case/hyphen-normalized component(s), free_pad(s), pad(s), or drill(s).
   */
  object?: string | null;
  type?: string | null;
  kind?: string | StringArray | null;
  kinds?: string | StringArray | null;
  designators?: string | StringArray | null;
  hole_size_mils?: MilRange | null;
  plated?: boolean | null;
};
export type MilRange = RecordUnknown & {
  min?: number | null;
  max?: number | null;
};
export type ProjectionAction = ComponentAction | ReferenceAction | LabelAction;
export type ComponentAction = RecordUnknown & {
  part?: string | null;
  role?: string | null;
  description?: string | null;
  symbol_name?: string | null;
  footprint_name?: string | null;
  designator_prefix?: string | null;
  signal_pad_designator?: string | null;
  kind: "mate_component";
};
export type ReferenceAction = RecordUnknown & {
  kind: "reference_graphics";
  shape?: "source_pad_outline" | "destination_pad_outline" | null;
  layer?: string | null;
  enabled?: boolean | null;
  style?: ReferenceStyle;
};
export type ReferenceStyle = RecordUnknown & {
  mode?: string | null;
  outline_count?: number | null;
  clearance_mils?: number;
  outline_spacing_mils?: number;
  stroke_width_mils?: number;
};
export type LabelAction = RecordUnknown & {
  kind: "label";
  enabled?: boolean | null;
  style?: TextStyle | null;
  /**
   * Retained input; current label generation uses source nets.
   */
  text?: string | null;
  value?: string | null;
  placement?: LabelPlacement | null;
};
export type LabelPlacement = RecordUnknown & {
  side?: "left" | "right" | "board_left" | "board_right" | null;
  offset_mils?: Pair | null;
  box_size_mils?: Pair | null;
  center_box_on_target?: boolean | null;
  row_spacing_mils?: number | null;
  column_spacing_mils?: number | null;
  auto_width_padding_mils?: number | null;
};
export type BoardProjection = RecordUnknown & {
  outline?: {
    graphics?: Graphics;
  };
  cutouts?: {
    graphics?: Graphics;
    scope?: "all" | "interior" | null;
    actual_cutouts?: boolean | null;
    layer?: string | null;
  };
};
export type Graphics = RecordUnknown & {
  enabled?: boolean | null;
  layer?: string | null;
  stroke_width_mils?: number;
};
export type LegacyMate = RecordUnknown & {
  output?: Output;
  libraries?: Libraries | null;
  known_parts?: KnownParts | null;
  pcb_designators?: Designators | null;
  artifacts?: Artifacts;
  schema?: "altium_cruncher.mate.legacy.a0" | null;
  source?: {
    dut?: string | null;
  };
  marker?: {
    enabled?: boolean | null;
    text?: string | null;
    position_mils?: Pair | null;
    height_mils?: number | null;
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
};
export type Labels = RecordUnknown & {
  side?: "left" | "right" | "board_left" | "board_right" | null;
  offset_mils?: Pair | null;
  box_size_mils?: Pair | null;
  center_box_on_target?: boolean | null;
  row_spacing_mils?: number | null;
  column_spacing_mils?: number | null;
  auto_width_padding_mils?: number | null;
  enabled?: boolean | null;
  style?: TextStyle;
};
export type SelectedBoard = RecordUnknown & {
  board_key?: string;
  pcb_path?: string;
  components?: SelectedComponent[];
  free_pads?: SelectedPad[];
  board_outline_mils?: Bounds | null;
  board_outline?: InputOutline | null;
};
export type SelectedComponent = RecordUnknown & {
  mate_projection_id?: string | null;
  mate_part_role?: string | null;
  mate_component?: MateComponentSettings | null;
  mate_pcb_label?: Labels | null;
  mate_reference_graphics?: ReferenceGraphics | null;
  source_power_port?: InputPowerPort | null;
  source_pad_geometries?: InputPadGeometry[] | null;
  designator?: string;
  kind?: string;
  layer?: string;
  footprint?: string;
  x_mils?: number;
  y_mils?: number;
  net_name?: string | null;
};
export type MateComponentSettings = RecordUnknown & {
  kind?: "mate_component";
  part?: string | null;
  role?: string | null;
  description?: string | null;
  symbol_name?: string | null;
  footprint_name?: string | null;
  designator_prefix?: string | null;
  signal_pad_designator?: string | null;
};
export type ReferenceGraphics = RecordUnknown & {
  enabled?: boolean | null;
  layer?: string | null;
  shape?: "source_pad_outline" | "destination_pad_outline" | null;
  style?: ReferenceStyle;
};
export type InputPowerPort = RecordUnknown & {
  text?: string | null;
  style?: string | null;
  show_net_name?: boolean;
};
export type InputPadGeometry = RecordUnknown & {
  x_mils?: number;
  y_mils?: number;
  width_mils?: number;
  height_mils?: number;
  shape?: number;
  layer?: number;
  rotation_degrees?: number;
  corner_radius_mils?: number;
};
export type SelectedPad = RecordUnknown & {
  mate_projection_id?: string | null;
  mate_part_role?: string | null;
  mate_component?: MateComponentSettings | null;
  mate_pcb_label?: Labels | null;
  mate_reference_graphics?: ReferenceGraphics | null;
  source_power_port?: InputPowerPort | null;
  source_pad_geometries?: InputPadGeometry[] | null;
  designator?: string;
  kind?: string;
  x_mils?: number;
  y_mils?: number;
  net_name?: string | null;
  width_mils?: number;
  height_mils?: number;
  hole_size_mils?: number;
  shape?: number;
  layer?: number;
  rotation_degrees?: number;
};
export type InputOutline = RecordUnknown & {
  vertices: InputVertex[];
  closed?: boolean;
  cutouts?: (InputOutline | InputVertex[])[] | null;
};
export type InputVertex = RecordUnknown & {
  x_mils: number;
  y_mils: number;
  segment?: "line" | "arc" | null;
  center_mils?: Pair;
  radius_mils?: number;
  start_angle_degrees?: number;
  end_angle_degrees?: number;
};

export interface RecordUnknown {
  [k: string]: unknown;
}
export interface Bounds {
  left: number;
  bottom: number;
  right: number;
  top: number;
}
export interface Point {
  x: number;
  y: number;
}
export interface BoardOutline {
  color?: Color;
  cutout_color?: Color;
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
