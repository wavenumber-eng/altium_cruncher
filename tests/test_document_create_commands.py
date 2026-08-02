from __future__ import annotations

import json
import subprocess
import sys
import uuid
from pathlib import Path

import pytest

from altium_cruncher.altium_cruncher_cmd_pcbdoc import build_pcbdoc_create_mco


PACKAGE_ROOT = Path(__file__).resolve().parents[1]

# StackUpX ids must be GUID strings (Altium's Layer Stack Manager rejects
# anything else), so derive deterministic uuid5 ids from stable role seeds.
_STACKUPX_TEST_ID_NAMESPACE = uuid.UUID("2f0a4a7e-6f0c-4b0f-9a4d-6d1f6a5b9c21")


def _stackupx_test_guid(*parts: object) -> str:
    seed = "|".join(str(part) for part in parts)
    return str(uuid.uuid5(_STACKUPX_TEST_ID_NAMESPACE, seed))


def _skip_without_stackupx_api() -> None:
    import altium_monkey

    required = (
        "AltiumLayerStackDocument",
        "AltiumStackupXDocument",
        "PcbLayerRef",
        "StackupXFeature",
        "StackupXLayer",
        "StackupXProperty",
        "StackupXSpan",
        "StackupXStack",
    )
    if any(not hasattr(altium_monkey, name) for name in required):
        pytest.skip("requires V7-aware altium-monkey StackUpX API")


def _write_signal_stackupx(path: Path, *, signal_layer_count: int) -> None:
    from altium_monkey import (
        AltiumStackupXDocument,
        StackupXFeature,
        StackupXLayer,
        StackupXProperty,
        StackupXSpan,
        StackupXStack,
    )

    copper_type_id = "f4eccd87-2cfb-4f37-be50-4f3a272b4d01"
    prepreg_type_id = "1a79611a-039d-4d40-a204-53c26c50f8b5"
    layers: list[StackupXLayer] = []
    for signal_index in range(signal_layer_count):
        layers.append(
            StackupXLayer(
                id=_stackupx_test_guid("layer-copper", f"{signal_index + 1:03d}"),
                type_id=copper_type_id,
                name=_signal_layer_name(signal_index, signal_layer_count),
                is_shared=True,
                is_enabled=True,
                is_stiffener=None,
                is_adhesive=None,
                properties=(
                    StackupXProperty("Thickness", "LengthValue", "1.4mil"),
                    StackupXProperty("ComponentPlacement", "", "None"),
                ),
                raw_attributes=(),
            )
        )
        if signal_index < signal_layer_count - 1:
            layers.append(
                StackupXLayer(
                    id=_stackupx_test_guid(
                        "layer-dielectric", f"{signal_index + 1:03d}"
                    ),
                    type_id=prepreg_type_id,
                    name=f"Dielectric {signal_index + 1}",
                    is_shared=True,
                    is_enabled=True,
                    is_stiffener=None,
                    is_adhesive=None,
                    properties=(
                        StackupXProperty("Thickness", "LengthValue", "4mil"),
                        StackupXProperty(
                            "DielectricConstant",
                            "DimensionlessValue",
                            "4.200",
                        ),
                        StackupXProperty("Material", "String", "FR-4"),
                    ),
                    raw_attributes=(),
                )
            )
    stack = StackupXStack(
        id=_stackupx_test_guid("stack-main"),
        name=f"{signal_layer_count} Signal Proof",
        stack_type="0",
        is_flex=False,
        is_symmetric=False,
        template_id="",
        layers=tuple(layers),
        via_spans=(
            StackupXSpan(
                id=_stackupx_test_guid("span-through"),
                auto_name="Top Layer-Bottom Layer",
                span_type="Layer",
                start_layer_id=layers[0].id,
                stop_layer_id=layers[-1].id,
                raw_attributes=(),
            ),
        ),
        drill_spans=(),
        raw_attributes=(),
    )
    AltiumStackupXDocument(
        serializer_version="1.1.0.0",
        version="2.1.0.0",
        id=_stackupx_test_guid("stackup-doc", signal_layer_count),
        revision_id=_stackupx_test_guid("stackup-revision", signal_layer_count),
        revision_date="2026-07-30T00:00:00.0000000Z",
        features=(
            StackupXFeature(id="c8939e8a-fd0e-4d52-8860-b7a98f452016", name="Standard"),
        ),
        stackup_attributes=(),
        stacks=(stack,),
        branches=(),
    ).write(path)


def _signal_layer_name(signal_index: int, signal_layer_count: int) -> str:
    if signal_index == 0:
        return "Top Layer"
    if signal_index == signal_layer_count - 1:
        return "Bottom Layer"
    return f"SIG{signal_index + 1:02d}"


def _run_pcbdoc_create_stackupx_cli(
    tmp_path: Path,
    stackupx_file: Path,
) -> tuple[Path, dict[str, object]]:
    output_file = tmp_path / "stackupx_128.PcbDoc"
    mco_file = tmp_path / "stackupx_128.mco.json"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "pcbdoc",
            "create",
            str(output_file),
            "--stackupx-file",
            str(stackupx_file),
            "--mechanical-layer-profile",
            "none",
            "--emit-mco",
            str(mco_file),
            "--json",
        ],
        cwd=PACKAGE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["ok"] is True
    generated_mco = json.loads(mco_file.read_text(encoding="utf-8"))
    return output_file, generated_mco["operations"][0]["args"]


def _pcbdoc_copper_layers(pcbdoc_file: Path) -> list[object]:
    from altium_monkey import AltiumPcbDoc
    from altium_monkey.altium_layer_stack_document import AltiumLayerStackDocument

    pcbdoc = AltiumPcbDoc.from_file(pcbdoc_file)
    stack = AltiumLayerStackDocument.from_pcbdoc(pcbdoc)
    return [
        layer for layer in stack.physical_stacks[0].layers if layer.family == "copper"
    ]


def _assert_128_signal_stack(copper_layers: list[object]) -> None:
    from altium_monkey import PcbLayerRef

    assert len(copper_layers) == 128
    assert copper_layers[0].display_name == "Top Layer"
    assert copper_layers[31].display_name == "SIG32"
    assert copper_layers[126].display_name == "SIG127"
    assert copper_layers[-1].display_name == "Bottom Layer"
    assert int(copper_layers[0].layer_id) == PcbLayerRef.top().v7_saved_layer_id
    assert (
        int(copper_layers[31].layer_id) == PcbLayerRef.mid_layer(31).v7_saved_layer_id
    )
    assert (
        int(copper_layers[126].layer_id) == PcbLayerRef.mid_layer(126).v7_saved_layer_id
    )
    assert int(copper_layers[-1].layer_id) == PcbLayerRef.bottom().v7_saved_layer_id


def test_document_authoring_parent_and_subcommand_help_start() -> None:
    for command in ("schdoc", "schlib", "pcbdoc", "pcblib"):
        for args in (
            (command,),
            (command, "--help"),
            (command, "create", "--help"),
        ):
            completed = subprocess.run(
                [sys.executable, "-m", "altium_cruncher", *args],
                cwd=PACKAGE_ROOT,
                check=False,
                capture_output=True,
                text=True,
            )

            assert completed.returncode == 0, completed.stderr
            assert "usage:" in completed.stdout
            assert command in completed.stdout


def test_schdoc_create_cli_defaults_to_d_sheet(tmp_path: Path) -> None:
    output_file = tmp_path / "fixture.SchDoc"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "schdoc",
            "create",
            str(output_file),
            "--json",
        ],
        cwd=PACKAGE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["ok"] is True

    from altium_monkey import AltiumSchDoc
    from altium_monkey.altium_record_sch__sheet import SheetStyle

    schdoc = AltiumSchDoc(output_file)
    assert schdoc.sheet is not None
    assert schdoc.sheet.sheet_style == SheetStyle.D


def test_schdoc_create_config_first_flow(tmp_path: Path) -> None:
    first_completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "schdoc",
            "create",
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert first_completed.returncode == 0, first_completed.stderr
    assert first_completed.stdout.startswith("\n")
    assert "Writing SchDoc create config template:" in first_completed.stdout
    assert "Please edit it, then rerun `acr schdoc create`" in first_completed.stdout

    config_file = tmp_path / "schdoc_create.jsonc"
    assert config_file.exists()
    assert not (tmp_path / f"{tmp_path.name}.SchDoc").exists()

    second_completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "schdoc",
            "create",
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert second_completed.returncode == 0, second_completed.stderr
    assert "Using SchDoc create config:" in second_completed.stdout
    assert (tmp_path / f"{tmp_path.name}.SchDoc").exists()


def test_schlib_create_cli_writes_one_empty_symbol(tmp_path: Path) -> None:
    output_file = tmp_path / "fixture.SchLib"
    mco_file = tmp_path / "fixture.mco.json"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "schlib",
            "create",
            str(output_file),
            "--symbol",
            "BLANK_SYMBOL",
            "--description",
            "Blank symbol",
            "--emit-mco",
            str(mco_file),
            "--json",
        ],
        cwd=PACKAGE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["ok"] is True
    generated_mco = json.loads(mco_file.read_text(encoding="utf-8"))
    assert [operation["op"] for operation in generated_mco["operations"]] == [
        "schlib.create",
        "schlib.add_symbol",
    ]

    from altium_monkey import AltiumSchLib

    schlib = AltiumSchLib(output_file)
    assert [symbol.name for symbol in schlib.symbols] == ["BLANK_SYMBOL"]
    assert schlib.symbols[0].description == "Blank symbol"


def test_pcbdoc_create_cli_writes_generated_stack_and_mechanical_kinds(
    tmp_path: Path,
) -> None:
    output_file = tmp_path / "fixture.PcbDoc"
    mco_file = tmp_path / "fixture.mco.json"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "pcbdoc",
            "create",
            str(output_file),
            "--layers",
            "4",
            "--mechanical-layer-profile",
            "standard_component_pairs",
            "--emit-mco",
            str(mco_file),
            "--json",
        ],
        cwd=PACKAGE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["ok"] is True
    generated_mco = json.loads(mco_file.read_text(encoding="utf-8"))
    args = generated_mco["operations"][0]["args"]
    assert args["rigid_stack"]["mode"] == "generated_rigid"
    assert len(args["mechanical_layer_kinds"]) == 30

    from altium_monkey import AltiumPcbDoc, MechanicalLayerKind
    from altium_monkey.altium_layer_stack_document import AltiumLayerStackDocument

    pcbdoc = AltiumPcbDoc.from_file(output_file)
    stack = AltiumLayerStackDocument.from_pcbdoc(pcbdoc)
    assert [
        layer.display_name
        for layer in stack.physical_stacks[0].layers
        if layer.family == "copper"
    ] == ["Top Layer", "Mid-Layer 1", "Mid-Layer 2", "Bottom Layer"]
    assert (
        pcbdoc.get_mechanical_layer_kind("MECHANICAL20")
        == MechanicalLayerKind.COURTYARD_TOP
    )


def test_v7_mechanical_53_profile_args_include_numbered_layers() -> None:
    from altium_cruncher.altium_cruncher_project_profiles import (
        mechanical_profile_args,
    )

    profile_args = mechanical_profile_args("v7_mechanical_53")
    mechanical_layers = profile_args["mechanical_layers"]
    mechanical_layer_kinds = profile_args["mechanical_layer_kinds"]

    assert isinstance(mechanical_layers, list)
    assert len(mechanical_layers) == 53
    assert mechanical_layers[31] == {
        "layer": "MECHANICAL32",
        "name": "Mechanical 32",
        "enabled": True,
    }
    assert mechanical_layers[-1] == {
        "layer": "MECHANICAL53",
        "name": "Mechanical 53",
        "enabled": True,
    }
    assert isinstance(mechanical_layer_kinds, list)
    assert {row["layer"] for row in mechanical_layer_kinds} == {
        f"MECHANICAL{index}" for index in range(2, 32)
    }


def test_pcbdoc_create_cli_accepts_v7_mechanical_53_profile_when_available(
    tmp_path: Path,
) -> None:
    import altium_monkey

    if not hasattr(altium_monkey, "coerce_pcb_layer_ref"):
        pytest.skip("requires V7-aware altium-monkey layer API")

    output_file = tmp_path / "fixture_v7.PcbDoc"
    mco_file = tmp_path / "fixture_v7.mco.json"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "pcbdoc",
            "create",
            str(output_file),
            "--mechanical-layer-profile",
            "v7_mechanical_53",
            "--emit-mco",
            str(mco_file),
            "--json",
        ],
        cwd=PACKAGE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["ok"] is True
    generated_mco = json.loads(mco_file.read_text(encoding="utf-8"))
    args = generated_mco["operations"][0]["args"]
    assert len(args["mechanical_layers"]) == 53
    assert args["mechanical_layers"][-1] == {
        "layer": "MECHANICAL53",
        "name": "Mechanical 53",
        "enabled": True,
    }

    from altium_monkey import AltiumPcbDoc
    from altium_monkey.altium_layer_stack_document import AltiumLayerStackDocument

    pcbdoc = AltiumPcbDoc.from_file(output_file)
    stack = AltiumLayerStackDocument.from_pcbdoc(pcbdoc)
    mechanical_53_entries = [
        entry
        for entry in stack.layer_registry.entries
        if entry.family == "mechanical" and entry.v7_layer_id == 16908341
    ]
    assert len(mechanical_53_entries) == 1
    assert mechanical_53_entries[0].display_name == "Mechanical 53"
    assert mechanical_53_entries[0].enabled is True


def test_pcbdoc_create_cli_accepts_stackupx_file_128_signal_when_available(
    tmp_path: Path,
) -> None:
    _skip_without_stackupx_api()

    stackupx_file = tmp_path / "ad26_128_signal.stackupx"
    _write_signal_stackupx(stackupx_file, signal_layer_count=128)

    output_file, args = _run_pcbdoc_create_stackupx_cli(tmp_path, stackupx_file)
    assert args["stackupx_file"] == str(stackupx_file)
    assert "rigid_stack" not in args
    assert "layer_stack_template" not in args
    _assert_128_signal_stack(_pcbdoc_copper_layers(output_file))


def test_pcbdoc_create_rejects_stackupx_file_with_template(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="layer_stack_template or stackupx_file"):
        build_pcbdoc_create_mco(
            tmp_path / "invalid.PcbDoc",
            layer_stack_template="2-layer",
            stackupx_file=tmp_path / "board.stackupx",
        )


def test_pcbdoc_create_config_first_flow(tmp_path: Path) -> None:
    first_completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "pcbdoc",
            "create",
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert first_completed.returncode == 0, first_completed.stderr
    assert first_completed.stdout.startswith("\n")
    assert "Writing PcbDoc create config template:" in first_completed.stdout
    assert "Please edit it, then rerun `acr pcbdoc create`" in first_completed.stdout

    config_file = tmp_path / "pcbdoc_create.jsonc"
    assert config_file.exists()
    config_text = config_file.read_text(encoding="utf-8")
    assert '"schema": "altium_cruncher.pcbdoc.create.config.a0"' in config_text
    assert "Valid mechanical layer ids/indexes/default names:" in config_text
    assert not (tmp_path / f"{tmp_path.name}.PcbDoc").exists()

    second_completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "pcbdoc",
            "create",
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert second_completed.returncode == 0, second_completed.stderr
    assert "Using PcbDoc create config:" in second_completed.stdout
    assert (tmp_path / f"{tmp_path.name}.PcbDoc").exists()
