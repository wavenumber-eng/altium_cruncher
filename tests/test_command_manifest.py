from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


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
