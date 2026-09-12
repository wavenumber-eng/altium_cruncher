"""Designator fitting ported unchanged from pcb-autodoc/cca_designator_layout.py.

Only the source geometry type is adapted locally; fitting and cache rules match
the reference application. Coordinates are millimeters with SVG Y down.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass

from shapely import affinity, prepare
from shapely.geometry import LineString, Point, box
from shapely.geometry.base import BaseGeometry
from shapely.ops import polygonize, unary_union


Segment = tuple[tuple[float, float], tuple[float, float]]

@dataclass(frozen=True, slots=True)
class CcaComponentGeometryFact:
    bounds_mm: tuple[float, float, float, float]
    line_segments_mm: tuple[Segment, ...] = ()
    bounds_kind: str = "model"
    annotation_bounds_mm: tuple[float, float, float, float] | None = None
    annotation_line_segments_mm: tuple[Segment, ...] = ()


_TEXT_ADVANCE_PER_CHARACTER = 0.62
_CENTER_GRID_DIVISIONS = 4
_BINARY_SEARCH_STEPS = 12
_LAST_SESSION_TELEMETRY: dict[str, int | float] = {}


@dataclass(frozen=True, slots=True)
class CcaDesignatorFit:
    center_mm: tuple[float, float]
    font_size_mm: float
    rotation_degrees: float


@dataclass(slots=True)
class CcaDesignatorFitTelemetry:
    requests: int = 0
    hits: int = 0
    misses: int = 0
    elapsed_seconds: float = 0.0

    def as_dict(self) -> dict[str, int | float]:
        return {
            "requests": self.requests,
            "hits": self.hits,
            "misses": self.misses,
            "elapsed_seconds": round(self.elapsed_seconds, 6),
        }


class CcaDesignatorFitSession:
    """Reuse complete relative fits across translated equivalent silhouettes."""

    def __init__(self) -> None:
        self._fits: dict[tuple[object, ...], CcaDesignatorFit | None] = {}
        self.telemetry = CcaDesignatorFitTelemetry()

    def fit(
        self,
        *,
        text_length: int,
        segments: tuple[Segment, ...],
        bounds: tuple[float, float, float, float],
        bounds_kind: str,
        fill_ratio: float,
        maximum_font_size_mm: float,
        rotations: tuple[float, ...],
        manual: bool,
    ) -> CcaDesignatorFit | None:
        started_at = time.perf_counter()
        self.telemetry.requests += 1
        anchor, relative_segments, relative_bounds, geometry_key = _relative_geometry_key(
            segments,
            bounds,
        )
        text_aspect = max(1.0, int(text_length) * _TEXT_ADVANCE_PER_CHARACTER)
        key = (
            geometry_key,
            tuple(_quantize(value) for value in relative_bounds),
            str(bounds_kind).casefold(),
            _quantize(text_aspect),
            tuple(_quantize(value) for value in rotations),
            _quantize(fill_ratio),
            _quantize(maximum_font_size_mm),
            "manual" if manual else "automatic",
        )
        if key in self._fits:
            self.telemetry.hits += 1
            relative = self._fits[key]
        else:
            self.telemetry.misses += 1
            relative = _fit_uncached(
                text_aspect=text_aspect,
                segments=relative_segments,
                bounds=relative_bounds,
                bounds_kind=bounds_kind,
                fill_ratio=fill_ratio,
                maximum_font_size_mm=maximum_font_size_mm,
                rotations=rotations,
            )
            self._fits[key] = relative
        self.telemetry.elapsed_seconds += time.perf_counter() - started_at
        if relative is None:
            return None
        return CcaDesignatorFit(
            center_mm=(relative.center_mm[0] + anchor[0], relative.center_mm[1] + anchor[1]),
            font_size_mm=relative.font_size_mm,
            rotation_degrees=relative.rotation_degrees,
        )

    def publish_telemetry(self) -> None:
        _LAST_SESSION_TELEMETRY.clear()
        _LAST_SESSION_TELEMETRY.update(self.telemetry.as_dict())


def designator_fit_telemetry_snapshot() -> dict[str, int | float]:
    return dict(_LAST_SESSION_TELEMETRY)


def reset_designator_fit_telemetry() -> None:
    _LAST_SESSION_TELEMETRY.clear()


def fit_designator_to_geometry(
    designator: str,
    geometry: CcaComponentGeometryFact,
    *,
    fill_ratio: float,
    maximum_font_size_mm: float,
    auto_base_rotation_degrees: float = 0.0,
    manual_rotation_degrees: float | None = None,
    session: CcaDesignatorFitSession | None = None,
) -> CcaDesignatorFit | None:
    """Choose the largest safe fit on either normalized component axis."""

    segments = geometry.annotation_line_segments_mm or geometry.line_segments_mm
    if manual_rotation_degrees is not None:
        rotations = (normalize_designator_axis(manual_rotation_degrees),)
    else:
        primary = normalize_designator_axis(auto_base_rotation_degrees)
        secondary = normalize_designator_axis(primary + 90.0)
        rotations = (primary,) if abs(primary - secondary) <= 1.0e-9 else (primary, secondary)
    active_session = session or CcaDesignatorFitSession()
    raw_bounds = geometry.annotation_bounds_mm or geometry.bounds_mm
    bounds = (
        float(raw_bounds[0]),
        float(raw_bounds[1]),
        float(raw_bounds[2]),
        float(raw_bounds[3]),
    )
    return active_session.fit(
        text_length=len(str(designator)),
        segments=tuple(segments),
        bounds=bounds,
        bounds_kind=str(geometry.bounds_kind),
        fill_ratio=min(1.0, max(0.05, float(fill_ratio))),
        maximum_font_size_mm=max(0.0, float(maximum_font_size_mm)),
        rotations=rotations,
        manual=manual_rotation_degrees is not None,
    )


def normalize_designator_axis(angle_degrees: float) -> float:
    """Normalize an undirected text axis to the readable [-90, 90) range."""

    normalized = (float(angle_degrees) + 90.0) % 180.0 - 90.0
    return 0.0 if abs(normalized) <= 1.0e-12 else normalized


def _fit_uncached(
    *,
    text_aspect: float,
    segments: tuple[Segment, ...],
    bounds: tuple[float, float, float, float],
    bounds_kind: str,
    fill_ratio: float,
    maximum_font_size_mm: float,
    rotations: tuple[float, ...],
) -> CcaDesignatorFit | None:
    region = _annotation_region(segments, bounds=bounds, bounds_kind=bounds_kind)
    if region.is_empty:
        return None
    prepare(region)
    centers = _candidate_centers(region)
    if not centers:
        return None
    best: CcaDesignatorFit | None = None
    for rotation in rotations:
        raw_font, center = _largest_font_at_candidates(
            region,
            centers=centers,
            text_aspect=text_aspect,
            rotation_degrees=rotation,
        )
        font_size = min(maximum_font_size_mm, raw_font * fill_ratio)
        candidate = CcaDesignatorFit(center, font_size, rotation)
        if font_size <= 0.0:
            continue
        # Prefer the larger safe text. When both perpendicular axes fit equally,
        # use the axis closest to document-horizontal for consistent reading.
        if (
            best is None
            or candidate.font_size_mm > best.font_size_mm + 1.0e-6
            or (
                abs(candidate.font_size_mm - best.font_size_mm) <= 1.0e-6
                and abs(candidate.rotation_degrees) < abs(best.rotation_degrees)
            )
        ):
            best = candidate
    return best


def _relative_geometry_key(
    segments: tuple[Segment, ...],
    bounds: tuple[float, float, float, float],
) -> tuple[
    tuple[float, float],
    tuple[Segment, ...],
    tuple[float, float, float, float],
    tuple[tuple[float, float, float, float], ...],
]:
    anchor = float(bounds[0]), float(bounds[1])
    relative_bounds = (
        0.0,
        0.0,
        float(bounds[2]) - anchor[0],
        float(bounds[3]) - anchor[1],
    )
    canonical: set[Segment] = set()
    for start, end in segments:
        relative_start = (float(start[0]) - anchor[0], float(start[1]) - anchor[1])
        relative_end = (float(end[0]) - anchor[0], float(end[1]) - anchor[1])
        canonical.add(
            (relative_start, relative_end)
            if relative_start <= relative_end
            else (relative_end, relative_start)
        )
    relative_segments = tuple(sorted(canonical))
    geometry_key = tuple(
        (
            _quantize(start[0]),
            _quantize(start[1]),
            _quantize(end[0]),
            _quantize(end[1]),
        )
        for start, end in relative_segments
    )
    return anchor, relative_segments, relative_bounds, geometry_key


def _quantize(value: float) -> float:
    rounded = round(float(value), 9)
    return 0.0 if rounded == 0.0 else rounded


def _annotation_region(
    segments: tuple[Segment, ...],
    *,
    bounds: tuple[float, float, float, float],
    bounds_kind: str,
) -> BaseGeometry:
    lines = tuple(
        LineString((start, end)) for start, end in segments if math.dist(start, end) > 1.0e-9
    )
    polygons = tuple(polygonize(unary_union(lines))) if lines else ()
    region: BaseGeometry = unary_union(polygons) if polygons else box(*bounds)
    if not region.is_valid:
        region = region.buffer(0)
    # Multiple pads define one physical annotation envelope. A single circular
    # testpoint remains circular because its convex hull is unchanged.
    if bounds_kind.casefold() == "pads":
        region = region.convex_hull
    return region


def _candidate_centers(region: BaseGeometry) -> tuple[tuple[float, float], ...]:
    min_x, min_y, max_x, max_y = region.bounds
    candidates: list[tuple[float, float]] = []

    def add(point: Point | tuple[float, float]) -> None:
        x, y = (float(point.x), float(point.y)) if isinstance(point, Point) else point
        candidate = (float(x), float(y))
        if region.covers(Point(candidate)) and candidate not in candidates:
            candidates.append(candidate)

    add(region.centroid)
    add(region.representative_point())
    add(((min_x + max_x) / 2.0, (min_y + max_y) / 2.0))
    parts = tuple(getattr(region, "geoms", ())) or (region,)
    parts = tuple(
        sorted(
            parts,
            key=lambda part: (
                tuple(float(value) for value in part.bounds),
                float(part.area),
                bytes(part.normalize().wkb),
            ),
        )
    )
    for part in parts:
        add(part.centroid)
        add(part.representative_point())
        part_min_x, part_min_y, part_max_x, part_max_y = part.bounds
        add(((part_min_x + part_max_x) / 2.0, (part_min_y + part_max_y) / 2.0))
    for x_index in range(1, _CENTER_GRID_DIVISIONS):
        x = min_x + (max_x - min_x) * x_index / _CENTER_GRID_DIVISIONS
        for y_index in range(1, _CENTER_GRID_DIVISIONS):
            y = min_y + (max_y - min_y) * y_index / _CENTER_GRID_DIVISIONS
            add((x, y))
    return tuple(candidates)


def _largest_font_at_candidates(
    region: BaseGeometry,
    *,
    centers: tuple[tuple[float, float], ...],
    text_aspect: float,
    rotation_degrees: float,
) -> tuple[float, tuple[float, float]]:
    min_x, min_y, max_x, max_y = region.bounds
    upper_bound = max(max_x - min_x, max_y - min_y)
    best_font = 0.0
    best_center = centers[0]
    for center in centers:
        low = 0.0
        high = upper_bound
        for _ in range(_BINARY_SEARCH_STEPS):
            font_size = (low + high) / 2.0
            if _text_box_fits(
                region,
                center=center,
                font_size=font_size,
                text_aspect=text_aspect,
                rotation_degrees=rotation_degrees,
            ):
                low = font_size
            else:
                high = font_size
        if low > best_font + 1.0e-9:
            best_font = low
            best_center = center
    return best_font, best_center


def _text_box_fits(
    region: BaseGeometry,
    *,
    center: tuple[float, float],
    font_size: float,
    text_aspect: float,
    rotation_degrees: float,
) -> bool:
    half_width = text_aspect * font_size / 2.0
    half_height = font_size / 2.0
    normalized_rotation = abs(rotation_degrees) % 180.0
    if abs(normalized_rotation - 90.0) <= 1.0e-9:
        half_width, half_height = half_height, half_width
    rectangle = box(
        center[0] - half_width,
        center[1] - half_height,
        center[0] + half_width,
        center[1] + half_height,
    )
    if abs(normalized_rotation) > 1.0e-9 and abs(normalized_rotation - 90.0) > 1.0e-9:
        rectangle = affinity.rotate(
            rectangle,
            rotation_degrees,
            origin=center,
            use_radians=False,
        )
    return bool(region.covers(rectangle))


__all__ = [
    "CcaDesignatorFit",
    "CcaDesignatorFitSession",
    "CcaDesignatorFitTelemetry",
    "designator_fit_telemetry_snapshot",
    "reset_designator_fit_telemetry",
    "fit_designator_to_geometry",
    "normalize_designator_axis",
]


def _clear_designator_center(
    designator: str,
    *,
    center: tuple[float, float],
    font_size: float,
    rotation: float,
    component_bounds: tuple[float, float, float, float],
    obstacles: tuple[tuple[float, float, float, float], ...],
) -> tuple[float, float]:
    if not obstacles:
        return center
    angle = math.radians(rotation)
    text_width = max(font_size, len(designator) * font_size * 0.62)
    text_height = font_size
    half_width = (abs(math.cos(angle)) * text_width + abs(math.sin(angle)) * text_height) / 2.0
    half_height = (abs(math.sin(angle)) * text_width + abs(math.cos(angle)) * text_height) / 2.0
    left, top, right, bottom = component_bounds
    candidates = (
        center,
        (left + half_width, center[1]),
        (right - half_width, center[1]),
        (center[0], top + half_height),
        (center[0], bottom - half_height),
    )

    def bounds(candidate: tuple[float, float]) -> tuple[float, float, float, float]:
        return (
            candidate[0] - half_width,
            candidate[1] - half_height,
            candidate[0] + half_width,
            candidate[1] + half_height,
        )

    def overlap(
        first: tuple[float, float, float, float], second: tuple[float, float, float, float]
    ) -> float:
        return max(0.0, min(first[2], second[2]) - max(first[0], second[0])) * max(
            0.0, min(first[3], second[3]) - max(first[1], second[1])
        )

    return min(
        candidates,
        key=lambda candidate: (
            sum(overlap(bounds(candidate), obstacle) for obstacle in obstacles),
            math.dist(candidate, center),
        ),
    )
