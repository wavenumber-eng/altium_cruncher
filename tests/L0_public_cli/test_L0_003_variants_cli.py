from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[2]


def _cli_env() -> dict[str, str]:
    env = os.environ.copy()
    pythonpath = str(PACKAGE_ROOT / "src" / "py")
    if env.get("PYTHONPATH"):
        pythonpath = pythonpath + os.pathsep + env["PYTHONPATH"]
    env["PYTHONPATH"] = pythonpath
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def _write_project(path: Path, *, variant: str = "A") -> None:
    from altium_monkey.altium_prjpcb import AltiumPrjPcb

    project = AltiumPrjPcb.create_minimal(path.stem)
    project.add_variant(variant, unique_id=f"{variant}-GUID", allow_fabrication=True)
    project.save(path)


def test_variants_cli_auto_detects_project_and_edits_dnp(tmp_path: Path) -> None:
    project_path = tmp_path / "demo.PrjPcb"
    _write_project(project_path)

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "variants",
            "toggle-dnp",
            "A",
            "R1",
            "--unique-id",
            "R1UID",
        ],
        cwd=tmp_path,
        env=_cli_env(),
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert "marked DNP R1" in completed.stdout

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "variants",
            "list",
            "--json",
        ],
        cwd=tmp_path,
        env=_cli_env(),
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["schema"] == "altium_cruncher.variants.list.a0"
    assert payload["project"] == str(project_path.resolve())
    assert payload["variants"][0]["dnp"] == ["R1"]
    assert payload["rows"][0]["operation"] == "DNP"

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "variants",
        ],
        cwd=tmp_path,
        env=_cli_env(),
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert "Changes By Variant" in completed.stdout
    assert "R1" in completed.stdout
    assert "DNP" in completed.stdout

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "variants",
            "toggle-dnp",
            "A",
            "R1",
        ],
        cwd=tmp_path,
        env=_cli_env(),
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert "reverted to fitted R1" in completed.stdout

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "variants",
            "list",
            "--json",
        ],
        cwd=tmp_path,
        env=_cli_env(),
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["variants"][0]["dnp"] == []
    assert payload["rows"] == []

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "variants",
            "list",
            "--no-color",
        ],
        cwd=tmp_path,
        env=_cli_env(),
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert "Changes By Variant" in completed.stdout
    assert "No DNP or parameter changes." in completed.stdout


def test_variants_cli_refuses_ambiguous_cwd_projects(tmp_path: Path) -> None:
    _write_project(tmp_path / "alpha.PrjPcb")
    _write_project(tmp_path / "beta.PrjPcb")

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "variants",
            "list",
        ],
        cwd=tmp_path,
        env=_cli_env(),
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 1
    assert "Multiple .PrjPcb files found" in completed.stderr
    assert "alpha.PrjPcb" in completed.stderr
    assert "beta.PrjPcb" in completed.stderr


def test_variants_cli_missing_args_lists_available_variants(tmp_path: Path) -> None:
    _write_project(tmp_path / "demo.PrjPcb", variant="B4")

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "variants",
            "clone",
        ],
        cwd=tmp_path,
        env=_cli_env(),
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 1
    assert "missing required argument(s): source_name, name" in completed.stderr
    assert "Available variants: B4" in completed.stderr


def test_variants_cli_help_lists_toggle_dnp_command() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "variants",
            "--help",
        ],
        cwd=PACKAGE_ROOT,
        env=_cli_env(),
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert "toggle-dnp" in completed.stdout
    assert "toggle one designator DNP in a variant" in completed.stdout
    assert "add-dnp" not in completed.stdout


def test_variants_cli_resolves_altium_value_expressions() -> None:
    project_path = (
        PACKAGE_ROOT
        / "tests"
        / "assets"
        / "projects"
        / "node_test_array"
        / "input"
        / "11-10077__node-test-array__B4.PrjPcb"
    )

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "variants",
            "list",
            str(project_path),
            "--json",
        ],
        env=_cli_env(),
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    dnp_row = next(
        row
        for row in payload["rows"]
        if row["designator"] == "R26_1" and row["operation"] == "DNP"
    )
    param_row = next(
        row
        for row in payload["rows"]
        if row["designator"] == "R26_1" and row["operation"] == "parameter"
    )
    assert dnp_row["alternate_part"] == "=Value"
    assert dnp_row["alternate_part_resolved"] == "0\u03a9"
    assert dnp_row["component_value"] == "0\u03a9"
    assert "alternate_part=0\u03a9 (from =Value)" in dnp_row["detail"]
    assert param_row["raw_value"] == "=Value"
    assert param_row["resolved_value"] == "0\u03a9"
    assert param_row["component_value"] == "0\u03a9"
