import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model PcbdocAddFillArgs extends Record<unknown> {
  ...MutationArgs;
  corner1_mils: PointMils;
  corner2_mils: PointMils;
  rotation_degrees?: float64 | null = 0.0;
  layer?: NativeEnum | null = "TOP";
  net?: string | null = null;
}

@extension(
  "x-acr-operation",
  #{
    name: "pcbdoc.add_fill",
    group: "pcbdoc",
    summary: "Add a rectangular PCB fill.",
  }
)
model PcbdocAddFillOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "pcbdoc.add_fill";
  args: PcbdocAddFillArgs;
}
