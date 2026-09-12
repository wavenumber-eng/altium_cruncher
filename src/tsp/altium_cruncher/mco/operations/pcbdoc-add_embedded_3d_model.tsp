import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model PcbdocAddEmbedded3dModelArgs extends Record<unknown> {
  ...MutationArgs;
  model_file: McoString;
  model_name?: string | null;
  name?: string | null;
  layer?: NativeEnum | null = "MECHANICAL_13";
  side?: NativeEnum | null = "TOP";
  location_mils?: PointMils | null = #[0.0, 0.0];
  rotation_x_degrees?: float64 | null = 0.0;
  rotation_y_degrees?: float64 | null = 0.0;
  rotation_z_degrees?: float64 | null = 0.0;
  z_mm?: float64 | null = 0;
  bounds_mils?: BoundsObject | BoundsArray | null;
  projection_outline_mils?: RegionPoints | null;
  overall_height_mils?: float64 | null;
  opacity?: float64 | null = 1.0;

  @doc("Takes precedence over z_mm when supplied.")
  z_mils?: float64;
}

@extension(
  "x-acr-operation",
  #{
    name: "pcbdoc.add_embedded_3d_model",
    group: "pcbdoc",
    summary: "Embed a 3D model in a PCB document.",
  }
)
model PcbdocAddEmbedded3dModelOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "pcbdoc.add_embedded_3d_model";
  args: PcbdocAddEmbedded3dModelArgs;
}
