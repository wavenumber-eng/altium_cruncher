"""sch-svg command for altium_cruncher."""

import argparse
import json
import logging
import re
from pathlib import Path

from altium_cruncher.altium_cruncher_common import (
    _resolve_output_dir,
    find_prjpcb_in_cwd,
)
from altium_cruncher.altium_cruncher_cmd_sch_ir import (
    log_current_font_resolution_diagnostics,
)

log = logging.getLogger(__name__)

SCHEMATIC_SVG_MANIFEST_SCHEMA = "altium_cruncher.schematic_svg_manifest.b0"


def cmd_sch_svg(args) -> int:
    """
    Handle sch-svg subcommand - generate SVG from SchDoc/PrjPcb/SchLib files.
    """
    input_file = _resolve_sch_svg_input(args.file)
    if input_file is None:
        return 1
    output_dir = _resolve_output_dir(args.output, "sch-svg")
    suffix = input_file.suffix.lower()

    if suffix in {".schdoc", ".prjpcb"}:
        return _write_compiled_schematic_bundle(input_file, output_dir)
    if suffix == ".schlib":
        return _write_schlib_svgs(input_file, output_dir)
    log.error(f"Unsupported file type: {suffix}")
    log.info("Supported schematic SVG types: .SchDoc, .PrjPcb, .SchLib")
    return 1


def _resolve_sch_svg_input(raw_file: str | None) -> Path | None:
    if raw_file:
        input_file = Path(raw_file).resolve()
        if input_file.exists():
            return input_file
        log.error(f"File not found: {input_file}")
        return None
    input_file = find_prjpcb_in_cwd()
    if input_file:
        log.info(f"Auto-detected project: {input_file.name}")
        return input_file
    log.error("No file specified and no .PrjPcb found in current directory")
    log.info(
        "Usage: altium-cruncher sch-svg [file.SchDoc | project.PrjPcb | library.SchLib]"
    )
    return None


def _write_compiled_schematic_bundle(input_file: Path, output_dir: Path) -> int:
    """Write self-contained compiled SVG, Design b0, and manifest artifacts."""
    from altium_monkey.altium_design import AltiumDesign

    design = (
        AltiumDesign.from_schdoc(input_file)
        if input_file.suffix.lower() == ".schdoc"
        else AltiumDesign.from_prjpcb(input_file)
    )
    payload = design.to_json(include_indexes=True)
    project_parameters = _project_parameters(getattr(design, "project", None))
    artifacts = _write_compiled_schematic_svg_artifacts(
        design,
        output_dir,
        payload=payload,
        project_parameters=project_parameters,
        source_base=input_file.resolve().parent,
    )
    from altium_cruncher.altium_cruncher_design_review import (
        COMPILED_GRAPH_SCHEMA,
        DESIGN_SCHEMA,
        _compiled_schematic_pages,
    )

    expected_count = len(_compiled_schematic_pages(payload))
    if not artifacts or len(artifacts) != expected_count:
        log.error(
            "Generated %d/%d compiled schematic SVG page(s)",
            len(artifacts),
            expected_count,
        )
        return 1

    design_path = output_dir / "design" / f"{input_file.stem}_design.json"
    design_path.parent.mkdir(parents=True, exist_ok=True)
    design_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    manifest = {
        "schema": SCHEMATIC_SVG_MANIFEST_SCHEMA,
        "input": input_file.name,
        "design_json": design_path.relative_to(output_dir).as_posix(),
        "design_schema": DESIGN_SCHEMA,
        "compiled_schematic_graph_schema": COMPILED_GRAPH_SCHEMA,
        "svgs": artifacts,
    }
    manifest_path = output_dir / "schematic_svg_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    log.info("Design b0 sidecar: %s", design_path.name)
    log.info("Schematic SVG manifest: %s", manifest_path.name)
    log.info("Successfully generated %d SVG file(s)", len(artifacts))
    return 0


def _project_parameters(project: object) -> dict[str, str]:
    if project is None:
        return {}
    parameters = dict(getattr(project, "parameters", {}))
    current_variant = project.get_current_variant()
    if current_variant:
        parameters["VariantName"] = current_variant
    return parameters


def _write_schlib_svgs(input_file: Path, output_dir: Path) -> int:
    from altium_monkey.altium_schlib import AltiumSchLib

    try:
        schlib = AltiumSchLib(input_file)
        log.info(f"Processing SchLib: {input_file.name}")
        log.info(f"  Symbols: {len(schlib.symbols)}")
        svg_dict = schlib.to_svg(output_dir=output_dir)
        total_svgs = _log_schlib_svg_outputs(svg_dict)
        log.info(f"Successfully generated {total_svgs} SVG file(s)")
        return 0
    except Exception as exc:
        log.error(f"Error processing SchLib: {exc}")
        return 1


def _log_schlib_svg_outputs(svg_dict: dict[str, object]) -> int:
    total_svgs = 0
    for symbol_name, parts in svg_dict.items():
        for part_id in parts:
            total_svgs += 1
            suffix = f"_part{part_id}" if len(parts) > 1 else ""
            log.info(f"  -> {symbol_name}{suffix}.svg")
    return total_svgs


def _write_project_schematic_svgs(
    design: object,
    output_dir: Path,
    *,
    project_parameters: dict[str, str],
) -> int:
    """Compatibility wrapper returning the compiled SVG artifact count."""
    payload = design.to_json(include_indexes=True)
    return len(
        _write_compiled_schematic_svg_artifacts(
            design,
            output_dir,
            payload=payload,
            project_parameters=project_parameters,
            source_base=output_dir,
        )
    )


def _write_compiled_schematic_svg_artifacts(
    design: object,
    output_dir: Path,
    *,
    payload: dict[str, object],
    project_parameters: dict[str, str],
    source_base: Path,
) -> list[dict[str, object]]:
    """Write graph-scoped compiled SVG pages and return manifest rows."""
    to_physical_svg = getattr(design, "to_physical_svg", None)
    if not callable(to_physical_svg):
        log.warning("Compiled schematic SVG API is unavailable")
        return []

    from altium_cruncher.altium_cruncher_design_review import (
        _compiled_schematic_pages,
        _compiled_page_source,
        _enrich_project_schematic_svg,
    )

    pages = _compiled_schematic_pages(payload)
    if not pages:
        return []

    log.info("Found %d compiled schematic page(s)", len(pages))
    used_names: set[str] = set()
    artifacts: list[dict[str, object]] = []
    for index, page in enumerate(pages, start=1):
        page_id = str(page.get("page_occurrence_ref") or "").strip()
        if not page_id:
            continue
        output_file = output_dir / _compiled_page_svg_filename(
            page,
            index=index,
            used_names=used_names,
        )
        log.info(f"Processing compiled page: {page_id}")
        try:
            svg_content = to_physical_svg(
                page_id,
                project_parameters=project_parameters,
                wrap_components=True,
            )
            svg_content = _enrich_project_schematic_svg(
                svg_content,
                design_payload=payload,
                schematic_page=page,
                source_base=source_base,
            )
            log_current_font_resolution_diagnostics()
            output_file.write_text(svg_content, encoding="utf-8")
            log.info(f"  -> {output_file.name}")
            artifacts.append(
                {
                    "file": output_file.relative_to(output_dir).as_posix(),
                    "page_occurrence_ref": page_id,
                    "artifact_key": "sch.dwg_scene",
                    "source": _compiled_page_source(page, source_base),
                    "source_sheet": str(page.get("source_sheet") or ""),
                    "page_number": index,
                    "page_count": len(pages),
                }
            )
        except Exception as exc:
            log.error(f"Error processing compiled page {page_id}: {exc}")
    return artifacts


def _compiled_page_svg_filename(
    page: dict[str, object],
    *,
    index: int,
    used_names: set[str],
) -> str:
    source_sheet = Path(str(page.get("source_sheet") or "sheet")).stem
    label = _compiled_page_label(page)
    base = _safe_svg_stem(f"{index:03d}_{source_sheet}_{label}")
    return _unique_svg_filename(base, used_names)


def _compiled_page_label(page: dict[str, object]) -> str:
    metadata = page.get("physical_page_metadata")
    if not isinstance(metadata, dict):
        metadata = {}
    for key in (
        "room_name",
        "channel_prefix",
        "channel_alpha",
        "physical_instance_path",
        "page_occurrence_ref",
    ):
        label = str(metadata.get(key) or page.get(key) or "").strip()
        if label:
            return label
    return "sheet"


def _unique_svg_filename(base: str, used_names: set[str]) -> str:
    name = f"{base}.svg"
    suffix = 2
    while name.lower() in used_names:
        name = f"{base}_{suffix}.svg"
        suffix += 1
    used_names.add(name.lower())
    return name


def _safe_svg_stem(value: str) -> str:
    stem = re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("._")
    return stem or "sheet"


def register_parser(subparsers):
    sch_svg_parser = subparsers.add_parser(
        "sch-svg",
        help="generate schematic SVG from Altium SchDoc/PrjPcb/SchLib",
        description="Generate SVG files from Altium SchDoc, PrjPcb, or SchLib inputs.",
        epilog="Examples:\n"
        "  altium-cruncher sch-svg schematic.SchDoc\n"
        "  altium-cruncher sch-svg project.PrjPcb\n"
        "  altium-cruncher sch-svg library.SchLib\n"
        "  altium-cruncher sch-svg                             # Auto-detect PrjPcb in CWD\n"
        "  altium-cruncher sch-svg project.PrjPcb -o output_dir/",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sch_svg_parser.add_argument(
        "file",
        nargs="?",
        help="SchDoc, PrjPcb, or SchLib file (optional if PrjPcb in CWD)",
    )
    sch_svg_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output directory (default: ./output/sch-svg)",
    )
    sch_svg_parser.set_defaults(handler=cmd_sch_svg)
    return sch_svg_parser
