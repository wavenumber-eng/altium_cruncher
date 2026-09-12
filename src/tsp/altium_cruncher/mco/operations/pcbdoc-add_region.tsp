import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model PcbdocAddRegionArgs extends Record<unknown> {
  ...MutationArgs;
  outline_points_mils: RegionPoints;
  layer?: NativeEnum | null = "TOP";
  hole_points_mils?: PointMils[][] | null;
  is_keepout?: boolean | null = false;
  keepout_restrictions?: float64 | null = 0;
  net?: string | null = null;
  is_board_cutout?: boolean | null = false;
}

@extension(
  "x-acr-operation",
  #{ name: "pcbdoc.add_region", group: "pcbdoc", summary: "Add a PCB region." }
)
model PcbdocAddRegionOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "pcbdoc.add_region";
  args: PcbdocAddRegionArgs;
}
