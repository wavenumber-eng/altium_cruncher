from __future__ import annotations

import json
import subprocess
import sys
import tomllib
from datetime import date
from pathlib import Path

import altium_cruncher
from altium_cruncher._version import cli_version_text


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "2026.5.25"
EXPECTED_RELEASE_DATE = date(2026, 5, 25)


def test_version_contract_matches_date_based_release() -> None:
    pyproject = tomllib.loads((PACKAGE_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    version = altium_cruncher.version()

    assert pyproject["project"]["version"] == EXPECTED_VERSION
    assert altium_cruncher.__version__ == EXPECTED_VERSION
    assert version.string == EXPECTED_VERSION
    assert (version.major, version.minor, version.patch, version.build) == (
        2026,
        5,
        25,
        None,
    )
    assert version.release_date == EXPECTED_RELEASE_DATE
    assert version.release_date <= date.today()


def test_cli_emits_package_version() -> None:
    for args in (("--version",), ("version",)):
        completed = subprocess.run(
            [sys.executable, "-m", "altium_cruncher", *args],
            check=False,
            capture_output=True,
            text=True,
        )

        assert completed.returncode == 0, completed.stderr
        assert completed.stdout.strip() == cli_version_text()


def test_python_signoff_does_not_regress() -> None:
    baseline = PACKAGE_ROOT / "scripts" / "py_signoff_baseline.json"
    script = PACKAGE_ROOT / "scripts" / "py_signoff.py"

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
