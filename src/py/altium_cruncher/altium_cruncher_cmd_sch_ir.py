"""sch-ir command for altium_cruncher."""

import argparse
import json
import logging
from pathlib import Path

from altium_cruncher.altium_cruncher_common import (
    _resolve_output_dir,
    find_prjpcb_in_cwd,
)

log = logging.getLogger(__name__)


def _find_prjpcb_in_dir(input_dir: Path) -> Path | None:
    prjpcb_files = sorted(
        [
            path
            for path in input_dir.iterdir()
            if path.is_file() and path.suffix.lower() == ".prjpcb"
        ],
        key=lambda path: path.name.lower(),
    )
    if len(prjpcb_files) == 1:
        input_file = prjpcb_files[0].resolve()
        log.info("Auto-detected project: %s", input_file.name)
        return input_file
    if not prjpcb_files:
        log.error("No .PrjPcb found in directory: %s", input_dir)
        return None
    log.error("Multiple .PrjPcb files found in directory: %s", input_dir)
    for prjpcb_file in prjpcb_files:
        log.info("  %s", prjpcb_file.name)
    return None


def _resolve_input_file(args: argparse.Namespace) -> Path | None:
    if args.file:
        input_file = Path(args.file).resolve()
        if not input_file.exists():
            log.error("File not found: %s", input_file)
            return None
        if input_file.is_dir():
            return _find_prjpcb_in_dir(input_file)
        return input_file

    input_file = find_prjpcb_in_cwd()
    if not input_file:
        log.error("No file specified and no .PrjPcb found in current directory")
        log.info(
            "Usage: altium-cruncher sch-ir [file.SchDoc | project.PrjPcb | project-folder]"
        )
        return None
    log.info("Auto-detected project: %s", input_file.name)
    return input_file


def _schdoc_inputs_for_file(
    input_file: Path,
) -> tuple[list[Path], dict[str, str]] | None:
    from altium_monkey.altium_prjpcb import AltiumPrjPcb

    suffix = input_file.suffix.lower()
    if suffix == ".schdoc":
        return [input_file], {}
    if suffix != ".prjpcb":
        log.error("Unsupported file type: %s", suffix)
        log.info("Supported schematic IR types: .SchDoc, .PrjPcb")
        return None

    project = AltiumPrjPcb(input_file)
    schdoc_files = project.get_schdoc_paths()
    project_parameters = dict(project.parameters)
    current_variant = project.get_current_variant()
    if current_variant:
        project_parameters["VariantName"] = current_variant
    if not schdoc_files:
        log.error("No SchDoc files found in project: %s", input_file)
        return None
    log.info("Found %s SchDoc file(s) in project", len(schdoc_files))
    return schdoc_files, project_parameters


def _font_diagnostics_from_ir_payload(
    payload: dict[str, object],
) -> list[dict[str, object]]:
    render_hints = payload.get("render_hints")
    if not isinstance(render_hints, dict):
        return []
    font_resolution = render_hints.get("font_resolution")
    if not isinstance(font_resolution, dict):
        return []
    diagnostics = font_resolution.get("diagnostics")
    if not isinstance(diagnostics, list):
        return []
    return [item for item in diagnostics if isinstance(item, dict)]


def _log_font_diagnostics(diagnostics: list[dict[str, object]]) -> None:
    for diagnostic in diagnostics:
        status = str(diagnostic.get("status", "") or "")
        if status == "exact":
            continue
        requested = str(diagnostic.get("requested_family", "") or "")
        resolved = str(diagnostic.get("resolved_family", "") or "")
        source = str(diagnostic.get("source", "") or "")
        if status == "missing":
            log.warning("Font unresolved: %s; using hard fallback metrics", requested)
        elif resolved:
            label = {
                "generic_fallback": "fallback",
                "style_fallback": "style fallback",
                "substituted": "substituted",
            }.get(status, status)
            log.warning(
                "Font %s: %s -> %s (%s)",
                label,
                requested,
                resolved,
                source,
            )


def log_current_font_resolution_diagnostics() -> None:
    """Log process-local Altium Monkey font diagnostics after SVG rendering."""
    from altium_monkey.altium_font_resolver import get_font_resolution_diagnostics

    _log_font_diagnostics(
        [diagnostic.to_dict() for diagnostic in get_font_resolution_diagnostics()]
    )


def cmd_sch_ir(args: argparse.Namespace) -> int:
    """
    Handle sch-ir subcommand - export gotIR JSON from SchDoc/PrjPcb files.
    """
    from altium_monkey.altium_schdoc import AltiumSchDoc

    input_file = _resolve_input_file(args)
    if input_file is None:
        return 1

    resolved_inputs = _schdoc_inputs_for_file(input_file)
    if resolved_inputs is None:
        return 1
    schdoc_files, project_parameters = resolved_inputs
    output_dir = _resolve_output_dir(args.output, "sch-ir")

    success_count = 0
    for schdoc_path in schdoc_files:
        output_file = output_dir / f"{schdoc_path.stem}.gotir.json"
        log.info("Processing: %s", schdoc_path.name)
        try:
            schdoc = AltiumSchDoc(schdoc_path)
            document = schdoc.to_ir(
                project_parameters=project_parameters,
                profile="onscreen",
            )
            payload = document.to_dict()
            _log_font_diagnostics(_font_diagnostics_from_ir_payload(payload))
            output_file.write_text(
                json.dumps(payload, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            log.info("  -> %s", output_file.name)
            success_count += 1
        except Exception as exc:
            log.error("Error processing %s: %s", schdoc_path.name, exc)

    if success_count == len(schdoc_files):
        log.info("Successfully generated %s gotIR JSON file(s)", success_count)
        return 0

    log.warning("Generated %s/%s gotIR JSON file(s)", success_count, len(schdoc_files))
    return 1


def register_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    sch_ir_parser = subparsers.add_parser(
        "sch-ir",
        help="export schematic gotIR JSON from Altium SchDoc/PrjPcb",
        description=(
            "Export schematic gotIR JSON from Altium SchDoc, PrjPcb, "
            "or project-directory inputs."
        ),
        epilog=(
            "Examples:\n"
            "  altium-cruncher sch-ir schematic.SchDoc\n"
            "  altium-cruncher sch-ir project.PrjPcb\n"
            "  altium-cruncher sch-ir ./project-dir\n"
            "  altium-cruncher sch-ir                    # Auto-detect PrjPcb in CWD\n"
            "  altium-cruncher sch-ir project.PrjPcb -o output_dir/"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sch_ir_parser.add_argument(
        "file",
        nargs="?",
        help="SchDoc, PrjPcb, or project directory (optional if PrjPcb in CWD)",
    )
    sch_ir_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output directory (default: ./output/sch-ir)",
    )
    sch_ir_parser.set_defaults(handler=cmd_sch_ir)
    return sch_ir_parser
