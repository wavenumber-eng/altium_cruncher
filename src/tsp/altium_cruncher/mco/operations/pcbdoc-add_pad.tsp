import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model PcbdocAddPadArgs extends Record<unknown> {
  ...MutationArgs;
  designator: McoString;
  position_mils: PointMils;
  width_mils: float64;
  height_mils: float64;
  shape?: NativeEnum | null;
  corner_radius_percent?: float64 | null;
  rotation_degrees?: float64 | null = 0.0;
  hole_size_mils?: float64 | null = 0.0;
  plated?: boolean | null;
  layer?: NativeEnum | null = "TOP";
  net?: string | null = null;
  solder_mask_expansion_mils?: float64 | null;
  paste_mask_expansion_mils?: float64 | null;
  tenting_top?: boolean | null;
  tenting_bottom?: boolean | null;
  solder_mask_expansion_mode?: integer | null;
  paste_mask_expansion_mode?: integer | null;
}

@extension(
  "x-acr-operation",
  #{ name: "pcbdoc.add_pad", group: "pcbdoc", summary: "Add a free PCB pad." }
)
model PcbdocAddPadOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "pcbdoc.add_pad";
  args: PcbdocAddPadArgs;
}
