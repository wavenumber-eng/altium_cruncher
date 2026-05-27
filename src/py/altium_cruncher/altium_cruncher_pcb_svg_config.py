"""A0 config model for explicit PCB SVG layer/view rendering."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

from altium_monkey.altium_record_types import PcbLayer

PCB_SVG_CONFIG_FILENAME = "pcb.svg.config"
PCB_SVG_CONFIG_SCHEMA = "pcb.svg.config.a0"
PCB_DEFAULT_SVG_SCALE = 10.0
PCB_SVG_CANVAS_BOUNDS_MODES = frozenset({"board_outline", "all_geometry"})

PCB_SVG_SPECIAL_LAYERS = frozenset(
    {
        "BOARD_OUTLINE",
        "BOARD_CUTOUTS",
        "DRILLS",
        "SLOTS",
        "ASSEMBLY_HLR_TOP",
        "ASSEMBLY_HLR_BOTTOM",
    }
)

_STYLE_ORDER = (
    "board_outline",
    "board_cutouts",
    "drills",
    "slots",
    "copper_traces",
    "vias",
    "copper_polygons",
    "smd_pads",
    "through_hole_pads",
    "silkscreen_component_graphics",
    "silkscreen_designators",
    "silkscreen_board_graphics",
    "keepout",
    "assembly_hlr",
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


def _coerce_nonnegative_float(value: object, default: float, *, field_name: str) -> float:
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
        return PcbLayer.from_json_name(normalized).to_json_name()
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


def pcb_svg_physical_layer_from_token(token: str) -> PcbLayer | None:
    """Return a physical PcbLayer for a token, or None for A0 synthetic layers."""
    normalized = _normalize_layer_token(token)
    if normalized in PCB_SVG_SPECIAL_LAYERS:
        return None
    return PcbLayer.from_json_name(normalized)


def default_pcb_svg_styles() -> dict[str, dict[str, object]]:
    """Return the default A0 style table."""
    return {
        "board_outline": {
            "enabled": True,
            "color": "#000000",
            "line_width_mm": 0.10,
        },
        "board_cutouts": {
            "enabled": True,
            "color": "#FF0000",
            "hatch": True,
            "hatch_spacing_mm": 2.0,
            "hatch_angle_deg": 45.0,
            "hatch_line_width_mm": 0.08,
            "outline_style": "solid",
            "outline_dash_mm": 1.5,
            "outline_width_mm": 0.15,
        },
        "drills": {
            "enabled": True,
            "plated_color": "#90EE90",
            "non_plated_color": "#ADD8E6",
            "opacity": 1.0,
        },
        "slots": {
            "enabled": True,
            "plated_color": "#90EE90",
            "non_plated_color": "#ADD8E6",
            "opacity": 1.0,
        },
        "copper_traces": {"enabled": True, "color": "#000000"},
        "vias": {"enabled": True, "color": "#000000"},
        "copper_polygons": {"enabled": True, "color": "#888888"},
        "smd_pads": {"enabled": True, "color": "#000000"},
        "through_hole_pads": {"enabled": True, "color": "#000000"},
        "silkscreen_component_graphics": {"enabled": True, "color": "#000000"},
        "silkscreen_designators": {"enabled": True, "color": "#000000"},
        "silkscreen_board_graphics": {"enabled": True, "color": "#000000"},
        "keepout": {"enabled": True, "color": "#CC00CC"},
        "assembly_hlr": {
            "enabled": True,
            "color": "#F59E0B",
            "curve_mode": "native_arcs",
            "samples_per_curve": 24,
            "round_digits": 3,
            "include_visible": True,
            "include_outline": True,
            "union_polygons": True,
        },
    }


def merge_pcb_svg_styles(
    base: dict[str, dict[str, object]],
    override: Mapping[str, object] | None,
) -> dict[str, dict[str, object]]:
    """Merge an A0 style table while preserving default style keys."""
    merged = {name: dict(base.get(name, {})) for name in _STYLE_ORDER}
    if override:
        for name, raw_style in override.items():
            if not isinstance(raw_style, dict):
                raise ValueError(f"pcb-svg style '{name}' must be an object")
            target = merged.setdefault(str(name), {})
            target.update(raw_style)
    return merged


def _coerce_object_mapping(value: object, *, field_name: str) -> dict[str, object] | None:
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise ValueError(f"pcb-svg config field '{field_name}' must be an object")
    return {str(key): item for key, item in value.items()}


@dataclass(slots=True)
class PcbSvgCanvasConfig:
    """Canvas normalization policy for PCB SVG viewBox coordinates."""

    bounds: str = "board_outline"
    margin_mm: float = 1.0

    @classmethod
    def from_dict(cls, data: dict[str, object] | None) -> "PcbSvgCanvasConfig":
        if data is None:
            return cls()
        if not isinstance(data, dict):
            raise ValueError("pcb-svg config field 'global.canvas' must be an object")
        bounds = str(data.get("bounds", "board_outline") or "board_outline").strip().lower()
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
                1.0,
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

    pcbdoc: str | None = None
    canvas: PcbSvgCanvasConfig = field(default_factory=PcbSvgCanvasConfig)
    include_metadata: bool = True
    show_empty_layers: bool = False
    clip_to_outline: bool = True
    clip_holes_from_copper: bool = True
    mirror_bottom_view: bool = True
    svg_scale: float = PCB_DEFAULT_SVG_SCALE
    svg_size_unit: str = ""
    clean_output: bool = False
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
        return {
            "pcbdoc": self.pcbdoc,
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


@dataclass(slots=True)
class PcbSvgViewConfig:
    """One explicit A0 composed PCB SVG view."""

    name: str
    enabled: bool = True
    group_id: str | None = None
    output_svg: str | None = None
    layers: list[str] = field(default_factory=list)
    mirror: bool | None = None
    assembly_hlr_mode: str = "detail"
    styles: dict[str, dict[str, object]] = field(default_factory=dict)
    description: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "PcbSvgViewConfig":
        if not isinstance(data, dict):
            raise ValueError("Each item in pcb-svg config 'views' must be an object")
        name = _coerce_optional_str(data.get("name"))
        if not name:
            raise ValueError("Each pcb-svg view must include a non-empty 'name'")
        mode = str(data.get("assembly_hlr_mode", "detail") or "detail").lower()
        if mode not in {"simple", "detail", "detailed"}:
            raise ValueError(
                f"Unsupported assembly_hlr_mode {mode!r} for pcb-svg view {name!r}"
            )
        if mode == "detailed":
            mode = "detail"
        styles = _coerce_object_mapping(
            data.get("styles"),
            field_name=f"views.{name}.styles",
        ) or {}
        return cls(
            name=name,
            enabled=_coerce_bool(data.get("enabled"), True),
            group_id=_coerce_optional_str(data.get("group_id")),
            output_svg=_coerce_optional_str(data.get("output_svg")),
            layers=_coerce_str_list(data.get("layers"), field_name=f"views.{name}.layers"),
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


def _default_layer_outputs() -> dict[str, object]:
    return {
        "enabled": True,
        "layers": "auto",
        "include_special_layers": [
            "BOARD_OUTLINE",
            "BOARD_CUTOUTS",
            "DRILLS",
            "SLOTS",
        ],
        "output_dir": "layers",
    }


def _normalize_layer_outputs(data: dict[str, object] | None) -> dict[str, object]:
    merged = _default_layer_outputs()
    if data is None:
        return merged
    if not isinstance(data, dict):
        raise ValueError("pcb-svg config field 'layer_outputs' must be an object")
    merged.update(data)
    merged["enabled"] = _coerce_bool(merged.get("enabled"), True)
    layers = merged.get("layers", "auto")
    if isinstance(layers, str) and layers.strip().lower() == "auto":
        merged["layers"] = "auto"
    else:
        merged["layers"] = _coerce_str_list(layers, field_name="layer_outputs.layers")
    merged["include_special_layers"] = _coerce_str_list(
        merged.get("include_special_layers"),
        field_name="layer_outputs.include_special_layers",
    )
    merged["output_dir"] = str(merged.get("output_dir") or "layers")
    return merged


def _default_pcb_svg_views() -> list[PcbSvgViewConfig]:
    return [
        PcbSvgViewConfig(
            name="top_view",
            group_id="pcb-svg-view-top",
            output_svg="views/{board}__top_view.svg",
            layers=[
                "BOARD_OUTLINE",
                "TOP",
                "TOPOVERLAY",
                "BOARD_CUTOUTS",
                "DRILLS",
                "SLOTS",
                "ASSEMBLY_HLR_TOP",
            ],
            mirror=False,
            assembly_hlr_mode="detail",
            description="Top view",
        ),
        PcbSvgViewConfig(
            name="bottom_view",
            group_id="pcb-svg-view-bottom",
            output_svg="views/{board}__bottom_view.svg",
            layers=[
                "BOARD_OUTLINE",
                "BOTTOM",
                "BOTTOMOVERLAY",
                "BOARD_CUTOUTS",
                "DRILLS",
                "SLOTS",
                "ASSEMBLY_HLR_BOTTOM",
            ],
            mirror=True,
            assembly_hlr_mode="detail",
            description="Bottom view",
        ),
        PcbSvgViewConfig(
            name="board_cutouts",
            group_id="pcb-svg-view-board-cutouts",
            output_svg="views/{board}__board_cutouts.svg",
            layers=["BOARD_OUTLINE", "BOARD_CUTOUTS"],
            mirror=False,
            description="Board cutouts",
        ),
    ]


@dataclass(slots=True)
class PcbSvgConfig:
    """Root pcb-svg A0 configuration model."""

    schema: str = PCB_SVG_CONFIG_SCHEMA
    global_options: PcbSvgGlobalConfig = field(default_factory=PcbSvgGlobalConfig)
    layer_outputs: dict[str, object] = field(default_factory=_default_layer_outputs)
    views: list[PcbSvgViewConfig] = field(default_factory=_default_pcb_svg_views)

    @classmethod
    def default(cls) -> "PcbSvgConfig":
        return cls()

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "PcbSvgConfig":
        if not isinstance(data, dict):
            raise ValueError("pcb-svg config root must be a JSON object")
        schema = str(data.get("schema") or PCB_SVG_CONFIG_SCHEMA)
        if schema != PCB_SVG_CONFIG_SCHEMA:
            raise ValueError(
                f"Unsupported pcb-svg config schema: {schema!r}; "
                f"expected {PCB_SVG_CONFIG_SCHEMA!r}"
            )
        raw_views = data.get("views")
        if raw_views is None:
            views = _default_pcb_svg_views()
        else:
            if not isinstance(raw_views, list):
                raise ValueError("pcb-svg config field 'views' must be an array")
            views = [PcbSvgViewConfig.from_dict(item) for item in raw_views]
        return cls(
            schema=schema,
            global_options=PcbSvgGlobalConfig.from_dict(
                _coerce_object_mapping(data.get("global"), field_name="global")
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
        return {
            "schema": self.schema,
            "global": self.global_options.to_dict(),
            "layer_outputs": dict(self.layer_outputs),
            "views": [view.to_dict() for view in self.views],
        }

    def enabled_views(self) -> list[PcbSvgViewConfig]:
        return [view for view in self.views if view.enabled]

    def resolved_styles_for_view(self, view: PcbSvgViewConfig) -> dict[str, dict[str, object]]:
        return merge_pcb_svg_styles(self.global_options.styles, view.styles)


def resolve_config_output_path(output_dir: Path, pattern: str, *, board: str, view: str) -> Path:
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
    "PCB_SVG_CONFIG_FILENAME",
    "PCB_SVG_CONFIG_SCHEMA",
    "PCB_SVG_SPECIAL_LAYERS",
    "PcbSvgConfig",
    "PcbSvgCanvasConfig",
    "PcbSvgGlobalConfig",
    "PcbSvgViewConfig",
    "default_pcb_svg_styles",
    "merge_pcb_svg_styles",
    "parse_pcb_layer_selector",
    "pcb_svg_physical_layer_from_token",
    "resolve_config_output_path",
]
