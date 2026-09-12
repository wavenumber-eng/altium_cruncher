import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model SchdocAddNetLabelArgs extends Record<unknown> {
  ...MutationArgs;
  text: McoString;
  location_mils: PointMils;
  orientation?: NativeEnum | null;
  justification?: NativeEnum = "BOTTOM_LEFT";
}

@extension(
  "x-acr-operation",
  #{
    name: "schdoc.add_net_label",
    group: "schdoc",
    summary: "Add a schematic net label.",
  }
)
model SchdocAddNetLabelOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "schdoc.add_net_label";
  args: SchdocAddNetLabelArgs;
}
