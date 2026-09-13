"""Adapt renderer-neutral Geometer illustration geometry to SVG markup."""

from __future__ import annotations

from typing import Any
import xml.etree.ElementTree as ET

_SVG = "http://www.w3.org/2000/svg"


def geometry_svg(rendered: object, outline_width_mm: float) -> tuple[str, tuple]:
    """Return SVG markup and outline segments used by board annotation."""
    geometry = rendered.geometry
    root = ET.Element(f"{{{_SVG}}}svg")
    _append_background(root, geometry)
    _append_surfaces(root, geometry)
    _append_lines(root, geometry)
    outline = tuple(
        ((line.start[0], -line.start[1]), (line.end[0], -line.end[1]))
        for line in geometry.lines
        if line.width >= outline_width_mm * 0.9
    )
    return ET.tostring(root, encoding="unicode"), outline


def _number(value: float) -> str:
    value = 0.0 if value == 0 else value
    return f"{value:.10g}"


def _append_background(root: ET.Element, geometry: object) -> None:
    presentation = geometry.presentation
    if presentation.transparent_background:
        return
    bounds = geometry.bounds
    ET.SubElement(
        root,
        f"{{{_SVG}}}rect",
        {
            "x": _number(bounds.min[0]),
            "y": _number(-bounds.max[1]),
            "width": _number(bounds.max[0] - bounds.min[0]),
            "height": _number(bounds.max[1] - bounds.min[1]),
            "fill": presentation.background,
        },
    )


def _ring_commands(rings: object) -> list[str]:
    commands: list[str] = []
    for ring in rings:
        if not ring.points:
            continue
        x, y = ring.points[0]
        commands.append(f"M{_number(x)} {_number(-y)}")
        commands.extend(
            f"L{_number(point_x)} {_number(-point_y)}"
            for point_x, point_y in ring.points[1:]
        )
        commands.append("Z")
    return commands


def _append_surfaces(root: ET.Element, geometry: object) -> None:
    presentation = geometry.presentation
    for surface in geometry.surfaces:
        for layer in surface.layers:
            commands = _ring_commands(layer.rings)
            if not commands:
                continue
            attributes = {
                "d": "".join(commands),
                "fill": layer.fill,
                "fill-rule": presentation.fill_rule,
                "stroke": layer.fill,
                "stroke-width": _number(presentation.seam_width),
                "stroke-linejoin": presentation.line_join,
            }
            if layer.opacity < 0.999:
                attributes["opacity"] = _number(layer.opacity)
            ET.SubElement(root, f"{{{_SVG}}}path", attributes)


def _append_lines(root: ET.Element, geometry: object) -> None:
    presentation = geometry.presentation
    for line in geometry.lines:
        ET.SubElement(
            root,
            f"{{{_SVG}}}line",
            {
                "x1": _number(line.start[0]),
                "y1": _number(-line.start[1]),
                "x2": _number(line.end[0]),
                "y2": _number(-line.end[1]),
                "fill": "none",
                "stroke": line.color,
                "stroke-width": _number(line.width),
                "stroke-linecap": presentation.line_cap,
                "stroke-linejoin": presentation.line_join,
            },
        )
