"""Breaking output-contract signoff for Design b0 downstream artifacts."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

from jsonschema import Draft202012Validator


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
CONTRACTS_ROOT = PACKAGE_ROOT / "docs" / "contracts"


def _validator(name: str) -> Draft202012Validator:
    schema = json.loads((CONTRACTS_ROOT / name).read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def _assert_valid(validator: Draft202012Validator, payload: object) -> None:
    assert list(validator.iter_errors(payload)) == []


def _assert_invalid(validator: Draft202012Validator, payload: object) -> None:
    assert list(validator.iter_errors(payload))


def test_design_review_manifest_b0_rejects_retired_compiled_page_id() -> None:
    validator = _validator("design_review_manifest.b0.schema.json")
    artifact = {
        "file": "sch/001.svg",
        "page_occurrence_ref": "page-1",
        "artifact_key": "sch.dwg_scene",
        "source": "Sheet1.SchDoc",
        "source_sheet": "Sheet1.SchDoc",
        "page_number": 1,
        "page_count": 1,
    }
    payload = {
        "schema": "altium_cruncher.design_review_manifest.b0",
        "input": "Project.PrjPcb",
        "design_json": "design/Project_design.json",
        "document_jsons": [],
        "notes_json": "notes/Project_notes.jsonc",
        "schematic_svgs": [artifact],
        "schematic_irs": [],
        "pcb_svgs": [],
        "readme": "README.md",
    }
    _assert_valid(validator, payload)

    retired = deepcopy(payload)
    retired_artifact = retired["schematic_svgs"][0]
    retired_artifact["compiled_page_id"] = retired_artifact.pop("page_occurrence_ref")
    _assert_invalid(validator, retired)


def test_compiled_svg_enrichment_b0_rejects_retired_embedded_design() -> None:
    validator = _validator("schematic_svg_enrichment.b0.schema.json")
    payload = {
        "schema": "altium_cruncher.schematic.svg.enrichment.b0",
        "source": {
            "altium_schdoc_file": "Sheet1.SchDoc",
            "page_occurrence_ref": "page-1",
            "artifact_key": "sch.dwg_scene",
        },
        "view": {
            "kind": "compiled_schematic_page",
            "profile": "design_review",
            "sheet_name": "Sheet1",
            "sheet_file": "Sheet1.SchDoc",
            "page_occurrence_ref": "page-1",
            "artifact_key": "sch.dwg_scene",
            "physical_page_metadata": {},
        },
    }
    _assert_valid(validator, payload)

    retired = deepcopy(payload)
    retired["schema"] = "altium_monkey.schematic.svg.enrichment.a0"
    retired["design"] = {"schema": "altium_monkey.design.a2"}
    retired["view_indexes"] = {}
    _assert_invalid(validator, retired)


def test_megamaid_manifest_b0_requires_versioned_graph_summary() -> None:
    validator = _validator("megamaid_manifest.b0.schema.json")
    payload = {
        "schema": "altium_cruncher.megamaid_manifest.b0",
        "kind": "megamaid",
        "input_project": "Project.PrjPcb",
        "output_root": "output/megamaid",
        "variants": [],
        "bom_pnp_config": None,
        "schdoc_count": 1,
        "pcbdoc_count": 1,
        "bom": {},
        "pnp": {},
        "netlist": {
            "design_json": "netlist/Project_netlist.json",
            "design_schema": "altium_monkey.design.b0",
            "compiled_schematic_graph_schema": (
                "altium_monkey.compiled_schematic_graph.a0"
            ),
            "component_count": 0,
            "net_count": 0,
            "page_occurrence_count": 1,
            "graphical_artifact_link_count": 0,
        },
        "document_jsons": [],
        "library_jsons": {},
        "notes": {},
        "schlib": [],
        "pcblib": [],
        "embedded_assets": {},
        "sch_images": {},
    }
    _assert_valid(validator, payload)

    schema_less = deepcopy(payload)
    schema_less.pop("schema")
    _assert_invalid(validator, schema_less)

    missing_graph_summary = deepcopy(payload)
    missing_graph_summary["netlist"].pop("page_occurrence_count")
    _assert_invalid(validator, missing_graph_summary)


def test_schematic_svg_manifest_b0_requires_resolvable_design_sidecar() -> None:
    validator = _validator("schematic_svg_manifest.b0.schema.json")
    payload = {
        "schema": "altium_cruncher.schematic_svg_manifest.b0",
        "input": "Sheet1.SchDoc",
        "design_json": "design/Sheet1_design.json",
        "design_schema": "altium_monkey.design.b0",
        "compiled_schematic_graph_schema": (
            "altium_monkey.compiled_schematic_graph.a0"
        ),
        "svgs": [
            {
                "file": "001_Sheet1.svg",
                "page_occurrence_ref": "page-1",
                "artifact_key": "sch.dwg_scene",
                "source": "Sheet1.SchDoc",
                "source_sheet": "Sheet1.SchDoc",
                "page_number": 1,
                "page_count": 1,
            }
        ],
    }
    _assert_valid(validator, payload)

    missing_design = deepcopy(payload)
    missing_design.pop("design_json")
    _assert_invalid(validator, missing_design)

    unscoped_svg = deepcopy(payload)
    unscoped_svg["svgs"][0].pop("page_occurrence_ref")
    _assert_invalid(validator, unscoped_svg)
