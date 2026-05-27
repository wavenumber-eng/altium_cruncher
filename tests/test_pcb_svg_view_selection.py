from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

import pytest

import altium_cruncher.altium_cruncher_pcb_svg_a0_renderer as pcb_svg_a0_renderer
from altium_cruncher.altium_cruncher_cmd_pcb_svg import (
    PCB_SVG_CONFIG_FILENAME,
    PCB_SVG_CONFIG_SCHEMA,
    PcbSvgConfig,
    PcbSvgViewConfig,
    _apply_pcb_layer_selection,
    _apply_pcb_view_selection,
    _default_pcb_svg_config_text,
    _load_pcb_svg_config,
    _resolve_view_render_settings,
    resolve_pcb_svg_configs,
)
from altium_cruncher.altium_cruncher_pcb_svg_a0_renderer import (
    PcbSvgA0Renderer,
    write_or_update_view_svg,
)
from altium_cruncher.altium_cruncher_pcb_svg_inventory import (
    PcbSvgComponentInventory,
    build_pcb_svg_component_inventory_from_pcbdoc,
    load_pcb_svg_component_inventory,
)
from altium_cruncher.altium_cruncher_pcb_svg_pin1 import choose_pin1_pad_designator
from altium_monkey.altium_pcb_enums import PadShape
from altium_monkey.altium_pcbdoc import AltiumPcbDoc
from altium_monkey.altium_record_types import PcbLayer


ROOT = Path(__file__).resolve().parents[1]
CRICKET_PCBDOC = (
    ROOT
    / "tests"
    / "assets"
    / "projects"
    / "cricket-node"
    / "input"
    / "cricket-node-hw__B.PcbDoc"
)


def _enabled_views(config: PcbSvgConfig) -> set[str]:
    return {view.name for view in config.views if view.enabled}


def test_pcb_svg_default_config_uses_a0_schema_and_explicit_views() -> None:
    config = PcbSvgConfig.default()
    payload = config.to_dict()
    global_options = cast(dict[str, object], payload["global"])
    layer_outputs = cast(dict[str, object], payload["layer_outputs"])
    views = cast(list[dict[str, object]], payload["views"])

    assert payload["schema"] == PCB_SVG_CONFIG_SCHEMA
    assert PCB_SVG_CONFIG_FILENAME == "pcb.svg.config"
    assert "pcbdoc" not in global_options
    assert "assembly" not in payload
    assert "dnp" not in payload
    assert "diodes" not in payload
    assert "components" not in payload
    assert layer_outputs["enabled"] is True
    assert "BOARD_CUTOUTS" in cast(list[str], layer_outputs["include_special_layers"])
    top_view = next(view for view in views if view["name"] == "top_view")
    top_layers = cast(list[str], top_view["layers"])
    assert top_view["group_id"] == "pcb-svg-view-top"
    assert top_layers[-1] == "ASSEMBLY_HLR_TOP"
    top_pin1_view = next(view for view in views if view["name"] == "top_pin1_view")
    bottom_pin1_view = next(view for view in views if view["name"] == "bottom_pin1_view")
    top_hlr_bounds = next(
        view for view in views if view["name"] == "top_hlr_bounding_boxes"
    )
    bottom_hlr_bounds = next(
        view for view in views if view["name"] == "bottom_hlr_bounding_boxes"
    )
    assert top_pin1_view["layers"] == [
        "BOARD_OUTLINE",
        "TOP",
        "DRILLS",
        "SLOTS",
        "PIN1_TOP",
        "ASSEMBLY_HLR_TOP",
    ]
    assert bottom_pin1_view["layers"] == [
        "BOARD_OUTLINE",
        "BOTTOM",
        "DRILLS",
        "SLOTS",
        "PIN1_BOTTOM",
        "ASSEMBLY_HLR_BOTTOM",
    ]
    assert top_pin1_view["assembly_hlr_mode"] == "simple"
    assert bottom_pin1_view["assembly_hlr_mode"] == "simple"
    top_pin1_styles = cast(dict[str, dict[str, object]], top_pin1_view["styles"])
    bottom_pin1_styles = cast(dict[str, dict[str, object]], bottom_pin1_view["styles"])
    assert top_pin1_styles["assembly_hlr"]["include_visible"] is False
    assert top_pin1_styles["assembly_hlr"]["include_outline"] is True
    assert bottom_pin1_styles["assembly_hlr"]["include_visible"] is False
    assert bottom_pin1_styles["assembly_hlr"]["include_outline"] is True
    assert top_hlr_bounds["assembly_hlr_mode"] == "bounding_box"
    assert bottom_hlr_bounds["assembly_hlr_mode"] == "bounding_box"


def test_pcb_svg_default_cutout_style_has_no_text_label() -> None:
    root = PcbSvgConfig.default().to_dict()
    global_options = cast(dict[str, object], root["global"])
    styles = cast(dict[str, dict[str, object]], global_options["styles"])
    payload = styles["board_cutouts"]

    assert payload["hatch"] is True
    assert "label_text" not in payload
    assert "label" not in payload


def test_pcb_svg_default_canvas_uses_board_outline_bounds() -> None:
    root = PcbSvgConfig.default().to_dict()
    global_options = cast(dict[str, object], root["global"])
    canvas = cast(dict[str, object], global_options["canvas"])

    assert canvas == {"bounds": "board_outline", "margin_mm": 1.0}


def test_pcb_svg_board_outline_canvas_ignores_off_board_geometry() -> None:
    config = PcbSvgConfig.default()
    renderer = PcbSvgA0Renderer(config)
    outline = SimpleNamespace(
        vertices=[object()],
        bounding_box=(1000.0, 2000.0, 2000.0, 3000.0),
    )
    pcbdoc = SimpleNamespace(board=SimpleNamespace(outline=outline))

    bounds = renderer._compute_bounds_mils(cast(AltiumPcbDoc, pcbdoc))  # noqa: SLF001

    margin_mils = 1.0 / 0.0254
    assert bounds == pytest.approx(
        (
            1000.0 - margin_mils,
            2000.0 - margin_mils,
            2000.0 + margin_mils,
            3000.0 + margin_mils,
        )
    )


def test_pcb_svg_cli_views_enable_requested_views_and_layer_outputs() -> None:
    config = PcbSvgConfig.default()

    _apply_pcb_view_selection(config, "top,bottom,layers")

    assert _enabled_views(config) == {"top_view", "bottom_view"}
    assert config.layer_outputs["enabled"] is True


def test_pcb_svg_cli_views_enable_pin1_and_hlr_bounds_aliases() -> None:
    config = PcbSvgConfig.default()

    _apply_pcb_view_selection(
        config,
        "pin1-top,pin1-bottom,top-hlr-bounds,bottom-hlr-bounds",
    )

    assert _enabled_views(config) == {
        "top_pin1_view",
        "bottom_pin1_view",
        "top_hlr_bounding_boxes",
        "bottom_hlr_bounding_boxes",
    }
    assert config.layer_outputs["enabled"] is False


def test_pcb_svg_pin1_selector_supports_bga_lga_and_manual_override() -> None:
    pads = ["74", "A8", "A10", "B1", "C1", "AA24"]

    assert choose_pin1_pad_designator(pads) == "B1"
    assert choose_pin1_pad_designator(pads, override="A10") == "A10"


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
    created_text = config_path.read_text(encoding="utf-8")
    assert created_configs == [config_path.resolve()]
    assert created_text.startswith("// altium-cruncher pcb-svg configuration")
    assert "Common physical layer tokens" in created_text
    assert "Synthetic layer tokens" in created_text
    assert "add global.pcbdoc" in created_text
    assert "Projection modes: detail, simple, bounding_box, none" in created_text
    assert '"pcbdoc": null' not in created_text
    assert _enabled_views(resolved) == {"top_view"}
    assert resolved.layer_outputs["enabled"] is True
    assert resolved.layer_outputs["layers"] == ["BOTTOM"]


def test_pcb_svg_config_accepts_virtual_assembly_options() -> None:
    config = PcbSvgConfig.from_dict(
        {
            "schema": PCB_SVG_CONFIG_SCHEMA,
            "assembly": {
                "default_projection": "bounding-box",
                "dnp_projection": "none",
                "designator_color": "#123456",
                "dnp_designator_color": "#FF0000",
            },
            "dnp": {
                "color": "#AA0000",
                "hatch": True,
                "hatch_spacing_mm": 1.25,
                "hatch_angle_deg": 30.0,
                "hatch_line_width_mm": 0.11,
            },
            "diodes": {
                "numeric_cathode_pad": "1",
                "cathode_pad_names": ["K", "C"],
                "designator_prefixes": ["D", "LED"],
                "parameter_terms": ["diode", "zener"],
            },
            "components": {
                "D15": {
                    "side": "top",
                    "projection": "none",
                    "assembly_hlr": {
                        "color": "#FF0000",
                        "line_width_mm": 0.2,
                        "mesh_linear_deflection": 0.01,
                    },
                    "pin1_enabled": False,
                    "pin1_pad": "1",
                    "cathode_pad": "C",
                    "diode": True,
                    "diode_line_art": False,
                    "show_designator": True,
                }
            },
            "views": [
                {
                    "name": "pin1",
                    "layers": ["BOARD_OUTLINE", "PIN_1_TOP"],
                }
            ],
        }
    )

    assert config.assembly.default_projection == "bounding_box"
    assert config.assembly.dnp_projection == "none"
    assert config.dnp.hatch_spacing_mm == 1.25
    assert config.diodes.numeric_cathode_pad == "1"
    assert config.components["D15"].cathode_pad == "C"
    assert config.components["D15"].pin1_enabled is False
    assert config.components["D15"].assembly_hlr["color"] == "#FF0000"
    assert config.components["D15"].assembly_hlr["mesh_linear_deflection"] == 0.01
    assert config.views[0].layers == ["BOARD_OUTLINE", "PIN1_TOP"]
    payload = config.to_dict()
    assert "assembly" in payload
    assert "dnp" in payload
    assert "diodes" in payload
    assert "components" in payload


def test_pcb_svg_component_inventory_detects_sides_and_diodes() -> None:
    led_component = SimpleNamespace(
        designator="D1",
        footprint="LED-0603",
        description="green LED diode",
        unique_id="ABC123",
        parameters={"Value": "LED"},
        raw_record={"SOURCEDESCRIPTION": "LED"},
        get_layer_normalized=lambda: "top",
        get_rotation_degrees=lambda: 90.0,
    )
    resistor_component = SimpleNamespace(
        designator="R1",
        footprint="R0603",
        description="resistor",
        unique_id="DEF456",
        parameters={"Value": "10k"},
        raw_record={},
        get_layer_normalized=lambda: "bottom",
        get_rotation_degrees=lambda: 180.0,
    )
    pcbdoc = SimpleNamespace(
        components=[led_component, resistor_component],
        pads=[
            SimpleNamespace(component_index=0, designator="A"),
            SimpleNamespace(component_index=0, designator="C"),
            SimpleNamespace(component_index=1, designator="1"),
            SimpleNamespace(component_index=1, designator="2"),
        ],
    )

    inventory = build_pcb_svg_component_inventory_from_pcbdoc(
        board_key="board",
        pcb_path=Path("board.PcbDoc"),
        pcbdoc=cast(AltiumPcbDoc, pcbdoc),
    )

    assert [component.designator for component in inventory.components] == ["D1", "R1"]
    assert inventory.components[0].pin1_pad is None
    diode = inventory.diode_candidates[0]
    assert diode.designator == "D1"
    assert diode.side == "top"
    assert diode.pad_designators == ("A", "C")
    assert diode.cathode_pad == "C"
    assert diode.is_two_pin_diode is True


def test_pcb_svg_config_template_comments_include_cricket_node_inventory() -> None:
    inventories = load_pcb_svg_component_inventory(CRICKET_PCBDOC)

    text = _default_pcb_svg_config_text(cast(tuple[PcbSvgComponentInventory, ...], inventories))

    assert "// Component inventory (designator: side, footprint, auto pin-1):" in text
    assert "//   D15: top, footprint=LED-0805-RED, pin1=none" in text
    assert "Component override examples:" in text
    assert '"TP1": {"pin1_enabled": false}' in text
    assert "drills.non_plated_color" in text
    assert "// Auto-detected diode candidates:" in text
    assert "//   D15: two-pin, side=top, pads=A,C, cathode=C" in text
    assert '"U5": {"pin1_pad": "B1", "assembly_hlr": {"color": "#2563EB"}}' in text


def test_pcb_svg_without_hlr_tokens_does_not_construct_hlr_renderer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FailingHlrRenderer:
        def __init__(self, *_args: Any, **_kwargs: Any) -> None:
            raise AssertionError("HLR renderer should not be constructed")

    monkeypatch.setattr(
        pcb_svg_a0_renderer,
        "CruncherPcbAssemblySvgRenderer",
        FailingHlrRenderer,
    )
    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(0, 0, 1000, 500)
    config = PcbSvgConfig.default()
    view = PcbSvgViewConfig(
        name="top_no_hlr",
        group_id="pcb-svg-view-top-no-hlr",
        layers=["BOARD_OUTLINE", "TOP", "DRILLS", "SLOTS"],
        mirror=False,
    )
    renderer = PcbSvgA0Renderer(config)

    svg = renderer.render_view_svg(
        pcbdoc,
        view,
        project_parameters={},
        layers=view.layers,
        group_id=view.resolved_group_id(),
        mirror=False,
        styles=config.resolved_styles_for_view(view),
    )

    assert 'id="pcb-svg-view-top-no-hlr"' in svg
    assert "ASSEMBLY_HLR" not in svg


def test_pcb_svg_pin1_layer_renders_smd_dot_a1_pad_and_through_hole() -> None:
    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(0, 0, 1000, 500)
    pcbdoc.add_component(
        designator="U1",
        footprint="QFN",
        position_mils=(100.0, 100.0),
        layer="TOP",
    )
    pcbdoc.add_component(
        designator="J1",
        footprint="BGA",
        position_mils=(300.0, 100.0),
        layer="TOP",
    )
    pcbdoc.add_component(
        designator="J2",
        footprint="HDR",
        position_mils=(500.0, 100.0),
        layer="TOP",
    )
    pcbdoc.add_component(
        designator="TP1",
        footprint="TESTPOINT",
        position_mils=(700.0, 100.0),
        layer="TOP",
    )
    pad_1 = pcbdoc.add_pad(
        designator="1",
        position_mils=(100.0, 100.0),
        width_mils=40.0,
        height_mils=30.0,
        layer=PcbLayer.TOP,
        shape=PadShape.RECTANGLE,
    )
    pad_2 = pcbdoc.add_pad(
        designator="2",
        position_mils=(150.0, 100.0),
        width_mils=40.0,
        height_mils=30.0,
        layer=PcbLayer.TOP,
        shape=PadShape.RECTANGLE,
    )
    pad_a1 = pcbdoc.add_pad(
        designator="A1",
        position_mils=(300.0, 100.0),
        width_mils=28.0,
        height_mils=28.0,
        layer=PcbLayer.TOP,
        shape=PadShape.CIRCLE,
    )
    pad_a2 = pcbdoc.add_pad(
        designator="A2",
        position_mils=(340.0, 100.0),
        width_mils=28.0,
        height_mils=28.0,
        layer=PcbLayer.TOP,
        shape=PadShape.CIRCLE,
    )
    pad_th_1 = pcbdoc.add_pad(
        designator="1",
        position_mils=(500.0, 100.0),
        width_mils=55.0,
        height_mils=55.0,
        layer=PcbLayer.MULTI_LAYER,
        shape=PadShape.CIRCLE,
        hole_size_mils=28.0,
    )
    pad_th_2 = pcbdoc.add_pad(
        designator="2",
        position_mils=(560.0, 100.0),
        width_mils=55.0,
        height_mils=55.0,
        layer=PcbLayer.MULTI_LAYER,
        shape=PadShape.CIRCLE,
        hole_size_mils=28.0,
    )
    pad_tp = pcbdoc.add_pad(
        designator="1",
        position_mils=(700.0, 100.0),
        width_mils=35.0,
        height_mils=35.0,
        layer=PcbLayer.TOP,
        shape=PadShape.CIRCLE,
    )
    pad_1.component_index = 0
    pad_2.component_index = 0
    pad_a1.component_index = 1
    pad_a2.component_index = 1
    pad_th_1.component_index = 2
    pad_th_2.component_index = 2
    pad_tp.component_index = 3
    config = PcbSvgConfig.default()
    view = PcbSvgViewConfig(
        name="pin1",
        group_id="pcb-svg-view-pin1",
        layers=["BOARD_OUTLINE", "PIN1_TOP"],
        mirror=False,
    )
    renderer = PcbSvgA0Renderer(config)

    svg = renderer.render_view_svg(
        pcbdoc,
        view,
        project_parameters={},
        layers=view.layers,
        group_id=view.resolved_group_id(),
        mirror=False,
        styles=config.resolved_styles_for_view(view),
    )

    assert 'data-layer-key="PIN1_TOP"' in svg
    assert 'data-feature="pin1-marker"' in svg
    assert '<circle ' in svg
    assert 'data-component-designator="U1"' in svg
    assert 'data-pad-designator="1"' in svg
    assert 'data-component-designator="J1"' in svg
    assert 'data-pad-designator="A1"' in svg
    assert 'data-component-designator="J2"' in svg
    assert 'data-primitive="pad-hole"' in svg
    assert 'data-component-designator="TP1"' not in svg


def test_pcb_svg_pin1_view_renders_non_plated_zero_annulus_holes() -> None:
    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(0, 0, 1000, 500)
    pcbdoc.add_component(
        designator="J1",
        footprint="HDR",
        position_mils=(100.0, 100.0),
        layer="TOP",
    )
    plated = pcbdoc.add_pad(
        designator="1",
        position_mils=(100.0, 100.0),
        width_mils=55.0,
        height_mils=55.0,
        layer=PcbLayer.MULTI_LAYER,
        shape=PadShape.CIRCLE,
        hole_size_mils=28.0,
        plated=True,
    )
    non_plated = pcbdoc.add_pad(
        designator="M1",
        position_mils=(160.0, 100.0),
        width_mils=0.0,
        height_mils=0.0,
        layer=PcbLayer.MULTI_LAYER,
        shape=PadShape.CIRCLE,
        hole_size_mils=40.0,
        plated=False,
    )
    plated.component_index = 0
    non_plated.component_index = 0
    config = PcbSvgConfig.default()
    view = PcbSvgViewConfig(
        name="pin1",
        group_id="pcb-svg-view-pin1",
        layers=["BOARD_OUTLINE", "TOP", "DRILLS", "PIN1_TOP"],
        mirror=False,
    )
    renderer = PcbSvgA0Renderer(config)

    svg = renderer.render_view_svg(
        pcbdoc,
        view,
        project_parameters={},
        layers=view.layers,
        group_id=view.resolved_group_id(),
        mirror=False,
        styles=config.resolved_styles_for_view(view),
    )

    assert 'data-layer-key="DRILLS"' in svg
    assert 'data-pad-designator="M1"' in svg
    assert 'data-hole-plating="non-plated"' in svg
    assert 'fill="#ADD8E6"' in svg


def test_pcb_svg_pin1_layer_honors_disabled_component_override() -> None:
    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(0, 0, 1000, 500)
    pcbdoc.add_component(
        designator="U1",
        footprint="QFN",
        position_mils=(100.0, 100.0),
        layer="TOP",
    )
    for designator, x_mils in [("1", 100.0), ("2", 140.0)]:
        pad = pcbdoc.add_pad(
            designator=designator,
            position_mils=(x_mils, 100.0),
            width_mils=35.0,
            height_mils=35.0,
            layer=PcbLayer.TOP,
            shape=PadShape.CIRCLE,
        )
        pad.component_index = 0
    config = PcbSvgConfig.from_dict(
        {
            "schema": PCB_SVG_CONFIG_SCHEMA,
            "components": {"U1": {"pin1_enabled": False}},
        }
    )
    view = PcbSvgViewConfig(
        name="pin1",
        group_id="pcb-svg-view-pin1",
        layers=["BOARD_OUTLINE", "PIN1_TOP"],
        mirror=False,
    )
    renderer = PcbSvgA0Renderer(config)

    svg = renderer.render_view_svg(
        pcbdoc,
        view,
        project_parameters={},
        layers=view.layers,
        group_id=view.resolved_group_id(),
        mirror=False,
        styles=config.resolved_styles_for_view(view),
    )

    assert 'data-feature="pin1-marker"' not in svg


def test_pcb_svg_pin1_layer_renders_bga_lga_grid_candidate_and_override() -> None:
    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(0, 0, 1000, 500)
    pcbdoc.add_component(
        designator="U5",
        footprint="NRF52840-QIAA-R",
        position_mils=(100.0, 100.0),
        layer="TOP",
    )
    for designator, x_mils in [
        ("74", 50.0),
        ("A8", 100.0),
        ("A10", 150.0),
        ("B1", 200.0),
        ("C1", 250.0),
    ]:
        pad = pcbdoc.add_pad(
            designator=designator,
            position_mils=(x_mils, 100.0),
            width_mils=22.0,
            height_mils=22.0,
            layer=PcbLayer.TOP,
            shape=PadShape.CIRCLE,
        )
        pad.component_index = 0
    view = PcbSvgViewConfig(
        name="pin1",
        group_id="pcb-svg-view-pin1",
        layers=["BOARD_OUTLINE", "PIN1_TOP"],
        mirror=False,
    )
    renderer = PcbSvgA0Renderer(PcbSvgConfig.default())

    svg = renderer.render_view_svg(
        pcbdoc,
        view,
        project_parameters={},
        layers=view.layers,
        group_id=view.resolved_group_id(),
        mirror=False,
        styles=renderer.config.resolved_styles_for_view(view),
    )

    assert 'data-component-designator="U5"' in svg
    assert 'data-pad-designator="B1"' in svg
    assert 'data-pad-designator="A8"' not in svg

    override_config = PcbSvgConfig.from_dict(
        {
            "schema": PCB_SVG_CONFIG_SCHEMA,
            "components": {"U5": {"pin1_pad": "A10"}},
        }
    )
    renderer = PcbSvgA0Renderer(override_config)
    override_svg = renderer.render_view_svg(
        pcbdoc,
        view,
        project_parameters={},
        layers=view.layers,
        group_id=view.resolved_group_id(),
        mirror=False,
        styles=override_config.resolved_styles_for_view(view),
    )

    assert 'data-pad-designator="A10"' in override_svg
    assert 'data-pad-designator="B1"' not in override_svg


def test_pcb_svg_hlr_bounding_box_mode_does_not_construct_hlr_renderer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FailingHlrRenderer:
        def __init__(self, *_args: Any, **_kwargs: Any) -> None:
            raise AssertionError("HLR renderer should not be constructed")

    monkeypatch.setattr(
        pcb_svg_a0_renderer,
        "CruncherPcbAssemblySvgRenderer",
        FailingHlrRenderer,
    )
    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(0, 0, 1000, 500)
    pcbdoc.add_component(
        designator="U1",
        footprint="SOIC",
        position_mils=(100.0, 100.0),
        layer="TOP",
    )
    pad = pcbdoc.add_pad(
        designator="1",
        position_mils=(100.0, 100.0),
        width_mils=60.0,
        height_mils=30.0,
        layer=PcbLayer.TOP,
        shape=PadShape.ROUNDED_RECTANGLE,
    )
    pad.component_index = 0
    config = PcbSvgConfig.default()
    view = PcbSvgViewConfig(
        name="top_hlr_bounds",
        group_id="pcb-svg-view-hlr-bounds",
        layers=["BOARD_OUTLINE", "ASSEMBLY_HLR_TOP"],
        assembly_hlr_mode="bounding_box",
        mirror=False,
    )
    renderer = PcbSvgA0Renderer(config)

    svg = renderer.render_view_svg(
        pcbdoc,
        view,
        project_parameters={},
        layers=view.layers,
        group_id=view.resolved_group_id(),
        mirror=False,
        styles=config.resolved_styles_for_view(view),
    )

    assert 'data-projection-mode="bounding_box"' in svg
    assert 'data-feature="assembly-bounding-box"' in svg
    assert 'data-component-designator="U1"' in svg


def test_pcb_svg_hlr_bounding_box_mode_honors_component_none_override(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FailingHlrRenderer:
        def __init__(self, *_args: Any, **_kwargs: Any) -> None:
            raise AssertionError("HLR renderer should not be constructed")

    monkeypatch.setattr(
        pcb_svg_a0_renderer,
        "CruncherPcbAssemblySvgRenderer",
        FailingHlrRenderer,
    )
    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(0, 0, 1000, 500)
    for index, designator in enumerate(["J1", "U1"]):
        pcbdoc.add_component(
            designator=designator,
            footprint="HDR",
            position_mils=(100.0 + index * 200.0, 100.0),
            layer="TOP",
        )
        pad = pcbdoc.add_pad(
            designator="1",
            position_mils=(100.0 + index * 200.0, 100.0),
            width_mils=60.0,
            height_mils=30.0,
            layer=PcbLayer.TOP,
            shape=PadShape.ROUNDED_RECTANGLE,
        )
        pad.component_index = index
    config = PcbSvgConfig.from_dict(
        {
            "schema": PCB_SVG_CONFIG_SCHEMA,
            "components": {"J1": {"projection": "none"}},
        }
    )
    view = PcbSvgViewConfig(
        name="top_hlr_bounds",
        group_id="pcb-svg-view-hlr-bounds",
        layers=["BOARD_OUTLINE", "ASSEMBLY_HLR_TOP"],
        assembly_hlr_mode="bounding_box",
        mirror=False,
    )
    renderer = PcbSvgA0Renderer(config)

    svg = renderer.render_view_svg(
        pcbdoc,
        view,
        project_parameters={},
        layers=view.layers,
        group_id=view.resolved_group_id(),
        mirror=False,
        styles=config.resolved_styles_for_view(view),
    )

    assert 'data-component-designator="J1"' not in svg
    assert 'data-component-designator="U1"' in svg


def test_pcb_svg_hlr_bounding_box_mode_honors_component_style_override() -> None:
    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(0, 0, 1000, 500)
    for index, designator in enumerate(["J1", "U1"]):
        pcbdoc.add_component(
            designator=designator,
            footprint="HDR",
            position_mils=(100.0 + index * 200.0, 100.0),
            layer="TOP",
        )
        pad = pcbdoc.add_pad(
            designator="1",
            position_mils=(100.0 + index * 200.0, 100.0),
            width_mils=60.0,
            height_mils=30.0,
            layer=PcbLayer.TOP,
            shape=PadShape.ROUNDED_RECTANGLE,
        )
        pad.component_index = index
    config = PcbSvgConfig.from_dict(
        {
            "schema": PCB_SVG_CONFIG_SCHEMA,
            "global": {
                "styles": {
                    "assembly_hlr": {
                        "color": "#00AA00",
                        "line_width_mm": 0.1,
                    }
                }
            },
            "components": {
                "J1": {
                    "assembly_hlr": {
                        "color": "#FF0000",
                        "line_width_mm": 0.33,
                    }
                }
            },
        }
    )
    view = PcbSvgViewConfig(
        name="top_hlr_bounds",
        group_id="pcb-svg-view-hlr-bounds",
        layers=["BOARD_OUTLINE", "ASSEMBLY_HLR_TOP"],
        assembly_hlr_mode="bounding_box",
        mirror=False,
    )
    renderer = PcbSvgA0Renderer(config)

    svg = renderer.render_view_svg(
        pcbdoc,
        view,
        project_parameters={},
        layers=view.layers,
        group_id=view.resolved_group_id(),
        mirror=False,
        styles=config.resolved_styles_for_view(view),
    )

    assert (
        'stroke="#FF0000" stroke-width="0.33" '
        'data-component-designator="J1"'
    ) in svg
    assert (
        'stroke="#00AA00" stroke-width="0.1" '
        'data-component-designator="U1"'
    ) in svg


def test_pcb_svg_hlr_component_style_override_builds_projection_options() -> None:
    pcbdoc = AltiumPcbDoc()
    pcbdoc.add_component(
        designator="U1",
        footprint="QFN",
        position_mils=(100.0, 100.0),
        layer="TOP",
    )
    config = PcbSvgConfig.from_dict(
        {
            "schema": PCB_SVG_CONFIG_SCHEMA,
            "components": {
                "U1": {
                    "assembly_hlr": {
                        "color": "#123456",
                        "line_width_mm": 0.22,
                        "projection_algorithm": "exact",
                        "curve_mode": "polyline",
                        "samples_per_curve": 18,
                        "round_digits": 4,
                        "mesh_linear_deflection": 0.01,
                        "mesh_angular_deflection": 0.5,
                        "mesh_relative": False,
                        "hlr_angle_tolerance": 0.0174533,
                        "edge_h_outline": False,
                    }
                }
            },
        }
    )
    renderer = PcbSvgA0Renderer(config)
    styles = config.resolved_styles_for_view(
        PcbSvgViewConfig(
            name="top_hlr",
            group_id="pcb-svg-view-top-hlr",
            layers=["ASSEMBLY_HLR_TOP"],
            assembly_hlr_mode="detail",
            mirror=False,
        )
    )
    component_styles = renderer._component_assembly_hlr_styles_for_side(  # noqa: SLF001
        pcbdoc,
        "top",
        styles,
    )

    options = renderer._build_hlr_render_options(  # noqa: SLF001
        side="top",
        mode="detail",
        styles=styles,
        source_layers=[PcbLayer.TOP],
        override_modes={},
        component_styles=component_styles,
    )

    component_options = (options.assembly_component_projection_options or {})["U1"]
    component_stroke = (options.assembly_component_stroke_styles or {})["U1"]
    assert component_options.projection_algorithm == "exact"
    assert component_options.curve_mode == "polyline"
    assert component_options.samples_per_curve == 18
    assert component_options.round_digits == 4
    assert component_options.mesh_linear_deflection == 0.01
    assert component_options.mesh_angular_deflection == 0.5
    assert component_options.mesh_relative is False
    assert component_options.hlr_angle_tolerance == 0.0174533
    assert component_options.edge_flags == {"edge_h_outline": False}
    assert component_stroke == {"color": "#123456", "line_width_mm": 0.22}


def test_pcb_svg_rejects_v1_config() -> None:
    with pytest.raises(ValueError, match="Unsupported pcb-svg config schema"):
        PcbSvgConfig.from_dict({"schema": "wn.pcb.svg.config.v1"})


def test_pcb_svg_config_loader_accepts_jsonc(tmp_path) -> None:
    """Load hand-edited PCB SVG configs with comments and trailing commas."""
    config_path = tmp_path / "pcb.svg.config"
    config_path.write_text(
        """
        {
          // users often toggle views while testing generated output
          "schema": "pcb.svg.config.a0",
          "views": [
            {
              "name": "cutouts",
              "layers": ["BOARD_OUTLINE", "BOARD_CUTOUTS",],
            },
          ],
        }
        """,
        encoding="utf-8",
    )

    config = _load_pcb_svg_config(config_path)

    assert config.views[0].name == "cutouts"
    assert config.views[0].layers == ["BOARD_OUTLINE", "BOARD_CUTOUTS"]


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


def test_pcb_svg_config_validates_canvas_options() -> None:
    with pytest.raises(ValueError, match="global.canvas.bounds"):
        PcbSvgConfig.from_dict(
            {
                "schema": PCB_SVG_CONFIG_SCHEMA,
                "global": {"canvas": {"bounds": "origin_absolute"}},
                "views": [],
            }
        )

    with pytest.raises(ValueError, match="global.canvas.margin_mm"):
        PcbSvgConfig.from_dict(
            {
                "schema": PCB_SVG_CONFIG_SCHEMA,
                "global": {"canvas": {"margin_mm": -1}},
                "views": [],
            }
        )


def test_pcb_svg_durable_group_update_preserves_user_svg_content(tmp_path) -> None:
    target = tmp_path / "view.svg"
    target.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1">'
        '<metadata id="pcb-enrichment-a0">old-meta</metadata>'
        '<text id="user-note">keep</text>'
        '<g id="pcb-svg-view-top"><path id="old"/></g></svg>',
        encoding="utf-8",
    )
    replacement = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2 2">'
        '<metadata id="pcb-enrichment-a0">new-meta</metadata><g id="scene">'
        '<g id="pcb-svg-view-top"><path id="new"/></g></g></svg>'
    )

    write_or_update_view_svg(target, replacement, group_id="pcb-svg-view-top")
    text = target.read_text(encoding="utf-8")

    assert "user-note" in text
    assert 'viewBox="0 0 2 2"' in text
    assert "new-meta" in text
    assert "old-meta" not in text
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
