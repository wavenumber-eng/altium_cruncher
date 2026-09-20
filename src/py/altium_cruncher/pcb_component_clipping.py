"""Board-aware qualification for Geometer B0 half-space clipping.

This module owns PCB policy only.  The illustration pipeline adapts its
resolution to Geometer's generated request values at the native-call boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import isfinite
from typing import Literal

import geometer as g

from .pcb_board_region_envelope_index import (
    BoardRegionEnvelopeIndex,
    BoardRegionQueryStatus,
)


type Side = Literal["top", "bottom"]
type Bounds3 = tuple[float, float, float, float, float, float]
_MM_PER_MIL = 0.0254


class ComponentVisibilityAction(StrEnum):
    """Safe action before a requested top/bottom illustration."""

    RENDER_UNCLIPPED = "render_unclipped"
    RENDER_CLIPPED = "render_clipped"
    OMIT = "omit"


@dataclass(frozen=True)
class HalfSpacePlane:
    """Canonical world-space plane matching Geometer issue 40 semantics."""

    normal: tuple[float, float, float]
    distance_mm: float
    tolerance_mm: float
    cap_policy: Literal["none"] = "none"

    def identity(self) -> tuple[object, ...]:
        return (
            self.normal,
            round(self.distance_mm, 12),
            round(self.tolerance_mm, 12),
            self.cap_policy,
        )


@dataclass(frozen=True)
class ComponentVisibilityResolution:
    """Deterministic qualification result for one placed component body group."""

    action: ComponentVisibilityAction
    reason: str
    requested_side: Side
    authored_side: Side
    plane: HalfSpacePlane | None = None
    region_name: str | None = None
    query_status: BoardRegionQueryStatus | None = None

    @property
    def crosses_to_opposite_side(self) -> bool:
        return (
            self.requested_side != self.authored_side
            and self.action is ComponentVisibilityAction.RENDER_CLIPPED
        )


def resolve_component_visibility(
    region_index: BoardRegionEnvelopeIndex,
    *,
    anchor_mm: tuple[float, float],
    bounds_local_mm: Bounds3,
    authored_side: Side,
    requested_side: Side,
    tolerance_mm: float = 1e-6,
) -> ComponentVisibilityResolution:
    """Qualify a component for surface clipping without guessing overhangs.

    The XY query is conservative. A partially covered box can still use one Z
    plane when every intersected region resolves to the same envelope; SVG
    composition separately limits that fragment to the board material domain.
    Ambiguous or unlike envelopes cannot be represented by one Z half-space.
    """

    _validate_request(
        anchor_mm,
        bounds_local_mm,
        authored_side,
        requested_side,
        tolerance_mm,
    )
    min_x, min_y, min_z, max_x, max_y, max_z = bounds_local_mm
    query = region_index.query_bounds(
        (anchor_mm[0] + min_x) / _MM_PER_MIL,
        (anchor_mm[1] + min_y) / _MM_PER_MIL,
        (anchor_mm[0] + max_x) / _MM_PER_MIL,
        (anchor_mm[1] + max_y) / _MM_PER_MIL,
    )
    if query.status is not BoardRegionQueryStatus.RESOLVED or query.region is None:
        return _unsafe_xy_resolution(
            authored_side,
            requested_side,
            f"board-region-{query.status.value}",
            query.status,
        )
    return _resolve_z_visibility(
        min_z=min_z,
        max_z=max_z,
        thickness_mm=query.region.total_thickness_mils * _MM_PER_MIL,
        tolerance_mm=tolerance_mm,
        requested_side=requested_side,
        authored_side=authored_side,
        region_name=query.region.name,
        query_status=query.status,
    )


def native_clipping(
    resolution: ComponentVisibilityResolution,
) -> g.IllustrationClipping:
    """Adapt PCB visibility policy to Geometer's generated B0 contract."""

    plane = resolution.plane
    if plane is None:
        raise ValueError("clipped component visibility requires a half-space plane")
    return g.IllustrationClipping(
        planes=(
            g.HalfSpacePlane(
                normal=plane.normal,
                distance_mm=plane.distance_mm,
                tolerance_mm=plane.tolerance_mm,
            ),
        ),
        cap_policy=plane.cap_policy,
    )


def clipped_conservative_bounds(
    bounds: Bounds3,
    resolution: ComponentVisibilityResolution | None,
) -> Bounds3:
    """Clamp conservative source bounds to the selected clipping plane."""

    if (
        resolution is None
        or resolution.action is not ComponentVisibilityAction.RENDER_CLIPPED
        or resolution.plane is None
    ):
        return bounds
    min_x, min_y, min_z, max_x, max_y, max_z = bounds
    boundary = (
        resolution.plane.distance_mm - resolution.plane.tolerance_mm
        if resolution.requested_side == "top"
        else -resolution.plane.distance_mm + resolution.plane.tolerance_mm
    )
    if resolution.requested_side == "top":
        min_z = max(min_z, boundary)
    else:
        max_z = min(max_z, boundary)
    return min_x, min_y, min_z, max_x, max_y, max_z


def _validate_request(
    anchor_mm: tuple[float, float],
    bounds_local_mm: Bounds3,
    authored_side: Side,
    requested_side: Side,
    tolerance_mm: float,
) -> None:
    _validate_sides(authored_side, requested_side)
    _validate_tolerance(tolerance_mm)
    _validate_bounds(bounds_local_mm)
    _validate_anchor(anchor_mm)


def _validate_sides(authored_side: Side, requested_side: Side) -> None:
    if authored_side not in {"top", "bottom"} or requested_side not in {
        "top",
        "bottom",
    }:
        raise ValueError("authored_side and requested_side must be top or bottom")


def _validate_tolerance(tolerance_mm: float) -> None:
    if not isfinite(tolerance_mm) or tolerance_mm < 0:
        raise ValueError("tolerance_mm must be finite and non-negative")


def _validate_bounds(bounds_local_mm: Bounds3) -> None:
    if len(bounds_local_mm) != 6 or not all(
        isfinite(value) for value in bounds_local_mm
    ):
        raise ValueError("bounds_local_mm must contain six finite values")
    min_x, min_y, min_z, max_x, max_y, max_z = bounds_local_mm
    if max_x < min_x or max_y < min_y or max_z < min_z:
        raise ValueError("bounds_local_mm minima must not exceed maxima")


def _validate_anchor(anchor_mm: tuple[float, float]) -> None:
    if len(anchor_mm) != 2 or not all(isfinite(value) for value in anchor_mm):
        raise ValueError("anchor_mm must contain two finite values")


def _resolve_z_visibility(
    *,
    min_z: float,
    max_z: float,
    thickness_mm: float,
    tolerance_mm: float,
    requested_side: Side,
    authored_side: Side,
    region_name: str,
    query_status: BoardRegionQueryStatus,
) -> ComponentVisibilityResolution:
    plane = _visibility_plane(requested_side, thickness_mm, tolerance_mm)
    action, reason = _classify_z_bounds(
        min_z,
        max_z,
        requested_side,
        thickness_mm,
        tolerance_mm,
    )
    return ComponentVisibilityResolution(
        action,
        reason,
        requested_side,
        authored_side,
        plane,
        region_name,
        query_status,
    )


def _visibility_plane(
    side: Side, thickness_mm: float, tolerance_mm: float
) -> HalfSpacePlane:
    if side == "top":
        return HalfSpacePlane((0.0, 0.0, 1.0), 0.0, tolerance_mm)
    return HalfSpacePlane((0.0, 0.0, -1.0), thickness_mm, tolerance_mm)


def _classify_z_bounds(
    min_z: float,
    max_z: float,
    side: Side,
    thickness_mm: float,
    tolerance_mm: float,
) -> tuple[ComponentVisibilityAction, str]:
    if side == "top":
        empty = max_z < -tolerance_mm
        entirely_visible = min_z >= -tolerance_mm
    else:
        bottom_z = -thickness_mm
        empty = min_z > bottom_z + tolerance_mm
        entirely_visible = max_z <= bottom_z + tolerance_mm
    if empty:
        return ComponentVisibilityAction.OMIT, "clipped-fragment-empty"
    if entirely_visible:
        return (
            ComponentVisibilityAction.RENDER_UNCLIPPED,
            "body-entirely-in-visible-half-space",
        )
    return ComponentVisibilityAction.RENDER_CLIPPED, "body-crosses-board-surface"


def _unsafe_xy_resolution(
    authored_side: Side,
    requested_side: Side,
    reason: str,
    query_status: BoardRegionQueryStatus,
    *,
    region_name: str | None = None,
) -> ComponentVisibilityResolution:
    if authored_side == requested_side:
        return ComponentVisibilityResolution(
            ComponentVisibilityAction.RENDER_UNCLIPPED,
            reason + ":mounting-side-fallback",
            requested_side,
            authored_side,
            region_name=region_name,
            query_status=query_status,
        )
    return ComponentVisibilityResolution(
        ComponentVisibilityAction.OMIT,
        reason + ":opposite-side-unsafe",
        requested_side,
        authored_side,
        region_name=region_name,
        query_status=query_status,
    )


__all__ = [
    "ComponentVisibilityAction",
    "ComponentVisibilityResolution",
    "HalfSpacePlane",
    "clipped_conservative_bounds",
    "native_clipping",
    "resolve_component_visibility",
]
