/** Generated from src/tsp/altium_cruncher/config/clean-config.tsp. Do not edit. */

/**
 * JSON/JSONC configuration contract for schematic, schematic-library, and PCB-library clean workflows.
 */
export type CleanConfigInput = SchematicCleanConfig | PcblibCleanConfig;
export type ColorValue = number | string;
export type LineWidth = ("smallest" | "zero" | "small" | "medium" | "large") | number;
export type NoErcRuleSymbol = number | string;
export type NoErcRuleStyle = number | string;
export type StringList = string[];
/**
 * Layer name filters. Accepts legacy PcbLayer names, display names such as 'Mechanical 17', and V7 semantic tokens such as 'MECHANICAL17' when the installed altium-monkey exposes the V7-aware layer API; token and display forms match the same layer.
 */
export type StringList1 = string[];
/**
 * Layer name filters. Accepts legacy PcbLayer names, display names such as 'Mechanical 17', and V7 semantic tokens such as 'MECHANICAL17' when the installed altium-monkey exposes the V7-aware layer API; token and display forms match the same layer.
 */
export type StringList2 = string[];
/**
 * Layer name filters. Accepts legacy PcbLayer names, display names such as 'Mechanical 17', and V7 semantic tokens such as 'MECHANICAL17' when the installed altium-monkey exposes the V7-aware layer API; token and display forms match the same layer.
 */
export type StringList3 = string[];

export interface SchematicCleanConfig {
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
export interface PinFonts {
  enabled?: boolean;
  name_font?: FontSpec;
  name?: FontSpec;
  designator_font?: FontSpec;
  designator?: FontSpec;
}
export interface FontSpec {
  font_name?: string;
  font?: string;
  size_pt?: number;
  size?: number;
  bold?: boolean;
  italic?: boolean;
  color_win32?: ColorValue;
  color?: ColorValue;
}
export interface SymbolBodyRectangles {
  enabled?: boolean;
  min_width_mils?: number;
  min_height_mils?: number;
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
export interface FontAndColorRule {
  enabled?: boolean;
  color_win32?: ColorValue;
  color?: ColorValue;
  font_name?: string;
  size_pt?: number;
  bold?: boolean;
  italic?: boolean;
  font?: FontSpec;
}
export interface ComponentFontRule {
  enabled?: boolean;
  font?: FontSpec;
}
export interface ComponentFreeText {
  enabled?: boolean;
  font_name?: string;
  font?: string;
  color_win32?: ColorValue;
  color?: ColorValue;
}
export interface ColorRule {
  enabled?: boolean;
  color_win32?: ColorValue;
  color?: ColorValue;
}
export interface NoErcRule {
  enabled?: boolean;
  color_win32?: ColorValue;
  color?: ColorValue;
  symbol?: NoErcRuleSymbol;
  style?: NoErcRuleStyle;
}
export interface SheetStyle {
  enabled?: boolean;
  line_color_win32?: ColorValue;
  line_color?: ColorValue;
  color?: ColorValue;
  area_color_win32?: ColorValue;
  area_color?: ColorValue;
  document_font?: FontSpec;
  font?: FontSpec;
}
export interface InternalGraphics {
  enabled?: boolean;
  saturation?: number;
}
export interface PcblibCleanConfig {
  schema?: "altium_cruncher.pcblib.clean.config.a0" | null;
  profile?: "default" | "raw";
  remove_mechanical_primitives?: PcblibMechanicalPrimitives;
  remove_text_strings?: PcblibTextStrings;
  remove_regions?: PcblibRegions;
}
export interface PcblibMechanicalPrimitives {
  enabled?: boolean;
  primitive_types?: StringList;
  layers?: StringList1;
  preserve_regions?: boolean;
  preserve_component_bodies?: boolean;
}
export interface PcblibTextStrings {
  enabled?: boolean;
  layers?: StringList2;
  match?: "all" | "regex" | "contains" | "exact";
  patterns?: StringList;
}
export interface PcblibRegions {
  enabled?: boolean;
  layers?: StringList3;
  preserve_component_linked?: boolean;
  preserve_model_associated?: boolean;
  preserve_keepouts?: boolean;
  preserve_board_cutouts?: boolean;
  preserve_custom_pad_regions?: boolean;
}
