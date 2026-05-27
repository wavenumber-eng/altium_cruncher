"""Fixture-backed CLI workflow tests for public commands."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from altium_cruncher.output_path_templates import resolve_output_relative_path
from altium_monkey.altium_design import AltiumDesign


def _project_root() -> Path:
    """Find the repository root from this test file."""
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Could not locate repository root")


PACKAGE_ROOT = _project_root()
HYDROSCOPE_DIR = PACKAGE_ROOT / "examples" / "assets" / "projects" / "hydroscope"
HYDROSCOPE_PROJECT = HYDROSCOPE_DIR / "Hydroscope.PrjPcb"
HYDROSCOPE_SCHDOC = HYDROSCOPE_DIR / "CPU.SchDoc"
HYDROSCOPE_SCHLIB = HYDROSCOPE_DIR / "Hydroscope.SCHLIB"
HYDROSCOPE_PCBDOC = HYDROSCOPE_DIR / "TZ-SB-0001-PCB-[A] (HydroScope Mainboard).PcbDoc"
RT_SUPER_C1_INTLIB = (
    PACKAGE_ROOT / "tests" / "assets" / "intlib" / "rt_super_c1" / "input"
    / "RT_SUPER_C1.IntLib"
)
CUTOUTS_DIR = PACKAGE_ROOT / "tests" / "assets" / "projects" / "cutouts"
CUTOUTS_PCBDOC = CUTOUTS_DIR / "input" / "cutout_multiple.PcbDoc"
CRICKET_NODE_DIR = PACKAGE_ROOT / "tests" / "assets" / "projects" / "cricket-node"
CRICKET_NODE_PCBDOC = CRICKET_NODE_DIR / "input" / "cricket-node-hw__B.PcbDoc"


def _run_cli(*args: str) -> str:
    """Run Altium Cruncher and return combined output."""
    completed = subprocess.run(
        [sys.executable, "-m", "altium_cruncher", *args],
        cwd=PACKAGE_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    combined = completed.stdout + completed.stderr
    assert completed.returncode == 0, combined
    assert "Traceback" not in combined
    assert "Logging error" not in combined
    return combined


def test_schematic_and_design_json_commands_use_public_project(tmp_path: Path) -> None:
    """Exercise Sch SVG, BOM, PnP, and netlist commands on Hydroscope."""
    sch_svg_dir = tmp_path / "sch-svg"
    _run_cli("sch-svg", str(HYDROSCOPE_SCHDOC), "-o", str(sch_svg_dir))
    sch_svg = sch_svg_dir / "CPU.svg"
    assert sch_svg.exists()
    assert "<svg" in sch_svg.read_text(encoding="utf-8", errors="ignore")[:200]

    bom_dir = tmp_path / "bom"
    _run_cli(
        "bom",
        str(HYDROSCOPE_PROJECT),
        "--format",
        "generic-json",
        "-o",
        str(bom_dir),
    )
    bom_payload = json.loads((bom_dir / "Hydroscope_bom.json").read_text(encoding="utf-8"))
    assert bom_payload["schema"] == "wn.altium_cruncher.bom.v1"
    assert bom_payload["component_count"] >= 100

    pnp_dir = tmp_path / "pnp"
    _run_cli("pnp", str(HYDROSCOPE_PROJECT), "--format", "json", "-o", str(pnp_dir))
    pnp_payload = json.loads((pnp_dir / "Hydroscope_pnp.json").read_text(encoding="utf-8"))
    assert pnp_payload["units"] == "mm"
    assert len(pnp_payload["placements"]) >= 100

    netlist_dir = tmp_path / "netlist"
    _run_cli("netlist", str(HYDROSCOPE_PROJECT), "-o", str(netlist_dir))
    netlist_payload = json.loads(
        (netlist_dir / "Hydroscope_netlist.json").read_text(encoding="utf-8")
    )
    assert len(netlist_payload["components"]) >= 100
    assert len(netlist_payload["nets"]) >= 100


def test_bom_pnp_config_and_jlc_command_use_public_project(tmp_path: Path) -> None:
    """Exercise shared BOM/PnP config and paired JLC outputs."""
    config_path = tmp_path / "bom.config"
    _run_cli("bom", "--write-config", str(config_path))
    config_payload = json.loads(config_path.read_text(encoding="utf-8"))
    assert config_payload["schema"] == "wn.altium_cruncher.bom.config.v1"

    bom_root = tmp_path / "configured-bom"
    _run_cli("bom", str(HYDROSCOPE_PROJECT), "--config", str(config_path), "-o", str(bom_root))
    assert (bom_root / "bom" / "Hydroscope_base_raw-json.json").exists()
    assert (bom_root / "bom" / "Hydroscope_base_grouped-xlsx.xlsx").exists()
    assert (bom_root / "bom" / "bom.config.used.json").exists()

    pnp_root = tmp_path / "configured-pnp"
    _run_cli("pnp", str(HYDROSCOPE_PROJECT), "--config", str(config_path), "-o", str(pnp_root))
    assert (pnp_root / "pnp" / "Hydroscope_base_json.json").exists()
    assert (pnp_root / "pnp" / "Hydroscope_base_csv.csv").exists()
    assert (pnp_root / "pnp" / "bom.config.used.json").exists()

    jlc_root = tmp_path / "jlc"
    _run_cli("jlc", str(HYDROSCOPE_PROJECT), "--config", str(config_path), "-o", str(jlc_root))
    assert (jlc_root / "jlc" / "Hydroscope_base_jlc-xlsx.xlsx").exists()
    assert (jlc_root / "jlc" / "Hydroscope_base_jlc-cpl-xlsx.xlsx").exists()
    assert (jlc_root / "jlc" / "bom.config.used.json").exists()


def test_output_path_template_uses_public_project_parameters() -> None:
    """Resolve a release-style output folder from a real public PrjPcb fixture."""
    design = AltiumDesign.from_prjpcb(HYDROSCOPE_PROJECT)
    assert design.project is not None

    resolved = resolve_output_relative_path(
        "'releases/' + PCB_VERSION + '/' + CCA_PART_NUMBER + ' - ' + "
        "PCB_TITLE + ' - ' + VariantName",
        design.project.parameters,
        variant_name="A",
    )

    assert str(resolved) == (
        "releases/A/TZ-SB-0001 - Sonic Density Sensor Mainboard - A"
    )


def test_library_extract_split_merge_commands_use_public_fixtures(tmp_path: Path) -> None:
    """Exercise library extraction plus split/merge on public Hydroscope files."""
    extract_dir = tmp_path / "extract"
    _run_cli("extract", str(HYDROSCOPE_SCHDOC), "--combined", "-o", str(extract_dir))
    extracted = extract_dir / "CPU.SchLib"
    assert extracted.exists()
    assert extracted.stat().st_size > 0

    split_dir = tmp_path / "split"
    _run_cli("split", str(HYDROSCOPE_SCHLIB), "-o", str(split_dir), "--symbols", "SMT_TEST")
    split_file = split_dir / "SMT_TEST.SchLib"
    assert split_file.exists()
    assert split_file.stat().st_size > 0

    merge_dir = tmp_path / "merge"
    _run_cli("merge", str(split_dir), "-o", str(merge_dir))
    merged_files = list(merge_dir.glob("*.SchLib"))
    assert len(merged_files) == 1
    assert merged_files[0].stat().st_size > 0


def test_intlib_extract_command_uses_public_fixture(tmp_path: Path) -> None:
    """Exercise IntLib source extraction on a redistributable fixture."""
    output_dir = tmp_path / "intlib"

    _run_cli("extract", str(RT_SUPER_C1_INTLIB), "-o", str(output_dir))

    manifest = json.loads(
        (output_dir / "RT_SUPER_C1_intlib_extract_manifest.json").read_text(
            encoding="utf-8"
        )
    )
    assert manifest["schema"] == "wn.altium_cruncher.extract.intlib.v1"
    assert manifest["source_count"] == 2
    assert sorted(source["kind"] for source in manifest["sources"]) == [
        "PCBLib",
        "SchLib",
    ]
    assert (output_dir / "SchLib" / "RT_SUPER_C1.SCHLIB").exists()
    assert (output_dir / "PCBLib" / "RT_SUPER_C1.PcbLib").exists()
    assert (output_dir / "RT_SUPER_C1.LibPkg").exists()


def test_pcb_svg_command_uses_public_pcbdoc_without_private_context(tmp_path: Path) -> None:
    """Exercise pcb-svg against a copied public PcbDoc and explicit config."""
    pcbdoc = tmp_path / "board.PcbDoc"
    shutil.copy2(HYDROSCOPE_PCBDOC, pcbdoc)
    config = tmp_path / "pcb.svg.config"
    config.write_text(
        json.dumps(
            {
                "schema": "pcb.svg.config.a0",
                "global": {
                    "include_metadata": True,
                    "show_empty_layers": False,
                },
                "layer_outputs": {
                    "enabled": True,
                    "layers": ["TOP"],
                    "include_special_layers": ["BOARD_OUTLINE", "DRILLS", "SLOTS"],
                },
                "views": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    output_dir = tmp_path / "pcb-svg"
    _run_cli(
        "pcb-svg",
        str(pcbdoc),
        "--config",
        str(config),
        "--export",
        "outline",
        "-o",
        str(output_dir),
    )

    manifest = json.loads((output_dir / "board__views.json").read_text(encoding="utf-8"))
    assert manifest["schema"] == "pcb.svg.manifest.a0"
    assert manifest["board"] == "board"
    assert (output_dir / "layers" / "board__TOP.svg").exists()


def test_pcb_svg_assembly_views_use_geometer_hlr(tmp_path: Path) -> None:
    """Exercise assembly top/bottom SVG views with geometer-backed HLR enabled."""
    pcbdoc = tmp_path / "board.PcbDoc"
    shutil.copy2(HYDROSCOPE_PCBDOC, pcbdoc)
    config = tmp_path / "pcb.svg.config"
    config.write_text(
        json.dumps(
            {
                "schema": "pcb.svg.config.a0",
                "global": {
                    "include_metadata": True,
                    "styles": {
                        "assembly_hlr": {
                            "curve_mode": "polyline",
                        }
                    },
                },
                "layer_outputs": {
                    "enabled": False,
                },
                "views": [
                    {
                        "name": "assembly_top_view",
                        "enabled": True,
                        "group_id": "pcb-svg-view-assembly-top",
                        "output_svg": "assembly_top_view/{board}__assembly_top_view.svg",
                        "layers": ["BOARD_OUTLINE", "TOP", "ASSEMBLY_HLR_TOP"],
                        "assembly_hlr_mode": "simple",
                    },
                    {
                        "name": "assembly_bottom_view",
                        "enabled": True,
                        "group_id": "pcb-svg-view-assembly-bottom",
                        "output_svg": "assembly_bottom_view/{board}__assembly_bottom_view.svg",
                        "layers": ["BOARD_OUTLINE", "BOTTOM", "ASSEMBLY_HLR_BOTTOM"],
                        "assembly_hlr_mode": "simple",
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    output_dir = tmp_path / "pcb-svg-assembly"
    _run_cli("pcb-svg", str(pcbdoc), "--config", str(config), "-o", str(output_dir))

    top_svg = (
        output_dir / "assembly_top_view" / "board__assembly_top_view.svg"
    ).read_text(encoding="utf-8")
    assert (output_dir / "assembly_bottom_view" / "board__assembly_bottom_view.svg").exists()
    assert 'id="assembly-overlay"' in top_svg
    assert 'data-assembly-symbol="simple"' in top_svg
    assert 'data-layer-id="1"' in top_svg
    assert 'id="layer-TOPOVERLAY"' not in top_svg


def test_pcb_svg_copper_polygon_style_colors_shape_based_regions(
    tmp_path: Path,
) -> None:
    """Verify A0 copper polygon color applies to linked shape-based regions."""
    config = tmp_path / "pcb.svg.config"
    config.write_text(
        json.dumps(
            {
                "schema": "pcb.svg.config.a0",
                "global": {
                    "canvas": {"bounds": "board_outline", "margin_mm": 0.5},
                    "styles": {
                        "copper_traces": {"color": "#111111"},
                        "copper_polygons": {"color": "#12AB34"},
                    }
                },
                "layer_outputs": {"enabled": False},
                "views": [
                    {
                        "name": "top_view",
                        "enabled": True,
                        "output_svg": "views/{board}__top_view.svg",
                        "layers": ["TOP"],
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    output_dir = tmp_path / "pcb-svg"

    _run_cli("pcb-svg", str(CRICKET_NODE_PCBDOC), "--config", str(config), "-o", str(output_dir))

    top_svg = (output_dir / "views" / "cricket-node-hw__B__top_view.svg").read_text(
        encoding="utf-8"
    )
    assert 'data-primitive="shapebased-region"' in top_svg
    assert 'fill="#12AB34" fill-rule="evenodd" stroke="none" data-primitive="shapebased-region"' in top_svg
    assert 'fill="#000000" fill-rule="evenodd" stroke="none" data-primitive="shapebased-region"' not in top_svg
    assert 'data-canvas-bounds-mode="board_outline"' in top_svg
    assert '"canvas":{"altium_origin_mils":' in top_svg
    assert '"x_absolute_mils":' in top_svg
    assert '"x_origin_relative_mils":' in top_svg
    view_box_match = re.search(r'viewBox="0 0 ([0-9.]+) ([0-9.]+)"', top_svg)
    assert view_box_match is not None
    assert float(view_box_match.group(1)) < 100.0


def test_pcb_svg_cutout_layer_uses_configured_hashes(tmp_path: Path) -> None:
    """Exercise the cutout fixture with dashed outlines and configured hashes."""
    config = tmp_path / "pcb.svg.config"
    config.write_text(
        json.dumps(
            {
                "schema": "pcb.svg.config.a0",
                "global": {
                    "include_metadata": True,
                    "styles": {
                        "board_cutouts": {
                            "enabled": True,
                            "hatch": True,
                            "hatch_spacing_mm": 1.25,
                            "hatch_angle_deg": 30,
                            "hatch_line_width_mm": 0.12,
                            "outline_style": "dashed",
                            "outline_dash_mm": 0.9,
                            "outline_width_mm": 0.33,
                        }
                    },
                },
                "layer_outputs": {
                    "enabled": True,
                    "layers": ["BOARD_CUTOUTS"],
                    "include_special_layers": ["BOARD_OUTLINE"],
                },
                "views": [
                    {
                        "name": "top_view",
                        "enabled": True,
                        "output_svg": "top_view/{board}__top_view.svg",
                        "layers": ["BOARD_OUTLINE", "TOP", "BOARD_CUTOUTS"],
                    },
                    {
                        "name": "bottom_view",
                        "enabled": True,
                        "output_svg": "bottom_view/{board}__bottom_view.svg",
                        "layers": ["BOARD_OUTLINE", "BOTTOM", "BOARD_CUTOUTS"],
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    output_dir = CUTOUTS_DIR / "output" / "pcb-svg" / "cutout-layer"

    _run_cli("pcb-svg", str(CUTOUTS_PCBDOC), "--config", str(config), "-o", str(output_dir))

    cutout_svg_path = output_dir / "layers" / "cutout_multiple__BOARD_CUTOUTS.svg"
    cutout_svg = cutout_svg_path.read_text(encoding="utf-8")
    assert cutout_svg.count('data-feature="board-cutout"') == 4
    assert 'width="1.25" height="1.25"' in cutout_svg
    assert 'patternTransform="rotate(30)"' in cutout_svg
    assert 'stroke-width="0.12"' in cutout_svg
    assert 'stroke-dasharray="0.9 0.9"' in cutout_svg
    assert 'stroke-width="0.33"' in cutout_svg
    assert ">cutout</text>" not in cutout_svg
    for view_folder in ("top_view", "bottom_view"):
        view_svg = (
            output_dir / view_folder / f"cutout_multiple__{view_folder}.svg"
        ).read_text(encoding="utf-8")
        assert 'id="board-cutout-hatch"' in view_svg
        assert 'width="1.25" height="1.25"' in view_svg
        assert 'patternTransform="rotate(30)"' in view_svg
        assert 'stroke-dasharray="0.9 0.9"' in view_svg
        assert 'stroke-width="0.33"' in view_svg


def test_clean_command_creates_template_for_public_schdoc_copy(tmp_path: Path) -> None:
    """Exercise clean command template generation without mutating assets."""
    schdoc = tmp_path / "CPU.SchDoc"
    shutil.copy2(HYDROSCOPE_SCHDOC, schdoc)

    _run_cli("clean", str(schdoc))

    config_path = tmp_path / "altium-clean.json"
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    assert payload["schema"] == "wn.altium.clean.config.v1"
