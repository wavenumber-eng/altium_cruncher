"""Experimental top/bottom component illustrations, in board millimeters.

The job owns native calls and caches. Each component's authored bodies remain
separate meshes in one native illustration. Repeated component poses reuse SVGs;
Geometer combines matching painted surfaces as in its demos.
Invisible geometry is removed before both illustration and HLR.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields, replace
import logging
import math
from typing import TYPE_CHECKING, Literal, TypedDict, cast
from collections.abc import Sequence
from concurrent.futures import Future

from altium_monkey.altium_pcbdoc import AltiumPcbDoc
from altium_monkey.altium_pcb_component import AltiumPcbComponent
from altium_monkey.altium_record_pcb__component_body import AltiumPcbComponentBody
import geometer as g

from .altium_cruncher_pcb_assembly_model_helper import PcbAssemblyModelHelper
from .pcb_illustration_diagnostics import (
    DiagnosticMetadata as _DiagnosticMetadata,
    IllustrationDiagnosticsMixin,
    WarningEvents,
    body_failure_classification as _body_failure_classification,
    body_model_label as _body_model_label,
    geometer_failure_message as _geometer_failure_message,
    report_step_completions as _report_step_completions,
    unavailable_step_reason as _unavailable_step_reason,
)
from .pcb_illustration_model_geometry import (
    Bounds3,
    IllustrationProjection,
    IllustrationSymbol,
    Meshes,
    ModelGeometryError,
    colorref as _colorref,
    column_major as _column_major,
    component_rotation_degrees as _component_rotation_degrees,
    decode_cached_symbol as _decode_cached_symbol,
    decode_cached_tessellation as _decode_cached_tessellation,
    digest as _digest,
    empty_illustration_symbol as _empty_illustration_symbol,
    extrusion_extents_mm as extrusion_extents_mm,
    fast_hlr_options as _fast_hlr_options,
    illustration_style as _illustration_style,
    model_tessellation as _model_tessellation,
    rotation_z as _rotation_z,
    symbol_from_geometry as _symbol_from_geometry,
    tessellation_disk_key as _tessellation_disk_key,
    transform_mesh as _transform_mesh,
    translation as _translation,
)
from .pcb_illustration_source_geometry import (
    body_outline_bounds_local_mm as _body_outline_bounds_local_mm,
    cylinder_mesh as _cylinder_mesh,
    extrusion_request as _extrusion_request,
    illustration_ring as _illustration_ring,
    mesh_bounds as _mesh_bounds,
    placed_meshes as _placed_meshes,
    step_matrix as _step_matrix,
)
from .pcb_model_rotation import resolve_model_z_rotation
from .pcb_board_region_envelope_index import (
    BoardRegionEnvelopeIndex,
    BoardRegionQueryStatus,
)
from .pcb_component_clipping import (
    COMPONENT_CLIP_CAP_POLICY,
    COMPONENT_CLIP_TOLERANCE_MM,
    ComponentVisibilityAction,
    ComponentVisibilityResolution,
    clipped_conservative_bounds as _clipped_conservative_bounds,
    native_clipping as _native_clipping,
    resolve_component_visibility,
)

if TYPE_CHECKING:
    from .pcb_svg_model_cache import PcbSvgModelCache
    from .pcb_svg_workers import PcbSvgNativeWorkers

log = logging.getLogger(__name__)

_IU_MM = 0.00000254
_MIL_MM = 0.0254
_COORDINATE_SPAN = 1_000_000


type Side = Literal["top", "bottom"]
type Vector2 = tuple[float, float]
type ModelCatalog = dict[str, list[dict[str, object]]]
type CatalogContext = tuple[PcbAssemblyModelHelper, ModelCatalog, ModelCatalog]
type ComponentPlacement = IllustrationComponent | CachedComponentPlacement
type PlacedIllustrations = list[tuple[ComponentPlacement, IllustrationSymbol]]
type CachedBodies = dict[int, tuple[CachedComponentPlacement | None, WarningEvents]]
type RenderKeys = tuple[str, str]
type PreparedIllustration = IllustrationSymbol | Future[IllustrationSymbol]


class BodyMetadata(TypedDict):
    index: int
    kind: str
    lower_z_mm: float
    upper_z_mm: float
    color: tuple[float, float, float] | None
    opacity: float


@dataclass(frozen=True)
class CachedComponentPlacement:
    """Complete positive artwork placement; no mesh arrays are needed on a hit."""

    designator: str
    anchor_mm: Vector2
    bodies: tuple[BodyMetadata, ...]
    component_index: int | None
    bounds: Bounds3
    authored_side: Side = "top"
    board_z_offset_mm: float = 0.0
    illustration_label: str | None = None


@dataclass(frozen=True)
class DirectIllustrationSource:
    """Compact model input retained until Geometer performs one-pass illustration."""

    source: g.ModelIllustrationSourceA0
    model: bytes | None
    identity: object
    label: str
    footprint_local_source: g.ModelIllustrationSourceA0 | None = None
    authored_outline_bounds_mm: tuple[float, float, float, float] | None = None


@dataclass(frozen=True)
class IllustrationComponent:
    designator: str
    anchor_mm: tuple[float, float]
    meshes: tuple[g.MeshIllustrationMesh, ...]
    bodies: tuple[BodyMetadata, ...]
    component_index: int | None = None
    direct: DirectIllustrationSource | None = None
    resolved_bounds: Bounds3 | None = None
    authored_side: Side = "top"
    board_z_offset_mm: float = 0.0

    @property
    def bounds(self) -> tuple[float, float, float, float, float, float]:
        if self.resolved_bounds is not None:
            return self.resolved_bounds
        if not self.meshes:
            raise ValueError("Direct illustration bounds are available after rendering")
        positions = [mesh.positions for mesh in self.meshes]
        return tuple(
            fn(value for points in positions for value in points[axis::3])
            for fn in (min, max)
            for axis in range(3)
        )  # type: ignore[return-value]


def _illustration_label(component: ComponentPlacement) -> str | None:
    """Return the diagnostic label retained by fresh and cached placements."""
    if isinstance(component, CachedComponentPlacement):
        return component.illustration_label
    return component.direct.label if component.direct is not None else None


def model_catalog_context(pcbdoc: AltiumPcbDoc) -> CatalogContext:
    """Resolve the embedded model lookup once for a source board."""
    helper = PcbAssemblyModelHelper()
    catalog, _ = helper._collect_embedded_step_model_catalog(pcbdoc)
    by_id: dict[str, list[dict[str, object]]] = {}
    by_name: dict[str, list[dict[str, object]]] = {}
    for entry in catalog:
        by_id.setdefault(entry["id_norm"], []).append(entry)
        by_name.setdefault(entry["name_norm"], []).append(entry)
    return helper, by_id, by_name


def _excluded_component(
    component: AltiumPcbComponent | None, excluded: frozenset[str]
) -> bool:
    return component is not None and component.designator in excluded


def _merge_component_body(
    groups: dict[tuple[int, Side], ComponentPlacement],
    key: tuple[int, Side],
    part: ComponentPlacement,
) -> None:
    previous = groups.get(key)
    if previous is None:
        groups[key] = part
        return
    # A cached placement represents every body for its owner; later cache rows
    # carry None, so only fresh mesh-bearing bodies reach this merge.
    previous = cast(IllustrationComponent, previous)
    part = cast(IllustrationComponent, part)
    groups[key] = replace(
        previous,
        meshes=previous.meshes + part.meshes,
        bodies=previous.bodies + part.bodies,
    )


class IllustrationJob(IllustrationDiagnosticsMixin):
    """One native client and reusable tessellations/illustrations per render job."""

    def __init__(
        self,
        client: g.GeometerClient,
        *,
        line_width_mm: float = 0.025,
        cache: PcbSvgModelCache | None = None,
        emit_warnings: bool = True,
        region_index: BoardRegionEnvelopeIndex | None = None,
    ) -> None:
        if not math.isfinite(line_width_mm) or line_width_mm <= 0:
            raise ValueError("Illustration line width must be positive millimeters")
        self.client = client
        self.line_width_mm = line_width_mm
        self.cache = cache
        self.region_index = region_index
        self._tessellations: dict[str, tuple[g.MeshIllustrationMesh, ...]] = {}
        self._tessellation_warnings: dict[str, tuple[str, ...]] = {}
        self._tessellation_failures: dict[str, str] = {}
        self._prepared_tessellations = {}
        self._illustrations: dict[str, IllustrationSymbol] = {}
        self._illustration_failures: dict[str, str] = {}
        # Immutable tessellations/placed arrays are shared only for this job.
        # Retain source objects alongside identity keys to prevent ID reuse.
        self._placements = {}
        self._appearance_meshes = {}
        self._appearance_keys = {}
        self._early_components = {}
        self._body_warning_events = {}
        self._warning_capture = None
        self._suppress_collection_warnings = False
        self.counts = dict(
            tessellations=0,
            tessellation_hits=0,
            illustrations=0,
            illustration_hits=0,
            tessellation_disk_hits=0,
            illustration_disk_hits=0,
        )
        self._initialize_diagnostics(emit_warnings)

    def _tessellate(
        self,
        key: str,
        payload: bytes | dict[str, object],
        *,
        context: str | None = None,
    ) -> tuple[g.MeshIllustrationMesh, ...]:
        if key in self._tessellations:
            self.counts["tessellation_hits"] += 1
            self._warn_tessellation(key, context)
            return self._tessellations[key]
        if key in self._tessellation_failures:
            raise ModelGeometryError(self._tessellation_failures[key])
        disk_key = _tessellation_disk_key(key)
        prepared = self._prepared_tessellations.pop(key, None)
        cached = prepared[1] if prepared is not None and prepared[0] == "disk" else None
        if prepared is None and self.cache is not None:
            cached = self.cache.load(
                "tessellation", disk_key, _decode_cached_tessellation
            )
        if cached is not None:
            meshes, warnings = cached
            self._tessellations[key], self._tessellation_warnings[key] = (
                meshes,
                warnings,
            )
            self.counts["tessellation_disk_hits"] += 1
            self._warn_tessellation(key, context)
            log.debug("Reused cached model: %s", context or key[:12])
            return meshes
        result = self._tessellate_native(key, payload, prepared, context)
        self._tessellation_warnings[key] = tuple(result.metadata.warnings)
        self._warn_tessellation(key, context)
        self.counts["tessellations"] += 1
        self._tessellations[key] = result.mesh_collection.meshes
        if self.cache is not None:
            self.cache.store(
                "tessellation",
                disk_key,
                dict(
                    meshes=[asdict(mesh) for mesh in result.mesh_collection.meshes],
                    warnings=self._tessellation_warnings[key],
                ),
            )
        return result.mesh_collection.meshes

    def _tessellate_native(
        self,
        key: str,
        payload: bytes | dict[str, object],
        prepared: tuple[Literal["native"], Future[g.ModelTessellation]] | None,
        context: str | None,
    ) -> g.ModelTessellation:
        try:
            if prepared is not None:
                result = prepared[1].result()
            else:
                log.info("Tessellating model: %s", context or key[:12])
                step = payload if isinstance(payload, bytes) else g.planar_step(payload)
                result = _model_tessellation(self.client, step)
        except (g.GeometerOperationError, g.GeometerError) as error:
            reason = _geometer_failure_message(error)
            self._tessellation_failures[key] = reason
            raise ModelGeometryError(reason) from error
        return result

    def _warn_tessellation(self, key: str, context: str | None) -> None:
        for warning in self._tessellation_warnings.get(key, ()):
            self.warn(
                f"{context}: {warning}" if context else warning,
                code="geometer-warning",
                category="geometer_geometry",
                producer="geometer",
                model_identity=key,
                detail={"upstream_message": warning},
            )

    def collect_top(self, pcbdoc: AltiumPcbDoc) -> list[ComponentPlacement]:
        return self.collect(pcbdoc, side="top")

    def _prefetch_steps(
        self,
        pcbdoc: AltiumPcbDoc,
        helper: PcbAssemblyModelHelper,
        by_id: ModelCatalog,
        by_name: ModelCatalog,
        side: Side,
        excluded: frozenset[str],
        workers: PcbSvgNativeWorkers,
        cached_bodies: CachedBodies | tuple[()] = (),
        direct_indices: frozenset[int] = frozenset(),
        include_opposite: bool = False,
    ) -> None:
        futures = {}
        for index, body in enumerate(pcbdoc.component_bodies):
            if index in cached_bodies or index in direct_indices:
                continue
            entry = self._prefetch_entry(
                pcbdoc,
                body,
                (helper, by_id, by_name),
                side,
                excluded,
                include_opposite,
            )
            if entry is None:
                continue
            key = cast(str, entry["hash"])
            if (
                key in self._tessellations
                or key in self._tessellation_failures
                or key in self._prepared_tessellations
            ):
                continue
            scheduled = self._prepare_tessellation(key, entry, workers)
            if scheduled is not None:
                futures[scheduled] = (
                    entry["name"],
                    _owning_component(pcbdoc, body),
                    index,
                )
        if futures:
            log.info("Preparing %s STEP models: %d unique models", side, len(futures))
            log.debug(
                "Tessellating %d unique %s STEP models across up to %d native workers",
                len(futures),
                side,
                workers.count,
            )
            # Finish the batch before serial extrusions use the collection
            # client: do not run a fifth native operation beside four workers.
            _report_step_completions(futures, side)

    def _prepare_tessellation(
        self,
        key: str,
        entry: dict[str, object],
        workers: PcbSvgNativeWorkers,
    ) -> Future[g.ModelTessellation] | None:
        cached = (
            self.cache.load(
                "tessellation",
                _tessellation_disk_key(key),
                _decode_cached_tessellation,
            )
            if self.cache is not None
            else None
        )
        if cached is not None:
            self._prepared_tessellations[key] = "disk", cached
            return None
        future = workers.submit(_model_tessellation, cast(bytes, entry["step_bytes"]))
        self._prepared_tessellations[key] = "native", future
        return future

    @staticmethod
    def _prefetch_entry(
        pcbdoc: AltiumPcbDoc,
        body: AltiumPcbComponentBody,
        catalog: CatalogContext,
        side: Side,
        excluded: frozenset[str],
        include_opposite: bool = False,
    ) -> dict[str, object] | None:
        helper, by_id, by_name = catalog
        if body.model_type != 1:
            return None
        component = _owning_component(pcbdoc, body)
        if component is not None and component.designator in excluded:
            return None
        # This pass schedules eligible work only. Validation and diagnostics
        # still occur in the original body-order collection below.
        try:
            if not include_opposite and helper._component_body_is_bottom(
                body.properties, component
            ) != (side == "bottom"):
                return None
            if (
                _body_opacity(body) == 0
                or _body_anchor(helper, body, component) is None
            ):
                return None
        except ValueError, TypeError:
            return None
        entry = helper._resolve_component_body_model_entry(
            body.properties,
            models_by_id=by_id,
            models_by_name=by_name,
        )
        if entry is None:
            return None
        return entry

    def collect(
        self,
        pcbdoc: AltiumPcbDoc,
        *,
        side: Literal["top", "bottom"] = "top",
        excluded_designators: frozenset[str] = frozenset(),
        workers: PcbSvgNativeWorkers | None = None,
        cached_bodies: CachedBodies | None = None,
        catalog_context: CatalogContext | None = None,
        capture_warnings: bool = False,
    ) -> list[ComponentPlacement]:
        if side not in {"top", "bottom"}:
            raise ValueError(f"Invalid illustration side: {side}")
        helper, by_id, by_name = catalog_context or model_catalog_context(pcbdoc)
        cached_bodies = cached_bodies or {}
        include_opposite = self.region_index is not None
        direct_batches = self._direct_body_batches(
            pcbdoc,
            helper,
            side,
            excluded_designators,
            cached_bodies,
            include_opposite,
        )
        direct_indices = frozenset(
            index for indices in direct_batches.values() for index in indices
        )
        if workers is not None and workers.count > 1:
            self._prefetch_steps(
                pcbdoc,
                helper,
                by_id,
                by_name,
                side,
                excluded_designators,
                workers,
                cached_bodies,
                direct_indices,
                include_opposite,
            )
        return self._collect_placements(
            pcbdoc,
            (helper, by_id, by_name),
            side,
            excluded_designators,
            cached_bodies,
            capture_warnings,
            direct_batches,
            include_opposite,
        )

    def _direct_body_batches(
        self,
        pcbdoc: AltiumPcbDoc,
        helper: PcbAssemblyModelHelper,
        side: Side,
        excluded: frozenset[str],
        cached_bodies: CachedBodies,
        include_opposite: bool = False,
    ) -> dict[int, tuple[int, ...]]:
        owner_indices: dict[int, list[int]] = {}
        for index, body in enumerate(pcbdoc.component_bodies):
            owner = (
                body.component_index if body.component_index is not None else -index - 1
            )
            owner_indices.setdefault(owner, []).append(index)
        direct_batches: dict[int, tuple[int, ...]] = {}
        for indices in owner_indices.values():
            relevant = self._eligible_direct_indices(
                pcbdoc,
                helper,
                indices,
                side,
                excluded,
                cached_bodies,
                include_opposite,
            )
            by_authored_side: dict[Side, list[int]] = {"top": [], "bottom": []}
            for index in relevant:
                body = pcbdoc.component_bodies[index]
                component = _owning_component(pcbdoc, body)
                authored_side: Side = (
                    "bottom"
                    if helper._component_body_is_bottom(body.properties, component)
                    else "top"
                )
                by_authored_side[authored_side].append(index)
            for authored in by_authored_side.values():
                if authored and self._direct_batch_supported(pcbdoc, authored):
                    direct_batches[authored[0]] = tuple(authored)
        return direct_batches

    @staticmethod
    def _eligible_direct_indices(
        pcbdoc: AltiumPcbDoc,
        helper: PcbAssemblyModelHelper,
        indices: list[int],
        side: Side,
        excluded: frozenset[str],
        cached_bodies: CachedBodies,
        include_opposite: bool = False,
    ) -> list[int]:
        relevant = []
        try:
            for index in indices:
                body = pcbdoc.component_bodies[index]
                component = _owning_component(pcbdoc, body)
                if (
                    not _excluded_component(component, excluded)
                    and (
                        include_opposite
                        or helper._component_body_is_bottom(body.properties, component)
                        == (side == "bottom")
                    )
                    and _body_opacity(body) != 0
                    and index not in cached_bodies
                ):
                    relevant.append(index)
        except ValueError, TypeError:
            return []
        return relevant

    @staticmethod
    def _direct_batch_supported(pcbdoc: AltiumPcbDoc, indices: list[int]) -> bool:
        model_types = [pcbdoc.component_bodies[index].model_type for index in indices]
        return (len(model_types) == 1 and model_types[0] in {0, 1, 2, 3}) or all(
            model_type in {0, 2, 3} for model_type in model_types
        )

    def _collect_placements(
        self,
        pcbdoc: AltiumPcbDoc,
        catalog: CatalogContext,
        side: Side,
        excluded: frozenset[str],
        cached_bodies: CachedBodies,
        capture_warnings: bool,
        direct_batches: dict[int, tuple[int, ...]],
        include_opposite: bool = False,
    ) -> list[ComponentPlacement]:
        helper, _, _ = catalog
        groups: dict[tuple[int, Side], ComponentPlacement] = {}
        consumed_direct: set[int] = set()
        for index, body in enumerate(pcbdoc.component_bodies):
            if index in consumed_direct:
                continue
            component = _owning_component(pcbdoc, body)
            if _excluded_component(component, excluded):
                continue
            batch = direct_batches.get(index)
            if self._collect_direct_batch(
                pcbdoc, body, component, helper, side, batch, groups, consumed_direct
            ):
                continue
            part = self._collect_or_replay_body(
                body,
                index,
                component,
                catalog,
                side,
                cached_bodies,
                capture_warnings,
                batch is not None and len(batch) == 1,
                include_opposite,
            )
            if part is None:
                continue
            owner = (
                cast(int, body.component_index) if component is not None else -index - 1
            )
            key = (owner, cast(IllustrationComponent, part).authored_side)
            _merge_component_body(groups, key, part)
        return list(groups.values())

    def _collect_direct_batch(
        self,
        pcbdoc: AltiumPcbDoc,
        body: AltiumPcbComponentBody,
        component: AltiumPcbComponent | None,
        helper: PcbAssemblyModelHelper,
        side: Side,
        batch: tuple[int, ...] | None,
        groups: dict[tuple[int, Side], ComponentPlacement],
        consumed: set[int],
    ) -> bool:
        if batch is None or len(batch) <= 1:
            return False
        try:
            authored_side: Side = (
                "bottom"
                if helper._component_body_is_bottom(body.properties, component)
                else "top"
            )
            part = self._collect_direct_analytic_group(
                pcbdoc, batch, component, helper, authored_side
            )
            if part is not None:
                part = self._place_on_board_surface(part)
        except ModelGeometryError, ValueError, TypeError, AttributeError:
            return False
        if part is None:
            return False
        for body_index in batch:
            self._body_warning_events[body_index] = []
        groups[(cast(int, body.component_index), authored_side)] = part
        consumed.update(batch[1:])
        return True

    def _collect_direct_analytic_group(
        self,
        pcbdoc: AltiumPcbDoc,
        indices: tuple[int, ...],
        component: AltiumPcbComponent | None,
        helper: PcbAssemblyModelHelper,
        side: Side,
    ) -> IllustrationComponent | None:
        if component is None:
            return None
        anchor = _body_anchor(helper, pcbdoc.component_bodies[indices[0]], component)
        if anchor is None:
            raise ModelGeometryError("missing component/model anchor")
        anchor_mm = (anchor[0] * _MIL_MM, anchor[1] * _MIL_MM)
        rotation = _component_rotation_degrees(component)
        primitives: list[g.AnalyticPrimitiveA0] = []
        bodies: list[BodyMetadata] = []
        identities = []
        for index in indices:
            body = pcbdoc.component_bodies[index]
            body_anchor = _body_anchor(helper, body, component)
            if body_anchor is None or body_anchor != anchor:
                raise ModelGeometryError(
                    "analytic component bodies require one common anchor"
                )
            color = _colorref(body.body_color_3d)
            opacity = _body_opacity(body)
            if opacity < 1:
                self.warn(
                    f"{component.designator} body {index}: partial opacity uses opaque HLR occlusion",
                    code="partial-opacity-opaque-occlusion",
                    category="geometer_geometry",
                    component_designator=str(component.designator),
                    body_index=index,
                )
            primitive, lower, upper, identity = _analytic_body(
                body,
                index,
                anchor,
                anchor_mm,
                rotation,
                side == "bottom",
                color,
                opacity,
            )
            primitives.append(primitive)
            identities.append(identity)
            bodies.append(
                cast(
                    BodyMetadata,
                    dict(
                        index=index,
                        kind={0: "extruded", 2: "cylinder", 3: "sphere"}[
                            body.model_type
                        ],
                        lower_z_mm=lower,
                        upper_z_mm=upper,
                        color=color,
                        opacity=opacity,
                    ),
                )
            )
        source = g.AnalyticIllustrationSourceA0(
            kind="analytic",
            scene=g.AnalyticSceneA0(
                definitions=(
                    g.AnalyticDefinitionA0(
                        id="component", primitives=tuple(primitives)
                    ),
                ),
                occurrences=(
                    g.AnalyticOccurrenceA0(
                        id="component",
                        definition_id="component",
                        transform=_column_major(_rotation_z(rotation)),
                    ),
                ),
            ),
            lowering=g.AnalyticLoweringOptionsA0(
                linear_deflection_mm=0.01, angular_deflection_rad=0.5
            ),
        )
        return IllustrationComponent(
            str(component.designator),
            anchor_mm,
            (),
            tuple(bodies),
            pcbdoc.component_bodies[indices[0]].component_index,
            DirectIllustrationSource(
                source,
                None,
                dict(kind="analytic-component", values=identities, rotation=rotation),
                "analytic bodies",
            ),
            authored_side=side,
        )

    def _collect_or_replay_body(
        self,
        body: AltiumPcbComponentBody,
        index: int,
        component: AltiumPcbComponent | None,
        catalog: CatalogContext,
        side: Side,
        cached_bodies: CachedBodies,
        capture_warnings: bool,
        direct: bool,
        include_opposite: bool = False,
    ) -> ComponentPlacement | None:
        helper, by_id, by_name = catalog
        if index in cached_bodies:
            part, events = cached_bodies[index]
            self._body_warning_events[index] = events
            for deduplicate, message, metadata in events:
                (self.warn if deduplicate else self._append_warning)(
                    message, **metadata
                )
        else:
            events = [] if capture_warnings else None
            self._warning_capture = events
            try:
                part = self._collect_body(
                    body,
                    index,
                    component,
                    helper,
                    by_id,
                    by_name,
                    side,
                    direct,
                    include_opposite,
                )
                if part is not None:
                    part = self._place_on_board_surface(part)
            finally:
                self._warning_capture = None
            if capture_warnings:
                self._body_warning_events[index] = events
        return part

    def _place_on_board_surface(
        self, part: IllustrationComponent
    ) -> IllustrationComponent:
        """Move a bottom-authored model from top-surface zero to its region surface."""

        if part.authored_side != "bottom" or self.region_index is None:
            return part
        query = self.region_index.query_point(
            part.anchor_mm[0] / _MIL_MM,
            part.anchor_mm[1] / _MIL_MM,
        )
        region = query.region
        if (
            query.status is BoardRegionQueryStatus.OUTSIDE
            and len(self.region_index.regions) == 1
            and not self.region_index.invalid_regions
            and self.region_index.regions[0].is_flex is False
        ):
            region = self.region_index.regions[0]
            log.debug(
                "%s: using sole rigid board region %s for outside component anchor",
                part.designator,
                region.name,
            )
        if region is None:
            self.warn(
                f"{part.designator}: bottom-side placement retained at z=0 because "
                f"the board region at its anchor is {query.status.value}",
                code="component-placement-region-unresolved",
                category="clipping",
                component_designator=part.designator,
                detail={
                    "authored_side": part.authored_side,
                    "query_status": query.status.value,
                    "query_detail": query.detail,
                },
            )
            return part
        return _translate_component_z(part, -region.total_thickness_mils * _MIL_MM)

    def _collect_body(
        self,
        body: AltiumPcbComponentBody,
        index: int,
        component: AltiumPcbComponent | None,
        helper: PcbAssemblyModelHelper,
        by_id: dict[str, list[dict[str, object]]],
        by_name: dict[str, list[dict[str, object]]],
        side: Literal["top", "bottom"],
        direct: bool = False,
        include_opposite: bool = False,
    ) -> IllustrationComponent | None:
        is_bottom = helper._component_body_is_bottom(body.properties, component)
        if not include_opposite and is_bottom != (side == "bottom"):
            return None
        authored_side: Side = "bottom" if is_bottom else "top"
        opacity = _body_opacity(body)
        if opacity == 0:
            return None
        anchor = _body_anchor(helper, body, component)
        if anchor is None:
            self.warn(
                f"Body {index}: missing component/model anchor; omitted",
                code="missing-model-anchor",
                category="invalid_model_geometry",
                body_index=index,
                model_identity=_body_model_label(body),
            )
            return None
        anchor_mm = (anchor[0] * _MIL_MM, anchor[1] * _MIL_MM)
        designator = (
            str(component.designator) if component is not None else f"free-body-{index}"
        )
        try:
            direct_part = self._try_collect_direct_body(
                direct,
                body,
                index,
                component,
                helper,
                by_id,
                by_name,
                authored_side,
                anchor,
                anchor_mm,
                designator,
                opacity,
            )
            if direct_part is not None:
                return direct_part
            return self._collect_mesh_body(
                body,
                index,
                component,
                helper,
                by_id,
                by_name,
                anchor,
                anchor_mm,
                designator,
                opacity,
                is_bottom,
            )
        except ModelGeometryError as error:
            name = _body_model_label(body)
            category, code = _body_failure_classification(body)
            self.warn(
                f"{designator} body {index} ({name}): {error}; omitted",
                code=code,
                category=category,
                component_designator=designator,
                body_index=index,
                model_identity=name,
            )
            return None

    def _try_collect_direct_body(
        self,
        direct: bool,
        body: AltiumPcbComponentBody,
        index: int,
        component: AltiumPcbComponent | None,
        helper: PcbAssemblyModelHelper,
        by_id: ModelCatalog,
        by_name: ModelCatalog,
        side: Side,
        anchor: tuple[float, float],
        anchor_mm: Vector2,
        designator: str,
        opacity: float,
    ) -> IllustrationComponent | None:
        if not direct:
            return None
        return self._collect_direct_body(
            body,
            index,
            component,
            helper,
            by_id,
            by_name,
            side,
            anchor,
            anchor_mm,
            designator,
            opacity,
        )

    def _collect_mesh_body(
        self,
        body: AltiumPcbComponentBody,
        index: int,
        component: AltiumPcbComponent | None,
        helper: PcbAssemblyModelHelper,
        by_id: ModelCatalog,
        by_name: ModelCatalog,
        anchor: tuple[float, float],
        anchor_mm: Vector2,
        designator: str,
        opacity: float,
        is_bottom: bool,
    ) -> IllustrationComponent | None:
        geometry = self._body_geometry(
            body,
            component,
            anchor,
            helper,
            by_id,
            by_name,
            f"{designator} body {index}",
            is_bottom,
        )
        if geometry is None:
            return None
        raw_meshes, matrix, color, kind = geometry
        meshes = self._place_body(raw_meshes, matrix, color, opacity, index)
        if kind == "step":
            alternative_matrix = _step_matrix(
                helper,
                body,
                component,
                anchor,
                is_bottom=is_bottom,
                rotation_mode="footprint_local",
            )
            if alternative_matrix != matrix:
                target = _body_outline_bounds_local_mm(body, anchor_mm)
                if target is None:
                    self.warn(
                        f"{designator} body {index}: authored outline cannot resolve model Z rotation; retaining current placement",
                        code="rotation-outline-unavailable",
                        category="rotation_resolution",
                        component_designator=designator,
                        body_index=index,
                        model_identity=_body_model_label(body),
                    )
                else:
                    alternative_meshes = self._place_body(
                        raw_meshes,
                        alternative_matrix,
                        color,
                        opacity,
                        index,
                    )
                    resolution = resolve_model_z_rotation(
                        target,
                        _mesh_bounds(meshes),
                        _mesh_bounds(alternative_meshes),
                    )
                    if resolution.choice == "footprint_local":
                        meshes = alternative_meshes
                    elif resolution.choice == "unresolved":
                        self.warn(
                            f"{designator} body {index}: neither supported model Z-rotation interpretation matches the authored outline; retaining current placement",
                            code="rotation-unresolved",
                            category="rotation_resolution",
                            component_designator=designator,
                            body_index=index,
                            model_identity=_body_model_label(body),
                            detail={
                                "reason": resolution.reason,
                                "instance_space_score": resolution.current_score,
                                "footprint_local_score": resolution.footprint_local_score,
                            },
                        )
        if not meshes:
            return None
        z_values = [z for mesh in meshes for z in mesh.positions[2::3]]
        metadata = cast(
            BodyMetadata,
            dict(
                index=index,
                kind=kind,
                lower_z_mm=min(z_values),
                upper_z_mm=max(z_values),
                color=color,
                opacity=opacity,
            ),
        )
        self._warn_partial_opacity(meshes, designator, index)
        return IllustrationComponent(
            designator,
            anchor_mm,
            meshes,
            (metadata,),
            body.component_index if component is not None else None,
            authored_side="bottom" if is_bottom else "top",
        )

    def _collect_direct_body(
        self,
        body: AltiumPcbComponentBody,
        index: int,
        component: AltiumPcbComponent | None,
        helper: PcbAssemblyModelHelper,
        by_id: ModelCatalog,
        by_name: ModelCatalog,
        side: Side,
        anchor_mils: tuple[float, float],
        anchor_mm: Vector2,
        designator: str,
        opacity: float,
    ) -> IllustrationComponent | None:
        color = _colorref(body.body_color_3d)
        is_bottom = side == "bottom"
        if body.model_type == 1:
            direct_source = self._direct_step_source(
                body,
                component,
                helper,
                by_id,
                by_name,
                anchor_mils,
                is_bottom,
                color,
                opacity,
            )
            if direct_source is None:
                return None
            lower = upper = 0.0
            kind = "step"
        else:
            direct_source, lower, upper = _direct_analytic_source(
                body,
                index,
                component,
                anchor_mils,
                anchor_mm,
                is_bottom,
                color,
                opacity,
            )
            kind = {0: "extruded", 2: "cylinder", 3: "sphere"}[body.model_type]
        metadata = cast(
            BodyMetadata,
            dict(
                index=index,
                kind=kind,
                lower_z_mm=lower,
                upper_z_mm=upper,
                color=color
                if body.model_type != 1 or body.body_override_color
                else None,
                opacity=opacity,
            ),
        )
        if opacity < 1:
            self._append_warning(
                f"{designator} body {index}: partial opacity uses opaque HLR occlusion",
                code="partial-opacity-opaque-occlusion",
                category="geometer_geometry",
                component_designator=designator,
                body_index=index,
            )
        return IllustrationComponent(
            designator,
            anchor_mm,
            (),
            (metadata,),
            body.component_index if component is not None else None,
            direct_source,
            authored_side=side,
        )

    def _direct_step_source(
        self,
        body: AltiumPcbComponentBody,
        component: AltiumPcbComponent | None,
        helper: PcbAssemblyModelHelper,
        by_id: ModelCatalog,
        by_name: ModelCatalog,
        anchor_mils: tuple[float, float],
        is_bottom: bool,
        color: tuple[float, float, float],
        opacity: float,
    ) -> DirectIllustrationSource | None:
        if opacity != 1 and not body.body_override_color:
            return None
        entry = helper._resolve_component_body_model_entry(
            body.properties, models_by_id=by_id, models_by_name=by_name
        )
        if entry is None:
            name = str(body.properties.get("MODEL.NAME") or "")
            raise ModelGeometryError(_unavailable_step_reason(name))
        failure = self._tessellation_failures.get(str(entry["hash"]))
        if failure is not None:
            raise ModelGeometryError(failure)
        matrix = _step_matrix(helper, body, component, anchor_mils, is_bottom=is_bottom)
        footprint_local_matrix = _step_matrix(
            helper,
            body,
            component,
            anchor_mils,
            is_bottom=is_bottom,
            rotation_mode="footprint_local",
        )
        override = (
            g.MeshIllustrationMaterial(color=color, opacity=opacity)
            if body.body_override_color
            else None
        )
        source = g.ModelAttachmentIllustrationSourceA0(
            kind="model",
            attachment="model",
            transform=_column_major(matrix),
            material_override=override,
            tessellation=g.ModelTessellationOptionsA0(
                linear_deflection_mm=0.01,
                angular_deflection_rad=0.5,
                root_placement=g.ModelRootPlacement.PRESERVE,
            ),
        )
        footprint_local_source = (
            None
            if footprint_local_matrix == matrix
            else replace(source, transform=_column_major(footprint_local_matrix))
        )
        outline_bounds = _body_outline_bounds_local_mm(
            body, (anchor_mils[0] * _MIL_MM, anchor_mils[1] * _MIL_MM)
        )
        return DirectIllustrationSource(
            source,
            cast(bytes, entry["step_bytes"]),
            dict(
                kind="step",
                model=entry["hash"],
                rotation_candidates=dict(
                    instance_space=matrix,
                    footprint_local=footprint_local_matrix,
                    authored_outline_bounds_mm=outline_bounds,
                ),
                override=asdict(override) if override is not None else None,
            ),
            str(entry["name"]),
            footprint_local_source,
            outline_bounds,
        )

    def _warn_partial_opacity(
        self, meshes: Meshes, designator: str, index: int
    ) -> None:
        if any(
            cast(float, material.opacity) < 1
            for mesh in meshes
            for material in mesh.materials
        ):
            self._append_warning(
                f"{designator} body {index}: partial opacity uses opaque HLR occlusion",
                code="partial-opacity-opaque-occlusion",
                category="geometer_geometry",
                component_designator=designator,
                body_index=index,
            )

    def _body_geometry(
        self,
        body: AltiumPcbComponentBody,
        component: AltiumPcbComponent | None,
        anchor: tuple[float, float],
        helper: PcbAssemblyModelHelper,
        by_id: dict[str, list[dict[str, object]]],
        by_name: dict[str, list[dict[str, object]]],
        designator: str,
        is_bottom: bool,
    ) -> (
        tuple[
            tuple[g.MeshIllustrationMesh, ...],
            list[list[float]],
            tuple[float, float, float] | None,
            str,
        ]
        | None
    ):
        color = _colorref(body.body_color_3d)
        if body.model_type == 0:
            rotation = _component_rotation_degrees(component)
            payload = _extrusion_request(
                body,
                (anchor[0] * _MIL_MM, anchor[1] * _MIL_MM),
                component_rotation_degrees=rotation,
                is_bottom=is_bottom,
            )
            return (
                self._tessellate(
                    _digest(payload), payload, context=f"{designator} (extruded body)"
                ),
                _rotation_z(rotation),
                color,
                "extruded",
            )
        if body.model_type == 1:
            entry = helper._resolve_component_body_model_entry(
                body.properties, models_by_id=by_id, models_by_name=by_name
            )
            if entry is None:
                name = str(body.properties.get("MODEL.NAME") or "")
                raise ModelGeometryError(_unavailable_step_reason(name))
            meshes = self._tessellate(
                entry["hash"],
                entry["step_bytes"],
                context=f"{designator} ({entry['name']})",
            )
            matrix = _step_matrix(helper, body, component, anchor, is_bottom=is_bottom)
            return meshes, matrix, color if body.body_override_color else None, "step"
        if body.model_type == 2:
            rotation = _component_rotation_degrees(component)
            key, mesh = _cylinder_mesh(
                body,
                anchor,
                component_rotation_degrees=rotation,
                is_bottom=is_bottom,
            )
            meshes = self._tessellations.setdefault(key, (mesh,))
            return meshes, _rotation_z(rotation), color, "cylinder"
        raise ModelGeometryError(f"unsupported model type {body.model_type}")

    def _place_body(
        self,
        raw_meshes: Meshes,
        matrix: list[list[float]],
        color: tuple[float, float, float] | None,
        opacity: float,
        index: int,
    ) -> Meshes:
        # Serialize the small pose exactly (including signed zero); never round
        # cache keys or compare approximate rotations/offsets.
        key = id(raw_meshes), _digest((matrix, color, opacity))
        cached = self._placements.get(key)
        if cached is None:
            meshes = _placed_meshes(raw_meshes, matrix, color, opacity, index)
            self._placements[key] = raw_meshes, meshes
            for mesh in meshes:
                self._appearance_meshes[id(mesh)] = mesh, mesh
            return meshes
        _, canonical = cached
        meshes = tuple(
            replace(mesh, id=f"body-{index}-face-{mesh.id.rsplit('-', 1)[1]}")
            for mesh in canonical
        )
        for mesh, source in zip(meshes, canonical):
            self._appearance_meshes[id(mesh)] = mesh, source
        return meshes

    def _render_keys(
        self, component: ComponentPlacement, side: Side, illustrate: bool
    ) -> RenderKeys:
        if side not in {"top", "bottom"}:
            raise ValueError(f"Invalid illustration side: {side}")
        early = self._early_components.get(id(component))
        if early is not None:
            if early[3:] != (side, self.line_width_mm, illustrate):
                raise ValueError(
                    "Cached component placement belongs to another render style"
                )
            return early[1]
        if (
            isinstance(component, IllustrationComponent)
            and component.direct is not None
        ):
            key = _digest(
                dict(
                    renderer_contract="geometer-b0-half-space-v5-scoped-apertures",
                    source=component.direct.identity,
                    line_width_mm=self.line_width_mm,
                    side=side,
                    illustrate=illustrate,
                    clipping=self._clipping_identity(component),
                )
            )
            warning_key = _digest(
                dict(
                    appearance=key,
                    body_ids=[body["index"] for body in component.bodies],
                )
            )
            return key, warning_key
        component = cast(IllustrationComponent, component)
        # Geometry is relative to the anchor; retain pose, body offsets and
        # materials. Source IDs identify diagnostics, not painted appearance.
        canonical = []
        for mesh in component.meshes:
            entry = self._appearance_meshes.setdefault(id(mesh), (mesh, mesh))
            canonical.append(entry[1])
        identity = (
            tuple(id(mesh) for mesh in canonical),
            self.line_width_mm,
            side,
            illustrate,
            _digest(self._clipping_identity(component)),
        )
        key = self._appearance_keys.get(identity)
        if key is None:
            # Mesh arrays are immutable tuples. Keep the established JSON key
            # bytes without recursively copying every scalar via asdict.
            appearance = []
            for mesh in canonical:
                value = {
                    field.name: getattr(mesh, field.name)
                    for field in fields(mesh)
                    if field.name != "id"
                }
                value["materials"] = [asdict(mat) for mat in mesh.materials]
                appearance.append(value)
            key = _digest(
                dict(
                    renderer_contract="geometer-b0-half-space-v5-scoped-apertures",
                    meshes=appearance,
                    line_width_mm=self.line_width_mm,
                    side=side,
                    illustrate=illustrate,
                    clipping=self._clipping_identity(component),
                )
            )
            self._appearance_keys[identity] = key
        warning_key = _digest(
            dict(appearance=key, mesh_ids=[m.id for m in component.meshes])
        )
        return key, warning_key

    def _clipping_identity(self, component: IllustrationComponent) -> object:
        if self.region_index is None:
            return None
        return {
            "anchor_mm": component.anchor_mm,
            "authored_side": component.authored_side,
            "policy": self._clipping_policy_identity(),
            "partition": self._region_clipping_identity(),
        }

    @staticmethod
    def _clipping_policy_identity() -> object:
        """Return policy inputs shared by every clipping-aware cache layer."""
        return {
            "clip_tolerance_mm": COMPONENT_CLIP_TOLERANCE_MM,
            "cap_policy": COMPONENT_CLIP_CAP_POLICY,
        }

    def _component_artwork_clipping_identity(self) -> object:
        """Return clipping inputs for the early whole-component artwork cache."""
        if self.region_index is None:
            return None
        return {
            "policy": self._clipping_policy_identity(),
            "partition": self._region_clipping_identity(),
        }

    def _region_clipping_identity(self) -> object:
        if self.region_index is None:
            return None
        return {
            "query_tolerance_mils": self.region_index.tolerance_mils,
            "regions": [
                {
                    "source_index": region.source_index,
                    "name": region.name,
                    "outline_mils": region.outline_mils,
                    "holes_mils": region.holes_mils,
                    "thickness_mils": region.total_thickness_mils,
                }
                for region in self.region_index.regions
            ],
            "invalid_regions": [
                {
                    "source_index": region.source_index,
                    "name": region.name,
                    "reason": region.reason,
                    "bounds_mils": region.bounds_mils,
                }
                for region in self.region_index.invalid_regions
            ],
        }

    def _load_symbol(self, key: str, warning_key: str) -> IllustrationSymbol | None:
        if self.cache is None:
            return None
        cached = self.cache.load("illustration", key, _decode_cached_symbol)
        if cached is None:
            cached = self.cache.load(
                "illustration",
                warning_key,
                lambda payload: _decode_cached_symbol(payload, allow_warnings=True),
            )
        return cached

    def render(
        self,
        component: ComponentPlacement,
        *,
        side: Literal["top", "bottom"] = "top",
        illustrate: bool = True,
    ) -> IllustrationSymbol:
        return self._render_keyed(
            component,
            self._render_keys(component, side, illustrate),
            side=side,
            illustrate=illustrate,
            prepared=(
                self._early_components[id(component)][2]
                if id(component) in self._early_components
                else None
            ),
        )

    def _render_keyed(
        self,
        component: ComponentPlacement,
        keys: RenderKeys,
        *,
        side: Side,
        illustrate: bool,
        prepared: PreparedIllustration | None = None,
    ) -> IllustrationSymbol:
        key, warning_key = keys
        if key in self._illustrations:
            self.counts["illustration_hits"] += 1
            return self._illustrations[key]
        if key in self._illustration_failures:
            raise ModelGeometryError(self._illustration_failures[key])
        # A prepared value is either a disk symbol or a future for a native miss.
        cached = prepared if isinstance(prepared, IllustrationSymbol) else None
        if prepared is None:
            cached = self._load_symbol(key, warning_key)
        if cached is not None:
            self._illustrations[key] = cached
            self.counts["illustration_disk_hits"] += 1
            self.warnings.extend(cached.warnings)
            self._log_direct_warnings(component, cached, side)
            return cached
        try:
            symbol = (
                cast(Future[IllustrationSymbol], prepared).result()
                if prepared is not None
                else self._render_native(
                    cast(IllustrationComponent, component),
                    side=side,
                    illustrate=illustrate,
                )
            )
        except g.GeometerOperationError as error:
            reason = _geometer_failure_message(error)
            self._illustration_failures[key] = reason
            raise ModelGeometryError(reason) from error
        self._illustrations[key] = symbol
        if illustrate:
            self.counts["illustrations"] += 1
        self.warnings.extend(symbol.warnings)
        self._log_direct_warnings(component, symbol, side)
        self._store_symbol(symbol, key, warning_key)
        return symbol

    def _store_symbol(
        self, symbol: IllustrationSymbol, key: str, warning_key: str
    ) -> None:
        if self.cache is not None:
            self.cache.store(
                "illustration", warning_key if symbol.warnings else key, asdict(symbol)
            )

    def _log_direct_warnings(
        self,
        component: ComponentPlacement,
        symbol: IllustrationSymbol,
        side: Side,
    ) -> None:
        if not symbol.warnings:
            return
        label = _illustration_label(component)
        context = (
            f"{component.designator} / {label} ({side})"
            if label is not None
            else f"{component.designator} ({side})"
        )
        body_index = (
            component.bodies[0]["index"] if len(component.bodies) == 1 else None
        )
        for warning in symbol.warnings:
            metadata = _DiagnosticMetadata(
                code="geometer-warning",
                category="geometer_geometry",
                producer="geometer",
                component_designator=component.designator,
                body_index=body_index,
                model_identity=label,
                detail={"side": side, "upstream_message": warning},
            )
            self._record_diagnostic(
                f"{context}: {warning}",
                metadata,
            )
        if self.emit_warnings and label is not None:
            log.warning("%s: %s", context, symbol.warnings[0])
            for warning in symbol.warnings[1:]:
                log.debug("%s: %s", context, warning)

    def render_many(
        self,
        components: Sequence[ComponentPlacement],
        *,
        side: Side,
        illustrate: bool,
        workers: PcbSvgNativeWorkers | None = None,
    ) -> PlacedIllustrations:
        prepared = {}
        keyed = []
        if workers is not None and workers.count > 1:
            keyed, prepared = self._prepare_illustrations(
                components, side, illustrate, workers
            )
        else:
            keyed = [(part, None) for part in components]
        placed = []
        for index, (part, keys) in enumerate(keyed, 1):
            self._report_illustration_progress(side, index, len(keyed), part)
            try:
                symbol = self._render_prepared(part, keys, prepared, side, illustrate)
            except ModelGeometryError as error:
                self.warn(
                    f"{part.designator} ({side}): {error}; component illustration omitted",
                    code="component-illustration-failed",
                    category="geometer_geometry",
                    producer="geometer",
                    component_designator=part.designator,
                    detail={"side": side},
                )
                continue
            if symbol.empty:
                continue
            part = self._resolve_direct_bounds(part, symbol)
            placed.append((part, symbol))
        return placed

    @staticmethod
    def _report_illustration_progress(
        side: Side, index: int, total: int, part: ComponentPlacement
    ) -> None:
        if index == 1 or index % 25 == 0:
            log.info(
                "Illustrating %s components: %d/%d (%s)",
                side,
                index,
                total,
                part.designator,
            )

    def _render_prepared(
        self,
        part: ComponentPlacement,
        keys: RenderKeys | None,
        prepared: dict[str, PreparedIllustration],
        side: Side,
        illustrate: bool,
    ) -> IllustrationSymbol:
        if keys is None:
            return self.render(part, side=side, illustrate=illustrate)
        return self._render_keyed(
            part,
            keys,
            side=side,
            illustrate=illustrate,
            prepared=prepared.get(keys[0]),
        )

    @staticmethod
    def _resolve_direct_bounds(
        part: ComponentPlacement, symbol: IllustrationSymbol
    ) -> ComponentPlacement:
        resolved_bounds = symbol.source_bounds_mm
        if symbol.aperture_source_bounds_mm is not None:
            resolved_bounds = (
                symbol.aperture_source_bounds_mm
                if resolved_bounds is None
                else (
                    *(
                        min(
                            resolved_bounds[axis],
                            symbol.aperture_source_bounds_mm[axis],
                        )
                        for axis in range(3)
                    ),
                    *(
                        max(
                            resolved_bounds[axis],
                            symbol.aperture_source_bounds_mm[axis],
                        )
                        for axis in range(3, 6)
                    ),
                )
            )
        if (
            not isinstance(part, IllustrationComponent)
            or part.direct is None
            or resolved_bounds is None
        ):
            return part
        bodies = part.bodies
        if len(bodies) == 1 and bodies[0]["kind"] == "step":
            body = dict(bodies[0])
            body["lower_z_mm"], body["upper_z_mm"] = (
                resolved_bounds[2],
                resolved_bounds[5],
            )
            bodies = (cast(BodyMetadata, body),)
        return replace(part, resolved_bounds=resolved_bounds, bodies=bodies)

    def _prepare_illustrations(
        self,
        components: Sequence[ComponentPlacement],
        side: Side,
        illustrate: bool,
        workers: PcbSvgNativeWorkers,
    ) -> tuple[
        list[tuple[ComponentPlacement, RenderKeys]], dict[str, PreparedIllustration]
    ]:
        keyed = []
        prepared = {}
        submitted = 0
        for part in components:
            keys = self._render_keys(part, side, illustrate)
            keyed.append((part, keys))
            key, warning_key = keys
            if (
                key in prepared
                or key in self._illustrations
                or key in self._illustration_failures
            ):
                continue
            early = self._early_components.get(id(part))
            cached = (
                early[2] if early is not None else self._load_symbol(key, warning_key)
            )
            if cached is not None:
                prepared[key] = cached
            else:
                prepared[key] = workers.submit(
                    _illustrate_with_client,
                    cast(IllustrationComponent, part),
                    self.line_width_mm,
                    side,
                    illustrate,
                    self.region_index,
                )
                submitted += 1
        log.debug(
            "Scheduled %d unique %s component requests across up to %d native workers",
            submitted,
            side,
            workers.count,
        )
        return keyed, prepared

    def _render_native(
        self,
        component: IllustrationComponent,
        *,
        side: Literal["top", "bottom"],
        illustrate: bool,
    ) -> IllustrationSymbol:
        if component.direct is not None:
            return self._render_direct(component, side, illustrate)
        return self._render_meshes(component, side, illustrate)

    def _render_direct(
        self, component: IllustrationComponent, side: Side, illustrate: bool
    ) -> IllustrationSymbol:
        direct = component.direct
        if direct is None:
            raise ModelGeometryError("direct illustration source is unavailable")
        current = self._render_direct_source(
            direct.source, direct.model, side, illustrate
        )
        alternative_source = direct.footprint_local_source
        target = direct.authored_outline_bounds_mm
        if alternative_source is None:
            return self._apply_direct_visibility(
                component, direct.source, current, side, illustrate
            )
        body_index = (
            component.bodies[0]["index"] if len(component.bodies) == 1 else None
        )
        if target is None or current.source_bounds_mm is None:
            self.warn(
                f"{component.designator}: authored outline cannot resolve model Z rotation; retaining current placement",
                code="rotation-outline-unavailable",
                category="rotation_resolution",
                component_designator=component.designator,
                body_index=body_index,
                model_identity=direct.label,
            )
            return self._apply_direct_visibility(
                component, direct.source, current, side, illustrate
            )
        current_check = resolve_model_z_rotation(
            target, current.source_bounds_mm, current.source_bounds_mm
        )
        if current_check.choice == "instance_space":
            return self._apply_direct_visibility(
                component, direct.source, current, side, illustrate
            )
        alternative = self._render_direct_source(
            alternative_source, direct.model, side, illustrate
        )
        if alternative.source_bounds_mm is None:
            self._queue_discarded_symbol_warnings(component, alternative, side, direct)
            self.warn(
                f"{component.designator}: alternative model Z rotation returned no native bounds; retaining current placement",
                code="rotation-bounds-unavailable",
                category="rotation_resolution",
                producer="geometer",
                component_designator=component.designator,
                body_index=body_index,
                model_identity=direct.label,
            )
            return self._apply_direct_visibility(
                component, direct.source, current, side, illustrate
            )
        resolution = resolve_model_z_rotation(
            target, current.source_bounds_mm, alternative.source_bounds_mm
        )
        if resolution.choice == "footprint_local":
            self._queue_discarded_symbol_warnings(component, current, side, direct)
            return self._apply_direct_visibility(
                component, alternative_source, alternative, side, illustrate
            )
        self._queue_discarded_symbol_warnings(component, alternative, side, direct)
        if resolution.choice == "unresolved":
            self.warn(
                f"{component.designator}: neither supported model Z-rotation interpretation matches the authored outline; retaining current placement",
                code="rotation-unresolved",
                category="rotation_resolution",
                component_designator=component.designator,
                body_index=body_index,
                model_identity=direct.label,
                detail={
                    "reason": resolution.reason,
                    "instance_space_score": resolution.current_score,
                    "footprint_local_score": resolution.footprint_local_score,
                },
            )
        return self._apply_direct_visibility(
            component, direct.source, current, side, illustrate
        )

    def _apply_direct_visibility(
        self,
        component: IllustrationComponent,
        source: g.ModelIllustrationSourceA0,
        uncut: IllustrationSymbol,
        side: Side,
        illustrate: bool,
    ) -> IllustrationSymbol:
        resolution = self._component_visibility(component, uncut.source_bounds_mm, side)
        if (
            resolution is None
            or resolution.action is ComponentVisibilityAction.RENDER_UNCLIPPED
        ):
            return uncut
        if resolution.action is ComponentVisibilityAction.OMIT:
            self._warn_unsafe_opposite_visibility(component, resolution)
            return _with_aperture_projection(_empty_illustration_symbol(), uncut)
        surface = self._render_direct_source(
            source,
            cast(DirectIllustrationSource, component.direct).model,
            side,
            illustrate,
            clipping=_native_clipping(resolution),
        )
        return _with_aperture_projection(surface, uncut)

    def _component_visibility(
        self,
        component: IllustrationComponent,
        bounds: Bounds3 | None,
        side: Side,
    ) -> ComponentVisibilityResolution | None:
        if self.region_index is None:
            return None
        if bounds is None:
            raise ModelGeometryError("native illustration did not return model bounds")
        return resolve_component_visibility(
            self.region_index,
            anchor_mm=component.anchor_mm,
            bounds_local_mm=bounds,
            authored_side=component.authored_side,
            requested_side=side,
            tolerance_mm=COMPONENT_CLIP_TOLERANCE_MM,
        )

    def _warn_unsafe_opposite_visibility(
        self,
        component: IllustrationComponent,
        resolution: ComponentVisibilityResolution,
    ) -> None:
        if (
            resolution.requested_side == component.authored_side
            or resolution.reason == "clipped-fragment-empty"
        ):
            return
        self.warn(
            f"{component.designator}: opposite-side model fragment omitted because {resolution.reason}",
            code="component-clipping-unresolved",
            category="clipping",
            component_designator=component.designator,
            detail={
                "authored_side": component.authored_side,
                "requested_side": resolution.requested_side,
                "reason": resolution.reason,
                "region_name": resolution.region_name,
            },
        )

    def _render_direct_source(
        self,
        source: g.ModelIllustrationSourceA0,
        model: bytes | None,
        side: Side,
        illustrate: bool,
        *,
        clipping: g.IllustrationClipping | None = None,
    ) -> IllustrationSymbol:
        bottom = side == "bottom"
        rendered = self.client.model_illustration_geometry(
            g.ModelIllustrationGeometryRequestB0(
                schema="geometry.model_illustration_geometry.request.b0",
                source=source,
                view=g.MeshIllustrationView(
                    direction=(0, 0, -1) if bottom else (0, 0, 1),
                    up=(0, 1, 0),
                    mirror_x=bottom,
                ),
                linework=g.ModelIllustrationLineworkOptionsA0(
                    fast=_fast_hlr_options(),
                    outline_width_mm=self.line_width_mm,
                    detail_width_mm=self.line_width_mm * 0.55,
                ),
                style=_illustration_style(bottom),
                clipping=clipping,
            ),
            model,
            timeout=60,
        )
        return _symbol_from_geometry(
            rendered, outline_width_mm=self.line_width_mm, illustrate=illustrate
        )

    def _queue_discarded_symbol_warnings(
        self,
        component: IllustrationComponent,
        symbol: IllustrationSymbol,
        side: Side,
        direct: DirectIllustrationSource,
    ) -> None:
        body_index = (
            component.bodies[0]["index"] if len(component.bodies) == 1 else None
        )
        for warning in symbol.warnings:
            self.warn(
                f"{component.designator} / {direct.label} ({side}): {warning}",
                code="geometer-warning",
                category="geometer_geometry",
                producer="geometer",
                component_designator=component.designator,
                body_index=body_index,
                model_identity=direct.label,
                detail={"side": side, "upstream_message": warning},
            )

    def _render_meshes(
        self, component: IllustrationComponent, side: Side, illustrate: bool
    ) -> IllustrationSymbol:
        resolution = self._component_visibility(component, component.bounds, side)
        if (
            resolution is None
            or resolution.action is ComponentVisibilityAction.RENDER_UNCLIPPED
        ):
            return self._render_mesh_projection(
                component, side, illustrate, clipping=None, resolution=resolution
            )
        if resolution.action is ComponentVisibilityAction.OMIT:
            self._warn_unsafe_opposite_visibility(component, resolution)
            uncut = self._render_mesh_projection(
                component, side, illustrate, clipping=None, resolution=None
            )
            return _with_aperture_projection(_empty_illustration_symbol(), uncut)
        surface = self._render_mesh_projection(
            component,
            side,
            illustrate,
            clipping=_native_clipping(resolution),
            resolution=resolution,
        )
        uncut = self._render_mesh_projection(
            component, side, illustrate, clipping=None, resolution=None
        )
        return _with_aperture_projection(surface, uncut)

    def _render_mesh_projection(
        self,
        component: IllustrationComponent,
        side: Side,
        illustrate: bool,
        *,
        clipping: g.IllustrationClipping | None,
        resolution: ComponentVisibilityResolution | None,
    ) -> IllustrationSymbol:
        bottom = side == "bottom"
        meshes = component.meshes
        visible_bounds = _clipped_conservative_bounds(component.bounds, resolution)
        direction = (0, 0, -1) if bottom else (0, 0, 1)
        view = g.HlrViewSpec(id=side, direction=direction, up=(0, 1, 0))
        hlr = self.client.mesh_hlr_projection(
            g.MeshCollectionA0(
                schema="geometry.mesh_collection.a0",
                length_unit="millimeter",
                meshes=meshes,
            ),
            g.MeshHlrProjectionRequestB0(
                schema="geometry.mesh_hlr_projection.request.b0",
                views=(view,),
                output_outline=True,
                output_detail=True,
                output_bbox=True,
                round_digits=6,
                fast=_fast_hlr_options(),
                clipping=clipping,
            ),
            timeout=60,
        )
        projected_view = next(v for v in hlr.views if v.id == side)
        projected = projected_view.modes.outline
        outline = tuple(
            (((-x1 if bottom else x1), -y1), ((-x2 if bottom else x2), -y2))
            for x1, y1, x2, y2 in projected.segments
        )
        if hlr.empty:
            return replace(
                _empty_illustration_symbol(),
                outline_segments_mm=outline,
                source_bounds_mm=visible_bounds,
            )
        if not illustrate:
            return IllustrationSymbol(
                "", 0, 0, 1, {}, (), outline, visible_bounds, hlr.empty
            )
        projected_bounds = projected_view.modes.bbox.bounds
        if projected_bounds is None:
            raise ModelGeometryError(
                "nonempty clipped illustration did not return projected bounds"
            )
        # HLR's -Z view reverses X.  mesh_illustration mirrors that view back
        # into board coordinates, so use the correspondingly mirrored origin.
        min_x = -projected_bounds.max_x if bottom else projected_bounds.min_x
        max_y = projected_bounds.max_y
        span = max(projected_bounds.width, projected_bounds.height, 1e-9)
        result = self.client.mesh_illustration(
            g.MeshIllustrationInputB0(
                schema="geometry.mesh_illustration.input.b0",
                meshes=meshes,
                # Native bottom projection reverses X. Undo that here to retain
                # board XY registration; the whole SVG is mirrored once by the
                # compositor together with copper, film and silkscreen.
                view=g.MeshIllustrationView(
                    direction=direction, up=(0, 1, 0), mirror_x=bottom
                ),
                style=replace(
                    _illustration_style(bottom),
                    outline_width=self.line_width_mm / span,
                    crease_width=self.line_width_mm * 0.55 / span,
                ),
                svg=g.MeshIllustrationSvgOptions(coordinate_span=_COORDINATE_SPAN),
                clipping=clipping,
            ),
            hlr_projection=hlr,
            timeout=60,
        )
        return IllustrationSymbol(
            result.svg,
            min_x - 0.06 * span,
            -max_y - 0.06 * span,
            span / _COORDINATE_SPAN,
            asdict(result.stats),
            result.warnings,
            outline,
            visible_bounds,
            result.empty,
        )


def _with_aperture_projection(
    surface: IllustrationSymbol, uncut: IllustrationSymbol
) -> IllustrationSymbol:
    """Pair disjoint board-surface and aperture projections for SVG composition."""

    if uncut.empty:
        return surface
    aperture = IllustrationProjection(
        uncut.svg,
        uncut.x_mm,
        uncut.y_mm,
        uncut.mm_per_unit,
    )
    warnings = tuple(dict.fromkeys((*surface.warnings, *uncut.warnings)))
    return replace(
        surface,
        warnings=warnings,
        outline_segments_mm=uncut.outline_segments_mm,
        empty=False,
        aperture=aperture,
        aperture_source_bounds_mm=uncut.source_bounds_mm,
    )


def _illustrate_with_client(
    client: g.GeometerClient,
    component: IllustrationComponent,
    line_width: float,
    side: Side,
    illustrate: bool,
    region_index: BoardRegionEnvelopeIndex | None = None,
) -> IllustrationSymbol:
    # A task's style is immutable even when later views use another line width.
    return IllustrationJob(
        client, line_width_mm=line_width, region_index=region_index
    )._render_native(
        component,
        side=side,
        illustrate=illustrate,
    )


def _translate_component_z(
    component: IllustrationComponent, offset_mm: float
) -> IllustrationComponent:
    """Apply a world-Z board-surface placement to every source representation."""

    if not math.isfinite(offset_mm):
        raise ValueError("Component board Z offset must be finite")
    if offset_mm == component.board_z_offset_mm:
        return component
    if component.board_z_offset_mm != 0.0:
        raise ValueError("Component board Z placement cannot be applied twice")
    meshes = tuple(
        _transform_mesh(mesh, _translation(0, 0, offset_mm), mesh.id)
        for mesh in component.meshes
    )
    direct = component.direct
    if direct is not None:
        direct = replace(
            direct,
            source=_translate_direct_source_z(direct.source, offset_mm),
            identity={
                "source": direct.identity,
                "board_z_offset_mm": offset_mm,
            },
            footprint_local_source=(
                None
                if direct.footprint_local_source is None
                else _translate_direct_source_z(
                    direct.footprint_local_source, offset_mm
                )
            ),
        )
    bodies = tuple(
        cast(
            BodyMetadata,
            {
                **body,
                "lower_z_mm": body["lower_z_mm"] + offset_mm,
                "upper_z_mm": body["upper_z_mm"] + offset_mm,
            },
        )
        for body in component.bodies
    )
    bounds = component.resolved_bounds
    if bounds is not None:
        bounds = (
            bounds[0],
            bounds[1],
            bounds[2] + offset_mm,
            bounds[3],
            bounds[4],
            bounds[5] + offset_mm,
        )
    return replace(
        component,
        meshes=meshes,
        bodies=bodies,
        direct=direct,
        resolved_bounds=bounds,
        board_z_offset_mm=offset_mm,
    )


def _translate_direct_source_z(
    source: g.ModelIllustrationSourceA0, offset_mm: float
) -> g.ModelIllustrationSourceA0:
    if isinstance(source, g.ModelAttachmentIllustrationSourceA0):
        transform = list(source.transform or _column_major(_translation(0, 0)))
        transform[14] += offset_mm
        return replace(
            source,
            transform=cast(g.IllustrationMatrix4x4, tuple(transform)),
        )
    if isinstance(source, g.AnalyticIllustrationSourceA0):
        occurrences = tuple(
            _translate_analytic_occurrence_z(occurrence, offset_mm)
            for occurrence in source.scene.occurrences
        )
        return replace(source, scene=replace(source.scene, occurrences=occurrences))
    raise TypeError(f"Unsupported direct illustration source {type(source).__name__}")


def _translate_analytic_occurrence_z(
    occurrence: g.AnalyticOccurrenceA0, offset_mm: float
) -> g.AnalyticOccurrenceA0:
    transform = list(occurrence.transform or _column_major(_translation(0, 0)))
    transform[14] += offset_mm
    return replace(
        occurrence,
        transform=cast(g.IllustrationMatrix4x4, tuple(transform)),
    )


def combine_components(
    components: list[IllustrationComponent],
) -> IllustrationComponent:
    """Place all bodies in one scene and let Geometer resolve their depth."""
    if not components:
        raise ValueError("No component illustrations to combine")
    anchor = components[0].anchor_mm
    meshes = []
    for index, component in enumerate(components):
        matrix = _translation(
            component.anchor_mm[0] - anchor[0], component.anchor_mm[1] - anchor[1]
        )
        meshes.extend(
            _transform_mesh(mesh, matrix, f"component-{index}-{mesh.id}")
            for mesh in component.meshes
        )
    direct = _combine_analytic_sources(components, anchor)
    if direct is None and not meshes:
        raise ValueError(
            "Direct STEP components are illustrated separately and cannot be combined"
        )
    return IllustrationComponent(
        "board-components",
        anchor,
        tuple(meshes),
        tuple(body for component in components for body in component.bodies),
        direct=direct,
        authored_side=components[0].authored_side,
    )


def _combine_analytic_sources(
    components: list[IllustrationComponent], anchor: Vector2
) -> DirectIllustrationSource | None:
    direct_sources = [component.direct for component in components]
    if not all(_is_analytic_source(source) for source in direct_sources):
        return None
    definitions = []
    occurrences = []
    identities = []
    lowering = None
    for index, (component, source) in enumerate(
        zip(components, direct_sources, strict=True)
    ):
        source = cast(DirectIllustrationSource, source)
        analytic = cast(g.AnalyticIllustrationSourceA0, source.source)
        prefix = f"component-{index}-"
        renamed = {
            definition.id: prefix + definition.id
            for definition in analytic.scene.definitions
        }
        definitions.extend(
            replace(definition, id=renamed[definition.id])
            for definition in analytic.scene.definitions
        )
        dx = component.anchor_mm[0] - anchor[0]
        dy = component.anchor_mm[1] - anchor[1]
        occurrences.extend(
            _translated_occurrence(occurrence, prefix, renamed, dx, dy)
            for occurrence in analytic.scene.occurrences
        )
        lowering = analytic.lowering
        identities.append((source.identity, dx, dy))
    return DirectIllustrationSource(
        g.AnalyticIllustrationSourceA0(
            kind="analytic",
            scene=g.AnalyticSceneA0(
                definitions=tuple(definitions), occurrences=tuple(occurrences)
            ),
            lowering=lowering,
        ),
        None,
        dict(kind="analytic-components", values=identities),
        "analytic components",
    )


def _is_analytic_source(source: DirectIllustrationSource | None) -> bool:
    return bool(
        source is not None
        and source.model is None
        and isinstance(source.source, g.AnalyticIllustrationSourceA0)
    )


def _translated_occurrence(
    occurrence: g.AnalyticOccurrenceA0,
    prefix: str,
    renamed: dict[str, str],
    dx: float,
    dy: float,
) -> g.AnalyticOccurrenceA0:
    transform = list(occurrence.transform or _column_major(_translation(0, 0)))
    transform[12] += dx
    transform[13] += dy
    return replace(
        occurrence,
        id=prefix + occurrence.id,
        definition_id=renamed[occurrence.definition_id],
        transform=cast(g.IllustrationMatrix4x4, tuple(transform)),
    )


def _owning_component(
    pcbdoc: AltiumPcbDoc, body: AltiumPcbComponentBody
) -> AltiumPcbComponent | None:
    index = body.component_index
    if index is None or not 0 <= index < len(pcbdoc.components):
        return None
    return pcbdoc.components[index]


def _body_opacity(body: AltiumPcbComponentBody) -> float:
    opacity = float(body.body_opacity_3d)
    if not math.isfinite(opacity) or not 0 <= opacity <= 1:
        raise ValueError(f"Invalid body opacity {opacity}")
    return opacity


def _body_anchor(
    helper: PcbAssemblyModelHelper,
    body: AltiumPcbComponentBody,
    component: AltiumPcbComponent | None,
) -> tuple[float, float] | None:
    values = [
        helper._parse_altium_mils(
            getattr(component, axis)
            if component is not None
            else body.properties.get(f"MODEL.2D.{axis.upper()}"),
            assume_internal_units=False,
            default=None,
        )
        for axis in ("x", "y")
    ]
    if values[0] is None or values[1] is None:
        return None
    return values[0], values[1]


def _analytic_body(
    body: AltiumPcbComponentBody,
    index: int,
    anchor_mils: tuple[float, float],
    anchor_mm: Vector2,
    rotation: float,
    is_bottom: bool,
    color: tuple[float, float, float],
    opacity: float,
) -> tuple[g.AnalyticPrimitiveA0, float, float, object]:
    material = g.MeshIllustrationMaterial(color=color, opacity=opacity)
    if body.model_type == 0:
        return _analytic_extrusion(
            body, index, anchor_mm, rotation, is_bottom, material, color, opacity
        )
    return _analytic_radial_body(
        body, index, anchor_mils, rotation, is_bottom, material, color, opacity
    )


def _analytic_extrusion(
    body: AltiumPcbComponentBody,
    index: int,
    anchor_mm: Vector2,
    rotation: float,
    is_bottom: bool,
    material: g.MeshIllustrationMaterial,
    color: tuple[float, float, float],
    opacity: float,
) -> tuple[g.AnalyticPrimitiveA0, float, float, object]:
    request = _extrusion_request(
        body, anchor_mm, component_rotation_degrees=rotation, is_bottom=is_bottom
    )
    value = cast(dict[str, object], cast(list[object], request["bodies"])[0])
    regions = tuple(
        g.IllustrationProfileRegionA0(
            outer=_illustration_ring(cast(dict[str, object], authored["outer"])),
            holes=tuple(
                _illustration_ring(hole)
                for hole in cast(list[dict[str, object]], authored["holes"])
            ),
        )
        for authored in cast(list[dict[str, object]], value["regions"])
    )
    lower = float(cast(float | int | str, value["z_mm"]))
    upper = lower + float(cast(float | int | str, value["thickness_mm"]))
    primitive = g.AnalyticExtrusionA0(
        kind="extrusion",
        id=f"body-{index}",
        regions=regions,
        z_min_mm=lower,
        z_max_mm=upper,
        material=material,
    )
    identity = dict(kind="extrusion", geometry=request, color=color, opacity=opacity)
    return primitive, lower, upper, identity


def _analytic_radial_body(
    body: AltiumPcbComponentBody,
    index: int,
    anchor_mils: tuple[float, float],
    rotation: float,
    is_bottom: bool,
    material: g.MeshIllustrationMaterial,
    color: tuple[float, float, float],
    opacity: float,
) -> tuple[g.AnalyticPrimitiveA0, float, float, object]:
    radius = (
        float(
            body.model_cylinder_radius
            if body.model_type == 2
            else body.model_sphere_radius
        )
        * _IU_MM
    )
    lower = float(body.standoff_height) * _IU_MM
    if not math.isfinite(radius + lower) or radius <= 0:
        if body.model_type == 2:
            height = float(body.model_cylinder_height) * _IU_MM
            raise ModelGeometryError(
                "cylinder requires positive finite radius and height; "
                f"received {radius:g}, {height:g} mm"
            )
        raise ModelGeometryError(
            f"analytic body requires a positive finite radius; received {radius:g} mm"
        )
    board_center = (
        float(body.model_2d_x) * _IU_MM - anchor_mils[0] * _MIL_MM,
        float(body.model_2d_y) * _IU_MM - anchor_mils[1] * _MIL_MM,
    )
    radians = math.radians(rotation)
    cosine, sine = math.cos(radians), math.sin(radians)
    center = (
        round((cosine * board_center[0]) + (sine * board_center[1]), 10),
        round((-sine * board_center[0]) + (cosine * board_center[1]), 10),
    )
    if body.model_type == 2:
        height = float(body.model_cylinder_height) * _IU_MM
        if not math.isfinite(height) or height <= 0:
            raise ModelGeometryError(
                f"cylinder requires a positive finite height; received {height:g} mm"
            )
        upper = lower + height
        if is_bottom:
            lower, upper = -upper, -lower
        primitive = g.AnalyticCylinderA0(
            kind="cylinder",
            id=f"body-{index}",
            center_mm=center,
            radius_mm=radius,
            z_min_mm=lower,
            z_max_mm=upper,
            material=material,
        )
    else:
        center_z = lower + radius
        if is_bottom:
            center_z = -center_z
        lower, upper = center_z - radius, center_z + radius
        primitive = g.AnalyticSphereA0(
            kind="sphere",
            id=f"body-{index}",
            center_mm=(center[0], center[1], center_z),
            radius_mm=radius,
            material=material,
        )
    identity = dict(
        kind=body.model_type,
        center_mm=center,
        radius_mm=radius,
        lower_z_mm=lower,
        upper_z_mm=upper,
        color=color,
        opacity=opacity,
    )
    return primitive, lower, upper, identity


def _direct_analytic_source(
    body: AltiumPcbComponentBody,
    index: int,
    component: AltiumPcbComponent | None,
    anchor_mils: tuple[float, float],
    anchor_mm: Vector2,
    is_bottom: bool,
    color: tuple[float, float, float],
    opacity: float,
) -> tuple[DirectIllustrationSource, float, float]:
    rotation = _component_rotation_degrees(component)
    primitive, lower, upper, identity = _analytic_body(
        body, index, anchor_mils, anchor_mm, rotation, is_bottom, color, opacity
    )
    source = g.AnalyticIllustrationSourceA0(
        kind="analytic",
        scene=g.AnalyticSceneA0(
            definitions=(g.AnalyticDefinitionA0(id="body", primitives=(primitive,)),),
            occurrences=(
                g.AnalyticOccurrenceA0(
                    id="body",
                    definition_id="body",
                    transform=_column_major(_rotation_z(rotation)),
                ),
            ),
        ),
        lowering=g.AnalyticLoweringOptionsA0(
            linear_deflection_mm=0.01, angular_deflection_rad=0.5
        ),
    )
    return (
        DirectIllustrationSource(
            source,
            None,
            dict(kind="analytic", value=identity, rotation=rotation),
            _body_model_label(body),
        ),
        lower,
        upper,
    )
