"""Substrate composition: opaque exposed board, transparent physical voids."""

from io import BytesIO
from copy import deepcopy
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from altium_monkey.altium_board import (
    AltiumBoard,
    AltiumBoardOutline,
    BoardOutlineVertex,
)
from altium_monkey.altium_pcbdoc import AltiumPcbDoc
from altium_monkey.altium_record_pcb__pad import AltiumPcbPad
from altium_monkey.altium_record_pcb__track import AltiumPcbTrack
from altium_monkey.altium_record_pcb__via import AltiumPcbVia
from altium_monkey.altium_pcb_enums import PcbIpc4761ViaType
from altium_monkey.altium_record_types import PcbLayer
from jsonschema import Draft202012Validator
from PIL import Image
import pytest

from altium_cruncher.altium_cruncher_pcb_svg_renderer import PcbSvgCompositeRenderer
from altium_cruncher.altium_cruncher_pcb_svg_config import (
    PcbSvgConfig,
    PcbSvgViewConfig,
    parse_pcb_layer_selector,
)
from altium_cruncher.pcb_illustration_config import illustration_preset
from altium_cruncher.altium_cruncher_pcb_svg_substrate import BoardSubstrateRenderer
from resvg_py import svg_to_bytes

NS = {"s": "http://www.w3.org/2000/svg"}
ROOT = Path(__file__).resolve().parents[1]


def _board():
    pcb = AltiumPcbDoc()
    outline = AltiumBoardOutline.rectangle_mils(
        left_mils=0,
        bottom_mils=0,
        right_mils=1000,
        top_mils=800,
    )
    for left, right in [(400, 600), (500, 700)]:
        outline.cutouts.append(
            [
                BoardOutlineVertex.line(x, y)
                for x, y in [(left, 300), (right, 300), (right, 500), (left, 500)]
            ]
        )
    pcb.board = AltiumBoard(outline=outline)
    return pcb


def _render(pcb, *, layers=None, styles=None, config=None, bottom=False):
    config = config or PcbSvgConfig.default()
    config.global_options.clip_to_outline = False  # intrinsic substrate clipping
    view = PcbSvgViewConfig(
        name="substrate", layers=layers or ["BOARD_SUBSTRATE"], styles=styles or {}
    )
    renderer = PcbSvgCompositeRenderer(config)
    root = ET.fromstring(
        renderer.render_view_svg(
            pcb,
            view,
            project_parameters=None,
            layers=view.layers,
            group_id="substrate",
            mirror=bottom,
            styles=config.resolved_styles_for_view(view),
        )
    )
    ctx = renderer._build_context(pcb, project_parameters=None)
    return root, ctx


def _pixels(root, ctx, points, *, bottom=False):
    root = deepcopy(root)
    _, _, width, height = root.get("viewBox").split()
    root.set("width", f"{width}mm")
    root.set("height", f"{height}mm")
    picture = Image.open(
        BytesIO(
            svg_to_bytes(
                svg_string=ET.tostring(root, encoding="unicode"),
                dpi=1016,
            )
        )
    ).convert("RGBA")
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
    pad.layer, pad.x, pad.y, pad.hole_size = (
        PcbLayer.MULTI_LAYER,
        1500000,
        1500000,
        300000,
    )
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
    points = [
        (100, 600),
        (150, 150),
        (250, 150),
        (750, 150),
        (450, 400),
        (550, 400),
        (650, 400),
        (-20, 600),
    ]
    pixels = _pixels(root, ctx, points, bottom=bottom)
    assert pixels[0] == (182, 162, 107, 255)
    assert all(p[3] == 0 for p in pixels[1:])
    group = root.find('.//s:g[@id="layer-BOARD_SUBSTRATE"]', NS)
    assert group.get("data-layer-id") == "9014"
    assert group.get("data-layer-origin") == "synthetic-board-substrate"
    assert group.find("s:path", NS).get("stroke") == "none"
    slotted = group.find('.//s:path[@stroke-linecap="round"]', NS)
    assert float(slotted.get("stroke-width")) == pytest.approx(0.508)
    ids = [e.get("id") for e in root.iter() if e.get("id")]
    assert len(ids) == len(set(ids))


def test_mask_artwork_reveals_substrate_and_view_color_overrides_global():
    pcb = _board()
    track = AltiumPcbTrack()
    track.layer, track.width = PcbLayer.TOP_SOLDER, 100000
    track.start_x, track.end_x = 1000000, 3000000
    track.start_y = track.end_y = 1500000
    pcb.tracks = [track]
    config = PcbSvgConfig.default()
    config.global_options.styles["board_substrate"]["color"] = "#112233"
    root, ctx = _render(
        pcb,
        config=config,
        layers=["BOARD_SUBSTRATE", "SOLDERMASK_FILM_TOP"],
        styles={
            "board_substrate": {"color": "#B6A26B"},
            "soldermask_film": {"color": "#EEEEEE", "opacity": 1},
        },
    )
    # Mask artwork exposes opaque substrate, not the transparent canvas.
    assert _pixels(root, ctx, [(200, 150), (200, 200)]) == [
        (182, 162, 107, 255),
        (238, 238, 238, 255),
    ]
    assert config.global_options.styles["board_substrate"]["color"] == "#112233"
    root, ctx = _render(pcb, config=config)
    assert _pixels(root, ctx, [(200, 150)]) == [(17, 34, 51, 255)]
    disabled, _ = _render(pcb, styles={"board_substrate": {"enabled": False}})
    assert disabled.find('.//s:g[@id="layer-BOARD_SUBSTRATE"]', NS) is None


def test_substrate_via_mouths_follow_selected_outer_surface():
    pcb = _board()
    via = AltiumPcbVia()
    via.x, via.y, via.hole_size, via.diameter = 1500000, 1500000, 300000, 600000
    via.layer_start, via.layer_end = 1, 2  # top blind via
    pcb.vias = [via]
    for layers, count in [
        (["BOARD_SUBSTRATE"], 0),
        (["BOARD_SUBSTRATE", "TOP"], 1),
        (["BOARD_SUBSTRATE", "BOTTOM"], 0),
    ]:
        root, _ = _render(pcb, layers=layers)
        assert (
            len(root.findall('.//s:mask[@id="board-substrate-openings"]/s:circle', NS))
            == count
        )


def test_component_occlusion_domain_uses_side_aware_through_openings():
    pcb = _board()
    plated = AltiumPcbPad()
    plated.layer, plated.x, plated.y, plated.hole_size = (
        PcbLayer.MULTI_LAYER,
        1500000,
        1500000,
        300000,
    )
    plated.is_plated = True
    plated.is_tenting_top = True
    plated.is_tenting_bottom = False
    npth = AltiumPcbPad()
    npth.layer, npth.x, npth.y, npth.hole_size = (
        PcbLayer.MULTI_LAYER,
        2500000,
        1500000,
        300000,
    )
    npth.is_plated = False
    npth.is_tenting_top = npth.is_tenting_bottom = True
    via = AltiumPcbVia()
    via.x, via.y, via.hole_size, via.diameter = 3500000, 1500000, 300000, 600000
    via.is_tent_top, via.is_tent_bottom = True, False
    blind = AltiumPcbVia()
    blind.x, blind.y, blind.hole_size, blind.diameter = (
        7500000,
        1500000,
        300000,
        600000,
    )
    blind.layer_start, blind.layer_end = 1, 2
    pcb.pads, pcb.vias = [plated, npth], [via, blind]

    renderer = PcbSvgCompositeRenderer(PcbSvgConfig.default())
    ctx = renderer._build_context(pcb, project_parameters=None)
    domains = BoardSubstrateRenderer(renderer.options)
    top = domains.occlusion_domain(ctx, pcb, "top")
    bottom = domains.occlusion_domain(ctx, pcb, "bottom")

    # Two routed cutouts plus the NPTH. The plated pad and through via are
    # tented on top, while the blind via never becomes a through-opening.
    assert len(top.openings) == 3
    # Bottom additionally exposes the untented plated pad and through via.
    assert len(bottom.openings) == 5
    mask = top.mask_element(
        ctx,
        "open-space",
        extent=(-5.0, -2.0, ctx.width_mm + 10.0, ctx.height_mm + 4.0),
        complement=True,
    )
    assert mask.get("x") == "-5"
    assert mask.get("y") == "-2"
    assert float(mask.get("width")) > ctx.width_mm
    assert mask.find("s:rect", NS).get("fill") == "white"
    assert mask.find("s:path", NS).get("fill") == "black"
    assert all(
        element.get("fill") != "black" and element.get("stroke") != "black"
        for element in list(mask)[2:]
    )


@pytest.mark.parametrize(
    "via_type",
    [
        PcbIpc4761ViaType.TYPE_3A_PLUGGING,
        PcbIpc4761ViaType.TYPE_3B_PLUGGING,
        PcbIpc4761ViaType.TYPE_4A_PLUGGING_AND_COVERING,
        PcbIpc4761ViaType.TYPE_4B_PLUGGING_AND_COVERING,
        PcbIpc4761ViaType.TYPE_5_FILLING,
        PcbIpc4761ViaType.TYPE_6A_FILLING_AND_COVERING,
        PcbIpc4761ViaType.TYPE_6B_FILLING_AND_COVERING,
        PcbIpc4761ViaType.TYPE_7_FILLING_AND_CAPPING,
    ],
)
@pytest.mark.parametrize("side", ["top", "bottom"])
def test_plugged_filled_and_capped_vias_are_not_physical_openings(via_type, side):
    pcb = _board()
    via = AltiumPcbVia()
    via.x, via.y, via.hole_size, via.diameter = 1500000, 1500000, 300000, 600000
    via.ipc4761_via_type = via_type
    pcb.vias = [via]

    renderer = PcbSvgCompositeRenderer(PcbSvgConfig.default())
    ctx = renderer._build_context(pcb, project_parameters=None)
    domains = BoardSubstrateRenderer(renderer.options)

    # Only the board's two routed cutouts remain. The via is closed in both
    # the physical substrate domain and opposite-side component occlusion.
    assert len(domains.material_domain(ctx, pcb).openings) == 2
    assert len(domains.occlusion_domain(ctx, pcb, side).openings) == 2


@pytest.mark.parametrize("side", ["top", "bottom"])
def test_unfilled_untented_through_via_is_a_physical_opening(side):
    pcb = _board()
    via = AltiumPcbVia()
    via.x, via.y, via.hole_size, via.diameter = 1500000, 1500000, 300000, 600000
    via.ipc4761_via_type = PcbIpc4761ViaType.NONE
    pcb.vias = [via]

    renderer = PcbSvgCompositeRenderer(PcbSvgConfig.default())
    ctx = renderer._build_context(pcb, project_parameters=None)
    domains = BoardSubstrateRenderer(renderer.options)

    assert len(domains.material_domain(ctx, pcb).openings) == 3
    assert len(domains.occlusion_domain(ctx, pcb, side).openings) == 3


def test_substrate_preserves_curved_cutouts_and_requires_outline():
    pcb = AltiumPcbDoc.from_file(
        ROOT / "tests/assets/projects/cutouts/input/cutout_multiple.PcbDoc"
    )
    root, _ = _render(pcb)
    cutouts = root.findall(
        './/s:mask[@id="board-substrate-openings"]/s:path[@fill="black"]', NS
    )
    assert len(cutouts) == 4
    assert sum("A " in p.get("d") for p in cutouts) == 3
    with pytest.raises(ValueError, match="BOARD_SUBSTRATE requires a board outline"):
        _render(AltiumPcbDoc())


def test_substrate_contract_presets_and_config_roundtrip():
    schema = json.loads(
        (ROOT / "docs/contracts/pcb_svg_config.a1.schema.json").read_text()
    )
    validator = Draft202012Validator(schema)
    assert parse_pcb_layer_selector("BOARD_SUBSTRATE,top") == ["BOARD_SUBSTRATE", "TOP"]
    payloads = [illustration_preset()]
    for name in (
        "board-preview",
        "illustration-preview",
        "assembly-illustration-preview",
    ):
        payloads.append(
            json.loads((ROOT / f"examples/pcb-svg/{name}.config.json").read_text())
        )
    for payload in payloads:
        validator.validate(payload)
        config = PcbSvgConfig.from_dict(payload)
        validator.validate(config.to_dict())
        assert config.global_options.styles["board_substrate"]["color"] == "auto"
        assert (
            config.global_options.styles["board_substrate"]["rigid_color"] == "#B6A26B"
        )
        assert (
            config.global_options.styles["board_substrate"]["flex_color"] == "#D18B28"
        )
        assert all(v.layers[0] == "BOARD_SUBSTRATE" for v in config.views)
    config = PcbSvgConfig.from_dict(
        {"layer_outputs": {"enabled": True, "layers": ["BOARD_SUBSTRATE"]}}
    )
    assert config.layer_outputs["layers"] == ["BOARD_SUBSTRATE"]


@pytest.mark.slow
def test_bluetooth_regions_use_saved_rigid_color_amber_flex_and_only_authored_film():
    pcb = AltiumPcbDoc.from_file(
        ROOT
        / "tests/assets/projects/bluetooth_sentinel_flex/input/Bluetooth_Sentinel.PcbDoc"
    )
    root, ctx = _render(
        pcb,
        layers=["BOARD_SUBSTRATE", "SURFACE_COPPER_TOP", "SOLDERMASK_FILM_TOP"],
    )

    # The legacy outline bounding box sees only the flex strip's arc endpoints.
    # Valid split-board regions partition the complete rigid-flex board and must
    # therefore expand the canvas to include both circular rigid lobes.
    view_box = [float(value) for value in root.get("viewBox").split()]
    assert view_box[2:] == pytest.approx([82.0, 57.0], abs=0.001)
    assert (ctx.max_y_mils - ctx.min_y_mils) * 0.0254 == pytest.approx(57.0, abs=0.001)

    surface_copper = root.find('.//s:g[@id="layer-SURFACE_COPPER_TOP"]', NS)
    copper_groups = surface_copper.findall("s:g", NS)
    assert {group.get("data-surface-layer-key") for group in copper_groups} == {
        "L1",
        "L3",
    }
    assert {group.get("data-layer-token") for group in copper_groups} == {"TOP", "MID2"}
    assert all(group.get("clip-path") for group in copper_groups)

    substrate = root.find('.//s:g[@id="layer-BOARD_SUBSTRATE"]', NS)
    substrate_paths = substrate.findall("s:path", NS)
    by_region = {path.get("data-region-name"): path for path in substrate_paths}
    assert set(by_region) == {
        "Layer Stack Region 1",
        "Layer Stack Region 2",
        "Layer Stack Region 3",
    }
    assert by_region["Layer Stack Region 1"].get("fill") == "#D9DBCD"
    assert by_region["Layer Stack Region 2"].get("fill") == "#D9DBCD"
    assert by_region["Layer Stack Region 3"].get("fill") == "#D18B28"
    assert (
        by_region["Layer Stack Region 3"].get("data-substrate-material") == "Polyamide"
    )

    film = root.find('.//s:g[@id="layer-SOLDERMASK_FILM_TOP"]', NS)
    film_paths = film.findall("s:path", NS)
    assert {path.get("data-region-name") for path in film_paths} == {
        "Layer Stack Region 1",
        "Layer Stack Region 2",
    }
    assert {path.get("data-surface-kind") for path in film_paths} == {"solder_mask"}
    assert all(path.get("fill") == "#000000" for path in film_paths)
