import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model ProjectDeleteVariantArgs extends Record<unknown> {
  file: McoString;
  name: McoString;
}

@extension(
  "x-acr-operation",
  #{
    name: "project.delete_variant",
    group: "project",
    summary: "Delete one project variant.",
  }
)
model ProjectDeleteVariantOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "project.delete_variant";
  args: ProjectDeleteVariantArgs;
}
