"""Generated from src/tsp/altium_cruncher/outputs/pcb-svg-component-layers.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

PcbSvgComponentLayers = TypedDict("PcbSvgComponentLayers", {
    "schema": "Literal[\"pcb.svg.component-layers.a0\"]",
    "coordinate_policy": "str",
    "layers": "list[PcbSvgComponentLayersLayersItem]",
}, extra_items="object")

PcbSvgComponentLayersLayersItem = TypedDict("PcbSvgComponentLayersLayersItem", {
    "token": "Literal[\"ILLUSTRATION_TOP\"] | Literal[\"ILLUSTRATION_BOTTOM\"] | Literal[\"ASSEMBLY_DESIGNATORS_TOP\"] | Literal[\"ASSEMBLY_DESIGNATORS_BOTTOM\"]",
    "group_id": "str",
    "side": "Literal[\"top\"] | Literal[\"bottom\"]",
    "instances": "list[PcbSvgComponentLayersLayersItemInstancesItem]",
    "unique_symbols": NotRequired["int"],
}, extra_items="object")

PcbSvgComponentLayersLayersItemInstancesItem = TypedDict("PcbSvgComponentLayersLayersItemInstancesItem", {
    "group_id": "str",
    "component_index": "int | None",
    "designator": "str",
    "side": NotRequired["Literal[\"top\"] | Literal[\"bottom\"]"],
    "symbol_id": NotRequired["str"],
    "anchor_svg_mm": NotRequired["list[float]"],
    "anchor_board_mm": NotRequired["list[float]"],
    "bounds_local_xyz_mm": NotRequired["list[float]"],
    "bodies": NotRequired["list[PcbSvgComponentLayersLayersItemInstancesItemBodiesItem]"],
    "paint_order": NotRequired["int"],
    "geometry_source": NotRequired["Literal[\"model\"] | Literal[\"pads\"]"],
    "center_view_mm": NotRequired["list[float]"],
    "font_size_mm": NotRequired["float"],
    "rotation_degrees": NotRequired["float"],
}, extra_items="object")

PcbSvgComponentLayersLayersItemInstancesItemBodiesItem = TypedDict("PcbSvgComponentLayersLayersItemInstancesItemBodiesItem", {
    "index": "int",
    "kind": "Literal[\"step\"] | Literal[\"extruded\"]",
    "lower_z_mm": "float",
    "upper_z_mm": "float",
    "color": "list[float] | None",
    "opacity": "float",
}, extra_items="object")

RecordUnknown = dict[str, object]
