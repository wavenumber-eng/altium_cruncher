import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model SchdocAddWireArgs extends Record<unknown> {
  ...MutationArgs;
  points_mils: WirePoints;
}

@extension(
  "x-acr-operation",
  #{
    name: "schdoc.add_wire",
    group: "schdoc",
    summary: "Add a schematic wire.",
  }
)
model SchdocAddWireOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "schdoc.add_wire";
  args: SchdocAddWireArgs;
}
