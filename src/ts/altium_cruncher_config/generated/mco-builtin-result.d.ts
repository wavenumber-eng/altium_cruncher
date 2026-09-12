/** Generated from src/tsp/altium_cruncher/outputs/mco-builtins.tsp. Do not edit. */

/**
 * Explicit default-registry result contract, including dry-run shapes and flush failures. Use the generic execution contract for custom registries, which may replace even a built-in operation name. No new wire tag is inserted.
 */
export type McoBuiltinResult =
  | Failure
  | {
      op: "mco.message" | "message";
      id: string;
      status: "ok";
      message: string;
      outputs: {};
    }
  | {
      op: "project.create";
      id: string;
      status: "ok";
      message: string;
      outputs: ProjectPath;
    }
  | {
      op: "project.add_document";
      id: string;
      status: "ok";
      message: string;
      outputs: {
        project: string;
        document: string;
      };
    }
  | {
      op: "project.add_parameter" | "project.add_variant";
      id: string;
      status: "ok";
      message: string;
      outputs: NamedProject;
    }
  | {
      op: "project.list_variants";
      id: string;
      status: "ok";
      message: string;
      outputs: ImportedVariantsList;
    }
  | {
      op: "project.delete_variant";
      id: string;
      status: "ok";
      message: string;
      outputs: SectionProject;
    }
  | {
      op: "project.rename_variant";
      id: string;
      status: "ok";
      message: string;
      outputs: {
        project: string;
        name: string;
        section: string;
        new_name: string;
      };
    }
  | {
      op: "project.clone_variant";
      id: string;
      status: "ok";
      message: string;
      outputs: {
        project: string;
        name: string;
        section: string;
        source_name: string;
        unique_id: string;
      };
    }
  | {
      op: "project.add_variant_dnp";
      id: string;
      status: "ok";
      message: string;
      outputs: DnpAdded;
    }
  | {
      op: "project.toggle_variant_dnp";
      id: string;
      status: "ok";
      message: string;
      outputs: ToggleAdded | ToggleRemoved;
    }
  | {
      op: "schdoc.create";
      id: string;
      status: "ok";
      message: string;
      outputs: {
        schematic: string;
      };
    }
  | {
      op: "pcbdoc.create";
      id: string;
      status: "ok";
      message: string;
      outputs: {
        board: string;
      };
    }
  | {
      op: "schlib.create" | "pcblib.create";
      id: string;
      status: "ok";
      message: string;
      outputs: {
        library: string;
      };
    }
  | {
      op: "schlib.add_symbol";
      id: string;
      status: "ok";
      message: string;
      outputs: {
        library: string;
        symbol: string;
      };
    }
  | {
      op: "file.copy";
      id: string;
      status: "ok";
      message: string;
      outputs: {
        source: string;
        destination: string;
      };
    }
  | {
      op: "schdoc.add_wire";
      id: string;
      status: "ok";
      message: string;
      outputs: {
        file: string;
        points: number;
      };
    }
  | {
      op: "schdoc.add_net_label" | "schdoc.add_power_port";
      id: string;
      status: "ok";
      message: string;
      outputs: TextOutput;
    }
  | {
      op: "pcbdoc.add_text";
      id: string;
      status: "ok";
      message: string;
      outputs: TextOutput | TextDryRun;
    }
  | {
      op: "schdoc.add_component";
      id: string;
      status: "ok";
      message: string;
      outputs: {
        file: string;
        library: string;
        symbol: string;
        designator: string;
      };
    }
  | {
      op: "pcbdoc.add_component";
      id: string;
      status: "ok";
      message: string;
      outputs: {
        file: string;
        library: string;
        footprint: string;
        designator: string;
      };
    }
  | {
      op: "pcblib.add_footprint";
      id: string;
      status: "ok";
      message: string;
      outputs: {
        file: string;
        footprint: string;
        parameters: number;
        primitive_parameters: number;
      };
    }
  | {
      op: "pcbdoc.arrange_designators";
      id: string;
      status: "ok";
      message: string;
      outputs: ArrangeDone | ArrangeDryRun;
    }
  | {
      op: "pcbdoc.add_track";
      id: string;
      status: "ok";
      message: string;
      outputs: {
        file: string;
        width_mils: number;
      };
    }
  | {
      op: "pcbdoc.add_arc";
      id: string;
      status: "ok";
      message: string;
      outputs: {
        file: string;
        radius_mils: number;
      };
    }
  | {
      op: "pcbdoc.add_pad";
      id: string;
      status: "ok";
      message: string;
      outputs: {
        file: string;
        designator: string;
      };
    }
  | {
      op: "pcbdoc.add_via";
      id: string;
      status: "ok";
      message: string;
      outputs: {
        file: string;
        position_mils: Pair;
      };
    }
  | {
      op: "pcbdoc.add_fill";
      id: string;
      status: "ok";
      message: string;
      outputs: {
        file: string;
        corner1_mils: Pair;
      };
    }
  | {
      op: "pcbdoc.add_region";
      id: string;
      status: "ok";
      message: string;
      outputs: {
        file: string;
        points: number;
        is_board_cutout: boolean;
      };
    }
  | {
      op: "pcbdoc.create_user_union";
      id: string;
      status: "ok";
      message: string;
      outputs: UnionDone | UnionDryRun;
    }
  | {
      op: "pcbdoc.export_layer_step";
      id: string;
      status: "ok";
      message: string;
      outputs: StepExport;
    }
  | {
      op: "pcbdoc.add_embedded_3d_model";
      id: string;
      status: "ok";
      message: string;
      outputs: EmbeddedModel;
    };
export type ImportedVariantsList_Count = number;
/**
 * @minItems 2
 * @maxItems 2
 */
export type Pair = [number, number];

export interface Failure {
  op: string;
  id: string;
  status: "fail";
  message: string;
  outputs: {};
  error?: string;
}
export interface ProjectPath {
  project: string;
}
export interface NamedProject {
  project: string;
  name: string;
}
export interface ImportedVariantsList {
  schema: "altium_cruncher.variants.list.a0";
  project: string;
  current_variant: string | null;
  variant_count: ImportedVariantsList_Count;
  variants: ImportedVariantsList_Variant[];
  rows: ImportedVariantsList_VariantRow[];
  index_errors: string[];
}
export interface ImportedVariantsList_Variant {
  name: string;
  unique_id: string;
  allow_fabrication: boolean;
  current: boolean;
  dnp: string[];
  variation_count: ImportedVariantsList_Count;
  parameter_count: ImportedVariantsList_Count;
  param_variation_count: ImportedVariantsList_Count;
  rows: ImportedVariantsList_VariantRow[];
}
export interface ImportedVariantsList_VariantRow {
  variant: string;
  sheet: string;
  designator: string;
  operation: string;
  detail: string;
  component_value: string;
  parameter_name: string;
  value: string;
  unique_id: string;
  alternate_part?: string;
  alternate_part_resolved?: string;
}
export interface SectionProject {
  project: string;
  name: string;
  section: string;
}
export interface DnpAdded {
  project: string;
  variant: string;
  designator: string;
  unique_id: string;
  variation: string;
}
export interface ToggleAdded {
  project: string;
  variant: string;
  designator: string;
  unique_id: string;
  variation: string;
  action: "added";
  dnp: true;
}
export interface ToggleRemoved {
  project: string;
  variant: string;
  designator: string;
  action: "removed";
  dnp: false;
}
export interface TextOutput {
  file: string;
  text: string;
}
export interface TextDryRun {
  file: string;
  text: string;
  font_kind: string;
  text_justification: string | number | null;
}
export interface ArrangeDone {
  file: string;
  updated: number;
}
export interface ArrangeDryRun {
  file: string;
  designators: number | "all";
  placement: string;
}
export interface UnionDone {
  file: string;
  name: string;
  union_index: number;
  member_count: number;
}
export interface UnionDryRun {
  file: string;
  name: string;
}
export interface StepExport {
  file: string;
  step_file: string;
  manifest_file: string;
  highlight_count: number;
  layer?: string;
}
export interface EmbeddedModel {
  file: string;
  model_file: string;
  name: string;
  z_mils?: number;
}
