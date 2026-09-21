"""Model-geometry transforms, visibility filtering, and cache codecs."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import asdict, dataclass, replace
import hashlib
import json
import math
import re
from typing import cast
import xml.etree.ElementTree as ET

import geometer as g
from altium_monkey.altium_pcb_component import AltiumPcbComponent
from altium_monkey.altium_record_pcb__component_body import AltiumPcbComponentBody

from .pcb_illustration_geometry_svg import geometry_svg


_IU_MM = 0.00000254
_SVG = "http://www.w3.org/2000/svg"
type Bounds3 = tuple[float, float, float, float, float, float]
type Meshes = tuple[g.MeshIllustrationMesh, ...]
type TessellationCacheValue = tuple[Meshes, tuple[str, ...]]


class ModelGeometryError(Exception):
    """A single authored model cannot supply illustration geometry."""


@dataclass(frozen=True)
class IllustrationProjection:
    """One SVG projection in component-local board coordinates."""

    svg: str
    x_mm: float
    y_mm: float
    mm_per_unit: float

    def group(self, symbol_id: str, *, opaque_paint: bool = False) -> ET.Element:
        return _projection_group(self, symbol_id, opaque_paint=opaque_paint)


@dataclass(frozen=True)
class IllustrationSymbol(IllustrationProjection):
    """Rendered component symbol and its board-space placement metadata.

    ``aperture`` is the uncut projection used only outside the board-material
    domain.  The primary projection remains the board-surface Z fragment.
    """

    stats: dict[str, object]
    warnings: tuple[str, ...]
    outline_segments_mm: tuple[
        tuple[tuple[float, float], tuple[float, float]], ...
    ] = ()
    source_bounds_mm: Bounds3 | None = None
    empty: bool = False
    aperture: IllustrationProjection | None = None
    aperture_source_bounds_mm: Bounds3 | None = None

    def aperture_group(
        self, symbol_id: str, *, opaque_paint: bool = False
    ) -> ET.Element:
        if self.aperture is None:
            raise ValueError("illustration has no aperture projection")
        return self.aperture.group(symbol_id, opaque_paint=opaque_paint)


def _projection_group(
    projection: IllustrationProjection,
    symbol_id: str,
    *,
    opaque_paint: bool = False,
) -> ET.Element:
    """Inline native CSS so multiple symbols cannot recolor one another."""
    root = ET.fromstring(projection.svg)
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
    if opaque_paint:
        for element in root.iter():
            element.attrib.pop("opacity", None)
    local = ET.SubElement(
        group,
        f"{{{_SVG}}}g",
        {
            "transform": (
                f"translate({projection.x_mm:.12g} {projection.y_mm:.12g}) "
                f"scale({projection.mm_per_unit:.12g})"
            )
        },
    )
    local.extend(child for child in root if child.tag != f"{{{_SVG}}}title")
    return group


def fast_hlr_options() -> g.FastHlrOptionsA0:
    return g.FastHlrOptionsA0(
        include_hidden=False,
        suppress_coplanar_seams=False,
        crease_angle_rad=math.radians(25),
    )


def empty_illustration_symbol() -> IllustrationSymbol:
    return IllustrationSymbol("", 0, 0, 1, {}, (), empty=True)


def with_aperture_projection(
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


def invisible_illustration_symbol(uncut: IllustrationSymbol) -> IllustrationSymbol:
    """Preserve diagnostics from completed native work while omitting artwork."""

    return replace(
        empty_illustration_symbol(),
        warnings=uncut.warnings,
        outline_segments_mm=uncut.outline_segments_mm,
        source_bounds_mm=uncut.source_bounds_mm,
    )


def illustration_style(bottom: bool) -> g.MeshIllustrationStyleA0:
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


def digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode()
    ).hexdigest()


def tessellation_disk_key(key: str) -> str:
    return digest(
        dict(
            model=key,
            linear_deflection_mm=0.01,
            angular_deflection_rad=0.5,
            root_placement="preserve",
            allow_partial="native-default",
        )
    )


def model_tessellation(client: g.GeometerClient, step: bytes) -> g.ModelTessellation:
    return client.model_tessellation(
        step,
        g.ModelTessellationRequestA0(
            schema="geometry.model_tessellation.request.a0",
            linear_deflection_mm=0.01,
            angular_deflection_rad=0.5,
            root_placement=g.ModelRootPlacement.PRESERVE,
        ),
        timeout=60,
    )


def colorref(value: int) -> tuple[float, float, float]:
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


def transform_mesh(
    mesh: g.MeshIllustrationMesh, matrix: list[list[float]], mesh_id: str
) -> g.MeshIllustrationMesh:
    source = mesh.matrix
    if source is not None:
        native = [[source[col * 4 + row] for col in range(4)] for row in range(4)]
        matrix = [
            [sum(matrix[r][k] * native[k][c] for k in range(4)) for c in range(4)]
            for r in range(4)
        ]

    def transform_positions(values: tuple[float, ...]) -> tuple[float, ...]:
        a, b, c, tx = matrix[0]
        d, e, f, ty = matrix[1]
        h, j, k, tz = matrix[2]
        result = []
        for i in range(0, len(values), 3):
            x, y, z = values[i : i + 3]
            result.extend(
                (
                    round(sum((a * x, b * y, c * z)) + tx, 10),
                    round(sum((d * x, e * y, f * z)) + ty, 10),
                    round(sum((h * x, j * y, k * z)) + tz, 10),
                )
            )
        return tuple(result)

    def transform_normals(values: tuple[float, ...]) -> tuple[float, ...]:
        a, b, c = matrix[0][:3]
        d, e, f = matrix[1][:3]
        h, j, k = matrix[2][:3]
        determinant = a * (e * k - f * j) - b * (d * k - f * h) + c * (d * j - e * h)
        if math.isclose(determinant, 0.0, abs_tol=1e-15):
            raise ValueError("mesh affine transform is singular; normals are undefined")
        # Cofactor(A) == inverse(A).T * det(A), which is the correct affine
        # normal transform for rotation, reflection, and nonuniform scale.
        normal_matrix = (
            (
                (e * k - f * j) / determinant,
                (f * h - d * k) / determinant,
                (d * j - e * h) / determinant,
            ),
            (
                (c * j - b * k) / determinant,
                (a * k - c * h) / determinant,
                (b * h - a * j) / determinant,
            ),
            (
                (b * f - c * e) / determinant,
                (c * d - a * f) / determinant,
                (a * e - b * d) / determinant,
            ),
        )
        result: list[float] = []
        for i in range(0, len(values), 3):
            x, y, z = values[i : i + 3]
            nx, ny, nz = (
                sum(
                    (
                        normal_matrix[0][0] * x,
                        normal_matrix[0][1] * y,
                        normal_matrix[0][2] * z,
                    )
                ),
                sum(
                    (
                        normal_matrix[1][0] * x,
                        normal_matrix[1][1] * y,
                        normal_matrix[1][2] * z,
                    )
                ),
                sum(
                    (
                        normal_matrix[2][0] * x,
                        normal_matrix[2][1] * y,
                        normal_matrix[2][2] * z,
                    )
                ),
            )
            length = math.sqrt(nx * nx + ny * ny + nz * nz)
            if math.isclose(length, 0.0, abs_tol=1e-15):
                result.extend((0.0, 0.0, 0.0))
            else:
                result.extend(
                    (
                        round(nx / length, 10),
                        round(ny / length, 10),
                        round(nz / length, 10),
                    )
                )
        return tuple(result)

    return replace(
        mesh,
        id=mesh_id,
        positions=transform_positions(mesh.positions),
        normals=transform_normals(mesh.normals) if mesh.normals else None,
        matrix=None,
    )


def translation(x: float, y: float, z: float = 0) -> list[list[float]]:
    return [[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]]


def rotation_z(degrees: float) -> list[list[float]]:
    radians = math.radians(degrees)
    cosine, sine = math.cos(radians), math.sin(radians)
    return [
        [cosine, -sine, 0, 0],
        [sine, cosine, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]


def column_major(matrix: Sequence[Sequence[float]]) -> g.IllustrationMatrix4x4:
    values = tuple(
        float(matrix[row][column]) for column in range(4) for row in range(4)
    )
    return cast(g.IllustrationMatrix4x4, values)


def symbol_from_geometry(
    rendered: g.ModelIllustrationGeometry,
    *,
    outline_width_mm: float,
    illustrate: bool,
) -> IllustrationSymbol:
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
        rendered.metadata.empty,
    )


def component_rotation_degrees(component: AltiumPcbComponent | None) -> float:
    degrees = float(component.rotation or 0) if component is not None else 0.0
    if not math.isfinite(degrees):
        raise ModelGeometryError(
            f"component rotation must be finite; received {degrees}"
        )
    degrees %= 360.0
    return 0.0 if math.isclose(degrees, 0.0, abs_tol=1e-12) else degrees


def visible_mesh(
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
    indices = mesh.indices or tuple(range(len(mesh.positions) // 3))
    face_materials = mesh.triangle_material_indices or (0,) * (len(indices) // 3)
    kept = [
        i
        for i, material in enumerate(face_materials)
        if cast(float, materials[material].opacity) > 0
    ]
    if not kept:
        return None
    vertex_ids = sorted({v for i in kept for v in indices[3 * i : 3 * i + 3]})
    remap = {v: i for i, v in enumerate(vertex_ids)}
    return replace(
        mesh,
        materials=materials,
        positions=tuple(
            mesh.positions[3 * v + axis] for v in vertex_ids for axis in range(3)
        ),
        normals=(
            tuple(mesh.normals[3 * v + axis] for v in vertex_ids for axis in range(3))
            if mesh.normals
            else None
        ),
        indices=tuple(remap[v] for i in kept for v in indices[3 * i : 3 * i + 3]),
        triangle_material_indices=tuple(face_materials[i] for i in kept),
    )


def decode_cached_tessellation(payload: object) -> TessellationCacheValue:
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
    if not all(isinstance(warning, str) for warning in warnings):
        raise ValueError("invalid cached warnings")
    return tuple(meshes), warnings


def decode_cached_symbol(
    payload: object, *, allow_warnings: bool = False
) -> IllustrationSymbol:
    fields = dict(cast(dict, payload))
    if not isinstance(fields.get("stats"), dict):
        raise ValueError("invalid cached illustration")
    _validate_cached_svg(fields.get("svg"))
    fields["warnings"] = _cached_warnings(fields.get("warnings"), allow_warnings)
    fields["outline_segments_mm"] = _cached_outline_segments(
        fields.get("outline_segments_mm")
    )
    fields["source_bounds_mm"] = _cached_bounds(fields.get("source_bounds_mm"))
    fields["aperture_source_bounds_mm"] = _cached_bounds(
        fields.get("aperture_source_bounds_mm")
    )
    fields["aperture"] = _cached_projection(fields.get("aperture"))
    symbol = IllustrationSymbol(**fields)
    _validate_symbol_geometry(symbol)
    return symbol


def _validate_cached_svg(value: object) -> None:
    if not isinstance(value, str):
        raise ValueError("invalid cached illustration")
    try:
        if value and ET.fromstring(value).tag != f"{{{_SVG}}}svg":
            raise ValueError("invalid cached SVG root")
    except ET.ParseError as error:
        raise ValueError("invalid cached SVG") from error


def _cached_warnings(value: object, allow_warnings: bool) -> tuple[str, ...]:
    warnings = tuple(cast(Sequence[object], value))
    if not all(isinstance(warning, str) for warning in warnings):
        raise ValueError("invalid cached illustration warnings")
    if warnings and not allow_warnings:
        raise ValueError("instance-specific illustration warnings are not persistable")
    return cast(tuple[str, ...], warnings)


def _cached_outline_segments(
    value: object,
) -> tuple[tuple[tuple[float, float], tuple[float, float]], ...]:
    return cast(
        tuple[tuple[tuple[float, float], tuple[float, float]], ...],
        tuple(
            tuple(tuple(point) for point in segment)
            for segment in cast(Sequence[Sequence[Sequence[float]]], value)
        ),
    )


def _cached_bounds(value: object) -> Bounds3 | None:
    return None if value is None else cast(Bounds3, _finite_vector(value, 6))


def _cached_projection(value: object) -> IllustrationProjection | None:
    return None if value is None else IllustrationProjection(**dict(cast(dict, value)))


def _finite_vector(value: object, length: int) -> tuple[float, ...]:
    if not isinstance(value, (list, tuple)) or len(value) != length:
        raise ValueError("invalid cached geometry vector")
    try:
        invalid = any(
            isinstance(item, bool)
            or not isinstance(item, (int, float))
            or not math.isfinite(item)
            for item in value
        )
    except OverflowError as error:
        raise ValueError("cached coordinate exceeds numeric range") from error
    if invalid:
        raise ValueError("nonfinite cached geometry")
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
    indices = mesh.indices or tuple(range(len(mesh.positions) // 3))
    if len(indices) % 3:
        raise ValueError("invalid cached triangle array")
    _validate_mesh_indices(indices, len(mesh.positions) // 3)
    if mesh.triangle_material_indices is not None:
        if len(mesh.triangle_material_indices) != len(indices) // 3:
            raise ValueError("invalid cached material array")
        _validate_mesh_indices(mesh.triangle_material_indices, len(mesh.materials))
    _validate_cached_materials(mesh.materials)


def _validate_cached_materials(
    materials: Sequence[g.MeshIllustrationMaterial],
) -> None:
    for material in materials:
        _finite_vector(material.color, 3)
        if material.opacity is not None:
            _finite_vector((material.opacity,), 1)


def _validate_symbol_geometry(symbol: IllustrationSymbol) -> None:
    _validate_projection_geometry(symbol, "symbol")
    _validate_optional_bounds(symbol.source_bounds_mm, "source")
    _validate_optional_bounds(symbol.aperture_source_bounds_mm, "aperture source")
    _validate_outline_segments(symbol.outline_segments_mm)
    if symbol.aperture is not None:
        _validate_projection_geometry(symbol.aperture, "aperture symbol")


def _validate_projection_geometry(
    projection: IllustrationProjection, label: str
) -> None:
    _finite_vector((projection.x_mm, projection.y_mm, projection.mm_per_unit), 3)
    if projection.mm_per_unit <= 0:
        raise ValueError(f"invalid cached {label} scale")


def _validate_optional_bounds(bounds: Bounds3 | None, label: str) -> None:
    if bounds is None:
        return
    values = _finite_vector(bounds, 6)
    if values[0] > values[3] or values[1] > values[4] or values[2] > values[5]:
        raise ValueError(f"invalid cached {label} bounds")


def _validate_outline_segments(
    segments: Sequence[tuple[tuple[float, float], tuple[float, float]]],
) -> None:
    for segment in segments:
        if len(segment) != 2:
            raise ValueError("invalid cached outline segment")
        for point in segment:
            _finite_vector(point, 2)


def _inline_styles(element: ET.Element, styles: dict[str, dict[str, str]]) -> None:
    for item in element.iter():
        for name in item.attrib.pop("class", "").split():
            if name not in styles:
                raise ValueError(f"Unsupported native illustration CSS class: {name}")
            for key, value in styles[name].items():
                item.set(key.strip(), value.strip())
        if "id" in item.attrib or any(
            "url(" in value for value in item.attrib.values()
        ):
            raise ValueError("Native illustration references require SVG namespacing")


__all__ = [
    "Bounds3",
    "IllustrationProjection",
    "IllustrationSymbol",
    "Meshes",
    "ModelGeometryError",
    "TessellationCacheValue",
    "colorref",
    "column_major",
    "component_rotation_degrees",
    "decode_cached_symbol",
    "decode_cached_tessellation",
    "digest",
    "extrusion_extents_mm",
    "empty_illustration_symbol",
    "fast_hlr_options",
    "illustration_style",
    "model_tessellation",
    "rotation_z",
    "symbol_from_geometry",
    "tessellation_disk_key",
    "transform_mesh",
    "translation",
    "visible_mesh",
]
