import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model ProjectListVariantsArgs extends Record<unknown> {
  file: McoString;
}

@extension(
  "x-acr-operation",
  #{
    name: "project.list_variants",
    group: "project",
    summary: "List project variants, DNP rows, and parameter changes.",
  }
)
model ProjectListVariantsOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "project.list_variants";
  args: ProjectListVariantsArgs;
}
