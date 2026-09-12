import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model PcbdocAddTextArgs extends Record<unknown> {
  ...MutationArgs;
  text: McoString;
  position_mils: PointMils;
  layer?: NativeEnum | null = "TOP_OVERLAY";
  height_mils: float64;
  font_kind?: string | null = "stroke";
  font_name?: string | null = "Arial";
  bold?: boolean | null = false;
  italic?: boolean | null = false;
  rotation_degrees?: float64 | null = 0.0;
  stroke_width_mils?: float64 | null = 10.0;
  is_comment?: boolean | null = false;
  is_designator?: boolean | null = false;
  is_mirrored?: boolean | null = false;
  is_inverted?: boolean | null = false;
  inverted_margin_mils?: float64 | null = 0.0;
  use_inverted_rectangle?: boolean | null = false;
  inverted_rectangle_size_mils?: PointMils | null;
  is_frame?: boolean | null = false;
  frame_size_mils?: PointMils | null;
  barcode_full_size_mils?: PointMils | null;
  barcode_margin_mils?: PointMils | null = #[20.0, 20.0];
  barcode_min_width_mils?: float64 | null = 0.0;
  barcode_show_text?: boolean | null = true;
  barcode_inverted?: boolean | null = true;
  text_justification?: NativeEnum | null;
  barcode_kind?: NativeEnum | null;
  barcode_render_mode?: NativeEnum | null;
}

@extension(
  "x-acr-operation",
  #{ name: "pcbdoc.add_text", group: "pcbdoc", summary: "Add PCB text." }
)
model PcbdocAddTextOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "pcbdoc.add_text";
  args: PcbdocAddTextArgs;
}
