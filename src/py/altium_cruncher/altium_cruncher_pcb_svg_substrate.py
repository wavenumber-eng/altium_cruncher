"""Bare PCB substrate for compositions containing copper and solder-mask film."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
import hashlib
import html
import math
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
from altium_monkey.altium_board import resolve_outline_arc_segment
from shapely.geometry import Polygon, box
from shapely.geometry.base import BaseGeometry

from .pcb_board_surface_appearance import (
    BoardRegionAppearance,
    BoardSurfaceAppearanceIndex,
)
from .pcb_board_region_envelope_index import BoardRegionEnvelopeIndex

if TYPE_CHECKING:
    from altium_monkey.altium_board import BoardOutlineVertex
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc
    from altium_monkey.altium_record_pcb__pad import AltiumPcbPad
    from altium_monkey.altium_record_pcb__via import AltiumPcbVia


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


@dataclass(frozen=True)
class _BoardOpenSpaceIndex:
    """Conservative board/opening test used to suppress invisible aperture art."""

    region_index: BoardRegionEnvelopeIndex
    opening_bounds_mils: tuple[tuple[float, float, float, float], ...]
    clearance_mils: float = 1e-3
    material_geometry: BaseGeometry | None = None
    material_geometry_trusted: bool = True
    _strict_material_geometry: BaseGeometry | None = field(
        init=False, repr=False, compare=False, default=None
    )
    _material_wkb_sha256: str | None = field(
        init=False, repr=False, compare=False, default=None
    )

    def __post_init__(self) -> None:
        if self.material_geometry_trusted and self.material_geometry is not None:
            object.__setattr__(
                self,
                "_strict_material_geometry",
                self.material_geometry.buffer(-self.clearance_mils),
            )
        if self.material_geometry is not None:
            object.__setattr__(
                self,
                "_material_wkb_sha256",
                hashlib.sha256(self.material_geometry.wkb).hexdigest(),
            )

    def cache_identity(self) -> dict[str, object]:
        """Identify every input that can change the conservative skip result."""

        return {
            "clearance_mils": self.clearance_mils,
            "opening_bounds_mils": self.opening_bounds_mils,
            "material_geometry_trusted": self.material_geometry_trusted,
            "material_wkb_sha256": self._material_wkb_sha256,
        }

    def may_intersect(
        self,
        *,
        anchor_mm: tuple[float, float],
        bounds_local_mm: tuple[float, float, float, float, float, float],
    ) -> bool:
        mm_per_mil = 0.0254
        left = (anchor_mm[0] + bounds_local_mm[0]) / mm_per_mil
        top = (anchor_mm[1] + bounds_local_mm[1]) / mm_per_mil
        right = (anchor_mm[0] + bounds_local_mm[3]) / mm_per_mil
        bottom = (anchor_mm[1] + bounds_local_mm[4]) / mm_per_mil
        query_box = box(left, top, right, bottom)
        if not self.material_geometry_trusted:
            return True
        if self.material_geometry is not None:
            material = self._strict_material_geometry
            fully_inside = bool(
                material is not None
                and not material.is_empty
                and material.covers(query_box)
            )
        else:
            fully_inside = self.region_index.fully_contains_bounds(
                left,
                top,
                right,
                bottom,
                clearance_mils=self.clearance_mils,
            )
        if not fully_inside:
            return True
        tolerance = self.clearance_mils
        return any(
            left <= opening[2] + tolerance
            and right >= opening[0] - tolerance
            and top <= opening[3] + tolerance
            and bottom >= opening[1] - tolerance
            for opening in self.opening_bounds_mils
        )


def _space_id(index: _BoardOpenSpaceIndex | None) -> object:
    return None if index is None else index.cache_identity()


def _board_material_geometry(
    pcbdoc: AltiumPcbDoc,
) -> tuple[BaseGeometry | None, float, bool]:
    outline = pcbdoc.board.outline if pcbdoc.board is not None else None
    if outline is None:
        return None, 0.0, False
    outer, outer_error = _outline_ring(outline.vertices)
    holes = []
    maximum_error = outer_error
    for cutout in outline.cutouts:
        ring, error = _outline_ring(cutout)
        maximum_error = max(maximum_error, error)
        if len(ring) >= 3:
            holes.append(ring)
    if len(outer) < 3:
        return None, maximum_error, False
    geometry = Polygon(outer, holes)
    if not geometry.is_valid:
        return None, maximum_error, False
    if geometry.is_empty:
        return None, maximum_error, False
    # Erode past the maximum arc chord error before declaring a strict
    # interior. This makes tessellation uncertainty conservative.
    return geometry, maximum_error + 1e-3, True


def _outline_ring(
    vertices: Sequence[BoardOutlineVertex],
) -> tuple[list[tuple[float, float]], float]:
    if not vertices:
        return [], 0.0
    points: list[tuple[float, float]] = []
    maximum_error = 0.0
    step_limit = math.radians(0.5)
    for index, current in enumerate(vertices):
        nxt = vertices[(index + 1) % len(vertices)]
        if not points:
            points.append((float(current.x_mils), float(current.y_mils)))
        if not getattr(current, "is_arc", False):
            points.append((float(nxt.x_mils), float(nxt.y_mils)))
            continue
        radius = float(current.radius_mils)
        if radius <= 0.0:
            radius = math.hypot(
                float(current.x_mils) - float(current.center_x_mils),
                float(current.y_mils) - float(current.center_y_mils),
            )
        clockwise, sweep_degrees = resolve_outline_arc_segment(current, nxt)
        sweep = math.radians(sweep_degrees)
        steps = max(1, math.ceil(sweep / step_limit))
        increment = sweep / steps
        maximum_error = max(
            maximum_error,
            radius * (1.0 - math.cos(increment * 0.5)),
        )
        start = math.atan2(
            float(current.y_mils) - float(current.center_y_mils),
            float(current.x_mils) - float(current.center_x_mils),
        )
        direction = -1.0 if clockwise else 1.0
        for step in range(1, steps + 1):
            angle = start + direction * increment * step
            points.append(
                (
                    float(current.center_x_mils) + radius * math.cos(angle),
                    float(current.center_y_mils) + radius * math.sin(angle),
                )
            )
    if len(points) > 1 and points[-1] == points[0]:
        points.pop()
    return points, maximum_error


def _cutout_opening_bounds(
    pcbdoc: AltiumPcbDoc,
) -> list[tuple[float, float, float, float]]:
    outline = pcbdoc.board.outline if pcbdoc.board is not None else None
    result: list[tuple[float, float, float, float]] = []
    for cutout in outline.cutouts if outline is not None else ():
        xs = [float(vertex.x_mils) for vertex in cutout]
        ys = [float(vertex.y_mils) for vertex in cutout]
        for vertex in cutout:
            if vertex.is_arc and vertex.radius_mils > 0.0:
                xs.extend(
                    (
                        vertex.center_x_mils - vertex.radius_mils,
                        vertex.center_x_mils + vertex.radius_mils,
                    )
                )
                ys.extend(
                    (
                        vertex.center_y_mils - vertex.radius_mils,
                        vertex.center_y_mils + vertex.radius_mils,
                    )
                )
        if xs and ys:
            result.append((min(xs), min(ys), max(xs), max(ys)))
    return result


def _pad_opening_bounds(
    renderer: BoardSubstrateRenderer,
    pcbdoc: AltiumPcbDoc,
    side: str,
    layer: PcbLayer,
) -> list[tuple[float, float, float, float]]:
    result = []
    for pad in pcbdoc.pads:
        if not _pad_is_open_on_side(renderer, pad, side, layer):
            continue
        diameter = float(pad.hole_size_mils)
        slot_length = max(float(pad.slot_size or 0) / 10000.0, diameter)
        radius = max(diameter, slot_length) * 0.5
        center_x, center_y = pad.hole_center_mils(layer)
        result.append(
            (center_x - radius, center_y - radius, center_x + radius, center_y + radius)
        )
    return result


def _pad_is_open_on_side(
    renderer: BoardSubstrateRenderer,
    pad: AltiumPcbPad,
    side: str,
    layer: PcbLayer,
) -> bool:
    return bool(
        getattr(pad, "hole_size", 0) > 0
        and not renderer._should_skip_primitive_for_svg(pad)
        and pad._should_render_on_layer(layer)
        and not bool(
            getattr(pad, "is_plated", False)
            and getattr(pad, f"is_tenting_{side}", False)
        )
    )


def _via_opening_bounds(
    renderer: BoardSubstrateRenderer,
    pcbdoc: AltiumPcbDoc,
    side: str,
) -> list[tuple[float, float, float, float]]:
    result = []
    for via in pcbdoc.vias:
        if not _via_is_open_on_side(renderer, via, side):
            continue
        radius = float(via.hole_size_mils) * 0.5
        if radius > 0.0:
            result.append(
                (
                    via.x_mils - radius,
                    via.y_mils - radius,
                    via.x_mils + radius,
                    via.y_mils + radius,
                )
            )
    return result


def _via_is_open_on_side(
    renderer: BoardSubstrateRenderer, via: AltiumPcbVia, side: str
) -> bool:
    return bool(
        not renderer._should_skip_primitive_for_svg(via)
        and _via_bore_is_mechanically_open(via)
        and all(
            via._spans_layer(layer) for layer in (PcbLayer.TOP, PcbLayer.BOTTOM)
        )
        and not bool(getattr(via, f"is_tent_{side}", False))
    )


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

    def open_space_index(
        self,
        pcbdoc: AltiumPcbDoc,
        side: str,
        region_index: BoardRegionEnvelopeIndex,
    ) -> _BoardOpenSpaceIndex:
        """Build a conservative spatial index matching the occlusion mask policy."""

        if side not in {"top", "bottom"}:
            raise ValueError("board open-space side must be top or bottom")
        layer = PcbLayer.TOP if side == "top" else PcbLayer.BOTTOM
        bounds = _cutout_opening_bounds(pcbdoc)
        bounds.extend(_pad_opening_bounds(self, pcbdoc, side, layer))
        bounds.extend(_via_opening_bounds(self, pcbdoc, side))
        material_geometry, arc_clearance, material_geometry_trusted = (
            _board_material_geometry(pcbdoc)
        )
        return _BoardOpenSpaceIndex(
            region_index,
            tuple(bounds),
            max(1e-3, arc_clearance),
            material_geometry,
            material_geometry_trusted,
        )

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
        outline = pcbdoc.board.outline if pcbdoc.board is not None else None
        if outline is None:
            return openings
        for cutout in outline.cutouts:
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
