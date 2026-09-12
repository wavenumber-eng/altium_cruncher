/** Generated from src/tsp/altium_cruncher/config/creation.tsp. Do not edit. */

export type ProjectSkeletonConfigInput = RecordUnknown & {
  /**
   * Project skeleton config contract id.
   */
  schema: "altium_cruncher.project_skeleton.a0";
  project: ProjectOutput;
  /**
   * SchDoc sheets to create and add to the project. Empty creates no sheets.
   */
  schematics: SchdocChild[];
  /**
   * Optional PcbDoc output; null creates no board.
   */
  pcb?: PcbdocChild | null;
};
/**
 * PrjPcb output and project-level parameters.
 */
export type ProjectOutput = RecordUnknown & {
  /**
   * PrjPcb file to create, relative to this config file unless absolute.
   */
  file: string;
  /**
   * Project display name; omission, null or empty derives it from the file.
   */
  name?: string | null;
  parameters?: RecordUnknown1;
};
export type SchdocChild = RecordUnknown & {
  /**
   * SchDoc file to create, relative to this config file unless absolute.
   */
  file: string;
  /**
   * Altium SheetStyle enum name or native integer id. Falsy input uses D.
   */
  sheet_style?: string | number | boolean | null;
  /**
   * Optional SchDot template file to copy settings from.
   */
  template?: NonemptyString | null;
  /**
   * Whether to copy visual sheet settings from the template; legacy JSON truthiness is preserved. Prefer true or false.
   */
  apply_template_visual_sheet_settings?: boolean | string | number | null | unknown[] | RecordUnknown;
  /**
   * Optional explicit sheet size in mils.
   */
  custom_sheet_mils?: CustomSheetMils | null;
};
export type NonemptyString = string;
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
export type PcbdocChild = RecordUnknown & {
  /**
   * PcbDoc file to create, relative to this config file unless absolute.
   */
  file: string;
  /**
   * Optional rectangular board outline in mils.
   */
  board_outline_mils?: BoardOutlineMils | null;
  /**
   * Generated rigid stack; use only one layer-stack input.
   */
  layer_stack?: RigidLayerStack | null;
  /**
   * Named layer-stack template; defaults to 2-layer when no stack input is supplied.
   */
  layer_stack_template?: string | null;
  /**
   * Optional .stackupx path to import as the PcbDoc layer-stack document.
   */
  stackupx_file?: NonemptyString | null;
  /**
   * Optional profile; case, surrounding whitespace and hyphen aliases are accepted.
   */
  mechanical_layer_profile?:
    | (
        | "none"
        | ""
        | "standard_component_pairs"
        | "standard-component-pairs"
        | "v7_mechanical_53"
        | "v7-mechanical-53"
        | null
      )
    | string;
  mechanical_layers?: MechanicalLayer[] | null;
  mechanical_layer_pairs?: (GroupedMechanicalPair | FlatMechanicalPair)[] | null;
  mechanical_layer_kinds?: MechanicalKind[] | null;
};
export type BoardOutlineMils = RecordUnknown & {
  left: number | boolean;
  bottom: number | boolean;
  right: number | boolean;
  top: number | boolean;
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
export type MechanicalLayer = RecordUnknown & {
  layer: NonemptyString;
  name?: NonemptyString | null;
  enabled?: boolean | string | number | null | unknown[] | RecordUnknown;
  kind?: NonemptyString | null;
};
export type GroupedMechanicalPair = RecordUnknown & {
  top: MechanicalPairSide;
  bottom: MechanicalPairSide;
};
export type MechanicalPairSide = RecordUnknown & {
  layer: NonemptyString;
  name?: NonemptyString | null;
  enabled?: boolean | string | number | null | unknown[] | RecordUnknown;
  kind: NonemptyString;
};
export type FlatMechanicalPair = RecordUnknown & {
  layer_1: NonemptyString;
  layer_2: NonemptyString;
  pair_index?: number | null;
  top?: never;
  bottom?: never;
};
export type MechanicalKind = RecordUnknown & {
  layer: NonemptyString;
  kind: NonemptyString | number;
};

export interface RecordUnknown {
  [k: string]: unknown;
}
/**
 * Project parameters; the Python adapter converts authored values to strings.
 */
export interface RecordUnknown1 {
  [k: string]: unknown;
}
