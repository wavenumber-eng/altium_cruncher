"""Mate artifact MCO generation helpers."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from pathlib import Path

from altium_cruncher.bom_pnp_model import designator_sort_key
from altium_cruncher.altium_cruncher_mco import JsonObject

_PCB_LAYER_STEP_OPTION_KEYS = (
    "thickness_mm",
    "z_mm",
    "copper_color",
    "track_color",
    "track_body",
    "polygon_color",
    "polygon_body",
    "outline_width_mm",
    "outline_color",
    "board_cutout_color",
    "include_copper",
    "include_board_outline",
    "include_board_cutouts",
    "include_poured_polygons",
    "cut_holes",
    "drill_hole_mode",
    "max_boolean_drill_cuts",
    "drill_hole_color",
    "drill_plated_hole_color",
    "drill_non_plated_hole_color",
    "drill_overlay_thickness_mm",
    "drill_minimum_diameter_mm",
    "drill_hole_shape",
    "drill_ring_width_mm",
    "drill_plated_ring_shape",
    "fuse_copper",
    "fuse_board_outline",
    "arc_segments",
    "include_tracks",
    "include_arcs",
    "include_fills",
    "include_regions",
    "include_vias",
    "include_component_pads",
    "include_free_pads",
    "include_designators",
    "features",
    "colors",
    "drills",
    "board_outline",
)

_PCB_LAYER_STEP_CACHE_VERSION = "mate-pcb-layer-step-2026-06-07-a"


def build_mate_artifact_operations(config: object) -> list[JsonObject]:
    """Build artifact MCO operations requested by a mate config."""
    artifacts = getattr(config, "artifacts", {})
    if not isinstance(artifacts, dict):
        raise ValueError("Mate artifacts must be an object")
    layer_step = artifacts.get("pcb_layer_step")
    if not isinstance(layer_step, dict) or not _optional_bool(
        layer_step,
        "enabled",
        False,
    ):
        return []
    selection = getattr(config, "selection")
    output = getattr(config, "output")
    operations: list[JsonObject] = []
    for board in getattr(selection, "boards", ()):
        if not str(getattr(board, "pcb_path", "") or ""):
            continue
        step_operation = _pcb_layer_step_operation(
            board=board,
            output_dir=str(getattr(output, "output_dir")),
            layer_step=layer_step,
        )
        operations.append(step_operation)
        insert_operation = _pcb_layer_step_insert_operation(
            board=board,
            output_dir=str(getattr(output, "output_dir")),
            output_board_filename=_output_board_filename(output),
            output_board_outline_mils=getattr(output, "board_outline_mils", None),
            source_board_outline_mils=getattr(board, "board_outline_mils", None),
            output_board_origin_mils=getattr(output, "board_origin_mils", None),
            step_operation=step_operation,
            layer_step=layer_step,
        )
        if insert_operation is not None:
            operations.append(insert_operation)
    return operations


def _pcb_layer_step_operation(
    *,
    board: object,
    output_dir: str,
    layer_step: Mapping[str, object],
) -> JsonObject:
    source_layer = _optional_string(layer_step, "source_layer", "bottom") or "bottom"
    board_key = str(
        getattr(board, "board_key", "") or Path(getattr(board, "pcb_path")).stem
    )
    args: JsonObject = {
        "file": str(getattr(board, "pcb_path")),
        "overwrite": True,
        "layer": source_layer,
        "board_name": board_key,
        "z_mm": _optional_float(
            layer_step,
            "z_mm",
            _centered_copper_z_mm(layer_step),
        ),
        "highlights": _pcb_layer_step_highlights(board, layer_step),
    }
    for option_key in _PCB_LAYER_STEP_OPTION_KEYS:
        if option_key in layer_step:
            args[option_key] = layer_step[option_key]
    colors = _pcb_layer_step_colors(board, layer_step)
    if colors:
        args["colors"] = colors
    artifact_hash = _pcb_layer_step_artifact_hash(
        board=board,
        board_key=board_key,
        source_layer=source_layer,
        args=args,
    )
    output_file = (
        Path(output_dir)
        / "artifacts"
        / "pcb-layer-step"
        / f"{_safe_id(board_key)}__{_safe_id(source_layer)}__{artifact_hash}.step"
    )
    args["output_file"] = output_file.as_posix()
    return {
        "id": f"export_{_safe_id(board_key)}_{_safe_id(source_layer)}_pcb_layer_step",
        "op": "pcbdoc.export-layer-step",
        "message": f"Export {board_key} {source_layer} PCB layer STEP artifact",
        "args": args,
    }


def _pcb_layer_step_artifact_hash(
    *,
    board: object,
    board_key: str,
    source_layer: str,
    args: Mapping[str, object],
) -> str:
    source_path = Path(str(getattr(board, "pcb_path", "") or ""))
    fingerprint: JsonObject = {
        "name": source_path.name,
    }
    try:
        stat = source_path.stat()
    except OSError:
        fingerprint["path"] = str(source_path)
    else:
        fingerprint["size"] = int(stat.st_size)
        fingerprint["mtime_ns"] = int(stat.st_mtime_ns)
    hash_args = dict(args)
    if "file" in hash_args:
        hash_args["file"] = source_path.name
    payload = {
        "version": _PCB_LAYER_STEP_CACHE_VERSION,
        "board_key": board_key,
        "source_layer": source_layer,
        "source": fingerprint,
        "args": hash_args,
    }
    data = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")
    return hashlib.sha1(data).hexdigest()[:10]


def _pcb_layer_step_insert_operation(
    *,
    board: object,
    output_dir: str,
    output_board_filename: str,
    output_board_outline_mils: object,
    source_board_outline_mils: object,
    output_board_origin_mils: object,
    step_operation: Mapping[str, object],
    layer_step: Mapping[str, object],
) -> JsonObject | None:
    insert = layer_step.get("insert_in_output")
    if insert is True:
        insert_config: JsonObject = {"enabled": True}
    elif isinstance(insert, dict):
        insert_config = dict(insert)
    else:
        return None
    if not _optional_bool(insert_config, "enabled", False):
        return None

    args = step_operation.get("args", {})
    if not isinstance(args, dict):
        raise ValueError("Internal pcb_layer_step operation args must be an object")
    step_file = str(args.get("output_file", "") or "")
    if not step_file:
        raise ValueError("Internal pcb_layer_step operation missing output_file")

    board_key = str(
        getattr(board, "board_key", "") or Path(getattr(board, "pcb_path")).stem
    )
    model_args: JsonObject = {
        "file": (Path(output_dir) / output_board_filename).as_posix(),
        "overwrite": True,
        "model_file": step_file,
        "model_name": Path(step_file).name,
        "name": _optional_string(
            insert_config,
            "name",
            f"{board_key} layer STEP",
        ),
        "layer": _optional_string(insert_config, "layer", "MECHANICAL_13"),
        "side": _optional_string(insert_config, "side", "TOP"),
        "location_mils": _optional_number_pair(
            insert_config,
            "location_mils",
            default=_origin_location_mils(output_board_origin_mils),
        ),
        "z_mm": _optional_float(insert_config, "z_mm", 0.0),
    }
    _add_optional(
        model_args, "rotation_z_degrees", insert_config.get("rotation_z_degrees")
    )
    _add_optional(model_args, "opacity", insert_config.get("opacity"))
    default_bounds = source_board_outline_mils or output_board_outline_mils
    bounds = insert_config.get("bounds_mils", default_bounds)
    _add_optional(model_args, "bounds_mils", bounds)
    return {
        "id": f"insert_{_safe_id(board_key)}_pcb_layer_step",
        "op": "pcbdoc.add-embedded-3d-model",
        "message": f"Insert {board_key} PCB layer STEP into mate board",
        "args": model_args,
    }


def _pcb_layer_step_highlights(
    board: object,
    layer_step: Mapping[str, object],
) -> list[JsonObject]:
    specs = _highlight_specs(layer_step)
    result: list[JsonObject] = []
    for spec in specs:
        projection_id = _required_string(spec, "projection")
        geometries = _source_pad_geometries_for_projection(
            board,
            projection_id,
            include_components=False,
            include_free_pads=True,
        )
        if not geometries:
            continue
        highlight: JsonObject = {
            "id": projection_id,
            "name": _optional_string(spec, "name", projection_id) or projection_id,
            "color": _optional_string(spec, "color", "#ffcc00") or "#ffcc00",
            "pad_geometries": geometries,
        }
        _add_optional(highlight, "z_offset_mm", spec.get("z_offset_mm"))
        _add_optional(highlight, "thickness_mm", spec.get("thickness_mm"))
        result.append(highlight)
    return result


def _pcb_layer_step_colors(
    board: object,
    layer_step: Mapping[str, object],
) -> JsonObject | None:
    rules: list[JsonObject] = []
    for spec in _highlight_specs(layer_step):
        projection_id = _required_string(spec, "projection")
        designators = _component_designators_for_projection(board, projection_id)
        if not designators:
            continue
        rules.append(
            {
                "designators": designators,
                "color": _optional_string(spec, "color", "#ffcc00") or "#ffcc00",
                "body": projection_id,
            }
        )
    existing = layer_step.get("colors")
    if existing is not None and not isinstance(existing, dict):
        raise ValueError("Mate pcb_layer_step.colors must be an object")
    colors: JsonObject = dict(existing) if isinstance(existing, dict) else {}
    if not rules:
        return colors or None
    existing_rules = colors.get("pad_rules", [])
    if existing_rules is None:
        existing_rules = []
    if not isinstance(existing_rules, list):
        raise ValueError("Mate pcb_layer_step.colors.pad_rules must be an array")
    colors["pad_rules"] = [*existing_rules, *rules]
    return colors


def _highlight_specs(layer_step: Mapping[str, object]) -> list[JsonObject]:
    value = layer_step.get("highlights", [])
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("Mate pcb_layer_step.highlights must be an array")
    result: list[JsonObject] = []
    for item in value:
        if not isinstance(item, dict):
            raise ValueError("Mate pcb_layer_step.highlights items must be objects")
        result.append(dict(item))
    return result


def _source_pad_geometries_for_projection(
    board: object,
    projection_id: str,
    *,
    include_components: bool = True,
    include_free_pads: bool = True,
) -> list[JsonObject]:
    geometries: list[JsonObject] = []
    items = [
        *(list(getattr(board, "components", ()) or ()) if include_components else []),
        *(list(getattr(board, "free_pads", ()) or ()) if include_free_pads else []),
    ]
    for item in items:
        if getattr(item, "mate_projection_id", None) != projection_id:
            continue
        geometries.extend(
            dict(geometry)
            for geometry in getattr(item, "source_pad_geometries", ()) or ()
            if isinstance(geometry, dict)
        )
    return geometries


def _component_designators_for_projection(
    board: object,
    projection_id: str,
) -> list[str]:
    designators: list[str] = []
    for component in getattr(board, "components", ()) or ():
        if getattr(component, "mate_projection_id", None) != projection_id:
            continue
        designator = str(getattr(component, "designator", "") or "").strip()
        if designator:
            designators.append(designator)
    return sorted(set(designators), key=designator_sort_key)


def _required_string(args: Mapping[str, object], name: str) -> str:
    value = args.get(name)
    if not isinstance(value, str) or not value:
        raise ValueError(f"Field {name!r} must be a non-empty string")
    return value


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


def _optional_float(args: Mapping[str, object], name: str, default: float) -> float:
    value = args.get(name)
    if value is None:
        return default
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise ValueError(f"Field {name!r} must be numeric")
    return float(value)


def _optional_number_pair(
    args: Mapping[str, object],
    name: str,
    *,
    default: list[float],
) -> list[float]:
    value = args.get(name)
    if value is None:
        return list(default)
    if not isinstance(value, list | tuple) or len(value) != 2:
        raise ValueError(f"Field {name!r} must be a two-number array")
    result: list[float] = []
    for item in value:
        if not isinstance(item, int | float) or isinstance(item, bool):
            raise ValueError(f"Field {name!r} must be a two-number array")
        result.append(float(item))
    return result


def _add_optional(payload: JsonObject, name: str, value: object | None) -> None:
    if value is not None:
        payload[name] = value


def _output_board_filename(output: object) -> str:
    board_filename = getattr(output, "board_filename", None)
    if board_filename:
        return str(board_filename)
    return f"{getattr(output, 'project_name')}.PcbDoc"


def _origin_location_mils(origin: object) -> list[float]:
    if not isinstance(origin, dict):
        return [0.0, 0.0]
    x_value = origin.get("x", 0.0)
    y_value = origin.get("y", 0.0)
    if not isinstance(x_value, int | float) or isinstance(x_value, bool):
        return [0.0, 0.0]
    if not isinstance(y_value, int | float) or isinstance(y_value, bool):
        return [0.0, 0.0]
    return [float(x_value), float(y_value)]


def _centered_copper_z_mm(layer_step: Mapping[str, object]) -> float:
    return -_optional_float(layer_step, "thickness_mm", 0.035) / 2.0


def _safe_id(value: str) -> str:
    result = "".join(char.lower() if char.isalnum() else "_" for char in value)
    return result.strip("_") or "artifact"
