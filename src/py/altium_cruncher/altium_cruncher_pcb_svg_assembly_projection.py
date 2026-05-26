"""Geometer-backed STEP projection helpers for Altium assembly overlays."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import logging
from typing import Any, Literal

log = logging.getLogger(__name__)

ProjectionSide = Literal["top", "bottom"]
CurveMode = Literal["native_arcs", "polyline"]


@dataclass(frozen=True)
class AssemblyProjectionOptions:
    side: ProjectionSide
    curve_mode: CurveMode = "native_arcs"
    samples_per_curve: int = 24
    round_digits: int = 3
    include_visible: bool = True
    include_outline: bool = True
    union_polygons: bool = True


@dataclass(frozen=True)
class AssemblyProjectedArc:
    start: tuple[float, float]
    end: tuple[float, float]
    center: tuple[float, float]
    radius: float
    extent_rad: float
    ccw: bool
    full_circle: bool


@dataclass(frozen=True)
class AssemblyProjectedGeometry:
    simple_line_segments: tuple[tuple[tuple[float, float], tuple[float, float]], ...]
    simple_arcs: tuple[AssemblyProjectedArc, ...]
    detail_line_segments: tuple[tuple[tuple[float, float], tuple[float, float]], ...]
    detail_arcs: tuple[AssemblyProjectedArc, ...]

    @property
    def is_empty(self) -> bool:
        return (
            not self.simple_line_segments
            and not self.simple_arcs
            and not self.detail_line_segments
            and not self.detail_arcs
        )


class AssemblyProjectionCache:
    """Caches Geometer HLR results for repeated component instances."""

    def __init__(self) -> None:
        self._projection_by_key: dict[tuple[Any, ...], AssemblyProjectedGeometry] = {}

    def build_cache_key(
        self,
        *,
        model_hash: str,
        pose_signature: tuple[float, ...],
        options: AssemblyProjectionOptions,
    ) -> tuple[Any, ...]:
        return (
            str(model_hash),
            str(options.side),
            str(options.curve_mode),
            int(max(2, options.samples_per_curve)),
            int(max(0, options.round_digits)),
            bool(options.include_visible),
            bool(options.include_outline),
            bool(options.union_polygons),
            tuple(float(v) for v in pose_signature),
        )

    def project(
        self,
        *,
        model_hash: str,
        step_bytes: bytes,
        pose_signature: tuple[float, ...],
        transform_matrix: Any,
        options: AssemblyProjectionOptions,
        model_label: str | None = None,
    ) -> tuple[tuple[Any, ...], AssemblyProjectedGeometry]:
        cache_key = self.build_cache_key(
            model_hash=model_hash,
            pose_signature=pose_signature,
            options=options,
        )
        cached = self._projection_by_key.get(cache_key)
        if cached is not None:
            return cache_key, cached

        label = str(model_label or "").strip() or f"hash:{str(model_hash)[:12]}"
        log.info(
            "Computing Geometer HLR STEP projection: %s (hash=%s, side=%s, pose=%s)",
            label,
            str(model_hash)[:12],
            str(options.side),
            ",".join(f"{float(value):.6g}" for value in pose_signature),
        )

        projected = self._project_with_geometer(
            step_bytes=bytes(step_bytes),
            transform_matrix=transform_matrix,
            options=options,
        )
        self._projection_by_key[cache_key] = projected
        return cache_key, projected

    def _project_with_geometer(
        self,
        *,
        step_bytes: bytes,
        transform_matrix: Any,
        options: AssemblyProjectionOptions,
    ) -> AssemblyProjectedGeometry:
        try:
            import geometer
        except Exception as exc:  # pragma: no cover - dependency failure path
            raise RuntimeError(
                "The geometer Python package is required for Altium Cruncher "
                "assembly STEP projection."
            ) from exc

        side = str(options.side).strip().lower()
        if side == "bottom":
            view_id = "bottom"
            direction = [0.0, 0.0, -1.0]
            projection_y_direction = [1.0, 0.0, 0.0]
        else:
            view_id = "top"
            direction = [0.0, 0.0, 1.0]
            projection_y_direction = [-1.0, 0.0, 0.0]

        round_digits = int(max(0, options.round_digits))
        curve_mode = str(options.curve_mode).strip().lower()
        if curve_mode not in {"native_arcs", "polyline"}:
            curve_mode = "native_arcs"

        result = geometer.project_step_hlr(
            step_bytes,
            views=[
                {
                    "id": view_id,
                    "direction": direction,
                    "up": projection_y_direction,
                }
            ],
            model_transform=_matrix4_for_geometer(transform_matrix),
            options={
                "curve_mode": curve_mode,
                "samples_per_curve": int(max(2, options.samples_per_curve)),
                "round_digits": round_digits,
                "include_visible": bool(options.include_visible),
                "include_outline": bool(options.include_outline),
                "union_simple_polygons": bool(options.union_polygons),
            },
        )

        simple = result.geometry(view_id, "simple")
        detail = result.geometry(view_id, "detail")
        return AssemblyProjectedGeometry(
            simple_line_segments=self._dedupe_segments(
                list(_segments_from_mode(simple)),
                round_digits=round_digits,
            ),
            simple_arcs=self._dedupe_arcs(
                list(_arcs_from_mode(simple)),
                round_digits=round_digits,
            ),
            detail_line_segments=self._dedupe_segments(
                list(_segments_from_mode(detail)),
                round_digits=round_digits,
            ),
            detail_arcs=self._dedupe_arcs(
                list(_arcs_from_mode(detail)),
                round_digits=round_digits,
            ),
        )

    def _dedupe_segments(
        self,
        segments: list[tuple[tuple[float, float], tuple[float, float]]],
        *,
        round_digits: int,
    ) -> tuple[tuple[tuple[float, float], tuple[float, float]], ...]:
        deduped: list[tuple[tuple[float, float], tuple[float, float]]] = []
        seen: set[tuple[float, float, float, float]] = set()
        for (x1, y1), (x2, y2) in segments:
            rx1 = round(float(x1), round_digits)
            ry1 = round(float(y1), round_digits)
            rx2 = round(float(x2), round_digits)
            ry2 = round(float(y2), round_digits)
            if rx1 == rx2 and ry1 == ry2:
                continue
            if rx1 > rx2 or (rx1 == rx2 and ry1 > ry2):
                rx1, ry1, rx2, ry2 = rx2, ry2, rx1, ry1
            key = (rx1, ry1, rx2, ry2)
            if key in seen:
                continue
            seen.add(key)
            deduped.append(((rx1, ry1), (rx2, ry2)))
        return tuple(deduped)

    def _dedupe_arcs(
        self,
        arcs: list[AssemblyProjectedArc],
        *,
        round_digits: int,
    ) -> tuple[AssemblyProjectedArc, ...]:
        deduped: list[AssemblyProjectedArc] = []
        seen: set[tuple[Any, ...]] = set()
        for arc in arcs:
            start = (
                round(float(arc.start[0]), round_digits),
                round(float(arc.start[1]), round_digits),
            )
            end = (
                round(float(arc.end[0]), round_digits),
                round(float(arc.end[1]), round_digits),
            )
            center = (
                round(float(arc.center[0]), round_digits),
                round(float(arc.center[1]), round_digits),
            )
            radius = round(float(arc.radius), round_digits)
            if arc.full_circle:
                key = ("full", center[0], center[1], radius)
            else:
                key = (
                    "arc",
                    start[0],
                    start[1],
                    end[0],
                    end[1],
                    center[0],
                    center[1],
                    radius,
                    round(float(arc.extent_rad), max(round_digits, 3)),
                    bool(arc.ccw),
                )
            if key in seen:
                continue
            seen.add(key)
            deduped.append(
                AssemblyProjectedArc(
                    start=start,
                    end=end,
                    center=center,
                    radius=radius,
                    extent_rad=float(arc.extent_rad),
                    ccw=bool(arc.ccw),
                    full_circle=bool(arc.full_circle),
                )
            )
        return tuple(deduped)


def _matrix4_for_geometer(matrix: Any) -> list[list[float]]:
    if hasattr(matrix, "tolist"):
        matrix = matrix.tolist()
    values = list(matrix)
    if len(values) == 16 and not _is_nested_sequence(values):
        flat = [float(value) for value in values]
        return [flat[idx : idx + 4] for idx in range(0, 16, 4)]
    if len(values) != 4:
        raise ValueError("transform_matrix must be a 4x4 matrix or flat 16-value sequence")
    rows: list[list[float]] = []
    for row in values:
        row_values = list(row)
        if len(row_values) != 4:
            raise ValueError("transform_matrix rows must contain 4 values")
        rows.append([float(value) for value in row_values])
    return rows


def _is_nested_sequence(values: Sequence[Any]) -> bool:
    return any(
        isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray)
        for value in values
    )


def _segments_from_mode(
    mode: Mapping[str, Any],
) -> tuple[tuple[tuple[float, float], tuple[float, float]], ...]:
    segments: list[tuple[tuple[float, float], tuple[float, float]]] = []
    for raw in list(mode.get("segments") or []):
        parsed = _segment_from_json(raw)
        if parsed is not None:
            segments.append(parsed)
    return tuple(segments)


def _segment_from_json(
    raw: Any,
) -> tuple[tuple[float, float], tuple[float, float]] | None:
    if isinstance(raw, Mapping):
        start = _point2(raw.get("start"))
        end = _point2(raw.get("end"))
        if start is None or end is None:
            return None
        return start, end
    if not isinstance(raw, Sequence) or isinstance(raw, str | bytes | bytearray):
        return None
    values = list(raw)
    if len(values) == 4:
        return (float(values[0]), float(values[1])), (float(values[2]), float(values[3]))
    if len(values) == 2:
        start = _point2(values[0])
        end = _point2(values[1])
        if start is None or end is None:
            return None
        return start, end
    return None


def _arcs_from_mode(mode: Mapping[str, Any]) -> tuple[AssemblyProjectedArc, ...]:
    arcs: list[AssemblyProjectedArc] = []
    for raw in list(mode.get("arcs") or []):
        parsed = _arc_from_json(raw)
        if parsed is not None:
            arcs.append(parsed)
    return tuple(arcs)


def _arc_from_json(raw: Any) -> AssemblyProjectedArc | None:
    if not isinstance(raw, Mapping):
        return None
    start = _point2(raw.get("start"))
    end = _point2(raw.get("end"))
    center = _point2(raw.get("center"))
    if start is None or end is None or center is None:
        return None
    try:
        radius = float(raw.get("radius"))
        extent_rad = float(raw.get("extent_rad"))
    except (TypeError, ValueError):
        return None
    return AssemblyProjectedArc(
        start=start,
        end=end,
        center=center,
        radius=radius,
        extent_rad=extent_rad,
        ccw=bool(raw.get("ccw", True)),
        full_circle=bool(raw.get("full_circle", False)),
    )


def _point2(raw: Any) -> tuple[float, float] | None:
    if not isinstance(raw, Sequence) or isinstance(raw, str | bytes | bytearray):
        return None
    values = list(raw)
    if len(values) < 2:
        return None
    try:
        return float(values[0]), float(values[1])
    except (TypeError, ValueError):
        return None


_GLOBAL_ASSEMBLY_PROJECTION_CACHE = AssemblyProjectionCache()


def get_assembly_projection_cache() -> AssemblyProjectionCache:
    return _GLOBAL_ASSEMBLY_PROJECTION_CACHE


__all__ = [
    "AssemblyProjectedArc",
    "AssemblyProjectedGeometry",
    "AssemblyProjectionCache",
    "AssemblyProjectionOptions",
    "CurveMode",
    "ProjectionSide",
    "get_assembly_projection_cache",
]
