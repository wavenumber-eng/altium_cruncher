from __future__ import annotations

import json
import subprocess
import sys
import types
from pathlib import Path

from altium_cruncher.altium_cruncher_mco import (
    MCO_SCHEMA,
    McoExecutionContext,
    McoOperationResult,
    execute_mco,
    load_jsonc_file,
    loads_jsonc,
    write_mco_template,
)


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def test_loads_jsonc_preserves_comment_markers_inside_strings() -> None:
    payload = loads_jsonc(
        """
        {
          // line comment
          "schema": "wn.altium_cruncher.mco.v1",
          "url": "https://example.test/a//b",
          "operations": [
            {
              "id": "hello",
              "op": "mco.message",
              "args": {
                "text": "/* not a comment */",
              },
            },
          ],
        }
        """
    )

    assert isinstance(payload, dict)
    assert payload["url"] == "https://example.test/a//b"
    assert payload["operations"][0]["args"]["text"] == "/* not a comment */"


def test_load_jsonc_file_accepts_utf8_bom(tmp_path: Path) -> None:
    jsonc_path = tmp_path / "bom.mco.jsonc"
    jsonc_path.write_text(
        '{"schema":"wn.altium_cruncher.mco.v1","operations":[]}',
        encoding="utf-8-sig",
    )

    payload = load_jsonc_file(jsonc_path)

    assert isinstance(payload, dict)
    assert payload["operations"] == []


def test_execute_mco_supports_on_fail_jump() -> None:
    calls: list[str] = []

    def fail_handler(spec, _context):
        calls.append(spec.operation_id)
        return McoOperationResult.failed(spec, "failed intentionally")

    def ok_handler(spec, _context):
        calls.append(spec.operation_id)
        return McoOperationResult.succeeded(spec, "recovered")

    result = execute_mco(
        {
            "schema": MCO_SCHEMA,
            "operations": [
                {"id": "try", "op": "test.fail", "on_fail": "recover"},
                {"id": "skip", "op": "test.ok"},
                {"id": "recover", "op": "test.ok"},
            ],
        },
        McoExecutionContext(work_dir=Path.cwd()),
        registry={"test.fail": fail_handler, "test.ok": ok_handler},
    )

    assert result.ok is True
    assert calls == ["try", "recover"]
    assert [item.operation_id for item in result.results] == ["try", "recover"]


def test_execute_mco_rejects_on_fail_loop() -> None:
    def fail_handler(spec, _context):
        return McoOperationResult.failed(spec, "failed intentionally")

    result = execute_mco(
        {
            "schema": MCO_SCHEMA,
            "operations": [
                {"id": "try", "op": "test.fail", "on_fail": "try"},
            ],
        },
        McoExecutionContext(work_dir=Path.cwd()),
        registry={"test.fail": fail_handler},
    )

    assert result.ok is False
    assert result.results[-1].operation_id == "mco-control-flow"
    assert "loop" in result.results[-1].message


def test_execute_mco_caches_documents_and_flushes_on_exit(tmp_path: Path) -> None:
    document_path = tmp_path / "document.txt"
    document_path.write_text("seed", encoding="utf-8")
    loads: list[Path] = []
    saves: list[Path] = []

    def load_document(path: Path) -> dict[str, str]:
        loads.append(path)
        return {"text": path.read_text(encoding="utf-8")}

    def save_document(document: dict[str, str], path: Path) -> None:
        saves.append(path)
        path.write_text(document["text"], encoding="utf-8")

    def append_handler(spec, context):
        document = context.open_document_for_mutation(
            "testdoc",
            document_path,
            document_path,
            load=load_document,
            save=save_document,
        )
        suffix = spec.args["suffix"]
        assert isinstance(suffix, str)
        document["text"] += suffix
        context.mark_document_dirty("testdoc", document_path)
        assert document_path.read_text(encoding="utf-8") == "seed"
        return McoOperationResult.succeeded(spec, "appended")

    result = execute_mco(
        {
            "schema": MCO_SCHEMA,
            "operations": [
                {"id": "append_a", "op": "test.append", "args": {"suffix": "A"}},
                {"id": "append_b", "op": "test.append", "args": {"suffix": "B"}},
            ],
        },
        McoExecutionContext(work_dir=tmp_path),
        registry={"test.append": append_handler},
    )

    assert result.ok is True
    assert loads == [document_path.resolve()]
    assert saves == [document_path.resolve()]
    assert document_path.read_text(encoding="utf-8") == "seedAB"


def test_project_create_skeleton_dry_run_reports_outputs_without_writing(
    tmp_path: Path,
) -> None:
    result = execute_mco(
        {
            "schema": MCO_SCHEMA,
            "operations": [
                {
                    "id": "create",
                    "op": "project.create-skeleton",
                    "args": {
                        "output_dir": "generated",
                        "project_name": "debug_plate",
                        "board_outline_mils": {
                            "left": 0,
                            "bottom": 0,
                            "right": 500,
                            "top": 300,
                        },
                    },
                }
            ],
        },
        McoExecutionContext(work_dir=tmp_path, dry_run=True),
    )

    assert result.ok is True
    assert result.results[0].outputs["project"].endswith("debug_plate.PrjPcb")
    assert not (tmp_path / "generated").exists()


def test_project_create_skeleton_writes_altium_project_bundle(tmp_path: Path) -> None:
    result = execute_mco(
        {
            "schema": MCO_SCHEMA,
            "operations": [
                {
                    "id": "create",
                    "op": "project.create-skeleton",
                    "args": {
                        "output_dir": "generated",
                        "project_name": "debug_plate",
                        "overwrite": True,
                        "documents": [
                            "libraries/schlib/contact.SchLib",
                            "libraries/pcblib/contact.PcbLib",
                        ],
                    },
                }
            ],
        },
        McoExecutionContext(work_dir=tmp_path),
    )

    assert result.ok is True
    assert (tmp_path / "generated" / "debug_plate.PrjPcb").exists()
    assert (tmp_path / "generated" / "debug_plate.SchDoc").exists()
    assert (tmp_path / "generated" / "debug_plate.PcbDoc").exists()

    from altium_monkey.altium_prjpcb import AltiumPrjPcb

    project = AltiumPrjPcb(tmp_path / "generated" / "debug_plate.PrjPcb")
    assert [document["path"] for document in project.documents] == [
        "libraries\\schlib\\contact.SchLib",
        "libraries\\pcblib\\contact.PcbLib",
        "debug_plate.SchDoc",
        "debug_plate.PcbDoc",
    ]


def test_file_copy_operation_copies_into_generated_tree(tmp_path: Path) -> None:
    source = tmp_path / "source" / "fixture.SchLib"
    source.parent.mkdir(parents=True)
    source.write_text("fixture", encoding="utf-8")

    result = execute_mco(
        {
            "schema": MCO_SCHEMA,
            "operations": [
                {
                    "id": "copy",
                    "op": "file.copy",
                    "args": {
                        "source": "source/fixture.SchLib",
                        "destination": "generated/libraries/fixture.SchLib",
                    },
                }
            ],
        },
        McoExecutionContext(work_dir=tmp_path),
    )

    assert result.ok is True
    output_path = tmp_path / "generated" / "libraries" / "fixture.SchLib"
    assert output_path.read_text(encoding="utf-8") == "fixture"


def test_atomic_cad_operations_mutate_generated_project(tmp_path: Path) -> None:
    result = execute_mco(
        {
            "schema": MCO_SCHEMA,
            "operations": [
                {
                    "id": "create",
                    "op": "project.create-skeleton",
                    "args": {
                        "output_dir": "generated",
                        "project_name": "debug_plate",
                        "overwrite": True,
                    },
                },
                {
                    "id": "wire",
                    "op": "schdoc.add-wire",
                    "args": {
                        "file": "generated/debug_plate.SchDoc",
                        "overwrite": True,
                        "points_mils": [[1000, 1000], [1400, 1000]],
                    },
                },
                {
                    "id": "net",
                    "op": "schdoc.add-net-label",
                    "args": {
                        "file": "generated/debug_plate.SchDoc",
                        "overwrite": True,
                        "text": "DBG_NET",
                        "location_mils": [1200, 1000],
                    },
                },
                {
                    "id": "text",
                    "op": "pcbdoc.add-text",
                    "args": {
                        "file": "generated/debug_plate.PcbDoc",
                        "overwrite": True,
                        "text": "DBG",
                        "position_mils": [200, 200],
                        "height_mils": 60,
                    },
                },
                {
                    "id": "track",
                    "op": "pcbdoc.add-track",
                    "args": {
                        "file": "generated/debug_plate.PcbDoc",
                        "overwrite": True,
                        "start_mils": [100, 100],
                        "end_mils": [300, 100],
                        "width_mils": 8,
                        "layer": "Top Layer",
                    },
                },
                {
                    "id": "arc",
                    "op": "pcbdoc.add-arc",
                    "args": {
                        "file": "generated/debug_plate.PcbDoc",
                        "overwrite": True,
                        "center_mils": [400, 400],
                        "radius_mils": 75,
                        "start_angle_degrees": 0,
                        "end_angle_degrees": 180,
                        "width_mils": 8,
                    },
                },
                {
                    "id": "pad",
                    "op": "pcbdoc.add-pad",
                    "args": {
                        "file": "generated/debug_plate.PcbDoc",
                        "overwrite": True,
                        "designator": "NPTH1",
                        "position_mils": [520, 400],
                        "width_mils": 90,
                        "height_mils": 90,
                        "layer": "MULTI_LAYER",
                        "shape": "CIRCLE",
                        "hole_size_mils": 45,
                        "plated": False,
                        "solder_mask_expansion_mils": 0,
                        "paste_mask_expansion_mils": 0,
                        "tenting_top": True,
                        "tenting_bottom": True,
                        "solder_mask_expansion_mode": 0,
                        "paste_mask_expansion_mode": 0,
                    },
                },
                {
                    "id": "via",
                    "op": "pcbdoc.add-via",
                    "args": {
                        "file": "generated/debug_plate.PcbDoc",
                        "overwrite": True,
                        "position_mils": [620, 400],
                        "diameter_mils": 40,
                        "hole_size_mils": 20,
                    },
                },
                {
                    "id": "fill",
                    "op": "pcbdoc.add-fill",
                    "args": {
                        "file": "generated/debug_plate.PcbDoc",
                        "overwrite": True,
                        "corner1_mils": [700, 300],
                        "corner2_mils": [850, 360],
                    },
                },
                {
                    "id": "region",
                    "op": "pcbdoc.add-region",
                    "args": {
                        "file": "generated/debug_plate.PcbDoc",
                        "overwrite": True,
                        "outline_points_mils": [
                            [700, 450],
                            [850, 450],
                            [820, 540],
                            [730, 540],
                        ],
                    },
                },
                {
                    "id": "union",
                    "op": "pcbdoc.create-user-union",
                    "args": {
                        "file": "generated/debug_plate.PcbDoc",
                        "overwrite": True,
                        "name": "DEBUG_PLATE_FEATURES",
                    },
                },
            ],
        },
        McoExecutionContext(work_dir=tmp_path),
    )

    assert result.ok is True

    from altium_monkey import AltiumPcbDoc, AltiumSchDoc

    schdoc = AltiumSchDoc(tmp_path / "generated" / "debug_plate.SchDoc")
    pcbdoc = AltiumPcbDoc.from_file(tmp_path / "generated" / "debug_plate.PcbDoc")
    assert len(schdoc.wires) == 1
    assert [label.text for label in schdoc.net_labels] == ["DBG_NET"]
    assert [text.text_content for text in pcbdoc.texts] == ["DBG"]
    assert len(pcbdoc.tracks) == 1
    assert len(pcbdoc.arcs) == 1
    assert len(pcbdoc.pads) == 1
    assert pcbdoc.pads[0].is_tenting_top is True
    assert pcbdoc.pads[0].is_tenting_bottom is True
    assert len(pcbdoc.vias) == 1
    assert len(pcbdoc.fills) == 1
    assert len(pcbdoc.regions) == 1
    assert [user_union.name for user_union in pcbdoc.user_unions] == [
        "DEBUG_PLATE_FEATURES"
    ]
    assert pcbdoc.user_unions[0].member_count >= 6


def test_pcbdoc_add_text_exposes_inverted_frame_label_options(
    tmp_path: Path,
) -> None:
    result = execute_mco(
        {
            "schema": MCO_SCHEMA,
            "operations": [
                {
                    "id": "create",
                    "op": "project.create-skeleton",
                    "args": {
                        "output_dir": "generated",
                        "project_name": "debug_plate",
                        "overwrite": True,
                    },
                },
                {
                    "id": "label",
                    "op": "pcbdoc.add-text",
                    "args": {
                        "file": "generated/debug_plate.PcbDoc",
                        "overwrite": True,
                        "text": "I2C0-SDA",
                        "position_mils": [3980, 3165],
                        "height_mils": 65,
                        "layer": "TOP_OVERLAY",
                        "font_kind": "truetype",
                        "font_name": "Arial",
                        "bold": True,
                        "stroke_width_mils": 10,
                        "is_inverted": True,
                        "inverted_margin_mils": 10,
                        "use_inverted_rectangle": True,
                        "inverted_rectangle_size_mils": [450, 70],
                        "is_frame": True,
                        "frame_size_mils": [450, 70],
                        "text_justification": "RIGHT_TOP",
                    },
                },
            ],
        },
        McoExecutionContext(work_dir=tmp_path),
    )

    assert result.ok is True

    from altium_monkey import AltiumPcbDoc, PcbLayer, PcbTextJustification

    pcbdoc = AltiumPcbDoc.from_file(tmp_path / "generated" / "debug_plate.PcbDoc")
    [label] = pcbdoc.texts
    assert label.text_content == "I2C0-SDA"
    assert label.layer == PcbLayer.TOP_OVERLAY
    assert label.font_name == "Arial"
    assert label.font_type == 1
    assert label.is_bold is True
    assert label.is_inverted is True
    assert label.is_frame is True
    assert label.use_inverted_rectangle is True
    assert label.is_justification_valid is True
    assert label.textbox_rect_justification == PcbTextJustification.RIGHT_TOP
    assert label.textbox_rect_width_mils == 450.0
    assert label.textbox_rect_height_mils == 70.0
    assert label.height_mils == 65.0
    assert label.stroke_width_mils == 10.0
    assert label.margin_border_width == 100000


def test_pcbdoc_export_layer_step_operation_writes_artifact(
    monkeypatch,
    tmp_path: Path,
) -> None:
    from altium_monkey import AltiumPcbDoc, PadShape, PcbLayer

    source_path = tmp_path / "source.PcbDoc"
    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_outline_rectangle_mils(0, 0, 1000, 700)
    pcbdoc.add_pad(
        designator="TP1",
        position_mils=(200, 300),
        width_mils=80,
        height_mils=80,
        layer=PcbLayer.BOTTOM,
        shape=PadShape.CIRCLE,
        hole_size_mils=25,
    )
    pcbdoc.save(source_path)

    requests: list[dict[str, object]] = []

    def write_planar_step(request, output_path) -> None:
        requests.append(request)
        Path(output_path).write_text("ISO-10303-21;\n", encoding="utf-8")

    monkeypatch.setitem(
        sys.modules,
        "geometer",
        types.SimpleNamespace(write_planar_step=write_planar_step),
    )

    result = execute_mco(
        {
            "schema": MCO_SCHEMA,
            "operations": [
                {
                    "id": "step",
                    "op": "pcbdoc.export-layer-step",
                    "args": {
                        "file": "source.PcbDoc",
                        "output_file": "generated/bottom.step",
                        "overwrite": True,
                        "layer": "bottom",
                        "highlights": [
                            {
                                "id": "test_points",
                                "name": "Test points",
                                "color": "#ffcc00",
                                "pad_geometries": [
                                    {
                                        "x_mils": 200,
                                        "y_mils": 300,
                                        "width_mils": 80,
                                        "height_mils": 80,
                                        "shape": int(PadShape.CIRCLE.value),
                                        "layer": int(PcbLayer.BOTTOM.value),
                                    }
                                ],
                            }
                        ],
                    },
                }
            ],
        },
        McoExecutionContext(work_dir=tmp_path),
    )

    assert result.ok is True
    assert (tmp_path / "generated" / "bottom.step").exists()
    assert (tmp_path / "generated" / "bottom.json").exists()
    assert result.results[0].outputs["highlight_count"] == 1
    assert [body["id"] for body in requests[0]["bodies"]] == [
        "copper",
        "test_points",
        "board_outline",
    ]


def test_library_component_operations_place_schematic_and_pcb_parts(
    tmp_path: Path,
) -> None:
    from altium_monkey import AltiumPcbLib, AltiumSchLib, PcbLayer
    from altium_monkey.altium_record_sch__pin import AltiumSchPin

    schlib_path = tmp_path / "fixture.SchLib"
    schlib = AltiumSchLib()
    symbol = schlib.add_symbol("DBG_CONTACT")
    symbol.add_pin(AltiumSchPin("1", "SIG", -100, 0, orientation=2, length=100))
    schlib.save(schlib_path)

    pcblib_path = tmp_path / "fixture.PcbLib"
    pcblib = AltiumPcbLib()
    footprint = pcblib.add_footprint("DBG_CONTACT_FP")
    footprint.add_pad(
        designator="1",
        position_mils=(0.0, 0.0),
        width_mils=80.0,
        height_mils=80.0,
        layer=PcbLayer.TOP,
    )
    pcblib.save(pcblib_path)

    result = execute_mco(
        {
            "schema": MCO_SCHEMA,
            "operations": [
                {
                    "id": "create",
                    "op": "project.create-skeleton",
                    "args": {
                        "output_dir": "generated",
                        "project_name": "debug_plate",
                        "overwrite": True,
                    },
                },
                {
                    "id": "symbol",
                    "op": "schdoc.add-component",
                    "args": {
                        "file": "generated/debug_plate.SchDoc",
                        "overwrite": True,
                        "library": str(schlib_path),
                        "symbol": "DBG_CONTACT",
                        "designator": "TP1",
                        "position_mils": [500, 700],
                        "parameters": {
                            "Value": "Debug Contact",
                            "Manufacturer Part Number": "DBG-001",
                        },
                        "footprint_model": "DBG_CONTACT_FP",
                        "footprint_library": "DBG_CONTACT_FP",
                    },
                },
                {
                    "id": "footprint",
                    "op": "pcbdoc.add-component",
                    "args": {
                        "file": "generated/debug_plate.PcbDoc",
                        "overwrite": True,
                        "library": str(pcblib_path),
                        "footprint": "DBG_CONTACT_FP",
                        "designator": "TP1",
                        "position_mils": [500, 700],
                        "layer": "TOP",
                    },
                },
            ],
        },
        McoExecutionContext(work_dir=tmp_path),
    )

    assert result.ok is True

    from altium_monkey import AltiumPcbDoc, AltiumSchDoc
    from altium_monkey.altium_record_sch__designator import AltiumSchDesignator

    schdoc = AltiumSchDoc(tmp_path / "generated" / "debug_plate.SchDoc")
    pcbdoc = AltiumPcbDoc.from_file(tmp_path / "generated" / "debug_plate.PcbDoc")
    schematic_designators = [
        parameter.text
        for component in schdoc.components
        for parameter in component.parameters
        if isinstance(parameter, AltiumSchDesignator)
    ]
    assert schematic_designators == ["TP1"]
    assert [component.lib_reference for component in schdoc.components] == [
        "DBG_CONTACT"
    ]
    params = {
        parameter.name: parameter.text
        for component in schdoc.components
        for parameter in component.parameters
        if getattr(parameter, "name", "")
    }
    assert params["Value"] == "Debug Contact"
    assert params["Manufacturer Part Number"] == "DBG-001"
    assert schdoc.components[0].footprint == "DBG_CONTACT_FP"
    assert [component.designator for component in pcbdoc.components] == ["TP1"]
    assert [component.footprint for component in pcbdoc.components] == [
        "DBG_CONTACT_FP"
    ]
    assert len(pcbdoc.pads) == 1


def test_mco_cli_init_list_and_run(tmp_path: Path) -> None:
    mco_path = tmp_path / "debug-plate.mco.jsonc"
    completed = subprocess.run(
        [sys.executable, "-m", "altium_cruncher", "mco", "init", str(mco_path)],
        cwd=PACKAGE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert mco_path.exists()
    assert json.loads(
        subprocess.run(
            [sys.executable, "-m", "altium_cruncher", "mco", "list-ops"],
            cwd=PACKAGE_ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    )["operations"] == [
        "fail",
        "file.copy",
        "mco.fail",
        "mco.message",
        "message",
        "pcbdoc.add-arc",
        "pcbdoc.add-component",
        "pcbdoc.add-fill",
        "pcbdoc.add-pad",
        "pcbdoc.add-region",
        "pcbdoc.add-text",
        "pcbdoc.add-track",
        "pcbdoc.add-via",
        "pcbdoc.create-user-union",
        "pcbdoc.export-layer-step",
        "project.create-skeleton",
        "schdoc.add-component",
        "schdoc.add-net-label",
        "schdoc.add-wire",
    ]

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "mco",
            "run",
            str(mco_path),
            "--dry-run",
        ],
        cwd=PACKAGE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["ok"] is True
    assert payload["dry_run"] is True


def test_write_mco_template_requires_force_for_existing_file(tmp_path: Path) -> None:
    output_path = tmp_path / "template.mco.jsonc"
    write_mco_template(output_path)

    try:
        write_mco_template(output_path)
    except FileExistsError as exc:
        assert "already exists" in str(exc)
    else:
        raise AssertionError("Expected FileExistsError")
