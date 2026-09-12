"""Bare PCB substrate for compositions containing copper and solder-mask film."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import html
from typing import TYPE_CHECKING

from altium_monkey.altium_pcb_svg_renderer import (
    PcbSvgRenderer,
    PcbSvgRenderContext,
    should_render_via_drill_hole,
)
from altium_monkey.altium_record_types import PcbLayer

if TYPE_CHECKING:
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc


BOARD_SUBSTRATE_LAYER_ID = 9014
DEFAULT_SUBSTRATE_COLOR = "#B6A26B"


class BoardSubstrateRenderer(PcbSvgRenderer):
    """Paint the board domain, subtracting physical bores and scoped cutouts."""

    def render_substrate(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        style: Mapping[str, object],
        source_layers: Sequence[PcbLayer] = (),
    ) -> list[str]:
        if not style.get("enabled", True):
            return []
        outline = pcbdoc.board.outline if pcbdoc.board is not None else None
        domain = self._path_from_vertices(ctx, outline.vertices) if outline else ""
        if not domain:
            raise ValueError("BOARD_SUBSTRATE requires a board outline")
        color = html.escape(str(style.get("color", DEFAULT_SUBSTRATE_COLOR)))
        openings = self._cutout_openings(ctx, pcbdoc)
        openings.extend(self._pad_openings(ctx, pcbdoc))
        openings.extend(self._via_openings(ctx, pcbdoc, source_layers))
        attrs = ['id="layer-BOARD_SUBSTRATE"']
        if ctx.options.include_metadata:
            attrs.extend(
                [
                    f'data-layer-id="{BOARD_SUBSTRATE_LAYER_ID}"',
                    'data-layer-key="BOARD_SUBSTRATE"',
                    'data-layer-name="BOARD_SUBSTRATE"',
                    'data-layer-origin="synthetic-board-substrate"',
                ]
            )
        # Independent black shapes make overlapping cutouts/bores a union.
        return [
            f"<g {' '.join(attrs)}>",
            "<defs>",
            '<mask id="board-substrate-openings" maskUnits="userSpaceOnUse" '
            'maskContentUnits="userSpaceOnUse" x="0" y="0" '
            f'width="{ctx.fmt(ctx.width_mm)}" height="{ctx.fmt(ctx.height_mm)}" '
            'style="mask-type:luminance" color-interpolation="sRGB">',
            f'<path d="{domain}" fill="white" fill-rule="evenodd"/>',
            *openings,
            "</mask>",
            "</defs>",
            f'<path d="{domain}" fill="{color}" fill-rule="evenodd" '
            'stroke="none" mask="url(#board-substrate-openings)"/>',
            "</g>",
        ]

    def _cutout_openings(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
    ) -> list[str]:
        openings: list[str] = []
        for cutout in pcbdoc.board.outline.cutouts:
            path = self._path_from_vertices(ctx, cutout)
            if path:
                openings.append(f'<path d="{path}" fill="black" fill-rule="evenodd"/>')
        return openings

    def _pad_openings(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
    ) -> list[str]:
        openings: list[str] = []
        # Physical holes exist even if the pad has no land or its film is tented.
        # The separate film and drill layers determine their final appearance.
        for pad in pcbdoc.pads:
            if pad.hole_size <= 0 or self._should_skip_primitive_for_svg(pad):
                continue
            openings.extend(
                pad._hole_knockout_svg_elements(
                    ctx,
                    PcbLayer.TOP,
                    include_metadata=False,
                    hole_color="black",
                )
            )
        return openings

    def _via_openings(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        source_layers: Sequence[PcbLayer],
    ) -> list[str]:
        openings: list[str] = []
        outer_layers = {
            layer for layer in source_layers if layer in (PcbLayer.TOP, PcbLayer.BOTTOM)
        }
        for via in pcbdoc.vias:
            if self._should_skip_primitive_for_svg(
                via
            ) or not should_render_via_drill_hole(via):
                continue
            # A composed surface includes via mouths on that side. With no outer
            # side selected, the side-neutral substrate shows through vias only.
            if outer_layers:
                if not any(via._spans_layer(layer) for layer in outer_layers):
                    continue
            elif not all(
                via._spans_layer(layer) for layer in (PcbLayer.TOP, PcbLayer.BOTTOM)
            ):
                continue
            radius = via.hole_size_mils * 0.0254 / 2
            if radius > 0:
                openings.append(
                    f'<circle cx="{ctx.fmt(ctx.x_to_svg(via.x_mils))}" '
                    f'cy="{ctx.fmt(ctx.y_to_svg(via.y_mils))}" '
                    f'r="{ctx.fmt(radius)}" fill="black"/>'
                )
        return openings
