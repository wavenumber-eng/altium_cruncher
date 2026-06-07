from __future__ import annotations

import argparse
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from altium_cruncher import altium_cruncher_cmd_outjob as outjob_cmd


def _write_project(root: Path, name: str, outjobs: list[str]) -> Path:
    sections = ["[Design]", "OpenOutputs=1"]
    for index, outjob in enumerate(outjobs, start=1):
        outjob_path = root / outjob.replace("\\", "/")
        outjob_path.parent.mkdir(parents=True, exist_ok=True)
        outjob_path.write_text("[OutputJobFile]\n", encoding="utf-8")
        sections.extend(
            [
                f"[Document{index}]",
                f"DocumentPath={outjob}",
                f"DocumentUniqueId=JOB{index:04d}",
            ]
        )
    project = root / name
    project.write_text("\n".join(sections) + "\n", encoding="utf-8")
    return project


def _write_project_with_pcbdoc(root: Path, name: str, outjobs: list[str]) -> Path:
    pcbdoc = root / "board.PcbDoc"
    pcbdoc.write_text("", encoding="utf-8")
    sections = ["[Design]", "OpenOutputs=1"]
    sections.extend(
        [
            "[Document1]",
            "DocumentPath=board.PcbDoc",
            "DocumentUniqueId=PCB0001",
        ]
    )
    for index, outjob in enumerate(outjobs, start=2):
        outjob_path = root / outjob.replace("\\", "/")
        outjob_path.parent.mkdir(parents=True, exist_ok=True)
        outjob_path.write_text("[OutputJobFile]\n", encoding="utf-8")
        sections.extend(
            [
                f"[Document{index}]",
                f"DocumentPath={outjob}",
                f"DocumentUniqueId=JOB{index:04d}",
            ]
        )
    project = root / name
    project.write_text("\n".join(sections) + "\n", encoding="utf-8")
    return project


def _args(**overrides: object) -> argparse.Namespace:
    defaults = {
        "outjob_action": "run",
        "target": None,
        "outjobs": [],
        "project": None,
        "ad_version": None,
        "timeout": 300.0,
        "default_generated_output_path": None,
        "bind_pcbdoc": None,
        "auto_bind_pcbdoc": True,
        "stage_outjob_copy": False,
        "no_normalize_generated_paths": False,
        "script_directory": None,
        "keep_script_artifacts": False,
        "stop_on_error": False,
        "json": True,
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def _install_fake_runner(
    monkeypatch: pytest.MonkeyPatch,
    *,
    success: bool = True,
    mutate_outjob: bool = False,
) -> list[dict[str, object]]:
    calls: list[dict[str, object]] = []

    class FakeRunner:
        def __init__(self, preferred_version: int | None) -> None:
            self.preferred_version = preferred_version

        def run(self, project_path: Path, **kwargs: object) -> object:
            outjob_path = Path(str(kwargs["outjob_path"]))
            if mutate_outjob:
                outjob_path.write_text("mutated by runner", encoding="utf-8")
            calls.append(
                {
                    "preferred_version": self.preferred_version,
                    "project_path": Path(project_path),
                    **kwargs,
                }
            )
            return SimpleNamespace(
                project_path=Path(project_path),
                outjob_path=outjob_path,
                success=success,
                launch_code=0 if success else 1,
                timed_out=False,
                error_count=0 if success else 2,
                marker_text="DONE:0" if success else "DONE:2",
                normalized_changed=True,
                rebound_document_paths=1,
                marker_path=outjob_path.with_suffix(".done"),
                log_path=outjob_path.with_suffix(".log"),
            )

    monkeypatch.setattr(outjob_cmd, "AltiumOutJobRunner", FakeRunner)
    return calls


def test_outjob_run_auto_detects_project_and_runs_referenced_outjobs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(outjob_cmd.sys, "platform", "win32")
    project = _write_project(
        tmp_path,
        "demo.PrjPcb",
        ["fab.OutJob", "assembly.OutJob"],
    )
    calls = _install_fake_runner(monkeypatch)
    monkeypatch.chdir(tmp_path)

    exit_code = outjob_cmd.cmd_outjob(
        _args(
            ad_version="AD26",
            timeout=12.5,
            default_generated_output_path="Generated\\",
            auto_bind_pcbdoc=True,
            keep_script_artifacts=True,
        )
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert exit_code == 0, captured.err
    assert payload["schema"] == outjob_cmd.OUTJOB_RUN_SCHEMA
    assert payload["project"] == str(project.resolve())
    assert [Path(result["outjob"]).name for result in payload["results"]] == [
        "fab.OutJob",
        "assembly.OutJob",
    ]
    assert [Path(str(call["outjob_path"])).name for call in calls] == [
        "fab.OutJob",
        "assembly.OutJob",
    ]
    assert calls[0]["preferred_version"] == 26
    assert calls[0]["timeout_seconds"] == 12.5
    assert calls[0]["default_generated_output_path"] == "Generated\\"
    assert calls[0]["auto_bind_pcbdoc"] is False
    assert calls[0]["keep_script_artifacts"] is True
    assert calls[0]["stage_outjob_copy"] is False


def test_outjob_run_refuses_ambiguous_auto_detect(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(outjob_cmd.sys, "platform", "win32")
    _write_project(tmp_path, "alpha.PrjPcb", ["alpha.OutJob"])
    _write_project(tmp_path, "beta.PrjPcb", ["beta.OutJob"])
    _install_fake_runner(monkeypatch)
    monkeypatch.chdir(tmp_path)

    exit_code = outjob_cmd.cmd_outjob(_args())

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert "Multiple .PrjPcb files found" in captured.err
    assert "alpha.PrjPcb" in captured.err
    assert "beta.PrjPcb" in captured.err


def test_outjob_run_accepts_explicit_project_and_outjob_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(outjob_cmd.sys, "platform", "win32")
    project = _write_project(tmp_path, "demo.PrjPcb", ["referenced.OutJob"])
    extra = tmp_path / "extra" / "manual.OutJob"
    extra.parent.mkdir(parents=True)
    extra.write_text("[OutputJobFile]\n", encoding="utf-8")
    calls = _install_fake_runner(monkeypatch)

    exit_code = outjob_cmd.cmd_outjob(
        _args(project=project, target=Path("extra") / "manual.OutJob")
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert exit_code == 0, captured.err
    assert Path(payload["results"][0]["outjob"]) == extra.resolve()
    assert Path(str(calls[0]["outjob_path"])) == extra.resolve()


def test_outjob_run_returns_failure_for_failed_runner_result(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(outjob_cmd.sys, "platform", "win32")
    _write_project(tmp_path, "demo.PrjPcb", ["fab.OutJob"])
    _install_fake_runner(monkeypatch, success=False)
    monkeypatch.chdir(tmp_path)

    exit_code = outjob_cmd.cmd_outjob(_args())

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert exit_code == 1
    assert payload["success"] is False
    assert payload["results"][0]["error_count"] == 2


def test_outjob_run_auto_binds_single_project_pcbdoc_and_restores_outjob(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(outjob_cmd.sys, "platform", "win32")
    project = _write_project_with_pcbdoc(tmp_path, "demo.PrjPcb", ["fab.OutJob"])
    outjob = tmp_path / "fab.OutJob"
    original = (
        "[OutputJobFile]\n"
        "[OutputGroup1]\n"
        "OutputMedium1_Type=GeneratedFiles\n"
        "[PublishSettings]\n"
        "OutputBasePath1=outputs\\\n"
        "[GeneratedFilesSettings]\n"
        "RelativeOutputPath1=outputs\\\n"
    )
    outjob.write_text(original, encoding="utf-8")
    calls = _install_fake_runner(monkeypatch, mutate_outjob=True)
    monkeypatch.chdir(tmp_path)

    exit_code = outjob_cmd.cmd_outjob(_args(project=project, target=outjob))

    captured = capsys.readouterr()
    assert exit_code == 0, captured.err
    assert outjob.read_text(encoding="utf-8") == original
    assert Path(str(calls[0]["bind_pcbdoc_path"])) == (tmp_path / "board.PcbDoc").resolve()
    assert calls[0]["auto_bind_pcbdoc"] is False
    assert calls[0]["stage_outjob_copy"] is False


def test_outjob_run_reports_windows_requirement_on_non_windows(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(outjob_cmd.sys, "platform", "linux")
    _write_project(tmp_path, "demo.PrjPcb", ["fab.OutJob"])
    _install_fake_runner(monkeypatch)
    monkeypatch.chdir(tmp_path)

    exit_code = outjob_cmd.cmd_outjob(_args())

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert "requires Windows with Altium Designer installed" in captured.err
