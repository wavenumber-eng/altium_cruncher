"""Small value and primitive helpers shared by the PCB SVG compositor."""

from __future__ import annotations

import html

from altium_monkey.altium_record_types import PcbLayer

from .altium_cruncher_pcb_svg_component_layers import COMPONENT_LAYER_IDS


_HLR_TOKENS = {"ASSEMBLY_HLR_TOP", "ASSEMBLY_HLR_BOTTOM"}
_HOLE_TOKENS = {"DRILLS", "SLOTS"}


def style_enabled(styles: dict[str, dict[str, object]], name: str) -> bool:
    return bool(styles.get(name, {}).get("enabled", True))


def style_color(styles: dict[str, dict[str, object]], name: str, default: str) -> str:
    return str(styles.get(name, {}).get("color") or default)


def style_float(
    styles: dict[str, dict[str, object]],
    name: str,
    key: str,
    default: float,
) -> float:
    value = styles.get(name, {}).get(key, default)
    if not isinstance(value, (int, float, str)):
        raise ValueError(f"Invalid pcb-svg style value {name}.{key}")
    try:
        return float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"Invalid pcb-svg style value {name}.{key}") from error


def style_int(
    styles: dict[str, dict[str, object]], name: str, key: str, default: int
) -> int:
    value = styles.get(name, {}).get(key, default)
    if not isinstance(value, (int, float, str)):
        raise ValueError(f"Invalid pcb-svg style value {name}.{key}")
    try:
        return int(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"Invalid pcb-svg style value {name}.{key}") from error


def style_bool(
    styles: dict[str, dict[str, object]],
    name: str,
    key: str,
    default: bool,
) -> bool:
    value = styles.get(name, {}).get(key, default)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.lower().strip()
        if normalized in {"1", "true", "yes", "on"}:
            return True
        if normalized in {"0", "false", "no", "off"}:
            return False
    return bool(value)


def style_plating_color(
    styles: dict[str, dict[str, object]], name: str, *, plated: bool
) -> str:
    style = styles.get(name, {})
    key = "plated_color" if plated else "non_plated_color"
    return str(style.get(key) or ("#90EE90" if plated else "#ADD8E6"))


def is_component_linked(primitive: object) -> bool:
    try:
        component_index = int(getattr(primitive, "component_index", -1))
    except TypeError, ValueError:
        return False
    return component_index >= 0 and component_index not in {0xFFFF, 65535}


def pad_has_hole(pad: object) -> bool:
    try:
        return int(getattr(pad, "hole_size", 0) or 0) > 0
    except TypeError, ValueError:
        return False


def pad_is_slot(pad: object) -> bool:
    try:
        hole_shape = int(getattr(pad, "hole_shape", 0) or 0)
        hole_size = int(getattr(pad, "hole_size", 0) or 0)
        slot_size = int(getattr(pad, "slot_size", 0) or 0)
    except TypeError, ValueError:
        return False
    return hole_shape == 2 and hole_size > 0 and slot_size > hole_size


def object_float(value: object, default: float = 0.0) -> float:
    if isinstance(value, (int, float, str)):
        try:
            return float(value)
        except TypeError, ValueError:
            return default
    return default


def pad_center_mils(pad: object) -> tuple[float, float]:
    center = getattr(pad, "pad_center_mils", None)
    if callable(center):
        try:
            result = center()
            if isinstance(result, (list, tuple)) and len(result) >= 2:
                return (object_float(result[0]), object_float(result[1]))
        except TypeError, ValueError:
            pass
    return (
        object_float(getattr(pad, "x_mils", 0.0)),
        object_float(getattr(pad, "y_mils", 0.0)),
    )


def pad_size_mils(pad: object, layer: PcbLayer) -> tuple[float, float]:
    layer_size = getattr(pad, "_layer_size", None)
    if callable(layer_size):
        try:
            result = layer_size(layer)
            if isinstance(result, (list, tuple)) and len(result) >= 2:
                return (
                    object_float(result[0]) / 10000.0,
                    object_float(result[1]) / 10000.0,
                )
        except TypeError, ValueError:
            pass
    return (
        object_float(getattr(pad, "width_mils", 0.0)),
        object_float(getattr(pad, "height", 0.0)) / 10000.0,
    )


def pad_renders_on_layer(pad: object, layer: PcbLayer) -> bool:
    should_render = getattr(pad, "_should_render_on_layer", None)
    if callable(should_render):
        try:
            return bool(should_render(layer))
        except TypeError, ValueError:
            return False
    return True


def component_side(component: object) -> str:
    normalized = getattr(component, "get_layer_normalized", None)
    if callable(normalized):
        try:
            side = str(normalized()).strip().lower()
            if side:
                return side
        except TypeError, ValueError:
            pass
    raw_layer = str(getattr(component, "layer", "") or "").strip().lower()
    if "bottom" in raw_layer:
        return "bottom"
    if "top" in raw_layer:
        return "top"
    return raw_layer


def component_designator(component: object) -> str:
    return str(getattr(component, "designator", "") or "").strip()


def reference_designator_prefix(designator: str) -> str:
    text = str(designator or "").strip().upper()
    index = 0
    while index < len(text) and text[index].isalpha():
        index += 1
    return text[:index] if index > 0 else text


def normalize_draw_order(tokens: list[str]) -> list[str]:
    body: list[str] = []
    holes: list[str] = []
    hlr: list[str] = []
    components: list[str] = []
    for token in tokens:
        if token in COMPONENT_LAYER_IDS:
            if token not in components:
                components.append(token)
        elif token in _HLR_TOKENS:
            if token not in hlr:
                hlr.append(token)
        elif token in _HOLE_TOKENS:
            if token not in holes:
                holes.append(token)
        elif token not in body:
            body.append(token)
    return body + holes + hlr + components


def svg_symbol_mode(projection_mode: str) -> str:
    return "simple" if projection_mode in {"outline", "simple"} else projection_mode


def safe_svg_id(value: str) -> str:
    return "".join(
        char if char.isalnum() or char in "._-" else "-" for char in value
    ).strip("-")


def synthetic_layer_metadata_attrs(
    layer_id: int,
    *,
    key: str,
    display_name: str,
    role: str = "annotation",
) -> list[str]:
    return [
        f'data-layer-id="{int(layer_id)}"',
        f'data-layer-key="{html.escape(key)}"',
        f'data-layer-name="{html.escape(key)}"',
        f'data-layer-display-name="{html.escape(display_name)}"',
        f'data-layer-role="{html.escape(role)}"',
    ]


__all__ = [
    "component_designator",
    "component_side",
    "is_component_linked",
    "normalize_draw_order",
    "object_float",
    "pad_center_mils",
    "pad_has_hole",
    "pad_is_slot",
    "pad_renders_on_layer",
    "pad_size_mils",
    "reference_designator_prefix",
    "safe_svg_id",
    "style_bool",
    "style_color",
    "style_enabled",
    "style_float",
    "style_int",
    "style_plating_color",
    "svg_symbol_mode",
    "synthetic_layer_metadata_attrs",
]
