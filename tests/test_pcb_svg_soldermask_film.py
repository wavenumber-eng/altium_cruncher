from __future__ import annotations

from pathlib import Path
from copy import deepcopy
from io import BytesIO
import json
import xml.etree.ElementTree as ET

import pytest
from jsonschema import Draft202012Validator
from altium_monkey.altium_board import (
    AltiumBoard,
    AltiumBoardOutline,
    BoardOutlineVertex,
)
from altium_monkey.altium_pcbdoc import AltiumPcbDoc
from altium_monkey.altium_pcb_custom_shapes import AltiumPcbCustomPadShape
from altium_monkey.altium_pcb_extended_primitive_information import (
    build_mask_expansion_extended_primitive_information,
)
from altium_monkey.altium_pcb_rule import AltiumPcbRule
from altium_monkey.altium_record_pcb__arc import AltiumPcbArc
from altium_monkey.altium_record_pcb__fill import AltiumPcbFill
from altium_monkey.altium_record_pcb__pad import AltiumPcbPad
from altium_monkey.altium_record_pcb__region import AltiumPcbRegion, RegionVertex
from altium_monkey.altium_record_pcb__track import AltiumPcbTrack
from altium_monkey.altium_record_pcb__via import AltiumPcbVia
from altium_monkey.altium_record_types import PcbLayer

from altium_cruncher.altium_cruncher_pcb_svg_a0_renderer import PcbSvgA0Renderer
from altium_cruncher.altium_cruncher_pcb_svg_config import (
    PcbSvgConfig,
    PcbSvgViewConfig,
)
from altium_cruncher.altium_cruncher_pcb_svg_soldermask_film import (
    saved_soldermask_color,
)
from resvg_py import svg_to_bytes

NS = {"s": "http://www.w3.org/2000/svg"}
ROOT = Path(__file__).resolve().parents[1]


def _board() -> AltiumPcbDoc:
    pcb = AltiumPcbDoc()
    outline = AltiumBoardOutline.rectangle_mils(
        left_mils=0,
        bottom_mils=0,
        right_mils=1000,
        top_mils=800,
    )
    outline.cutouts.append(
        [
            BoardOutlineVertex.line(x, y)
            for x, y in [(300, 300), (500, 300), (500, 500), (300, 500)]
        ]
    )
    pcb.board = AltiumBoard(outline=outline)
    return pcb


def _render(
    pcb: AltiumPcbDoc,
    *,
    bottom: bool = False,
    config: PcbSvgConfig | None = None,
    style: dict[str, object] | None = None,
    extra_layers: list[str] | None = None,
) -> ET.Element:
    config = config or PcbSvgConfig.default()
    # Film clipping is intrinsic even when general layer clipping is disabled.
    config.global_options.clip_to_outline = False
    token = "SOLDERMASK_FILM_BOTTOM" if bottom else "SOLDERMASK_FILM_TOP"
    view = PcbSvgViewConfig(
        name="film",
        layers=[token, *(extra_layers or [])],
        styles={"soldermask_film": style or {}},
    )
    return ET.fromstring(
        PcbSvgA0Renderer(config).render_view_svg(
            pcb,
            view,
            project_parameters=None,
            layers=view.layers,
            group_id="film",
            mirror=bottom,
            styles=config.resolved_styles_for_view(view),
        )
    )


def _pad(x_mils: int = 150, expansion: int = 100000) -> AltiumPcbPad:
    pad = AltiumPcbPad()
    pad.layer = PcbLayer.TOP
    pad.x = x_mils * 10000
    pad.y = 1500000
    pad.top_width = pad.top_height = 1000000
    pad._has_mask_expansion = True
    pad.soldermask_expansion_mode = 2
    pad.soldermask_expansion_manual = expansion
    return pad


def test_saved_color_and_config_overrides() -> None:
    pcb = _board()
    pcb.board.raw_record["3DCONFIGURATION"] = (
        "`CFG3D.TOPSOLDERMASKCOLOR=3351057`CFG3D.BOTSOLDERMASKCOLOR=0"
    )
    assert saved_soldermask_color(pcb, "top") == "#112233"
    assert saved_soldermask_color(pcb, "bottom") == "#000000"
    assert (
        _render(pcb)
        .find(".//s:g[@id='layer-SOLDERMASK_FILM_TOP']/s:path", NS)
        .get("fill")
        == "#112233"
    )
    assert (
        _render(pcb, bottom=True)
        .find(".//s:g[@id='layer-SOLDERMASK_FILM_BOTTOM']/s:path", NS)
        .get("fill")
        == "#000000"
    )
    config = PcbSvgConfig.default()
    config.global_options.styles["soldermask_film"].update(color="#123456", opacity=0.8)
    root = _render(pcb, config=config, style={"opacity": 0.35})
    painted = root.find(".//s:g[@id='layer-SOLDERMASK_FILM_TOP']/s:path", NS)
    assert painted.get("fill") == "#123456"
    assert painted.get("opacity") == "0.35"
    pcb.board.raw_record["3DCONFIGURATION"] = "`CFG3D.TOPSOLDERMASKCOLOR=invalid"
    assert saved_soldermask_color(pcb, "top") is None
    assert (
        _render(pcb)
        .find(".//s:g[@id='layer-SOLDERMASK_FILM_TOP']/s:path", NS)
        .get("fill")
        == "#176B3A"
    )


def test_film_uses_cutouts_and_unions_overlapping_expanded_openings() -> None:
    pcb = _board()
    # The first two apertures overlap; independent black paint must subtract both.
    pcb.pads = [_pad(150), _pad(180), _pad(600, -100000), _pad(700, -600000)]
    pcb.pads[1].soldermask_expansion_mode = 1  # saved rule expansion, same geometry
    # A second cutout overlaps the first and crosses the board edge.
    pcb.board.outline.cutouts.append(
        [
            BoardOutlineVertex.line(x, y)
            for x, y in [(400, 400), (1100, 400), (1100, 900), (400, 900)]
        ]
    )
    root = _render(pcb, extra_layers=["TOP_SOLDER"])
    mask = root.find(".//s:mask[@id='soldermask-film-openings-top']", NS)
    domain = mask.find("s:path", NS)
    assert domain.get("fill-rule") == "evenodd"
    assert domain.get("d").count("M ") == 1
    cutouts = [e for e in mask.findall("s:path", NS) if e.get("fill") == "black"]
    assert len(cutouts) == 2
    painted = root.find(".//s:g[@id='layer-SOLDERMASK_FILM_TOP']/s:path", NS)
    assert painted.get("d") == domain.get(
        "d"
    )  # fill never extends outside outer profile
    openings = mask.findall("s:ellipse", NS)
    assert len(openings) == 3  # fourth has a fully collapsed negative expansion
    assert [float(e.get("rx")) for e in openings] == pytest.approx(
        [1.524, 1.524, 1.016]
    )
    assert all(e.get("fill") == "black" for e in openings)
    ids = [e.get("id") for e in root.iter() if e.get("id")]
    assert len(ids) == len(set(ids))
    assert root.find(".//s:g[@data-layer-id='9010']", NS) is not None


@pytest.mark.parametrize("scope, expected", [("all", 4), ("interior", 1)])
def test_cutout_scope_agrees_in_copper_clip_film_and_artwork(scope, expected) -> None:
    pcb = _board()
    for left, right in [(0, 100), (900, 1100), (1100, 1200)]:
        # Boundary-touching, boundary-crossing and wholly exterior cutouts.
        pcb.board.outline.cutouts.append(
            [
                BoardOutlineVertex.line(x, y)
                for x, y in [(left, 100), (right, 100), (right, 200), (left, 200)]
            ]
        )
    source_cutouts = list(pcb.board.outline.cutouts)
    config = PcbSvgConfig.default()
    view = PcbSvgViewConfig(
        name="scope",
        layers=["TOP", "SOLDERMASK_FILM_TOP", "BOARD_CUTOUTS"],
        styles={"board_cutouts": {"scope": scope, "hatch": False}},
    )
    root = ET.fromstring(
        PcbSvgA0Renderer(config).render_view_svg(
            pcb, view, project_parameters=None, layers=view.layers,
            group_id="scope", mirror=False,
            styles=config.resolved_styles_for_view(view),
        )
    )
    clip = root.find(".//s:clipPath/s:path", NS)
    film = root.find(".//s:mask[@id='soldermask-film-openings-top']", NS)
    assert clip.get("d").count("M ") == expected + 1
    assert len([e for e in film if e.get("fill") == "black"]) == expected
    assert len(root.findall(".//s:path[@data-feature='board-cutout']", NS)) == expected
    assert pcb.board.outline.cutouts == source_cutouts


def test_tenting_np_through_slots_and_via_hole_edge_expansion() -> None:
    pcb = _board()
    tented = _pad()
    tented.is_tenting_top = True
    slot = _pad(250, -1000000)
    slot.layer = PcbLayer.MULTI_LAYER
    slot.is_plated = False
    slot.hole_size = 300000
    slot.hole_shape = 2
    slot.slot_size = 800000
    slot.slot_rotation = 30
    pcb.pads = [tented, slot]
    via = AltiumPcbVia()
    via.x = 6500000
    via.y = 6500000
    via.diameter = 600000
    via.hole_size = 200000
    via.soldermask_expansion_from_hole_edge = True
    via._has_soldermask_expansion_front = via._has_soldermask_expansion_back = True
    via.solder_mask_expansion_mode = 2
    via.soldermask_expansion_front = 50000
    via.soldermask_expansion_back = 100000
    pcb.vias = [via]
    mask = _render(pcb).find(".//s:mask", NS)
    assert not mask.findall("s:ellipse", NS)  # tented SMD and collapsed slot land
    assert float(mask.find("s:circle", NS).get("r")) == pytest.approx(0.381)
    slot_path = next(
        p for p in mask.findall("s:path", NS) if p.get("stroke") == "black"
    )
    assert float(slot_path.get("stroke-width")) == pytest.approx(0.762)
    assert slot_path.get("stroke-linecap") == "round"
    via.is_tent_top = True
    assert not _render(pcb).findall(".//s:mask/s:circle", NS)
    bottom = _render(pcb, bottom=True)
    assert float(bottom.find(".//s:mask/s:circle", NS).get("r")) == pytest.approx(0.508)
    via.is_tent_top = False
    via.layer_start = 2  # buried from the top side
    assert not _render(pcb).findall(".//s:mask/s:circle", NS)
    assert via.diameter == 600000  # rendering must not alter source records


@pytest.mark.parametrize("opacity", [-0.1, 1.1, float("nan"), True])
def test_invalid_opacity_is_rejected(opacity: object) -> None:
    with pytest.raises(ValueError, match="soldermask_film.opacity"):
        _render(_board(), style={"opacity": opacity})


def test_rt_saved_white_color_and_tented_vias() -> None:
    pcb = AltiumPcbDoc.from_file(
        ROOT / "tests/assets/projects/rt_super_c1/input/RT_SUPER_C1.PCBdoc"
    )
    assert saved_soldermask_color(pcb, "top") == "#FFFFFF"
    assert saved_soldermask_color(pcb, "bottom") == "#FFFFFF"
    assert all(v.is_tent_top and v.is_tent_bottom for v in pcb.vias)
    root = _render(pcb)
    # Every circular knockout here is one of the three NPTH pogo-connector bores.
    assert len(root.findall(".//s:mask/s:circle", NS)) == 3
    assert (
        root.find(".//s:g[@id='layer-SOLDERMASK_FILM_TOP']/s:path", NS).get("fill")
        == "#FFFFFF"
    )


@pytest.mark.parametrize(
    "filename", ["soldermask-film.config.json", "drill-preview.config.json"]
)
def test_film_example_config_matches_contract(filename: str) -> None:
    payload = json.loads((ROOT / "examples/pcb-svg" / filename).read_text())
    schema = json.loads(
        (ROOT / "docs/contracts/pcb_svg_config.a0.schema.json").read_text()
    )
    validator = Draft202012Validator(schema)
    validator.validate(payload)
    config = PcbSvgConfig.from_dict(payload)
    validator.validate(config.to_dict())
    assert config.views[0].layers[0] == "SOLDERMASK_FILM_TOP"
    assert config.views[1].layers[0] == "SOLDERMASK_FILM_BOTTOM"


def _hole_config() -> PcbSvgConfig:
    return PcbSvgConfig.from_dict(
        json.loads((ROOT / "examples/pcb-svg/drill-preview.config.json").read_text())
    )


def test_rt_film_drill_outlines_use_actual_holes_without_copper_layer() -> None:
    pcb = AltiumPcbDoc.from_file(
        ROOT / "tests/assets/projects/rt_super_c1/input/RT_SUPER_C1.PCBdoc"
    )
    config = _hole_config()
    root = _render(pcb, config=config, extra_layers=["DRILLS", "SLOTS"])
    holes = root.findall(".//s:g[@id='layer-DRILLS']/s:circle", NS)
    assert len(holes) == 83
    assert sorted(float(e.get("r")) for e in holes) == pytest.approx(
        sorted([0.3556] * 76 + [0.889] * 4 + [0.4445] * 3)
    )
    assert all(e.get("fill") == "none" and e.get("stroke") == "#000000" for e in holes)
    assert all(float(e.get("stroke-width")) == 0.025 for e in holes)
    assert root.find(".//s:g[@id='layer-TOP']", NS) is None
    mixed = _render(pcb, config=config, extra_layers=["MID1", "DRILLS"])
    assert len(mixed.findall(".//s:g[@id='layer-DRILLS']/s:circle", NS)) == 83
    # Existing filled drill mode is still available; tenting policy is opt-in.
    config.global_options.styles["drills"].update(outline=False, respect_tenting=False)
    all_holes = _render(pcb, config=config, extra_layers=["DRILLS"]).findall(
        ".//s:g[@id='layer-DRILLS']/s:circle", NS
    )
    assert (
        len(all_holes) == 199
    )  # 83 pad holes + 116 unfilled via bores; 91 are filled/capped
    assert all(e.get("fill") == "#000000" for e in all_holes)


def test_slot_outline_keeps_source_size_and_combined_rotation() -> None:
    pcb = _board()
    slot = _pad()
    slot.layer = PcbLayer.MULTI_LAYER
    slot.is_plated = True
    slot.hole_shape = 2
    slot.hole_size = 300000
    slot.slot_size = 800000
    slot.rotation = 20
    slot.slot_rotation = 35
    pcb.pads = [slot]
    config = _hole_config()
    root = _render(pcb, config=config, extra_layers=["SLOTS"])
    rect = root.find(".//s:g[@id='layer-SLOTS']/s:rect", NS)
    assert float(rect.get("width")) == pytest.approx(2.032)
    assert float(rect.get("height")) == pytest.approx(0.762)
    assert float(rect.get("rx")) == pytest.approx(0.381)
    assert rect.get("transform").startswith("rotate(-55 ")
    assert rect.get("fill") == "none"
    slot.is_tenting_top = True
    assert (
        _render(pcb, config=config, extra_layers=["SLOTS"]).find(
            ".//s:g[@id='layer-SLOTS']", NS
        )
        is None
    )
    assert (
        _render(pcb, bottom=True, config=config, extra_layers=["SLOTS"]).find(
            ".//s:g[@id='layer-SLOTS']", NS
        )
        is not None
    )
    slot.is_plated = False  # an NPTH remains open regardless of mask tenting flags
    assert (
        _render(pcb, config=config, extra_layers=["SLOTS"]).find(
            ".//s:g[@id='layer-SLOTS']", NS
        )
        is not None
    )


def test_real_cutouts_preserve_arcs_in_film_and_visible_edges() -> None:
    pcb = AltiumPcbDoc.from_file(
        ROOT / "tests/assets/projects/cutouts/input/cutout_multiple.PcbDoc"
    )
    root = _render(pcb, config=_hole_config(), extra_layers=["BOARD_CUTOUTS"])
    cuts = [e for e in root.findall(".//s:mask/s:path", NS) if e.get("fill") == "black"]
    assert len(cuts) == 4
    assert sum("A " in e.get("d") for e in cuts) == 3
    # Outlines and film knockouts share the same source path; no hatching covers the voids.
    visible = [e for e in root.findall(".//s:path", NS) if e.get("stroke") == "#000000"]
    assert len(visible) == 4
    assert {e.get("d") for e in visible} == {e.get("d") for e in cuts}
    assert all(e.get("fill") == "none" for e in visible)


def _region(points, *, holes=(), layer=PcbLayer.TOP):
    region = AltiumPcbRegion()
    region.layer = layer
    region.outline_vertices = [RegionVertex(x * 10000, y * 10000) for x, y in points]
    region.hole_vertices = [
        [RegionVertex(x * 10000, y * 10000) for x, y in hole] for hole in holes
    ]
    return region


def _mask_info(kind, expansion=10, *, mode="Manual", index=0):
    info = build_mask_expansion_extended_primitive_information(
        primitive_index=index, primitive_object_id=kind,
        solder_mask_expansion_mils=expansion,
    )
    info.solder_mask_expansion_mode = mode
    return info


def _rule(expansion="4mil", scope="All", priority=1, **extra):
    return AltiumPcbRule.from_record({
        "RULEKIND": "SolderMaskExpansion", "NAME": scope,
        "SCOPE1EXPRESSION": scope, "SCOPE2EXPRESSION": "All",
        "ENABLED": "TRUE", "PRIORITY": priority, "EXPANSION": expansion,
        **extra,
    })


def _film_alpha(pcb, root, points):
    """Independently rasterize the SVG film for interior-point assertions."""
    from PIL import Image

    ctx = PcbSvgA0Renderer(PcbSvgConfig.default())._build_context(
        pcb, project_parameters=None,
    )
    coords = [(ctx.x_to_svg(x), ctx.y_to_svg(y)) for x, y in points]
    # Crop the SVG viewport for fast, detailed checks even on a full fixture board.
    left = min(x for x, y in coords) - 1
    top = min(y for x, y in coords) - 1
    width = max(x for x, y in coords) - left + 1
    height = max(y for x, y in coords) - top + 1
    root = deepcopy(root)
    root.set("viewBox", f"{left} {top} {width} {height}")
    root.set("width", f"{width}mm")
    root.set("height", f"{height}mm")
    png = svg_to_bytes(svg_string=ET.tostring(root, encoding="unicode"), dpi=2540)
    with Image.open(BytesIO(png)) as image:
        alpha = image.convert("RGBA").getchannel("A")
        return [alpha.getpixel((round((x-left)*100), round((y-top)*100))) for x, y in coords]


def test_hydroscope_u13_region_opens_center_land_with_board_rule() -> None:
    pcb = AltiumPcbDoc.from_file(
        ROOT / "tests/assets/projects/hydroscope/input/TZ-SB-0001-PCB-[A] (HydroScope Mainboard).PcbDoc"
    )
    region = pcb.regions[2]
    assert pcb.components[region.component_index].designator == "U13"
    assert len(region.outline_vertices) == 8
    root = _render(pcb)
    opening = next(p for p in root.findall(".//s:mask/s:path", NS)
                   if p.get("stroke-width") == "0.2032")
    assert opening.get("fill") == "black"
    assert opening.get("stroke-linejoin") == "round"
    # Outside rectangular pad 2: land interior, the 4 mil expansion, and film.
    assert _film_alpha(pcb, root, [(27410, 18943), (27436, 18943), (27444, 18943)]) == [0, 0, 255]
    pcb.extended_primitive_information = []
    assert _film_alpha(pcb, _render(pcb), [(27410, 18943)]) == [255]


@pytest.mark.parametrize("expansion, expected", [
    (10, [0, 0, 0, 255]), (0, [255, 0, 255, 255]),
    (-10, [255, 255, 255, 255]), (-60, [255, 255, 255, 255]),
])
def test_region_expansion_preserves_holes_and_does_not_open_unmarked_copper(expansion, expected):
    pcb = _board()
    pcb.regions = [
        _region([(100, 100), (200, 100), (200, 250), (100, 250)],
                holes=[[(130, 140), (170, 140), (170, 210), (130, 210)]]),
        _region([(600, 100), (700, 100), (700, 250), (600, 250)]),
    ]
    pcb.extended_primitive_information = [_mask_info("Region", expansion)]
    root = _render(pcb)
    assert _film_alpha(pcb, root, [(95, 120), (105, 120), (133, 175), (650, 175)]) == expected
    assert _film_alpha(pcb, root, [(150, 175)]) == [255]  # central hole stays masked


@pytest.mark.parametrize("kind", ["Track", "Arc"])
@pytest.mark.parametrize("expansion", [10, 0, -5, -10, -20])
def test_track_and_arc_expansion_and_collapse(kind, expansion):
    pcb = _board()
    if kind == "Track":
        primitive = AltiumPcbTrack()
        primitive.start_x, primitive.start_y = 1000000, 1000000
        primitive.end_x, primitive.end_y = 2000000, 1000000
        pcb.tracks = [primitive]
    else:
        primitive = AltiumPcbArc()
        primitive.center_x = primitive.center_y = 1500000
        primitive.radius = 500000
        primitive.start_angle, primitive.end_angle = 0, 270
        pcb.arcs = [primitive]
    primitive.layer, primitive.width = PcbLayer.TOP, 200000
    pcb.extended_primitive_information = [_mask_info(kind, expansion)]
    mask = _render(pcb).find(".//s:mask", NS)
    stroked = [p for p in mask if p.get("stroke") == "black"]
    assert len(stroked) == (1 if expansion > -10 else 0)
    if stroked:
        assert float(stroked[0].get("stroke-width")) == pytest.approx((20 + 2*expansion) * .0254)
        assert stroked[0].get("stroke-linecap") == "round"
        if kind == "Arc":
            assert "A " in stroked[0].get("d")
    assert primitive.width == 200000  # no source mutation
    assert not [p for p in _render(pcb, bottom=True).find(".//s:mask", NS)
                if p.get("stroke") == "black"]


def test_rotated_fill_negative_expansion_and_overlapping_apertures():
    pcb = _board()
    fill = AltiumPcbFill()
    fill.layer, fill.rotation = PcbLayer.TOP, 45
    fill.pos1_x = fill.pos1_y = 1000000
    fill.pos2_x = fill.pos2_y = 2000000
    pcb.fills = [fill]
    pcb.extended_primitive_information = [_mask_info("Fill", -10)]
    assert _film_alpha(pcb, _render(pcb), [(150, 150), (150, 85), (150, 100)]) == [0, 255, 0]
    # The erosion mask cannot put film back over an overlapping pad aperture.
    pcb.pads = [_pad(150, 100000)]
    assert _film_alpha(pcb, _render(pcb), [(150, 95)]) == [0]
    # A rotated fill can enter the board even when its local contour crosses the
    # SVG canvas edge; the private erosion mask must not clip that contour early.
    pcb.pads = []
    fill.pos1_x, fill.pos2_x = -2800000, 1200000
    fill.pos1_y, fill.pos2_y = 0, 4000000
    assert _film_alpha(pcb, _render(pcb), [(26, 59)]) == [0]


def test_rule_priority_side_expansions_none_and_unresolved_queries(caplog):
    pcb = _board()
    pcb.regions = [_region([(100, 100), (200, 100), (200, 200), (100, 200)])]
    info = _mask_info("Region", mode="Rule")
    pcb.extended_primitive_information = [info]
    pcb.rules = [_rule(), _rule("8mil", "IsRegion", 0, USESEPARATEEXPANSIONS="TRUE", EXPANSIONBOTTOM="12mil")]
    assert _render(pcb).find(".//s:mask/s:path[@stroke='black']", NS).get("stroke-width") == "0.4064"
    pcb.regions[0].layer = PcbLayer.BOTTOM
    assert _render(pcb, bottom=True).find(".//s:mask/s:path[@stroke='black']", NS).get("stroke-width") == "0.6096"
    pcb.rules[1].is_tenting_bottom = True
    assert _render(pcb, bottom=True).find(".//s:mask/s:path[@stroke='black']", NS) is None
    pcb.regions[0].layer = PcbLayer.TOP
    pcb.rules[1].enabled = False
    assert _render(pcb).find(".//s:mask/s:path[@stroke='black']", NS).get("stroke-width") == "0.2032"
    pcb.rules.append(_rule("20mil", "InComponent('U13')", 0))
    assert _render(pcb).find(".//s:mask/s:path[@stroke='black']", NS) is None
    assert "cannot resolve rule" in caplog.text
    info.solder_mask_expansion_mode = "None"
    caplog.clear()
    assert _render(pcb).find(".//s:mask/s:path[@stroke='black']", NS) is None
    assert "cannot resolve rule" not in caplog.text


def test_custom_pad_uses_contour_instead_of_tiny_anchor_and_prefers_saved_mask():
    pcb = _board()
    pad = _pad(150, 100000)
    pad.top_width = pad.top_height = 10000  # custom pad's tiny anchor
    copper = _region([(100, 100), (200, 100), (200, 200), (100, 200)])
    pad.custom_shape = AltiumPcbCustomPadShape(source="test", anchor_pad_index=0)
    pad.custom_shape.add_layer_shape(layer=1, shape_kind=0, source_record=None, region=copper)
    pcb.pads, pcb.regions = [pad], [copper]
    assert _film_alpha(pcb, _render(pcb), [(105, 150), (95, 150), (85, 150)]) == [0, 0, 255]
    pad.is_tenting_top = True
    assert _film_alpha(pcb, _render(pcb), [(105, 150)]) == [255]
    pad.is_tenting_top = False
    saved = _region([(100, 100), (180, 100), (180, 200), (100, 200)], layer=PcbLayer.TOP_SOLDER)
    pcb.regions.append(saved)
    pad.custom_shape.add_layer_shape(layer=37, shape_kind=0, source_record=None, region=saved)
    assert _film_alpha(pcb, _render(pcb), [(105, 150), (95, 150), (190, 150)]) == [0, 255, 255]
