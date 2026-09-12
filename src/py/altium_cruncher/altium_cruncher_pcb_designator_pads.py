"""Autodoc pad-shape normalization and sampling for model-less designators."""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any
from altium_monkey.altium_record_types import PcbLayer
from altium_monkey.altium_pcb_enums import PadShape
from altium_monkey.altium_record_pcb__pad import AltiumPcbPad
from .altium_cruncher_pcb_designator_layout import CcaComponentGeometryFact

Point = tuple[float, float]
Segment = tuple[Point, Point]
CcaPadShape = str

@dataclass(frozen=True)
class CcaPadFact:
    x_mm: float
    y_mm: float
    size_x_mm: float
    size_y_mm: float
    angle_degrees: float
    shape: str
    roundrect_rratio: float | None = None
    polygon_rings_mm: tuple[tuple[Point, ...], ...] = ()


def component_designator_pads(
    pads: list[AltiumPcbPad], component_index: int, side: str,
) -> list[AltiumPcbPad]:
    """Use visible electrical pads, falling back to mechanical holes if needed."""
    layer = PcbLayer.BOTTOM if side == "bottom" else PcbLayer.TOP
    eligible = [
        pad for pad in pads
        if pad.component_index == component_index
        and (
            pad._should_render_on_layer(layer)
            or pad._should_force_svg_copper_render(layer)
        )
    ]
    # TC2030 contacts can carry Altium's mask-only flag. Match the copper
    # renderer's testpoint exception before deciding which envelope to fit.
    electrical = [pad for pad in eligible if pad.hole_size_mils <= 0 or pad.is_plated]
    return electrical or eligible


def pad_geometry(pads: list[object], side: str) -> CcaComponentGeometryFact | None:
    facts = tuple(_pad_fact(pad, side) for pad in pads)
    segments = tuple(segment for pad in facts for ring in _pad_rings(pad)
                     for segment in _closed_ring_segments(ring))
    if segments:
        xs, ys = zip(*(point for segment in segments for point in segment))
        bounds = min(xs), min(ys), max(xs), max(ys)
    else:
        bounds = _pad_bounds(facts)
    return CcaComponentGeometryFact(bounds, segments, "pads") if bounds else None


def _pad_fact(pad: Any, side: str) -> CcaPadFact:
    layer = PcbLayer.BOTTOM if side == "bottom" else PcbLayer.TOP
    width, height, shape_code = _pad_size_shape(pad, side=side)
    shape_code = _effective_pad_shape(pad, layer=layer, base_shape=shape_code)
    shape = _neutral_pad_shape(shape_code, width=width, height=height)
    x_mm, y_mm = float(pad.x) * 0.00000254, -float(pad.y) * 0.00000254
    size_x_mm = max(width * 0.00000254, 0.01)
    size_y_mm = max(height * 0.00000254, 0.01)
    angle = -float(pad.rotation or 0)
    polygon_rings = _octagonal_pad_rings(
        x_mm=x_mm, y_mm=y_mm, width_mm=size_x_mm, height_mm=size_y_mm,
        angle_degrees=angle,
    ) if shape_code == int(PadShape.OCTAGONAL) else ()
    ratio = None
    if shape == "roundrect":
        minor_mils = min(width, height) / 10000
        radius_mils = float(pad.corner_radius_mils_on_layer(layer) or 0)
        ratio = min(max(radius_mils / minor_mils, 0), 0.5) if minor_mils > 0 else 0
        if ratio == 0:
            ratio = 0.5
    return CcaPadFact(x_mm, y_mm, size_x_mm, size_y_mm, angle, shape, ratio, polygon_rings)


def _pad_size_shape(pad: Any, *, side: str) -> tuple[int, int, int]:
    if side == "bottom":
        return (
            int(pad.bot_width or pad.width),
            int(pad.bot_height or pad.height),
            int(pad.bot_shape or pad.shape),
        )
    return (
        int(pad.top_width or pad.width),
        int(pad.top_height or pad.height),
        int(pad.top_shape or pad.shape),
    )


def _effective_pad_shape(pad: Any, *, layer: PcbLayer, base_shape: int) -> int:
    layer_index = layer.value - 1
    alt_shapes = tuple(getattr(pad, "alt_shape", ()) or ())
    if 0 <= layer_index < len(alt_shapes) and int(alt_shapes[layer_index]) == 9:
        return int(PadShape.ROUNDED_RECTANGLE)
    return int(base_shape)


def _neutral_pad_shape(shape_code: int, *, width: int, height: int) -> CcaPadShape:
    if shape_code == int(PadShape.CIRCLE):
        return "circle" if width == height else "roundrect"
    if shape_code == int(PadShape.RECTANGLE):
        return "rect"
    if shape_code == int(PadShape.OCTAGONAL):
        return "polygon"
    if shape_code == int(PadShape.ROUNDED_RECTANGLE):
        return "roundrect"
    return "unsupported"


def _pad_shape_name(shape_code: int) -> str:
    try:
        return PadShape(shape_code).name.casefold()
    except ValueError:
        return f"altium-pad-shape-{shape_code}"


def _octagonal_pad_rings(
    *,
    x_mm: float,
    y_mm: float,
    width_mm: float,
    height_mm: float,
    angle_degrees: float,
) -> tuple[tuple[tuple[float, float], ...], ...]:
    half_x = width_mm / 2.0
    half_y = height_mm / 2.0
    chamfer = min(width_mm, height_mm) * 0.25
    local = (
        (-half_x + chamfer, -half_y),
        (half_x - chamfer, -half_y),
        (half_x, -half_y + chamfer),
        (half_x, half_y - chamfer),
        (half_x - chamfer, half_y),
        (-half_x + chamfer, half_y),
        (-half_x, half_y - chamfer),
        (-half_x, -half_y + chamfer),
    )
    angle = math.radians(angle_degrees)
    cosine = math.cos(angle)
    sine = math.sin(angle)
    return (
        tuple(
            (
                x_mm + local_x * cosine - local_y * sine,
                y_mm + local_x * sine + local_y * cosine,
            )
            for local_x, local_y in local
        ),
    )


def _pad_sides(pad: Any) -> tuple[str, ...]:
    layer = int(pad.layer)
    if layer == PcbLayer.MULTI_LAYER.value:
        return ("top", "bottom")
    if layer == PcbLayer.TOP.value:
        return ("top",)
    if layer == PcbLayer.BOTTOM.value:
        return ("bottom",)
    return ()


def _pad_bounds(pads: tuple[CcaPadFact, ...]) -> tuple[float, float, float, float] | None:
    if not pads:
        return None
    boxes = []
    for pad in pads:
        angle = math.radians(pad.angle_degrees)
        half_x = pad.size_x_mm / 2.0
        half_y = pad.size_y_mm / 2.0
        extent_x = abs(half_x * math.cos(angle)) + abs(half_y * math.sin(angle))
        extent_y = abs(half_x * math.sin(angle)) + abs(half_y * math.cos(angle))
        boxes.append(
            (pad.x_mm - extent_x, pad.y_mm - extent_y, pad.x_mm + extent_x, pad.y_mm + extent_y)
        )
    return (
        min(item[0] for item in boxes),
        min(item[1] for item in boxes),
        max(item[2] for item in boxes),
        max(item[3] for item in boxes),
    )



def _pad_rings(pad: CcaPadFact) -> tuple[tuple[Point, ...], ...]:
    if pad.shape == "unsupported":
        return ()
    if pad.polygon_rings_mm:
        return pad.polygon_rings_mm

    width = max(0.0, pad.size_x_mm)
    height = max(0.0, pad.size_y_mm)
    if width <= 0.0 or height <= 0.0:
        return ()
    shape = pad.shape.strip().casefold().replace("-", "_")
    if shape == "circle":
        local = _ellipse_points(width / 2.0, height / 2.0)
    elif shape in {"oval", "oblong"}:
        local = _roundrect_points(width, height, min(width, height) / 2.0)
    elif shape == "roundrect":
        ratio = min(0.5, max(0.0, float(pad.roundrect_rratio or 0.0)))
        local = _roundrect_points(width, height, min(width, height) * ratio)
    elif shape == "rect":
        local = (
            (-width / 2.0, -height / 2.0),
            (width / 2.0, -height / 2.0),
            (width / 2.0, height / 2.0),
            (-width / 2.0, height / 2.0),
        )
    else:
        return ()
    return (tuple(_transform(point, pad) for point in local),)


def _ellipse_points(radius_x: float, radius_y: float, *, count: int = 40) -> tuple[Point, ...]:
    return tuple(
        (
            radius_x * math.cos(2.0 * math.pi * index / count),
            radius_y * math.sin(2.0 * math.pi * index / count),
        )
        for index in range(count)
    )


def _roundrect_points(width: float, height: float, radius: float) -> tuple[Point, ...]:
    radius = min(max(0.0, radius), width / 2.0, height / 2.0)
    if radius <= 0.0:
        return (
            (-width / 2.0, -height / 2.0),
            (width / 2.0, -height / 2.0),
            (width / 2.0, height / 2.0),
            (-width / 2.0, height / 2.0),
        )
    points: list[Point] = []
    for center_x, center_y, start_degrees in (
        (width / 2.0 - radius, -height / 2.0 + radius, -90.0),
        (width / 2.0 - radius, height / 2.0 - radius, 0.0),
        (-width / 2.0 + radius, height / 2.0 - radius, 90.0),
        (-width / 2.0 + radius, -height / 2.0 + radius, 180.0),
    ):
        points.extend(
            (
                center_x + radius * math.cos(math.radians(start_degrees + step * 15.0)),
                center_y + radius * math.sin(math.radians(start_degrees + step * 15.0)),
            )
            for step in range(7)
        )
    return tuple(points)


def _transform(point: Point, pad: CcaPadFact) -> Point:
    angle = math.radians(pad.angle_degrees)
    cosine = math.cos(angle)
    sine = math.sin(angle)
    return (
        pad.x_mm + point[0] * cosine - point[1] * sine,
        pad.y_mm + point[0] * sine + point[1] * cosine,
    )


def _closed_ring_segments(ring: tuple[Point, ...]) -> tuple[Segment, ...]:
    if len(ring) < 2:
        return ()
    return tuple((ring[index], ring[(index + 1) % len(ring)]) for index in range(len(ring)))
