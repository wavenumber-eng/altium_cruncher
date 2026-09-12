"""Static consumer of generated requiredness, record values and open styles."""

from typing import assert_type
from altium_cruncher.contracts.generated.public import decode_contract

builtin_result = decode_contract("mco_builtin_result", {})
if builtin_result["status"] == "ok" and builtin_result["op"] == "pcbdoc.add_via":
    assert_type(builtin_result["outputs"]["position_mils"], list[float])

from altium_cruncher.contracts.generated.pcb_svg_config import (
    ComponentOverride,
    IllustrationStyle,
    PcbSvgConfigInput,
    StyleTable,
)

component = ComponentOverride(show_designator=False)
style = IllustrationStyle(vendor_option=True)
styles = StyleTable(custom={"vendor": {"nested": 1}}, illustration=style)
config: PcbSvgConfigInput = {
    "components": {"J1": component},
    "global": {"styles": styles},
}

from altium_cruncher.contracts.generated.project_skeleton_config import (
    ProjectSkeletonConfigInput,
)
from altium_cruncher.contracts.generated.pcbdoc_create_config import (
    PcbdocCreateConfigInput,
    FlatMechanicalPair,
)

project: ProjectSkeletonConfigInput = {
    "schema": "altium_cruncher.project_skeleton.a0",
    "project": {"file": "a.PrjPcb", "parameters": {"Count": 2}},
    "schematics": [],
    "pcb": None,
    "editor": {"expanded": False},
}
pair = FlatMechanicalPair(
    layer_1="MECHANICAL10", layer_2="MECHANICAL11", pair_index=None
)
pcb: PcbdocCreateConfigInput = {
    "schema": "altium_cruncher.pcbdoc.create.config.a0",
    "file": "a.PcbDoc",
    "mechanical_layer_pairs": [pair],
    "mechanical_layer_kinds": [{"layer": "MECHANICAL2", "kind": 0}],
}

from altium_cruncher.contracts.generated.mco_input import BuiltinOperation, McoDocument

operation: BuiltinOperation = {
    "op": "pcbdoc.add_text",
    "args": {
        "file": "a.PcbDoc",
        "text": "Hi",
        "position_mils": [0, 0],
        "height_mils": 40,
    },
}
document: McoDocument = {"operations": [operation]}
