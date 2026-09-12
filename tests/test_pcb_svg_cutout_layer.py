from __future__ import annotations

import xml.etree.ElementTree as ET

import pytest
from altium_monkey.altium_board import (
    AltiumBoard,
    AltiumBoardOutline,
    BoardOutlineVertex,
)
from altium_monkey.altium_pcb_svg_renderer import PcbSvgRenderOptions
from altium_monkey.altium_pcbdoc import AltiumPcbDoc
from altium_monkey.altium_record_types import PcbLayer

from altium_cruncher.altium_cruncher_pcb_svg_cutout_layer import (
    CruncherPcbCutoutLayerRenderer,
    CruncherPcbCutoutStyle,
)


def _pcbdoc_with_cutout() -> AltiumPcbDoc:
    pcbdoc = AltiumPcbDoc()
    outline = AltiumBoardOutline.rectangle_mils(
        left_mils=0.0,
        bottom_mils=0.0,
        right_mils=1000.0,
        top_mils=800.0,
    )
    outline.cutouts.append(
        [
            BoardOutlineVertex.line(300.0, 300.0),
            BoardOutlineVertex.line(500.0, 300.0),
            BoardOutlineVertex.line(500.0, 500.0),
            BoardOutlineVertex.line(300.0, 500.0),
        ]
    )
    pcbdoc.board = AltiumBoard(outline=outline)
    return pcbdoc


def test_cutout_layer_renderer_emits_hatched_labeled_cutouts() -> None:
    renderer = CruncherPcbCutoutLayerRenderer(
        PcbSvgRenderOptions(
            include_metadata=True,
            board_cutout_color="#FF0000",
        )
    )

    svg = renderer.render_board_cutout_layer(
        _pcbdoc_with_cutout(),
        include_hatch=True,
        include_label=True,
        label_text="cutout",
    )

    assert svg is not None
    assert 'data-layer-key="BOARD_CUTOUTS"' in svg
    assert 'id="board-cutout-hatch"' in svg
    assert 'data-feature="board-cutout"' in svg
    assert 'data-feature="board-cutout-label"' in svg
    assert ">cutout</text>" in svg


def test_cutout_layer_renderer_honors_hash_and_outline_options() -> None:
    renderer = CruncherPcbCutoutLayerRenderer(
        PcbSvgRenderOptions(
            include_metadata=True,
            board_cutout_color="#FF0000",
        )
    )

    svg = renderer.render_board_cutout_layer(
        _pcbdoc_with_cutout(),
        include_hatch=True,
        hatch_spacing_mm=1.25,
        hatch_angle_deg=30.0,
        hatch_line_width_mm=0.12,
        outline_style="dashed",
        outline_dash_mm=0.9,
        outline_width_mm=0.33,
    )

    assert svg is not None
    assert 'width="1.25" height="1.25"' in svg
    assert 'patternTransform="rotate(30)"' in svg
    assert 'stroke-width="0.12"' in svg
    assert 'stroke-dasharray="0.9 0.9"' in svg
    assert 'stroke-width="0.33"' in svg
    assert 'data-outline-style="dashed"' in svg


def test_cutout_layer_renderer_obeys_board_outline_option() -> None:
    renderer = CruncherPcbCutoutLayerRenderer(
        PcbSvgRenderOptions(
            include_metadata=True,
            board_outline_color="#000000",
            board_cutout_color="#FF0000",
        )
    )

    with_outline = renderer.render_board_cutout_layer(
        _pcbdoc_with_cutout(),
        include_board_outline=True,
    )
    without_outline = renderer.render_board_cutout_layer(
        _pcbdoc_with_cutout(),
        include_board_outline=False,
    )

    assert with_outline is not None
    assert without_outline is not None
    assert 'data-feature="board-outline"' in with_outline
    assert 'data-feature="board-outline"' not in without_outline
    assert with_outline.count('data-feature="board-cutout"') == 1
    assert without_outline.count('data-feature="board-cutout"') == 1


def test_cutout_overlay_inherits_hash_style_for_composed_view() -> None:
    renderer = CruncherPcbCutoutLayerRenderer(
        PcbSvgRenderOptions(
            visible_layers={PcbLayer.TOP},
            include_metadata=True,
            show_board_outline=True,
            board_cutout_color="#FF0000",
        ),
        cutout_style=CruncherPcbCutoutStyle(
            include_overlay=True,
            include_hatch=True,
            hatch_spacing_mm=1.25,
            hatch_angle_deg=30.0,
            hatch_line_width_mm=0.12,
            outline_style="dashed",
            outline_dash_mm=0.9,
            outline_width_mm=0.33,
        ),
    )

    svg = renderer.render_board(_pcbdoc_with_cutout())

    assert 'id="board-cutout-hatch"' in svg
    assert 'width="1.25" height="1.25"' in svg
    assert 'patternTransform="rotate(30)"' in svg
    assert 'stroke-width="0.12"' in svg
    assert 'stroke-dasharray="0.9 0.9"' in svg
    assert 'stroke-width="0.33"' in svg


def test_cutout_layer_renderer_skips_boards_without_cutouts() -> None:
    pcbdoc = AltiumPcbDoc()
    pcbdoc.board = AltiumBoard(
        outline=AltiumBoardOutline.rectangle_mils(
            left_mils=0.0,
            bottom_mils=0.0,
            right_mils=1000.0,
            top_mils=800.0,
        )
    )
    renderer = CruncherPcbCutoutLayerRenderer(PcbSvgRenderOptions())

    assert renderer.render_board_cutout_layer(pcbdoc) is None


@pytest.mark.parametrize("bottom", [False, True])
def test_autodoc_cutout_styles_fit_labels_and_keep_bottom_text_readable(bottom, tmp_path) -> None:
    from altium_cruncher.altium_cruncher_pcb_svg_a0_renderer import (
        PcbSvgA0Renderer,
        write_or_update_view_svg,
    )
    from altium_cruncher.altium_cruncher_pcb_svg_config import PcbSvgConfig, PcbSvgViewConfig

    pcb = _pcbdoc_with_cutout()
    for width in (100, 1):
        pcb.board.outline.cutouts.append([
            BoardOutlineVertex.line(x, y)
            for x, y in [(600, 100), (600 + width, 100), (600 + width, 700), (600, 700)]
        ])
    style = {
        "color": "#555555", "outline_opacity": 0.25,
        "hatch": True, "hatch_color": "#777777", "hatch_opacity": 0.18,
        "hatch_spacing_mm": 1.0, "hatch_line_width_mm": 0.12,
        "label": "CUTOUT", "label_color": "#444444", "label_opacity": 0.35,
    }
    view = PcbSvgViewConfig(name="cutouts", layers=["BOARD_CUTOUTS"], styles={"board_cutouts": style})
    config = PcbSvgConfig.default()
    svg = PcbSvgA0Renderer(config).render_view_svg(
        pcb, view, project_parameters=None, layers=view.layers,
        group_id="cutouts", mirror=bottom, styles=config.resolved_styles_for_view(view),
    )
    root = ET.fromstring(svg)
    ns = {"s": "http://www.w3.org/2000/svg"}
    paths = root.findall(".//s:path[@data-feature='board-cutout']", ns)
    assert len(paths) == 3
    assert all(p.get("stroke") == "#555555" and p.get("stroke-opacity") == "0.25" for p in paths)
    hatch = root.find(".//s:pattern/s:line", ns)
    assert hatch.get("stroke") == "#777777"
    assert hatch.get("opacity") == "0.18"
    labels = root.findall(".//s:text[@data-feature='board-cutout-label']", ns)
    assert len(labels) == 2  # Reference skips labels smaller than 0.2 mm.
    assert all(t.text == "CUTOUT" and t.get("fill-opacity") == "0.35" for t in labels)
    assert float(labels[1].get("font-size")) == pytest.approx(1.8288, abs=0.003)  # 12-step silhouette fit, then SVG rounding
    assert labels[1].get("transform").startswith("rotate(-90 ")
    wrappers = root.findall(".//s:g[@data-feature='board-cutout-label-orientation']", ns)
    assert len(wrappers) == (2 if bottom else 0)
    if bottom:
        assert all("scale(-1 1)" in w.get("transform") for w in wrappers)
    target = tmp_path / "cutouts.svg"
    write_or_update_view_svg(target, svg, group_id="cutouts")
    write_or_update_view_svg(target, svg, group_id="cutouts")
    refreshed = ET.parse(target).getroot()
    assert len(refreshed.findall(".//s:text[@data-feature='board-cutout-label']", ns)) == 2


@pytest.mark.parametrize("field, value", [
    ("outline_opacity", 2), ("hatch_opacity", -0.1), ("label_opacity", -1),
    ("label_fill_ratio", 2), ("label_fill_ratio", 0),
    ("label_max_font_size_mm", float("inf")), ("label_max_font_size_mm", -1),
])
def test_cutout_presentation_rejects_invalid_values_on_render(field, value) -> None:
    from altium_cruncher.altium_cruncher_pcb_svg_a0_renderer import PcbSvgA0Renderer
    from altium_cruncher.altium_cruncher_pcb_svg_config import PcbSvgConfig, PcbSvgViewConfig

    config = PcbSvgConfig.default()
    view = PcbSvgViewConfig(name="cutouts", layers=["BOARD_CUTOUTS"])
    styles = config.resolved_styles_for_view(view)
    styles["board_cutouts"][field] = value
    with pytest.raises(ValueError, match=f"board_cutouts.{field}"):
        PcbSvgA0Renderer(config).render_view_svg(
            _pcbdoc_with_cutout(), view, project_parameters=None, layers=view.layers,
            group_id="cutouts", mirror=False, styles=styles,
        )
