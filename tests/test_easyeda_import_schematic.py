from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

pytest.importorskip("easyeda_monkey")

from altium_cruncher.altium_cruncher_cmd_easyeda_import import cmd_easyeda_import
from altium_cruncher.altium_cruncher_cmd_easyeda_review import cmd_easyeda_review
from altium_cruncher.easyeda_altium_symbol import (
    EasyEdaSchematicImportPolicy,
    build_altium_schlib_from_easyeda_symbol,
    load_easyeda_symbol_input,
)
from altium_monkey.altium_sch_enums import IeeeSymbol, PinElectrical, PinItemMode, Rotation90
from altium_monkey.altium_schlib import AltiumSchLib


CASES_DIR = (
    Path(__file__).resolve().parent / "assets" / "easyeda" / "api_responses"
)


def _fixture_path(name: str) -> Path:
    path = CASES_DIR / name
    assert path.exists(), f"fixture not found: {path}"
    return path


def test_easyeda_c2040_imports_to_schlib_with_all_pins(tmp_path: Path) -> None:
    easyeda_symbol, source_data = load_easyeda_symbol_input(
        _fixture_path("C2040__mcu_rp2040.json")
    )

    result = build_altium_schlib_from_easyeda_symbol(
        easyeda_symbol,
        source_data=source_data,
    )

    assert result.report.symbol_name == "RP2040"
    assert result.report.designator == "U?"
    assert result.report.pin_count == 57
    assert result.report.rectangle_count == 1
    assert result.report.unsupported_count == 0
    assert result.report.grid["source_common_offset_possible"] is False
    assert result.report.grid["off_grid_hotspot_count"] > 0
    assert result.report.warnings

    symbol = result.library.symbols[0]
    pin9 = next(pin for pin in symbol.pins if pin.designator == "9")
    assert pin9.name == "GPIO7"
    assert pin9.orientation == Rotation90.DEG_0
    assert pin9.location.x_mils < pin9.get_hot_spot().x_mils

    schlib_path = tmp_path / "C2040.SchLib"
    result.library.save(schlib_path, sync_pin_text_data=True)
    reloaded = AltiumSchLib(schlib_path)
    assert len(reloaded.symbols) == 1
    assert reloaded.symbols[0].name == "RP2040"
    assert len(reloaded.symbols[0].pins) == 57


def test_easyeda_passive_designator_and_path_endpoint_direction() -> None:
    easyeda_symbol, source_data = load_easyeda_symbol_input(
        _fixture_path("C14663__capacitor_0402_100nf.json")
    )

    result = build_altium_schlib_from_easyeda_symbol(
        easyeda_symbol,
        source_data=source_data,
    )

    symbol = result.library.symbols[0]
    assert symbol.designators[0].text == "C?"
    pin1 = next(pin for pin in symbol.pins if pin.designator == "1")
    pin2 = next(pin for pin in symbol.pins if pin.designator == "2")

    assert pin1.orientation == Rotation90.DEG_180
    assert pin1.location.x_mils > pin1.get_hot_spot().x_mils
    assert pin2.orientation == Rotation90.DEG_0
    assert pin2.location.x_mils < pin2.get_hot_spot().x_mils


def test_easyeda_resistor_imports_designator_and_body_rectangle() -> None:
    easyeda_symbol, source_data = load_easyeda_symbol_input(
        _fixture_path("C21190__resistor_0603_1k.json")
    )

    result = build_altium_schlib_from_easyeda_symbol(
        easyeda_symbol,
        source_data=source_data,
    )

    symbol = result.library.symbols[0]
    assert result.report.symbol_name == "0603WAF1001T5E"
    assert result.report.designator == "R?"
    assert result.report.pin_count == 2
    assert result.report.rectangle_count == 1
    assert symbol.designators[0].text == "R?"
    assert len(symbol.pins) == 2
    assert len(symbol.rectangles) == 1


def test_easyeda_power_step_imports_dense_symbol() -> None:
    easyeda_symbol, source_data = load_easyeda_symbol_input(
        _fixture_path("C80192__power_step_powerstep01.json")
    )

    result = build_altium_schlib_from_easyeda_symbol(
        easyeda_symbol,
        source_data=source_data,
    )

    symbol = result.library.symbols[0]
    assert result.report.symbol_name == "POWERSTEP01"
    assert result.report.designator == "U?"
    assert result.report.pin_count == 98
    assert result.report.rectangle_count == 1
    assert result.report.ellipse_count == 1
    assert result.report.unsupported_count == 0
    assert result.report.grid["source_common_offset_possible"] is True
    assert result.report.grid["anchor_adjusted_to_grid"] is True
    assert result.report.grid["off_grid_hotspot_count"] == 0
    assert result.report.warnings == []
    assert len(symbol.pins) == 98
    assert len(symbol.rectangles) == 1
    assert len(symbol.ellipses) == 1


def test_easyeda_transistor_imports_line_and_polygon_geometry() -> None:
    easyeda_symbol, source_data = load_easyeda_symbol_input(
        _fixture_path("C57668__transistor_bc847b_215.json")
    )

    result = build_altium_schlib_from_easyeda_symbol(
        easyeda_symbol,
        source_data=source_data,
    )

    symbol = result.library.symbols[0]
    assert result.report.symbol_name == "BC847B,215"
    assert result.report.designator == "Q?"
    assert result.report.pin_count == 3
    assert result.report.polyline_count == 3
    assert result.report.polygon_count == 1
    assert result.report.unsupported_count == 0
    assert len(symbol.pins) == 3
    assert len(symbol.polylines) == 3
    assert len(symbol.polygons) == 1


def test_easyeda_led_matrix_imports_repeated_ellipse_geometry() -> None:
    easyeda_symbol, source_data = load_easyeda_symbol_input(
        _fixture_path("C53078__led_matrix_fj2088bh.json")
    )

    result = build_altium_schlib_from_easyeda_symbol(
        easyeda_symbol,
        source_data=source_data,
    )

    symbol = result.library.symbols[0]
    assert result.report.symbol_name == "LED FJ2088BH"
    assert result.report.designator == "LED?"
    assert result.report.pin_count == 16
    assert result.report.rectangle_count == 1
    assert result.report.ellipse_count == 64
    assert result.report.unsupported_count == 0
    assert result.report.grid["off_grid_hotspot_count"] == 0
    assert len(symbol.ellipses) == 64


def test_easyeda_rj45_imports_internal_line_geometry() -> None:
    easyeda_symbol, source_data = load_easyeda_symbol_input(
        _fixture_path("C7501824__rj45_hc_wk88_h16_db.json")
    )

    result = build_altium_schlib_from_easyeda_symbol(
        easyeda_symbol,
        source_data=source_data,
    )

    symbol = result.library.symbols[0]
    assert result.report.symbol_name == "HC-WK88-H16-DB"
    assert result.report.pin_count == 14
    assert result.report.rectangle_count == 1
    assert result.report.polyline_count == 9
    assert result.report.unsupported_count == 0
    assert result.report.grid["source_common_offset_possible"] is False
    assert result.report.grid["off_grid_hotspot_count"] == 14
    assert len(symbol.polylines) == 9


def test_easyeda_led_segment_imports_mixed_symbol_graphics() -> None:
    easyeda_symbol, source_data = load_easyeda_symbol_input(
        _fixture_path("C132660__led_segment_sr410361n.json")
    )

    result = build_altium_schlib_from_easyeda_symbol(
        easyeda_symbol,
        source_data=source_data,
    )

    symbol = result.library.symbols[0]
    assert result.report.symbol_name == "SR410361N"
    assert result.report.designator == "LED?"
    assert result.report.pin_count == 12
    assert result.report.rectangle_count == 1
    assert result.report.ellipse_count == 4
    assert result.report.polyline_count == 8
    assert result.report.unsupported_count == 0
    assert len(symbol.ellipses) == 4
    assert len(symbol.polylines) == 8


def test_easyeda_pled18s_reports_unsupported_symbol_paths() -> None:
    easyeda_symbol, source_data = load_easyeda_symbol_input(
        _fixture_path("C42413366__pled18s_internal_graphics.json")
    )

    result = build_altium_schlib_from_easyeda_symbol(
        easyeda_symbol,
        source_data=source_data,
    )

    symbol = result.library.symbols[0]
    assert result.report.symbol_name == "PLED18S_C42413366"
    assert result.report.designator == "D?"
    assert result.report.pin_count == 2
    assert result.report.rectangle_count == 1
    assert result.report.polyline_count == 12
    assert result.report.unsupported_count == 2
    assert result.report.unsupported_graphics == ["path:gge79", "path:gge157"]
    assert len(symbol.polylines) == 12


def test_easyeda_pin_policy_defaults_to_passive_and_can_use_source_electrical() -> None:
    easyeda_symbol, source_data = load_easyeda_symbol_input(
        _fixture_path("C2040__mcu_rp2040.json")
    )
    source_io_pin = next(pin for pin in easyeda_symbol.pins if pin.electrical_type == "3")

    default_result = build_altium_schlib_from_easyeda_symbol(
        easyeda_symbol,
        source_data=source_data,
    )
    default_pin = next(
        pin for pin in default_result.library.symbols[0].pins if pin.designator == source_io_pin.number
    )
    assert default_pin.electrical == PinElectrical.PASSIVE
    assert default_result.report.policy["use_source_pin_electrical"] is False

    source_result = build_altium_schlib_from_easyeda_symbol(
        easyeda_symbol,
        source_data=source_data,
        policy=EasyEdaSchematicImportPolicy(use_source_pin_electrical=True),
    )
    source_pin = next(
        pin for pin in source_result.library.symbols[0].pins if pin.designator == source_io_pin.number
    )
    assert source_pin.electrical == PinElectrical.IO
    assert source_result.report.policy["use_source_pin_electrical"] is True


def test_easyeda_pin_policy_controls_text_visibility_and_rotation() -> None:
    easyeda_symbol, source_data = load_easyeda_symbol_input(
        _fixture_path("C2040__mcu_rp2040.json")
    )

    result = build_altium_schlib_from_easyeda_symbol(
        easyeda_symbol,
        source_data=source_data,
        policy=EasyEdaSchematicImportPolicy(
            pin_name_visibility="hide",
            pin_designator_visibility="show",
            pin_text_orientation="vertical",
        ),
    )

    symbol = result.library.symbols[0]
    assert all(not pin.show_name for pin in symbol.pins)
    assert all(pin.show_designator for pin in symbol.pins)
    assert result.report.policy["pin_text_orientation"] == "vertical"


def test_easyeda_pin_policy_can_match_source_text_orientation() -> None:
    easyeda_symbol, source_data = load_easyeda_symbol_input(
        _fixture_path("C2040__mcu_rp2040.json")
    )

    default_result = build_altium_schlib_from_easyeda_symbol(
        easyeda_symbol,
        source_data=source_data,
    )
    default_symbol = default_result.library.symbols[0]
    default_vertical_pin = next(pin for pin in default_symbol.pins if pin.designator == "50")
    assert default_vertical_pin.name_settings.position_mode == PinItemMode.DEFAULT
    assert default_vertical_pin.designator_settings.position_mode == PinItemMode.DEFAULT

    source_result = build_altium_schlib_from_easyeda_symbol(
        easyeda_symbol,
        source_data=source_data,
        policy=EasyEdaSchematicImportPolicy(pin_text_orientation="source"),
    )
    source_symbol = source_result.library.symbols[0]
    source_vertical_pin = next(pin for pin in source_symbol.pins if pin.designator == "50")
    source_horizontal_pin = next(pin for pin in source_symbol.pins if pin.designator == "9")

    assert source_result.report.policy["pin_text_orientation"] == "source"
    assert source_vertical_pin.name_settings.position_mode == PinItemMode.DEFAULT
    assert source_vertical_pin.designator_settings.position_mode == PinItemMode.DEFAULT
    assert source_horizontal_pin.name_settings.position_mode == PinItemMode.DEFAULT
    assert source_horizontal_pin.designator_settings.position_mode == PinItemMode.DEFAULT


def test_easyeda_pin_policy_controls_source_pin_ieee_symbols() -> None:
    easyeda_symbol, source_data = load_easyeda_symbol_input(
        _fixture_path("C2040__mcu_rp2040.json")
    )
    source_pin_with_dot = easyeda_symbol.pins[0]
    source_pin_with_dot.dot_visible = True

    default_result = build_altium_schlib_from_easyeda_symbol(
        easyeda_symbol,
        source_data=source_data,
    )
    default_pin = next(
        pin
        for pin in default_result.library.symbols[0].pins
        if pin.designator == source_pin_with_dot.number
    )
    assert default_pin.symbol_outer == IeeeSymbol.NONE

    source_symbol_result = build_altium_schlib_from_easyeda_symbol(
        easyeda_symbol,
        source_data=source_data,
        policy=EasyEdaSchematicImportPolicy(use_source_pin_ieee_symbols=True),
    )
    source_symbol_pin = next(
        pin
        for pin in source_symbol_result.library.symbols[0].pins
        if pin.designator == source_pin_with_dot.number
    )
    assert source_symbol_pin.symbol_outer == IeeeSymbol.DOT


def test_easyeda_import_cli_generates_schlib_report_and_preview(tmp_path: Path) -> None:
    result = cmd_easyeda_import(
        argparse.Namespace(
            lcsc_id="C2040",
            input_json=_fixture_path("C2040__mcu_rp2040.json"),
            cache_dir=None,
            no_fetch=True,
            symbol_name=None,
            schlib_name=None,
            symbol_only=False,
            preview=True,
            pin_grid_mils=100.0,
            no_align_pin_grid=False,
            output=tmp_path,
        )
    )

    assert result == 0
    case_dir = tmp_path / "C2040"
    assert (case_dir / "C2040.SchLib").exists()
    assert (case_dir / "C2040.PcbLib").exists()
    assert not (case_dir / "easyeda-3d-models.json").exists()
    report = json.loads((case_dir / "easyeda-import-report.json").read_text(encoding="utf-8"))
    assert report["symbol_name"] == "RP2040"
    assert report["pin_count"] == 57
    assert report["grid"]["off_grid_hotspot_count"] > 0
    assert report["warnings"]
    preview_dir = case_dir / "preview"
    assert (preview_dir / "easyeda-source.svg").exists()
    assert (preview_dir / "compare.svg").exists()
    assert "EasyEDA Source" in (preview_dir / "compare.svg").read_text(encoding="utf-8")
    assert "Altium Generated" in (preview_dir / "compare.svg").read_text(encoding="utf-8")
    assert "Overlay" in (preview_dir / "compare.svg").read_text(encoding="utf-8")


def test_easyeda_review_cli_generates_multi_case_html_and_svg(tmp_path: Path) -> None:
    result = cmd_easyeda_review(
        argparse.Namespace(
            inputs=[
                _fixture_path("C53078__led_matrix_fj2088bh.json"),
                _fixture_path("C7501824__rj45_hc_wk88_h16_db.json"),
            ],
            fixture_dir=None,
            pattern="*.json",
            only=None,
            title="EasyEDA Review Test",
            pin_grid_mils=100.0,
            no_align_pin_grid=False,
            output=tmp_path,
        )
    )

    assert result == 0
    review_html = tmp_path / "review.html"
    review_svg = tmp_path / "review.svg"
    assert review_html.exists()
    assert review_svg.exists()

    html_text = review_html.read_text(encoding="utf-8")
    assert "EasyEDA Review Test" in html_text
    assert "C53078" in html_text
    assert "C7501824" in html_text
    assert "EasyEDA Source" in html_text
    assert "Altium Generated" in html_text

    svg_text = review_svg.read_text(encoding="utf-8")
    assert "review-row-1" in svg_text
    assert "review-row-2" in svg_text
    assert "EasyEDA Source" in svg_text
    assert "Altium Generated" in svg_text


def test_easyeda_review_source_pin_text_orientation_updates_preview_svg(tmp_path: Path) -> None:
    result = cmd_easyeda_review(
        argparse.Namespace(
            inputs=[_fixture_path("C2040__mcu_rp2040.json")],
            fixture_dir=None,
            pattern="*.json",
            only=None,
            title="EasyEDA Source Text Review Test",
            pin_grid_mils=100.0,
            no_align_pin_grid=False,
            use_source_pin_electrical=False,
            use_source_pin_ieee_symbols=False,
            pin_name_visibility="source",
            pin_designator_visibility="source",
            pin_text_orientation="source",
            rotate_vertical_pin_text=False,
            output=tmp_path,
        )
    )

    assert result == 0
    preview_svg = tmp_path / "case-previews" / "C2040" / "RP2040_ir.svg"
    assert preview_svg.exists()
    assert "rotate(" in preview_svg.read_text(encoding="utf-8")
