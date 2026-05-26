from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = PACKAGE_ROOT / "contracts" / "command_manifest.v0.json"


def _manifest_commands() -> list[str]:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert payload["schema"] == "altium_cruncher.command_manifest.v0"
    commands = payload["commands"]
    assert isinstance(commands, list)
    names = [str(command["name"]) for command in commands]
    assert len(names) == len(set(names))
    return names


def _manifest_entries() -> list[dict[str, object]]:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return list(payload["commands"])


def test_command_manifest_lists_registered_cli_commands() -> None:
    """Every manifest command should appear in top-level CLI help."""
    completed = subprocess.run(
        [sys.executable, "-m", "altium_cruncher", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    help_text = completed.stdout
    for command in _manifest_commands():
        assert command in help_text


def test_command_manifest_has_docs_anchor() -> None:
    """README command list should mention every manifest command."""
    readme = (PACKAGE_ROOT / "README.md").read_text(encoding="utf-8")
    for command in _manifest_commands():
        assert f"`{command}`" in readme


def test_each_manifest_command_has_help() -> None:
    """Every manifest command should start and show command-level help."""
    for command in _manifest_commands():
        completed = subprocess.run(
            [sys.executable, "-m", "altium_cruncher", command, "--help"],
            check=False,
            capture_output=True,
            text=True,
        )

        assert completed.returncode == 0, f"{command}: {completed.stderr}"
        assert command in completed.stdout
        assert "usage:" in completed.stdout


def test_planned_easyeda_commands_have_missing_dependency_placeholder() -> None:
    """EasyEDA commands should fail clearly in a base install."""
    if importlib.util.find_spec("easyeda_monkey") is not None:
        pytest.skip("easyeda-monkey is installed; this is a base-install check")

    planned_easyeda = [
        str(entry["name"])
        for entry in _manifest_entries()
        if entry.get("requires_extra") == "easyeda"
    ]

    assert planned_easyeda
    for command in planned_easyeda:
        completed = subprocess.run(
            [sys.executable, "-m", "altium_cruncher", command],
            check=False,
            capture_output=True,
            text=True,
        )

        assert completed.returncode == 2
        assert "easyeda-monkey" in completed.stderr
