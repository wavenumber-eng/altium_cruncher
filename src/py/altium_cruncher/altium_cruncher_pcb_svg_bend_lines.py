"""Flat SVG annotations for rigid-flex bend lines.

This module intentionally does not fold or otherwise deform board geometry.
``BoardRegions/Data`` persists bend endpoints in a region-local coordinate
frame; the narrow adapter below lifts those endpoints into board space.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, replace
import html
from math import hypot, isfinite
from typing import TYPE_CHECKING

from shapely.geometry import LineString, Point, Polygon
from shapely.geometry.base import BaseGeometry

if TYPE_CHECKING:
    from altium_monkey.altium_layer_stack_document import (
        AltiumLayerStackDocument,
        AltiumStackBendLine,
        AltiumStackRegion,
    )
    from altium_monkey.altium_pcb_svg_renderer import PcbSvgRenderContext


BEND_LINES_LAYER_ID = 9015
DEFAULT_BEND_LINE_COLOR = "#D97706"
_INTERNAL_UNITS_PER_MIL = 10000.0
_MM_TO_MIL = 1.0 / 0.0254


@dataclass(frozen=True)
class BoardSpaceBendLine:
    """One valid source bend line after its region-local translation."""

    region_index: int
    region_name: str
    source_index: int
    fold_index: int | None
    angle_deg: float | None
    radius_mils: float | None
    x1_mils: float
    y1_mils: float
    x2_mils: float
    y2_mils: float
    clip_to_region: bool = True
    extension_mm: float = 0.0


def board_space_bend_lines(
    document: AltiumLayerStackDocument,
    *,
    on_invalid: Callable[[int, str, int, str], None] | None = None,
) -> tuple[BoardSpaceBendLine, ...]:
    """Lift valid, distinct region-local bend records into board space.

    The temporary Cruncher adapter interprets current Monkey bend endpoints
    relative to the lower-left of the source region geometry envelope. This
    matches Bluetooth Sentinel and translated authoring vectors, but remains
    isolated here until altium_monkey_dev issue 96 exposes the source transform
    as a core semantic contract.
    """

    candidates: list[BoardSpaceBendLine] = []
    for region_index, region in enumerate(tuple(document.board_regions or ())):
        candidates.extend(_region_bend_lines(region_index, region, on_invalid))
    return _distinct_bend_lines(candidates)


def _region_bend_lines(
    region_index: int,
    region: AltiumStackRegion,
    on_invalid: Callable[[int, str, int, str], None] | None,
) -> list[BoardSpaceBendLine]:
    region_name = str(region.name or f"Board region {region_index + 1}")
    source_lines = tuple(region.bending_lines or ())
    origin = _region_local_origin(region)
    if origin is None:
        _report_missing_region_origin(
            region_index, region_name, len(source_lines), on_invalid
        )
        return []
    result: list[BoardSpaceBendLine] = []
    for source_index, line in enumerate(source_lines):
        lifted, error = _lift_line(
            region_index,
            region_name,
            source_index,
            line,
            *origin,
        )
        if lifted is not None:
            result.append(lifted)
        elif on_invalid is not None:
            on_invalid(
                region_index,
                region_name,
                source_index,
                error or "invalid bend-line geometry",
            )
    return result


def _report_missing_region_origin(
    region_index: int,
    region_name: str,
    line_count: int,
    on_invalid: Callable[[int, str, int, str], None] | None,
) -> None:
    if on_invalid is None:
        return
    for source_index in range(line_count):
        on_invalid(
            region_index,
            region_name,
            source_index,
            "owning region has no finite outline origin",
        )


def _distinct_bend_lines(
    candidates: Iterable[BoardSpaceBendLine],
) -> tuple[BoardSpaceBendLine, ...]:
    result: list[BoardSpaceBendLine] = []
    seen: set[tuple[object, ...]] = set()
    for line in candidates:
        key = (
            line.region_index,
            line.fold_index,
            line.angle_deg,
            line.radius_mils,
            line.x1_mils,
            line.y1_mils,
            line.x2_mils,
            line.y2_mils,
        )
        if key not in seen:
            seen.add(key)
            result.append(line)
    return tuple(result)


class BendLinesRenderer:
    """Render region-clipped bend annotations from Monkey's semantic model."""

    def render(
        self,
        ctx: PcbSvgRenderContext,
        document: AltiumLayerStackDocument,
        style: Mapping[str, object],
        *,
        on_invalid: Callable[[int, str, int, str], None] | None = None,
    ) -> list[str]:
        if not style.get("enabled", True):
            return []
        bends = display_bend_lines(document, style, on_invalid=on_invalid)
        if not bends:
            return []

        regions = tuple(document.board_regions or ())
        clip_paths = _active_clip_paths(ctx, bends, regions)
        attrs = _group_attributes(ctx, style)
        lines = [f"<g {' '.join(attrs)}>"]
        lines.extend(_clip_definitions(clip_paths))
        for bend in bends:
            if not bend.clip_to_region or bend.region_index in clip_paths:
                lines.append(_bend_svg_line(ctx, bend))
        lines.append("</g>")
        return lines

    def bounds_mm(
        self,
        ctx: PcbSvgRenderContext,
        document: AltiumLayerStackDocument,
        style: Mapping[str, object],
    ) -> tuple[float, float, float, float] | None:
        """Return displayed annotation bounds in the unmirrored SVG frame."""

        if not style.get("enabled", True):
            return None
        bends = display_bend_lines(document, style)
        if not bends:
            return None
        x_values = tuple(
            value
            for bend in bends
            for value in (ctx.x_to_svg(bend.x1_mils), ctx.x_to_svg(bend.x2_mils))
        )
        y_values = tuple(
            value
            for bend in bends
            for value in (ctx.y_to_svg(bend.y1_mils), ctx.y_to_svg(bend.y2_mils))
        )
        padding = _positive_float(style.get("line_width_mm", 0.15), 0.15) / 2.0
        return (
            min(x_values) - padding,
            min(y_values) - padding,
            max(x_values) + padding,
            max(y_values) + padding,
        )


def bend_line_view_bounds(
    ctx: PcbSvgRenderContext,
    document: AltiumLayerStackDocument,
    style: Mapping[str, object],
    *,
    requested: bool,
    mirror: bool,
) -> tuple[tuple[float, float, float, float], ...]:
    """Return zero or one view-box bounds entries for bend annotations."""

    if not requested:
        return ()
    bounds = BendLinesRenderer().bounds_mm(ctx, document, style)
    if bounds is None:
        return ()
    if mirror:
        bounds = (
            ctx.width_mm - bounds[2],
            bounds[1],
            ctx.width_mm - bounds[0],
            bounds[3],
        )
    return (bounds,)


def display_bend_lines(
    document: AltiumLayerStackDocument,
    style: Mapping[str, object],
    *,
    on_invalid: Callable[[int, str, int, str], None] | None = None,
) -> tuple[BoardSpaceBendLine, ...]:
    """Resolve region chords and apply the configured per-end overrun."""

    bends = board_space_bend_lines(document, on_invalid=on_invalid)
    regions = tuple(document.board_regions or ())
    extension = _nonnegative_float(style.get("extension_mm", 1.0), 1.0)
    return tuple(_display_bend_line(bend, regions, extension) for bend in bends)


def _active_clip_paths(
    ctx: PcbSvgRenderContext,
    bends: Iterable[BoardSpaceBendLine],
    regions: tuple[AltiumStackRegion, ...],
) -> dict[int, str]:
    result: dict[int, str] = {}
    for region_index in sorted(
        {line.region_index for line in bends if line.clip_to_region}
    ):
        if region_index < len(regions) and (
            path := _region_path(ctx, regions[region_index])
        ):
            result[region_index] = path
    return result


def _display_bend_line(
    bend: BoardSpaceBendLine,
    regions: tuple[AltiumStackRegion, ...],
    extension_mm: float,
) -> BoardSpaceBendLine:
    if bend.region_index >= len(regions):
        return bend
    chord = _region_chord(bend, regions[bend.region_index])
    if chord is None:
        return bend
    (x1, y1), (x2, y2) = chord
    length = hypot(x2 - x1, y2 - y1)
    if length <= 0.0:
        return bend
    overrun = extension_mm * _MM_TO_MIL
    ux, uy = (x2 - x1) / length, (y2 - y1) / length
    return replace(
        bend,
        x1_mils=x1 - ux * overrun,
        y1_mils=y1 - uy * overrun,
        x2_mils=x2 + ux * overrun,
        y2_mils=y2 + uy * overrun,
        clip_to_region=extension_mm <= 0.0,
        extension_mm=extension_mm,
    )


def _region_chord(
    bend: BoardSpaceBendLine,
    region: AltiumStackRegion,
) -> tuple[tuple[float, float], tuple[float, float]] | None:
    polygon = _region_polygon_mils(region)
    if polygon is None:
        return None
    dx, dy = bend.x2_mils - bend.x1_mils, bend.y2_mils - bend.y1_mils
    length = hypot(dx, dy)
    if length <= 0.0:
        return None
    ux, uy = dx / length, dy / length
    midpoint = Point(
        (bend.x1_mils + bend.x2_mils) / 2.0,
        (bend.y1_mils + bend.y2_mils) / 2.0,
    )
    min_x, min_y, max_x, max_y = polygon.bounds
    reach = hypot(max_x - min_x, max_y - min_y) + length + 1.0
    axis = LineString(
        (
            (midpoint.x - ux * reach, midpoint.y - uy * reach),
            (midpoint.x + ux * reach, midpoint.y + uy * reach),
        )
    )
    segments = _line_segments(polygon.intersection(axis))
    if not segments:
        return None
    segment = min(segments, key=lambda item: (item.distance(midpoint), -item.length))
    coordinates = tuple(segment.coords)
    if len(coordinates) < 2:
        return None
    endpoints = (coordinates[0], coordinates[-1])
    return tuple(
        sorted(
            endpoints,
            key=lambda point: (
                (point[0] - midpoint.x) * ux + (point[1] - midpoint.y) * uy
            ),
        )
    )  # type: ignore[return-value]


def _region_polygon_mils(region: AltiumStackRegion) -> Polygon | None:
    outline = _ring_mils(region.outline_vertices)
    if len(outline) < 3:
        return None
    holes = tuple(
        ring
        for vertices in tuple(region.hole_vertices or ())
        if len(ring := _ring_mils(vertices)) >= 3
    )
    polygon = Polygon(outline, holes)
    if not polygon.is_valid:
        polygon = polygon.buffer(0)
    return polygon if isinstance(polygon, Polygon) and not polygon.is_empty else None


def _ring_mils(
    vertices: Iterable[tuple[float, float]],
) -> tuple[tuple[float, float], ...]:
    return tuple(
        (float(x) / _INTERNAL_UNITS_PER_MIL, float(y) / _INTERNAL_UNITS_PER_MIL)
        for x, y in vertices
        if isfinite(float(x)) and isfinite(float(y))
    )


def _line_segments(geometry: BaseGeometry) -> tuple[LineString, ...]:
    if isinstance(geometry, LineString):
        return (geometry,) if geometry.length > 0.0 else ()
    return tuple(
        part
        for child in getattr(geometry, "geoms", ())
        for part in _line_segments(child)
    )


def _group_attributes(
    ctx: PcbSvgRenderContext, style: Mapping[str, object]
) -> list[str]:
    color = html.escape(str(style.get("color", DEFAULT_BEND_LINE_COLOR)))
    opacity = _finite_float(style.get("opacity", 0.8), 0.8)
    width = _positive_float(style.get("line_width_mm", 0.15), 0.15)
    attrs = ['id="layer-BEND_LINES"']
    if ctx.options.include_metadata:
        attrs.extend(
            [
                f'data-layer-id="{BEND_LINES_LAYER_ID}"',
                'data-layer-key="BEND_LINES"',
                'data-layer-name="BEND_LINES"',
                'data-layer-origin="board-regions-bend-lines"',
            ]
        )
    attrs.extend(
        [
            'fill="none"',
            f'stroke="{color}"',
            f'stroke-width="{ctx.fmt(width)}"',
            f'opacity="{ctx.fmt(min(1.0, max(0.0, opacity)))}"',
            'stroke-linecap="butt"',
        ]
    )
    if str(style.get("line_style", "dashed")).strip().lower() == "dashed":
        dash = ctx.fmt(_positive_float(style.get("dash_length_mm", 0.5), 0.5))
        gap = ctx.fmt(_positive_float(style.get("dash_gap_mm", 0.3), 0.3))
        attrs.append(f'stroke-dasharray="{dash} {gap}"')
    return attrs


def _clip_definitions(clip_paths: Mapping[int, str]) -> list[str]:
    if not clip_paths:
        return []
    lines = ["<defs>"]
    for region_index, path in clip_paths.items():
        lines.append(
            f'<clipPath id="bend-lines-region-{region_index}">'
            f'<path d="{path}" fill-rule="evenodd" clip-rule="evenodd"/>'
            "</clipPath>"
        )
    lines.append("</defs>")
    return lines


def _bend_svg_line(ctx: PcbSvgRenderContext, bend: BoardSpaceBendLine) -> str:
    metadata = _bend_metadata(bend) if ctx.options.include_metadata else []
    clip = (
        f'clip-path="url(#bend-lines-region-{bend.region_index})" '
        if bend.clip_to_region
        else ""
    )
    return (
        f'<line x1="{ctx.fmt(ctx.x_to_svg(bend.x1_mils))}" '
        f'y1="{ctx.fmt(ctx.y_to_svg(bend.y1_mils))}" '
        f'x2="{ctx.fmt(ctx.x_to_svg(bend.x2_mils))}" '
        f'y2="{ctx.fmt(ctx.y_to_svg(bend.y2_mils))}" '
        f"{clip}"
        f"{' '.join(metadata)}/>"
    )


def _bend_metadata(bend: BoardSpaceBendLine) -> list[str]:
    metadata = [
        f'data-region-index="{bend.region_index}"',
        f'data-region-name="{html.escape(bend.region_name)}"',
        f'data-source-index="{bend.source_index}"',
    ]
    optional = (
        ("fold-index", bend.fold_index),
        ("angle-deg", bend.angle_deg),
        ("radius-mils", bend.radius_mils),
        ("extension-mm", bend.extension_mm),
    )
    metadata.extend(
        f'data-{name}="{value:g}"' for name, value in optional if value is not None
    )
    return metadata


def _region_local_origin(region: AltiumStackRegion) -> tuple[float, float] | None:
    vertices = tuple(region.outline_vertices or ())
    finite = tuple(
        (float(x), float(y))
        for x, y in vertices
        if isfinite(float(x)) and isfinite(float(y))
    )
    if not finite:
        return None
    return min(x for x, _ in finite), min(y for _, y in finite)


def _lift_line(
    region_index: int,
    region_name: str,
    source_index: int,
    line: AltiumStackBendLine,
    origin_x: float,
    origin_y: float,
) -> tuple[BoardSpaceBendLine | None, str | None]:
    coordinates, coordinate_error = _bend_coordinates(line)
    if coordinates is None:
        return None, coordinate_error
    angle, angle_error = _optional_finite(line.angle_deg, "bend angle")
    if angle_error is not None:
        return None, angle_error
    radius, radius_error = _optional_finite(line.radius_mils, "bend radius")
    if radius_error is not None:
        return None, radius_error
    x1, y1, x2, y2 = coordinates
    return (
        BoardSpaceBendLine(
            region_index=region_index,
            region_name=region_name,
            source_index=source_index,
            fold_index=line.fold_index,
            angle_deg=angle,
            radius_mils=radius,
            x1_mils=(origin_x + x1) / _INTERNAL_UNITS_PER_MIL,
            y1_mils=(origin_y + y1) / _INTERNAL_UNITS_PER_MIL,
            x2_mils=(origin_x + x2) / _INTERNAL_UNITS_PER_MIL,
            y2_mils=(origin_y + y2) / _INTERNAL_UNITS_PER_MIL,
        ),
        None,
    )


def _bend_coordinates(
    line: AltiumStackBendLine,
) -> tuple[tuple[float, float, float, float] | None, str | None]:
    raw = (line.x1, line.y1, line.x2, line.y2)
    if any(value is None for value in raw):
        return None, "bend-line endpoints are incomplete"
    coordinates = tuple(float(value) for value in raw if value is not None)
    if len(coordinates) != 4 or not all(isfinite(value) for value in coordinates):
        return None, "bend-line endpoints are not finite"
    return coordinates, None  # type: ignore[return-value]


def _optional_finite(
    value: object | None, label: str
) -> tuple[float | None, str | None]:
    if value is None:
        return None, None
    parsed = float(value)
    if not isfinite(parsed):
        return None, f"{label} is not finite"
    return parsed, None


def _region_path(ctx: PcbSvgRenderContext, region: AltiumStackRegion) -> str:
    rings: list[str] = []
    for vertices in (region.outline_vertices, *tuple(region.hole_vertices or ())):
        ring = _ring_path(ctx, vertices)
        if ring:
            rings.append(ring)
    return " ".join(rings)


def _ring_path(
    ctx: PcbSvgRenderContext, vertices: Iterable[tuple[float, float]]
) -> str:
    points = tuple(vertices)
    if len(points) < 3:
        return ""
    coordinates: list[tuple[float, float]] = []
    for x, y in points:
        x_mils = float(x) / _INTERNAL_UNITS_PER_MIL
        y_mils = float(y) / _INTERNAL_UNITS_PER_MIL
        if not isfinite(x_mils) or not isfinite(y_mils):
            return ""
        coordinates.append((ctx.x_to_svg(x_mils), ctx.y_to_svg(y_mils)))
    first_x, first_y = coordinates[0]
    commands = [f"M {ctx.fmt(first_x)} {ctx.fmt(first_y)}"]
    commands.extend(f"L {ctx.fmt(x)} {ctx.fmt(y)}" for x, y in coordinates[1:])
    commands.append("Z")
    return " ".join(commands)


def _finite_float(value: object, default: float) -> float:
    try:
        parsed = float(value)  # type: ignore[arg-type]
    except TypeError, ValueError:
        return default
    return parsed if isfinite(parsed) else default


def _positive_float(value: object, default: float) -> float:
    parsed = _finite_float(value, default)
    return parsed if parsed > 0.0 else default


def _nonnegative_float(value: object, default: float) -> float:
    parsed = _finite_float(value, default)
    return parsed if parsed >= 0.0 else default


__all__ = [
    "BEND_LINES_LAYER_ID",
    "BendLinesRenderer",
    "BoardSpaceBendLine",
    "bend_line_view_bounds",
    "board_space_bend_lines",
    "display_bend_lines",
]
