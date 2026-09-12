"""Add existing copper rendering beneath the approved film and components.

Run pcb_illustration_review.py first, then:
uv run --no-sync python tests/support_scripts/pcb_copper_review.py
Updates the same illustration-review/index.html without rerunning Geometer.
"""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from altium_monkey.altium_pcbdoc import AltiumPcbDoc

from altium_cruncher.altium_cruncher_pcb_svg_a0_renderer import PcbSvgA0Renderer
from altium_cruncher.altium_cruncher_pcb_svg_config import PcbSvgConfig
from pcb_review_page import OUTPUT, write_review_page

ROOT = Path(__file__).resolve().parents[2]
SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)


def main() -> None:
    approved = ET.parse(OUTPUT / "top-components.svg").getroot()
    pcb = AltiumPcbDoc.from_file(
        ROOT / "tests/assets/projects/rt_super_c1/input/RT_SUPER_C1.PCBdoc"
    )
    config = PcbSvgConfig.from_dict(
        json.loads((ROOT / "examples/pcb-svg/copper-preview.config.json").read_text())
    )
    renderer = PcbSvgA0Renderer(config)
    for view in config.views:
        surface = ET.fromstring(
            renderer.render_view_svg(
                pcb,
                view,
                project_parameters=None,
                layers=view.layers,
                group_id=view.group_id,
                mirror=False,
                styles=config.resolved_styles_for_view(view),
            )
        )
        name = view.name.replace("_", "-")
        ET.ElementTree(surface).write(
            OUTPUT / f"{name}-surface.svg", encoding="utf-8", xml_declaration=True
        )
        preview = deepcopy(approved)
        scene = preview.find(f"{{{SVG}}}g")
        for child in list(scene):
            if child.get("data-pcb-svg-group") == "view":
                scene.remove(child)
        # The copper layer's board clip and drill masks remain inside its view
        # group; component overhangs above it retain their approved geometry.
        group = surface.find(f".//{{{SVG}}}g[@id='{view.group_id}']")
        scene.insert(0, deepcopy(group))
        ET.ElementTree(preview).write(
            OUTPUT / f"{name}.svg", encoding="utf-8", xml_declaration=True
        )
    print(write_review_page(OUTPUT))


if __name__ == "__main__":
    main()
