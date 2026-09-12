"""MCO transport and execution boundaries that must survive contract generation."""

import json
from pathlib import Path

import pytest

from altium_cruncher.contracts.mco import (
    decode_mco,
    encode_mco,
    mco_metadata,
    validate_builtin_args,
)
from altium_cruncher.altium_cruncher_mco import (
    DEFAULT_MCO_OPERATIONS,
    McoExecutionContext,
    McoOperationResult,
    execute_mco,
    parse_mco_operations,
    mco_operation_catalog,
)

VECTORS = json.loads(
    (Path(__file__).parent / "fixtures/mco-contract-vectors.json").read_text()
)


@pytest.mark.parametrize("case", VECTORS, ids=lambda case: case["name"])
def test_shared_mco_vectors(case):
    original = json.loads(json.dumps(case["value"]))
    if not case["valid"]:
        with pytest.raises(ValueError):
            decode_mco(case["value"])
        return
    value = decode_mco(case["value"])
    assert value == original == case["value"]
    assert value is not case["value"]
    assert json.loads(encode_mco(value)) == original


def test_catalog_and_handlers_cover_the_same_contract_operations():
    infos = mco_operation_catalog()
    assert {info.name for info in infos} == {
        info["name"] for info in mco_metadata()["operations"]
    }
    assert set(DEFAULT_MCO_OPERATIONS) == {
        tag for info in infos for tag in [info.name, *info.aliases]
    }
    by_name = {info.name: info for info in infos}
    assert "height_mils" in by_name["pcbdoc.add_text"].required_args
    assert "output_file" in by_name["pcbdoc.add_text"].optional_args
    assert "inverted_box" not in by_name["pcbdoc.add_text"].optional_args
    assert "designators" in by_name["pcbdoc.arrange_designators"].optional_args
    assert "layer" in by_name["pcbdoc.export_layer_step"].optional_args


def test_bad_builtin_arguments_can_recover_and_skipped_arguments_are_not_checked(
    tmp_path,
):
    payload = [
        {"op": "file.copy", "id": "try", "on_fail": "recover"},
        {"op": "pcbdoc.add_text", "id": "skip", "args": {"invalid": object()}},
        {"op": "message", "id": "recover", "args": {"text": "Recovered"}},
    ]
    result = execute_mco(payload, McoExecutionContext(work_dir=tmp_path))
    assert result.ok
    assert [item.operation_id for item in result.results] == ["try", "recover"]
    assert result.results[0].status == "fail"


def test_custom_registry_replacement_keeps_its_own_argument_contract(tmp_path):
    token = object()
    seen = []

    def custom(spec, context):
        seen.append(spec.args["token"])
        return McoOperationResult.succeeded(spec, "custom")

    result = execute_mco(
        [
            {"op": "file.copy", "args": {"token": token}},
            {"op": "my.operation", "args": {"token": token}},
        ],
        McoExecutionContext(work_dir=tmp_path),
        registry={"file.copy": custom, "my.operation": custom},
    )
    assert result.ok
    assert seen == [token, token]


def test_programmatic_tuple_points_and_integral_native_ids_preserve_authored_input():
    from collections import namedtuple

    Point = namedtuple("Point", ["x", "y"])
    args = {
        "file": "board.PcbDoc",
        "designator": "1",
        "position_mils": Point(0.0, 1.0),
        "width_mils": 10.0,
        "height_mils": 20.0,
        "layer": 1.0,
        "solder_mask_expansion_mode": 0.0,
    }
    normalized = validate_builtin_args("pcbdoc.add_pad", args)
    assert normalized["position_mils"] == (0.0, 1.0)
    assert isinstance(normalized["position_mils"], tuple)
    assert normalized["position_mils"] is args["position_mils"]
    assert type(normalized["layer"]) is int
    assert type(normalized["solder_mask_expansion_mode"]) is int
    assert type(args["layer"]) is float
    with pytest.raises(ValueError):
        decode_mco([{"op": "pcbdoc.add_pad", "args": args}])


def test_dry_run_keeps_existing_partial_checks(tmp_path):
    result = execute_mco(
        [
            {
                "op": "pcbdoc.add_pad",
                "args": {
                    "file": "a.PcbDoc",
                    "overwrite": True,
                    "designator": "1",
                    "position_mils": [0, 0],
                },
            }
        ],
        McoExecutionContext(work_dir=tmp_path, dry_run=True),
    )
    assert result.ok  # Legacy dry-run path does not read width/height.


def test_builtin_handler_can_be_registered_under_a_custom_name(tmp_path):
    result = execute_mco(
        [{"op": "custom.create", "args": {"file": "custom.PrjPcb"}}],
        McoExecutionContext(work_dir=tmp_path, dry_run=True),
        registry={"custom.create": DEFAULT_MCO_OPERATIONS["project.create"]},
    )
    assert result.ok


def test_operation_id_defaults_precede_duplicate_detection():
    assert [
        item.operation_id
        for item in parse_mco_operations(
            [
                {"op": "message", "id": None},
                {"op": "message", "id": ""},
            ]
        )
    ] == ["op1", "op2"]
    with pytest.raises(ValueError, match="Duplicate MCO operation id"):
        parse_mco_operations([{"op": "message"}, {"op": "message", "id": "op1"}])
