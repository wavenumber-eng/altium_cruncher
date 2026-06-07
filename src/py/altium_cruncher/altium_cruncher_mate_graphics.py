"""Mate PCB reference graphics helpers."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from altium_cruncher.altium_cruncher_mco import JsonObject

_PAD_SHAPE_CIRCLE = 1
_PAD_SHAPE_OCTAGONAL = 3


@dataclass(frozen=True, slots=True)
class _BoardProjectionOptions:
    outline_graphics_enabled: bool
    outline_layer: str
    outline_width_mils: float
    cutout_graphics_enabled: bool
    cutout_layer: str
    cutout_width_mils: float
    actual_cutouts_enabled: bool
    actual_cutout_layer: str


def component_pad_geometries(
    pcbdoc: object,
    component_index: int,
) -> tuple[JsonObject, ...]:
    """Return absolute source-pad geometry for one component."""
    try:
        primitives = getattr(pcbdoc, "get_component_primitives")(component_index)
    except Exception:
        primitives = {}
    pads = primitives.get("pads", []) if isinstance(primitives, dict) else []
    geometries: list[JsonObject] = []
    for pad in pads:
        geometry = pad_geometry(pad)
        if geometry is not None:
            geometries.append(geometry)
    return tuple(geometries)


def pad_geometry(pad: object) -> JsonObject | None:
    """Return the geometry subset needed by mate reference graphics."""
    width_mils = pad_width_mils(pad)
    height_mils = pad_height_mils(pad)
    if width_mils <= 0.0 or height_mils <= 0.0:
        return None
    return {
        "x_mils": _float_attr(pad, "x_mils"),
        "y_mils": _float_attr(pad, "y_mils"),
        "width_mils": width_mils,
        "height_mils": height_mils,
        "shape": _int_attr(pad, "shape"),
        "layer": _int_attr(pad, "layer"),
        "rotation_degrees": _float_attr(pad, "rotation"),
    }


def pad_width_mils(pad: object) -> float:
    width = _float_attr(pad, "width_mils")
    if width > 0.0:
        return width
    for name in ("width", "top_width"):
        width = _int_attr(pad, name) / 10000.0
        if width > 0.0:
            return width
    return 0.0


def pad_height_mils(pad: object) -> float:
    height = _float_attr(pad, "height_mils")
    if height > 0.0:
        return height
    for name in ("height", "top_height"):
        height = _int_attr(pad, name) / 10000.0
        if height > 0.0:
            return height
    return 0.0


def build_pcb_reference_graphics_operations(
    *,
    output_dir: str,
    board_filename: str,
    target: Mapping[str, object],
    designator: str,
) -> list[JsonObject]:
    """Build PCB MCO operations for one target's reference graphics."""
    config = target.get("mate_reference_graphics")
    if not isinstance(config, dict) or not _optional_bool(config, "enabled", True):
        return []
    if str(config.get("shape", "") or "").strip() != "source_pad_outline":
        return []

    style = _section(config, "style")
    layer = _optional_string(config, "layer", "MECHANICAL_1") or "MECHANICAL_1"
    width_mils = _mapping_number(style, "stroke_width_mils", 10.0)
    clearance_mils = _mapping_number(style, "clearance_mils", 10.0)
    outline_spacing_mils = _mapping_number(
        style,
        "outline_spacing_mils",
        clearance_mils,
    )
    outline_count = _outline_count(style, str(style.get("mode", "outline") or "outline"))

    operations: list[JsonObject] = []
    for pad_index, geometry in enumerate(_target_source_pad_geometries(target), start=1):
        operations.extend(
            _pad_outline_operations(
                output_dir=output_dir,
                board_filename=board_filename,
                designator=designator,
                pad_index=pad_index,
                geometry=geometry,
                layer=layer,
                width_mils=width_mils,
                clearance_mils=clearance_mils,
                outline_count=outline_count,
                outline_spacing_mils=outline_spacing_mils,
            )
        )
    return operations


def _outline_count(style: Mapping[str, object], mode: str) -> int:
    explicit_count = style.get("outline_count")
    if explicit_count is not None:
        if not isinstance(explicit_count, int) or isinstance(explicit_count, bool):
            raise ValueError("Field 'outline_count' must be an integer")
        if explicit_count < 1:
            raise ValueError("Field 'outline_count' must be at least 1")
        return explicit_count

    normalized = mode.strip().lower().replace("-", "_")
    if normalized in {"double", "double_outline", "double_ring"}:
        return 2
    if normalized in {
        "outline",
        "pad_outline",
        "single",
        "single_outline",
        "single_ring",
        "trace_outline",
    }:
        return 1
    raise ValueError(
        "Mate reference_graphics style.mode must be outline or double_outline"
    )


def build_pcb_board_projection_operations(
    *,
    output_dir: str,
    board_filename: str,
    board_projection: Mapping[str, object],
    selection: object,
) -> list[JsonObject]:
    """Build PCB MCO operations for source-board projection graphics."""
    options = _board_projection_options(board_projection)
    if not _board_projection_has_enabled_outputs(options):
        return []

    operations: list[JsonObject] = []
    for board in getattr(selection, "boards", ()) or ():
        operations.extend(
            _board_projection_operations_for_board(
                output_dir=output_dir,
                board_filename=board_filename,
                board=board,
                options=options,
            )
        )
    return operations


def _board_projection_options(
    board_projection: Mapping[str, object],
) -> _BoardProjectionOptions:
    outline_graphics = _section(_section(board_projection, "outline"), "graphics")
    cutouts = _section(board_projection, "cutouts")
    cutout_graphics = _section(cutouts, "graphics")
    return _BoardProjectionOptions(
        outline_graphics_enabled=_optional_bool(outline_graphics, "enabled", False),
        outline_layer=(
            _optional_string(outline_graphics, "layer", "MECHANICAL_1")
            or "MECHANICAL_1"
        ),
        outline_width_mils=_mapping_number(
            outline_graphics,
            "stroke_width_mils",
            8.0,
        ),
        cutout_graphics_enabled=_optional_bool(cutout_graphics, "enabled", False),
        cutout_layer=(
            _optional_string(cutout_graphics, "layer", "MECHANICAL_1")
            or "MECHANICAL_1"
        ),
        cutout_width_mils=_mapping_number(cutout_graphics, "stroke_width_mils", 8.0),
        actual_cutouts_enabled=_optional_bool(cutouts, "actual_cutouts", False),
        actual_cutout_layer=_optional_string(cutouts, "layer", "MULTI_LAYER")
        or "MULTI_LAYER",
    )


def _board_projection_has_enabled_outputs(options: _BoardProjectionOptions) -> bool:
    return (
        options.outline_graphics_enabled
        or options.cutout_graphics_enabled
        or options.actual_cutouts_enabled
    )


def _board_projection_operations_for_board(
    *,
    output_dir: str,
    board_filename: str,
    board: object,
    options: _BoardProjectionOptions,
) -> list[JsonObject]:
    board_outline = getattr(board, "board_outline", None)
    if not isinstance(board_outline, dict):
        return []
    board_key = str(getattr(board, "board_key", "") or "board")
    operations = _board_outline_projection_operations(
        output_dir=output_dir,
        board_filename=board_filename,
        board_key=board_key,
        board_outline=board_outline,
        options=options,
    )
    operations.extend(
        _board_cutout_projection_operations(
            output_dir=output_dir,
            board_filename=board_filename,
            board_key=board_key,
            board_outline=board_outline,
            options=options,
        )
    )
    return operations


def _board_outline_projection_operations(
    *,
    output_dir: str,
    board_filename: str,
    board_key: str,
    board_outline: Mapping[str, object],
    options: _BoardProjectionOptions,
) -> list[JsonObject]:
    if not options.outline_graphics_enabled:
        return []
    return _board_outline_segment_operations(
        output_dir=output_dir,
        board_filename=board_filename,
        board_key=board_key,
        outline=board_outline,
        layer=options.outline_layer,
        width_mils=options.outline_width_mils,
    )


def _board_cutout_projection_operations(
    *,
    output_dir: str,
    board_filename: str,
    board_key: str,
    board_outline: Mapping[str, object],
    options: _BoardProjectionOptions,
) -> list[JsonObject]:
    operations: list[JsonObject] = []
    for cutout_index, cutout_outline in enumerate(
        _outline_cutouts(board_outline),
        start=1,
    ):
        operations.extend(
            _board_cutout_operations(
                output_dir=output_dir,
                board_filename=board_filename,
                board_key=board_key,
                cutout_index=cutout_index,
                cutout_outline=cutout_outline,
                options=options,
            )
        )
    return operations


def _board_cutout_operations(
    *,
    output_dir: str,
    board_filename: str,
    board_key: str,
    cutout_index: int,
    cutout_outline: Mapping[str, object],
    options: _BoardProjectionOptions,
) -> list[JsonObject]:
    operations: list[JsonObject] = []
    cutout_key = f"{board_key}_cutout_{cutout_index}"
    if options.cutout_graphics_enabled:
        operations.extend(
            _board_outline_segment_operations(
                output_dir=output_dir,
                board_filename=board_filename,
                board_key=cutout_key,
                outline=cutout_outline,
                layer=options.cutout_layer,
                width_mils=options.cutout_width_mils,
            )
        )
    if options.actual_cutouts_enabled:
        region = _board_cutout_region_operation(
            output_dir=output_dir,
            board_filename=board_filename,
            board_key=board_key,
            cutout_index=cutout_index,
            outline=cutout_outline,
            layer=options.actual_cutout_layer,
        )
        if region is not None:
            operations.append(region)
    return operations


def board_outline_bounds_mils(pcbdoc: object) -> JsonObject | None:
    """Return rectangular bounds for the loaded board outline."""
    board = getattr(pcbdoc, "board", None)
    outline = getattr(board, "outline", None) if board is not None else None
    vertices = list(getattr(outline, "vertices", []) or [])
    if not vertices:
        return None
    xs = [float(getattr(vertex, "x_mils")) for vertex in vertices]
    ys = [float(getattr(vertex, "y_mils")) for vertex in vertices]
    return {
        "left": min(xs),
        "bottom": min(ys),
        "right": max(xs),
        "top": max(ys),
    }


def board_outline_geometry(pcbdoc: object) -> JsonObject | None:
    """Return ordered source-board outline geometry for projection graphics."""
    board = getattr(pcbdoc, "board", None)
    outline = getattr(board, "outline", None) if board is not None else None
    vertices = list(getattr(outline, "vertices", []) or [])
    if not vertices:
        return None
    payload: JsonObject = {
        "vertices": [_board_outline_vertex(vertex) for vertex in vertices],
        "closed": True,
    }
    cutouts: list[JsonObject] = []
    for cutout in list(getattr(outline, "cutouts", []) or []):
        cutout_vertices = list(cutout or [])
        if cutout_vertices:
            cutouts.append(
                {
                    "vertices": [
                        _board_outline_vertex(vertex) for vertex in cutout_vertices
                    ],
                    "closed": True,
                }
            )
    if cutouts:
        payload["cutouts"] = cutouts
    return payload


def board_origin_mils(pcbdoc: object) -> JsonObject | None:
    """Return the loaded board origin in mils."""
    board = getattr(pcbdoc, "board", None)
    if board is None:
        return None
    return {
        "x": float(getattr(board, "origin_x", 0.0) or 0.0),
        "y": float(getattr(board, "origin_y", 0.0) or 0.0),
    }


def single_inspection_board_outline(
    inspection: Mapping[str, object],
) -> JsonObject | None:
    """Return the only inspected board outline, if there is exactly one."""
    outlines = [
        dict(board["board_outline_mils"])
        for board in _list_field(inspection, "boards")
        if isinstance(board, dict) and isinstance(board.get("board_outline_mils"), dict)
    ]
    if len(outlines) == 1:
        return outlines[0]
    return None


def single_inspection_board_origin(
    inspection: Mapping[str, object],
) -> JsonObject | None:
    """Return the only inspected board origin, if there is exactly one."""
    origins = [
        dict(board["board_origin_mils"])
        for board in _list_field(inspection, "boards")
        if isinstance(board, dict) and isinstance(board.get("board_origin_mils"), dict)
    ]
    if len(origins) == 1:
        return origins[0]
    return None


def parse_source_pad_geometries(
    raw: Mapping[str, object],
) -> tuple[JsonObject, ...]:
    """Parse stored source-pad geometry from a selection payload."""
    value = raw.get("source_pad_geometries", [])
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ValueError("Mate source_pad_geometries must be an array")
    result: list[JsonObject] = []
    for item in value:
        if not isinstance(item, dict):
            raise ValueError("Mate source_pad_geometries items must be objects")
        result.append(dict(item))
    return tuple(result)


def parse_selection_pad_geometries(
    raw: Mapping[str, object],
) -> tuple[JsonObject, ...]:
    """Parse free-pad geometry, falling back to the selection's own geometry."""
    parsed = parse_source_pad_geometries(raw)
    if parsed:
        return parsed
    geometry = _pad_geometry_from_selection(raw)
    return (geometry,) if geometry is not None else ()


def transform_source_pad_geometries(
    geometries: tuple[JsonObject, ...],
    placement: object | None,
) -> list[JsonObject]:
    """Apply a mate placement transform to source-pad geometry."""
    transformed: list[JsonObject] = []
    for geometry in geometries:
        x_mils, y_mils = _transform_placement(
            _mapping_number(geometry, "x_mils", 0.0),
            _mapping_number(geometry, "y_mils", 0.0),
            placement,
        )
        item = dict(geometry)
        item["x_mils"] = x_mils
        item["y_mils"] = y_mils
        transformed.append(item)
    return transformed


def _pad_geometry_from_selection(raw: Mapping[str, object]) -> JsonObject | None:
    required = ("x_mils", "y_mils", "width_mils", "height_mils")
    if any(name not in raw for name in required):
        return None
    return {
        "x_mils": _mapping_number(raw, "x_mils", 0.0),
        "y_mils": _mapping_number(raw, "y_mils", 0.0),
        "width_mils": _mapping_number(raw, "width_mils", 0.0),
        "height_mils": _mapping_number(raw, "height_mils", 0.0),
        "shape": int(_mapping_number(raw, "shape", 1.0)) if "shape" in raw else 1,
        "layer": int(_mapping_number(raw, "layer", 0.0)) if "layer" in raw else 0,
        "rotation_degrees": _mapping_number(raw, "rotation_degrees", 0.0)
        if "rotation_degrees" in raw
        else 0.0,
    }


def _transform_placement(
    x_mils: float,
    y_mils: float,
    placement: object | None,
) -> tuple[float, float]:
    if placement is None:
        return (x_mils, y_mils)
    mirror_origin_x, mirror_origin_y = getattr(placement, "mirror_origin_mils")
    transformed_x = 2.0 * mirror_origin_x - x_mils if getattr(placement, "mirror_x") else x_mils
    transformed_y = 2.0 * mirror_origin_y - y_mils if getattr(placement, "mirror_y") else y_mils
    offset_x, offset_y = getattr(placement, "offset_mils")
    return (transformed_x + offset_x, transformed_y + offset_y)


def _board_outline_segment_operations(
    *,
    output_dir: str,
    board_filename: str,
    board_key: str,
    outline: Mapping[str, object],
    layer: str,
    width_mils: float,
) -> list[JsonObject]:
    vertices = _outline_vertices(outline)
    if len(vertices) < 2:
        return []
    operations: list[JsonObject] = []
    for index, start in enumerate(vertices):
        end = vertices[(index + 1) % len(vertices)]
        if str(start.get("segment", "line") or "line").lower() == "arc":
            operation = _board_outline_arc_operation(
                output_dir=output_dir,
                board_filename=board_filename,
                board_key=board_key,
                index=index + 1,
                start=start,
                layer=layer,
                width_mils=width_mils,
            )
        else:
            operation = _board_outline_track_operation(
                output_dir=output_dir,
                board_filename=board_filename,
                board_key=board_key,
                index=index + 1,
                start=start,
                end=end,
                layer=layer,
                width_mils=width_mils,
            )
        if operation is not None:
            operations.append(operation)
    return operations


def _board_outline_track_operation(
    *,
    output_dir: str,
    board_filename: str,
    board_key: str,
    index: int,
    start: Mapping[str, object],
    end: Mapping[str, object],
    layer: str,
    width_mils: float,
) -> JsonObject:
    return {
        "id": f"project_{_safe_id(board_key)}_outline_segment_{index}",
        "op": "pcbdoc.add-track",
        "message": f"Project {board_key} board outline segment {index}",
        "args": {
            "file": (Path(output_dir) / board_filename).as_posix(),
            "overwrite": True,
            "start_mils": _outline_point(start),
            "end_mils": _outline_point(end),
            "width_mils": width_mils,
            "layer": layer,
        },
    }


def _board_outline_arc_operation(
    *,
    output_dir: str,
    board_filename: str,
    board_key: str,
    index: int,
    start: Mapping[str, object],
    layer: str,
    width_mils: float,
) -> JsonObject | None:
    center = start.get("center_mils")
    if not isinstance(center, list | tuple) or len(center) != 2:
        return None
    center_payload = {"x": center[0], "y": center[1]}
    return {
        "id": f"project_{_safe_id(board_key)}_outline_arc_{index}",
        "op": "pcbdoc.add-arc",
        "message": f"Project {board_key} board outline arc {index}",
        "args": {
            "file": (Path(output_dir) / board_filename).as_posix(),
            "overwrite": True,
            "center_mils": [
                _mapping_number(center_payload, "x", 0.0),
                _mapping_number(center_payload, "y", 0.0),
            ],
            "radius_mils": _mapping_number(start, "radius_mils", 0.0),
            "start_angle_degrees": _mapping_number(
                start,
                "start_angle_degrees",
                0.0,
            ),
            "end_angle_degrees": _mapping_number(
                start,
                "end_angle_degrees",
                0.0,
            ),
            "width_mils": width_mils,
            "layer": layer,
        },
    }


def _board_cutout_region_operation(
    *,
    output_dir: str,
    board_filename: str,
    board_key: str,
    cutout_index: int,
    outline: Mapping[str, object],
    layer: str,
) -> JsonObject | None:
    points = _linearized_outline_points(outline)
    if len(points) < 3:
        return None
    return {
        "id": f"project_{_safe_id(board_key)}_cutout_{cutout_index}_region",
        "op": "pcbdoc.add-region",
        "message": f"Project {board_key} board cutout {cutout_index}",
        "args": {
            "file": (Path(output_dir) / board_filename).as_posix(),
            "overwrite": True,
            "outline_points_mils": points,
            "layer": layer,
            "is_board_cutout": True,
        },
    }


def _outline_vertices(outline: Mapping[str, object]) -> list[JsonObject]:
    value = outline.get("vertices", [])
    if not isinstance(value, list):
        raise ValueError("Mate board_outline.vertices must be an array")
    return [dict(item) for item in value if isinstance(item, dict)]


def _outline_cutouts(outline: Mapping[str, object]) -> list[JsonObject]:
    value = outline.get("cutouts", [])
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("Mate board_outline.cutouts must be an array")
    cutouts: list[JsonObject] = []
    for item in value:
        if isinstance(item, dict):
            vertices = _outline_vertices(item)
        elif isinstance(item, list):
            vertices = [dict(vertex) for vertex in item if isinstance(vertex, dict)]
        else:
            continue
        if len(vertices) >= 3:
            cutouts.append({"vertices": vertices, "closed": True})
    return cutouts


def _outline_point(vertex: Mapping[str, object]) -> list[float]:
    return [
        _mapping_number(vertex, "x_mils", 0.0),
        _mapping_number(vertex, "y_mils", 0.0),
    ]


def _linearized_outline_points(outline: Mapping[str, object]) -> list[list[float]]:
    vertices = _outline_vertices(outline)
    if len(vertices) < 3:
        return []
    points: list[list[float]] = []
    for index, current in enumerate(vertices):
        current_point = _outline_point(current)
        if not points or points[-1] != current_point:
            points.append(current_point)
        next_vertex = vertices[(index + 1) % len(vertices)]
        if str(current.get("segment", "line") or "line").lower() == "arc":
            points.extend(_sample_outline_arc_points(current, next_vertex)[1:])
    if len(points) > 1 and points[0] == points[-1]:
        points.pop()
    return points


def _sample_outline_arc_points(
    current: Mapping[str, object],
    next_vertex: Mapping[str, object],
) -> list[list[float]]:
    center = current.get("center_mils")
    if not isinstance(center, list | tuple) or len(center) != 2:
        return [_outline_point(current), _outline_point(next_vertex)]
    radius = _mapping_number(current, "radius_mils", 0.0)
    if radius <= 0.0:
        return [_outline_point(current), _outline_point(next_vertex)]
    center_x = _number_from_value(center[0], "center_mils.x")
    center_y = _number_from_value(center[1], "center_mils.y")
    start_angle = math.degrees(
        math.atan2(
            _mapping_number(current, "y_mils", 0.0) - center_y,
            _mapping_number(current, "x_mils", 0.0) - center_x,
        )
    ) % 360.0
    end_angle = math.degrees(
        math.atan2(
            _mapping_number(next_vertex, "y_mils", 0.0) - center_y,
            _mapping_number(next_vertex, "x_mils", 0.0) - center_x,
        )
    ) % 360.0
    clockwise, sweep = _outline_arc_direction(current, next_vertex)
    segments = max(2, int(math.ceil(abs(sweep) / 15.0)))
    points: list[list[float]] = []
    for step in range(segments + 1):
        fraction = step / segments
        angle = (
            start_angle - sweep * fraction
            if clockwise
            else start_angle + sweep * fraction
        )
        if step == segments:
            angle = end_angle
        radians = math.radians(angle)
        points.append(
            [
                center_x + radius * math.cos(radians),
                center_y + radius * math.sin(radians),
            ]
        )
    return points


def _outline_arc_direction(
    current: Mapping[str, object],
    next_vertex: Mapping[str, object],
) -> tuple[bool, float]:
    center = current.get("center_mils")
    if not isinstance(center, list | tuple) or len(center) != 2:
        return (False, 0.0)
    center_x = _number_from_value(center[0], "center_mils.x")
    center_y = _number_from_value(center[1], "center_mils.y")
    current_angle = math.degrees(
        math.atan2(
            _mapping_number(current, "y_mils", 0.0) - center_y,
            _mapping_number(current, "x_mils", 0.0) - center_x,
        )
    ) % 360.0
    next_angle = math.degrees(
        math.atan2(
            _mapping_number(next_vertex, "y_mils", 0.0) - center_y,
            _mapping_number(next_vertex, "x_mils", 0.0) - center_x,
        )
    ) % 360.0
    start_angle = _mapping_number(current, "start_angle_degrees", current_angle)
    end_angle = _mapping_number(current, "end_angle_degrees", next_angle)
    span = (end_angle - start_angle) % 360.0
    if span == 0.0:
        span = 360.0
    if _angle_close(current_angle, start_angle) and _angle_close(
        next_angle,
        end_angle,
    ):
        return (False, span)
    if _angle_close(current_angle, end_angle) and _angle_close(next_angle, start_angle):
        return (True, span)
    clockwise_sweep = (current_angle - next_angle) % 360.0
    counterclockwise_sweep = (next_angle - current_angle) % 360.0
    if clockwise_sweep <= counterclockwise_sweep:
        return (True, clockwise_sweep)
    return (False, counterclockwise_sweep)


def _angle_close(left: float, right: float, *, tolerance: float = 1.0) -> bool:
    return min((left - right) % 360.0, (right - left) % 360.0) <= tolerance


def _board_outline_vertex(vertex: object) -> JsonObject:
    payload: JsonObject = {
        "x_mils": _float_attr(vertex, "x_mils"),
        "y_mils": _float_attr(vertex, "y_mils"),
        "segment": "arc" if bool(getattr(vertex, "is_arc", False)) else "line",
    }
    if payload["segment"] == "arc":
        payload.update(
            {
                "center_mils": [
                    _float_attr(vertex, "center_x_mils"),
                    _float_attr(vertex, "center_y_mils"),
                ],
                "radius_mils": _float_attr(vertex, "radius_mils"),
                "start_angle_degrees": float(
                    getattr(vertex, "start_angle_deg", 0.0) or 0.0
                ),
                "end_angle_degrees": float(
                    getattr(vertex, "end_angle_deg", 0.0) or 0.0
                ),
            }
        )
    return payload


def _pad_outline_operations(
    *,
    output_dir: str,
    board_filename: str,
    designator: str,
    pad_index: int,
    geometry: Mapping[str, object],
    layer: str,
    width_mils: float,
    clearance_mils: float,
    outline_count: int,
    outline_spacing_mils: float,
) -> list[JsonObject]:
    if outline_count <= 0:
        return []
    width = _mapping_number(geometry, "width_mils", 0.0)
    height = _mapping_number(geometry, "height_mils", 0.0)
    if width <= 0.0 or height <= 0.0:
        return []
    operations: list[JsonObject] = []
    for outline_index in range(1, outline_count + 1):
        expansion_mils = _outline_centerline_expansion_mils(
            clearance_mils=clearance_mils,
            stroke_width_mils=width_mils,
            outline_index=outline_index,
            outline_spacing_mils=outline_spacing_mils,
        )
        operations.extend(
            _pad_single_outline_operations(
                output_dir=output_dir,
                board_filename=board_filename,
                designator=designator,
                pad_index=pad_index,
                outline_index=outline_index,
                geometry=geometry,
                layer=layer,
                width_mils=width_mils,
                expansion_mils=expansion_mils,
            )
        )
    return operations


def _outline_centerline_expansion_mils(
    *,
    clearance_mils: float,
    stroke_width_mils: float,
    outline_index: int,
    outline_spacing_mils: float,
) -> float:
    return (
        clearance_mils
        + (stroke_width_mils / 2.0)
        + (float(outline_index - 1) * outline_spacing_mils)
    )


def _pad_single_outline_operations(
    *,
    output_dir: str,
    board_filename: str,
    designator: str,
    pad_index: int,
    outline_index: int,
    geometry: Mapping[str, object],
    layer: str,
    width_mils: float,
    expansion_mils: float,
) -> list[JsonObject]:
    shape = int(_mapping_number(geometry, "shape", float(_PAD_SHAPE_CIRCLE)))
    if shape == _PAD_SHAPE_CIRCLE:
        return _pad_circular_outline_operations(
            output_dir=output_dir,
            board_filename=board_filename,
            designator=designator,
            pad_index=pad_index,
            outline_index=outline_index,
            geometry=geometry,
            layer=layer,
            width_mils=width_mils,
            expansion_mils=expansion_mils,
        )
    if shape == _PAD_SHAPE_OCTAGONAL:
        return _pad_polygon_outline_operations(
            output_dir=output_dir,
            board_filename=board_filename,
            designator=designator,
            pad_index=pad_index,
            outline_index=outline_index,
            points=_pad_octagon_points(geometry, expansion_mils),
            layer=layer,
            width_mils=width_mils,
        )
    return _pad_polygon_outline_operations(
        output_dir=output_dir,
        board_filename=board_filename,
        designator=designator,
        pad_index=pad_index,
        outline_index=outline_index,
        points=_pad_rectangle_points(geometry, expansion_mils),
        layer=layer,
        width_mils=width_mils,
    )


def _pad_circular_outline_operations(
    *,
    output_dir: str,
    board_filename: str,
    designator: str,
    pad_index: int,
    outline_index: int,
    geometry: Mapping[str, object],
    layer: str,
    width_mils: float,
    expansion_mils: float,
) -> list[JsonObject]:
    width = _mapping_number(geometry, "width_mils", 0.0)
    height = _mapping_number(geometry, "height_mils", 0.0)
    if math.isclose(width, height, rel_tol=1e-9, abs_tol=1e-9):
        return [
            _pad_ring_operation(
                output_dir=output_dir,
                board_filename=board_filename,
                designator=designator,
                pad_index=pad_index,
                ring_index=outline_index,
                geometry=geometry,
                radius_mils=(width / 2.0) + expansion_mils,
                layer=layer,
                width_mils=width_mils,
            )
        ]
    return _pad_polygon_outline_operations(
        output_dir=output_dir,
        board_filename=board_filename,
        designator=designator,
        pad_index=pad_index,
        outline_index=outline_index,
        points=_pad_ellipse_points(geometry, expansion_mils),
        layer=layer,
        width_mils=width_mils,
    )


def _pad_polygon_outline_operations(
    *,
    output_dir: str,
    board_filename: str,
    designator: str,
    pad_index: int,
    outline_index: int,
    points: list[tuple[float, float]],
    layer: str,
    width_mils: float,
) -> list[JsonObject]:
    if len(points) < 2:
        return []
    operations: list[JsonObject] = []
    for segment_index, start in enumerate(points, start=1):
        end = points[segment_index % len(points)]
        operations.append(
            _pad_outline_track_operation(
                output_dir=output_dir,
                board_filename=board_filename,
                designator=designator,
                pad_index=pad_index,
                outline_index=outline_index,
                segment_index=segment_index,
                start=start,
                end=end,
                layer=layer,
                width_mils=width_mils,
            )
        )
    return operations


def _pad_rectangle_points(
    geometry: Mapping[str, object],
    expansion_mils: float,
) -> list[tuple[float, float]]:
    cx = _mapping_number(geometry, "x_mils", 0.0)
    cy = _mapping_number(geometry, "y_mils", 0.0)
    half_w = (_mapping_number(geometry, "width_mils", 0.0) / 2.0) + expansion_mils
    half_h = (_mapping_number(geometry, "height_mils", 0.0) / 2.0) + expansion_mils
    points = [
        (cx - half_w, cy - half_h),
        (cx + half_w, cy - half_h),
        (cx + half_w, cy + half_h),
        (cx - half_w, cy + half_h),
    ]
    return _rotate_points(points, (cx, cy), _mapping_number(geometry, "rotation_degrees", 0.0))


def _pad_octagon_points(
    geometry: Mapping[str, object],
    expansion_mils: float,
) -> list[tuple[float, float]]:
    cx = _mapping_number(geometry, "x_mils", 0.0)
    cy = _mapping_number(geometry, "y_mils", 0.0)
    half_w = (_mapping_number(geometry, "width_mils", 0.0) / 2.0) + expansion_mils
    half_h = (_mapping_number(geometry, "height_mils", 0.0) / 2.0) + expansion_mils
    chamfer = min(half_w, half_h) / 2.0
    points = [
        (cx + half_w, cy - (half_h - chamfer)),
        (cx + half_w, cy + half_h - chamfer),
        (cx + half_w - chamfer, cy + half_h),
        (cx - (half_w - chamfer), cy + half_h),
        (cx - half_w, cy + half_h - chamfer),
        (cx - half_w, cy - (half_h - chamfer)),
        (cx - (half_w - chamfer), cy - half_h),
        (cx + half_w - chamfer, cy - half_h),
    ]
    return _rotate_points(points, (cx, cy), _mapping_number(geometry, "rotation_degrees", 0.0))


def _pad_ellipse_points(
    geometry: Mapping[str, object],
    expansion_mils: float,
) -> list[tuple[float, float]]:
    cx = _mapping_number(geometry, "x_mils", 0.0)
    cy = _mapping_number(geometry, "y_mils", 0.0)
    radius_x = (_mapping_number(geometry, "width_mils", 0.0) / 2.0) + expansion_mils
    radius_y = (_mapping_number(geometry, "height_mils", 0.0) / 2.0) + expansion_mils
    points = [
        (
            cx + (math.cos((2.0 * math.pi * index) / 32.0) * radius_x),
            cy + (math.sin((2.0 * math.pi * index) / 32.0) * radius_y),
        )
        for index in range(32)
    ]
    return _rotate_points(points, (cx, cy), _mapping_number(geometry, "rotation_degrees", 0.0))


def _rotate_points(
    points: list[tuple[float, float]],
    center: tuple[float, float],
    rotation_degrees: float,
) -> list[tuple[float, float]]:
    if math.isclose(rotation_degrees, 0.0, abs_tol=1e-9):
        return points
    angle = math.radians(rotation_degrees)
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    cx, cy = center
    rotated: list[tuple[float, float]] = []
    for x, y in points:
        dx = x - cx
        dy = y - cy
        rotated.append(
            (
                cx + (dx * cos_angle) - (dy * sin_angle),
                cy + (dx * sin_angle) + (dy * cos_angle),
            )
        )
    return rotated


def _pad_outline_track_operation(
    *,
    output_dir: str,
    board_filename: str,
    designator: str,
    pad_index: int,
    outline_index: int,
    segment_index: int,
    start: tuple[float, float],
    end: tuple[float, float],
    layer: str,
    width_mils: float,
) -> JsonObject:
    return {
        "id": (
            f"reference_{_safe_id(designator)}_pad_{pad_index}"
            f"_outline_{outline_index}_segment_{segment_index}"
        ),
        "op": "pcbdoc.add-track",
        "message": f"Add mate reference outline for {designator}",
        "args": {
            "file": (Path(output_dir) / board_filename).as_posix(),
            "overwrite": True,
            "start_mils": [start[0], start[1]],
            "end_mils": [end[0], end[1]],
            "width_mils": width_mils,
            "layer": layer,
        },
    }


def _pad_ring_operation(
    *,
    output_dir: str,
    board_filename: str,
    designator: str,
    pad_index: int,
    ring_index: int,
    geometry: Mapping[str, object],
    radius_mils: float,
    layer: str,
    width_mils: float,
) -> JsonObject:
    return {
        "id": f"reference_{_safe_id(designator)}_pad_{pad_index}_ring_{ring_index}",
        "op": "pcbdoc.add-arc",
        "message": f"Add mate reference outline for {designator}",
        "args": {
            "file": (Path(output_dir) / board_filename).as_posix(),
            "overwrite": True,
            "center_mils": [
                _mapping_number(geometry, "x_mils", 0.0),
                _mapping_number(geometry, "y_mils", 0.0),
            ],
            "radius_mils": radius_mils,
            "start_angle_degrees": 0.0,
            "end_angle_degrees": 360.0,
            "width_mils": width_mils,
            "layer": layer,
        },
    }


def _target_source_pad_geometries(
    target: Mapping[str, object],
) -> list[JsonObject]:
    value = target.get("source_pad_geometries", [])
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, dict)]


def _list_field(payload: Mapping[str, object], name: str) -> list[object]:
    value = payload.get(name, [])
    return list(value) if isinstance(value, list) else []


def _section(root: Mapping[str, object], name: str) -> JsonObject:
    value = root.get(name, {})
    if not isinstance(value, dict):
        raise ValueError(f"Mate graphics field {name!r} must be an object")
    return dict(value)


def _optional_string(
    args: Mapping[str, object],
    name: str,
    default: str | None,
) -> str | None:
    value = args.get(name)
    if value is None:
        return default
    if not isinstance(value, str):
        raise ValueError(f"Field {name!r} must be a string")
    return value


def _optional_bool(args: Mapping[str, object], name: str, default: bool) -> bool:
    value = args.get(name)
    if value is None:
        return default
    if not isinstance(value, bool):
        raise ValueError(f"Field {name!r} must be a boolean")
    return value


def _mapping_number(args: Mapping[str, object], name: str, default: float) -> float:
    value = args.get(name, default)
    return _number_from_value(value, name)


def _number_from_value(value: object, name: str) -> float:
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise ValueError(f"Field {name!r} must be numeric")
    return float(value)


def _float_attr(obj: object, name: str) -> float:
    value = getattr(obj, name, 0.0)
    return 0.0 if value is None else float(value)


def _int_attr(obj: object, name: str) -> int:
    value = getattr(obj, name, 0)
    return 0 if value is None else int(value)


def _safe_id(value: str) -> str:
    result = "".join(char.lower() if char.isalnum() else "_" for char in value)
    return result.strip("_") or "target"
