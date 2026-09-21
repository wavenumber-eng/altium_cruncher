"""Flat rigid-flex bend-line virtual-layer coverage."""

from collections import Counter
from dataclasses import replace
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from altium_monkey.altium_layer_stack_document import (
    AltiumLayerStackDocument,
    AltiumStackBendLine,
    AltiumStackRegion,
)
from altium_monkey.altium_pcbdoc import AltiumPcbDoc
from jsonschema import Draft202012Validator
import pytest

from altium_cruncher.altium_cruncher_pcb_svg_renderer import PcbSvgCompositeRenderer
from altium_cruncher.altium_cruncher_pcb_svg_bend_lines import (
    board_space_bend_lines,
    display_bend_lines,
)
from altium_cruncher.altium_cruncher_pcb_svg_config import (
    PcbSvgConfig,
    PcbSvgViewConfig,
    parse_pcb_layer_selector,
)


ROOT = Path(__file__).resolve().parents[1]
BLUETOOTH = (
    ROOT
    / "tests/assets/projects/bluetooth_sentinel_flex/input/Bluetooth_Sentinel.PcbDoc"
)
NS = {"s": "http://www.w3.org/2000/svg"}


def _document(*regions: AltiumStackRegion) -> AltiumLayerStackDocument:
    return replace(
        AltiumLayerStackDocument.canonical_empty(), board_regions=tuple(regions)
    )


def test_region_local_adapter_translates_from_source_geometry_envelope():
    region = AltiumStackRegion(
        name="Translated flex",
        outline_vertices=(
            (1_000_000, 2_000_000),
            (3_000_000, 2_000_000),
            (3_000_000, 4_000_000),
            (1_000_000, 4_000_000),
        ),
        bending_lines=(
            AltiumStackBendLine(
                angle_deg=-45,
                radius_raw=250_000,
                fold_index=7,
                x1=100_000,
                y1=200_000,
                x2=1_500_000,
                y2=200_000,
            ),
        ),
    )

    bends = board_space_bend_lines(_document(region))

    assert len(bends) == 1
    assert bends[0].region_name == "Translated flex"
    assert bends[0].fold_index == 7
    assert bends[0].radius_mils == 25
    assert (bends[0].x1_mils, bends[0].y1_mils) == (110, 220)
    assert (bends[0].x2_mils, bends[0].y2_mils) == (250, 220)


def test_display_bend_line_defaults_to_one_millimeter_per_end():
    region = AltiumStackRegion(
        name="Flex",
        outline_vertices=(
            (1_000_000, 2_000_000),
            (3_000_000, 2_000_000),
            (3_000_000, 4_000_000),
            (1_000_000, 4_000_000),
        ),
        bending_lines=(
            AltiumStackBendLine(
                x1=100_000,
                y1=200_000,
                x2=1_500_000,
                y2=200_000,
            ),
        ),
    )

    extended = display_bend_lines(_document(region), {})[0]
    edge_only = display_bend_lines(_document(region), {"extension_mm": 0})[0]

    assert (edge_only.x1_mils, edge_only.x2_mils) == pytest.approx((100, 300))
    assert edge_only.clip_to_region is True
    assert (extended.x1_mils, extended.x2_mils) == pytest.approx(
        (100 - 1 / 0.0254, 300 + 1 / 0.0254)
    )
    assert extended.extension_mm == 1
    assert extended.clip_to_region is False


def test_region_local_adapter_deduplicates_exact_records_and_skips_incomplete():
    valid = AltiumStackBendLine(
        angle_deg=-90,
        radius_raw=100_000,
        fold_index=0,
        x1=0,
        y1=0,
        x2=100_000,
        y2=0,
    )
    invalid = AltiumStackBendLine(x1=0, y1=0, x2=None, y2=0)
    region = AltiumStackRegion(
        name="Flex",
        outline_vertices=((0, 0), (200_000, 0), (200_000, 200_000), (0, 200_000)),
        bending_lines=(valid, valid, invalid),
    )

    bends = board_space_bend_lines(_document(region))

    assert len(bends) == 1
    assert bends[0].source_index == 0


@pytest.fixture(scope="module")
def bluetooth_pcbdoc() -> AltiumPcbDoc:
    return AltiumPcbDoc.from_file(BLUETOOTH)


def test_bluetooth_has_six_board_space_flex_lines_only(bluetooth_pcbdoc):
    document = AltiumLayerStackDocument.from_pcbdoc(bluetooth_pcbdoc)

    bends = board_space_bend_lines(document)

    assert len(bends) == 6
    assert {line.region_name for line in bends} == {"Layer Stack Region 3"}
    assert Counter(line.angle_deg for line in bends) == {-90.0: 2, -25.0: 2, -145.0: 2}
    assert Counter(line.fold_index for line in bends) == {0: 1, 1: 2, 2: 2, 3: 1}
    assert bends[0].x1_mils == pytest.approx(60408.4641)
    assert bends[0].y1_mils == pytest.approx(39368.110099679274)
    assert bends[0].x2_mils == pytest.approx(60802.16599999999)
    assert bends[0].y2_mils == pytest.approx(39368.111199679275)


def test_bluetooth_bend_layer_renders_clipped_styled_metadata(bluetooth_pcbdoc):
    config = PcbSvgConfig.default()
    view = PcbSvgViewConfig(
        name="bends",
        layers=["BEND_LINES"],
        styles={
            "bend_lines": {
                "color": "#123456",
                "opacity": 0.6,
                "line_width_mm": 0.2,
                "line_style": "dashed",
                "dash_length_mm": 0.75,
                "dash_gap_mm": 0.25,
                "extension_mm": 0,
            }
        },
    )
    svg = PcbSvgCompositeRenderer(config).render_view_svg(
        bluetooth_pcbdoc,
        view,
        project_parameters=None,
        layers=view.layers,
        group_id="bends",
        mirror=False,
        styles=config.resolved_styles_for_view(view),
    )
    root = ET.fromstring(svg)
    group = root.find('.//s:g[@id="layer-BEND_LINES"]', NS)

    assert group is not None
    assert group.get("data-layer-id") == "9015"
    assert group.get("stroke") == "#123456"
    assert float(group.get("opacity", "")) == pytest.approx(0.6)
    assert float(group.get("stroke-width", "")) == pytest.approx(0.2)
    assert group.get("stroke-dasharray") == "0.75 0.25"
    clip_paths = group.findall("s:defs/s:clipPath", NS)
    rendered = group.findall("s:line", NS)
    assert len(clip_paths) == 1
    assert len(rendered) == 6
    assert {line.get("data-region-name") for line in rendered} == {
        "Layer Stack Region 3"
    }
    assert all(
        line.get("clip-path") == "url(#bend-lines-region-2)" for line in rendered
    )

    bottom = ET.fromstring(
        PcbSvgCompositeRenderer(config).render_view_svg(
            bluetooth_pcbdoc,
            view,
            project_parameters=None,
            layers=view.layers,
            group_id="bends",
            mirror=True,
            styles=config.resolved_styles_for_view(view),
        )
    )
    bottom_scene = bottom.find('.//s:g[@id="scene"]', NS)
    bottom_lines = bottom.findall('.//s:g[@id="layer-BEND_LINES"]/s:line', NS)
    assert bottom_scene is not None and "scale(-1 1)" in bottom_scene.get(
        "transform", ""
    )
    assert [
        (line.get("x1"), line.get("y1"), line.get("x2"), line.get("y2"))
        for line in bottom_lines
    ] == [
        (line.get("x1"), line.get("y1"), line.get("x2"), line.get("y2"))
        for line in rendered
    ]


def test_bend_layer_can_be_disabled(bluetooth_pcbdoc):
    config = PcbSvgConfig.default()
    view = PcbSvgViewConfig(
        name="bends",
        layers=["BEND_LINES"],
        styles={"bend_lines": {"enabled": False}},
    )
    root = ET.fromstring(
        PcbSvgCompositeRenderer(config).render_view_svg(
            bluetooth_pcbdoc,
            view,
            project_parameters=None,
            layers=view.layers,
            group_id="bends",
            mirror=False,
            styles=config.resolved_styles_for_view(view),
        )
    )

    assert root.find('.//s:g[@id="layer-BEND_LINES"]', NS) is None


def test_bend_lines_public_config_contract():
    schema = json.loads(
        (ROOT / "docs/contracts/pcb_svg_config.a1.schema.json").read_text()
    )
    payload = {
        "schema": "pcb.svg.config.a1",
        "global": {
            "styles": {
                "bend_lines": {
                    "enabled": True,
                    "color": "#123456",
                    "opacity": 0.5,
                    "line_width_mm": 0.2,
                    "line_style": "solid",
                    "dash_length_mm": 0.75,
                    "dash_gap_mm": 0.25,
                    "extension_mm": 1,
                }
            }
        },
        "layer_outputs": {"include_special_layers": ["BEND_LINES"]},
    }

    Draft202012Validator(schema).validate(payload)
    assert parse_pcb_layer_selector("BEND_LINES") == ["BEND_LINES"]
    defaults = PcbSvgConfig.default().global_options.styles["bend_lines"]
    assert defaults["line_width_mm"] == 0.15
    assert defaults["dash_length_mm"] == 0.5
    assert defaults["dash_gap_mm"] == 0.3
    assert defaults["extension_mm"] == 1
    assert PcbSvgConfig.from_dict(payload).global_options.styles["bend_lines"] == {
        "enabled": True,
        "color": "#123456",
        "opacity": 0.5,
        "line_width_mm": 0.2,
        "line_style": "solid",
        "dash_length_mm": 0.75,
        "dash_gap_mm": 0.25,
        "extension_mm": 1,
    }
