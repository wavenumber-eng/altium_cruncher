"""Tests for notes extraction and design-review bundle output."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

import jsonc  # type: ignore[import-untyped]
import pytest

from altium_monkey.altium_record_types import SchPointMils, SchRectMils
from altium_monkey.altium_sch_object_factory import (
    make_sch_note,
    make_sch_text_frame,
    make_sch_text_string,
)
from altium_monkey.altium_schdoc import AltiumSchDoc

from altium_cruncher.altium_cruncher_notes import build_notes_payload
from altium_cruncher.altium_cruncher_design_review import (
    _enrich_schematic_svg,
    _write_project_schematic_artifacts,
)


_LOW_LEVEL_NOTE_KEYS = {
    "source_scope",
    "owner_index",
    "is_hidden",
    "orientation",
    "justification",
    "alignment",
    "page_number",
    "page_count",
    "page_name",
    "object_type",
    "collapsed",
    "kind",
}


def _assert_sparse_note_entry(entry: dict[str, object]) -> None:
    assert not (_LOW_LEVEL_NOTE_KEYS & set(entry))


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


def _write_annotation_schdoc_with_template_text(path: Path) -> None:
    doc = AltiumSchDoc()
    doc.add_object(
        make_sch_text_frame(
            bounds_mils=SchRectMils(100, 200, 500, 420),
            text="User frame note",
        )
    )
    doc.add_object(
        make_sch_text_string(
            location_mils=SchPointMils(700, 240),
            text="User free text",
        )
    )
    template_frame = make_sch_text_frame(
        bounds_mils=SchRectMils(1000, 200, 1400, 420),
        text="=TITLE_BLOCK_FIELD",
    )
    template_frame._owner_index = 1
    doc.add_object(template_frame)
    template_text = make_sch_text_string(
        location_mils=SchPointMils(1500, 240),
        text="Sheet Number",
    )
    template_text._owner_index = 1
    doc.add_object(template_text)
    assert doc.save(path)


def _write_review_pcb_project(project_path: Path) -> Path:
    from altium_monkey import AltiumPcbDoc, PcbLayer
    from altium_monkey.altium_prjpcb import AltiumPrjPcb
    from altium_monkey.altium_schdoc import AltiumSchDoc

    pcbdoc_path = project_path.with_suffix(".PcbDoc")
    schdoc_path = project_path.with_suffix(".SchDoc")
    AltiumSchDoc().save(schdoc_path)

    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(0, 0, 1000, 700)
    pcbdoc.set_layer_stack_template("4-layer")
    pcbdoc.add_track((100, 100), (900, 100), width_mils=10, layer=PcbLayer.TOP)
    pcbdoc.add_track((100, 175), (900, 175), width_mils=10, layer=PcbLayer.MID1)
    pcbdoc.add_track((100, 250), (900, 250), width_mils=10, layer=PcbLayer.BOTTOM)
    pcbdoc.save(pcbdoc_path)

    project = AltiumPrjPcb()
    project.add_document(schdoc_path.name)
    project.add_document(pcbdoc_path.name)
    project.save(project_path)
    return pcbdoc_path


def _run_cli(repo_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    python_paths = [str(repo_root / "src" / "py")]
    monkey_dev_src = Path(
        os.environ.get("ALTIUM_MONKEY_DEV", r"C:\eli\altium_monkey_dev")
    ) / "src" / "py"
    if monkey_dev_src.exists():
        python_paths.insert(0, str(monkey_dev_src))
    env["PYTHONPATH"] = (
        os.pathsep.join(python_paths)
        if not env.get("PYTHONPATH")
        else os.pathsep.join(python_paths) + os.pathsep + env["PYTHONPATH"]
    )
    return subprocess.run(
        [sys.executable, "-m", "altium_cruncher", *args],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def _node_test_array_project_path() -> Path:
    corpus_root = Path(os.environ.get("WN_TEST_CORPUS", r"C:\eli\wn_test_corpus"))
    project_path = (
        corpus_root
        / "altium"
        / "common"
        / "real_world_pcbdoc"
        / "node_test_array"
        / "input"
        / "11-10077__node-test-array__B4.PrjPcb"
    )
    if not project_path.exists():
        pytest.skip(f"node_test_array corpus fixture not found: {project_path}")
    return project_path


def _iter_json_strings(value: object) -> Iterator[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from _iter_json_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_json_strings(child)


def test_notes_payload_separates_note_text_frame_and_free_text(tmp_path: Path) -> None:
    """Extract dedicated notes, text frames, and free text into separate arrays."""
    schdoc_path = tmp_path / "annotated.SchDoc"
    _write_annotation_schdoc(schdoc_path)

    payload = build_notes_payload(schdoc_path)

    page = payload["schdocs"][0]
    assert payload["schema"] == "altium_cruncher.notes.a0"
    assert payload["input"] == "annotated.SchDoc"
    assert payload["path_base"] == "input_directory"
    assert page["notes"][0]["text"] == "Dedicated note\nsecond line"
    assert page["notes"][0]["author"] == "Reviewer"
    assert "unique_id" in page["notes"][0]
    _assert_sparse_note_entry(page["notes"][0])
    assert page["text_frames"][0]["text"] == "Frame note"
    assert "unique_id" in page["text_frames"][0]
    _assert_sparse_note_entry(page["text_frames"][0])
    assert page["free_text"][0]["text"] == "Free text"
    assert page["free_text"][0]["position_mils"] == {"x": 1300.0, "y": 240.0}
    assert "unique_id" in page["free_text"][0]
    _assert_sparse_note_entry(page["free_text"][0])
    assert "counts" not in payload
    assert "suppressed_counts" not in payload
    assert "counts" not in page
    assert "suppressed_counts" not in page
    assert "page_number" not in page
    assert "page_count" not in page
    assert not Path(str(page["file"])).is_absolute()


def test_notes_payload_suppresses_sheet_template_text_by_default(
    tmp_path: Path,
) -> None:
    """Suppress sheet-template/title-block text while keeping authored annotations."""
    schdoc_path = tmp_path / "annotated.SchDoc"
    _write_annotation_schdoc_with_template_text(schdoc_path)

    payload = build_notes_payload(schdoc_path)
    raw_payload = build_notes_payload(
        schdoc_path,
        include_sheet_template_text=True,
    )

    page = payload["schdocs"][0]
    assert "notes" not in page
    assert page["text_frames"][0]["text"] == "User frame note"
    assert page["free_text"][0]["text"] == "User free text"
    assert len(page["text_frames"]) == 1
    assert len(page["free_text"]) == 1
    raw_page = raw_payload["schdocs"][0]
    assert [entry["text"] for entry in raw_page["text_frames"]] == [
        "User frame note",
        "=TITLE_BLOCK_FIELD",
    ]
    assert [entry["text"] for entry in raw_page["free_text"]] == [
        "User free text",
        "Sheet Number",
    ]
    for entries in (raw_page["text_frames"], raw_page["free_text"]):
        for entry in entries:
            _assert_sparse_note_entry(entry)
    assert "counts" not in raw_payload
    assert "suppressed_counts" not in raw_payload


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
    assert manifest["input"] == "annotated.SchDoc"
    assert str(manifest["design_json"]).startswith("design/")
    assert (output_dir / manifest["design_json"]).exists()
    assert (output_dir / manifest["notes_json"]).exists()
    assert (output_dir / manifest["readme"]).exists()
    assert str(manifest["notes_json"]).endswith(".jsonc")
    assert len(manifest["document_jsons"]) == 1
    assert manifest["document_jsons"][0]["kind"] == "SchDoc"
    assert manifest["document_jsons"][0]["source"] == "annotated.SchDoc"
    assert manifest["document_jsons"][0]["file"].startswith("json/schdoc/")
    assert len(manifest["schematic_svgs"]) == 1
    assert manifest["schematic_svgs"][0]["source"] == "annotated.SchDoc"
    assert manifest["schematic_svgs"][0]["file"].startswith("sch/")
    assert manifest["schematic_irs"] == []
    assert manifest["pcb_svgs"] == []
    assert "Document JSON: json/schdoc/annotated.SchDoc.json" in result.stdout
    assert "Schematic SVG: sch/annotated.svg" in result.stdout
    schematic_svg = (output_dir / manifest["schematic_svgs"][0]["file"]).read_text(
        encoding="utf-8",
    )
    assert "altium_monkey.schematic.svg.enrichment.a0" in schematic_svg
    assert 'data-review-theme="altium_cruncher.design_review.schematic_svg.a0"' in schematic_svg
    assert 'id="schematic-enrichment-a0"' in schematic_svg
    notes_text = (output_dir / manifest["notes_json"]).read_text(encoding="utf-8")
    assert notes_text.startswith("/*\naltium-cruncher notes artifact")
    notes_payload = jsonc.loads(notes_text)
    assert notes_payload["schema"] == "altium_cruncher.notes.a0"
    assert notes_payload["input"] == "annotated.SchDoc"
    readme = (output_dir / "README.md").read_text(encoding="utf-8")
    assert "Altium Design Review Bundle" in readme
    assert "https://github.com/wavenumber-eng/altium_monkey" in readme
    assert "parsed-document dumps" in readme
    assert "altium_monkey.schdoc.interop.a0" in readme
    assert "BOM-like part of the netlist" in readme
    assert "Power-Tree Review Hint" in readme
    assert "compiled, resolved schematic pages" in readme
    assert "sch-ir/" in readme
    assert "zero-ohm" in readme
    assert "current-sense resistors" in readme
    assert "indexes.component_to_nets" in readme


def test_design_review_uses_design_review_default_output_dir(tmp_path: Path) -> None:
    """Default design-review output should be output/design_review."""
    repo_root = Path(__file__).resolve().parents[1]
    schdoc_path = tmp_path / "annotated.SchDoc"
    _write_annotation_schdoc(schdoc_path)
    env = os.environ.copy()
    src_path = str(repo_root / "src" / "py")
    env["PYTHONPATH"] = (
        src_path
        if not env.get("PYTHONPATH")
        else src_path + os.pathsep + env["PYTHONPATH"]
    )

    result = subprocess.run(
        [sys.executable, "-m", "altium_cruncher", "dr", str(schdoc_path)],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr + result.stdout
    assert (
        tmp_path / "output" / "design_review" / "design_review_manifest.json"
    ).exists()


def test_design_review_schematic_svg_enrichment_embeds_component_lookup(
    tmp_path: Path,
) -> None:
    """Embed schematic review metadata and component attrs into DR SVGs."""
    schdoc_path = tmp_path / "Sheet1.SchDoc"
    svg = '<svg xmlns="http://www.w3.org/2000/svg"><g id = "ABC123" ></g></svg>'
    design_payload: dict[str, object] = {
        "schema": "altium_monkey.design.a0",
        "components": [
            {
                "designator": "R1",
                "svg_id": "ABC123",
                "value": "10k",
                "footprint": "RES_0603",
                "library_ref": "RES",
                "hierarchy": {"sheet": "Sheet1.SchDoc"},
                "classification": {"type": "resistor"},
            }
        ],
        "indexes": {"component_to_nets": {"R1": ["NET_A"]}},
    }

    enriched = _enrich_schematic_svg(
        svg,
        design_payload=design_payload,
        schdoc_path=schdoc_path,
        source_base=tmp_path,
    )

    assert 'data-enrichment-schema="altium_monkey.schematic.svg.enrichment.a0"' in enriched
    assert 'data-review-theme="altium_cruncher.design_review.schematic_svg.a0"' in enriched
    assert 'id="schematic-enrichment-a0"' in enriched
    assert 'data-component="R1"' in enriched
    assert 'data-designator="R1"' in enriched
    assert 'data-symbol-library-ref="RES"' in enriched
    assert 'data-footprint="RES_0603"' in enriched
    assert '"svg_to_component": {' in enriched
    assert '"ABC123": "R1"' in enriched


def test_design_review_project_schematic_artifacts_are_compiled_outputs(
    tmp_path: Path,
) -> None:
    """Project schematic review outputs should be compiled pages by default."""

    from altium_monkey.altium_sch_geometry_oracle import (
        SchGeometryDocument,
        SchGeometryOp,
        SchGeometryRecord,
    )

    class FakeDesign:
        project = None

        def __init__(self) -> None:
            self.ir_calls = 0

        def to_physical_ir(self, page_id: str, **kwargs: object) -> SchGeometryDocument:
            self.ir_calls += 1
            assert page_id == "PDOC1"
            assert kwargs["profile"] == "onscreen"
            return SchGeometryDocument(
                records=[
                    SchGeometryRecord(
                        handle="1",
                        unique_id="CUID1",
                        kind="component",
                        object_id="eComponent",
                        operations=[
                            SchGeometryOp.string(
                                x=10,
                                y=-10,
                                text="R1.1",
                                font={"name": "Arial", "size": 12, "rotation": 0},
                                brush={"color_hex": "#000000"},
                            )
                        ],
                    )
                ],
                document_id=page_id,
                canvas={"width_px": 100, "height_px": 100},
                coordinate_space={"units_per_px": 64},
            )

    design_payload: dict[str, object] = {
        "physical_pages": [
            {
                "id": "PDOC1",
                "source_sheet": "Sheet1.SchDoc",
                "source_path": str(tmp_path / "Sheet1.SchDoc"),
                "components": [
                    {
                        "designator": "R1.1",
                        "svg_id": "CUID1",
                        "value": "10k",
                        "library_ref": "RES",
                    }
                ],
            }
        ],
        "indexes": {"component_to_nets": {"R1.1": ["VIN"]}},
    }

    fake_design = FakeDesign()
    svgs, irs = _write_project_schematic_artifacts(
        tmp_path / "review",
        fake_design,
        design_payload=design_payload,
        source_base=tmp_path,
    )

    assert fake_design.ir_calls == 1
    assert len(svgs) == 1
    assert len(irs) == 1
    assert svgs[0]["file"].startswith("sch/")
    assert irs[0]["file"].startswith("sch-ir/")
    assert "/physical/" not in svgs[0]["file"]
    assert "/physical/" not in irs[0]["file"]
    assert svgs[0]["compiled_page_id"] == "PDOC1"
    svg = (tmp_path / "review" / svgs[0]["file"]).read_text(encoding="utf-8")
    assert 'data-view-kind="compiled_schematic_page"' in svg
    assert 'data-compiled-page-id="PDOC1"' in svg
    assert 'data-component="R1.1"' in svg


def test_design_review_node_test_array_uses_compiled_physical_pages(
    tmp_path: Path,
) -> None:
    """Real-world DR bundles should expose resolved compiled schematic pages."""
    repo_root = Path(__file__).resolve().parents[1]
    project_path = _node_test_array_project_path()
    output_dir = tmp_path / "node_test_array_review"

    result = _run_cli(repo_root, "dr", str(project_path), "-o", str(output_dir))

    assert result.returncode == 0, result.stderr + result.stdout
    manifest = json.loads(
        (output_dir / "design_review_manifest.json").read_text(encoding="utf-8")
    )
    design_payload = json.loads(
        (output_dir / manifest["design_json"]).read_text(encoding="utf-8")
    )
    physical_pages = [
        page for page in design_payload["physical_pages"] if isinstance(page, dict)
    ]
    physical_page_ids = {str(page["id"]) for page in physical_pages}
    svg_page_ids = {
        str(entry["compiled_page_id"]) for entry in manifest["schematic_svgs"]
    }
    ir_page_ids = {
        str(entry["compiled_page_id"]) for entry in manifest["schematic_irs"]
    }

    assert len(physical_pages) > len({page["source_sheet"] for page in physical_pages})
    assert len(manifest["schematic_svgs"]) == len(physical_pages)
    assert len(manifest["schematic_irs"]) == len(physical_pages)
    assert svg_page_ids == physical_page_ids
    assert ir_page_ids == physical_page_ids

    page_component_designators = {
        str(component["designator"])
        for page in physical_pages
        for component in page.get("components", [])
        if isinstance(component, dict) and str(component.get("designator") or "")
    }
    top_level_component_designators = {
        str(component["designator"])
        for component in design_payload["components"]
        if isinstance(component, dict) and str(component.get("designator") or "")
    }
    assert page_component_designators
    assert page_component_designators <= top_level_component_designators

    resolved_component = next(
        component
        for component in design_payload["components"]
        if isinstance(component, dict)
        and component.get("logical_designator")
        and component.get("logical_designator") != component.get("designator")
        and component.get("physical_sheet_id") in physical_page_ids
    )
    resolved_designator = str(resolved_component["designator"])
    resolved_page_id = str(resolved_component["physical_sheet_id"])
    svg_entry = next(
        entry
        for entry in manifest["schematic_svgs"]
        if entry["compiled_page_id"] == resolved_page_id
    )
    ir_entry = next(
        entry
        for entry in manifest["schematic_irs"]
        if entry["compiled_page_id"] == resolved_page_id
    )

    svg_text = (output_dir / svg_entry["file"]).read_text(encoding="utf-8")
    assert f'data-compiled-page-id="{resolved_page_id}"' in svg_text
    assert f'data-component="{resolved_designator}"' in svg_text
    assert resolved_designator in svg_text

    dnp_component = next(
        component
        for component in design_payload["components"]
        if isinstance(component, dict)
        and component.get("dnp") is True
        and component.get("physical_sheet_id") in physical_page_ids
    )
    dnp_designator = str(dnp_component["designator"])
    dnp_page_id = str(dnp_component["physical_sheet_id"])
    dnp_svg_entry = next(
        entry
        for entry in manifest["schematic_svgs"]
        if entry["compiled_page_id"] == dnp_page_id
    )
    dnp_svg_text = (output_dir / dnp_svg_entry["file"]).read_text(encoding="utf-8")
    assert f'data-component="{dnp_designator}"' in dnp_svg_text
    assert 'data-dnp="true"' in dnp_svg_text
    assert 'data-fitted="false"' in dnp_svg_text

    ir_payload = json.loads((output_dir / ir_entry["file"]).read_text(encoding="utf-8"))
    assert resolved_designator in set(_iter_json_strings(ir_payload))


def test_design_review_pcb_svgs_are_copper_layer_only(tmp_path: Path) -> None:
    """Verify dr emits cheap copper review layers and no composed assembly views."""
    repo_root = Path(__file__).resolve().parents[1]
    project_path = tmp_path / "fixture.PrjPcb"
    _write_review_pcb_project(project_path)
    output_dir = tmp_path / "review"

    result = _run_cli(repo_root, "dr", str(project_path), "-o", str(output_dir))

    assert result.returncode == 0, result.stderr + result.stdout
    manifest = json.loads(
        (output_dir / "design_review_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["schematic_svgs"]
    assert "physical_schematic_svgs" not in manifest
    assert "physical_schematic_irs" not in manifest
    assert all(
        entry["file"].startswith("sch/") and "/physical/" not in entry["file"]
        for entry in manifest["schematic_svgs"]
    )
    assert len(manifest["pcb_svgs"]) == 1
    pcb_entry = manifest["pcb_svgs"][0]
    assert pcb_entry["views"] == []
    layers = {entry["name"]: entry for entry in pcb_entry["layer_outputs"]}
    assert set(layers) == {"TOP", "MID1", "BOTTOM"}
    assert "PCB SVG: pcb/layers/fixture__MID1.svg" in result.stdout
    for entry in layers.values():
        assert entry["file"].startswith("pcb/layers/")
        assert "ASSEMBLY_HLR_TOP" not in entry["layers"]
        assert "ASSEMBLY_HLR_BOTTOM" not in entry["layers"]
        assert set(entry["layers"]) <= {
            entry["name"],
            "BOARD_OUTLINE",
            "BOARD_CUTOUTS",
            "DRILLS",
            "SLOTS",
        }
        assert (output_dir / entry["file"]).exists()
