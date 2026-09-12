"""Generated from src/tsp/altium_cruncher/config/creation.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

ProjectSkeletonConfigInput = TypedDict("ProjectSkeletonConfigInput", {
    "schema": "Literal[\"altium_cruncher.project_skeleton.a0\"]",
    "project": "ProjectOutput",
    "schematics": "list[SchdocChild]",
    "pcb": NotRequired["PcbdocChild | None"],
}, extra_items="object")

ProjectOutput = TypedDict("ProjectOutput", {
    "file": "NonemptyString",
    "name": NotRequired["str | None"],
    "parameters": NotRequired["RecordUnknown"],
}, extra_items="object")

SchdocChild = TypedDict("SchdocChild", {
    "file": "NonemptyString",
    "sheet_style": NotRequired["str | int | bool | None"],
    "template": NotRequired["NonemptyString | None"],
    "apply_template_visual_sheet_settings": NotRequired["bool | str | float | None | list[object] | RecordUnknown"],
    "custom_sheet_mils": NotRequired["CustomSheetMils | None"],
}, extra_items="object")

PcbdocChild = TypedDict("PcbdocChild", {
    "file": "NonemptyString",
    "board_outline_mils": NotRequired["BoardOutlineMils | None"],
    "layer_stack": NotRequired["RigidLayerStack | None"],
    "layer_stack_template": NotRequired["str | None"],
    "stackupx_file": NotRequired["NonemptyString | None"],
    "mechanical_layer_profile": NotRequired["Literal[\"none\"] | Literal[\"\"] | Literal[\"standard_component_pairs\"] | Literal[\"standard-component-pairs\"] | Literal[\"v7_mechanical_53\"] | Literal[\"v7-mechanical-53\"] | None | str"],
    "mechanical_layers": NotRequired["list[MechanicalLayer] | None"],
    "mechanical_layer_pairs": NotRequired["list[GroupedMechanicalPair | FlatMechanicalPair] | None"],
    "mechanical_layer_kinds": NotRequired["list[MechanicalKind] | None"],
}, extra_items="object")

CustomSheetMils = TypedDict("CustomSheetMils", {
    "width": "float | bool",
    "height": "float | bool",
}, extra_items="object")

BoardOutlineMils = TypedDict("BoardOutlineMils", {
    "left": "float | bool",
    "bottom": "float | bool",
    "right": "float | bool",
    "top": "float | bool",
}, extra_items="object")

RigidLayerStack = TypedDict("RigidLayerStack", {
    "mode": NotRequired["Literal[\"generated_rigid\"] | None"],
    "name": NotRequired["str | None"],
    "copper_layers": "list[CopperLayer]",
    "dielectrics_between": "list[DielectricLayer]",
}, extra_items="object")

MechanicalLayer = TypedDict("MechanicalLayer", {
    "layer": "NonemptyString",
    "name": NotRequired["NonemptyString | None"],
    "enabled": NotRequired["bool | str | float | None | list[object] | RecordUnknown"],
    "kind": NotRequired["NonemptyString | None"],
}, extra_items="object")

GroupedMechanicalPair = TypedDict("GroupedMechanicalPair", {
    "top": "MechanicalPairSide",
    "bottom": "MechanicalPairSide",
}, extra_items="object")

FlatMechanicalPair = TypedDict("FlatMechanicalPair", {
    "layer_1": "NonemptyString",
    "layer_2": "NonemptyString",
    "pair_index": NotRequired["int | None"],
    "top": NotRequired["Never"],
    "bottom": NotRequired["Never"],
}, extra_items="object")

MechanicalKind = TypedDict("MechanicalKind", {
    "layer": "NonemptyString",
    "kind": "NonemptyString | int",
}, extra_items="object")

CopperLayer = TypedDict("CopperLayer", {
    "name": "NonemptyString",
    "copper_thickness_mils": NotRequired["float | None"],
    "thickness_mils": NotRequired["object"],
    "component_placement": NotRequired["int | None"],
    "copper_orientation": NotRequired["int | None"],
}, extra_items="object")

DielectricLayer = TypedDict("DielectricLayer", {
    "name": "NonemptyString",
    "material": "NonemptyString",
    "thickness_mils": "float",
    "dielectric_constant": "float",
    "dk": NotRequired["object"],
    "dielectric_type": NotRequired["int | None"],
    "type_code": NotRequired["object"],
    "loss_tangent": NotRequired["float | None"],
}, extra_items="object")

MechanicalPairSide = TypedDict("MechanicalPairSide", {
    "layer": "NonemptyString",
    "name": NotRequired["NonemptyString | None"],
    "enabled": NotRequired["bool | str | float | None | list[object] | RecordUnknown"],
    "kind": "NonemptyString",
}, extra_items="object")

RecordUnknown = dict[str, object]
NonemptyString = str
