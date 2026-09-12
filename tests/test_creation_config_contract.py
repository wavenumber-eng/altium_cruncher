"""Shared authored creation-contract conformance and adapter compatibility."""

import json
from pathlib import Path

import pytest

from altium_cruncher.contracts.creation import (
    decode_schdoc_create_config,
    encode_schdoc_create_config,
    decode_pcbdoc_create_config,
    encode_pcbdoc_create_config,
    decode_project_skeleton_config,
    encode_project_skeleton_config,
)

VECTORS = json.loads(
    (Path(__file__).parent / "fixtures/creation-config-vectors.json").read_text()
)
CODECS = {
    "schdoc": (decode_schdoc_create_config, encode_schdoc_create_config),
    "pcbdoc": (decode_pcbdoc_create_config, encode_pcbdoc_create_config),
    "project": (decode_project_skeleton_config, encode_project_skeleton_config),
}


@pytest.mark.parametrize("case", VECTORS, ids=lambda case: case["name"])
def test_shared_creation_vectors(case):
    decode, encode = CODECS[case["family"]]
    original = json.loads(json.dumps(case["value"]))
    if not case["valid"]:
        with pytest.raises(ValueError):
            decode(case["value"])
        return
    result = decode(case["value"])
    assert result == original == case["value"]
    assert result is not case["value"]
    assert json.loads(encode(result)) == original


def test_creation_file_loaders_validate_structure(tmp_path):
    from altium_cruncher.altium_cruncher_cmd_schdoc import load_schdoc_create_config
    from altium_cruncher.altium_cruncher_cmd_pcbdoc import load_pcbdoc_create_config
    from altium_cruncher.altium_cruncher_cmd_prjpcb import load_project_config

    for loader, schema in (
        (load_schdoc_create_config, "altium_cruncher.schdoc.create.config.a0"),
        (load_pcbdoc_create_config, "altium_cruncher.pcbdoc.create.config.a0"),
        (load_project_config, "altium_cruncher.project_skeleton.a0"),
    ):
        path = tmp_path / "config.jsonc"
        path.write_text(json.dumps({"schema": schema}))
        with pytest.raises(ValueError):
            loader(path)


def test_empty_project_and_template_truthiness_keep_adapter_behavior():
    from altium_cruncher.altium_cruncher_cmd_prjpcb import build_project_create_mco
    from altium_cruncher.altium_cruncher_cmd_schdoc import (
        build_schdoc_create_mco_from_config,
    )

    project = decode_project_skeleton_config(
        {
            "schema": "altium_cruncher.project_skeleton.a0",
            "project": {"file": "board.PrjPcb"},
            "schematics": [],
            "pcb": None,
        }
    )
    assert len(build_project_create_mco(dict(project))["operations"]) == 1
    schdoc = decode_schdoc_create_config(
        {
            "schema": "altium_cruncher.schdoc.create.config.a0",
            "file": "board.SchDoc",
            "template": "template.SchDot",
            "apply_template_visual_sheet_settings": "false",
        }
    )
    payload = build_schdoc_create_mco_from_config(dict(schdoc))
    assert (
        payload["operations"][0]["args"]["apply_template_visual_sheet_settings"] is True
    )


def test_integral_json_numbers_lower_to_native_ids_without_mutating_input():
    from altium_cruncher.altium_cruncher_cmd_pcbdoc import (
        build_pcbdoc_create_mco_from_config,
    )

    value = {
        "schema": "altium_cruncher.pcbdoc.create.config.a0",
        "file": "a.PcbDoc",
        "layer_stack": {
            "copper_layers": [
                {"name": "Top", "component_placement": 0.0},
                {"name": "Bottom", "copper_orientation": 1.0},
            ],
            "dielectrics_between": [
                {
                    "name": "Core",
                    "material": "FR-4",
                    "thickness_mils": 58.9,
                    "dielectric_constant": 4.8,
                    "dielectric_type": 0.0,
                }
            ],
        },
        "mechanical_layer_pairs": [
            {"layer_1": "MECHANICAL10", "layer_2": "MECHANICAL11", "pair_index": 1.0}
        ],
        "mechanical_layer_kinds": [{"layer": "MECHANICAL2", "kind": 0.0}],
    }
    decoded = decode_pcbdoc_create_config(value)
    args = build_pcbdoc_create_mco_from_config(dict(decoded))["operations"][0]["args"]
    assert type(args["rigid_stack"]["copper_layers"][0]["component_placement"]) is int
    assert type(args["rigid_stack"]["copper_layers"][1]["copper_orientation"]) is int
    assert type(args["rigid_stack"]["dielectrics_between"][0]["dielectric_type"]) is int
    assert type(args["mechanical_layer_pairs"][0]["pair_index"]) is int
    assert type(args["mechanical_layer_kinds"][0]["kind"]) is int
    assert (
        type(decoded["layer_stack"]["copper_layers"][0]["component_placement"]) is float
    )
    assert type(value["mechanical_layer_pairs"][0]["pair_index"]) is float
