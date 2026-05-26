"""Release signoff tests for the public package."""

from __future__ import annotations

import json
import subprocess
import sys
import tomllib
from datetime import date
from pathlib import Path

import altium_cruncher
from altium_cruncher._version import cli_version_text


def _project_root() -> Path:
    """Find the repository root from this test file."""
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Could not locate repository root")


PACKAGE_ROOT = _project_root()
EXPECTED_VERSION = "2026.5.26"
EXPECTED_RELEASE_DATE = date(2026, 5, 26)


def test_version_contract_matches_date_based_release() -> None:
    """Verify that package version metadata follows the date release contract."""
    pyproject = tomllib.loads((PACKAGE_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    version = altium_cruncher.version()

    assert pyproject["project"]["version"] == EXPECTED_VERSION
    assert altium_cruncher.__version__ == EXPECTED_VERSION
    assert version.string == EXPECTED_VERSION
    assert (version.major, version.minor, version.patch, version.build) == (
        2026,
        5,
        26,
        None,
    )
    assert version.release_date == EXPECTED_RELEASE_DATE
    assert version.release_date <= date.today()
    assert pyproject["project"]["scripts"] == {
        "altium-cruncher": "altium_cruncher._cli:main"
    }


def test_cli_emits_package_version() -> None:
    """Verify that CLI version commands emit the canonical package version text."""
    for args in (("--version",), ("version",)):
        completed = subprocess.run(
            [sys.executable, "-m", "altium_cruncher", *args],
            check=False,
            capture_output=True,
            text=True,
        )

        assert completed.returncode == 0, completed.stderr
        assert completed.stdout.strip() == cli_version_text()
        assert completed.stdout.startswith("altium-cruncher ")


def test_changelog_mentions_package_version() -> None:
    """Verify that release notes mention the current package version."""
    changelog = (PACKAGE_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    assert f"## {EXPECTED_VERSION}" in changelog


def test_developer_working_docs_are_excluded_from_release_artifacts() -> None:
    """Verify that developer-only plan and research docs are not packaged."""
    pyproject = tomllib.loads((PACKAGE_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    sdist = pyproject["tool"]["hatch"]["build"]["targets"]["sdist"]

    assert "docs/**" in sdist["include"]
    assert "docs/plans/**" in sdist["exclude"]
    assert "docs/research/**" in sdist["exclude"]


def test_python_signoff_does_not_regress() -> None:
    """Verify that the Python source signoff has no findings."""
    baseline = PACKAGE_ROOT / "tests" / "support_scripts" / "py_signoff_baseline.json"
    script = PACKAGE_ROOT / "tests" / "support_scripts" / "py_signoff.py"

    completed = subprocess.run(
        [
            sys.executable,
            str(script),
            "--root",
            str(PACKAGE_ROOT),
            "--baseline",
            str(baseline),
            "--format",
            "json",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr + completed.stdout
    payload = json.loads(completed.stdout)
    assert payload["finding_count"] == 0
