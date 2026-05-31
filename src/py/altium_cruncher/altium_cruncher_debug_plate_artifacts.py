"""Debug-plate artifact MCO generation helpers."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from altium_cruncher.altium_cruncher_mco import JsonObject

_PCB_LAYER_STEP_OPTION_KEYS = (
    "thickness_mm",
    "z_mm",
    "copper_color",
    "outline_width_mm",
    "outline_color",
    "include_copper",
    "include_board_outline",
    "include_poured_polygons",
    "cut_holes",
    "fuse_copper",
    "fuse_board_outline",
    "arc_segments",
)


def build_debug_plate_artifact_operations(config: object) -> list[JsonObject]:
    """Build artifact MCO operations requested by a debug-plate config."""
    artifacts = getattr(config, "artifacts", {})
    if not isinstance(artifacts, dict):
        raise ValueError("Debug-plate artifacts must be an object")
    layer_step = artifacts.get("pcb_layer_step")
    if not isinstance(layer_step, dict) or not _optional_bool(
        layer_step,
        "enabled",
        False,
    ):
        return []
    selection = getattr(config, "selection")
    output = getattr(config, "output")
    return [
        _pcb_layer_step_operation(
            board=board,
            output_dir=str(getattr(output, "output_dir")),
            layer_step=layer_step,
        )
        for board in getattr(selection, "boards", ())
        if str(getattr(board, "pcb_path", "") or "")
    ]


def _pcb_layer_step_operation(
    *,
    board: object,
    output_dir: str,
    layer_step: Mapping[str, object],
) -> JsonObject:
    source_layer = _optional_string(layer_step, "source_layer", "bottom") or "bottom"
    board_key = str(getattr(board, "board_key", "") or Path(getattr(board, "pcb_path")).stem)
    output_file = (
        Path(output_dir)
        / "artifacts"
        / "pcb-layer-step"
        / f"{_safe_id(board_key)}__{_safe_id(source_layer)}.step"
    )
    args: JsonObject = {
        "file": str(getattr(board, "pcb_path")),
        "output_file": output_file.as_posix(),
        "overwrite": True,
        "layer": source_layer,
        "board_name": board_key,
        "highlights": _pcb_layer_step_highlights(board, layer_step),
    }
    for option_key in _PCB_LAYER_STEP_OPTION_KEYS:
        if option_key in layer_step:
            args[option_key] = layer_step[option_key]
    return {
        "id": f"export_{_safe_id(board_key)}_{_safe_id(source_layer)}_pcb_layer_step",
        "op": "pcbdoc.export-layer-step",
        "message": f"Export {board_key} {source_layer} PCB layer STEP artifact",
        "args": args,
    }


def _pcb_layer_step_highlights(
    board: object,
    layer_step: Mapping[str, object],
) -> list[JsonObject]:
    specs = _highlight_specs(layer_step)
    result: list[JsonObject] = []
    for spec in specs:
        projection_id = _required_string(spec, "projection")
        geometries = _source_pad_geometries_for_projection(board, projection_id)
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


def _highlight_specs(layer_step: Mapping[str, object]) -> list[JsonObject]:
    value = layer_step.get("highlights", [])
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("Debug-plate pcb_layer_step.highlights must be an array")
    result: list[JsonObject] = []
    for item in value:
        if not isinstance(item, dict):
            raise ValueError(
                "Debug-plate pcb_layer_step.highlights items must be objects"
            )
        result.append(dict(item))
    return result


def _source_pad_geometries_for_projection(
    board: object,
    projection_id: str,
) -> list[JsonObject]:
    geometries: list[JsonObject] = []
    for item in [
        *list(getattr(board, "components", ()) or ()),
        *list(getattr(board, "free_pads", ()) or ()),
    ]:
        if getattr(item, "mate_projection_id", None) != projection_id:
            continue
        geometries.extend(
            dict(geometry)
            for geometry in getattr(item, "source_pad_geometries", ()) or ()
            if isinstance(geometry, dict)
        )
    return geometries


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


def _add_optional(payload: JsonObject, name: str, value: object | None) -> None:
    if value is not None:
        payload[name] = value


def _safe_id(value: str) -> str:
    result = "".join(char.lower() if char.isalnum() else "_" for char in value)
    return result.strip("_") or "artifact"
