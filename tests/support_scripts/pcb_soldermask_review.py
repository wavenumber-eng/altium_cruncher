"""Fast film/style iteration using the approved component SVG, without rerunning 3D.

Run pcb_illustration_review.py first, then:
uv run --no-sync python tests/support_scripts/pcb_soldermask_review.py
"""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from altium_monkey.altium_pcbdoc import AltiumPcbDoc

from pcb_review_page import write_review_page

from altium_cruncher.altium_cruncher_pcb_svg_renderer import PcbSvgCompositeRenderer
from altium_cruncher.altium_cruncher_pcb_svg_config import (
    PcbSvgConfig,
    PcbSvgViewConfig,
)
from altium_cruncher.altium_cruncher_pcb_svg_soldermask_film import (
    saved_soldermask_color,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests/assets/projects/rt_super_c1"
OUTPUT = FIXTURE / "output/pcb-svg/illustration-review"
SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)


def main() -> None:
    approved = ET.parse(OUTPUT / "top-components.svg").getroot()
    pcb = AltiumPcbDoc.from_file(FIXTURE / "input/RT_SUPER_C1.PCBdoc")
    config = PcbSvgConfig.default()
    config.global_options.include_metadata = False
    variants = [
        ("saved", "auto", 1.0, "Saved Altium color (white), opaque film"),
        ("green", "#176B3A", 1.0, "Green color override, opaque film"),
        ("transparent", "#176B3A", 0.55, "Green override, 55% opacity"),
    ]
    for name, color, opacity, label in variants:
        view = PcbSvgViewConfig(
            name=f"film-{name}",
            layers=["SOLDERMASK_FILM_TOP"],
            styles={"soldermask_film": {"color": color, "opacity": opacity}},
        )
        root = ET.fromstring(
            PcbSvgCompositeRenderer(config).render_view_svg(
                pcb,
                view,
                project_parameters=None,
                layers=view.layers,
                group_id=view.name,
                mirror=False,
                styles=config.resolved_styles_for_view(view),
            )
        )
        ET.ElementTree(root).write(
            OUTPUT / f"top-film-{name}.svg", encoding="utf-8", xml_declaration=True
        )
        preview = deepcopy(approved)
        scene = preview.find(f"{{{SVG}}}g")
        # Remove the original review's visible board-outline group. Film supplies
        # the board shape; illustrations and their registration remain untouched.
        for child in list(scene):
            if child.get("data-pcb-svg-group") == "view":
                scene.remove(child)
        film = root.find(f".//{{{SVG}}}g[@id='layer-SOLDERMASK_FILM_TOP']")
        scene.insert(0, deepcopy(film))
        filename = f"top-preview-{name}.svg"
        ET.ElementTree(preview).write(
            OUTPUT / filename, encoding="utf-8", xml_declaration=True
        )
    # Bottom film uses its own saved color and openings, mirrored as an assembly view.
    bottom = PcbSvgViewConfig(name="film-bottom", layers=["SOLDERMASK_FILM_BOTTOM"])
    (OUTPUT / "bottom-film.svg").write_text(
        PcbSvgCompositeRenderer(config).render_view_svg(
            pcb,
            bottom,
            project_parameters=None,
            layers=bottom.layers,
            group_id=bottom.name,
            mirror=True,
            styles=config.resolved_styles_for_view(bottom),
        ),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "top_saved_color": saved_soldermask_color(pcb, "top"),
                "bottom_saved_color": saved_soldermask_color(pcb, "bottom"),
                "review": str(write_review_page(OUTPUT)),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
