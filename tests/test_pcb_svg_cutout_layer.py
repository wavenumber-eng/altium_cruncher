from __future__ import annotations

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
