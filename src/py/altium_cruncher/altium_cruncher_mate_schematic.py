"""Schematic operation planning helpers for mate workflows."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from math import ceil

from altium_cruncher.altium_cruncher_mco import JsonObject, mco_operation

_SCHEMATIC_COLUMN_COUNT = 4
_SCHEMATIC_ORIGIN_MILS = (1200.0, 1200.0)
_SCHEMATIC_COLUMN_SPACING_MILS = 2400.0
_SCHEMATIC_ROW_SPACING_MILS = 900.0
_SCHEMATIC_GROUP_GAP_ROWS = 1
_SCHEMATIC_DESIGNATOR_Y_OFFSET_MILS = 180.0
_SCHEMATIC_DESIGNATOR_FONT_SIZE = 10
_SCHEMATIC_NET_LABEL_OFFSET_MILS = 160.0
_SCHEMATIC_NET_LABEL_MIN_SPAN_MILS = 350.0
_SCHEMATIC_NET_LABEL_CHAR_WIDTH_MILS = 75.0
_SCHEMATIC_NET_LABEL_TRAILING_MARGIN_MILS = 120.0


@dataclass(frozen=True, slots=True)
class MateSchematicNetRoute:
    """Computed schematic wire route for a generated mate part."""

    wire_start_mils: tuple[float, float]
    wire_end_mils: tuple[float, float]
    label_position_mils: tuple[float, float]
    pin_orientation: int
    label_orientation: int


def schematic_grouped_positions(group_keys: Sequence[str]) -> list[tuple[float, float]]:
    group_start_rows: dict[str, int] = {}
    group_counts: dict[str, int] = {}
    group_order: list[str] = []
    for key in group_keys:
        if key not in group_counts:
            group_order.append(key)
            group_counts[key] = 0
        group_counts[key] += 1

    next_row = 0
    for key in group_order:
        group_start_rows[key] = next_row
        group_rows = ceil(group_counts[key] / _SCHEMATIC_COLUMN_COUNT)
        next_row += group_rows + _SCHEMATIC_GROUP_GAP_ROWS

    positions: list[tuple[float, float]] = []
    group_indices: dict[str, int] = {}
    for key in group_keys:
        group_index = group_indices.get(key, 0)
        group_indices[key] = group_index + 1
        row = group_start_rows[key] + group_index // _SCHEMATIC_COLUMN_COUNT
        column = group_index % _SCHEMATIC_COLUMN_COUNT
        positions.append(_schematic_position_at(row=row, column=column))
    return positions


def schematic_designator_style(
    designator: str,
    component_position_mils: tuple[float, float],
) -> JsonObject:
    component_x, component_y = component_position_mils
    return {
        "position_mils": [
            component_x,
            component_y + _SCHEMATIC_DESIGNATOR_Y_OFFSET_MILS,
        ],
        "justification": "BOTTOM_CENTER",
        "font_name": "Arial",
        "font_size": _SCHEMATIC_DESIGNATOR_FONT_SIZE,
        "bold": True,
    }


def schematic_net_route(
    *,
    symbol_library_path: str,
    symbol_name: str,
    signal_pin_designator: str | None,
    component_position_mils: tuple[float, float],
    net_name: str | None,
) -> MateSchematicNetRoute | None:
    if not net_name:
        return None
    component_x, component_y = component_position_mils
    pin_x, pin_y, orientation, pin_length = _signal_pin_layout(
        symbol_library_path=symbol_library_path,
        symbol_name=symbol_name,
        signal_pin_designator=signal_pin_designator,
    )
    direction_x, direction_y = _pin_direction(orientation)
    wire_start = (
        component_x + pin_x + direction_x * pin_length,
        component_y + pin_y + direction_y * pin_length,
    )
    wire_length = _net_label_wire_length_mils(net_name)
    wire_end = (
        wire_start[0] + direction_x * wire_length,
        wire_start[1] + direction_y * wire_length,
    )
    label_position = (
        wire_start[0] + direction_x * _SCHEMATIC_NET_LABEL_OFFSET_MILS,
        wire_start[1] + direction_y * _SCHEMATIC_NET_LABEL_OFFSET_MILS,
    )
    return MateSchematicNetRoute(
        wire_start_mils=wire_start,
        wire_end_mils=wire_end,
        label_position_mils=label_position,
        pin_orientation=orientation,
        label_orientation=orientation % 4,
    )


def schematic_wire_operation(
    *,
    schematic_file: str,
    designator: str,
    route: MateSchematicNetRoute,
) -> JsonObject:
    return mco_operation(
        "schdoc.add_wire",
        f"wire_{_safe_id(designator)}_net",
        f"Add mate schematic wire for {designator}",
        {
            "file": schematic_file,
            "overwrite": True,
            "points_mils": [
                list(route.wire_start_mils),
                list(route.wire_end_mils),
            ],
        },
    )


def schematic_net_label_operation(
    *,
    schematic_file: str,
    designator: str,
    net_name: str,
    route: MateSchematicNetRoute,
) -> JsonObject:
    return mco_operation(
        "schdoc.add_net_label",
        f"label_{_safe_id(designator)}_net",
        f"Add mate schematic net label for {designator}",
        {
            "file": schematic_file,
            "overwrite": True,
            "text": net_name,
            "location_mils": list(route.label_position_mils),
            "orientation": route.label_orientation,
        },
    )


def _signal_pin_layout(
    *,
    symbol_library_path: str,
    symbol_name: str,
    signal_pin_designator: str | None,
) -> tuple[float, float, int, float]:
    pin = _signal_pin(
        symbol_library_path=symbol_library_path,
        symbol_name=symbol_name,
        signal_pin_designator=signal_pin_designator,
    )
    if pin is None:
        return (0.0, 0.0, 0, 0.0)
    orientation = getattr(pin, "orientation", 0)
    return (
        float(getattr(pin, "x_mils", 0.0) or 0.0),
        float(getattr(pin, "y_mils", 0.0) or 0.0),
        int(getattr(orientation, "value", orientation)),
        float(getattr(pin, "length_mils", 0.0) or 0.0),
    )


def _signal_pin(
    *,
    symbol_library_path: str,
    symbol_name: str,
    signal_pin_designator: str | None,
) -> object | None:
    try:
        from altium_monkey import AltiumSchLib

        schlib = AltiumSchLib(symbol_library_path)
        symbol = schlib.get_symbol(symbol_name)
    except Exception:
        return None
    pins = list(getattr(symbol, "pins", []) or []) if symbol is not None else []
    if not pins:
        return None
    if signal_pin_designator:
        for pin in pins:
            if str(getattr(pin, "designator", "") or "") == signal_pin_designator:
                return pin
    return pins[0]


def _pin_direction(orientation: int) -> tuple[float, float]:
    normalized = int(orientation) % 4
    if normalized == 1:
        return (0.0, 1.0)
    if normalized == 2:
        return (-1.0, 0.0)
    if normalized == 3:
        return (0.0, -1.0)
    return (1.0, 0.0)


def _net_label_wire_length_mils(net_name: str) -> float:
    label_span = max(
        _SCHEMATIC_NET_LABEL_MIN_SPAN_MILS,
        len(net_name) * _SCHEMATIC_NET_LABEL_CHAR_WIDTH_MILS,
    )
    return (
        _SCHEMATIC_NET_LABEL_OFFSET_MILS
        + label_span
        + _SCHEMATIC_NET_LABEL_TRAILING_MARGIN_MILS
    )


def _schematic_position_at(*, row: int, column: int) -> tuple[float, float]:
    origin_x, origin_y = _SCHEMATIC_ORIGIN_MILS
    return (
        origin_x + column * _SCHEMATIC_COLUMN_SPACING_MILS,
        origin_y + row * _SCHEMATIC_ROW_SPACING_MILS,
    )


def _safe_id(value: str) -> str:
    return "".join(char.lower() if char.isalnum() else "_" for char in value).strip("_")
