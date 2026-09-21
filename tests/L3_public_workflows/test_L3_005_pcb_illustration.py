"""Native demo rendering with Altium body placement and extrusions."""

from dataclasses import replace
from io import BytesIO
from pathlib import Path
import re
from types import SimpleNamespace
import xml.etree.ElementTree as ET

import geometer as g
from PIL import Image
import pytest
from resvg_py import svg_to_bytes
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
from altium_cruncher.pcb_board_region_envelope_index import (
    BoardRegionEnvelopeIndex,
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
        parts = [
            part for part, _ in job.render_many(parts, side="top", illustrate=True)
        ]
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
        green, red = job.render(by_name["D3"]), job.render(by_name["D4"])
        u1 = job.render(by_name["U1"])
        assert green.source_bounds_mm is not None
        assert green.source_bounds_mm[5] == pytest.approx(0.75000104)
        assert u1.source_bounds_mm is not None
        assert u1.source_bounds_mm[2] == pytest.approx(0.00999998)
        assert "rgb(47,152,47)" in green.svg
        assert "rgb(190,29,29)" in red.svg
        assert green.stats["surface_draws"] < green.stats["triangles"]
        combined = ET.Element("svg")
        combined.extend([green.group("green"), red.group("red")])
        assert not any(node.get("class") for node in combined.iter())
        assert not list(combined.iter(f"{{{SVG}}}style"))
        assert job.counts["illustrations"] == 3
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
        red_part = job.collect_top(
            SimpleNamespace(
                components=[], component_bodies=[_body(200, 0, 100, 0x0000FF)]
            )
        )[0]
        red = replace(red_part, designator="red-instance", anchor_mm=instance.anchor_mm)
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
        parts = [
            part for part, _ in job.render_many(parts, side="bottom", illustrate=True)
        ]
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
        t1 = job.render(by_name["T1"], side="bottom").source_bounds_mm
        c10 = job.render(by_name["C10"], side="bottom").source_bounds_mm
        assert t1 is not None and c10 is not None
        assert (t1[2], t1[5]) == pytest.approx((-4.4069, 2.5273), abs=1e-5)
        assert (c10[2], c10[5]) == pytest.approx((-0.55, 0), abs=1e-5)
        assert "D3" not in by_name and "J1" not in by_name
        assert job.counts["illustrations"] == 2
        assert not job.warnings


def test_rt_through_board_model_uses_clipped_fragments_on_both_sides():
    pcb = AltiumPcbDoc.from_file(
        ROOT / "tests/assets/projects/rt_super_c1/input/RT_SUPER_C1.PCBdoc"
    )
    regions = BoardRegionEnvelopeIndex.from_pcbdoc(pcb)
    with g.GeometerClient() as client:
        job = IllustrationJob(client, region_index=regions)
        top_parts = {part.designator: part for part in job.collect(pcb, side="top")}
        top_part = top_parts["T1"]
        bottom_part = next(
            part for part in job.collect(pcb, side="bottom") if part.designator == "T1"
        )
        assert top_part.authored_side == bottom_part.authored_side == "bottom"
        assert top_part.board_z_offset_mm == pytest.approx(-1.0239248)
        assert bottom_part.board_z_offset_mm == pytest.approx(-1.0239248)

        # A bottom-side SMD whose model ends at its mounting plane has no
        # board-surface fragment. Its retained full projection is masked to
        # apertures/outside-board by the SVG compositor.
        c10_top = job.render(top_parts["C10"], side="top")
        assert c10_top.svg == ""
        assert c10_top.aperture is not None

        top = job.render(top_part, side="top")
        bottom = job.render(bottom_part, side="bottom")
        assert not top.empty and not bottom.empty
        assert top.source_bounds_mm == pytest.approx(
            (-0.2413, -0.23954065132, -1e-6, 0.2413, 0.23954065132, 1.5033752),
            abs=1e-9,
        )
        assert bottom.source_bounds_mm == pytest.approx(
            (
                -0.508,
                -0.504296108042,
                -5.4308248,
                0.508,
                0.504296108042,
                -1.0239238,
            ),
            abs=1e-9,
        )


@pytest.mark.slow
def test_issue67_reporter_ic_orientation_and_p1_pin_registration():
    pcb = AltiumPcbDoc.from_file(
        ROOT / "tests/assets/projects/issue67-reporter/input/sample.PcbDoc"
    )
    regions = BoardRegionEnvelopeIndex.from_pcbdoc(pcb)
    component_indices = {
        component.designator: index for index, component in enumerate(pcb.components)
    }

    with g.GeometerClient() as client:
        job = IllustrationJob(client, region_index=regions, emit_warnings=False)
        parts = {part.designator: part for part in job.collect(pcb, side="bottom")}

        for designator in ("IC1", "IC2", "IC3"):
            part = parts[designator]
            component = pcb.components[component_indices[designator]]
            symbol = job.render(part, side="bottom")
            pads = [
                pad
                for pad in pcb.pads
                if pad.component_index == component_indices[designator]
            ]

            assert str(component.layer).upper() == "BOTTOM"
            assert float(component.rotation) == pytest.approx(270.0)
            assert symbol.source_bounds_mm == pytest.approx(
                (-4.95, -3.0, -2.16148, 4.95, 3.0, -0.41148), abs=1e-6
            )
            local_pad_x = [float(pad.x) * 2.54e-6 - part.anchor_mm[0] for pad in pads]
            local_pad_y = [float(pad.y) * 2.54e-6 - part.anchor_mm[1] for pad in pads]
            assert min(local_pad_x) > -4.95 and max(local_pad_x) < 4.95
            assert min(local_pad_y) > -3.0 and max(local_pad_y) < 3.0

        # The first authored IC3 pad is pin 1. In board coordinates it is
        # upper-left of the component anchor; the single bottom-view mirror
        # makes it upper-right, matching the reporter's Altium reference.
        ic3 = parts["IC3"]
        ic3_pads = [
            pad for pad in pcb.pads if pad.component_index == component_indices["IC3"]
        ]
        pin1_x = float(ic3_pads[0].x) * 2.54e-6 - ic3.anchor_mm[0]
        pin1_y = float(ic3_pads[0].y) * 2.54e-6 - ic3.anchor_mm[1]
        assert (-pin1_x, pin1_y) == pytest.approx((4.445, 2.71200118), abs=1e-6)

        p1 = parts["P1"]
        p1_index = component_indices["P1"]
        p1_pads = [pad for pad in pcb.pads if pad.component_index == p1_index]
        pad_centers = sorted(
            (
                float(pad.x) * 2.54e-6 - p1.anchor_mm[0],
                float(pad.y) * 2.54e-6 - p1.anchor_mm[1],
            )
            for pad in p1_pads
        )
        body_indices = sorted(body["index"] for body in p1.bodies)
        model_centers = []
        for body_index in body_indices:
            meshes = [
                mesh for mesh in p1.meshes if mesh.id.startswith(f"body-{body_index}-")
            ]
            xs = [value for mesh in meshes for value in mesh.positions[0::3]]
            ys = [value for mesh in meshes for value in mesh.positions[1::3]]
            model_centers.append(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2))

        assert len(pad_centers) == len(model_centers) == 7
        for model_center, pad_center in zip(
            sorted(model_centers), pad_centers, strict=True
        ):
            assert model_center == pytest.approx(pad_center, abs=5e-4)


@pytest.mark.slow
def test_gate6_analytic_fixture_clips_each_supported_body_type_on_both_sides():
    pcb = AltiumPcbDoc.from_file(
        ROOT
        / "tests/assets/projects/toon-analytic-bodies/input/toon_analytic_bodies.PcbDoc"
    )
    regions = BoardRegionEnvelopeIndex.from_pcbdoc(pcb)

    with g.GeometerClient() as client:
        job = IllustrationJob(client, region_index=regions, emit_warnings=False)
        parts = {part.designator: part for part in job.collect(pcb, side="top")}

        assert "A9" not in parts  # zero-opacity omission control
        assert len(parts) == 13
        for designator in ("A3", "A4", "B4"):
            top = job.render(parts[designator], side="top")
            bottom = job.render(parts[designator], side="bottom")
            assert top.svg and bottom.svg
            assert top.aperture is not None and bottom.aperture is not None
            assert top.source_bounds_mm is not None
            assert bottom.source_bounds_mm is not None
            assert top.source_bounds_mm[2] == pytest.approx(-1e-6)
            assert bottom.source_bounds_mm[5] == pytest.approx(-1.587499)

        top_only = job.render(parts["A1"], side="bottom")
        bottom_only = job.render(parts["B1"], side="top")
        assert top_only.svg == "" and top_only.aperture is not None
        assert bottom_only.svg == "" and bottom_only.aperture is not None


@pytest.mark.slow
@pytest.mark.parametrize(
    ("fixture", "filename", "side", "designators"),
    [
        (
            "projection-test",
            "projection_test.PcbDoc",
            "bottom",
            ("J2", "J7"),
        ),
        (
            "usb-edge",
            "usb_edge.PcbDoc",
            "top",
            ("D1",),
        ),
        (
            "single-throughhole",
            "single-though-hole-top.PcbDoc",
            "bottom",
            ("J1",),
        ),
    ],
)
def test_aperture_composition_stress_fixtures(fixture, filename, side, designators):
    from altium_cruncher.altium_cruncher_pcb_svg_renderer import (
        PcbSvgCompositeRenderer,
    )
    from altium_cruncher.altium_cruncher_pcb_svg_config import PcbSvgConfig
    from altium_cruncher.pcb_illustration_config import illustration_preset

    pcb = AltiumPcbDoc.from_file(
        ROOT / f"tests/assets/projects/{fixture}/input/{filename}"
    )
    config = PcbSvgConfig.from_dict(illustration_preset())
    view = next(view for view in config.views if view.name.startswith(side))
    renderer = PcbSvgCompositeRenderer(config)
    root = ET.fromstring(
        renderer.render_view_svg(
            pcb,
            view,
            project_parameters=None,
            layers=view.layers,
            group_id="aperture-stress",
            mirror=side == "bottom",
            styles=config.resolved_styles_for_view(view),
        )
    )

    mask = root.find(f".//{{{SVG}}}mask[@id='illustration_{side}-open-space']")
    assert mask is not None
    ctx = renderer._build_context(pcb, project_parameters=None)
    # The mask is authored before the outer bottom-view reflection, so compare
    # it with the unmirrored board canvas rather than the final viewBox.
    assert float(mask.get("x")) < 0
    assert float(mask.get("width")) > ctx.width_mm
    for designator in designators:
        component = root.find(
            f".//{{{SVG}}}g[@data-feature='component-illustration']"
            f"[@data-designator='{designator}']"
        )
        assert component is not None
        branches = list(component)
        assert {branch.get("data-visibility-domain") for branch in branches} == {
            "aperture",
            "board-surface",
        }
        for branch in branches:
            assert branch.tag == f"{{{SVG}}}g"
            assert branch.get("mask", "").startswith("url(#")
            use = branch.find(f"{{{SVG}}}use")
            assert use is not None
            assert use.get("transform", "").startswith("translate(")
            assert use.get("mask") is None
    if fixture == "usb-edge":
        # D1 is a reverse-mount LED in one physical plated slot. The complement
        # mask must expose that bore; colored DRILLS/SLOTS artwork is separate.
        slot_openings = [node for node in mask if node.get("stroke") == "white"]
        assert len(slot_openings) == 1
        assert slot_openings[0].tag == f"{{{SVG}}}path"
        assert slot_openings[0].get("fill") == "none"
        assert slot_openings[0].get("stroke-linecap") == "round"


def _raster_signature(svg: str) -> tuple[tuple[int, int], bytes]:
    picture = Image.open(BytesIO(svg_to_bytes(svg_string=svg, dpi=254))).convert("RGBA")
    return picture.size, picture.tobytes()


@pytest.mark.slow
@pytest.mark.parametrize(
    ("fixture", "filename", "designator", "placement_side", "through_board"),
    [
        (
            "single-throughhole",
            "single-though-hole-top.PcbDoc",
            "J1",
            "top",
            True,
        ),
        (
            "single-throughhole",
            "single-though-hole-bottom.PcbDoc",
            "J1",
            "bottom",
            True,
        ),
        ("single-smt", "single-smt-top.PcbDoc", "R1", "top", False),
        ("single-smt", "single-smt-bottom.PcbDoc", "R1", "bottom", False),
    ],
)
def test_single_part_geometry_and_designator_side_matrix(
    fixture, filename, designator, placement_side, through_board
):
    """Exercise both views and both label modes for each Gate 1 document."""

    from altium_cruncher.altium_cruncher_pcb_svg_renderer import (
        PcbSvgCompositeRenderer,
    )
    from altium_cruncher.altium_cruncher_pcb_svg_config import PcbSvgConfig
    from altium_cruncher.pcb_illustration_config import illustration_preset

    pcb = AltiumPcbDoc.from_file(
        ROOT / f"tests/assets/projects/{fixture}/input/{filename}"
    )
    config = PcbSvgConfig.from_dict(illustration_preset())
    renderer = PcbSvgCompositeRenderer(config)

    for side in ("top", "bottom"):
        view = next(candidate for candidate in config.views if candidate.name == side)
        illustration_token = f"ILLUSTRATION_{side.upper()}"

        def render(layers):
            selected_layers = list(layers)
            return renderer.render_view_svg(
                pcb,
                replace(view, layers=selected_layers),
                project_parameters=None,
                layers=selected_layers,
                group_id=f"single-part-{side}",
                mirror=side == "bottom",
                styles=config.resolved_styles_for_view(view),
            )

        without_designator = render(view.layers)
        without_root = ET.fromstring(without_designator)
        assert (
            without_root.find(f".//{{{SVG}}}g[@data-feature='assembly-designator']")
            is None
        )

        without_component = render(
            token for token in view.layers if token != illustration_token
        )
        pixels_changed = _raster_signature(without_designator) != _raster_signature(
            without_component
        )
        assert pixels_changed is (through_board or side == placement_side)

        with_designator = render([*view.layers, f"ASSEMBLY_DESIGNATORS_{side.upper()}"])
        label = ET.fromstring(with_designator).find(
            f".//{{{SVG}}}g[@data-feature='assembly-designator']"
            f"[@data-designator='{designator}']"
        )
        assert (label is not None) is (side == placement_side)


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
    from altium_cruncher.altium_cruncher_pcb_svg_renderer import (
        PcbSvgCompositeRenderer,
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
    renderer = PcbSvgCompositeRenderer(config)
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
    assert [len(layer["instances"]) for layer in layers] == [2, 2]
    assert {item["designator"] for item in layers[1]["instances"]} == {"U1", "U2"}
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
