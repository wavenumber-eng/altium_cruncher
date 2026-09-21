"""Ready-to-render PCB illustration presets using the existing SVG schema."""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from typing import Literal, cast

from .altium_cruncher_pcb_svg_config import (
    PcbSvgConfig,
    PcbSvgViewConfig,
    resolve_pcb_svg_config,
)
from .contracts.pcb_svg import config_metadata
from .contracts.generated.pcb_svg_config import PcbSvgConfigInput

type IllustrationSide = Literal["top", "bottom"]
type IllustrationTheme = Literal[
    "saved", "white", "black", "blue", "red", "purple", "yellow", "green"
]

ILLUSTRATION_THEMES = cast(
    tuple[IllustrationTheme, ...], tuple(config_metadata()["toon-themes"])
)


def illustration_preset() -> PcbSvgConfigInput:
    """Copy the TypeSpec-authored top/bottom illustration preset."""
    return deepcopy(cast(PcbSvgConfigInput, config_metadata()["toon-preset"]))


_SILK_STYLES = (
    "silkscreen_component_graphics",
    "silkscreen_designators",
    "silkscreen_board_graphics",
)


def _overlay(
    base: Mapping[str, object], override: Mapping[str, object]
) -> dict[str, object]:
    result = deepcopy(dict(base))
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _overlay(cast(dict[str, object], result[key]), value)
        else:
            result[key] = deepcopy(value)
    return result


def illustration_view_side(view: PcbSvgViewConfig) -> IllustrationSide:
    sides = [
        side
        for side in ("top", "bottom")
        if f"ILLUSTRATION_{side.upper()}" in view.layers
    ]
    if len(sides) != 1:
        raise ValueError(
            f"Illustration view '{view.name}' must contain exactly one of "
            "ILLUSTRATION_TOP or ILLUSTRATION_BOTTOM; use pcb-svg for other compositions"
        )
    return cast(IllustrationSide, sides[0])


def resolve_illustration_config(
    override: PcbSvgConfigInput | None = None,
    *,
    side: Literal["top", "bottom", "both"] = "both",
    theme: IllustrationTheme | None = None,
    assembly: bool = False,
    pcbdoc: str | None = None,
) -> PcbSvgConfig:
    """Apply config overrides, then explicit command choices to the preset."""
    config = resolve_pcb_svg_config(_overlay(illustration_preset(), override or {}))
    if config.layer_outputs.get("enabled"):
        raise ValueError("toon renders composed views; use pcb-svg for layer_outputs")
    if pcbdoc:
        config.global_options.pcbdoc = pcbdoc
    for view in config.enabled_views():
        view_side = illustration_view_side(view)
        view.enabled = side == "both" or side == view_side
        if not view.enabled:
            continue
        if theme is not None:
            _apply_theme(view, theme)
        if assembly:
            _apply_assembly(
                view,
                view_side,
                hide_silkscreen_designators=(
                    config.assembly.hide_silkscreen_designators
                ),
            )
    if not config.enabled_views():
        raise ValueError(f"No enabled illustration views for --side {side}")
    return config


def _apply_theme(view: PcbSvgViewConfig, theme: IllustrationTheme) -> None:
    colors = cast(dict[str, dict[str, str]], config_metadata()["toon-themes"])[theme]
    view.styles.setdefault("soldermask_film", {})["color"] = colors["mask"]
    for name in _SILK_STYLES:
        view.styles.setdefault(name, {})["color"] = colors["silk"]


def _apply_assembly(
    view: PcbSvgViewConfig,
    side: IllustrationSide,
    *,
    hide_silkscreen_designators: bool,
) -> None:
    token = f"ASSEMBLY_DESIGNATORS_{side.upper()}"
    if token not in view.layers:
        view.layers.append(token)
    if hide_silkscreen_designators:
        view.styles.setdefault("silkscreen_designators", {})["enabled"] = False
