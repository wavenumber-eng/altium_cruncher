import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model McoFailArgs extends Record<unknown> {
  message?: string | null;
}

@extension(
  "x-acr-operation",
  #{
    name: "mco.fail",
    group: "mco",
    summary: "Fail intentionally, usually for control-flow tests.",
  }
)
model McoFailOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "mco.fail" | "fail";
  args?: McoFailArgs;
}
