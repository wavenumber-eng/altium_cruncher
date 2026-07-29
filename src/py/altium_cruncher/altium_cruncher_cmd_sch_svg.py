"""sch-svg command for altium_cruncher."""

import argparse
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


def cmd_sch_svg(args) -> int:
    """
    Handle sch-svg subcommand - generate SVG from SchDoc/PrjPcb/SchLib files.
    """
    input_file = _resolve_sch_svg_input(args.file)
    if input_file is None:
        return 1
    output_dir = _resolve_output_dir(args.output, "sch-svg")
    suffix = input_file.suffix.lower()

    if suffix == ".schdoc":
        return _write_logical_schdoc_svgs([input_file], output_dir)
    if suffix == ".prjpcb":
        return _write_project_or_logical_svgs(input_file, output_dir)
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


def _write_project_or_logical_svgs(input_file: Path, output_dir: Path) -> int:
    from altium_monkey.altium_design import AltiumDesign
    from altium_monkey.altium_prjpcb import AltiumPrjPcb

    design = AltiumDesign.from_prjpcb(input_file)
    project = design.project or AltiumPrjPcb(input_file)
    schdoc_files = project.get_schdoc_paths()
    project_parameters = _project_parameters(project)
    if not schdoc_files:
        log.error(f"No SchDoc files found in project: {input_file}")
        return 1
    log.info(f"Found {len(schdoc_files)} SchDoc file(s) in project")

    success_count = _write_project_schematic_svgs(
        design,
        output_dir,
        project_parameters=project_parameters,
    )
    if success_count > 0:
        log.info(f"Successfully generated {success_count} SVG file(s)")
        return 0
    log.warning(
        "No compiled schematic pages were available; falling back to logical SchDoc SVGs"
    )
    return _write_logical_schdoc_svgs(
        schdoc_files,
        output_dir,
        project_parameters=project_parameters,
    )


def _project_parameters(project: object) -> dict[str, str]:
    parameters = dict(getattr(project, "parameters", {}))
    current_variant = project.get_current_variant()
    if current_variant:
        parameters["VariantName"] = current_variant
    return parameters


def _write_logical_schdoc_svgs(
    schdoc_files: list[Path],
    output_dir: Path,
    *,
    project_parameters: dict[str, str] | None = None,
) -> int:
    from altium_monkey.altium_schdoc import AltiumSchDoc

    parameters = project_parameters or {}
    success_count = 0
    for schdoc_path in schdoc_files:
        output_file = output_dir / f"{schdoc_path.stem}.svg"
        log.info(f"Processing: {schdoc_path.name}")
        try:
            schdoc = AltiumSchDoc(schdoc_path)
            svg_content = schdoc.to_svg(
                project_parameters=parameters, wrap_components=True
            )
            log_current_font_resolution_diagnostics()
            output_file.write_text(svg_content, encoding="utf-8")
            log.info(f"  -> {output_file.name}")
            success_count += 1
        except Exception as exc:
            log.error(f"Error processing {schdoc_path.name}: {exc}")

    if success_count == len(schdoc_files):
        log.info(f"Successfully generated {success_count} SVG file(s)")
        return 0

    log.warning(f"Generated {success_count}/{len(schdoc_files)} SVG file(s)")
    return 1


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
    """Write compiled/resolved schematic page SVGs for a project input."""
    to_physical_svg = getattr(design, "to_physical_svg", None)
    if not callable(to_physical_svg):
        log.warning("Compiled schematic SVG API is unavailable")
        return 0

    payload = design.to_json(include_indexes=True)
    raw_pages = payload.get("physical_pages", [])
    pages = [page for page in raw_pages if isinstance(page, dict)]
    if not pages:
        return 0

    log.info(f"Found {len(pages)} compiled schematic page(s) in project")
    used_names: set[str] = set()
    success_count = 0
    for index, page in enumerate(pages, start=1):
        page_id = str(page.get("id") or "").strip()
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
            log_current_font_resolution_diagnostics()
            output_file.write_text(svg_content, encoding="utf-8")
            log.info(f"  -> {output_file.name}")
            success_count += 1
        except Exception as exc:
            log.error(f"Error processing compiled page {page_id}: {exc}")
    return success_count


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
    for key in (
        "room_name",
        "channel_prefix",
        "channel_alpha",
        "physical_instance_path",
        "id",
    ):
        label = str(page.get(key) or "").strip()
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
