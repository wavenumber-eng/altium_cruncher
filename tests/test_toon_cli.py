"""Focused toon command, export, config and variant contracts."""

import argparse
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest

from altium_cruncher.altium_cruncher_cmd_toon import (
    TOON_CONFIG_FILENAME,
    _cmd_toon,
    _resolve_config,
    register_parser,
)
from altium_cruncher.config_json import load_json_config
from altium_cruncher.pcb_illustration_config import resolve_illustration_config
from altium_cruncher.pcb_illustration_variants import illustration_variants
from altium_cruncher.toon_gallery import (
    _ToonGalleryArtifact,
    write_toon_gallery,
)

ROOT = Path(__file__).resolve().parents[1]


def _args(*tokens):
    parser = argparse.ArgumentParser()
    register_parser(parser.add_subparsers())
    return parser.parse_args(["toon", *tokens])


@pytest.mark.parametrize(
    "tokens",
    [
        ("--format", "svg"),
        ("--format", "png"),
        ("--format", "both"),
        ("--dpi", "300"),
        ("--width", "4096"),
        ("--background", "transparent"),
    ],
)
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
    assert _args().warning_mode == "summary"
    assert _args().warning_report is None
    assert _args("--warnings", "all").warning_mode == "all"
    assert _args("--warnings", "none").warning_mode == "none"
    assert _args("--warning-report", str(tmp_path / "warnings.json")).warning_report == (
        tmp_path / "warnings.json"
    )
    assert _args().workers == 4
    assert not _args().gallery and not _args().open_gallery
    assert _args("--gallery").gallery
    assert _args("--open").open_gallery
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


def test_toon_gallery_centers_current_rendered_artifacts(tmp_path):
    output = tmp_path / "toon"
    top = output / "base" / "board top.svg"
    bottom = output / "production" / "board-bottom.svg"
    stale = output / "stale.svg"
    top.parent.mkdir(parents=True)
    bottom.parent.mkdir(parents=True)
    top.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>', encoding="utf-8")
    bottom.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>', encoding="utf-8")
    stale.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>', encoding="utf-8")

    gallery = write_toon_gallery(
        output,
        [
            _ToonGalleryArtifact(top, "control", "main", None, "top", "top"),
            _ToonGalleryArtifact(
                bottom, "control", "main", "Production", "bottom", "bottom"
            ),
        ],
    )

    text = gallery.read_text(encoding="utf-8")
    assert gallery == output / "index.html"
    assert "align-items: center; justify-content: center" in text
    assert "object-position: center center" in text
    assert "grid-template-columns: minmax(0, 1fr)" in text
    assert "base/board%20top.svg?v=" in text
    assert "stale.svg" not in text
    assert "control · main · Base" in text
    assert "control · main · Production" in text
    assert text.count("Open raw SVG") == 2


def test_toon_open_writes_gallery_and_uses_default_browser(tmp_path, monkeypatch):
    from altium_cruncher import altium_cruncher_cmd_toon as toon

    source = tmp_path / "board.PrjPcb"
    source.write_text("fixture", encoding="utf-8")
    output = tmp_path / "output"
    svg = output / "board__top.svg"
    svg.parent.mkdir(parents=True)
    svg.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>', encoding="utf-8")
    artifact = _ToonGalleryArtifact(svg, "board", "board", None, "top", "top")
    monkeypatch.setattr(toon, "render_project", lambda *args, **kwargs: [artifact])
    opened: list[str] = []
    monkeypatch.setattr(
        toon.webbrowser,
        "open_new_tab",
        lambda uri: opened.append(uri) or True,
    )

    summary = _cmd_toon(
        _args(str(source), "-o", str(output), "--open"),
        SimpleNamespace(),
    )

    gallery = output / "index.html"
    assert gallery.is_file()
    assert opened == [gallery.resolve().as_uri()]
    assert summary == f"Success: wrote 1 SVG file to {output.resolve()}"


def test_toon_gallery_options_are_rejected_when_only_writing_config(tmp_path):
    with pytest.raises(ValueError, match="cannot be used"):
        _cmd_toon(
            _args("--write-config", str(tmp_path / "toon.jsonc"), "--gallery"),
            SimpleNamespace(),
        )


@pytest.mark.parametrize(
    ("theme", "mask", "silk"),
    [
        ("saved", "auto", "#F5F5F5"),
        ("white", "#EEEEEE", "#000000"),
        ("black", "#000000", "#F5F5F5"),
        ("blue", "#1D4F91", "#F5F5F5"),
        ("red", "#A62A2A", "#F5F5F5"),
        ("purple", "#6F3C8A", "#F5F5F5"),
        ("yellow", "#D6A600", "#F5F5F5"),
        ("green", "#176B3A", "#F5F5F5"),
    ],
)
def test_common_mask_and_silk_themes(theme, mask, silk):
    assert _args("--theme", theme).theme == theme
    config = resolve_illustration_config(side="top", theme=theme)
    styles = config.resolved_styles_for_view(config.enabled_views()[0])
    assert styles["soldermask_film"]["color"] == mask
    assert styles["silkscreen_board_graphics"]["color"] == silk


def test_public_toon_command_writes_editable_substrate_preset(tmp_path):
    target = tmp_path / "toon.config"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "toon",
            "--write-config",
            str(target),
        ],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    config = load_json_config(target)
    assert config["schema"] == "pcb.svg.config.a1"
    assert [v["group_id"] for v in config["views"]] == ["toon-top", "toon-bottom"]
    assert all(v["layers"][0] == "BOARD_SUBSTRATE" for v in config["views"])
    substrate = config["global"]["styles"]["board_substrate"]
    assert substrate["color"] == "auto"
    assert substrate["rigid_color"] == "#B6A26B"
    assert substrate["flex_color"] == "#D18B28"
    assert config["global"]["styles"]["silkscreen_surface"]["clip_mode"] == "film"


def test_config_accepts_partial_settings_and_custom_views():
    config = resolve_illustration_config(
        {
            "global": {"styles": {"illustration": {"opacity": 0.3}}},
            "views": [{"name": "custom", "layers": ["ILLUSTRATION_BOTTOM"]}],
        },
        side="bottom",
    )
    assert config.views[0].name == "custom"
    assert (
        config.resolved_styles_for_view(config.views[0])["illustration"]["opacity"]
        == 0.3
    )
    with pytest.raises(ValueError, match="exactly one"):
        resolve_illustration_config({"views": [{"name": "copper", "layers": ["TOP"]}]})


def test_rt_variants_read_dnp_and_leave_project_unchanged():
    from altium_monkey.altium_design import AltiumDesign
    from altium_monkey.altium_prjpcb import AltiumPrjPcb

    project = AltiumPrjPcb(
        ROOT / "tests/assets/projects/rt_super_c1/input/RT_SUPER_C1.PrjPcb"
    )
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
        project=SimpleNamespace(
            variants={"alternate": {"variations": [{"Designator": "U1", "Kind": "2"}]}}
        ),
    )
    with pytest.raises(ValueError, match="alternate 3D model resolution"):
        illustration_variants(design, variant="alternate")


def test_variant_parameters_are_applied_without_mutating_saved_components():
    from altium_monkey.altium_pcb_component import AltiumPcbComponent

    design = SimpleNamespace(
        get_variants=lambda: ["production"],
        project=SimpleNamespace(
            variants={
                "production": {
                    "parameters": [{"ParameterName": "Revision", "Value": "B"}],
                }
            }
        ),
        get_pcb_project_parameters=lambda: {"Revision": "A", "VariantName": "saved"},
        get_variant_parameter_overrides=lambda name: {"R1": {"Value": "20k"}},
    )
    component = AltiumPcbComponent(
        "R1", "0603", "TOP", "0mil", "0mil", parameters={"Value": "10k"}
    )
    saved = SimpleNamespace(components=[component], pads=[object()])
    variant = illustration_variants(design, variant="production")[0]
    rendered = variant.board(saved)
    assert variant.project_parameters == {"Revision": "B", "VariantName": "production"}
    assert rendered.components[0].parameters == {"Value": "20k"}
    assert saved.components[0].parameters == {"Value": "10k"}
    assert rendered.pads is saved.pads


@pytest.mark.parametrize("level", ["INFO", "DEBUG", "WARNING"])
def test_svg_job_reports_progress_and_writes_timings(
    tmp_path, monkeypatch, caplog, level
):
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
    pcb.board = AltiumBoard(
        outline=AltiumBoardOutline.rectangle_mils(
            left_mils=0, bottom_mils=0, right_mils=1000, top_mils=1000
        )
    )
    design = SimpleNamespace(
        get_variants=lambda: [],
        get_pcb_project_parameters=lambda: {},
        get_variant_parameter_overrides=lambda name: {},
    )

    def load_preview(path, *, load_schematics):
        assert load_schematics is False
        return design, "test"

    monkeypatch.setattr(workflow, "load_design_for_pcb_input", load_preview)
    monkeypatch.setattr(
        workflow,
        "iter_pcb_render_inputs",
        lambda *a, **k: [CruncherPcbRenderInput("board", source, pcb, {})],
    )
    output, timing = tmp_path / "output", tmp_path / "timing.json"
    assert (
        toon.cmd_toon(_args(str(source), "-o", str(output), "--timings", str(timing)))
        == 0
    )
    assert len(list(output.glob("*.svg"))) == 2
    assert not list(output.glob("*.png"))
    report = json.loads(timing.read_text())
    assert report["schema"] == "pcb.svg.timings.a0"
    assert report["events"][0]["stage"] == "job"
    assert not report["events"][0]["failed"]
    assert not any(e["stage"] == "raster" for e in report["events"])

    for message in (
        "Loading project/board context",
        "Loading selected PCB documents",
        "Rendering board / base / top",
        "Wrote SVG",
        "Success: wrote 2 SVG files",
    ):
        assert (message in caplog.text) == (level != "WARNING")
    for message in (
        "Loaded design context",
        "Variant base",
        "Render timing layer",
        "SVG native workers",
        "SVG disk cache",
    ):
        assert (message in caplog.text) == (level == "DEBUG")
    if level != "WARNING":
        assert caplog.records[-1].message == f"Success: wrote 2 SVG files to {output}"


@pytest.mark.parametrize(
    ("warning_mode", "expected_detail"),
    [("summary", False), ("all", True), ("none", False)],
)
def test_toon_queues_warnings_until_completion_and_can_write_report(
    tmp_path, monkeypatch, caplog, warning_mode, expected_detail
):
    import json
    from altium_cruncher import altium_cruncher_cmd_toon as toon

    caplog.set_level("INFO")
    report_path = tmp_path / f"{warning_mode}.json"

    def render(_args, render_job):
        assert "Nonfatal warnings" not in caplog.text
        render_job.diagnose(
            code="missing-renderable-model",
            category="missing_model",
            producer="altium-cruncher",
            message="U1: fitted component has no renderable 3D model",
            component_designator="U1",
            source_scoped=True,
            occurrence_key="component:U1",
        )
        assert "missing-renderable-model" not in caplog.text
        return "Success: fixture"

    monkeypatch.setattr(toon, "_cmd_toon", render)
    args = _args(
        "--no-cache",
        "--warnings",
        warning_mode,
        "--warning-report",
        str(report_path),
    )

    assert toon.cmd_toon(args) == 0
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["schema"] == "toon.warning_report.a0"
    assert payload["summary"]["unique_diagnostic_count"] == 1
    assert payload["diagnostics"][0]["component_designator"] == "U1"
    assert ("Nonfatal warnings: 1 unique" in caplog.text) == (
        warning_mode != "none"
    )
    assert (
        "U1: fitted component has no renderable 3D model" in caplog.text
    ) == expected_detail
    assert caplog.records[-1].message == "Success: fixture"


@pytest.mark.parametrize("failure_stage", ["render", "finish", "write_timings"])
def test_failed_toon_job_does_not_report_success(
    tmp_path, monkeypatch, caplog, failure_stage
):
    import json
    from altium_cruncher import altium_cruncher_cmd_toon as toon

    caplog.set_level("INFO")

    def fail(*args, **kwargs):
        raise OSError("fixture failure")

    monkeypatch.setattr(
        toon,
        "_cmd_toon",
        fail if failure_stage == "render" else lambda *a: "Success: wrote SVG files",
    )
    if failure_stage != "render":
        monkeypatch.setattr(toon.PcbSvgRenderJob, failure_stage, fail)
    timing = tmp_path / "timings.json"
    assert toon.cmd_toon(_args("--no-cache", "--timings", str(timing))) == 1
    assert "fixture failure" in caplog.text
    assert "Success:" not in caplog.text
    if failure_stage != "write_timings":
        assert json.loads(timing.read_text())["events"][0]["failed"] is True
