from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

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
    for symbol_name, pin_name in [
        ("YZ209315103P-01", "SIGNAL"),
        ("9774080360R", "MOUNT"),
        ("H2184-05", "ALIGN"),
    ]:
        schlib_path = cache_dir / "schlib" / f"{symbol_name}.SchLib"
        schlib_path.parent.mkdir(parents=True, exist_ok=True)
        schlib = AltiumSchLib()
        symbol = schlib.add_symbol(symbol_name)
        symbol.add_pin(AltiumSchPin("1", pin_name, -100, 0, orientation=2, length=100))
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


def _write_mate_source_pcbdoc(path: Path, *, tp2_layer: str = "BOTTOM") -> Path:
    from altium_monkey import AltiumPcbDoc, PadShape, PcbLayer

    tp2_pcb_layer = PcbLayer.TOP if tp2_layer.upper() == "TOP" else PcbLayer.BOTTOM
    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(0, 0, 1400, 900)
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
    manifest_path = write_debug_plate_known_parts_manifest(
        build_node_test_array_parts_manifest(
            tmp_path / "node-test-array.PrjPcb",
            cache_dir,
        ),
        cache_dir / DEBUG_PLATE_PARTS_CACHE_FILENAME,
    )

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
        "schdoc.add-net-label",
        "pcbdoc.add-component",
        "pcbdoc.add-text",
        "pcbdoc.create-user-union",
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
    assert operations[8]["args"]["text"] == "ALIGN_NET"
    assert operations[8]["args"]["location_mils"] == [2450.0, 1200.0]
    assert operations[9]["args"]["footprint"] == "H2184-05"
    assert operations[9]["args"]["position_mils"] == [1710.0, 420.0]
    assert operations[9]["args"]["pad_nets"] == {"1": "ALIGN_NET"}
    assert operations[10]["args"]["text"] == "ALIGN_NET"
    assert operations[10]["args"]["position_mils"] == [1830.0, 385.0]
    assert operations[10]["args"]["height_mils"] == 65.0
    assert operations[10]["args"]["layer"] == "TOP_OVERLAY"
    assert operations[10]["args"]["font_kind"] == "truetype"
    assert operations[10]["args"]["font_name"] == "Arial"
    assert operations[10]["args"]["bold"] is True
    assert operations[10]["args"]["is_inverted"] is True
    assert operations[10]["args"]["inverted_rectangle_size_mils"] == [450.0, 70.0]
    assert operations[10]["args"]["frame_size_mils"] == [450.0, 70.0]
    assert operations[10]["args"]["text_justification"] == "RIGHT_TOP"
    assert operations[-1]["args"]["name"] == "DEBUG_PLATE_FEATURES"


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
        "schdoc.add-net-label",
        "pcbdoc.add-component",
        "pcbdoc.add-text",
        "schdoc.add-component",
        "pcbdoc.add-component",
        "schdoc.add-component",
        "schdoc.add-net-label",
        "pcbdoc.add-component",
        "pcbdoc.add-text",
        "pcbdoc.create-user-union",
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
        "TP1",
        None,
        "M1",
        "M1",
        "P1",
        None,
        "P1",
        None,
        None,
    ]
    assert [
        operation["args"].get("text")
        for operation in operations
        if operation["op"] in {"schdoc.add-net-label", "pcbdoc.add-text"}
    ] == ["+VIN", "+VIN", "ALIGN_NET", "ALIGN_NET"]
    assert operations[-1]["args"]["name"] == "DEBUG_PLATE_FEATURES"


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
    assert [projection["id"] for projection in payload["projections"]] == [
        "test_points",
        "mounts",
        "alignment_pins",
    ]
    projections = {projection["id"]: projection for projection in payload["projections"]}
    assert projections["test_points"]["source"]["designators"] == "TP1-27"
    assert projections["mounts"]["source"]["designators"] == "M1-4"
    assert payload["artifacts"]["pcb_layer_step"]["source_layer"] == "bottom"


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
        "kind": "free_npth",
        "hole_size_mils": {"min": 75, "max": 85},
        "plated": False,
    }
    assert payload["validation"]["source_side"] == "infer_single_side"
    assert payload["validation"]["side_agnostic_kinds"] == ["mount"]
    assert payload["artifacts"]["pcb_layer_step"]["highlights"] == [
        {"projection": "test_points", "color": "#ffcc00"}
    ]


def test_debug_plate_mate_config_resolves_source_selectors(tmp_path: Path) -> None:
    source_path = _write_mate_source_pcbdoc(tmp_path / "dut.PcbDoc")
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
                    "highlights": [
                        {"projection": "test_points", "color": "#ffcc00"},
                        {"projection": "alignment_pins", "color": "#44aaee"},
                    ],
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
                        "kind": "free_npth",
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
    assert config.pcb_labels.enabled is False

    payload = build_debug_plate_mco(config)
    operations = payload["operations"]
    assert operations[0]["args"]["board_outline_mils"] == {
        "left": 0.0,
        "bottom": 0.0,
        "right": 1400.0,
        "top": 900.0,
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
    ]
    assert [operation["args"]["radius_mils"] for operation in pcb_reference_arcs] == [
        40.0,
        50.0,
        40.0,
        50.0,
    ]
    assert {operation["args"]["layer"] for operation in pcb_reference_arcs} == {
        "MECHANICAL_1"
    }
    assert {operation["args"]["width_mils"] for operation in pcb_reference_arcs} == {
        4.0
    }
    assert pcb_labels[0]["args"]["position_mils"] == [320.0, 265.0]
    assert pcb_labels[0]["args"]["height_mils"] == 50.0
    assert pcb_labels[0]["args"]["text_justification"] == "RIGHT_TOP"
    assert pcb_labels[-1]["args"]["position_mils"] == [610.0, 470.0]
    assert pcb_labels[-1]["args"]["height_mils"] == 45.0
    assert pcb_labels[-1]["args"]["text_justification"] == "LEFT_TOP"
    user_union = [
        operation
        for operation in operations
        if operation["op"] == "pcbdoc.create-user-union"
    ][0]
    assert user_union["args"]["name"] == "DEBUG_PLATE_FEATURES"
    step_op = operations[-1]
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
        ("test_points", "#ffcc00", 2),
        ("alignment_pins", "#44aaee", 1),
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
    from altium_monkey.altium_record_sch__designator import AltiumSchDesignator

    schdoc = AltiumSchDoc(tmp_path / "generated" / "debug_plate.SchDoc")
    pcbdoc = AltiumPcbDoc.from_file(tmp_path / "generated" / "debug_plate.PcbDoc")
    schematic_designators = [
        parameter.text
        for component in schdoc.components
        for parameter in component.parameters
        if isinstance(parameter, AltiumSchDesignator)
    ]
    assert schematic_designators == ["TP1", "M1", "P1"]
    assert [label.text for label in schdoc.net_labels] == ["+VIN", "ALIGN_NET"]
    assert [component.designator for component in pcbdoc.components] == [
        "TP1",
        "M1",
        "P1",
    ]
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
