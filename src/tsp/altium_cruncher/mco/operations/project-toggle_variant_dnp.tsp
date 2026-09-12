import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model ProjectToggleVariantDnpArgs extends Record<unknown> {
  file: McoString;
  variant: McoString;
  designator: McoString;
  unique_id?: string | null = null;
  alternate_part?: string | null = "";
}

@extension(
  "x-acr-operation",
  #{
    name: "project.toggle_variant_dnp",
    group: "project",
    summary: "Toggle one designator between fitted and Not Fitted in a project variant.",
  }
)
model ProjectToggleVariantDnpOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "project.toggle_variant_dnp";
  args: ProjectToggleVariantDnpArgs;
}
