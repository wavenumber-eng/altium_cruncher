"""PcbLib cleanup transforms used by the altium-cruncher clean workflow."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from altium_cruncher.config_json import load_json_config

PCBLIB_CLEAN_CONFIG_SCHEMA_V1 = "wn.altium.pcblib.clean.config.v1"
DEFAULT_PCBLIB_CLEAN_CONFIG_FILENAME = "altium-pcblib-clean.json"
PcbLibCleanProfile = Literal["raw", "default"]


@dataclass(slots=True)
class PcbLibMechanicalPrimitiveRemovalConfig:
    enabled: bool = True
    primitive_types: tuple[str, ...] = ("tracks", "arcs", "fills", "texts")
    layers: tuple[str, ...] = ("mechanical",)
    preserve_regions: bool = True
    preserve_component_bodies: bool = True

    @classmethod
    def from_dict(
        cls,
        data: object,
    ) -> PcbLibMechanicalPrimitiveRemovalConfig:
        default = cls()
        if data is None:
            return default
        if not isinstance(data, dict):
            raise ValueError("remove_mechanical_primitives must be a JSON object")
        return cls(
            enabled=_coerce_bool(data.get("enabled"), default.enabled),
            primitive_types=_coerce_string_tuple(
                data.get("primitive_types"),
                default.primitive_types,
                field_name="remove_mechanical_primitives.primitive_types",
            ),
            layers=_coerce_string_tuple(
                data.get("layers"),
                default.layers,
                field_name="remove_mechanical_primitives.layers",
            ),
            preserve_regions=_coerce_bool(
                data.get("preserve_regions"),
                default.preserve_regions,
            ),
            preserve_component_bodies=_coerce_bool(
                data.get("preserve_component_bodies"),
                default.preserve_component_bodies,
            ),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "enabled": self.enabled,
            "primitive_types": list(self.primitive_types),
            "layers": list(self.layers),
            "preserve_regions": self.preserve_regions,
            "preserve_component_bodies": self.preserve_component_bodies,
        }


@dataclass(slots=True)
class PcbLibTextStringRemovalConfig:
    enabled: bool = True
    layers: tuple[str, ...] = ("any",)
    match: str = "regex"
    patterns: tuple[str, ...] = (r"(?i)\bdesignator\b",)

    @classmethod
    def from_dict(cls, data: object) -> PcbLibTextStringRemovalConfig:
        default = cls()
        if data is None:
            return default
        if not isinstance(data, dict):
            raise ValueError("remove_text_strings must be a JSON object")

        match = str(data.get("match", default.match) or default.match).strip().lower()
        if match not in {"all", "regex", "contains", "exact"}:
            raise ValueError(
                "remove_text_strings.match must be one of: all, regex, contains, exact"
            )

        patterns = _coerce_pattern_tuple(
            data.get("patterns"),
            default.patterns,
            field_name="remove_text_strings.patterns",
        )
        if match == "regex":
            _validate_regex_patterns(patterns, field_name="remove_text_strings.patterns")

        return cls(
            enabled=_coerce_bool(data.get("enabled"), default.enabled),
            layers=_coerce_string_tuple(
                data.get("layers"),
                default.layers,
                field_name="remove_text_strings.layers",
            ),
            match=match,
            patterns=patterns,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "enabled": self.enabled,
            "layers": list(self.layers),
            "match": self.match,
            "patterns": list(self.patterns),
        }


@dataclass(slots=True)
class PcbLibRegionRemovalConfig:
    enabled: bool = True
    layers: tuple[str, ...] = ("mechanical",)
    preserve_component_linked: bool = True
    preserve_model_associated: bool = True
    preserve_keepouts: bool = True
    preserve_board_cutouts: bool = True
    preserve_custom_pad_regions: bool = True

    @classmethod
    def from_dict(cls, data: object) -> PcbLibRegionRemovalConfig:
        default = cls()
        if data is None:
            return default
        if not isinstance(data, dict):
            raise ValueError("remove_regions must be a JSON object")
        return cls(
            enabled=_coerce_bool(data.get("enabled"), default.enabled),
            layers=_coerce_string_tuple(
                data.get("layers"),
                default.layers,
                field_name="remove_regions.layers",
            ),
            preserve_component_linked=_coerce_bool(
                data.get("preserve_component_linked"),
                default.preserve_component_linked,
            ),
            preserve_model_associated=_coerce_bool(
                data.get("preserve_model_associated"),
                default.preserve_model_associated,
            ),
            preserve_keepouts=_coerce_bool(
                data.get("preserve_keepouts"),
                default.preserve_keepouts,
            ),
            preserve_board_cutouts=_coerce_bool(
                data.get("preserve_board_cutouts"),
                default.preserve_board_cutouts,
            ),
            preserve_custom_pad_regions=_coerce_bool(
                data.get("preserve_custom_pad_regions"),
                default.preserve_custom_pad_regions,
            ),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "enabled": self.enabled,
            "layers": list(self.layers),
            "preserve_component_linked": self.preserve_component_linked,
            "preserve_model_associated": self.preserve_model_associated,
            "preserve_keepouts": self.preserve_keepouts,
            "preserve_board_cutouts": self.preserve_board_cutouts,
            "preserve_custom_pad_regions": self.preserve_custom_pad_regions,
        }


@dataclass(slots=True)
class PcbLibCleanConfig:
    schema: str = PCBLIB_CLEAN_CONFIG_SCHEMA_V1
    profile: str = "default"
    remove_mechanical_primitives: PcbLibMechanicalPrimitiveRemovalConfig = field(
        default_factory=PcbLibMechanicalPrimitiveRemovalConfig
    )
    remove_text_strings: PcbLibTextStringRemovalConfig = field(
        default_factory=PcbLibTextStringRemovalConfig
    )
    remove_regions: PcbLibRegionRemovalConfig = field(
        default_factory=PcbLibRegionRemovalConfig
    )

    @classmethod
    def from_dict(cls, data: object) -> PcbLibCleanConfig:
        if not isinstance(data, dict):
            raise ValueError("PcbLib clean config must be a JSON object")
        schema = str(
            data.get("schema", PCBLIB_CLEAN_CONFIG_SCHEMA_V1)
            or PCBLIB_CLEAN_CONFIG_SCHEMA_V1
        ).strip()
        if schema != PCBLIB_CLEAN_CONFIG_SCHEMA_V1:
            raise ValueError(f"Unsupported PcbLib clean config schema: {schema!r}")
        profile = str(data.get("profile", "default") or "default").strip() or "default"
        return cls(
            schema=schema,
            profile=profile,
            remove_mechanical_primitives=PcbLibMechanicalPrimitiveRemovalConfig.from_dict(
                data.get("remove_mechanical_primitives")
            ),
            remove_text_strings=PcbLibTextStringRemovalConfig.from_dict(
                data.get("remove_text_strings")
            ),
            remove_regions=PcbLibRegionRemovalConfig.from_dict(
                data.get("remove_regions")
            ),
        )

    @classmethod
    def template(cls) -> PcbLibCleanConfig:
        return cls()

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": self.schema,
            "profile": self.profile,
            "remove_mechanical_primitives": self.remove_mechanical_primitives.to_dict(),
            "remove_text_strings": self.remove_text_strings.to_dict(),
            "remove_regions": self.remove_regions.to_dict(),
        }

    @classmethod
    def from_file(cls, path: str | Path) -> PcbLibCleanConfig:
        config_path = Path(path)
        try:
            raw = load_json_config(config_path)
        except Exception as exc:
            raise ValueError(f"Invalid JSON in PcbLib clean config: {config_path}: {exc}") from exc
        return cls.from_dict(raw)


@dataclass(slots=True)
class PcbLibFootprintCleanReport:
    footprint_name: str
    removed_by_collection: dict[str, int] = field(default_factory=dict)
    removed_by_layer: dict[str, int] = field(default_factory=dict)
    preserved_region_count: int = 0
    preserved_component_body_count: int = 0

    @property
    def total_removed(self) -> int:
        return sum(self.removed_by_collection.values())


@dataclass(slots=True)
class PcbLibCleanApplyResult:
    profile: str
    footprint_reports: list[PcbLibFootprintCleanReport] = field(default_factory=list)

    @property
    def total_footprints(self) -> int:
        return len(self.footprint_reports)

    @property
    def total_removed(self) -> int:
        return sum(report.total_removed for report in self.footprint_reports)

    @property
    def removed_by_collection(self) -> dict[str, int]:
        totals: dict[str, int] = {}
        for report in self.footprint_reports:
            for key, count in report.removed_by_collection.items():
                totals[key] = totals.get(key, 0) + count
        return totals

    @property
    def removed_by_layer(self) -> dict[str, int]:
        totals: dict[str, int] = {}
        for report in self.footprint_reports:
            for key, count in report.removed_by_layer.items():
                totals[key] = totals.get(key, 0) + count
        return totals


def normalize_pcblib_clean_profile(value: str | None) -> PcbLibCleanProfile:
    normalized = str(value or "default").strip().lower()
    if normalized in {"raw", "none", "off"}:
        return "raw"
    if normalized in {"default", "clean", "wn-default"}:
        return "default"
    raise ValueError(f"Unsupported PcbLib clean profile: {value}")


def load_default_pcblib_clean_config(
    *,
    start_dir: str | Path | None = None,
    env: dict[str, str] | None = None,
) -> tuple[PcbLibCleanConfig, Path | None]:
    config_path = find_workspace_pcblib_clean_config_path(
        start_dir=start_dir,
        env=env,
    )
    if config_path is not None and config_path.exists():
        return PcbLibCleanConfig.from_file(config_path), config_path
    return PcbLibCleanConfig.template(), None


def find_workspace_pcblib_clean_config_path(
    *,
    start_dir: str | Path | None = None,
    env: dict[str, str] | None = None,
) -> Path | None:
    config_dir = _find_hw_config_dir(start_dir=start_dir, env=env)
    if config_dir is None:
        return None
    return config_dir / DEFAULT_PCBLIB_CLEAN_CONFIG_FILENAME


def apply_clean_to_pcblib(pcblib: object, config: PcbLibCleanConfig) -> PcbLibCleanApplyResult:
    reports = [
        apply_clean_to_pcblib_footprint(footprint, config)
        for footprint in getattr(pcblib, "footprints", []) or []
    ]
    return PcbLibCleanApplyResult(profile=config.profile, footprint_reports=reports)


def apply_clean_to_pcblib_footprint(
    footprint: object,
    config: PcbLibCleanConfig,
) -> PcbLibFootprintCleanReport:
    report = PcbLibFootprintCleanReport(
        footprint_name=str(getattr(footprint, "name", "") or ""),
        preserved_region_count=len(getattr(footprint, "regions", []) or []),
        preserved_component_body_count=len(getattr(footprint, "component_bodies", []) or []),
    )

    removal = config.remove_mechanical_primitives
    removed_ids: set[int] = set()

    if removal.enabled:
        remove_collections = {
            _normalize_collection_name(name)
            for name in removal.primitive_types
            if _normalize_collection_name(name)
        }
        for collection_name in ("tracks", "arcs", "fills", "texts"):
            if collection_name not in remove_collections:
                continue
            collection = list(getattr(footprint, collection_name, []) or [])
            kept: list[object] = []
            removed_count = 0
            for primitive in collection:
                layer = getattr(primitive, "layer", None)
                if _matches_layer_policy(layer, removal.layers):
                    removed_ids.add(id(primitive))
                    removed_count += 1
                    layer_key = _layer_report_key(layer)
                    report.removed_by_layer[layer_key] = (
                        report.removed_by_layer.get(layer_key, 0) + 1
                    )
                else:
                    kept.append(primitive)
            if removed_count:
                setattr(footprint, collection_name, kept)
                report.removed_by_collection[collection_name] = removed_count

    text_removal = config.remove_text_strings
    if text_removal.enabled:
        collection = list(getattr(footprint, "texts", []) or [])
        kept: list[object] = []
        removed_count = 0
        for text_primitive in collection:
            layer = getattr(text_primitive, "layer", None)
            if _matches_layer_policy(layer, text_removal.layers) and _matches_text_string_policy(
                _primitive_text_content(text_primitive),
                text_removal,
            ):
                removed_ids.add(id(text_primitive))
                removed_count += 1
                layer_key = _layer_report_key(layer)
                report.removed_by_layer[layer_key] = (
                    report.removed_by_layer.get(layer_key, 0) + 1
                )
            else:
                kept.append(text_primitive)
        if removed_count:
            setattr(footprint, "texts", kept)
            report.removed_by_collection["texts"] = (
                report.removed_by_collection.get("texts", 0) + removed_count
            )

    region_removal = config.remove_regions
    if region_removal.enabled:
        collection = list(getattr(footprint, "regions", []) or [])
        kept_regions: list[object] = []
        removed_count = 0
        for region in collection:
            layer = getattr(region, "layer", None)
            if _matches_layer_policy(layer, region_removal.layers) and not _preserve_region(
                region,
                region_removal,
            ):
                removed_ids.add(id(region))
                removed_count += 1
                layer_key = _layer_report_key(layer)
                report.removed_by_layer[layer_key] = (
                    report.removed_by_layer.get(layer_key, 0) + 1
                )
            else:
                kept_regions.append(region)
        if removed_count:
            setattr(footprint, "regions", kept_regions)
            report.removed_by_collection["regions"] = removed_count

    if removed_ids:
        record_order = list(getattr(footprint, "_record_order", []) or [])
        setattr(
            footprint,
            "_record_order",
            [primitive for primitive in record_order if id(primitive) not in removed_ids],
        )

    return report


def infer_pcblib_clean_config_path(
    input_file: Path,
    *,
    config_filename: str = DEFAULT_PCBLIB_CLEAN_CONFIG_FILENAME,
) -> Path:
    workspace_config = find_workspace_pcblib_clean_config_path(start_dir=input_file)
    if workspace_config is not None and workspace_config.exists():
        return workspace_config
    return input_file.resolve().parent / config_filename


def _coerce_bool(value: object, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "on"}:
        return True
    if text in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"Invalid boolean value in PcbLib clean config: {value!r}")


def _coerce_string_tuple(
    value: object,
    default: tuple[str, ...],
    *,
    field_name: str,
) -> tuple[str, ...]:
    if value is None:
        return default
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a JSON array")
    result = tuple(str(item).strip().lower() for item in value if str(item).strip())
    return result or default


def _coerce_pattern_tuple(
    value: object,
    default: tuple[str, ...],
    *,
    field_name: str,
) -> tuple[str, ...]:
    if value is None:
        return default
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a JSON array")
    result = tuple(str(item).strip() for item in value if str(item).strip())
    return result or default


def _validate_regex_patterns(patterns: tuple[str, ...], *, field_name: str) -> None:
    for pattern in patterns:
        try:
            re.compile(pattern)
        except re.error as exc:
            raise ValueError(f"Invalid regex in {field_name}: {pattern!r}: {exc}") from exc


def _normalize_collection_name(value: str) -> str:
    normalized = value.strip().lower().replace("-", "_")
    aliases = {
        "track": "tracks",
        "tracks": "tracks",
        "line": "tracks",
        "lines": "tracks",
        "arc": "arcs",
        "arcs": "arcs",
        "fill": "fills",
        "fills": "fills",
        "text": "texts",
        "texts": "texts",
        "string": "texts",
        "strings": "texts",
    }
    return aliases.get(normalized, "")


def _matches_layer_policy(layer: object, layer_policy: tuple[str, ...]) -> bool:
    if not layer_policy:
        return False
    normalized = {_normalize_layer_policy_token(item) for item in layer_policy if item.strip()}
    if normalized.intersection({"any", "all", "*"}):
        return True
    if "mechanical" in normalized and _is_mechanical_layer(layer):
        return True
    layer_id = _coerce_layer_id(layer)
    layer_name = _normalize_layer_policy_token(_layer_report_key(layer))
    return (
        str(layer_id) in normalized
        if layer_id is not None
        else False
    ) or layer_name.lower() in normalized


def _matches_text_string_policy(
    text: str,
    config: PcbLibTextStringRemovalConfig,
) -> bool:
    if config.match == "all":
        return True
    if not text:
        return False
    if config.match == "regex":
        return any(re.search(pattern, text) is not None for pattern in config.patterns)
    text_lower = text.lower()
    if config.match == "contains":
        return any(pattern.lower() in text_lower for pattern in config.patterns)
    if config.match == "exact":
        return any(pattern.lower() == text_lower for pattern in config.patterns)
    return False


def _preserve_region(
    region: object,
    config: PcbLibRegionRemovalConfig,
) -> bool:
    if config.preserve_keepouts and bool(getattr(region, "is_keepout", False)):
        return True
    if config.preserve_board_cutouts and _is_board_cutout_region(region):
        return True
    if config.preserve_custom_pad_regions and _is_custom_pad_region(region):
        return True
    if config.preserve_component_linked and _is_component_linked_region(region):
        return True
    if config.preserve_model_associated and _is_model_associated_region(region):
        return True
    return False


def _is_board_cutout_region(region: object) -> bool:
    props = _primitive_properties(region)
    if str(props.get("ISBOARDCUTOUT", "")).strip().lower() == "true":
        return True
    if bool(getattr(region, "is_board_cutout", False)):
        return True
    try:
        return int(getattr(region, "kind", 0) or 0) == 3
    except (TypeError, ValueError):
        return False


def _is_custom_pad_region(region: object) -> bool:
    props = _primitive_properties(region)
    return any(
        str(key).upper() in {"PADINDEX", "PADGUID", "PADSTACKID"}
        for key in props
    )


def _is_component_linked_region(region: object) -> bool:
    value = getattr(region, "component_index", None)
    if value is None:
        return False
    try:
        return int(value) not in {-1, 0, 0xFFFF}
    except (TypeError, ValueError):
        return bool(str(value).strip())


def _is_model_associated_region(region: object) -> bool:
    marker_attrs = ("model_id", "model_name", "model_source", "model_type")
    for attr_name in marker_attrs:
        value = getattr(region, attr_name, None)
        if value not in {None, "", 0}:
            return True

    props = _primitive_properties(region)
    for key, value in props.items():
        key_upper = str(key).upper()
        value_text = str(value or "").strip().lower()
        if key_upper.startswith("MODEL") or key_upper in {"BODYID", "BODYGUID"}:
            return True
        if any(token in value_text for token in (".step", ".stp", ".igs", ".iges")):
            return True
    return False


def _primitive_properties(primitive: object) -> dict[object, object]:
    props = getattr(primitive, "properties", None)
    return props if isinstance(props, dict) else {}


def _primitive_text_content(primitive: object) -> str:
    for attr_name in ("text_content", "text", "string"):
        value = getattr(primitive, attr_name, None)
        if value is not None:
            return str(value or "").strip()
    return ""


def _normalize_layer_policy_token(value: object) -> str:
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")


def _is_mechanical_layer(value: object) -> bool:
    layer_id = _coerce_layer_id(value)
    return 57 <= layer_id <= 72 if layer_id is not None else False


def _coerce_layer_id(value: object) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return int(value)

    text = str(value or "").strip()
    if not text:
        return None
    try:
        return int(text)
    except ValueError:
        pass
    try:
        from altium_monkey.altium_record_types import PcbLayer

        return int(PcbLayer.from_json_name(text).value)
    except Exception:
        return None


def _layer_report_key(value: object) -> str:
    layer_id = _coerce_layer_id(value)
    if layer_id is None:
        return "unknown"
    try:
        from altium_monkey.altium_record_types import PcbLayer

        return PcbLayer(layer_id).to_json_name()
    except Exception:
        return str(layer_id)


def _find_hw_config_dir(
    *,
    start_dir: str | Path | None = None,
    env: dict[str, str] | None = None,
) -> Path | None:
    env_map = os.environ if env is None else env
    workspace = str(env_map.get("ALX_HW_WORKSPACE", "")).strip()
    if workspace:
        return (Path(workspace).expanduser() / "config").resolve()

    base = Path(start_dir or Path.cwd()).expanduser().resolve()
    if base.is_file():
        base = base.parent
    for root in (base, *base.parents):
        if root.name == "config" and (root / "workspace.json").exists():
            return root.resolve()
        candidate = root / "config"
        if (candidate / "workspace.json").exists():
            return candidate.resolve()
    return None
