"""Generated from src/tsp/altium_cruncher/outputs/easyeda.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

EasyedaSymbolReport = TypedDict("EasyedaSymbolReport", {
    "lcsc_id": "str",
    "symbol_name": "str",
    "designator": "str",
    "pin_count": "int",
    "rectangle_count": "int",
    "circle_count": "int",
    "ellipse_count": "int",
    "polyline_count": "int",
    "polygon_count": "int",
    "unsupported_count": "int",
    "unsupported_graphics": "list[str]",
    "warnings": "list[str]",
    "policy": "SymbolPolicy",
    "grid": "HotspotGrid",
}, closed=True)

SymbolPolicy = TypedDict("SymbolPolicy", {
    "mils_per_easyeda_unit": NotRequired["float"],
    "invert_y": NotRequired["bool"],
    "default_pin_length_mils": NotRequired["float"],
    "hotspot_grid_mils": NotRequired["float"],
    "align_hotspots_to_grid": NotRequired["bool"],
    "body_color": NotRequired["int"],
    "body_fill_color": NotRequired["int"],
    "use_source_pin_electrical": NotRequired["bool"],
    "use_source_pin_ieee_symbols": NotRequired["bool"],
    "pin_name_visibility": NotRequired["str"],
    "pin_designator_visibility": NotRequired["str"],
    "pin_text_orientation": NotRequired["str"],
    "rotate_vertical_pin_text": NotRequired["bool"],
}, closed=True)

HotspotGrid = TypedDict("HotspotGrid", {
    "hotspot_grid_mils": NotRequired["float"],
    "align_hotspots_to_grid": NotRequired["bool"],
    "anchor_adjusted_to_grid": NotRequired["bool"],
    "source_grid_units": NotRequired["float"],
    "source_common_offset_possible": NotRequired["bool"],
    "source_x_remainder": NotRequired["float | None"],
    "source_y_remainder": NotRequired["float | None"],
    "hotspot_count": NotRequired["int"],
    "off_grid_hotspot_count": NotRequired["int"],
    "max_hotspot_error_mils": NotRequired["float"],
    "off_grid_hotspots_sample": NotRequired["list[OffGridHotspot]"],
}, closed=True)

OffGridHotspot = TypedDict("OffGridHotspot", {
    "pin": "str",
    "name": "str",
    "x_mils": "float",
    "y_mils": "float",
    "x_error_mils": "float",
    "y_error_mils": "float",
}, closed=True)
