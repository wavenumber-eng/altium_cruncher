import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model PcblibAddFootprintArgs extends Record<unknown> {
  ...MutationArgs;
  name: McoString;
  height?: string | null = "0mil";
  description?: string | null = "";
  item_guid?: string | null = "";
  revision_guid?: string | null = "";
  parameters?: Record<string> | null;
  primitive_parameters?: Record<string> | null;
}

@extension(
  "x-acr-operation",
  #{
    name: "pcblib.add_footprint",
    group: "pcblib",
    summary: "Add one empty footprint container to a PcbLib.",
  }
)
model PcblibAddFootprintOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "pcblib.add_footprint";
  args: PcblibAddFootprintArgs;
}
