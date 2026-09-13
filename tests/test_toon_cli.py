"""Focused toon command, export, config and variant contracts."""

import argparse
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest

from altium_cruncher.altium_cruncher_cmd_toon import (
    TOON_CONFIG_FILENAME, _resolve_config, register_parser,
)
from altium_cruncher.config_json import load_json_config
from altium_cruncher.pcb_illustration_config import resolve_illustration_config
from altium_cruncher.pcb_illustration_variants import illustration_variants

ROOT = Path(__file__).resolve().parents[1]



def _args(*tokens):
    parser = argparse.ArgumentParser()
    register_parser(parser.add_subparsers())
    return parser.parse_args(["toon", *tokens])


@pytest.mark.parametrize("tokens", [
    ("--format", "svg"), ("--format", "png"), ("--format", "both"),
    ("--dpi", "300"), ("--width", "4096"), ("--background", "transparent"),
])
def test_removed_output_options_are_rejected(tokens):
    with pytest.raises(SystemExit):
        _args(*tokens)


@pytest.mark.parametrize("value", ["0", "-1", "1.5", "auto"])
def test_invalid_worker_counts_fail_before_rendering(value):
    with pytest.raises(SystemExit):
        _args("--workers", value)


def test_config_is_created_and_reused_with_cli_overrides(tmp_path):
    source = tmp_path / "board.PrjPcb"
    first = _resolve_config(_args("--theme", "white"), source)
    path = tmp_path / TOON_CONFIG_FILENAME
    assert path.name == "toon.config"
    assert _args().output == Path("output/toon")
    assert not hasattr(_args(), "format")
    assert _args().timings is None
    assert _args().workers == 4
    assert _args("--workers", "8").workers == 8
    assert _args("--workers", "1").workers == 1
    assert _args().cache_dir is None and not _args().no_cache
    assert _args("--cache-dir", str(tmp_path)).cache_dir == tmp_path
    assert _args("--no-cache").no_cache
    assert path.is_file()
    assert len(first.enabled_views()) == 2
    payload = load_json_config(path)
    payload["global"]["styles"]["assembly_designators"]["color"] = "#00FF00"
    payload["components"] = {"J1": {"show_designator": False}}
    import json
    path.write_text(json.dumps(payload), encoding="utf-8")
    saved = path.read_bytes()
    config = _resolve_config(_args("--side", "bottom", "--assembly"), source)
    assert path.read_bytes() == saved
    assert [v.name for v in config.enabled_views()] == ["bottom"]
    bottom = config.enabled_views()[0]
    assert bottom.mirror is True
    assert "png" not in config.global_options.to_dict()
    assert "ASSEMBLY_DESIGNATORS_BOTTOM" in bottom.layers
    styles = config.resolved_styles_for_view(bottom)
    assert styles["soldermask_film"]["color"] == "#EEEEEE"
    assert styles["silkscreen_board_graphics"]["color"] == "#000000"
    assert styles["assembly_designators"]["color"] == "#00FF00"
    assert config.components["J1"].show_designator is False


def test_public_toon_command_writes_editable_substrate_preset(tmp_path):
    target = tmp_path / "toon.config"
    result = subprocess.run(
        [sys.executable, "-m", "altium_cruncher", "toon", "--write-config", str(target)],
        cwd=tmp_path, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    config = load_json_config(target)
    assert config["schema"] == "pcb.svg.config.a0"
    assert [v["group_id"] for v in config["views"]] == ["toon-top", "toon-bottom"]
    assert all(v["layers"][0] == "BOARD_SUBSTRATE" for v in config["views"])
    assert config["global"]["styles"]["board_substrate"]["color"] == "#B6A26B"


def test_config_accepts_partial_settings_and_custom_views():
    config = resolve_illustration_config({
        "global": {"styles": {"illustration": {"opacity": 0.3}}},
        "views": [{"name": "custom", "layers": ["ILLUSTRATION_BOTTOM"]}],
    }, side="bottom")
    assert config.views[0].name == "custom"
    assert config.resolved_styles_for_view(config.views[0])["illustration"]["opacity"] == 0.3
    with pytest.raises(ValueError, match="exactly one"):
        resolve_illustration_config({"views": [{"name": "copper", "layers": ["TOP"]}]})


def test_rt_variants_read_dnp_and_leave_project_unchanged():
    from altium_monkey.altium_design import AltiumDesign
    from altium_monkey.altium_prjpcb import AltiumPrjPcb

    project = AltiumPrjPcb(ROOT / "tests/assets/projects/rt_super_c1/input/RT_SUPER_C1.PrjPcb")
    design = AltiumDesign(project=project, schdocs=[])
    current = project.get_current_variant()
    variants = illustration_variants(design, all_variants=True)
    assert len(variants) == 3
    assert variants[0].name is None
    assert not variants[0].excluded_designators
    assert variants[0].project_parameters["VariantName"] == ""
    for variant in variants[1:]:
        assert len(variant.excluded_designators) == 6
        assert variant.project_parameters["VariantName"] == variant.name
    assert {"U5", "U6"} <= set().union(*(v.excluded_designators for v in variants))
    assert project.get_current_variant() == current
    with pytest.raises(ValueError, match="Unknown variant"):
        illustration_variants(design, variant="missing")


def test_alternate_model_variant_is_reported_before_rendering():
    design = SimpleNamespace(
        get_variants=lambda: ["alternate"],
        project=SimpleNamespace(variants={"alternate": {"variations": [{"Designator": "U1", "Kind": "2"}]}}),
    )
    with pytest.raises(ValueError, match="alternate 3D model resolution"):
        illustration_variants(design, variant="alternate")


def test_variant_parameters_are_applied_without_mutating_saved_components():
    from altium_monkey.altium_pcb_component import AltiumPcbComponent

    design = SimpleNamespace(
        get_variants=lambda: ["production"],
        project=SimpleNamespace(variants={"production": {
            "parameters": [{"ParameterName": "Revision", "Value": "B"}],
        }}),
        get_pcb_project_parameters=lambda: {"Revision": "A", "VariantName": "saved"},
        get_variant_parameter_overrides=lambda name: {"R1": {"Value": "20k"}},
    )
    component = AltiumPcbComponent("R1", "0603", "TOP", "0mil", "0mil", parameters={"Value": "10k"})
    saved = SimpleNamespace(components=[component], pads=[object()])
    variant = illustration_variants(design, variant="production")[0]
    rendered = variant.board(saved)
    assert variant.project_parameters == {"Revision": "B", "VariantName": "production"}
    assert rendered.components[0].parameters == {"Value": "20k"}
    assert saved.components[0].parameters == {"Value": "10k"}
    assert rendered.pads is saved.pads


@pytest.mark.parametrize("level", ["INFO", "DEBUG", "WARNING"])
def test_svg_job_reports_progress_and_writes_timings(tmp_path, monkeypatch, caplog, level):
    caplog.set_level(level)
    import json
    from altium_monkey.altium_board import AltiumBoard, AltiumBoardOutline
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc
    from altium_cruncher import altium_cruncher_cmd_toon as toon
    from altium_cruncher import pcb_illustration_workflow as workflow
    from altium_cruncher.altium_cruncher_pcb_workflow import CruncherPcbRenderInput

    source = tmp_path / "board.PrjPcb"
    source.write_text("fixture context supplied below")
    pcb = AltiumPcbDoc()
    pcb.board = AltiumBoard(outline=AltiumBoardOutline.rectangle_mils(
        left_mils=0, bottom_mils=0, right_mils=1000, top_mils=1000))
    design = SimpleNamespace(get_variants=lambda: [], get_pcb_project_parameters=lambda: {},
                             get_variant_parameter_overrides=lambda name: {})
    def load_preview(path, *, load_schematics):
        assert load_schematics is False
        return design, "test"
    monkeypatch.setattr(workflow, "load_design_for_pcb_input", load_preview)
    monkeypatch.setattr(workflow, "iter_pcb_render_inputs", lambda *a, **k: [CruncherPcbRenderInput("board", source, pcb, {})])
    output, timing = tmp_path / "output", tmp_path / "timing.json"
    assert toon.cmd_toon(_args(str(source), "-o", str(output), "--timings", str(timing))) == 0
    assert len(list(output.glob("*.svg"))) == 2
    assert not list(output.glob("*.png"))
    report = json.loads(timing.read_text())
    assert report["schema"] == "pcb.svg.timings.a0"
    assert report["events"][0]["stage"] == "job"
    assert not report["events"][0]["failed"]
    assert not any(e["stage"] == "raster" for e in report["events"])

    for message in ("Loading project/board context", "Loading selected PCB documents", "Rendering board / base / top", "Wrote SVG", "Success: wrote 2 SVG files"):
        assert (message in caplog.text) == (level != "WARNING")
    for message in ("Loaded design context", "Variant base", "Render timing layer", "SVG native workers", "SVG disk cache"):
        assert (message in caplog.text) == (level == "DEBUG")
    if level != "WARNING":
        assert caplog.records[-1].message == f"Success: wrote 2 SVG files to {output}"


@pytest.mark.parametrize("failure_stage", ["render", "finish", "write_timings"])
def test_failed_toon_job_does_not_report_success(tmp_path, monkeypatch, caplog, failure_stage):
    import json
    from altium_cruncher import altium_cruncher_cmd_toon as toon

    caplog.set_level("INFO")
    def fail(*args, **kwargs):
        raise OSError("fixture failure")
    monkeypatch.setattr(toon, "_cmd_toon", fail if failure_stage == "render" else lambda *a: "Success: wrote SVG files")
    if failure_stage != "render":
        monkeypatch.setattr(toon.PcbSvgRenderJob, failure_stage, fail)
    timing = tmp_path / "timings.json"
    assert toon.cmd_toon(_args("--no-cache", "--timings", str(timing))) == 1
    assert "fixture failure" in caplog.text
    assert "Success:" not in caplog.text
    if failure_stage != "write_timings":
        assert json.loads(timing.read_text())["events"][0]["failed"] is True
