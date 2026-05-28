from __future__ import annotations

import json
from pathlib import Path
from typing import cast

import pytest

from altium_cruncher.bom_pnp_cli_common import load_or_create_bom_pnp_config
from altium_cruncher.bom_pnp_model import (
    BOM_PNP_CONFIG_SCHEMA,
    BomPnpConfig,
    FieldAliasConfig,
    JLC_BOM_COLUMNS,
    JLC_CPL_COLUMNS,
    bom_raw_payload,
    configured_output_file,
    flat_raw_bom_payload,
    group_bom_components,
    grouped_bom_table_rows,
    grouped_bom_payload,
    jlc_bom_rows,
    jlc_cpl_rows,
    load_bom_pnp_config,
    normalize_bom_components,
    normalize_pnp_entries,
    ordered_bom_lines,
    pnp_table_rows,
    pnp_payload,
    select_variant_names,
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

    raw_payload = flat_raw_bom_payload(raw_bom)
    assert isinstance(raw_payload, list)
    assert raw_payload[0]["parameters"] == raw_bom[0]["parameters"]
    assert "canonical_fields" not in raw_payload[0]


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


def test_dnp_placement_can_follow_part_or_move_to_end() -> None:
    """Order split DNP lines beside matching parts or at the end."""
    raw_bom = [
        {
            "designator": "R1",
            "value": "10k",
            "footprint": "0603",
            "parameters": {"MPN": "RC0603"},
        },
        {
            "designator": "U1",
            "value": "100nF",
            "footprint": "0603",
            "parameters": {"MPN": "CC0603"},
        },
        {
            "designator": "C1",
            "value": "10k",
            "footprint": "0603",
            "parameters": {"MPN": "RC0603"},
            "dnp": True,
        },
    ]

    lines = group_bom_components(normalize_bom_components(raw_bom))
    inline_rows = grouped_bom_table_rows(
        lines,
        fields=("item", "designators", "dnp", "manufacturer_part_number"),
        dnp_placement="inline",
    )
    end_rows = grouped_bom_table_rows(
        lines,
        fields=("item", "designators", "dnp", "manufacturer_part_number"),
        dnp_placement="end",
    )

    assert [row["designators"] for row in inline_rows] == ["R1", "C1", "U1"]
    assert inline_rows[1]["manufacturer_part_number"] == "RC0603"
    assert [row["item"] for row in inline_rows] == ["1", "2", "3"]
    assert [row["designators"] for row in end_rows] == ["R1", "U1", "C1"]
    assert ordered_bom_lines(lines, dnp_placement="end")[-1].dnp is True


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
    assert payload["position_mode"] == "altium-pick-place"
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


def test_bom_pnp_config_parses_outputs_and_templates(tmp_path: Path) -> None:
    """Parse config mappings and resolve configured output paths."""
    config = BomPnpConfig.from_mapping(
        {
            "schema": BOM_PNP_CONFIG_SCHEMA,
            "variants": {"mode": "named", "names": ["B4"], "include_base": False},
            "bom": {
                "outputs": ["raw-json", "grouped-xlsx", "jlc-csv", "jlc-xlsx"],
                "group_fields": ["manufacturer_part_number", "value"],
                "highlight_dnp_rows": False,
            },
            "pnp": {
                "outputs": ["json", "xlsx", "jlc-cpl", "jlc-cpl-xlsx"],
                "layer_order": ["bottom", "top"],
                "position_mode": "component-origin",
            },
            "output": {
                "dir_template": "{Command}/{VariantName}",
                "name_template": "{SourceStem}_{PartNumberPCB}_{OutputKind}",
            },
        }
    )

    output = configured_output_file(
        tmp_path,
        config,
        source=Path("Project.PrjPcb"),
        command="bom",
        output_kind="grouped-xlsx",
        extension="xlsx",
        project_parameters={"PartNumberPCB": "175:TEST"},
        variant_name="B4",
    )

    assert config.schema == BOM_PNP_CONFIG_SCHEMA
    assert config.bom_outputs == ("raw-json", "grouped-xlsx", "jlc-csv", "jlc-xlsx")
    assert BomPnpConfig().variant_mode == "all"
    assert BomPnpConfig().bom_outputs == ("raw-json", "grouped-xlsx")
    assert BomPnpConfig().bom_group_fields == ("mfg", "mpn", "description")
    assert BomPnpConfig().bom_output_fields == (
        "mfg",
        "mpn",
        "description",
        "quantity",
        "designators",
    )
    assert "item" not in BomPnpConfig().bom_output_fields
    assert config.pnp_outputs == ("json", "xlsx", "jlc-cpl", "jlc-cpl-xlsx")
    assert config.highlight_dnp_rows is False
    assert config.pnp_position_mode == "component-origin"
    assert select_variant_names(["A", "B4"], config) == ["B4"]
    assert output == tmp_path / "bom" / "B4" / "Project_175_TEST_grouped-xlsx.xlsx"


def test_bom_pnp_config_loader_accepts_utf8_bom(tmp_path: Path) -> None:
    """Load Windows-written configs and hand-edited JSONC syntax."""
    config_path = tmp_path / "bom.config"
    config_path.write_text(
        """
        {
          // user notes are allowed in editable config files
          "schema": "wn.altium_cruncher.bom.config.v1",
        }
        """,
        encoding="utf-8-sig",
    )

    config = load_bom_pnp_config(config_path)

    assert config.schema == BOM_PNP_CONFIG_SCHEMA


def test_bom_config_auto_create_uses_default_policy(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Create the editable BOM config in the working folder on first use."""
    monkeypatch.chdir(tmp_path)

    config, config_path, created = load_or_create_bom_pnp_config(None)

    assert created is True
    assert config_path == tmp_path / "bom.config"
    assert config_path.exists()
    assert config.variant_mode == "all"
    assert config.include_base_variant is True
    assert config.bom_outputs == ("raw-json", "grouped-xlsx")
    assert config.bom_output_fields == (
        "mfg",
        "mpn",
        "description",
        "quantity",
        "designators",
    )


def test_configured_bom_and_pnp_table_rows_use_selected_fields() -> None:
    """Build configured table rows from grouped BOM and placement records."""
    bom_lines = group_bom_components(
        normalize_bom_components(
            [
                {
                    "designator": "R1",
                    "value": "10k",
                    "footprint": "R0603",
                    "parameters": {"MPN": "RC0603"},
                }
            ]
        )
    )
    placements = normalize_pnp_entries(
        [
            {
                "designator": "R1",
                "comment": "10k",
                "layer": "TopLayer",
                "footprint": "R0603",
                "center_x": 1,
                "center_y": 2,
                "rotation": 90,
            }
        ],
        units="mm",
    )

    assert grouped_bom_table_rows(
        bom_lines,
        fields=("mfg", "mpn", "description", "quantity", "designators"),
    ) == [
        {
            "mfg": "",
            "mpn": "RC0603",
            "description": "",
            "quantity": "1",
            "designators": "R1",
        }
    ]
    assert pnp_table_rows(placements, fields=("designator", "layer", "center_x")) == [
        {"designator": "R1", "layer": "top", "center_x": "1"}
    ]
