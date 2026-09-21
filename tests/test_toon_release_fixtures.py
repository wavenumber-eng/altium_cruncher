"""Release-fixture structure and provenance for the Toon closeout gates."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
ANALYTIC = ROOT / "tests/assets/projects/toon-analytic-bodies"
_GENERATOR = runpy.run_path(
    str(ROOT / "tests/support_scripts/generate_toon_analytic_bodies.py")
)
build_board = _GENERATOR["build_board"]
semantic_inventory = _GENERATOR["semantic_inventory"]


def test_analytic_fixture_matches_committed_semantic_inventory_and_manifest():
    pcbdoc = ANALYTIC / "input/toon_analytic_bodies.PcbDoc"
    expected = json.loads((ANALYTIC / "semantic-inventory.json").read_text())
    manifest = json.loads((ANALYTIC / "source-manifest.json").read_text())

    assert semantic_inventory(pcbdoc) == expected
    assert expected["board"] == {
        "component_count": 14,
        "body_count": 19,
        "cutout_count": 1,
    }
    assert {body["model_type"] for body in expected["bodies"]} == {0, 2, 3}
    assert {body["side"] for body in expected["bodies"]} == {"top", "bottom"}
    assert {body["designator"] for body in expected["bodies"]} == {
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "A6",
        "A7",
        "A8",
        "A9",
        "B1",
        "B2",
        "B3",
        "B4",
        "B5",
    }
    record = manifest["files"][0]
    content = pcbdoc.read_bytes()
    assert record["bytes"] == len(content)
    assert record["sha256"] == hashlib.sha256(content).hexdigest()


def test_analytic_generator_has_deterministic_semantics(tmp_path):
    first = build_board(tmp_path / "first.PcbDoc")
    second = build_board(tmp_path / "second.PcbDoc")

    assert semantic_inventory(first) == semantic_inventory(second)
