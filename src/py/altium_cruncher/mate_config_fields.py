"""Mate configuration field readers and source-path resolution.

TypeSpec validates authored structure; these readers apply existing domain
fallbacks and preserve field-specific error messages used by Mate planning.
"""
from __future__ import annotations
from collections.abc import Mapping
from pathlib import Path

type JsonObject = dict[str, object]


def _optional_section(
    root: Mapping[str, object],
    name: str,
) -> JsonObject | None:
    value = root.get(name)
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError(f"Mate config field {name!r} must be an object")
    return dict(value)


def _section(root: Mapping[str, object], name: str) -> JsonObject:
    value = root.get(name, {})
    if not isinstance(value, dict):
        raise ValueError(f"Mate config field {name!r} must be an object")
    return dict(value)


def _json_object(value: object, label: str) -> JsonObject:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return dict(value)


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


def _number_like(args: Mapping[str, object], name: str) -> float:
    value = args.get(name, 0.0)
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise ValueError(f"Field {name!r} must be numeric")
    return float(value)


def _target_float(args: Mapping[str, object], name: str) -> float:
    value = args.get(name)
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise ValueError(f"Field {name!r} must be numeric")
    return float(value)


def _target_optional_string(args: Mapping[str, object], name: str) -> str | None:
    value = args.get(name)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"Field {name!r} must be a string")
    return value or None


def _style_string(args: Mapping[str, object], name: str, default: str) -> str:
    value = args.get(name)
    if value is None:
        return default
    if not isinstance(value, str):
        raise ValueError(f"Field pcb_labels.style.{name} must be a string")
    return value


def _style_string_or_int(
    args: Mapping[str, object],
    name: str,
    default: str | int,
) -> str | int:
    value = args.get(name)
    if value is None:
        return default
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value
    raise ValueError(f"Field pcb_labels.style.{name} must be a string or integer")


def _style_bool(args: Mapping[str, object], name: str, default: bool) -> bool:
    value = args.get(name)
    if value is None:
        return default
    if not isinstance(value, bool):
        raise ValueError(f"Field pcb_labels.style.{name} must be a boolean")
    return value


def _style_float(args: Mapping[str, object], name: str, default: float) -> float:
    value = args.get(name)
    if value is None:
        return default
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise ValueError(f"Field pcb_labels.style.{name} must be numeric")
    return float(value)


def _part_string(part: Mapping[str, object], field: str) -> str:
    value = part.get(field)
    if not isinstance(value, str) or not value:
        raise ValueError(
            f"Known-part manifest field {field!r} must be a non-empty string"
        )
    return value


def _part_optional_string(part: Mapping[str, object], field: str) -> str | None:
    value = part.get(field)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"Known-part manifest field {field!r} must be a string")
    return value or None


def _safe_id(value: str) -> str:
    result = "".join(char.lower() if char.isalnum() else "_" for char in value)
    return result.strip("_") or "part"


def _resolve_config_path(value: str, base_dir: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (base_dir / path).resolve()


def _optional_bool(args: Mapping[str, object], name: str, default: bool) -> bool:
    value = args.get(name)
    if value is None:
        return default
    if not isinstance(value, bool):
        raise ValueError(f"Field {name!r} must be a boolean")
    return value


def _optional_float(
    args: Mapping[str, object],
    name: str,
    default: float,
) -> float:
    value = args.get(name)
    if value is None:
        return default
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise ValueError(f"Field {name!r} must be numeric")
    return float(value)


def _optional_float_or_none(
    args: Mapping[str, object],
    name: str,
) -> float | None:
    value = args.get(name)
    if value is None:
        return None
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise ValueError(f"Field {name!r} must be numeric")
    return float(value)


def _required_point(
    args: Mapping[str, object],
    name: str,
    *,
    default: tuple[float, float],
) -> tuple[float, float]:
    value = args.get(name)
    if value is None:
        return default
    if not isinstance(value, list | tuple) or len(value) != 2:
        raise ValueError(f"Field {name!r} must be a two-number array")
    return (_point_number(value[0], name), _point_number(value[1], name))


def _optional_point(
    args: Mapping[str, object],
    name: str,
) -> tuple[float, float] | None:
    value = args.get(name)
    if value is None:
        return None
    if not isinstance(value, list | tuple) or len(value) != 2:
        raise ValueError(f"Field {name!r} must be a two-number array")
    return (_point_number(value[0], name), _point_number(value[1], name))


def _point_number(value: object, name: str) -> float:
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise ValueError(f"Field {name!r} point values must be numeric")
    return float(value)


def _optional_number_object(
    args: Mapping[str, object],
    name: str,
    fields: tuple[str, ...],
) -> JsonObject | None:
    value = args.get(name)
    if value is None:
        return None
    raw = _json_object(value, name)
    return {field: _number_field(raw, name, field) for field in fields}


def _number_field(args: Mapping[str, object], name: str, field: str) -> float:
    value = args.get(field)
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise ValueError(f"Field {name}.{field} must be numeric")
    return float(value)
