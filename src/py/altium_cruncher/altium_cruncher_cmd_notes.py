"""notes command for altium_cruncher."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from altium_cruncher.altium_cruncher_common import find_prjpcb_in_cwd
from altium_cruncher.altium_cruncher_notes import build_notes_payload, write_notes_payload

log = logging.getLogger(__name__)


def cmd_notes(args: argparse.Namespace) -> int:
    """Extract schematic note/text annotations as structured JSON."""
    input_file = _resolve_notes_input(args)
    if input_file is None:
        return 1
    try:
        if getattr(args, "stdout", False):
            print(
                json.dumps(
                    build_notes_payload(
                        input_file,
                        include_sheet_template_text=args.include_sheet_template_text,
                    ),
                    indent=2,
                )
            )
        else:
            output_path = write_notes_payload(
                input_file,
                output=args.output,
                include_sheet_template_text=args.include_sheet_template_text,
            )
            log.info("Notes JSON: %s", output_path)
    except Exception as exc:
        log.error("Notes extraction failed for %s: %s", input_file.name, exc)
        return 1
    return 0


def _resolve_notes_input(args: argparse.Namespace) -> Path | None:
    if args.file:
        input_file = Path(args.file).resolve()
        if not input_file.exists():
            log.error("File not found: %s", input_file)
            return None
    else:
        input_file = find_prjpcb_in_cwd()
        if input_file is None:
            log.error("No file specified and no .PrjPcb found in current directory")
            return None
        log.info("Auto-detected project: %s", input_file.name)
    if input_file.suffix.lower() not in {".schdoc", ".prjpcb"}:
        log.error("Unsupported notes input type: %s", input_file.suffix)
        return None
    return input_file


def register_parser(
    subparsers: argparse._SubParsersAction,
) -> argparse.ArgumentParser:
    """Register the notes command parser."""
    parser = subparsers.add_parser(
        "notes",
        help="extract schematic notes, text frames, and free text to JSON",
        description=(
            "Extract dedicated schematic Note objects, text frames, and free "
            "text strings from a SchDoc or all SchDocs in a PrjPcb."
        ),
        epilog=(
            "Examples:\n"
            "  altium-cruncher notes project.PrjPcb\n"
            "  altium-cruncher notes schematic.SchDoc --stdout\n"
            "  altium-cruncher notes project.PrjPcb -o output/notes"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="SchDoc or PrjPcb file (optional if PrjPcb in CWD)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output directory (default: ./output/notes)",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="write JSON payload to stdout instead of a file",
    )
    parser.add_argument(
        "--include-sheet-template-text",
        action="store_true",
        help="include title-block/sheet-template owned text normally suppressed",
    )
    parser.set_defaults(handler=cmd_notes)
    return parser
