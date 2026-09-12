import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model PcbdocCreateArgs extends Record<unknown> {
  file: McoString;
  layer_stack_template?: string | null;
  rigid_stack?: Wavenumber.AltiumCruncher.Creation.RigidLayerStack | null;
  stackupx_file?: McoString | null;
  board_outline_mils?:
    | Wavenumber.AltiumCruncher.Creation.BoardOutlineMils
    | null;
  board_origin_mils?: OriginMils | null;
  sheet_frame_mils?: SheetFrameMils | null;
  mechanical_layer_profile?: string | null;
  mechanical_layers?: McoMechanicalLayer[] | null;
  mechanical_layer_pairs?: McoMechanicalPair[] | null;
  mechanical_layer_kinds?: McoMechanicalKind[] | null;
  overwrite?: boolean | null = false;
}

@extension(
  "x-acr-operation",
  #{
    name: "pcbdoc.create",
    group: "pcbdoc",
    summary: "Create an empty PCB document.",
  }
)
model PcbdocCreateOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "pcbdoc.create";
  args: PcbdocCreateArgs;
}
