"""Schematic operation planning helpers for debug-plate workflows."""

from __future__ import annotations

from dataclasses import dataclass

from altium_cruncher.altium_cruncher_mco import JsonObject

_SCHEMATIC_COLUMN_COUNT = 4
_SCHEMATIC_ORIGIN_MILS = (1200.0, 1200.0)
_SCHEMATIC_COLUMN_SPACING_MILS = 1500.0
_SCHEMATIC_ROW_SPACING_MILS = 900.0
_SCHEMATIC_WIRE_LENGTH_MILS = 350.0
_SCHEMATIC_NET_LABEL_OFFSET_MILS = 180.0


@dataclass(frozen=True, slots=True)
class DebugPlateSchematicNetRoute:
    """Computed schematic wire route for a generated mate part."""

    wire_start_mils: tuple[float, float]
    wire_end_mils: tuple[float, float]
    label_position_mils: tuple[float, float]
    pin_orientation: int


def schematic_position(index: int) -> tuple[float, float]:
    column = (index - 1) % _SCHEMATIC_COLUMN_COUNT
    row = (index - 1) // _SCHEMATIC_COLUMN_COUNT
    origin_x, origin_y = _SCHEMATIC_ORIGIN_MILS
    return (
        origin_x + column * _SCHEMATIC_COLUMN_SPACING_MILS,
        origin_y + row * _SCHEMATIC_ROW_SPACING_MILS,
    )


def schematic_net_route(
    *,
    symbol_library_path: str,
    symbol_name: str,
    signal_pin_designator: str | None,
    component_position_mils: tuple[float, float],
    net_name: str | None,
) -> DebugPlateSchematicNetRoute | None:
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
    wire_end = (
        wire_start[0] + direction_x * _SCHEMATIC_WIRE_LENGTH_MILS,
        wire_start[1] + direction_y * _SCHEMATIC_WIRE_LENGTH_MILS,
    )
    label_position = (
        wire_start[0] + direction_x * _SCHEMATIC_NET_LABEL_OFFSET_MILS,
        wire_start[1] + direction_y * _SCHEMATIC_NET_LABEL_OFFSET_MILS,
    )
    return DebugPlateSchematicNetRoute(
        wire_start_mils=wire_start,
        wire_end_mils=wire_end,
        label_position_mils=label_position,
        pin_orientation=orientation,
    )


def schematic_wire_operation(
    *,
    schematic_file: str,
    designator: str,
    route: DebugPlateSchematicNetRoute,
) -> JsonObject:
    return {
        "id": f"wire_{_safe_id(designator)}_net",
        "op": "schdoc.add-wire",
        "message": f"Add debug-plate schematic wire for {designator}",
        "args": {
            "file": schematic_file,
            "overwrite": True,
            "points_mils": [
                list(route.wire_start_mils),
                list(route.wire_end_mils),
            ],
        },
    }


def schematic_net_label_operation(
    *,
    schematic_file: str,
    designator: str,
    net_name: str,
    route: DebugPlateSchematicNetRoute,
) -> JsonObject:
    return {
        "id": f"label_{_safe_id(designator)}_net",
        "op": "schdoc.add-net-label",
        "message": f"Add debug-plate schematic net label for {designator}",
        "args": {
            "file": schematic_file,
            "overwrite": True,
            "text": net_name,
            "location_mils": list(route.label_position_mils),
        },
    }


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


def _safe_id(value: str) -> str:
    return "".join(char.lower() if char.isalnum() else "_" for char in value).strip("_")
