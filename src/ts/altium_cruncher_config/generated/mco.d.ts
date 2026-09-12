/** Generated from src/tsp/altium_cruncher/mco/main.tsp. Do not edit. */

export type McoInput = McoDocument | (BuiltinOperation | CustomOperation)[];
export type McoDocument = RecordUnknown & {
  schema?: "altium_cruncher.mco.a0" | null;
  operations: (BuiltinOperation | CustomOperation)[];
};
export type BuiltinOperation =
  | FileCopyOperation
  | McoFailOperation
  | McoMessageOperation
  | PcbdocAddArcOperation
  | PcbdocAddComponentOperation
  | PcbdocAddEmbedded3DModelOperation
  | PcbdocAddFillOperation
  | PcbdocAddPadOperation
  | PcbdocAddRegionOperation
  | PcbdocAddTextOperation
  | PcbdocAddTrackOperation
  | PcbdocAddViaOperation
  | PcbdocArrangeDesignatorsOperation
  | PcbdocCreateOperation
  | PcbdocCreateUserUnionOperation
  | PcbdocExportLayerStepOperation
  | PcblibAddFootprintOperation
  | PcblibCreateOperation
  | ProjectAddDocumentOperation
  | ProjectAddParameterOperation
  | ProjectAddVariantOperation
  | ProjectAddVariantDnpOperation
  | ProjectCloneVariantOperation
  | ProjectCreateOperation
  | ProjectDeleteVariantOperation
  | ProjectListVariantsOperation
  | ProjectRenameVariantOperation
  | ProjectToggleVariantDnpOperation
  | SchdocAddComponentOperation
  | SchdocAddNetLabelOperation
  | SchdocAddPowerPortOperation
  | SchdocAddWireOperation
  | SchdocCreateOperation
  | SchlibAddSymbolOperation
  | SchlibCreateOperation;
export type FileCopyOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "file.copy";
  args: FileCopyArgs;
};
export type FileCopyArgs = RecordUnknown & {
  source: McoString;
  destination: McoString;
  overwrite?: boolean | null;
};
export type McoString = string;
export type McoFailOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "mco.fail" | "fail";
  args?: McoFailArgs;
};
export type McoFailArgs = RecordUnknown & {
  message?: string | null;
};
export type McoMessageOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "mco.message" | "message";
  args?: McoMessageArgs;
};
export type McoMessageArgs = RecordUnknown & {
  text?: string | null;
};
export type PcbdocAddArcOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "pcbdoc.add_arc";
  args: PcbdocAddArcArgs;
};
export type PcbdocAddArcArgs = RecordUnknown & {
  /**
   * Input Altium document path, relative to the MCO file directory.
   */
  file: string;
  /**
   * Optional output document; otherwise overwrite=true is required.
   */
  output_file?: string | null;
  /**
   * Allow overwriting the input or existing output document.
   */
  overwrite?: boolean | null;
  center_mils: PointMils;
  radius_mils: number;
  start_angle_degrees: number;
  end_angle_degrees: number;
  width_mils: number;
  layer?: string | number | null;
  net?: string | null;
};
/**
 * @minItems 2
 * @maxItems 2
 */
export type PointMils = [number, number];
export type PcbdocAddComponentOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "pcbdoc.add_component";
  args: PcbdocAddComponentArgs;
};
export type PcbdocAddComponentArgs = RecordUnknown & {
  /**
   * Input Altium document path, relative to the MCO file directory.
   */
  file: string;
  /**
   * Optional output document; otherwise overwrite=true is required.
   */
  output_file?: string | null;
  /**
   * Allow overwriting the input or existing output document.
   */
  overwrite?: boolean | null;
  library: McoString;
  footprint: McoString;
  designator: McoString;
  position_mils: PointMils;
  layer?: string | number | null;
  source_unique_id?: string | null;
  source_hierarchical_path?: string | null;
  source_component_library?: string | null;
  source_lib_reference?: string | null;
  source_description?: string | null;
  channel_offset?: number | null;
  comment_text?: string | null;
  component_parameters?: RecordString | null;
  pad_nets?: RecordString | null;
  rotation_degrees?: number | null;
  source_footprint_library?: string | null;
  comment_visible?: boolean | null;
  source_designator?: string | null;
};
export type PcbdocAddEmbedded3DModelOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "pcbdoc.add_embedded_3d_model";
  args: PcbdocAddEmbedded3DModelArgs;
};
export type PcbdocAddEmbedded3DModelArgs = RecordUnknown & {
  /**
   * Input Altium document path, relative to the MCO file directory.
   */
  file: string;
  /**
   * Optional output document; otherwise overwrite=true is required.
   */
  output_file?: string | null;
  /**
   * Allow overwriting the input or existing output document.
   */
  overwrite?: boolean | null;
  model_file: McoString;
  model_name?: string | null;
  name?: string | null;
  layer?: string | number | null;
  side?: string | number | null;
  location_mils?: PointMils | null;
  rotation_x_degrees?: number | null;
  rotation_y_degrees?: number | null;
  rotation_z_degrees?: number | null;
  z_mm?: number | null;
  bounds_mils?: BoundsObject | BoundsArray | null;
  projection_outline_mils?: RegionPoints | null;
  overall_height_mils?: number | null;
  opacity?: number | null;
  /**
   * Takes precedence over z_mm when supplied.
   */
  z_mils?: number;
};
export type BoundsObject = RecordUnknown & {
  left: number;
  bottom: number;
  right: number;
  top: number;
};
/**
 * @minItems 4
 * @maxItems 4
 */
export type BoundsArray = [number, number, number, number];
/**
 * @minItems 3
 */
export type RegionPoints = [PointMils, PointMils, PointMils, ...PointMils[]];
export type PcbdocAddFillOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "pcbdoc.add_fill";
  args: PcbdocAddFillArgs;
};
export type PcbdocAddFillArgs = RecordUnknown & {
  /**
   * Input Altium document path, relative to the MCO file directory.
   */
  file: string;
  /**
   * Optional output document; otherwise overwrite=true is required.
   */
  output_file?: string | null;
  /**
   * Allow overwriting the input or existing output document.
   */
  overwrite?: boolean | null;
  corner1_mils: PointMils;
  corner2_mils: PointMils;
  rotation_degrees?: number | null;
  layer?: string | number | null;
  net?: string | null;
};
export type PcbdocAddPadOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "pcbdoc.add_pad";
  args: PcbdocAddPadArgs;
};
export type PcbdocAddPadArgs = RecordUnknown & {
  /**
   * Input Altium document path, relative to the MCO file directory.
   */
  file: string;
  /**
   * Optional output document; otherwise overwrite=true is required.
   */
  output_file?: string | null;
  /**
   * Allow overwriting the input or existing output document.
   */
  overwrite?: boolean | null;
  designator: McoString;
  position_mils: PointMils;
  width_mils: number;
  height_mils: number;
  shape?: string | number | null;
  corner_radius_percent?: number | null;
  rotation_degrees?: number | null;
  hole_size_mils?: number | null;
  plated?: boolean | null;
  layer?: string | number | null;
  net?: string | null;
  solder_mask_expansion_mils?: number | null;
  paste_mask_expansion_mils?: number | null;
  tenting_top?: boolean | null;
  tenting_bottom?: boolean | null;
  solder_mask_expansion_mode?: number | null;
  paste_mask_expansion_mode?: number | null;
};
export type PcbdocAddRegionOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "pcbdoc.add_region";
  args: PcbdocAddRegionArgs;
};
export type PcbdocAddRegionArgs = RecordUnknown & {
  /**
   * Input Altium document path, relative to the MCO file directory.
   */
  file: string;
  /**
   * Optional output document; otherwise overwrite=true is required.
   */
  output_file?: string | null;
  /**
   * Allow overwriting the input or existing output document.
   */
  overwrite?: boolean | null;
  outline_points_mils: RegionPoints;
  layer?: string | number | null;
  hole_points_mils?: PointMils[][] | null;
  is_keepout?: boolean | null;
  keepout_restrictions?: number | null;
  net?: string | null;
  is_board_cutout?: boolean | null;
};
export type PcbdocAddTextOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "pcbdoc.add_text";
  args: PcbdocAddTextArgs;
};
export type PcbdocAddTextArgs = RecordUnknown & {
  /**
   * Input Altium document path, relative to the MCO file directory.
   */
  file: string;
  /**
   * Optional output document; otherwise overwrite=true is required.
   */
  output_file?: string | null;
  /**
   * Allow overwriting the input or existing output document.
   */
  overwrite?: boolean | null;
  text: McoString;
  position_mils: PointMils;
  layer?: string | number | null;
  height_mils: number;
  font_kind?: string | null;
  font_name?: string | null;
  bold?: boolean | null;
  italic?: boolean | null;
  rotation_degrees?: number | null;
  stroke_width_mils?: number | null;
  is_comment?: boolean | null;
  is_designator?: boolean | null;
  is_mirrored?: boolean | null;
  is_inverted?: boolean | null;
  inverted_margin_mils?: number | null;
  use_inverted_rectangle?: boolean | null;
  inverted_rectangle_size_mils?: PointMils | null;
  is_frame?: boolean | null;
  frame_size_mils?: PointMils | null;
  barcode_full_size_mils?: PointMils | null;
  barcode_margin_mils?: PointMils | null;
  barcode_min_width_mils?: number | null;
  barcode_show_text?: boolean | null;
  barcode_inverted?: boolean | null;
  text_justification?: string | number | null;
  barcode_kind?: string | number | null;
  barcode_render_mode?: string | number | null;
};
export type PcbdocAddTrackOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "pcbdoc.add_track";
  args: PcbdocAddTrackArgs;
};
export type PcbdocAddTrackArgs = RecordUnknown & {
  /**
   * Input Altium document path, relative to the MCO file directory.
   */
  file: string;
  /**
   * Optional output document; otherwise overwrite=true is required.
   */
  output_file?: string | null;
  /**
   * Allow overwriting the input or existing output document.
   */
  overwrite?: boolean | null;
  start_mils: PointMils;
  end_mils: PointMils;
  width_mils: number;
  layer?: string | number | null;
  net?: string | null;
};
export type PcbdocAddViaOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "pcbdoc.add_via";
  args: PcbdocAddViaArgs;
};
export type PcbdocAddViaArgs = RecordUnknown & {
  /**
   * Input Altium document path, relative to the MCO file directory.
   */
  file: string;
  /**
   * Optional output document; otherwise overwrite=true is required.
   */
  output_file?: string | null;
  /**
   * Allow overwriting the input or existing output document.
   */
  overwrite?: boolean | null;
  position_mils: PointMils;
  diameter_mils: number;
  hole_size_mils: number;
  layer_start?: string | number | null;
  layer_end?: string | number | null;
  net?: string | null;
};
export type PcbdocArrangeDesignatorsOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "pcbdoc.arrange_designators";
  args: PcbdocArrangeDesignatorsArgs;
};
export type PcbdocArrangeDesignatorsArgs = RecordUnknown & {
  /**
   * Input Altium document path, relative to the MCO file directory.
   */
  file: string;
  /**
   * Optional output document; otherwise overwrite=true is required.
   */
  output_file?: string | null;
  /**
   * Allow overwriting the input or existing output document.
   */
  overwrite?: boolean | null;
  designators?: McoString[] | null;
  placement?: string | null;
  offset_mils?: PointMils | null;
  height_mils?: number | null;
  layer?: string | number | null;
  stroke_width_mils?: number | null;
  width_factor?: number | null;
  bold?: boolean | null;
  italic?: boolean | null;
  font_name?: string | null;
  font_kind?: string | null;
};
export type PcbdocCreateOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "pcbdoc.create";
  args: PcbdocCreateArgs;
};
export type PcbdocCreateArgs = RecordUnknown & {
  file: McoString;
  layer_stack_template?: string | null;
  rigid_stack?: RigidLayerStack | null;
  stackupx_file?: McoString | null;
  board_outline_mils?: BoardOutlineMils | null;
  board_origin_mils?: OriginMils | null;
  sheet_frame_mils?: SheetFrameMils | null;
  mechanical_layer_profile?: string | null;
  mechanical_layers?: McoMechanicalLayer[] | null;
  mechanical_layer_pairs?: McoMechanicalPair[] | null;
  mechanical_layer_kinds?: McoMechanicalKind[] | null;
  overwrite?: boolean | null;
};
export type RigidLayerStack = RecordUnknown & {
  /**
   * Layer-stack generation mode. Omission or null uses generated_rigid.
   */
  mode?: "generated_rigid" | null;
  name?: string | null;
  /**
   * Copper layers in top-to-bottom order.
   *
   * @minItems 2
   */
  copper_layers: [CopperLayer, CopperLayer, ...CopperLayer[]];
  /**
   * Dielectric layers between adjacent copper layers.
   */
  dielectrics_between: DielectricLayer[];
};
export type CopperLayer = RecordUnknown & {
  /**
   * Copper layer display name.
   */
  name: string;
  /**
   * Copper thickness in mils.
   */
  copper_thickness_mils?: number | null;
  /**
   * Historical extension field; ignored by creation. Use copper_thickness_mils.
   */
  thickness_mils?: {
    [k: string]: unknown;
  };
  /**
   * Optional native component-placement enum id.
   */
  component_placement?: number | null;
  /**
   * Optional native copper-orientation enum id.
   */
  copper_orientation?: number | null;
} & {
  /**
   * Copper layer display name.
   */
  name: string;
  /**
   * Copper thickness in mils.
   */
  copper_thickness_mils?: number | null;
  /**
   * Historical extension field; ignored by creation. Use copper_thickness_mils.
   */
  thickness_mils?: {
    [k: string]: unknown;
  };
  /**
   * Optional native component-placement enum id.
   */
  component_placement?: number | null;
  /**
   * Optional native copper-orientation enum id.
   */
  copper_orientation?: number | null;
} & {
  /**
   * Copper layer display name.
   */
  name: string;
  /**
   * Copper thickness in mils.
   */
  copper_thickness_mils?: number | null;
  /**
   * Historical extension field; ignored by creation. Use copper_thickness_mils.
   */
  thickness_mils?: {
    [k: string]: unknown;
  };
  /**
   * Optional native component-placement enum id.
   */
  component_placement?: number | null;
  /**
   * Optional native copper-orientation enum id.
   */
  copper_orientation?: number | null;
};
export type DielectricLayer = RecordUnknown & {
  name: NonemptyString;
  material: NonemptyString;
  thickness_mils: number;
  dielectric_constant: number;
  /**
   * Historical extension field; ignored by creation. Use dielectric_constant.
   */
  dk?: {
    [k: string]: unknown;
  };
  dielectric_type?: number | null;
  /**
   * Historical extension field; ignored by creation. Use dielectric_type.
   */
  type_code?: {
    [k: string]: unknown;
  };
  loss_tangent?: number | null;
};
export type NonemptyString = string;
export type BoardOutlineMils = RecordUnknown & {
  left: number | boolean;
  bottom: number | boolean;
  right: number | boolean;
  top: number | boolean;
};
export type OriginMils = RecordUnknown & {
  x: number | boolean;
  y: number | boolean;
};
export type SheetFrameMils = RecordUnknown & {
  x: number | boolean;
  y: number | boolean;
  width: number | boolean;
  height: number | boolean;
};
export type McoMechanicalLayer = RecordUnknown & {
  layer: McoString;
  name?: string | null;
  enabled?: boolean | null;
};
export type McoMechanicalPair = RecordUnknown & {
  layer_1: McoString;
  layer_2: McoString;
  /**
   * Defaults to the row's zero-based source index.
   */
  pair_index?: number | null;
};
export type McoMechanicalKind = RecordUnknown & {
  layer: McoString;
  kind: string | number | boolean;
};
export type PcbdocCreateUserUnionOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "pcbdoc.create_user_union";
  args: PcbdocCreateUserUnionArgs;
};
export type PcbdocCreateUserUnionArgs = RecordUnknown & {
  /**
   * Input Altium document path, relative to the MCO file directory.
   */
  file: string;
  /**
   * Optional output document; otherwise overwrite=true is required.
   */
  output_file?: string | null;
  /**
   * Allow overwriting the input or existing output document.
   */
  overwrite?: boolean | null;
  name: McoString;
  members?: "all" | null;
};
export type PcbdocExportLayerStepOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "pcbdoc.export_layer_step";
  args: PcbdocExportLayerStepArgs;
};
export type PcbdocExportLayerStepArgs = RecordUnknown & {
  file: McoString;
  output_file: McoString;
  /**
   * Delegated to PcbLayerStepConfig along with additional fixture options; see pcb-layer-step configuration.
   */
  layer?: string | number | null;
  board_name?: string | null;
  highlights?: LayerStepHighlight[] | null;
  overwrite?: boolean | null;
};
export type LayerStepHighlight = RecordUnknown & {
  id: McoString;
  name?: string | null;
  color: McoString;
  /**
   * Geometry records consumed by the existing STEP exporter; non-object entries are ignored.
   */
  pad_geometries?: unknown[];
  z_offset_mm?: number | null;
  thickness_mm?: number | null;
};
export type PcblibAddFootprintOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "pcblib.add_footprint";
  args: PcblibAddFootprintArgs;
};
export type PcblibAddFootprintArgs = RecordUnknown & {
  /**
   * Input Altium document path, relative to the MCO file directory.
   */
  file: string;
  /**
   * Optional output document; otherwise overwrite=true is required.
   */
  output_file?: string | null;
  /**
   * Allow overwriting the input or existing output document.
   */
  overwrite?: boolean | null;
  name: McoString;
  height?: string | null;
  description?: string | null;
  item_guid?: string | null;
  revision_guid?: string | null;
  parameters?: RecordString | null;
  primitive_parameters?: RecordString | null;
};
export type PcblibCreateOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "pcblib.create";
  args: PcblibCreateArgs;
};
export type PcblibCreateArgs = RecordUnknown & {
  file: McoString;
  overwrite?: boolean | null;
};
export type ProjectAddDocumentOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "project.add_document";
  args: ProjectAddDocumentArgs;
};
export type ProjectAddDocumentArgs = RecordUnknown & {
  file: McoString;
  document: McoString;
  unique_id?: string | null;
};
export type ProjectAddParameterOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "project.add_parameter";
  args: ProjectAddParameterArgs;
};
export type ProjectAddParameterArgs = RecordUnknown & {
  file: McoString;
  name: McoString;
  value: McoString;
};
export type ProjectAddVariantOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "project.add_variant";
  args: ProjectAddVariantArgs;
};
export type ProjectAddVariantArgs = RecordUnknown & {
  file: McoString;
  name: McoString;
  unique_id?: string | null;
  allow_fabrication?: boolean | null;
  current?: boolean | null;
};
export type ProjectAddVariantDnpOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "project.add_variant_dnp";
  args: ProjectAddVariantDnpArgs;
};
export type ProjectAddVariantDnpArgs = RecordUnknown & {
  file: McoString;
  variant: McoString;
  designator: McoString;
  unique_id?: string | null;
  alternate_part?: string | null;
};
export type ProjectCloneVariantOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "project.clone_variant";
  args: ProjectCloneVariantArgs;
};
export type ProjectCloneVariantArgs = RecordUnknown & {
  file: McoString;
  source_name: McoString;
  name: McoString;
  unique_id?: string | null;
  allow_fabrication?: boolean | null;
  current?: boolean | null;
};
export type ProjectCreateOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "project.create";
  args: ProjectCreateArgs;
};
export type ProjectCreateArgs = RecordUnknown & {
  file: McoString;
  name?: string | null;
  project_name?: string | null;
  overwrite?: boolean | null;
};
export type ProjectDeleteVariantOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "project.delete_variant";
  args: ProjectDeleteVariantArgs;
};
export type ProjectDeleteVariantArgs = RecordUnknown & {
  file: McoString;
  name: McoString;
};
export type ProjectListVariantsOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "project.list_variants";
  args: ProjectListVariantsArgs;
};
export type ProjectListVariantsArgs = RecordUnknown & {
  file: McoString;
};
export type ProjectRenameVariantOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "project.rename_variant";
  args: ProjectRenameVariantArgs;
};
export type ProjectRenameVariantArgs = RecordUnknown & {
  file: McoString;
  name: McoString;
  new_name: McoString;
};
export type ProjectToggleVariantDnpOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "project.toggle_variant_dnp";
  args: ProjectToggleVariantDnpArgs;
};
export type ProjectToggleVariantDnpArgs = RecordUnknown & {
  file: McoString;
  variant: McoString;
  designator: McoString;
  unique_id?: string | null;
  alternate_part?: string | null;
};
export type SchdocAddComponentOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "schdoc.add_component";
  args: SchdocAddComponentArgs;
};
export type SchdocAddComponentArgs = RecordUnknown & {
  /**
   * Input Altium document path, relative to the MCO file directory.
   */
  file: string;
  /**
   * Optional output document; otherwise overwrite=true is required.
   */
  output_file?: string | null;
  /**
   * Allow overwriting the input or existing output document.
   */
  overwrite?: boolean | null;
  library: McoString;
  symbol: McoString;
  designator: McoString;
  position_mils: PointMils;
  unique_id?: string | null;
  design_item_id?: string | null;
  footprint_model?: string | null;
  footprint_library?: string | null;
  parameters?: RecordString | null;
  orientation?: number | null;
  mirrored?: boolean | null;
  part_id?: number | null;
  display_mode?: number | null;
  designator_style?: SchematicTextStyle | null;
  comment_style?: SchematicTextStyle | null;
  footprint_description?: string | null;
};
export type SchematicTextStyle = RecordUnknown & {
  position_mils?: PointMils | null;
  font_name?: string | null;
  font_size?: number | null;
  /**
   * Default is true for designator style and false for comment style.
   */
  bold?: boolean | null;
  justification?: string | number | null;
  /**
   * Explicit hidden takes precedence over visible.
   */
  hidden?: boolean | null;
  visible?: boolean | null;
};
export type SchdocAddNetLabelOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "schdoc.add_net_label";
  args: SchdocAddNetLabelArgs;
};
export type SchdocAddNetLabelArgs = RecordUnknown & {
  /**
   * Input Altium document path, relative to the MCO file directory.
   */
  file: string;
  /**
   * Optional output document; otherwise overwrite=true is required.
   */
  output_file?: string | null;
  /**
   * Allow overwriting the input or existing output document.
   */
  overwrite?: boolean | null;
  text: McoString;
  location_mils: PointMils;
  orientation?: string | number | null;
  justification?: string | number;
};
export type SchdocAddPowerPortOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "schdoc.add_power_port";
  args: SchdocAddPowerPortArgs;
};
export type SchdocAddPowerPortArgs = RecordUnknown & {
  /**
   * Input Altium document path, relative to the MCO file directory.
   */
  file: string;
  /**
   * Optional output document; otherwise overwrite=true is required.
   */
  output_file?: string | null;
  /**
   * Allow overwriting the input or existing output document.
   */
  overwrite?: boolean | null;
  text: McoString;
  location_mils: PointMils;
  style?: string | number;
  orientation?: string | number | null;
  show_net_name?: boolean | null;
};
export type SchdocAddWireOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "schdoc.add_wire";
  args: SchdocAddWireArgs;
};
export type SchdocAddWireArgs = RecordUnknown & {
  /**
   * Input Altium document path, relative to the MCO file directory.
   */
  file: string;
  /**
   * Optional output document; otherwise overwrite=true is required.
   */
  output_file?: string | null;
  /**
   * Allow overwriting the input or existing output document.
   */
  overwrite?: boolean | null;
  points_mils: WirePoints;
};
/**
 * @minItems 2
 */
export type WirePoints = [PointMils, PointMils, ...PointMils[]];
export type SchdocCreateOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "schdoc.create";
  args: SchdocCreateArgs;
};
export type SchdocCreateArgs = RecordUnknown & {
  file: McoString;
  template?: McoString | null;
  sheet_style?: string | null;
  apply_template_visual_sheet_settings?: boolean | null;
  custom_sheet_mils?: CustomSheetMils | null;
  overwrite?: boolean | null;
};
export type CustomSheetMils = RecordUnknown & {
  /**
   * Custom sheet width in mils.
   */
  width: number | boolean;
  /**
   * Custom sheet height in mils.
   */
  height: number | boolean;
};
export type SchlibAddSymbolOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "schlib.add_symbol";
  args: SchlibAddSymbolArgs;
};
export type SchlibAddSymbolArgs = RecordUnknown & {
  file: McoString;
  name: McoString;
  description?: string | null;
};
export type SchlibCreateOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: "schlib.create";
  args: SchlibCreateArgs;
};
export type SchlibCreateArgs = RecordUnknown & {
  file: McoString;
  overwrite?: boolean | null;
};
export type CustomOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  /**
   * Custom registry operation name; built-in names are excluded during generation.
   */
  op: string;
  args?: RecordUnknown;
};

export interface RecordUnknown {
  [k: string]: unknown;
}
export interface RecordString {
  [k: string]: string;
}
