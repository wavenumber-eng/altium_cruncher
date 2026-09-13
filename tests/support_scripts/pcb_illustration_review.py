"""Generate the first RT_SUPER_C1 illustration visual checkpoint.

Run: uv run python tests/support_scripts/pcb_illustration_review.py
Outputs stay under the fixture's ignored output directory. This board-only
proof deliberately uses the saved PCB, with no project variant selection.
"""

from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import time
import xml.etree.ElementTree as ET

import geometer as g
from altium_monkey.altium_pcbdoc import AltiumPcbDoc

from pcb_review_page import write_review_page

from altium_cruncher.altium_cruncher_pcb_illustration import (
    IllustrationComponent,
    IllustrationJob,
)
from altium_cruncher.altium_cruncher_pcb_svg_a0_renderer import PcbSvgA0Renderer
from altium_cruncher.altium_cruncher_pcb_svg_config import (
    PcbSvgConfig,
    PcbSvgViewConfig,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests/assets/projects/rt_super_c1"
OUTPUT = FIXTURE / "output/pcb-svg/illustration-review"
SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)


def stacked_bodies(job: IllustrationJob) -> IllustrationComponent:
    """The user's 100x200 mil lower / 100x100 mil raised upper example."""
    meshes = []
    bodies = []
    for name, width, length, low, high, color in (
        ("lower", 2.54, 5.08, 0.0, 2.54, (0.8, 0.65, 0.1)),
        ("upper", 2.54, 2.54, 2.54, 5.08, (0.1, 0.35, 0.85)),
    ):
        request = dict(
            schema="geometry.planar_step.request.a0",
            units="mm",
            name=name,
            bodies=[
                dict(
                    id=name,
                    name=name,
                    z_mm=low,
                    thickness_mm=high - low,
                    regions=[
                        dict(
                            outer=dict(
                                points=[
                                    [0, 0],
                                    [width, 0],
                                    [width, length],
                                    [0, length],
                                ]
                            )
                        )
                    ],
                )
            ],
        )
        raw = job._tessellate(name, request)
        meshes.extend(
            replace(
                mesh,
                id=f"{name}-{mesh.id}",
                materials=(g.MeshIllustrationMaterial(color=color),),
                triangle_material_indices=(0,) * (len(mesh.indices) // 3),
            )
            for mesh in raw
        )
        bodies.append(dict(kind="extruded", lower_z_mm=low, upper_z_mm=high))
    return IllustrationComponent(
        "stacked-example", (0, 0), tuple(meshes), tuple(bodies)
    )


def _namespace_registration(overlay: ET.Element) -> None:
    # Every copied ID/reference belongs to the registration overlay.
    id_map = {
        node.get("id"): "registration-" + node.get("id")
        for node in overlay.iter()
        if node.get("id")
    }
    for node in overlay.iter():
        for attr, value in list(node.attrib.items()):
            if attr == "id":
                node.set(attr, id_map[value])
            elif attr.endswith("href") and value.startswith("#"):
                node.set(attr, "#" + id_map[value[1:]])
            elif "url(#" in value:
                for old, new in id_map.items():
                    value = value.replace(f"url(#{old})", f"url(#{new})")
                node.set(attr, value)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    pcb = AltiumPcbDoc.from_file(FIXTURE / "input/RT_SUPER_C1.PCBdoc")
    config = PcbSvgConfig.default()
    config.global_options.include_metadata = False
    renderer = PcbSvgA0Renderer(config)

    def assembly(name: str, layers: list[str], color: str = "#ee3366") -> str:
        view = PcbSvgViewConfig(name=name, layers=layers)
        styles = config.resolved_styles_for_view(view)
        styles["assembly_hlr"].update(color=color, line_width_mm=0.035)
        return renderer.render_view_svg(
            pcb,
            view,
            project_parameters=None,
            layers=layers,
            group_id=name,
            mirror=False,
            styles=styles,
        )

    t = time.perf_counter()
    fast_svg = assembly("assembly-fast", ["BOARD_OUTLINE", "ASSEMBLY_HLR_TOP"])
    fast_seconds = time.perf_counter() - t
    (OUTPUT / "assembly-fast.svg").write_text(fast_svg, encoding="utf-8")
    base = ET.fromstring(assembly("components", ["BOARD_OUTLINE"]))
    scene = base.find(f"{{{SVG}}}g")
    defs = ET.SubElement(base, f"{{{SVG}}}defs")
    layer = ET.SubElement(scene, f"{{{SVG}}}g", {"id": "component-illustrations"})
    ctx = renderer._build_context(pcb, project_parameters=None)
    report = dict(
        source="RT_SUPER_C1.PCBdoc",
        variant="saved PCB; no project variant",
        fast_assembly_seconds=fast_seconds,
    )
    with g.GeometerClient() as client:
        job = IllustrationJob(client)
        t = time.perf_counter()
        components = job.collect_top(pcb)
        symbol_ids = {}
        extents = [0.0, 0.0, *map(float, base.attrib["viewBox"].split()[2:])]
        rendered_components = []
        for group in components:
            symbol = job.render(group)
            rendered_components.append((group, symbol))
            identity = id(symbol)
            symbol_id = symbol_ids.get(identity)
            if symbol_id is None:
                symbol_id = f"illustration-{len(symbol_ids)}"
                symbol_ids[identity] = symbol_id
                defs.append(symbol.group(symbol_id))
            x, y = (
                ctx.x_to_svg(group.anchor_mm[0] / 0.0254),
                ctx.y_to_svg(group.anchor_mm[1] / 0.0254),
            )
            use = ET.SubElement(
                layer,
                f"{{{SVG}}}use",
                {"href": f"#{symbol_id}", "transform": f"translate({x:.9g} {y:.9g})"},
            )
            ET.SubElement(use, f"{{{SVG}}}title").text = group.designator
            bounds = symbol.source_bounds_mm or group.bounds
            extents = [
                min(extents[0], x + bounds[0] - 0.1),
                min(extents[1], y - bounds[4] - 0.1),
                max(extents[2], x + bounds[3] + 0.1),
                max(extents[3], y - bounds[1] + 0.1),
            ]
        base.set(
            "viewBox",
            f"{extents[0]} {extents[1]} {extents[2] - extents[0]} {extents[3] - extents[1]}",
        )
        ET.ElementTree(base).write(
            OUTPUT / "top-components.svg", encoding="utf-8", xml_declaration=True
        )
        registration = ET.fromstring(fast_svg)
        overlay = registration.find(f"{{{SVG}}}g")
        overlay.set("opacity", "0.65")
        _namespace_registration(overlay)
        base.append(overlay)
        ET.ElementTree(base).write(
            OUTPUT / "top-registration.svg", encoding="utf-8", xml_declaration=True
        )
        report.update(
            component_seconds=time.perf_counter() - t,
            components=len(components),
            visibility_groups=len(components),
            body_count=sum(len(c.bodies) for c in components),
            components_detail=[
                dict(
                    designator=c.designator,
                    anchor_mm=c.anchor_mm,
                    bounds_mm=s.source_bounds_mm or c.bounds,
                    bodies=c.bodies,
                )
                for c, s in rendered_components
            ],
        )
        selected = [
            c
            for c in components
            if c.designator in {"D3", "D4", "U1", "U2", "R1", "X1"}
        ]
        selected.append(stacked_bodies(job))
        for component in selected:
            symbol = job.render(component)
            (OUTPUT / f"{component.designator}.svg").write_text(
                symbol.svg, encoding="utf-8"
            )
        report.update(
            counts=job.counts,
            warnings=job.warnings,
            seconds=time.perf_counter() - start,
            svg_bytes=(OUTPUT / "top-components.svg").stat().st_size,
        )
    (OUTPUT / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {key: value for key, value in report.items() if key != "components_detail"},
            indent=2,
        )
    )
    print(write_review_page(OUTPUT))


if __name__ == "__main__":
    main()
