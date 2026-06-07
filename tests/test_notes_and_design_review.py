"""Tests for notes extraction and design-review bundle output."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from altium_monkey.altium_record_types import SchPointMils, SchRectMils
from altium_monkey.altium_sch_object_factory import (
    make_sch_note,
    make_sch_text_frame,
    make_sch_text_string,
)
from altium_monkey.altium_schdoc import AltiumSchDoc

from altium_cruncher.altium_cruncher_notes import build_notes_payload


def _write_annotation_schdoc(path: Path) -> None:
    doc = AltiumSchDoc()
    doc.add_object(
        make_sch_note(
            bounds_mils=SchRectMils(100, 200, 500, 420),
            text="Dedicated note\nsecond line",
            author="Reviewer",
        )
    )
    doc.add_object(
        make_sch_text_frame(
            bounds_mils=SchRectMils(700, 200, 1100, 420),
            text="Frame note",
        )
    )
    doc.add_object(
        make_sch_text_string(
            location_mils=SchPointMils(1300, 240),
            text="Free text",
        )
    )
    assert doc.save(path)


def _run_cli(repo_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "altium_cruncher", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )


def test_notes_payload_separates_note_text_frame_and_free_text(tmp_path: Path) -> None:
    """Extract dedicated notes, text frames, and free text into separate arrays."""
    schdoc_path = tmp_path / "annotated.SchDoc"
    _write_annotation_schdoc(schdoc_path)

    payload = build_notes_payload(schdoc_path)

    page = payload["schdocs"][0]
    assert payload["schema"] == "altium_cruncher.notes.a0"
    assert payload["counts"] == {
        "notes": 1,
        "text_frames": 1,
        "free_text": 1,
        "all_text_annotations": 3,
    }
    assert page["notes"][0]["text"] == "Dedicated note\nsecond line"
    assert page["notes"][0]["author"] == "Reviewer"
    assert page["text_frames"][0]["text"] == "Frame note"
    assert page["free_text"][0]["text"] == "Free text"
    assert page["free_text"][0]["position_mils"] == {"x": 1300.0, "y": 240.0}


def test_design_review_bundle_writes_agent_artifacts(tmp_path: Path) -> None:
    """Verify design/dr output contains design, notes, SVG, document JSON, and README."""
    repo_root = Path(__file__).resolve().parents[1]
    schdoc_path = tmp_path / "annotated.SchDoc"
    output_dir = tmp_path / "review"
    _write_annotation_schdoc(schdoc_path)

    result = _run_cli(repo_root, "dr", str(schdoc_path), "-o", str(output_dir))

    assert result.returncode == 0, result.stderr + result.stdout
    manifest = json.loads(
        (output_dir / "design_review_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["schema"] == "altium_cruncher.design_review_manifest.a0"
    assert (output_dir / manifest["design_json"]).exists()
    assert (output_dir / manifest["notes_json"]).exists()
    assert (output_dir / manifest["readme"]).exists()
    assert len(manifest["document_jsons"]) == 1
    assert manifest["document_jsons"][0]["kind"] == "SchDoc"
    assert len(manifest["schematic_svgs"]) == 1
    assert manifest["pcb_svgs"] == []
    readme = (output_dir / "README.md").read_text(encoding="utf-8")
    assert "Altium Design Review Bundle" in readme
