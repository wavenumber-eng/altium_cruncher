from types import SimpleNamespace
from typing import cast

import pytest

from altium_cruncher.altium_cruncher_cmd_pcb_svg import (
    PCB_SVG_CONFIG_FILENAME,
    PCB_SVG_CONFIG_SCHEMA,
    PcbSvgConfig,
    _apply_pcb_layer_selection,
    _apply_pcb_view_selection,
    _resolve_view_render_settings,
    resolve_pcb_svg_configs,
)
from altium_cruncher.altium_cruncher_pcb_svg_a0_renderer import write_or_update_view_svg


def _enabled_views(config: PcbSvgConfig) -> set[str]:
    return {view.name for view in config.views if view.enabled}


def test_pcb_svg_default_config_uses_a0_schema_and_explicit_views() -> None:
    config = PcbSvgConfig.default()
    payload = config.to_dict()
    layer_outputs = cast(dict[str, object], payload["layer_outputs"])
    views = cast(list[dict[str, object]], payload["views"])

    assert payload["schema"] == PCB_SVG_CONFIG_SCHEMA
    assert PCB_SVG_CONFIG_FILENAME == "pcb.svg.config.a0"
    assert layer_outputs["enabled"] is True
    assert "BOARD_CUTOUTS" in cast(list[str], layer_outputs["include_special_layers"])
    top_view = next(view for view in views if view["name"] == "top_view")
    top_layers = cast(list[str], top_view["layers"])
    assert top_view["group_id"] == "pcb-svg-view-top"
    assert top_layers[-1] == "ASSEMBLY_HLR_TOP"


def test_pcb_svg_default_cutout_style_has_no_text_label() -> None:
    root = PcbSvgConfig.default().to_dict()
    global_options = cast(dict[str, object], root["global"])
    styles = cast(dict[str, dict[str, object]], global_options["styles"])
    payload = styles["board_cutouts"]

    assert payload["hatch"] is True
    assert "label_text" not in payload
    assert "label" not in payload


def test_pcb_svg_cli_views_enable_requested_views_and_layer_outputs() -> None:
    config = PcbSvgConfig.default()

    _apply_pcb_view_selection(config, "top,bottom,layers")

    assert _enabled_views(config) == {"top_view", "bottom_view"}
    assert config.layer_outputs["enabled"] is True


def test_pcb_svg_cli_views_none_disables_all_outputs() -> None:
    config = PcbSvgConfig.default()

    _apply_pcb_view_selection(config, "none")

    assert _enabled_views(config) == set()
    assert config.layer_outputs["enabled"] is False


def test_pcb_svg_cli_views_reject_unknown_view() -> None:
    config = PcbSvgConfig.default()

    with pytest.raises(ValueError, match="Unknown --views token"):
        _apply_pcb_view_selection(config, "top,mechanical")


def test_pcb_svg_cli_layers_filter_layer_outputs() -> None:
    config = PcbSvgConfig.default()

    _apply_pcb_layer_selection(config, "bottom")

    assert config.layer_outputs["layers"] == ["BOTTOM"]


def test_pcb_svg_cli_overrides_created_default_config(tmp_path) -> None:
    config_path = tmp_path / PCB_SVG_CONFIG_FILENAME
    input_file = tmp_path / "board.PrjPcb"
    input_file.write_text("", encoding="utf-8")
    args = SimpleNamespace(
        config=config_path,
        pcb_views="top,layers",
        pcb_layers="bottom",
        pcbdoc=None,
        pcb_svg_scale=None,
        pcb_svg_size_unit=None,
        pcb_clean_output=False,
    )

    config_by_input, created_configs = resolve_pcb_svg_configs(args, [input_file])

    resolved = config_by_input[input_file.resolve()]
    assert created_configs == [config_path.resolve()]
    assert _enabled_views(resolved) == {"top_view"}
    assert resolved.layer_outputs["enabled"] is True
    assert resolved.layer_outputs["layers"] == ["BOTTOM"]


def test_pcb_svg_rejects_v1_config() -> None:
    with pytest.raises(ValueError, match="Unsupported pcb-svg config schema"):
        PcbSvgConfig.from_dict({"schema": "wn.pcb.svg.config.v1"})


def test_pcb_svg_view_style_override_merges_with_global() -> None:
    config = PcbSvgConfig.from_dict(
        {
            "schema": PCB_SVG_CONFIG_SCHEMA,
            "global": {
                "styles": {
                    "drills": {
                        "enabled": True,
                        "plated_color": "#111111",
                        "non_plated_color": "#222222",
                    }
                }
            },
            "views": [
                {
                    "name": "top_view",
                    "layers": ["TOP", "DRILLS", "SLOTS"],
                    "styles": {
                        "drills": {"plated_color": "#333333"},
                        "slots": {"plated_color": "#444444"},
                    },
                }
            ],
        }
    )

    resolved = _resolve_view_render_settings(config.global_options, config.views[0])

    styles = cast(dict[str, dict[str, object]], resolved["styles"])
    assert styles["drills"]["plated_color"] == "#333333"
    assert styles["drills"]["non_plated_color"] == "#222222"
    assert styles["slots"]["plated_color"] == "#444444"


def test_pcb_svg_config_validates_cutout_style_options() -> None:
    config = PcbSvgConfig.from_dict(
        {
            "schema": PCB_SVG_CONFIG_SCHEMA,
            "global": {"styles": {"board_cutouts": {"outline_style": "dotted"}}},
            "views": [{"name": "top_view", "layers": ["BOARD_CUTOUTS"]}],
        }
    )

    with pytest.raises(ValueError, match="board_cutouts.outline_style"):
        _resolve_view_render_settings(config.global_options, config.views[0])


def test_pcb_svg_config_validates_cutout_positive_dimensions() -> None:
    config = PcbSvgConfig.from_dict(
        {
            "schema": PCB_SVG_CONFIG_SCHEMA,
            "global": {"styles": {"board_cutouts": {"hatch_spacing_mm": 0.0}}},
            "views": [{"name": "top_view", "layers": ["BOARD_CUTOUTS"]}],
        }
    )

    with pytest.raises(ValueError, match="board_cutouts.hatch_spacing_mm"):
        _resolve_view_render_settings(config.global_options, config.views[0])


def test_pcb_svg_durable_group_update_preserves_user_svg_content(tmp_path) -> None:
    target = tmp_path / "view.svg"
    target.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg"><text id="user-note">keep</text>'
        '<g id="pcb-svg-view-top"><path id="old"/></g></svg>',
        encoding="utf-8",
    )
    replacement = (
        '<svg xmlns="http://www.w3.org/2000/svg"><g id="scene">'
        '<g id="pcb-svg-view-top"><path id="new"/></g></g></svg>'
    )

    write_or_update_view_svg(target, replacement, group_id="pcb-svg-view-top")
    text = target.read_text(encoding="utf-8")

    assert "user-note" in text
    assert 'id="new"' in text
    assert 'id="old"' not in text


def test_pcb_svg_missing_durable_group_rewrites_stale_svg(tmp_path) -> None:
    target = tmp_path / "view.svg"
    target.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg"><text>cutout</text>'
        '<g id="legacy-generated-view"><path id="old"/></g></svg>',
        encoding="utf-8",
    )
    replacement = (
        '<svg xmlns="http://www.w3.org/2000/svg"><g id="scene">'
        '<g id="pcb-svg-view-top"><path id="new"/></g></g></svg>'
    )

    write_or_update_view_svg(target, replacement, group_id="pcb-svg-view-top")
    text = target.read_text(encoding="utf-8")

    assert "cutout" not in text
    assert "legacy-generated-view" not in text
    assert 'id="pcb-svg-view-top"' in text
    assert 'id="new"' in text


def test_pcb_svg_group_update_removes_legacy_generated_cutout_labels(tmp_path) -> None:
    target = tmp_path / "view.svg"
    target.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg">'
        '<text id="user-note">keep</text><g id="scene">'
        '<g id="board-cutouts-layer" data-layer-key="BOARD_CUTOUTS">'
        '<text data-feature="board-cutout-label">cutout</text></g>'
        '<g id="pcb-svg-view-top"><path id="old"/></g></g></svg>',
        encoding="utf-8",
    )
    replacement = (
        '<svg xmlns="http://www.w3.org/2000/svg"><g id="scene">'
        '<g id="pcb-svg-view-top"><path id="new"/></g></g></svg>'
    )

    write_or_update_view_svg(target, replacement, group_id="pcb-svg-view-top")
    text = target.read_text(encoding="utf-8")

    assert "user-note" in text
    assert "board-cutout-label" not in text
    assert ">cutout</text>" not in text
    assert 'id="new"' in text
    assert 'id="old"' not in text
