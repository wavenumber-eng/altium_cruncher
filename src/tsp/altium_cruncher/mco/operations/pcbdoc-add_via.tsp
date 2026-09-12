import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model PcbdocAddViaArgs extends Record<unknown> {
  ...MutationArgs;
  position_mils: PointMils;
  diameter_mils: float64;
  hole_size_mils: float64;
  layer_start?: NativeEnum | null = "TOP";
  layer_end?: NativeEnum | null = "BOTTOM";
  net?: string | null = null;
}

@extension(
  "x-acr-operation",
  #{ name: "pcbdoc.add_via", group: "pcbdoc", summary: "Add a PCB via." }
)
model PcbdocAddViaOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "pcbdoc.add_via";
  args: PcbdocAddViaArgs;
}
