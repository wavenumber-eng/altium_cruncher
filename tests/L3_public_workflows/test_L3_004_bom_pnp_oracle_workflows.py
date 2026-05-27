"""Fixture-backed BOM, PnP, and JLC oracle workflow tests."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET


def _project_root() -> Path:
    """Find the repository root from this test file."""
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Could not locate repository root")


PACKAGE_ROOT = _project_root()
PROJECTS_ROOT = PACKAGE_ROOT / "tests" / "assets" / "projects"


@dataclass(frozen=True, slots=True)
class BomPnpOracleCase:
    """One project/variant pair with Altium BOM and PnP oracle files."""

    name: str
    project: Path
    variant: str | None
    bom_xml: Path
    pnp_csv: Path
    expect_exact_fitted_bom: bool
    expect_exact_pnp: bool

    @property
    def variant_label(self) -> str:
        """Return the output-folder-safe variant label."""
        return self.variant or "no_variant"

    @property
    def cli_variant_label(self) -> str:
        """Return the variant label used by configured CLI output templates."""
        return self.variant or "base"


NODE_TEST_ARRAY_B4 = BomPnpOracleCase(
    name="node_test_array",
    project=(
        PROJECTS_ROOT
        / "node_test_array"
        / "input"
        / "11-10077__node-test-array__B4.PrjPcb"
    ),
    variant="B4",
    bom_xml=(
        PROJECTS_ROOT
        / "node_test_array"
        / "reference_output"
        / "B4"
        / "XML-BOM"
        / "XML-BOM-11-10077__node-test-array__B4(B4).xml"
    ),
    pnp_csv=(
        PROJECTS_ROOT
        / "node_test_array"
        / "reference_output"
        / "B4"
        / "PNP-METRIC"
        / "Pick Place for node-test-array__B4(B4).csv"
    ),
    expect_exact_fitted_bom=False,
    expect_exact_pnp=False,
)
LOZ_OLD_MAN_BASE = BomPnpOracleCase(
    name="loz-old-man",
    project=PROJECTS_ROOT / "loz-old-man" / "input" / "loz-old-man.PrjPcb",
    variant=None,
    bom_xml=(
        PROJECTS_ROOT
        / "loz-old-man"
        / "reference_output"
        / "no_variant"
        / "XML-BOM"
        / "XML-BOM-loz-old-man.xml"
    ),
    pnp_csv=(
        PROJECTS_ROOT
        / "loz-old-man"
        / "reference_output"
        / "no_variant"
        / "PNP-METRIC"
        / "Pick Place for SB0037A.csv"
    ),
    expect_exact_fitted_bom=True,
    expect_exact_pnp=True,
)
ORACLE_CASES = (NODE_TEST_ARRAY_B4, LOZ_OLD_MAN_BASE)
PNP_COORDINATE_TOLERANCE_MM = 0.001


def _run_cli(*args: str) -> str:
    """Run Altium Cruncher and return combined command output."""
    completed = subprocess.run(
        [sys.executable, "-m", "altium_cruncher", *args],
        cwd=PACKAGE_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    combined = completed.stdout + completed.stderr
    assert completed.returncode == 0, combined
    assert "Traceback" not in combined
    assert "Logging error" not in combined
    return combined


def _variant_args(variant: str | None) -> list[str]:
    """Return CLI arguments for an optional variant."""
    if variant is None:
        return []
    return ["--variant", variant]


def _case_output_dir(root: Path, case: BomPnpOracleCase, command: str) -> Path:
    """Return the project fixture output folder used by workflow tests."""
    return root / case.name / "output" / command / case.variant_label


def _legacy_output_name(project: Path, variant: str | None, kind: str, ext: str) -> str:
    """Return a legacy single-format CLI output filename."""
    variant_part = f"_{variant}" if variant else ""
    return f"{project.stem}{variant_part}_{kind}.{ext}"


def _xml_bom_rows(path: Path) -> list[dict[str, str]]:
    """Parse Altium XML-BOM rows into dictionaries."""
    root = ET.parse(path).getroot()
    return [dict(row.attrib) for row in root.findall(".//ROW")]


def _pnp_rows(path: Path) -> list[dict[str, str]]:
    """Parse an Altium PNP-METRIC CSV and skip its metadata preamble."""
    lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    header_index = next(
        index
        for index, line in enumerate(lines)
        if line.startswith('"Designator"') or line.startswith("Designator")
    )
    return list(csv.DictReader(lines[header_index:]))


def _designators_from_bom_rows(rows: Iterable[dict[str, str]]) -> set[str]:
    """Return all designators named by Altium BOM rows."""
    designators: set[str] = set()
    for row in rows:
        for designator in row.get("Designator", "").split(","):
            normalized = designator.strip()
            if normalized:
                designators.add(normalized)
    return designators


def _component_by_designator(payload: dict[str, object]) -> dict[str, dict[str, object]]:
    """Index raw BOM JSON components by designator."""
    components = payload["components"]
    assert isinstance(components, list)
    result: dict[str, dict[str, object]] = {}
    for component in components:
        assert isinstance(component, dict)
        designator = str(component.get("designator", ""))
        result[designator] = component
    return result


def _normalize_oracle_layer(layer: str) -> str:
    """Normalize Altium PnP layer names to CLI JSON layer names."""
    normalized = layer.strip().lower()
    if normalized == "toplayer":
        return "top"
    if normalized == "bottomlayer":
        return "bottom"
    return normalized


def _float_text(value: str) -> float:
    """Parse Altium numeric text."""
    return float(value.strip())


def test_bom_raw_json_covers_altium_xml_oracle_designators(tmp_path: Path) -> None:
    """Validate raw BOM source data against Altium XML-BOM oracle designators."""
    for case in ORACLE_CASES:
        output_dir = _case_output_dir(tmp_path, case, "bom")
        _run_cli(
            "bom",
            str(case.project),
            *_variant_args(case.variant),
            "--format",
            "raw-json",
            "-o",
            str(output_dir),
        )

        payload_path = output_dir / _legacy_output_name(
            case.project,
            case.variant,
            "bom",
            "json",
        )
        payload = json.loads(payload_path.read_text(encoding="utf-8"))
        assert payload["schema"] == "wn.altium_cruncher.bom.raw.v1"

        components = _component_by_designator(payload)
        raw_designators = set(components)
        fitted_designators = {
            designator
            for designator, component in components.items()
            if not bool(component.get("dnp"))
        }
        oracle_rows = _xml_bom_rows(case.bom_xml)
        oracle_designators = _designators_from_bom_rows(oracle_rows)

        assert oracle_designators <= raw_designators
        if case.expect_exact_fitted_bom:
            assert oracle_designators == fitted_designators

        for row in oracle_rows[:20]:
            designator = row["Designator"]
            if "," in designator:
                continue
            component = components[designator]
            assert component["value"] == row["Name"]
            assert component["description"] == row["Description"]
            parameters = component["parameters"]
            assert isinstance(parameters, dict)
            expected_mpn = parameters.get("Manufacturer Part Number")
            if expected_mpn:
                assert expected_mpn == row["LibRef"]


def test_pnp_json_matches_altium_metric_oracle_core_geometry(tmp_path: Path) -> None:
    """Validate PnP JSON placement geometry against Altium PNP-METRIC CSV."""
    for case in ORACLE_CASES:
        output_dir = _case_output_dir(tmp_path, case, "pnp")
        _run_cli(
            "pnp",
            str(case.project),
            *_variant_args(case.variant),
            "--format",
            "json",
            "--exclude-no-bom",
            "-o",
            str(output_dir),
        )

        payload_path = output_dir / _legacy_output_name(
            case.project,
            case.variant,
            "pnp",
            "json",
        )
        payload = json.loads(payload_path.read_text(encoding="utf-8"))
        assert payload["schema"] == "wn.altium_cruncher.pnp.v1"
        assert payload["units"] == "mm"
        assert payload["position_mode"] == "altium-pick-place"

        oracle_by_designator = {
            row["Designator"]: row for row in _pnp_rows(case.pnp_csv)
        }
        placements = payload["placements"]
        assert isinstance(placements, list)
        placement_designators = {
            str(placement["designator"])
            for placement in placements
            if isinstance(placement, dict)
        }
        oracle_designators = set(oracle_by_designator)

        assert placement_designators <= oracle_designators
        if case.expect_exact_pnp:
            assert placement_designators == oracle_designators

        coordinate_mismatches: set[str] = set()
        for placement in placements:
            assert isinstance(placement, dict)
            row = oracle_by_designator[str(placement["designator"])]
            assert placement["layer"] == _normalize_oracle_layer(row["Layer"])
            assert abs(float(placement["rotation"]) - _float_text(row["Rotation"])) < 0.0002
            x_delta = abs(float(placement["center_x"]) - _float_text(row["Center-X(mm)"]))
            y_delta = abs(float(placement["center_y"]) - _float_text(row["Center-Y(mm)"]))
            if (
                x_delta >= PNP_COORDINATE_TOLERANCE_MM
                or y_delta >= PNP_COORDINATE_TOLERANCE_MM
            ):
                coordinate_mismatches.add(str(placement["designator"]))

        assert coordinate_mismatches == set()


def test_jlc_command_writes_paired_outputs_for_primary_fixtures(tmp_path: Path) -> None:
    """Exercise paired JLC BOM/CPL output for hierarchy and high-count fixtures."""
    for case in ORACLE_CASES:
        output_root = _case_output_dir(tmp_path, case, "jlc")
        _run_cli(
            "jlc",
            str(case.project),
            *_variant_args(case.variant),
            "--exclude-no-bom",
            "-o",
            str(output_root),
        )

        jlc_dir = output_root / "jlc"
        bom_path = jlc_dir / f"{case.project.stem}_{case.cli_variant_label}_jlc-csv.csv"
        cpl_path = jlc_dir / f"{case.project.stem}_{case.cli_variant_label}_jlc-cpl.csv"

        with bom_path.open(encoding="utf-8", newline="") as f:
            bom_rows = list(csv.DictReader(f))
        with cpl_path.open(encoding="utf-8", newline="") as f:
            cpl_rows = list(csv.DictReader(f))

        assert bom_rows
        assert cpl_rows
        assert tuple(bom_rows[0]) == (
            "Comment",
            "Designator",
            "Footprint",
            "JLCPCB Part #",
        )
        assert tuple(cpl_rows[0]) == (
            "Designator",
            "Layer",
            "Mid X",
            "Mid Y",
            "Rotation",
        )
