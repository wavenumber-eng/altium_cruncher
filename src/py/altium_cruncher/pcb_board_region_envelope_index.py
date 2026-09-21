"""Temporary board-space region to physical-stack-envelope query.

Altium Monkey owns layer-stack parsing and envelope resolution.  Cruncher owns
only the spatial join in this module until altium_monkey_dev issue 95 ships a
public board-coordinate query.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from math import isfinite
from typing import TYPE_CHECKING, Callable, Iterable, Protocol, cast

from shapely.geometry import Point, Polygon, box
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

if TYPE_CHECKING:
    from altium_monkey.altium_resolved_layer_stack import ResolvedStackEnvelope


class _LayerStackDocumentLike(Protocol):
    @property
    def board_regions(self) -> Iterable[object]: ...


class _ResolvedLayerStackLike(Protocol):
    def stack_envelope_for_board_region(
        self, region: object
    ) -> ResolvedStackEnvelope | None: ...

    def substack_for_board_region(self, region: object) -> object | None: ...


_INTERNAL_UNITS_PER_MIL = 10000.0
_DEFAULT_TOLERANCE_MILS = 1e-6
_ENVELOPE_COMPARE_DIGITS = 9


class BoardRegionQueryStatus(StrEnum):
    """Typed outcomes for a board-space envelope query."""

    RESOLVED = "resolved"
    OUTSIDE = "outside"
    AMBIGUOUS = "ambiguous"
    INVALID = "invalid"


@dataclass(frozen=True)
class BoardRegionEnvelope:
    """One valid board region joined to its resolved physical envelope."""

    source_index: int
    name: str
    layerstack_id: str
    substack_name: str
    is_flex: bool | None
    outline_mils: tuple[tuple[float, float], ...]
    holes_mils: tuple[tuple[tuple[float, float], ...], ...]
    bounds_mils: tuple[float, float, float, float]
    envelope: ResolvedStackEnvelope
    _geometry: BaseGeometry = field(repr=False, compare=False)

    @property
    def total_thickness_mils(self) -> float:
        return float(self.envelope.total_thickness_mils)

    @property
    def top_surface_z_mils(self) -> float:
        """Top surface in Cruncher's top-surface-zero board frame."""

        return 0.0

    @property
    def bottom_surface_z_mils(self) -> float:
        """Bottom surface in Cruncher's top-surface-zero board frame."""

        return -self.total_thickness_mils


@dataclass(frozen=True)
class InvalidBoardRegion:
    """Region rejected before spatial lookup, retained for safe diagnostics."""

    source_index: int
    name: str
    layerstack_id: str
    reason: str
    bounds_mils: tuple[float, float, float, float] | None = None


@dataclass(frozen=True)
class BoardRegionEnvelopeQuery:
    """Result of a point or conservative bounds query."""

    status: BoardRegionQueryStatus
    region: BoardRegionEnvelope | None = None
    matches: tuple[BoardRegionEnvelope, ...] = ()
    invalid_regions: tuple[InvalidBoardRegion, ...] = ()
    detail: str = ""
    fully_covered: bool = False

    @property
    def envelope(self) -> ResolvedStackEnvelope | None:
        return None if self.region is None else self.region.envelope


class BoardRegionEnvelopeIndex:
    """Immutable spatial index over source-aware Altium board regions."""

    def __init__(
        self,
        regions: Iterable[BoardRegionEnvelope],
        *,
        invalid_regions: Iterable[InvalidBoardRegion] = (),
        tolerance_mils: float = _DEFAULT_TOLERANCE_MILS,
    ) -> None:
        if not isfinite(tolerance_mils) or tolerance_mils < 0.0:
            raise ValueError("tolerance_mils must be finite and non-negative")
        self.regions = tuple(regions)
        self.invalid_regions = tuple(invalid_regions)
        self.tolerance_mils = float(tolerance_mils)

    @property
    def complete_partition_bounds_mils(
        self,
    ) -> tuple[float, float, float, float] | None:
        """Return the complete valid region partition envelope, if available."""

        if not self.regions or self.invalid_regions:
            return None
        return (
            min(region.bounds_mils[0] for region in self.regions),
            min(region.bounds_mils[1] for region in self.regions),
            max(region.bounds_mils[2] for region in self.regions),
            max(region.bounds_mils[3] for region in self.regions),
        )

    @classmethod
    def from_pcbdoc(
        cls,
        pcbdoc: object,
        *,
        tolerance_mils: float = _DEFAULT_TOLERANCE_MILS,
    ) -> "BoardRegionEnvelopeIndex":
        """Build the temporary index from Monkey's public semantic models."""

        from altium_monkey.altium_layer_stack_document import AltiumLayerStackDocument

        document = AltiumLayerStackDocument.from_pcbdoc(pcbdoc)
        resolved = cast(_ResolvedLayerStackLike, document.to_resolved_layer_stack())
        return cls.from_layer_stack_document(
            cast(_LayerStackDocumentLike, document),
            resolved,
            tolerance_mils=tolerance_mils,
        )

    @classmethod
    def from_layer_stack_document(
        cls,
        document: object,
        resolved: object,
        *,
        tolerance_mils: float = _DEFAULT_TOLERANCE_MILS,
    ) -> "BoardRegionEnvelopeIndex":
        document_view = cast(_LayerStackDocumentLike, document)
        resolved_view = cast(_ResolvedLayerStackLike, resolved)
        regions: list[BoardRegionEnvelope] = []
        invalid: list[InvalidBoardRegion] = []
        for source_index, source in enumerate(tuple(document_view.board_regions or ())):
            record, error = _build_region(source_index, source, resolved_view)
            if record is not None:
                regions.append(record)
            elif error is not None:
                invalid.append(error)
        return cls(
            regions,
            invalid_regions=invalid,
            tolerance_mils=tolerance_mils,
        )

    def query_point(self, x_mils: float, y_mils: float) -> BoardRegionEnvelopeQuery:
        """Resolve the physical envelope at one board-space point in mils."""

        if not isfinite(x_mils) or not isfinite(y_mils):
            return BoardRegionEnvelopeQuery(
                BoardRegionQueryStatus.INVALID,
                detail="query point must contain finite board-space coordinates",
            )
        point = Point(float(x_mils), float(y_mils))
        return self._query_geometry(
            point,
            lambda geometry: (
                geometry.covers(point)
                or geometry.distance(point) <= self.tolerance_mils
            ),
        )

    def query_bounds(
        self,
        min_x_mils: float,
        min_y_mils: float,
        max_x_mils: float,
        max_y_mils: float,
    ) -> BoardRegionEnvelopeQuery:
        """Conservatively resolve all regions touched by an XY bounds box."""

        values = (min_x_mils, min_y_mils, max_x_mils, max_y_mils)
        if not all(isfinite(value) for value in values):
            return BoardRegionEnvelopeQuery(
                BoardRegionQueryStatus.INVALID,
                detail="query bounds must contain finite board-space coordinates",
            )
        if max_x_mils < min_x_mils or max_y_mils < min_y_mils:
            return BoardRegionEnvelopeQuery(
                BoardRegionQueryStatus.INVALID,
                detail="query bounds minimum must not exceed maximum",
            )
        if min_x_mils == max_x_mils and min_y_mils == max_y_mils:
            return self.query_point(min_x_mils, min_y_mils)
        query_geometry = box(
            float(min_x_mils),
            float(min_y_mils),
            float(max_x_mils),
            float(max_y_mils),
        )
        return self._query_geometry(
            query_geometry,
            lambda geometry: (
                geometry.intersects(query_geometry)
                or geometry.distance(query_geometry) <= self.tolerance_mils
            ),
        )

    def fully_contains_bounds(
        self,
        min_x_mils: float,
        min_y_mils: float,
        max_x_mils: float,
        max_y_mils: float,
        *,
        clearance_mils: float = 0.0,
    ) -> bool:
        """Return whether valid board material strictly contains a bounds box."""

        if not isfinite(clearance_mils) or clearance_mils < 0.0:
            raise ValueError("clearance_mils must be finite and non-negative")
        query = self.query_bounds(min_x_mils, min_y_mils, max_x_mils, max_y_mils)
        if query.status in {BoardRegionQueryStatus.INVALID, BoardRegionQueryStatus.OUTSIDE}:
            return False
        geometry = box(min_x_mils, min_y_mils, max_x_mils, max_y_mils)
        coverage = unary_union(tuple(item._geometry for item in query.matches))
        if clearance_mils > 0.0:
            coverage = coverage.buffer(-clearance_mils)
        return bool(not coverage.is_empty and coverage.covers(geometry))

    def _query_geometry(
        self,
        query_geometry: BaseGeometry,
        matches_geometry: Callable[[BaseGeometry], bool],
    ) -> BoardRegionEnvelopeQuery:
        invalid_hits = tuple(
            item
            for item in self.invalid_regions
            if item.bounds_mils is None
            or box(*item.bounds_mils).intersects(query_geometry)
        )
        matches = tuple(
            sorted(
                (item for item in self.regions if matches_geometry(item._geometry)),
                key=_canonical_region_key,
            )
        )
        if invalid_hits:
            return BoardRegionEnvelopeQuery(
                BoardRegionQueryStatus.INVALID,
                matches=matches,
                invalid_regions=invalid_hits,
                detail="query intersects region geometry that could not be resolved",
            )
        if not matches:
            return BoardRegionEnvelopeQuery(
                BoardRegionQueryStatus.OUTSIDE,
                detail="query does not intersect a resolved board region",
            )
        signatures = {_envelope_signature(item) for item in matches}
        if len(signatures) != 1:
            return BoardRegionEnvelopeQuery(
                BoardRegionQueryStatus.AMBIGUOUS,
                matches=matches,
                detail="query intersects board regions with different physical envelopes",
            )
        return BoardRegionEnvelopeQuery(
            BoardRegionQueryStatus.RESOLVED,
            region=matches[0],
            matches=matches,
            fully_covered=_fully_covers(
                tuple(item._geometry for item in matches),
                query_geometry,
                self.tolerance_mils,
            ),
            detail=(
                "query intersects equivalent physical envelopes; canonical region selected"
                if len(matches) > 1
                else ""
            ),
        )


def _fully_covers(
    geometries: tuple[BaseGeometry, ...],
    query_geometry: BaseGeometry,
    tolerance_mils: float,
) -> bool:
    if not geometries:
        return False
    coverage = unary_union(geometries)
    if tolerance_mils > 0:
        coverage = coverage.buffer(tolerance_mils)
    return bool(coverage.covers(query_geometry))


def _build_region(
    source_index: int,
    source: object,
    resolved: _ResolvedLayerStackLike,
) -> tuple[BoardRegionEnvelope | None, InvalidBoardRegion | None]:
    name, layerstack_id = _region_identity(source_index, source)
    outline, holes, bounds, geometry, geometry_error = _source_region_geometry(source)
    if geometry_error is not None or geometry is None:
        return None, _invalid_region(
            source_index,
            name,
            layerstack_id,
            bounds,
            geometry_error or "region polygon could not be constructed",
        )
    envelope = resolved.stack_envelope_for_board_region(source)
    envelope_error = _envelope_error(envelope)
    if envelope_error is not None:
        return None, _invalid_region(
            source_index,
            name,
            layerstack_id,
            bounds,
            envelope_error,
        )
    assert envelope is not None
    substack = resolved.substack_for_board_region(source)
    geometry_bounds = geometry.bounds
    return (
        BoardRegionEnvelope(
            source_index=source_index,
            name=name,
            layerstack_id=layerstack_id,
            substack_name=str(getattr(substack, "name", "") or envelope.substack_name),
            is_flex=getattr(substack, "is_flex", envelope.is_flex),
            outline_mils=outline,
            holes_mils=holes,
            bounds_mils=(
                float(geometry_bounds[0]),
                float(geometry_bounds[1]),
                float(geometry_bounds[2]),
                float(geometry_bounds[3]),
            ),
            envelope=envelope,
            _geometry=geometry,
        ),
        None,
    )


def _region_identity(source_index: int, source: object) -> tuple[str, str]:
    name = str(getattr(source, "name", "") or f"Board region {source_index + 1}")
    layerstack_id = str(getattr(source, "layerstack_id", "") or "")
    return name, layerstack_id


def _source_region_geometry(
    source: object,
) -> tuple[
    tuple[tuple[float, float], ...],
    tuple[tuple[tuple[float, float], ...], ...],
    tuple[float, float, float, float] | None,
    Polygon | None,
    str | None,
]:
    outline = _ring_mils(getattr(source, "outline_vertices", ()))
    holes = tuple(
        ring
        for values in tuple(getattr(source, "hole_vertices", ()) or ())
        if (ring := _ring_mils(values))
    )
    bounds = _ring_bounds(outline)
    geometry, error = _validated_region_geometry(outline, holes)
    return outline, holes, bounds, geometry, error


def _validated_region_geometry(
    outline: tuple[tuple[float, float], ...],
    holes: tuple[tuple[tuple[float, float], ...], ...],
) -> tuple[Polygon | None, str | None]:
    if len(set(outline)) < 3:
        return None, "region outline has fewer than three unique finite vertices"
    geometry = Polygon(outline, holes)
    if geometry.is_empty or geometry.area <= 0.0:
        return None, "region outline has no positive area"
    if not geometry.is_valid:
        return None, "region outline or holes form invalid polygon topology"
    return geometry, None


def _envelope_error(envelope: object | None) -> str | None:
    if envelope is None:
        return "region layer-stack reference has no finite physical envelope"
    thickness = float(getattr(envelope, "total_thickness_mils", float("nan")))
    if not isfinite(thickness):
        return "region layer-stack reference has no finite physical envelope"
    if thickness <= 0.0:
        return "region physical envelope has non-positive thickness"
    return None


def _invalid_region(
    source_index: int,
    name: str,
    layerstack_id: str,
    bounds_mils: tuple[float, float, float, float] | None,
    reason: str,
) -> InvalidBoardRegion:
    return InvalidBoardRegion(
        source_index=source_index,
        name=name,
        layerstack_id=layerstack_id,
        reason=reason,
        bounds_mils=bounds_mils,
    )


def _ring_mils(
    values: Iterable[tuple[float, float]],
) -> tuple[tuple[float, float], ...]:
    points: list[tuple[float, float]] = []
    for raw_x, raw_y in tuple(values or ()):
        x = float(raw_x) / _INTERNAL_UNITS_PER_MIL
        y = float(raw_y) / _INTERNAL_UNITS_PER_MIL
        if isfinite(x) and isfinite(y):
            points.append((x, y))
    if len(points) > 1 and points[0] == points[-1]:
        points.pop()
    return tuple(points)


def _ring_bounds(
    points: tuple[tuple[float, float], ...],
) -> tuple[float, float, float, float] | None:
    if not points:
        return None
    xs = tuple(point[0] for point in points)
    ys = tuple(point[1] for point in points)
    return min(xs), min(ys), max(xs), max(ys)


def _canonical_region_key(region: BoardRegionEnvelope) -> tuple[str, str, int]:
    return region.layerstack_id.upper(), region.name.casefold(), region.source_index


def _envelope_signature(region: BoardRegionEnvelope) -> tuple[object, ...]:
    # Cruncher's clipping coordinate system deliberately normalizes every
    # region to top Z=0 and bottom Z=-thickness. Source stack Z-zero choices
    # remain diagnostic metadata, but cannot make equal physical slabs
    # ambiguous at a shared boundary.
    return (round(float(region.total_thickness_mils), _ENVELOPE_COMPARE_DIGITS),)
