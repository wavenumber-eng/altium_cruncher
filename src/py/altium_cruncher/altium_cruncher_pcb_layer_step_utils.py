"""Small geometry/name helpers for PCB layer STEP export."""

from __future__ import annotations

import math
from pathlib import Path
import re

from altium_monkey.altium_record_types import PcbLayer

MIL_TO_MM = 0.0254
INTERNAL_UNITS_PER_MIL = 10000.0


def _octagon_points(
    cx: float, cy: float, half_w: float, half_h: float
) -> list[tuple[float, float]]:
    chamfer = min(half_w, half_h) / 2.0
    return [
        (cx + half_w, cy - (half_h - chamfer)),
        (cx + half_w, cy + half_h - chamfer),
        (cx + half_w - chamfer, cy + half_h),
        (cx - (half_w - chamfer), cy + half_h),
        (cx - half_w, cy + half_h - chamfer),
        (cx - half_w, cy - (half_h - chamfer)),
        (cx - (half_w - chamfer), cy - half_h),
        (cx + half_w - chamfer, cy - half_h),
    ]


def _mils_to_mm(value: float) -> float:
    return float(value) * MIL_TO_MM


def _iu_to_mils(value: object) -> float:
    return float(value or 0.0) / INTERNAL_UNITS_PER_MIL


def _points_close(
    a: tuple[float, float], b: tuple[float, float], tol: float = 1e-9
) -> bool:
    return math.isclose(a[0], b[0], abs_tol=tol) and math.isclose(
        a[1], b[1], abs_tol=tol
    )


def _dedupe_closed_points(
    points: list[tuple[float, float]],
) -> list[tuple[float, float]]:
    deduped: list[tuple[float, float]] = []
    for x, y in points:
        point = (float(x), float(y))
        if deduped and _points_close(deduped[-1], point):
            continue
        deduped.append(point)
    if len(deduped) > 1 and _points_close(deduped[0], deduped[-1]):
        deduped.pop()
    return deduped


def _board_name_from_pcbdoc(pcbdoc: object) -> str:
    filepath = getattr(pcbdoc, "filepath", None)
    if filepath:
        return Path(filepath).stem
    return "board"


def _step_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]+", "_", value).strip("_") or "board"


def layer_step_output_name(board_name: str, layer: PcbLayer) -> str:
    """Return the conventional filename for one generated layer STEP artifact."""
    layer_name = re.sub(r"[^A-Za-z0-9]+", "_", layer.to_json_name().lower()).strip("_")
    return f"{_step_name(board_name)}__{layer_name}_layer.step"
