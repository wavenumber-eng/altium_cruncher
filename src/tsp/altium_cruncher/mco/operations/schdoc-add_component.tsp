import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model SchdocAddComponentArgs extends Record<unknown> {
  ...MutationArgs;
  library: McoString;
  symbol: McoString;
  designator: McoString;
  position_mils: PointMils;
  unique_id?: string | null = null;
  design_item_id?: string | null = null;
  footprint_model?: string | null = null;
  footprint_library?: string | null = "";
  parameters?: Record<string> | null;
  orientation?: float64 | null = 0.0;
  mirrored?: boolean | null = false;
  part_id?: float64 | null = 1.0;
  display_mode?: float64 | null = 0.0;
  designator_style?: SchematicTextStyle | null;
  comment_style?: SchematicTextStyle | null;
  footprint_description?: string | null = "";
}

@extension(
  "x-acr-operation",
  #{
    name: "schdoc.add_component",
    group: "schdoc",
    summary: "Insert a schematic component from a SchLib.",
  }
)
model SchdocAddComponentOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "schdoc.add_component";
  args: SchdocAddComponentArgs;
}
