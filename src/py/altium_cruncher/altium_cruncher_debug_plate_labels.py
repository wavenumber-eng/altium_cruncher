"""PCB label layout helpers for debug-plate generated boards."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from altium_cruncher.altium_cruncher_mco import JsonObject

_PCB_LABEL_STYLE_PASSTHROUGH_KEYS = (
    "rotation_degrees",
    "stroke_font_type",
    "italic",
    "is_comment",
    "is_designator",
    "is_mirrored",
    "barcode_kind",
    "barcode_render_mode",
    "barcode_full_size_mils",
    "barcode_margin_mils",
    "barcode_min_width_mils",
    "barcode_show_text",
    "barcode_inverted",
)


@dataclass(frozen=True, slots=True)
class DebugPlatePcbLabelsConfig:
    """PCB-side net-label generation settings for projected DUT targets."""

    enabled: bool
    side: str
    offset_mils: tuple[float, float]
    box_size_mils: tuple[float, float] | None
    center_box_on_target: bool
    row_spacing_mils: float | None
    column_spacing_mils: float | None
    auto_width_padding_mils: float | None
    style: JsonObject


@dataclass(frozen=True, slots=True)
class PcbNetLabelRequest:
    labels: DebugPlatePcbLabelsConfig
    target: Mapping[str, object]
    designator: str
    board_label_row: int = 0
    board_label_column: int = 0
    board_label_column_title: str = ""


def pcb_net_label_request(
    labels: DebugPlatePcbLabelsConfig,
    target: Mapping[str, object],
    designator: str,
    *,
    board_label_column_indices: dict[str, int],
    board_label_rows: dict[str, int],
) -> PcbNetLabelRequest | None:
    if not labels.enabled or not _target_optional_string(target, "net_name"):
        return None
    if not is_board_edge_label_side(labels.side):
        return PcbNetLabelRequest(labels, target, designator)

    column_key, column_title = _pcb_label_column_identity(target)
    if column_key not in board_label_column_indices:
        board_label_column_indices[column_key] = len(board_label_column_indices)
    row = board_label_rows.get(column_key, 0)
    board_label_rows[column_key] = row + 1
    return PcbNetLabelRequest(
        labels,
        target,
        designator,
        board_label_row=row,
        board_label_column=board_label_column_indices[column_key],
        board_label_column_title=column_title,
    )


def pcb_net_label_operations(
    *,
    board_file: str,
    board_outline_mils: JsonObject | None,
    requests: list[PcbNetLabelRequest],
) -> list[JsonObject]:
    edge_width = _uniform_board_edge_label_width_mils(requests)
    operations: list[JsonObject] = []
    emitted_headers: set[int] = set()
    for request in requests:
        width = edge_width if is_board_edge_label_side(request.labels.side) else None
        if width is not None and request.board_label_column not in emitted_headers:
            operations.append(
                _pcb_label_column_header_operation(
                    board_file,
                    board_outline_mils,
                    request,
                    width,
                )
            )
            emitted_headers.add(request.board_label_column)
        operations.append(
            _pcb_net_label_operation(
                board_file,
                board_outline_mils,
                request,
                board_label_width_mils=width,
            )
        )
    return operations


def is_board_edge_label_side(side: str) -> bool:
    return side in {"board_left", "board_right"}


def _pcb_label_column_identity(target: Mapping[str, object]) -> tuple[str, str]:
    projection_id = _target_optional_string(target, "mate_projection_id")
    if projection_id:
        return (f"projection:{projection_id}", projection_id)
    kind = _target_optional_string(target, "kind")
    if kind:
        return (f"kind:{kind}", kind)
    return ("default", "labels")


def _uniform_board_edge_label_width_mils(
    requests: list[PcbNetLabelRequest],
) -> float | None:
    widths = [
        _pcb_label_required_width_mils(
            request.labels,
            _target_optional_string(request.target, "net_name") or "",
        )
        for request in requests
        if is_board_edge_label_side(request.labels.side)
    ]
    return max(widths) if widths else None


def _pcb_label_required_width_mils(
    labels: DebugPlatePcbLabelsConfig,
    text: str,
) -> float:
    configured_width = labels.box_size_mils[0] if labels.box_size_mils else 0.0
    height_mils = _style_float(dict(labels.style), "height_mils", 65.0)
    padding_mils = labels.auto_width_padding_mils
    if padding_mils is None:
        padding_mils = 80.0
    return max(configured_width, (len(text) * height_mils * 0.6) + padding_mils)


def _pcb_net_label_operation(
    board_file: str,
    board_outline_mils: JsonObject | None,
    request: PcbNetLabelRequest,
    *,
    board_label_width_mils: float | None,
) -> JsonObject:
    net_name = _target_optional_string(request.target, "net_name")
    if not net_name:
        raise ValueError("Debug-plate PCB net label target must have a net name")
    return {
        "id": f"label_{_safe_id(request.designator)}_pcb_net",
        "op": "pcbdoc.add-text",
        "message": f"Add debug-plate PCB net label for {request.designator}",
        "args": {
            "file": board_file,
            "overwrite": True,
            "text": net_name,
            "position_mils": list(
                _pcb_net_label_position(
                    board_outline_mils,
                    request,
                    board_label_width_mils=board_label_width_mils,
                )
            ),
            **_pcb_net_label_style_args(
                request.labels,
                box_size_mils=_pcb_label_box_size(
                    request.labels,
                    board_label_width_mils,
                ),
            ),
        },
    }


def _pcb_label_column_header_operation(
    board_file: str,
    board_outline_mils: JsonObject | None,
    request: PcbNetLabelRequest,
    width_mils: float,
) -> JsonObject:
    labels = request.labels
    return {
        "id": f"label_column_{_safe_id(request.board_label_column_title)}_header",
        "op": "pcbdoc.add-text",
        "message": f"Add debug-plate PCB label column header {request.board_label_column_title}",
        "args": {
            "file": board_file,
            "overwrite": True,
            "text": request.board_label_column_title,
            "position_mils": list(
                _pcb_board_edge_label_position(
                    board_outline_mils,
                    labels,
                    row=0,
                    board_label_column=request.board_label_column,
                    board_label_width_mils=width_mils,
                    header=True,
                )
            ),
            **_pcb_label_header_style_args(labels),
        },
    }


def _pcb_net_label_position(
    board_outline_mils: JsonObject | None,
    request: PcbNetLabelRequest,
    *,
    board_label_width_mils: float | None,
) -> tuple[float, float]:
    labels = request.labels
    if is_board_edge_label_side(labels.side):
        return _pcb_board_edge_label_position(
            board_outline_mils,
            labels,
            row=request.board_label_row,
            board_label_column=request.board_label_column,
            board_label_width_mils=board_label_width_mils,
        )
    x_mils = _target_float(request.target, "x_mils")
    y_mils = _target_float(request.target, "y_mils")
    offset_x, offset_y = labels.offset_mils
    box_width = labels.box_size_mils[0] if labels.box_size_mils is not None else 0.0
    x_mils = x_mils - offset_x - box_width if labels.side == "left" else x_mils + offset_x
    y_mils = y_mils + offset_y
    if labels.center_box_on_target and labels.box_size_mils is not None:
        y_mils -= labels.box_size_mils[1] / 2.0
    return (x_mils, y_mils)


def _pcb_board_edge_label_position(
    board_outline_mils: JsonObject | None,
    labels: DebugPlatePcbLabelsConfig,
    row: int,
    *,
    board_label_column: int,
    board_label_width_mils: float | None,
    header: bool = False,
) -> tuple[float, float]:
    outline = board_outline_mils
    if not isinstance(outline, dict):
        raise ValueError(
            "Debug-plate board-edge PCB labels require output board_outline_mils"
        )
    offset_x, offset_y = labels.offset_mils
    box_size = _pcb_label_box_size(labels, board_label_width_mils)
    box_width = box_size[0] if box_size is not None else 0.0
    box_height = box_size[1] if box_size is not None else 70.0
    column_spacing = labels.column_spacing_mils
    if column_spacing is None:
        column_spacing = 80.0
    left = _target_float(outline, "left")
    right = _target_float(outline, "right")
    top = _target_float(outline, "top")
    column_delta = float(board_label_column) * (box_width + column_spacing)
    x_mils = left + offset_x + column_delta
    if labels.side == "board_right":
        x_mils = right - offset_x - box_width - column_delta
    y_mils = top - offset_y - box_height - (float(row) * _row_spacing(labels, box_height))
    return (x_mils, y_mils + box_height + 10.0) if header else (x_mils, y_mils)


def _row_spacing(labels: DebugPlatePcbLabelsConfig, box_height: float) -> float:
    return labels.row_spacing_mils if labels.row_spacing_mils is not None else box_height + 20.0


def _pcb_label_box_size(
    labels: DebugPlatePcbLabelsConfig,
    width_mils: float | None,
) -> tuple[float, float] | None:
    if width_mils is None:
        return labels.box_size_mils
    height_mils = labels.box_size_mils[1] if labels.box_size_mils is not None else 70.0
    return (width_mils, height_mils)


def _pcb_net_label_style_args(
    labels: DebugPlatePcbLabelsConfig,
    *,
    box_size_mils: tuple[float, float] | None = None,
) -> JsonObject:
    style = dict(labels.style)
    use_box = box_size_mils is not None
    args: JsonObject = {
        "height_mils": _style_float(style, "height_mils", 65.0),
        "layer": _style_string_or_int(style, "layer", "TOP_OVERLAY"),
        "font_kind": _style_string(style, "font_kind", "truetype"),
        "font_name": _style_string(style, "font_name", "Arial"),
        "bold": _style_bool(style, "bold", True),
        "stroke_width_mils": _style_float(style, "stroke_width_mils", 10.0),
        "is_inverted": _style_bool(style, "is_inverted", use_box),
        "inverted_margin_mils": _style_float(style, "inverted_margin_mils", 10.0),
        "use_inverted_rectangle": _style_bool(style, "use_inverted_rectangle", use_box),
        "is_frame": _style_bool(style, "is_frame", use_box),
        "text_justification": _style_string_or_int(
            style,
            "text_justification",
            _default_pcb_label_justification(labels.side),
        ),
    }
    if box_size_mils is not None:
        box_size = list(box_size_mils)
        if args["use_inverted_rectangle"]:
            args["inverted_rectangle_size_mils"] = box_size
        if args["is_frame"]:
            args["frame_size_mils"] = box_size
    for key in _PCB_LABEL_STYLE_PASSTHROUGH_KEYS:
        if key not in args and key in style:
            args[key] = style[key]
    return args


def _pcb_label_header_style_args(labels: DebugPlatePcbLabelsConfig) -> JsonObject:
    style = dict(labels.style)
    return {
        "height_mils": _style_float(style, "header_height_mils", 50.0),
        "layer": _style_string_or_int(style, "layer", "TOP_OVERLAY"),
        "font_kind": _style_string(style, "font_kind", "truetype"),
        "font_name": _style_string(style, "font_name", "Arial"),
        "bold": _style_bool(style, "bold", True),
        "italic": _style_bool(style, "italic", False),
        "stroke_width_mils": _style_float(style, "header_stroke_width_mils", 8.0),
        "text_justification": _default_pcb_label_justification(labels.side),
    }


def _default_pcb_label_justification(side: str) -> str:
    return "LEFT_TOP" if side in {"left", "board_left"} else "RIGHT_TOP"


def _target_optional_string(target: Mapping[str, object], name: str) -> str | None:
    value = target.get(name)
    if value is None:
        return None
    return str(value)


def _target_float(target: Mapping[str, object], name: str) -> float:
    value = target.get(name)
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise ValueError(f"Debug-plate target field {name!r} must be numeric")
    return float(value)


def _style_string(style: Mapping[str, object], name: str, default: str) -> str:
    value = style.get(name)
    if value is None:
        return default
    if not isinstance(value, str):
        raise ValueError(f"Field pcb_labels.style.{name} must be a string")
    return value


def _style_string_or_int(
    style: Mapping[str, object],
    name: str,
    default: str | int,
) -> str | int:
    value = style.get(name)
    if value is None:
        return default
    if isinstance(value, str | int) and not isinstance(value, bool):
        return value
    raise ValueError(f"Field pcb_labels.style.{name} must be a string or integer")


def _style_bool(style: Mapping[str, object], name: str, default: bool) -> bool:
    value = style.get(name)
    if value is None:
        return default
    if not isinstance(value, bool):
        raise ValueError(f"Field pcb_labels.style.{name} must be a boolean")
    return value


def _style_float(style: Mapping[str, object], name: str, default: float) -> float:
    value = style.get(name)
    if value is None:
        return default
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise ValueError(f"Field pcb_labels.style.{name} must be numeric")
    return float(value)


def _safe_id(value: str) -> str:
    result = "".join(char.lower() if char.isalnum() else "_" for char in value)
    return result.strip("_") or "label"
