"""Synthetic PCB SVG layer for board-profile cutouts."""

from __future__ import annotations

from collections.abc import Sequence
from .altium_cruncher_pcb_designator_layout import CcaDesignatorFitSession, CcaDesignatorFit

import html
import math
from copy import copy
from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING

from altium_monkey.altium_pcb_svg_renderer import PcbSvgRenderer, PcbSvgRenderOptions
from altium_cruncher.svg_hatch_patterns import (
    fmt_svg_number,
    svg_hatch_pattern_defs,
    svg_stroke_dasharray_for_style,
)

if TYPE_CHECKING:
    from altium_monkey.altium_board import BoardOutlineVertex
    from altium_monkey.altium_pcb_svg_renderer import PcbSvgRenderContext
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc

PCB_SVG_BOARD_CUTOUTS_LAYER_ID = 9002
PCB_SVG_BOARD_CUTOUTS_LAYER_NAME = "BOARD_CUTOUTS"
PCB_SVG_BOARD_CUTOUTS_HATCH_PATTERN_ID = "board-cutout-hatch"


def _validate_cutout_presentation(style: Mapping[str, object]) -> None:
    """Validate fitted-label and opacity controls on the actual render path."""
    for name, default, maximum, positive in (
        ("outline_opacity", 1.0, 1.0, False),
        ("hatch_opacity", 0.55, 1.0, False),
        ("label_opacity", 1.0, 1.0, False),
        ("label_max_font_size_mm", 3.0, math.inf, True),
        ("label_fill_ratio", 0.72, 1.0, True),
        ("label_rotation_min_gain", 0.25, math.inf, False),
    ):
        value = style.get(name, default)
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or value < 0
            or (positive and value == 0)
            or value > maximum
        ):
            raise ValueError(f"Invalid board_cutouts.{name}: {value!r}")
    if not isinstance(style.get("label", ""), str):
        raise ValueError("board_cutouts.label must be a string")


def _pcbdoc_with_cutout_scope(pcbdoc: "AltiumPcbDoc", scope: object) -> "AltiumPcbDoc":
    """Filter a render-only board copy using Mate's existing interior predicate."""
    if scope not in ("all", "interior"):
        raise ValueError("board_cutouts.scope must be 'all' or 'interior'")
    if scope == "all":
        return pcbdoc
    outline = getattr(getattr(pcbdoc, "board", None), "outline", None)
    if outline is None or not outline.cutouts:
        return pcbdoc

    from altium_cruncher.altium_cruncher_mate_graphics import (
        _board_outline_vertex,
        _linearized_outline_points,
        _outline_is_strictly_inside_outline,
    )

    points = _linearized_outline_points(
        {"vertices": [_board_outline_vertex(v) for v in outline.vertices]}
    )
    # Sampling only classifies containment. Retain the original arc/line vertices
    # for all subsequent clip paths, film apertures and visible cutout outlines.
    cutouts = [
        cutout
        for cutout in outline.cutouts
        if len(points) >= 3
        and _outline_is_strictly_inside_outline(
            {"vertices": [_board_outline_vertex(v) for v in cutout]}, points
        )
    ]
    if len(cutouts) == len(outline.cutouts):
        return pcbdoc
    filtered = copy(pcbdoc)
    filtered.board = copy(pcbdoc.board)
    filtered.board.outline = copy(outline)
    filtered.board.outline.cutouts = cutouts
    return filtered


@dataclass(frozen=True, slots=True)
class CruncherPcbCutoutStyle:
    """Resolved cutout styling shared by standalone and composed PCB SVG views."""

    include_overlay: bool = False
    include_hatch: bool = False
    hatch_spacing_mm: float = 2.0
    hatch_angle_deg: float = 45.0
    hatch_line_width_mm: float = 0.08
    include_label: bool = False
    label_text: str = "cutout"
    outline_style: str = "solid"
    outline_dash_mm: float = 1.5
    outline_width_mm: float = 0.15


class CruncherPcbCutoutLayerRenderer(PcbSvgRenderer):
    """Render board cutouts as a dedicated SVG layer artifact."""

    def __init__(
        self,
        options: PcbSvgRenderOptions | None = None,
        *,
        cutout_style: CruncherPcbCutoutStyle | None = None,
    ) -> None:
        super().__init__(options=options)
        self.cutout_style = cutout_style or CruncherPcbCutoutStyle()

    def render_board_cutout_layer(
        self,
        pcbdoc: "AltiumPcbDoc",
        project_parameters: dict[str, str] | None = None,
        *,
        include_hatch: bool = False,
        hatch_spacing_mm: float = 2.0,
        hatch_angle_deg: float = 45.0,
        hatch_line_width_mm: float = 0.08,
        include_label: bool = False,
        label_text: str = "cutout",
        include_board_outline: bool = True,
        outline_style: str = "solid",
        outline_dash_mm: float = 1.5,
        outline_width_mm: float = 0.15,
    ) -> str | None:
        """Render only interior board cutout contours, or ``None`` when absent."""
        outline = getattr(getattr(pcbdoc, "board", None), "outline", None)
        cutouts: list[list[BoardOutlineVertex]] = list(
            getattr(outline, "cutouts", []) or []
        )
        if not cutouts:
            return None

        ctx = self._build_context(  # noqa: SLF001
            pcbdoc,
            project_parameters=project_parameters,
        )
        view_kind = "board_cutouts"
        svg_attrs = self._build_svg_document_attrs(ctx, pcbdoc, view_kind)  # noqa: SLF001
        active_layer_ids = [PCB_SVG_BOARD_CUTOUTS_LAYER_ID]
        extra_defs = (
            self._cutout_hatch_defs(
                hatch_spacing_mm=hatch_spacing_mm,
                hatch_angle_deg=hatch_angle_deg,
                hatch_line_width_mm=hatch_line_width_mm,
            )
            if include_hatch
            else []
        )

        lines = [f"<svg {' '.join(svg_attrs)}>"]
        self._append_svg_metadata(  # noqa: SLF001
            lines,
            ctx,
            view_kind,
            active_layer_ids,
            ["BOARD_CUTOUTS"],
            includes_board_outline=include_board_outline,
            pcbdoc=pcbdoc,
        )
        self._append_svg_defs(  # noqa: SLF001
            lines,
            ctx,
            "",
            "",
            {},
            extra_defs,
        )
        lines.append(f"  <g {' '.join(self._build_scene_attrs(ctx))}>")  # noqa: SLF001
        if include_board_outline and self.options.show_board_outline:
            lines.extend(self._render_board_profile_outline(ctx, outline))
        lines.extend(
            self._render_cutout_paths(
                ctx,
                cutouts,
                include_hatch=include_hatch,
                include_label=include_label,
                label_text=label_text,
                outline_style=outline_style,
                outline_dash_mm=outline_dash_mm,
                outline_width_mm=outline_width_mm,
            )
        )
        lines.append("  </g>")
        lines.append("</svg>")
        return "\n".join(lines)

    def _render_overlay_defs_scene(
        self,
        ctx: "PcbSvgRenderContext",
        pcbdoc: "AltiumPcbDoc",
    ) -> tuple[list[str], list[str]]:
        """Inject configured cutout styling into composed top/bottom PCB views."""
        if not self.cutout_style.include_overlay or not self.options.show_board_outline:
            return [], []
        outline = getattr(getattr(pcbdoc, "board", None), "outline", None)
        cutouts = self._board_cutouts(outline)
        if not cutouts:
            return [], []

        defs = (
            self._cutout_hatch_defs(
                hatch_spacing_mm=self.cutout_style.hatch_spacing_mm,
                hatch_angle_deg=self.cutout_style.hatch_angle_deg,
                hatch_line_width_mm=self.cutout_style.hatch_line_width_mm,
            )
            if self.cutout_style.include_hatch
            else []
        )
        scene = self._render_cutout_paths(
            ctx,
            cutouts,
            include_hatch=self.cutout_style.include_hatch,
            include_label=self.cutout_style.include_label,
            label_text=self.cutout_style.label_text,
            outline_style=self.cutout_style.outline_style,
            outline_dash_mm=self.cutout_style.outline_dash_mm,
            outline_width_mm=self.cutout_style.outline_width_mm,
        )
        return defs, scene

    def _board_cutouts(self, outline: object) -> list[list["BoardOutlineVertex"]]:
        return list(getattr(outline, "cutouts", []) or [])

    def _render_board_profile_outline(
        self,
        ctx: "PcbSvgRenderContext",
        outline: object,
    ) -> list[str]:
        vertices = getattr(outline, "vertices", None)
        if not outline or not vertices:
            return []

        main_path = self._path_from_vertices(ctx, vertices)  # noqa: SLF001
        if not main_path:
            return []

        stroke_color = html.escape(str(self.options.board_outline_color or "#000000"))
        attrs = [
            f'd="{main_path}"',
            'fill="none"',
            f'stroke="{stroke_color}"',
            'stroke-width="0.1"',
            'stroke-linejoin="round"',
            'vector-effect="non-scaling-stroke"',
        ]
        if self.options.include_metadata:
            attrs.append('data-feature="board-outline"')
            attrs.append('data-element-key="board-outline"')
        return [
            '    <g id="board-profile-outline">',
            "      " + f"<path {' '.join(attrs)}/>",
            "    </g>",
        ]

    def _cutout_hatch_defs(
        self,
        *,
        hatch_spacing_mm: float,
        hatch_angle_deg: float,
        hatch_line_width_mm: float,
        hatch_color: str | None = None,
        hatch_opacity: float = 0.55,
    ) -> list[str]:
        color = str(hatch_color or self.options.board_cutout_color or "#FF0000")
        return svg_hatch_pattern_defs(
            pattern_id=PCB_SVG_BOARD_CUTOUTS_HATCH_PATTERN_ID,
            stroke_color=color,
            spacing_mm=hatch_spacing_mm,
            angle_deg=hatch_angle_deg,
            line_width_mm=hatch_line_width_mm,
            opacity=hatch_opacity,
        )

    def _render_cutout_paths(
        self,
        ctx: "PcbSvgRenderContext",
        cutouts: list[list["BoardOutlineVertex"]],
        *,
        include_hatch: bool,
        include_label: bool,
        label_text: str,
        outline_style: str,
        outline_dash_mm: float,
        outline_width_mm: float,
        outline_opacity: float = 1.0,
        label_style: Mapping[str, object] | None = None,
    ) -> list[str]:
        stroke_color = html.escape(str(self.options.board_cutout_color or "#FF0000"))
        fill = (
            f"url(#{PCB_SVG_BOARD_CUTOUTS_HATCH_PATTERN_ID})"
            if include_hatch
            else "none"
        )
        dasharray = svg_stroke_dasharray_for_style(
            outline_style=outline_style,
            dash_mm=outline_dash_mm,
        )
        lines = [
            '    <g id="board-cutouts-layer" data-layer-key="BOARD_CUTOUTS" '
            'data-layer-name="Board Cutouts">'
        ]
        for cutout_index, cutout_vertices in enumerate(cutouts):
            cutout_path = self._path_from_vertices(ctx, cutout_vertices)  # noqa: SLF001
            if not cutout_path:
                continue
            attrs = [
                f'd="{cutout_path}"',
                f'fill="{fill}"',
                f'stroke="{stroke_color}"',
                f'stroke-width="{fmt_svg_number(outline_width_mm)}"',
                f'stroke-opacity="{fmt_svg_number(outline_opacity)}"',
                'stroke-linejoin="round"',
                f'data-outline-style="{html.escape(str(outline_style))}"',
            ]
            if dasharray:
                attrs.append(f'stroke-dasharray="{dasharray}"')
            if self.options.include_metadata:
                attrs.extend(
                    [
                        'data-feature="board-cutout"',
                        f'data-feature-index="{cutout_index}"',
                        f'data-element-key="board-cutout-{cutout_index}"',
                    ]
                )
            lines.append("      " + f"<path {' '.join(attrs)}/>")
            if include_label:
                if label_style is not None:
                    label_line = self._fitted_cutout_label_element(
                        ctx, cutout_vertices, cutout_index=cutout_index,
                        label_text=label_text, style=label_style,
                    )
                else:
                    label_line = self._cutout_label_element(
                        ctx,
                        cutout_vertices,
                        cutout_index=cutout_index,
                        label_text=label_text,
                        stroke_color=stroke_color,
                    )
                if label_line:
                    lines.append(label_line)
        lines.append("    </g>")
        return lines

    def _fitted_cutout_label_element(
        self,
        ctx: "PcbSvgRenderContext",
        vertices: list["BoardOutlineVertex"],
        *,
        cutout_index: int,
        label_text: str,
        style: Mapping[str, object],
    ) -> str:
        """Port pcb-autodoc's centroid placement, size fit and bottom reflection."""
        from altium_cruncher.altium_cruncher_mate_graphics import (
            _board_outline_vertex,
            _linearized_outline_points,
        )

        label = label_text.strip()
        points = [
            (ctx.x_to_svg(x), ctx.y_to_svg(y))
            for x, y in _linearized_outline_points(
                {"vertices": [_board_outline_vertex(v) for v in vertices]}
            )
        ]
        if not label or not points:
            return ""
        fit = fit_cutout_label(points, label, style)
        if fit is None:
            return ""
        x, y = fit.center_mm
        size = fit.font_size_mm
        transform = (
            f' transform="rotate({ctx.fmt(fit.rotation_degrees)} {ctx.fmt(x)} {ctx.fmt(y)})"'
            if fit.rotation_degrees else ""
        )
        color = str(style.get("label_color") or self.options.board_cutout_color or "#FF0000")
        text = (
            f'<text data-feature="board-cutout-label" data-feature-index="{cutout_index}" '
            f'x="{ctx.fmt(x)}" y="{ctx.fmt(y)}"{transform} text-anchor="middle" '
            f'dominant-baseline="central" font-size="{ctx.fmt(size)}" '
            f'fill="{html.escape(color)}" '
            f'fill-opacity="{ctx.fmt(float(style.get("label_opacity", 1.0)))}" '
            f'font-family="sans-serif" font-weight="700">{html.escape(label)}</text>'
        )
        if ctx.options.mirror_x:
            return (
                '<g data-feature="board-cutout-label-orientation" '
                f'transform="translate({ctx.fmt(2.0 * x)} 0) scale(-1 1)">'
                f'{text}</g>'
            )
        return text

    def _cutout_label_element(
        self,
        ctx: "PcbSvgRenderContext",
        cutout_vertices: list["BoardOutlineVertex"],
        *,
        cutout_index: int,
        label_text: str,
        stroke_color: str,
    ) -> str:
        points = [
            (ctx.x_to_svg(vertex.x_mils), ctx.y_to_svg(vertex.y_mils))
            for vertex in cutout_vertices
        ]
        if not points:
            return ""
        min_x = min(point[0] for point in points)
        max_x = max(point[0] for point in points)
        min_y = min(point[1] for point in points)
        text_x = (min_x + max_x) / 2.0
        text_y = max(0.4, min_y - 0.6)
        safe_label = html.escape(str(label_text or "cutout"))
        attrs = [
            f'x="{ctx.fmt(text_x)}"',
            f'y="{ctx.fmt(text_y)}"',
            f'fill="{stroke_color}"',
            'font-family="monospace"',
            'font-size="1.4"',
            'text-anchor="middle"',
            'dominant-baseline="baseline"',
        ]
        if self.options.include_metadata:
            attrs.append('data-feature="board-cutout-label"')
            attrs.append(f'data-feature-index="{cutout_index}"')
        return "      " + f"<text {' '.join(attrs)}>{safe_label}</text>"


__all__ = [
    "CruncherPcbCutoutLayerRenderer",
    "CruncherPcbCutoutStyle",
    "PCB_SVG_BOARD_CUTOUTS_HATCH_PATTERN_ID",
    "PCB_SVG_BOARD_CUTOUTS_LAYER_ID",
    "PCB_SVG_BOARD_CUTOUTS_LAYER_NAME",
]


def fit_cutout_label(
    points: Sequence[tuple[float, float]], label: str, style: Mapping[str, object], *,
    session: CcaDesignatorFitSession | None = None,
) -> CcaDesignatorFit | None:
    """Fit inside the contour; require a meaningful gain before rotating."""
    from .altium_cruncher_pcb_designator_layout import (
        CcaComponentGeometryFact, fit_designator_to_geometry,
    )
    if not points or not label:
        return None
    xs, ys = zip(*points)
    geometry = CcaComponentGeometryFact(
        (min(xs), min(ys), max(xs), max(ys)),
        tuple((point, points[(index + 1) % len(points)]) for index, point in enumerate(points)),
    )
    fits = [fit_designator_to_geometry(
        label, geometry, fill_ratio=float(style.get("label_fill_ratio", .72)),
        maximum_font_size_mm=float(style.get("label_max_font_size_mm", 3)),
        manual_rotation_degrees=angle, session=session,
    ) for angle in (0, -90)]
    horizontal, vertical = fits
    best = horizontal
    if vertical and (horizontal is None or vertical.font_size_mm >
                     horizontal.font_size_mm * (1 + float(style.get("label_rotation_min_gain", .25))) + 1e-6):
        best = vertical
    return best if best and best.font_size_mm >= .2 else None
