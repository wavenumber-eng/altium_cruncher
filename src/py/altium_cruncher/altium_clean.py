"""Cleanup transforms used by the altium-cruncher clean workflow."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from altium_monkey.altium_sch_enums import PinItemMode
from altium_monkey.altium_font_manager import FontIDManager
from altium_monkey.altium_record_sch__arc import AltiumSchArc
from altium_monkey.altium_record_sch__designator import AltiumSchDesignator
from altium_monkey.altium_record_sch__label import AltiumSchLabel
from altium_monkey.altium_record_sch__line import AltiumSchLine
from altium_monkey.altium_record_sch__net_label import AltiumSchNetLabel
from altium_monkey.altium_record_sch__no_erc import AltiumSchNoErc, NoErcSymbol
from altium_monkey.altium_record_sch__parameter import AltiumSchParameter
from altium_monkey.altium_record_sch__pin import AltiumSchPin
from altium_monkey.altium_record_sch__polygon import AltiumSchPolygon
from altium_monkey.altium_record_sch__polyline import AltiumSchPolyline
from altium_monkey.altium_record_sch__power_port import AltiumSchPowerPort
from altium_monkey.altium_record_sch__rectangle import AltiumSchRectangle
from altium_monkey.altium_record_sch__wire import AltiumSchWire
from altium_monkey.altium_record_types import LineWidth, SchGraphicalObject, rgb_to_win32_color

CLEAN_CONFIG_SCHEMA_V1 = "wn.altium.clean.config.v1"


def _coerce_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "on"}:
            return True
        if normalized in {"0", "false", "no", "off"}:
            return False
    raise ValueError(f"Invalid boolean value in clean config: {value!r}")


def _coerce_int(value: Any, *, field_name: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid integer for clean config field '{field_name}': {value!r}") from exc


def _coerce_float(value: Any, *, field_name: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid numeric value for clean config field '{field_name}': {value!r}") from exc


def _coerce_non_empty_str(value: Any, *, field_name: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"Missing required clean config field '{field_name}'")
    return text


def _coerce_color(value: Any, *, field_name: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"Invalid color for clean config field '{field_name}': {value!r}")

    if isinstance(value, (int, float)):
        color = int(value)
    elif isinstance(value, str):
        text = value.strip()
        if not text:
            raise ValueError(f"Invalid color for clean config field '{field_name}': {value!r}")
        if text.startswith("#"):
            rgb_text = text[1:]
            if len(rgb_text) != 6:
                raise ValueError(
                    f"Invalid hex color for clean config field '{field_name}': {value!r}. Expected #RRGGBB"
                )
            try:
                r = int(rgb_text[0:2], 16)
                g = int(rgb_text[2:4], 16)
                b = int(rgb_text[4:6], 16)
            except ValueError as exc:
                raise ValueError(
                    f"Invalid hex color for clean config field '{field_name}': {value!r}. Expected #RRGGBB"
                ) from exc
            color = rgb_to_win32_color(r, g, b)
        else:
            try:
                color = int(text, 0)
            except ValueError as exc:
                raise ValueError(f"Invalid color for clean config field '{field_name}': {value!r}") from exc
    else:
        raise ValueError(f"Invalid color for clean config field '{field_name}': {value!r}")

    if color < 0 or color > 0xFFFFFF:
        raise ValueError(
            f"Color out of range for clean config field '{field_name}': {color}. Expected 0x000000..0xFFFFFF"
        )
    return color


def _coerce_line_width(value: Any, *, field_name: str) -> LineWidth:
    if value is None:
        return LineWidth.SMALL
    if isinstance(value, LineWidth):
        return value
    if isinstance(value, (int, float)):
        try:
            return LineWidth(int(value))
        except ValueError as exc:
            raise ValueError(f"Invalid line width for clean config field '{field_name}': {value!r}") from exc
    if isinstance(value, str):
        text = value.strip().lower()
        mapping = {
            "smallest": LineWidth.SMALLEST,
            "zero": LineWidth.SMALLEST,
            "small": LineWidth.SMALL,
            "medium": LineWidth.MEDIUM,
            "large": LineWidth.LARGE,
        }
        if text in mapping:
            return mapping[text]
    raise ValueError(f"Invalid line width for clean config field '{field_name}': {value!r}")


def _coerce_no_erc_symbol(value: Any, *, field_name: str) -> NoErcSymbol:
    if value is None:
        return NoErcSymbol.CROSS_SMALL
    if isinstance(value, NoErcSymbol):
        return value
    if isinstance(value, bool):
        raise ValueError(f"Invalid no-erc symbol for clean config field '{field_name}': {value!r}")
    if isinstance(value, (int, float)):
        try:
            return NoErcSymbol(int(value))
        except ValueError as exc:
            raise ValueError(f"Invalid no-erc symbol for clean config field '{field_name}': {value!r}") from exc
    if isinstance(value, str):
        text = value.strip().lower().replace("-", " ").replace("_", " ")
        mapping = {
            "cross": NoErcSymbol.CROSS,
            "thick cross": NoErcSymbol.CROSS,
            "cross thick": NoErcSymbol.CROSS,
            "thin cross": NoErcSymbol.CROSS_THIN,
            "cross thin": NoErcSymbol.CROSS_THIN,
            "small cross": NoErcSymbol.CROSS_SMALL,
            "cross small": NoErcSymbol.CROSS_SMALL,
            "checkbox": NoErcSymbol.CHECKBOX,
            "check box": NoErcSymbol.CHECKBOX,
            "triangle": NoErcSymbol.TRIANGLE,
        }
        if text in mapping:
            return mapping[text]
        try:
            return NoErcSymbol(int(text, 0))
        except ValueError as exc:
            raise ValueError(f"Invalid no-erc symbol for clean config field '{field_name}': {value!r}") from exc
    raise ValueError(f"Invalid no-erc symbol for clean config field '{field_name}': {value!r}")


@dataclass(slots=True)
class CleanFontSpec:
    font_name: str
    size_pt: int
    bold: bool = False
    italic: bool = False
    color_win32: int | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any], *, field_name: str) -> CleanFontSpec:
        if not isinstance(data, dict):
            raise ValueError(f"Clean config field '{field_name}' must be an object")
        color_raw = data.get("color_win32", data.get("color"))
        return cls(
            font_name=_coerce_non_empty_str(data.get("font_name", data.get("font")), field_name=f"{field_name}.font_name"),
            size_pt=_coerce_int(data.get("size_pt", data.get("size")), field_name=f"{field_name}.size_pt"),
            bold=_coerce_bool(data.get("bold"), False),
            italic=_coerce_bool(data.get("italic"), False),
            color_win32=_coerce_color(color_raw, field_name=f"{field_name}.color") if color_raw is not None else None,
        )

    def to_dict(self, *, include_color: bool = True) -> dict[str, Any]:
        payload = {
            "font_name": self.font_name,
            "size_pt": self.size_pt,
            "bold": self.bold,
            "italic": self.italic,
        }
        if include_color:
            payload["color_win32"] = self.color_win32
        return payload

def _default_component_designator_font() -> CleanFontSpec:
    return CleanFontSpec(font_name="Arial", size_pt=12, bold=True, italic=False, color_win32=0x000000)


def _default_component_parameter_font() -> CleanFontSpec:
    return CleanFontSpec(font_name="Arial", size_pt=10, bold=False, italic=False, color_win32=0x000000)


def _default_sheet_document_font() -> CleanFontSpec:
    return CleanFontSpec(font_name="Times New Roman", size_pt=10, bold=False, italic=False)


@dataclass(slots=True)
class PinFontNormalizationConfig:
    enabled: bool = True
    name_font: CleanFontSpec | None = None
    designator_font: CleanFontSpec | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> PinFontNormalizationConfig:
        if data is None:
            return cls()
        if not isinstance(data, dict):
            raise ValueError("Clean config field 'normalize_pin_fonts' must be an object")

        name_font_raw = data.get("name_font", data.get("name"))
        designator_font_raw = data.get("designator_font", data.get("designator"))
        name_font = CleanFontSpec.from_dict(name_font_raw, field_name="normalize_pin_fonts.name_font") if name_font_raw else None
        designator_font = (
            CleanFontSpec.from_dict(designator_font_raw, field_name="normalize_pin_fonts.designator_font")
            if designator_font_raw
            else None
        )
        return cls(
            enabled=_coerce_bool(data.get("enabled"), True),
            name_font=name_font,
            designator_font=designator_font,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "name_font": self.name_font.to_dict() if self.name_font else None,
            "designator_font": self.designator_font.to_dict() if self.designator_font else None,
        }


@dataclass(slots=True)
class SymbolBodyRectangleNormalizationConfig:
    enabled: bool = True
    min_width_mils: float = 40.0
    min_height_mils: float = 40.0
    outline_color_win32: int = 0x000000
    line_width: LineWidth = LineWidth.SMALL
    fill_color_win32: int = 0xFFFFFF
    is_solid: bool = True
    transparent: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> SymbolBodyRectangleNormalizationConfig:
        if data is None:
            return cls()
        if not isinstance(data, dict):
            raise ValueError("Clean config field 'normalize_symbol_body_rectangles' must be an object")

        min_width_mils = _coerce_float(data.get("min_width_mils", 40.0), field_name="normalize_symbol_body_rectangles.min_width_mils")
        min_height_mils = _coerce_float(
            data.get("min_height_mils", 40.0),
            field_name="normalize_symbol_body_rectangles.min_height_mils",
        )
        if min_width_mils < 0:
            raise ValueError("normalize_symbol_body_rectangles.min_width_mils must be >= 0")
        if min_height_mils < 0:
            raise ValueError("normalize_symbol_body_rectangles.min_height_mils must be >= 0")

        return cls(
            enabled=_coerce_bool(data.get("enabled"), True),
            min_width_mils=min_width_mils,
            min_height_mils=min_height_mils,
            outline_color_win32=_coerce_color(
                data.get("outline_color_win32", data.get("outline_color", data.get("color", "#000000"))),
                field_name="normalize_symbol_body_rectangles.outline_color",
            ),
            line_width=_coerce_line_width(
                data.get("line_width", "small"),
                field_name="normalize_symbol_body_rectangles.line_width",
            ),
            fill_color_win32=_coerce_color(
                data.get("fill_color_win32", data.get("fill_color", data.get("area_color", "#FFFFFF"))),
                field_name="normalize_symbol_body_rectangles.fill_color",
            ),
            is_solid=_coerce_bool(data.get("is_solid"), True),
            transparent=_coerce_bool(data.get("transparent"), False),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "min_width_mils": self.min_width_mils,
            "min_height_mils": self.min_height_mils,
            "outline_color_win32": self.outline_color_win32,
            "line_width": self.line_width.name.lower(),
            "fill_color_win32": self.fill_color_win32,
            "is_solid": self.is_solid,
            "transparent": self.transparent,
        }


@dataclass(slots=True)
class PowerSymbolNormalizationConfig:
    enabled: bool = True
    color_win32: int = 0x000000
    font_name: str = "Arial"
    size_pt: int = 10
    bold: bool = True
    italic: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> PowerSymbolNormalizationConfig:
        if data is None:
            return cls()
        if not isinstance(data, dict):
            raise ValueError("Clean config field 'normalize_power_symbols' must be an object")

        font_data = data.get("font")
        if font_data is not None and not isinstance(font_data, dict):
            raise ValueError("Clean config field 'normalize_power_symbols.font' must be an object")

        font_payload = font_data or {}
        font_name = _coerce_non_empty_str(
            font_payload.get("font_name", font_payload.get("font", "Arial")),
            field_name="normalize_power_symbols.font.font_name",
        )
        size_pt = _coerce_int(
            font_payload.get("size_pt", font_payload.get("size", 10)),
            field_name="normalize_power_symbols.font.size_pt",
        )
        return cls(
            enabled=_coerce_bool(data.get("enabled"), True),
            color_win32=_coerce_color(
                data.get("color_win32", data.get("color", "#000000")),
                field_name="normalize_power_symbols.color",
            ),
            font_name=font_name,
            size_pt=size_pt,
            bold=_coerce_bool(font_payload.get("bold"), True),
            italic=_coerce_bool(font_payload.get("italic"), False),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "color_win32": self.color_win32,
            "font": {
                "font_name": self.font_name,
                "size_pt": self.size_pt,
                "bold": self.bold,
                "italic": self.italic,
            },
        }


@dataclass(slots=True)
class NetLabelNormalizationConfig:
    enabled: bool = True
    color_win32: int = 0x000000
    font_name: str = "Arial"
    size_pt: int = 8
    bold: bool = True
    italic: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> NetLabelNormalizationConfig:
        if data is None:
            return cls()
        if not isinstance(data, dict):
            raise ValueError("Clean config field 'normalize_net_labels' must be an object")

        font_data = data.get("font")
        if font_data is not None and not isinstance(font_data, dict):
            raise ValueError("Clean config field 'normalize_net_labels.font' must be an object")
        font_payload = font_data or {}

        return cls(
            enabled=_coerce_bool(data.get("enabled"), True),
            color_win32=_coerce_color(
                data.get("color_win32", data.get("color", "#000000")),
                field_name="normalize_net_labels.color",
            ),
            font_name=_coerce_non_empty_str(
                font_payload.get("font_name", font_payload.get("font", "Arial")),
                field_name="normalize_net_labels.font.font_name",
            ),
            size_pt=_coerce_int(
                font_payload.get("size_pt", font_payload.get("size", 8)),
                field_name="normalize_net_labels.font.size_pt",
            ),
            bold=_coerce_bool(font_payload.get("bold"), True),
            italic=_coerce_bool(font_payload.get("italic"), False),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "color_win32": self.color_win32,
            "font": {
                "font_name": self.font_name,
                "size_pt": self.size_pt,
                "bold": self.bold,
                "italic": self.italic,
            },
        }


@dataclass(slots=True)
class ComponentDesignatorNormalizationConfig:
    enabled: bool = True
    font: CleanFontSpec = field(default_factory=_default_component_designator_font)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> ComponentDesignatorNormalizationConfig:
        if data is None:
            return cls()
        if not isinstance(data, dict):
            raise ValueError("Clean config field 'normalize_component_designators' must be an object")

        font_data = data.get("font")
        if font_data is not None and not isinstance(font_data, dict):
            raise ValueError("Clean config field 'normalize_component_designators.font' must be an object")

        return cls(
            enabled=_coerce_bool(data.get("enabled"), True),
            font=(
                CleanFontSpec.from_dict(font_data, field_name="normalize_component_designators.font")
                if font_data
                else _default_component_designator_font()
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "font": self.font.to_dict(),
        }


@dataclass(slots=True)
class ComponentParameterNormalizationConfig:
    enabled: bool = True
    font: CleanFontSpec = field(default_factory=_default_component_parameter_font)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> ComponentParameterNormalizationConfig:
        if data is None:
            return cls()
        if not isinstance(data, dict):
            raise ValueError("Clean config field 'normalize_component_parameters' must be an object")

        font_data = data.get("font")
        if font_data is not None and not isinstance(font_data, dict):
            raise ValueError("Clean config field 'normalize_component_parameters.font' must be an object")

        return cls(
            enabled=_coerce_bool(data.get("enabled"), True),
            font=(
                CleanFontSpec.from_dict(font_data, field_name="normalize_component_parameters.font")
                if font_data
                else _default_component_parameter_font()
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "font": self.font.to_dict(),
        }


@dataclass(slots=True)
class SheetStyleNormalizationConfig:
    enabled: bool = True
    line_color_win32: int = 0x000000
    area_color_win32: int = 0xFFFFFF
    document_font: CleanFontSpec = field(default_factory=_default_sheet_document_font)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> SheetStyleNormalizationConfig:
        if data is None:
            return cls()
        if not isinstance(data, dict):
            raise ValueError("Clean config field 'normalize_sheet_style' must be an object")

        document_font_raw = data.get("document_font", data.get("font"))
        if document_font_raw is not None and not isinstance(document_font_raw, dict):
            raise ValueError("Clean config field 'normalize_sheet_style.document_font' must be an object")

        return cls(
            enabled=_coerce_bool(data.get("enabled"), True),
            line_color_win32=_coerce_color(
                data.get("line_color_win32", data.get("line_color", data.get("color", "#000000"))),
                field_name="normalize_sheet_style.line_color",
            ),
            area_color_win32=_coerce_color(
                data.get("area_color_win32", data.get("area_color", "#FFFFFF")),
                field_name="normalize_sheet_style.area_color",
            ),
            document_font=(
                CleanFontSpec.from_dict(document_font_raw, field_name="normalize_sheet_style.document_font")
                if document_font_raw
                else _default_sheet_document_font()
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "line_color_win32": self.line_color_win32,
            "area_color_win32": self.area_color_win32,
            "document_font": self.document_font.to_dict(include_color=False),
        }


@dataclass(slots=True)
class ComponentFreeTextNormalizationConfig:
    enabled: bool = True
    font_name: str = "Arial"
    color_win32: int = 0x000000

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> ComponentFreeTextNormalizationConfig:
        if data is None:
            return cls()
        if not isinstance(data, dict):
            raise ValueError("Clean config field 'normalize_component_free_text' must be an object")
        return cls(
            enabled=_coerce_bool(data.get("enabled"), True),
            font_name=_coerce_non_empty_str(
                data.get("font_name", data.get("font", "Arial")),
                field_name="normalize_component_free_text.font_name",
            ),
            color_win32=_coerce_color(
                data.get("color_win32", data.get("color", "#000000")),
                field_name="normalize_component_free_text.color",
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "font_name": self.font_name,
            "color_win32": self.color_win32,
        }


@dataclass(slots=True)
class WireNormalizationConfig:
    enabled: bool = True
    color_win32: int = 0x434343

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> WireNormalizationConfig:
        if data is None:
            return cls()
        if not isinstance(data, dict):
            raise ValueError("Clean config field 'normalize_wires' must be an object")
        return cls(
            enabled=_coerce_bool(data.get("enabled"), True),
            color_win32=_coerce_color(
                data.get("color_win32", data.get("color", "#434343")),
                field_name="normalize_wires.color",
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "color_win32": self.color_win32,
        }


@dataclass(slots=True)
class NoErcNormalizationConfig:
    enabled: bool = True
    color_win32: int = 0x000000
    symbol: NoErcSymbol = NoErcSymbol.CROSS_SMALL

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> NoErcNormalizationConfig:
        if data is None:
            return cls()
        if not isinstance(data, dict):
            raise ValueError("Clean config field 'normalize_no_erc' must be an object")
        return cls(
            enabled=_coerce_bool(data.get("enabled"), True),
            color_win32=_coerce_color(
                data.get("color_win32", data.get("color", "#000000")),
                field_name="normalize_no_erc.color",
            ),
            symbol=_coerce_no_erc_symbol(
                data.get("symbol", data.get("style", "small_cross")),
                field_name="normalize_no_erc.symbol",
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "color_win32": self.color_win32,
            "symbol": self.symbol.name.lower(),
        }


@dataclass(slots=True)
class SymbolInternalGraphicsMonochromeConfig:
    enabled: bool = True
    saturation: float = 0.0

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> SymbolInternalGraphicsMonochromeConfig:
        if data is None:
            return cls()
        if not isinstance(data, dict):
            raise ValueError("Clean config field 'normalize_symbol_internal_graphics_monochrome' must be an object")

        saturation = _coerce_float(
            data.get("saturation", 0.0),
            field_name="normalize_symbol_internal_graphics_monochrome.saturation",
        )
        if saturation < 0.0 or saturation > 1.0:
            raise ValueError("normalize_symbol_internal_graphics_monochrome.saturation must be in range [0.0, 1.0]")

        return cls(
            enabled=_coerce_bool(data.get("enabled"), True),
            saturation=saturation,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "saturation": self.saturation,
        }


@dataclass(slots=True)
class AltiumCleanConfig:
    schema: str = CLEAN_CONFIG_SCHEMA_V1
    normalize_pin_fonts: PinFontNormalizationConfig = field(default_factory=PinFontNormalizationConfig)
    normalize_symbol_body_rectangles: SymbolBodyRectangleNormalizationConfig = field(
        default_factory=SymbolBodyRectangleNormalizationConfig
    )
    normalize_power_symbols: PowerSymbolNormalizationConfig = field(default_factory=PowerSymbolNormalizationConfig)
    normalize_net_labels: NetLabelNormalizationConfig = field(default_factory=NetLabelNormalizationConfig)
    normalize_component_designators: ComponentDesignatorNormalizationConfig = field(
        default_factory=ComponentDesignatorNormalizationConfig
    )
    normalize_component_parameters: ComponentParameterNormalizationConfig = field(
        default_factory=ComponentParameterNormalizationConfig
    )
    normalize_component_free_text: ComponentFreeTextNormalizationConfig = field(
        default_factory=ComponentFreeTextNormalizationConfig
    )
    normalize_wires: WireNormalizationConfig = field(default_factory=WireNormalizationConfig)
    normalize_no_erc: NoErcNormalizationConfig = field(default_factory=NoErcNormalizationConfig)
    normalize_sheet_style: SheetStyleNormalizationConfig = field(default_factory=SheetStyleNormalizationConfig)
    normalize_symbol_internal_graphics_monochrome: SymbolInternalGraphicsMonochromeConfig = field(
        default_factory=SymbolInternalGraphicsMonochromeConfig
    )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AltiumCleanConfig:
        if not isinstance(data, dict):
            raise ValueError("Clean config must be a JSON object")
        schema = str(data.get("schema", CLEAN_CONFIG_SCHEMA_V1) or CLEAN_CONFIG_SCHEMA_V1).strip()
        if schema != CLEAN_CONFIG_SCHEMA_V1:
            raise ValueError(f"Unsupported clean config schema: {schema!r}")
        return cls(
            schema=schema,
            normalize_pin_fonts=PinFontNormalizationConfig.from_dict(data.get("normalize_pin_fonts")),
            normalize_symbol_body_rectangles=SymbolBodyRectangleNormalizationConfig.from_dict(
                data.get("normalize_symbol_body_rectangles")
            ),
            normalize_power_symbols=PowerSymbolNormalizationConfig.from_dict(data.get("normalize_power_symbols")),
            normalize_net_labels=NetLabelNormalizationConfig.from_dict(data.get("normalize_net_labels")),
            normalize_component_designators=ComponentDesignatorNormalizationConfig.from_dict(
                data.get("normalize_component_designators")
            ),
            normalize_component_parameters=ComponentParameterNormalizationConfig.from_dict(
                data.get("normalize_component_parameters")
            ),
            normalize_component_free_text=ComponentFreeTextNormalizationConfig.from_dict(
                data.get("normalize_component_free_text")
            ),
            normalize_wires=WireNormalizationConfig.from_dict(data.get("normalize_wires")),
            normalize_no_erc=NoErcNormalizationConfig.from_dict(data.get("normalize_no_erc")),
            normalize_sheet_style=SheetStyleNormalizationConfig.from_dict(data.get("normalize_sheet_style")),
            normalize_symbol_internal_graphics_monochrome=SymbolInternalGraphicsMonochromeConfig.from_dict(
                data.get("normalize_symbol_internal_graphics_monochrome")
            ),
        )

    @classmethod
    def template(cls) -> AltiumCleanConfig:
        return cls(
            schema=CLEAN_CONFIG_SCHEMA_V1,
            normalize_pin_fonts=PinFontNormalizationConfig(
                enabled=True,
                name_font=CleanFontSpec(font_name="Arial", size_pt=10, color_win32=0x000000),
                designator_font=CleanFontSpec(font_name="Arial", size_pt=10, color_win32=0x000000),
            ),
            normalize_symbol_body_rectangles=SymbolBodyRectangleNormalizationConfig(
                enabled=True,
                min_width_mils=40.0,
                min_height_mils=40.0,
                outline_color_win32=0x000000,
                line_width=LineWidth.SMALL,
                fill_color_win32=0xFFFFFF,
                is_solid=True,
                transparent=False,
            ),
            normalize_power_symbols=PowerSymbolNormalizationConfig(
                enabled=True,
                color_win32=0x000000,
                font_name="Arial",
                size_pt=10,
                bold=True,
                italic=False,
            ),
            normalize_net_labels=NetLabelNormalizationConfig(
                enabled=True,
                color_win32=0x000000,
                font_name="Arial",
                size_pt=8,
                bold=True,
                italic=False,
            ),
            normalize_component_designators=ComponentDesignatorNormalizationConfig(
                enabled=True,
                font=_default_component_designator_font(),
            ),
            normalize_component_parameters=ComponentParameterNormalizationConfig(
                enabled=True,
                font=_default_component_parameter_font(),
            ),
            normalize_component_free_text=ComponentFreeTextNormalizationConfig(
                enabled=True,
                font_name="Arial",
                color_win32=0x000000,
            ),
            normalize_wires=WireNormalizationConfig(
                enabled=True,
                color_win32=0x434343,
            ),
            normalize_no_erc=NoErcNormalizationConfig(
                enabled=True,
                color_win32=0x000000,
                symbol=NoErcSymbol.CROSS_SMALL,
            ),
            normalize_sheet_style=SheetStyleNormalizationConfig(
                enabled=True,
                line_color_win32=0x000000,
                area_color_win32=0xFFFFFF,
                document_font=_default_sheet_document_font(),
            ),
            normalize_symbol_internal_graphics_monochrome=SymbolInternalGraphicsMonochromeConfig(
                enabled=True,
                saturation=0.0,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "normalize_pin_fonts": self.normalize_pin_fonts.to_dict(),
            "normalize_symbol_body_rectangles": self.normalize_symbol_body_rectangles.to_dict(),
            "normalize_power_symbols": self.normalize_power_symbols.to_dict(),
            "normalize_net_labels": self.normalize_net_labels.to_dict(),
            "normalize_component_designators": self.normalize_component_designators.to_dict(),
            "normalize_component_parameters": self.normalize_component_parameters.to_dict(),
            "normalize_component_free_text": self.normalize_component_free_text.to_dict(),
            "normalize_wires": self.normalize_wires.to_dict(),
            "normalize_no_erc": self.normalize_no_erc.to_dict(),
            "normalize_sheet_style": self.normalize_sheet_style.to_dict(),
            "normalize_symbol_internal_graphics_monochrome": self.normalize_symbol_internal_graphics_monochrome.to_dict(),
        }


@dataclass(slots=True)
class PinFontNormalizationResult:
    total_pins: int = 0
    updated_name_fonts: int = 0
    updated_designator_fonts: int = 0

    @property
    def changed(self) -> bool:
        return (self.updated_name_fonts + self.updated_designator_fonts) > 0


@dataclass(slots=True)
class SymbolBodyRectangleNormalizationResult:
    total_rectangles: int = 0
    matched_rectangles: int = 0
    updated_rectangles: int = 0
    reordered_rectangles: int = 0

    @property
    def changed(self) -> bool:
        return self.updated_rectangles > 0 or self.reordered_rectangles > 0


@dataclass(slots=True)
class PowerSymbolNormalizationResult:
    total_power_symbols: int = 0
    updated_power_symbol_colors: int = 0
    updated_power_symbol_fonts: int = 0

    @property
    def changed(self) -> bool:
        return (self.updated_power_symbol_colors + self.updated_power_symbol_fonts) > 0


@dataclass(slots=True)
class NetLabelNormalizationResult:
    total_net_labels: int = 0
    updated_net_label_colors: int = 0
    updated_net_label_fonts: int = 0

    @property
    def changed(self) -> bool:
        return (self.updated_net_label_colors + self.updated_net_label_fonts) > 0


@dataclass(slots=True)
class ComponentDesignatorNormalizationResult:
    total_component_designators: int = 0
    updated_component_designator_colors: int = 0
    updated_component_designator_fonts: int = 0

    @property
    def changed(self) -> bool:
        return (self.updated_component_designator_colors + self.updated_component_designator_fonts) > 0


@dataclass(slots=True)
class ComponentParameterNormalizationResult:
    total_component_parameters: int = 0
    updated_component_parameter_colors: int = 0
    updated_component_parameter_fonts: int = 0

    @property
    def changed(self) -> bool:
        return (self.updated_component_parameter_colors + self.updated_component_parameter_fonts) > 0


@dataclass(slots=True)
class ComponentFreeTextNormalizationResult:
    total_component_free_texts: int = 0
    updated_component_free_text_colors: int = 0
    updated_component_free_text_fonts: int = 0

    @property
    def changed(self) -> bool:
        return (self.updated_component_free_text_colors + self.updated_component_free_text_fonts) > 0


@dataclass(slots=True)
class WireNormalizationResult:
    total_wires: int = 0
    updated_wire_colors: int = 0

    @property
    def changed(self) -> bool:
        return self.updated_wire_colors > 0


@dataclass(slots=True)
class NoErcNormalizationResult:
    total_no_ercs: int = 0
    updated_no_erc_colors: int = 0
    updated_no_erc_symbols: int = 0

    @property
    def changed(self) -> bool:
        return (self.updated_no_erc_colors + self.updated_no_erc_symbols) > 0


@dataclass(slots=True)
class SheetStyleNormalizationResult:
    total_sheets: int = 0
    updated_sheet_line_colors: int = 0
    updated_sheet_area_colors: int = 0
    updated_sheet_document_fonts: int = 0

    @property
    def changed(self) -> bool:
        return (
            self.updated_sheet_line_colors + self.updated_sheet_area_colors + self.updated_sheet_document_fonts
        ) > 0


@dataclass(slots=True)
class SymbolInternalGraphicsMonochromeResult:
    total_symbol_internal_graphics: int = 0
    updated_symbol_internal_graphic_stroke_colors: int = 0
    updated_symbol_internal_graphic_fill_colors: int = 0

    @property
    def changed(self) -> bool:
        return (
            self.updated_symbol_internal_graphic_stroke_colors + self.updated_symbol_internal_graphic_fill_colors
        ) > 0


@dataclass(slots=True)
class CleanApplyResult:
    total_pins: int = 0
    updated_name_fonts: int = 0
    updated_designator_fonts: int = 0
    total_rectangles: int = 0
    matched_rectangles: int = 0
    updated_rectangles: int = 0
    reordered_rectangles: int = 0
    total_power_symbols: int = 0
    updated_power_symbol_colors: int = 0
    updated_power_symbol_fonts: int = 0
    total_net_labels: int = 0
    updated_net_label_colors: int = 0
    updated_net_label_fonts: int = 0
    total_component_designators: int = 0
    updated_component_designator_colors: int = 0
    updated_component_designator_fonts: int = 0
    total_component_parameters: int = 0
    updated_component_parameter_colors: int = 0
    updated_component_parameter_fonts: int = 0
    total_component_free_texts: int = 0
    updated_component_free_text_colors: int = 0
    updated_component_free_text_fonts: int = 0
    total_wires: int = 0
    updated_wire_colors: int = 0
    total_no_ercs: int = 0
    updated_no_erc_colors: int = 0
    updated_no_erc_symbols: int = 0
    total_sheets: int = 0
    updated_sheet_line_colors: int = 0
    updated_sheet_area_colors: int = 0
    updated_sheet_document_fonts: int = 0
    total_symbol_internal_graphics: int = 0
    updated_symbol_internal_graphic_stroke_colors: int = 0
    updated_symbol_internal_graphic_fill_colors: int = 0

    @property
    def changed(self) -> bool:
        return (
            self.updated_name_fonts > 0
            or self.updated_designator_fonts > 0
            or self.updated_rectangles > 0
            or self.reordered_rectangles > 0
            or self.updated_power_symbol_colors > 0
            or self.updated_power_symbol_fonts > 0
            or self.updated_net_label_colors > 0
            or self.updated_net_label_fonts > 0
            or self.updated_component_designator_colors > 0
            or self.updated_component_designator_fonts > 0
            or self.updated_component_parameter_colors > 0
            or self.updated_component_parameter_fonts > 0
            or self.updated_component_free_text_colors > 0
            or self.updated_component_free_text_fonts > 0
            or self.updated_wire_colors > 0
            or self.updated_no_erc_colors > 0
            or self.updated_no_erc_symbols > 0
            or self.updated_sheet_line_colors > 0
            or self.updated_sheet_area_colors > 0
            or self.updated_sheet_document_fonts > 0
            or self.updated_symbol_internal_graphic_stroke_colors > 0
            or self.updated_symbol_internal_graphic_fill_colors > 0
        )

    @classmethod
    def from_parts(
        cls,
        pin_result: PinFontNormalizationResult,
        rect_result: SymbolBodyRectangleNormalizationResult,
        power_result: PowerSymbolNormalizationResult | None = None,
        net_label_result: NetLabelNormalizationResult | None = None,
        component_designator_result: ComponentDesignatorNormalizationResult | None = None,
        component_parameter_result: ComponentParameterNormalizationResult | None = None,
        component_free_text_result: ComponentFreeTextNormalizationResult | None = None,
        wire_result: WireNormalizationResult | None = None,
        no_erc_result: NoErcNormalizationResult | None = None,
        sheet_style_result: SheetStyleNormalizationResult | None = None,
        symbol_internal_graphics_result: SymbolInternalGraphicsMonochromeResult | None = None,
    ) -> CleanApplyResult:
        effective_power = power_result or PowerSymbolNormalizationResult()
        effective_net_label = net_label_result or NetLabelNormalizationResult()
        effective_component_designator = component_designator_result or ComponentDesignatorNormalizationResult()
        effective_component_parameter = component_parameter_result or ComponentParameterNormalizationResult()
        effective_component_free_text = component_free_text_result or ComponentFreeTextNormalizationResult()
        effective_wire = wire_result or WireNormalizationResult()
        effective_no_erc = no_erc_result or NoErcNormalizationResult()
        effective_sheet_style = sheet_style_result or SheetStyleNormalizationResult()
        effective_symbol_graphics = symbol_internal_graphics_result or SymbolInternalGraphicsMonochromeResult()
        return cls(
            total_pins=pin_result.total_pins,
            updated_name_fonts=pin_result.updated_name_fonts,
            updated_designator_fonts=pin_result.updated_designator_fonts,
            total_rectangles=rect_result.total_rectangles,
            matched_rectangles=rect_result.matched_rectangles,
            updated_rectangles=rect_result.updated_rectangles,
            reordered_rectangles=rect_result.reordered_rectangles,
            total_power_symbols=effective_power.total_power_symbols,
            updated_power_symbol_colors=effective_power.updated_power_symbol_colors,
            updated_power_symbol_fonts=effective_power.updated_power_symbol_fonts,
            total_net_labels=effective_net_label.total_net_labels,
            updated_net_label_colors=effective_net_label.updated_net_label_colors,
            updated_net_label_fonts=effective_net_label.updated_net_label_fonts,
            total_component_designators=effective_component_designator.total_component_designators,
            updated_component_designator_colors=effective_component_designator.updated_component_designator_colors,
            updated_component_designator_fonts=effective_component_designator.updated_component_designator_fonts,
            total_component_parameters=effective_component_parameter.total_component_parameters,
            updated_component_parameter_colors=effective_component_parameter.updated_component_parameter_colors,
            updated_component_parameter_fonts=effective_component_parameter.updated_component_parameter_fonts,
            total_component_free_texts=effective_component_free_text.total_component_free_texts,
            updated_component_free_text_colors=effective_component_free_text.updated_component_free_text_colors,
            updated_component_free_text_fonts=effective_component_free_text.updated_component_free_text_fonts,
            total_wires=effective_wire.total_wires,
            updated_wire_colors=effective_wire.updated_wire_colors,
            total_no_ercs=effective_no_erc.total_no_ercs,
            updated_no_erc_colors=effective_no_erc.updated_no_erc_colors,
            updated_no_erc_symbols=effective_no_erc.updated_no_erc_symbols,
            total_sheets=effective_sheet_style.total_sheets,
            updated_sheet_line_colors=effective_sheet_style.updated_sheet_line_colors,
            updated_sheet_area_colors=effective_sheet_style.updated_sheet_area_colors,
            updated_sheet_document_fonts=effective_sheet_style.updated_sheet_document_fonts,
            total_symbol_internal_graphics=effective_symbol_graphics.total_symbol_internal_graphics,
            updated_symbol_internal_graphic_stroke_colors=effective_symbol_graphics.updated_symbol_internal_graphic_stroke_colors,
            updated_symbol_internal_graphic_fill_colors=effective_symbol_graphics.updated_symbol_internal_graphic_fill_colors,
        )


def _win32_to_rgb(color_win32: int) -> tuple[int, int, int]:
    red = color_win32 & 0xFF
    green = (color_win32 >> 8) & 0xFF
    blue = (color_win32 >> 16) & 0xFF
    return red, green, blue


def _is_win32_grayscale(color_win32: int) -> bool:
    red, green, blue = _win32_to_rgb(color_win32)
    return red == green == blue


def _normalize_monochrome_color(color_win32: int) -> int:
    # Preserve existing grayscale shades; force chromatic colors to black.
    if _is_win32_grayscale(color_win32):
        return color_win32
    return 0x000000


def _compute_margin_mils(pin: AltiumSchPin, *, for_name: bool) -> float | None:
    if for_name:
        margin_mils = getattr(pin, "_name_margin_mils", None)
        settings = pin.name_settings
    else:
        margin_mils = getattr(pin, "_designator_margin_mils", None)
        settings = pin.designator_settings
    if margin_mils is not None:
        return float(margin_mils)
    if settings.position_margin is None:
        return None
    return float(settings.position_margin * 10 + (settings.position_margin_frac or 0) / 10000.0)


def _apply_font_spec_to_pin(
    pin: AltiumSchPin,
    *,
    spec: CleanFontSpec,
    font_id: int,
    for_name: bool,
) -> bool:
    settings = pin.name_settings if for_name else pin.designator_settings
    changed = False

    if settings.font_mode != PinItemMode.CUSTOM:
        settings.font_mode = PinItemMode.CUSTOM
        changed = True
    if settings.font_id != font_id:
        settings.font_id = font_id
        changed = True

    # Keep unresolved style fields aligned with config for downstream builders/tools.
    if settings.font_name != spec.font_name:
        settings.font_name = spec.font_name
        changed = True
    if settings.font_size != spec.size_pt:
        settings.font_size = spec.size_pt
        changed = True
    if settings.font_bold != spec.bold:
        settings.font_bold = spec.bold
        changed = True
    if settings.font_italic != spec.italic:
        settings.font_italic = spec.italic
        changed = True
    if spec.color_win32 is not None and settings.color != spec.color_win32:
        settings.color = spec.color_win32
        changed = True

    # Persist current position margins in canonical fields so reserialization
    # can preserve custom-position records.
    if settings.position_mode == PinItemMode.CUSTOM:
        margin_mils = _compute_margin_mils(pin, for_name=for_name)
        if margin_mils is not None:
            internal_coord = int(round(margin_mils * 10000))
            margin_whole = internal_coord // 100000
            margin_frac = internal_coord % 100000
            if settings.position_margin != margin_whole:
                settings.position_margin = margin_whole
                changed = True
            if settings.position_margin_frac != margin_frac:
                settings.position_margin_frac = margin_frac
                changed = True
            if for_name:
                if getattr(pin, "_name_margin_mils", None) != margin_mils:
                    pin._name_margin_mils = margin_mils
                    changed = True
            else:
                if getattr(pin, "_designator_margin_mils", None) != margin_mils:
                    pin._designator_margin_mils = margin_mils
                    changed = True

    return changed


def _resolve_text_font_id(
    *,
    font_manager: FontIDManager,
    current_font_id: int | None,
    spec: CleanFontSpec,
) -> int:
    default_font_id = font_manager.get_default_font_id()
    effective_font_id = int(current_font_id or default_font_id)
    default_info = font_manager.get_font_info(default_font_id) or {}
    current_info = font_manager.get_font_info(effective_font_id) or {}
    effective_info = current_info or default_info
    return font_manager.get_or_create_font(
        font_name=spec.font_name,
        font_size=spec.size_pt,
        bold=spec.bold,
        italic=spec.italic,
        rotation=int(effective_info.get("rotation", default_info.get("rotation", 0))),
        underline=bool(effective_info.get("underline", default_info.get("underline", False))),
        strikeout=bool(effective_info.get("strikeout", default_info.get("strikeout", False))),
    )


def _apply_font_spec_to_text_record(
    record: AltiumSchDesignator | AltiumSchParameter,
    *,
    font_manager: FontIDManager,
    spec: CleanFontSpec,
) -> tuple[bool, bool]:
    color_changed = False
    font_changed = False

    target_font_id = _resolve_text_font_id(
        font_manager=font_manager,
        current_font_id=getattr(record, "font_id", None),
        spec=spec,
    )
    if getattr(record, "font_id", None) != target_font_id:
        record.font_id = target_font_id
        font_changed = True

    if spec.color_win32 is not None and getattr(record, "color", None) != spec.color_win32:
        record.color = spec.color_win32
        color_changed = True

    return color_changed, font_changed


def _iter_schdoc_pins(schdoc) -> list[AltiumSchPin]:
    pins: list[AltiumSchPin] = []
    seen: set[int] = set()

    for obj in getattr(schdoc, "all_objects", []):
        if isinstance(obj, AltiumSchPin) and id(obj) not in seen:
            pins.append(obj)
            seen.add(id(obj))

    for comp in getattr(schdoc, "components", []):
        for pin in getattr(comp, "pins", []):
            if isinstance(pin, AltiumSchPin) and id(pin) not in seen:
                pins.append(pin)
                seen.add(id(pin))

    return pins


def normalize_pin_fonts_in_schdoc(schdoc, config: AltiumCleanConfig) -> PinFontNormalizationResult:
    result = PinFontNormalizationResult()
    pin_cfg = config.normalize_pin_fonts
    if not pin_cfg.enabled:
        return result

    pins = _iter_schdoc_pins(schdoc)
    result.total_pins = len(pins)
    if not pins:
        return result

    font_manager = schdoc.font_manager

    name_font_id = None
    if pin_cfg.name_font:
        name_font_id = font_manager.get_or_create_font(
            pin_cfg.name_font.font_name,
            pin_cfg.name_font.size_pt,
            bold=pin_cfg.name_font.bold,
            italic=pin_cfg.name_font.italic,
        )

    designator_font_id = None
    if pin_cfg.designator_font:
        designator_font_id = font_manager.get_or_create_font(
            pin_cfg.designator_font.font_name,
            pin_cfg.designator_font.size_pt,
            bold=pin_cfg.designator_font.bold,
            italic=pin_cfg.designator_font.italic,
        )

    for pin in pins:
        if (
            pin_cfg.name_font
            and name_font_id is not None
            and _apply_font_spec_to_pin(pin, spec=pin_cfg.name_font, font_id=name_font_id, for_name=True)
        ):
            result.updated_name_fonts += 1
        if (
            pin_cfg.designator_font
            and designator_font_id is not None
            and _apply_font_spec_to_pin(
                pin,
                spec=pin_cfg.designator_font,
                font_id=designator_font_id,
                for_name=False,
            )
        ):
            result.updated_designator_fonts += 1

    return result


def _ensure_schlib_font_manager(schlib) -> FontIDManager:
    if getattr(schlib, "font_manager", None) is None:
        schlib.font_manager = FontIDManager.from_font_dict({})
    return schlib.font_manager


def normalize_pin_fonts_in_schlib(schlib, config: AltiumCleanConfig) -> PinFontNormalizationResult:
    result = PinFontNormalizationResult()
    pin_cfg = config.normalize_pin_fonts
    if not pin_cfg.enabled:
        return result

    symbols = getattr(schlib, "symbols", [])
    pins: list[AltiumSchPin] = []
    for symbol in symbols:
        pins.extend([p for p in getattr(symbol, "pins", []) if isinstance(p, AltiumSchPin)])

    result.total_pins = len(pins)
    if not pins:
        return result

    font_manager = _ensure_schlib_font_manager(schlib)

    name_font_id = None
    if pin_cfg.name_font:
        name_font_id = font_manager.get_or_create_font(
            pin_cfg.name_font.font_name,
            pin_cfg.name_font.size_pt,
            bold=pin_cfg.name_font.bold,
            italic=pin_cfg.name_font.italic,
        )

    designator_font_id = None
    if pin_cfg.designator_font:
        designator_font_id = font_manager.get_or_create_font(
            pin_cfg.designator_font.font_name,
            pin_cfg.designator_font.size_pt,
            bold=pin_cfg.designator_font.bold,
            italic=pin_cfg.designator_font.italic,
        )

    for pin in pins:
        if (
            pin_cfg.name_font
            and name_font_id is not None
            and _apply_font_spec_to_pin(pin, spec=pin_cfg.name_font, font_id=name_font_id, for_name=True)
        ):
            result.updated_name_fonts += 1
        if (
            pin_cfg.designator_font
            and designator_font_id is not None
            and _apply_font_spec_to_pin(
                pin,
                spec=pin_cfg.designator_font,
                font_id=designator_font_id,
                for_name=False,
            )
        ):
            result.updated_designator_fonts += 1

    return result


def _iter_schdoc_symbol_rectangles(schdoc) -> list[AltiumSchRectangle]:
    rectangles: list[AltiumSchRectangle] = []
    seen: set[int] = set()
    for comp in getattr(schdoc, "components", []):
        for graphic in getattr(comp, "graphics", []):
            if isinstance(graphic, AltiumSchRectangle) and id(graphic) not in seen:
                rectangles.append(graphic)
                seen.add(id(graphic))
    return rectangles


def _iter_schlib_symbol_rectangles(schlib) -> list[AltiumSchRectangle]:
    rectangles: list[AltiumSchRectangle] = []
    seen: set[int] = set()
    for symbol in getattr(schlib, "symbols", []):
        for graphic in getattr(symbol, "graphic_primitives", []):
            if isinstance(graphic, AltiumSchRectangle) and id(graphic) not in seen:
                rectangles.append(graphic)
                seen.add(id(graphic))
    return rectangles


def _rectangle_dimensions_mils(rect: AltiumSchRectangle) -> tuple[float, float]:
    x1 = float(rect.location.x_mils)
    x2 = float(rect.corner.x_mils)
    y1 = float(rect.location.y_mils)
    y2 = float(rect.corner.y_mils)
    return abs(x2 - x1), abs(y2 - y1)


def _record_part_display_group_key(record: Any) -> tuple[int | None, int]:
    part_id = getattr(record, "owner_part_id", None)
    try:
        normalized_part_id = int(part_id) if part_id is not None else None
    except (TypeError, ValueError):
        normalized_part_id = None

    display_mode = getattr(record, "owner_part_display_mode", None)
    try:
        normalized_display_mode = int(display_mode) if display_mode is not None else 0
    except (TypeError, ValueError):
        normalized_display_mode = 0

    return normalized_part_id, normalized_display_mode


def _rectangle_meets_body_size_floor(
    rect: AltiumSchRectangle,
    cfg: SymbolBodyRectangleNormalizationConfig,
) -> bool:
    width_mils, height_mils = _rectangle_dimensions_mils(rect)
    return width_mils > cfg.min_width_mils and height_mils > cfg.min_height_mils


def _symbol_body_foreground_boundary(record: Any) -> bool:
    return isinstance(record, AltiumSchPin) or isinstance(record, SchGraphicalObject)


def _select_body_rectangles_from_ordered_records(
    records: list[Any],
    cfg: SymbolBodyRectangleNormalizationConfig,
) -> list[AltiumSchRectangle]:
    back_candidates_by_group: dict[tuple[int | None, int], list[AltiumSchRectangle]] = {}
    candidates_by_group: dict[tuple[int | None, int], list[AltiumSchRectangle]] = {}
    foreground_seen_by_group: set[tuple[int | None, int]] = set()

    for record in records:
        group_key = _record_part_display_group_key(record)
        if isinstance(record, AltiumSchRectangle):
            if _rectangle_meets_body_size_floor(record, cfg):
                candidates_by_group.setdefault(group_key, []).append(record)
                if group_key not in foreground_seen_by_group:
                    back_candidates_by_group.setdefault(group_key, []).append(record)
            else:
                foreground_seen_by_group.add(group_key)
            continue
        if _symbol_body_foreground_boundary(record):
            foreground_seen_by_group.add(group_key)

    selected_ids: set[int] = set()
    for group_key, candidates in candidates_by_group.items():
        back_candidates = back_candidates_by_group.get(group_key)
        if back_candidates:
            selected_ids.update(id(rect) for rect in back_candidates)
            continue

        largest_area = max(
            _rectangle_dimensions_mils(rect)[0] * _rectangle_dimensions_mils(rect)[1]
            for rect in candidates
        )
        for rect in candidates:
            width_mils, height_mils = _rectangle_dimensions_mils(rect)
            if width_mils * height_mils == largest_area:
                selected_ids.add(id(rect))

    return [record for record in records if isinstance(record, AltiumSchRectangle) and id(record) in selected_ids]


def _ordered_component_symbol_records(component: Any) -> list[Any]:
    children = list(getattr(component, "children", []) or [])
    seen = {id(child) for child in children}
    missing_records = [
        child
        for collection_name in ("graphics", "pins")
        for child in getattr(component, collection_name, []) or []
        if id(child) not in seen
    ]
    missing_records.sort(key=lambda child: int(getattr(child, "_record_index", 999999999) or 999999999))
    return children + missing_records


def _apply_body_rectangle_style(
    rect: AltiumSchRectangle,
    cfg: SymbolBodyRectangleNormalizationConfig,
) -> bool:
    changed = False
    if rect.color != cfg.outline_color_win32:
        rect.color = cfg.outline_color_win32
        changed = True
    if rect.line_width != cfg.line_width:
        rect.line_width = cfg.line_width
        changed = True
    if rect.area_color != cfg.fill_color_win32:
        rect.area_color = cfg.fill_color_win32
        changed = True
    if rect.is_solid != cfg.is_solid:
        rect.is_solid = cfg.is_solid
        changed = True
    if rect.transparent != cfg.transparent:
        rect.transparent = cfg.transparent
        changed = True
    return changed


def _move_body_rectangles_behind_symbol_objects(symbol: Any, body_rectangle_ids: set[int]) -> int:
    objects_collection = getattr(symbol, "objects", None)
    if objects_collection is None:
        return 0

    objects = list(objects_collection)
    if not objects:
        return 0

    body_rectangles = [obj for obj in objects if id(obj) in body_rectangle_ids]
    if not body_rectangles:
        return 0

    body_indexes = [idx for idx, obj in enumerate(objects) if id(obj) in body_rectangle_ids]
    first_non_body_index = next((idx for idx, obj in enumerate(objects) if id(obj) not in body_rectangle_ids), None)
    if first_non_body_index is None:
        return 0
    if all(idx < first_non_body_index for idx in body_indexes):
        return 0

    reordered = body_rectangles + [obj for obj in objects if id(obj) not in body_rectangle_ids]

    objects_collection.clear()
    objects_collection.extend(reordered)
    return len(body_rectangles)


def _coerce_record_index(value: Any) -> int | None:
    try:
        record_index = int(value)
    except (TypeError, ValueError):
        return None
    return record_index if record_index >= 0 else None


def _update_reordered_owner_indexes(raw_records: list[dict[str, Any]], old_to_new_index: dict[int, int]) -> None:
    for record in raw_records:
        for key in ("OwnerIndex", "OWNERINDEX"):
            if key not in record:
                continue
            owner_index = _coerce_record_index(record.get(key))
            if owner_index is None or owner_index not in old_to_new_index:
                continue
            record[key] = str(old_to_new_index[owner_index])


def _move_body_rectangles_behind_symbol_raw_records(symbol: Any, body_rectangle_ids: set[int]) -> int:
    raw_records = list(getattr(symbol, "raw_records", []) or [])
    if not raw_records:
        return 0

    non_body_indices = [
        record_index
        for obj in getattr(symbol, "objects", [])
        if id(obj) not in body_rectangle_ids
        and (record_index := _coerce_record_index(getattr(obj, "_record_index", None))) is not None
        and record_index < len(raw_records)
    ]
    if not non_body_indices:
        return 0
    first_non_body_index = min(non_body_indices)

    body_indices = [
        record_index
        for obj in getattr(symbol, "objects", [])
        if id(obj) in body_rectangle_ids
        and (record_index := _coerce_record_index(getattr(obj, "_record_index", None))) is not None
        and record_index < len(raw_records)
    ]
    if not body_indices or all(idx < first_non_body_index for idx in body_indices):
        return 0

    body_index_set = set(body_indices)
    indexed_records = list(enumerate(raw_records))
    body_records = [(idx, raw_records[idx]) for idx in sorted(body_index_set)]

    reordered_indexed_records: list[tuple[int, dict[str, Any]]] = []
    inserted = False
    for old_index, record in indexed_records:
        if old_index in body_index_set:
            continue
        if old_index == first_non_body_index and not inserted:
            reordered_indexed_records.extend(body_records)
            inserted = True
        reordered_indexed_records.append((old_index, record))

    if not inserted:
        return 0

    old_to_new_index = {
        old_index: new_index
        for new_index, (old_index, _record) in enumerate(reordered_indexed_records)
    }
    reordered_records = [record for _old_index, record in reordered_indexed_records]
    _update_reordered_owner_indexes(reordered_records, old_to_new_index)

    symbol.raw_records = reordered_records
    for obj in getattr(symbol, "objects", []):
        record_index = _coerce_record_index(getattr(obj, "_record_index", None))
        if record_index is not None and record_index in old_to_new_index:
            setattr(obj, "_record_index", old_to_new_index[record_index])

    return len(body_indices)


def _move_schlib_body_rectangles_behind_symbol_objects(schlib: Any, body_rectangle_ids: set[int]) -> int:
    if not body_rectangle_ids:
        return 0

    reordered = 0
    for symbol in getattr(schlib, "symbols", []):
        raw_reordered = _move_body_rectangles_behind_symbol_raw_records(symbol, body_rectangle_ids)
        object_reordered = _move_body_rectangles_behind_symbol_objects(symbol, body_rectangle_ids)
        reordered += max(raw_reordered, object_reordered)
    return reordered


def normalize_symbol_body_rectangles_in_schdoc(
    schdoc,
    config: AltiumCleanConfig,
) -> SymbolBodyRectangleNormalizationResult:
    result = SymbolBodyRectangleNormalizationResult()
    rect_cfg = config.normalize_symbol_body_rectangles
    if not rect_cfg.enabled:
        return result

    rectangles = _iter_schdoc_symbol_rectangles(schdoc)
    result.total_rectangles = len(rectangles)

    matched_rectangle_ids: set[int] = set()
    for comp in getattr(schdoc, "components", []):
        for rect in _select_body_rectangles_from_ordered_records(_ordered_component_symbol_records(comp), rect_cfg):
            if id(rect) in matched_rectangle_ids:
                continue
            matched_rectangle_ids.add(id(rect))
            result.matched_rectangles += 1
            if _apply_body_rectangle_style(rect, rect_cfg):
                result.updated_rectangles += 1

    return result


def normalize_symbol_body_rectangles_in_schlib(
    schlib,
    config: AltiumCleanConfig,
) -> SymbolBodyRectangleNormalizationResult:
    result = SymbolBodyRectangleNormalizationResult()
    rect_cfg = config.normalize_symbol_body_rectangles
    if not rect_cfg.enabled:
        return result

    rectangles = _iter_schlib_symbol_rectangles(schlib)
    result.total_rectangles = len(rectangles)
    matched_rectangle_ids: set[int] = set()

    for symbol in getattr(schlib, "symbols", []):
        for rect in _select_body_rectangles_from_ordered_records(list(getattr(symbol, "objects", []) or []), rect_cfg):
            if id(rect) in matched_rectangle_ids:
                continue
            result.matched_rectangles += 1
            matched_rectangle_ids.add(id(rect))
            if _apply_body_rectangle_style(rect, rect_cfg):
                result.updated_rectangles += 1

    result.reordered_rectangles = _move_schlib_body_rectangles_behind_symbol_objects(schlib, matched_rectangle_ids)
    return result


def _is_symbol_internal_graphic_target(graphic: Any) -> bool:
    if isinstance(graphic, (AltiumSchLine, AltiumSchPolyline, AltiumSchPolygon, AltiumSchArc)):
        return True
    return "region" in type(graphic).__name__.lower()


def _iter_schdoc_symbol_internal_graphics(schdoc) -> list[Any]:
    graphics: list[Any] = []
    seen: set[int] = set()
    for comp in getattr(schdoc, "components", []):
        for graphic in getattr(comp, "graphics", []):
            if id(graphic) in seen or not _is_symbol_internal_graphic_target(graphic):
                continue
            graphics.append(graphic)
            seen.add(id(graphic))
    return graphics


def _iter_schlib_symbol_internal_graphics(schlib) -> list[Any]:
    graphics: list[Any] = []
    seen: set[int] = set()
    for symbol in getattr(schlib, "symbols", []):
        for graphic in getattr(symbol, "graphic_primitives", []):
            if id(graphic) in seen or not _is_symbol_internal_graphic_target(graphic):
                continue
            graphics.append(graphic)
            seen.add(id(graphic))
    return graphics


def _apply_symbol_internal_graphic_monochrome(
    graphic: Any,
    cfg: SymbolInternalGraphicsMonochromeConfig,
) -> tuple[bool, bool]:
    stroke_changed = False
    fill_changed = False

    stroke_color = getattr(graphic, "color", None)
    if isinstance(stroke_color, int):
        mono_stroke = _normalize_monochrome_color(stroke_color)
        if mono_stroke != stroke_color:
            graphic.color = mono_stroke
            stroke_changed = True

    fill_color = getattr(graphic, "area_color", None)
    if isinstance(fill_color, int):
        mono_fill = _normalize_monochrome_color(fill_color)
        if mono_fill != fill_color:
            graphic.area_color = mono_fill
            fill_changed = True

    return stroke_changed, fill_changed


def normalize_symbol_internal_graphics_monochrome_in_schdoc(
    schdoc,
    config: AltiumCleanConfig,
) -> SymbolInternalGraphicsMonochromeResult:
    result = SymbolInternalGraphicsMonochromeResult()
    graphics_cfg = config.normalize_symbol_internal_graphics_monochrome
    if not graphics_cfg.enabled:
        return result

    graphics = _iter_schdoc_symbol_internal_graphics(schdoc)
    result.total_symbol_internal_graphics = len(graphics)
    for graphic in graphics:
        stroke_changed, fill_changed = _apply_symbol_internal_graphic_monochrome(graphic, graphics_cfg)
        if stroke_changed:
            result.updated_symbol_internal_graphic_stroke_colors += 1
        if fill_changed:
            result.updated_symbol_internal_graphic_fill_colors += 1
    return result


def normalize_symbol_internal_graphics_monochrome_in_schlib(
    schlib,
    config: AltiumCleanConfig,
) -> SymbolInternalGraphicsMonochromeResult:
    result = SymbolInternalGraphicsMonochromeResult()
    graphics_cfg = config.normalize_symbol_internal_graphics_monochrome
    if not graphics_cfg.enabled:
        return result

    graphics = _iter_schlib_symbol_internal_graphics(schlib)
    result.total_symbol_internal_graphics = len(graphics)
    for graphic in graphics:
        stroke_changed, fill_changed = _apply_symbol_internal_graphic_monochrome(graphic, graphics_cfg)
        if stroke_changed:
            result.updated_symbol_internal_graphic_stroke_colors += 1
        if fill_changed:
            result.updated_symbol_internal_graphic_fill_colors += 1
    return result


def _iter_schdoc_power_symbols(schdoc) -> list[AltiumSchPowerPort]:
    power_ports: list[AltiumSchPowerPort] = []
    seen: set[int] = set()

    for port in getattr(schdoc, "power_ports", []):
        if isinstance(port, AltiumSchPowerPort) and id(port) not in seen:
            power_ports.append(port)
            seen.add(id(port))

    for obj in getattr(schdoc, "all_objects", []):
        if isinstance(obj, AltiumSchPowerPort) and id(obj) not in seen:
            power_ports.append(obj)
            seen.add(id(obj))

    return power_ports


def normalize_power_symbols_in_schdoc(
    schdoc,
    config: AltiumCleanConfig,
) -> PowerSymbolNormalizationResult:
    result = PowerSymbolNormalizationResult()
    power_cfg = config.normalize_power_symbols
    if not power_cfg.enabled:
        return result

    power_ports = _iter_schdoc_power_symbols(schdoc)
    result.total_power_symbols = len(power_ports)
    if not power_ports:
        return result

    font_id = schdoc.font_manager.get_or_create_font(
        power_cfg.font_name,
        power_cfg.size_pt,
        bold=power_cfg.bold,
        italic=power_cfg.italic,
    )

    for port in power_ports:
        if port.color != power_cfg.color_win32:
            port.color = power_cfg.color_win32
            result.updated_power_symbol_colors += 1
        if port.font_id != font_id:
            port.font_id = font_id
            result.updated_power_symbol_fonts += 1

    return result


def _iter_schdoc_net_labels(schdoc) -> list[AltiumSchNetLabel]:
    net_labels: list[AltiumSchNetLabel] = []
    seen: set[int] = set()

    for label in getattr(schdoc, "net_labels", []):
        if isinstance(label, AltiumSchNetLabel) and id(label) not in seen:
            net_labels.append(label)
            seen.add(id(label))

    for obj in getattr(schdoc, "all_objects", []):
        if isinstance(obj, AltiumSchNetLabel) and id(obj) not in seen:
            net_labels.append(obj)
            seen.add(id(obj))

    return net_labels


def normalize_net_labels_in_schdoc(
    schdoc,
    config: AltiumCleanConfig,
) -> NetLabelNormalizationResult:
    result = NetLabelNormalizationResult()
    net_cfg = config.normalize_net_labels
    if not net_cfg.enabled:
        return result

    net_labels = _iter_schdoc_net_labels(schdoc)
    result.total_net_labels = len(net_labels)
    if not net_labels:
        return result

    font_id = schdoc.font_manager.get_or_create_font(
        net_cfg.font_name,
        net_cfg.size_pt,
        bold=net_cfg.bold,
        italic=net_cfg.italic,
    )

    for label in net_labels:
        if label.color != net_cfg.color_win32:
            label.color = net_cfg.color_win32
            result.updated_net_label_colors += 1
        if label.font_id != font_id:
            label.font_id = font_id
            result.updated_net_label_fonts += 1

    return result


def _iter_schdoc_component_designators(schdoc) -> list[AltiumSchDesignator]:
    designators: list[AltiumSchDesignator] = []
    seen: set[int] = set()

    for component in getattr(schdoc, "components", []):
        for item in getattr(component, "parameters", []):
            if isinstance(item, AltiumSchDesignator) and id(item) not in seen:
                designators.append(item)
                seen.add(id(item))

    return designators


def _iter_schlib_component_designators(schlib) -> list[AltiumSchDesignator]:
    designators: list[AltiumSchDesignator] = []
    seen: set[int] = set()

    for symbol in getattr(schlib, "symbols", []):
        for item in getattr(symbol, "designators", []):
            if isinstance(item, AltiumSchDesignator) and id(item) not in seen:
                designators.append(item)
                seen.add(id(item))

    return designators


def normalize_component_designators_in_schdoc(
    schdoc,
    config: AltiumCleanConfig,
) -> ComponentDesignatorNormalizationResult:
    result = ComponentDesignatorNormalizationResult()
    designator_cfg = config.normalize_component_designators
    if not designator_cfg.enabled:
        return result

    designators = _iter_schdoc_component_designators(schdoc)
    result.total_component_designators = len(designators)
    if not designators:
        return result

    font_manager = schdoc.font_manager
    for designator in designators:
        color_changed, font_changed = _apply_font_spec_to_text_record(
            designator,
            font_manager=font_manager,
            spec=designator_cfg.font,
        )
        if color_changed:
            result.updated_component_designator_colors += 1
        if font_changed:
            result.updated_component_designator_fonts += 1

    return result


def normalize_component_designators_in_schlib(
    schlib,
    config: AltiumCleanConfig,
) -> ComponentDesignatorNormalizationResult:
    result = ComponentDesignatorNormalizationResult()
    designator_cfg = config.normalize_component_designators
    if not designator_cfg.enabled:
        return result

    designators = _iter_schlib_component_designators(schlib)
    result.total_component_designators = len(designators)
    if not designators:
        return result

    font_manager = _ensure_schlib_font_manager(schlib)
    for designator in designators:
        color_changed, font_changed = _apply_font_spec_to_text_record(
            designator,
            font_manager=font_manager,
            spec=designator_cfg.font,
        )
        if color_changed:
            result.updated_component_designator_colors += 1
        if font_changed:
            result.updated_component_designator_fonts += 1

    return result


def _iter_schdoc_component_parameters(schdoc) -> list[AltiumSchParameter]:
    parameters: list[AltiumSchParameter] = []
    seen: set[int] = set()

    for component in getattr(schdoc, "components", []):
        for item in getattr(component, "parameters", []):
            if isinstance(item, AltiumSchParameter) and id(item) not in seen:
                parameters.append(item)
                seen.add(id(item))

    return parameters


def _iter_schlib_component_parameters(schlib) -> list[AltiumSchParameter]:
    parameters: list[AltiumSchParameter] = []
    seen: set[int] = set()

    for symbol in getattr(schlib, "symbols", []):
        for item in getattr(symbol, "parameters", []):
            if isinstance(item, AltiumSchParameter) and id(item) not in seen:
                parameters.append(item)
                seen.add(id(item))

    return parameters


def normalize_component_parameters_in_schdoc(
    schdoc,
    config: AltiumCleanConfig,
) -> ComponentParameterNormalizationResult:
    result = ComponentParameterNormalizationResult()
    parameter_cfg = config.normalize_component_parameters
    if not parameter_cfg.enabled:
        return result

    parameters = _iter_schdoc_component_parameters(schdoc)
    result.total_component_parameters = len(parameters)
    if not parameters:
        return result

    font_manager = schdoc.font_manager
    for parameter in parameters:
        color_changed, font_changed = _apply_font_spec_to_text_record(
            parameter,
            font_manager=font_manager,
            spec=parameter_cfg.font,
        )
        if color_changed:
            result.updated_component_parameter_colors += 1
        if font_changed:
            result.updated_component_parameter_fonts += 1

    return result


def normalize_component_parameters_in_schlib(
    schlib,
    config: AltiumCleanConfig,
) -> ComponentParameterNormalizationResult:
    result = ComponentParameterNormalizationResult()
    parameter_cfg = config.normalize_component_parameters
    if not parameter_cfg.enabled:
        return result

    parameters = _iter_schlib_component_parameters(schlib)
    result.total_component_parameters = len(parameters)
    if not parameters:
        return result

    font_manager = _ensure_schlib_font_manager(schlib)
    for parameter in parameters:
        color_changed, font_changed = _apply_font_spec_to_text_record(
            parameter,
            font_manager=font_manager,
            spec=parameter_cfg.font,
        )
        if color_changed:
            result.updated_component_parameter_colors += 1
        if font_changed:
            result.updated_component_parameter_fonts += 1

    return result


def _iter_schdoc_component_free_text_labels(schdoc) -> list[AltiumSchLabel]:
    labels: list[AltiumSchLabel] = []
    seen: set[int] = set()
    for comp in getattr(schdoc, "components", []):
        for graphic in getattr(comp, "graphics", []):
            if not isinstance(graphic, AltiumSchLabel):
                continue
            if int(getattr(graphic, "record_type", -1)) != 4:
                continue
            obj_id = id(graphic)
            if obj_id in seen:
                continue
            labels.append(graphic)
            seen.add(obj_id)
    return labels


def _iter_schlib_component_free_text_labels(schlib) -> list[AltiumSchLabel]:
    labels: list[AltiumSchLabel] = []
    seen: set[int] = set()
    for symbol in getattr(schlib, "symbols", []):
        for label in getattr(symbol, "labels", []):
            if not isinstance(label, AltiumSchLabel):
                continue
            obj_id = id(label)
            if obj_id in seen:
                continue
            labels.append(label)
            seen.add(obj_id)
        # Some flows may place label records in graphics collections.
        for graphic in getattr(symbol, "graphics", []):
            if not isinstance(graphic, AltiumSchLabel):
                continue
            if int(getattr(graphic, "record_type", -1)) != 4:
                continue
            obj_id = id(graphic)
            if obj_id in seen:
                continue
            labels.append(graphic)
            seen.add(obj_id)
    return labels


def _resolve_component_free_text_font_id(
    *,
    font_manager: FontIDManager,
    label: AltiumSchLabel,
    target_font_name: str,
) -> int:
    default_font_id = font_manager.get_default_font_id()
    default_info = font_manager.get_font_info(default_font_id) or {}
    label_font_info = font_manager.get_font_info(int(getattr(label, "font_id", default_font_id) or default_font_id)) or {}
    effective = label_font_info or default_info

    return font_manager.get_or_create_font(
        font_name=target_font_name,
        font_size=int(effective.get("size", default_info.get("size", 10))),
        bold=bool(effective.get("bold", default_info.get("bold", False))),
        italic=bool(effective.get("italic", default_info.get("italic", False))),
        rotation=int(effective.get("rotation", default_info.get("rotation", 0))),
        underline=bool(effective.get("underline", default_info.get("underline", False))),
        strikeout=bool(effective.get("strikeout", default_info.get("strikeout", False))),
    )


def normalize_component_free_text_in_schdoc(
    schdoc,
    config: AltiumCleanConfig,
) -> ComponentFreeTextNormalizationResult:
    result = ComponentFreeTextNormalizationResult()
    free_text_cfg = config.normalize_component_free_text
    if not free_text_cfg.enabled:
        return result

    labels = _iter_schdoc_component_free_text_labels(schdoc)
    result.total_component_free_texts = len(labels)
    if not labels:
        return result

    font_manager = schdoc.font_manager
    for label in labels:
        if label.color != free_text_cfg.color_win32:
            label.color = free_text_cfg.color_win32
            result.updated_component_free_text_colors += 1

        target_font_id = _resolve_component_free_text_font_id(
            font_manager=font_manager,
            label=label,
            target_font_name=free_text_cfg.font_name,
        )
        if label.font_id != target_font_id:
            label.font_id = target_font_id
            result.updated_component_free_text_fonts += 1

    return result


def normalize_component_free_text_in_schlib(
    schlib,
    config: AltiumCleanConfig,
) -> ComponentFreeTextNormalizationResult:
    result = ComponentFreeTextNormalizationResult()
    free_text_cfg = config.normalize_component_free_text
    if not free_text_cfg.enabled:
        return result

    labels = _iter_schlib_component_free_text_labels(schlib)
    result.total_component_free_texts = len(labels)
    if not labels:
        return result

    font_manager = _ensure_schlib_font_manager(schlib)
    for label in labels:
        if label.color != free_text_cfg.color_win32:
            label.color = free_text_cfg.color_win32
            result.updated_component_free_text_colors += 1

        target_font_id = _resolve_component_free_text_font_id(
            font_manager=font_manager,
            label=label,
            target_font_name=free_text_cfg.font_name,
        )
        if label.font_id != target_font_id:
            label.font_id = target_font_id
            result.updated_component_free_text_fonts += 1

    return result


def _iter_schdoc_wires(schdoc) -> list[AltiumSchWire]:
    wires: list[AltiumSchWire] = []
    seen: set[int] = set()

    for wire in getattr(schdoc, "wires", []):
        if isinstance(wire, AltiumSchWire) and id(wire) not in seen:
            wires.append(wire)
            seen.add(id(wire))

    for obj in getattr(schdoc, "all_objects", []):
        if isinstance(obj, AltiumSchWire) and id(obj) not in seen:
            wires.append(obj)
            seen.add(id(obj))

    return wires


def normalize_wires_in_schdoc(
    schdoc,
    config: AltiumCleanConfig,
) -> WireNormalizationResult:
    result = WireNormalizationResult()
    wire_cfg = config.normalize_wires
    if not wire_cfg.enabled:
        return result

    wires = _iter_schdoc_wires(schdoc)
    result.total_wires = len(wires)

    for wire in wires:
        if wire.color != wire_cfg.color_win32:
            wire.color = wire_cfg.color_win32
            result.updated_wire_colors += 1

    return result


def _iter_schdoc_no_ercs(schdoc) -> list[AltiumSchNoErc]:
    no_ercs: list[AltiumSchNoErc] = []
    seen: set[int] = set()

    for marker in getattr(schdoc, "no_ercs", []):
        if isinstance(marker, AltiumSchNoErc) and id(marker) not in seen:
            no_ercs.append(marker)
            seen.add(id(marker))

    for obj in getattr(schdoc, "all_objects", []):
        if isinstance(obj, AltiumSchNoErc) and id(obj) not in seen:
            no_ercs.append(obj)
            seen.add(id(obj))

    return no_ercs


def normalize_no_erc_in_schdoc(
    schdoc,
    config: AltiumCleanConfig,
) -> NoErcNormalizationResult:
    result = NoErcNormalizationResult()
    no_erc_cfg = config.normalize_no_erc
    if not no_erc_cfg.enabled:
        return result

    no_erc_markers = _iter_schdoc_no_ercs(schdoc)
    result.total_no_ercs = len(no_erc_markers)

    for marker in no_erc_markers:
        if marker.color != no_erc_cfg.color_win32:
            marker.color = no_erc_cfg.color_win32
            result.updated_no_erc_colors += 1
        if marker.symbol != no_erc_cfg.symbol:
            marker.symbol = no_erc_cfg.symbol
            result.updated_no_erc_symbols += 1

    return result


def normalize_sheet_style_in_schdoc(
    schdoc,
    config: AltiumCleanConfig,
) -> SheetStyleNormalizationResult:
    result = SheetStyleNormalizationResult()
    sheet_cfg = config.normalize_sheet_style
    if not sheet_cfg.enabled:
        return result

    sheet = getattr(schdoc, "sheet", None)
    if sheet is None:
        return result

    result.total_sheets = 1

    if sheet.color != sheet_cfg.line_color_win32:
        sheet.color = sheet_cfg.line_color_win32
        result.updated_sheet_line_colors += 1
    if sheet.area_color != sheet_cfg.area_color_win32:
        sheet.area_color = sheet_cfg.area_color_win32
        result.updated_sheet_area_colors += 1

    target_font_id = _resolve_text_font_id(
        font_manager=schdoc.font_manager,
        current_font_id=getattr(sheet, "system_font", None),
        spec=sheet_cfg.document_font,
    )
    if sheet.system_font != target_font_id:
        sheet.system_font = target_font_id
        result.updated_sheet_document_fonts += 1

    return result


def apply_clean_to_schdoc(schdoc, config: AltiumCleanConfig) -> CleanApplyResult:
    pin_result = normalize_pin_fonts_in_schdoc(schdoc, config)
    rect_result = normalize_symbol_body_rectangles_in_schdoc(schdoc, config)
    power_result = normalize_power_symbols_in_schdoc(schdoc, config)
    net_label_result = normalize_net_labels_in_schdoc(schdoc, config)
    component_designator_result = normalize_component_designators_in_schdoc(schdoc, config)
    component_parameter_result = normalize_component_parameters_in_schdoc(schdoc, config)
    component_free_text_result = normalize_component_free_text_in_schdoc(schdoc, config)
    wire_result = normalize_wires_in_schdoc(schdoc, config)
    no_erc_result = normalize_no_erc_in_schdoc(schdoc, config)
    sheet_style_result = normalize_sheet_style_in_schdoc(schdoc, config)
    symbol_internal_graphics_result = normalize_symbol_internal_graphics_monochrome_in_schdoc(schdoc, config)
    return CleanApplyResult.from_parts(
        pin_result=pin_result,
        rect_result=rect_result,
        power_result=power_result,
        net_label_result=net_label_result,
        component_designator_result=component_designator_result,
        component_parameter_result=component_parameter_result,
        component_free_text_result=component_free_text_result,
        wire_result=wire_result,
        no_erc_result=no_erc_result,
        sheet_style_result=sheet_style_result,
        symbol_internal_graphics_result=symbol_internal_graphics_result,
    )


def apply_clean_to_schlib(schlib, config: AltiumCleanConfig) -> CleanApplyResult:
    pin_result = normalize_pin_fonts_in_schlib(schlib, config)
    rect_result = normalize_symbol_body_rectangles_in_schlib(schlib, config)
    component_designator_result = normalize_component_designators_in_schlib(schlib, config)
    component_parameter_result = normalize_component_parameters_in_schlib(schlib, config)
    component_free_text_result = normalize_component_free_text_in_schlib(schlib, config)
    symbol_internal_graphics_result = normalize_symbol_internal_graphics_monochrome_in_schlib(schlib, config)
    return CleanApplyResult.from_parts(
        pin_result=pin_result,
        rect_result=rect_result,
        component_designator_result=component_designator_result,
        component_parameter_result=component_parameter_result,
        component_free_text_result=component_free_text_result,
        symbol_internal_graphics_result=symbol_internal_graphics_result,
    )


def infer_clean_config_path(input_file: Path, *, config_filename: str = "altium-clean.json") -> Path:
    return input_file.resolve().parent / config_filename
