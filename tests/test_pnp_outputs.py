from __future__ import annotations

import csv

from altium_cruncher.altium_cruncher_cmd_pnp import (
    _pnp_format_option_error,
    _write_jlc_cpl_csv,
    _write_pnp_csv,
)


def _sample_placements() -> list[dict[str, object]]:
    """Return placement dictionaries matching Altium Monkey PnP fields."""
    return [
        {
            "designator": "R10",
            "comment": "10k",
            "layer": "bottom",
            "footprint": "R0603",
            "center_x": 1.25,
            "center_y": 2.5,
            "rotation": 180,
            "description": "resistor",
            "parameters": {"MPN": "ABC"},
        },
        {
            "designator": "R2",
            "comment": "10k",
            "layer": "top",
            "footprint": "R0603",
            "center_x": 3,
            "center_y": 4,
            "rotation": 90,
            "description": "resistor",
            "parameters": {"MPN": "ABC"},
        },
    ]


def test_write_pnp_csv_uses_normalized_sort_and_parameters(tmp_path) -> None:
    """Write standard PnP CSV from normalized records."""
    output = tmp_path / "pnp.csv"

    _write_pnp_csv(output, _sample_placements(), units="mm")

    rows = list(csv.reader(output.open(encoding="utf-8")))
    assert rows[0] == [
        "Designator",
        "Comment",
        "Layer",
        "Footprint",
        "Center-X(mm)",
        "Center-Y(mm)",
        "Rotation",
        "Description",
        "MPN",
    ]
    assert rows[1][0] == "R2"
    assert rows[2][0] == "R10"


def test_write_jlc_cpl_csv_uses_jlc_columns_and_mm_guard(tmp_path) -> None:
    """Write JLC CPL CSV and reject non-mm JLC units."""
    output = tmp_path / "cpl.csv"

    _write_jlc_cpl_csv(output, _sample_placements(), units="mm")

    rows = list(csv.DictReader(output.open(encoding="utf-8")))
    assert rows[0] == {
        "Designator": "R2",
        "Layer": "Top",
        "Mid X": "3",
        "Mid Y": "4",
        "Rotation": "90",
    }
    assert _pnp_format_option_error("jlc-cpl", "mils")
    assert _pnp_format_option_error("jlc-cpl", "mm") == ""
