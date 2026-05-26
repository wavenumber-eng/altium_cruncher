from __future__ import annotations

import json
from pathlib import Path
from typing import cast

from altium_cruncher.bom_pnp_model import (
    FieldAliasConfig,
    JLC_BOM_COLUMNS,
    JLC_CPL_COLUMNS,
    bom_raw_payload,
    group_bom_components,
    grouped_bom_payload,
    jlc_bom_rows,
    jlc_cpl_rows,
    normalize_bom_components,
    normalize_pnp_entries,
    pnp_payload,
    sort_designators,
)


def test_bom_alias_resolution_tracks_parameter_sources(tmp_path) -> None:
    """Normalize BOM fields through aliases and keep traceability."""
    raw_bom = [
        {
            "designator": "R1",
            "value": "10k",
            "footprint": "R0603",
            "description": "pullup",
            "parameters": {
                "Mfr": "Yageo",
                "MPN": "RC0603FR-0710KL",
                "LCSC": "C25804",
            },
            "dnp": False,
        }
    ]

    [component] = normalize_bom_components(raw_bom)
    component_list = [component]
    payload = bom_raw_payload(component_list, source=tmp_path, variant=None)

    assert component.canonical_fields["manufacturer"] == "Yageo"
    assert component.canonical_fields["manufacturer_part_number"] == "RC0603FR-0710KL"
    assert component.canonical_fields["jlcpcb_part_number"] == "C25804"
    assert component.field_sources["manufacturer"] == "parameter:Mfr"
    assert payload["schema"] == "wn.altium_cruncher.bom.raw.v1"
    assert payload["component_count"] == len(component_list)
    assert json.loads(json.dumps(payload))["schema"] == payload["schema"]


def test_bom_grouping_uses_aliases_and_natural_designator_sort() -> None:
    """Group same manufacturable parts and sort designators naturally."""
    raw_bom = [
        {
            "designator": "R10",
            "value": "10k",
            "footprint": "R0603",
            "parameters": {"Manufacturer": "Yageo", "MPN": "RC0603FR-0710KL"},
        },
        {
            "designator": "R2",
            "value": "10k",
            "footprint": "R0603",
            "parameters": {
                "Manufacturer": "Yageo",
                "Manufacturer Part Number": "RC0603FR-0710KL",
            },
        },
        {
            "designator": "R3",
            "value": "10k",
            "footprint": "R0603",
            "parameters": {"Manufacturer": "Yageo", "MPN": "RC0603FR-0710KL"},
            "dnp": True,
        },
    ]

    components = normalize_bom_components(raw_bom)
    lines = group_bom_components(components)

    assert sort_designators(["R10", "R2", "C1"]) == ["C1", "R2", "R10"]
    assert len(lines) == 2
    assert lines[0].designators == ("R2", "R10")
    assert lines[0].quantity == 2
    assert lines[0].dnp is False
    assert lines[1].designators == ("R3",)
    assert lines[1].dnp is True


def test_jlc_bom_rows_skip_dnp_by_default_and_preserve_columns() -> None:
    """Build JLC BOM rows from grouped lines."""
    raw_bom = [
        {
            "designator": "C1",
            "value": "100nF",
            "footprint": "C0603",
            "description": "decoupling capacitor",
            "parameters": {"JLCPCB Part #": "C14663"},
        },
        {
            "designator": "C2",
            "value": "100nF",
            "footprint": "C0603",
            "description": "decoupling capacitor",
            "parameters": {"JLCPCB Part #": "C14663"},
            "dnp": True,
        },
    ]

    lines = group_bom_components(normalize_bom_components(raw_bom))
    rows = jlc_bom_rows(lines)
    payload = grouped_bom_payload(lines, source=Path(__file__), variant="B4")

    assert tuple(rows[0]) == JLC_BOM_COLUMNS
    assert rows == [
        {
            "Comment": "decoupling capacitor",
            "Designator": "C1",
            "Footprint": "C0603",
            "JLCPCB Part #": "C14663",
        }
    ]
    assert payload["schema"] == "wn.altium_cruncher.bom.grouped.v1"
    assert payload["dnp_line_count"] == 1


def test_pnp_normalization_and_jlc_cpl_rows_sort_top_before_bottom() -> None:
    """Normalize placement entries and emit stable JLC CPL rows."""
    entries = [
        {
            "designator": "R10",
            "comment": "10k",
            "layer": "BottomLayer",
            "footprint": "R0603",
            "center_x": 1.23456,
            "center_y": 2.0,
            "rotation": 180.0,
            "description": "resistor",
            "parameters": {"MPN": "RC0603FR-0710KL"},
        },
        {
            "designator": "R2",
            "comment": "10k",
            "layer": "TopLayer",
            "footprint": "R0603",
            "center_x": 5,
            "center_y": 6,
            "rotation": 90,
            "parameters": {"MPN": "RC0603FR-0710KL"},
        },
    ]

    placements = normalize_pnp_entries(entries, units="mm")
    rows = jlc_cpl_rows(placements)
    payload = pnp_payload(placements, source=Path(__file__), variant=None, units="mm")

    assert tuple(rows[0]) == JLC_CPL_COLUMNS
    assert rows == [
        {
            "Designator": "R2",
            "Layer": "Top",
            "Mid X": "5",
            "Mid Y": "6",
            "Rotation": "90",
        },
        {
            "Designator": "R10",
            "Layer": "Bottom",
            "Mid X": "1.2346",
            "Mid Y": "2",
            "Rotation": "180",
        },
    ]
    assert payload["schema"] == "wn.altium_cruncher.pnp.v1"
    assert payload["placement_count"] == 2
    payload_placements = cast(list[dict[str, object]], payload["placements"])
    assert payload_placements[0]["designator"] == "R2"


def test_field_alias_config_accepts_json_style_custom_aliases() -> None:
    """Load custom canonical aliases from a config-style mapping."""
    aliases = FieldAliasConfig.from_mapping(
        {"manufacturer_part_number": ["Supplier MPN"]}
    )
    raw_bom = [
        {
            "designator": "U1",
            "value": "MCU",
            "parameters": {"Supplier MPN": "STM32-EXAMPLE"},
        }
    ]

    [component] = normalize_bom_components(raw_bom, aliases)

    assert component.canonical_fields["manufacturer_part_number"] == "STM32-EXAMPLE"
    assert aliases.to_json_obj() == {"manufacturer_part_number": ["Supplier MPN"]}
