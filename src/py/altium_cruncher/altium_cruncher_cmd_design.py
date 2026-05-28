"""Design JSON command for altium_cruncher."""

import argparse
import json
import logging
from pathlib import Path

from altium_cruncher.altium_cruncher_common import _resolve_output_dir, find_prjpcb_in_cwd

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
    from altium_monkey.altium_design import AltiumDesign

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

    # Validate file type
    suffix = input_file.suffix.lower()
    if suffix == '.schdoc':
        design = AltiumDesign.from_schdoc(input_file)
    elif suffix == '.prjpcb':
        design = AltiumDesign.from_prjpcb(input_file)
    else:
        log.error(f"Unsupported file type: {suffix}")
        log.info("Supported types: .SchDoc, .PrjPcb")
        return 1

    # Determine output directory
    output_dir = _resolve_output_dir(args.output, "design")

    # Determine output filename
    output_file = output_dir / f"{input_file.stem}_design.json"

    # Include indexes option
    include_indexes = not getattr(args, 'no_indexes', False)

    # Serialize the design model to JSON
    design_json = design.to_json(include_indexes=include_indexes)

    # Write JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(design_json, f, indent=2)

    # Summary
    log.info(
        f"Design JSON: {len(design_json.get('components', []))} components, "
        f"{len(design_json.get('nets', []))} nets -> {output_file.name}"
    )

    return 0


def register_parser(subparsers):
    """Register the design command parser."""
    design_parser = subparsers.add_parser(
        "design",
        help="generate design JSON with nets, components, and SVG IDs",
        description=(
            "Generate design JSON from Altium SchDoc or PrjPcb files. "
            "The output is the full AltiumDesign model: netlist data, "
            "component records, hierarchy, SVG IDs, and lookup indexes."
        ),
        epilog=(
            "Examples:\n"
            "  altium-cruncher design project.PrjPcb\n"
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
