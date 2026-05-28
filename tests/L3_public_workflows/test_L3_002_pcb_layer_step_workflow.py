"""Fixture-backed pcb-layer-step workflow tests."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

from altium_cruncher.altium_cruncher_cmd_pcb_layer_step import cmd_pcb_layer_step

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
CRICKET_PCBDOC = (
    PACKAGE_ROOT
    / "tests"
    / "assets"
    / "projects"
    / "cricket-node"
    / "input"
    / "cricket-node-hw__B.PcbDoc"
)


def test_pcb_layer_step_cricket_bottom_layer_uses_configured_colors(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Generate bottom-layer STEP artifacts from the cricket-node fixture."""
    captured: dict[str, object] = {}

    def write_planar_step(request: dict[str, object], output_path: Path) -> Path:
        captured["request"] = request
        output_path.write_text("ISO-10303-21;\nEND-ISO-10303-21;\n", encoding="utf-8")
        return output_path

    monkeypatch.setitem(
        sys.modules,
        "geometer",
        SimpleNamespace(write_planar_step=write_planar_step),
    )

    output_dir = tmp_path / "output"
    result = cmd_pcb_layer_step(
        SimpleNamespace(
            file=CRICKET_PCBDOC,
            output=output_dir,
            config=tmp_path / "pcb-layer-step.json",
            pcbdoc=None,
            project_context="none",
            layer="bottom",
            thickness_mm=None,
            z_mm=None,
            copper_color="#3D85C6",
            outline_width_mm=None,
            outline_color="#CCCCCC",
            outline_only=False,
            no_board_outline=False,
            exclude_poured_polygons=False,
            no_hole_cuts=False,
            no_fuse=False,
            arc_segments=None,
        )
    )

    assert result == 0
    step_files = list(output_dir.glob("*.step"))
    manifest_files = list(output_dir.glob("*.json"))
    assert len(step_files) == 1
    assert len(manifest_files) == 1
    assert step_files[0].read_text(encoding="utf-8").startswith("ISO-10303-21;")

    manifest = json.loads(manifest_files[0].read_text(encoding="utf-8"))
    assert manifest["schema"] == "wn.altium_cruncher.pcb_layer_step.v1"
    assert manifest["layer"]["json_name"] == "BOTTOM"
    assert manifest["options"]["copper_color"] == "#3D85C6"
    assert manifest["options"]["outline_color"] == "#CCCCCC"
    assert manifest["counts"]["source_layer_geometries"] > 0
    assert manifest["counts"]["outline_bodies"] > 0

    request = cast(dict[str, Any], captured["request"])
    bodies = cast(list[dict[str, Any]], request["bodies"])
    assert bodies[0]["id"] == "copper"
    assert bodies[0]["color"] == "#3D85C6"
    assert bodies[1]["id"] == "drill_holes"
    assert bodies[1]["color"] == "#FFFFFF"
    assert bodies[2]["id"] == "board_outline"
    assert bodies[2]["color"] == "#CCCCCC"
