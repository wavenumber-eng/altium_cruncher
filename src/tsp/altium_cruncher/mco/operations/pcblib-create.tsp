import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model PcblibCreateArgs extends Record<unknown> {
  file: McoString;
  overwrite?: boolean | null = false;
}

@extension(
  "x-acr-operation",
  #{
    name: "pcblib.create",
    group: "pcblib",
    summary: "Initialize a new PCB footprint library for later PcbLib operations.",
  }
)
model PcblibCreateOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "pcblib.create";
  args: PcblibCreateArgs;
}
