"""Solder-mask film from the existing Altium SVG aperture geometry."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import copy
from dataclasses import dataclass, replace
import html
import logging
import math
from typing import TYPE_CHECKING, Literal
import xml.etree.ElementTree as ET

from altium_monkey.altium_pcb_property_helpers import parse_pcb_mils_token_as_internal
from altium_monkey.altium_pcb_rule import AltiumSolderMaskExpansionRule
from altium_monkey.altium_pcb_mask_paste_rules import get_pad_mask_expansion_iu
from altium_monkey.altium_pcb_svg_renderer import PcbSvgRenderer, PcbSvgRenderContext
from altium_monkey.altium_pcbdoc_builder import PcbDocNestedConfig
from altium_monkey.altium_record_types import PcbLayer

from .pcb_svg_primitive_dispatch import PrimitiveDispatchCacheMixin
from .pcb_board_surface_appearance import (
    BoardRegionAppearance,
    BoardSurfaceAppearance,
    BoardSurfaceAppearanceIndex,
    BoardSurfaceKind,
)

if TYPE_CHECKING:
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc
    from altium_monkey.altium_record_pcb__pad import AltiumPcbPad
    from altium_monkey.altium_record_pcb__track import AltiumPcbTrack
    from altium_monkey.altium_record_pcb__arc import AltiumPcbArc
    from altium_monkey.altium_record_pcb__fill import AltiumPcbFill
    from altium_monkey.altium_record_pcb__region import AltiumPcbRegion
    from altium_monkey.altium_pcb_extended_primitive_information import (
        AltiumPcbExtendedPrimitiveInformation,
    )


SOLDERMASK_FILM_LAYER_IDS = {
    "SOLDERMASK_FILM_TOP": 9010,
    "SOLDERMASK_FILM_BOTTOM": 9011,
}
DEFAULT_SOLDERMASK_FILM_COLOR = "#176B3A"
DEFAULT_COVERLAY_FILM_COLOR = "#D18B28"
log = logging.getLogger(__name__)


@dataclass(frozen=True)
class SurfaceFilmDomain:
    """Reusable region-local film domain and its aperture geometry."""

    side: Literal["top", "bottom"]
    path: str
    openings: tuple[str, ...]
    region_paths: tuple[tuple[BoardRegionAppearance, str], ...]

    def mask_lines(self, ctx: PcbSvgRenderContext, mask_id: str) -> list[str]:
        return [
            f'<mask id="{mask_id}" maskUnits="userSpaceOnUse" '
            f'maskContentUnits="userSpaceOnUse" x="0" y="0" '
            f'width="{ctx.fmt(ctx.width_mm)}" height="{ctx.fmt(ctx.height_mm)}" '
            'style="mask-type:luminance" color-interpolation="sRGB">',
            f'<path d="{self.path}" fill="white" fill-rule="evenodd"/>',
            *self.openings,
            "</mask>",
        ]


def saved_soldermask_color(
    pcbdoc: AltiumPcbDoc, side: Literal["top", "bottom"]
) -> str | None:
    """Read the saved 3D view's COLORREF; this is not a fabrication attribute."""
    if pcbdoc.board is None:
        return None
    raw = pcbdoc.board.raw_record.get("3DCONFIGURATION")
    if not isinstance(raw, str):
        return None
    config = PcbDocNestedConfig.from_value(raw)
    key = "TOP" if side == "top" else "BOT"
    value = config.get_value(f"CFG3D.{key}SOLDERMASKCOLOR")
    try:
        color = int(value) if value is not None else -1
    except ValueError:
        return None
    if not 0 <= color <= 0xFFFFFF:
        return None
    return f"#{color & 255:02X}{(color >> 8) & 255:02X}{(color >> 16) & 255:02X}"


def _film_opacity(style: Mapping[str, object]) -> float:
    value = style.get("opacity", 1.0)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("soldermask_film.opacity must be a number from 0 to 1")
    opacity = float(value)
    if not math.isfinite(opacity) or not 0 <= opacity <= 1:
        raise ValueError("soldermask_film.opacity must be a number from 0 to 1")
    return opacity


def _valid_appearances(
    appearance_index: BoardSurfaceAppearanceIndex | None,
) -> tuple[BoardRegionAppearance, ...]:
    if appearance_index is None or appearance_index.invalid_regions:
        return ()
    return tuple(appearance_index.regions)


def _film_group_attributes(ctx: PcbSvgRenderContext, token: str) -> list[str]:
    attrs = [f'id="layer-{token}"']
    if ctx.options.include_metadata:
        attrs.extend(
            [
                f'data-layer-id="{SOLDERMASK_FILM_LAYER_IDS[token]}"',
                f'data-layer-key="{token}"',
                f'data-layer-name="{token}"',
                'data-layer-origin="synthetic-soldermask-film"',
            ]
        )
    return attrs


def _film_paint_lines(
    ctx: PcbSvgRenderContext,
    pcbdoc: AltiumPcbDoc,
    style: Mapping[str, object],
    side: Literal["top", "bottom"],
    domain: SurfaceFilmDomain,
    mask_id: str,
    opacity: float,
) -> list[str]:
    if not domain.region_paths:
        color = html.escape(_fallback_film_color(pcbdoc, side, style))
        return [
            f'<path d="{domain.path}" fill="{color}" '
            f'fill-rule="evenodd" opacity="{ctx.fmt(opacity)}" '
            f'mask="url(#{mask_id})"/>'
        ]
    return [
        _film_region_line(
            ctx,
            pcbdoc,
            style,
            side,
            appearance,
            path,
            mask_id,
            opacity,
        )
        for appearance, path in domain.region_paths
    ]


def _film_region_line(
    ctx: PcbSvgRenderContext,
    pcbdoc: AltiumPcbDoc,
    style: Mapping[str, object],
    side: Literal["top", "bottom"],
    appearance: BoardRegionAppearance,
    path: str,
    mask_id: str,
    opacity: float,
) -> str:
    surface = appearance.surface(side)
    color = html.escape(_film_color(pcbdoc, side, surface, style))
    metadata = ""
    if ctx.options.include_metadata:
        metadata = (
            f' data-region-index="{appearance.region.source_index}"'
            f' data-region-name="{html.escape(appearance.region.name)}"'
            f' data-surface-kind="{surface.kind.value}"'
            f' data-surface-material="{html.escape(surface.material or "")}"'
        )
    return (
        f'<path d="{path}" fill="{color}" '
        f'fill-rule="evenodd" opacity="{ctx.fmt(opacity)}" '
        f'mask="url(#{mask_id})"{metadata}/>'
    )


class SoldermaskFilmRenderer(PrimitiveDispatchCacheMixin, PcbSvgRenderer):
    """Reuse native primitive/outline paths and subtract apertures with an SVG mask."""

    def render_film(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        token: str,
        style: Mapping[str, object],
        appearance_index: BoardSurfaceAppearanceIndex | None = None,
    ) -> list[str]:
        if not style.get("enabled", True):
            return []
        opacity = _film_opacity(style)
        side: Literal["top", "bottom"] = "top" if token.endswith("_TOP") else "bottom"
        domain = self.surface_domain(ctx, pcbdoc, side, appearance_index)
        appearances = _valid_appearances(appearance_index)
        if appearances and not domain.region_paths:
            return []
        mask_id = f"soldermask-film-openings-{side}"
        attrs = _film_group_attributes(ctx, token)
        lines = [f"<g {' '.join(attrs)}>", "<defs>"]
        # Independent black cutouts and apertures overlap as a union. Combining
        # unrelated rings into one evenodd path would put film back in overlaps.
        lines.extend(domain.mask_lines(ctx, mask_id))
        lines.append("</defs>")
        lines.extend(
            _film_paint_lines(
                ctx,
                pcbdoc,
                style,
                side,
                domain,
                mask_id,
                opacity,
            )
        )
        lines.append("</g>")
        return lines

    def surface_domain(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        side: Literal["top", "bottom"],
        appearance_index: BoardSurfaceAppearanceIndex | None = None,
    ) -> SurfaceFilmDomain:
        """Build the exact mask domain shared by film and silk rendering."""

        outline = pcbdoc.board.outline if pcbdoc.board is not None else None
        board_path = self._path_from_vertices(ctx, outline.vertices) if outline else ""
        if not board_path:
            raise ValueError("surface film requires a board outline")
        appearances = (
            tuple(appearance_index.regions)
            if appearance_index and not appearance_index.invalid_regions
            else ()
        )
        region_paths = tuple(
            (appearance, _region_path(ctx, appearance))
            for appearance in appearances
            if appearance.surface(side).has_film
        )
        region_paths = tuple(
            (appearance, path) for appearance, path in region_paths if path
        )
        path = (
            " ".join(item_path for _appearance, item_path in region_paths)
            if appearances
            else board_path
        )
        # Aperture IDs must not collide with a physical mask layer in the same SVG.
        self.options = replace(self.options, include_metadata=False)
        layer = PcbLayer.TOP_SOLDER if side == "top" else PcbLayer.BOTTOM_SOLDER
        openings = self._openings(ctx, pcbdoc, layer, side)
        openings.extend(self._cutout_openings(ctx, pcbdoc))
        return SurfaceFilmDomain(side, path, tuple(openings), region_paths)

    def _cutout_openings(
        self, ctx: PcbSvgRenderContext, pcbdoc: AltiumPcbDoc
    ) -> list[str]:
        outline = pcbdoc.board.outline if pcbdoc.board is not None else None
        openings: list[str] = []
        if outline is not None:
            for cutout in outline.cutouts:
                path = self._path_from_vertices(ctx, cutout)
                if path:
                    openings.append(
                        f'<path d="{path}" fill="black" fill-rule="evenodd"/>'
                    )
        return openings

    def _openings(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        layer: PcbLayer,
        side: Literal["top", "bottom"],
    ) -> list[str]:
        elements: list[str] = []
        for collection in (pcbdoc.tracks, pcbdoc.arcs, pcbdoc.fills):
            elements.extend(
                self._render_primitive_collection(ctx, collection, layer, "black")
            )
        elements.extend(self._render_regions_for_layer(ctx, pcbdoc, layer, "black"))
        elements.extend(self._render_texts_for_layer(ctx, pcbdoc, layer, "black"))
        elements.extend(self._extended_openings(ctx, pcbdoc, side))
        copper = PcbLayer.TOP if side == "top" else PcbLayer.BOTTOM
        for pad_index, pad in enumerate(pcbdoc.pads):
            if self._should_skip_primitive_for_svg(pad):
                continue
            if not getattr(pad, f"is_tenting_{side}", False):
                custom = self._custom_pad_opening(ctx, pad, layer, copper, pad_index)
                elements.extend(
                    custom
                    if custom is not None
                    else pad.to_svg(
                        ctx,
                        stroke="black",
                        for_layer=layer,
                        include_metadata=False,
                        render_holes=False,
                    )
                )
            # Physical NPTH bores/slots remain open even when larger than the land.
            # Do not punch via drills through tented film.
            if pad.hole_size > 0 and not pad.is_plated:
                elements.extend(
                    pad._hole_knockout_svg_elements(
                        ctx, layer=copper, include_metadata=False, hole_color="black"
                    )
                )
        elements.extend(self._via_openings(ctx, pcbdoc, layer))
        return elements

    def _via_openings(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        layer: PcbLayer,
    ) -> list[str]:
        elements: list[str] = []
        for via in pcbdoc.vias:
            if self._should_skip_primitive_for_svg(via):
                continue
            aperture = via
            if via.soldermask_expansion_from_hole_edge:
                aperture = copy(via)
                aperture.diameter = via.hole_size
            elements.extend(
                aperture.to_svg(
                    ctx,
                    stroke="black",
                    for_layer=layer,
                    include_metadata=False,
                    render_holes=False,
                )
            )

        return elements

    @staticmethod
    def _custom_pad_opening(
        ctx: PcbSvgRenderContext,
        pad: AltiumPcbPad,
        layer: PcbLayer,
        copper: PcbLayer,
        index: int,
    ) -> list[str] | None:
        custom = pad.custom_shape
        if custom is None:
            return None
        if custom.get_layer_shape(int(layer)) is not None:
            # An authored mask contour is already emitted on the physical layer.
            # It includes its saved expansion and must not be expanded twice.
            return []
        shape = custom.get_layer_shape(int(copper))
        if shape is None:
            return None
        contour = shape.shape_region or shape.region
        if contour is None:
            return None
        geometry = contour.to_svg(
            ctx,
            stroke="black",
            for_layer=copper,
            include_metadata=False,
        )
        expansion = get_pad_mask_expansion_iu(pad)
        if expansion == 0:
            return geometry
        return _offset_contours(
            ctx,
            geometry,
            expansion,
            f"soldermask-custom-pad-{int(layer)}-{index}",
        )

    def _extended_openings(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        side: Literal["top", "bottom"],
    ) -> list[str]:
        """Copper graphics opt into mask apertures through the extended stream.

        Raw track expansion bytes also contain packed user-union data. Only the
        typed Mask records establish that a copper graphic should open the film.
        Indices refer to the source collection, not a filtered layer collection.
        """
        collections = {
            "track": pcbdoc.tracks,
            "arc": pcbdoc.arcs,
            "fill": pcbdoc.fills,
            "region": pcbdoc.regions,
        }
        copper = PcbLayer.TOP if side == "top" else PcbLayer.BOTTOM
        rules = sorted(
            (
                r
                for r in pcbdoc.rules
                if isinstance(r, AltiumSolderMaskExpansionRule)
                and r.enabled is not False
            ),
            key=lambda r: r.priority if r.priority is not None else math.inf,
        )
        elements: list[str] = []
        for record_index, info in enumerate(pcbdoc.extended_primitive_information):
            mode = info.solder_mask_expansion_mode.strip().lower()
            if info.info_type.lower() != "mask" or mode in {"", "none", "0"}:
                continue
            source = self._extended_source(info, collections, copper, side)
            if source is None:
                continue
            kind, index, primitive = source
            expansion = self._extended_expansion(info, rules, kind, index, side)
            if expansion is None:
                continue
            elements.extend(
                self._extended_geometry(
                    ctx,
                    primitive,
                    kind,
                    copper,
                    expansion,
                    f"soldermask-aperture-{side}-{record_index}",
                )
            )
        return elements

    def _extended_source(
        self,
        info: AltiumPcbExtendedPrimitiveInformation,
        collections: dict[str, Sequence],
        copper: PcbLayer,
        side: str,
    ) -> (
        tuple[str, int, AltiumPcbTrack | AltiumPcbArc | AltiumPcbFill | AltiumPcbRegion]
        | None
    ):
        kind = info.primitive_object_id.lower()
        collection = collections.get(kind)
        index = info.primitive_index
        if collection is None or index is None or not 0 <= index < len(collection):
            log.warning(
                "Soldermask film: unsupported or missing %s %s mask source",
                info.primitive_object_id,
                index,
            )
            return None
        primitive = collection[index]
        if primitive.layer != copper or self._should_skip_primitive_for_svg(primitive):
            return None
        if getattr(primitive, f"is_tenting_{side}", False):
            return None
        return kind, index, primitive

    def _extended_expansion(
        self,
        info: AltiumPcbExtendedPrimitiveInformation,
        rules: Sequence[AltiumSolderMaskExpansionRule],
        kind: str,
        index: int,
        side: str,
    ) -> int | None:
        mode = info.solder_mask_expansion_mode.strip().lower()
        if mode in {"manual", "2"}:
            expansion = info.solder_mask_expansion_manual
            if expansion is None:
                log.warning(
                    "Soldermask film: invalid manual expansion for %s %s", kind, index
                )
        elif mode in {"rule", "1"}:
            expansion = self._rule_expansion(rules, kind, index, side)
        else:
            log.warning(
                "Soldermask film: unsupported expansion mode %r for %s %s",
                mode,
                kind,
                index,
            )
            return None
        return expansion

    @staticmethod
    def _extended_geometry(
        ctx: PcbSvgRenderContext,
        primitive: AltiumPcbTrack | AltiumPcbArc | AltiumPcbFill | AltiumPcbRegion,
        kind: str,
        copper: PcbLayer,
        expansion: int,
        mask_id: str,
    ) -> list[str]:
        aperture = primitive
        if kind in {"track", "arc"}:
            aperture = copy(primitive)
            aperture.width = primitive.width + 2 * expansion
            if aperture.width <= 0:
                return []
        geometry = aperture.to_svg(
            ctx,
            stroke="black",
            for_layer=copper,
            include_metadata=False,
        )
        if kind in {"track", "arc"} or expansion == 0:
            return geometry
        else:
            return _offset_contours(
                ctx,
                geometry,
                expansion,
                mask_id,
            )

    @staticmethod
    def _rule_expansion(
        rules: Sequence[AltiumSolderMaskExpansionRule], kind: str, index: int, side: str
    ) -> int | None:
        # Use the saved board-wide rule and simple primitive-type scopes. Do not
        # guess past a higher-priority query that might match this primitive.
        for rule in rules:
            scope = rule.scope1_expression.strip().lower()
            if scope in {
                "istrack",
                "isarc",
                "isfill",
                "isregion",
                "ispad",
                "isvia",
                "ispolygon",
            }:
                if scope != "is" + kind:
                    continue
            elif scope != "all":
                log.warning(
                    "Soldermask film: cannot resolve rule %r scope %r for %s %s; aperture omitted",
                    rule.name,
                    rule.scope1_expression,
                    kind,
                    index,
                )
                return None
            if getattr(rule, f"is_tenting_{side}"):
                return None
            token = (
                rule.bottom_expansion
                if side == "bottom" and rule.use_separate_expansions
                else rule.top_expansion
            )
            expansion = parse_pcb_mils_token_as_internal(token)
            if expansion is None:
                log.warning("Soldermask film: invalid expansion in rule %r", rule.name)
            return expansion
        log.warning(
            "Soldermask film: no matching expansion rule for %s %s", kind, index
        )
        return None


def _offset_contours(
    ctx: PcbSvgRenderContext,
    geometry: list[str],
    expansion_iu: int,
    mask_id: str,
) -> list[str]:
    """Offset native filled paths/rectangles, retaining curves, holes and rotation.

    A centered stroke dilates a filled contour by half its width. For erosion,
    remove that boundary in a private mask so it cannot repaint another aperture.
    These strokes define apertures only; they never become visible board strokes.
    """
    width = ctx.fmt(abs(expansion_iu) * 2 * 0.0254 / 10000)
    elements: list[str] = []
    for index, svg in enumerate(geometry):
        contour = ET.fromstring(svg)
        contour.set("stroke", "black")
        contour.set("stroke-width", width)
        contour.set("stroke-linejoin", "round")
        if expansion_iu > 0:
            elements.append(ET.tostring(contour, encoding="unicode"))
            continue
        local_id = f"{mask_id}-{index}"
        contour.set("fill", "white")
        contour.set("paint-order", "fill stroke")
        # Put rotation on the group enclosing both the contour and its mask;
        # otherwise a rotated fill's mask would apply its transform twice.
        transform = contour.attrib.pop("transform", None)
        painted = ET.fromstring(svg)
        painted.attrib.pop("transform", None)
        painted.set("stroke", "none")
        painted.set("mask", f"url(#{local_id})")
        # Erosion cannot extend outside the source shape. Its own bounds also
        # avoid clipping rotated fills whose unrotated corners cross the canvas.
        mask = ET.Element(
            "mask",
            {
                "id": local_id,
                "maskUnits": "objectBoundingBox",
                "maskContentUnits": "userSpaceOnUse",
                "x": "0",
                "y": "0",
                "width": "1",
                "height": "1",
                "style": "mask-type:luminance",
                "color-interpolation": "sRGB",
            },
        )
        mask.append(contour)
        group = ET.Element("g", {"transform": transform} if transform else {})
        ET.SubElement(group, "defs").append(mask)
        group.append(painted)
        elements.append(ET.tostring(group, encoding="unicode"))
    return elements


def _film_color(
    pcbdoc: AltiumPcbDoc,
    side: Literal["top", "bottom"],
    surface: BoardSurfaceAppearance,
    style: Mapping[str, object],
) -> str:
    override = str(style.get("color", "auto")).strip()
    if override.casefold() != "auto":
        return override
    if surface.authored_color:
        return surface.authored_color
    if surface.kind is BoardSurfaceKind.COVERLAY:
        coverlay = str(style.get("coverlay_color", DEFAULT_COVERLAY_FILM_COLOR)).strip()
        return (
            coverlay if coverlay.casefold() != "auto" else DEFAULT_COVERLAY_FILM_COLOR
        )
    return saved_soldermask_color(pcbdoc, side) or DEFAULT_SOLDERMASK_FILM_COLOR


def _fallback_film_color(
    pcbdoc: AltiumPcbDoc,
    side: Literal["top", "bottom"],
    style: Mapping[str, object],
) -> str:
    override = str(style.get("color", "auto")).strip()
    if override.casefold() != "auto":
        return override
    return saved_soldermask_color(pcbdoc, side) or DEFAULT_SOLDERMASK_FILM_COLOR


def _relative_luminance(color: str) -> float | None:
    """Return CSS sRGB luminance for simple authored hex colors."""

    value = color.strip().casefold()
    value = {"black": "#000000", "white": "#ffffff"}.get(value, value)
    if not value.startswith("#") or len(value) not in {4, 5, 7, 9}:
        return None
    digits = value[1:]
    if len(digits) in {3, 4}:
        digits = "".join(channel * 2 for channel in digits)
    try:
        channels = tuple(int(digits[offset : offset + 2], 16) / 255 for offset in (0, 2, 4))
    except ValueError:
        return None
    linear = tuple(
        channel / 12.92
        if channel <= 0.04045
        else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    )
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrasting_silkscreen_color(
    pcbdoc: AltiumPcbDoc,
    side: Literal["top", "bottom"],
    film_style: Mapping[str, object],
    appearance_index: BoardSurfaceAppearanceIndex | None = None,
) -> str:
    """Choose one black/near-white ink with the best worst-case film contrast."""

    appearances = _valid_appearances(appearance_index)
    colors = tuple(
        _film_color(pcbdoc, side, appearance.surface(side), film_style)
        for appearance in appearances
        if appearance.surface(side).has_film
    )
    if not colors:
        colors = (_fallback_film_color(pcbdoc, side, film_style),)
    luminances = tuple(
        luminance
        for color in colors
        if (luminance := _relative_luminance(color)) is not None
    )
    if not luminances:
        return "#F5F5F5"
    black_min = min((luminance + 0.05) / 0.05 for luminance in luminances)
    white_min = min(1.05 / (luminance + 0.05) for luminance in luminances)
    return "#000000" if black_min >= white_min else "#F5F5F5"


def _region_path(
    ctx: PcbSvgRenderContext,
    appearance: BoardRegionAppearance,
) -> str:
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
