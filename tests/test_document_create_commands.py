from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


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
