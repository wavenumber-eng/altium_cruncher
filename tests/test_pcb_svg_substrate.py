"""Substrate composition: opaque exposed board, transparent physical voids."""

from io import BytesIO
from copy import deepcopy
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from altium_monkey.altium_board import AltiumBoard, AltiumBoardOutline, BoardOutlineVertex
from altium_monkey.altium_pcbdoc import AltiumPcbDoc
from altium_monkey.altium_record_pcb__pad import AltiumPcbPad
from altium_monkey.altium_record_pcb__track import AltiumPcbTrack
from altium_monkey.altium_record_pcb__via import AltiumPcbVia
from altium_monkey.altium_record_types import PcbLayer
from jsonschema import Draft202012Validator
from PIL import Image
import pytest

from altium_cruncher.altium_cruncher_pcb_svg_a0_renderer import PcbSvgA0Renderer
from altium_cruncher.altium_cruncher_pcb_svg_config import (
    PcbSvgConfig, PcbSvgViewConfig, parse_pcb_layer_selector,
)
from altium_cruncher.pcb_illustration_config import illustration_preset
from resvg_py import svg_to_bytes

NS = {"s": "http://www.w3.org/2000/svg"}
ROOT = Path(__file__).resolve().parents[1]


def _board():
    pcb = AltiumPcbDoc()
    outline = AltiumBoardOutline.rectangle_mils(
        left_mils=0, bottom_mils=0, right_mils=1000, top_mils=800,
    )
    for left, right in [(400, 600), (500, 700)]:
        outline.cutouts.append([BoardOutlineVertex.line(x, y) for x, y in
                                [(left, 300), (right, 300), (right, 500), (left, 500)]])
    pcb.board = AltiumBoard(outline=outline)
    return pcb


def _render(pcb, *, layers=None, styles=None, config=None, bottom=False):
    config = config or PcbSvgConfig.default()
    config.global_options.clip_to_outline = False  # intrinsic substrate clipping
    view = PcbSvgViewConfig(name="substrate", layers=layers or ["BOARD_SUBSTRATE"], styles=styles or {})
    renderer = PcbSvgA0Renderer(config)
    root = ET.fromstring(renderer.render_view_svg(
        pcb, view, project_parameters=None, layers=view.layers, group_id="substrate",
        mirror=bottom, styles=config.resolved_styles_for_view(view),
    ))
    ctx = renderer._build_context(pcb, project_parameters=None)
    return root, ctx


def _pixels(root, ctx, points, *, bottom=False):
    root = deepcopy(root)
    _, _, width, height = root.get("viewBox").split()
    root.set("width", f"{width}mm")
    root.set("height", f"{height}mm")
    picture = Image.open(BytesIO(svg_to_bytes(
        svg_string=ET.tostring(root, encoding="unicode"), dpi=1016,
    ))).convert("RGBA")
    pixels = []
    for x, y in points:
        sx, sy = ctx.x_to_svg(x), ctx.y_to_svg(y)
        if bottom:
            sx = ctx.width_mm - sx
        pixels.append(picture.getpixel((round(sx * 40), round(sy * 40))))
    return pixels


@pytest.mark.parametrize("bottom", [False, True])
def test_substrate_clips_profile_unions_cutouts_and_removes_actual_holes(bottom):
    pcb = _board()
    pad = AltiumPcbPad()
    pad.layer, pad.x, pad.y, pad.hole_size = PcbLayer.MULTI_LAYER, 1500000, 1500000, 300000
    pad.top_width = pad.top_height = 0  # a physical hole need not have a copper land
    slot = AltiumPcbPad()
    slot.layer, slot.x, slot.y = PcbLayer.MULTI_LAYER, 2500000, 1500000
    slot.hole_size, slot.hole_shape, slot.slot_size = 200000, 2, 800000
    slot.rotation, slot.slot_rotation = 20, 35
    slot.is_plated = False
    pcb.pads = [pad, slot]
    via = AltiumPcbVia()
    via.x, via.y, via.hole_size, via.diameter = 7500000, 1500000, 300000, 600000
    pcb.vias = [via]
    root, ctx = _render(pcb, bottom=bottom)
    points = [(100, 600), (150, 150), (250, 150), (750, 150), (450, 400), (550, 400), (650, 400), (-20, 600)]
    pixels = _pixels(root, ctx, points, bottom=bottom)
    assert pixels[0] == (182, 162, 107, 255)
    assert all(p[3] == 0 for p in pixels[1:])
    group = root.find('.//s:g[@id="layer-BOARD_SUBSTRATE"]', NS)
    assert group.get("data-layer-id") == "9014"
    assert group.get("data-layer-origin") == "synthetic-board-substrate"
    assert group.find('s:path', NS).get('stroke') == 'none'
    slotted = group.find('.//s:path[@stroke-linecap="round"]', NS)
    assert float(slotted.get('stroke-width')) == pytest.approx(.508)
    ids = [e.get('id') for e in root.iter() if e.get('id')]
    assert len(ids) == len(set(ids))


def test_mask_artwork_reveals_substrate_and_view_color_overrides_global():
    pcb = _board()
    track = AltiumPcbTrack()
    track.layer, track.width = PcbLayer.TOP_SOLDER, 100000
    track.start_x, track.end_x = 1000000, 3000000
    track.start_y = track.end_y = 1500000
    pcb.tracks = [track]
    config = PcbSvgConfig.default()
    config.global_options.styles['board_substrate']['color'] = '#112233'
    root, ctx = _render(pcb, config=config,
                        layers=['BOARD_SUBSTRATE', 'SOLDERMASK_FILM_TOP'], styles={
                            'board_substrate': {'color': '#B6A26B'},
                            'soldermask_film': {'color': '#EEEEEE', 'opacity': 1},
                        })
    # Mask artwork exposes opaque substrate, not the transparent canvas.
    assert _pixels(root, ctx, [(200, 150), (200, 200)]) == [(182, 162, 107, 255), (238, 238, 238, 255)]
    assert config.global_options.styles['board_substrate']['color'] == '#112233'
    root, ctx = _render(pcb, config=config)
    assert _pixels(root, ctx, [(200, 150)]) == [(17, 34, 51, 255)]
    disabled, _ = _render(pcb, styles={'board_substrate': {'enabled': False}})
    assert disabled.find('.//s:g[@id="layer-BOARD_SUBSTRATE"]', NS) is None


def test_substrate_via_mouths_follow_selected_outer_surface():
    pcb = _board()
    via = AltiumPcbVia()
    via.x, via.y, via.hole_size, via.diameter = 1500000, 1500000, 300000, 600000
    via.layer_start, via.layer_end = 1, 2  # top blind via
    pcb.vias = [via]
    for layers, count in [(['BOARD_SUBSTRATE'], 0), (['BOARD_SUBSTRATE', 'TOP'], 1), (['BOARD_SUBSTRATE', 'BOTTOM'], 0)]:
        root, _ = _render(pcb, layers=layers)
        assert len(root.findall('.//s:mask[@id="board-substrate-openings"]/s:circle', NS)) == count


def test_substrate_preserves_curved_cutouts_and_requires_outline():
    pcb = AltiumPcbDoc.from_file(ROOT / 'tests/assets/projects/cutouts/input/cutout_multiple.PcbDoc')
    root, _ = _render(pcb)
    cutouts = root.findall('.//s:mask[@id="board-substrate-openings"]/s:path[@fill="black"]', NS)
    assert len(cutouts) == 4
    assert sum('A ' in p.get('d') for p in cutouts) == 3
    with pytest.raises(ValueError, match='BOARD_SUBSTRATE requires a board outline'):
        _render(AltiumPcbDoc())


def test_substrate_contract_presets_and_config_roundtrip():
    schema = json.loads((ROOT / 'docs/contracts/pcb_svg_config.a0.schema.json').read_text())
    validator = Draft202012Validator(schema)
    assert parse_pcb_layer_selector('BOARD_SUBSTRATE,top') == ['BOARD_SUBSTRATE', 'TOP']
    payloads = [illustration_preset()]
    for name in ('board-preview', 'illustration-preview', 'assembly-illustration-preview'):
        payloads.append(json.loads((ROOT / f'examples/pcb-svg/{name}.config.json').read_text()))
    for payload in payloads:
        validator.validate(payload)
        config = PcbSvgConfig.from_dict(payload)
        validator.validate(config.to_dict())
        assert config.global_options.styles['board_substrate']['color'] == '#B6A26B'
        assert all(v.layers[0] == 'BOARD_SUBSTRATE' for v in config.views)
    config = PcbSvgConfig.from_dict({'layer_outputs': {'enabled': True, 'layers': ['BOARD_SUBSTRATE']}})
    assert config.layer_outputs['layers'] == ['BOARD_SUBSTRATE']
