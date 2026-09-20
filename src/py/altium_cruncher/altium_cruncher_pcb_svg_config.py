"""A1 config model for explicit PCB SVG layer/view rendering."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import cast

from .contracts.pcb_svg import config_default, config_metadata

from altium_monkey.altium_pcb_layer_ref import PcbLayerRef
from altium_monkey.altium_record_types import PcbLayer

from altium_cruncher.altium_cruncher_pcb_layer_resolve import (
    resolve_pcb_layer_ref,
)
from altium_cruncher.config_json import JsoncCommentMap, render_commented_jsonc

PCB_SVG_CONFIG_FILENAME = "pcb.svg.config"
PCB_SVG_CONFIG_SCHEMA = cast(str, config_metadata()["schema"])
PCB_SVG_CONFIG_LEGACY_SCHEMAS = frozenset({"pcb.svg.config.a0"})
PCB_DEFAULT_SVG_SCALE = cast(float, config_default("global", "svg_scale"))
PCB_SVG_CANVAS_BOUNDS_MODES = frozenset({"board_outline", "all_geometry"})
PCB_SVG_COMPONENT_PROJECTION_MODES = frozenset(
    {"detail", "outline", "simple", "bounding_box", "none"}
)
PCB_SVG_COMPONENT_SIDES = frozenset({"top", "bottom"})

PCB_SVG_SPECIAL_LAYERS = frozenset(cast(list[str], config_metadata()["special-layers"]))

_STYLE_ORDER = tuple(cast(list[str], config_metadata()["style-order"]))

_PCB_SVG_CONFIG_COMMENTS = cast(JsoncCommentMap, config_metadata()["jsonc-comments"])

_PCB_SVG_CONFIG_KEY_COMMENTS = cast(
    Mapping[str, str | Sequence[str]], config_metadata()["jsonc-key-comments"]
)


def _coerce_bool(value: object, default: bool) -> bool:
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
    raise ValueError(f"Invalid boolean value in pcb-svg config: {value!r}")


def _coerce_float(value: object, default: float) -> float:
    if value is None:
        return float(default)
    if not isinstance(value, (int, float, str)):
        raise ValueError(f"Invalid numeric value in pcb-svg config: {value!r}")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid numeric value in pcb-svg config: {value!r}") from exc


def _coerce_nonnegative_float(
    value: object, default: float, *, field_name: str
) -> float:
    result = _coerce_float(value, default)
    if result < 0.0:
        raise ValueError(f"pcb-svg config field '{field_name}' must be non-negative")
    return result


def _coerce_optional_str(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _coerce_str_list(value: object, *, field_name: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"pcb-svg config field '{field_name}' must be an array")
    result: list[str] = []
    for item in value:
        text = str(item).strip()
        if text:
            result.append(_normalize_layer_token(text))
    return result


def _coerce_raw_str_list(
    value: object,
    default: list[str],
    *,
    field_name: str,
) -> list[str]:
    if value is None:
        return list(default)
    if not isinstance(value, list):
        raise ValueError(f"pcb-svg config field '{field_name}' must be an array")
    return [str(item).strip() for item in value if str(item).strip()]


def _coerce_projection_mode(value: object, default: str, *, field_name: str) -> str:
    raw = str(value or default).strip().lower().replace("-", "_")
    aliases = {
        "simple": "outline",
        "silhouette": "outline",
        "profile": "outline",
        "bbox": "bounding_box",
        "box": "bounding_box",
        "bounds": "bounding_box",
        "off": "none",
        "disabled": "none",
    }
    mode = aliases.get(raw, raw)
    if mode not in PCB_SVG_COMPONENT_PROJECTION_MODES:
        raise ValueError(
            f"pcb-svg config field '{field_name}' must be one of: "
            + ", ".join(sorted(PCB_SVG_COMPONENT_PROJECTION_MODES))
        )
    return mode


def _coerce_component_side(value: object, *, field_name: str) -> str | None:
    raw = str(value or "").strip().lower()
    if not raw:
        return None
    aliases = {"toplayer": "top", "bottomlayer": "bottom"}
    side = aliases.get(raw.replace("_", "").replace("-", ""), raw)
    if side not in PCB_SVG_COMPONENT_SIDES:
        raise ValueError(
            f"pcb-svg config field '{field_name}' must be 'top' or 'bottom'"
        )
    return side


def _normalize_layer_token(value: str) -> str:
    token = value.strip()
    if not token:
        raise ValueError("Empty layer token in pcb-svg config")
    normalized = token.upper().replace(" ", "_").replace("-", "_")
    aliases = {
        "TOP_LAYER": "TOP",
        "BOTTOM_LAYER": "BOTTOM",
        "TOPSILK": "TOPOVERLAY",
        "BOTTOMSILK": "BOTTOMOVERLAY",
        "TOP_SILK": "TOPOVERLAY",
        "BOTTOM_SILK": "BOTTOMOVERLAY",
        "TOP_SILKSCREEN": "TOPOVERLAY",
        "BOTTOM_SILKSCREEN": "BOTTOMOVERLAY",
        "TOP_MASK": "TOPSOLDER",
        "BOTTOM_MASK": "BOTTOMSOLDER",
        "TOP_PASTE_MASK": "TOPPASTE",
        "BOTTOM_PASTE_MASK": "BOTTOMPASTE",
        "CUTOUTS": "BOARD_CUTOUTS",
        "CUTOUT": "BOARD_CUTOUTS",
        "OUTLINE": "BOARD_OUTLINE",
        "BOARD_PROFILE": "BOARD_OUTLINE",
        "HLR_TOP": "ASSEMBLY_HLR_TOP",
        "HLR_BOTTOM": "ASSEMBLY_HLR_BOTTOM",
        "DESIGNATORS_TOP": "ASSEMBLY_DESIGNATORS_TOP",
        "DESIGNATORS_BOTTOM": "ASSEMBLY_DESIGNATORS_BOTTOM",
        "ASSEMBLY_DESIGNATOR_TOP": "ASSEMBLY_DESIGNATORS_TOP",
        "ASSEMBLY_DESIGNATOR_BOTTOM": "ASSEMBLY_DESIGNATORS_BOTTOM",
        "PIN_1_TOP": "PIN1_TOP",
        "PIN_1_BOTTOM": "PIN1_BOTTOM",
    }
    return aliases.get(normalized, normalized)


def _parse_single_pcb_layer_selector(token: str) -> str:
    normalized = _normalize_layer_token(token)
    compact = normalized.replace("_", "")
    numeric_token = compact[1:] if compact.startswith("L") else compact
    if numeric_token.isdigit():
        try:
            return PcbLayer(int(numeric_token)).to_json_name()
        except ValueError as exc:
            raise ValueError(f"Unknown PCB layer id in --layers: {token}") from exc
    if normalized in PCB_SVG_SPECIAL_LAYERS:
        return normalized
    try:
        return resolve_pcb_layer_ref(normalized).token
    except ValueError as exc:
        raise ValueError(f"Unknown PCB layer token in --layers: {token}") from exc


def parse_pcb_layer_selector(raw_layers: str | None) -> list[str] | None:
    """Parse CLI layer selectors into canonical A0 layer tokens."""
    if raw_layers is None:
        return None

    tokens = [token.strip() for token in raw_layers.split(",") if token.strip()]
    if not tokens:
        raise ValueError("--layers was provided but no valid layer tokens were found")

    resolved: list[str] = []
    for token in tokens:
        normalized = _parse_single_pcb_layer_selector(token)
        if normalized not in resolved:
            resolved.append(normalized)
    return resolved


def pcb_svg_layer_ref_from_token(token: str) -> PcbLayerRef | None:
    """Return a PcbLayerRef for a token, or None for A0 synthetic layers.

    Raises ValueError for unknown tokens. Covers both legacy and V7 layers.
    """
    normalized = _normalize_layer_token(token)
    if normalized in PCB_SVG_SPECIAL_LAYERS:
        return None
    return resolve_pcb_layer_ref(normalized)


def pcb_svg_physical_layer_from_token(token: str) -> PcbLayer | None:
    """Return a legacy physical PcbLayer for a token, or None for A0
    synthetic layers and V7-only layers with no legacy equivalent."""
    ref = pcb_svg_layer_ref_from_token(token)
    return None if ref is None else ref.legacy_layer


def default_pcb_svg_styles() -> dict[str, dict[str, object]]:
    """Copy the TypeSpec-authored default style table."""
    return cast(dict[str, dict[str, object]], config_default("global", "styles"))


def merge_pcb_svg_styles(
    base: dict[str, dict[str, object]],
    override: Mapping[str, object] | None,
) -> dict[str, dict[str, object]]:
    """Merge an A0 style table while preserving default style keys."""
    merged = {name: dict(base.get(name, {})) for name in _STYLE_ORDER}
    # Styles are extensible; keep every supplied group through view resolution.
    merged.update({name: dict(style) for name, style in base.items()})
    if override:
        for name, raw_style in override.items():
            if not isinstance(raw_style, dict):
                raise ValueError(f"pcb-svg style '{name}' must be an object")
            target = merged.setdefault(str(name), {})
            target.update(raw_style)
    return merged


def _coerce_object_mapping(
    value: object, *, field_name: str
) -> dict[str, object] | None:
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise ValueError(f"pcb-svg config field '{field_name}' must be an object")
    return {str(key): item for key, item in value.items()}


@dataclass(slots=True)
class PcbSvgCanvasConfig:
    """Canvas normalization policy for PCB SVG viewBox coordinates."""

    bounds: str = cast(str, config_default("global", "canvas", "bounds"))
    margin_mm: float = cast(float, config_default("global", "canvas", "margin_mm"))

    @classmethod
    def from_dict(cls, data: dict[str, object] | None) -> "PcbSvgCanvasConfig":
        if data is None:
            return cls()
        if not isinstance(data, dict):
            raise ValueError("pcb-svg config field 'global.canvas' must be an object")
        default = cls()
        bounds = (
            str(data.get("bounds", default.bounds) or default.bounds).strip().lower()
        )
        aliases = {
            "board": "board_outline",
            "outline": "board_outline",
            "board_profile": "board_outline",
            "legacy": "all_geometry",
            "all": "all_geometry",
            "rendered_view": "all_geometry",
            "rendered_geometry": "all_geometry",
        }
        bounds = aliases.get(bounds, bounds)
        if bounds not in PCB_SVG_CANVAS_BOUNDS_MODES:
            raise ValueError(
                "pcb-svg config field 'global.canvas.bounds' must be "
                "'board_outline' or 'all_geometry'"
            )
        return cls(
            bounds=bounds,
            margin_mm=_coerce_nonnegative_float(
                data.get("margin_mm"),
                default.margin_mm,
                field_name="global.canvas.margin_mm",
            ),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "bounds": self.bounds,
            "margin_mm": self.margin_mm,
        }


@dataclass(slots=True)
class PcbSvgGlobalConfig:
    """Global pcb-svg A0 options applied to layer outputs and views."""

    pcbdoc: str | None = cast(str | None, config_default("global", "pcbdoc"))
    canvas: PcbSvgCanvasConfig = field(default_factory=PcbSvgCanvasConfig)
    include_metadata: bool = cast(bool, config_default("global", "include_metadata"))
    show_empty_layers: bool = cast(bool, config_default("global", "show_empty_layers"))
    clip_to_outline: bool = cast(bool, config_default("global", "clip_to_outline"))
    clip_holes_from_copper: bool = cast(
        bool, config_default("global", "clip_holes_from_copper")
    )
    mirror_bottom_view: bool = cast(
        bool, config_default("global", "mirror_bottom_view")
    )
    svg_scale: float = cast(float, config_default("global", "svg_scale"))
    svg_size_unit: str = cast(str, config_default("global", "svg_size_unit"))
    clean_output: bool = cast(bool, config_default("global", "clean_output"))
    styles: dict[str, dict[str, object]] = field(default_factory=default_pcb_svg_styles)

    @classmethod
    def from_dict(cls, data: dict[str, object] | None) -> "PcbSvgGlobalConfig":
        if data is None:
            return cls()
        if not isinstance(data, dict):
            raise ValueError("pcb-svg config field 'global' must be an object")
        default = cls()
        return cls(
            pcbdoc=_coerce_optional_str(data.get("pcbdoc")),
            canvas=PcbSvgCanvasConfig.from_dict(
                _coerce_object_mapping(data.get("canvas"), field_name="global.canvas")
            ),
            include_metadata=_coerce_bool(
                data.get("include_metadata"), default.include_metadata
            ),
            show_empty_layers=_coerce_bool(
                data.get("show_empty_layers"), default.show_empty_layers
            ),
            clip_to_outline=_coerce_bool(
                data.get("clip_to_outline"), default.clip_to_outline
            ),
            clip_holes_from_copper=_coerce_bool(
                data.get("clip_holes_from_copper"), default.clip_holes_from_copper
            ),
            mirror_bottom_view=_coerce_bool(
                data.get("mirror_bottom_view"), default.mirror_bottom_view
            ),
            svg_scale=_coerce_float(data.get("svg_scale"), default.svg_scale),
            svg_size_unit=str(data.get("svg_size_unit", default.svg_size_unit) or ""),
            clean_output=_coerce_bool(data.get("clean_output"), default.clean_output),
            styles=merge_pcb_svg_styles(
                default.styles,
                _coerce_object_mapping(data.get("styles"), field_name="global.styles"),
            ),
        )

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "canvas": self.canvas.to_dict(),
            "include_metadata": self.include_metadata,
            "show_empty_layers": self.show_empty_layers,
            "clip_to_outline": self.clip_to_outline,
            "clip_holes_from_copper": self.clip_holes_from_copper,
            "mirror_bottom_view": self.mirror_bottom_view,
            "svg_scale": self.svg_scale,
            "svg_size_unit": self.svg_size_unit,
            "clean_output": self.clean_output,
            "styles": self.styles,
        }
        if self.pcbdoc is not None:
            result["pcbdoc"] = self.pcbdoc
        return result


@dataclass(slots=True)
class PcbSvgViewConfig:
    """One explicit A0 composed PCB SVG view."""

    name: str
    enabled: bool = cast(bool, config_default("view", "enabled"))
    group_id: str | None = cast(str | None, config_default("view", "group_id"))
    output_svg: str | None = cast(str | None, config_default("view", "output_svg"))
    layers: list[str] = field(
        default_factory=lambda: cast(list[str], config_default("view", "layers"))
    )
    mirror: bool | None = cast(bool | None, config_default("view", "mirror"))
    assembly_hlr_mode: str = cast(str, config_default("view", "assembly_hlr_mode"))
    styles: dict[str, dict[str, object]] = field(
        default_factory=lambda: cast(
            dict[str, dict[str, object]], config_default("view", "styles")
        )
    )
    description: str | None = cast(str | None, config_default("view", "description"))

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "PcbSvgViewConfig":
        if not isinstance(data, dict):
            raise ValueError("Each item in pcb-svg config 'views' must be an object")
        name = _coerce_optional_str(data.get("name"))
        if not name:
            raise ValueError("Each pcb-svg view must include a non-empty 'name'")
        default = cls(name=name)
        mode = str(
            data.get("assembly_hlr_mode", default.assembly_hlr_mode)
            or default.assembly_hlr_mode
        ).lower()
        aliases = {
            "detailed": "detail",
            "simple": "outline",
            "silhouette": "outline",
            "profile": "outline",
            "bounding-box": "bounding_box",
            "bbox": "bounding_box",
            "box": "bounding_box",
            "off": "none",
        }
        mode = aliases.get(mode, mode)
        if mode not in {"outline", "detail", "bounding_box", "none"}:
            raise ValueError(
                f"Unsupported assembly_hlr_mode {mode!r} for pcb-svg view {name!r}"
            )
        styles = (
            _coerce_object_mapping(
                data.get("styles"),
                field_name=f"views.{name}.styles",
            )
            or {}
        )
        return cls(
            name=name,
            enabled=_coerce_bool(data.get("enabled"), default.enabled),
            group_id=_coerce_optional_str(data.get("group_id")),
            output_svg=_coerce_optional_str(data.get("output_svg")),
            layers=_coerce_str_list(
                data.get("layers", default.layers), field_name=f"views.{name}.layers"
            ),
            mirror=(
                None
                if data.get("mirror") is None
                else _coerce_bool(data.get("mirror"), False)
            ),
            assembly_hlr_mode=mode,
            styles=merge_pcb_svg_styles({}, styles),
            description=_coerce_optional_str(data.get("description")),
        )

    def resolved_group_id(self) -> str:
        return self.group_id or f"pcb-svg-view-{self.name.replace('_', '-')}"

    def resolved_output_svg(self) -> str:
        return self.output_svg or f"views/{{board}}__{self.name}.svg"

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "name": self.name,
            "enabled": self.enabled,
            "group_id": self.resolved_group_id(),
            "output_svg": self.resolved_output_svg(),
            "layers": list(self.layers),
            "assembly_hlr_mode": self.assembly_hlr_mode,
        }
        if self.mirror is not None:
            result["mirror"] = self.mirror
        if self.styles:
            result["styles"] = self.styles
        if self.description:
            result["description"] = self.description
        return result


@dataclass(slots=True)
class PcbSvgAssemblyConfig:
    """Component assembly projection defaults for PCB SVG virtual layers."""

    default_projection: str = cast(
        str, config_default("assembly", "default_projection")
    )
    dnp_projection: str = cast(str, config_default("assembly", "dnp_projection"))
    designator_color: str = cast(str, config_default("assembly", "designator_color"))
    dnp_designator_color: str = cast(
        str, config_default("assembly", "dnp_designator_color")
    )

    @classmethod
    def from_dict(cls, data: dict[str, object] | None) -> "PcbSvgAssemblyConfig":
        if data is None:
            return cls()
        if not isinstance(data, dict):
            raise ValueError("pcb-svg config field 'assembly' must be an object")
        default = cls()
        return cls(
            default_projection=_coerce_projection_mode(
                data.get("default_projection"),
                default.default_projection,
                field_name="assembly.default_projection",
            ),
            dnp_projection=_coerce_projection_mode(
                data.get("dnp_projection"),
                default.dnp_projection,
                field_name="assembly.dnp_projection",
            ),
            designator_color=str(
                data.get("designator_color", default.designator_color)
                or default.designator_color
            ),
            dnp_designator_color=str(
                data.get("dnp_designator_color", default.dnp_designator_color)
                or default.dnp_designator_color
            ),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "default_projection": self.default_projection,
            "dnp_projection": self.dnp_projection,
            "designator_color": self.designator_color,
            "dnp_designator_color": self.dnp_designator_color,
        }


@dataclass(slots=True)
class PcbSvgDnpConfig:
    """DNP projection and hatching defaults for PCB SVG component overlays."""

    color: str = cast(str, config_default("dnp", "color"))
    hatch: bool = cast(bool, config_default("dnp", "hatch"))
    hatch_spacing_mm: float = cast(float, config_default("dnp", "hatch_spacing_mm"))
    hatch_angle_deg: float = cast(float, config_default("dnp", "hatch_angle_deg"))
    hatch_line_width_mm: float = cast(
        float, config_default("dnp", "hatch_line_width_mm")
    )

    @classmethod
    def from_dict(cls, data: dict[str, object] | None) -> "PcbSvgDnpConfig":
        if data is None:
            return cls()
        if not isinstance(data, dict):
            raise ValueError("pcb-svg config field 'dnp' must be an object")
        default = cls()
        return cls(
            color=str(data.get("color", default.color) or default.color),
            hatch=_coerce_bool(data.get("hatch"), default.hatch),
            hatch_spacing_mm=_coerce_float(
                data.get("hatch_spacing_mm"),
                default.hatch_spacing_mm,
            ),
            hatch_angle_deg=_coerce_float(
                data.get("hatch_angle_deg"),
                default.hatch_angle_deg,
            ),
            hatch_line_width_mm=_coerce_float(
                data.get("hatch_line_width_mm"),
                default.hatch_line_width_mm,
            ),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "color": self.color,
            "hatch": self.hatch,
            "hatch_spacing_mm": self.hatch_spacing_mm,
            "hatch_angle_deg": self.hatch_angle_deg,
            "hatch_line_width_mm": self.hatch_line_width_mm,
        }


@dataclass(slots=True)
class PcbSvgDiodeConfig:
    """Diode detection and cathode-marker defaults for PCB SVG overlays."""

    enabled: bool = cast(bool, config_default("diodes", "enabled"))
    line_art: bool = cast(bool, config_default("diodes", "line_art"))
    marker_color: str = cast(str, config_default("diodes", "marker_color"))
    numeric_cathode_pad: str = cast(
        str, config_default("diodes", "numeric_cathode_pad")
    )
    cathode_pad_names: list[str] = field(
        default_factory=lambda: cast(
            list[str], config_default("diodes", "cathode_pad_names")
        )
    )
    designator_prefixes: list[str] = field(
        default_factory=lambda: cast(
            list[str], config_default("diodes", "designator_prefixes")
        )
    )
    parameter_terms: list[str] = field(
        default_factory=lambda: cast(
            list[str], config_default("diodes", "parameter_terms")
        )
    )

    @classmethod
    def from_dict(cls, data: dict[str, object] | None) -> "PcbSvgDiodeConfig":
        if data is None:
            return cls()
        if not isinstance(data, dict):
            raise ValueError("pcb-svg config field 'diodes' must be an object")
        default = cls()
        return cls(
            enabled=_coerce_bool(data.get("enabled"), default.enabled),
            line_art=_coerce_bool(data.get("line_art"), default.line_art),
            marker_color=str(
                data.get("marker_color", default.marker_color) or default.marker_color
            ),
            numeric_cathode_pad=str(
                data.get("numeric_cathode_pad", default.numeric_cathode_pad)
                or default.numeric_cathode_pad
            ),
            cathode_pad_names=_coerce_raw_str_list(
                data.get("cathode_pad_names"),
                default.cathode_pad_names,
                field_name="diodes.cathode_pad_names",
            ),
            designator_prefixes=_coerce_raw_str_list(
                data.get("designator_prefixes"),
                default.designator_prefixes,
                field_name="diodes.designator_prefixes",
            ),
            parameter_terms=_coerce_raw_str_list(
                data.get("parameter_terms"),
                default.parameter_terms,
                field_name="diodes.parameter_terms",
            ),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "enabled": self.enabled,
            "line_art": self.line_art,
            "marker_color": self.marker_color,
            "numeric_cathode_pad": self.numeric_cathode_pad,
            "cathode_pad_names": list(self.cathode_pad_names),
            "designator_prefixes": list(self.designator_prefixes),
            "parameter_terms": list(self.parameter_terms),
        }


@dataclass(slots=True)
class PcbSvgPin1Config:
    """Pin-1 overlay behavior defaults."""

    exclude_designator_prefixes: list[str] = field(
        default_factory=lambda: cast(
            list[str], config_default("pin1", "exclude_designator_prefixes")
        )
    )

    @classmethod
    def from_dict(cls, data: dict[str, object] | None) -> "PcbSvgPin1Config":
        if data is None:
            return cls()
        if not isinstance(data, dict):
            raise ValueError("pcb-svg config field 'pin1' must be an object")
        default = cls()
        prefixes = _coerce_raw_str_list(
            data.get("exclude_designator_prefixes"),
            default.exclude_designator_prefixes,
            field_name="pin1.exclude_designator_prefixes",
        )
        return cls(
            exclude_designator_prefixes=[
                prefix.upper() for prefix in prefixes if prefix.strip()
            ]
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "exclude_designator_prefixes": list(self.exclude_designator_prefixes),
        }


@dataclass(slots=True)
class PcbSvgComponentOverride:
    """Per-designator PCB SVG virtual assembly override."""

    side: str | None = cast(str | None, config_default("component", "side"))
    projection: str | None = cast(str | None, config_default("component", "projection"))
    assembly_hlr: dict[str, object] = field(
        default_factory=lambda: cast(
            dict[str, object], config_default("component", "assembly_hlr")
        )
    )
    pin1_enabled: bool | None = cast(
        bool | None, config_default("component", "pin1_enabled")
    )
    pin1_pad: str | None = cast(str | None, config_default("component", "pin1_pad"))
    cathode_pad: str | None = cast(
        str | None, config_default("component", "cathode_pad")
    )
    diode: bool | None = cast(bool | None, config_default("component", "diode"))
    diode_line_art: bool | None = cast(
        bool | None, config_default("component", "diode_line_art")
    )
    show_designator: bool | None = cast(
        bool | None, config_default("component", "show_designator")
    )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, object],
        *,
        designator: str,
    ) -> "PcbSvgComponentOverride":
        if not isinstance(data, dict):
            raise ValueError(
                f"pcb-svg config field 'components.{designator}' must be an object"
            )
        projection = None
        if data.get("projection") is not None:
            projection = _coerce_projection_mode(
                data.get("projection"),
                "detail",
                field_name=f"components.{designator}.projection",
            )
        assembly_hlr_raw = data.get("assembly_hlr")
        assembly_hlr: dict[str, object] = {}
        if assembly_hlr_raw is not None:
            if not isinstance(assembly_hlr_raw, Mapping):
                raise ValueError(
                    f"pcb-svg config field 'components.{designator}.assembly_hlr' "
                    "must be an object"
                )
            assembly_hlr = dict(assembly_hlr_raw)
        return cls(
            side=_coerce_component_side(
                data.get("side"),
                field_name=f"components.{designator}.side",
            ),
            projection=projection,
            assembly_hlr=assembly_hlr,
            pin1_enabled=(
                None
                if data.get("pin1_enabled") is None
                else _coerce_bool(data.get("pin1_enabled"), True)
            ),
            pin1_pad=_coerce_optional_str(data.get("pin1_pad")),
            cathode_pad=_coerce_optional_str(data.get("cathode_pad")),
            diode=(
                None
                if data.get("diode") is None
                else _coerce_bool(data.get("diode"), False)
            ),
            diode_line_art=(
                None
                if data.get("diode_line_art") is None
                else _coerce_bool(data.get("diode_line_art"), False)
            ),
            show_designator=(
                None
                if data.get("show_designator") is None
                else _coerce_bool(data.get("show_designator"), False)
            ),
        )

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {}
        if self.side is not None:
            result["side"] = self.side
        if self.projection is not None:
            result["projection"] = self.projection
        if self.assembly_hlr:
            result["assembly_hlr"] = dict(self.assembly_hlr)
        if self.pin1_enabled is not None:
            result["pin1_enabled"] = self.pin1_enabled
        if self.pin1_pad is not None:
            result["pin1_pad"] = self.pin1_pad
        if self.cathode_pad is not None:
            result["cathode_pad"] = self.cathode_pad
        if self.diode is not None:
            result["diode"] = self.diode
        if self.diode_line_art is not None:
            result["diode_line_art"] = self.diode_line_art
        if self.show_designator is not None:
            result["show_designator"] = self.show_designator
        return result


def _default_layer_outputs() -> dict[str, object]:
    return cast(dict[str, object], config_default("layer_outputs"))


def _normalize_layer_outputs(data: dict[str, object] | None) -> dict[str, object]:
    defaults = _default_layer_outputs()
    merged = dict(defaults)
    if data is None:
        return merged
    if not isinstance(data, dict):
        raise ValueError("pcb-svg config field 'layer_outputs' must be an object")
    merged.update(data)
    merged["enabled"] = _coerce_bool(merged.get("enabled"), bool(defaults["enabled"]))
    layers = merged.get("layers", defaults["layers"])
    if isinstance(layers, str) and layers.strip().lower() == "auto":
        merged["layers"] = "auto"
    else:
        merged["layers"] = _coerce_str_list(layers, field_name="layer_outputs.layers")
    merged["include_special_layers"] = _coerce_str_list(
        merged.get("include_special_layers"),
        field_name="layer_outputs.include_special_layers",
    )
    merged["output_dir"] = str(merged.get("output_dir") or defaults["output_dir"])
    return merged


def _normalize_component_overrides(
    data: dict[str, object] | None,
) -> dict[str, PcbSvgComponentOverride]:
    if data is None:
        return {}
    result: dict[str, PcbSvgComponentOverride] = {}
    for raw_designator, raw_override in data.items():
        designator = str(raw_designator).strip()
        if not designator:
            raise ValueError(
                "pcb-svg config field 'components' has an empty designator"
            )
        if not isinstance(raw_override, dict):
            raise ValueError(
                f"pcb-svg config field 'components.{designator}' must be an object"
            )
        result[designator] = PcbSvgComponentOverride.from_dict(
            raw_override,
            designator=designator,
        )
    return result


def _default_pcb_svg_views() -> list[PcbSvgViewConfig]:
    return [
        PcbSvgViewConfig.from_dict(view)
        for view in cast(list[dict[str, object]], config_default("views"))
    ]


@dataclass(slots=True)
class PcbSvgConfig:
    """Root pcb-svg A1 configuration model."""

    schema: str = PCB_SVG_CONFIG_SCHEMA
    global_options: PcbSvgGlobalConfig = field(default_factory=PcbSvgGlobalConfig)
    assembly: PcbSvgAssemblyConfig = field(default_factory=PcbSvgAssemblyConfig)
    dnp: PcbSvgDnpConfig = field(default_factory=PcbSvgDnpConfig)
    diodes: PcbSvgDiodeConfig = field(default_factory=PcbSvgDiodeConfig)
    pin1: PcbSvgPin1Config = field(default_factory=PcbSvgPin1Config)
    components: dict[str, PcbSvgComponentOverride] = field(default_factory=dict)
    layer_outputs: dict[str, object] = field(default_factory=_default_layer_outputs)
    views: list[PcbSvgViewConfig] = field(default_factory=_default_pcb_svg_views)

    @classmethod
    def default(cls) -> "PcbSvgConfig":
        return cls()

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "PcbSvgConfig":
        if not isinstance(data, dict):
            raise ValueError("pcb-svg config root must be a JSON object")
        source_schema = str(data.get("schema") or PCB_SVG_CONFIG_SCHEMA)
        if source_schema not in {PCB_SVG_CONFIG_SCHEMA, *PCB_SVG_CONFIG_LEGACY_SCHEMAS}:
            raise ValueError(
                f"Unsupported pcb-svg config schema: {source_schema!r}; "
                f"expected {PCB_SVG_CONFIG_SCHEMA!r} or an additive predecessor"
            )
        raw_views = data.get("views")
        if raw_views is None:
            views = _default_pcb_svg_views()
        else:
            if not isinstance(raw_views, list):
                raise ValueError("pcb-svg config field 'views' must be an array")
            views = [PcbSvgViewConfig.from_dict(item) for item in raw_views]
        return cls(
            # Resolved/written configs use the current discriminator. Authored
            # A0 files are accepted without being rewritten during ordinary use.
            schema=PCB_SVG_CONFIG_SCHEMA,
            global_options=PcbSvgGlobalConfig.from_dict(
                _coerce_object_mapping(data.get("global"), field_name="global")
            ),
            assembly=PcbSvgAssemblyConfig.from_dict(
                _coerce_object_mapping(data.get("assembly"), field_name="assembly")
            ),
            dnp=PcbSvgDnpConfig.from_dict(
                _coerce_object_mapping(data.get("dnp"), field_name="dnp")
            ),
            diodes=PcbSvgDiodeConfig.from_dict(
                _coerce_object_mapping(data.get("diodes"), field_name="diodes")
            ),
            pin1=PcbSvgPin1Config.from_dict(
                _coerce_object_mapping(data.get("pin1"), field_name="pin1")
            ),
            components=_normalize_component_overrides(
                _coerce_object_mapping(
                    data.get("components"),
                    field_name="components",
                )
            ),
            layer_outputs=_normalize_layer_outputs(
                _coerce_object_mapping(
                    data.get("layer_outputs"),
                    field_name="layer_outputs",
                )
            ),
            views=views,
        )

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "schema": self.schema,
            "global": self.global_options.to_dict(),
            "pin1": self.pin1.to_dict(),
            "layer_outputs": dict(self.layer_outputs),
            "views": [view.to_dict() for view in self.views],
        }
        if self.assembly != PcbSvgAssemblyConfig():
            result["assembly"] = self.assembly.to_dict()
        if self.dnp != PcbSvgDnpConfig():
            result["dnp"] = self.dnp.to_dict()
        if self.diodes != PcbSvgDiodeConfig():
            result["diodes"] = self.diodes.to_dict()
        if self.components:
            result["components"] = {
                designator: override.to_dict()
                for designator, override in sorted(self.components.items())
            }
        return result

    def enabled_views(self) -> list[PcbSvgViewConfig]:
        return [view for view in self.views if view.enabled]

    def resolved_styles_for_view(
        self, view: PcbSvgViewConfig
    ) -> dict[str, dict[str, object]]:
        return merge_pcb_svg_styles(self.global_options.styles, view.styles)


def pcb_svg_config_template_payload(
    config: PcbSvgConfig | None = None,
) -> dict[str, object]:
    """Return the generated editable config payload with optional sections exposed."""
    template = config or PcbSvgConfig.default()
    payload = template.to_dict()
    payload.setdefault("assembly", template.assembly.to_dict())
    payload.setdefault("dnp", template.dnp.to_dict())
    payload.setdefault("diodes", template.diodes.to_dict())
    payload.setdefault("components", {})
    return payload


def pcb_svg_config_text(config: PcbSvgConfig | None = None) -> str:
    """Render an editable PCB SVG config as commented JSONC."""
    return render_commented_jsonc(
        pcb_svg_config_template_payload(config),
        comments_by_path=_PCB_SVG_CONFIG_COMMENTS,
        comments_by_key=_PCB_SVG_CONFIG_KEY_COMMENTS,
    )


def resolve_config_output_path(
    output_dir: Path, pattern: str, *, board: str, view: str
) -> Path:
    """Resolve an A0 output pattern relative to the command output directory."""
    safe_board = board.replace("/", "_").replace("\\", "_")
    safe_view = view.replace("/", "_").replace("\\", "_")
    text = pattern.format(board=safe_board, view=safe_view)
    path = Path(text)
    if not path.is_absolute():
        path = output_dir / path
    return path


__all__ = [
    "PCB_DEFAULT_SVG_SCALE",
    "PCB_SVG_CANVAS_BOUNDS_MODES",
    "PCB_SVG_COMPONENT_PROJECTION_MODES",
    "PCB_SVG_COMPONENT_SIDES",
    "PCB_SVG_CONFIG_FILENAME",
    "PCB_SVG_CONFIG_SCHEMA",
    "PCB_SVG_CONFIG_LEGACY_SCHEMAS",
    "PCB_SVG_SPECIAL_LAYERS",
    "PcbSvgAssemblyConfig",
    "PcbSvgConfig",
    "PcbSvgCanvasConfig",
    "PcbSvgComponentOverride",
    "PcbSvgDiodeConfig",
    "PcbSvgDnpConfig",
    "PcbSvgGlobalConfig",
    "PcbSvgPin1Config",
    "PcbSvgViewConfig",
    "default_pcb_svg_styles",
    "merge_pcb_svg_styles",
    "parse_pcb_layer_selector",
    "pcb_svg_physical_layer_from_token",
    "pcb_svg_config_template_payload",
    "pcb_svg_config_text",
    "resolve_config_output_path",
]
