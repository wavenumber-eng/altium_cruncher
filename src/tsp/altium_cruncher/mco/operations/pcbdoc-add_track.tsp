import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model PcbdocAddTrackArgs extends Record<unknown> {
  ...MutationArgs;
  start_mils: PointMils;
  end_mils: PointMils;
  width_mils: float64;
  layer?: NativeEnum | null = "TOP";
  net?: string | null = null;
}

@extension(
  "x-acr-operation",
  #{ name: "pcbdoc.add_track", group: "pcbdoc", summary: "Add a PCB track." }
)
model PcbdocAddTrackOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "pcbdoc.add_track";
  args: PcbdocAddTrackArgs;
}
