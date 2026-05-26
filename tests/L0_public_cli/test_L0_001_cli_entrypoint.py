"""Rack tests for the standalone public CLI package."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from altium_cruncher._version import __version__

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_MANIFEST_PATH = _PROJECT_ROOT / "contracts" / "command_manifest.v0.json"


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    """Run the current checkout's CLI through the active Python environment."""
    return subprocess.run(
        [sys.executable, "-m", "altium_cruncher", *args],
        cwd=_PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli_version_command() -> None:
    """Verify that the version subcommand reports the package version."""
    result = _run_cli("version")

    assert result.returncode == 0, result.stderr
    assert __version__ in result.stdout


def test_cli_help_lists_manifest_commands() -> None:
    """Verify that manifest commands are visible from root help output."""
    manifest = json.loads(_MANIFEST_PATH.read_text(encoding="utf-8"))
    expected_commands = [entry["name"] for entry in manifest["commands"]]

    result = _run_cli("--help")

    assert result.returncode == 0, result.stderr
    assert "usage: altium-cruncher" in result.stdout
    for command in expected_commands:
        assert command in result.stdout


def test_cli_command_help_starts_for_manifest_commands() -> None:
    """Verify that each manifest command has command-level help."""
    manifest = json.loads(_MANIFEST_PATH.read_text(encoding="utf-8"))

    for entry in manifest["commands"]:
        command = entry["name"]
        result = _run_cli(command, "--help")

        assert result.returncode == 0, f"{command}: {result.stderr}"
        assert "usage:" in result.stdout
        assert command in result.stdout
