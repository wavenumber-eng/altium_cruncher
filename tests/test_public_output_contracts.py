"""Qualify generated contracts against real public serializers, not schema examples."""

from argparse import Namespace
from copy import deepcopy
import json
from pathlib import Path

import pytest

from altium_cruncher.contracts.generated.public import decode_contract


def assert_contract(name, value):
    original = deepcopy(value)
    assert decode_contract(name, value) == original
    assert value == original


@pytest.mark.parametrize("kind", ["SchDoc", "SchLib", "PcbDoc", "PcbLib"])
def test_json_dump_real_document_shapes(tmp_path, kind):
    from altium_monkey import AltiumPcbDoc, AltiumPcbLib, AltiumSchDoc, AltiumSchLib
    from altium_cruncher.altium_cruncher_json_dump import build_json_dump_payload, write_json_dumps

    doc = {"SchDoc": AltiumSchDoc, "SchLib": AltiumSchLib, "PcbDoc": AltiumPcbDoc, "PcbLib": AltiumPcbLib}[kind]()
    if kind == "SchLib":
        doc.add_symbol("R")
    if kind == "PcbLib":
        doc.add_footprint("0805")
    if kind == "PcbDoc":
        doc.set_outline_rectangle_mils(0, 0, 1000, 700)
    path = tmp_path / f"board.{kind}"
    doc.save(path)
    payload = build_json_dump_payload(path)
    assert_contract("json_dump", payload)
    wrong_kind = deepcopy(payload)
    wrong_kind["kind"] = "SchDoc" if kind != "SchDoc" else "PcbDoc"
    with pytest.raises(ValueError):
        decode_contract("json_dump", wrong_kind)
    result = write_json_dumps([path], output=tmp_path / "dump")
    assert_contract("json_dump_manifest", result.to_manifest())


def test_bom_pnp_serializers_cover_empty_and_populated_outputs():
    from altium_cruncher.bom_pnp_model import (
        NormalizedBomComponent, GroupedBomLine, NormalizedPlacement,
        bom_raw_payload, grouped_bom_payload, pnp_payload, flat_raw_bom_payload,
    )
    from altium_cruncher.altium_cruncher_cmd_bom import _generic_bom_payload

    component = NormalizedBomComponent("R1", "10k", "0805", "R", "Resistor", "Main", False)
    group = GroupedBomLine(1, 1, ("R1",), False, {"mpn": "example"})
    placement = NormalizedPlacement("R1", "10k", "top", "0805", 1.5, 2.5, 90, "mm")
    for populated in (False, True):
        common = dict(source=Path("board.PrjPcb"), variant="A" if populated else None)
        assert_contract("bom_normalized", bom_raw_payload([component] if populated else [], **common))
        assert_contract("bom_grouped", grouped_bom_payload([group] if populated else [], **common))
        assert_contract("pnp", pnp_payload([placement] if populated else [], units="mm", **common))
        raw = [{"designator": "R1", "value": "10k", "parameters": {"MPN": "example"}, "dnp": False}] if populated else []
        assert_contract("bom_array", flat_raw_bom_payload(raw))
        assert_contract("bom_legacy", _generic_bom_payload(raw, **common))


def test_mco_results_preserve_custom_outputs():
    from altium_cruncher.altium_cruncher_mco import McoExecutionResult, McoOperationResult, mco_operation_catalog

    for results in ((), (McoOperationResult("op1", "custom.example", "fail", "failed", {"custom": {"n": 1}}, "reason"),)):
        assert_contract("mco_execution", McoExecutionResult(not results, True, results).to_dict())
    assert_contract("mco_operations", {"schema": "altium_cruncher.mco.operations.a0", "operations": [info.to_dict() for info in mco_operation_catalog()]})


def test_timing_no_cache_serializes_null(tmp_path):
    from altium_cruncher.pcb_svg_render_job import PcbSvgRenderJob

    with PcbSvgRenderJob() as job:
        with job.measure("job", command="toon"):
            pass
    path = tmp_path / "timings.json"
    job.write_timings(path)
    payload = json.loads(path.read_text())
    assert payload["model_cache"] is None
    assert_contract("pcb_svg_timings", payload)


def test_environment_and_library_reports(tmp_path, capsys):
    from altium_cruncher.altium_environment import AltiumInstall, AltiumProfile
    from altium_cruncher.altium_cruncher_cmd_launch import _print_launch_result
    from altium_cruncher.altium_cruncher_cmd_profiles import _cmd_profiles_list
    from altium_cruncher.altium_cruncher_mate_libraries import scan_altium_libraries

    install = AltiumInstall("Altium", tmp_path / "X2.exe", None, "filesystem")
    assert_contract("installs", {"schema": "altium_cruncher.installs.a0", "installs": [install.to_dict()]})
    _print_launch_result(Namespace(json=True, dry_run=True), install, None, [str(install.x2_path)])
    assert_contract("launch", json.loads(capsys.readouterr().out))
    profile = AltiumProfile("AD", "GUID", tmp_path, tmp_path, tmp_path / "registry", False, "test", tmp_path / "module", False, False, None, tmp_path / "test.dll", False, None)
    _cmd_profiles_list(Namespace(json=True), [profile])
    assert_contract("profiles", json.loads(capsys.readouterr().out))
    assert_contract("libraries_scan", scan_altium_libraries([tmp_path]).to_dict())


def test_easyeda_default_report_serializers():
    from altium_cruncher.easyeda_altium_symbol import EasyEdaSchematicMappingReport
    from altium_cruncher.easyeda_altium_footprint import EasyEdaFootprintMappingReport

    assert_contract("easyeda_symbol_report", EasyEdaSchematicMappingReport("C1", "R", "R?").to_dict())
    assert_contract("easyeda_footprint_report", EasyEdaFootprintMappingReport("C1", "0805").to_dict())


def test_easyeda_checked_placement_bounds(monkeypatch):
    from types import SimpleNamespace
    from altium_cruncher import easyeda_altium_footprint as module

    monkeypatch.setattr(module, "compute_step_model_bounds_mils",
        lambda *args, **kwargs: SimpleNamespace(bounds_mils=(-100, -50, 100, 50)))
    placement = module.EasyEda3DModelPlacement("part.step", b"fixture", 0, 0)
    checked = module._model_placement_check(placement, module._FootprintTransform(0, 0, 1, False),
        module._MilsPoint(0, 0), (-90, -40, 90, 40))
    assert checked["checked"] is True
    report = module.EasyEdaFootprintMappingReport("C1", "0805").to_dict()
    report["model_3d"] = {"placement_check": checked}
    assert_contract("easyeda_footprint_report", report)
    assert_contract("easyeda_models", {"schema": "altium_cruncher.easyeda.3d_models.a0",
        "lcsc_id": "C1", "placement_implemented": True, "placement_note": "checked",
        "models": [], "placement_check": checked})


def test_step_manifest_serializer(tmp_path):
    from altium_monkey import PcbLayer
    from altium_cruncher.altium_cruncher_pcb_layer_step import PcbLayerStepOptions, _build_manifest
    from altium_cruncher.altium_cruncher_pcb_layer_step_origin import coordinate_origin_payload

    path = tmp_path / "board.step"
    path.write_bytes(b"fixture")
    payload = _build_manifest(opts=PcbLayerStepOptions(), output_path=path,
        board_name="board", source_input=None, layer=PcbLayer.TOP, drill_hole_mode="overlay",
        counts={"tracks": 0}, coordinate_origin=coordinate_origin_payload((1.0, 2.0)))
    assert_contract("pcb_layer_step", payload)


def test_notes_and_variant_native_serializers(tmp_path):
    from altium_monkey import AltiumSchDoc
    from altium_monkey.altium_prjpcb import AltiumPrjPcb
    from altium_monkey.altium_record_types import SchPointMils
    from altium_monkey.altium_sch_object_factory import make_sch_text_string
    from altium_cruncher.altium_cruncher_notes import build_notes_payload
    from altium_cruncher.altium_cruncher_prjpcb_variants import summarize_project_variants

    sch = AltiumSchDoc()
    sch.add_object(make_sch_text_string(location_mils=SchPointMils(100, 100), text="Review this"))
    sch_path = tmp_path / "notes.SchDoc"
    sch.save(sch_path)
    assert_contract("notes", build_notes_payload(sch_path))
    project = AltiumPrjPcb()
    project.add_document(sch_path.name)
    project.add_variant("Production")
    path = tmp_path / "board.PrjPcb"
    project.save(path)
    assert_contract("variants_list", summarize_project_variants(path))


def test_intlib_native_extraction_manifest(tmp_path):
    from altium_monkey.altium_intlib import AltiumIntLib
    from altium_cruncher.altium_cruncher_cmd_extract import _intlib_extract_manifest

    path = Path(__file__).resolve().parent / "assets/intlib/rt_super_c1/input/RT_SUPER_C1.IntLib"
    with AltiumIntLib.from_file(path) as library:
        result = library.extract_sources(tmp_path, write_libpkg=True)
        assert_contract("intlib_extract", _intlib_extract_manifest(path, library, result))
