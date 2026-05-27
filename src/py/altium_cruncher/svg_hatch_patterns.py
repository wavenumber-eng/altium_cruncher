"""Reusable SVG hatch/hash pattern helpers."""

from __future__ import annotations

import html
import math

MIN_HATCH_SPACING_MM = 0.05
MIN_HATCH_LINE_WIDTH_MM = 0.01
MIN_DASH_MM = 0.05


def fmt_svg_number(value: float) -> str:
    """Format a compact SVG numeric value."""
    return f"{float(value):.4f}".rstrip("0").rstrip(".")


def svg_hatch_pattern_defs(
    *,
    pattern_id: str,
    stroke_color: str,
    spacing_mm: float,
    angle_deg: float,
    line_width_mm: float = 0.08,
    opacity: float = 0.55,
    indent: str = "    ",
) -> list[str]:
    """Build SVG pattern defs for clipping hatches through any filled shape."""
    spacing = _positive_float(spacing_mm, minimum=MIN_HATCH_SPACING_MM)
    line_width = _positive_float(line_width_mm, minimum=MIN_HATCH_LINE_WIDTH_MM)
    bounded_opacity = min(max(float(opacity), 0.0), 1.0)
    safe_id = html.escape(str(pattern_id), quote=True)
    safe_color = html.escape(str(stroke_color), quote=True)
    return [
        f'{indent}<pattern id="{safe_id}" patternUnits="userSpaceOnUse" '
        f'width="{fmt_svg_number(spacing)}" height="{fmt_svg_number(spacing)}" '
        f'patternTransform="rotate({fmt_svg_number(float(angle_deg))})">',
        f'{indent}  <line x1="0" y1="0" x2="0" y2="{fmt_svg_number(spacing)}" '
        f'stroke="{safe_color}" stroke-width="{fmt_svg_number(line_width)}" '
        f'opacity="{fmt_svg_number(bounded_opacity)}" stroke-linecap="butt"/>',
        f"{indent}</pattern>",
    ]


def svg_stroke_dasharray_for_style(
    *,
    outline_style: str,
    dash_mm: float,
) -> str:
    """Return a dasharray value for a named outline style."""
    style = str(outline_style or "solid").strip().lower()
    if style == "solid":
        return ""
    if style != "dashed":
        raise ValueError("outline_style must be 'solid' or 'dashed'")
    dash = _positive_float(dash_mm, minimum=MIN_DASH_MM)
    return f"{fmt_svg_number(dash)} {fmt_svg_number(dash)}"


def _positive_float(value: float, *, minimum: float) -> float:
    number = float(value)
    if not math.isfinite(number) or number < minimum:
        raise ValueError(f"Expected a finite value >= {minimum}")
    return number


__all__ = [
    "MIN_DASH_MM",
    "MIN_HATCH_LINE_WIDTH_MM",
    "MIN_HATCH_SPACING_MM",
    "fmt_svg_number",
    "svg_hatch_pattern_defs",
    "svg_stroke_dasharray_for_style",
]
