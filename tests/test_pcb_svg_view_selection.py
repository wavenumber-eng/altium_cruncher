from types import SimpleNamespace

import pytest

from altium_cruncher.altium_cruncher_cmd_pcb_svg import (
    PcbSvgConfig,
    _apply_pcb_layer_selection,
    _apply_pcb_view_selection,
    _resolve_view_render_settings,
    resolve_pcb_svg_configs,
)


def _enabled_sources(config: PcbSvgConfig) -> set[str]:
    return {view.source for view in config.views if view.enabled}


def test_pcb_svg_cli_views_enable_requested_content_views():
    config = PcbSvgConfig.default()

    _apply_pcb_view_selection(config, "assembly-top,assembly-bottom")

    assert _enabled_sources(config) == {"assembly-top", "assembly-bottom"}


def test_pcb_svg_default_assembly_views_are_copper_only():
    config = PcbSvgConfig.default()

    assembly_views = [view for view in config.views if view.source.startswith("assembly")]

    assert assembly_views
    assert {tuple(view.layer_order or []) for view in assembly_views} == {("copper",)}


def test_pcb_svg_default_config_includes_board_cutout_layer_options():
    config = PcbSvgConfig.default()
    payload = config.to_dict()["global"]

    assert payload["include_board_cutout_layer"] is True
    assert payload["board_cutout_layer_hatch"] is True
    assert "board_cutout_layer_hash_spacing_mm" in payload
    assert "board_cutout_layer_hash_angle_deg" in payload
    assert "board_cutout_layer_hash_line_width_mm" in payload
    assert "board_cutout_layer_outline_style" in payload
    assert "board_cutout_layer_outline_dash_mm" in payload
    assert "board_cutout_layer_outline_width_mm" in payload


def test_pcb_svg_cli_views_all_enables_all_content_views():
    config = PcbSvgConfig.default()

    _apply_pcb_view_selection(config, "all")

    assert _enabled_sources(config) == {
        "layers",
        "top",
        "bottom",
        "assembly-top",
        "assembly-bottom",
    }


def test_pcb_svg_cli_views_override_created_default_config(tmp_path):
    config_path = tmp_path / "pcb-svg.json"
    input_file = tmp_path / "board.PrjPcb"
    input_file.write_text("", encoding="utf-8")
    args = SimpleNamespace(config=config_path, pcb_views="assembly-top,assembly-bottom")

    config_by_input, created_configs = resolve_pcb_svg_configs(args, [input_file])

    assert created_configs == [config_path.resolve()]
    assert _enabled_sources(config_by_input[input_file.resolve()]) == {
        "assembly-top",
        "assembly-bottom",
    }


def test_pcb_svg_cli_views_reject_unknown_view():
    config = PcbSvgConfig.default()

    with pytest.raises(ValueError, match="Unknown --pcb-views token"):
        _apply_pcb_view_selection(config, "top,mechanical")


def test_pcb_svg_cli_layers_filter_layer_view():
    config = PcbSvgConfig.default()

    _apply_pcb_layer_selection(config, "bottom")

    layer_view = next(view for view in config.views if view.source == "layers")
    assert layer_view.layers == ["BOTTOM"]


def test_pcb_svg_cli_layers_override_created_default_config(tmp_path):
    config_path = tmp_path / "pcb-svg.json"
    input_file = tmp_path / "board.PrjPcb"
    input_file.write_text("", encoding="utf-8")
    args = SimpleNamespace(config=config_path, pcb_views="layers", pcb_layers="bottom")

    config_by_input, created_configs = resolve_pcb_svg_configs(args, [input_file])

    assert created_configs == [config_path.resolve()]
    layer_view = next(
        view
        for view in config_by_input[input_file.resolve()].views
        if view.source == "layers"
    )
    assert layer_view.enabled is True
    assert layer_view.layers == ["BOTTOM"]


def test_pcb_svg_config_parses_board_cutout_layer_options():
    config = PcbSvgConfig.from_dict(
        {
            "schema": "wn.pcb.svg.config.v1",
            "global": {
                "include_board_cutout_layer": True,
                "board_cutout_layer_hatch": True,
                "board_cutout_layer_hash_spacing_mm": 1.25,
                "board_cutout_layer_hash_angle_deg": 30,
                "board_cutout_layer_hash_line_width_mm": 0.12,
                "board_cutout_layer_outline_style": "dashed",
                "board_cutout_layer_outline_dash_mm": 0.9,
                "board_cutout_layer_outline_width_mm": 0.33,
                "board_cutout_layer_label": True,
                "board_cutout_layer_label_text": "slot",
            },
            "views": [{"name": "layers", "source": "layers", "enabled": True}],
        }
    )

    assert config.global_options.include_board_cutout_layer is True
    assert config.global_options.board_cutout_layer_hatch is True
    assert config.global_options.board_cutout_layer_hash_spacing_mm == 1.25
    assert config.global_options.board_cutout_layer_hash_angle_deg == 30
    assert config.global_options.board_cutout_layer_hash_line_width_mm == 0.12
    assert config.global_options.board_cutout_layer_outline_style == "dashed"
    assert config.global_options.board_cutout_layer_outline_dash_mm == 0.9
    assert config.global_options.board_cutout_layer_outline_width_mm == 0.33
    assert config.global_options.board_cutout_layer_label is True
    assert config.global_options.board_cutout_layer_label_text == "slot"


def test_pcb_svg_config_validates_board_cutout_layer_options():
    config = PcbSvgConfig.from_dict(
        {
            "schema": "wn.pcb.svg.config.v1",
            "global": {"board_cutout_layer_outline_style": "dotted"},
            "views": [{"name": "layers", "source": "layers", "enabled": True}],
        }
    )

    with pytest.raises(ValueError, match="board_cutout_layer_outline_style"):
        _resolve_view_render_settings(config.global_options, config.views[0])


def test_pcb_svg_config_validates_board_cutout_hash_spacing():
    config = PcbSvgConfig.from_dict(
        {
            "schema": "wn.pcb.svg.config.v1",
            "global": {"board_cutout_layer_hash_spacing_mm": 0.0},
            "views": [{"name": "layers", "source": "layers", "enabled": True}],
        }
    )

    with pytest.raises(ValueError, match="board_cutout_layer_hash_spacing_mm"):
        _resolve_view_render_settings(config.global_options, config.views[0])


def test_pcb_svg_config_validates_board_cutout_line_widths():
    config = PcbSvgConfig.from_dict(
        {
            "schema": "wn.pcb.svg.config.v1",
            "global": {
                "board_cutout_layer_hash_line_width_mm": 0.0,
                "board_cutout_layer_outline_width_mm": 0.0,
            },
            "views": [{"name": "layers", "source": "layers", "enabled": True}],
        }
    )

    with pytest.raises(ValueError, match="board_cutout_layer_hash_line_width_mm"):
        _resolve_view_render_settings(config.global_options, config.views[0])
