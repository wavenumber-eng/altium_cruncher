"""Native demo rendering with Altium body placement and extrusions."""

from dataclasses import replace
from pathlib import Path
import re
from types import SimpleNamespace
import xml.etree.ElementTree as ET

import geometer as g
import pytest
from altium_monkey.altium_pcbdoc import AltiumPcbDoc
from altium_monkey.altium_record_pcb__component_body import AltiumPcbComponentBody
from altium_monkey.altium_record_pcb__shapebased_region import PcbExtendedVertex

from altium_cruncher.altium_cruncher_pcb_illustration import (
    IllustrationComponent,
    IllustrationJob,
    _digest,
    combine_components,
    _cylinder_mesh,
    _extrusion_request,
    extrusion_extents_mm,
)

ROOT = Path(__file__).resolve().parents[2]
SVG = "http://www.w3.org/2000/svg"
INKSCAPE = "http://www.inkscape.org/namespaces/inkscape"


def _body(length_mils, lower_mils, upper_mils, color, component_index=None):
    body = AltiumPcbComponentBody()
    body.component_index = component_index
    body.properties = {
        "MODEL.2D.X": "0mil",
        "MODEL.2D.Y": "0mil",
        "BODYPROJECTION": "0",
        "MODEL.EXTRUDED.MINZ": f"{lower_mils}mil",
        "MODEL.EXTRUDED.MAXZ": f"{upper_mils}mil",
    }
    body.model_extruded_min_z = int(lower_mils * 10000)
    body.model_extruded_max_z = int(upper_mils * 10000)
    body.body_color_3d = color
    for x, y in [(0, 0), (100, 0), (100, length_mils), (0, length_mils)]:
        vertex = PcbExtendedVertex()
        vertex.x, vertex.y = int(x * 10000), int(y * 10000)
        body.outline.append(vertex)
    return body


def _paint_at(symbol, x_mm, y_mm):
    """Sample opaque native rectangle fills, in painter order, away from edges."""
    x = (x_mm - symbol.x_mm) / symbol.mm_per_unit
    y = (-y_mm - symbol.y_mm) / symbol.mm_per_unit
    color = None
    for path in symbol.group("sample").iter(f"{{{SVG}}}path"):
        fill = path.get("fill")
        if not fill or fill == "none":
            continue
        assert not re.search(r"[ACHQSTVachqstv]", path.get("d", ""))
        values = list(map(float, re.findall(r"-?\d+(?:\.\d+)?", path.get("d", ""))))
        points = list(zip(values[::2], values[1::2]))
        inside = False
        for (ax, ay), (bx, by) in zip(points, points[1:] + points[:1]):
            if (ay > y) != (by > y) and x < (bx - ax) * (y - ay) / (by - ay) + ax:
                inside = not inside
        if inside:
            color = fill
    return color


def test_extruded_bodies_use_native_depth_and_surface_fusion():
    lower = _body(200, 0, 100, 0x00CC33)
    upper = _body(100, 100, 200, 0x0000FF)
    pcb = SimpleNamespace(components=[], component_bodies=[upper, lower])
    with g.GeometerClient() as client:
        job = IllustrationJob(client)
        parts = job.collect_top(pcb)
        assert len(parts) == 2  # Free bodies have nullable component indices.
        assert parts[0].bounds[2] == pytest.approx(2.54)
        assert parts[0].bounds[5] == pytest.approx(5.08)
        combined = combine_components(parts)
        symbol = job.render(combined)
        assert _paint_at(symbol, 1, 1) == _paint_at(job.render(parts[0]), 1, 1)
        assert _paint_at(symbol, 1, 4) == _paint_at(job.render(parts[1]), 1, 4)
        assert _paint_at(symbol, 1, 1) != _paint_at(symbol, 1, 4)
        assert symbol.stats["surface_draws"] < symbol.stats["triangles"]
        assert "<polygon" not in symbol.svg  # Native fuses matching triangles.
        assert symbol.stats["details"] > 0 and symbol.stats["outlines"] > 0
        assert not symbol.warnings
        assert job.render(replace(combined, anchor_mm=(20, 30))) is symbol
        upper.body_opacity_3d = 0
        assert len(job.collect_top(pcb)) == 1


def test_rt_components_include_extrusions_and_omit_parts_without_models():
    pcb = AltiumPcbDoc.from_file(
        ROOT / "tests/assets/projects/rt_super_c1/input/RT_SUPER_C1.PCBdoc"
    )
    with g.GeometerClient() as client:
        job = IllustrationJob(client)
        components = job.collect_top(pcb)
        by_name = {part.designator: part for part in components}
        assert len(components) == 50
        assert (
            sum(
                body["kind"] == "extruded"
                for part in components
                for body in part.bodies
            )
            == 18
        )
        assert "J1" not in by_name  # Pad-only connector: no invented illustration.
        assert len(by_name["D3"].bodies) == len(by_name["D4"].bodies) == 6
        assert by_name["D3"].bounds[5] == pytest.approx(0.75000104)
        assert by_name["U1"].bounds[2] == pytest.approx(0.00999998)
        green, red = job.render(by_name["D3"]), job.render(by_name["D4"])
        assert "rgb(47,152,47)" in green.svg
        assert "rgb(190,29,29)" in red.svg
        assert green.stats["surface_draws"] < green.stats["triangles"]
        combined = ET.Element("svg")
        combined.extend([green.group("green"), red.group("red")])
        assert not any(node.get("class") for node in combined.iter())
        assert not list(combined.iter(f"{{{SVG}}}style"))
        assert job.counts["tessellation_hits"] > 0
        assert not job.warnings


def test_component_svg_cache_reuses_instances_and_keeps_material_variants():
    pcb = SimpleNamespace(
        components=[], component_bodies=[_body(200, 0, 100, 0x00CC33)]
    )
    with g.GeometerClient() as client:
        job = IllustrationJob(client)
        part = job.collect_top(pcb)[0]
        symbol = job.render(part)
        instance = replace(
            part,
            designator="another-instance",
            anchor_mm=(100, 200),
            meshes=tuple(replace(mesh, id="other-" + mesh.id) for mesh in part.meshes),
        )
        assert job.render(instance) is symbol
        assert job.counts["illustrations"] == 1
        assert job.counts["illustration_hits"] == 1
        red = replace(
            instance,
            meshes=tuple(
                replace(
                    mesh,
                    materials=tuple(
                        replace(mat, color=(1, 0, 0)) for mat in mesh.materials
                    ),
                )
                for mesh in instance.meshes
            ),
        )
        red_symbol = job.render(red)
        assert red_symbol is not symbol
        assert _paint_at(red_symbol, 1, 1) != _paint_at(symbol, 1, 1)


def test_bottom_extrusions_preserve_xy_and_outward_depth():
    lower = _body(200, 0, 100, 0x00CC33)
    upper = _body(100, 100, 200, 0x0000FF)
    for body in (lower, upper):
        body.properties["BODYPROJECTION"] = "1"
        # An asymmetric X offset makes a mistaken native mirror observable.
        for vertex in body.outline:
            vertex.x += 200000
    pcb = SimpleNamespace(components=[], component_bodies=[upper, lower])
    with g.GeometerClient() as client:
        job = IllustrationJob(client)
        assert job.collect_top(pcb) == []
        parts = job.collect(pcb, side="bottom")
        assert parts[0].bounds == pytest.approx((0.508, 0, -5.08, 3.048, 2.54, -2.54))
        combined = combine_components(parts)
        symbol = job.render(combined, side="bottom")
        assert _paint_at(symbol, 1, 1) == _paint_at(
            job.render(parts[0], side="bottom"), 1, 1
        )
        assert _paint_at(symbol, 1, 4) == _paint_at(
            job.render(parts[1], side="bottom"), 1, 4
        )
        assert _paint_at(symbol, 1, 1) != _paint_at(symbol, 1, 4)
        assert _paint_at(symbol, 0, 1) is None
        assert job.render(combined, side="top") is not symbol
        assert job.render(combined, side="bottom") is symbol
        assert not job.warnings


def test_rt_bottom_models_use_body_side_and_signed_z_offset():
    pcb = AltiumPcbDoc.from_file(
        ROOT / "tests/assets/projects/rt_super_c1/input/RT_SUPER_C1.PCBdoc"
    )
    with g.GeometerClient() as client:
        job = IllustrationJob(client)
        parts = job.collect(pcb, side="bottom")
        by_name = {part.designator: part for part in parts}
        assert len(parts) == 107
        assert all(body["kind"] == "step" for part in parts for body in part.bodies)
        assert (by_name["T1"].bounds[2], by_name["T1"].bounds[5]) == pytest.approx(
            (-4.4069, 2.5273), abs=1e-5
        )
        assert (by_name["C10"].bounds[2], by_name["C10"].bounds[5]) == pytest.approx(
            (-0.55, 0), abs=1e-5
        )
        assert "D3" not in by_name and "J1" not in by_name
        assert job.counts["tessellation_hits"] > 0
        assert not job.warnings


def test_step_tessellation_preserves_root_placement_used_by_assembly():
    request = dict(
        schema="geometry.planar_step.request.a0",
        units="mm",
        name="rooted",
        bodies=[
            dict(
                id="body",
                name="body",
                z_mm=0,
                thickness_mm=1,
                regions=[dict(outer=dict(points=[[0, 0], [2, 0], [2, 3], [0, 3]]))],
            )
        ],
    )
    step = g.planar_step(request).decode()
    # Give the generated box an asymmetric STEP root frame, distinct from its
    # face-local placements. No checked-in or private CAD fixture is required.
    root_axis = re.search(
        r"ADVANCED_BREP_SHAPE_REPRESENTATION\('',\(#(\d+),", step
    ).group(1)
    point, z_dir, x_dir = re.search(
        rf"#{root_axis} = AXIS2_PLACEMENT_3D\('',#(\d+),#(\d+),#(\d+)\);", step
    ).groups()
    for entity, kind, values in (
        (point, "CARTESIAN_POINT", "10.,20.,-5."),
        (z_dir, "DIRECTION", "0.,0.,-1."),
        (x_dir, "DIRECTION", "-1.,0.,0."),
    ):
        step = re.sub(
            rf"#{entity} = {kind}\([^;]+;", f"#{entity} = {kind}('',({values}));", step
        )
    with g.GeometerClient() as client:
        job = IllustrationJob(client)
        meshes = job._tessellate("rooted", step.encode())
        part = IllustrationComponent("rooted", (0, 0), meshes, ())
        assert part.bounds == pytest.approx((8, 20, -6, 10, 23, -5))
        symbol = job.render(part)
        assert _paint_at(symbol, 9, 21) is not None
        assert _paint_at(symbol, 1, 1) is None


def test_extrusion_legacy_heights_are_elevations():
    body = _body(200, 0, 100, 0x808080)
    body.properties = {}
    body.standoff_height, body.overall_height = 1_000_000, 2_000_000
    assert extrusion_extents_mm(body) == pytest.approx((2.54, 5.08))
    body.overall_height = body.standoff_height
    with pytest.raises(ValueError, match="upper Z > lower Z"):
        extrusion_extents_mm(body)


def test_rotated_extrusion_occurrences_share_canonical_geometry():
    canonical = _body(200, 0, 100, 0x00CC33)
    occurrence = _body(200, 0, 100, 0x00CC33)
    anchor_mils = (1000.0, 2000.0)
    for vertex in occurrence.outline:
        local_x, local_y = vertex.x / 10000, vertex.y / 10000
        vertex.x = round((anchor_mils[0] - local_y) * 10000)
        vertex.y = round((anchor_mils[1] + local_x) * 10000)

    canonical_request = _extrusion_request(canonical, (0.0, 0.0))
    occurrence_request = _extrusion_request(
        occurrence,
        tuple(value * 0.0254 for value in anchor_mils),
        component_rotation_degrees=90.0,
    )
    assert _digest(occurrence_request) == _digest(canonical_request)


def test_altium_cylinder_uses_analytic_dimensions_without_native_tessellation():
    body = AltiumPcbComponentBody()
    body.model_cylinder_radius = 500_000
    body.model_cylinder_height = 1_000_000
    body.standoff_height = 250_000
    body.model_2d_x = 1_000_000
    body.model_2d_y = 2_000_000
    key, top = _cylinder_mesh(body, (90.0, 180.0))
    same_key, bottom = _cylinder_mesh(body, (90.0, 180.0), is_bottom=True)
    assert key != same_key
    assert len(top.indices) // 3 == 48 * 4
    assert (min(top.positions[2::3]), max(top.positions[2::3])) == pytest.approx(
        (0.635, 3.175)
    )
    assert (min(bottom.positions[2::3]), max(bottom.positions[2::3])) == pytest.approx(
        (-3.175, -0.635)
    )
    assert (
        sum(top.positions[0::3]) / (len(top.positions) // 3),
        sum(top.positions[1::3]) / (len(top.positions) // 3),
    ) == pytest.approx((0.254, 0.508))


@pytest.mark.parametrize("side", ["top", "bottom"])
def test_component_virtual_layers_compose_cache_and_link_metadata(side, tmp_path):
    import json
    from altium_monkey.altium_board import AltiumBoard, AltiumBoardOutline
    from altium_monkey.altium_pcb_component import AltiumPcbComponent
    from altium_monkey.altium_record_pcb__pad import AltiumPcbPad
    from altium_monkey.altium_record_types import PcbLayer
    from altium_cruncher.altium_cruncher_pcb_svg_a0_renderer import (
        PcbSvgA0Renderer,
        write_or_update_view_svg,
    )
    from altium_cruncher.altium_cruncher_pcb_svg_config import (
        PcbSvgConfig,
        PcbSvgViewConfig,
    )

    pcb = AltiumPcbDoc()
    pcb.board = AltiumBoard(
        outline=AltiumBoardOutline.rectangle_mils(
            left_mils=-100, bottom_mils=-100, right_mils=800, top_mils=800
        )
    )
    pcb.components = [
        AltiumPcbComponent(
            name, "test", side.upper(), "0mil", "0mil", unique_id=name + "-UID"
        )
        for name in ("U1", "U2", "J1")
    ]
    for index in (0, 1):
        body = _body(200, 0, 100, 0x00CC33, component_index=index)
        body.properties["BODYPROJECTION"] = "1" if side == "bottom" else "0"
        pcb.component_bodies.append(body)
    pad = AltiumPcbPad()
    pad.component_index = 2
    pad.designator = "1"
    pad.x, pad.y = 4000000, 4000000
    pad.top_width = pad.bot_width = pad.width = 1000000
    pad.top_height = pad.bot_height = pad.height = 1000000
    pad.layer = PcbLayer.BOTTOM if side == "bottom" else PcbLayer.TOP
    pcb.pads.append(pad)
    config = PcbSvgConfig.default()
    renderer = PcbSvgA0Renderer(config)
    view = PcbSvgViewConfig(
        name="preview", layers=["DRILLS", "ILLUSTRATION_" + side.upper()]
    )

    def render(active):
        return renderer.render_view_svg(
            pcb,
            active,
            project_parameters=None,
            layers=active.layers,
            group_id="review",
            mirror=side == "bottom",
            styles=config.resolved_styles_for_view(active),
        )

    render(view)
    calls = dict(renderer.component_layers.job.counts)
    assembly = replace(
        view, layers=view.layers + ["ASSEMBLY_DESIGNATORS_" + side.upper()]
    )
    svg = render(assembly)
    assert (
        renderer.component_layers.job.counts == calls
    )  # No new HLR or painted SVG calls.
    assert renderer.component_layers.layer_hits == 1
    root = ET.fromstring(svg)
    view_group = root.find(f"{{{SVG}}}g/{{{SVG}}}g")
    assert view_group.get(f"{{{INKSCAPE}}}groupmode") == "layer"
    illustration_layer = root.find(
        f".//{{{SVG}}}g[@data-layer-name='ILLUSTRATION_{side.upper()}']"
    )
    assert illustration_layer.get(f"{{{INKSCAPE}}}label") == (
        f"Illustration {side.title()}"
    )
    ids = [node.get("id") for node in root.iter() if node.get("id")]
    assert len(ids) == len(set(ids))
    uses = root.findall(f".//{{{SVG}}}use")
    assert len(uses) == 2 and uses[0].get("href") == uses[1].get("href")
    assert uses[0].get("href")[1:] in ids
    metadata = json.loads(root.find(f"{{{SVG}}}metadata").text)
    from jsonschema import Draft202012Validator

    schema = json.loads(
        (ROOT / "docs/contracts/pcb_svg_component_layers.a0.schema.json").read_text()
    )
    Draft202012Validator(schema).validate(metadata["virtual_component_layers"])
    layers = metadata["virtual_component_layers"]["layers"]
    assert [len(layer["instances"]) for layer in layers] == [2, 3]
    assert layers[1]["instances"][2]["geometry_source"] == "pads"
    label = root.find(
        f".//{{{SVG}}}g[@data-feature='assembly-designator'][@data-component-index='0']"
    )
    assert label.get(f"{{{INKSCAPE}}}label") == "U1"
    assert label.get("aria-label") == "U1 assembly designator"
    assert label.get("data-component-uid") == "U1-UID"
    assert label.find(f"{{{SVG}}}text").get("fill") == "#FF0000"
    assert (label.get("transform") is not None) == (side == "bottom")
    # Native outline coordinates must align with the authored asymmetric body.
    placed = next(iter(renderer.component_layers._placed.values()))
    outline = placed[0][1].outline_segments_mm
    xs, ys = zip(*(point for segment in outline for point in segment))
    assert (min(xs), max(xs), min(ys), max(ys)) == pytest.approx((0, 2.54, -5.08, 0))
    target = tmp_path / "preview.svg"
    write_or_update_view_svg(target, svg, group_id="review")
    write_or_update_view_svg(target, svg, group_id="review")
    refreshed = ET.parse(target).getroot()
    assert len(refreshed.findall(f".//{{{SVG}}}use")) == 2
    refreshed_component = refreshed.find(
        f".//{{{SVG}}}g[@data-feature='component-illustration']"
    )
    assert refreshed_component.get(f"{{{INKSCAPE}}}label") == "U1"
