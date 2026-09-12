"""Generated from src/tsp/altium_cruncher/outputs/pcb-svg-enrichment.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

PcbSvgEnrichment = TypedDict("PcbSvgEnrichment", {
    "canvas": "Canvas",
    "virtual_component_layers": NotRequired["ImportedPcbSvgComponentLayers"],
}, extra_items="object")

Canvas = TypedDict("Canvas", {
    "bounds_mode": "Literal[\"all_geometry\"] | Literal[\"board_outline\"]",
    "bounds_mils": "Bounds",
    "margin_mm": "float",
    "altium_origin_mils": "Pair",
    "svg_units": "Literal[\"mm\"]",
    "geometry_transform": "Canvas_geometry_transform",
    "metadata_coordinate_policy": "str",
    "view_box_mm": NotRequired["Bounds"],
    "scene_mirror_x": NotRequired["bool"],
    "scene_mirror_width_mm": NotRequired["float"],
}, closed=True)

ImportedPcbSvgComponentLayers = TypedDict("ImportedPcbSvgComponentLayers", {
    "schema": "Literal[\"pcb.svg.component-layers.a0\"]",
    "coordinate_policy": "str",
    "layers": "list[ImportedPcbSvgComponentLayers_PcbSvgComponentLayersLayersItem]",
}, extra_items="object")

ImportedPcbSvgComponentLayers_PcbSvgComponentLayersLayersItem = TypedDict("ImportedPcbSvgComponentLayers_PcbSvgComponentLayersLayersItem", {
    "token": "Literal[\"ILLUSTRATION_TOP\"] | Literal[\"ILLUSTRATION_BOTTOM\"] | Literal[\"ASSEMBLY_DESIGNATORS_TOP\"] | Literal[\"ASSEMBLY_DESIGNATORS_BOTTOM\"]",
    "group_id": "str",
    "side": "Literal[\"top\"] | Literal[\"bottom\"]",
    "instances": "list[ImportedPcbSvgComponentLayers_PcbSvgComponentLayersLayersItemInstancesItem]",
    "unique_symbols": NotRequired["int"],
}, extra_items="object")

ImportedPcbSvgComponentLayers_PcbSvgComponentLayersLayersItemInstancesItem = TypedDict("ImportedPcbSvgComponentLayers_PcbSvgComponentLayersLayersItemInstancesItem", {
    "group_id": "str",
    "component_index": "int | None",
    "designator": "str",
    "side": NotRequired["Literal[\"top\"] | Literal[\"bottom\"]"],
    "symbol_id": NotRequired["str"],
    "anchor_svg_mm": NotRequired["list[float]"],
    "anchor_board_mm": NotRequired["list[float]"],
    "bounds_local_xyz_mm": NotRequired["list[float]"],
    "bodies": NotRequired["list[ImportedPcbSvgComponentLayers_PcbSvgComponentLayersLayersItemInstancesItemBodiesItem]"],
    "paint_order": NotRequired["int"],
    "geometry_source": NotRequired["Literal[\"model\"] | Literal[\"pads\"]"],
    "center_view_mm": NotRequired["list[float]"],
    "font_size_mm": NotRequired["float"],
    "rotation_degrees": NotRequired["float"],
}, extra_items="object")

ImportedPcbSvgComponentLayers_PcbSvgComponentLayersLayersItemInstancesItemBodiesItem = TypedDict("ImportedPcbSvgComponentLayers_PcbSvgComponentLayersLayersItemInstancesItemBodiesItem", {
    "index": "int",
    "kind": "Literal[\"step\"] | Literal[\"extruded\"]",
    "lower_z_mm": "float",
    "upper_z_mm": "float",
    "color": "list[float] | None",
    "opacity": "float",
}, extra_items="object")

Canvas_geometry_transform = TypedDict("Canvas_geometry_transform", {
    "x_svg_mm": "str",
    "y_svg_mm": "str",
}, closed=True)

RecordUnknown = dict[str, object]
Bounds = list[float]
Pair = list[float]
ImportedPcbSvgComponentLayers_RecordUnknown = dict[str, object]
