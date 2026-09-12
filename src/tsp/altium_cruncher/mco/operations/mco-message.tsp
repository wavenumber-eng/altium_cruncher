import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model McoMessageArgs extends Record<unknown> {
  text?: string | null;
}

@extension(
  "x-acr-operation",
  #{
    name: "mco.message",
    group: "mco",
    summary: "Emit a human-readable message.",
  }
)
model McoMessageOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "mco.message" | "message";
  args?: McoMessageArgs;
}
