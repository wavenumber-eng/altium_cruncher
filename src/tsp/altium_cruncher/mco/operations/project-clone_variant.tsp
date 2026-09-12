import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model ProjectCloneVariantArgs extends Record<unknown> {
  file: McoString;
  source_name: McoString;
  name: McoString;
  unique_id?: string | null = null;
  allow_fabrication?: boolean | null;
  current?: boolean | null = false;
}

@extension(
  "x-acr-operation",
  #{
    name: "project.clone_variant",
    group: "project",
    summary: "Clone an existing project variant under a new name.",
  }
)
model ProjectCloneVariantOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "project.clone_variant";
  args: ProjectCloneVariantArgs;
}
