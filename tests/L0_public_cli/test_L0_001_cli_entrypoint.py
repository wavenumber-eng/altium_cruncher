"""Rack tests for the standalone public CLI package."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from colorama import Fore, Style

from altium_cruncher._cli import _color_command_names_in_help, _format_parser_error_line
from altium_cruncher._version import __version__, cli_version_text

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_MANIFEST_PATH = _PROJECT_ROOT / "docs" / "contracts" / "command_manifest.v0.json"


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


def test_cli_help_lists_global_logging_controls() -> None:
    """Verify that root help documents global logging controls."""
    result = _run_cli("--help")

    assert result.returncode == 0, result.stderr
    assert "--quiet" in result.stdout
    assert "--verbose" in result.stdout
    assert "--log-level" in result.stdout


def test_design_help_describes_design_json_contents() -> None:
    """Verify design help explains the broader design JSON payload."""
    result = _run_cli("design", "--help")

    assert result.returncode == 0, result.stderr
    assert "netlist data" in result.stdout
    assert "component records" in result.stdout
    assert "SVG IDs" in result.stdout


def test_easyeda_help_marks_commands_experimental() -> None:
    """Verify EasyEDA command help is explicit about experimental status."""
    root_result = _run_cli("--help")

    assert root_result.returncode == 0, root_result.stderr
    assert "easyeda-import" in root_result.stdout
    assert "EXPERIMENTAL" in root_result.stdout

    command_result = _run_cli("easyeda-import", "--help")
    assert command_result.returncode == 0, command_result.stderr
    assert "EXPERIMENTAL" in command_result.stdout


def test_easyeda_review_commands_are_not_public_cli_commands() -> None:
    """Verify EasyEDA review helpers are not exposed as public CLI commands."""
    for command in ("easyeda-review", "easyeda-footprint-review"):
        result = _run_cli(command, "--help")

        assert result.returncode != 0
        assert "invalid choice" in result.stderr


def test_netlist_command_name_is_retired() -> None:
    """Verify the old netlist command name is not a public command."""
    result = _run_cli("netlist", "--help")

    assert result.returncode != 0
    assert "invalid choice" in result.stderr
    assert Style.BRIGHT not in result.stderr


def test_cli_quiet_suppresses_info_logs(tmp_path: Path) -> None:
    """Verify that --quiet hides normal command info logs."""
    config_path = tmp_path / "bom.config"

    result = _run_cli("--quiet", "bom", "--write-config", str(config_path))

    assert result.returncode == 0, result.stderr
    assert config_path.exists()
    assert "Wrote BOM/PnP config template" not in result.stdout


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


def test_cli_help_colorizes_root_command_names_with_altium_amber() -> None:
    """Verify terminal help highlights root command names in amber/yellow."""
    help_text = "\n".join(
        [
            "positional arguments:",
            "  <command>             Available commands",
            "    bom                 generate BOM",
            "    pcb-layer-step      generate STEP geometry",
        ]
    )

    colored = _color_command_names_in_help(
        help_text,
        ("bom", "pcb-layer-step"),
    )
    color = f"{Style.BRIGHT}{Fore.YELLOW}"

    assert f"    {color}bom{Style.RESET_ALL}                 generate BOM" in colored
    assert f"    {color}pcb-layer-step{Style.RESET_ALL}      generate STEP geometry" in colored


def test_cli_parser_error_formatter_supports_red_terminal_output() -> None:
    """Verify parser errors can be highlighted in red for terminal output."""
    formatted = _format_parser_error_line(
        "altium-cruncher",
        "invalid choice: 'netlist'",
        color=True,
    )

    assert formatted == (
        f"{Style.BRIGHT}{Fore.RED}"
        "altium-cruncher: error: invalid choice: 'netlist'"
        f"{Style.RESET_ALL}\n"
    )


def test_cli_command_help_starts_for_manifest_commands() -> None:
    """Verify that each manifest command has command-level help."""
    expected_commands = _manifest_commands()

    for command in expected_commands:
        result = _run_cli(command, "--help")

        assert result.returncode == 0, f"{command}: {result.stderr}"
        assert cli_version_text() in result.stdout
        assert "usage:" in result.stdout
        assert command in result.stdout


def test_svg_help_describes_combined_svg_command() -> None:
    """Verify that svg help describes the combined schematic and PCB behavior."""
    result = _run_cli("svg", "--help")

    assert result.returncode == 0, result.stderr
    assert "Run schematic SVG generation, PCB SVG generation, or both" in result.stdout
    assert "legacy shortcut" not in result.stdout
