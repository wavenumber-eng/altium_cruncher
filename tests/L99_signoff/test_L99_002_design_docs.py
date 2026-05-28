"""Design documentation signoff tests for public CLI commands."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys


def _project_root() -> Path:
    """Find the repository root from this test file."""
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Could not locate repository root")


PACKAGE_ROOT = _project_root()
DESIGN_ROOT = PACKAGE_ROOT / "docs" / "design"
COMMAND_MANIFEST = PACKAGE_ROOT / "docs" / "contracts" / "command_manifest.v0.json"


def _manifest_commands() -> list[str]:
    """Return registered public command names from the command manifest."""
    payload = json.loads(COMMAND_MANIFEST.read_text(encoding="utf-8"))
    assert payload["schema"] == "altium_cruncher.command_manifest.v0"
    commands = payload["commands"]
    assert isinstance(commands, list)
    return [str(command["name"]) for command in commands]


def _root_help_commands() -> list[str]:
    """Return command names registered by the actual CLI parser."""
    completed = subprocess.run(
        [sys.executable, "-m", "altium_cruncher", "--help"],
        cwd=PACKAGE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    command_pattern = re.compile(r"^    ([a-z0-9][a-z0-9-]*)(?:\s|$)")
    return [
        match.group(1)
        for line in completed.stdout.splitlines()
        if (match := command_pattern.match(line)) is not None
    ]


def _cli_index_commands() -> list[str]:
    """Return command rows declared by the CLI design index."""
    cli_index = (DESIGN_ROOT / "cli" / "index.html").read_text(encoding="utf-8")
    return re.findall(r'<tr[^>]*data-command="([^"]+)"', cli_index)


def _cli_design_doc_commands() -> dict[str, Path]:
    """Return command declarations from per-command CLI design docs."""
    docs: dict[str, Path] = {}
    for design_doc in sorted((DESIGN_ROOT / "cli").glob("*.html")):
        if design_doc.name == "index.html":
            continue
        text = design_doc.read_text(encoding="utf-8")
        match = re.search(r'<body[^>]*data-command="([^"]+)"', text)
        if match is not None:
            docs[match.group(1)] = design_doc
    return docs


def _set_diff_message(
    label: str,
    actual: set[str],
    expected: set[str],
) -> list[str]:
    """Format inventory drift messages for command sets."""
    failures: list[str] = []
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        failures.append(f"{label}: missing {', '.join(missing)}")
    if extra:
        failures.append(f"{label}: extra {', '.join(extra)}")
    return failures


def test_design_entry_points_exist() -> None:
    """Verify that the master design docs entry points exist."""
    assert (DESIGN_ROOT / "index.html").exists()
    assert (DESIGN_ROOT / "styles.css").exists()
    assert (DESIGN_ROOT / "cli" / "index.html").exists()
    assert (DESIGN_ROOT / "api" / "index.html").exists()


def test_cli_command_inventory_matches_parser_manifest_and_design_docs() -> None:
    """Verify parser, manifest, design index, and design docs declare one command set."""
    manifest_commands = _manifest_commands()
    manifest_set = set(manifest_commands)
    help_commands = _root_help_commands()
    index_commands = _cli_index_commands()
    doc_commands = _cli_design_doc_commands()
    failures: list[str] = []

    for label, commands in (
        ("CLI parser help", help_commands),
        ("CLI design index", index_commands),
        ("CLI design docs", list(doc_commands)),
    ):
        failures.extend(_set_diff_message(label, set(commands), manifest_set))
        if len(commands) != len(set(commands)):
            failures.append(f"{label}: duplicate command declaration")

    for command in manifest_commands:
        expected_name = f"{command}.html"
        design_doc = doc_commands.get(command)
        if design_doc is not None and design_doc.name != expected_name:
            failures.append(
                f"{command}: design doc should be cli/{expected_name}, "
                f"got cli/{design_doc.name}"
            )

    assert failures == [], "CLI command inventory drift:\n" + "\n".join(failures)


def test_cli_commands_have_matching_design_docs() -> None:
    """Verify that every registered CLI command has a matching design document."""
    cli_index = (DESIGN_ROOT / "cli" / "index.html").read_text(encoding="utf-8")
    failures: list[str] = []

    for command in _manifest_commands():
        design_rel = Path("cli") / f"{command}.html"
        design_doc = DESIGN_ROOT / design_rel
        if f'data-command="{command}"' not in cli_index:
            failures.append(f"{command}: missing cli index row")
        if design_rel.as_posix() not in cli_index:
            failures.append(f"{command}: cli index does not reference {design_rel.as_posix()}")
        if not design_doc.exists():
            failures.append(f"{command}: missing design doc {design_rel.as_posix()}")
            continue

        text = design_doc.read_text(encoding="utf-8")
        for required in (
            f'data-command="{command}"',
            '<section id="usage">',
            '<section id="arguments">',
            '<section id="output">',
            '<section id="tests">',
            'data-config-contract="',
        ):
            if required not in text:
                failures.append(f"{command}: {design_rel.as_posix()} missing {required}")

    assert failures == [], "CLI design doc signoff gaps:\n" + "\n".join(failures)


def test_cli_commands_have_dedicated_modules() -> None:
    """Verify that public CLI behavior lives outside the orchestrator."""
    commands_root = PACKAGE_ROOT / "src" / "py" / "altium_cruncher"
    failures: list[str] = []

    for command in _manifest_commands():
        if command == "version":
            continue
        module_path = commands_root / f"altium_cruncher_cmd_{command.replace('-', '_')}.py"
        if not module_path.exists():
            failures.append(f"{command}: missing command module {module_path.name}")

    assert failures == [], "CLI command module signoff gaps:\n" + "\n".join(failures)
