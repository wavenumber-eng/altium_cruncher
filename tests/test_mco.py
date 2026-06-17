from __future__ import annotations

import json
import subprocess
import sys
import types
from pathlib import Path

import pytest

from altium_cruncher.altium_cruncher_mco import (
    MCO_SCHEMA,
    McoExecutionContext,
    McoExecutionResult,
    McoOperationResult,
    McoOperationSpec,
    execute_mco,
    load_jsonc_file,
    loads_jsonc,
    write_mco_template,
)
from altium_cruncher.altium_cruncher_cmd_mco import print_mco_execution_result


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def _mco_create_project_ops(
    *,
    output_dir: str = "generated",
    project_name: str = "mate",
    overwrite: bool = True,
    schematic_sheet_style: str | None = None,
    board_outline_mils: dict[str, float] | None = None,
    board_origin_mils: dict[str, float] | None = None,
    documents: list[str] | None = None,
) -> list[dict[str, object]]:
    project_file = f"{output_dir}/{project_name}.PrjPcb"
    schematic_file = f"{output_dir}/{project_name}.SchDoc"
    board_file = f"{output_dir}/{project_name}.PcbDoc"
    board_args: dict[str, object] = {
        "file": board_file,
        "layer_stack_template": "2-layer",
        "overwrite": overwrite,
    }
    if board_outline_mils is not None:
        board_args["board_outline_mils"] = board_outline_mils
    if board_origin_mils is not None:
        board_args["board_origin_mils"] = board_origin_mils
    operations: list[dict[str, object]] = [
        {
            "op": "project.create",
            "id": "create_project",
            "args": {
                "file": project_file,
                "name": project_name,
                "overwrite": overwrite,
            },
        },
        {
            "op": "schdoc.create",
            "id": "create_schematic",
            "args": {
                "file": schematic_file,
                "sheet_style": schematic_sheet_style,
                "overwrite": overwrite,
            },
        },
        {
            "op": "pcbdoc.create",
            "id": "create_board",
            "args": board_args,
        },
    ]
    project_documents = [
        *(documents or []),
        f"{project_name}.SchDoc",
        f"{project_name}.PcbDoc",
    ]
    for index, document in enumerate(project_documents, start=1):
        operations.append(
            {
                "op": "project.add_document",
                "id": f"add_document_{index}",
                "args": {
                    "file": project_file,
                    "document": document,
                },
            }
        )
    return operations


def test_loads_jsonc_preserves_comment_markers_inside_strings() -> None:
    payload = loads_jsonc(
        """
        {
          // line comment
          "schema": "altium_cruncher.mco.a0",
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
        '{"schema":"altium_cruncher.mco.a0","operations":[]}',
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


def test_execute_mco_caches_created_pcbdoc_and_flushes_once(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from altium_monkey import AltiumPcbDoc

    board_path = tmp_path / "generated" / "mate.PcbDoc"
    saves: list[Path] = []
    original_save = AltiumPcbDoc.save

    def save_document(
        document: AltiumPcbDoc,
        path: Path | str,
        *args: object,
        **kwargs: object,
    ) -> None:
        saves.append(Path(path).resolve())
        original_save(document, path, *args, **kwargs)

    monkeypatch.setattr(AltiumPcbDoc, "save", save_document)

    result = execute_mco(
        {
            "schema": MCO_SCHEMA,
            "operations": [
                {
                    "id": "create",
                    "op": "pcbdoc.create",
                    "args": {
                        "file": str(board_path),
                        "overwrite": True,
                        "board_outline_mils": {
                            "left": 0,
                            "bottom": 0,
                            "right": 500,
                            "top": 300,
                        },
                    },
                },
                {
                    "id": "track",
                    "op": "pcbdoc.add_track",
                    "args": {
                        "file": str(board_path),
                        "overwrite": True,
                        "start_mils": [50, 50],
                        "end_mils": [200, 50],
                        "width_mils": 8,
                    },
                },
                {
                    "id": "union",
                    "op": "pcbdoc.create_user_union",
                    "args": {
                        "file": str(board_path),
                        "overwrite": True,
                        "name": "generated",
                    },
                },
            ],
        },
        McoExecutionContext(work_dir=tmp_path),
    )

    assert result.ok is True
    assert saves == [board_path.resolve()]
    pcbdoc = AltiumPcbDoc.from_file(board_path)
    assert len(pcbdoc.tracks) == 1


def test_project_primitive_dry_run_reports_outputs_without_writing(
    tmp_path: Path,
) -> None:
    result = execute_mco(
        {
            "schema": MCO_SCHEMA,
            "operations": _mco_create_project_ops(
                overwrite=False,
                board_outline_mils={
                    "left": 0,
                    "bottom": 0,
                    "right": 500,
                    "top": 300,
                },
            ),
        },
        McoExecutionContext(work_dir=tmp_path, dry_run=True),
    )

    assert result.ok is True
    assert result.results[0].outputs["project"].endswith("mate.PrjPcb")
    assert not (tmp_path / "generated").exists()


def test_project_primitives_write_altium_project_bundle(tmp_path: Path) -> None:
    result = execute_mco(
        {
            "schema": MCO_SCHEMA,
            "operations": _mco_create_project_ops(
                schematic_sheet_style="D",
                board_outline_mils={
                    "left": 100,
                    "bottom": 200,
                    "right": 600,
                    "top": 500,
                },
                board_origin_mils={"x": 1234, "y": 5678},
                documents=[
                    "libraries/schlib/contact.SchLib",
                    "libraries/pcblib/contact.PcbLib",
                ],
            ),
        },
        McoExecutionContext(work_dir=tmp_path),
    )

    assert result.ok is True
    assert (tmp_path / "generated" / "mate.PrjPcb").exists()
    assert (tmp_path / "generated" / "mate.SchDoc").exists()
    assert (tmp_path / "generated" / "mate.PcbDoc").exists()

    from altium_monkey import AltiumPcbDoc, AltiumSchDoc
    from altium_monkey.altium_record_sch__sheet import SheetStyle
    from altium_monkey.altium_prjpcb import AltiumPrjPcb

    schdoc = AltiumSchDoc(tmp_path / "generated" / "mate.SchDoc")
    assert schdoc.sheet is not None
    assert schdoc.sheet.sheet_style == SheetStyle.D

    pcbdoc = AltiumPcbDoc.from_file(tmp_path / "generated" / "mate.PcbDoc")
    assert pcbdoc.board.origin_x == 1234.0
    assert pcbdoc.board.origin_y == 5678.0

    project = AltiumPrjPcb(tmp_path / "generated" / "mate.PrjPcb")
    assert [document["path"] for document in project.documents] == [
        "libraries\\schlib\\contact.SchLib",
        "libraries\\pcblib\\contact.PcbLib",
        "mate.SchDoc",
        "mate.PcbDoc",
    ]


def test_pcblib_primitives_create_library_with_footprint(tmp_path: Path) -> None:
    result = execute_mco(
        {
            "schema": MCO_SCHEMA,
            "operations": [
                {
                    "id": "create",
                    "op": "pcblib.create",
                    "args": {
                        "file": "generated/fixture.PcbLib",
                        "overwrite": False,
                    },
                },
                {
                    "id": "footprint",
                    "op": "pcblib.add_footprint",
                    "args": {
                        "file": "generated/fixture.PcbLib",
                        "name": "DBG_CONTACT_FP",
                        "height": "12mil",
                        "description": "Debug contact footprint",
                        "parameters": {"AREA": "1mil^2"},
                        "primitive_parameters": {
                            "FixtureRole": "contact",
                            "Value": "A|B=C",
                        },
                        "overwrite": True,
                    },
                },
            ],
        },
        McoExecutionContext(work_dir=tmp_path),
    )

    assert result.ok is True

    from altium_monkey import AltiumPcbLib

    pcblib = AltiumPcbLib.from_file(tmp_path / "generated" / "fixture.PcbLib")
    assert [footprint.name for footprint in pcblib.footprints] == ["DBG_CONTACT_FP"]
    footprint = pcblib.footprints[0]
    assert footprint.parameters["HEIGHT"] == "12mil"
    assert footprint.parameters["DESCRIPTION"] == "Debug contact footprint"
    assert footprint.parameters["AREA"] == "1mil^2"
    assert footprint.footprint_primitive_parameters["FixtureRole"] == "contact"
    assert footprint.footprint_primitive_parameters["Value"] == "A|B=C"


def test_document_create_primitives_roundtrip_generated_assets(tmp_path: Path) -> None:
    from altium_cruncher.altium_cruncher_project_profiles import (
        generated_rigid_stack_config,
    )

    result = execute_mco(
        {
            "schema": MCO_SCHEMA,
            "operations": [
                {
                    "id": "schdoc",
                    "op": "schdoc.create",
                    "args": {
                        "file": "generated/demo.SchDoc",
                        "overwrite": False,
                    },
                },
                {
                    "id": "schlib",
                    "op": "schlib.create",
                    "args": {
                        "file": "generated/demo.SchLib",
                        "overwrite": False,
                    },
                },
                {
                    "id": "symbol",
                    "op": "schlib.add_symbol",
                    "args": {
                        "file": "generated/demo.SchLib",
                        "name": "DEMO_SYMBOL",
                        "description": "Demo symbol",
                    },
                },
                {
                    "id": "pcbdoc",
                    "op": "pcbdoc.create",
                    "args": {
                        "file": "generated/demo.PcbDoc",
                        "rigid_stack": generated_rigid_stack_config(4),
                        "mechanical_layer_profile": "standard_component_pairs",
                        "overwrite": False,
                    },
                },
            ],
        },
        McoExecutionContext(work_dir=tmp_path),
    )

    assert result.ok is True

    from altium_monkey import (
        AltiumPcbDoc,
        AltiumSchDoc,
        AltiumSchLib,
        MechanicalLayerKind,
    )
    from altium_monkey.altium_layer_stack_document import AltiumLayerStackDocument
    from altium_monkey.altium_record_sch__sheet import SheetStyle

    schdoc = AltiumSchDoc(tmp_path / "generated" / "demo.SchDoc")
    assert schdoc.sheet is not None
    assert schdoc.sheet.sheet_style == SheetStyle.D

    schlib = AltiumSchLib(tmp_path / "generated" / "demo.SchLib")
    assert [symbol.name for symbol in schlib.symbols] == ["DEMO_SYMBOL"]
    assert schlib.symbols[0].description == "Demo symbol"

    pcbdoc = AltiumPcbDoc.from_file(tmp_path / "generated" / "demo.PcbDoc")
    stack = AltiumLayerStackDocument.from_pcbdoc(pcbdoc)
    assert [
        layer.display_name
        for layer in stack.physical_stacks[0].layers
        if layer.family == "copper"
    ] == ["Top Layer", "Mid-Layer 1", "Mid-Layer 2", "Bottom Layer"]
    assert (
        pcbdoc.get_mechanical_layer_kind("MECHANICAL10")
        == MechanicalLayerKind.BODY_3D_TOP
    )


def test_project_variant_mco_operations_roundtrip(tmp_path: Path) -> None:
    from altium_monkey.altium_prjpcb import AltiumPrjPcb

    project_path = tmp_path / "demo.PrjPcb"
    project = AltiumPrjPcb.create_minimal("demo")
    project.add_variant("A", unique_id="A-GUID", allow_fabrication=True, current=True)
    project.save(project_path)

    result = execute_mco(
        {
            "schema": MCO_SCHEMA,
            "operations": [
                {
                    "id": "dnp",
                    "op": "project.toggle_variant_dnp",
                    "args": {
                        "file": "demo.PrjPcb",
                        "variant": "A",
                        "designator": "R1",
                        "unique_id": "R1UID",
                    },
                },
                {
                    "id": "clone",
                    "op": "project.clone_variant",
                    "args": {
                        "file": "demo.PrjPcb",
                        "source_name": "A",
                        "name": "B",
                        "unique_id": "B-GUID",
                        "allow_fabrication": False,
                        "current": True,
                    },
                },
                {
                    "id": "rename",
                    "op": "project.rename_variant",
                    "args": {
                        "file": "demo.PrjPcb",
                        "name": "B",
                        "new_name": "C",
                    },
                },
                {
                    "id": "delete",
                    "op": "project.delete_variant",
                    "args": {
                        "file": "demo.PrjPcb",
                        "name": "A",
                    },
                },
                {
                    "id": "list",
                    "op": "project.list_variants",
                    "args": {
                        "file": "demo.PrjPcb",
                    },
                },
            ],
        },
        McoExecutionContext(work_dir=tmp_path),
    )

    assert result.ok is True
    reparsed = AltiumPrjPcb(project_path)
    assert set(reparsed.variants) == {"C"}
    assert reparsed.get_current_variant() == "C"
    variant = reparsed.variants["C"]
    assert variant["unique_id"] == "B-GUID"
    assert variant["allow_fabrication"] is False
    assert variant["DNP"] == ["R1"]
    assert variant["variations"] == [
        {
            "Designator": "R1",
            "UniqueId": "\\R1UID",
            "Kind": "1",
            "AlternatePart": "",
        }
    ]
    list_payload = result.results[-1].outputs
    assert list_payload["schema"] == "altium_cruncher.variants.list.a0"
    assert list_payload["variant_count"] == 1
    assert list_payload["rows"][0]["operation"] == "DNP"


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
                *_mco_create_project_ops(),
                {
                    "id": "wire",
                    "op": "schdoc.add_wire",
                    "args": {
                        "file": "generated/mate.SchDoc",
                        "overwrite": True,
                        "points_mils": [[1000, 1000], [1400, 1000]],
                    },
                },
                {
                    "id": "net",
                    "op": "schdoc.add_net_label",
                    "args": {
                        "file": "generated/mate.SchDoc",
                        "overwrite": True,
                        "text": "DBG_NET",
                        "location_mils": [1200, 1000],
                        "orientation": "DEG_90",
                    },
                },
                {
                    "id": "text",
                    "op": "pcbdoc.add_text",
                    "args": {
                        "file": "generated/mate.PcbDoc",
                        "overwrite": True,
                        "text": "DBG",
                        "position_mils": [200, 200],
                        "height_mils": 60,
                    },
                },
                {
                    "id": "track",
                    "op": "pcbdoc.add_track",
                    "args": {
                        "file": "generated/mate.PcbDoc",
                        "overwrite": True,
                        "start_mils": [100, 100],
                        "end_mils": [300, 100],
                        "width_mils": 8,
                        "layer": "Top Layer",
                    },
                },
                {
                    "id": "arc",
                    "op": "pcbdoc.add_arc",
                    "args": {
                        "file": "generated/mate.PcbDoc",
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
                    "op": "pcbdoc.add_pad",
                    "args": {
                        "file": "generated/mate.PcbDoc",
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
                    "op": "pcbdoc.add_via",
                    "args": {
                        "file": "generated/mate.PcbDoc",
                        "overwrite": True,
                        "position_mils": [620, 400],
                        "diameter_mils": 40,
                        "hole_size_mils": 20,
                    },
                },
                {
                    "id": "fill",
                    "op": "pcbdoc.add_fill",
                    "args": {
                        "file": "generated/mate.PcbDoc",
                        "overwrite": True,
                        "corner1_mils": [700, 300],
                        "corner2_mils": [850, 360],
                    },
                },
                {
                    "id": "region",
                    "op": "pcbdoc.add_region",
                    "args": {
                        "file": "generated/mate.PcbDoc",
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
                    "op": "pcbdoc.create_user_union",
                    "args": {
                        "file": "generated/mate.PcbDoc",
                        "overwrite": True,
                        "name": "MATE_FEATURES",
                    },
                },
            ],
        },
        McoExecutionContext(work_dir=tmp_path),
    )

    assert result.ok is True

    from altium_monkey import AltiumPcbDoc, AltiumSchDoc

    schdoc = AltiumSchDoc(tmp_path / "generated" / "mate.SchDoc")
    pcbdoc = AltiumPcbDoc.from_file(tmp_path / "generated" / "mate.PcbDoc")
    assert len(schdoc.wires) == 1
    assert [label.text for label in schdoc.net_labels] == ["DBG_NET"]
    assert [int(label.orientation) for label in schdoc.net_labels] == [1]
    assert [text.text_content for text in pcbdoc.texts] == ["DBG"]
    assert len(pcbdoc.tracks) == 1
    assert len(pcbdoc.arcs) == 1
    assert len(pcbdoc.pads) == 1
    assert pcbdoc.pads[0].is_tenting_top is True
    assert pcbdoc.pads[0].is_tenting_bottom is True
    assert len(pcbdoc.vias) == 1
    assert len(pcbdoc.fills) == 1
    assert len(pcbdoc.regions) == 1
    assert [user_union.name for user_union in pcbdoc.user_unions] == ["MATE_FEATURES"]
    assert pcbdoc.user_unions[0].member_count >= 6


def test_pcbdoc_add_text_exposes_inverted_frame_label_options(
    tmp_path: Path,
) -> None:
    result = execute_mco(
        {
            "schema": MCO_SCHEMA,
            "operations": [
                *_mco_create_project_ops(),
                {
                    "id": "label",
                    "op": "pcbdoc.add_text",
                    "args": {
                        "file": "generated/mate.PcbDoc",
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

    pcbdoc = AltiumPcbDoc.from_file(tmp_path / "generated" / "mate.PcbDoc")
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


def test_pcbdoc_add_region_can_create_board_cutout(tmp_path: Path) -> None:
    result = execute_mco(
        {
            "schema": MCO_SCHEMA,
            "operations": [
                *_mco_create_project_ops(),
                {
                    "id": "cutout",
                    "op": "pcbdoc.add_region",
                    "args": {
                        "file": "generated/mate.PcbDoc",
                        "overwrite": True,
                        "outline_points_mils": [
                            [100, 100],
                            [250, 100],
                            [250, 220],
                            [100, 220],
                        ],
                        "layer": "MULTI_LAYER",
                        "is_board_cutout": True,
                    },
                },
            ],
        },
        McoExecutionContext(work_dir=tmp_path),
    )

    assert result.ok is True

    from altium_monkey import AltiumPcbDoc

    pcbdoc = AltiumPcbDoc.from_file(tmp_path / "generated" / "mate.PcbDoc")
    assert len(pcbdoc.regions) == 1
    assert pcbdoc.regions[0].is_board_cutout is True
    assert pcbdoc.regions[0].properties["ISBOARDCUTOUT"] == "TRUE"
    assert len(pcbdoc.board.outline.cutouts) == 1


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
    pcbdoc.add_track((100, 100), (300, 100), width_mils=12, layer=PcbLayer.BOTTOM)
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
                    "op": "pcbdoc.export_layer_step",
                    "args": {
                        "file": "source.PcbDoc",
                        "output_file": "generated/bottom.step",
                        "overwrite": True,
                        "layer": "bottom",
                        "features": {
                            "tracks": {
                                "enabled": True,
                                "color": "#123456",
                            },
                            "polygons": {
                                "enabled": False,
                                "color": "#654321",
                            },
                        },
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
        "tracks",
        "copper_pads",
        "test_points",
        "board_outline",
    ]
    bodies = {body["id"]: body for body in requests[0]["bodies"]}
    assert bodies["tracks"]["color"] == "#123456"


def test_pcbdoc_add_embedded_3d_model_operation_dry_run(tmp_path: Path) -> None:
    (tmp_path / "generated").mkdir()
    (tmp_path / "generated" / "bottom.step").write_text(
        "ISO-10303-21;\n",
        encoding="utf-8",
    )

    result = execute_mco(
        {
            "schema": MCO_SCHEMA,
            "operations": [
                {
                    "id": "insert_step",
                    "op": "pcbdoc.add_embedded_3d_model",
                    "args": {
                        "file": "generated/mate.PcbDoc",
                        "overwrite": True,
                        "model_file": "generated/bottom.step",
                        "name": "DUT bottom layer",
                        "z_mm": 1.6,
                        "bounds_mils": {
                            "left": 0,
                            "bottom": 0,
                            "right": 1000,
                            "top": 700,
                        },
                    },
                }
            ],
        },
        McoExecutionContext(work_dir=tmp_path, dry_run=True),
    )

    assert result.ok is True
    assert result.results[0].outputs["name"] == "DUT bottom layer"
    assert result.results[0].outputs["z_mils"] == pytest.approx(62.992126)


def test_created_pcbdoc_inserts_step_model_once(tmp_path: Path) -> None:
    (tmp_path / "generated").mkdir()
    (tmp_path / "generated" / "bottom.step").write_text(
        "ISO-10303-21;\n",
        encoding="utf-8",
    )

    result = execute_mco(
        {
            "schema": MCO_SCHEMA,
            "operations": [
                *_mco_create_project_ops(
                    board_outline_mils={
                        "left": 0,
                        "bottom": 0,
                        "right": 1000,
                        "top": 700,
                    },
                ),
                {
                    "id": "insert_step",
                    "op": "pcbdoc.add_embedded_3d_model",
                    "args": {
                        "file": "generated/mate.PcbDoc",
                        "overwrite": True,
                        "model_file": "generated/bottom.step",
                        "model_name": "bottom.step",
                        "name": "DUT bottom layer",
                        "location_mils": [0, 0],
                        "z_mm": 1.6,
                        "bounds_mils": {
                            "left": 0,
                            "bottom": 0,
                            "right": 1000,
                            "top": 700,
                        },
                    },
                },
            ],
        },
        McoExecutionContext(work_dir=tmp_path),
    )

    assert result.ok is True

    from altium_monkey import AltiumPcbDoc

    pcbdoc = AltiumPcbDoc.from_file(tmp_path / "generated" / "mate.PcbDoc")
    model_names = [model.name for model in pcbdoc.models]
    model_body_names = [
        body.name
        for body in pcbdoc.component_bodies
        if getattr(body, "model_name", None) == "bottom.step"
    ]
    assert model_names.count("bottom.step") == 1
    assert model_body_names == ["DUT bottom layer"]


def test_schdoc_add_power_port_operation_writes_power_symbol(
    tmp_path: Path,
) -> None:
    result = execute_mco(
        {
            "schema": MCO_SCHEMA,
            "operations": [
                *_mco_create_project_ops(),
                {
                    "id": "power",
                    "op": "schdoc.add_power_port",
                    "args": {
                        "file": "generated/mate.SchDoc",
                        "overwrite": True,
                        "text": "GND",
                        "location_mils": [500, 700],
                        "style": "BAR",
                        "orientation": "DEGREES_0",
                        "show_net_name": False,
                    },
                },
            ],
        },
        McoExecutionContext(work_dir=tmp_path),
    )

    assert result.ok is True

    from altium_monkey import AltiumSchDoc

    schdoc = AltiumSchDoc(tmp_path / "generated" / "mate.SchDoc")
    power_ports = schdoc.get_power_ports()
    assert len(power_ports) == 1
    assert power_ports[0].text == "GND"
    assert power_ports[0].record.location_mils.x_mils == 500.0
    assert power_ports[0].record.location_mils.y_mils == 700.0
    assert power_ports[0].record.show_net_name is False


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
                *_mco_create_project_ops(),
                {
                    "id": "symbol",
                    "op": "schdoc.add_component",
                    "args": {
                        "file": "generated/mate.SchDoc",
                        "overwrite": True,
                        "library": str(schlib_path),
                        "symbol": "DBG_CONTACT",
                        "designator": "TP1",
                        "unique_id": "ABC12345",
                        "position_mils": [500, 700],
                        "designator_style": {
                            "position_mils": [500, 850],
                            "justification": "BOTTOM_CENTER",
                            "font_name": "Arial",
                            "font_size": 10,
                            "bold": True,
                        },
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
                    "op": "pcbdoc.add_component",
                    "args": {
                        "file": "generated/mate.PcbDoc",
                        "overwrite": True,
                        "library": str(pcblib_path),
                        "footprint": "DBG_CONTACT_FP",
                        "designator": "TP1",
                        "position_mils": [500, 700],
                        "layer": "TOP",
                        "source_unique_id": "ABC12345",
                        "source_hierarchical_path": "mate",
                        "source_component_library": "fixture.SchLib",
                        "source_lib_reference": "DBG_CONTACT",
                        "source_description": "Debug contact symbol",
                        "channel_offset": 0,
                    },
                },
                {
                    "id": "designator",
                    "op": "pcbdoc.arrange_designators",
                    "args": {
                        "file": "generated/mate.PcbDoc",
                        "overwrite": True,
                        "designators": ["TP1"],
                        "placement": "above_component",
                        "offset_mils": [0, 10],
                        "height_mils": 40,
                        "font_kind": "truetype",
                        "font_name": "Arial",
                        "bold": True,
                        "stroke_width_mils": 8,
                    },
                },
            ],
        },
        McoExecutionContext(work_dir=tmp_path),
    )

    assert result.ok is True

    from altium_monkey import AltiumPcbDoc, AltiumSchDoc, TextJustification
    from altium_monkey.altium_record_sch__designator import AltiumSchDesignator

    schdoc = AltiumSchDoc(tmp_path / "generated" / "mate.SchDoc")
    pcbdoc = AltiumPcbDoc.from_file(tmp_path / "generated" / "mate.PcbDoc")
    schematic_designators = [
        parameter.text
        for component in schdoc.components
        for parameter in component.parameters
        if isinstance(parameter, AltiumSchDesignator)
    ]
    assert schematic_designators == ["TP1"]
    designator_record = next(
        parameter
        for component in schdoc.components
        for parameter in component.parameters
        if isinstance(parameter, AltiumSchDesignator)
    )
    assert designator_record.location.x_mils == 500.0
    assert designator_record.location.y_mils == 850.0
    assert designator_record.justification == TextJustification.BOTTOM_CENTER
    assert designator_record.auto_position is False
    assert [component.lib_reference for component in schdoc.components] == [
        "DBG_CONTACT"
    ]
    assert schdoc.components[0].unique_id == "ABC12345"
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
    assert pcbdoc.components[0].source_unique_id == "\\ABC12345"
    assert pcbdoc.components[0].source_hierarchical_path == "mate"
    assert pcbdoc.components[0].source_component_library == "fixture.SchLib"
    assert pcbdoc.components[0].source_lib_reference == "DBG_CONTACT"
    assert pcbdoc.components[0].description == "Debug contact symbol"
    assert pcbdoc.components[0].channel_offset == 0
    assert len(pcbdoc.pads) == 1
    designator_text = next(text for text in pcbdoc.texts if text.is_designator)
    assert designator_text.text_content == "TP1"
    assert designator_text.component_index == 0
    assert designator_text.x_mils == 464.0
    assert designator_text.y_mils == 750.0
    assert designator_text.height_mils == 40.0
    assert designator_text.stroke_width_mils == 8.0
    assert designator_text.font_name == "Arial"
    assert designator_text.is_bold is True


def test_mco_cli_init_list_and_run(tmp_path: Path) -> None:
    mco_path = tmp_path / "mate.mco.jsonc"
    completed = subprocess.run(
        [sys.executable, "-m", "altium_cruncher", "mco", "init", str(mco_path)],
        cwd=PACKAGE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert mco_path.exists()
    catalog = json.loads(
        subprocess.run(
            [sys.executable, "-m", "altium_cruncher", "mco", "list", "--json"],
            cwd=PACKAGE_ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    )
    assert [operation["op"] for operation in catalog["operations"]] == [
        "file.copy",
        "mco.fail",
        "mco.message",
        "pcbdoc.add_arc",
        "pcbdoc.add_component",
        "pcbdoc.add_embedded_3d_model",
        "pcbdoc.add_fill",
        "pcbdoc.add_pad",
        "pcbdoc.add_region",
        "pcbdoc.add_text",
        "pcbdoc.add_track",
        "pcbdoc.add_via",
        "pcbdoc.arrange_designators",
        "pcbdoc.create",
        "pcbdoc.create_user_union",
        "pcbdoc.export_layer_step",
        "pcblib.add_footprint",
        "pcblib.create",
        "project.add_document",
        "project.add_parameter",
        "project.add_variant",
        "project.add_variant_dnp",
        "project.clone_variant",
        "project.create",
        "project.delete_variant",
        "project.list_variants",
        "project.rename_variant",
        "project.toggle_variant_dnp",
        "schdoc.add_component",
        "schdoc.add_net_label",
        "schdoc.add_power_port",
        "schdoc.add_wire",
        "schdoc.create",
        "schlib.add_symbol",
        "schlib.create",
    ]
    human_catalog = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "mco",
            "list",
            "--no-color",
        ],
        cwd=PACKAGE_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert "    required: file, document" in human_catalog
    assert "    optional: unique_id" in human_catalog
    assert "unique_id?" not in human_catalog

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "mco",
            "run",
            str(mco_path),
            "--dry-run",
            "--json",
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


def test_mco_pretty_output_leads_with_message(
    capsys: pytest.CaptureFixture[str],
) -> None:
    spec = McoOperationSpec(
        operation_id="create_mate_project",
        op="project.create",
        args={},
        message="Create mate project",
    )
    result = McoExecutionResult(
        ok=True,
        dry_run=True,
        results=(
            McoOperationResult.succeeded(
                spec,
                "Create mate project",
            ),
        ),
    )

    print_mco_execution_result(result, title="mate", color=False)

    lines = capsys.readouterr().out.splitlines()
    assert lines[1] == "  OK   Create mate project"
    assert lines[2] == "       project.create create_mate_project"


def test_write_mco_template_requires_force_for_existing_file(tmp_path: Path) -> None:
    output_path = tmp_path / "template.mco.jsonc"
    write_mco_template(output_path)

    text = output_path.read_text(encoding="utf-8")
    assert "MCO operation name. Options:" in text
    assert "project.create" in text

    try:
        write_mco_template(output_path)
    except FileExistsError as exc:
        assert "already exists" in str(exc)
    else:
        raise AssertionError("Expected FileExistsError")
