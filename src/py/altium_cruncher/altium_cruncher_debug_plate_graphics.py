"""Debug-plate PCB reference graphics helpers."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from altium_cruncher.altium_cruncher_mco import JsonObject


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
    width_mils = _mapping_number(style, "stroke_width_mils", 5.0)
    clearance_mils = _mapping_number(style, "clearance_mils", 10.0)
    mode = str(style.get("mode", "single_ring") or "single_ring")

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
                double_ring=mode == "double_ring",
            )
        )
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


def parse_source_pad_geometries(
    raw: Mapping[str, object],
) -> tuple[JsonObject, ...]:
    """Parse stored source-pad geometry from a selection payload."""
    value = raw.get("source_pad_geometries", [])
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ValueError("Debug-plate source_pad_geometries must be an array")
    result: list[JsonObject] = []
    for item in value:
        if not isinstance(item, dict):
            raise ValueError("Debug-plate source_pad_geometries items must be objects")
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
    """Apply a debug-plate placement transform to source-pad geometry."""
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
    double_ring: bool,
) -> list[JsonObject]:
    radius = max(
        _mapping_number(geometry, "width_mils", 0.0),
        _mapping_number(geometry, "height_mils", 0.0),
    ) / 2.0
    if radius <= 0.0:
        return []
    radii = [radius, radius + clearance_mils] if double_ring else [
        radius + clearance_mils
    ]
    return [
        _pad_ring_operation(
            output_dir=output_dir,
            board_filename=board_filename,
            designator=designator,
            pad_index=pad_index,
            ring_index=ring_index,
            geometry=geometry,
            radius_mils=ring_radius,
            layer=layer,
            width_mils=width_mils,
        )
        for ring_index, ring_radius in enumerate(radii, start=1)
    ]


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
        "message": f"Add debug-plate reference outline for {designator}",
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
        raise ValueError(f"Debug-plate graphics field {name!r} must be an object")
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
