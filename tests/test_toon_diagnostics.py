"""Structured, deterministic end-of-run Toon diagnostics."""

import json
from pathlib import Path
from typing import cast

from jsonschema import Draft202012Validator

from altium_cruncher.toon_diagnostics import ToonDiagnosticCollector
from altium_cruncher.pcb_svg_render_job import PcbSvgRenderJob


ROOT = Path(__file__).resolve().parents[1]


def _add_missing(collector: ToonDiagnosticCollector, designator: str) -> None:
    collector.add(
        code="missing-renderable-model",
        category="missing_model",
        producer="altium-cruncher",
        message=f"{designator}: fitted component has no renderable 3D model",
        board="board.PcbDoc",
        component_designator=designator,
        occurrence_key=f"component:{designator}",
    )


def test_report_is_sorted_grouped_and_schema_valid():
    collector = ToonDiagnosticCollector()
    _add_missing(collector, "U2")
    _add_missing(collector, "U1")
    collector.add(
        code="geometer-warning",
        category="geometer_geometry",
        producer="geometer",
        message="Partial model tessellation",
        board="board.PcbDoc",
        component_designator="J1",
        body_index=0,
        model_identity="connector.step",
    )

    report = collector.report()

    diagnostics = cast(list[dict[str, object]], report["diagnostics"])
    assert [item["category"] for item in diagnostics] == [
        "geometer_geometry",
        "missing_model",
        "missing_model",
    ]
    assert [item["component_designator"] for item in diagnostics[1:]] == [
        "U1",
        "U2",
    ]
    summary = cast(dict[str, object], report["summary"])
    assert summary["unique_diagnostic_count"] == 3
    assert summary["occurrence_count"] == 3
    groups = cast(list[dict[str, object]], summary["groups"])
    assert groups[0]["affected_body_count"] == 1
    assert groups[0]["affected_model_count"] == 1
    assert groups[1]["sample_designators"] == ["U1", "U2"]
    schema = json.loads(
        (ROOT / "docs/contracts/toon_warning_report.a0.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(report)


def test_occurrence_keys_deduplicate_retries_but_count_distinct_occurrences():
    collector = ToonDiagnosticCollector()
    def add(occurrence_key: str) -> None:
        collector.add(
            code="invalid-bend-line",
            category="region_resolution",
            producer="altium-cruncher",
            message="Flex bend line 2 is incomplete; omitted",
            board="board.PcbDoc",
            occurrence_key=occurrence_key,
        )

    add("region:2:line:2")
    add("region:2:line:2")
    add("region:3:line:2")

    assert len(collector.diagnostics) == 1
    assert collector.diagnostics[0].occurrence_count == 2
    summary = cast(dict[str, object], collector.report()["summary"])
    assert summary["occurrence_count"] == 2


def test_explicit_empty_report_is_written(tmp_path):
    collector = ToonDiagnosticCollector()
    target = tmp_path / "nested" / "warnings.json"

    collector.write(target)

    payload = json.loads(target.read_text())
    assert payload == {
        "schema": "toon.warning_report.a0",
        "summary": {
            "unique_diagnostic_count": 0,
            "occurrence_count": 0,
            "groups": [],
        },
        "diagnostics": [],
    }
    assert collector.summary_lines() == ()


def test_missing_model_diagnostics_follow_the_active_variant_population():
    from types import SimpleNamespace

    pcb = SimpleNamespace(
        components=[
            SimpleNamespace(designator="U1"),
            SimpleNamespace(designator="U2"),
            SimpleNamespace(designator="U3"),
        ],
        component_bodies=[SimpleNamespace(component_index=1)],
    )
    job = PcbSvgRenderJob(workers=1)
    session = job.components(pcb)

    session._diagnose_missing_models(pcb, frozenset({"U3"}))
    session._diagnose_missing_models(pcb, frozenset({"U3"}))

    diagnostics = job.diagnostics.diagnostics
    assert len(diagnostics) == 1
    assert diagnostics[0].code == "missing-renderable-model"
    assert diagnostics[0].component_designator == "U1"
    assert diagnostics[0].variant is None and diagnostics[0].view is None
