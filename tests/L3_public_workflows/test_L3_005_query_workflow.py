"""Fixture-backed CLI workflow tests for the query command."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def _project_root() -> Path:
    """Find the repository root from this test file."""
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Could not locate repository root")


PACKAGE_ROOT = _project_root()
HYDROSCOPE_DIR = PACKAGE_ROOT / "tests" / "assets" / "projects" / "hydroscope" / "input"
HYDROSCOPE_PROJECT = HYDROSCOPE_DIR / "Hydroscope.PrjPcb"
HYDROSCOPE_SCHDOC = HYDROSCOPE_DIR / "CPU.SchDoc"


def _run_query(*args: str) -> subprocess.CompletedProcess[str]:
    """Run one query CLI invocation through the current Python environment."""
    return subprocess.run(
        [sys.executable, "-m", "altium_cruncher", "query", *args],
        cwd=PACKAGE_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def _run_query_json(*args: str) -> dict[str, object]:
    """Run one query invocation and parse its stdout as one JSON payload."""
    completed = _run_query(*args)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    return json.loads(completed.stdout)


def test_query_summary_reports_hydroscope_overview() -> None:
    """Summary payload reports sheets, counts, variants, and power nets."""
    payload = _run_query_json("summary", str(HYDROSCOPE_PROJECT))

    assert payload["schema"] == "altium_cruncher.query.summary.a0"
    assert payload["project_file"] == "Hydroscope.PrjPcb"
    assert payload["variants"] == ["A", "B"]
    assert payload["component_count"] >= 100
    assert payload["net_count"] >= 100
    sheet_files = {sheet["filename"] for sheet in payload["sheets"]}
    assert "CPU.SchDoc" in sheet_files
    top_level = [s for s in payload["sheets"] if s["is_top_level"]]
    assert [s["filename"] for s in top_level] == ["TOP_LEVEL.SchDoc"]
    assert "GND" in payload["power_and_ground_nets"]


def test_query_components_filters_by_type_and_sheet() -> None:
    """Component rows respect type/sheet filters and brief default fields."""
    payload = _run_query_json(
        "components",
        str(HYDROSCOPE_PROJECT),
        "--type",
        "ic",
        "--sheet",
        "CPU.SchDoc",
    )

    assert payload["schema"] == "altium_cruncher.query.components.a0"
    components = payload["components"]
    assert payload["count"] == len(components) > 0
    for component in components:
        assert component["type"] == "ic"
        assert Path(component["sheet"]).name == "CPU.SchDoc"
        assert set(component) == {
            "designator",
            "value",
            "footprint",
            "type",
            "sheet",
            "pin_count",
        }


def test_query_nets_listing_and_named_terminal_detail() -> None:
    """Net listing filters by substring and named nets return terminals."""
    listing = _run_query_json(
        "nets",
        str(HYDROSCOPE_PROJECT),
        "--contains",
        "GND",
    )
    assert listing["schema"] == "altium_cruncher.query.nets.a0"
    assert any(net["name"] == "GND" for net in listing["nets"])

    detail = _run_query_json("nets", str(HYDROSCOPE_PROJECT), "--name", "gnd")
    assert detail["schema"] == "altium_cruncher.query.net_detail.a0"
    assert detail["name"] == "GND"
    assert detail["terminal_count"] == len(detail["terminals"]) > 50
    assert {"designator", "pin"} <= set(detail["terminals"][0])


def test_query_connections_reports_designator_pin_rows() -> None:
    """Connections payload reports per-pin nets and connected terminals."""
    payload = _run_query_json(
        "connections",
        "U4",
        "--project",
        str(HYDROSCOPE_PROJECT),
    )

    assert payload["schema"] == "altium_cruncher.query.connections.a0"
    assert payload["designator"] == "U4"
    assert payload["sheet"] == "CPU.SchDoc"
    assert payload["pin_count"] == len(payload["pins"]) > 0
    reset_rows = [pin for pin in payload["pins"] if pin["net"] == "RST"]
    assert reset_rows
    connected = {
        (terminal["designator"], terminal["pin"])
        for terminal in reset_rows[0]["connected_to"]
    }
    assert ("U3", "48") in connected


def test_query_sheet_inspects_bare_schdoc() -> None:
    """Sheet payload inspects one SchDoc without needing a project."""
    payload = _run_query_json("sheet", str(HYDROSCOPE_SCHDOC))

    assert payload["schema"] == "altium_cruncher.query.sheet.a0"
    assert payload["filename"] == "CPU.SchDoc"
    assert payload["component_count"] == len(payload["components"]) > 0
    assert payload["net_label_count"] == len(payload["net_labels"])


def test_query_errors_exit_nonzero_with_stderr_hint() -> None:
    """Unknown designators and nets exit 1 with a stderr message."""
    unknown_designator = _run_query(
        "connections",
        "ZZ99",
        "--project",
        str(HYDROSCOPE_PROJECT),
    )
    assert unknown_designator.returncode == 1
    assert unknown_designator.stdout == ""
    assert "ZZ99" in unknown_designator.stderr

    unknown_net = _run_query(
        "nets",
        str(HYDROSCOPE_PROJECT),
        "--name",
        "NO_SUCH_NET",
    )
    assert unknown_net.returncode == 1
    assert "NO_SUCH_NET" in unknown_net.stderr


def test_query_stdout_stays_parseable_with_verbose_logging() -> None:
    """Verbose logging routes to stderr so stdout remains one JSON payload."""
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "--verbose",
            "query",
            "summary",
            str(HYDROSCOPE_PROJECT),
        ],
        cwd=PACKAGE_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["schema"] == "altium_cruncher.query.summary.a0"
