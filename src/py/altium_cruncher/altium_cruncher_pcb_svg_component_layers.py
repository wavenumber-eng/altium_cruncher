"""Composable component illustrations and autodoc-fitted assembly designators.

Caches belong to an immutable board snapshot in an SVG job, shared by selected
variants and views. Native processes are scoped to materialization, while their
geometry and SVG results survive until the job ends. Population filtering happens
after artwork preparation.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc
    from altium_monkey.altium_pcb_component import AltiumPcbComponent
    from altium_monkey.altium_pcb_svg_renderer import PcbSvgRenderContext
    from .altium_cruncher_pcb_svg_a0_renderer import PcbSvgA0Renderer
    from .pcb_svg_model_cache import PcbSvgModelCache
    from .pcb_svg_workers import PcbSvgNativeWorkers
import json
import logging
import math
import xml.etree.ElementTree as ET

import geometer as g

from .altium_cruncher_pcb_illustration import (
    IllustrationJob,
    ComponentPlacement,
    IllustrationSymbol,
    PlacedIllustrations,
    Side,
)
from .pcb_svg_component_cache import ComponentArtworkCache
from .altium_cruncher_pcb_designator_layout import (
    CcaComponentGeometryFact,
    CcaDesignatorFitSession,
    CcaDesignatorFit,
    fit_designator_to_geometry,
    normalize_designator_axis,
    _clear_designator_center,
)
from .altium_cruncher_pcb_designator_pads import component_designator_pads, pad_geometry
from .altium_cruncher_pcb_svg_cutout_layer import fit_cutout_label

COMPONENT_LAYER_IDS = {
    "ASSEMBLY_DESIGNATORS_TOP": 9008,
    "ASSEMBLY_DESIGNATORS_BOTTOM": 9009,
    "ILLUSTRATION_TOP": 9012,
    "ILLUSTRATION_BOTTOM": 9013,
}
SVG = "http://www.w3.org/2000/svg"
INKSCAPE = "http://www.inkscape.org/namespaces/inkscape"
ET.register_namespace("", SVG)
ET.register_namespace("inkscape", INKSCAPE)
log = logging.getLogger(__name__)


@dataclass(frozen=True)
class ComponentLayer:
    svg: str
    metadata: dict
    bounds_mm: tuple[float, float, float, float] | None = None


@dataclass(frozen=True)
class _DesignatorPaint:
    color: str
    opacity: float
    stroke_color: str
    stroke_width_mm: float


@dataclass(frozen=True)
class _DesignatorAnnotation:
    component_index: int
    designator: str
    geometry_source: str
    view_fit: CcaDesignatorFit


def _number(
    style: Mapping[str, object],
    name: str,
    default: float,
    *,
    minimum: float = 0,
    maximum: float = math.inf,
    positive: bool = False,
) -> float:
    value = style.get(name, default)
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value < minimum
        or value > maximum
        or (positive and value == 0)
    ):
        raise ValueError(f"Invalid component layer {name}: {value!r}")
    return float(value)


def _layer(token: str, role: str) -> ET.Element:
    layer_id = COMPONENT_LAYER_IDS[token]
    display_name = token.replace("_", " ").title()
    return ET.Element(
        f"{{{SVG}}}g",
        {
            "id": f"layer-{layer_id}",
            "data-layer-id": str(layer_id),
            "data-layer-key": token,
            "data-layer-name": token,
            "data-layer-display-name": display_name,
            "data-layer-role": role,
            f"{{{INKSCAPE}}}groupmode": "layer",
            f"{{{INKSCAPE}}}label": display_name,
            "aria-label": display_name,
        },
    )


def _component_attrs(
    ctx: PcbSvgRenderContext,
    index: int | None,
    designator: str,
    side: Side,
    feature: str,
    element_id: str,
) -> dict[str, str]:
    attrs = {
        "id": element_id,
        "data-feature": feature,
        "data-component-designator": designator,
        "data-designator": designator,
        "data-side": side,
        f"{{{INKSCAPE}}}label": designator,
        "aria-label": f"{designator} {feature.replace('-', ' ')}",
    }
    if ctx.options.include_metadata and index is not None:
        attrs.update({"data-component-index": str(index), "data-component": designator})
        uid = ctx.component_uid_by_index.get(index)
        if uid:
            attrs["data-component-uid"] = uid
    return attrs


class ComponentLayerSession:
    def __init__(
        self,
        excluded_designators: frozenset[str] = frozenset(),
        *,
        cache: PcbSvgModelCache | None = None,
        workers: PcbSvgNativeWorkers | None = None,
    ) -> None:
        self.excluded_designators = excluded_designators
        self.job = None
        self.cache = cache
        self.workers = workers
        self.fit_session = CcaDesignatorFitSession()
        self._parts = {}
        self._collected_sides = set()
        self._placed = {}
        self._layers = {}
        self._selected = {}
        self._records = []  # Retain identities used by the per-job keys.
        self.layer_hits = 0
        self.last_cache_status = "none"

    def _materialize(
        self,
        pcbdoc: AltiumPcbDoc,
        side: Side,
        line_width: float,
        illustrate: bool,
    ) -> PlacedIllustrations:
        identity = id(pcbdoc.components), id(pcbdoc.component_bodies)
        key = (*identity, side, line_width, illustrate)
        # A painted result also contains the outline used by designators.
        painted_key = (*identity, side, line_width, True)
        if painted_key in self._placed:
            return self._placed[painted_key]
        if key in self._placed:
            return self._placed[key]
        with g.GeometerClient() as client:
            if self.job is None:
                self.job = IllustrationJob(
                    client, line_width_mm=line_width, cache=self.cache
                )
            self.job.client = client
            self.job.line_width_mm = line_width
            parts_key = (*identity, side)
            artwork = None
            if self.cache is not None:
                # Meshless placements belong only to this exact width/mode.
                # Keep them out of the general, reusable geometry cache below.
                artwork = ComponentArtworkCache(
                    self.job, pcbdoc, side, illustrate, self.excluded_designators
                )
                # Other styles may need actual meshes again, but geometry
                # diagnostics retain the original once-per-side behavior.
                self.job._suppress_collection_warnings = (
                    parts_key in self._collected_sides
                )
                try:
                    parts = self.job.collect(
                        pcbdoc,
                        side=side,
                        excluded_designators=self.excluded_designators,
                        workers=self.workers,
                        cached_bodies=artwork.load(),
                        catalog_context=artwork.catalog_context,
                        capture_warnings=True,
                    )
                finally:
                    self.job._suppress_collection_warnings = False
                if parts_key not in self._collected_sides:
                    self._records.append((pcbdoc.components, pcbdoc.component_bodies))
                    self._collected_sides.add(parts_key)
            elif parts_key not in self._parts:
                self._records.append((pcbdoc.components, pcbdoc.component_bodies))
                log.info("Preparing %s component geometry", side)
                self._parts[parts_key] = self.job.collect(
                    pcbdoc,
                    side=side,
                    excluded_designators=self.excluded_designators,
                    workers=self.workers,
                )
            if artwork is None:
                parts = self._parts[parts_key]
            log.info(
                "Rendering %s component illustrations: %d components", side, len(parts)
            )
            placed = self.job.render_many(
                parts, side=side, illustrate=illustrate, workers=self.workers
            )
            if artwork is not None:
                artwork.store(placed)
            log.info(
                "Completed %s component illustrations: %d/%d", side, len(placed), len(parts)
            )
            log.debug(
                "Completed %s components: %d/%d (%d new, %d disk-cached illustrations in job)",
                side,
                len(placed),
                len(parts),
                self.job.counts["illustrations"],
                self.job.counts["illustration_disk_hits"],
            )
        placed.sort(
            key=lambda item: (
                -item[0].bounds[2] if side == "bottom" else item[0].bounds[5]
            )
        )
        self._placed[key] = placed
        return placed

    def render(
        self,
        renderer: PcbSvgA0Renderer,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        token: str,
        tokens: Sequence[str],
        styles: dict[str, dict[str, object]],
    ) -> ComponentLayer:
        source = renderer.render_job.geometry_source(pcbdoc)
        side = "bottom" if token.endswith("BOTTOM") else "top"
        illustrated = token.startswith("ILLUSTRATION_")
        style = styles.get(
            "illustration" if illustrated else "assembly_designators", {}
        )
        width = _number(
            styles.get("illustration", {}), "line_width_mm", 0.025, positive=True
        )
        if not style.get("enabled", True):
            self.last_cache_status = "disabled"
            return ComponentLayer("", {})
        obstacles = (
            cutout_label_obstacles(ctx, pcbdoc, styles)
            if "BOARD_CUTOUTS" in tokens
            else ()
        )
        key = (
            id(source.components),
            id(source.component_bodies),
            token,
            ctx.min_x_mils,
            ctx.max_y_mils,
            ctx.width_mm,
            ctx.height_mm,
            ctx.options.mirror_x,
            ctx.options.include_metadata,
            width,
            json.dumps(style, sort_keys=True),
            obstacles,
            json.dumps(
                {k: v.to_dict() for k, v in renderer.config.components.items()},
                sort_keys=True,
            ),
            renderer.config.assembly.designator_color,
        )
        if key in self._layers:
            self.layer_hits += 1
            self.last_cache_status = "hit"
        else:
            painted = f"ILLUSTRATION_{side.upper()}" in tokens and styles.get(
                "illustration", {}
            ).get("enabled", True)
            placed = self._materialize(source, side, width, illustrated or painted)
            if illustrated:
                result = self._illustrations(ctx, placed, token, side, style)
            else:
                result = self._designators(
                    renderer, ctx, pcbdoc, placed, token, side, style, obstacles
                )
            self._layers[key] = result
            self.last_cache_status = "built"
        return self._population_layer(key, renderer.excluded_designators, ctx)

    def _population_layer(
        self,
        key: tuple,
        excluded: frozenset[str],
        ctx: PcbSvgRenderContext,
    ) -> ComponentLayer:
        selected_key = key, excluded
        if not excluded:
            return self._layers[key]
        if selected_key not in self._selected:
            self._selected[selected_key] = _select_population(
                self._layers[key], excluded, ctx
            )
            if self.last_cache_status == "hit":
                self.last_cache_status = "assembled"
        return self._selected[selected_key]

    def _illustrations(
        self,
        ctx: PcbSvgRenderContext,
        placed: PlacedIllustrations,
        token: str,
        side: Side,
        style: Mapping[str, object],
    ) -> ComponentLayer:
        opacity = _number(style, "opacity", 1, maximum=1)
        layer = _layer(token, "illustration")
        layer.set("opacity", f"{opacity:g}")
        definitions = ET.SubElement(layer, f"{{{SVG}}}defs")
        ids = {}
        entries = []
        bounds = []
        for ordinal, (part, symbol) in enumerate(placed):
            symbol_id = ids.get(id(symbol))
            if symbol_id is None:
                symbol_id = f"{token.lower()}-symbol-{len(ids)}"
                ids[id(symbol)] = symbol_id
                definitions.append(symbol.group(symbol_id))
            x = ctx.x_to_svg(part.anchor_mm[0] / 0.0254)
            y = ctx.y_to_svg(part.anchor_mm[1] / 0.0254)
            identity = (
                part.component_index
                if part.component_index is not None
                else f"free-{part.bodies[0]['index']}"
            )
            group_id = f"{token.lower()}-component-{identity}"
            attrs = _component_attrs(
                ctx,
                part.component_index,
                part.designator,
                side,
                "component-illustration",
                group_id,
            )
            if ctx.options.include_metadata:
                attrs["data-body-indices"] = ",".join(
                    str(body["index"]) for body in part.bodies
                )
                attrs["data-geometry-source"] = ",".join(
                    sorted({body["kind"] for body in part.bodies})
                )
            group = ET.SubElement(layer, f"{{{SVG}}}g", attrs)
            ET.SubElement(
                group,
                f"{{{SVG}}}use",
                {
                    "href": "#" + symbol_id,
                    "transform": f"translate({x:.12g} {y:.12g})",
                },
            )
            low_x, low_y, low_z, high_x, high_y, high_z = part.bounds
            left, right = x + low_x - 0.1, x + high_x + 0.1
            if ctx.options.mirror_x:
                left, right = ctx.width_mm - right, ctx.width_mm - left
            bounds.append((left, y - high_y - 0.1, right, y - low_y + 0.1))
            entries.append(
                dict(
                    group_id=group_id,
                    component_index=part.component_index,
                    designator=part.designator,
                    side=side,
                    symbol_id=symbol_id,
                    anchor_svg_mm=[x, y],
                    anchor_board_mm=part.anchor_mm,
                    bounds_local_xyz_mm=part.bounds,
                    bodies=part.bodies,
                    paint_order=ordinal,
                )
            )
        combined = (
            (
                min(b[0] for b in bounds),
                min(b[1] for b in bounds),
                max(b[2] for b in bounds),
                max(b[3] for b in bounds),
            )
            if bounds
            else None
        )
        return ComponentLayer(
            ET.tostring(layer, encoding="unicode"),
            dict(
                token=token,
                group_id=layer.get("id"),
                side=side,
                instances=entries,
                unique_symbols=len(ids),
            ),
            combined,
        )

    def _designators(
        self,
        renderer: PcbSvgA0Renderer,
        ctx: PcbSvgRenderContext,
        pcbdoc: AltiumPcbDoc,
        placed: PlacedIllustrations,
        token: str,
        side: Side,
        style: Mapping[str, object],
        obstacles: Sequence[tuple[float, float, float, float]],
    ) -> ComponentLayer:
        fill = _number(style, "fill_ratio", 0.8, maximum=1, positive=True)
        maximum = _number(style, "max_font_size_mm", 2.5, positive=True)
        opacity = _number(style, "opacity", 1, maximum=1)
        color = str(style.get("color") or renderer.config.assembly.designator_color)
        stroke_width = _number(style, "stroke_width_mm", 0)
        stroke_color = str(style.get("stroke_color") or "#FFFFFF")
        paint = _DesignatorPaint(color, opacity, stroke_color, stroke_width)
        layer = _layer(token, "annotation")
        entries = []
        models = {
            part.component_index: (part, symbol)
            for part, symbol in placed
            if part.component_index is not None
        }
        authored_models = {body.component_index for body in pcbdoc.component_bodies}
        for index, component in enumerate(pcbdoc.components):
            designator = self._visible_designator(
                renderer, component, index in models, side
            )
            if designator is None:
                continue
            selected = self._designator_geometry(
                pcbdoc, index, designator, side, models, authored_models
            )
            if selected is None:
                continue
            geometry, source = selected
            fit = fit_designator_to_geometry(
                designator,
                geometry,
                fill_ratio=fill,
                maximum_font_size_mm=maximum,
                auto_base_rotation_degrees=-float(component.rotation or 0),
                session=self.fit_session,
            )
            if fit is None:
                continue
            center, rotation = _designator_view_position(
                ctx, designator, geometry, fit, obstacles
            )
            annotation = _DesignatorAnnotation(
                component_index=index,
                designator=designator,
                geometry_source=source,
                view_fit=replace(fit, center_mm=center, rotation_degrees=rotation),
            )
            entries.append(
                _append_designator(layer, ctx, token, side, annotation, paint)
            )
        return ComponentLayer(
            ET.tostring(layer, encoding="unicode"),
            dict(token=token, group_id=layer.get("id"), side=side, instances=entries),
        )

    def _visible_designator(
        self,
        renderer: PcbSvgA0Renderer,
        component: AltiumPcbComponent,
        has_model: bool,
        side: Side,
    ) -> str | None:
        from .altium_cruncher_pcb_svg_a0_renderer import _component_side

        # Altium can author a body's projection on the opposite side of
        # its owner (RT's test points do this). Label the visible model.
        if not has_model and _component_side(component) != side:
            return None
        designator = str(component.designator or "")
        override = renderer.config.components.get(designator)
        if (
            not designator
            or designator in self.excluded_designators
            or (override and override.show_designator is False)
        ):
            return None
        return designator

    def _designator_geometry(
        self,
        pcbdoc: AltiumPcbDoc,
        index: int,
        designator: str,
        side: Side,
        models: dict[int, tuple[ComponentPlacement, IllustrationSymbol]],
        authored_models: set[int | None],
    ) -> tuple[CcaComponentGeometryFact, str] | None:
        if index in models:
            part, symbol = models[index]
            segments = tuple(
                tuple(
                    (x + part.anchor_mm[0], y - part.anchor_mm[1]) for x, y in segment
                )
                for segment in symbol.outline_segments_mm
            )
            if not segments:
                self.job.warnings.append(
                    f"{designator}: no model outline for designator; omitted"
                )
                return None
            xs, ys = zip(*(point for segment in segments for point in segment))
            geometry = CcaComponentGeometryFact(
                (min(xs), min(ys), max(xs), max(ys)), segments
            )
            source = "model"
        elif index not in authored_models:
            pads = component_designator_pads(pcbdoc.pads, index, side)
            geometry = pad_geometry(pads, side)
            source = "pads"
            if geometry is None:
                return None
        else:
            # Missing or unsupported attached models must not silently turn
            # into invented pad-based component geometry.
            return None
        return geometry, source


def _designator_view_position(
    ctx: PcbSvgRenderContext,
    designator: str,
    geometry: CcaComponentGeometryFact,
    fit: CcaDesignatorFit,
    obstacles: Sequence[tuple[float, float, float, float]],
) -> tuple[tuple[float, float], float]:
    # Fit in source Y-down coordinates, then apply autodoc's reflected
    # center/angle and cutout-clearance rules in displayed coordinates.
    origin_x, origin_y = ctx.min_x_mils * 0.0254, -ctx.max_y_mils * 0.0254

    def view_x(x: float) -> float:
        x -= origin_x
        return ctx.width_mm - x if ctx.options.mirror_x else x

    rotation = normalize_designator_axis(
        180 - fit.rotation_degrees if ctx.options.mirror_x else fit.rotation_degrees
    )
    left, top, right, bottom = geometry.bounds_mm
    center = _clear_designator_center(
        designator,
        center=(view_x(fit.center_mm[0]), fit.center_mm[1] - origin_y),
        font_size=fit.font_size_mm,
        rotation=rotation,
        component_bounds=(
            min(view_x(left), view_x(right)),
            top - origin_y,
            max(view_x(left), view_x(right)),
            bottom - origin_y,
        ),
        obstacles=obstacles,
    )
    return center, rotation


def _append_designator(
    layer: ET.Element,
    ctx: PcbSvgRenderContext,
    token: str,
    side: Side,
    annotation: _DesignatorAnnotation,
    paint: _DesignatorPaint,
) -> dict[str, object]:
    index, designator, source = (
        annotation.component_index,
        annotation.designator,
        annotation.geometry_source,
    )
    center, rotation = (
        annotation.view_fit.center_mm,
        annotation.view_fit.rotation_degrees,
    )
    font_size_mm = annotation.view_fit.font_size_mm
    color, opacity = paint.color, paint.opacity
    stroke_color, stroke_width = paint.stroke_color, paint.stroke_width_mm
    x, y = center
    group_id = f"{token.lower()}-component-{index}"
    attrs = _component_attrs(
        ctx, index, designator, side, "assembly-designator", group_id
    )
    attrs["data-geometry-source"] = source
    group = ET.SubElement(layer, f"{{{SVG}}}g", attrs)
    # Counter the outer scene reflection; text coordinates above already
    # describe the displayed view. This keeps arbitrary angles readable.
    if ctx.options.mirror_x:
        group.set("transform", f"translate({ctx.width_mm:.12g} 0) scale(-1 1)")
    text = ET.SubElement(
        group,
        f"{{{SVG}}}text",
        {
            "x": f"{x:.12g}",
            "y": f"{y:.12g}",
            "transform": f"rotate({rotation:.12g} {x:.12g} {y:.12g})",
            "text-anchor": "middle",
            "dominant-baseline": "central",
            "font-size": f"{font_size_mm:.12g}",
            "font-family": "sans-serif",
            "font-weight": "700",
            "fill": color,
            "opacity": f"{opacity:g}",
            "stroke": "none",
        },
    )
    text.text = designator
    if stroke_width > 0:
        text.attrib.update(
            {
                "stroke": stroke_color,
                "stroke-width": f"{stroke_width:g}",
                "stroke-linejoin": "round",
                "paint-order": "stroke fill",
            }
        )
    return dict(
        group_id=group_id,
        component_index=index,
        designator=designator,
        geometry_source=source,
        center_view_mm=center,
        font_size_mm=font_size_mm,
        rotation_degrees=rotation,
    )


def _select_population(
    source: ComponentLayer,
    excluded: frozenset[str],
    ctx: PcbSvgRenderContext,
) -> ComponentLayer:
    """Compose a population from cached artwork; prune unused symbols and metadata."""
    removed = {
        e["group_id"]
        for e in source.metadata.get("instances", ())
        if e["component_index"] is not None and e["designator"] in excluded
    }
    entries = [
        dict(e)
        for e in source.metadata.get("instances", ())
        if e["group_id"] not in removed
    ]
    if len(entries) == len(source.metadata.get("instances", ())):
        return source
    root = ET.fromstring(source.svg)
    for child in list(root):
        if child.get("id") in removed:
            root.remove(child)
    metadata = {**source.metadata, "instances": entries}
    bounds = []
    definitions = root.find(f"{{{SVG}}}defs")
    if definitions is not None:
        bounds = _prune_population_symbols(root, definitions, entries, metadata, ctx)
    combined = (
        (
            min(b[0] for b in bounds),
            min(b[1] for b in bounds),
            max(b[2] for b in bounds),
            max(b[3] for b in bounds),
        )
        if bounds
        else None
    )
    return ComponentLayer(ET.tostring(root, encoding="unicode"), metadata, combined)


def _prune_population_symbols(
    root: ET.Element,
    definitions: ET.Element,
    entries: list[dict],
    metadata: dict,
    ctx: PcbSvgRenderContext,
) -> list[tuple[float, float, float, float]]:
    bounds = []
    original = {node.get("id"): node for node in definitions}
    ids = {}
    for ordinal, entry in enumerate(entries):
        old = entry["symbol_id"]
        if old not in ids:
            ids[old] = f"{metadata['token'].lower()}-symbol-{len(ids)}"
        entry.update(symbol_id=ids[old], paint_order=ordinal)
        x, y = entry["anchor_svg_mm"]
        low_x, low_y, _, high_x, high_y, _ = entry["bounds_local_xyz_mm"]
        left, right = x + low_x - 0.1, x + high_x + 0.1
        if ctx.options.mirror_x:
            left, right = ctx.width_mm - right, ctx.width_mm - left
        bounds.append((left, y - high_y - 0.1, right, y - low_y + 0.1))
    definitions.clear()
    for old, new in ids.items():
        node = original[old]
        node.set("id", new)
        definitions.append(node)
    for use in root.iter(f"{{{SVG}}}use"):
        use.set("href", "#" + ids[use.get("href")[1:]])
    metadata["unique_symbols"] = len(ids)
    return bounds


def cutout_label_obstacles(
    ctx: PcbSvgRenderContext,
    pcbdoc: AltiumPcbDoc,
    styles: Mapping[str, dict[str, object]],
) -> tuple[tuple[float, float, float, float], ...]:
    from .altium_cruncher_mate_graphics import (
        _board_outline_vertex,
        _linearized_outline_points,
    )

    style = styles.get("board_cutouts", {})
    label = str(style.get("label", "")).strip()
    if not label or not style.get("enabled", True):
        return ()
    result = []
    outline = getattr(getattr(pcbdoc, "board", None), "outline", None)
    for contour in getattr(outline, "cutouts", ()):
        points = [
            (ctx.x_to_svg(x), ctx.y_to_svg(y))
            for x, y in _linearized_outline_points(
                {"vertices": [_board_outline_vertex(v) for v in contour]}
            )
        ]
        fit = fit_cutout_label(points, label, style)
        if fit is None:
            continue
        x, y = fit.center_mm
        w, h = max(1, len(label) * 0.62) * fit.font_size_mm, fit.font_size_mm
        if fit.rotation_degrees:
            w, h = h, w
        if ctx.options.mirror_x:
            x = ctx.width_mm - x
        result.append((x - w / 2, y - h / 2, x + w / 2, y + h / 2))
    return tuple(result)
