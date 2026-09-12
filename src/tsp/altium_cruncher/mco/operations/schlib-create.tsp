import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model SchlibCreateArgs extends Record<unknown> {
  file: McoString;
  overwrite?: boolean | null = false;
}

@extension(
  "x-acr-operation",
  #{
    name: "schlib.create",
    group: "schlib",
    summary: "Create an empty schematic library.",
  }
)
model SchlibCreateOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "schlib.create";
  args: SchlibCreateArgs;
}
