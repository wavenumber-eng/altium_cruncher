"""Bare PCB substrate for compositions containing copper and solder-mask film."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import html
from typing import TYPE_CHECKING
import xml.etree.ElementTree as ET

from altium_monkey.altium_pcb_svg_renderer import (
    PcbSvgRenderer,
    PcbSvgRenderContext,
    should_render_via_drill_hole,
)
from altium_monkey.altium_pcb_enums import PcbIpc4761ViaType
from altium_monkey.altium_pcbdoc_builder import PcbDocNestedConfig
from altium_monkey.altium_record_types import PcbLayer

from .pcb_board_surface_appearance import (
    BoardRegionAppearance,
    BoardSurfaceAppearanceIndex,
)

if TYPE_CHECKING:
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc


BOARD_SUBSTRATE_LAYER_ID = 9014
DEFAULT_SUBSTRATE_COLOR = "#B6A26B"
DEFAULT_FLEX_SUBSTRATE_COLOR = "#D18B28"

_PLUGGED_VIA_TYPES = frozenset(
    {
        PcbIpc4761ViaType.TYPE_3A_PLUGGING,
        PcbIpc4761ViaType.TYPE_3B_PLUGGING,
        PcbIpc4761ViaType.TYPE_4A_PLUGGING_AND_COVERING,
        PcbIpc4761ViaType.TYPE_4B_PLUGGING_AND_COVERING,
    }
)


def _via_bore_is_mechanically_open(via: object) -> bool:
    """Return whether a via bore remains physical open space.

    Monkey's illustration helper intentionally answers whether a drill should
    be drawn. Cruncher's substrate/occlusion domain is stricter: an IPC-4761
    plugged bore is not open space even though its drill may remain useful in
    a fabrication illustration.
    """

    if not should_render_via_drill_hole(via):
        return False
    try:
        via_type = PcbIpc4761ViaType(int(getattr(via, "ipc4761_via_type", 0)))
    except TypeError, ValueError:
        return False
    return via_type not in _PLUGGED_VIA_TYPES


@dataclass(frozen=True)
class BoardMaterialDomain:
    """Reusable board-footprint domain with physical holes removed."""

    path: str
    openings: tuple[str, ...]

    def mask_lines(self, ctx: PcbSvgRenderContext, mask_id: str) -> list[str]:
        return [
            f'<mask id="{mask_id}" maskUnits="userSpaceOnUse" '
            'maskContentUnits="userSpaceOnUse" x="0" y="0" '
            f'width="{ctx.fmt(ctx.width_mm)}" height="{ctx.fmt(ctx.height_mm)}" '
            'style="mask-type:luminance" color-interpolation="sRGB">',
            f'<path d="{self.path}" fill="white" fill-rule="evenodd"/>',
            *self.openings,
            "</mask>",
        ]

    def mask_element(
        self,
        ctx: PcbSvgRenderContext,
        mask_id: str,
        *,
        extent: tuple[float, float, float, float],
        complement: bool = False,
    ) -> ET.Element:
        """Emit the positive domain or its complement over an explicit canvas."""

        x, y, width, height = extent
        mask = ET.Element(
            "{http://www.w3.org/2000/svg}mask",
            {
                "id": mask_id,
                "maskUnits": "userSpaceOnUse",
                "maskContentUnits": "userSpaceOnUse",
                "x": ctx.fmt(x),
                "y": ctx.fmt(y),
                "width": ctx.fmt(width),
                "height": ctx.fmt(height),
                "style": "mask-type:luminance",
                "color-interpolation": "sRGB",
            },
        )
        if complement:
            ET.SubElement(
                mask,
                "{http://www.w3.org/2000/svg}rect",
                {
                    "x": ctx.fmt(x),
                    "y": ctx.fmt(y),
                    "width": ctx.fmt(width),
                    "height": ctx.fmt(height),
                    "fill": "white",
                },
            )
        ET.SubElement(
            mask,
            "{http://www.w3.org/2000/svg}path",
            {
                "d": self.path,
                "fill": "black" if complement else "white",
                "fill-rule": "evenodd",
            },
        )
        for opening in self.openings:
            node = ET.fromstring(opening)
            if complement:
                for item in node.iter():
                    if item.get("fill") == "black":
                        item.set("fill", "white")
                    if item.get("stroke") == "black":
                        item.set("stroke", "white")
            mask.append(node)
        return mask


def saved_board_core_color(pcbdoc: AltiumPcbDoc) -> str | None:
    """Read the saved 3D board-core COLORREF, not a fabrication attribute."""

    if pcbdoc.board is None:
        return None
    raw = pcbdoc.board.raw_record.get("3DCONFIGURATION")
    if not isinstance(raw, str):
        return None
    value = PcbDocNestedConfig.from_value(raw).get_value("CFG3D.BOARDCORECOLOR")
    try:
        color = int(value) if value is not None else -1
    except ValueError:
        return None
    if not 0 <= color <= 0xFFFFFF:
        return None
    return f"#{color & 255:02X}{(color >> 8) & 255:02X}{(color >> 16) & 255:02X}"


class BoardSubstrateRenderer(PcbSvgRenderer):
    """Paint the board domain, subtracting physical bores and scoped cutouts."""

    def render_substrate(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        style: Mapping[str, object],
        source_layers: Sequence[PcbLayer] = (),
        appearance_index: BoardSurfaceAppearanceIndex | None = None,
    ) -> list[str]:
        if not style.get("enabled", True):
            return []
        outline = pcbdoc.board.outline if pcbdoc.board is not None else None
        domain = self._path_from_vertices(ctx, outline.vertices) if outline else ""
        if not domain:
            raise ValueError("BOARD_SUBSTRATE requires a board outline")
        region_paths = _appearance_region_paths(ctx, appearance_index)
        paint_domain = " ".join(path for _appearance, path in region_paths) or domain
        material_domain = self.material_domain(ctx, pcbdoc, source_layers)
        attrs = _substrate_group_attributes(ctx)
        # Independent black shapes make overlapping cutouts/bores a union.
        lines = [
            f"<g {' '.join(attrs)}>",
            "<defs>",
            '<mask id="board-substrate-openings" maskUnits="userSpaceOnUse" '
            'maskContentUnits="userSpaceOnUse" x="0" y="0" '
            f'width="{ctx.fmt(ctx.width_mm)}" height="{ctx.fmt(ctx.height_mm)}" '
            'style="mask-type:luminance" color-interpolation="sRGB">',
            f'<path d="{paint_domain}" fill="white" fill-rule="evenodd"/>',
            *material_domain.openings,
            "</mask>",
            "</defs>",
        ]
        lines.extend(_substrate_paint_lines(ctx, pcbdoc, style, domain, region_paths))
        lines.append("</g>")
        return lines

    def material_domain(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        source_layers: Sequence[PcbLayer] = (),
    ) -> BoardMaterialDomain:
        """Build the board domain shared by substrate and silk clipping."""

        outline = pcbdoc.board.outline if pcbdoc.board is not None else None
        path = self._path_from_vertices(ctx, outline.vertices) if outline else ""
        if not path:
            raise ValueError("board material domain requires a board outline")
        openings = self._cutout_openings(ctx, pcbdoc)
        openings.extend(self._pad_openings(ctx, pcbdoc))
        openings.extend(self._via_openings(ctx, pcbdoc, source_layers))
        return BoardMaterialDomain(path, tuple(openings))

    def occlusion_domain(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        side: str,
    ) -> BoardMaterialDomain:
        """Build board occlusion for opposite-side component visibility.

        The uncut projection may pass through routed cutouts, applicable
        through bores, and beyond the board edge. Film apertures are not
        mechanical openings. Tented or filled bores and blind/buried vias do
        not reveal opposite-side component geometry.
        """

        if side not in {"top", "bottom"}:
            raise ValueError("board occlusion side must be top or bottom")
        outline = pcbdoc.board.outline if pcbdoc.board is not None else None
        path = self._path_from_vertices(ctx, outline.vertices) if outline else ""
        if not path:
            raise ValueError("board occlusion domain requires a board outline")
        openings = self._cutout_openings(ctx, pcbdoc)
        openings.extend(self._pad_occlusion_openings(ctx, pcbdoc, side))
        openings.extend(self._via_occlusion_openings(ctx, pcbdoc, side))
        return BoardMaterialDomain(path, tuple(openings))

    def _pad_occlusion_openings(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        side: str,
    ) -> list[str]:
        layer = PcbLayer.TOP if side == "top" else PcbLayer.BOTTOM
        openings: list[str] = []
        for pad in pcbdoc.pads:
            if pad.hole_size <= 0 or self._should_skip_primitive_for_svg(pad):
                continue
            if not pad._should_render_on_layer(layer):
                continue
            if bool(pad.is_plated and getattr(pad, f"is_tenting_{side}", False)):
                continue
            openings.extend(
                pad._hole_knockout_svg_elements(
                    ctx,
                    layer,
                    include_metadata=False,
                    hole_color="black",
                )
            )
        return openings

    def _via_occlusion_openings(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        side: str,
    ) -> list[str]:
        openings: list[str] = []
        for via in pcbdoc.vias:
            if self._should_skip_primitive_for_svg(via):
                continue
            if not _via_bore_is_mechanically_open(via):
                continue
            if not all(
                via._spans_layer(layer) for layer in (PcbLayer.TOP, PcbLayer.BOTTOM)
            ):
                continue
            if bool(getattr(via, f"is_tent_{side}", False)):
                continue
            radius = via.hole_size_mils * 0.0254 / 2
            if radius > 0:
                openings.append(
                    f'<circle cx="{ctx.fmt(ctx.x_to_svg(via.x_mils))}" '
                    f'cy="{ctx.fmt(ctx.y_to_svg(via.y_mils))}" '
                    f'r="{ctx.fmt(radius)}" fill="black"/>'
                )
        return openings

    def _cutout_openings(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
    ) -> list[str]:
        openings: list[str] = []
        if pcbdoc.board is None:
            return openings
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
            ) or not _via_bore_is_mechanically_open(via):
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


def _appearance_region_paths(
    ctx: PcbSvgRenderContext,
    appearance_index: BoardSurfaceAppearanceIndex | None,
) -> tuple[tuple[BoardRegionAppearance, str], ...]:
    appearances = (
        tuple(appearance_index.regions)
        if appearance_index and not appearance_index.invalid_regions
        else ()
    )
    candidates = (
        (appearance, _region_path(ctx, appearance)) for appearance in appearances
    )
    return tuple((appearance, path) for appearance, path in candidates if path)


def _substrate_group_attributes(ctx: PcbSvgRenderContext) -> list[str]:
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
    return attrs


def _substrate_paint_lines(
    ctx: PcbSvgRenderContext,
    pcbdoc: AltiumPcbDoc,
    style: Mapping[str, object],
    domain: str,
    region_paths: tuple[tuple[BoardRegionAppearance, str], ...],
) -> list[str]:
    if not region_paths:
        color = html.escape(_fallback_substrate_color(pcbdoc, style))
        return [
            f'<path d="{domain}" fill="{color}" fill-rule="evenodd" '
            'stroke="none" mask="url(#board-substrate-openings)"/>'
        ]
    return [
        _substrate_region_line(ctx, pcbdoc, style, appearance, path)
        for appearance, path in region_paths
    ]


def _substrate_region_line(
    ctx: PcbSvgRenderContext,
    pcbdoc: AltiumPcbDoc,
    style: Mapping[str, object],
    appearance: BoardRegionAppearance,
    path: str,
) -> str:
    color = html.escape(_substrate_color(pcbdoc, appearance, style))
    metadata = ""
    if ctx.options.include_metadata:
        metadata = (
            f' data-region-index="{appearance.region.source_index}"'
            f' data-region-name="{html.escape(appearance.region.name)}"'
            f' data-substack-name="{html.escape(appearance.region.substack_name)}"'
            f' data-substrate-material="{html.escape(appearance.substrate_material or "")}"'
        )
    return (
        f'<path d="{path}" fill="{color}" fill-rule="evenodd" '
        f'stroke="none" mask="url(#board-substrate-openings)"{metadata}/>'
    )


def _substrate_color(
    pcbdoc: AltiumPcbDoc,
    appearance: BoardRegionAppearance,
    style: Mapping[str, object],
) -> str:
    override = str(style.get("color", "auto")).strip()
    if override.casefold() != "auto":
        return override
    if appearance.substrate_authored_color:
        return appearance.substrate_authored_color
    if appearance.region.is_flex is True:
        flex = str(style.get("flex_color", DEFAULT_FLEX_SUBSTRATE_COLOR)).strip()
        return flex if flex.casefold() != "auto" else DEFAULT_FLEX_SUBSTRATE_COLOR
    rigid = str(style.get("rigid_color", DEFAULT_SUBSTRATE_COLOR)).strip()
    return saved_board_core_color(pcbdoc) or (
        rigid if rigid.casefold() != "auto" else DEFAULT_SUBSTRATE_COLOR
    )


def _fallback_substrate_color(
    pcbdoc: AltiumPcbDoc,
    style: Mapping[str, object],
) -> str:
    override = str(style.get("color", "auto")).strip()
    if override.casefold() != "auto":
        return override
    rigid = str(style.get("rigid_color", DEFAULT_SUBSTRATE_COLOR)).strip()
    return saved_board_core_color(pcbdoc) or (
        rigid if rigid.casefold() != "auto" else DEFAULT_SUBSTRATE_COLOR
    )


def _region_path(ctx: PcbSvgRenderContext, appearance: BoardRegionAppearance) -> str:
    rings = (appearance.region.outline_mils, *appearance.region.holes_mils)
    commands: list[str] = []
    for ring in rings:
        if len(ring) < 3:
            continue
        first_x, first_y = ring[0]
        commands.append(
            f"M {ctx.fmt(ctx.x_to_svg(first_x))} {ctx.fmt(ctx.y_to_svg(first_y))}"
        )
        commands.extend(
            f"L {ctx.fmt(ctx.x_to_svg(x))} {ctx.fmt(ctx.y_to_svg(y))}"
            for x, y in ring[1:]
        )
        commands.append("Z")
    return " ".join(commands)
