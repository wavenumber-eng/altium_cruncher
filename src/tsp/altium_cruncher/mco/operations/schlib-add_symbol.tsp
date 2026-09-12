import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model SchlibAddSymbolArgs extends Record<unknown> {
  file: McoString;
  name: McoString;
  description?: string | null = "";
}

@extension(
  "x-acr-operation",
  #{
    name: "schlib.add_symbol",
    group: "schlib",
    summary: "Add one empty schematic symbol to a SchLib.",
  }
)
model SchlibAddSymbolOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "schlib.add_symbol";
  args: SchlibAddSymbolArgs;
}
