"""Generated from src/tsp/altium_cruncher/config/clean-config.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

SchematicCleanConfig = TypedDict("SchematicCleanConfig", {
    "schema": NotRequired["Literal[\"altium_cruncher.clean.config.a0\"] | None"],
    "normalize_pin_fonts": NotRequired["PinFonts"],
    "normalize_symbol_body_rectangles": NotRequired["SymbolBodyRectangles"],
    "normalize_power_symbols": NotRequired["FontAndColorRule"],
    "normalize_net_labels": NotRequired["FontAndColorRule"],
    "normalize_component_designators": NotRequired["ComponentFontRule"],
    "normalize_component_parameters": NotRequired["ComponentFontRule"],
    "normalize_component_free_text": NotRequired["ComponentFreeText"],
    "normalize_wires": NotRequired["ColorRule"],
    "normalize_no_erc": NotRequired["NoErcRule"],
    "normalize_sheet_style": NotRequired["SheetStyle"],
    "normalize_symbol_internal_graphics_monochrome": NotRequired["InternalGraphics"],
}, closed=True)

PcblibCleanConfig = TypedDict("PcblibCleanConfig", {
    "schema": NotRequired["Literal[\"altium_cruncher.pcblib.clean.config.a0\"] | None"],
    "profile": NotRequired["Literal[\"default\"] | Literal[\"raw\"]"],
    "remove_mechanical_primitives": NotRequired["PcblibMechanicalPrimitives"],
    "remove_text_strings": NotRequired["PcblibTextStrings"],
    "remove_regions": NotRequired["PcblibRegions"],
}, closed=True)

PinFonts = TypedDict("PinFonts", {
    "enabled": NotRequired["bool"],
    "name_font": NotRequired["FontSpec"],
    "name": NotRequired["FontSpec"],
    "designator_font": NotRequired["FontSpec"],
    "designator": NotRequired["FontSpec"],
}, closed=True)

SymbolBodyRectangles = TypedDict("SymbolBodyRectangles", {
    "enabled": NotRequired["bool"],
    "min_width_mils": NotRequired["float"],
    "min_height_mils": NotRequired["float"],
    "outline_color_win32": NotRequired["ColorValue"],
    "outline_color": NotRequired["ColorValue"],
    "color": NotRequired["ColorValue"],
    "line_width": NotRequired["LineWidth"],
    "fill_color_win32": NotRequired["ColorValue"],
    "fill_color": NotRequired["ColorValue"],
    "area_color": NotRequired["ColorValue"],
    "is_solid": NotRequired["bool"],
    "transparent": NotRequired["bool"],
}, closed=True)

FontAndColorRule = TypedDict("FontAndColorRule", {
    "enabled": NotRequired["bool"],
    "color_win32": NotRequired["ColorValue"],
    "color": NotRequired["ColorValue"],
    "font_name": NotRequired["str"],
    "size_pt": NotRequired["int"],
    "bold": NotRequired["bool"],
    "italic": NotRequired["bool"],
    "font": NotRequired["FontSpec"],
}, closed=True)

ComponentFontRule = TypedDict("ComponentFontRule", {
    "enabled": NotRequired["bool"],
    "font": NotRequired["FontSpec"],
}, closed=True)

ComponentFreeText = TypedDict("ComponentFreeText", {
    "enabled": NotRequired["bool"],
    "font_name": NotRequired["str"],
    "font": NotRequired["str"],
    "color_win32": NotRequired["ColorValue"],
    "color": NotRequired["ColorValue"],
}, closed=True)

ColorRule = TypedDict("ColorRule", {
    "enabled": NotRequired["bool"],
    "color_win32": NotRequired["ColorValue"],
    "color": NotRequired["ColorValue"],
}, closed=True)

NoErcRule = TypedDict("NoErcRule", {
    "enabled": NotRequired["bool"],
    "color_win32": NotRequired["ColorValue"],
    "color": NotRequired["ColorValue"],
    "symbol": NotRequired["NoErcRuleSymbol"],
    "style": NotRequired["NoErcRuleStyle"],
}, closed=True)

SheetStyle = TypedDict("SheetStyle", {
    "enabled": NotRequired["bool"],
    "line_color_win32": NotRequired["ColorValue"],
    "line_color": NotRequired["ColorValue"],
    "color": NotRequired["ColorValue"],
    "area_color_win32": NotRequired["ColorValue"],
    "area_color": NotRequired["ColorValue"],
    "document_font": NotRequired["FontSpec"],
    "font": NotRequired["FontSpec"],
}, closed=True)

InternalGraphics = TypedDict("InternalGraphics", {
    "enabled": NotRequired["bool"],
    "saturation": NotRequired["float"],
}, closed=True)

PcblibMechanicalPrimitives = TypedDict("PcblibMechanicalPrimitives", {
    "enabled": NotRequired["bool"],
    "primitive_types": NotRequired["StringList"],
    "layers": NotRequired["StringList"],
    "preserve_regions": NotRequired["bool"],
    "preserve_component_bodies": NotRequired["bool"],
}, closed=True)

PcblibTextStrings = TypedDict("PcblibTextStrings", {
    "enabled": NotRequired["bool"],
    "layers": NotRequired["StringList"],
    "match": NotRequired["Literal[\"all\"] | Literal[\"regex\"] | Literal[\"contains\"] | Literal[\"exact\"]"],
    "patterns": NotRequired["StringList"],
}, closed=True)

PcblibRegions = TypedDict("PcblibRegions", {
    "enabled": NotRequired["bool"],
    "layers": NotRequired["StringList"],
    "preserve_component_linked": NotRequired["bool"],
    "preserve_model_associated": NotRequired["bool"],
    "preserve_keepouts": NotRequired["bool"],
    "preserve_board_cutouts": NotRequired["bool"],
    "preserve_custom_pad_regions": NotRequired["bool"],
}, closed=True)

FontSpec = TypedDict("FontSpec", {
    "font_name": NotRequired["str"],
    "font": NotRequired["str"],
    "size_pt": NotRequired["int"],
    "size": NotRequired["int"],
    "bold": NotRequired["bool"],
    "italic": NotRequired["bool"],
    "color_win32": NotRequired["ColorValue"],
    "color": NotRequired["ColorValue"],
}, closed=True)

CleanConfigInput = SchematicCleanConfig | PcblibCleanConfig
ColorValue = int | str
LineWidth = Literal["smallest"] | Literal["zero"] | Literal["small"] | Literal["medium"] | Literal["large"] | int
NoErcRuleSymbol = int | str
NoErcRuleStyle = int | str
StringList = list[str]
