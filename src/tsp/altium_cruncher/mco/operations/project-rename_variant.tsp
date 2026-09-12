import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model ProjectRenameVariantArgs extends Record<unknown> {
  file: McoString;
  name: McoString;
  new_name: McoString;
}

@extension(
  "x-acr-operation",
  #{
    name: "project.rename_variant",
    group: "project",
    summary: "Rename one project variant.",
  }
)
model ProjectRenameVariantOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "project.rename_variant";
  args: ProjectRenameVariantArgs;
}
