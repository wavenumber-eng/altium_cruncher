"""Design JSON command for altium_cruncher."""

import argparse
import logging
from pathlib import Path

from altium_cruncher.altium_cruncher_common import _resolve_output_dir, find_prjpcb_in_cwd
from altium_cruncher.altium_cruncher_design_review import write_design_review_bundle

log = logging.getLogger(__name__)


def cmd_design(args: argparse.Namespace) -> int:
    """
    Handle design subcommand - generate design JSON from SchDoc/PrjPcb files.

    REQ-CLI-006: Design JSON generation using AltiumDesign.to_json().

    Args:
        args: Parsed argparse namespace with file and output options.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    # Determine input file
    input_file: Path | None = None

    if args.file:
        input_file = Path(args.file).resolve()
        if not input_file.exists():
            log.error(f"File not found: {input_file}")
            return 1
    else:
        # Auto-detect PrjPcb in CWD
        input_file = find_prjpcb_in_cwd()
        if not input_file:
            log.error("No file specified and no .PrjPcb found in current directory")
            log.info("Usage: altium-cruncher design [file.SchDoc | project.PrjPcb]")
            return 1
        log.info(f"Auto-detected project: {input_file.name}")

    suffix = input_file.suffix.lower()
    if suffix not in {".schdoc", ".prjpcb"}:
        log.error(f"Unsupported file type: {suffix}")
        log.info("Supported types: .SchDoc, .PrjPcb")
        return 1

    output_dir = _resolve_output_dir(args.output, "design")
    include_indexes = not getattr(args, 'no_indexes', False)

    try:
        manifest = write_design_review_bundle(
            input_file,
            output_dir,
            include_indexes=include_indexes,
        )
    except Exception as exc:
        log.error("Design review generation failed for %s: %s", input_file.name, exc)
        return 1

    log.info("Design review bundle: %s", output_dir)
    log.info("Design JSON: %s", manifest["design_json"])
    log.info("Manifest: design_review_manifest.json")
    return 0


def register_parser(
    subparsers: argparse._SubParsersAction,
) -> argparse.ArgumentParser:
    """Register the design command parser."""
    design_parser = subparsers.add_parser(
        "design",
        aliases=["design-review", "dr"],
        help="generate Altium design review artifacts",
        description=(
            "Generate an Altium design review bundle from SchDoc or PrjPcb "
            "files. The bundle includes AltiumDesign JSON, serialized SchDoc/"
            "PcbDoc JSON, schematic SVGs, PCB layer SVGs, structured notes "
            "JSON, a manifest, and an agent-facing README."
        ),
        epilog=(
            "Examples:\n"
            "  altium-cruncher design project.PrjPcb\n"
            "  altium-cruncher design-review project.PrjPcb\n"
            "  altium-cruncher dr project.PrjPcb\n"
            "  altium-cruncher design schematic.SchDoc\n"
            "  altium-cruncher design                    # Auto-detect PrjPcb in CWD\n"
            "  altium-cruncher design project.PrjPcb --no-indexes  # Without lookup indexes\n"
            "  altium-cruncher design project.PrjPcb -o output_dir/"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    design_parser.add_argument(
        "file",
        nargs="?",
        help="SchDoc or PrjPcb file (optional if PrjPcb in CWD)",
    )
    design_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output directory (default: ./output/design)",
    )
    design_parser.add_argument(
        "--no-indexes",
        action="store_true",
        help="exclude lookup indexes from JSON",
    )
    design_parser.set_defaults(handler=cmd_design)
    return design_parser
