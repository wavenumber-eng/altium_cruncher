from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import jsonschema

from altium_cruncher.config_json import load_json_config


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def test_project_init_and_create_cli_writes_config_mco_and_project(
    tmp_path: Path,
) -> None:
    config_file = tmp_path / "demo.project.jsonc"
    mco_file = tmp_path / "demo.mco.json"

    init_completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "project",
            "init",
            str(config_file),
            "--project-name",
            "demo",
            "--layers",
            "4",
        ],
        cwd=PACKAGE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert init_completed.returncode == 0, init_completed.stderr
    assert "generated_rigid" in config_file.read_text(encoding="utf-8")
    schema = json.loads(
        (
            PACKAGE_ROOT
            / "docs"
            / "contracts"
            / "project_skeleton_config.v1.schema.json"
        ).read_text(encoding="utf-8")
    )
    jsonschema.validate(load_json_config(config_file), schema)

    create_completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "project",
            "create",
            str(config_file),
            "--emit-mco",
            str(mco_file),
            "--json",
        ],
        cwd=PACKAGE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert create_completed.returncode == 0, create_completed.stderr
    assert json.loads(create_completed.stdout)["ok"] is True

    generated_mco = json.loads(mco_file.read_text(encoding="utf-8"))
    assert [operation["op"] for operation in generated_mco["operations"]] == [
        "project.create",
        "project.add_parameter",
        "schdoc.create",
        "pcbdoc.create",
        "project.add_document",
        "project.add_document",
    ]
    board_args = generated_mco["operations"][3]["args"]
    assert board_args["rigid_stack"]["mode"] == "generated_rigid"
    assert len(board_args["mechanical_layer_pairs"]) == 11

    from altium_monkey import AltiumPcbDoc, AltiumSchDoc, MechanicalLayerKind
    from altium_monkey.altium_layer_stack_document import AltiumLayerStackDocument
    from altium_monkey.altium_prjpcb import AltiumPrjPcb
    from altium_monkey.altium_record_sch__sheet import SheetStyle

    project = AltiumPrjPcb(tmp_path / "demo.PrjPcb")
    assert [document["path"] for document in project.documents] == [
        "demo.SchDoc",
        "demo.PcbDoc",
    ]
    assert project.parameters["ProjectName"] == "demo"

    schdoc = AltiumSchDoc(tmp_path / "demo.SchDoc")
    assert schdoc.sheet is not None
    assert schdoc.sheet.sheet_style == SheetStyle.D

    pcbdoc = AltiumPcbDoc.from_file(tmp_path / "demo.PcbDoc")
    stack = AltiumLayerStackDocument.from_pcbdoc(pcbdoc)
    assert [
        layer.display_name
        for layer in stack.physical_stacks[0].layers
        if layer.family == "copper"
    ] == ["Top Layer", "Mid-Layer 1", "Mid-Layer 2", "Bottom Layer"]
    assert (
        pcbdoc.get_mechanical_layer_kind("MECHANICAL30")
        == MechanicalLayerKind.VALUE_TOP
    )


def test_project_add_sheet_cli_creates_sheet_and_adds_document(tmp_path: Path) -> None:
    config_file = tmp_path / "demo.project.jsonc"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "project",
            "create",
            str(config_file),
            "--defaults",
            "--project-name",
            "demo",
            "--force",
            "--json",
        ],
        cwd=PACKAGE_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    add_completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "project",
            "add-sheet",
            str(tmp_path / "demo.PrjPcb"),
            str(tmp_path / "Power.SchDoc"),
            "--json",
        ],
        cwd=PACKAGE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert add_completed.returncode == 0, add_completed.stderr
    assert json.loads(add_completed.stdout)["ok"] is True

    from altium_monkey.altium_prjpcb import AltiumPrjPcb

    project = AltiumPrjPcb(tmp_path / "demo.PrjPcb")
    assert [document["path"] for document in project.documents] == [
        "demo.SchDoc",
        "demo.PcbDoc",
        "Power.SchDoc",
    ]
