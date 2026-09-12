import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model ProjectAddVariantArgs extends Record<unknown> {
  file: McoString;
  name: McoString;
  unique_id?: string | null = null;
  allow_fabrication?: boolean | null = true;
  current?: boolean | null = false;
}

@extension(
  "x-acr-operation",
  #{
    name: "project.add_variant",
    group: "project",
    summary: "Add one project variant.",
  }
)
model ProjectAddVariantOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "project.add_variant";
  args: ProjectAddVariantArgs;
}
