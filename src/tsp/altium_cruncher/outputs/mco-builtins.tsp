import "@typespec/json-schema";
import "./commands.tsp";
using TypeSpec.JsonSchema;
using Wavenumber.AltiumCruncher.CommandOutputs;
namespace Wavenumber.AltiumCruncher.McoBuiltinOutputs;

@minItems(2)
@maxItems(2)
model Pair is float64[];
model ProjectPath {
  project: string;
}
model NamedProject {
  ...ProjectPath;
  name: string;
}
model SectionProject {
  ...NamedProject;
  section: string;
}
model FilePath {
  file: string;
}
model TextOutput {
  ...FilePath;
  text: string;
}
model DnpAdded {
  ...ProjectPath;
  variant: string;
  designator: string;
  unique_id: string;
  variation: string;
}
model ToggleAdded {
  ...DnpAdded;
  action: "added";
  dnp: true;
}
model ToggleRemoved {
  ...ProjectPath;
  variant: string;
  designator: string;
  action: "removed";
  dnp: false;
}
model ArrangeDone {
  ...FilePath;
  updated: integer;
}
model ArrangeDryRun {
  ...FilePath;
  designators: integer | "all";
  placement: string;
}
model UnionDone {
  ...FilePath;
  name: string;
  union_index: integer;
  member_count: integer;
}
model UnionDryRun {
  ...FilePath;
  name: string;
}
model StepExport {
  ...FilePath;
  step_file: string;
  manifest_file: string;
  highlight_count: integer;
  layer?: string;
}
model EmbeddedModel {
  ...FilePath;
  model_file: string;
  name: string;
  z_mils?: float64;
}
model TextDryRun {
  ...TextOutput;
  font_kind: string;
  text_justification: string | integer | null;
}
model Result<Operation extends string, Output> {
  `op`: Operation;
  id: string;
  status: "ok";
  message: string;
  outputs: Output;
}
model Failure {
  `op`: string;
  id: string;
  status: "fail";
  message: string;
  outputs: {};
  error?: string;
}

@jsonSchema
@id("altium_cruncher.mco.builtin_result.a0")
@doc("Explicit default-registry result contract, including dry-run shapes and flush failures. Use the generic execution contract for custom registries, which may replace even a built-in operation name. No new wire tag is inserted.")
@extension(
  "x-acr-contract",
  #{
    stem: "mco_builtin_result",
    title: "Built-in MCO operation results",
    source: "../outputs/mco-builtins",
    kind: "output",
  }
)
union McoBuiltinResult {
  Failure,
  Result<"mco.message" | "message", {}>,
  Result<"project.create", ProjectPath>,
  Result<
    "project.add_document",
    {
      ...ProjectPath,
      document: string,
    }
  >,
  Result<"project.add_parameter" | "project.add_variant", NamedProject>,
  Result<"project.list_variants", VariantsList>,
  Result<"project.delete_variant", SectionProject>,
  Result<
    "project.rename_variant",
    {
      ...SectionProject,
      new_name: string,
    }
  >,
  Result<
    "project.clone_variant",
    {
      ...SectionProject,
      source_name: string,
      unique_id: string,
    }
  >,
  Result<"project.add_variant_dnp", DnpAdded>,
  Result<"project.toggle_variant_dnp", ToggleAdded | ToggleRemoved>,
  Result<
    "schdoc.create",
    {
      schematic: string,
    }
  >,
  Result<
    "pcbdoc.create",
    {
      board: string,
    }
  >,
  Result<
    "schlib.create" | "pcblib.create",
    {
      library: string,
    }
  >,
  Result<
    "schlib.add_symbol",
    {
      library: string,
      symbol: string,
    }
  >,
  Result<
    "file.copy",
    {
      source: string,
      destination: string,
    }
  >,
  Result<
    "schdoc.add_wire",
    {
      ...FilePath,
      points: integer,
    }
  >,
  Result<"schdoc.add_net_label" | "schdoc.add_power_port", TextOutput>,
  Result<"pcbdoc.add_text", TextOutput | TextDryRun>,
  Result<
    "schdoc.add_component",
    {
      ...FilePath,
      library: string,
      symbol: string,
      designator: string,
    }
  >,
  Result<
    "pcbdoc.add_component",
    {
      ...FilePath,
      library: string,
      footprint: string,
      designator: string,
    }
  >,
  Result<
    "pcblib.add_footprint",
    {
      ...FilePath,
      footprint: string,
      parameters: integer,
      primitive_parameters: integer,
    }
  >,
  Result<"pcbdoc.arrange_designators", ArrangeDone | ArrangeDryRun>,
  Result<
    "pcbdoc.add_track",
    {
      ...FilePath,
      width_mils: float64,
    }
  >,
  Result<
    "pcbdoc.add_arc",
    {
      ...FilePath,
      radius_mils: float64,
    }
  >,
  Result<
    "pcbdoc.add_pad",
    {
      ...FilePath,
      designator: string,
    }
  >,
  Result<
    "pcbdoc.add_via",
    {
      ...FilePath,
      position_mils: Pair,
    }
  >,
  Result<
    "pcbdoc.add_fill",
    {
      ...FilePath,
      corner1_mils: Pair,
    }
  >,
  Result<
    "pcbdoc.add_region",
    {
      ...FilePath,
      points: integer,
      is_board_cutout: boolean,
    }
  >,
  Result<"pcbdoc.create_user_union", UnionDone | UnionDryRun>,
  Result<"pcbdoc.export_layer_step", StepExport>,
  Result<"pcbdoc.add_embedded_3d_model", EmbeddedModel>,
}
