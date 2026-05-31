from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from altium_cruncher.altium_cruncher_debug_plate import (
    DEBUG_PLATE_CONFIG_SCHEMA,
    MATE_CONFIG_SCHEMA,
    build_debug_plate_mco,
    build_debug_plate_mate_seed_config,
    execute_debug_plate_config,
    inspect_debug_plate_source,
    inspect_pcbdoc_for_debug_plate,
    load_debug_plate_config,
    write_debug_plate_config_template,
)
from altium_cruncher.altium_cruncher_debug_plate_graphics import (
    build_pcb_board_projection_operations,
    build_pcb_reference_graphics_operations,
)
from altium_cruncher.altium_cruncher_debug_plate_parts import (
    DEBUG_PLATE_PARTS_CACHE_FILENAME,
    build_node_test_array_parts_manifest,
    load_debug_plate_known_parts_manifest,
    manifest_path_for_cache_dir,
    resolve_known_part,
    write_debug_plate_known_parts_manifest,
)
from altium_cruncher.altium_cruncher_mco import MCO_SCHEMA, load_jsonc_file


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def _write_json(path: Path, payload: object) -> Path:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def _write_minimal_known_part_cache(tmp_path: Path) -> Path:
    from altium_monkey import AltiumPcbLib, AltiumSchLib, PadShape, PcbLayer
    from altium_monkey.altium_record_sch__pin import AltiumSchPin

    cache_dir = tmp_path / "cache"
    for symbol_name, pin_name, x_mils, y_mils, orientation in [
        ("YZ209315103P-01", "SIGNAL", 0, 0, 0),
        ("9774080360R", "MOUNT", 0, -100, 3),
        ("H2184-05", "ALIGN", 0, -20, 3),
    ]:
        schlib_path = cache_dir / "schlib" / f"{symbol_name}.SchLib"
        schlib_path.parent.mkdir(parents=True, exist_ok=True)
        schlib = AltiumSchLib()
        symbol = schlib.add_symbol(symbol_name)
        symbol.add_pin(
            AltiumSchPin(
                "1",
                pin_name,
                x_mils,
                y_mils,
                orientation=orientation,
                length=100,
            )
        )
        schlib.save(schlib_path)

    for footprint_name, pcblib_name in [
        ("YZ209315103P-01", "YZ209315103P-01"),
        ("9774080360R-YIYUAN", "9774080360R-YIYUAN"),
        ("H2184-05", "H2184-05"),
    ]:
        pcblib_path = cache_dir / "pcblib" / "split" / f"{pcblib_name}.PcbLib"
        pcblib_path.parent.mkdir(parents=True, exist_ok=True)
        pcblib = AltiumPcbLib()
        footprint = pcblib.add_footprint(footprint_name)
        footprint.add_pad(
            designator="1",
            position_mils=(0.0, 0.0),
            width_mils=80.0,
            height_mils=80.0,
            layer=PcbLayer.MULTI_LAYER,
            shape=PadShape.CIRCLE,
            hole_size_mils=40.0,
            plated=False,
        )
        pcblib.save(pcblib_path)

    return write_debug_plate_known_parts_manifest(
        build_node_test_array_parts_manifest(
            tmp_path / "node-test-array.PrjPcb",
            cache_dir,
        ),
        cache_dir / DEBUG_PLATE_PARTS_CACHE_FILENAME,
    )


def _write_mate_source_pcbdoc(
    path: Path,
    *,
    tp2_layer: str = "BOTTOM",
    origin_mils: tuple[float, float] = (0.0, 0.0),
    duplicate_alignment_designator: bool = False,
) -> Path:
    from altium_monkey import AltiumPcbDoc, PadShape, PcbLayer

    tp2_pcb_layer = PcbLayer.TOP if tp2_layer.upper() == "TOP" else PcbLayer.BOTTOM
    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(0, 0, 1400, 900)
    pcbdoc.set_origin_mils(*origin_mils)
    pcbdoc.add_component(
        designator="TP1",
        footprint="TEST_POINT_2MM",
        position_mils=(200, 300),
        layer="BOTTOM",
    )
    tp1_pad = pcbdoc.add_pad(
        designator="1",
        position_mils=(200, 300),
        width_mils=80,
        height_mils=80,
        layer=PcbLayer.BOTTOM,
        shape=PadShape.CIRCLE,
        net="+VIN",
    )
    tp1_pad.component_index = 0
    pcbdoc.add_component(
        designator="TP2",
        footprint="TEST_POINT_2MM",
        position_mils=(250, 350),
        layer=tp2_layer,
    )
    tp2_pad = pcbdoc.add_pad(
        designator="1",
        position_mils=(250, 350),
        width_mils=80,
        height_mils=80,
        layer=tp2_pcb_layer,
        shape=PadShape.CIRCLE,
        net="I2C-SDA",
    )
    tp2_pad.component_index = 1
    pcbdoc.add_component(
        designator="M1",
        footprint="MOUNT_2_5",
        position_mils=(400, 500),
        layer="BOTTOM",
    )
    pcbdoc.add_component(
        designator="R1",
        footprint="R0603",
        position_mils=(600, 500),
        layer="BOTTOM",
    )
    pcbdoc.add_pad(
        designator="A1",
        position_mils=(1000, 500),
        width_mils=100,
        height_mils=100,
        layer=PcbLayer.MULTI_LAYER,
        shape=PadShape.CIRCLE,
        hole_size_mils=80,
        plated=False,
        net="ALIGN_NET",
    )
    if duplicate_alignment_designator:
        pcbdoc.add_pad(
            designator="A1",
            position_mils=(1100, 550),
            width_mils=100,
            height_mils=100,
            layer=PcbLayer.MULTI_LAYER,
            shape=PadShape.CIRCLE,
            hole_size_mils=80,
            plated=False,
            net="ALIGN_NET_2",
        )
    pcbdoc.add_pad(
        designator="B1",
        position_mils=(1200, 500),
        width_mils=60,
        height_mils=60,
        layer=PcbLayer.MULTI_LAYER,
        shape=PadShape.CIRCLE,
        hole_size_mils=40,
        plated=False,
        net="SMALL_NPTH",
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    pcbdoc.save(path)
    return path


def test_debug_plate_template_builds_initial_mco(tmp_path: Path) -> None:
    config_path = tmp_path / "debug-plate.jsonc"
    write_debug_plate_config_template(config_path)

    config = load_debug_plate_config(config_path)
    payload = build_debug_plate_mco(config)

    assert payload["schema"] == MCO_SCHEMA
    operations = payload["operations"]
    assert isinstance(operations, list)
    assert [operation["op"] for operation in operations] == [
        "project.create-skeleton",
        "pcbdoc.add-text",
    ]
    assert operations[0]["args"]["schematic_sheet_style"] == "D"
    assert operations[1]["args"]["file"] == "output/debug-plate/debug_plate.PcbDoc"


def test_debug_plate_run_creates_project_and_marker(tmp_path: Path) -> None:
    config_path = tmp_path / "debug-plate.jsonc"
    config_path.write_text(
        json.dumps(
            {
                "schema": DEBUG_PLATE_CONFIG_SCHEMA,
                "output": {
                    "output_dir": "generated",
                    "project_name": "debug_plate",
                    "overwrite": True,
                },
                "marker": {
                    "text": "CRICKET DEBUG",
                    "position_mils": [250, 300],
                    "height_mils": 75,
                },
            }
        ),
        encoding="utf-8",
    )

    result = execute_debug_plate_config(config_path)

    assert result.ok is True
    assert (tmp_path / "generated" / "debug_plate.PrjPcb").exists()
    assert (tmp_path / "generated" / "debug_plate.SchDoc").exists()

    from altium_monkey import AltiumPcbDoc

    pcbdoc = AltiumPcbDoc.from_file(tmp_path / "generated" / "debug_plate.PcbDoc")
    assert [text.text_content for text in pcbdoc.texts] == ["CRICKET DEBUG"]


def test_debug_plate_inspection_classifies_components_and_free_pads() -> None:
    from altium_monkey import AltiumPcbDoc, PadShape, PcbLayer
    from altium_monkey.altium_pcb_component import AltiumPcbComponent

    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(0, 0, 1000, 700)
    pcbdoc.set_origin_mils(1000, 2000)
    pcbdoc.add_pad(
        designator="A1",
        position_mils=(100, 120),
        width_mils=80,
        height_mils=80,
        layer=PcbLayer.MULTI_LAYER,
        shape=PadShape.CIRCLE,
        hole_size_mils=40,
        plated=False,
        net="ALIGN_NET",
    )
    pcbdoc.components.append(
        AltiumPcbComponent(
            designator="TP1",
            footprint="TEST_POINT",
            layer="BOTTOM",
            x="250mil",
            y="300mil",
        )
    )
    tp_pad = pcbdoc.add_pad(
        designator="1",
        position_mils=(250, 300),
        width_mils=80,
        height_mils=80,
        layer=PcbLayer.BOTTOM,
        shape=PadShape.CIRCLE,
        net="TP_NET",
    )
    tp_pad.component_index = 0
    pcbdoc.components.append(
        AltiumPcbComponent(
            designator="MH1",
            footprint="MOUNT_2_5",
            layer="TOP",
            x="400mil",
            y="500mil",
        )
    )
    pcbdoc.components.append(
        AltiumPcbComponent(
            designator="R1",
            footprint="R0603",
            layer="TOP",
            x="600mil",
            y="500mil",
        )
    )

    inspection = inspect_pcbdoc_for_debug_plate("fixture", pcbdoc, "fixture.PcbDoc")
    payload = inspection.to_dict()

    assert [item["designator"] for item in payload["components"]] == ["TP1", "MH1"]
    assert [item["kind"] for item in payload["components"]] == [
        "test_point",
        "mount",
    ]
    assert payload["components"][0]["net_name"] == "TP_NET"
    assert payload["board_outline_mils"] == {
        "left": 0.0,
        "bottom": 0.0,
        "right": 1000.0,
        "top": 700.0,
    }
    assert payload["board_origin_mils"] == {"x": 1000.0, "y": 2000.0}
    assert payload["components"][0]["source_pad_geometries"] == [
        {
            "x_mils": 250.0,
            "y_mils": 300.0,
            "width_mils": 80.0,
            "height_mils": 80.0,
            "shape": 1,
            "layer": 32,
            "rotation_degrees": 0.0,
        }
    ]
    assert payload["free_pads"][0]["kind"] == "free_npth"
    assert payload["free_pads"][0]["hole_size_mils"] == 40.0
    assert payload["free_pads"][0]["net_name"] == "ALIGN_NET"


def test_debug_plate_inspection_preserves_board_cutout_geometry() -> None:
    from altium_monkey import AltiumPcbDoc

    source_path = (
        PACKAGE_ROOT
        / "tests"
        / "assets"
        / "projects"
        / "cricket-node"
        / "input"
        / "cricket-node-hw__B.PcbDoc"
    )
    pcbdoc = AltiumPcbDoc.from_file(source_path)

    inspection = inspect_pcbdoc_for_debug_plate("cricket", pcbdoc, source_path)
    payload = inspection.to_dict()
    cutouts = payload["board_outline"]["cutouts"]

    assert len(cutouts) == 1
    assert len(cutouts[0]["vertices"]) >= 3
    assert any(vertex["segment"] == "arc" for vertex in cutouts[0]["vertices"])


def test_debug_plate_known_parts_manifest_tracks_node_test_array_roles(
    tmp_path: Path,
) -> None:
    cache_dir = tmp_path / "cache"
    for relative_path in [
        "schlib/YZ209315103P-01.SchLib",
        "pcblib/split/YZ209315103P-01.PcbLib",
        "schlib/9774080360R.SchLib",
        "pcblib/split/9774080360R-YIYUAN.PcbLib",
        "schlib/H2184-05.SchLib",
        "pcblib/split/H2184-05.PcbLib",
    ]:
        output_path = cache_dir / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(b"fixture")

    payload = build_node_test_array_parts_manifest(
        tmp_path / "node-test-array.PrjPcb",
        cache_dir,
    )
    manifest_path = write_debug_plate_known_parts_manifest(
        payload,
        cache_dir / DEBUG_PLATE_PARTS_CACHE_FILENAME,
    )

    loaded = load_debug_plate_known_parts_manifest(manifest_path)
    assert manifest_path_for_cache_dir(cache_dir) == manifest_path
    assert [part["role"] for part in loaded["parts"]] == [
        "test_point_pogo",
        "m25_smt_standoff",
        "alignment_pin_2mm_npth",
    ]
    assert resolve_known_part(loaded, "test_point")["footprint_name"] == (
        "YZ209315103P-01"
    )
    assert resolve_known_part(
        loaded,
        "TEST_POINT",
        role="test_point_pogo",
    )["footprint_name"] == "YZ209315103P-01"
    assert resolve_known_part(loaded, "test_point")["signal_pad_designator"] == "1"
    assert resolve_known_part(loaded, "mount")["symbol_name"] == "9774080360R"
    assert resolve_known_part(loaded, "mount")["signal_pad_designator"] is None
    assert resolve_known_part(loaded, "free_npth")["footprint_name"] == "H2184-05"
    assert loaded["designator_normalization"]["mount"]["M5"] == "M1"


def test_debug_plate_mco_places_known_parts_from_selection(tmp_path: Path) -> None:
    manifest_path = _write_minimal_known_part_cache(tmp_path)

    config = load_debug_plate_config(
        _write_json(
            tmp_path / "debug-plate.jsonc",
            {
                "schema": DEBUG_PLATE_CONFIG_SCHEMA,
                "output": {
                    "output_dir": "generated",
                    "project_name": "debug_plate",
                    "overwrite": True,
                },
                "known_parts": {
                    "manifest": str(manifest_path),
                },
                "placement": {
                    "source_mount_side": "bottom",
                    "offset_mils": [10, 20],
                    "mirror_x": True,
                    "mirror_y": False,
                    "mirror_origin_mils": [1000, 0],
                },
                "pcb_labels": {
                    "enabled": True,
                    "side": "right",
                    "offset_mils": [120, 0],
                    "box_size_mils": [450, 70],
                    "center_box_on_target": True,
                },
                "marker": {"enabled": False},
                "selection": {
                    "boards": [
                        {
                            "board_key": "fixture",
                            "components": [
                                {
                                    "designator": "M5",
                                    "kind": "mount",
                                    "footprint": "M2.5",
                                    "layer": "TOP",
                                    "x_mils": 100,
                                    "y_mils": 200,
                                }
                            ],
                            "free_pads": [
                                {
                                    "designator": "G1",
                                    "kind": "free_npth",
                                    "net_name": "ALIGN_NET",
                                    "x_mils": 300,
                                    "y_mils": 400,
                                }
                            ],
                        }
                    ]
                },
            },
        )
    )

    payload = build_debug_plate_mco(config)
    operations = payload["operations"]

    assert [operation["op"] for operation in operations[:5]] == [
        "project.create-skeleton",
        "file.copy",
        "file.copy",
        "file.copy",
        "file.copy",
    ]
    assert operations[0]["args"]["documents"] == [
        "libraries/pcblib/split/9774080360R-YIYUAN.PcbLib",
        "libraries/pcblib/split/H2184-05.PcbLib",
        "libraries/schlib/9774080360R.SchLib",
        "libraries/schlib/H2184-05.SchLib",
    ]
    assert [operation["op"] for operation in operations[5:]] == [
        "schdoc.add-component",
        "pcbdoc.add-component",
        "schdoc.add-component",
        "schdoc.add-wire",
        "schdoc.add-net-label",
        "pcbdoc.add-component",
        "pcbdoc.create-user-union",
        "pcbdoc.add-text",
    ]
    assert operations[5]["args"]["designator"] == "M1"
    assert operations[5]["args"]["symbol"] == "9774080360R"
    assert operations[5]["args"]["library"] == (
        "generated/libraries/schlib/9774080360R.SchLib"
    )
    assert operations[6]["args"]["footprint"] == "9774080360R-YIYUAN"
    assert operations[6]["args"]["library"] == (
        "generated/libraries/pcblib/split/9774080360R-YIYUAN.PcbLib"
    )
    assert operations[6]["args"]["position_mils"] == [1910.0, 220.0]
    assert operations[7]["args"]["designator"] == "P1"
    assert operations[7]["args"]["parameters"]["DebugPlateSourceNet"] == "ALIGN_NET"
    assert operations[8]["args"]["points_mils"] == [[2700.0, 1080.0], [2700.0, 730.0]]
    assert operations[9]["args"]["text"] == "ALIGN_NET"
    assert operations[9]["args"]["location_mils"] == [2700.0, 900.0]
    assert operations[10]["args"]["footprint"] == "H2184-05"
    assert operations[10]["args"]["position_mils"] == [1710.0, 420.0]
    assert operations[10]["args"]["pad_nets"] == {"1": "ALIGN_NET"}
    assert operations[11]["args"]["name"] == "DEBUG_PLATE_FEATURES"
    assert operations[12]["args"]["text"] == "ALIGN_NET"
    assert operations[12]["args"]["position_mils"] == [1830.0, 385.0]
    assert operations[12]["args"]["height_mils"] == 65.0
    assert operations[12]["args"]["layer"] == "TOP_OVERLAY"
    assert operations[12]["args"]["font_kind"] == "truetype"
    assert operations[12]["args"]["font_name"] == "Arial"
    assert operations[12]["args"]["bold"] is True
    assert operations[12]["args"]["is_inverted"] is True
    assert operations[12]["args"]["inverted_rectangle_size_mils"] == [450.0, 70.0]
    assert operations[12]["args"]["frame_size_mils"] == [450.0, 70.0]
    assert operations[12]["args"]["text_justification"] == "RIGHT_TOP"


def test_cricket_node_debug_plate_example_config_is_planable() -> None:
    example_config = (
        PACKAGE_ROOT
        / "examples"
        / "debug-plate"
        / "cricket-node"
        / "debug-plate.jsonc"
    )

    payload = build_debug_plate_mco(load_debug_plate_config(example_config))
    operations = payload["operations"]

    assert payload["schema"] == MCO_SCHEMA
    assert [operation["op"] for operation in operations] == [
        "project.create-skeleton",
        "file.copy",
        "file.copy",
        "file.copy",
        "file.copy",
        "file.copy",
        "file.copy",
        "schdoc.add-component",
        "schdoc.add-wire",
        "schdoc.add-net-label",
        "pcbdoc.add-component",
        "schdoc.add-component",
        "pcbdoc.add-component",
        "schdoc.add-component",
        "schdoc.add-wire",
        "schdoc.add-net-label",
        "pcbdoc.add-component",
        "pcbdoc.create-user-union",
        "pcbdoc.add-text",
        "pcbdoc.add-text",
    ]
    assert operations[0]["args"]["documents"] == [
        "libraries/pcblib/split/9774080360R-YIYUAN.PcbLib",
        "libraries/pcblib/split/H2184-05.PcbLib",
        "libraries/pcblib/split/YZ209315103P-01.PcbLib",
        "libraries/schlib/9774080360R.SchLib",
        "libraries/schlib/H2184-05.SchLib",
        "libraries/schlib/YZ209315103P-01.SchLib",
    ]
    assert [operation["args"].get("designator") for operation in operations] == [
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        "TP1",
        None,
        None,
        "TP1",
        "M1",
        "M1",
        "P1",
        None,
        None,
        "P1",
        None,
        None,
        None,
    ]
    assert operations[8]["args"]["points_mils"] == [[1300.0, 1200.0], [1650.0, 1200.0]]
    assert operations[9]["args"]["location_mils"] == [1480.0, 1200.0]
    assert operations[14]["args"]["points_mils"] == [[4200.0, 1080.0], [4200.0, 730.0]]
    assert operations[15]["args"]["location_mils"] == [4200.0, 900.0]
    assert [
        operation["args"].get("text")
        for operation in operations
        if operation["op"] in {"schdoc.add-net-label", "pcbdoc.add-text"}
    ] == ["+VIN", "ALIGN_NET", "+VIN", "ALIGN_NET"]
    assert operations[-3]["args"]["name"] == "DEBUG_PLATE_FEATURES"


def test_cricket_node_draft_mate_config_is_parseable() -> None:
    draft_config = (
        PACKAGE_ROOT
        / "examples"
        / "debug-plate"
        / "cricket-node"
        / "debug-plate.mate.a0.jsonc"
    )

    payload = load_jsonc_file(draft_config)

    assert isinstance(payload, dict)
    assert payload["schema"] == MATE_CONFIG_SCHEMA
    assert payload["source"]["board"] == (
        "input/cricket-node/11-10028__cricket-node-hw__B.PrjPcb"
    )
    assert payload["output"]["backend"] == "altium"
    assert payload["output"]["board_outline"] == {
        "mode": "source_bounds_with_margin",
        "margin_mils": {
            "left": 500,
            "bottom": 500,
            "right": 3000,
            "top": 500,
        },
    }
    assert [projection["id"] for projection in payload["projections"]] == [
        "test_points",
        "mounts",
        "alignment_pins",
    ]
    projections = {projection["id"]: projection for projection in payload["projections"]}
    assert projections["test_points"]["source"]["designators"] == "TP1-27"
    assert projections["mounts"]["source"]["designators"] == "M1-4"
    assert "kind" not in projections["alignment_pins"]["source"]
    assert payload["board_projection"]["outline"]["graphics"]["layer"] == "TOP_OVERLAY"
    assert payload["board_projection"]["cutouts"]["graphics"] == {
        "enabled": True,
        "layer": "MECHANICAL_1",
        "stroke_width_mils": 8,
    }
    assert payload["board_projection"]["cutouts"]["actual_cutouts"] is True
    assert payload["artifacts"]["pcb_layer_step"]["source_layer"] == "bottom"
    assert payload["artifacts"]["pcb_layer_step"]["z_mm"] == -0.0175
    assert payload["artifacts"]["pcb_layer_step"]["features"]["tracks"] == {
        "enabled": True,
        "color": "#B87333",
    }
    assert payload["artifacts"]["pcb_layer_step"]["features"]["polygons"] == {
        "enabled": True,
        "color": "#7A8F2A",
    }
    assert payload["artifacts"]["pcb_layer_step"]["insert_in_output"]["z_mm"] == 8.5
    assert projections["test_points"]["actions"][1]["style"]["mode"] == "outline"
    assert projections["test_points"]["actions"][1]["style"]["outline_count"] == 1
    test_point_label = projections["test_points"]["actions"][2]
    assert test_point_label["placement"]["side"] == "board_right"
    assert projections["mounts"]["actions"][1]["kind"] == "reference_graphics"
    assert projections["alignment_pins"]["actions"][1]["kind"] == "reference_graphics"
    assert payload["pcb_designators"]["style"]["height_mils"] == 40
    assert payload["pcb_designators"]["style"]["font_name"] == "Arial"


def test_debug_plate_mate_seed_config_uses_selectors(tmp_path: Path) -> None:
    source_path = _write_mate_source_pcbdoc(tmp_path / "dut.PcbDoc")
    manifest_path = tmp_path / "known-parts" / "debug-plate-known-parts.json"

    payload = build_debug_plate_mate_seed_config(
        source_path,
        known_parts_manifest=manifest_path,
        project_context="none",
    )

    assert payload["schema"] == MATE_CONFIG_SCHEMA
    assert payload["source"]["board"] == str(source_path.resolve())
    assert payload["source"]["project_context"] == "none"
    assert payload["output"]["origin"] == "preserve_source"
    assert payload["output"]["board_outline"] == {
        "mode": "source_bounds_with_margin",
        "margin_mils": 250.0,
    }
    assert payload["known_parts"]["manifest"] == str(manifest_path)
    projections = {projection["id"]: projection for projection in payload["projections"]}
    assert projections["test_points"]["source"] == {
        "object": "component",
        "designators": "TP1-2",
    }
    assert projections["test_points"]["actions"][0] == {
        "kind": "mate_component",
        "part": "test_point_pogo",
    }
    assert projections["mounts"]["source"] == {
        "object": "component",
        "designators": "M1",
    }
    assert projections["alignment_pins"]["source"] == {
        "object": "free_pad",
        "hole_size_mils": {"min": 75, "max": 85},
        "plated": False,
    }
    assert payload["board_projection"]["outline"]["graphics"] == {
        "enabled": True,
        "layer": "TOP_OVERLAY",
        "stroke_width_mils": 8,
    }
    assert payload["board_projection"]["cutouts"] == {
        "graphics": {
            "enabled": True,
            "layer": "MECHANICAL_1",
            "stroke_width_mils": 8,
        },
        "actual_cutouts": False,
    }
    assert payload["validation"]["source_side"] == "infer_single_side"
    assert payload["validation"]["side_agnostic_kinds"] == ["mount"]
    assert payload["artifacts"]["pcb_layer_step"]["highlights"] == [
        {"projection": "test_points", "color": "#FF0000"}
    ]
    assert payload["artifacts"]["pcb_layer_step"]["features"]["tracks"]["enabled"] is True
    assert payload["artifacts"]["pcb_layer_step"]["features"]["polygons"]["enabled"] is True
    assert payload["artifacts"]["pcb_layer_step"]["insert_in_output"]["z_mm"] == 8.5
    assert payload["projections"][0]["actions"][1] == {
        "kind": "reference_graphics",
        "shape": "source_pad_outline",
        "layer": "MECHANICAL_1",
        "style": {
            "mode": "outline",
            "outline_count": 1,
            "clearance_mils": 10,
            "stroke_width_mils": 10,
        },
    }
    assert payload["projections"][0]["actions"][2]["placement"]["side"] == "board_right"
    assert payload["projections"][1]["actions"][1]["kind"] == "reference_graphics"
    assert payload["projections"][2]["actions"][1]["kind"] == "reference_graphics"
    assert payload["pcb_designators"]["style"]["height_mils"] == 40


def test_debug_plate_reference_graphics_trace_pad_shape() -> None:
    circle_ops = build_pcb_reference_graphics_operations(
        output_dir="generated",
        board_filename="debug_plate.PcbDoc",
        designator="TP1",
        target={
            "mate_reference_graphics": {
                "shape": "source_pad_outline",
                "layer": "MECHANICAL_1",
                "style": {"clearance_mils": 5, "stroke_width_mils": 3},
            },
            "source_pad_geometries": [
                {
                    "x_mils": 100,
                    "y_mils": 200,
                    "width_mils": 80,
                    "height_mils": 80,
                    "shape": 1,
                }
            ],
        },
    )

    assert len(circle_ops) == 1
    assert circle_ops[0]["op"] == "pcbdoc.add-arc"
    assert circle_ops[0]["args"]["center_mils"] == [100.0, 200.0]
    assert circle_ops[0]["args"]["radius_mils"] == 46.5

    touching_ops = build_pcb_reference_graphics_operations(
        output_dir="generated",
        board_filename="debug_plate.PcbDoc",
        designator="TP2",
        target={
            "mate_reference_graphics": {
                "shape": "source_pad_outline",
                "layer": "MECHANICAL_1",
                "style": {"clearance_mils": 0, "stroke_width_mils": 10},
            },
            "source_pad_geometries": [
                {
                    "x_mils": 100,
                    "y_mils": 200,
                    "width_mils": 80,
                    "height_mils": 80,
                    "shape": 1,
                }
            ],
        },
    )
    assert touching_ops[0]["args"]["radius_mils"] == 45.0

    rectangle_ops = build_pcb_reference_graphics_operations(
        output_dir="generated",
        board_filename="debug_plate.PcbDoc",
        designator="U1",
        target={
            "mate_reference_graphics": {
                "shape": "source_pad_outline",
                "layer": "MECHANICAL_1",
                "style": {
                    "mode": "double_outline",
                    "clearance_mils": 5,
                    "outline_spacing_mils": 10,
                    "stroke_width_mils": 3,
                },
            },
            "source_pad_geometries": [
                {
                    "x_mils": 100,
                    "y_mils": 200,
                    "width_mils": 80,
                    "height_mils": 40,
                    "shape": 2,
                    "rotation_degrees": 0,
                }
            ],
        },
    )

    assert [operation["op"] for operation in rectangle_ops] == ["pcbdoc.add-track"] * 8
    assert rectangle_ops[0]["args"]["start_mils"] == [53.5, 173.5]
    assert rectangle_ops[0]["args"]["end_mils"] == [146.5, 173.5]
    assert rectangle_ops[4]["args"]["start_mils"] == [43.5, 163.5]
    assert rectangle_ops[4]["args"]["end_mils"] == [156.5, 163.5]
    assert {operation["args"]["width_mils"] for operation in rectangle_ops} == {3.0}


def test_debug_plate_board_projection_projects_cutout_graphics_and_regions() -> None:
    selection = SimpleNamespace(
        boards=(
            SimpleNamespace(
                board_key="dut",
                board_outline={
                    "vertices": [
                        {"x_mils": 0, "y_mils": 0},
                        {"x_mils": 1000, "y_mils": 0},
                        {"x_mils": 1000, "y_mils": 700},
                        {"x_mils": 0, "y_mils": 700},
                    ],
                    "cutouts": [
                        {
                            "vertices": [
                                {"x_mils": 100, "y_mils": 100},
                                {"x_mils": 250, "y_mils": 100},
                                {"x_mils": 250, "y_mils": 220},
                                {"x_mils": 100, "y_mils": 220},
                            ]
                        }
                    ],
                },
            ),
        )
    )

    operations = build_pcb_board_projection_operations(
        output_dir="generated",
        board_filename="debug_plate.PcbDoc",
        board_projection={
            "cutouts": {
                "graphics": {
                    "enabled": True,
                    "layer": "MECHANICAL_1",
                    "stroke_width_mils": 6,
                },
                "actual_cutouts": True,
            }
        },
        selection=selection,
    )

    cutout_tracks = [
        operation for operation in operations if operation["op"] == "pcbdoc.add-track"
    ]
    cutout_regions = [
        operation for operation in operations if operation["op"] == "pcbdoc.add-region"
    ]
    assert len(cutout_tracks) == 4
    assert len(cutout_regions) == 1
    assert {operation["args"]["layer"] for operation in cutout_tracks} == {
        "MECHANICAL_1"
    }
    assert {operation["args"]["width_mils"] for operation in cutout_tracks} == {6.0}
    assert cutout_regions[0]["args"]["layer"] == "MULTI_LAYER"
    assert cutout_regions[0]["args"]["is_board_cutout"] is True
    assert cutout_regions[0]["args"]["outline_points_mils"] == [
        [100.0, 100.0],
        [250.0, 100.0],
        [250.0, 220.0],
        [100.0, 220.0],
    ]


def test_debug_plate_mate_output_board_outline_modes(tmp_path: Path) -> None:
    source_path = _write_mate_source_pcbdoc(tmp_path / "dut.PcbDoc")

    def first_outline(output: object) -> object:
        config_path = _write_json(
            tmp_path / "debug-plate.mate.a0.jsonc",
            {
                "schema": MATE_CONFIG_SCHEMA,
                "source": {"board": str(source_path), "project_context": "none"},
                "output": output,
            },
        )
        config = load_debug_plate_config(config_path)
        return build_debug_plate_mco(config)["operations"][0]["args"].get(
            "board_outline_mils"
        )

    assert first_outline(
        {
            "origin": "preserve_source",
            "board_outline": {"mode": "source_bounds"},
        }
    ) == {
        "left": 0.0,
        "bottom": 0.0,
        "right": 1400.0,
        "top": 900.0,
    }
    assert first_outline(
        {
            "origin": "preserve_source",
            "board_outline": {
                "mode": "source_bounds_with_margin",
                "margin_mils": {
                    "left": 100,
                    "bottom": 200,
                    "right": 300,
                    "top": 400,
                },
            },
        }
    ) == {
        "left": -100.0,
        "bottom": -200.0,
        "right": 1700.0,
        "top": 1300.0,
    }
    with pytest.raises(ValueError, match="match_shape"):
        first_outline(
            {
                "origin": "preserve_source",
                "board_outline": {"mode": "match_shape"},
            }
        )


def test_debug_plate_mate_config_resolves_source_selectors(tmp_path: Path) -> None:
    source_path = _write_mate_source_pcbdoc(
        tmp_path / "dut.PcbDoc",
        origin_mils=(1000.0, 2000.0),
    )
    manifest_path = _write_minimal_known_part_cache(tmp_path)
    manifest_payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_payload["parts"].append(
        {
            "role": "alternate_test_point_pogo",
            "description": "Alternate pogo used to prove config role selection.",
            "symbol_name": "ALT_TEST_POINT",
            "symbol_library": "schlib/ALT_TEST_POINT.SchLib",
            "footprint_name": "ALT_TEST_POINT",
            "footprint_library": "pcblib/split/ALT_TEST_POINT.PcbLib",
            "target_kinds": ["test_point"],
            "designator_prefix": "X",
            "signal_pad_designator": "1",
        }
    )
    _write_json(manifest_path, manifest_payload)
    config_path = _write_json(
        tmp_path / "debug-plate.mate.a0.jsonc",
        {
            "schema": MATE_CONFIG_SCHEMA,
            "source": {
                "board": str(source_path),
                "project_context": "none",
            },
            "output": {
                "backend": "altium",
                "output_dir": "generated",
                "project_name": "debug_plate",
                "overwrite": True,
            },
            "known_parts": {
                "manifest": str(manifest_path),
            },
            "artifacts": {
                "pcb_layer_step": {
                    "enabled": True,
                    "source_layer": "bottom",
                    "insert_in_output": {
                        "enabled": True,
                        "z_mm": 8.5,
                        "layer": "MECHANICAL_13",
                    },
                    "features": {
                        "tracks": {"enabled": True, "color": "#B87333"},
                        "polygons": {"enabled": True, "color": "#7A8F2A"},
                    },
                    "highlights": [
                        {"projection": "test_points", "color": "#FF0000"},
                        {"projection": "alignment_pins", "color": "#44aaee"},
                    ],
                }
            },
            "board_projection": {
                "outline": {
                    "graphics": {
                        "enabled": True,
                        "layer": "TOP_OVERLAY",
                        "stroke_width_mils": 9,
                    }
                }
            },
            "projections": [
                {
                    "id": "test_points",
                    "source": {
                        "object": "component",
                        "designators": "TP1-2, U12",
                    },
                    "actions": [
                        {
                            "kind": "mate_component",
                            "part": "alternate_test_point_pogo",
                        },
                        {
                            "kind": "reference_graphics",
                            "shape": "source_pad_outline",
                            "layer": "MECHANICAL_1",
                            "style": {
                                "mode": "double_ring",
                                "clearance_mils": 10,
                                "stroke_width_mils": 4,
                            },
                        },
                        {
                            "kind": "label",
                            "value": "source_net",
                            "placement": {
                                "side": "right",
                                "offset_mils": [120, 0],
                                "box_size_mils": [450, 70],
                                "center_box_on_target": True,
                            },
                            "style": {
                                "height_mils": 50,
                                "text_justification": "RIGHT_TOP",
                            },
                        },
                    ],
                },
                {
                    "id": "mounts",
                    "source": {
                        "object": "component",
                        "designators": "M1",
                    },
                    "actions": [
                        {
                            "kind": "mate_component",
                            "part": "m25_smt_standoff",
                        }
                    ],
                },
                {
                    "id": "alignment_pins",
                    "source": {
                        "object": "free_pad",
                        "plated": False,
                        "hole_size_mils": {"min": 75, "max": 85},
                    },
                    "actions": [
                        {
                            "kind": "mate_component",
                            "part": "alignment_pin_2mm_npth",
                        },
                        {
                            "kind": "label",
                            "text": "source_net",
                            "placement": {
                                "side": "left",
                                "offset_mils": [90, 0],
                                "box_size_mils": [300, 60],
                                "center_box_on_target": True,
                            },
                            "style": {
                                "height_mils": 45,
                                "text_justification": "LEFT_TOP",
                            },
                        },
                    ],
                },
            ],
        },
    )

    config = load_debug_plate_config(config_path)
    board = config.selection.boards[0]

    assert [component.designator for component in board.components] == [
        "TP1",
        "TP2",
        "M1",
    ]
    assert [component.net_name for component in board.components] == [
        "+VIN",
        "I2C-SDA",
        None,
    ]
    assert [component.mate_part_role for component in board.components] == [
        "alternate_test_point_pogo",
        "alternate_test_point_pogo",
        "m25_smt_standoff",
    ]
    assert [component.mate_projection_id for component in board.components] == [
        "test_points",
        "test_points",
        "mounts",
    ]
    assert board.components[0].mate_pcb_label is not None
    assert [pad.designator for pad in board.free_pads] == ["A1"]
    assert board.free_pads[0].net_name == "ALIGN_NET"
    assert board.free_pads[0].mate_part_role == "alignment_pin_2mm_npth"
    assert board.free_pads[0].mate_projection_id == "alignment_pins"
    assert board.free_pads[0].mate_pcb_label is not None
    assert board.board_outline is not None
    assert len(board.board_outline["vertices"]) == 4
    assert config.pcb_labels.enabled is False

    payload = build_debug_plate_mco(config)
    operations = payload["operations"]
    assert operations[0]["args"]["board_outline_mils"] == {
        "left": -250.0,
        "bottom": -250.0,
        "right": 1650.0,
        "top": 1150.0,
    }
    assert operations[0]["args"]["board_origin_mils"] == {
        "x": 1000.0,
        "y": 2000.0,
    }
    pcb_components = [
        operation
        for operation in operations
        if operation["op"] == "pcbdoc.add-component"
    ]
    pcb_labels = [
        operation
        for operation in operations
        if operation["op"] == "pcbdoc.add-text"
    ]

    assert [operation["args"]["designator"] for operation in pcb_components] == [
        "TP1",
        "TP2",
        "M1",
        "P1",
    ]
    assert [operation["args"]["footprint"] for operation in pcb_components] == [
        "ALT_TEST_POINT",
        "ALT_TEST_POINT",
        "9774080360R-YIYUAN",
        "H2184-05",
    ]
    assert [operation["args"]["position_mils"] for operation in pcb_components] == [
        [200.0, 300.0],
        [250.0, 350.0],
        [400.0, 500.0],
        [1000.0, 500.0],
    ]
    assert [operation["args"]["text"] for operation in pcb_labels] == [
        "+VIN",
        "I2C-SDA",
        "ALIGN_NET",
    ]
    arrange_designators = [
        operation
        for operation in operations
        if operation["op"] == "pcbdoc.arrange-designators"
    ]
    assert len(arrange_designators) == 1
    assert arrange_designators[0]["args"]["designators"] == ["TP1", "TP2", "M1", "P1"]
    assert arrange_designators[0]["args"]["height_mils"] == 40.0
    assert arrange_designators[0]["args"]["font_name"] == "Arial"
    pcb_reference_arcs = [
        operation
        for operation in operations
        if operation["op"] == "pcbdoc.add-arc"
    ]
    assert [operation["args"]["center_mils"] for operation in pcb_reference_arcs] == [
        [200.0, 300.0],
        [200.0, 300.0],
        [250.0, 350.0],
        [250.0, 350.0],
        [1000.0, 500.0],
    ]
    assert [operation["args"]["radius_mils"] for operation in pcb_reference_arcs] == [
        52.0,
        62.0,
        52.0,
        62.0,
        65.0,
    ]
    assert {operation["args"]["layer"] for operation in pcb_reference_arcs} == {
        "MECHANICAL_1"
    }
    assert [operation["args"]["width_mils"] for operation in pcb_reference_arcs] == [
        4.0,
        4.0,
        4.0,
        4.0,
        10.0,
    ]
    outline_tracks = [
        operation
        for operation in operations
        if operation["op"] == "pcbdoc.add-track"
        and str(operation["id"]).startswith("project_dut_outline_segment")
    ]
    assert len(outline_tracks) == 4
    assert outline_tracks[0]["args"]["start_mils"] == [0.0, 0.0]
    assert outline_tracks[0]["args"]["end_mils"] == [1400.0, 0.0]
    assert {operation["args"]["layer"] for operation in outline_tracks} == {
        "TOP_OVERLAY"
    }
    assert {operation["args"]["width_mils"] for operation in outline_tracks} == {9.0}
    assert pcb_labels[0]["args"]["position_mils"] == [320.0, 265.0]
    assert pcb_labels[0]["args"]["height_mils"] == 50.0
    assert pcb_labels[0]["args"]["text_justification"] == "RIGHT_TOP"
    assert pcb_labels[-1]["args"]["position_mils"] == [610.0, 470.0]
    assert pcb_labels[-1]["args"]["height_mils"] == 45.0
    assert pcb_labels[-1]["args"]["text_justification"] == "LEFT_TOP"
    user_union = next(
        operation
        for operation in operations
        if operation["op"] == "pcbdoc.create-user-union"
    )
    assert user_union["op"] == "pcbdoc.create-user-union"
    assert user_union["args"]["name"] == "DEBUG_PLATE_FEATURES"
    step_op = [
        operation
        for operation in operations
        if operation["op"] == "pcbdoc.export-layer-step"
    ][0]
    assert step_op["op"] == "pcbdoc.export-layer-step"
    assert step_op["args"]["file"] == str(source_path)
    assert step_op["args"]["output_file"] == (
        "generated/artifacts/pcb-layer-step/dut__bottom.step"
    )
    assert step_op["args"]["layer"] == "bottom"
    assert [
        (highlight["id"], highlight["color"], len(highlight["pad_geometries"]))
        for highlight in step_op["args"]["highlights"]
    ] == [
        ("test_points", "#FF0000", 2),
        ("alignment_pins", "#44aaee", 1),
    ]
    assert step_op["args"]["z_mm"] == -0.0175
    assert step_op["args"]["features"]["tracks"] == {
        "enabled": True,
        "color": "#B87333",
    }
    assert step_op["args"]["features"]["polygons"] == {
        "enabled": True,
        "color": "#7A8F2A",
    }
    insert_step_op = next(
        operation
        for operation in operations
        if operation["op"] == "pcbdoc.add-embedded-3d-model"
    )
    assert insert_step_op["op"] == "pcbdoc.add-embedded-3d-model"
    assert insert_step_op["args"]["file"] == "generated/debug_plate.PcbDoc"
    assert insert_step_op["args"]["model_file"] == (
        "generated/artifacts/pcb-layer-step/dut__bottom.step"
    )
    assert insert_step_op["args"]["location_mils"] == [1000.0, 2000.0]
    assert insert_step_op["args"]["z_mm"] == 8.5
    assert insert_step_op["args"]["bounds_mils"] == {
        "left": 0.0,
        "bottom": 0.0,
        "right": 1400.0,
        "top": 900.0,
    }


def test_debug_plate_mate_config_keeps_duplicate_free_pad_designators(
    tmp_path: Path,
) -> None:
    source_path = _write_mate_source_pcbdoc(
        tmp_path / "dut.PcbDoc",
        duplicate_alignment_designator=True,
    )
    manifest_path = _write_minimal_known_part_cache(tmp_path)
    config_path = _write_json(
        tmp_path / "debug-plate.mate.a0.jsonc",
        {
            "schema": MATE_CONFIG_SCHEMA,
            "source": {
                "board": str(source_path),
                "project_context": "none",
            },
            "output": {
                "backend": "altium",
                "output_dir": "generated",
                "project_name": "debug_plate",
                "overwrite": True,
            },
            "known_parts": {
                "manifest": str(manifest_path),
            },
            "projections": [
                {
                    "id": "alignment_pins",
                    "source": {
                        "object": "free_pad",
                        "kind": "free_npth",
                        "hole_size_mils": {"min": 75, "max": 85},
                        "plated": False,
                    },
                    "actions": [
                        {
                            "kind": "mate_component",
                            "part": "alignment_pin_2mm_npth",
                        },
                    ],
                },
            ],
        },
    )

    config = load_debug_plate_config(config_path)
    board = config.selection.boards[0]

    assert [pad.designator for pad in board.free_pads] == ["A1", "A1"]
    payload = build_debug_plate_mco(config)
    pcb_components = [
        operation
        for operation in payload["operations"]
        if operation["op"] == "pcbdoc.add-component"
    ]
    assert [operation["args"]["designator"] for operation in pcb_components] == [
        "P1",
        "P2",
    ]
    assert [operation["args"]["position_mils"] for operation in pcb_components] == [
        [1000.0, 500.0],
        [1100.0, 550.0],
    ]


def test_debug_plate_mate_config_rejects_mixed_component_sides(
    tmp_path: Path,
) -> None:
    source_path = _write_mate_source_pcbdoc(
        tmp_path / "dut.PcbDoc",
        tp2_layer="TOP",
    )
    config_path = _write_json(
        tmp_path / "debug-plate.mate.a0.jsonc",
        {
            "schema": MATE_CONFIG_SCHEMA,
            "source": {
                "board": str(source_path),
                "project_context": "none",
            },
            "output": {
                "backend": "altium",
                "output_dir": "generated",
                "project_name": "debug_plate",
                "overwrite": True,
            },
            "validation": {
                "source_side": "infer_single_side",
            },
            "projections": [
                {
                    "id": "test_points",
                    "source": {
                        "object": "component",
                        "designators": "TP1-2",
                    },
                    "actions": [
                        {
                            "kind": "mate_component",
                            "part": "test_point_pogo",
                        }
                    ],
                }
            ],
        },
    )

    with pytest.raises(ValueError, match="mixes top and bottom"):
        load_debug_plate_config(config_path)


def test_debug_plate_seed_cli_can_write_mate_config(tmp_path: Path) -> None:
    source_path = _write_mate_source_pcbdoc(tmp_path / "dut.PcbDoc")
    seed_path = tmp_path / "debug-plate.mate.a0.jsonc"
    manifest_path = tmp_path / "known-parts" / "debug-plate-known-parts.json"

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "debug-plate",
            "seed",
            str(source_path),
            "--project-context",
            "none",
            "--mate-config",
            "--known-parts-manifest",
            str(manifest_path),
            "--config",
            str(seed_path),
        ],
        cwd=PACKAGE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(seed_path.read_text(encoding="utf-8"))
    assert payload["schema"] == MATE_CONFIG_SCHEMA
    assert payload["known_parts"]["manifest"] == str(manifest_path)
    assert [projection["id"] for projection in payload["projections"]] == [
        "test_points",
        "mounts",
        "alignment_pins",
    ]


def test_debug_plate_run_writes_known_part_and_pcb_label(tmp_path: Path) -> None:
    manifest_path = _write_minimal_known_part_cache(tmp_path)
    config_path = _write_json(
        tmp_path / "debug-plate.jsonc",
        {
            "schema": DEBUG_PLATE_CONFIG_SCHEMA,
            "output": {
                "output_dir": "generated",
                "project_name": "debug_plate",
                "overwrite": True,
            },
            "known_parts": {
                "manifest": str(manifest_path),
            },
            "placement": {
                "source_mount_side": "bottom",
                "offset_mils": [0, 0],
                "mirror_x": False,
                "mirror_y": False,
                "mirror_origin_mils": [0, 0],
            },
            "pcb_labels": {
                "enabled": True,
                "side": "right",
                "offset_mils": [100, 0],
                "box_size_mils": [300, 60],
                "center_box_on_target": True,
                "style": {
                    "height_mils": 50,
                    "text_justification": "RIGHT_TOP",
                },
            },
            "marker": {"enabled": False},
            "selection": {
                "boards": [
                    {
                        "board_key": "fixture",
                        "components": [
                            {
                                "designator": "TP1",
                                "kind": "test_point",
                                "footprint": "TEST_POINT",
                                "layer": "BOTTOM",
                                "net_name": "+VIN",
                                "x_mils": 200,
                                "y_mils": 300,
                            },
                            {
                                "designator": "M5",
                                "kind": "mount",
                                "footprint": "M2.5",
                                "layer": "TOP",
                                "x_mils": 400,
                                "y_mils": 500,
                            },
                        ],
                        "free_pads": [
                            {
                                "designator": "G1",
                                "kind": "free_npth",
                                "net_name": "ALIGN_NET",
                                "x_mils": 1000,
                                "y_mils": 500,
                            }
                        ],
                    }
                ]
            },
        },
    )

    result = execute_debug_plate_config(config_path)

    assert result.ok is True

    from altium_monkey import AltiumPcbDoc, AltiumSchDoc, PcbTextJustification
    from altium_monkey.altium_record_sch__sheet import SheetStyle
    from altium_monkey.altium_record_sch__designator import AltiumSchDesignator

    schdoc = AltiumSchDoc(tmp_path / "generated" / "debug_plate.SchDoc")
    pcbdoc = AltiumPcbDoc.from_file(tmp_path / "generated" / "debug_plate.PcbDoc")
    assert schdoc.sheet is not None
    assert schdoc.sheet.sheet_style == SheetStyle.D
    schematic_designators = [
        parameter.text
        for component in schdoc.components
        for parameter in component.parameters
        if isinstance(parameter, AltiumSchDesignator)
    ]
    assert schematic_designators == ["TP1", "M1", "P1"]
    assert [label.text for label in schdoc.net_labels] == ["+VIN", "ALIGN_NET"]
    assert [
        [(point.x_mils, point.y_mils) for point in wire.points_mils]
        for wire in schdoc.wires
    ] == [
        [(1300.0, 1200.0), (1650.0, 1200.0)],
        [(4200.0, 1080.0), (4200.0, 730.0)],
    ]
    assert [component.designator for component in pcbdoc.components] == [
        "TP1",
        "M1",
        "P1",
    ]
    sch_ids_by_designator = {
        parameter.text: component.unique_id
        for component in schdoc.components
        for parameter in component.parameters
        if isinstance(parameter, AltiumSchDesignator)
    }
    pcb_components_by_designator = {
        component.designator: component for component in pcbdoc.components
    }
    assert pcb_components_by_designator["TP1"].source_unique_id == (
        f"\\{sch_ids_by_designator['TP1']}"
    )
    assert pcb_components_by_designator["TP1"].source_hierarchical_path == "debug_plate"
    assert pcb_components_by_designator["TP1"].source_component_library == (
        "YZ209315103P-01.SchLib"
    )
    assert pcb_components_by_designator["TP1"].source_lib_reference == "YZ209315103P-01"
    assert pcb_components_by_designator["M1"].channel_offset == 0
    assert pcb_components_by_designator["P1"].channel_offset == 1
    assert pcb_components_by_designator["TP1"].channel_offset == 2
    labels_by_text = {
        text.text_content: text
        for text in pcbdoc.texts
        if text.text_content in {"+VIN", "ALIGN_NET"}
    }
    assert sorted(labels_by_text) == ["+VIN", "ALIGN_NET"]
    assert labels_by_text["+VIN"].x_mils == 300.0
    assert labels_by_text["+VIN"].y_mils == 270.0
    label = labels_by_text["ALIGN_NET"]
    assert label.x_mils == 1100.0
    assert label.y_mils == 470.0
    for label in labels_by_text.values():
        assert label.height_mils == 50.0
        assert label.is_inverted is True
        assert label.use_inverted_rectangle is True
        assert label.is_frame is True
        assert label.textbox_rect_width_mils == 300.0
        assert label.textbox_rect_height_mils == 60.0
        assert label.textbox_rect_justification == PcbTextJustification.RIGHT_TOP
        assert label.union_index == 0xFFFFFFFF
    assert [user_union.name for user_union in pcbdoc.user_unions] == [
        "DEBUG_PLATE_FEATURES"
    ]


def test_debug_plate_left_side_pcb_labels_default_left_justified(
    tmp_path: Path,
) -> None:
    manifest_path = _write_minimal_known_part_cache(tmp_path)
    config = load_debug_plate_config(
        _write_json(
            tmp_path / "debug-plate.jsonc",
            {
                "schema": DEBUG_PLATE_CONFIG_SCHEMA,
                "output": {
                    "output_dir": "generated",
                    "project_name": "debug_plate",
                    "overwrite": True,
                },
                "known_parts": {
                    "manifest": str(manifest_path),
                },
                "placement": {
                    "source_mount_side": "bottom",
                    "offset_mils": [0, 0],
                    "mirror_x": False,
                    "mirror_y": False,
                    "mirror_origin_mils": [0, 0],
                },
                "pcb_labels": {
                    "enabled": True,
                    "side": "left",
                    "offset_mils": [140, 0],
                    "box_size_mils": [300, 60],
                    "center_box_on_target": True,
                },
                "marker": {"enabled": False},
                "selection": {
                    "boards": [
                        {
                            "board_key": "fixture",
                            "free_pads": [
                                {
                                    "designator": "G1",
                                    "kind": "free_npth",
                                    "net_name": "ALIGN_NET",
                                    "x_mils": 1000,
                                    "y_mils": 500,
                                }
                            ],
                        }
                    ]
                },
            },
        )
    )

    payload = build_debug_plate_mco(config)
    label_op = next(
        operation
        for operation in payload["operations"]
        if operation["op"] == "pcbdoc.add-text"
    )

    assert label_op["args"]["text"] == "ALIGN_NET"
    assert label_op["args"]["position_mils"] == [560.0, 470.0]
    assert label_op["args"]["text_justification"] == "LEFT_TOP"


def test_debug_plate_board_edge_pcb_labels_stack_in_column(
    tmp_path: Path,
) -> None:
    manifest_path = _write_minimal_known_part_cache(tmp_path)
    config = load_debug_plate_config(
        _write_json(
            tmp_path / "debug-plate.jsonc",
            {
                "schema": DEBUG_PLATE_CONFIG_SCHEMA,
                "output": {
                    "output_dir": "generated",
                    "project_name": "debug_plate",
                    "overwrite": True,
                    "board_outline_mils": {
                        "left": 0,
                        "bottom": 0,
                        "right": 2000,
                        "top": 1000,
                    },
                },
                "known_parts": {
                    "manifest": str(manifest_path),
                },
                "placement": {
                    "source_mount_side": "bottom",
                    "offset_mils": [0, 0],
                    "mirror_x": False,
                    "mirror_y": False,
                    "mirror_origin_mils": [0, 0],
                },
                "pcb_labels": {
                    "enabled": True,
                    "side": "board_right",
                    "offset_mils": [100, 50],
                    "box_size_mils": [300, 60],
                    "row_spacing_mils": 80,
                },
                "marker": {"enabled": False},
                "selection": {
                    "boards": [
                        {
                            "board_key": "fixture",
                            "components": [
                                {
                                    "designator": "TP1",
                                    "kind": "test_point",
                                    "footprint": "TEST_POINT",
                                    "layer": "BOTTOM",
                                    "net_name": "LONG_NET_NAME",
                                    "x_mils": 200,
                                    "y_mils": 300,
                                }
                            ],
                            "free_pads": [
                                {
                                    "designator": "G1",
                                    "kind": "free_npth",
                                    "net_name": "NET_A",
                                    "x_mils": 1000,
                                    "y_mils": 500,
                                },
                                {
                                    "designator": "G2",
                                    "kind": "free_npth",
                                    "net_name": "NET_B",
                                    "x_mils": 1100,
                                    "y_mils": 600,
                                },
                            ],
                        }
                    ]
                },
            },
        )
    )

    payload = build_debug_plate_mco(config)
    label_ops = [
        operation
        for operation in payload["operations"]
        if operation["op"] == "pcbdoc.add-text"
    ]

    assert [operation["args"]["text"] for operation in label_ops] == [
        "test_point",
        "LONG_NET_NAME",
        "free_npth",
        "NET_A",
        "NET_B",
    ]
    assert [operation["args"]["position_mils"] for operation in label_ops] == [
        [1313.0, 960.0],
        [1313.0, 890.0],
        [646.0, 960.0],
        [646.0, 890.0],
        [646.0, 810.0],
    ]
    assert {
        tuple(operation["args"]["inverted_rectangle_size_mils"])
        for operation in label_ops
        if "inverted_rectangle_size_mils" in operation["args"]
    } == {(587.0, 60.0)}
    assert {operation["args"]["text_justification"] for operation in label_ops} == {
        "RIGHT_TOP"
    }


def test_debug_plate_inspect_cli_reports_free_npth(tmp_path: Path) -> None:
    from altium_monkey import AltiumPcbDoc, PadShape, PcbLayer

    pcb_path = tmp_path / "dut.PcbDoc"
    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(0, 0, 1000, 700)
    pcbdoc.add_pad(
        designator="A1",
        position_mils=(100, 120),
        width_mils=80,
        height_mils=80,
        layer=PcbLayer.MULTI_LAYER,
        shape=PadShape.CIRCLE,
        hole_size_mils=40,
        plated=False,
    )
    pcbdoc.save(pcb_path)

    payload = inspect_debug_plate_source(pcb_path, project_context="none")

    assert payload["schema"].endswith(".inspect.v1")
    board = payload["boards"][0]
    assert board["board_key"] == "dut"
    assert board["free_pads"][0]["kind"] == "free_npth"

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "debug-plate",
            "inspect",
            str(pcb_path),
            "--project-context",
            "none",
        ],
        cwd=PACKAGE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    cli_payload = json.loads(completed.stdout)
    assert cli_payload["boards"][0]["free_pads"][0]["hole_size_mils"] == 40.0

    seed_path = tmp_path / "debug-plate.seed.jsonc"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "debug-plate",
            "seed",
            str(pcb_path),
            "--project-context",
            "none",
            "--config",
            str(seed_path),
        ],
        cwd=PACKAGE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    seed_payload = json.loads(seed_path.read_text(encoding="utf-8"))
    assert seed_payload["source"]["dut"] == str(pcb_path.resolve())
    seeded_board = seed_payload["selection"]["boards"][0]
    assert seeded_board["free_pads"][0]["kind"] == "free_npth"


def test_debug_plate_cli_init_plan_and_dry_run(tmp_path: Path) -> None:
    config_path = tmp_path / "debug-plate.jsonc"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "debug-plate",
            "init",
            str(config_path),
        ],
        cwd=PACKAGE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert config_path.exists()

    mco_path = tmp_path / "debug-plate.mco.jsonc"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "debug-plate",
            "plan",
            str(config_path),
            "--output-mco",
            str(mco_path),
        ],
        cwd=PACKAGE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert mco_path.exists()

    emitted_mco = tmp_path / "emitted.mco.jsonc"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "debug-plate",
            "run",
            str(config_path),
            "--dry-run",
            "--emit-mco",
            str(emitted_mco),
        ],
        cwd=PACKAGE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert emitted_mco.exists()
    payload = json.loads(completed.stdout)
    assert payload["ok"] is True
    assert payload["dry_run"] is True
