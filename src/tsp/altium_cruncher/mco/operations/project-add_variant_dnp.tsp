import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model ProjectAddVariantDnpArgs extends Record<unknown> {
  file: McoString;
  variant: McoString;
  designator: McoString;
  unique_id?: string | null = null;
  alternate_part?: string | null = "";
}

@extension(
  "x-acr-operation",
  #{
    name: "project.add_variant_dnp",
    group: "project",
    summary: "Mark one designator Not Fitted in a project variant.",
  }
)
model ProjectAddVariantDnpOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "project.add_variant_dnp";
  args: ProjectAddVariantDnpArgs;
}
