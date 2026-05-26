"""Merge command for altium_cruncher."""

import argparse
import logging
from pathlib import Path

from altium_cruncher.altium_cruncher_common import _resolve_output_dir

log = logging.getLogger(__name__)


def _find_files_with_suffix(directory: Path, suffix: str) -> list[Path]:
    return sorted(
        [
            path for path in directory.iterdir()
            if path.is_file() and path.suffix.lower() == suffix.lower()
        ],
        key=lambda path: path.name.lower(),
    )


def _cmd_merge_schlib(input_path: Path, output_dir: Path, handle_conflicts: str) -> int:
    from altium_monkey.altium_schlib import AltiumSchLib

    output_file = output_dir / f"{input_path.name}_merged.SchLib"
    log.info(f"Merging SchLib files from: {input_path}")
    log.info(f"Output file: {output_file}")

    merged = AltiumSchLib.merge(
        input_paths=input_path,
        output_path=output_file,
        handle_conflicts=handle_conflicts,
        verbose=True,
    )
    log.info("-" * 60)
    log.info(f"Merge complete: {len(merged.symbols)} symbols in {output_file.name}")
    return 0


def _cmd_merge_pcblib(input_path: Path, output_dir: Path, handle_conflicts: str) -> int:
    from altium_monkey.altium_pcblib import AltiumPcbLib

    if handle_conflicts != "rename":
        raise ValueError("PcbLib merge currently supports only --conflicts rename")

    output_file = output_dir / f"{input_path.name}_merged.PcbLib"
    log.info(f"Merging PcbLib files from: {input_path}")
    log.info(f"Output file: {output_file}")

    merged = AltiumPcbLib.combine(input_path, verbose=True)
    merged.save(output_file)
    provenance_path = merged.write_combine_provenance()

    log.info("-" * 60)
    log.info(f"Merge complete: {len(merged.footprints)} footprints in {output_file.name}")
    log.info(f"Provenance manifest: {provenance_path.name}")
    return 0


def cmd_merge(args) -> int:
    """
    Handle merge subcommand.

    Supported inputs:
    - directory of `.SchLib` files -> merged `SchLib`
    - directory of `.PcbLib` files -> merged `PcbLib`
    """
    input_path = Path(args.input).resolve()
    if not input_path.exists():
        log.error(f"Input not found: {input_path}")
        return 1

    if not input_path.is_dir():
        log.error(f"Input must be a directory containing SchLib or PcbLib files: {input_path}")
        return 1

    schlib_files = _find_files_with_suffix(input_path, ".SchLib")
    pcblib_files = _find_files_with_suffix(input_path, ".PcbLib")
    if schlib_files and pcblib_files:
        log.error("Input directory contains both SchLib and PcbLib files; use a single library type")
        return 1
    if not schlib_files and not pcblib_files:
        log.error(f"No SchLib or PcbLib files found in: {input_path}")
        return 1

    output_dir = _resolve_output_dir(args.output, "merge")
    handle_conflicts = getattr(args, "conflicts", "rename")

    try:
        if schlib_files:
            return _cmd_merge_schlib(input_path, output_dir, handle_conflicts)
        return _cmd_merge_pcblib(input_path, output_dir, handle_conflicts)
    except ValueError as exc:
        log.error(f"Merge failed: {exc}")
        return 1
    except Exception as exc:
        log.error(f"Error merging library files: {exc}")
        import traceback

        traceback.print_exc()
        return 1


def register_parser(subparsers):
    merge_parser = subparsers.add_parser(
        "merge",
        help="merge multiple SchLib or PcbLib files into one library",
        description=(
            "Merge multiple individual SchLib files into a single multi-symbol SchLib, "
            "or multiple PcbLib files into a single multi-footprint PcbLib."
        ),
        epilog=(
            "Examples:\n"
            "  altium-cruncher merge input_directory/\n"
            "  altium-cruncher merge input_directory/ -o output_dir/\n"
            "  altium-cruncher merge input_directory/ --conflicts skip\n"
            "  altium-cruncher merge input_directory/ --conflicts error\n"
            "  altium-cruncher merge split_pcblib_dir/ --conflicts rename"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    merge_parser.add_argument("input", help="directory containing SchLib or PcbLib files to merge")
    merge_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output directory (default: ./output/merge)",
    )
    merge_parser.add_argument(
        "--conflicts",
        choices=["rename", "skip", "error"],
        default="rename",
        help="how to handle duplicate symbol names (PcbLib currently supports rename only)",
    )
    merge_parser.set_defaults(handler=cmd_merge)
    return merge_parser
