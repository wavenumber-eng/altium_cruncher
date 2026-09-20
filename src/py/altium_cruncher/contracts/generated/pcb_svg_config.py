"""Generated from src/tsp/altium_cruncher/config/pcb-svg.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

PcbSvgConfigInput = TypedDict("PcbSvgConfigInput", {
    "schema": NotRequired["Literal[\"pcb.svg.config.a1\"] | Literal[\"pcb.svg.config.a0\"] | None"],
    "global": NotRequired["GlobalOptions | None"],
    "assembly": NotRequired["AssemblyOptions | None"],
    "dnp": NotRequired["DnpOptions | None"],
    "diodes": NotRequired["DiodeOptions | None"],
    "pin1": NotRequired["Pin1Options | None"],
    "components": NotRequired["RecordComponentOverride | None"],
    "layer_outputs": NotRequired["LayerOutputOptions | None"],
    "views": NotRequired["list[ViewOptions] | None"],
}, extra_items="object")

GlobalOptions = TypedDict("GlobalOptions", {
    "pcbdoc": NotRequired["str | None"],
    "canvas": NotRequired["CanvasOptions | None"],
    "include_metadata": NotRequired["bool | None | float | str"],
    "show_empty_layers": NotRequired["bool | None | float | str"],
    "clip_to_outline": NotRequired["bool | None | float | str"],
    "clip_holes_from_copper": NotRequired["bool | None | float | str"],
    "mirror_bottom_view": NotRequired["bool | None | float | str"],
    "svg_scale": NotRequired["float | None | bool | str"],
    "svg_size_unit": NotRequired["str | None"],
    "clean_output": NotRequired["bool | None | float | str"],
    "styles": NotRequired["StyleTable | None"],
}, extra_items="object")

AssemblyOptions = TypedDict("AssemblyOptions", {
    "default_projection": NotRequired["Literal[\"detail\"] | Literal[\"outline\"] | Literal[\"simple\"] | Literal[\"bounding_box\"] | Literal[\"none\"] | Literal[\"silhouette\"] | Literal[\"profile\"] | Literal[\"bounding-box\"] | Literal[\"bbox\"] | Literal[\"box\"] | Literal[\"bounds\"] | Literal[\"off\"] | Literal[\"disabled\"] | None | str"],
    "dnp_projection": NotRequired["Literal[\"detail\"] | Literal[\"outline\"] | Literal[\"simple\"] | Literal[\"bounding_box\"] | Literal[\"none\"] | Literal[\"silhouette\"] | Literal[\"profile\"] | Literal[\"bounding-box\"] | Literal[\"bbox\"] | Literal[\"box\"] | Literal[\"bounds\"] | Literal[\"off\"] | Literal[\"disabled\"] | None | str"],
    "designator_color": NotRequired["str | None"],
    "dnp_designator_color": NotRequired["str | None"],
}, closed=True)

DnpOptions = TypedDict("DnpOptions", {
    "color": NotRequired["str | None"],
    "hatch": NotRequired["bool | None | float | str"],
    "hatch_spacing_mm": NotRequired["float | None | bool | str"],
    "hatch_angle_deg": NotRequired["float | None | bool | str"],
    "hatch_line_width_mm": NotRequired["float | None | bool | str"],
}, closed=True)

DiodeOptions = TypedDict("DiodeOptions", {
    "enabled": NotRequired["bool | None | float | str"],
    "line_art": NotRequired["bool | None | float | str"],
    "marker_color": NotRequired["str | None"],
    "numeric_cathode_pad": NotRequired["str | None"],
    "cathode_pad_names": NotRequired["list[str] | None"],
    "designator_prefixes": NotRequired["list[str] | None"],
    "parameter_terms": NotRequired["list[str] | None"],
}, closed=True)

Pin1Options = TypedDict("Pin1Options", {
    "exclude_designator_prefixes": NotRequired["list[str] | None"],
}, closed=True)

LayerOutputOptions = TypedDict("LayerOutputOptions", {
    "enabled": NotRequired["bool | None | float | str"],
    "layers": NotRequired["Literal[\"auto\"] | Literal[\"AUTO\"] | list[str] | None | str"],
    "include_special_layers": NotRequired["list[Literal[\"BOARD_SUBSTRATE\"] | Literal[\"BOARD_OUTLINE\"] | Literal[\"BOARD_CUTOUTS\"] | Literal[\"DRILLS\"] | Literal[\"SLOTS\"] | Literal[\"ASSEMBLY_HLR_TOP\"] | Literal[\"ASSEMBLY_HLR_BOTTOM\"] | Literal[\"ASSEMBLY_DESIGNATORS_TOP\"] | Literal[\"ASSEMBLY_DESIGNATORS_BOTTOM\"] | Literal[\"PIN1_TOP\"] | Literal[\"PIN1_BOTTOM\"] | Literal[\"SOLDERMASK_FILM_TOP\"] | Literal[\"SOLDERMASK_FILM_BOTTOM\"] | Literal[\"SURFACE_COPPER_TOP\"] | Literal[\"SURFACE_COPPER_BOTTOM\"] | Literal[\"BEND_LINES\"] | Literal[\"ILLUSTRATION_TOP\"] | Literal[\"ILLUSTRATION_BOTTOM\"] | str] | None"],
    "output_dir": NotRequired["str | None"],
}, extra_items="object")

ViewOptions = TypedDict("ViewOptions", {
    "name": "str",
    "enabled": NotRequired["bool | None | float | str"],
    "group_id": NotRequired["str | None"],
    "output_svg": NotRequired["str | None"],
    "layers": NotRequired["list[str] | None"],
    "mirror": NotRequired["bool | None | None | float | str"],
    "assembly_hlr_mode": NotRequired["Literal[\"outline\"] | Literal[\"simple\"] | Literal[\"detail\"] | Literal[\"detailed\"] | Literal[\"bounding_box\"] | Literal[\"none\"] | Literal[\"silhouette\"] | Literal[\"profile\"] | Literal[\"bounding-box\"] | Literal[\"bbox\"] | Literal[\"box\"] | Literal[\"off\"] | None | str"],
    "styles": NotRequired["StyleTable | None"],
    "description": NotRequired["str | None"],
}, closed=True)

CanvasOptions = TypedDict("CanvasOptions", {
    "bounds": NotRequired["Literal[\"board_outline\"] | Literal[\"all_geometry\"] | Literal[\"board\"] | Literal[\"outline\"] | Literal[\"board_profile\"] | Literal[\"legacy\"] | Literal[\"all\"] | Literal[\"rendered_view\"] | Literal[\"rendered_geometry\"] | None | str"],
    "margin_mm": NotRequired["float | None | bool | str"],
}, closed=True)

StyleTable = TypedDict("StyleTable", {
    "illustration": NotRequired["IllustrationStyle"],
    "assembly_designators": NotRequired["AssemblyDesignatorsStyle"],
    "board_substrate": NotRequired["BoardSubstrateStyle"],
    "soldermask_film": NotRequired["SoldermaskFilmStyle"],
    "bend_lines": NotRequired["BendLinesStyle"],
    "assembly_hlr": NotRequired["AssemblyHlrStyle"],
    "board_outline": NotRequired["BoardOutlineStyle"],
    "board_cutouts": NotRequired["BoardCutoutsStyle"],
    "drills": NotRequired["HoleStyle"],
    "slots": NotRequired["HoleStyle"],
    "copper_traces": NotRequired["CopperTracesStyle"],
    "vias": NotRequired["ViasStyle"],
    "copper_polygons": NotRequired["CopperPolygonsStyle"],
    "smd_pads": NotRequired["SmdPadsStyle"],
    "through_hole_pads": NotRequired["ThroughHolePadsStyle"],
    "silkscreen_component_graphics": NotRequired["SilkscreenComponentGraphicsStyle"],
    "silkscreen_designators": NotRequired["SilkscreenDesignatorsStyle"],
    "silkscreen_board_graphics": NotRequired["SilkscreenBoardGraphicsStyle"],
    "silkscreen_surface": NotRequired["SilkscreenSurfaceStyle"],
    "pin1_marker": NotRequired["Pin1MarkerStyle"],
    "keepout": NotRequired["KeepoutStyle"],
}, extra_items="StyleObject")

ComponentOverride = TypedDict("ComponentOverride", {
    "side": NotRequired["Literal[\"top\"] | Literal[\"bottom\"] | Literal[\"toplayer\"] | Literal[\"bottomlayer\"] | Literal[\"top_layer\"] | Literal[\"bottom_layer\"] | Literal[\"top-layer\"] | Literal[\"bottom-layer\"] | None | None | str"],
    "projection": NotRequired["Literal[\"detail\"] | Literal[\"outline\"] | Literal[\"simple\"] | Literal[\"bounding_box\"] | Literal[\"none\"] | Literal[\"silhouette\"] | Literal[\"profile\"] | Literal[\"bounding-box\"] | Literal[\"bbox\"] | Literal[\"box\"] | Literal[\"bounds\"] | Literal[\"off\"] | Literal[\"disabled\"] | None | None | str"],
    "assembly_hlr": NotRequired["AssemblyHlrStyle | None"],
    "pin1_enabled": NotRequired["bool | None | None | float | str"],
    "pin1_pad": NotRequired["str | None"],
    "cathode_pad": NotRequired["str | None"],
    "diode": NotRequired["bool | None | None | float | str"],
    "diode_line_art": NotRequired["bool | None | None | float | str"],
    "show_designator": NotRequired["bool | None | None | float | str"],
}, closed=True)

IllustrationStyle = TypedDict("IllustrationStyle", {
    "enabled": NotRequired["bool | float | str"],
    "line_width_mm": NotRequired["float | bool | str"],
    "opacity": NotRequired["float | bool | str"],
}, extra_items="object")

AssemblyDesignatorsStyle = TypedDict("AssemblyDesignatorsStyle", {
    "enabled": NotRequired["bool | float | str"],
    "color": NotRequired["str"],
    "stroke_color": NotRequired["str"],
    "stroke_width_mm": NotRequired["float | bool | str"],
    "fill_ratio": NotRequired["float | bool | str"],
    "max_font_size_mm": NotRequired["float | bool | str"],
    "opacity": NotRequired["float | bool | str"],
}, extra_items="object")

BoardSubstrateStyle = TypedDict("BoardSubstrateStyle", {
    "enabled": NotRequired["bool | float | str"],
    "color": NotRequired["str"],
    "rigid_color": NotRequired["str"],
    "flex_color": NotRequired["str"],
}, extra_items="object")

SoldermaskFilmStyle = TypedDict("SoldermaskFilmStyle", {
    "enabled": NotRequired["bool | float | str"],
    "color": NotRequired["str"],
    "coverlay_color": NotRequired["str"],
    "opacity": NotRequired["float | bool | str"],
}, extra_items="object")

BendLinesStyle = TypedDict("BendLinesStyle", {
    "enabled": NotRequired["bool | float | str"],
    "color": NotRequired["str"],
    "opacity": NotRequired["float | bool | str"],
    "line_width_mm": NotRequired["float | bool | str"],
    "line_style": NotRequired["Literal[\"solid\"] | Literal[\"dashed\"] | str"],
    "dash_length_mm": NotRequired["float | bool | str"],
    "dash_gap_mm": NotRequired["float | bool | str"],
    "extension_mm": NotRequired["float | bool | str"],
}, extra_items="object")

AssemblyHlrStyle = TypedDict("AssemblyHlrStyle", {
    "projection_algorithm": NotRequired["Literal[\"fast\"] | Literal[\"poly\"] | Literal[\"exact\"]"],
    "outline_algorithm": NotRequired["Literal[\"fast-mesh-shadow\"] | Literal[\"mesh-shadow\"] | Literal[\"hlr-close\"]"],
    "fast": NotRequired["FastHlrOptions"],
    "enabled": NotRequired["bool | float | str"],
    "color": NotRequired["str"],
    "line_width_mm": NotRequired["float | bool | str"],
    "curve_mode": NotRequired["str"],
    "samples_per_curve": NotRequired["float | bool | str"],
    "round_digits": NotRequired["float | bool | str"],
    "include_visible": NotRequired["bool | float | str"],
    "include_outline": NotRequired["bool | float | str"],
    "union_polygons": NotRequired["bool | float | str"],
}, extra_items="object")

BoardOutlineStyle = TypedDict("BoardOutlineStyle", {
    "enabled": NotRequired["bool | float | str"],
    "color": NotRequired["str"],
    "line_width_mm": NotRequired["float | bool | str"],
}, extra_items="object")

BoardCutoutsStyle = TypedDict("BoardCutoutsStyle", {
    "enabled": NotRequired["bool | float | str"],
    "scope": NotRequired["Literal[\"all\"] | Literal[\"interior\"]"],
    "outline_opacity": NotRequired["float | bool | str"],
    "hatch_color": NotRequired["str"],
    "hatch_opacity": NotRequired["float | bool | str"],
    "label": NotRequired["str"],
    "label_color": NotRequired["str"],
    "label_opacity": NotRequired["float | bool | str"],
    "label_max_font_size_mm": NotRequired["float | bool | str"],
    "label_fill_ratio": NotRequired["float | bool | str"],
    "label_rotation_min_gain": NotRequired["float | bool | str"],
    "color": NotRequired["str"],
    "hatch": NotRequired["bool | float | str"],
    "hatch_spacing_mm": NotRequired["float | bool | str"],
    "hatch_angle_deg": NotRequired["float | bool | str"],
    "hatch_line_width_mm": NotRequired["float | bool | str"],
    "outline_style": NotRequired["Literal[\"solid\"] | Literal[\"dashed\"] | str"],
    "outline_dash_mm": NotRequired["float | bool | str"],
    "outline_width_mm": NotRequired["float | bool | str"],
}, extra_items="object")

HoleStyle = TypedDict("HoleStyle", {
    "enabled": NotRequired["bool | float | str"],
    "plated_color": NotRequired["str"],
    "non_plated_color": NotRequired["str"],
    "outline": NotRequired["bool | float | str"],
    "outline_width_mm": NotRequired["float | bool | str"],
    "respect_tenting": NotRequired["bool | float | str"],
    "opacity": NotRequired["float | bool | str"],
}, extra_items="object")

CopperTracesStyle = TypedDict("CopperTracesStyle", {
    "enabled": NotRequired["bool | float | str"],
    "color": NotRequired["str"],
}, extra_items="object")

ViasStyle = TypedDict("ViasStyle", {
    "enabled": NotRequired["bool | float | str"],
    "color": NotRequired["str"],
}, extra_items="object")

CopperPolygonsStyle = TypedDict("CopperPolygonsStyle", {
    "enabled": NotRequired["bool | float | str"],
    "color": NotRequired["str"],
}, extra_items="object")

SmdPadsStyle = TypedDict("SmdPadsStyle", {
    "enabled": NotRequired["bool | float | str"],
    "color": NotRequired["str"],
}, extra_items="object")

ThroughHolePadsStyle = TypedDict("ThroughHolePadsStyle", {
    "enabled": NotRequired["bool | float | str"],
    "color": NotRequired["str"],
}, extra_items="object")

SilkscreenComponentGraphicsStyle = TypedDict("SilkscreenComponentGraphicsStyle", {
    "enabled": NotRequired["bool | float | str"],
    "color": NotRequired["str"],
}, extra_items="object")

SilkscreenDesignatorsStyle = TypedDict("SilkscreenDesignatorsStyle", {
    "enabled": NotRequired["bool | float | str"],
    "color": NotRequired["str"],
}, extra_items="object")

SilkscreenBoardGraphicsStyle = TypedDict("SilkscreenBoardGraphicsStyle", {
    "enabled": NotRequired["bool | float | str"],
    "color": NotRequired["str"],
}, extra_items="object")

SilkscreenSurfaceStyle = TypedDict("SilkscreenSurfaceStyle", {
    "clip_mode": NotRequired["Literal[\"none\"] | Literal[\"board\"] | Literal[\"film\"] | str"],
}, extra_items="object")

Pin1MarkerStyle = TypedDict("Pin1MarkerStyle", {
    "enabled": NotRequired["bool | float | str"],
    "color": NotRequired["str"],
    "dot_diameter_mm": NotRequired["float | bool | str"],
    "min_dot_diameter_mm": NotRequired["float | bool | str"],
}, extra_items="object")

KeepoutStyle = TypedDict("KeepoutStyle", {
    "enabled": NotRequired["bool | float | str"],
    "color": NotRequired["str"],
}, extra_items="object")

FastHlrOptions = TypedDict("FastHlrOptions", {
    "include_hidden": NotRequired["bool | float | str"],
    "include_boundaries": NotRequired["bool | float | str"],
    "include_creases": NotRequired["bool | float | str"],
    "include_silhouettes": NotRequired["bool | float | str"],
    "suppress_coplanar_seams": NotRequired["bool | float | str"],
}, extra_items="object")

RecordComponentOverride = dict[str, ComponentOverride]
RecordUnknown = dict[str, object]
StyleObject = dict[str, object]
RecordStyleObject = dict[str, StyleObject]
