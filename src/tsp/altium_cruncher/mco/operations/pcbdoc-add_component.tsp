import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model PcbdocAddComponentArgs extends Record<unknown> {
  ...MutationArgs;
  library: McoString;
  footprint: McoString;
  designator: McoString;
  position_mils: PointMils;
  layer?: NativeEnum | null = "TOP";
  source_unique_id?: string | null;
  source_hierarchical_path?: string | null;
  source_component_library?: string | null;
  source_lib_reference?: string | null;
  source_description?: string | null;
  channel_offset?: integer | null;
  comment_text?: string | null = null;
  component_parameters?: Record<string> | null;
  pad_nets?: Record<string> | null;
  rotation_degrees?: float64 | null = 0.0;
  source_footprint_library?: string | null;
  comment_visible?: boolean | null = false;
  source_designator?: string | null;
}

@extension(
  "x-acr-operation",
  #{
    name: "pcbdoc.add_component",
    group: "pcbdoc",
    summary: "Insert a PCB component from a PcbLib.",
  }
)
model PcbdocAddComponentOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "pcbdoc.add_component";
  args: PcbdocAddComponentArgs;
}
