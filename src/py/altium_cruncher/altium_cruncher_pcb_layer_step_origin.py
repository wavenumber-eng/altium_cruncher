"""Coordinate-origin helpers for PCB layer STEP requests."""

from __future__ import annotations

from collections.abc import MutableMapping
from typing import Any

MIL_TO_MM = 0.0254


def board_origin_mils(pcbdoc: Any) -> tuple[float, float]:
    """Return the Altium board placement origin in source mils."""
    board = getattr(pcbdoc, "board", None)
    if board is None:
        return (0.0, 0.0)
    try:
        return (
            float(getattr(board, "origin_x", 0.0) or 0.0),
            float(getattr(board, "origin_y", 0.0) or 0.0),
        )
    except (TypeError, ValueError):
        return (0.0, 0.0)


def apply_origin_relative_geometry(
    bodies: list[dict[str, Any]],
    origin_mils: tuple[float, float],
) -> None:
    """Translate Geometer body regions from Altium absolute to origin-relative XY."""
    dx_mm = -origin_mils[0] * MIL_TO_MM
    dy_mm = -origin_mils[1] * MIL_TO_MM
    if dx_mm == 0.0 and dy_mm == 0.0:
        return
    for body in bodies:
        _translate_regions(body.get("regions"), dx_mm, dy_mm)
        _translate_regions(body.get("cutouts"), dx_mm, dy_mm)


def coordinate_origin_payload(origin_mils: tuple[float, float]) -> dict[str, object]:
    """Return manifest metadata for the STEP coordinate normalization."""
    return {
        "mode": "board_origin",
        "origin_mils": [origin_mils[0], origin_mils[1]],
        "origin_mm": [origin_mils[0] * MIL_TO_MM, origin_mils[1] * MIL_TO_MM],
        "geometry": (
            "x_step_mm=(x_absolute_mils-origin_x_mils)*0.0254; "
            "y_step_mm=(y_absolute_mils-origin_y_mils)*0.0254"
        ),
    }


def _translate_regions(value: object, dx_mm: float, dy_mm: float) -> None:
    if not isinstance(value, list):
        return
    for region in value:
        if isinstance(region, MutableMapping):
            _translate_region(region, dx_mm, dy_mm)


def _translate_region(
    region: MutableMapping[str, Any],
    dx_mm: float,
    dy_mm: float,
) -> None:
    outer = region.get("outer")
    if isinstance(outer, MutableMapping):
        _translate_ring(outer, dx_mm, dy_mm)
    holes = region.get("holes")
    if isinstance(holes, list):
        for hole in holes:
            if isinstance(hole, MutableMapping):
                _translate_ring(hole, dx_mm, dy_mm)


def _translate_ring(
    ring: MutableMapping[str, Any],
    dx_mm: float,
    dy_mm: float,
) -> None:
    points = ring.get("points")
    if isinstance(points, list):
        ring["points"] = [
            [float(point[0]) + dx_mm, float(point[1]) + dy_mm]
            for point in points
            if isinstance(point, list | tuple) and len(point) >= 2
        ]
    segments = ring.get("segments")
    if isinstance(segments, list):
        for segment in segments:
            if isinstance(segment, MutableMapping):
                _translate_segment(segment, dx_mm, dy_mm)


def _translate_segment(
    segment: MutableMapping[str, Any],
    dx_mm: float,
    dy_mm: float,
) -> None:
    center = segment.get("center")
    if isinstance(center, list | tuple) and len(center) >= 2:
        segment["center"] = [float(center[0]) + dx_mm, float(center[1]) + dy_mm]
