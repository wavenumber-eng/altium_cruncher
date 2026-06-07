from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from altium_cruncher.altium_cruncher_json_dump import (
    JSON_DUMP_MANIFEST_SCHEMA,
    JSON_DUMP_SCHEMA,
    PCB_DOC_STRUCTURAL_FORMAT,
    PCB_LIB_STRUCTURAL_FORMAT,
    SCH_DOC_INTEROP_FORMAT,
    SCH_LIB_INTEROP_FORMAT,
    build_json_dump_payload,
    write_json_dumps,
)

PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def _write_text_pcbdoc(path: Path) -> Path:
    from altium_monkey import AltiumPcbDoc, PcbLayer

    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(0, 0, 1000, 700)
    pcbdoc.add_text(
        text="DBG_LABEL",
        position_mils=(100.0, 200.0),
        height_mils=50.0,
        layer=PcbLayer.TOP_OVERLAY,
        rotation_degrees=90.0,
        font_kind="truetype",
        font_name="Arial",
        bold=True,
    )
    pcbdoc.save(path)
    return path


def test_json_dump_pcbdoc_writes_minimal_a0_envelope(tmp_path: Path) -> None:
    pcbdoc_path = _write_text_pcbdoc(tmp_path / "labels.PcbDoc")

    payload = build_json_dump_payload(pcbdoc_path)

    assert payload["schema"] == JSON_DUMP_SCHEMA
    assert payload["kind"] == "PcbDoc"
    assert set(payload) == {"schema", "kind", "document"}
    document = payload["document"]
    assert isinstance(document, dict)
    assert document["format"] == PCB_DOC_STRUCTURAL_FORMAT
    assert document["counts"]["texts"] == 1
    text_entry = document["texts"][0]
    assert text_entry["fields"]["text_content"] == "DBG_LABEL"
    assert text_entry["properties"]["x_mils"] == 100.0
    assert text_entry["properties"]["y_mils"] == 200.0
    assert text_entry["properties"]["height_mils"] == 50.0


def test_json_dump_schlib_writes_minimal_a0_envelope(tmp_path: Path) -> None:
    from altium_monkey import AltiumSchLib
    from altium_monkey.altium_record_sch__pin import AltiumSchPin

    schlib_path = tmp_path / "fixture.SchLib"
    schlib = AltiumSchLib()
    symbol = schlib.add_symbol("DBG_SYMBOL")
    symbol.add_pin(AltiumSchPin("1", "SIG", -100, 0, orientation=2, length=100))
    schlib.save(schlib_path)

    payload = build_json_dump_payload(schlib_path)

    assert payload["schema"] == JSON_DUMP_SCHEMA
    assert payload["kind"] == "SchLib"
    assert set(payload) == {"schema", "kind", "document"}
    document = payload["document"]
    assert isinstance(document, dict)
    assert document["format"] == SCH_LIB_INTEROP_FORMAT
    assert "Symbols" in document


def test_json_dump_schdoc_uses_altium_monkey_interop_format(
    tmp_path: Path,
) -> None:
    from altium_monkey import AltiumSchDoc

    schdoc_path = tmp_path / "fixture.SchDoc"
    AltiumSchDoc().save(schdoc_path)

    payload = build_json_dump_payload(schdoc_path)

    assert payload["schema"] == JSON_DUMP_SCHEMA
    assert payload["kind"] == "SchDoc"
    document = payload["document"]
    assert isinstance(document, dict)
    assert document["format"] == SCH_DOC_INTEROP_FORMAT
    assert "Objects" in document


def test_json_dump_pcblib_uses_altium_monkey_document_format(tmp_path: Path) -> None:
    from altium_monkey import AltiumPcbLib

    pcblib_path = tmp_path / "fixture.PcbLib"
    pcblib = AltiumPcbLib()
    pcblib.add_footprint("DBG_FOOTPRINT")
    pcblib.save(pcblib_path)

    payload = build_json_dump_payload(pcblib_path)

    assert payload["schema"] == JSON_DUMP_SCHEMA
    assert payload["kind"] == "PcbLib"
    document = payload["document"]
    assert isinstance(document, dict)
    assert document["format"] == PCB_LIB_STRUCTURAL_FORMAT
    assert document["footprint_count"] == 1


def test_json_dump_expands_project_and_writes_manifest(tmp_path: Path) -> None:
    from altium_monkey.altium_prjpcb import AltiumPrjPcb

    pcbdoc_path = _write_text_pcbdoc(tmp_path / "fixture.PcbDoc")
    project_path = tmp_path / "fixture.PrjPcb"
    project = AltiumPrjPcb()
    project.add_document(pcbdoc_path.name)
    project.add_document("ignored.OutJob")
    project.save(project_path)

    result = write_json_dumps([project_path], output=tmp_path / "dump")

    assert len(result.outputs) == 1
    assert result.outputs[0].source_path == pcbdoc_path.resolve()
    assert result.outputs[0].output_path == (
        tmp_path / "dump" / "json" / "pcbdoc" / "fixture.PcbDoc.json"
    )
    output_payload = json.loads(
        result.outputs[0].output_path.read_text(encoding="utf-8")
    )
    assert output_payload["kind"] == "PcbDoc"
    assert set(output_payload) == {"schema", "kind", "document"}
    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    assert manifest["schema"] == JSON_DUMP_MANIFEST_SCHEMA
    assert set(manifest) == {"schema", "outputs"}
    assert manifest["outputs"][0]["kind"] == "PcbDoc"


def test_json_dump_cli_stdout_writes_single_document_json(tmp_path: Path) -> None:
    pcbdoc_path = _write_text_pcbdoc(tmp_path / "stdout.PcbDoc")

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "json-dump",
            str(pcbdoc_path),
            "--stdout",
        ],
        cwd=PACKAGE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["schema"] == JSON_DUMP_SCHEMA
    assert payload["kind"] == "PcbDoc"
