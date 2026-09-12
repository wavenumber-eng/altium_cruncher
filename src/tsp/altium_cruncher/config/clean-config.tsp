import "@typespec/json-schema";
import "./clean-config-defaults.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.CleanConfigInputContract;

@oneOf
union ColorValue {
  integer,
  string,
}

@oneOf
union LineWidth {
  "smallest" | "zero" | "small" | "medium" | "large",
  integer,
}

model FontSpec {
  @extension("minLength", 1)
  font_name?: string;

  @extension("minLength", 1)
  font?: string;

  @extension("minimum", 1)
  size_pt?: integer;

  @extension("minimum", 1)
  size?: integer;

  bold?: boolean;
  italic?: boolean;
  color_win32?: ColorValue;
  color?: ColorValue;
}

model EnabledObject {
  enabled?: boolean;
}

model SchematicCleanConfig {
  schema?: "altium_cruncher.clean.config.a0" | null;
  normalize_pin_fonts?: PinFonts;
  normalize_symbol_body_rectangles?: SymbolBodyRectangles;
  normalize_power_symbols?: FontAndColorRule;
  normalize_net_labels?: FontAndColorRule;
  normalize_component_designators?: ComponentFontRule;
  normalize_component_parameters?: ComponentFontRule;
  normalize_component_free_text?: ComponentFreeText;
  normalize_wires?: ColorRule;
  normalize_no_erc?: NoErcRule;
  normalize_sheet_style?: SheetStyle;
  normalize_symbol_internal_graphics_monochrome?: InternalGraphics;
}

model PinFonts {
  enabled?: boolean;
  name_font?: FontSpec;
  name?: FontSpec;
  designator_font?: FontSpec;
  designator?: FontSpec;
}

model SymbolBodyRectangles {
  enabled?: boolean;

  @extension("minimum", 0)
  min_width_mils?: float64;

  @extension("minimum", 0)
  min_height_mils?: float64;

  outline_color_win32?: ColorValue;
  outline_color?: ColorValue;
  color?: ColorValue;
  line_width?: LineWidth;
  fill_color_win32?: ColorValue;
  fill_color?: ColorValue;
  area_color?: ColorValue;
  is_solid?: boolean;
  transparent?: boolean;
}

model FontAndColorRule {
  enabled?: boolean;
  color_win32?: ColorValue;
  color?: ColorValue;

  @extension("minLength", 1)
  font_name?: string;

  @extension("minimum", 1)
  size_pt?: integer;

  bold?: boolean;
  italic?: boolean;
  font?: FontSpec;
}

model ComponentFontRule {
  enabled?: boolean;
  font?: FontSpec;
}

model ComponentFreeText {
  enabled?: boolean;

  @extension("minLength", 1)
  font_name?: string;

  @extension("minLength", 1)
  font?: string;

  color_win32?: ColorValue;
  color?: ColorValue;
}

model ColorRule {
  enabled?: boolean;
  color_win32?: ColorValue;
  color?: ColorValue;
}

@oneOf
union NoErcRuleSymbol {
  integer,
  string,
}

@oneOf
union NoErcRuleStyle {
  integer,
  string,
}

model NoErcRule {
  enabled?: boolean;
  color_win32?: ColorValue;
  color?: ColorValue;
  symbol?: NoErcRuleSymbol;
  style?: NoErcRuleStyle;
}

model SheetStyle {
  enabled?: boolean;
  line_color_win32?: ColorValue;
  line_color?: ColorValue;
  color?: ColorValue;
  area_color_win32?: ColorValue;
  area_color?: ColorValue;
  document_font?: FontSpec;
  font?: FontSpec;
}

model InternalGraphics {
  enabled?: boolean;

  @extension("minimum", 0)
  @extension("maximum", 1)
  saturation?: float64;
}

model PcblibCleanConfig {
  schema?: "altium_cruncher.pcblib.clean.config.a0" | null;
  profile?: "default" | "raw";
  remove_mechanical_primitives?: PcblibMechanicalPrimitives;
  remove_text_strings?: PcblibTextStrings;
  remove_regions?: PcblibRegions;
}

model StringList is string[];

model PcblibMechanicalPrimitives {
  enabled?: boolean;
  primitive_types?: StringList;

  @doc("Layer name filters. Accepts legacy PcbLayer names, display names such as 'Mechanical 17', and V7 semantic tokens such as 'MECHANICAL17' when the installed altium-monkey exposes the V7-aware layer API; token and display forms match the same layer.")
  layers?: StringList;

  preserve_regions?: boolean;
  preserve_component_bodies?: boolean;
}

model PcblibTextStrings {
  enabled?: boolean;

  @doc("Layer name filters. Accepts legacy PcbLayer names, display names such as 'Mechanical 17', and V7 semantic tokens such as 'MECHANICAL17' when the installed altium-monkey exposes the V7-aware layer API; token and display forms match the same layer.")
  layers?: StringList;

  match?: "all" | "regex" | "contains" | "exact";
  patterns?: StringList;
}

model PcblibRegions {
  enabled?: boolean;

  @doc("Layer name filters. Accepts legacy PcbLayer names, display names such as 'Mechanical 17', and V7 semantic tokens such as 'MECHANICAL17' when the installed altium-monkey exposes the V7-aware layer API; token and display forms match the same layer.")
  layers?: StringList;

  preserve_component_linked?: boolean;
  preserve_model_associated?: boolean;
  preserve_keepouts?: boolean;
  preserve_board_cutouts?: boolean;
  preserve_custom_pad_regions?: boolean;
}

@jsonSchema
@id("https://github.com/wavenumber-eng/altium_cruncher/docs/contracts/clean_config.a0.schema.json")
@doc("JSON/JSONC configuration contract for schematic, schematic-library, and PCB-library clean workflows.")
@extension("title", "Altium Cruncher Clean Config")
union CleanConfigInput {
  SchematicCleanConfig,
  PcblibCleanConfig,
}
