"""Composable component illustrations and autodoc-fitted assembly designators.

Caches belong to an immutable board snapshot in an SVG job, shared by selected
variants and views. Native processes are scoped to materialization, while their
geometry and SVG results survive until the job ends. Population filtering happens
after artwork preparation.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc
    from altium_monkey.altium_pcb_component import AltiumPcbComponent
    from altium_monkey.altium_pcb_svg_renderer import PcbSvgRenderContext
    from .altium_cruncher_pcb_svg_a0_renderer import PcbSvgA0Renderer
    from .pcb_svg_model_cache import PcbSvgModelCache
    from .pcb_svg_workers import PcbSvgNativeWorkers
    from .pcb_board_region_envelope_index import BoardRegionEnvelopeIndex
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
from .altium_cruncher_pcb_svg_substrate import (
    BoardMaterialDomain,
    BoardSubstrateRenderer,
)

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
        diagnostic_sink: Callable[..., object] | None = None,
    ) -> None:
        self.excluded_designators = excluded_designators
        self.job = None
        self.cache = cache
        self.workers = workers
        self.diagnostic_sink = diagnostic_sink
        self._reported_diagnostic_count = 0
        self._diagnosed_missing_populations: set[tuple[int, frozenset[str]]] = set()
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
        region_index: BoardRegionEnvelopeIndex | None = None,
    ) -> PlacedIllustrations:
        identity = id(pcbdoc.components), id(pcbdoc.component_bodies)
        key = (*identity, side, line_width, illustrate)
        # A painted result also contains the outline used by designators.
        painted_key = (*identity, side, line_width, True)
        if painted_key in self._placed:
            return self._placed[painted_key]
        if key in self._placed:
            return self._placed[key]
        parts: list[ComponentPlacement]
        with g.GeometerClient() as client:
            if self.job is None:
                self.job = IllustrationJob(
                    client,
                    line_width_mm=line_width,
                    cache=self.cache,
                    emit_warnings=self.diagnostic_sink is None,
                    region_index=region_index,
                )
            self.job.client = client
            self.job.line_width_mm = line_width
            self.job.region_index = region_index
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
                "Completed %s component illustrations: %d/%d",
                side,
                len(placed),
                len(parts),
            )
            log.debug(
                "Completed %s components: %d/%d (%d new, %d disk-cached illustrations in job)",
                side,
                len(placed),
                len(parts),
                self.job.counts["illustrations"],
                self.job.counts["illustration_disk_hits"],
            )
            self._flush_diagnostics()
        placed.sort(
            key=lambda item: (
                -item[0].bounds[2] if side == "bottom" else item[0].bounds[5]
            )
        )
        self._placed[key] = placed
        return placed

    def _flush_diagnostics(self) -> None:
        if self.diagnostic_sink is None or self.job is None:
            return
        for diagnostic in self.job.diagnostics[self._reported_diagnostic_count :]:
            self.diagnostic_sink(
                code=diagnostic.code,
                category=diagnostic.category,
                producer=diagnostic.producer,
                message=diagnostic.message,
                component_designator=diagnostic.component_designator,
                body_index=diagnostic.body_index,
                model_identity=diagnostic.model_identity,
                detail=diagnostic.detail,
                occurrence_key=(
                    f"component:{diagnostic.component_designator or ''}:"
                    f"body:{diagnostic.body_index}:model:{diagnostic.model_identity or ''}:"
                    f"code:{diagnostic.code}"
                ),
                source_scoped=True,
            )
        self._reported_diagnostic_count = len(self.job.diagnostics)

    def _diagnose_missing_models(
        self,
        pcbdoc: AltiumPcbDoc,
        excluded_designators: frozenset[str],
    ) -> None:
        if self.diagnostic_sink is None:
            return
        population_key = id(pcbdoc.components), excluded_designators
        if population_key in self._diagnosed_missing_populations:
            return
        self._diagnosed_missing_populations.add(population_key)
        owners = {
            body.component_index
            for body in pcbdoc.component_bodies
            if body.component_index is not None
        }
        for index, component in enumerate(pcbdoc.components):
            designator = str(component.designator or "")
            if not designator or designator in excluded_designators or index in owners:
                continue
            self.diagnostic_sink(
                code="missing-renderable-model",
                category="missing_model",
                producer="altium-cruncher",
                message=f"{designator}: fitted component has no renderable 3D model",
                component_designator=designator,
                occurrence_key=f"component:{index}:{designator}:missing-renderable-model",
                source_scoped=True,
            )

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
        if illustrated:
            self._diagnose_missing_models(pcbdoc, renderer.excluded_designators)
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
            painted = bool(
                f"ILLUSTRATION_{side.upper()}" in tokens
                and styles.get("illustration", {}).get("enabled", True)
            )
            placed = self._materialize(
                source,
                side,
                width,
                illustrated or painted,
                renderer.render_job.board_region_envelopes(source),
            )
            if illustrated:
                occlusion_domain = BoardSubstrateRenderer(
                    renderer.options
                ).occlusion_domain(ctx, source, side)
                result = self._illustrations(
                    ctx, placed, token, side, style, occlusion_domain
                )
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
        occlusion_domain: BoardMaterialDomain,
    ) -> ComponentLayer:
        opacity = _number(style, "opacity", 1, maximum=1)
        layer = _layer(token, "illustration")
        layer.set("opacity", f"{opacity:g}")
        definitions = ET.SubElement(layer, f"{{{SVG}}}defs")
        ids = {}
        aperture_ids = {}
        entries = []
        bounds = []
        mask_extent = _illustration_mask_extent(ctx, placed)
        board_mask_id = f"{token.lower()}-board-occlusion"
        aperture_mask_id = f"{token.lower()}-open-space"
        if any(symbol.aperture is not None for _part, symbol in placed):
            definitions.append(
                occlusion_domain.mask_element(ctx, board_mask_id, extent=mask_extent)
            )
            definitions.append(
                occlusion_domain.mask_element(
                    ctx, aperture_mask_id, extent=mask_extent, complement=True
                )
            )
        for ordinal, (part, symbol) in enumerate(placed):
            symbol_id = _surface_symbol_definition(
                definitions, ids, aperture_ids, token, symbol
            )
            aperture_symbol_id = _aperture_symbol_definition(
                definitions, ids, aperture_ids, token, symbol
            )
            entry, instance_bounds = _append_illustration_instance(
                ctx,
                layer,
                part,
                symbol_id,
                aperture_symbol_id,
                token,
                side,
                board_mask_id,
                aperture_mask_id,
                ordinal,
            )
            entries.append(entry)
            bounds.append(instance_bounds)
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
                unique_symbols=len(ids) + len(aperture_ids),
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
                job = self.job
                if job is None:
                    raise RuntimeError("component geometry was not materialized")
                job.warn(
                    f"{designator}: no model outline for designator; omitted",
                    code="missing-model-outline",
                    category="geometer_geometry",
                    component_designator=designator,
                )
                self._flush_diagnostics()
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


def _illustration_mask_extent(
    ctx: PcbSvgRenderContext,
    placed: PlacedIllustrations,
) -> tuple[float, float, float, float]:
    """Cover the board canvas and every projected component overhang."""

    left, top, right, bottom = 0.0, 0.0, ctx.width_mm, ctx.height_mm
    for part, symbol in placed:
        source_bounds = symbol.aperture_source_bounds_mm or symbol.source_bounds_mm
        low_x, low_y, _, high_x, high_y, _ = source_bounds or part.bounds
        x = ctx.x_to_svg(part.anchor_mm[0] / 0.0254)
        y = ctx.y_to_svg(part.anchor_mm[1] / 0.0254)
        left = min(left, x + low_x)
        top = min(top, y - high_y)
        right = max(right, x + high_x)
        bottom = max(bottom, y - low_y)
    padding = 0.1
    left -= padding
    top -= padding
    return left, top, right - left + padding, bottom - top + padding


def _surface_symbol_definition(
    definitions: ET.Element,
    ids: dict[int, str],
    aperture_ids: Mapping[int, str],
    token: str,
    symbol: IllustrationSymbol,
) -> str | None:
    del aperture_ids  # Keep both symbol registries explicit at the call site.
    if not symbol.svg:
        return None
    symbol_id = ids.get(id(symbol))
    if symbol_id is None:
        symbol_id = f"{token.lower()}-symbol-{len(ids)}"
        ids[id(symbol)] = symbol_id
        definitions.append(symbol.group(symbol_id))
    return symbol_id


def _aperture_symbol_definition(
    definitions: ET.Element,
    ids: Mapping[int, str],
    aperture_ids: dict[int, str],
    token: str,
    symbol: IllustrationSymbol,
) -> str | None:
    del ids  # Keep both symbol registries explicit at the call site.
    if symbol.aperture is None:
        return None
    key = id(symbol.aperture)
    symbol_id = aperture_ids.get(key)
    if symbol_id is None:
        symbol_id = f"{token.lower()}-aperture-symbol-{len(aperture_ids)}"
        aperture_ids[key] = symbol_id
        definitions.append(symbol.aperture_group(symbol_id))
    return symbol_id


def _append_illustration_instance(
    ctx: PcbSvgRenderContext,
    layer: ET.Element,
    part: ComponentPlacement,
    symbol_id: str | None,
    aperture_symbol_id: str | None,
    token: str,
    side: Side,
    board_mask_id: str,
    aperture_mask_id: str,
    ordinal: int,
) -> tuple[dict[str, object], tuple[float, float, float, float]]:
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
    transform = f"translate({x:.12g} {y:.12g})"
    if aperture_symbol_id is not None:
        ET.SubElement(
            group,
            f"{{{SVG}}}use",
            {
                "href": "#" + aperture_symbol_id,
                "transform": transform,
                "mask": f"url(#{aperture_mask_id})",
                "data-visibility-domain": "aperture",
            },
        )
    if symbol_id is not None:
        ET.SubElement(
            group,
            f"{{{SVG}}}use",
            {
                "href": "#" + symbol_id,
                "transform": transform,
                "mask": f"url(#{board_mask_id})" if aperture_symbol_id else "none",
                "data-visibility-domain": "board-surface",
            },
        )
    low_x, low_y, _, high_x, high_y, _ = part.bounds
    left, right = x + low_x - 0.1, x + high_x + 0.1
    if ctx.options.mirror_x:
        left, right = ctx.width_mm - right, ctx.width_mm - left
    bounds = left, y - high_y - 0.1, right, y - low_y + 0.1
    entry = dict(
        group_id=group_id,
        component_index=part.component_index,
        designator=part.designator,
        side=side,
        symbol_id=symbol_id,
        aperture_symbol_id=aperture_symbol_id,
        anchor_svg_mm=[x, y],
        anchor_board_mm=part.anchor_mm,
        bounds_local_xyz_mm=part.bounds,
        bodies=part.bodies,
        paint_order=ordinal,
    )
    return entry, bounds


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
    original = {
        node.get("id"): node
        for node in definitions
        if node.tag == f"{{{SVG}}}g" and node.get("id")
    }
    fixed_definitions = [node for node in definitions if node.tag != f"{{{SVG}}}g"]
    used = _used_population_symbols(root, entries)
    ids, bounds = _renumber_population_entries(entries, metadata, ctx)
    for old in used:
        ids.setdefault(old, f"{metadata['token'].lower()}-symbol-{len(ids)}")
    _replace_population_definitions(root, definitions, fixed_definitions, original, ids)
    metadata["unique_symbols"] = len(ids)
    return bounds


def _used_population_symbols(
    root: ET.Element, entries: Sequence[Mapping[str, object]]
) -> list[str]:
    groups = {child.get("id"): child for child in root if child.get("id")}
    used: list[str] = []
    for entry in entries:
        group = groups.get(cast(str, entry["group_id"]))
        if group is None:
            continue
        for use in group.iter(f"{{{SVG}}}use"):
            href = use.get("href", "")
            if href.startswith("#") and href[1:] not in used:
                used.append(href[1:])
    return used


def _renumber_population_entries(
    entries: list[dict], metadata: Mapping[str, object], ctx: PcbSvgRenderContext
) -> tuple[dict[str, str], list[tuple[float, float, float, float]]]:
    ids: dict[str, str] = {}
    bounds: list[tuple[float, float, float, float]] = []
    for ordinal, entry in enumerate(entries):
        old = entry.get("symbol_id")
        if old is not None and old not in ids:
            ids[old] = f"{metadata['token'].lower()}-symbol-{len(ids)}"
        entry.update(
            symbol_id=ids.get(old) if old is not None else None,
            paint_order=ordinal,
        )
        x, y = entry["anchor_svg_mm"]
        low_x, low_y, _, high_x, high_y, _ = entry["bounds_local_xyz_mm"]
        left, right = x + low_x - 0.1, x + high_x + 0.1
        if ctx.options.mirror_x:
            left, right = ctx.width_mm - right, ctx.width_mm - left
        bounds.append((left, y - high_y - 0.1, right, y - low_y + 0.1))
    return ids, bounds


def _replace_population_definitions(
    root: ET.Element,
    definitions: ET.Element,
    fixed_definitions: Sequence[ET.Element],
    original: Mapping[str | None, ET.Element],
    ids: Mapping[str, str],
) -> None:
    definitions.clear()
    definitions.extend(fixed_definitions)
    for old, new in ids.items():
        node = original[old]
        node.set("id", new)
        definitions.append(node)
    for use in root.iter(f"{{{SVG}}}use"):
        old = use.get("href", "")[1:]
        if old in ids:
            use.set("href", "#" + ids[old])


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
