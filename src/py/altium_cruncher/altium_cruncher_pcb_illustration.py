"""Experimental top/bottom component illustrations, in board millimeters.

The job owns native calls and caches. Each component's authored bodies remain
separate meshes in one native illustration. Repeated component poses reuse SVGs;
Geometer combines matching painted surfaces as in its demos.
Invisible geometry is removed before both illustration and HLR.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields, replace
import hashlib
import json
import logging
import math
import re
from typing import TYPE_CHECKING, Literal, TypedDict, cast
from collections.abc import Sequence
from concurrent.futures import Future, as_completed
from pathlib import Path

from altium_monkey.altium_pcbdoc import AltiumPcbDoc
from altium_monkey.altium_pcb_component import AltiumPcbComponent
from altium_monkey.altium_record_pcb__component_body import AltiumPcbComponentBody
from altium_monkey.altium_record_pcb__shapebased_region import (
    PcbExtendedVertex,
    PcbSimpleVertex,
)
import xml.etree.ElementTree as ET

import geometer as g

from .altium_cruncher_pcb_assembly_model_helper import PcbAssemblyModelHelper
from .altium_cruncher_pcb_layer_step import _extended_vertices_ring
from .pcb_illustration_geometry_svg import geometry_svg

if TYPE_CHECKING:
    from .pcb_svg_model_cache import PcbSvgModelCache
    from .pcb_svg_workers import PcbSvgNativeWorkers

log = logging.getLogger(__name__)

_IU_MM = 0.00000254
_MIL_MM = 0.0254
_SVG = "http://www.w3.org/2000/svg"
_COORDINATE_SPAN = 1_000_000


class ModelGeometryError(Exception):
    """A single authored model cannot supply illustration geometry."""


def _unavailable_step_reason(name: str) -> str:
    extension = Path(name.strip().strip("\x00")).suffix.lower()
    formats = {
        ".x_t": "Parasolid text",
        ".x_b": "Parasolid binary",
        ".sldprt": "SolidWorks part",
        ".sldasm": "SolidWorks assembly",
    }
    if extension and extension not in {".step", ".stp"}:
        return (
            f"unsupported model format {formats.get(extension, 'unknown')} ({extension}); "
            "Toon supports embedded STEP (.step/.stp), Altium extruded bodies, "
            "and Altium cylinder bodies"
        )
    return "embedded STEP unavailable or unreadable"


def _body_model_label(body: AltiumPcbComponentBody) -> str:
    labels = {0: "extruded body", 2: "cylinder body", 3: "sphere body"}
    fallback = labels.get(body.model_type, "unnamed model")
    return str(body.properties.get("MODEL.NAME") or fallback)


def _report_step_completions(
    futures: dict[
        Future[g.ModelTessellation], tuple[str, AltiumPcbComponent | None, int]
    ],
    side: str,
) -> None:
    # Observe completion without raising task errors here; source-order
    # consumption still supplies body-specific warnings/errors.
    for completed, future in enumerate(as_completed(futures), 1):
        name, component, index = futures[future]
        owner = component.designator if component is not None else f"free-body-{index}"
        failed = future.cancelled() or future.exception() is not None
        log.info(
            "%s %s STEP model %d/%d: %s (%s)",
            "Failed" if failed else "Completed",
            side,
            completed,
            len(futures),
            name,
            owner,
        )


def _geometer_failure_message(error: g.GeometerOperationError | g.GeometerError) -> str:
    if isinstance(error, g.GeometerOperationError):
        details = "; ".join(f"{d.code}: {d.message}" for d in error.diagnostics)
        return f"{error.operation}: {details}" if details else str(error)
    return str(error)


type Side = Literal["top", "bottom"]
type Vector2 = tuple[float, float]
type Bounds3 = tuple[float, float, float, float, float, float]
type Meshes = tuple[g.MeshIllustrationMesh, ...]
type WarningEvents = list[tuple[bool, str]]
type TessellationCacheValue = tuple[Meshes, tuple[str, ...]]
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


@dataclass(frozen=True)
class DirectIllustrationSource:
    """Compact model input retained until Geometer performs one-pass illustration."""

    source: g.ModelIllustrationSourceA0
    model: bytes | None
    identity: object
    label: str


@dataclass(frozen=True)
class IllustrationComponent:
    designator: str
    anchor_mm: tuple[float, float]
    meshes: tuple[g.MeshIllustrationMesh, ...]
    bodies: tuple[BodyMetadata, ...]
    component_index: int | None = None
    direct: DirectIllustrationSource | None = None
    resolved_bounds: Bounds3 | None = None

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


@dataclass(frozen=True)
class IllustrationSymbol:
    svg: str
    # Native SVG origin/scale expressed in board-space SVG coordinates (Y down).
    x_mm: float
    y_mm: float
    mm_per_unit: float
    stats: dict[str, object]
    warnings: tuple[str, ...]
    outline_segments_mm: tuple[
        tuple[tuple[float, float], tuple[float, float]], ...
    ] = ()
    source_bounds_mm: Bounds3 | None = None

    def group(self, symbol_id: str) -> ET.Element:
        """Inline native CSS so multiple symbols cannot recolor one another."""
        root = ET.fromstring(self.svg)
        styles: dict[str, dict[str, str]] = {}
        for style in root.findall(f"{{{_SVG}}}style"):
            for selector, declarations in re.findall(
                r"\.([\w-]+)\s*\{([^}]+)\}", style.text or ""
            ):
                styles[selector] = dict(
                    part.strip().split(":", 1)
                    for part in declarations.split(";")
                    if ":" in part
                )
            root.remove(style)
        group = ET.Element(f"{{{_SVG}}}g", {"id": symbol_id})
        _inline_styles(root, styles)
        local = ET.SubElement(
            group,
            f"{{{_SVG}}}g",
            {
                "transform": f"translate({self.x_mm:.12g} {self.y_mm:.12g}) scale({self.mm_per_unit:.12g})"
            },
        )
        local.extend(child for child in root if child.tag != f"{{{_SVG}}}title")
        return group


def _digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode()
    ).hexdigest()


def _tessellation_disk_key(key: str) -> str:
    return _digest(
        dict(
            model=key,
            linear_deflection_mm=0.01,
            angular_deflection_rad=0.5,
            root_placement="preserve",
            allow_partial="native-default",
        )
    )


def _model_tessellation(client: g.GeometerClient, step: bytes) -> g.ModelTessellation:
    return client.model_tessellation(
        step,
        g.ModelTessellationRequestA0(
            schema="geometry.model_tessellation.request.a0",
            linear_deflection_mm=0.01,
            angular_deflection_rad=0.5,
            # Preserve the STEP root, including Z, before Altium placement.
            root_placement=g.ModelRootPlacement.PRESERVE,
        ),
        timeout=60,
    )


def _colorref(value: int) -> tuple[float, float, float]:
    return tuple(((int(value) >> shift) & 255) / 255 for shift in (0, 8, 16))  # type: ignore[return-value]


def extrusion_extents_mm(body: AltiumPcbComponentBody) -> tuple[float, float]:
    """Altium MAXZ/OVERALLHEIGHT is the upper elevation, not thickness."""
    props = body.properties
    low = (
        body.model_extruded_min_z
        if "MODEL.EXTRUDED.MINZ" in props
        else body.standoff_height
    )
    high = (
        body.model_extruded_max_z
        if "MODEL.EXTRUDED.MAXZ" in props
        else body.overall_height
    )
    lower, upper = float(low) * _IU_MM, float(high) * _IU_MM
    if not math.isfinite(lower + upper) or upper <= lower:
        raise ValueError(
            f"Extruded body requires upper Z > lower Z; received {lower:g}, {upper:g} mm"
        )
    return lower, upper


def _transform_mesh(
    mesh: g.MeshIllustrationMesh, matrix: list[list[float]], mesh_id: str
) -> g.MeshIllustrationMesh:
    # Tessellation mesh matrices are column-major; helper matrices are row-major.
    source = mesh.matrix
    if source is not None:
        native = [[source[col * 4 + row] for col in range(4)] for row in range(4)]
        matrix = [
            [sum(matrix[r][k] * native[k][c] for k in range(4)) for c in range(4)]
            for r in range(4)
        ]

    def transform(values: tuple[float, ...], translate: bool) -> tuple[float, ...]:
        a, b, c, tx = matrix[0]
        d, e, f, ty = matrix[1]
        h, j, k, tz = matrix[2]
        if not translate:
            tx = ty = tz = 0
        result = []
        for i in range(0, len(values), 3):
            x, y, z = values[i : i + 3]
            # Preserve Python's float summation and decimal rounding.
            # Avoid allocating three generator objects for every vertex/normal.
            result.extend(
                (
                    round(sum((a * x, b * y, c * z)) + tx, 10),
                    round(sum((d * x, e * y, f * z)) + ty, 10),
                    round(sum((h * x, j * y, k * z)) + tz, 10),
                )
            )
        return tuple(result)

    return replace(
        mesh,
        id=mesh_id,
        positions=transform(mesh.positions, True),
        normals=transform(mesh.normals, False) if mesh.normals else None,
        matrix=None,
    )


def _translation(x: float, y: float, z: float = 0) -> list[list[float]]:
    return [[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]]


def _rotation_z(degrees: float) -> list[list[float]]:
    radians = math.radians(degrees)
    cosine, sine = math.cos(radians), math.sin(radians)
    return [
        [cosine, -sine, 0, 0],
        [sine, cosine, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]


def _column_major(matrix: Sequence[Sequence[float]]) -> g.IllustrationMatrix4x4:
    values = tuple(
        float(matrix[row][column]) for column in range(4) for row in range(4)
    )
    return cast(g.IllustrationMatrix4x4, values)


def _symbol_from_geometry(
    rendered: g.ModelIllustrationGeometry,
    *,
    outline_width_mm: float,
    illustrate: bool,
) -> IllustrationSymbol:
    """Adapt renderer-neutral Geometer geometry to board-local SVG millimeters."""
    svg, outline = geometry_svg(rendered, outline_width_mm)
    return IllustrationSymbol(
        svg if illustrate else "",
        0,
        0,
        1,
        asdict(rendered.metadata.stats),
        rendered.metadata.warnings,
        outline,
        cast(Bounds3, rendered.metadata.bounds_mm),
    )


def _component_rotation_degrees(
    component: AltiumPcbComponent | None,
) -> float:
    degrees = float(component.rotation or 0) if component is not None else 0.0
    if not math.isfinite(degrees):
        raise ModelGeometryError(
            f"component rotation must be finite; received {degrees}"
        )
    degrees %= 360.0
    return 0.0 if math.isclose(degrees, 0.0, abs_tol=1e-12) else degrees


def _visible_mesh(
    mesh: g.MeshIllustrationMesh,
    opacity: float,
    color: tuple[float, float, float] | None,
) -> g.MeshIllustrationMesh | None:
    materials = tuple(
        replace(
            mat,
            opacity=opacity * (1.0 if mat.opacity is None else mat.opacity),
            color=color if color is not None else mat.color,
        )
        for mat in mesh.materials
    )
    indices = (
        mesh.indices
        if mesh.indices is not None
        else tuple(range(len(mesh.positions) // 3))
    )
    face_materials = mesh.triangle_material_indices or (0,) * (len(indices) // 3)
    kept = [
        i
        for i, material in enumerate(face_materials)
        if cast(float, materials[material].opacity) > 0
    ]
    if not kept:
        return None
    # Compact vertices too: hidden/unused vertices must not expand SVG bounds.
    vertex_ids = sorted({v for i in kept for v in indices[3 * i : 3 * i + 3]})
    remap = {v: i for i, v in enumerate(vertex_ids)}
    return replace(
        mesh,
        materials=materials,
        positions=tuple(
            mesh.positions[3 * v + a] for v in vertex_ids for a in range(3)
        ),
        normals=tuple(mesh.normals[3 * v + a] for v in vertex_ids for a in range(3))
        if mesh.normals
        else None,
        indices=tuple(remap[v] for i in kept for v in indices[3 * i : 3 * i + 3]),
        triangle_material_indices=tuple(face_materials[i] for i in kept),
    )


def _finite_vector(value: object, length: int) -> tuple[float, ...]:
    if not isinstance(value, (list, tuple)) or len(value) != length:
        raise ValueError("invalid cached geometry vector")
    try:
        if any(
            isinstance(v, bool)
            or not isinstance(v, (int, float))
            or not math.isfinite(v)
            for v in value
        ):
            raise ValueError("nonfinite cached geometry")
    except OverflowError as error:
        raise ValueError("cached coordinate exceeds numeric range") from error
    return tuple(value)


def _validate_mesh_indices(values: Sequence[int], count: int) -> None:
    if any(type(index) is not int or not 0 <= index < count for index in values):
        raise ValueError("invalid cached mesh index")


def _validate_cached_mesh(mesh: g.MeshIllustrationMesh) -> None:
    if not mesh.positions or len(mesh.positions) % 3 or not mesh.materials:
        raise ValueError("invalid cached mesh")
    _finite_vector(mesh.positions, len(mesh.positions))
    if mesh.normals is not None:
        _finite_vector(mesh.normals, len(mesh.positions))
    if mesh.matrix is not None:
        _finite_vector(mesh.matrix, 16)
    indices = (
        mesh.indices
        if mesh.indices is not None
        else tuple(range(len(mesh.positions) // 3))
    )
    if len(indices) % 3:
        raise ValueError("invalid cached triangle array")
    _validate_mesh_indices(indices, len(mesh.positions) // 3)
    if mesh.triangle_material_indices is not None:
        if len(mesh.triangle_material_indices) != len(indices) // 3:
            raise ValueError("invalid cached material array")
        _validate_mesh_indices(mesh.triangle_material_indices, len(mesh.materials))
    _validate_cached_materials(mesh.materials)


def _validate_cached_materials(materials: Sequence[g.MeshIllustrationMaterial]) -> None:
    for material in materials:
        _finite_vector(material.color, 3)
        if material.opacity is not None:
            _finite_vector((material.opacity,), 1)


def _validate_symbol_geometry(symbol: IllustrationSymbol) -> None:
    _finite_vector((symbol.x_mm, symbol.y_mm, symbol.mm_per_unit), 3)
    if symbol.mm_per_unit <= 0:
        raise ValueError("invalid cached symbol scale")
    if symbol.source_bounds_mm is not None:
        bounds = _finite_vector(symbol.source_bounds_mm, 6)
        if bounds[0] > bounds[3] or bounds[1] > bounds[4] or bounds[2] > bounds[5]:
            raise ValueError("invalid cached source bounds")
    for segment in symbol.outline_segments_mm:
        if len(segment) != 2:
            raise ValueError("invalid cached outline segment")
        for point in segment:
            _finite_vector(point, 2)


def _decode_cached_tessellation(payload: object) -> TessellationCacheValue:
    payload = cast(dict, payload)
    meshes = []
    for value in payload["meshes"]:
        fields = dict(value)
        for name in (
            "positions",
            "normals",
            "indices",
            "matrix",
            "triangle_material_indices",
        ):
            if fields.get(name) is not None:
                fields[name] = tuple(fields[name])
        fields["materials"] = tuple(
            g.MeshIllustrationMaterial(**{**m, "color": tuple(m["color"])})
            for m in fields["materials"]
        )
        mesh = g.MeshIllustrationMesh(**fields)
        _validate_cached_mesh(mesh)
        meshes.append(mesh)
    warnings = tuple(payload["warnings"])
    if not all(isinstance(w, str) for w in warnings):
        raise ValueError("invalid cached warnings")
    return tuple(meshes), warnings


def _decode_cached_symbol(
    payload: object, *, allow_warnings: bool = False
) -> IllustrationSymbol:
    fields = dict(cast(dict, payload))
    if not isinstance(fields["svg"], str) or not isinstance(fields["stats"], dict):
        raise ValueError("invalid cached illustration")
    try:
        if fields["svg"] and ET.fromstring(fields["svg"]).tag != f"{{{_SVG}}}svg":
            raise ValueError("invalid cached SVG root")
    except ET.ParseError as error:
        raise ValueError("invalid cached SVG") from error
    fields["warnings"] = tuple(fields["warnings"])
    if not all(isinstance(w, str) for w in fields["warnings"]):
        raise ValueError("invalid cached illustration warnings")
    if fields["warnings"] and not allow_warnings:
        raise ValueError("instance-specific illustration warnings are not persistable")
    fields["outline_segments_mm"] = tuple(
        tuple(tuple(point) for point in segment)
        for segment in fields["outline_segments_mm"]
    )
    if fields.get("source_bounds_mm") is not None:
        fields["source_bounds_mm"] = cast(
            Bounds3, _finite_vector(fields["source_bounds_mm"], 6)
        )
    symbol = IllustrationSymbol(**fields)
    _validate_symbol_geometry(symbol)
    return symbol


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
    groups: dict[int, ComponentPlacement], key: int, part: ComponentPlacement
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


class IllustrationJob:
    """One native client and reusable tessellations/illustrations per render job."""

    def __init__(
        self,
        client: g.GeometerClient,
        *,
        line_width_mm: float = 0.025,
        cache: PcbSvgModelCache | None = None,
    ) -> None:
        if not math.isfinite(line_width_mm) or line_width_mm <= 0:
            raise ValueError("Illustration line width must be positive millimeters")
        self.client = client
        self.line_width_mm = line_width_mm
        self.cache = cache
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
        self.warnings: list[str] = []

    def warn(self, message: str) -> None:
        if self._warning_capture is not None:
            self._warning_capture.append((True, message))
        if self._suppress_collection_warnings:
            return
        if message not in self.warnings:
            self.warnings.append(message)
            log.warning(message)

    def _append_warning(self, message: str) -> None:
        if self._warning_capture is not None:
            self._warning_capture.append((False, message))
        if not self._suppress_collection_warnings:
            self.warnings.append(message)

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
            self.warn(f"{context}: {warning}" if context else warning)

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
    ) -> None:
        futures = {}
        for index, body in enumerate(pcbdoc.component_bodies):
            if index in cached_bodies or index in direct_indices:
                continue
            entry = self._prefetch_entry(
                pcbdoc, body, (helper, by_id, by_name), side, excluded
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
            if helper._component_body_is_bottom(body.properties, component) != (
                side == "bottom"
            ):
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
        direct_batches = self._direct_body_batches(
            pcbdoc, helper, side, excluded_designators, cached_bodies
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
            )
        return self._collect_placements(
            pcbdoc,
            (helper, by_id, by_name),
            side,
            excluded_designators,
            cached_bodies,
            capture_warnings,
            direct_batches,
        )

    def _direct_body_batches(
        self,
        pcbdoc: AltiumPcbDoc,
        helper: PcbAssemblyModelHelper,
        side: Side,
        excluded: frozenset[str],
        cached_bodies: CachedBodies,
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
                pcbdoc, helper, indices, side, excluded, cached_bodies
            )
            if relevant and self._direct_batch_supported(pcbdoc, relevant):
                direct_batches[relevant[0]] = tuple(relevant)
        return direct_batches

    @staticmethod
    def _eligible_direct_indices(
        pcbdoc: AltiumPcbDoc,
        helper: PcbAssemblyModelHelper,
        indices: list[int],
        side: Side,
        excluded: frozenset[str],
        cached_bodies: CachedBodies,
    ) -> list[int]:
        relevant = []
        try:
            for index in indices:
                body = pcbdoc.component_bodies[index]
                component = _owning_component(pcbdoc, body)
                if (
                    not _excluded_component(component, excluded)
                    and helper._component_body_is_bottom(body.properties, component)
                    == (side == "bottom")
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
    ) -> list[ComponentPlacement]:
        helper, _, _ = catalog
        groups: dict[int, ComponentPlacement] = {}
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
            )
            if part is None:
                continue
            key = (
                cast(int, body.component_index) if component is not None else -index - 1
            )
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
        groups: dict[int, ComponentPlacement],
        consumed: set[int],
    ) -> bool:
        if batch is None or len(batch) <= 1:
            return False
        try:
            part = self._collect_direct_analytic_group(
                pcbdoc, batch, component, helper, side
            )
        except ModelGeometryError, ValueError, TypeError, AttributeError:
            return False
        if part is None:
            return False
        for body_index in batch:
            self._body_warning_events[body_index] = []
        groups[cast(int, body.component_index)] = part
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
                    f"{component.designator} body {index}: partial opacity uses opaque HLR occlusion"
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
    ) -> ComponentPlacement | None:
        helper, by_id, by_name = catalog
        if index in cached_bodies:
            part, events = cached_bodies[index]
            self._body_warning_events[index] = events
            for deduplicate, message in events:
                (self.warn if deduplicate else self._append_warning)(message)
        else:
            events = [] if capture_warnings else None
            self._warning_capture = events
            try:
                part = self._collect_body(
                    body, index, component, helper, by_id, by_name, side, direct
                )
            finally:
                self._warning_capture = None
            if capture_warnings:
                self._body_warning_events[index] = events
        return part

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
    ) -> IllustrationComponent | None:
        is_bottom = helper._component_body_is_bottom(body.properties, component)
        if is_bottom != (side == "bottom"):
            return None
        opacity = _body_opacity(body)
        if opacity == 0:
            return None
        anchor = _body_anchor(helper, body, component)
        if anchor is None:
            self.warn(f"Body {index}: missing component/model anchor; omitted")
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
                side,
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
            self.warn(f"{designator} body {index} ({name}): {error}; omitted")
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
                f"{designator} body {index}: partial opacity uses opaque HLR occlusion"
            )
        return IllustrationComponent(
            designator,
            anchor_mm,
            (),
            (metadata,),
            body.component_index if component is not None else None,
            direct_source,
        )

    @staticmethod
    def _direct_step_source(
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
        matrix = _step_matrix(helper, body, component, anchor_mils, is_bottom=is_bottom)
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
        return DirectIllustrationSource(
            source,
            cast(bytes, entry["step_bytes"]),
            dict(
                kind="step",
                model=entry["hash"],
                matrix=matrix,
                override=asdict(override) if override is not None else None,
            ),
            str(entry["name"]),
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
                f"{designator} body {index}: partial opacity uses opaque HLR occlusion"
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
                    source=component.direct.identity,
                    line_width_mm=self.line_width_mm,
                    side=side,
                    illustrate=illustrate,
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
                    meshes=appearance,
                    line_width_mm=self.line_width_mm,
                    side=side,
                    illustrate=illustrate,
                )
            )
            self._appearance_keys[identity] = key
        warning_key = _digest(
            dict(appearance=key, mesh_ids=[m.id for m in component.meshes])
        )
        return key, warning_key

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

    @staticmethod
    def _log_direct_warnings(
        component: ComponentPlacement, symbol: IllustrationSymbol, side: Side
    ) -> None:
        if (
            not symbol.warnings
            or not isinstance(component, IllustrationComponent)
            or component.direct is None
        ):
            return
        context = f"{component.designator} / {component.direct.label} ({side})"
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
                    f"{part.designator} ({side}): {error}; component illustration omitted"
                )
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
        if (
            not isinstance(part, IllustrationComponent)
            or part.direct is None
            or symbol.source_bounds_mm is None
        ):
            return part
        bodies = part.bodies
        if len(bodies) == 1 and bodies[0]["kind"] == "step":
            body = dict(bodies[0])
            body["lower_z_mm"], body["upper_z_mm"] = (
                symbol.source_bounds_mm[2],
                symbol.source_bounds_mm[5],
            )
            bodies = (cast(BodyMetadata, body),)
        return replace(part, resolved_bounds=symbol.source_bounds_mm, bodies=bodies)

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
        bottom = side == "bottom"
        rendered = self.client.model_illustration_geometry(
            g.ModelIllustrationGeometryRequestA0(
                schema="geometry.model_illustration_geometry.request.a0",
                source=cast(g.ModelIllustrationSourceA0, component.direct.source),
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
            ),
            component.direct.model,
            timeout=60,
        )
        return _symbol_from_geometry(
            rendered, outline_width_mm=self.line_width_mm, illustrate=illustrate
        )

    def _render_meshes(
        self, component: IllustrationComponent, side: Side, illustrate: bool
    ) -> IllustrationSymbol:
        bottom = side == "bottom"
        meshes = component.meshes
        min_x, min_y, _, max_x, max_y, _ = component.bounds
        span = max(max_x - min_x, max_y - min_y, 1e-9)
        indexed = _combine_mesh_arrays(meshes)
        direction = (0, 0, -1) if bottom else (0, 0, 1)
        view = g.HlrViewSpec(id=side, direction=direction, up=(0, 1, 0))
        hlr = self.client.mesh_hlr_projection(
            indexed,
            g.HlrProjectionOptionsA0(
                views=(view,),
                output_outline=True,
                output_detail=True,
                output_bbox=False,
                curve_mode=g.HlrCurveMode.POLYLINE,
                round_digits=6,
                projection_algorithm=g.HlrProjectionAlgorithm.FAST,
                outline_algorithm=g.HlrOutlineAlgorithm.FAST_MESH_SHADOW,
                fast=_fast_hlr_options(),
            ),
            timeout=60,
        )
        projected = next(v for v in hlr.views if v.id == side).modes.outline
        outline = tuple(
            (((-x1 if bottom else x1), -y1), ((-x2 if bottom else x2), -y2))
            for x1, y1, x2, y2 in projected.segments
        )
        if not illustrate:
            return IllustrationSymbol("", 0, 0, 1, {}, (), outline)
        result = self.client.mesh_illustration(
            g.MeshIllustrationInputA0(
                schema="geometry.mesh_illustration.input.a0",
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
        )


def _fast_hlr_options() -> g.FastHlrOptionsA0:
    return g.FastHlrOptionsA0(
        include_hidden=False,
        suppress_coplanar_seams=False,
        crease_angle_rad=math.radians(25),
    )


def _illustration_style(bottom: bool) -> g.MeshIllustrationStyleA0:
    return g.MeshIllustrationStyleA0(
        shading=g.MeshIllustrationShading.TOON,
        ambient=0.28,
        key_intensity=0.9,
        rim_amount=0.12,
        light_direction=(-0.35, 0.8, -0.48) if bottom else (0.35, 0.8, 0.48),
        bands=3,
        source_colors=True,
        fallback_color=(113 / 255, 166 / 255, 160 / 255),
        transparent_background=True,
        fuse_surfaces=True,
        layer_coplanar_materials=True,
        double_sided=False,
        show_outlines=False,
        show_creases=False,
        show_hlr_outline=True,
        show_hlr_detail=True,
        outline_color="#000000",
        crease_color="#000000",
    )


def _combine_mesh_arrays(meshes: Meshes) -> g.IndexedTriangleMeshA0:
    positions: list[float] = []
    indices: list[int] = []
    source_faces: list[int] = []
    for face, mesh in enumerate(meshes):
        offset = len(positions) // 3
        local_indices = mesh.indices or tuple(range(len(mesh.positions) // 3))
        positions.extend(mesh.positions)
        indices.extend(index + offset for index in local_indices)
        source_faces.extend([face] * (len(local_indices) // 3))
    return g.IndexedTriangleMeshA0(positions, indices, source_faces)


def _illustrate_with_client(
    client: g.GeometerClient,
    component: IllustrationComponent,
    line_width: float,
    side: Side,
    illustrate: bool,
) -> IllustrationSymbol:
    # A task's style is immutable even when later views use another line width.
    return IllustrationJob(client, line_width_mm=line_width)._render_native(
        component,
        side=side,
        illustrate=illustrate,
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


def _inline_styles(root: ET.Element, styles: dict[str, dict[str, str]]) -> None:
    for element in root.iter():
        for name in element.attrib.pop("class", "").split():
            if name not in styles:
                raise ValueError(f"Unsupported native illustration CSS class: {name}")
            for key, value in styles[name].items():
                element.set(key.strip(), value.strip())
        # Current native illustrations emit no IDs/references. Fail rather
        # than silently introduce collisions if that contract changes.
        if "id" in element.attrib or any("url(" in v for v in element.attrib.values()):
            raise ValueError("Native illustration references require SVG namespacing")


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


def _placed_meshes(
    raw_meshes: tuple[g.MeshIllustrationMesh, ...],
    matrix: list[list[float]],
    color: tuple[float, float, float] | None,
    opacity: float,
    index: int,
) -> tuple[g.MeshIllustrationMesh, ...]:
    meshes = []
    for face, mesh in enumerate(raw_meshes):
        visible = _visible_mesh(mesh, opacity, color)
        if visible is not None:
            meshes.append(_transform_mesh(visible, matrix, f"body-{index}-face-{face}"))
    return tuple(meshes)


def _extrusion_ring(
    vertices: Sequence[PcbExtendedVertex | PcbSimpleVertex],
    anchor_mm: tuple[float, float],
    component_rotation_degrees: float = 0.0,
) -> dict[str, object]:
    ring = _extended_vertices_ring(list(vertices))
    if ring is None:
        raise ValueError("Invalid extrusion ring")
    value = ring.to_json()
    radians = math.radians(component_rotation_degrees)
    cosine, sine = math.cos(radians), math.sin(radians)

    def component_local(point: Sequence[float]) -> list[float]:
        x, y = point[0] - anchor_mm[0], point[1] - anchor_mm[1]
        result = [
            round((cosine * x) + (sine * y), 9),
            round((-sine * x) + (cosine * y), 9),
        ]
        return [0.0 if coordinate == 0 else coordinate for coordinate in result]

    points = cast(list[list[float]], value["points"])
    segments = cast(list[dict[str, object]], value["segments"])
    value["points"] = [component_local(point) for point in points]
    for segment in segments:
        if "center" in segment:
            segment["center"] = component_local(
                cast(Sequence[float], segment["center"])
            )
    return value


def _extrusion_request(
    body: AltiumPcbComponentBody,
    anchor_mm: tuple[float, float],
    *,
    component_rotation_degrees: float = 0.0,
    is_bottom: bool = False,
) -> dict[str, object]:
    lower, upper = extrusion_extents_mm(body)
    region = {
        "outer": _extrusion_ring(body.outline, anchor_mm, component_rotation_degrees),
        "holes": [
            _extrusion_ring(hole, anchor_mm, component_rotation_degrees)
            for hole in body.holes
        ],
    }
    return dict(
        schema="geometry.planar_step.request.a0",
        units="mm",
        name="extruded-body",
        bodies=[
            dict(
                id="body",
                name="body",
                z_mm=-upper if is_bottom else lower,
                thickness_mm=upper - lower,
                regions=[region],
            )
        ],
    )


def _illustration_ring(value: dict[str, object]) -> g.IllustrationProfileRingA0:
    points = cast(list[list[float]], value["points"])
    segments = cast(list[dict[str, object]], value["segments"])
    converted = []
    for segment in segments:
        if segment["kind"] == "line":
            converted.append(g.IllustrationProfileLineA0(kind="line"))
        elif segment["kind"] == "arc":
            center = cast(Sequence[float], segment["center"])
            converted.append(
                g.IllustrationProfileCircularArcA0(
                    kind="circular_arc",
                    center_mm=(float(center[0]), float(center[1])),
                    sweep=(
                        g.PlanarArcSweep.CCW
                        if segment["sweep"] == "ccw"
                        else g.PlanarArcSweep.CW
                    ),
                )
            )
        else:
            raise ModelGeometryError(f"unsupported extrusion segment {segment['kind']}")
    return g.IllustrationProfileRingA0(
        points_mm=tuple((float(point[0]), float(point[1])) for point in points),
        segments=tuple(converted),
    )


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


def _cylinder_mesh(
    body: AltiumPcbComponentBody,
    anchor_mils: tuple[float, float],
    *,
    component_rotation_degrees: float = 0.0,
    is_bottom: bool = False,
) -> tuple[str, g.MeshIllustrationMesh]:
    """Lower an Altium Z-axis cylinder directly to the illustration mesh boundary."""
    radius = float(body.model_cylinder_radius) * _IU_MM
    height = float(body.model_cylinder_height) * _IU_MM
    lower = float(body.standoff_height) * _IU_MM
    if not math.isfinite(radius + height + lower) or radius <= 0 or height <= 0:
        raise ModelGeometryError(
            f"cylinder requires positive finite radius and height; received {radius:g}, {height:g} mm"
        )
    upper = lower + height
    if is_bottom:
        lower, upper = -upper, -lower
    board_center = (
        float(body.model_2d_x) * _IU_MM - anchor_mils[0] * _MIL_MM,
        float(body.model_2d_y) * _IU_MM - anchor_mils[1] * _MIL_MM,
    )
    if not math.isfinite(board_center[0] + board_center[1]):
        raise ModelGeometryError("cylinder requires a finite 2D center")
    radians = math.radians(component_rotation_degrees)
    cosine, sine = math.cos(radians), math.sin(radians)
    center = (
        round((cosine * board_center[0]) + (sine * board_center[1]), 10),
        round((-sine * board_center[0]) + (cosine * board_center[1]), 10),
    )
    center = tuple(0.0 if coordinate == 0 else coordinate for coordinate in center)

    # The cylinder is already analytic Altium topology. A small local prism is
    # only the common interchange used by illustration for lighting, overlap,
    # and Z ordering; no STEP generation or OCCT tessellation is involved.
    segments = 48
    ring = tuple(
        (
            round(center[0] + radius * math.cos(2 * math.pi * index / segments), 10),
            round(center[1] + radius * math.sin(2 * math.pi * index / segments), 10),
        )
        for index in range(segments)
    )
    positions = tuple(
        coordinate for z in (lower, upper) for x, y in ring for coordinate in (x, y, z)
    ) + (center[0], center[1], lower, center[0], center[1], upper)
    bottom_center, top_center = 2 * segments, 2 * segments + 1
    indices: list[int] = []
    for index in range(segments):
        following = (index + 1) % segments
        bottom, next_bottom = index, following
        top, next_top = segments + index, segments + following
        indices.extend((bottom_center, next_bottom, bottom))
        indices.extend((top_center, top, next_top))
        indices.extend((bottom, next_bottom, next_top, bottom, next_top, top))
    key = _digest(
        {
            "kind": "altium-cylinder",
            "center_mm": center,
            "radius_mm": radius,
            "lower_z_mm": lower,
            "upper_z_mm": upper,
            "segments": segments,
        }
    )
    return key, g.MeshIllustrationMesh(
        id="cylinder",
        positions=positions,
        indices=tuple(indices),
        materials=(g.MeshIllustrationMaterial(color=(0.5, 0.5, 0.5)),),
    )


def _step_matrix(
    helper: PcbAssemblyModelHelper,
    body: AltiumPcbComponentBody,
    component: AltiumPcbComponent | None,
    anchor: tuple[float, float],
    *,
    is_bottom: bool = False,
) -> list[list[float]]:
    props = body.properties
    rotation = float(component.rotation) if component is not None else 0.0
    raw_rotz = props.get("MODEL.3D.ROTZ")
    rotz = (
        helper._parse_altium_float(raw_rotz, default=0.0)
        + (rotation if is_bottom else -rotation)
        if raw_rotz
        else 0.0
    )
    model_anchor = [
        cast(
            float,
            helper._parse_altium_mils(
                props.get(f"MODEL.2D.{axis}"),
                assume_internal_units=False,
                default=anchor[i],
            ),
        )
        for i, axis in enumerate(("X", "Y"))
    ]
    return helper._compose_step_component_transform(
        x_mm=(model_anchor[0] - anchor[0]) * _MIL_MM,
        y_mm=(model_anchor[1] - anchor[1]) * _MIL_MM,
        z_mm=float(body.model_3d_dz) * _IU_MM * (-1 if is_bottom else 1),
        model_2d_rotation_deg=rotation
        + helper._parse_altium_float(props.get("MODEL.2D.ROTATION"), default=0),
        model_rotx_deg=helper._parse_altium_float(
            props.get("MODEL.3D.ROTX"), default=0
        ),
        model_roty_deg=helper._parse_altium_float(
            props.get("MODEL.3D.ROTY"), default=0
        ),
        model_rotz_deg=rotz,
        is_bottom=is_bottom,
    )
