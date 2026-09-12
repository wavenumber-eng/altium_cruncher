import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model PcbdocArrangeDesignatorsArgs extends Record<unknown> {
  ...MutationArgs;
  designators?: McoString[] | null;
  placement?: string | null = "above_component";
  offset_mils?: PointMils | null = #[0.0, 10.0];
  height_mils?: float64 | null = 40.0;
  layer?: NativeEnum | null = "TOP_OVERLAY";
  stroke_width_mils?: float64 | null = 8.0;
  width_factor?: float64 | null = 0.6;
  bold?: boolean | null = true;
  italic?: boolean | null = false;
  font_name?: string | null = "Arial";
  font_kind?: string | null = "truetype";
}

@extension(
  "x-acr-operation",
  #{
    name: "pcbdoc.arrange_designators",
    group: "pcbdoc",
    summary: "Position generated PCB designator text.",
  }
)
model PcbdocArrangeDesignatorsOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "pcbdoc.arrange_designators";
  args: PcbdocArrangeDesignatorsArgs;
}
