"""EasyEDA schematic symbol to Altium SchLib mapping."""

from __future__ import annotations

import json
import math
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from altium_monkey.altium_record_types import SchPointMils
from altium_monkey.altium_sch_enums import (
    IeeeSymbol,
    PinElectrical,
    PinTextRotation,
    Rotation90,
)
from altium_monkey.altium_sch_object_factory import make_sch_pin
from altium_monkey.altium_schlib import AltiumSchLib, AltiumSymbol
from easyeda_monkey.easyeda_pin import EasyEdaPin
from easyeda_monkey.easyeda_symbol import EasyEdaSymbol


_PATH_TOKEN_RE = re.compile(
    r"[AaCcHhLlMmQqSsTtVvZz]|[-+]?(?:\d+\.\d+|\d+|\.\d+)(?:[eE][-+]?\d+)?"
)


@dataclass(frozen=True)
class EasyEdaSchematicImportPolicy:
    """Mapping controls for the initial direct Altium importer."""

    mils_per_easyeda_unit: float = 10.0
    invert_y: bool = True
    default_pin_length_mils: float = 100.0
    hotspot_grid_mils: float = 100.0
    align_hotspots_to_grid: bool = True
    body_color: int = 0x000000
    body_fill_color: int = 0xFFFFFF
    use_source_pin_electrical: bool = False
    use_source_pin_ieee_symbols: bool = False
    pin_name_visibility: str = "source"
    pin_designator_visibility: str = "source"
    pin_text_orientation: str = "default"
    rotate_vertical_pin_text: bool = False


@dataclass(frozen=True)
class EasyEdaSchematicImportResult:
    """Result paths and mapping report from a schematic import."""

    library: AltiumSchLib
    report: "EasyEdaSchematicMappingReport"


@dataclass
class EasyEdaSchematicMappingReport:
    """Human-readable import report written beside generated SchLib files."""

    lcsc_id: str
    symbol_name: str
    designator: str
    pin_count: int = 0
    rectangle_count: int = 0
    circle_count: int = 0
    ellipse_count: int = 0
    polyline_count: int = 0
    polygon_count: int = 0
    unsupported_count: int = 0
    unsupported_graphics: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    policy: dict[str, Any] = field(default_factory=dict)
    grid: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def write_json(self, path: Path) -> None:
        path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")


@dataclass(frozen=True)
class _EePoint:
    x: float
    y: float


@dataclass(frozen=True)
class _MilsPoint:
    x: float
    y: float


@dataclass(frozen=True)
class _SymbolTransform:
    anchor_x: float
    anchor_y: float
    scale: float
    invert_y: bool

    def point(self, point: _EePoint) -> _MilsPoint:
        y = point.y - self.anchor_y
        if self.invert_y:
            y = -y
        return _MilsPoint(
            x=(point.x - self.anchor_x) * self.scale,
            y=y * self.scale,
        )


@dataclass(frozen=True)
class _PinGeometry:
    location: _MilsPoint
    orientation: Rotation90
    length_mils: float


def load_easyeda_symbol_input(path: Path) -> tuple[EasyEdaSymbol, dict[str, Any] | None]:
    """Load either a full EasyEDA/LCSC API response or an EasyEdaSymbol JSON file."""

    data = json.loads(path.read_text(encoding="utf-8"))
    source_data = data if isinstance(data, dict) and "result" in data else None
    return EasyEdaSymbol.from_json(data), source_data


def extract_easyeda_component_params(source_data: dict[str, Any] | None) -> dict[str, str]:
    """Extract `head.c_para` fields from newer EasyEDA API responses."""

    if not source_data:
        return {}
    result = source_data.get("result", {})
    params = _extract_c_para(result.get("dataStr", {}))
    package_params = _extract_c_para(
        (result.get("packageDetail") or {}).get("dataStr", {})
    )

    for key, value in package_params.items():
        params.setdefault(key, value)
        params[f"package.{key}"] = value
    return params


def _extract_c_para(data_str: dict[str, Any]) -> dict[str, str]:
    head = data_str.get("head", {}) if isinstance(data_str, dict) else {}
    if not isinstance(head, dict):
        return {}
    raw_params = head.get("c_para", {})
    if not isinstance(raw_params, dict):
        return {}
    return {str(k): str(v) for k, v in raw_params.items() if v is not None}


def build_altium_schlib_from_easyeda_symbol(
    easyeda_symbol: EasyEdaSymbol,
    *,
    source_data: dict[str, Any] | None = None,
    symbol_name: str | None = None,
    policy: EasyEdaSchematicImportPolicy | None = None,
) -> EasyEdaSchematicImportResult:
    """Build a one-symbol Altium schematic library from an EasyEDA symbol."""

    policy = policy or EasyEdaSchematicImportPolicy()
    params = extract_easyeda_component_params(source_data)
    name = _symbol_name(easyeda_symbol, params, symbol_name)
    designator = _designator(easyeda_symbol, params)
    report = EasyEdaSchematicMappingReport(
        lcsc_id=easyeda_symbol.info.lcsc_id or params.get("Supplier Part", ""),
        symbol_name=name,
        designator=designator,
        policy=_policy_report(policy),
    )

    transform, grid_report = _build_transform(easyeda_symbol, policy)
    report.grid.update(grid_report)
    library = AltiumSchLib()
    symbol = library.add_symbol(name, description=easyeda_symbol.info.description)

    _add_symbol_metadata(symbol, easyeda_symbol, params, transform, designator)
    _add_easyeda_graphics(symbol, easyeda_symbol, transform, policy, report)
    _add_easyeda_pins(symbol, easyeda_symbol, transform, policy, report)
    _add_hotspot_grid_report(easyeda_symbol, transform, policy, report)

    return EasyEdaSchematicImportResult(library=library, report=report)


def _symbol_name(
    easyeda_symbol: EasyEdaSymbol,
    params: dict[str, str],
    override: str | None,
) -> str:
    if override:
        return override.strip()
    return (
        params.get("name")
        or params.get("Manufacturer Part")
        or easyeda_symbol.info.name
        or easyeda_symbol.info.lcsc_id
        or "EasyEDA_Part"
    ).strip()


def _designator(easyeda_symbol: EasyEdaSymbol, params: dict[str, str]) -> str:
    symbol_prefix = (params.get("pre") or easyeda_symbol.info.prefix or "").strip()
    package_prefix = (params.get("package.pre") or "").strip()
    if _is_generic_designator(symbol_prefix) and package_prefix:
        return package_prefix
    return (symbol_prefix or package_prefix or "U?").strip()


def _is_generic_designator(value: str) -> bool:
    return value.strip().upper() in {"", "U?"}


def _policy_report(policy: EasyEdaSchematicImportPolicy) -> dict[str, Any]:
    return {
        "mils_per_easyeda_unit": policy.mils_per_easyeda_unit,
        "invert_y": policy.invert_y,
        "default_pin_length_mils": policy.default_pin_length_mils,
        "hotspot_grid_mils": policy.hotspot_grid_mils,
        "align_hotspots_to_grid": policy.align_hotspots_to_grid,
        "use_source_pin_electrical": policy.use_source_pin_electrical,
        "use_source_pin_ieee_symbols": policy.use_source_pin_ieee_symbols,
        "pin_name_visibility": policy.pin_name_visibility,
        "pin_designator_visibility": policy.pin_designator_visibility,
        "pin_text_orientation": policy.pin_text_orientation,
        "rotate_vertical_pin_text": policy.rotate_vertical_pin_text,
    }


def _comment_text(easyeda_symbol: EasyEdaSymbol, params: dict[str, str]) -> str:
    return (
        params.get("Value")
        or params.get("Manufacturer Part")
        or params.get("name")
        or easyeda_symbol.info.name
        or easyeda_symbol.info.lcsc_id
    ).strip()


def _add_symbol_metadata(
    symbol: AltiumSymbol,
    easyeda_symbol: EasyEdaSymbol,
    params: dict[str, str],
    transform: _SymbolTransform,
    designator: str,
) -> None:
    min_point, max_point = _easyeda_bounds(easyeda_symbol)
    top_left = transform.point(_EePoint(min_point.x, min_point.y))
    bottom_right = transform.point(_EePoint(max_point.x, max_point.y))
    top_y = max(top_left.y, bottom_right.y)
    bottom_y = min(top_left.y, bottom_right.y)
    left_x = min(top_left.x, bottom_right.x)

    symbol.add_designator(designator, int(round(left_x)), int(round(top_y + 120)))
    comment = _comment_text(easyeda_symbol, params)
    if comment:
        symbol.add_parameter("Comment", comment, x=int(round(left_x)), y=int(round(bottom_y - 120)))

    hidden_params = {
        "LCSC Part": easyeda_symbol.info.lcsc_id or params.get("Supplier Part", ""),
        "Supplier": params.get("Supplier", ""),
        "Manufacturer": params.get("Manufacturer") or easyeda_symbol.info.manufacturer,
        "Manufacturer Part": params.get("Manufacturer Part", ""),
        "Package": params.get("package") or easyeda_symbol.info.package,
        "JLCPCB Part Class": params.get("JLCPCB Part Class", ""),
    }
    for key, value in hidden_params.items():
        if value:
            symbol.add_parameter(key, value, is_hidden=True)


def _add_easyeda_graphics(
    symbol: AltiumSymbol,
    easyeda_symbol: EasyEdaSymbol,
    transform: _SymbolTransform,
    policy: EasyEdaSchematicImportPolicy,
    report: EasyEdaSchematicMappingReport,
) -> None:
    for rect in easyeda_symbol.rectangles:
        p1 = transform.point(_EePoint(rect.x, rect.y))
        p2 = transform.point(_EePoint(rect.x + rect.width, rect.y + rect.height))
        fill_color = _hex_to_win32(rect.fill_color, default=policy.body_fill_color)
        transparent = _is_no_fill(rect.fill_color)
        symbol.add_rectangle(
            int(round(p1.x)),
            int(round(p1.y)),
            int(round(p2.x)),
            int(round(p2.y)),
            color=_hex_to_win32(rect.stroke_color, default=policy.body_color),
            area_color=fill_color,
            is_solid=not transparent,
            transparent=transparent,
        )
        report.rectangle_count += 1

    for circle in easyeda_symbol.circles:
        center = transform.point(_EePoint(circle.cx, circle.cy))
        symbol.add_arc(
            int(round(center.x)),
            int(round(center.y)),
            int(round(circle.radius * transform.scale)),
            color=_hex_to_win32(circle.stroke_color, default=policy.body_color),
        )
        report.circle_count += 1

    for ellipse in easyeda_symbol.ellipses:
        center = transform.point(_EePoint(ellipse.cx, ellipse.cy))
        symbol.add_ellipse(
            int(round(center.x)),
            int(round(center.y)),
            int(round(ellipse.rx * transform.scale)),
            int(round(ellipse.ry * transform.scale)),
            color=_hex_to_win32(ellipse.stroke_color, default=policy.body_color),
            area_color=_hex_to_win32(ellipse.fill_color, default=policy.body_fill_color),
            is_solid=not _is_no_fill(ellipse.fill_color),
        )
        report.ellipse_count += 1

    for polyline in easyeda_symbol.polylines:
        vertices = _transform_vertices(polyline.points, transform)
        if len(vertices) >= 2:
            symbol.add_polyline(
                vertices,
                color=_hex_to_win32(polyline.stroke_color, default=policy.body_color),
            )
            report.polyline_count += 1

    for polygon in easyeda_symbol.polygons:
        vertices = _transform_vertices(polygon.points, transform)
        if len(vertices) >= 3:
            symbol.add_polygon(
                vertices,
                color=_hex_to_win32(polygon.stroke_color, default=policy.body_color),
                area_color=_hex_to_win32(polygon.fill_color, default=policy.body_fill_color),
                is_solid=not _is_no_fill(polygon.fill_color),
            )
            report.polygon_count += 1

    for path in easyeda_symbol.paths:
        report.unsupported_graphics.append(f"path:{path.id or path.path_string[:40]}")
    for arc in easyeda_symbol.arcs:
        report.unsupported_graphics.append(f"arc:{arc.id or arc.path_string[:40]}")
    report.unsupported_count = len(report.unsupported_graphics)


def _add_easyeda_pins(
    symbol: AltiumSymbol,
    easyeda_symbol: EasyEdaSymbol,
    transform: _SymbolTransform,
    policy: EasyEdaSchematicImportPolicy,
    report: EasyEdaSchematicMappingReport,
) -> None:
    for index, pin in enumerate(easyeda_symbol.pins, start=1):
        geometry = _pin_geometry(pin, transform, policy, report)
        designator = (pin.number or pin.spice_number or str(index)).strip()
        name_rotation = _pin_text_rotation(
            source_rotation=pin.name_rotation,
            pin_orientation=geometry.orientation,
            policy=policy,
        )
        designator_rotation = _pin_text_rotation(
            source_rotation=pin.number_rotation,
            pin_orientation=geometry.orientation,
            policy=policy,
        )
        symbol.add_pin(
            make_sch_pin(
                designator=designator,
                name=(pin.name or "").strip(),
                location_mils=SchPointMils.from_mils(geometry.location.x, geometry.location.y),
                orientation=geometry.orientation,
                length_mils=geometry.length_mils,
                electrical_type=_pin_electrical_type(pin, policy),
                hidden=not pin.show,
                name_visible=_pin_text_visible(policy.pin_name_visibility, pin.name_visible),
                designator_visible=_pin_text_visible(
                    policy.pin_designator_visibility,
                    pin.number_visible,
                ),
                name_rotation=name_rotation,
                designator_rotation=designator_rotation,
                symbol_outer=_pin_symbol_outer(pin, policy),
                symbol_inner_edge=_pin_symbol_inner_edge(pin, policy),
            )
        )
        report.pin_count += 1


def _pin_geometry(
    pin: EasyEdaPin,
    transform: _SymbolTransform,
    policy: EasyEdaSchematicImportPolicy,
    report: EasyEdaSchematicMappingReport,
) -> _PinGeometry:
    hotspot_ee = _EePoint(pin.dot_x, pin.dot_y)
    body_ee = _pin_body_endpoint(pin, hotspot_ee, policy, report)
    hotspot = transform.point(hotspot_ee)
    body = transform.point(body_ee)
    dx = hotspot.x - body.x
    dy = hotspot.y - body.y
    orientation = _orientation_from_delta(dx, dy, pin.rotation)
    length = max(abs(dx), abs(dy))
    if length < 1.0:
        length = policy.default_pin_length_mils
    return _PinGeometry(location=body, orientation=orientation, length_mils=length)


def _pin_body_endpoint(
    pin: EasyEdaPin,
    hotspot: _EePoint,
    policy: EasyEdaSchematicImportPolicy,
    report: EasyEdaSchematicMappingReport,
) -> _EePoint:
    path_points = _parse_path_points(pin.path_string)
    if len(path_points) >= 2:
        first = path_points[0]
        last = path_points[-1]
        if _distance(first, hotspot) <= _distance(last, hotspot):
            return last
        return first

    report.warnings.append(
        f"pin {pin.number or pin.id or '?'} used rotation fallback for pin length"
    )
    length_ee = policy.default_pin_length_mils / policy.mils_per_easyeda_unit
    vx, vy = _easyeda_outward_vector(pin.rotation)
    return _EePoint(hotspot.x - (vx * length_ee), hotspot.y - (vy * length_ee))


def _parse_path_points(path_string: str) -> list[_EePoint]:
    tokens = _PATH_TOKEN_RE.findall(path_string or "")
    points: list[_EePoint] = []
    index = 0
    command = ""
    current = _EePoint(0.0, 0.0)
    start = _EePoint(0.0, 0.0)

    try:
        while index < len(tokens):
            token = tokens[index]
            if _is_path_command(token):
                command = token
                index += 1
                if command in "Zz":
                    current = start
                    points.append(current)
                    continue

            if command in "Mm":
                x, y, index = _read_pair(tokens, index)
                current = _relative_or_absolute(command, current, x, y)
                start = current
                points.append(current)
                command = "l" if command == "m" else "L"
            elif command in "Ll":
                x, y, index = _read_pair(tokens, index)
                current = _relative_or_absolute(command, current, x, y)
                points.append(current)
            elif command in "Hh":
                x, index = _read_number(tokens, index)
                current = _EePoint(current.x + x if command == "h" else x, current.y)
                points.append(current)
            elif command in "Vv":
                y, index = _read_number(tokens, index)
                current = _EePoint(current.x, current.y + y if command == "v" else y)
                points.append(current)
            else:
                break
    except ValueError:
        return points

    return points


def _read_pair(tokens: list[str], index: int) -> tuple[float, float, int]:
    x, index = _read_number(tokens, index)
    y, index = _read_number(tokens, index)
    return x, y, index


def _read_number(tokens: list[str], index: int) -> tuple[float, int]:
    if index >= len(tokens) or _is_path_command(tokens[index]):
        raise ValueError("expected path number")
    return float(tokens[index]), index + 1


def _is_path_command(token: str) -> bool:
    return len(token) == 1 and token.isalpha()


def _relative_or_absolute(command: str, current: _EePoint, x: float, y: float) -> _EePoint:
    if command.islower():
        return _EePoint(current.x + x, current.y + y)
    return _EePoint(x, y)


def _pin_electrical_type(pin: EasyEdaPin, policy: EasyEdaSchematicImportPolicy) -> PinElectrical:
    if not policy.use_source_pin_electrical:
        return PinElectrical.PASSIVE
    return {
        "": PinElectrical.PASSIVE,
        "0": PinElectrical.PASSIVE,
        "1": PinElectrical.INPUT,
        "2": PinElectrical.OUTPUT,
        "3": PinElectrical.IO,
        "4": PinElectrical.POWER,
    }.get(str(pin.electrical_type).strip(), PinElectrical.PASSIVE)


def _pin_text_visible(mode: str, source_visible: bool) -> bool:
    normalized = mode.strip().lower()
    if normalized == "source":
        return source_visible
    if normalized == "show":
        return True
    if normalized == "hide":
        return False
    raise ValueError(f"unsupported pin text visibility mode: {mode}")


def _pin_text_rotation(
    *,
    source_rotation: float,
    pin_orientation: Rotation90,
    policy: EasyEdaSchematicImportPolicy,
) -> PinTextRotation | None:
    mode = policy.pin_text_orientation.strip().lower()
    if policy.rotate_vertical_pin_text and mode == "default":
        mode = "vertical"
    if mode == "default":
        return None
    pin_is_vertical = pin_orientation in {Rotation90.DEG_90, Rotation90.DEG_270}
    if mode == "vertical":
        if pin_is_vertical:
            return None
        return PinTextRotation.VERTICAL
    if mode == "source":
        source_is_vertical = _source_rotation_is_vertical(source_rotation)
        if source_is_vertical and pin_is_vertical:
            return None
        if not source_is_vertical and pin_is_vertical:
            return PinTextRotation.VERTICAL
        if source_is_vertical:
            return PinTextRotation.VERTICAL
        return None
    raise ValueError(f"unsupported pin text orientation mode: {policy.pin_text_orientation}")


def _source_rotation_is_vertical(rotation: float) -> bool:
    normalized = int(round(rotation / 90.0) * 90) % 360
    return normalized in {90, 270}


def _pin_symbol_outer(pin: EasyEdaPin, policy: EasyEdaSchematicImportPolicy) -> IeeeSymbol:
    if policy.use_source_pin_ieee_symbols and pin.dot_visible:
        return IeeeSymbol.DOT
    return IeeeSymbol.NONE


def _pin_symbol_inner_edge(pin: EasyEdaPin, policy: EasyEdaSchematicImportPolicy) -> IeeeSymbol:
    if policy.use_source_pin_ieee_symbols and pin.clock_visible:
        return IeeeSymbol.CLOCK
    return IeeeSymbol.NONE


def _orientation_from_delta(dx: float, dy: float, fallback_rotation: float) -> Rotation90:
    if abs(dx) < 1e-6 and abs(dy) < 1e-6:
        return _rotation_to_orientation(fallback_rotation)
    if abs(dx) >= abs(dy):
        return Rotation90.DEG_0 if dx >= 0 else Rotation90.DEG_180
    return Rotation90.DEG_90 if dy >= 0 else Rotation90.DEG_270


def _rotation_to_orientation(rotation: float) -> Rotation90:
    normalized = int(round(rotation / 90.0) * 90) % 360
    return {
        0: Rotation90.DEG_0,
        90: Rotation90.DEG_90,
        180: Rotation90.DEG_180,
        270: Rotation90.DEG_270,
    }.get(normalized, Rotation90.DEG_0)


def _easyeda_outward_vector(rotation: float) -> tuple[float, float]:
    normalized = int(round(rotation / 90.0) * 90) % 360
    return {
        0: (1.0, 0.0),
        90: (0.0, -1.0),
        180: (-1.0, 0.0),
        270: (0.0, 1.0),
    }.get(normalized, (1.0, 0.0))


def _build_transform(
    easyeda_symbol: EasyEdaSymbol,
    policy: EasyEdaSchematicImportPolicy,
) -> tuple[_SymbolTransform, dict[str, Any]]:
    min_point, max_point = _easyeda_bounds(easyeda_symbol)
    anchor_x = (min_point.x + max_point.x) / 2.0
    anchor_y = (min_point.y + max_point.y) / 2.0
    grid_report: dict[str, Any] = {
        "hotspot_grid_mils": policy.hotspot_grid_mils,
        "align_hotspots_to_grid": policy.align_hotspots_to_grid,
        "anchor_adjusted_to_grid": False,
    }

    if policy.hotspot_grid_mils > 0:
        grid_units = policy.hotspot_grid_mils / policy.mils_per_easyeda_unit
        pin_dot_xs = [pin.dot_x for pin in easyeda_symbol.pins]
        pin_dot_ys = [pin.dot_y for pin in easyeda_symbol.pins]
        x_remainder = _common_grid_remainder(pin_dot_xs, grid_units)
        y_remainder = _common_grid_remainder(pin_dot_ys, grid_units)
        common_offset_possible = x_remainder is not None and y_remainder is not None
        grid_report.update(
            {
                "source_grid_units": grid_units,
                "source_common_offset_possible": common_offset_possible,
                "source_x_remainder": x_remainder,
                "source_y_remainder": y_remainder,
            }
        )
        if policy.align_hotspots_to_grid and common_offset_possible:
            anchor_x = _nearest_value_with_remainder(anchor_x, x_remainder, grid_units)
            anchor_y = _nearest_value_with_remainder(anchor_y, y_remainder, grid_units)
            grid_report["anchor_adjusted_to_grid"] = True

    return _SymbolTransform(
        anchor_x=anchor_x,
        anchor_y=anchor_y,
        scale=policy.mils_per_easyeda_unit,
        invert_y=policy.invert_y,
    ), grid_report


def _add_hotspot_grid_report(
    easyeda_symbol: EasyEdaSymbol,
    transform: _SymbolTransform,
    policy: EasyEdaSchematicImportPolicy,
    report: EasyEdaSchematicMappingReport,
) -> None:
    if policy.hotspot_grid_mils <= 0:
        return

    off_grid: list[dict[str, Any]] = []
    max_error = 0.0
    for pin in easyeda_symbol.pins:
        hotspot = transform.point(_EePoint(pin.dot_x, pin.dot_y))
        x_error = _distance_to_grid(hotspot.x, policy.hotspot_grid_mils)
        y_error = _distance_to_grid(hotspot.y, policy.hotspot_grid_mils)
        pin_error = max(x_error, y_error)
        max_error = max(max_error, pin_error)
        if pin_error > 1e-6:
            off_grid.append(
                {
                    "pin": pin.number or pin.id,
                    "name": pin.name,
                    "x_mils": round(hotspot.x, 6),
                    "y_mils": round(hotspot.y, 6),
                    "x_error_mils": round(x_error, 6),
                    "y_error_mils": round(y_error, 6),
                }
            )

    report.grid.update(
        {
            "hotspot_count": len(easyeda_symbol.pins),
            "off_grid_hotspot_count": len(off_grid),
            "max_hotspot_error_mils": round(max_error, 6),
            "off_grid_hotspots_sample": off_grid[:10],
        }
    )
    if off_grid:
        report.warnings.append(
            f"{len(off_grid)}/{len(easyeda_symbol.pins)} pin hotspots are not on "
            f"{policy.hotspot_grid_mils:g} mil grid; max error {max_error:g} mil"
        )


def _common_grid_remainder(values: list[float], grid_units: float) -> float | None:
    if not values or grid_units <= 0:
        return None
    residues = [_normalized_remainder(value, grid_units) for value in values]
    first = residues[0]
    for residue in residues[1:]:
        if abs(residue - first) > 1e-6:
            return None
    return round(first, 6)


def _normalized_remainder(value: float, grid_units: float) -> float:
    residue = value % grid_units
    if abs(residue - grid_units) < 1e-6 or abs(residue) < 1e-6:
        return 0.0
    return residue


def _nearest_value_with_remainder(value: float, remainder: float, grid_units: float) -> float:
    multiplier = round((value - remainder) / grid_units)
    return remainder + (multiplier * grid_units)


def _distance_to_grid(value: float, grid_mils: float) -> float:
    residue = abs(value) % grid_mils
    return min(residue, grid_mils - residue)


def _easyeda_bounds(easyeda_symbol: EasyEdaSymbol) -> tuple[_EePoint, _EePoint]:
    xs: list[float] = []
    ys: list[float] = []

    for pin in easyeda_symbol.pins:
        points = [_EePoint(pin.dot_x, pin.dot_y), _EePoint(pin.x, pin.y)]
        points.extend(_parse_path_points(pin.path_string))
        for point in points:
            xs.append(point.x)
            ys.append(point.y)

    for rect in easyeda_symbol.rectangles:
        xs.extend([rect.x, rect.x + rect.width])
        ys.extend([rect.y, rect.y + rect.height])
    for circle in easyeda_symbol.circles:
        xs.extend([circle.cx - circle.radius, circle.cx + circle.radius])
        ys.extend([circle.cy - circle.radius, circle.cy + circle.radius])
    for ellipse in easyeda_symbol.ellipses:
        xs.extend([ellipse.cx - ellipse.rx, ellipse.cx + ellipse.rx])
        ys.extend([ellipse.cy - ellipse.ry, ellipse.cy + ellipse.ry])
    for polyline in easyeda_symbol.polylines:
        for x, y in polyline.points:
            xs.append(x)
            ys.append(y)
    for polygon in easyeda_symbol.polygons:
        for x, y in polygon.points:
            xs.append(x)
            ys.append(y)

    if not xs or not ys:
        return _EePoint(0.0, 0.0), _EePoint(0.0, 0.0)
    return _EePoint(min(xs), min(ys)), _EePoint(max(xs), max(ys))


def _transform_vertices(
    points: list[tuple[float, float]],
    transform: _SymbolTransform,
) -> list[tuple[int, int]]:
    return [
        (int(round(point.x)), int(round(point.y)))
        for point in (transform.point(_EePoint(x, y)) for x, y in points)
    ]


def _distance(left: _EePoint, right: _EePoint) -> float:
    return math.hypot(left.x - right.x, left.y - right.y)


def _hex_to_win32(value: str, *, default: int) -> int:
    text = (value or "").strip()
    if _is_no_fill(text):
        return default
    if text.startswith("#"):
        text = text[1:]
    if len(text) == 3:
        text = "".join(ch * 2 for ch in text)
    if len(text) != 6:
        return default
    try:
        red = int(text[0:2], 16)
        green = int(text[2:4], 16)
        blue = int(text[4:6], 16)
    except ValueError:
        return default
    return (blue << 16) | (green << 8) | red


def _is_no_fill(value: str) -> bool:
    return (value or "").strip().lower() in {"", "none", "transparent"}
