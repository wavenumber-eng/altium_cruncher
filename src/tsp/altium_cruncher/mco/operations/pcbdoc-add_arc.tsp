import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model PcbdocAddArcArgs extends Record<unknown> {
  ...MutationArgs;
  center_mils: PointMils;
  radius_mils: float64;
  start_angle_degrees: float64;
  end_angle_degrees: float64;
  width_mils: float64;
  layer?: NativeEnum | null = "TOP";
  net?: string | null = null;
}

@extension(
  "x-acr-operation",
  #{ name: "pcbdoc.add_arc", group: "pcbdoc", summary: "Add a PCB arc." }
)
model PcbdocAddArcOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "pcbdoc.add_arc";
  args: PcbdocAddArcArgs;
}
