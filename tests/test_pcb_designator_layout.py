"""Geometry behavior shared with autodoc, and the separate cutout rotation bias."""
import math
from pathlib import Path

import pytest

from altium_cruncher.altium_cruncher_pcb_designator_layout import (
    CcaComponentGeometryFact, CcaDesignatorFitSession, fit_designator_to_geometry,
)
from altium_cruncher.altium_cruncher_pcb_svg_cutout_layer import fit_cutout_label
from altium_cruncher.altium_cruncher_pcb_designator_pads import component_designator_pads


def ring(x, y, w, h):
    return ((x, y), (x + w, y), (x + w, y + h), (x, y + h))


def segments(points):
    return tuple(zip(points, points[1:] + points[:1]))


def test_designators_follow_long_axis_and_preserve_disconnected_body_regions():
    small = ring(0, 0, 1, 1)
    tall = ring(10, 0, 1, 4)
    geometry = CcaComponentGeometryFact((0, 0, 11, 4), segments(small) + segments(tall))
    fit = fit_designator_to_geometry("R100", geometry, fill_ratio=.8, maximum_font_size_mm=2.5)
    assert fit.rotation_degrees == -90
    assert 10 < fit.center_mm[0] < 11  # The gap between bodies cannot hold a label.
    assert fit.font_size_mm == pytest.approx(.8, abs=.002)
    capped = fit_designator_to_geometry("R100", geometry, fill_ratio=.8, maximum_font_size_mm=.1)
    assert capped.rotation_degrees == 0  # Autodoc compares final capped sizes.


def test_pad_envelope_and_translated_fit_cache():
    pads = segments(ring(0, 0, 1, 1)) + segments(ring(3, 0, 1, 1))
    session = CcaDesignatorFitSession()
    results = []
    for dx, dy in ((0, 0), (17, -23)):
        geometry = CcaComponentGeometryFact(
            (dx, dy, dx + 4, dy + 1),
            tuple(tuple((x + dx, y + dy) for x, y in segment) for segment in pads), "pads",
        )
        results.append(fit_designator_to_geometry("J1", geometry, fill_ratio=.8,
                                               maximum_font_size_mm=2.5, session=session))
    assert results[0].center_mm == pytest.approx((2, .5))
    assert results[1].center_mm == pytest.approx((19, -22.5))
    assert results[0].font_size_mm == results[1].font_size_mm
    assert session.telemetry.hits == 1


def test_cutout_rotation_requires_meaningful_gain():
    circle = tuple((math.cos(i * math.tau / 48), math.sin(i * math.tau / 48) * (1 + 1e-14)) for i in range(48))
    for points in (circle, ring(0, 0, 2, 2.3)):
        assert fit_cutout_label(points, "CUTOUT", {}).rotation_degrees == 0
    assert fit_cutout_label(ring(0, 0, 1, 4), "CUTOUT", {}).rotation_degrees == -90


def _rt_pcb():
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc
    return AltiumPcbDoc.from_file(
        Path(__file__).resolve().parents[1] / "tests/assets/projects/rt_super_c1/input/RT_SUPER_C1.PCBdoc"
    )


@pytest.mark.parametrize("mirror", [False, True])
def test_rt_j1_designator_centers_on_electrical_pads(mirror):
    from dataclasses import replace
    from altium_monkey.altium_record_types import PcbLayer
    from altium_cruncher.altium_cruncher_pcb_svg_a0_renderer import PcbSvgA0Renderer
    from altium_cruncher.altium_cruncher_pcb_svg_config import PcbSvgConfig

    pcb = _rt_pcb()
    index = next(i for i, component in enumerate(pcb.components) if component.designator == "J1")
    selected = component_designator_pads(pcb.pads, index, "top")
    assert {pad.designator for pad in selected} == set("123456")
    assert all(not pad._should_render_on_layer(PcbLayer.TOP) for pad in selected)
    assert all(pad._should_force_svg_copper_render(PcbLayer.TOP) for pad in selected)
    renderer = PcbSvgA0Renderer(PcbSvgConfig.default())
    renderer.options = replace(renderer.options, mirror_x=mirror)
    ctx = renderer._build_context(pcb)
    # This exercises the actual layer adapter without requesting unused models.
    layer = renderer.component_layers._designators(
        renderer, ctx, pcb, [], "ASSEMBLY_DESIGNATORS_TOP", "top", {}, (),
    )
    entry = next(item for item in layer.metadata["instances"] if item["designator"] == "J1")
    x = sum(ctx.x_to_svg(pad.x_mils) for pad in selected) / len(selected)
    y = sum(ctx.y_to_svg(pad.y_mils) for pad in selected) / len(selected)
    assert entry["center_view_mm"] == pytest.approx((ctx.width_mm - x if mirror else x, y), abs=1e-8)
    assert entry["geometry_source"] == "pads"
    assert entry["font_size_mm"] == pytest.approx(1.6448534)


def test_model_less_pad_selection_retains_plated_holes_and_mechanical_fallback():
    from copy import copy
    pcb = _rt_pcb()
    index = next(i for i, component in enumerate(pcb.components) if component.designator == "J1")
    holes = [pad for pad in pcb.pads if pad.component_index == index and pad.hole_size_mils > 0]
    assert {pad.designator for pad in component_designator_pads(holes, index, "top")} == {"A", "B", "C"}
    assert component_designator_pads([], index, "top") == []
    plated = copy(holes[0])
    plated.is_plated = True
    assert component_designator_pads([plated, *holes[1:]], index, "top") == [plated]


@pytest.mark.parametrize("mirror", [False, True])
def test_designator_stroke_preserves_fit_and_text_fill(mirror):
    from dataclasses import replace
    import xml.etree.ElementTree as ET
    from altium_cruncher.altium_cruncher_pcb_svg_a0_renderer import PcbSvgA0Renderer
    from altium_cruncher.altium_cruncher_pcb_svg_config import PcbSvgConfig

    pcb = _rt_pcb()
    renderer = PcbSvgA0Renderer(PcbSvgConfig.default())
    renderer.options = replace(renderer.options, mirror_x=mirror)
    ctx = renderer._build_context(pcb)
    style = {"color": "#FF0000", "stroke_color": "#FFFFFF", "stroke_width_mm": 0.1}
    def render(style):
        return renderer.component_layers._designators(
            renderer, ctx, pcb, [], "ASSEMBLY_DESIGNATORS_TOP", "top", style, (),
        )
    plain, outlined = render({}), render(style)
    assert outlined.metadata == plain.metadata
    labels = ET.fromstring(outlined.svg).findall(".//{http://www.w3.org/2000/svg}text")
    assert labels
    for text in labels:
        assert text.get("fill") == "#FF0000"
        assert text.get("stroke") == "#FFFFFF"
        assert text.get("stroke-width") == "0.1"
        assert text.get("paint-order") == "stroke fill"
    disabled = render({**style, "stroke_width_mm": 0})
    assert all(text.get("stroke") == "none" for text in ET.fromstring(disabled.svg).findall(".//{http://www.w3.org/2000/svg}text"))
    with pytest.raises(ValueError, match="stroke_width_mm"):
        render({**style, "stroke_width_mm": -0.1})
