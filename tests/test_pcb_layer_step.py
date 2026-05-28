from __future__ import annotations

import json
import sys
from types import SimpleNamespace

from altium_monkey.altium_pcb_enums import PadShape
from altium_monkey.altium_pcbdoc import AltiumPcbDoc
from altium_monkey.altium_record_types import PcbLayer

from altium_cruncher.altium_cruncher_cmd_pcb_layer_step import (
    _options_from_config_and_args,
    _resolve_input_files,
    resolve_pcb_layer_step_configs,
)
from altium_cruncher.altium_cruncher_pcb_layer_step import (
    PCB_LAYER_STEP_CONFIG_SCHEMA_V2,
    PcbLayerStepConfig,
    PcbLayerStepOptions,
    export_pcb_layer_step,
    load_pcb_layer_step_config,
    resolve_pcb_layer_selector,
    _sample_svg_arc_points_mils,
    _svg_like_board_sweep_degrees,
)


def test_resolve_pcb_layer_selector_accepts_common_names() -> None:
    assert resolve_pcb_layer_selector("bottom") == PcbLayer.BOTTOM
    assert resolve_pcb_layer_selector("Bottom Layer") == PcbLayer.BOTTOM
    assert resolve_pcb_layer_selector("L1") == PcbLayer.TOP
    assert resolve_pcb_layer_selector("MECHANICAL_1") == PcbLayer.MECHANICAL_1


def test_pcb_layer_step_config_auto_created_next_to_input(tmp_path) -> None:
    input_file = tmp_path / "board.PcbDoc"
    input_file.write_text("", encoding="utf-8")
    args = SimpleNamespace(config=None)

    config_by_input, created_configs = resolve_pcb_layer_step_configs(
        args, [input_file]
    )

    config_path = tmp_path / "pcb-layer-step.json"
    assert created_configs == [config_path.resolve()]
    assert config_path.exists()
    assert config_by_input[input_file.resolve()].layer == "bottom"
    config_text = config_path.read_text(encoding="utf-8")
    assert "/* pcb-layer-step creates compact fixture-alignment models" in config_text
    config = load_pcb_layer_step_config(config_path)
    assert config.schema == PCB_LAYER_STEP_CONFIG_SCHEMA_V2
    assert len(config.outputs) == 1
    assert config.outputs[0].include_designators == ("TP*",)
    assert config.outputs[0].pad_color_rules[0].color == "#FF0000"


def test_pcb_layer_step_options_merge_config_with_cli_overrides() -> None:
    config = PcbLayerStepConfig(
        layer="top",
        thickness_mm=0.08,
        include_board_outline=False,
        fuse_copper=True,
        fuse_board_outline=True,
    )
    args = SimpleNamespace(
        layer="bottom",
        thickness_mm=None,
        z_mm=None,
        copper_color=None,
        outline_width_mm=None,
        outline_color=None,
        outline_only=False,
        no_board_outline=False,
        exclude_poured_polygons=False,
        no_hole_cuts=False,
        no_fuse=True,
        arc_segments=None,
    )

    options = _options_from_config_and_args(config, args)

    assert options.layer == PcbLayer.BOTTOM
    assert options.thickness_mm == 0.08
    assert options.include_board_outline is False
    assert options.fuse_copper is False
    assert options.fuse_board_outline is False


def test_pcb_layer_step_config_loader_accepts_jsonc(tmp_path) -> None:
    """Load editable layer STEP configs with comments and trailing commas."""
    config_path = tmp_path / "pcb-layer-step.json"
    config_path.write_text(
        """
        {
          "schema": "wn.altium_cruncher.pcb_layer_step.config.v1",
          "layer": "top", // temporarily switch layer while inspecting output
        }
        """,
        encoding="utf-8",
    )

    config = load_pcb_layer_step_config(config_path)

    assert config.layer == "top"


def test_pcb_layer_step_v2_config_parses_fixture_outputs(tmp_path) -> None:
    """Parse multi-output fixture-alignment configs with designator rules."""
    config_path = tmp_path / "pcb-layer-step.json"
    config_path.write_text(
        """
        {
          "schema": "wn.altium_cruncher.pcb_layer_step.config.v2",
          "defaults": {
            "layer": "bottom",
            "board_outline": {"color": "#CCCCCC", "fuse": false}
          },
          "outputs": [
            {
              "name": "fixture_alignment",
              "output_step": "{board}__fixture.step",
              "features": {
                "tracks": false,
                "component_pads": {
                  "mode": "matching_designators",
                  "include_designators": ["TP*", "J*", "U1", "U2"]
                },
                "free_pads": false,
                "vias": false,
              },
              "colors": {
                "default_copper": "copper",
                "pad_rules": [
                  {"designators": ["TP*"], "color": "red", "body": "test_points"}
                ],
              },
              "drills": {
                "mode": "overlay",
                "minimum_diameter_mm": 0.85,
                "shape": "ring",
                "ring_width_mm": 0.15,
              },
              "fuse_copper": false,
            }
          ]
        }
        """,
        encoding="utf-8",
    )

    config = load_pcb_layer_step_config(config_path)
    output = config.outputs[0]

    assert output.output_step == "{board}__fixture.step"
    assert output.include_tracks is False
    assert output.include_vias is False
    assert output.include_designators == ("TP*", "J*", "U1", "U2")
    assert output.pad_color_rules[0].color == "#FF0000"
    assert output.drill_minimum_diameter_mm == 0.85
    assert output.drill_hole_shape == "ring"


def test_pcb_layer_step_input_resolution_accepts_pcbdoc_and_prjpcb(tmp_path) -> None:
    pcbdoc = tmp_path / "board.PcbDoc"
    prjpcb = tmp_path / "project.PrjPcb"
    pcbdoc.write_text("", encoding="utf-8")
    prjpcb.write_text("", encoding="utf-8")

    assert _resolve_input_files(pcbdoc) == [pcbdoc.resolve()]
    assert _resolve_input_files(prjpcb) == [prjpcb.resolve()]


def test_svg_like_sampling_keeps_shape_region_arc_on_vertices() -> None:
    start = (31970.4282, 20366.8562)
    end = (31811.6832, 20366.8562)
    center = (31891.0557, 20376.8565)

    sweep = _svg_like_board_sweep_degrees(
        center_mils=center,
        radius_mils=80.0,
        start_point_mils=start,
        end_point_mils=end,
        start_degrees=187.1810,
        end_degrees=352.8190,
        default_sweep_flag=1,
    )
    points = _sample_svg_arc_points_mils(
        center_mils=center,
        radius_mils=80.0,
        start_point_mils=start,
        end_point_mils=end,
        start_degrees=187.1810,
        end_degrees=352.8190,
        default_sweep_flag=1,
        arc_segments=16,
    )

    assert sweep < 0.0
    assert points[0] == start
    assert points[-1] == end


def test_svg_like_sampling_matches_pcb_arc_center_side() -> None:
    start = (32090.878, 19513.794)
    end = (32090.878, 19528.794)
    center = (32090.878, 19521.294)

    points = _sample_svg_arc_points_mils(
        center_mils=center,
        radius_mils=7.5,
        start_point_mils=start,
        end_point_mils=end,
        start_degrees=270.0,
        end_degrees=90.0,
        default_sweep_flag=1,
        arc_segments=16,
    )

    assert (
        _svg_like_board_sweep_degrees(
            center_mils=center,
            radius_mils=7.5,
            start_point_mils=start,
            end_point_mils=end,
            start_degrees=270.0,
            end_degrees=90.0,
            default_sweep_flag=1,
        )
        > 0.0
    )
    assert max(x for x, _ in points) > center[0] + 7.0


def test_export_pcb_layer_step_writes_step_and_manifest(tmp_path) -> None:
    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(0, 0, 500, 300)
    pcbdoc.add_track((50, 50), (450, 50), width_mils=12, layer=PcbLayer.BOTTOM)
    pcbdoc.add_pad(
        designator="TP1",
        position_mils=(250, 150),
        width_mils=65,
        height_mils=65,
        layer=PcbLayer.MULTI_LAYER,
        shape=PadShape.CIRCLE,
        hole_size_mils=28,
        plated=True,
    )
    pcbdoc.add_via(
        position_mils=(120, 180),
        diameter_mils=40,
        hole_size_mils=20,
    )

    output_path = tmp_path / "bottom.step"
    result = export_pcb_layer_step(
        pcbdoc,
        output_path,
        board_name="fixture_board",
        source_input="fixture_board.PcbDoc",
        options=PcbLayerStepOptions(layer=PcbLayer.BOTTOM, thickness_mm=0.05),
    )

    assert result.output_path == output_path.resolve()
    assert output_path.read_text(encoding="utf-8", errors="ignore").startswith(
        "ISO-10303-21;"
    )
    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    assert manifest["schema"] == "wn.altium_cruncher.pcb_layer_step.v1"
    assert manifest["backend"] == "geometer.planar_step"
    assert manifest["layer"]["json_name"] == "BOTTOM"
    assert manifest["counts"]["copper_bodies"] >= 1
    assert manifest["counts"]["outline_bodies"] >= 1
    assert manifest["counts"]["drill_cut_geometries"] == 2
    assert manifest["options"]["fuse_copper"] is True
    assert manifest["options"]["fuse_board_outline"] is True


def test_export_pcb_layer_step_requests_geometer_fusion(monkeypatch, tmp_path) -> None:
    captured = {}

    def write_planar_step(request, output_path):
        captured["request"] = request
        output_path.write_bytes(b"ISO-10303-21;\n")
        return output_path

    monkeypatch.setitem(
        sys.modules, "geometer", SimpleNamespace(write_planar_step=write_planar_step)
    )

    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(0, 0, 500, 300)
    pcbdoc.add_track((50, 50), (450, 50), width_mils=12, layer=PcbLayer.BOTTOM)
    pcbdoc.add_track((250, 20), (250, 120), width_mils=12, layer=PcbLayer.BOTTOM)

    export_pcb_layer_step(
        pcbdoc,
        tmp_path / "bottom.step",
        board_name="fixture_board",
        options=PcbLayerStepOptions(layer=PcbLayer.BOTTOM),
    )

    copper_body = captured["request"]["bodies"][0]
    outline_body = captured["request"]["bodies"][1]
    assert copper_body["id"] == "copper"
    assert copper_body["fuse_regions"] is True
    assert outline_body["id"] == "board_outline"
    assert outline_body["fuse_regions"] is True


def test_export_pcb_layer_step_can_preserve_primitive_regions(
    monkeypatch, tmp_path
) -> None:
    captured = {}

    def write_planar_step(request, output_path):
        captured["request"] = request
        output_path.write_bytes(b"ISO-10303-21;\n")
        return output_path

    monkeypatch.setitem(
        sys.modules, "geometer", SimpleNamespace(write_planar_step=write_planar_step)
    )

    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(0, 0, 500, 300)
    pcbdoc.add_track((50, 50), (450, 50), width_mils=12, layer=PcbLayer.BOTTOM)

    export_pcb_layer_step(
        pcbdoc,
        tmp_path / "bottom.step",
        board_name="fixture_board",
        options=PcbLayerStepOptions(layer=PcbLayer.BOTTOM, fuse_copper=False),
    )

    copper_body = captured["request"]["bodies"][0]
    outline_body = captured["request"]["bodies"][1]
    assert "fuse_regions" not in copper_body
    assert outline_body["id"] == "board_outline"
    assert outline_body["fuse_regions"] is True


def test_export_pcb_layer_step_filters_designators_and_renders_drill_rings(
    monkeypatch,
    tmp_path,
) -> None:
    """Build fixture bodies from selected designators and filtered drill overlays."""
    captured = {}

    def write_planar_step(request, output_path):
        captured["request"] = request
        output_path.write_bytes(json.dumps(request).encode("utf-8"))
        return output_path

    monkeypatch.setitem(
        sys.modules, "geometer", SimpleNamespace(write_planar_step=write_planar_step)
    )

    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(0, 0, 1000, 500)
    for index, designator in enumerate(["TP1", "J1", "U1", "R1"]):
        pcbdoc.add_component(
            designator=designator,
            footprint="TEST",
            position_mils=(100 + (index * 100), 100),
            layer="BOTTOM",
        )
        pad = pcbdoc.add_pad(
            designator="1",
            position_mils=(100 + (index * 100), 100),
            width_mils=70,
            height_mils=70,
            layer=PcbLayer.BOTTOM,
            shape=PadShape.CIRCLE,
            hole_size_mils=40 if designator == "TP1" else 20,
        )
        pad.component_index = index
    pcbdoc.add_track((50, 50), (950, 50), width_mils=12, layer=PcbLayer.BOTTOM)
    pcbdoc.add_via(position_mils=(500, 250), diameter_mils=50, hole_size_mils=20)

    config = PcbLayerStepConfig.from_dict(
        {
            "schema": "wn.altium_cruncher.pcb_layer_step.config.v2",
            "outputs": [
                {
                    "features": {
                        "tracks": False,
                        "vias": False,
                        "component_pads": {
                            "mode": "matching_designators",
                            "include_designators": ["TP*", "J*", "U1"],
                        },
                        "free_pads": False,
                    },
                    "colors": {
                        "pad_rules": [
                            {
                                "designators": ["TP*"],
                                "color": "red",
                                "body": "test_points",
                            }
                        ]
                    },
                    "drills": {
                        "mode": "overlay",
                        "minimum_diameter_mm": 0.85,
                        "shape": "ring",
                    },
                }
            ],
        }
    )

    result = export_pcb_layer_step(
        pcbdoc,
        tmp_path / "fixture.step",
        options=config.outputs[0].to_options(),
    )

    bodies = {body["id"]: body for body in captured["request"]["bodies"]}
    assert set(bodies) == {"test_points", "copper", "drill_holes", "board_outline"}
    assert bodies["test_points"]["color"] == "#FF0000"
    assert len(bodies["test_points"]["regions"]) == 1
    assert len(bodies["copper"]["regions"]) == 2
    assert len(bodies["drill_holes"]["regions"]) == 1
    assert "holes" in bodies["drill_holes"]["regions"][0]

    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    assert manifest["counts"]["source_layer_geometries"] == 3
    assert manifest["counts"]["drill_overlay_geometries"] == 1
    assert manifest["options"]["features"]["tracks"] is False
    assert manifest["options"]["features"]["include_designators"] == ["TP*", "J*", "U1"]


def test_export_pcb_layer_step_overlays_dense_drill_sets(
    monkeypatch,
    tmp_path,
) -> None:
    """Avoid slow boolean drill cuts when dense boards exceed the auto threshold."""
    captured = {}

    def write_planar_step(request, output_path):
        captured["request"] = request
        output_path.write_bytes(b"ISO-10303-21;\n")
        return output_path

    monkeypatch.setitem(
        sys.modules, "geometer", SimpleNamespace(write_planar_step=write_planar_step)
    )

    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(0, 0, 5000, 5000)
    pcbdoc.add_track((50, 50), (4950, 50), width_mils=12, layer=PcbLayer.BOTTOM)
    for index in range(130):
        pcbdoc.add_via(
            position_mils=(100 + index * 30, 200),
            diameter_mils=40,
            hole_size_mils=20,
        )

    result = export_pcb_layer_step(
        pcbdoc,
        tmp_path / "bottom.step",
        board_name="fixture_board",
        options=PcbLayerStepOptions(layer=PcbLayer.BOTTOM),
    )

    bodies = captured["request"]["bodies"]
    assert [body["id"] for body in bodies] == [
        "copper",
        "drill_holes",
        "board_outline",
    ]
    assert "cutouts" not in bodies[0]
    assert len(bodies[1]["regions"]) == 130

    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    assert manifest["options"]["effective_drill_hole_mode"] == "overlay"
    assert manifest["counts"]["drill_boolean_cut_geometries"] == 0
    assert manifest["counts"]["drill_overlay_geometries"] == 130


def test_export_pcb_layer_step_can_preserve_board_outline_regions(
    monkeypatch, tmp_path
) -> None:
    captured = {}

    def write_planar_step(request, output_path):
        captured["request"] = request
        output_path.write_bytes(b"ISO-10303-21;\n")
        return output_path

    monkeypatch.setitem(
        sys.modules, "geometer", SimpleNamespace(write_planar_step=write_planar_step)
    )

    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(0, 0, 500, 300)

    export_pcb_layer_step(
        pcbdoc,
        tmp_path / "outline.step",
        board_name="fixture_board",
        options=PcbLayerStepOptions(
            layer=PcbLayer.BOTTOM,
            include_copper=False,
            fuse_board_outline=False,
        ),
    )

    outline_body = captured["request"]["bodies"][0]
    assert outline_body["id"] == "board_outline"
    assert "fuse_regions" not in outline_body
