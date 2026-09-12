import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model SchdocCreateArgs extends Record<unknown> {
  file: McoString;
  template?: McoString | null;
  sheet_style?: string | null = "D";
  apply_template_visual_sheet_settings?: boolean | null = false;
  custom_sheet_mils?: Wavenumber.AltiumCruncher.Creation.CustomSheetMils | null;
  overwrite?: boolean | null = false;
}

@extension(
  "x-acr-operation",
  #{
    name: "schdoc.create",
    group: "schdoc",
    summary: "Create an empty schematic document.",
  }
)
model SchdocCreateOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "schdoc.create";
  args: SchdocCreateArgs;
}
