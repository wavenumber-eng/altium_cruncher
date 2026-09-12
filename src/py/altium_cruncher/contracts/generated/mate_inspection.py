"""Generated from src/tsp/altium_cruncher/outputs/mate.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

MateInspection = TypedDict("MateInspection", {
    "schema": "Literal[\"altium_cruncher.mate.inspect.a0\"]",
    "source": "str",
    "source_tag": "str",
    "boards": "list[Board]",
}, closed=True)

Board = TypedDict("Board", {
    "board_key": "str",
    "pcb_path": "str",
    "components": "list[Component]",
    "free_pads": "list[FreePad]",
    "board_outline_mils": NotRequired["Bounds"],
    "board_outline": NotRequired["Outline"],
    "board_origin_mils": NotRequired["Point"],
}, closed=True)

Component = TypedDict("Component", {
    "designator": "str",
    "kind": "str",
    "layer": "str",
    "footprint": "str",
    "x_mils": "float",
    "y_mils": "float",
    "net_name": NotRequired["str"],
    "source_power_port": NotRequired["PowerPort"],
    "source_pad_geometries": NotRequired["list[PadGeometry]"],
}, closed=True)

FreePad = TypedDict("FreePad", {
    "designator": "str",
    "kind": "str",
    "layer": "int",
    "x_mils": "float",
    "y_mils": "float",
    "width_mils": "float",
    "height_mils": "float",
    "hole_size_mils": "float",
    "plated": "bool",
    "shape": "int",
    "net_name": NotRequired["str"],
    "source_power_port": NotRequired["PowerPort"],
}, closed=True)

Bounds = TypedDict("Bounds", {
    "left": "float",
    "bottom": "float",
    "right": "float",
    "top": "float",
}, closed=True)

Outline = TypedDict("Outline", {
    "vertices": "list[LineVertex | ArcVertex]",
    "closed": "bool",
    "cutouts": NotRequired["list[Outline]"],
}, closed=True)

Point = TypedDict("Point", {
    "x": "float",
    "y": "float",
}, closed=True)

PowerPort = TypedDict("PowerPort", {
    "text": "str",
    "style": "str",
    "show_net_name": "bool",
}, closed=True)

PadGeometry = TypedDict("PadGeometry", {
    "x_mils": "float",
    "y_mils": "float",
    "width_mils": "float",
    "height_mils": "float",
    "shape": "int",
    "layer": "int",
    "rotation_degrees": "float",
    "corner_radius_mils": NotRequired["float"],
}, closed=True)

LineVertex = TypedDict("LineVertex", {
    "x_mils": "float",
    "y_mils": "float",
    "segment": "Literal[\"line\"]",
}, closed=True)

ArcVertex = TypedDict("ArcVertex", {
    "x_mils": "float",
    "y_mils": "float",
    "segment": "Literal[\"arc\"]",
    "center_mils": "Pair",
    "radius_mils": "float",
    "start_angle_degrees": "float",
    "end_angle_degrees": "float",
}, closed=True)

Pair = list[float]
