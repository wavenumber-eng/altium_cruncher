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
    bodies_by_id = {str(body["id"]): body for body in bodies}
    assert "copper" not in bodies_by_id
    assert bodies_by_id["test_points"]["color"] == "#FF0000"
    assert bodies_by_id["board_outline"]["color"] == "#CCCCCC"
    assert manifest["options"]["features"]["tracks"] is False
    assert manifest["options"]["features"]["arcs"] is False


def test_pcb_layer_step_cricket_fixture_variants_compare_request_sizes(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Exercise fixture-focused Cricket Node variants from one JSONC config."""
    captured: list[dict[str, object]] = []

    def write_planar_step(request: dict[str, object], output_path: Path) -> Path:
        captured.append(request)
        payload = json.dumps(request, sort_keys=True)
        output_path.write_text(
            "ISO-10303-21;\n" + payload + "\nEND-ISO-10303-21;\n",
            encoding="utf-8",
        )
        return output_path

    monkeypatch.setitem(
        sys.modules,
        "geometer",
        SimpleNamespace(write_planar_step=write_planar_step),
    )
    config_path = tmp_path / "pcb-layer-step.json"
    config_path.write_text(
        """
        {
          /* Cricket Node fixture-alignment comparison. */
          "schema": "wn.altium_cruncher.pcb_layer_step.config.v2",
          "defaults": {
            "layer": "bottom",
            "board_outline": {"color": "#CCCCCC", "fuse": true}
          },
          "outputs": [
            {
              "name": "fused_with_traces",
              "output_step": "{board}__fused_with_traces.step",
              "features": {
                "tracks": true,
                "arcs": true,
                "fills": false,
                "polygons": false,
                "regions": false,
                "vias": false,
                "component_pads": {
                  "mode": "matching_designators",
                  "include_designators": ["TP*"]
                },
                "free_pads": false
              },
              "colors": {
                "pad_rules": [
                  {"designators": ["TP*"], "color": "red", "body": "test_points"}
                ]
              },
              "drills": {
                "mode": "none"
              },
              "fuse_copper": true
            },
            {
              "name": "nofuse_tp_drill_rings",
              "output_step": "{board}__nofuse_tp_drill_rings.step",
              "features": {
                "tracks": false,
                "arcs": false,
                "fills": false,
                "polygons": false,
                "regions": false,
                "vias": false,
                "component_pads": {
                  "mode": "matching_designators",
                  "include_designators": ["TP*"]
                },
                "free_pads": false
              },
              "colors": {
                "pad_rules": [
                  {"designators": ["TP*"], "color": "red", "body": "test_points"}
                ]
              },
              "drills": {
                "mode": "overlay",
                "minimum_diameter_mm": 0.85,
                "shape": "ring",
                "color": "#666666"
              },
              "fuse_copper": false
            }
          ]
        }
        """,
        encoding="utf-8",
    )

    output_dir = tmp_path / "output"
    result = cmd_pcb_layer_step(
        SimpleNamespace(
            file=CRICKET_PCBDOC,
            output=output_dir,
            config=config_path,
            pcbdoc=None,
            project_context="none",
            layer=None,
            thickness_mm=None,
            z_mm=None,
            copper_color=None,
            outline_width_mm=None,
            outline_color=None,
            outline_only=False,
            no_board_outline=False,
            exclude_poured_polygons=False,
            no_hole_cuts=False,
            no_fuse=False,
            arc_segments=None,
        )
    )

    assert result == 0
    assert len(captured) == 2
    manifests = sorted(output_dir.glob("*.json"))
    assert len(manifests) == 2
    manifest_payloads = [
        json.loads(path.read_text(encoding="utf-8")) for path in manifests
    ]
    byte_sizes = {
        payload["step_file"]: payload["bytes"] for payload in manifest_payloads
    }
    assert len(set(byte_sizes.values())) == 2

    nofuse_request = captured[1]
    bodies = {
        body["id"]: body
        for body in cast(list[dict[str, Any]], nofuse_request["bodies"])
    }
    assert bodies["test_points"]["color"] == "#FF0000"
    assert "fuse_regions" not in bodies["test_points"]
    if "drill_holes" in bodies:
        assert bodies["drill_holes"]["color"] == "#666666"
        assert all("holes" in region for region in bodies["drill_holes"]["regions"])
