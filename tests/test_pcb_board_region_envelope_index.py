"""Temporary Cruncher board-region envelope query coverage."""

from pathlib import Path
from dataclasses import dataclass
from types import SimpleNamespace

from altium_monkey.altium_layer_stack_document import AltiumStackRegion
from altium_monkey.altium_pcbdoc import AltiumPcbDoc
from altium_monkey.altium_resolved_layer_stack import ResolvedStackEnvelope
import pytest

from altium_cruncher.pcb_board_region_envelope_index import (
    BoardRegionEnvelopeIndex,
    BoardRegionQueryStatus,
)


ROOT = Path(__file__).resolve().parents[1]
BLUETOOTH = (
    ROOT
    / "tests/assets/projects/bluetooth_sentinel_flex/input/Bluetooth_Sentinel.PcbDoc"
)


def _region(
    name: str,
    stack_id: str,
    points_mils: tuple[tuple[float, float], ...],
    *,
    holes_mils: tuple[tuple[tuple[float, float], ...], ...] = (),
) -> AltiumStackRegion:
    scale = 10000.0
    return AltiumStackRegion(
        name=name,
        layerstack_id=stack_id,
        outline_vertices=tuple((x * scale, y * scale) for x, y in points_mils),
        hole_vertices=tuple(
            tuple((x * scale, y * scale) for x, y in hole) for hole in holes_mils
        ),
    )


def _envelope(stack_id: str, thickness: float) -> ResolvedStackEnvelope:
    return ResolvedStackEnvelope(
        source_stackup_ref=stack_id,
        substack_name=stack_id,
        is_flex=stack_id == "flex",
        z_zero="substack_midplane",
        total_thickness_mils=thickness,
        top_z_mils=thickness / 2.0,
        bottom_z_mils=-thickness / 2.0,
    )


class _Resolved:
    def __init__(self, thickness_by_stack: dict[str, float]) -> None:
        self.thickness_by_stack = thickness_by_stack

    def stack_envelope_for_board_region(
        self, region: object
    ) -> ResolvedStackEnvelope | None:
        assert isinstance(region, AltiumStackRegion)
        thickness = self.thickness_by_stack.get(region.layerstack_id)
        return None if thickness is None else _envelope(region.layerstack_id, thickness)

    def substack_for_board_region(self, region: object) -> object | None:
        assert isinstance(region, AltiumStackRegion)
        if region.layerstack_id not in self.thickness_by_stack:
            return None
        return SimpleNamespace(
            name=region.layerstack_id,
            is_flex=region.layerstack_id == "flex",
        )



@dataclass
class _Document:
    board_regions: tuple[AltiumStackRegion, ...]


def _index(*regions: AltiumStackRegion, thickness=None) -> BoardRegionEnvelopeIndex:
    document = _Document(board_regions=regions)
    return BoardRegionEnvelopeIndex.from_layer_stack_document(
        document,
        _Resolved(thickness or {"rigid": 32.0, "flex": 4.0}),
    )


def test_point_query_resolves_region_holes_and_normalized_surfaces():
    index = _index(
        _region(
            "Rigid",
            "rigid",
            ((0, 0), (10, 0), (10, 10), (0, 10)),
            holes_mils=(((4, 4), (6, 4), (6, 6), (4, 6)),),
        )
    )

    resolved = index.query_point(2, 3)
    assert resolved.status is BoardRegionQueryStatus.RESOLVED
    assert resolved.region is not None
    assert resolved.region.total_thickness_mils == 32.0
    assert resolved.region.top_surface_z_mils == 0.0
    assert resolved.region.bottom_surface_z_mils == -32.0
    assert resolved.fully_covered is True
    assert index.query_point(5, 5).status is BoardRegionQueryStatus.OUTSIDE
    assert index.query_point(20, 20).status is BoardRegionQueryStatus.OUTSIDE


def test_equal_envelope_boundary_selects_canonical_region_not_source_order():
    left = _region("B", "rigid", ((0, 0), (5, 0), (5, 5), (0, 5)))
    right = _region("A", "rigid", ((5, 0), (10, 0), (10, 5), (5, 5)))

    result = _index(left, right).query_point(5, 2)

    assert result.status is BoardRegionQueryStatus.RESOLVED
    assert result.region is not None
    assert result.region.name == "A"
    assert {item.name for item in result.matches} == {"A", "B"}
    assert "canonical" in result.detail
    assert result.fully_covered is True


def test_different_envelopes_are_ambiguous_for_point_and_spanning_bounds():
    rigid = _region("Rigid", "rigid", ((0, 0), (5, 0), (5, 5), (0, 5)))
    flex = _region("Flex", "flex", ((5, 0), (10, 0), (10, 5), (5, 5)))
    index = _index(rigid, flex)

    assert index.query_point(5, 2).status is BoardRegionQueryStatus.AMBIGUOUS
    assert index.query_bounds(4, 1, 6, 4).status is BoardRegionQueryStatus.AMBIGUOUS
    assert index.query_bounds(1, 1, 4, 4).status is BoardRegionQueryStatus.RESOLVED


def test_bounds_coverage_distinguishes_safe_slab_clipping_from_overhangs_and_holes():
    index = _index(
        _region(
            "Rigid",
            "rigid",
            ((0, 0), (10, 0), (10, 10), (0, 10)),
            holes_mils=(((4, 4), (6, 4), (6, 6), (4, 6)),),
        )
    )

    assert index.query_bounds(1, 1, 3, 3).fully_covered is True
    assert index.query_bounds(-1, 1, 3, 3).fully_covered is False
    assert index.query_bounds(3, 3, 7, 7).fully_covered is False


def test_invalid_region_is_a_typed_safe_failure():
    invalid = _region("Broken", "missing", ((0, 0), (10, 0), (10, 10)))
    result = _index(invalid).query_point(2, 2)

    assert result.status is BoardRegionQueryStatus.INVALID
    assert len(result.invalid_regions) == 1
    assert "envelope" in result.invalid_regions[0].reason


def test_non_finite_or_reversed_queries_are_invalid():
    index = _index(_region("Rigid", "rigid", ((0, 0), (5, 0), (0, 5))))

    assert index.query_point(float("nan"), 0).status is BoardRegionQueryStatus.INVALID
    assert index.query_bounds(2, 2, 1, 1).status is BoardRegionQueryStatus.INVALID


@pytest.mark.slow
def test_bluetooth_sentinel_resolves_rigid_and_flex_region_envelopes():
    pcbdoc = AltiumPcbDoc.from_file(BLUETOOTH)
    index = BoardRegionEnvelopeIndex.from_pcbdoc(pcbdoc)

    rigid_2 = index.query_point(60605.31505151517, 40082.82176948154)
    rigid_1 = index.query_point(60605.31313726855, 38830.56313808814)
    flex = index.query_point(60590.162861537574, 39449.11769487287)

    assert rigid_2.status is BoardRegionQueryStatus.RESOLVED
    assert rigid_1.status is BoardRegionQueryStatus.RESOLVED
    assert flex.status is BoardRegionQueryStatus.RESOLVED
    assert rigid_2.region is not None and rigid_2.region.name == "Layer Stack Region 2"
    assert rigid_1.region is not None and rigid_1.region.name == "Layer Stack Region 1"
    assert flex.region is not None and flex.region.name == "Layer Stack Region 3"
    assert rigid_2.region.total_thickness_mils == pytest.approx(32.1455)
    assert rigid_1.region.total_thickness_mils == pytest.approx(32.1455)
    assert flex.region.total_thickness_mils == pytest.approx(3.3267)
    assert rigid_2.region.is_flex is False
    assert flex.region.is_flex is True
