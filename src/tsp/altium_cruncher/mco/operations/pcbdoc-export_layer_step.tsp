import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model PcbdocExportLayerStepArgs extends Record<unknown> {
  file: McoString;
  output_file: McoString;

  @doc("Delegated to PcbLayerStepConfig along with additional fixture options; see pcb-layer-step configuration.")
  layer?: NativeEnum | null;

  board_name?: string | null;
  highlights?: LayerStepHighlight[] | null;
  overwrite?: boolean | null = false;
}

@extension(
  "x-acr-operation",
  #{
    name: "pcbdoc.export_layer_step",
    group: "pcbdoc",
    summary: "Export a PCB layer STEP artifact.",
  }
)
model PcbdocExportLayerStepOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "pcbdoc.export_layer_step";
  args: PcbdocExportLayerStepArgs;
}
