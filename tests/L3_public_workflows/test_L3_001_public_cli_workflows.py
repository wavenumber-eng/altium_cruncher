"""Fixture-backed CLI workflow tests for public commands."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

from jsonschema import Draft202012Validator

from altium_cruncher.config_json import load_json_config
from altium_cruncher.output_path_templates import resolve_output_relative_path
from altium_monkey.altium_design import AltiumDesign


def _project_root() -> Path:
    """Find the repository root from this test file."""
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Could not locate repository root")


PACKAGE_ROOT = _project_root()
HYDROSCOPE_DIR = PACKAGE_ROOT / "tests" / "assets" / "projects" / "hydroscope" / "input"
HYDROSCOPE_PROJECT = HYDROSCOPE_DIR / "Hydroscope.PrjPcb"
HYDROSCOPE_SCHDOC = HYDROSCOPE_DIR / "CPU.SchDoc"
HYDROSCOPE_SCHLIB = HYDROSCOPE_DIR / "Hydroscope.SCHLIB"
HYDROSCOPE_PCBDOC = HYDROSCOPE_DIR / "TZ-SB-0001-PCB-[A] (HydroScope Mainboard).PcbDoc"
NODE_TEST_ARRAY_DIR = (
    PACKAGE_ROOT / "tests" / "assets" / "projects" / "node_test_array" / "input"
)
NODE_TEST_ARRAY_PROJECT = NODE_TEST_ARRAY_DIR / "11-10077__node-test-array__B4.PrjPcb"
RT_SUPER_C1_INTLIB = (
    PACKAGE_ROOT
    / "tests"
    / "assets"
    / "intlib"
    / "rt_super_c1"
    / "input"
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


def _svg_tree_by_page(
    paths: list[Path],
) -> dict[str, tuple[ET.Element, dict[str, ET.Element]]]:
    pages: dict[str, tuple[ET.Element, dict[str, ET.Element]]] = {}
    for path in paths:
        root = ET.parse(path).getroot()
        page_ref = root.attrib.get("data-page-occurrence-ref", "")
        assert page_ref, path
        assert page_ref not in pages, page_ref
        elements = {
            element.attrib["id"]: element
            for element in root.iter()
            if element.attrib.get("id")
        }
        pages[page_ref] = (root, elements)
    return pages


def _assert_compiled_graph_svg_closure(
    graph: dict[str, object],
    svg_pages: dict[str, tuple[ET.Element, dict[str, ET.Element]]],
) -> None:
    raw_links = graph["graphical_artifact_links"]
    assert isinstance(raw_links, list)
    links = [link for link in raw_links if isinstance(link, dict)]
    assert links
    assert {str(link["artifact_key"]) for link in links} == {"sch.dwg_scene"}

    for link in links:
        page_ref = str(link["page_occurrence_ref"])
        element_id = str(link["element_id"])
        target_type = str(link["target_type"])
        target_ref = str(link["target_ref"])
        root, elements = svg_pages[page_ref]
        assert root.attrib["data-artifact-key"] == "sch.dwg_scene"
        element = elements[element_id]
        assert element.attrib["data-page-occurrence-ref"] == page_ref
        assert element.attrib["data-artifact-key"] == "sch.dwg_scene"
        assert element.attrib["data-element-id"] == element_id
        assert element.attrib["data-graph-target-type"] == target_type
        assert element.attrib["data-graph-target-ref"] == target_ref


def _load_schematic_svg_bundle(
    output_dir: Path,
) -> tuple[
    dict[str, object],
    dict[str, object],
    dict[str, tuple[ET.Element, dict[str, ET.Element]]],
]:
    manifest = json.loads(
        (output_dir / "schematic_svg_manifest.json").read_text(encoding="utf-8")
    )
    schema = json.loads(
        (
            PACKAGE_ROOT
            / "docs"
            / "contracts"
            / "schematic_svg_manifest.b0.schema.json"
        ).read_text(encoding="utf-8")
    )
    Draft202012Validator(schema).validate(manifest)
    design_payload = json.loads(
        (output_dir / manifest["design_json"]).read_text(encoding="utf-8")
    )
    svg_pages = _svg_tree_by_page(
        [output_dir / entry["file"] for entry in manifest["svgs"]]
    )
    assert manifest["design_schema"] == design_payload["schema"]
    assert (
        manifest["compiled_schematic_graph_schema"]
        == (design_payload["compiled_schematic_graph"]["schema"])
    )
    return manifest, design_payload, svg_pages


def test_cli_help_mentions_intlib_extract_support() -> None:
    help_text = _run_cli("--help")

    assert "extract symbols, footprints, or IntLib sources" in help_text


def test_schematic_and_design_json_commands_use_public_project(tmp_path: Path) -> None:
    """Exercise Sch SVG, BOM, PnP, and design JSON commands on Hydroscope."""
    sch_svg_dir = tmp_path / "sch-svg"
    _run_cli("sch-svg", str(HYDROSCOPE_SCHDOC), "-o", str(sch_svg_dir))
    standalone_manifest, standalone_design, standalone_svg_pages = (
        _load_schematic_svg_bundle(sch_svg_dir)
    )
    standalone_graph = standalone_design["compiled_schematic_graph"]
    assert standalone_manifest["input"] == "CPU.SchDoc"
    assert len(standalone_graph["page_occurrences"]) == 1
    assert set(standalone_svg_pages) == {
        str(page["id"])
        for page in standalone_graph["page_occurrences"]
        if isinstance(page, dict)
    }
    assert {
        root.attrib["data-enrichment-schema"]
        for root, _elements in standalone_svg_pages.values()
    } == {"altium_cruncher.schematic.svg.enrichment.b0"}
    _assert_compiled_graph_svg_closure(standalone_graph, standalone_svg_pages)

    bom_dir = tmp_path / "bom"
    _run_cli(
        "bom",
        str(HYDROSCOPE_PROJECT),
        "--format",
        "generic-json",
        "-o",
        str(bom_dir),
    )
    bom_payload = json.loads(
        (bom_dir / "Hydroscope_bom.json").read_text(encoding="utf-8")
    )
    assert bom_payload["schema"] == "altium_cruncher.bom.a0"
    assert bom_payload["component_count"] >= 100

    default_bom_dir = tmp_path / "bom-default"
    default_config = tmp_path / "bom-default.config"
    _run_cli(
        "bom",
        str(HYDROSCOPE_PROJECT),
        "--config",
        str(default_config),
        "-o",
        str(default_bom_dir),
    )
    assert default_config.exists()
    assert (default_bom_dir / "bom" / "Hydroscope_base_raw.json").exists()
    assert (default_bom_dir / "bom" / "Hydroscope_base_grouped.xlsx").exists()
    assert not (default_bom_dir / "bom" / "Hydroscope_base_grouped-json.json").exists()

    pnp_dir = tmp_path / "pnp"
    _run_cli("pnp", str(HYDROSCOPE_PROJECT), "--format", "json", "-o", str(pnp_dir))
    pnp_payload = json.loads(
        (pnp_dir / "Hydroscope_pnp.json").read_text(encoding="utf-8")
    )
    assert pnp_payload["units"] == "mm"
    assert len(pnp_payload["placements"]) >= 100

    design_dir = tmp_path / "design"
    _run_cli("design", str(HYDROSCOPE_PROJECT), "-o", str(design_dir))
    design_payload = json.loads(
        (design_dir / "design" / "Hydroscope_design.json").read_text(encoding="utf-8")
    )
    assert design_payload["schema"] == "altium_monkey.design.b0"
    assert len(design_payload["components"]) >= 100
    assert len(design_payload["nets"]) >= 100
    assert "physical_pages" not in design_payload
    assert isinstance(
        design_payload["compiled_schematic_graph"]["page_occurrences"], list
    )
    assert design_payload["indexes"]["svg_to_component"]

    project_svg_dir = tmp_path / "project-sch-svg"
    _run_cli("sch-svg", str(HYDROSCOPE_PROJECT), "-o", str(project_svg_dir))
    project_manifest, project_design, project_svg_pages = _load_schematic_svg_bundle(
        project_svg_dir
    )
    graph = design_payload["compiled_schematic_graph"]
    assert project_manifest["input"] == HYDROSCOPE_PROJECT.name
    assert project_design["compiled_schematic_graph"] == graph
    assert set(project_svg_pages) == {
        str(page["id"]) for page in graph["page_occurrences"] if isinstance(page, dict)
    }
    _assert_compiled_graph_svg_closure(graph, project_svg_pages)


def test_combined_svg_command_emits_schematic_graph_and_pcb_outputs(
    tmp_path: Path,
) -> None:
    """Exercise the combined project SVG path across schematic and PCB outputs."""
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
                    "include_special_layers": ["BOARD_OUTLINE"],
                },
                "views": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    output_root = tmp_path / "combined-svg"
    _run_cli(
        "svg",
        str(HYDROSCOPE_PROJECT),
        "--config",
        str(config),
        "-o",
        str(output_root),
    )

    manifest, design_payload, svg_pages = _load_schematic_svg_bundle(
        output_root / "sch-svg"
    )
    graph = design_payload["compiled_schematic_graph"]
    assert manifest["input"] == HYDROSCOPE_PROJECT.name
    assert set(svg_pages) == {
        str(page["id"]) for page in graph["page_occurrences"] if isinstance(page, dict)
    }
    assert {
        root.attrib["data-enrichment-schema"] for root, _elements in svg_pages.values()
    } == {"altium_cruncher.schematic.svg.enrichment.b0"}
    _assert_compiled_graph_svg_closure(graph, svg_pages)

    pcb_output_dir = output_root / "pcb-svg"
    pcb_manifest_paths = sorted(pcb_output_dir.glob("*__views.json"))
    assert pcb_manifest_paths
    for manifest_path in pcb_manifest_paths:
        pcb_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert pcb_manifest["schema"] == "pcb.svg.manifest.a0"
        layer_outputs = pcb_manifest["layer_outputs"]
        assert layer_outputs
        for layer_output in layer_outputs.values():
            assert (pcb_output_dir / layer_output["file"]).is_file()


def test_design_review_bundle_uses_compiled_graph_for_multichannel_project(
    tmp_path: Path,
) -> None:
    """Verify DR emits resolved physical-page SVG/IR artifacts for channel projects."""
    output_dir = tmp_path / "node-test-array-dr"

    _run_cli("dr", str(NODE_TEST_ARRAY_PROJECT), "-o", str(output_dir))

    manifest = json.loads(
        (output_dir / "design_review_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["schema"] == "altium_cruncher.design_review_manifest.b0"
    design_payload = json.loads(
        (output_dir / manifest["design_json"]).read_text(encoding="utf-8")
    )
    graph = design_payload["compiled_schematic_graph"]
    pages = [page for page in graph["page_occurrences"] if isinstance(page, dict)]
    page_ids = {str(page["id"]) for page in pages}
    svg_page_ids = {
        str(entry["page_occurrence_ref"])
        for entry in manifest["schematic_svgs"]
        if isinstance(entry, dict)
    }
    ir_page_ids = {
        str(entry["page_occurrence_ref"])
        for entry in manifest["schematic_irs"]
        if isinstance(entry, dict)
    }

    assert design_payload["schema"] == "altium_monkey.design.b0"
    assert "physical_pages" not in design_payload
    assert len(pages) >= 2
    assert svg_page_ids == page_ids
    assert ir_page_ids == page_ids

    component = next(
        component
        for component in graph["component_occurrences"]
        if isinstance(component, dict)
    )
    component_ref = str(component["id"])
    link = next(
        link
        for link in graph["graphical_artifact_links"]
        if isinstance(link, dict)
        and link.get("target_type") == "sch.component_occurrence"
        and link.get("target_ref") == component_ref
    )
    page_id = str(component["page_occurrence_ref"])
    element_id = str(link["element_id"])
    designator = str(component["physical_designator"])

    indexes = design_payload["indexes"]
    assert designator in indexes["component_to_nets"]

    svg_entry = next(
        entry
        for entry in manifest["schematic_svgs"]
        if entry["page_occurrence_ref"] == page_id
    )
    svg_text = (output_dir / svg_entry["file"]).read_text(encoding="utf-8")
    assert 'data-view-kind="compiled_schematic_page"' in svg_text
    assert f'data-page-occurrence-ref="{page_id}"' in svg_text
    assert f'data-element-id="{element_id}"' in svg_text
    assert f'data-component-occurrence-ref="{component_ref}"' in svg_text
    assert f'data-component="{designator}"' in svg_text

    dr_svg_pages = _svg_tree_by_page(
        [output_dir / entry["file"] for entry in manifest["schematic_svgs"]]
    )
    assert set(dr_svg_pages) == page_ids
    assert {
        root.attrib["data-enrichment-schema"]
        for root, _elements in dr_svg_pages.values()
    } == {"altium_cruncher.schematic.svg.enrichment.b0"}
    _assert_compiled_graph_svg_closure(graph, dr_svg_pages)


def test_bom_pnp_config_and_jlc_command_use_public_project(tmp_path: Path) -> None:
    """Exercise shared BOM/PnP config and paired JLC outputs."""
    config_path = tmp_path / "bom.config"
    _run_cli("bom", "--write-config", str(config_path))
    config_payload = load_json_config(config_path)
    assert config_payload["schema"] == "altium_cruncher.bom.config.a0"

    bom_root = tmp_path / "configured-bom"
    _run_cli(
        "bom",
        str(HYDROSCOPE_PROJECT),
        "--config",
        str(config_path),
        "-o",
        str(bom_root),
    )
    assert (bom_root / "bom" / "Hydroscope_base_raw.json").exists()
    assert (bom_root / "bom" / "Hydroscope_base_grouped.xlsx").exists()
    assert (bom_root / "bom" / "bom.config.used.json").exists()

    pnp_root = tmp_path / "configured-pnp"
    _run_cli(
        "pnp",
        str(HYDROSCOPE_PROJECT),
        "--config",
        str(config_path),
        "-o",
        str(pnp_root),
    )
    assert (pnp_root / "pnp" / "Hydroscope_base.json").exists()
    assert (pnp_root / "pnp" / "Hydroscope_base.csv").exists()
    assert (pnp_root / "pnp" / "bom.config.used.json").exists()

    jlc_root = tmp_path / "jlc"
    _run_cli(
        "jlc",
        str(HYDROSCOPE_PROJECT),
        "--config",
        str(config_path),
        "-o",
        str(jlc_root),
    )
    assert (jlc_root / "jlc" / "Hydroscope_base_jlc.xlsx").exists()
    assert (jlc_root / "jlc" / "Hydroscope_base_jlc-cpl.xlsx").exists()
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

    assert str(resolved) == ("releases/A/TZ-SB-0001 - Hydroscope Mainboard - A")


def test_library_extract_split_merge_commands_use_public_fixtures(
    tmp_path: Path,
) -> None:
    """Exercise library extraction plus split/merge on public Hydroscope files."""
    extract_dir = tmp_path / "extract"
    _run_cli("extract", str(HYDROSCOPE_SCHDOC), "--combined", "-o", str(extract_dir))
    extracted = extract_dir / "CPU.SchLib"
    assert extracted.exists()
    assert extracted.stat().st_size > 0

    split_dir = tmp_path / "split"
    _run_cli(
        "split", str(HYDROSCOPE_SCHLIB), "-o", str(split_dir), "--symbols", "SMT_TEST"
    )
    split_file = split_dir / "SMT_TEST.SchLib"
    assert split_file.exists()
    assert split_file.stat().st_size > 0

    merge_dir = tmp_path / "merge"
    _run_cli("merge", str(split_dir), "-o", str(merge_dir))
    merged_files = list(merge_dir.glob("*.SchLib"))
    assert len(merged_files) == 1
    assert merged_files[0].stat().st_size > 0


def test_pcblib_split_command_sanitizes_windows_invalid_footprint_filename(
    tmp_path: Path,
) -> None:
    """Verify PcbLib split filenames are safe without renaming footprints."""
    from altium_monkey import AltiumPcbLib

    footprint_name = 'HEADER 2x4 .100"'
    source_pcblib = tmp_path / "source.PcbLib"
    pcblib = AltiumPcbLib()
    pcblib.add_footprint(footprint_name)
    pcblib.save(source_pcblib)

    split_dir = tmp_path / "split"
    _run_cli("split", str(source_pcblib), "-o", str(split_dir))

    split_file = split_dir / "HEADER 2x4 .100_.PcbLib"
    assert split_file.exists()

    reloaded = AltiumPcbLib.from_file(split_file)
    assert [footprint.name for footprint in reloaded.footprints] == [footprint_name]


def test_intlib_extract_command_uses_public_fixture(tmp_path: Path) -> None:
    """Exercise IntLib source extraction on a redistributable fixture."""
    from altium_monkey.altium_pcblib import AltiumPcbLib
    from altium_monkey.altium_schlib import AltiumSchLib

    output_dir = tmp_path / "intlib"

    _run_cli("extract", str(RT_SUPER_C1_INTLIB), "-o", str(output_dir))

    manifest = json.loads(
        (output_dir / "RT_SUPER_C1_intlib_extract_manifest.json").read_text(
            encoding="utf-8"
        )
    )
    assert manifest["schema"] == "altium_cruncher.extract.intlib.a0"
    assert manifest["source_count"] == 2
    assert sorted(source["kind"] for source in manifest["sources"]) == [
        "PCBLib",
        "SchLib",
    ]
    assert (output_dir / "SchLib" / "RT_SUPER_C1.SCHLIB").exists()
    assert (output_dir / "PCBLib" / "RT_SUPER_C1.PcbLib").exists()
    assert (output_dir / "RT_SUPER_C1.LibPkg").exists()

    schlib = AltiumSchLib(output_dir / "SchLib" / "RT_SUPER_C1.SCHLIB")
    pcblib = AltiumPcbLib(output_dir / "PCBLib" / "RT_SUPER_C1.PcbLib")
    assert len(schlib.symbols) == manifest["component_count"]
    assert isinstance(pcblib.footprints, list)


def test_pcb_svg_command_uses_public_pcbdoc_without_private_context(
    tmp_path: Path,
) -> None:
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

    manifest = json.loads(
        (output_dir / "board__views.json").read_text(encoding="utf-8")
    )
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
                        "assembly_hlr_mode": "outline",
                    },
                    {
                        "name": "assembly_bottom_view",
                        "enabled": True,
                        "group_id": "pcb-svg-view-assembly-bottom",
                        "output_svg": "assembly_bottom_view/{board}__assembly_bottom_view.svg",
                        "layers": ["BOARD_OUTLINE", "BOTTOM", "ASSEMBLY_HLR_BOTTOM"],
                        "assembly_hlr_mode": "outline",
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
    assert (
        output_dir / "assembly_bottom_view" / "board__assembly_bottom_view.svg"
    ).exists()
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
                    },
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

    _run_cli(
        "pcb-svg",
        str(CRICKET_NODE_PCBDOC),
        "--config",
        str(config),
        "-o",
        str(output_dir),
    )

    top_svg = (output_dir / "views" / "cricket-node-hw__B__top_view.svg").read_text(
        encoding="utf-8"
    )
    assert 'data-primitive="shapebased-region"' in top_svg
    assert (
        'fill="#12AB34" fill-rule="evenodd" stroke="none" data-primitive="shapebased-region"'
        in top_svg
    )
    assert (
        'fill="#000000" fill-rule="evenodd" stroke="none" data-primitive="shapebased-region"'
        not in top_svg
    )
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

    _run_cli(
        "pcb-svg", str(CUTOUTS_PCBDOC), "--config", str(config), "-o", str(output_dir)
    )

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
    config_text = config_path.read_text(encoding="utf-8")
    payload = load_json_config(config_path)
    assert "// Generated by altium-cruncher clean." in config_text
    assert "/* Pin name/designator fonts inside symbols. */" in config_text
    assert payload["schema"] == "altium_cruncher.clean.config.a0"


def test_clean_init_config_writes_templates_without_cleaning(tmp_path: Path) -> None:
    """Exercise explicit clean config generation for schematic and PcbLib types."""
    schematic_config = tmp_path / "sch-clean.json"
    pcblib_config = tmp_path / "pcblib-clean.json"
    fake_schlib = tmp_path / "Vendor.SchLib"

    _run_cli(
        "clean",
        str(fake_schlib),
        "--init-config",
        "--config",
        str(schematic_config),
    )
    _run_cli(
        "clean",
        "--init-config",
        "--config-type",
        "pcblib",
        "--config",
        str(pcblib_config),
    )

    schematic_text = schematic_config.read_text(encoding="utf-8")
    pcblib_text = pcblib_config.read_text(encoding="utf-8")
    assert not fake_schlib.exists()
    assert (
        "/* Use --init-config to write this template without cleaning an input. */"
        in schematic_text
    )
    assert "/* Altium font family name to apply. */" in schematic_text
    assert (
        "/* Text matching mode. Options: all, regex, contains, exact. */" in pcblib_text
    )
    assert (
        load_json_config(schematic_config)["schema"]
        == "altium_cruncher.clean.config.a0"
    )
    assert (
        load_json_config(pcblib_config)["schema"]
        == "altium_cruncher.pcblib.clean.config.a0"
    )
