import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model SchdocAddPowerPortArgs extends Record<unknown> {
  ...MutationArgs;
  text: McoString;
  location_mils: PointMils;
  style?: NativeEnum = "BAR";
  orientation?: NativeEnum | null;
  show_net_name?: boolean | null = true;
}

@extension(
  "x-acr-operation",
  #{
    name: "schdoc.add_power_port",
    group: "schdoc",
    summary: "Add a schematic power port.",
  }
)
model SchdocAddPowerPortOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "schdoc.add_power_port";
  args: SchdocAddPowerPortArgs;
}
