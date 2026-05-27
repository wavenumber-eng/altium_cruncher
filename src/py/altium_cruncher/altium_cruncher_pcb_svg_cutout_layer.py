"""Synthetic PCB SVG layer for board-profile cutouts."""

from __future__ import annotations

import html
from typing import TYPE_CHECKING

from altium_monkey.altium_pcb_svg_renderer import PcbSvgRenderer
from altium_cruncher.svg_hatch_patterns import (
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


class CruncherPcbCutoutLayerRenderer(PcbSvgRenderer):
    """Render board cutouts as a dedicated SVG layer artifact."""

    def render_board_cutout_layer(
        self,
        pcbdoc: "AltiumPcbDoc",
        project_parameters: dict[str, str] | None = None,
        *,
        include_hatch: bool = False,
        hatch_spacing_mm: float = 2.0,
        hatch_angle_deg: float = 45.0,
        include_label: bool = False,
        label_text: str = "cutout",
        outline_style: str = "solid",
        outline_dash_mm: float = 1.5,
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
            include_board_outline=False,
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
        lines.extend(
            self._render_cutout_paths(
                ctx,
                cutouts,
                include_hatch=include_hatch,
                include_label=include_label,
                label_text=label_text,
                outline_style=outline_style,
                outline_dash_mm=outline_dash_mm,
            )
        )
        lines.append("  </g>")
        lines.append("</svg>")
        return "\n".join(lines)

    def _cutout_hatch_defs(
        self,
        *,
        hatch_spacing_mm: float,
        hatch_angle_deg: float,
    ) -> list[str]:
        color = html.escape(str(self.options.board_cutout_color or "#FF0000"))
        return svg_hatch_pattern_defs(
            pattern_id=PCB_SVG_BOARD_CUTOUTS_HATCH_PATTERN_ID,
            stroke_color=color,
            spacing_mm=hatch_spacing_mm,
            angle_deg=hatch_angle_deg,
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
                'stroke-width="0.15"',
                'stroke-linejoin="round"',
                'vector-effect="non-scaling-stroke"',
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
    "PCB_SVG_BOARD_CUTOUTS_HATCH_PATTERN_ID",
    "PCB_SVG_BOARD_CUTOUTS_LAYER_ID",
    "PCB_SVG_BOARD_CUTOUTS_LAYER_NAME",
]
