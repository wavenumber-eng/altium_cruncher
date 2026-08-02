from __future__ import annotations

import json
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest

from altium_monkey.altium_board import BoardOutlineVertex
from altium_monkey.altium_pcb_enums import PadShape
from altium_monkey.altium_pcbdoc import AltiumPcbDoc
from altium_monkey.altium_record_types import PcbLayer

from altium_cruncher.altium_cruncher_cmd_pcb_layer_step import (
    _options_from_config_and_args,
    _resolve_input_files,
    cmd_pcb_layer_step,
    resolve_pcb_layer_step_configs,
)
from altium_cruncher.altium_cruncher_pcb_workflow import load_design_for_pcb_input
from altium_cruncher.altium_cruncher_pcb_layer_step import (
    PCB_LAYER_STEP_CONFIG_SCHEMA_V2,
    PcbLayerStepHighlight,
    PcbLayerStepConfig,
    PcbLayerStepOptions,
    export_pcb_layer_step,
    load_pcb_layer_step_config,
    resolve_pcb_layer_selector,
    _sample_svg_arc_points_mils,
    _svg_like_board_sweep_degrees,
)

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
CRICKET_PRJPCB = (
    PACKAGE_ROOT
    / "tests"
    / "assets"
    / "projects"
    / "cricket-node"
    / "input"
    / "11-10028__cricket-node-hw__B.PrjPcb"
)


def _region_width(region: dict[str, object]) -> float:
    outer = region["outer"]
    assert isinstance(outer, dict)
    points = outer["points"]
    assert isinstance(points, list)
    x_values = [float(point[0]) for point in points]
    return max(x_values) - min(x_values)


def _region_height(region: dict[str, object]) -> float:
    outer = region["outer"]
    assert isinstance(outer, dict)
    points = outer["points"]
    assert isinstance(points, list)
    y_values = [float(point[1]) for point in points]
    return max(y_values) - min(y_values)


def _segment_kinds(region: dict[str, object]) -> list[str]:
    outer = region["outer"]
    assert isinstance(outer, dict)
    segments = outer["segments"]
    assert isinstance(segments, list)
    return [str(segment["kind"]) for segment in segments if isinstance(segment, dict)]


def _arc_segment_centers(region: dict[str, object]) -> list[list[float]]:
    outer = region["outer"]
    assert isinstance(outer, dict)
    segments = outer["segments"]
    assert isinstance(segments, list)
    centers: list[list[float]] = []
    for segment in segments:
        if not isinstance(segment, dict) or segment.get("kind") != "arc":
            continue
        center = segment["center"]
        assert isinstance(center, list)
        centers.append([float(center[0]), float(center[1])])
    return centers


def test_resolve_pcb_layer_selector_accepts_common_names() -> None:
    assert resolve_pcb_layer_selector("bottom") == PcbLayer.BOTTOM
    assert resolve_pcb_layer_selector("Bottom Layer") == PcbLayer.BOTTOM
    assert resolve_pcb_layer_selector("L1") == PcbLayer.TOP
    assert resolve_pcb_layer_selector("MECHANICAL_1") == PcbLayer.MECHANICAL_1


def test_resolve_pcb_layer_selector_rejects_v7_only_layers() -> None:
    """STEP export indexes dense legacy-layer arrays, so V7-only layers must
    fail loudly instead of resolving to a wrong legacy layer."""
    with pytest.raises(ValueError, match="V7-only layer 'MECHANICAL17'"):
        resolve_pcb_layer_selector("Mechanical 17")
    with pytest.raises(ValueError, match="V7-only layer 'MID31'"):
        resolve_pcb_layer_selector("Mid 31")
    with pytest.raises(ValueError, match="Unknown PCB layer selector"):
        resolve_pcb_layer_selector("not-a-layer")


def test_pcb_layer_step_config_auto_created_next_to_input(tmp_path) -> None:
    input_file = tmp_path / "board.PcbDoc"
    input_file.write_text("", encoding="utf-8")
    args = SimpleNamespace(config=None)

    config_by_input, created_configs = resolve_pcb_layer_step_configs(
        args, [input_file]
    )

    config_path = tmp_path / "pcb-layer-step.jsonc"
    assert created_configs == [config_path.resolve()]
    assert config_path.exists()
    assert config_by_input[input_file.resolve()].layer == "bottom"
    config_text = config_path.read_text(encoding="utf-8")
    assert "// pcb-layer-step creates compact fixture-alignment models" in config_text
    config = load_pcb_layer_step_config(config_path)
    assert config.schema == PCB_LAYER_STEP_CONFIG_SCHEMA_V2
    assert len(config.outputs) == 1
    assert config.outputs[0].include_designators == ("TP*", "M*")
    assert config.outputs[0].outline_color == "#FFFF00"
    assert config.outputs[0].board_cutout_color == "#FFFF00"
    assert config.outputs[0].pad_color_rules[0].color == "#FF0000"


def test_pcb_layer_step_init_config_writes_template_without_loading_input(
    tmp_path,
    monkeypatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    result = cmd_pcb_layer_step(
        SimpleNamespace(
            init_config=True,
            force_config=False,
            config=None,
            file=None,
        )
    )

    config_path = tmp_path / "pcb-layer-step.jsonc"
    config_text = config_path.read_text(encoding="utf-8")
    assert result == 0
    assert "COMMON OUTPUT FIELDS" in config_text
    assert "matching_designators" in config_text
    assert "drill_plated_ring_shape" in config_text
    assert "selected_component_mode" in config_text
    assert "altium-cruncher pcb-layer-step --help" in config_text
    assert "/* Global drill mode. Options: auto, cut, overlay, none. */" in config_text
    config = load_pcb_layer_step_config(config_path)
    assert config.outputs[0].include_tracks is False
    assert config.outputs[0].include_arcs is False


def test_pcb_layer_step_prjpcb_board_only_context_skips_schematic_loading(
    monkeypatch,
) -> None:
    import altium_monkey.altium_schdoc as schdoc_module

    def fail_on_schematic_load(*args, **kwargs):
        raise AssertionError("pcb-layer-step should not parse SchDocs")

    monkeypatch.setattr(schdoc_module, "AltiumSchDoc", fail_on_schematic_load)

    design, source_tag = load_design_for_pcb_input(
        CRICKET_PRJPCB,
        project_context="none",
    )

    assert source_tag == "prjpcb_board_only"
    assert design.schdocs == []
    assert [path.name for path in design.get_pcbdoc_paths()] == [
        "cricket-node-hw__B.PcbDoc"
    ]


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
    config_path = tmp_path / "pcb-layer-step.jsonc"
    config_path.write_text(
        """
        {
          "schema": "altium_cruncher.pcb_layer_step.config.a0",
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
          "schema": "altium_cruncher.pcb_layer_step.config.a0",
          "defaults": {
            "layer": "bottom",
            "board_outline": {
              "color": "#CCCCCC",
              "cutout_color": "red",
              "fuse": false
            }
          },
          "outputs": [
            {
              "name": "fixture_alignment",
              "output_step": "{board}__fixture.step",
              "features": {
                "tracks": {
                  "enabled": false,
                  "color": "#123456",
                  "step_body_name": "trace_copper",
                  "thickness_bias_mm": 0.001
                },
                "arcs": {
                  "enabled": false,
                  "color": "#ABCDEF",
                  "step_body_name": "arc_copper"
                },
                "polygons": {
                  "enabled": true,
                  "color": "#654321",
                  "step_body_name": "poured_copper",
                  "thickness_bias_mm": 0.004
                },
                "component_pads": {
                  "mode": "matching_designators",
                  "include_designators": ["TP*", "J*", "U1", "U2"],
                  "color": "#C0FFEE",
                  "step_body_name": "component_pad_copper",
                  "thickness_bias_mm": 0.011,
                  "highlight_rules": [
                    {
                      "designators": ["TP*"],
                      "color": "red",
                      "step_body_name": "test_points"
                    }
                  ]
                },
                "free_pads": false,
                "vias": {
                  "enabled": false,
                  "color": "#00CAFE",
                  "step_body_name": "via_copper",
                  "thickness_bias_mm": 0.007
                },
              },
              "drills": {
                "mode": "overlay",
                "minimum_diameter_mm": 0.85,
                "shape": "ring",
                "plated_color": "green",
                "non_plated_color": "blue",
                "ring_width_mm": 0.15,
                "plated_ring_shape": "annulus",
                "selected_component_mode": "cut",
                "other_component_mode": "none",
                "free_pad_mode": "overlay",
                "via_mode": "inherit",
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
    assert output.track_color == "#123456"
    assert output.track_body == "trace_copper"
    assert output.arc_color == "#ABCDEF"
    assert output.arc_body == "arc_copper"
    assert output.include_poured_polygons is True
    assert output.polygon_color == "#654321"
    assert output.polygon_body == "poured_copper"
    assert output.include_vias is False
    assert output.via_color == "#00CAFE"
    assert output.via_body == "via_copper"
    assert output.component_pad_color == "#C0FFEE"
    assert output.component_pad_body == "component_pad_copper"
    assert output.board_cutout_color == "#FF0000"
    assert output.include_designators == ("TP*", "J*", "U1", "U2")
    assert output.pad_color_rules[0].color == "#FF0000"
    assert output.track_thickness_bias_mm == 0.001
    assert output.polygon_thickness_bias_mm == 0.004
    assert output.via_thickness_bias_mm == 0.007
    assert output.component_pad_thickness_bias_mm == 0.011
    assert output.drill_minimum_diameter_mm == 0.85
    assert output.drill_hole_shape == "ring"
    assert output.drill_plated_hole_color == "#008000"
    assert output.drill_non_plated_hole_color == "#0000FF"
    assert output.drill_plated_ring_shape == "annulus"
    assert output.drill_selected_component_mode == "cut"
    assert output.drill_other_component_mode == "none"
    assert output.drill_free_pad_mode == "overlay"
    assert output.drill_via_mode == "inherit"


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
    assert manifest["schema"] == "altium_cruncher.pcb_layer_step.a0"
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


def test_export_pcb_layer_step_uses_board_origin_relative_coordinates(
    monkeypatch,
    tmp_path,
) -> None:
    captured = {}

    def write_planar_step(request, output_path):
        captured["request"] = request
        output_path.write_bytes(json.dumps(request).encode("utf-8"))
        return output_path

    monkeypatch.setitem(
        sys.modules, "geometer", SimpleNamespace(write_planar_step=write_planar_step)
    )

    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(1000, 1000, 1500, 1300)
    pcbdoc.set_origin_mils(1000, 1000)
    pcbdoc.add_pad(
        designator="TP1",
        position_mils=(1100, 1200),
        width_mils=100,
        height_mils=100,
        layer=PcbLayer.BOTTOM,
        shape=PadShape.CIRCLE,
    )

    result = export_pcb_layer_step(
        pcbdoc,
        tmp_path / "origin-relative.step",
        board_name="fixture_board",
        options=PcbLayerStepOptions(
            layer=PcbLayer.BOTTOM,
            include_board_outline=False,
            drill_hole_mode="none",
        ),
    )

    copper_body = captured["request"]["bodies"][0]
    points = copper_body["regions"][0]["outer"]["points"]
    center_x = (
        min(point[0] for point in points) + max(point[0] for point in points)
    ) / 2
    center_y = (
        min(point[1] for point in points) + max(point[1] for point in points)
    ) / 2
    assert abs(center_x - 2.54) < 1e-9
    assert abs(center_y - 5.08) < 1e-9

    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    assert manifest["coordinate_origin"]["mode"] == "board_origin"
    assert manifest["coordinate_origin"]["origin_mils"] == [1000.0, 1000.0]


def test_export_pcb_layer_step_renders_obround_circle_pads_as_capsules(
    monkeypatch,
    tmp_path,
) -> None:
    captured = {}

    def write_planar_step(request, output_path):
        captured["request"] = request
        output_path.write_bytes(json.dumps(request).encode("utf-8"))
        return output_path

    monkeypatch.setitem(
        sys.modules, "geometer", SimpleNamespace(write_planar_step=write_planar_step)
    )

    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(0, 0, 500, 300)
    pcbdoc.add_pad(
        designator="TP9",
        position_mils=(250, 150),
        width_mils=150,
        height_mils=75,
        layer=PcbLayer.BOTTOM,
        shape=PadShape.CIRCLE,
    )

    export_pcb_layer_step(
        pcbdoc,
        tmp_path / "obround.step",
        board_name="fixture_board",
        options=PcbLayerStepOptions(
            layer=PcbLayer.BOTTOM,
            include_board_outline=False,
            drill_hole_mode="none",
        ),
    )

    copper_body = captured["request"]["bodies"][0]
    region = copper_body["regions"][0]
    arc_centers = _arc_segment_centers(region)

    assert _segment_kinds(region) == ["line", "arc", "line", "arc"]
    assert abs(abs(arc_centers[0][0] - arc_centers[1][0]) - 1.905) < 1e-9
    assert abs(arc_centers[0][1] - arc_centers[1][1]) < 1e-9
    assert abs(_region_height(region) - 1.905) < 1e-9


def test_export_pcb_layer_step_renders_highlight_obround_pads_as_capsules(
    monkeypatch,
    tmp_path,
) -> None:
    captured = {}

    def write_planar_step(request, output_path):
        captured["request"] = request
        output_path.write_bytes(json.dumps(request).encode("utf-8"))
        return output_path

    monkeypatch.setitem(
        sys.modules, "geometer", SimpleNamespace(write_planar_step=write_planar_step)
    )

    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(0, 0, 500, 300)

    export_pcb_layer_step(
        pcbdoc,
        tmp_path / "highlight-obround.step",
        board_name="fixture_board",
        options=PcbLayerStepOptions(
            layer=PcbLayer.BOTTOM,
            include_copper=False,
            include_board_outline=False,
            drill_hole_mode="none",
            highlights=(
                PcbLayerStepHighlight(
                    id="test_points",
                    color="#FF0000",
                    pad_geometries=(
                        {
                            "x_mils": 250,
                            "y_mils": 150,
                            "width_mils": 150,
                            "height_mils": 75,
                            "shape": int(PadShape.CIRCLE),
                            "layer": int(PcbLayer.BOTTOM),
                        },
                    ),
                ),
            ),
        ),
    )

    highlight_body = captured["request"]["bodies"][0]
    region = highlight_body["regions"][0]
    arc_centers = _arc_segment_centers(region)

    assert highlight_body["id"] == "test_points"
    assert _segment_kinds(region) == ["line", "arc", "line", "arc"]
    assert abs(abs(arc_centers[0][0] - arc_centers[1][0]) - 1.905) < 1e-9
    assert abs(arc_centers[0][1] - arc_centers[1][1]) < 1e-9
    assert abs(_region_height(region) - 1.905) < 1e-9


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
            "schema": "altium_cruncher.pcb_layer_step.config.a0",
            "outputs": [
                {
                    "features": {
                        "tracks": False,
                        "vias": False,
                        "component_pads": {
                            "mode": "matching_designators",
                            "include_designators": ["TP*", "J*", "U1"],
                            "highlight_rules": [
                                {
                                    "designators": ["TP*"],
                                    "color": "red",
                                    "step_body_name": "test_points",
                                }
                            ],
                        },
                        "free_pads": False,
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
    assert set(bodies) == {
        "test_points",
        "copper_pads",
        "drill_holes",
        "board_outline",
    }
    assert bodies["test_points"]["color"] == "#FF0000"
    assert len(bodies["test_points"]["regions"]) == 1
    assert len(bodies["copper_pads"]["regions"]) == 2
    assert len(bodies["drill_holes"]["regions"]) == 1
    assert "holes" in bodies["drill_holes"]["regions"][0]

    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    assert manifest["counts"]["source_layer_geometries"] == 3
    assert manifest["counts"]["drill_overlay_geometries"] == 1
    assert manifest["options"]["features"]["tracks"] is False
    assert manifest["options"]["features"]["include_designators"] == ["TP*", "J*", "U1"]


def test_export_pcb_layer_step_colors_cutouts_and_plating_specific_drills(
    monkeypatch,
    tmp_path,
) -> None:
    """Color cutout outlines and split plated/non-plated drill overlay bodies."""
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
    plated_pad = pcbdoc.add_pad(
        designator="1",
        position_mils=(250, 250),
        width_mils=120,
        height_mils=120,
        layer=PcbLayer.MULTI_LAYER,
        shape=PadShape.CIRCLE,
        hole_size_mils=60,
        plated=True,
    )
    non_plated_pad = pcbdoc.add_pad(
        designator="1",
        position_mils=(750, 250),
        width_mils=120,
        height_mils=120,
        layer=PcbLayer.MULTI_LAYER,
        shape=PadShape.CIRCLE,
        hole_size_mils=60,
        plated=False,
    )
    assert plated_pad.is_plated is True
    assert non_plated_pad.is_plated is False
    pcbdoc.board.outline.cutouts.append(
        [
            BoardOutlineVertex.line(400, 180),
            BoardOutlineVertex.line(600, 180),
            BoardOutlineVertex.line(600, 320),
            BoardOutlineVertex.line(400, 320),
        ]
    )

    export_pcb_layer_step(
        pcbdoc,
        tmp_path / "fixture.step",
        board_name="fixture_board",
        options=PcbLayerStepOptions(
            layer=PcbLayer.BOTTOM,
            include_copper=False,
            board_cutout_color="#FF00FF",
            drill_hole_mode="overlay",
            drill_hole_shape="ring",
            drill_ring_width_mm=0.1,
            drill_plated_hole_color="#00FF00",
            drill_non_plated_hole_color="#0000FF",
        ),
    )

    bodies = {body["id"]: body for body in captured["request"]["bodies"]}
    assert set(bodies) == {
        "plated_drill_holes",
        "non_plated_drill_holes",
        "board_outline",
        "board_cutouts",
    }
    assert bodies["board_cutouts"]["color"] == "#FF00FF"
    assert bodies["plated_drill_holes"]["color"] == "#00FF00"
    assert bodies["non_plated_drill_holes"]["color"] == "#0000FF"

    plated_region = bodies["plated_drill_holes"]["regions"][0]
    non_plated_region = bodies["non_plated_drill_holes"]["regions"][0]
    assert "holes" in plated_region
    assert "holes" in non_plated_region
    plated_width = _region_width(plated_region)
    non_plated_width = _region_width(non_plated_region)
    assert abs(plated_width - non_plated_width) < 1e-9


def test_export_pcb_layer_step_splits_track_and_polygon_colors(
    monkeypatch,
    tmp_path,
) -> None:
    """Allow fixture configs to color traces and pours independently."""
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
    pcbdoc.add_track((50, 50), (450, 50), width_mils=12, layer=PcbLayer.BOTTOM)
    pcbdoc.add_track((50, 150), (450, 150), width_mils=20, layer=PcbLayer.BOTTOM)
    pcbdoc.tracks[-1].polygon_index = 1

    export_pcb_layer_step(
        pcbdoc,
        tmp_path / "fixture.step",
        board_name="fixture_board",
        options=PcbLayerStepOptions(
            layer=PcbLayer.BOTTOM,
            include_board_outline=False,
            drill_hole_mode="none",
            track_color="#123456",
            track_body="trace_copper",
            polygon_color="#654321",
            polygon_body="poured_copper",
        ),
    )

    bodies = {body["id"]: body for body in captured["request"]["bodies"]}
    assert set(bodies) == {"trace_copper", "poured_copper"}
    assert bodies["trace_copper"]["color"] == "#123456"
    assert bodies["poured_copper"]["color"] == "#654321"
    assert len(bodies["trace_copper"]["regions"]) == 1
    assert len(bodies["poured_copper"]["regions"]) == 1


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

    bodies = {body["id"]: body for body in captured["request"]["bodies"]}
    assert set(bodies) == {
        "copper",
        "copper_vias",
        "drill_holes",
        "board_outline",
    }
    assert "cutouts" in bodies["copper"]
    assert bodies["copper_vias"]["z_mm"] == -0.006
    assert bodies["copper_vias"]["thickness_mm"] == 0.047
    assert len(bodies["drill_holes"]["regions"]) == 130

    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    assert manifest["options"]["effective_drill_hole_mode"] == "overlay"
    assert manifest["counts"]["drill_boolean_cut_geometries"] == 0
    assert manifest["counts"]["drill_copper_cutout_geometries"] == 130
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


def test_pad_corner_radius_percent_prefers_exact_fractional_lane() -> None:
    from altium_cruncher.altium_cruncher_pcb_layer_step import (
        _pad_corner_radius_percent,
    )

    exact_pad = SimpleNamespace(
        exact_corner_radius_percent_on_layer=lambda layer: 18.181818,
        corner_radius=[18] * 32,
        corner_radius_percentage=18,
    )
    assert _pad_corner_radius_percent(exact_pad, PcbLayer.TOP) == pytest.approx(
        18.181818
    )

    rounded_pad = SimpleNamespace(
        exact_corner_radius_percent_on_layer=lambda layer: None,
        corner_radius=[25] * 32,
        corner_radius_percentage=25,
    )
    assert _pad_corner_radius_percent(rounded_pad, PcbLayer.TOP) == 25.0

    legacy_pad = SimpleNamespace(
        corner_radius=[],
        corner_radius_percentage=40,
    )
    assert _pad_corner_radius_percent(legacy_pad, PcbLayer.TOP) == 40.0


def test_highlight_pad_geometry_keeps_fractional_corner_radius_percent() -> None:
    from altium_cruncher.altium_cruncher_pcb_layer_step_highlights import (
        highlight_bodies_from_geometries,
    )

    captured: list[dict[str, object]] = []

    def pad_shape_region(**kwargs):
        captured.append(kwargs)
        return SimpleNamespace(to_json=lambda: {"outer": {"points": []}})

    highlight = PcbLayerStepHighlight(
        id="hl",
        color="#ff0000",
        pad_geometries=(
            {
                "x_mils": 0.0,
                "y_mils": 0.0,
                "width_mils": 60.0,
                "height_mils": 60.0,
                "shape": int(PadShape.ROUNDED_RECTANGLE.value),
                "corner_radius_percent": 18.181818,
            },
        ),
    )
    bodies = highlight_bodies_from_geometries(
        highlights=(highlight,),
        layer=PcbLayer.TOP,
        z_mm=0.0,
        copper_thickness_mm=0.035,
        pad_shape_region=pad_shape_region,
        step_name=lambda name: name,
    )

    assert len(bodies) == 1
    assert captured[0]["corner_radius_percent"] == pytest.approx(18.181818)
