"""Fixture-backed CLI workflow tests for public commands."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


def _project_root() -> Path:
    """Find the repository root from this test file."""
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Could not locate repository root")


PACKAGE_ROOT = _project_root()
HYDROSCOPE_DIR = PACKAGE_ROOT / "examples" / "assets" / "projects" / "hydroscope"
HYDROSCOPE_PROJECT = HYDROSCOPE_DIR / "Hydroscope.PrjPcb"
HYDROSCOPE_SCHDOC = HYDROSCOPE_DIR / "CPU.SchDoc"
HYDROSCOPE_SCHLIB = HYDROSCOPE_DIR / "Hydroscope.SCHLIB"
HYDROSCOPE_PCBDOC = HYDROSCOPE_DIR / "TZ-SB-0001-PCB-[A] (HydroScope Mainboard).PcbDoc"


def _run_cli(*args: str) -> str:
    """Run Altium Cruncher and return combined output."""
    completed = subprocess.run(
        [sys.executable, "-m", "altium_cruncher", *args],
        cwd=PACKAGE_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    combined = completed.stdout + completed.stderr
    assert completed.returncode == 0, combined
    assert "Traceback" not in combined
    assert "Logging error" not in combined
    return combined


def test_schematic_and_design_json_commands_use_public_project(tmp_path: Path) -> None:
    """Exercise Sch SVG, BOM, PnP, and netlist commands on Hydroscope."""
    sch_svg_dir = tmp_path / "sch-svg"
    _run_cli("sch-svg", str(HYDROSCOPE_SCHDOC), "-o", str(sch_svg_dir))
    sch_svg = sch_svg_dir / "CPU.svg"
    assert sch_svg.exists()
    assert "<svg" in sch_svg.read_text(encoding="utf-8", errors="ignore")[:200]

    bom_dir = tmp_path / "bom"
    _run_cli(
        "bom",
        str(HYDROSCOPE_PROJECT),
        "--format",
        "generic-json",
        "-o",
        str(bom_dir),
    )
    bom_payload = json.loads((bom_dir / "Hydroscope_bom.json").read_text(encoding="utf-8"))
    assert bom_payload["schema"] == "wn.altium_cruncher.bom.v1"
    assert bom_payload["component_count"] >= 100

    pnp_dir = tmp_path / "pnp"
    _run_cli("pnp", str(HYDROSCOPE_PROJECT), "--format", "json", "-o", str(pnp_dir))
    pnp_payload = json.loads((pnp_dir / "Hydroscope_pnp.json").read_text(encoding="utf-8"))
    assert pnp_payload["units"] == "mm"
    assert len(pnp_payload["placements"]) >= 100

    netlist_dir = tmp_path / "netlist"
    _run_cli("netlist", str(HYDROSCOPE_PROJECT), "-o", str(netlist_dir))
    netlist_payload = json.loads(
        (netlist_dir / "Hydroscope_netlist.json").read_text(encoding="utf-8")
    )
    assert len(netlist_payload["components"]) >= 100
    assert len(netlist_payload["nets"]) >= 100


def test_library_extract_split_merge_commands_use_public_fixtures(tmp_path: Path) -> None:
    """Exercise library extraction plus split/merge on public Hydroscope files."""
    extract_dir = tmp_path / "extract"
    _run_cli("extract", str(HYDROSCOPE_SCHDOC), "--combined", "-o", str(extract_dir))
    extracted = extract_dir / "CPU.SchLib"
    assert extracted.exists()
    assert extracted.stat().st_size > 0

    split_dir = tmp_path / "split"
    _run_cli("split", str(HYDROSCOPE_SCHLIB), "-o", str(split_dir), "--symbols", "SMT_TEST")
    split_file = split_dir / "SMT_TEST.SchLib"
    assert split_file.exists()
    assert split_file.stat().st_size > 0

    merge_dir = tmp_path / "merge"
    _run_cli("merge", str(split_dir), "-o", str(merge_dir))
    merged_files = list(merge_dir.glob("*.SchLib"))
    assert len(merged_files) == 1
    assert merged_files[0].stat().st_size > 0


def test_pcb_svg_command_uses_public_pcbdoc_without_private_context(tmp_path: Path) -> None:
    """Exercise pcb-svg against a copied public PcbDoc and explicit config."""
    pcbdoc = tmp_path / "board.PcbDoc"
    shutil.copy2(HYDROSCOPE_PCBDOC, pcbdoc)
    config = tmp_path / "pcb-svg.json"
    config.write_text(
        json.dumps(
            {
                "schema": "wn.pcb.svg.config.v1",
                "global": {
                    "include_metadata": True,
                    "show_empty_layers": False,
                },
                "views": [
                    {
                        "name": "layers",
                        "source": "layers",
                        "enabled": True,
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    output_dir = tmp_path / "pcb-svg"
    _run_cli(
        "pcb-svg",
        str(pcbdoc),
        "--config",
        str(config),
        "--export",
        "outline",
        "-o",
        str(output_dir),
    )

    manifest = json.loads((output_dir / "board__views.json").read_text(encoding="utf-8"))
    assert manifest["schema"] == "wn.pcb.svg.eg06.view_manifest.v1"
    assert manifest["board"] == "board"
    assert (output_dir / "layers" / "board__TOP.svg").exists()


def test_clean_command_creates_template_for_public_schdoc_copy(tmp_path: Path) -> None:
    """Exercise clean command template generation without mutating assets."""
    schdoc = tmp_path / "CPU.SchDoc"
    shutil.copy2(HYDROSCOPE_SCHDOC, schdoc)

    _run_cli("clean", str(schdoc))

    config_path = tmp_path / "altium-clean.json"
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    assert payload["schema"] == "wn.altium.clean.config.v1"
