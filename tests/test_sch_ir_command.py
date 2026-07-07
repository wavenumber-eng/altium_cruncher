from __future__ import annotations

import argparse
import json
from pathlib import Path

from altium_cruncher.altium_cruncher_cmd_sch_ir import cmd_sch_ir


def _args(file: str | None = None, output: Path | None = None) -> argparse.Namespace:
    return argparse.Namespace(file=file, output=output)


def _write_schdoc(path: Path) -> Path:
    from altium_monkey import AltiumSchDoc

    AltiumSchDoc().save(path)
    return path


def _write_project(path: Path, *document_names: str) -> Path:
    from altium_monkey.altium_prjpcb import AltiumPrjPcb

    project = AltiumPrjPcb()
    for document_name in document_names:
        project.add_document(document_name)
    project.save(path)
    return path


def _read_gotir(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_sch_ir_writes_single_schdoc_gotir_json(tmp_path: Path) -> None:
    schdoc_path = _write_schdoc(tmp_path / "fixture.SchDoc")
    output_dir = tmp_path / "gotir"

    result = cmd_sch_ir(_args(file=str(schdoc_path), output=output_dir))

    assert result == 0
    output_file = output_dir / "fixture.gotir.json"
    assert output_file.exists()
    payload = _read_gotir(output_file)
    assert payload["schema"] == "x2.sch_onscreen_geometry_oracle.v1"
    assert payload["source_kind"] == "SCH"
    assert str(payload["source_path"]).endswith("fixture.SchDoc")
    assert "records" in payload
    assert "render_hints" in payload


def test_sch_ir_expands_project_schdocs(tmp_path: Path) -> None:
    _write_schdoc(tmp_path / "first.SchDoc")
    _write_schdoc(tmp_path / "second.SchDoc")
    project_path = _write_project(
        tmp_path / "fixture.PrjPcb",
        "first.SchDoc",
        "second.SchDoc",
        "ignored.PcbDoc",
    )
    output_dir = tmp_path / "gotir"

    result = cmd_sch_ir(_args(file=str(project_path), output=output_dir))

    assert result == 0
    assert (output_dir / "first.gotir.json").exists()
    assert (output_dir / "second.gotir.json").exists()
    assert not (output_dir / "ignored.gotir.json").exists()


def test_sch_ir_auto_detects_project_in_cwd(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _write_schdoc(tmp_path / "auto.SchDoc")
    _write_project(tmp_path / "auto.PrjPcb", "auto.SchDoc")
    output_dir = tmp_path / "gotir"
    monkeypatch.chdir(tmp_path)

    result = cmd_sch_ir(_args(output=output_dir))

    assert result == 0
    assert (output_dir / "auto.gotir.json").exists()


def test_sch_ir_auto_detects_project_from_directory_argument(tmp_path: Path) -> None:
    _write_schdoc(tmp_path / "folder_auto.SchDoc")
    _write_project(tmp_path / "folder_auto.PrjPcb", "folder_auto.SchDoc")
    output_dir = tmp_path / "gotir"

    result = cmd_sch_ir(_args(file=str(tmp_path), output=output_dir))

    assert result == 0
    assert (output_dir / "folder_auto.gotir.json").exists()
