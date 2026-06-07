"""Tests for Altium install/profile discovery helpers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

from altium_cruncher.altium_cruncher_cmd_launch import cmd_launch
from altium_cruncher.altium_environment import (
    clean_altium_profiles,
    discover_altium_installs,
    discover_altium_profiles,
    select_altium_install,
)


def _fake_x2(tmp_path: Path) -> Path:
    root = tmp_path / "Altium" / "AD26"
    root.mkdir(parents=True)
    x2_path = root / "X2.exe"
    x2_path.write_text("", encoding="utf-8")
    return x2_path


def _launch_args(
    x2_path: Path,
    *,
    file: str | None = None,
    dry_run: bool = True,
) -> argparse.Namespace:
    return argparse.Namespace(
        altium_path=x2_path,
        ad_version=None,
        file=file,
        dry_run=dry_run,
        json=True,
    )


def test_discover_altium_installs_sorts_latest_major_first(tmp_path: Path) -> None:
    """Scan fake AD roots and select newest or requested major series."""
    root = tmp_path / "Altium"
    ad25 = root / "AD25"
    ad26 = root / "AD26"
    ad25.mkdir(parents=True)
    ad26.mkdir(parents=True)
    (ad25 / "X2.exe").write_text("", encoding="utf-8")
    (ad26 / "X2.exe").write_text("", encoding="utf-8")

    installs = [
        install
        for install in discover_altium_installs(install_roots=[root])
        if root.resolve() in install.x2_path.parents
    ]

    assert [install.label for install in installs[:2]] == ["AD26", "AD25"]
    assert select_altium_install(installs).label == "AD26"
    assert select_altium_install(installs, version="ad25").label == "AD25"


def test_launch_without_file_opens_single_project_in_cwd(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """No-argument launch should auto-open one local PrjPcb."""
    x2_path = _fake_x2(tmp_path)
    project = tmp_path / "demo.PrjPcb"
    project.write_text("", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    exit_code = cmd_launch(_launch_args(x2_path))

    captured = capsys.readouterr()
    assert exit_code == 0, captured.err
    payload = json.loads(captured.out)
    assert payload["file"] == str(project.resolve())
    assert payload["command"] == [str(x2_path.resolve()), str(project.resolve())]


def test_launch_without_file_launches_ad_when_no_project_exists(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """No-argument launch should still start AD when no local PrjPcb exists."""
    x2_path = _fake_x2(tmp_path)
    monkeypatch.chdir(tmp_path)

    exit_code = cmd_launch(_launch_args(x2_path))

    captured = capsys.readouterr()
    assert exit_code == 0, captured.err
    payload = json.loads(captured.out)
    assert payload["file"] is None
    assert payload["command"] == [str(x2_path.resolve())]


def test_launch_without_file_lists_multiple_projects(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """No-argument launch should refuse ambiguous local PrjPcb choices."""
    x2_path = _fake_x2(tmp_path)
    (tmp_path / "Beta.PrjPcb").write_text("", encoding="utf-8")
    (tmp_path / "alpha.PrjPcb").write_text("", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    exit_code = cmd_launch(_launch_args(x2_path))

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert "Multiple .PrjPcb files found" in captured.err
    assert "  alpha.PrjPcb" in captured.err
    assert "  Beta.PrjPcb" in captured.err


def test_launch_reports_windows_requirement_when_not_dry_run_on_non_windows(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Actual AD launch fails predictably on non-Windows hosts."""
    from altium_cruncher import altium_environment

    x2_path = _fake_x2(tmp_path)
    monkeypatch.setattr(altium_environment.sys, "platform", "linux")

    exit_code = cmd_launch(_launch_args(x2_path, dry_run=False))

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert "supported on Windows only" in captured.err


def test_profiles_list_and_clean_extension_state(tmp_path: Path) -> None:
    """Discover profile extension state and dry-run/remove selected module state."""
    profile = tmp_path / "Altium Designer {11111111-2222-3333-4444-555555555555}"
    extensions = profile / "Extensions"
    module_dir = extensions / "ad-panel-monkey"
    module_dir.mkdir(parents=True)
    (module_dir / "ad-panel-monkey.dll").write_text("", encoding="utf-8")
    registry = extensions / "ExtensionsRegistry.xml"
    registry.write_text(
        (
            "<?xml version='1.0' encoding='utf-8'?>\n"
            "<Extensions><Item HRID='ad-panel-monkey'><Version>1.2.3</Version></Item></Extensions>"
        ),
        encoding="utf-8",
    )

    profiles = discover_altium_profiles(programdata_root=tmp_path)

    assert len(profiles) == 1
    assert profiles[0].registered is True
    assert profiles[0].registry_version == "1.2.3"
    assert profiles[0].module_dir_exists is True
    dry_run_actions = clean_altium_profiles(
        profiles,
        all_profiles=True,
        dry_run=True,
    )
    assert dry_run_actions[0]["removed_module_dir"] is True
    assert module_dir.exists()

    actions = clean_altium_profiles(profiles, all_profiles=True, dry_run=False)

    assert actions[0]["removed_module_dir"] is True
    assert actions[0]["removed_registry_item"] is True
    assert not module_dir.exists()
    refreshed = discover_altium_profiles(programdata_root=tmp_path)
    assert refreshed[0].registered is False
