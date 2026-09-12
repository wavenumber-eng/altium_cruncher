"""Generated from src/tsp/altium_cruncher/outputs/mco-builtins.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

Failure = TypedDict("Failure", {
    "op": "str",
    "id": "str",
    "status": "Literal[\"fail\"]",
    "message": "str",
    "outputs": "dict[str, Never]",
    "error": NotRequired["str"],
}, closed=True)

ProjectPath = TypedDict("ProjectPath", {
    "project": "str",
}, closed=True)

NamedProject = TypedDict("NamedProject", {
    "project": "str",
    "name": "str",
}, closed=True)

SectionProject = TypedDict("SectionProject", {
    "project": "str",
    "name": "str",
    "section": "str",
}, closed=True)

DnpAdded = TypedDict("DnpAdded", {
    "project": "str",
    "variant": "str",
    "designator": "str",
    "unique_id": "str",
    "variation": "str",
}, closed=True)

ToggleAdded = TypedDict("ToggleAdded", {
    "project": "str",
    "variant": "str",
    "designator": "str",
    "unique_id": "str",
    "variation": "str",
    "action": "Literal[\"added\"]",
    "dnp": "Literal[True]",
}, closed=True)

ToggleRemoved = TypedDict("ToggleRemoved", {
    "project": "str",
    "variant": "str",
    "designator": "str",
    "action": "Literal[\"removed\"]",
    "dnp": "Literal[False]",
}, closed=True)

TextOutput = TypedDict("TextOutput", {
    "file": "str",
    "text": "str",
}, closed=True)

TextDryRun = TypedDict("TextDryRun", {
    "file": "str",
    "text": "str",
    "font_kind": "str",
    "text_justification": "str | int | None",
}, closed=True)

ArrangeDone = TypedDict("ArrangeDone", {
    "file": "str",
    "updated": "int",
}, closed=True)

ArrangeDryRun = TypedDict("ArrangeDryRun", {
    "file": "str",
    "designators": "int | Literal[\"all\"]",
    "placement": "str",
}, closed=True)

UnionDone = TypedDict("UnionDone", {
    "file": "str",
    "name": "str",
    "union_index": "int",
    "member_count": "int",
}, closed=True)

UnionDryRun = TypedDict("UnionDryRun", {
    "file": "str",
    "name": "str",
}, closed=True)

StepExport = TypedDict("StepExport", {
    "file": "str",
    "step_file": "str",
    "manifest_file": "str",
    "highlight_count": "int",
    "layer": NotRequired["str"],
}, closed=True)

EmbeddedModel = TypedDict("EmbeddedModel", {
    "file": "str",
    "model_file": "str",
    "name": "str",
    "z_mils": NotRequired["float"],
}, closed=True)

ImportedVariantsList = TypedDict("ImportedVariantsList", {
    "schema": "Literal[\"altium_cruncher.variants.list.a0\"]",
    "project": "str",
    "current_variant": "str | None",
    "variant_count": "ImportedVariantsList_Count",
    "variants": "list[ImportedVariantsList_Variant]",
    "rows": "list[ImportedVariantsList_VariantRow]",
    "index_errors": "list[str]",
}, closed=True)

ImportedVariantsList_Variant = TypedDict("ImportedVariantsList_Variant", {
    "name": "str",
    "unique_id": "str",
    "allow_fabrication": "bool",
    "current": "bool",
    "dnp": "list[str]",
    "variation_count": "ImportedVariantsList_Count",
    "parameter_count": "ImportedVariantsList_Count",
    "param_variation_count": "ImportedVariantsList_Count",
    "rows": "list[ImportedVariantsList_VariantRow]",
}, closed=True)

ImportedVariantsList_VariantRow = TypedDict("ImportedVariantsList_VariantRow", {
    "variant": "str",
    "sheet": "str",
    "designator": "str",
    "operation": "str",
    "detail": "str",
    "component_value": "str",
    "parameter_name": "str",
    "value": "str",
    "unique_id": "str",
    "alternate_part": NotRequired["str"],
    "alternate_part_resolved": NotRequired["str"],
}, closed=True)

McoBuiltinResult_anyOf_1 = TypedDict("McoBuiltinResult_anyOf_1", {
    "op": "Literal[\"mco.message\"] | Literal[\"message\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "dict[str, Never]",
}, closed=True)

McoBuiltinResult_anyOf_2 = TypedDict("McoBuiltinResult_anyOf_2", {
    "op": "Literal[\"project.create\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "ProjectPath",
}, closed=True)

McoBuiltinResult_anyOf_3 = TypedDict("McoBuiltinResult_anyOf_3", {
    "op": "Literal[\"project.add_document\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "McoBuiltinResult_anyOf_3_outputs",
}, closed=True)

McoBuiltinResult_anyOf_3_outputs = TypedDict("McoBuiltinResult_anyOf_3_outputs", {
    "project": "str",
    "document": "str",
}, closed=True)

McoBuiltinResult_anyOf_4 = TypedDict("McoBuiltinResult_anyOf_4", {
    "op": "Literal[\"project.add_parameter\"] | Literal[\"project.add_variant\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "NamedProject",
}, closed=True)

McoBuiltinResult_anyOf_5 = TypedDict("McoBuiltinResult_anyOf_5", {
    "op": "Literal[\"project.list_variants\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "ImportedVariantsList",
}, closed=True)

McoBuiltinResult_anyOf_6 = TypedDict("McoBuiltinResult_anyOf_6", {
    "op": "Literal[\"project.delete_variant\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "SectionProject",
}, closed=True)

McoBuiltinResult_anyOf_7 = TypedDict("McoBuiltinResult_anyOf_7", {
    "op": "Literal[\"project.rename_variant\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "McoBuiltinResult_anyOf_7_outputs",
}, closed=True)

McoBuiltinResult_anyOf_7_outputs = TypedDict("McoBuiltinResult_anyOf_7_outputs", {
    "project": "str",
    "name": "str",
    "section": "str",
    "new_name": "str",
}, closed=True)

McoBuiltinResult_anyOf_8 = TypedDict("McoBuiltinResult_anyOf_8", {
    "op": "Literal[\"project.clone_variant\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "McoBuiltinResult_anyOf_8_outputs",
}, closed=True)

McoBuiltinResult_anyOf_8_outputs = TypedDict("McoBuiltinResult_anyOf_8_outputs", {
    "project": "str",
    "name": "str",
    "section": "str",
    "source_name": "str",
    "unique_id": "str",
}, closed=True)

McoBuiltinResult_anyOf_9 = TypedDict("McoBuiltinResult_anyOf_9", {
    "op": "Literal[\"project.add_variant_dnp\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "DnpAdded",
}, closed=True)

McoBuiltinResult_anyOf_10 = TypedDict("McoBuiltinResult_anyOf_10", {
    "op": "Literal[\"project.toggle_variant_dnp\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "ToggleAdded | ToggleRemoved",
}, closed=True)

McoBuiltinResult_anyOf_11 = TypedDict("McoBuiltinResult_anyOf_11", {
    "op": "Literal[\"schdoc.create\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "McoBuiltinResult_anyOf_11_outputs",
}, closed=True)

McoBuiltinResult_anyOf_11_outputs = TypedDict("McoBuiltinResult_anyOf_11_outputs", {
    "schematic": "str",
}, closed=True)

McoBuiltinResult_anyOf_12 = TypedDict("McoBuiltinResult_anyOf_12", {
    "op": "Literal[\"pcbdoc.create\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "McoBuiltinResult_anyOf_12_outputs",
}, closed=True)

McoBuiltinResult_anyOf_12_outputs = TypedDict("McoBuiltinResult_anyOf_12_outputs", {
    "board": "str",
}, closed=True)

McoBuiltinResult_anyOf_13 = TypedDict("McoBuiltinResult_anyOf_13", {
    "op": "Literal[\"schlib.create\"] | Literal[\"pcblib.create\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "McoBuiltinResult_anyOf_13_outputs",
}, closed=True)

McoBuiltinResult_anyOf_13_outputs = TypedDict("McoBuiltinResult_anyOf_13_outputs", {
    "library": "str",
}, closed=True)

McoBuiltinResult_anyOf_14 = TypedDict("McoBuiltinResult_anyOf_14", {
    "op": "Literal[\"schlib.add_symbol\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "McoBuiltinResult_anyOf_14_outputs",
}, closed=True)

McoBuiltinResult_anyOf_14_outputs = TypedDict("McoBuiltinResult_anyOf_14_outputs", {
    "library": "str",
    "symbol": "str",
}, closed=True)

McoBuiltinResult_anyOf_15 = TypedDict("McoBuiltinResult_anyOf_15", {
    "op": "Literal[\"file.copy\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "McoBuiltinResult_anyOf_15_outputs",
}, closed=True)

McoBuiltinResult_anyOf_15_outputs = TypedDict("McoBuiltinResult_anyOf_15_outputs", {
    "source": "str",
    "destination": "str",
}, closed=True)

McoBuiltinResult_anyOf_16 = TypedDict("McoBuiltinResult_anyOf_16", {
    "op": "Literal[\"schdoc.add_wire\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "McoBuiltinResult_anyOf_16_outputs",
}, closed=True)

McoBuiltinResult_anyOf_16_outputs = TypedDict("McoBuiltinResult_anyOf_16_outputs", {
    "file": "str",
    "points": "int",
}, closed=True)

McoBuiltinResult_anyOf_17 = TypedDict("McoBuiltinResult_anyOf_17", {
    "op": "Literal[\"schdoc.add_net_label\"] | Literal[\"schdoc.add_power_port\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "TextOutput",
}, closed=True)

McoBuiltinResult_anyOf_18 = TypedDict("McoBuiltinResult_anyOf_18", {
    "op": "Literal[\"pcbdoc.add_text\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "TextOutput | TextDryRun",
}, closed=True)

McoBuiltinResult_anyOf_19 = TypedDict("McoBuiltinResult_anyOf_19", {
    "op": "Literal[\"schdoc.add_component\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "McoBuiltinResult_anyOf_19_outputs",
}, closed=True)

McoBuiltinResult_anyOf_19_outputs = TypedDict("McoBuiltinResult_anyOf_19_outputs", {
    "file": "str",
    "library": "str",
    "symbol": "str",
    "designator": "str",
}, closed=True)

McoBuiltinResult_anyOf_20 = TypedDict("McoBuiltinResult_anyOf_20", {
    "op": "Literal[\"pcbdoc.add_component\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "McoBuiltinResult_anyOf_20_outputs",
}, closed=True)

McoBuiltinResult_anyOf_20_outputs = TypedDict("McoBuiltinResult_anyOf_20_outputs", {
    "file": "str",
    "library": "str",
    "footprint": "str",
    "designator": "str",
}, closed=True)

McoBuiltinResult_anyOf_21 = TypedDict("McoBuiltinResult_anyOf_21", {
    "op": "Literal[\"pcblib.add_footprint\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "McoBuiltinResult_anyOf_21_outputs",
}, closed=True)

McoBuiltinResult_anyOf_21_outputs = TypedDict("McoBuiltinResult_anyOf_21_outputs", {
    "file": "str",
    "footprint": "str",
    "parameters": "int",
    "primitive_parameters": "int",
}, closed=True)

McoBuiltinResult_anyOf_22 = TypedDict("McoBuiltinResult_anyOf_22", {
    "op": "Literal[\"pcbdoc.arrange_designators\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "ArrangeDone | ArrangeDryRun",
}, closed=True)

McoBuiltinResult_anyOf_23 = TypedDict("McoBuiltinResult_anyOf_23", {
    "op": "Literal[\"pcbdoc.add_track\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "McoBuiltinResult_anyOf_23_outputs",
}, closed=True)

McoBuiltinResult_anyOf_23_outputs = TypedDict("McoBuiltinResult_anyOf_23_outputs", {
    "file": "str",
    "width_mils": "float",
}, closed=True)

McoBuiltinResult_anyOf_24 = TypedDict("McoBuiltinResult_anyOf_24", {
    "op": "Literal[\"pcbdoc.add_arc\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "McoBuiltinResult_anyOf_24_outputs",
}, closed=True)

McoBuiltinResult_anyOf_24_outputs = TypedDict("McoBuiltinResult_anyOf_24_outputs", {
    "file": "str",
    "radius_mils": "float",
}, closed=True)

McoBuiltinResult_anyOf_25 = TypedDict("McoBuiltinResult_anyOf_25", {
    "op": "Literal[\"pcbdoc.add_pad\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "McoBuiltinResult_anyOf_25_outputs",
}, closed=True)

McoBuiltinResult_anyOf_25_outputs = TypedDict("McoBuiltinResult_anyOf_25_outputs", {
    "file": "str",
    "designator": "str",
}, closed=True)

McoBuiltinResult_anyOf_26 = TypedDict("McoBuiltinResult_anyOf_26", {
    "op": "Literal[\"pcbdoc.add_via\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "McoBuiltinResult_anyOf_26_outputs",
}, closed=True)

McoBuiltinResult_anyOf_26_outputs = TypedDict("McoBuiltinResult_anyOf_26_outputs", {
    "file": "str",
    "position_mils": "Pair",
}, closed=True)

McoBuiltinResult_anyOf_27 = TypedDict("McoBuiltinResult_anyOf_27", {
    "op": "Literal[\"pcbdoc.add_fill\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "McoBuiltinResult_anyOf_27_outputs",
}, closed=True)

McoBuiltinResult_anyOf_27_outputs = TypedDict("McoBuiltinResult_anyOf_27_outputs", {
    "file": "str",
    "corner1_mils": "Pair",
}, closed=True)

McoBuiltinResult_anyOf_28 = TypedDict("McoBuiltinResult_anyOf_28", {
    "op": "Literal[\"pcbdoc.add_region\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "McoBuiltinResult_anyOf_28_outputs",
}, closed=True)

McoBuiltinResult_anyOf_28_outputs = TypedDict("McoBuiltinResult_anyOf_28_outputs", {
    "file": "str",
    "points": "int",
    "is_board_cutout": "bool",
}, closed=True)

McoBuiltinResult_anyOf_29 = TypedDict("McoBuiltinResult_anyOf_29", {
    "op": "Literal[\"pcbdoc.create_user_union\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "UnionDone | UnionDryRun",
}, closed=True)

McoBuiltinResult_anyOf_30 = TypedDict("McoBuiltinResult_anyOf_30", {
    "op": "Literal[\"pcbdoc.export_layer_step\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "StepExport",
}, closed=True)

McoBuiltinResult_anyOf_31 = TypedDict("McoBuiltinResult_anyOf_31", {
    "op": "Literal[\"pcbdoc.add_embedded_3d_model\"]",
    "id": "str",
    "status": "Literal[\"ok\"]",
    "message": "str",
    "outputs": "EmbeddedModel",
}, closed=True)

McoBuiltinResult = Failure | McoBuiltinResult_anyOf_1 | McoBuiltinResult_anyOf_2 | McoBuiltinResult_anyOf_3 | McoBuiltinResult_anyOf_4 | McoBuiltinResult_anyOf_5 | McoBuiltinResult_anyOf_6 | McoBuiltinResult_anyOf_7 | McoBuiltinResult_anyOf_8 | McoBuiltinResult_anyOf_9 | McoBuiltinResult_anyOf_10 | McoBuiltinResult_anyOf_11 | McoBuiltinResult_anyOf_12 | McoBuiltinResult_anyOf_13 | McoBuiltinResult_anyOf_14 | McoBuiltinResult_anyOf_15 | McoBuiltinResult_anyOf_16 | McoBuiltinResult_anyOf_17 | McoBuiltinResult_anyOf_18 | McoBuiltinResult_anyOf_19 | McoBuiltinResult_anyOf_20 | McoBuiltinResult_anyOf_21 | McoBuiltinResult_anyOf_22 | McoBuiltinResult_anyOf_23 | McoBuiltinResult_anyOf_24 | McoBuiltinResult_anyOf_25 | McoBuiltinResult_anyOf_26 | McoBuiltinResult_anyOf_27 | McoBuiltinResult_anyOf_28 | McoBuiltinResult_anyOf_29 | McoBuiltinResult_anyOf_30 | McoBuiltinResult_anyOf_31
Pair = list[float]
ImportedVariantsList_Count = int
