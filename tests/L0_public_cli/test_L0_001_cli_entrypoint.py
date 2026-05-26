"""Rack tests for the standalone public CLI package."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from altium_cruncher._version import __version__, cli_version_text

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


def _manifest_commands() -> list[str]:
    """Return public command names in manifest order."""
    manifest = json.loads(_MANIFEST_PATH.read_text(encoding="utf-8"))
    return [entry["name"] for entry in manifest["commands"]]


def test_cli_version_command() -> None:
    """Verify that the version subcommand reports the package version."""
    result = _run_cli("version")

    assert result.returncode == 0, result.stderr
    assert __version__ in result.stdout


def test_cli_no_args_prints_versioned_help() -> None:
    """Verify that a bare CLI invocation prints versioned command help."""
    result = _run_cli()

    assert result.returncode == 0, result.stderr
    assert cli_version_text() in result.stdout
    assert "usage: altium-cruncher" in result.stdout
    assert "Run `altium-cruncher <command> --help`" in result.stdout


def test_cli_help_lists_manifest_commands() -> None:
    """Verify that manifest commands are visible from root help output."""
    expected_commands = _manifest_commands()

    result = _run_cli("--help")

    assert result.returncode == 0, result.stderr
    assert cli_version_text() in result.stdout
    assert "usage: altium-cruncher" in result.stdout
    assert "Run `altium-cruncher <command> --help`" in result.stdout
    for command in expected_commands:
        assert command in result.stdout


def test_cli_help_lists_commands_alphabetically() -> None:
    """Verify that root help presents commands in alphabetical order."""
    expected_commands = _manifest_commands()
    result = _run_cli("--help")
    command_pattern = re.compile(r"^    ([a-z0-9][a-z0-9-]*)(?:\s|$)")

    help_commands = [
        match.group(1)
        for line in result.stdout.splitlines()
        if (match := command_pattern.match(line)) is not None
        and match.group(1) in expected_commands
    ]

    assert result.returncode == 0, result.stderr
    assert help_commands == sorted(expected_commands)


def test_cli_command_help_starts_for_manifest_commands() -> None:
    """Verify that each manifest command has command-level help."""
    expected_commands = _manifest_commands()

    for command in expected_commands:
        result = _run_cli(command, "--help")

        assert result.returncode == 0, f"{command}: {result.stderr}"
        assert cli_version_text() in result.stdout
        assert "usage:" in result.stdout
        assert command in result.stdout
