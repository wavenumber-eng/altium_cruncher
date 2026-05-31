"""Explicit highlight bodies for PCB layer STEP exports."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

from altium_monkey.altium_pcb_enums import PadShape
from altium_monkey.altium_record_types import PcbLayer


@dataclass(frozen=True, slots=True)
class PcbLayerStepHighlight:
    """Explicit pad geometry to overlay as a colored STEP highlight body."""

    id: str
    color: str
    pad_geometries: tuple[dict[str, object], ...]
    name: str | None = None
    z_offset_mm: float = 0.001
    thickness_mm: float = 0.01


class _RegionLike(Protocol):
    def to_json(self) -> dict[str, object]:
        """Return the planar STEP region payload."""


def highlight_bodies_from_geometries(
    *,
    highlights: tuple[PcbLayerStepHighlight, ...],
    layer: PcbLayer,
    z_mm: float,
    copper_thickness_mm: float,
    pad_shape_region: Callable[..., _RegionLike],
    step_name: Callable[[str], str],
) -> list[dict[str, object]]:
    """Return planar STEP bodies for explicit pad-geometry highlights."""
    bodies: list[dict[str, object]] = []
    for highlight in highlights:
        regions = [
            region
            for geometry in highlight.pad_geometries
            if (region := _highlight_pad_region(geometry, layer, pad_shape_region))
            is not None
        ]
        if regions:
            bodies.append(
                {
                    "id": step_name(highlight.id),
                    "name": highlight.name or highlight.id,
                    "kind": "highlight",
                    "color": highlight.color,
                    "z_mm": z_mm + copper_thickness_mm + highlight.z_offset_mm,
                    "thickness_mm": highlight.thickness_mm,
                    "regions": [region.to_json() for region in regions],
                    "fuse_regions": True,
                }
            )
    return bodies


def _highlight_pad_region(
    geometry: dict[str, object],
    layer: PcbLayer,
    pad_shape_region: Callable[..., _RegionLike],
) -> _RegionLike | None:
    if not _highlight_pad_should_render_on_layer(geometry, layer):
        return None
    width_mils = _geometry_float(geometry, "width_mils")
    height_mils = _geometry_float(geometry, "height_mils")
    if width_mils <= 0.0 or height_mils <= 0.0:
        return None
    return pad_shape_region(
        center=(
            _mils_to_mm(_geometry_float(geometry, "x_mils")),
            _mils_to_mm(_geometry_float(geometry, "y_mils")),
        ),
        width_mm=_mils_to_mm(width_mils),
        height_mm=_mils_to_mm(height_mils),
        shape=int(_geometry_float(geometry, "shape", default=PadShape.CIRCLE.value)),
        rotation_degrees=_geometry_float(geometry, "rotation_degrees"),
        corner_radius_percent=int(_geometry_float(geometry, "corner_radius_percent")),
    )


def _highlight_pad_should_render_on_layer(
    geometry: dict[str, object],
    layer: PcbLayer,
) -> bool:
    layer_id = int(_geometry_float(geometry, "layer", default=0))
    if layer_id == 0:
        return True
    if layer_id == PcbLayer.MULTI_LAYER.value:
        return layer.is_copper()
    return layer_id == layer.value


def _geometry_float(
    geometry: dict[str, object],
    name: str,
    *,
    default: float = 0.0,
) -> float:
    value = geometry.get(name, default)
    return (
        default
        if isinstance(value, bool) or not isinstance(value, int | float)
        else float(value)
    )


def _mils_to_mm(value: float) -> float:
    return float(value) * 0.0254
