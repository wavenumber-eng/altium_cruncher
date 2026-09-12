"""Review drill/slot edges and real cutouts above the approved film.

Run pcb_illustration_review.py first, then:
uv run --no-sync python tests/support_scripts/pcb_holes_review.py
"""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from altium_monkey.altium_board import AltiumBoard, AltiumBoardOutline
from altium_monkey.altium_pcbdoc import AltiumPcbDoc

from pcb_review_page import write_review_page
from altium_monkey.altium_record_pcb__pad import AltiumPcbPad
from altium_monkey.altium_record_types import PcbLayer

from altium_cruncher.altium_cruncher_pcb_svg_a0_renderer import PcbSvgA0Renderer
from altium_cruncher.altium_cruncher_pcb_svg_config import (
    PcbSvgConfig,
    PcbSvgViewConfig,
)

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "tests/assets/projects/rt_super_c1/output/pcb-svg/illustration-review"
SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)


def slot_example() -> AltiumPcbDoc:
    pcb = AltiumPcbDoc()
    pcb.board = AltiumBoard(
        outline=AltiumBoardOutline.rectangle_mils(
            left_mils=0,
            bottom_mils=0,
            right_mils=500,
            top_mils=350,
        )
    )
    for x, y, plated, rotation, slot in (
        (75, 70, False, 0, False),
        (200, 150, True, 0, True),
        (375, 240, False, 45, True),
    ):
        pad = AltiumPcbPad()
        pad.layer = PcbLayer.MULTI_LAYER
        pad.x, pad.y = x * 10000, y * 10000
        pad.hole_size = 350000
        pad.hole_shape = 2 if slot else 0
        pad.slot_size = 1000000 if slot else 0
        pad.slot_rotation = rotation
        pad.is_plated = plated
        if plated:
            pad.top_width, pad.top_height = 1300000, 650000
        pad.soldermask_expansion_mode = 2
        pad.soldermask_expansion_manual = 40000
        pad._has_mask_expansion = True
        pcb.pads.append(pad)
    return pcb


def render_surface(
    pcb: AltiumPcbDoc, config: PcbSvgConfig, name: str, color: str
) -> ET.Element:
    view = PcbSvgViewConfig(
        name=name,
        layers=["SOLDERMASK_FILM_TOP", "BOARD_CUTOUTS", "DRILLS", "SLOTS"],
        styles={"soldermask_film": {"color": color}},
    )
    return ET.fromstring(
        PcbSvgA0Renderer(config).render_view_svg(
            pcb,
            view,
            project_parameters=None,
            layers=view.layers,
            group_id=name,
            mirror=False,
            styles=config.resolved_styles_for_view(view),
        )
    )


def main() -> None:
    approved = ET.parse(OUTPUT / "top-components.svg").getroot()
    pcb = AltiumPcbDoc.from_file(
        ROOT / "tests/assets/projects/rt_super_c1/input/RT_SUPER_C1.PCBdoc"
    )
    config = PcbSvgConfig.from_dict(
        json.loads((ROOT / "examples/pcb-svg/drill-preview.config.json").read_text())
    )
    for name, color in (("saved", "auto"), ("green", "#176B3A")):
        surface = render_surface(pcb, config, f"holes-{name}", color)
        ET.ElementTree(surface).write(
            OUTPUT / f"top-holes-only-{name}.svg",
            encoding="utf-8",
            xml_declaration=True,
        )
        preview = deepcopy(approved)
        scene = preview.find(f"{{{SVG}}}g")
        for child in list(scene):
            if child.get("data-pcb-svg-group") == "view":
                scene.remove(child)
        group = surface.find(f".//{{{SVG}}}g[@id='holes-{name}']")
        scene.insert(0, deepcopy(group))
        ET.ElementTree(preview).write(
            OUTPUT / f"top-holes-{name}.svg", encoding="utf-8", xml_declaration=True
        )

    cutouts = AltiumPcbDoc.from_file(
        ROOT / "tests/assets/projects/cutouts/input/cutout_multiple.PcbDoc"
    )
    for name, source in (("cutouts-film", cutouts), ("slots-film", slot_example())):
        root = render_surface(source, config, name, "#176B3A")
        ET.ElementTree(root).write(
            OUTPUT / f"{name}.svg", encoding="utf-8", xml_declaration=True
        )

    print(write_review_page(OUTPUT))


if __name__ == "__main__":
    main()
