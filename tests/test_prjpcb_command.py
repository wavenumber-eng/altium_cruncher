from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import jsonschema

from altium_cruncher.altium_cruncher_cmd_prjpcb import (
    default_project_config,
    render_project_config,
)
from altium_cruncher.config_json import load_json_config


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def _cli_env() -> dict[str, str]:
    env = os.environ.copy()
    src_path = str(PACKAGE_ROOT / "src" / "py")
    env["PYTHONPATH"] = (
        src_path
        if not env.get("PYTHONPATH")
        else src_path + os.pathsep + env["PYTHONPATH"]
    )
    return env


def test_prjpcb_init_and_create_cli_writes_config_mco_and_project(
    tmp_path: Path,
) -> None:
    config_file = tmp_path / "demo.project.jsonc"
    mco_file = tmp_path / "demo.mco.json"

    init_completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "prjpcb",
            "init",
            str(config_file),
            "--project-name",
            "demo",
            "--layers",
            "4",
        ],
        cwd=PACKAGE_ROOT,
        env=_cli_env(),
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
            / "project_skeleton_config.a0.schema.json"
        ).read_text(encoding="utf-8")
    )
    jsonschema.validate(load_json_config(config_file), schema)

    create_completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "prjpcb",
            "create",
            str(config_file),
            "--emit-mco",
            str(mco_file),
            "--json",
        ],
        cwd=PACKAGE_ROOT,
        env=_cli_env(),
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
    assert "mechanical_layer_profile" not in board_args
    assert len(board_args["mechanical_layers"]) == 32
    assert len(board_args["mechanical_layer_pairs"]) == 11
    assert len(board_args["mechanical_layer_kinds"]) == 30

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


def test_prjpcb_init_bare_name_writes_named_project_config(tmp_path: Path) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "prjpcb",
            "init",
            "test",
            "--layers",
            "4",
        ],
        cwd=tmp_path,
        env=_cli_env(),
        check=False,
        capture_output=True,
        text=True,
    )

    config_file = tmp_path / "test.project.jsonc"
    assert completed.returncode == 0, completed.stderr
    assert config_file.exists()
    assert not (tmp_path / "test").exists()

    config = load_json_config(config_file)
    assert config["project"]["name"] == "test"
    assert config["project"]["file"] == "test.PrjPcb"
    assert config["schematics"][0]["file"] == "test.SchDoc"
    assert config["pcb"]["file"] == "test.PcbDoc"
    assert len(config["pcb"]["layer_stack"]["copper_layers"]) == 4
    assert "mechanical_layer_profile" not in config["pcb"]
    assert len(config["pcb"]["mechanical_layers"]) == 10
    assert len(config["pcb"]["mechanical_layer_pairs"]) == 11
    assert "mechanical_layer_kinds" not in config["pcb"]
    first_pair = config["pcb"]["mechanical_layer_pairs"][0]
    assert first_pair == {
        "top": {
            "layer": "MECHANICAL10",
            "name": "Top 3D Body",
            "enabled": True,
            "kind": "BODY_3D_TOP",
        },
        "bottom": {
            "layer": "MECHANICAL11",
            "name": "Bottom 3D Body",
            "enabled": True,
            "kind": "BODY_3D_BOTTOM",
        },
    }


def test_prjpcb_generated_config_comments_every_field() -> None:
    text = render_project_config(default_project_config(project_name="demo"))
    assert "Valid mechanical layer ids/indexes/default names:" in text
    assert "//   MECHANICAL1=index 1: Mechanical 1" in text
    assert "//   MECHANICAL32=index 32: Mechanical 32" in text
    assert "Valid mechanical layer kind enum names:" in text
    assert "//   BODY_3D_TOP" in text
    assert "//   WIREBONDING_BOTTOM" in text

    missing_comments: list[str] = []
    previous_content = ""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith('"') and '":' in stripped:
            if not previous_content.startswith("/*"):
                missing_comments.append(stripped)
        if stripped:
            previous_content = stripped

    assert missing_comments == []


def test_prjpcb_no_args_writes_then_uses_auto_config(tmp_path: Path) -> None:
    work_dir = tmp_path / "auto_project"
    work_dir.mkdir()

    first_completed = subprocess.run(
        [sys.executable, "-m", "altium_cruncher", "prjpcb", "create"],
        cwd=work_dir,
        env=_cli_env(),
        check=False,
        capture_output=True,
        text=True,
    )
    assert first_completed.returncode == 0, first_completed.stderr

    assert first_completed.stdout.startswith("\n")
    assert "Writing project init config template:" in first_completed.stdout
    assert "Please edit it, then rerun `acr prjpcb create`" in first_completed.stdout
    config_file = work_dir / "prjpcb_init.jsonc"
    assert config_file.exists()
    assert not (work_dir / "auto_project.PrjPcb").exists()
    config = load_json_config(config_file)
    assert config["project"]["name"] == "auto_project"

    second_completed = subprocess.run(
        [sys.executable, "-m", "altium_cruncher", "prjpcb", "create"],
        cwd=work_dir,
        env=_cli_env(),
        check=False,
        capture_output=True,
        text=True,
    )
    assert second_completed.returncode == 0, second_completed.stderr
    assert second_completed.stdout.startswith("\n")
    assert "Using project init config:" in second_completed.stdout
    assert (work_dir / "auto_project.PrjPcb").exists()
    assert (work_dir / "auto_project.SchDoc").exists()
    assert (work_dir / "auto_project.PcbDoc").exists()

    from altium_monkey.altium_prjpcb import AltiumPrjPcb

    project = AltiumPrjPcb(work_dir / "auto_project.PrjPcb")
    assert [document["path"] for document in project.documents] == [
        "auto_project.SchDoc",
        "auto_project.PcbDoc",
    ]


def test_prjpcb_add_sheet_cli_creates_sheet_and_adds_document(tmp_path: Path) -> None:
    config_file = tmp_path / "demo.project.jsonc"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "prjpcb",
            "create",
            str(config_file),
            "--defaults",
            "--project-name",
            "demo",
            "--force",
            "--json",
        ],
        cwd=PACKAGE_ROOT,
        env=_cli_env(),
        check=True,
        capture_output=True,
        text=True,
    )

    add_completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "prjpcb",
            "add-sheet",
            str(tmp_path / "demo.PrjPcb"),
            str(tmp_path / "Power.SchDoc"),
            "--json",
        ],
        cwd=PACKAGE_ROOT,
        env=_cli_env(),
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


def test_prjpcb_parent_and_subcommand_help_start() -> None:
    for args in (
        ("prjpcb",),
        ("prjpcb", "--help"),
        ("prjpcb", "create", "--help"),
        ("prjpcb", "init", "--help"),
        ("prjpcb", "add-sheet", "--help"),
    ):
        completed = subprocess.run(
            [sys.executable, "-m", "altium_cruncher", *args],
            cwd=PACKAGE_ROOT,
            env=_cli_env(),
            check=False,
            capture_output=True,
            text=True,
        )

        assert completed.returncode == 0, completed.stderr
        assert "usage:" in completed.stdout
        assert "prjpcb" in completed.stdout
