"""Generated from src/tsp/altium_cruncher/outputs/json-dump.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

SchdocDump = TypedDict("SchdocDump", {
    "schema": "Literal[\"altium_cruncher.json_dump.a0\"]",
    "kind": "Literal[\"SchDoc\"]",
    "document": "SchDoc",
}, closed=True)

SchlibDump = TypedDict("SchlibDump", {
    "schema": "Literal[\"altium_cruncher.json_dump.a0\"]",
    "kind": "Literal[\"SchLib\"]",
    "document": "SchLib",
}, closed=True)

PcbdocDump = TypedDict("PcbdocDump", {
    "schema": "Literal[\"altium_cruncher.json_dump.a0\"]",
    "kind": "Literal[\"PcbDoc\"]",
    "document": "PcbDoc",
}, closed=True)

PcblibDump = TypedDict("PcblibDump", {
    "schema": "Literal[\"altium_cruncher.json_dump.a0\"]",
    "kind": "Literal[\"PcbLib\"]",
    "document": "PcbLib",
}, closed=True)

SchDoc = TypedDict("SchDoc", {
    "format": "Literal[\"altium_monkey.schdoc.interop.a0\"]",
}, extra_items="object")

SchLib = TypedDict("SchLib", {
    "format": "Literal[\"altium_monkey.schlib.interop.a0\"]",
}, extra_items="object")

PcbDoc = TypedDict("PcbDoc", {
    "pads": "list[NativeValue]",
    "vias": "list[NativeValue]",
    "tracks": "list[NativeValue]",
    "arcs": "list[NativeValue]",
    "texts": "list[NativeValue]",
    "fills": "list[NativeValue]",
    "regions": "list[NativeValue]",
    "shapebased_regions": "list[NativeValue]",
    "component_bodies": "list[NativeValue]",
    "models": "list[NativeValue]",
    "format": "Literal[\"altium_monkey.pcbdoc.structural.a0\"]",
    "counts": "RecordCount",
    "raw_streams": "list[RawStream]",
    "board": "NativeValue",
    "union_name_records": "list[NativeValue]",
    "smart_unions": "list[NativeValue]",
    "user_unions": "list[UserUnion | UnionError]",
    "components": "list[NativeValue]",
    "nets": "list[NativeValue]",
    "net_classes": "list[NativeValue]",
    "differential_pairs": "list[NativeValue]",
    "polygons": "list[NativeValue]",
    "rules": "list[NativeValue]",
    "dimensions": "list[NativeValue]",
    "extended_primitive_information": "list[NativeValue]",
    "custom_shapes": "list[NativeValue]",
    "via_structures": "list[NativeValue]",
    "via_structure_links": "list[NativeValue]",
    "board_regions": "list[NativeValue]",
    "shapebased_component_bodies": "list[NativeValue]",
    "embedded_fonts": "list[NativeValue]",
    "embedded_models": "list[NativeValue]",
}, closed=True)

PcbLib = TypedDict("PcbLib", {
    "format": "Literal[\"altium_monkey.pcblib.structural.a0\"]",
    "footprint_count": "Count",
    "footprints": "list[Footprint]",
    "models_3d": "NativeValue",
    "raw_streams": "list[RawStream]",
}, closed=True)

RawStream = TypedDict("RawStream", {
    "name": "str",
    "byte_count": "Count",
    "sha256": "str",
}, closed=True)

UserUnion = TypedDict("UserUnion", {
    "union_index": "int",
    "name": "str",
    "member_count": "Count",
    "members": "list[UnionMember]",
}, closed=True)

UnionError = TypedDict("UnionError", {
    "error": "str",
}, closed=True)

Footprint = TypedDict("Footprint", {
    "pads": "list[NativeValue]",
    "vias": "list[NativeValue]",
    "tracks": "list[NativeValue]",
    "arcs": "list[NativeValue]",
    "texts": "list[NativeValue]",
    "fills": "list[NativeValue]",
    "regions": "list[NativeValue]",
    "shapebased_regions": "list[NativeValue]",
    "component_bodies": "list[NativeValue]",
    "models": "list[NativeValue]",
    "name": "str",
    "counts": "RecordCount",
}, closed=True)

UnionMember = TypedDict("UnionMember", {
    "collection": "str",
    "object_index": "int",
    "union_index": "int",
    "object_summary": "MemberSummary",
}, closed=True)

MemberSummary = TypedDict("MemberSummary", {
    "class": NotRequired["str"],
    "designator": NotRequired["NativeValue"],
    "name": NotRequired["NativeValue"],
    "text_content": NotRequired["NativeValue"],
    "footprint": NotRequired["NativeValue"],
    "comment": NotRequired["NativeValue"],
    "x_mils": NotRequired["NativeValue"],
    "y_mils": NotRequired["NativeValue"],
    "start_x_mils": NotRequired["NativeValue"],
    "start_y_mils": NotRequired["NativeValue"],
    "end_x_mils": NotRequired["NativeValue"],
    "end_y_mils": NotRequired["NativeValue"],
    "center_x_mils": NotRequired["NativeValue"],
    "center_y_mils": NotRequired["NativeValue"],
}, closed=True)

JsonDump = SchdocDump | SchlibDump | PcbdocDump | PcblibDump
RecordUnknown = dict[str, object]
NativeValue = object
Count = int
RecordCount = dict[str, Count]
