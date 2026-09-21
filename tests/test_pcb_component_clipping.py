"""PCB policy qualification for Geometer issue 40 clipping requests."""

from dataclasses import dataclass
from types import SimpleNamespace

import geometer as g
from shapely.geometry import Polygon
from altium_monkey.altium_resolved_layer_stack import ResolvedStackEnvelope
import pytest

from altium_cruncher.altium_cruncher_pcb_illustration import (
    DirectIllustrationSource,
    IllustrationComponent,
    IllustrationJob,
    IllustrationSymbol,
)
from altium_cruncher.pcb_board_region_envelope_index import (
    BoardRegionEnvelope,
    BoardRegionEnvelopeIndex,
)
from altium_cruncher.pcb_component_clipping import (
    ComponentVisibilityAction,
    resolve_component_visibility,
)
from altium_cruncher.altium_cruncher_pcb_svg_substrate import (
    _BoardOpenSpaceIndex,
    _board_material_geometry,
)


def _region(
    name: str,
    points: tuple[tuple[float, float], ...],
    *,
    thickness_mils: float = 40.312,
    holes: tuple[tuple[tuple[float, float], ...], ...] = (),
) -> BoardRegionEnvelope:
    geometry = Polygon(points, holes)
    envelope = ResolvedStackEnvelope(
        source_stackup_ref=name,
        substack_name=name,
        is_flex=False,
        z_zero="substack_midplane",
        total_thickness_mils=thickness_mils,
        top_z_mils=thickness_mils / 2,
        bottom_z_mils=-thickness_mils / 2,
    )
    return BoardRegionEnvelope(
        source_index=0,
        name=name,
        layerstack_id=name,
        substack_name=name,
        is_flex=False,
        outline_mils=points,
        holes_mils=holes,
        bounds_mils=tuple(float(value) for value in geometry.bounds),
        envelope=envelope,
        _geometry=geometry,
    )


def _index(*regions: BoardRegionEnvelope) -> BoardRegionEnvelopeIndex:
    return BoardRegionEnvelopeIndex(regions)


def test_rt_super_t_pin_bounds_require_real_fragments_on_both_sides():
    index = _index(_region("RT rigid", ((0, 0), (1000, 0), (1000, 1000), (0, 1000))))
    # Exact transformed T1 bounds characterized through Geometer 2026.9.13.
    bounds = (-0.508, -0.504296108, -4.4069, 0.508, 0.504296108, 2.5273)

    top = resolve_component_visibility(
        index,
        anchor_mm=(12.7, 12.7),
        bounds_local_mm=bounds,
        authored_side="bottom",
        requested_side="top",
    )
    bottom = resolve_component_visibility(
        index,
        anchor_mm=(12.7, 12.7),
        bounds_local_mm=bounds,
        authored_side="bottom",
        requested_side="bottom",
    )

    assert top.action is ComponentVisibilityAction.RENDER_CLIPPED
    assert top.crosses_to_opposite_side is True
    assert top.plane is not None and top.plane.normal == (0.0, 0.0, 1.0)
    assert top.plane.distance_mm == 0.0
    assert bottom.action is ComponentVisibilityAction.RENDER_CLIPPED
    assert bottom.crosses_to_opposite_side is False
    assert bottom.plane is not None and bottom.plane.normal == (0.0, 0.0, -1.0)
    assert bottom.plane.distance_mm == pytest.approx(1.0239248)


def test_shallow_source_side_penetration_does_not_create_opposite_fragment():
    index = _index(_region("Rigid", ((0, 0), (1000, 0), (1000, 1000), (0, 1000))))
    bounds = (-1.0, -1.0, -0.2, 1.0, 1.0, 2.0)

    top = resolve_component_visibility(
        index,
        anchor_mm=(12.7, 12.7),
        bounds_local_mm=bounds,
        authored_side="top",
        requested_side="top",
    )
    bottom = resolve_component_visibility(
        index,
        anchor_mm=(12.7, 12.7),
        bounds_local_mm=bounds,
        authored_side="top",
        requested_side="bottom",
    )

    assert top.action is ComponentVisibilityAction.RENDER_CLIPPED
    assert bottom.action is ComponentVisibilityAction.OMIT
    assert bottom.reason == "clipped-fragment-empty"


def test_wholly_visible_body_skips_native_clipping_and_opposite_body_is_empty():
    index = _index(_region("Rigid", ((0, 0), (1000, 0), (1000, 1000), (0, 1000))))
    bounds = (-1.0, -1.0, 0.1, 1.0, 1.0, 2.0)

    top = resolve_component_visibility(
        index,
        anchor_mm=(12.7, 12.7),
        bounds_local_mm=bounds,
        authored_side="top",
        requested_side="top",
    )
    bottom = resolve_component_visibility(
        index,
        anchor_mm=(12.7, 12.7),
        bounds_local_mm=bounds,
        authored_side="top",
        requested_side="bottom",
    )

    assert top.action is ComponentVisibilityAction.RENDER_UNCLIPPED
    assert bottom.action is ComponentVisibilityAction.OMIT


def test_open_space_index_proves_interior_bounds_and_keeps_opening_candidates():
    index = _index(
        _region("Rigid", ((0, 0), (1000, 0), (1000, 1000), (0, 1000)))
    )
    opening = (480.0, 480.0, 520.0, 520.0)
    open_space = _BoardOpenSpaceIndex(index, (opening,))
    bounds = (-1.0, -1.0, 0.1, 1.0, 1.0, 2.0)

    assert not open_space.may_intersect(anchor_mm=(6.35, 6.35), bounds_local_mm=bounds)
    assert open_space.may_intersect(anchor_mm=(12.7, 12.7), bounds_local_mm=bounds)
    assert open_space.may_intersect(anchor_mm=(0.0, 12.7), bounds_local_mm=bounds)


def test_open_space_domain_changes_clipping_aware_render_key():
    index = _index(
        _region("Rigid", ((0, 0), (1000, 0), (1000, 1000), (0, 1000)))
    )
    component = IllustrationComponent(
        "SMT",
        (12.7, 12.7),
        (),
        (),
        resolved_bounds=(-1.0, -1.0, 0.1, 1.0, 1.0, 2.0),
        authored_side="top",
    )
    closed = IllustrationJob(
        None, region_index=index, open_space_index=_BoardOpenSpaceIndex(index, ())
    )
    opened = IllustrationJob(
        None,
        region_index=index,
        open_space_index=_BoardOpenSpaceIndex(
            index, ((480.0, 480.0, 520.0, 520.0),)
        ),
    )

    assert closed._render_keys(component, "bottom", True) != opened._render_keys(
        component, "bottom", True
    )


@pytest.mark.parametrize(
    "outer,cutouts",
    [
        (
            ((0, 0), (1000, 1000), (0, 1000), (1000, 0)),
            (),
        ),
        (
            ((0, 0), (1000, 0), (1000, 1000), (0, 1000)),
            (((0, 400), (200, 400), (200, 600), (0, 600)),),
        ),
    ],
)
def test_invalid_or_touching_board_topology_never_proves_hidden_geometry(
    outer, cutouts
):
    def ring(points):
        return tuple(
            SimpleNamespace(x_mils=x, y_mils=y, is_arc=False) for x, y in points
        )

    pcb = SimpleNamespace(
        board=SimpleNamespace(
            outline=SimpleNamespace(
                vertices=ring(outer), cutouts=tuple(ring(points) for points in cutouts)
            )
        )
    )
    geometry, _clearance, trusted = _board_material_geometry(pcb)
    index = _index(_region("Rigid", ((0, 0), (1000, 0), (1000, 1000), (0, 1000))))
    open_space = _BoardOpenSpaceIndex(
        index,
        (),
        material_geometry=geometry,
        material_geometry_trusted=trusted,
    )

    assert geometry is None
    assert not trusted
    assert open_space.may_intersect(
        anchor_mm=(12.7, 12.7),
        bounds_local_mm=(-1.0, -1.0, 0.1, 1.0, 1.0, 2.0),
    )


def test_hidden_interior_body_omits_invisible_aperture_projection():
    index = _index(
        _region("Rigid", ((0, 0), (1000, 0), (1000, 1000), (0, 1000)))
    )
    bounds = (-1.0, -1.0, 0.1, 1.0, 1.0, 2.0)
    component = IllustrationComponent(
        "SMT",
        (12.7, 12.7),
        (),
        (),
        resolved_bounds=bounds,
        authored_side="top",
    )
    uncut = IllustrationSymbol(
        '<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0L1 1"/></svg>',
        0.0,
        0.0,
        1.0,
        {},
        (),
        source_bounds_mm=bounds,
    )
    job = IllustrationJob(
        None,
        region_index=index,
        open_space_index=_BoardOpenSpaceIndex(index, ()),
    )

    result = job._apply_direct_visibility(component, None, uncut, "bottom", True)

    assert result.empty
    assert result.aperture is None


def test_opposite_side_fact_skips_hidden_interior_direct_projection(monkeypatch):
    index = _index(
        _region("Rigid", ((0, 0), (1000, 0), (1000, 1000), (0, 1000)))
    )
    bounds = (-1.0, -1.0, 0.1, 1.0, 1.0, 2.0)
    source = g.AnalyticIllustrationSourceA0(
        kind="analytic",
        scene=g.AnalyticSceneA0(definitions=(), occurrences=()),
        lowering=g.AnalyticLoweringOptionsA0(),
    )
    component = IllustrationComponent(
        "SMT",
        (12.7, 12.7),
        (),
        (),
        direct=DirectIllustrationSource(source, None, "smt", "smt"),
        authored_side="top",
    )
    calls = []

    def render(self, source, model, side, illustrate, **kwargs):
        calls.append(side)
        return IllustrationSymbol(
            '<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0L1 1"/></svg>',
            0.0,
            0.0,
            1.0,
            {},
            (),
            source_bounds_mm=bounds,
        )

    monkeypatch.setattr(IllustrationJob, "_render_direct_source", render)
    job = IllustrationJob(
        None,
        region_index=index,
        open_space_index=_BoardOpenSpaceIndex(index, ()),
    )

    assert not job._render_native(component, side="top", illustrate=True).empty
    assert job._render_native(component, side="bottom", illustrate=True).empty
    assert calls == ["top"]


@pytest.mark.parametrize("unsafe_geometry", ["edge", "cutout"])
def test_edge_and_cutout_overhang_reuse_resolved_region_plane(unsafe_geometry):
    holes = (
        (((450, 450), (550, 450), (550, 550), (450, 550)),)
        if unsafe_geometry == "cutout"
        else ()
    )
    index = _index(
        _region(
            "Rigid",
            ((0, 0), (1000, 0), (1000, 1000), (0, 1000)),
            holes=holes,
        )
    )
    anchor = (0.0, 12.7) if unsafe_geometry == "edge" else (12.7, 12.7)
    bounds = (-1.0, -1.0, -2.0, 1.0, 1.0, 2.0)

    top = resolve_component_visibility(
        index,
        anchor_mm=anchor,
        bounds_local_mm=bounds,
        authored_side="top",
        requested_side="top",
    )
    bottom = resolve_component_visibility(
        index,
        anchor_mm=anchor,
        bounds_local_mm=bounds,
        authored_side="top",
        requested_side="bottom",
    )

    if unsafe_geometry == "edge":
        assert top.action is ComponentVisibilityAction.RENDER_CLIPPED
        assert bottom.action is ComponentVisibilityAction.RENDER_CLIPPED
        assert top.reason == bottom.reason == "body-crosses-board-surface"
        assert top.plane is not None and bottom.plane is not None
    else:
        assert top.action is ComponentVisibilityAction.RENDER_UNCLIPPED
        assert top.reason == "board-region-outside:mounting-side-fallback"
        assert bottom.action is ComponentVisibilityAction.OMIT
        assert bottom.reason == "board-region-outside:opposite-side-unsafe"
        assert top.plane is None and bottom.plane is None


def test_cross_region_different_envelopes_cannot_form_one_plane():
    index = _index(
        _region("Rigid", ((0, 0), (500, 0), (500, 1000), (0, 1000))),
        _region(
            "Flex",
            ((500, 0), (1000, 0), (1000, 1000), (500, 1000)),
            thickness_mils=4.0,
        ),
    )
    result = resolve_component_visibility(
        index,
        anchor_mm=(12.7, 12.7),
        bounds_local_mm=(-1.0, -1.0, -2.0, 1.0, 1.0, 2.0),
        authored_side="top",
        requested_side="bottom",
    )

    assert result.action is ComponentVisibilityAction.OMIT
    assert result.reason == "board-region-ambiguous:opposite-side-unsafe"


@pytest.mark.parametrize("placement", ["cutout", "outside"])
def test_wholly_open_space_body_preserves_uncut_aperture_projection(placement):
    hole = ((400, 400), (600, 400), (600, 600), (400, 600))
    index = _index(
        _region(
            "Rigid",
            ((0, 0), (1000, 0), (1000, 1000), (0, 1000)),
            holes=(hole,),
        )
    )
    anchor = (12.7, 12.7) if placement == "cutout" else (27.94, 12.7)
    bounds = (-1.0, -1.0, -2.0, 1.0, 1.0, 2.0)
    component = IllustrationComponent(
        "OPEN",
        anchor,
        (),
        (),
        resolved_bounds=bounds,
        authored_side="top",
    )
    uncut = IllustrationSymbol(
        '<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0L1 0L0 1Z"/></svg>',
        0.0,
        0.0,
        1.0,
        {},
        (),
        source_bounds_mm=bounds,
    )

    result = IllustrationJob(None, region_index=index)._apply_direct_visibility(
        component, None, uncut, "bottom", True
    )

    assert result.svg == ""
    assert result.aperture is not None
    assert result.aperture.svg == uncut.svg
    assert result.aperture_source_bounds_mm == bounds


def test_incompatible_envelopes_do_not_erase_open_space_projection():
    index = _index(
        _region("Rigid", ((0, 0), (500, 0), (500, 1000), (0, 1000))),
        _region(
            "Flex",
            ((500, 0), (1000, 0), (1000, 1000), (500, 1000)),
            thickness_mils=4.0,
        ),
    )
    # Cross both incompatible slabs and the lower board edge. The surface
    # branch is unsafe, while the uncut projection must remain available to
    # the SVG compositor's outside-board aperture mask.
    bounds = (-2.0, -2.0, -2.0, 2.0, 2.0, 2.0)
    component = IllustrationComponent(
        "MIXED",
        (12.7, 0.5),
        (),
        (),
        resolved_bounds=bounds,
        authored_side="top",
    )
    uncut = IllustrationSymbol(
        '<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0L1 0L0 1Z"/></svg>',
        0.0,
        0.0,
        1.0,
        {},
        (),
        source_bounds_mm=bounds,
    )

    result = IllustrationJob(None, region_index=index)._apply_direct_visibility(
        component, None, uncut, "bottom", True
    )

    assert result.svg == ""
    assert result.aperture is not None
    assert result.aperture_source_bounds_mm == bounds


def test_clipping_policy_rejects_nonfinite_or_reversed_bounds():
    index = _index(_region("Rigid", ((0, 0), (1000, 0), (1000, 1000), (0, 1000))))
    with pytest.raises(ValueError, match="finite"):
        resolve_component_visibility(
            index,
            anchor_mm=(0.0, 0.0),
            bounds_local_mm=(0, 0, 0, 1, 1, float("nan")),
            authored_side="top",
            requested_side="top",
        )
    with pytest.raises(ValueError, match="minima"):
        resolve_component_visibility(
            index,
            anchor_mm=(0.0, 0.0),
            bounds_local_mm=(1, 0, 0, 0, 1, 1),
            authored_side="top",
            requested_side="top",
        )


@pytest.mark.parametrize(("side", "expected_x"), (("top", 4.7), ("bottom", -10.3)))
def test_mesh_svg_canvas_uses_projected_fragment_bounds_after_clipping(
    side, expected_x
):
    """A narrow clipped fragment must not be stretched over full model bounds."""

    @dataclass(frozen=True)
    class Stats:
        triangles: int = 1

    class Client:
        def mesh_hlr_projection(self, collection, request, **kwargs):
            assert request.output_bbox
            bounds = SimpleNamespace(
                min_x=5.0,
                min_y=0.0,
                max_x=10.0,
                max_y=2.0,
                width=5.0,
                height=2.0,
            )
            modes = SimpleNamespace(
                outline=SimpleNamespace(segments=()),
                bbox=SimpleNamespace(bounds=bounds),
            )
            return SimpleNamespace(
                views=(SimpleNamespace(id=request.views[0].id, modes=modes),),
                empty=False,
            )

        def mesh_illustration(self, value, **kwargs):
            return SimpleNamespace(
                svg='<svg xmlns="http://www.w3.org/2000/svg"/>',
                stats=Stats(),
                warnings=(),
                empty=False,
            )

    mesh = g.MeshIllustrationMesh(
        id="sloped-pin",
        positions=(0.0, 0.0, -1.0, 10.0, 0.0, 1.0, 10.0, 2.0, 1.0),
        materials=(g.MeshIllustrationMaterial(color=(0.7, 0.7, 0.7)),),
    )
    component = IllustrationComponent("P1", (0.0, 0.0), (mesh,), ())
    symbol = IllustrationJob(Client()).render(component, side=side)

    # The Geometer SVG has a 1,000,000-unit square canvas with 6% padding.
    # Its placement must use the 5 mm projected fragment, not the 10 mm source.
    assert symbol.x_mm == pytest.approx(expected_x)
    assert symbol.y_mm == pytest.approx(-2.3)
    assert symbol.mm_per_unit == pytest.approx(5e-6)
