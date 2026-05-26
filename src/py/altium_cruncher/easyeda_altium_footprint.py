"""EasyEDA footprint to Altium PcbLib mapping."""

from __future__ import annotations

import html
import json
import math
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from altium_monkey.altium_pcb_enums import PadShape, PcbRegionKind
from altium_monkey.altium_pcblib import AltiumPcbLib
from altium_monkey.altium_record_pcb__shapebased_region import (
    AltiumPcbShapeBasedRegion,
    PcbExtendedVertex,
)
from altium_monkey.altium_record_types import PcbLayer
from easyeda_monkey.easyeda_footprint import EasyEdaFootprint


_SVG_ARC_RE = re.compile(
    r"M\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\s+"
    r"A\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\s+"
    r"([-+]?\d*\.?\d+)\s+([01])\s+([01])\s+"
    r"([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)",
    re.IGNORECASE,
)
_PATH_TOKEN_RE = re.compile(
    r"[AaCcHhLlMmQqSsTtVvZz]|[-+]?(?:\d+\.\d+|\d+|\.\d+)(?:[eE][-+]?\d+)?"
)


@dataclass(frozen=True)
class EasyEdaFootprintImportPolicy:
    """Mapping controls for the initial direct Altium footprint importer."""

    mils_per_easyeda_unit: float = 10.0
    invert_y: bool = True
    include_source_graphics: bool = True
    include_source_text: bool = False
    include_non_pad_holes: bool = True
    default_graphic_width_mils: float = 10.0
    curve_approximation_segments: int = 12
    arc_approximation_max_degrees: float = 15.0


@dataclass(frozen=True)
class EasyEdaFootprintImportResult:
    """Generated PcbLib and report for a footprint import."""

    library: AltiumPcbLib
    report: "EasyEdaFootprintMappingReport"


@dataclass
class EasyEdaFootprintMappingReport:
    """Human-readable report for EasyEDA footprint mapping."""

    lcsc_id: str
    footprint_name: str
    source_pad_count: int = 0
    generated_pad_count: int = 0
    generated_hole_pad_count: int = 0
    custom_pad_count: int = 0
    slotted_pad_count: int = 0
    track_count: int = 0
    track_segment_count: int = 0
    circle_count: int = 0
    arc_count: int = 0
    rectangle_count: int = 0
    region_count: int = 0
    text_count: int = 0
    unsupported_count: int = 0
    unsupported_graphics: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    layers: dict[str, int] = field(default_factory=dict)
    policy: dict[str, Any] = field(default_factory=dict)
    transform: dict[str, float | bool] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def write_json(self, path: Path) -> None:
        path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")


@dataclass(frozen=True)
class _EePoint:
    x: float
    y: float


@dataclass(frozen=True)
class _MilsPoint:
    x: float
    y: float


@dataclass(frozen=True)
class _RegionArc:
    center: _MilsPoint
    radius_mils: float
    start_angle_degrees: float
    end_angle_degrees: float


@dataclass(frozen=True)
class _RegionVertex:
    point: _MilsPoint
    arc_to_next: _RegionArc | None = None


@dataclass(frozen=True)
class _PathParseResult:
    vertices: list[_RegionVertex]
    approximations: tuple[str, ...] = ()


@dataclass(frozen=True)
class _FootprintTransform:
    anchor_x: float
    anchor_y: float
    scale: float
    invert_y: bool

    def point(self, point: _EePoint) -> _MilsPoint:
        y = point.y - self.anchor_y
        if self.invert_y:
            y = -y
        return _MilsPoint(
            x=(point.x - self.anchor_x) * self.scale,
            y=y * self.scale,
        )

    def scalar(self, value: float) -> float:
        return float(value) * self.scale

    def rotation(self, degrees: float) -> float:
        return -float(degrees) if self.invert_y else float(degrees)


def load_easyeda_footprint_input(
    path: Path,
) -> tuple[EasyEdaFootprint, dict[str, Any] | None]:
    """Load either a full EasyEDA/LCSC API response or an EasyEdaFootprint JSON file."""

    data = json.loads(path.read_text(encoding="utf-8"))
    source_data = data if isinstance(data, dict) and "result" in data else None
    return EasyEdaFootprint.from_json(data), source_data


def build_altium_pcblib_from_easyeda_footprint(
    easyeda_footprint: EasyEdaFootprint,
    *,
    source_data: dict[str, Any] | None = None,
    footprint_name: str | None = None,
    policy: EasyEdaFootprintImportPolicy | None = None,
) -> EasyEdaFootprintImportResult:
    """Build a one-footprint Altium PcbLib from an EasyEDA footprint."""

    policy = policy or EasyEdaFootprintImportPolicy()
    name = (footprint_name or easyeda_footprint.info.name or easyeda_footprint.info.lcsc_id or "EasyEDA_Footprint").strip()
    report = EasyEdaFootprintMappingReport(
        lcsc_id=easyeda_footprint.info.lcsc_id,
        footprint_name=name,
        source_pad_count=len(easyeda_footprint.pads),
        policy=asdict(policy),
    )
    transform = _build_transform(easyeda_footprint, source_data, policy)
    report.transform = {
        "anchor_x": transform.anchor_x,
        "anchor_y": transform.anchor_y,
        "mils_per_easyeda_unit": transform.scale,
        "invert_y": transform.invert_y,
    }

    library = AltiumPcbLib()
    footprint = library.add_footprint(name, description=easyeda_footprint.info.name)

    _add_pads(footprint, easyeda_footprint, transform, report)
    if policy.include_non_pad_holes:
        _add_non_pad_holes(footprint, easyeda_footprint, transform, report)
    _add_tracks(footprint, easyeda_footprint, transform, report)
    if policy.include_source_graphics:
        _add_raw_graphics(footprint, source_data, transform, policy, report)
    if policy.include_source_text:
        _add_texts(footprint, easyeda_footprint, transform, report)

    if library._authoring_builder is not None:
        library._sync_from_authored_library(library._authoring_builder.build())
    return EasyEdaFootprintImportResult(library=library, report=report)


def render_easyeda_footprint_source_svg(
    easyeda_footprint: EasyEdaFootprint,
    *,
    source_data: dict[str, Any] | None = None,
) -> str:
    """Render a simple source-side EasyEDA footprint SVG for review."""

    min_x, min_y, max_x, max_y = _source_bounds(easyeda_footprint, source_data)
    margin = max(5.0, (max_x - min_x) * 0.05, (max_y - min_y) * 0.05)
    min_x -= margin
    min_y -= margin
    max_x += margin
    max_y += margin
    width = max(1.0, max_x - min_x)
    height = max(1.0, max_y - min_y)
    parts = [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{min_x:.4f} {min_y:.4f} '
            f'{width:.4f} {height:.4f}" width="{width:.1f}" height="{height:.1f}" '
            f'data-doc-id="easyeda-footprint-source-{_attr(easyeda_footprint.info.lcsc_id)}">'
        ),
        '<rect x="{:.4f}" y="{:.4f}" width="{:.4f}" height="{:.4f}" fill="#101418"/>'.format(
            min_x, min_y, width, height
        ),
        '<g fill="none" stroke-linecap="round" stroke-linejoin="round">',
    ]

    for pad in easyeda_footprint.pads:
        color = "#C87932" if pad.layer_id != "11" else "#D8D8D8"
        layer_attrs = _source_layer_attrs(pad.layer_id, color=color, role="pad")
        shape = pad.shape.upper()
        if shape == "OVAL":
            if pad.width >= pad.height:
                half_straight = max((pad.width - pad.height) / 2.0, 0.0)
                x1 = pad.x - half_straight
                y1 = pad.y
                x2 = pad.x + half_straight
                y2 = pad.y
                stroke_width = pad.height
            else:
                half_straight = max((pad.height - pad.width) / 2.0, 0.0)
                x1 = pad.x
                y1 = pad.y - half_straight
                x2 = pad.x
                y2 = pad.y + half_straight
                stroke_width = pad.width
            parts.append(
                f'<line x1="{x1:.4f}" y1="{y1:.4f}" x2="{x2:.4f}" y2="{y2:.4f}" '
                f'stroke="{color}" stroke-width="{max(stroke_width, 0.1):.4f}" '
                f'stroke-linecap="round" fill="none" '
                f'transform="rotate({pad.rotation:.4f} {pad.x:.4f} {pad.y:.4f})" '
                f'{layer_attrs}/>'
            )
        elif shape == "ELLIPSE":
            parts.append(
                f'<ellipse cx="{pad.x:.4f}" cy="{pad.y:.4f}" rx="{pad.width / 2:.4f}" '
                f'ry="{pad.height / 2:.4f}" fill="{color}" stroke="none" '
                f'transform="rotate({pad.rotation:.4f} {pad.x:.4f} {pad.y:.4f})" '
                f'{layer_attrs}/>'
            )
        else:
            parts.append(
                f'<rect x="{pad.x - pad.width / 2:.4f}" y="{pad.y - pad.height / 2:.4f}" '
                f'width="{pad.width:.4f}" height="{pad.height:.4f}" fill="{color}" stroke="none" '
                f'transform="rotate({pad.rotation:.4f} {pad.x:.4f} {pad.y:.4f})" '
                f'{layer_attrs}/>'
            )
        if pad.hole_radius > 0:
            parts.append(_source_pad_hole_svg(pad))

    for hole in easyeda_footprint.holes:
        parts.append(_source_round_hole_svg(hole.x, hole.y, hole.diameter / 2.0))

    for track in easyeda_footprint.tracks:
        points = _parse_points(track.points_str)
        layer_attrs = _source_layer_attrs(track.layer_id, color="#F3D547", role="graphic")
        for start, end in zip(points, points[1:]):
            parts.append(
                f'<line x1="{start[0]:.4f}" y1="{start[1]:.4f}" '
                f'x2="{end[0]:.4f}" y2="{end[1]:.4f}" stroke="#F3D547" '
                f'stroke-width="{max(track.stroke_width, 0.1):.4f}" {layer_attrs}/>'
            )

    for shape in _raw_shapes(source_data):
        fields = shape.split("~")
        kind = fields[0].upper()
        if kind == "CIRCLE" and len(fields) >= 6:
            layer_attrs = _source_layer_attrs(fields[5], color="#F3D547", role="graphic")
            parts.append(
                f'<circle cx="{_float(fields[1]):.4f}" cy="{_float(fields[2]):.4f}" '
                f'r="{_float(fields[3]):.4f}" stroke="#F3D547" '
                f'stroke-width="{max(_float(fields[4]), 0.1):.4f}" {layer_attrs}/>'
            )
        elif kind == "RECT" and len(fields) >= 6:
            layer_attrs = _source_layer_attrs(fields[5], color="#F3D547", role="graphic")
            parts.append(
                f'<rect x="{_float(fields[1]):.4f}" y="{_float(fields[2]):.4f}" '
                f'width="{_float(fields[3]):.4f}" height="{_float(fields[4]):.4f}" '
                f'stroke="#F3D547" stroke-width="0.5" {layer_attrs}/>'
            )
        elif kind == "ARC" and len(fields) >= 5:
            layer_attrs = _source_layer_attrs(fields[2], color="#F3D547", role="graphic")
            parts.append(
                f'<path d="{_attr(fields[4])}" stroke="#F3D547" '
                f'stroke-width="{max(_float(fields[1]), 0.1):.4f}" {layer_attrs}/>'
            )
    parts.append("</g></svg>")
    return "\n".join(parts)


def _source_pad_hole_svg(pad: Any) -> str:
    points = _parse_points(getattr(pad, "hole_points_str", ""))
    diameter = max(float(getattr(pad, "hole_radius", 0.0) or 0.0) * 2.0, 0.0)
    hole_length = float(getattr(pad, "hole_length", 0.0) or 0.0)
    if diameter > 0 and hole_length > diameter and len(points) >= 2:
        start = points[0]
        end = points[-1]
        attrs = _source_layer_attrs("DRILLS", color="#F6F6F6", role="drill")
        return (
            f'<line x1="{start[0]:.4f}" y1="{start[1]:.4f}" '
            f'x2="{end[0]:.4f}" y2="{end[1]:.4f}" stroke="#101418" '
            f'stroke-width="{diameter:.4f}" stroke-linecap="round" fill="none" '
            f'data-hole-kind="slot" data-pad-designator="{_attr(getattr(pad, "number", ""))}" '
            f"{attrs}/>"
        )
    return _source_round_hole_svg(
        float(getattr(pad, "x", 0.0) or 0.0),
        float(getattr(pad, "y", 0.0) or 0.0),
        float(getattr(pad, "hole_radius", 0.0) or 0.0),
        pad_designator=str(getattr(pad, "number", "") or ""),
    )


def _source_round_hole_svg(
    x: float,
    y: float,
    radius: float,
    *,
    pad_designator: str = "",
) -> str:
    designator_attr = (
        f' data-pad-designator="{_attr(pad_designator)}"' if pad_designator else ""
    )
    return (
        f'<circle cx="{x:.4f}" cy="{y:.4f}" r="{radius:.4f}" fill="#101418" '
        f'stroke="none" data-hole-kind="round"{designator_attr} '
        f'{_source_layer_attrs("DRILLS", color="#F6F6F6", role="drill")}/>'
    )


def _add_pads(footprint: Any, easyeda_footprint: EasyEdaFootprint, transform: _FootprintTransform, report: EasyEdaFootprintMappingReport) -> None:
    for index, pad in enumerate(easyeda_footprint.pads, start=1):
        layer = _map_layer(pad.layer_id)
        _record_layer(report, pad.layer_id)
        if layer is None:
            _unsupported(report, f"pad-layer:{pad.layer_id}:{pad.id or index}")
            continue

        position = transform.point(_EePoint(pad.x, pad.y))
        hole_size_mils = transform.scalar(pad.hole_radius * 2.0)
        slot_length_mils = transform.scalar(pad.hole_length)
        if pad.shape.upper() == "POLYGON" and pad.points_str.strip():
            points = [_transform_tuple(transform, point) for point in _parse_points(pad.points_str)]
            if len(points) >= 3:
                footprint.add_custom_pad(
                    designator=pad.number or str(index),
                    position_mils=(position.x, position.y),
                    outline_points_mils=points,
                    layer=layer,
                    outline_points_are_local=False,
                    anchor_diameter_mils=max(1.0, min(transform.scalar(pad.width), transform.scalar(pad.height), 10.0)),
                )
                report.custom_pad_count += 1
                report.generated_pad_count += 1
                continue
            _unsupported(report, f"pad-polygon-points:{pad.id or index}")

        shape, corner_radius = _pad_shape(pad.shape, pad.width, pad.height)
        footprint.add_pad(
            designator=pad.number or str(index),
            position_mils=(position.x, position.y),
            width_mils=max(transform.scalar(pad.width), 0.1),
            height_mils=max(transform.scalar(pad.height), 0.1),
            layer=layer,
            shape=shape,
            corner_radius_percent=corner_radius,
            rotation_degrees=transform.rotation(pad.rotation),
            hole_size_mils=hole_size_mils,
            plated=pad.is_plated if pad.is_through_hole else None,
            slot_length_mils=slot_length_mils,
            slot_rotation_degrees=_pad_slot_rotation_degrees(pad, transform),
        )
        report.generated_pad_count += 1
        if slot_length_mils > 0:
            report.slotted_pad_count += 1


def _add_non_pad_holes(footprint: Any, easyeda_footprint: EasyEdaFootprint, transform: _FootprintTransform, report: EasyEdaFootprintMappingReport) -> None:
    for index, hole in enumerate(easyeda_footprint.holes, start=1):
        position = transform.point(_EePoint(hole.x, hole.y))
        diameter = max(transform.scalar(hole.diameter), 0.1)
        footprint.add_pad(
            designator=f"HOLE{index}",
            position_mils=(position.x, position.y),
            width_mils=diameter,
            height_mils=diameter,
            layer=PcbLayer.MULTI_LAYER,
            shape=PadShape.CIRCLE,
            hole_size_mils=diameter,
            plated=False,
        )
        report.generated_pad_count += 1
        report.generated_hole_pad_count += 1


def _add_tracks(footprint: Any, easyeda_footprint: EasyEdaFootprint, transform: _FootprintTransform, report: EasyEdaFootprintMappingReport) -> None:
    for index, track in enumerate(easyeda_footprint.tracks, start=1):
        layer = _map_layer(track.layer_id)
        _record_layer(report, track.layer_id)
        if layer is None:
            _unsupported(report, f"track-layer:{track.layer_id}:{track.id or index}")
            continue
        points = [_transform_tuple(transform, point) for point in _parse_points(track.points_str)]
        report.track_count += 1
        report.track_segment_count += _add_track_segments(
            footprint,
            points,
            width_mils=max(transform.scalar(track.stroke_width), 0.1),
            layer=layer,
        )


def _add_raw_graphics(
    footprint: Any,
    source_data: dict[str, Any] | None,
    transform: _FootprintTransform,
    policy: EasyEdaFootprintImportPolicy,
    report: EasyEdaFootprintMappingReport,
) -> None:
    for shape in _raw_shapes(source_data):
        fields = shape.split("~")
        kind = fields[0].upper()
        if kind in {"PAD", "TRACK", "HOLE", "VIA", "TEXT", "SVGNODE"}:
            continue
        if kind == "CIRCLE":
            _add_raw_circle(footprint, fields, transform, policy, report)
        elif kind == "RECT":
            _add_raw_rect(footprint, fields, transform, policy, report)
        elif kind == "ARC":
            _add_raw_arc(footprint, fields, transform, policy, report)
        elif kind == "PL":
            _add_raw_polyline(footprint, fields, transform, policy, report)
        elif kind == "SOLIDREGION":
            _add_raw_solid_region(footprint, fields, transform, policy, report)
        else:
            _unsupported(report, f"shape:{kind}")


def _add_raw_circle(footprint: Any, fields: list[str], transform: _FootprintTransform, policy: EasyEdaFootprintImportPolicy, report: EasyEdaFootprintMappingReport) -> None:
    if len(fields) < 6:
        _unsupported(report, "circle:malformed")
        return
    layer_id = fields[5]
    layer = _map_layer(layer_id)
    _record_layer(report, layer_id)
    if layer is None:
        _unsupported(report, f"circle-layer:{layer_id}:{fields[6] if len(fields) > 6 else ''}")
        return
    center = transform.point(_EePoint(_float(fields[1]), _float(fields[2])))
    footprint.add_arc(
        center_mils=(center.x, center.y),
        radius_mils=transform.scalar(_float(fields[3])),
        start_angle_degrees=0.0,
        end_angle_degrees=360.0,
        width_mils=max(transform.scalar(_float(fields[4])), policy.default_graphic_width_mils),
        layer=layer,
    )
    report.circle_count += 1


def _add_raw_rect(footprint: Any, fields: list[str], transform: _FootprintTransform, policy: EasyEdaFootprintImportPolicy, report: EasyEdaFootprintMappingReport) -> None:
    if len(fields) < 6:
        _unsupported(report, "rect:malformed")
        return
    layer_id = fields[5]
    layer = _map_layer(layer_id)
    _record_layer(report, layer_id)
    if layer is None:
        _unsupported(report, f"rect-layer:{layer_id}:{fields[6] if len(fields) > 6 else ''}")
        return
    x = _float(fields[1])
    y = _float(fields[2])
    w = _float(fields[3])
    h = _float(fields[4])
    stroke_width = _float(fields[8]) if len(fields) > 8 else 1.0
    points = [
        _transform_tuple(transform, (x, y)),
        _transform_tuple(transform, (x + w, y)),
        _transform_tuple(transform, (x + w, y + h)),
        _transform_tuple(transform, (x, y + h)),
        _transform_tuple(transform, (x, y)),
    ]
    report.track_segment_count += _add_track_segments(
        footprint,
        points,
        width_mils=max(transform.scalar(stroke_width), policy.default_graphic_width_mils),
        layer=layer,
    )
    report.rectangle_count += 1


def _add_raw_polyline(footprint: Any, fields: list[str], transform: _FootprintTransform, policy: EasyEdaFootprintImportPolicy, report: EasyEdaFootprintMappingReport) -> None:
    if len(fields) < 5:
        _unsupported(report, "polyline:malformed")
        return
    layer_id = fields[2]
    layer = _map_layer(layer_id)
    _record_layer(report, layer_id)
    if layer is None:
        _unsupported(report, f"polyline-layer:{layer_id}:{fields[5] if len(fields) > 5 else ''}")
        return
    points = [_transform_tuple(transform, point) for point in _parse_points(fields[4])]
    report.track_count += 1
    report.track_segment_count += _add_track_segments(
        footprint,
        points,
        width_mils=max(transform.scalar(_float(fields[1])), policy.default_graphic_width_mils),
        layer=layer,
    )


def _add_raw_arc(footprint: Any, fields: list[str], transform: _FootprintTransform, policy: EasyEdaFootprintImportPolicy, report: EasyEdaFootprintMappingReport) -> None:
    if len(fields) < 5:
        _unsupported(report, "arc:malformed")
        return
    layer_id = fields[2]
    layer = _map_layer(layer_id)
    _record_layer(report, layer_id)
    if layer is None:
        _unsupported(report, f"arc-layer:{layer_id}:{fields[6] if len(fields) > 6 else ''}")
        return
    arc = _parse_svg_arc(fields[4], transform)
    if arc is None:
        _unsupported(report, f"arc-path:{fields[6] if len(fields) > 6 else fields[4][:20]}")
        return
    center, radius_mils, start_angle, end_angle = arc
    footprint.add_arc(
        center_mils=(center.x, center.y),
        radius_mils=radius_mils,
        start_angle_degrees=start_angle,
        end_angle_degrees=end_angle,
        width_mils=max(transform.scalar(_float(fields[1])), policy.default_graphic_width_mils),
        layer=layer,
    )
    report.arc_count += 1


def _add_raw_solid_region(
    footprint: Any,
    fields: list[str],
    transform: _FootprintTransform,
    policy: EasyEdaFootprintImportPolicy,
    report: EasyEdaFootprintMappingReport,
) -> None:
    if len(fields) < 4:
        _unsupported(report, "solidregion:malformed")
        return
    layer_id = fields[1]
    layer = _map_layer(layer_id)
    _record_layer(report, layer_id)
    if layer is None:
        _unsupported(report, f"solidregion-layer:{layer_id}:{fields[5] if len(fields) > 5 else ''}")
        return
    parsed_path = _parse_region_path_vertices(fields[3], transform, policy=policy)
    vertices = parsed_path.vertices
    if len(vertices) < 3:
        _unsupported(report, f"solidregion-path:{fields[5] if len(fields) > 5 else ''}")
        return
    shape_id = fields[5] if len(fields) > 5 else ""
    for approximation in parsed_path.approximations:
        _warning(report, f"solidregion:{shape_id}:{approximation}")
    if any(vertex.arc_to_next is not None for vertex in vertices):
        _add_shape_based_region(footprint, vertices, layer=layer)
    else:
        points = [(vertex.point.x, vertex.point.y) for vertex in vertices]
        footprint.add_region(outline_points_mils=points, layer=layer)
    report.region_count += 1


def _add_shape_based_region(
    footprint: Any,
    vertices: list[_RegionVertex],
    *,
    layer: PcbLayer,
) -> None:
    outline_vertices = list(vertices)
    if _same_mils_point(outline_vertices[0].point, outline_vertices[-1].point):
        outline_vertices = outline_vertices[:-1]

    shape_region = AltiumPcbShapeBasedRegion()
    layer_id = int(layer)
    shape_region.layer = layer_id
    shape_region.is_locked = False
    shape_region.is_keepout = False
    shape_region.net_index = 0xFFFF
    shape_region.polygon_index = 0xFFFF
    shape_region.component_index = 0xFFFF
    shape_region.kind = PcbRegionKind.COPPER
    shape_region.is_shapebased = False
    shape_region.subpoly_index = -1
    shape_region.keepout_restrictions = 0
    shape_region.union_index = 0
    shape_region._flags1_raw = 0x0C
    shape_region._header_skip5 = b"\xFF\xFF\xFF\xFF\x00"
    shape_region._header_skip2 = b"\x00\x00"
    shape_region._props_has_trailing_null = False
    shape_region.properties = {
        "V7_LAYER": PcbLayer(layer_id).to_json_name(),
        "NAME": " ",
        "KIND": "0",
        "SUBPOLYINDEX": "-1",
        "UNIONINDEX": "0",
        "ARCRESOLUTION": "0.5mil",
        "ISSHAPEBASED": "FALSE",
        "CAVITYHEIGHT": "0mil",
    }
    shape_region.outline = [_to_extended_vertex(vertex) for vertex in outline_vertices]
    if shape_region.outline:
        closing = PcbExtendedVertex()
        first = shape_region.outline[0]
        closing.is_round = first.is_round
        closing.x = first.x
        closing.y = first.y
        closing.center_x = first.center_x
        closing.center_y = first.center_y
        closing.radius = first.radius
        closing.start_angle = first.start_angle
        closing.end_angle = first.end_angle
        shape_region.outline.append(closing)
    shape_region.holes = []
    shape_region.hole_count = 0

    footprint._require_authoring_builder()._append_primitive(footprint, shape_region)


def _to_extended_vertex(vertex: _RegionVertex) -> PcbExtendedVertex:
    out = PcbExtendedVertex()
    out.x = _mils_to_internal_units(vertex.point.x)
    out.y = _mils_to_internal_units(vertex.point.y)
    if vertex.arc_to_next is None:
        out.is_round = False
        out.center_x = 0
        out.center_y = 0
        out.radius = 0
        out.start_angle = 0.0
        out.end_angle = 0.0
    else:
        out.is_round = True
        out.center_x = _mils_to_internal_units(vertex.arc_to_next.center.x)
        out.center_y = _mils_to_internal_units(vertex.arc_to_next.center.y)
        out.radius = _mils_to_internal_units(vertex.arc_to_next.radius_mils)
        out.start_angle = float(vertex.arc_to_next.start_angle_degrees)
        out.end_angle = float(vertex.arc_to_next.end_angle_degrees)
    return out


def _add_texts(footprint: Any, easyeda_footprint: EasyEdaFootprint, transform: _FootprintTransform, report: EasyEdaFootprintMappingReport) -> None:
    for index, text in enumerate(easyeda_footprint.texts, start=1):
        layer = _map_layer(text.layer_id)
        _record_layer(report, text.layer_id)
        if layer is None:
            _unsupported(report, f"text-layer:{text.layer_id}:{text.id or index}")
            continue
        position = transform.point(_EePoint(text.x, text.y))
        footprint.add_text(
            text=text.text,
            position_mils=(position.x, position.y),
            height_mils=max(transform.scalar(text.font_size), 1.0),
            stroke_width_mils=max(transform.scalar(text.stroke_width), 0.1),
            rotation_degrees=transform.rotation(text.rotation),
            layer=layer,
        )
        report.text_count += 1


def _add_track_segments(footprint: Any, points: list[tuple[float, float]], *, width_mils: float, layer: PcbLayer) -> int:
    count = 0
    for start, end in zip(points, points[1:]):
        if _same_point(start, end):
            continue
        footprint.add_track(start, end, width_mils=width_mils, layer=layer)
        count += 1
    return count


def _pad_shape(shape: str, width: float, height: float) -> tuple[PadShape, int | None]:
    normalized = shape.strip().upper()
    if normalized == "ELLIPSE":
        if math.isclose(float(width), float(height), rel_tol=0.01, abs_tol=0.01):
            return PadShape.CIRCLE, None
        return PadShape.ROUNDED_RECTANGLE, 100
    if normalized == "OVAL":
        return PadShape.ROUNDED_RECTANGLE, 100
    return PadShape.RECTANGLE, None


def _pad_slot_rotation_degrees(pad: Any, transform: _FootprintTransform) -> float:
    if float(getattr(pad, "hole_length", 0.0) or 0.0) <= 0:
        return 0.0

    points = _parse_points(getattr(pad, "hole_points_str", ""))
    if len(points) >= 2:
        start = transform.point(_EePoint(points[0][0], points[0][1]))
        end = transform.point(_EePoint(points[-1][0], points[-1][1]))
        if not _same_point((start.x, start.y), (end.x, end.y)):
            absolute_angle = math.degrees(math.atan2(end.y - start.y, end.x - start.x))
            pad_rotation = transform.rotation(float(getattr(pad, "rotation", 0.0) or 0.0))
            return absolute_angle - pad_rotation

    shape = str(getattr(pad, "shape", "") or "").strip().upper()
    width = float(getattr(pad, "width", 0.0) or 0.0)
    height = float(getattr(pad, "height", 0.0) or 0.0)
    if shape == "OVAL" and height > width:
        return -90.0 if transform.invert_y else 90.0
    return 0.0


def _build_transform(
    easyeda_footprint: EasyEdaFootprint,
    source_data: dict[str, Any] | None,
    policy: EasyEdaFootprintImportPolicy,
) -> _FootprintTransform:
    min_x, min_y, max_x, max_y = _source_bounds(easyeda_footprint, source_data)
    return _FootprintTransform(
        anchor_x=(min_x + max_x) / 2.0,
        anchor_y=(min_y + max_y) / 2.0,
        scale=policy.mils_per_easyeda_unit,
        invert_y=policy.invert_y,
    )


def _source_bounds(
    easyeda_footprint: EasyEdaFootprint,
    source_data: dict[str, Any] | None,
) -> tuple[float, float, float, float]:
    points: list[tuple[float, float]] = []
    for pad in easyeda_footprint.pads:
        half_w = pad.width / 2.0
        half_h = pad.height / 2.0
        points.extend(
            [
                (pad.x - half_w, pad.y - half_h),
                (pad.x + half_w, pad.y + half_h),
            ]
        )
        points.extend(_parse_points(pad.points_str))
    for track in easyeda_footprint.tracks:
        points.extend(_parse_points(track.points_str))
    for hole in easyeda_footprint.holes:
        r = hole.diameter / 2.0
        points.extend([(hole.x - r, hole.y - r), (hole.x + r, hole.y + r)])

    for shape in _raw_shapes(source_data):
        fields = shape.split("~")
        kind = fields[0].upper()
        if kind == "CIRCLE" and len(fields) >= 4:
            cx = _float(fields[1])
            cy = _float(fields[2])
            r = _float(fields[3])
            points.extend([(cx - r, cy - r), (cx + r, cy + r)])
        elif kind == "RECT" and len(fields) >= 5:
            x = _float(fields[1])
            y = _float(fields[2])
            points.extend([(x, y), (x + _float(fields[3]), y + _float(fields[4]))])
        elif kind == "ARC" and len(fields) >= 5:
            points.extend(_parse_path_points(fields[4]))
        elif kind == "PL" and len(fields) >= 5:
            points.extend(_parse_points(fields[4]))
        elif kind == "SOLIDREGION" and len(fields) >= 4:
            points.extend(_parse_path_points(fields[3]))

    if not points:
        return (-5.0, -5.0, 5.0, 5.0)
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return min(xs), min(ys), max(xs), max(ys)


def _map_layer(layer_id: str) -> PcbLayer | None:
    normalized = str(layer_id or "").strip()
    return {
        "1": PcbLayer.TOP,
        "2": PcbLayer.BOTTOM,
        "3": PcbLayer.TOP_OVERLAY,
        "4": PcbLayer.BOTTOM_OVERLAY,
        "5": PcbLayer.TOP_PASTE,
        "6": PcbLayer.BOTTOM_PASTE,
        "7": PcbLayer.TOP_SOLDER,
        "8": PcbLayer.BOTTOM_SOLDER,
        "10": PcbLayer.MECHANICAL_1,
        "11": PcbLayer.MULTI_LAYER,
        "12": PcbLayer.MECHANICAL_1,
        "13": PcbLayer.MECHANICAL_13,
        "14": PcbLayer.MECHANICAL_14,
        "15": PcbLayer.MECHANICAL_1,
        "99": PcbLayer.MECHANICAL_13,
        "100": PcbLayer.MECHANICAL_14,
        "101": PcbLayer.TOP_OVERLAY,
    }.get(normalized)


def _source_layer_attrs(layer_id: str, *, color: str, role: str) -> str:
    normalized = str(layer_id or "").strip() or "UNKNOWN"
    display_name = _easyeda_layer_display_name(normalized)
    return (
        f'data-layer-id="{_attr("easyeda-" + normalized)}" '
        f'data-layer-key="{_attr("E" + normalized)}" '
        f'data-layer-name="{_attr("EASYEDA_" + normalized)}" '
        f'data-layer-display-name="{_attr(display_name)}" '
        f'data-layer-role="{_attr(role)}" '
        f'data-color="{_attr(color)}"'
    )


def _easyeda_layer_display_name(layer_id: str) -> str:
    return {
        "1": "EasyEDA Top Copper",
        "2": "EasyEDA Bottom Copper",
        "3": "EasyEDA Top Silkscreen",
        "4": "EasyEDA Bottom Silkscreen",
        "5": "EasyEDA Top Paste",
        "6": "EasyEDA Bottom Paste",
        "7": "EasyEDA Top Solder Mask",
        "8": "EasyEDA Bottom Solder Mask",
        "10": "EasyEDA Board Outline",
        "11": "EasyEDA Multi-Layer Pads",
        "12": "EasyEDA Document",
        "13": "EasyEDA Component Shape",
        "14": "EasyEDA Lead Shape",
        "15": "EasyEDA Polarity",
        "99": "EasyEDA Board Outline",
        "100": "EasyEDA Component Shape",
        "101": "EasyEDA Top Silkscreen",
        "DRILLS": "EasyEDA Drills",
    }.get(layer_id, f"EasyEDA Layer {layer_id}")


def _record_layer(report: EasyEdaFootprintMappingReport, layer_id: str) -> None:
    key = str(layer_id or "").strip() or "<empty>"
    report.layers[key] = report.layers.get(key, 0) + 1


def _unsupported(report: EasyEdaFootprintMappingReport, value: str) -> None:
    report.unsupported_graphics.append(value)
    report.unsupported_count = len(report.unsupported_graphics)


def _warning(report: EasyEdaFootprintMappingReport, value: str) -> None:
    if value not in report.warnings:
        report.warnings.append(value)


def _raw_shapes(source_data: dict[str, Any] | None) -> list[str]:
    if not source_data:
        return []
    result = source_data.get("result", {})
    package = result.get("packageDetail", {})
    data_str = package.get("dataStr", {})
    shapes = data_str.get("shape", [])
    return [shape for shape in shapes if isinstance(shape, str)]


def _parse_points(value: str) -> list[tuple[float, float]]:
    parts = str(value or "").replace(",", " ").split()
    points: list[tuple[float, float]] = []
    for index in range(0, len(parts) - 1, 2):
        points.append((_float(parts[index]), _float(parts[index + 1])))
    return points


def _parse_path_points(value: str) -> list[tuple[float, float]]:
    return [
        (vertex.point.x, vertex.point.y)
        for vertex in _parse_region_path_vertices(
            value,
            _FootprintTransform(0.0, 0.0, 1.0, False),
            policy=EasyEdaFootprintImportPolicy(),
        ).vertices
    ]


def _parse_region_path_vertices(
    value: str,
    transform: _FootprintTransform,
    *,
    policy: EasyEdaFootprintImportPolicy,
) -> _PathParseResult:
    tokens = _PATH_TOKEN_RE.findall(value or "")
    vertices: list[_RegionVertex] = []
    approximations: list[str] = []
    index = 0
    command = ""
    current_x = 0.0
    current_y = 0.0
    start_x = 0.0
    start_y = 0.0
    last_cubic_control: _EePoint | None = None
    last_quadratic_control: _EePoint | None = None
    previous_op = ""

    def is_command(token: str) -> bool:
        return len(token) == 1 and token.isalpha()

    def take_float() -> float:
        nonlocal index
        value = _float(tokens[index])
        index += 1
        return value

    def append_point(point: _EePoint) -> None:
        vertices.append(_RegionVertex(transform.point(point)))

    def add_approximation(kind: str, segment_count: int) -> None:
        approximations.append(f"approximated {kind} with {segment_count} line segment(s)")

    def absolute_point(x: float, y: float, *, relative: bool) -> _EePoint:
        if relative:
            return _EePoint(current_x + x, current_y + y)
        return _EePoint(x, y)

    try:
        while index < len(tokens):
            if is_command(tokens[index]):
                command = tokens[index]
                index += 1
            if not command:
                break

            relative = command.islower()
            op = command.upper()
            if op == "M":
                x = take_float()
                y = take_float()
                current_x = current_x + x if relative else x
                current_y = current_y + y if relative else y
                start_x = current_x
                start_y = current_y
                append_point(_EePoint(current_x, current_y))
                command = "l" if relative else "L"
                last_cubic_control = None
                last_quadratic_control = None
            elif op == "L":
                end = absolute_point(take_float(), take_float(), relative=relative)
                current_x = end.x
                current_y = end.y
                append_point(end)
                last_cubic_control = None
                last_quadratic_control = None
            elif op == "H":
                current_x = current_x + take_float() if relative else take_float()
                append_point(_EePoint(current_x, current_y))
                last_cubic_control = None
                last_quadratic_control = None
            elif op == "V":
                current_y = current_y + take_float() if relative else take_float()
                append_point(_EePoint(current_x, current_y))
                last_cubic_control = None
                last_quadratic_control = None
            elif op == "A":
                start = _EePoint(current_x, current_y)
                rx = take_float()
                ry = take_float()
                x_axis_rotation = take_float()
                large_arc = bool(int(take_float()))
                sweep = bool(int(take_float()))
                end = absolute_point(take_float(), take_float(), relative=relative)
                current_x = end.x
                current_y = end.y
                arc = _region_arc_from_svg(
                    start,
                    end,
                    rx,
                    ry,
                    x_axis_rotation,
                    large_arc,
                    sweep,
                    transform,
                )
                if arc is not None and vertices:
                    previous = vertices[-1]
                    vertices[-1] = _RegionVertex(previous.point, arc_to_next=arc)
                    append_point(end)
                else:
                    segment_count = _append_approximated_svg_arc(
                        vertices,
                        start,
                        end,
                        rx,
                        ry,
                        x_axis_rotation,
                        large_arc,
                        sweep,
                        transform,
                        policy,
                    )
                    add_approximation("elliptical arc", segment_count)
                last_cubic_control = None
                last_quadratic_control = None
            elif op == "C":
                start = _EePoint(current_x, current_y)
                control1 = absolute_point(take_float(), take_float(), relative=relative)
                control2 = absolute_point(take_float(), take_float(), relative=relative)
                end = absolute_point(take_float(), take_float(), relative=relative)
                segment_count = _append_approximated_cubic_bezier(
                    vertices, start, control1, control2, end, transform, policy
                )
                add_approximation("cubic bezier", segment_count)
                current_x = end.x
                current_y = end.y
                last_cubic_control = control2
                last_quadratic_control = None
            elif op == "S":
                start = _EePoint(current_x, current_y)
                if previous_op in {"C", "S"} and last_cubic_control is not None:
                    control1 = _EePoint(
                        (2.0 * current_x) - last_cubic_control.x,
                        (2.0 * current_y) - last_cubic_control.y,
                    )
                else:
                    control1 = start
                control2 = absolute_point(take_float(), take_float(), relative=relative)
                end = absolute_point(take_float(), take_float(), relative=relative)
                segment_count = _append_approximated_cubic_bezier(
                    vertices, start, control1, control2, end, transform, policy
                )
                add_approximation("smooth cubic bezier", segment_count)
                current_x = end.x
                current_y = end.y
                last_cubic_control = control2
                last_quadratic_control = None
            elif op == "Q":
                start = _EePoint(current_x, current_y)
                control = absolute_point(take_float(), take_float(), relative=relative)
                end = absolute_point(take_float(), take_float(), relative=relative)
                segment_count = _append_approximated_quadratic_bezier(
                    vertices, start, control, end, transform, policy
                )
                add_approximation("quadratic bezier", segment_count)
                current_x = end.x
                current_y = end.y
                last_cubic_control = None
                last_quadratic_control = control
            elif op in {"Q", "S"}:
                # Kept unreachable for static readability if new path commands are added.
                break
            elif op == "T":
                start = _EePoint(current_x, current_y)
                if previous_op in {"Q", "T"} and last_quadratic_control is not None:
                    control = _EePoint(
                        (2.0 * current_x) - last_quadratic_control.x,
                        (2.0 * current_y) - last_quadratic_control.y,
                    )
                else:
                    control = start
                end = absolute_point(take_float(), take_float(), relative=relative)
                segment_count = _append_approximated_quadratic_bezier(
                    vertices, start, control, end, transform, policy
                )
                add_approximation("smooth quadratic bezier", segment_count)
                current_x = end.x
                current_y = end.y
                last_cubic_control = None
                last_quadratic_control = control
            elif op == "Z":
                current_x = start_x
                current_y = start_y
                command = ""
                last_cubic_control = None
                last_quadratic_control = None
            else:
                break
            previous_op = op
    except (IndexError, ValueError):
        return _PathParseResult(vertices=vertices, approximations=tuple(approximations))
    return _PathParseResult(vertices=vertices, approximations=tuple(approximations))


def _append_approximated_svg_arc(
    vertices: list[_RegionVertex],
    start: _EePoint,
    end: _EePoint,
    rx: float,
    ry: float,
    x_axis_rotation: float,
    large_arc: bool,
    sweep: bool,
    transform: _FootprintTransform,
    policy: EasyEdaFootprintImportPolicy,
) -> int:
    params = _svg_arc_parameters(
        start.x,
        start.y,
        end.x,
        end.y,
        abs(float(rx)),
        abs(float(ry)),
        math.radians(float(x_axis_rotation)),
        large_arc,
        sweep,
    )
    if params is None:
        vertices.append(_RegionVertex(transform.point(end)))
        return 1

    center_x, center_y, radius_x, radius_y, phi, theta1, delta_theta = params
    segment_count = _arc_segment_count(math.degrees(abs(delta_theta)), policy)
    cos_phi = math.cos(phi)
    sin_phi = math.sin(phi)
    for index in range(1, segment_count + 1):
        theta = theta1 + (delta_theta * index / segment_count)
        x = (
            center_x
            + (radius_x * math.cos(theta) * cos_phi)
            - (radius_y * math.sin(theta) * sin_phi)
        )
        y = (
            center_y
            + (radius_x * math.cos(theta) * sin_phi)
            + (radius_y * math.sin(theta) * cos_phi)
        )
        vertices.append(_RegionVertex(transform.point(_EePoint(x, y))))
    return segment_count


def _append_approximated_cubic_bezier(
    vertices: list[_RegionVertex],
    start: _EePoint,
    control1: _EePoint,
    control2: _EePoint,
    end: _EePoint,
    transform: _FootprintTransform,
    policy: EasyEdaFootprintImportPolicy,
) -> int:
    segment_count = _curve_segment_count(policy)
    for index in range(1, segment_count + 1):
        t = index / segment_count
        inv = 1.0 - t
        x = (
            (inv * inv * inv * start.x)
            + (3.0 * inv * inv * t * control1.x)
            + (3.0 * inv * t * t * control2.x)
            + (t * t * t * end.x)
        )
        y = (
            (inv * inv * inv * start.y)
            + (3.0 * inv * inv * t * control1.y)
            + (3.0 * inv * t * t * control2.y)
            + (t * t * t * end.y)
        )
        vertices.append(_RegionVertex(transform.point(_EePoint(x, y))))
    return segment_count


def _append_approximated_quadratic_bezier(
    vertices: list[_RegionVertex],
    start: _EePoint,
    control: _EePoint,
    end: _EePoint,
    transform: _FootprintTransform,
    policy: EasyEdaFootprintImportPolicy,
) -> int:
    segment_count = _curve_segment_count(policy)
    for index in range(1, segment_count + 1):
        t = index / segment_count
        inv = 1.0 - t
        x = (inv * inv * start.x) + (2.0 * inv * t * control.x) + (t * t * end.x)
        y = (inv * inv * start.y) + (2.0 * inv * t * control.y) + (t * t * end.y)
        vertices.append(_RegionVertex(transform.point(_EePoint(x, y))))
    return segment_count


def _curve_segment_count(policy: EasyEdaFootprintImportPolicy) -> int:
    return max(2, int(policy.curve_approximation_segments))


def _arc_segment_count(sweep_degrees: float, policy: EasyEdaFootprintImportPolicy) -> int:
    max_degrees = max(1.0, float(policy.arc_approximation_max_degrees))
    return max(2, int(math.ceil(float(sweep_degrees) / max_degrees)))


def _region_arc_from_svg(
    start: _EePoint,
    end: _EePoint,
    rx: float,
    ry: float,
    x_axis_rotation: float,
    large_arc: bool,
    sweep: bool,
    transform: _FootprintTransform,
) -> _RegionArc | None:
    rx_f = abs(float(rx))
    ry_f = abs(float(ry))
    if not math.isclose(rx_f, ry_f, rel_tol=0.01, abs_tol=0.01):
        return None

    center = _svg_arc_center(
        start.x,
        start.y,
        end.x,
        end.y,
        rx_f,
        ry_f,
        math.radians(float(x_axis_rotation)),
        large_arc,
        sweep,
    )
    if center is None:
        return None

    center_mils = transform.point(_EePoint(center[0], center[1]))
    start_mils = transform.point(start)
    end_mils = transform.point(end)
    start_angle = math.degrees(
        math.atan2(start_mils.y - center_mils.y, start_mils.x - center_mils.x)
    )
    end_angle_base = math.degrees(
        math.atan2(end_mils.y - center_mils.y, end_mils.x - center_mils.x)
    )
    end_angle = _arc_end_angle_for_svg_flags(
        start_angle,
        end_angle_base,
        sweep=sweep,
        invert_y=transform.invert_y,
    )
    return _RegionArc(
        center=center_mils,
        radius_mils=transform.scalar(rx_f),
        start_angle_degrees=start_angle,
        end_angle_degrees=end_angle,
    )


def _arc_end_angle_for_svg_flags(
    start_angle: float,
    end_angle: float,
    *,
    sweep: bool,
    invert_y: bool,
) -> float:
    ccw = _svg_arc_is_ccw_after_transform(sweep, invert_y)
    if ccw:
        return start_angle + ((end_angle - start_angle) % 360.0)
    return start_angle - ((start_angle - end_angle) % 360.0)


def _svg_arc_is_ccw_after_transform(sweep: bool, invert_y: bool) -> bool:
    return (not sweep) if invert_y else sweep


def _parse_svg_arc(
    value: str,
    transform: _FootprintTransform,
) -> tuple[_MilsPoint, float, float, float] | None:
    match = _SVG_ARC_RE.search(value or "")
    if not match:
        return None
    x1, y1, rx, ry, x_axis_rotation, large_arc_flag, sweep_flag, x2, y2 = match.groups()
    rx_f = abs(_float(rx))
    ry_f = abs(_float(ry))
    if not math.isclose(rx_f, ry_f, rel_tol=0.01, abs_tol=0.01):
        return None

    center = _svg_arc_center(
        _float(x1),
        _float(y1),
        _float(x2),
        _float(y2),
        rx_f,
        ry_f,
        math.radians(_float(x_axis_rotation)),
        bool(int(large_arc_flag)),
        bool(int(sweep_flag)),
    )
    if center is None:
        return None
    center_mils = transform.point(_EePoint(center[0], center[1]))
    start_mils = transform.point(_EePoint(_float(x1), _float(y1)))
    end_mils = transform.point(_EePoint(_float(x2), _float(y2)))
    start_angle = math.degrees(math.atan2(start_mils.y - center_mils.y, start_mils.x - center_mils.x))
    end_angle_base = math.degrees(math.atan2(end_mils.y - center_mils.y, end_mils.x - center_mils.x))
    ccw = _svg_arc_is_ccw_after_transform(bool(int(sweep_flag)), transform.invert_y)
    if ccw:
        end_angle = start_angle + ((end_angle_base - start_angle) % 360.0)
        return center_mils, transform.scalar(rx_f), start_angle, end_angle

    # Altium arcs render counterclockwise from start to end. For clockwise SVG
    # arcs, reverse the endpoints so the same curve uses Altium's positive sweep.
    return center_mils, transform.scalar(rx_f), end_angle_base, start_angle


def _svg_arc_center(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    rx: float,
    ry: float,
    phi: float,
    large_arc: bool,
    sweep: bool,
) -> tuple[float, float] | None:
    params = _svg_arc_parameters(x1, y1, x2, y2, rx, ry, phi, large_arc, sweep)
    if params is None:
        return None
    return params[0], params[1]


def _svg_arc_parameters(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    rx: float,
    ry: float,
    phi: float,
    large_arc: bool,
    sweep: bool,
) -> tuple[float, float, float, float, float, float, float] | None:
    if rx <= 0 or ry <= 0:
        return None
    cos_phi = math.cos(phi)
    sin_phi = math.sin(phi)
    dx = (x1 - x2) / 2.0
    dy = (y1 - y2) / 2.0
    x1p = cos_phi * dx + sin_phi * dy
    y1p = -sin_phi * dx + cos_phi * dy
    lam = (x1p * x1p) / (rx * rx) + (y1p * y1p) / (ry * ry)
    if lam > 1.0:
        scale = math.sqrt(lam)
        rx *= scale
        ry *= scale
    numerator = rx * rx * ry * ry - rx * rx * y1p * y1p - ry * ry * x1p * x1p
    denominator = rx * rx * y1p * y1p + ry * ry * x1p * x1p
    if denominator == 0:
        return None
    factor = math.sqrt(max(0.0, numerator / denominator))
    if large_arc == sweep:
        factor = -factor
    cxp = factor * (rx * y1p / ry)
    cyp = factor * (-ry * x1p / rx)
    cx = cos_phi * cxp - sin_phi * cyp + (x1 + x2) / 2.0
    cy = sin_phi * cxp + cos_phi * cyp + (y1 + y2) / 2.0

    start_vector = ((x1p - cxp) / rx, (y1p - cyp) / ry)
    end_vector = ((-x1p - cxp) / rx, (-y1p - cyp) / ry)
    theta1 = _angle_between((1.0, 0.0), start_vector)
    delta_theta = _angle_between(start_vector, end_vector)
    if not sweep and delta_theta > 0:
        delta_theta -= math.tau
    elif sweep and delta_theta < 0:
        delta_theta += math.tau

    return cx, cy, rx, ry, phi, theta1, delta_theta


def _angle_between(
    start: tuple[float, float],
    end: tuple[float, float],
) -> float:
    cross = (start[0] * end[1]) - (start[1] * end[0])
    dot = (start[0] * end[0]) + (start[1] * end[1])
    return math.atan2(cross, dot)


def _transform_tuple(transform: _FootprintTransform, point: tuple[float, float]) -> tuple[float, float]:
    mils = transform.point(_EePoint(point[0], point[1]))
    return mils.x, mils.y


def _same_point(a: tuple[float, float], b: tuple[float, float]) -> bool:
    return math.isclose(a[0], b[0], abs_tol=1e-6) and math.isclose(a[1], b[1], abs_tol=1e-6)


def _same_mils_point(a: _MilsPoint, b: _MilsPoint) -> bool:
    return math.isclose(a.x, b.x, abs_tol=1e-6) and math.isclose(a.y, b.y, abs_tol=1e-6)


def _mils_to_internal_units(value: float) -> int:
    return int(round(float(value) * 10000.0))


def _float(value: Any, default: float = 0.0) -> float:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return default


def _attr(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)
