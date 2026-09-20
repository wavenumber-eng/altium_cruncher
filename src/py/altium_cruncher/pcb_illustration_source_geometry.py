"""Altium body lowering and placement helpers for component illustration."""

from __future__ import annotations

from collections.abc import Sequence
import math
from typing import Literal, cast

import geometer as g
from altium_monkey.altium_pcb_component import AltiumPcbComponent
from altium_monkey.altium_record_pcb__component_body import AltiumPcbComponentBody
from altium_monkey.altium_record_pcb__shapebased_region import (
    PcbExtendedVertex,
    PcbSimpleVertex,
)

from .altium_cruncher_pcb_assembly_model_helper import PcbAssemblyModelHelper
from .altium_cruncher_pcb_layer_step import _extended_vertices_ring
from .pcb_illustration_model_geometry import (
    Bounds3,
    Meshes,
    ModelGeometryError,
    digest,
    extrusion_extents_mm,
    transform_mesh,
    visible_mesh,
)


_IU_MM = 0.00000254
_MIL_MM = 0.0254


def body_outline_bounds_local_mm(
    body: AltiumPcbComponentBody, anchor_mm: tuple[float, float]
) -> tuple[float, float, float, float] | None:
    ring = _extended_vertices_ring(list(body.outline))
    if ring is None:
        return None
    value = ring.to_json()
    points_value = value.get("points")
    if not isinstance(points_value, list):
        return None
    points = cast(list[list[float]], points_value)
    if len(points) < 3 or any(
        len(point) < 2 or not math.isfinite(point[0] + point[1]) for point in points
    ):
        return None
    xs = [point[0] - anchor_mm[0] for point in points]
    ys = [point[1] - anchor_mm[1] for point in points]
    bounds = (min(xs), min(ys), max(xs), max(ys))
    return bounds if bounds[0] < bounds[2] and bounds[1] < bounds[3] else None


def mesh_bounds(meshes: Meshes) -> Bounds3:
    positions = [mesh.positions for mesh in meshes]
    if not positions or any(not points for points in positions):
        raise ModelGeometryError("model contains no positioned mesh vertices")
    return cast(
        Bounds3,
        tuple(
            fn(value for points in positions for value in points[axis::3])
            for fn in (min, max)
            for axis in range(3)
        ),
    )


def placed_meshes(
    raw_meshes: tuple[g.MeshIllustrationMesh, ...],
    matrix: list[list[float]],
    color: tuple[float, float, float] | None,
    opacity: float,
    index: int,
) -> tuple[g.MeshIllustrationMesh, ...]:
    meshes = []
    for face, mesh in enumerate(raw_meshes):
        visible = visible_mesh(mesh, opacity, color)
        if visible is not None:
            meshes.append(transform_mesh(visible, matrix, f"body-{index}-face-{face}"))
    return tuple(meshes)


def extrusion_ring(
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


def extrusion_request(
    body: AltiumPcbComponentBody,
    anchor_mm: tuple[float, float],
    *,
    component_rotation_degrees: float = 0.0,
    is_bottom: bool = False,
) -> dict[str, object]:
    lower, upper = extrusion_extents_mm(body)
    region = {
        "outer": extrusion_ring(body.outline, anchor_mm, component_rotation_degrees),
        "holes": [
            extrusion_ring(hole, anchor_mm, component_rotation_degrees)
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


def illustration_ring(value: dict[str, object]) -> g.IllustrationProfileRingA0:
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


def cylinder_mesh(
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
    key = digest(
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


def step_matrix(
    helper: PcbAssemblyModelHelper,
    body: AltiumPcbComponentBody,
    component: AltiumPcbComponent | None,
    anchor: tuple[float, float],
    *,
    is_bottom: bool = False,
    rotation_mode: Literal["instance_space", "footprint_local"] = "instance_space",
) -> list[list[float]]:
    props = body.properties
    rotation = float(component.rotation) if component is not None else 0.0
    raw_rotz = props.get("MODEL.3D.ROTZ")
    authored_rotz = (
        helper._parse_altium_float(raw_rotz, default=0.0) if raw_rotz else 0.0
    )
    rotz = (
        authored_rotz + (rotation if is_bottom else -rotation)
        if rotation_mode == "instance_space"
        else authored_rotz
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


__all__ = [
    "body_outline_bounds_local_mm",
    "cylinder_mesh",
    "extrusion_request",
    "illustration_ring",
    "mesh_bounds",
    "placed_meshes",
    "step_matrix",
]
