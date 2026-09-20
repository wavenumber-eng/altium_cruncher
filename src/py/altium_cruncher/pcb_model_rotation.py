"""Deterministic selection between documented Altium STEP Z-rotation meanings."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Literal


type Bounds3 = tuple[float, float, float, float, float, float]
type Bounds2 = tuple[float, float, float, float]
type RotationChoice = Literal["instance_space", "footprint_local", "unresolved"]


@dataclass(frozen=True)
class RotationResolution:
    choice: RotationChoice
    reason: str
    current_score: float | None
    footprint_local_score: float | None


def resolve_model_z_rotation(
    authored_outline_bounds_mm: Bounds2,
    instance_space_bounds_mm: Bounds3,
    footprint_local_bounds_mm: Bounds3,
    *,
    absolute_tolerance_mm: float = 0.05,
    relative_tolerance: float = 0.01,
    material_score_margin: float = 0.25,
) -> RotationResolution:
    """Choose the alternative only when native XY bounds uniquely support it."""

    _validate_tolerances(
        absolute_tolerance_mm,
        relative_tolerance,
        material_score_margin,
    )
    target = _outline_facts(authored_outline_bounds_mm)
    if target is None:
        return RotationResolution("unresolved", "invalid-authored-outline", None, None)
    current = _candidate_score(
        target,
        instance_space_bounds_mm,
        absolute_tolerance_mm,
        relative_tolerance,
    )
    alternative = _candidate_score(
        target,
        footprint_local_bounds_mm,
        absolute_tolerance_mm,
        relative_tolerance,
    )
    if current is None or alternative is None:
        return _invalid_candidate_resolution(current, alternative)
    return _select_resolution(current, alternative, material_score_margin)


def _validate_tolerances(
    absolute_tolerance_mm: float,
    relative_tolerance: float,
    material_score_margin: float,
) -> None:
    values = (
        (absolute_tolerance_mm, False),
        (relative_tolerance, True),
        (material_score_margin, True),
    )
    if any(not math.isfinite(value) or value < 0 for value, _ in values):
        raise ValueError(
            "Rotation-resolution tolerances must be finite and nonnegative"
        )
    if absolute_tolerance_mm == 0:
        raise ValueError("absolute_tolerance_mm must be positive")


def _invalid_candidate_resolution(
    current: tuple[float, bool] | None,
    alternative: tuple[float, bool] | None,
) -> RotationResolution:
    return RotationResolution(
        "unresolved",
        "invalid-candidate-bounds",
        None if current is None else current[0],
        None if alternative is None else alternative[0],
    )


def _select_resolution(
    current: tuple[float, bool],
    alternative: tuple[float, bool],
    material_score_margin: float,
) -> RotationResolution:
    current_score, current_valid = current
    alternative_score, alternative_valid = alternative
    if alternative_valid and (
        not current_valid or alternative_score + material_score_margin < current_score
    ):
        return RotationResolution(
            "footprint_local",
            "footprint-local-native-bounds-match",
            current_score,
            alternative_score,
        )
    if current_valid:
        return RotationResolution(
            "instance_space",
            "current-native-bounds-match",
            current_score,
            alternative_score,
        )
    return RotationResolution(
        "unresolved",
        "neither-candidate-matches-authored-outline",
        current_score,
        alternative_score,
    )


def _outline_facts(bounds: Bounds2) -> tuple[float, float, float, float] | None:
    if len(bounds) != 4 or not all(math.isfinite(value) for value in bounds):
        return None
    left, bottom, right, top = bounds
    width, height = right - left, top - bottom
    if width <= 0 or height <= 0:
        return None
    return ((left + right) / 2, (bottom + top) / 2, width, height)


def _candidate_score(
    target: tuple[float, float, float, float],
    bounds: Bounds3,
    absolute_tolerance_mm: float,
    relative_tolerance: float,
) -> tuple[float, bool] | None:
    if len(bounds) != 6 or not all(math.isfinite(value) for value in bounds):
        return None
    low_x, low_y, _low_z, high_x, high_y, _high_z = bounds
    width, height = high_x - low_x, high_y - low_y
    if width <= 0 or height <= 0:
        return None
    values = ((low_x + high_x) / 2, (low_y + high_y) / 2, width, height)
    tolerances = tuple(
        absolute_tolerance_mm + relative_tolerance * scale
        for scale in (target[2], target[3], target[2], target[3])
    )
    residuals = tuple(
        abs(actual - expected) / tolerance
        for actual, expected, tolerance in zip(values, target, tolerances)
    )
    return math.sqrt(sum(value * value for value in residuals) / 4), max(residuals) <= 1


__all__ = ["RotationResolution", "resolve_model_z_rotation"]
