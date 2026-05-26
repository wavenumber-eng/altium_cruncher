from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import pytest

pytest.importorskip("easyeda_monkey")

from altium_cruncher.altium_cruncher_cmd_easyeda_footprint_review import (
    cmd_easyeda_footprint_review,
)
from altium_cruncher.altium_cruncher_cmd_easyeda_import import cmd_easyeda_import
from altium_cruncher.easyeda_altium_footprint import (
    EasyEdaFootprintImportPolicy,
    build_altium_pcblib_from_easyeda_footprint,
    load_easyeda_footprint_input,
    render_easyeda_footprint_source_svg,
)
from altium_monkey.altium_pcb_enums import PadShape
from altium_monkey.altium_pcblib import AltiumPcbLib
from altium_monkey.altium_record_pcb__region import AltiumPcbRegion
from altium_monkey.altium_record_pcb__shapebased_region import AltiumPcbShapeBasedRegion
from altium_monkey.altium_record_types import PcbLayer
from easyeda_monkey.easyeda_footprint import EasyEdaFootprint


CASES_DIR = (
    Path(__file__).resolve().parent / "assets" / "easyeda" / "api_responses"
)

STRESS_FOOTPRINT_FIXTURES = [
    "C21190__resistor_0603_1k.json",
    "C963370__usb_gt_usb_7010an.json",
    "C80192__power_step_powerstep01.json",
    "C2890616__oled_n096_1608tbbig11_h13.json",
    "C53078__led_matrix_fj2088bh.json",
    "C132660__led_segment_sr410361n.json",
    "C266603__sd_socket_sd_106m.json",
    "C701343__esp32_wroom_32e_castellated.json",
    "C7463411__lm317_to220_through_hole.json",
    "C5203974__smt_pogo_yz110615028f_01.json",
    "C7471747__through_hole_pogo_yzp0436_30165_01.json",
    "C7501824__rj45_hc_wk88_h16_db.json",
    "C14663__capacitor_0402_100nf.json",
    "C429954__connector_usb_c.json",
    "C57668__transistor_bc847b_215.json",
    "C2040__mcu_rp2040.json",
    "C42413366__pled18s_internal_graphics.json",
]


def _fixture_path(name: str) -> Path:
    path = CASES_DIR / name
    assert path.exists(), f"fixture not found: {path}"
    return path


def test_easyeda_resistor_imports_to_pcblib_with_pads_and_silk(tmp_path: Path) -> None:
    easyeda_footprint, source_data = load_easyeda_footprint_input(
        _fixture_path("C21190__resistor_0603_1k.json")
    )

    result = build_altium_pcblib_from_easyeda_footprint(
        easyeda_footprint,
        source_data=source_data,
    )

    footprint = result.library.footprints[0]
    assert result.report.footprint_name == "0603WAF1001T5E"
    assert result.report.source_pad_count == 2
    assert result.report.generated_pad_count == 2
    assert result.report.generated_hole_pad_count == 0
    assert result.report.track_segment_count == 6
    assert result.report.region_count == 5
    assert result.report.unsupported_count == 0
    assert len(footprint.pads) == 2
    assert {pad.designator for pad in footprint.pads} == {"1", "2"}
    assert {int(pad.layer) for pad in footprint.pads} == {int(PcbLayer.TOP)}
    assert all(int(pad.shape) == int(PadShape.RECTANGLE) for pad in footprint.pads)

    pcblib_path = tmp_path / "C21190.PcbLib"
    result.library.save(pcblib_path)
    reloaded = AltiumPcbLib.from_file(pcblib_path)
    assert len(reloaded.footprints) == 1
    assert reloaded.footprints[0].name == "0603WAF1001T5E"
    assert len(reloaded.footprints[0].pads) == 2


def test_easyeda_usb_imports_slotted_pads_and_non_pad_holes() -> None:
    easyeda_footprint, source_data = load_easyeda_footprint_input(
        _fixture_path("C963370__usb_gt_usb_7010an.json")
    )

    result = build_altium_pcblib_from_easyeda_footprint(
        easyeda_footprint,
        source_data=source_data,
    )

    footprint = result.library.footprints[0]
    assert result.report.source_pad_count == 16
    assert result.report.generated_pad_count == 18
    assert result.report.generated_hole_pad_count == 2
    assert result.report.slotted_pad_count == 4
    assert result.report.circle_count == 4
    assert result.report.region_count == 33
    assert result.report.unsupported_count == 0
    assert len(footprint.pads) == 18
    assert sum(1 for pad in footprint.pads if pad.slot_size > 0) == 4
    assert {
        round(pad.slot_rotation)
        for pad in footprint.pads
        if pad.designator in {"13", "14", "15", "16"}
    } == {90}
    assert sum(
        1
        for region in footprint.regions
        if isinstance(region, AltiumPcbShapeBasedRegion)
        and any(vertex.is_round for vertex in region.outline)
    ) == 4
    hole_pads = [pad for pad in footprint.pads if pad.designator.startswith("HOLE")]
    assert {pad.designator for pad in hole_pads} == {
        "HOLE1",
        "HOLE2",
    }
    assert all(pad.hole_size > 0 and not pad.is_plated for pad in hole_pads)


def test_easyeda_multilayer_pad_drills_render_in_footprint_svg() -> None:
    for fixture_name in (
        "C132660__led_segment_sr410361n.json",
        "C429954__connector_usb_c.json",
    ):
        easyeda_footprint, source_data = load_easyeda_footprint_input(_fixture_path(fixture_name))

        result = build_altium_pcblib_from_easyeda_footprint(
            easyeda_footprint,
            source_data=source_data,
        )

        footprint = result.library.footprints[0]
        assert all(pad.layer == int(PcbLayer.MULTI_LAYER) for pad in footprint.pads)
        assert all(pad.hole_size > 0 for pad in footprint.pads)
        svg_text = footprint.to_svg()
        assert 'data-layer-name="DRILLS"' in svg_text
        assert 'data-hole-kind="round"' in svg_text


def test_easyeda_source_preview_draws_obround_pads_and_slots() -> None:
    easyeda_footprint, source_data = load_easyeda_footprint_input(
        _fixture_path("C963370__usb_gt_usb_7010an.json")
    )

    svg_text = render_easyeda_footprint_source_svg(
        easyeda_footprint,
        source_data=source_data,
    )

    assert 'data-hole-kind="slot"' in svg_text
    assert 'stroke-linecap="round"' in svg_text
    assert "<ellipse" not in svg_text
    assert 'stroke="#D8D8D8"' in svg_text


def test_easyeda_curved_solid_regions_survive_pcblib_reload(tmp_path: Path) -> None:
    easyeda_footprint, source_data = load_easyeda_footprint_input(
        _fixture_path("C963370__usb_gt_usb_7010an.json")
    )

    result = build_altium_pcblib_from_easyeda_footprint(
        easyeda_footprint,
        source_data=source_data,
    )
    pcblib_path = tmp_path / "C963370.PcbLib"
    result.library.save(pcblib_path)

    reloaded = AltiumPcbLib.from_file(pcblib_path)
    footprint = reloaded.footprints[0]
    curved_region_count = sum(
        1
        for region in footprint.regions
        if isinstance(region, AltiumPcbShapeBasedRegion)
        and any(vertex.is_round for vertex in region.outline)
    )
    assert curved_region_count == 4
    assert " A " in footprint.to_svg()


def test_easyeda_non_altium_curves_are_approximated_with_report_warnings() -> None:
    source_data = {
        "result": {
            "title": "CURVE_APPROX_TEST",
            "lcsc": {"number": "C0"},
            "packageDetail": {
                "dataStr": {
                    "head": "",
                    "shape": [
                        (
                            "SOLIDREGION~3~~M 0 0 A 10 5 0 0 1 20 0 "
                            "L 20 10 L 0 10 Z~solid~gge-ellipse~~~~0"
                        ),
                        (
                            "SOLIDREGION~3~~M 30 0 C 35 10 45 10 50 0 "
                            "L 50 10 L 30 10 Z~solid~gge-cubic~~~~0"
                        ),
                    ],
                }
            },
        }
    }
    easyeda_footprint = EasyEdaFootprint.from_json(source_data)

    result = build_altium_pcblib_from_easyeda_footprint(
        easyeda_footprint,
        source_data=source_data,
        policy=EasyEdaFootprintImportPolicy(
            curve_approximation_segments=6,
            arc_approximation_max_degrees=30.0,
        ),
    )

    footprint = result.library.footprints[0]
    regions = [region for region in footprint.regions if isinstance(region, AltiumPcbRegion)]
    assert result.report.unsupported_count == 0
    assert any("gge-ellipse:approximated elliptical arc" in item for item in result.report.warnings)
    assert any("gge-cubic:approximated cubic bezier" in item for item in result.report.warnings)
    assert len(regions) == 2
    assert len(regions[0].outline_vertices) > 4
    assert len(regions[1].outline_vertices) > 4


def test_easyeda_silkscreen_svg_arcs_keep_short_sweeps() -> None:
    easyeda_footprint, source_data = load_easyeda_footprint_input(
        _fixture_path("C14663__capacitor_0402_100nf.json")
    )

    result = build_altium_pcblib_from_easyeda_footprint(
        easyeda_footprint,
        source_data=source_data,
    )

    quarter_arcs = [
        arc
        for arc in result.library.footprints[0].arcs
        if int(arc.layer) == int(PcbLayer.TOP_OVERLAY) and arc.radius == 121980
    ]
    assert len(quarter_arcs) == 4
    for arc in quarter_arcs:
        assert math.isclose((arc.end_angle - arc.start_angle) % 360.0, 90.0, abs_tol=0.02)


def test_easyeda_sd_socket_svg_arcs_do_not_flip_to_large_sweeps() -> None:
    easyeda_footprint, source_data = load_easyeda_footprint_input(
        _fixture_path("C266603__sd_socket_sd_106m.json")
    )

    result = build_altium_pcblib_from_easyeda_footprint(
        easyeda_footprint,
        source_data=source_data,
    )

    sweeps = [
        (arc.end_angle - arc.start_angle) % 360.0
        for arc in result.library.footprints[0].arcs
        if int(arc.layer) == int(PcbLayer.TOP_OVERLAY)
        and not math.isclose((arc.end_angle - arc.start_angle) % 360.0, 0.0, abs_tol=0.02)
    ]
    assert max(sweeps) <= 180.02
    assert sum(math.isclose(sweep, 90.0, abs_tol=0.02) for sweep in sweeps) >= 4
    assert any(math.isclose(sweep, 180.0, abs_tol=0.02) for sweep in sweeps)


def test_easyeda_power_step_imports_polygon_custom_pads() -> None:
    easyeda_footprint, source_data = load_easyeda_footprint_input(
        _fixture_path("C80192__power_step_powerstep01.json")
    )

    result = build_altium_pcblib_from_easyeda_footprint(
        easyeda_footprint,
        source_data=source_data,
    )

    footprint = result.library.footprints[0]
    assert result.report.source_pad_count == 102
    assert result.report.generated_pad_count == 102
    assert result.report.custom_pad_count == 4
    assert result.report.unsupported_count == 0
    assert sum(1 for pad in footprint.pads if pad.custom_shape is not None) == 4
    assert len(footprint.regions) >= result.report.custom_pad_count


def test_easyeda_import_cli_generates_pcblib_report_and_footprint_preview(
    tmp_path: Path,
) -> None:
    result = cmd_easyeda_import(
        argparse.Namespace(
            lcsc_id="C963370",
            input_json=_fixture_path("C963370__usb_gt_usb_7010an.json"),
            cache_dir=None,
            no_fetch=True,
            symbol_name=None,
            schlib_name=None,
            footprint=True,
            full=False,
            footprint_name=None,
            pcblib_name=None,
            preview=True,
            pin_grid_mils=100.0,
            no_align_pin_grid=False,
            use_source_pin_electrical=False,
            use_source_pin_ieee_symbols=False,
            pin_name_visibility="source",
            pin_designator_visibility="source",
            pin_text_orientation="default",
            rotate_vertical_pin_text=False,
            output=tmp_path,
        )
    )

    assert result == 0
    case_dir = tmp_path / "C963370"
    assert (case_dir / "C963370.SchLib").exists()
    assert (case_dir / "C963370.PcbLib").exists()

    report = json.loads(
        (case_dir / "easyeda-footprint-report.json").read_text(encoding="utf-8")
    )
    assert report["footprint_name"] == "GT-USB-7010AN"
    assert report["generated_pad_count"] == 18
    assert report["generated_hole_pad_count"] == 2
    assert report["slotted_pad_count"] == 4
    assert report["unsupported_count"] == 0

    preview_dir = case_dir / "preview"
    assert (preview_dir / "easyeda-footprint-source.svg").exists()
    assert (preview_dir / "altium-footprint.svg").exists()
    assert (preview_dir / "footprint-compare.svg").exists()
    assert "Overlay" in (preview_dir / "footprint-compare.svg").read_text(
        encoding="utf-8"
    )


@pytest.mark.parametrize("fixture_name", STRESS_FOOTPRINT_FIXTURES)
def test_easyeda_requested_footprint_stress_cases_import_without_unsupported(
    fixture_name: str,
) -> None:
    easyeda_footprint, source_data = load_easyeda_footprint_input(_fixture_path(fixture_name))

    result = build_altium_pcblib_from_easyeda_footprint(
        easyeda_footprint,
        source_data=source_data,
    )

    footprint = result.library.footprints[0]
    assert result.report.unsupported_count == 0
    assert result.report.source_pad_count > 0
    assert result.report.generated_pad_count >= result.report.source_pad_count
    assert len(footprint.pads) == result.report.generated_pad_count
    assert "<svg" in footprint.to_svg()


def test_easyeda_footprint_review_cli_generates_multi_case_html_and_svg(
    tmp_path: Path,
) -> None:
    result = cmd_easyeda_footprint_review(
        argparse.Namespace(
            inputs=[
                _fixture_path("C963370__usb_gt_usb_7010an.json"),
                _fixture_path("C266603__sd_socket_sd_106m.json"),
                _fixture_path("C53078__led_matrix_fj2088bh.json"),
            ],
            fixture_dir=None,
            pattern="*.json",
            only=None,
            title="Footprint Review Test",
            curve_approximation_segments=12,
            arc_approximation_max_degrees=15.0,
            include_source_text=False,
            output=tmp_path,
        )
    )

    assert result == 0
    html_path = tmp_path / "review.html"
    svg_path = tmp_path / "review.svg"
    assert html_path.exists()
    assert svg_path.exists()

    html_text = html_path.read_text(encoding="utf-8")
    svg_text = svg_path.read_text(encoding="utf-8")
    source_svg_text = (
        tmp_path / "case-previews" / "C963370" / "easyeda-footprint-source.svg"
    ).read_text(encoding="utf-8")
    assert "C963370" in html_text
    assert "C266603" in html_text
    assert "C53078" in html_text
    assert "EasyEDA Source" in html_text
    assert "Altium Generated" in html_text
    assert "pads=" in html_text
    assert "data-svg-viewer" in html_text
    assert "data-layer-controls" in html_text
    assert "Color key" in html_text
    assert "Altium top copper" in html_text
    assert "Import layer mapping" in html_text
    assert "data-global-layer-controls" in html_text
    assert "Global layers" in html_text
    assert "99 - Board outline" in html_text
    assert "MECHANICAL13" in html_text
    assert "Source layers used" in html_text
    assert 'data-layer-display-name="EasyEDA' in source_svg_text
    assert 'data-doc-id="easyeda-altium-footprint-review"' in svg_text
    assert "footprint-review-row-3" in svg_text
