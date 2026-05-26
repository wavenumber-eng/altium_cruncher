"""Split command for altium_cruncher."""

import argparse
import logging
from pathlib import Path

from altium_cruncher.altium_cruncher_common import _resolve_output_dir

log = logging.getLogger(__name__)


def _cmd_split_schlib(input_file: Path, output_dir: Path, args) -> int:
    from altium_monkey.altium_schlib import AltiumSchLib

    schlib = AltiumSchLib(input_file)
    log.info(f"Found {len(schlib.symbols)} symbol(s)")

    symbol_filter = args.symbols if getattr(args, "symbols", None) else None
    results = schlib.split(
        output_dir=output_dir,
        name_pattern=args.pattern if getattr(args, "pattern", None) else "{symbol_name}.SchLib",
        symbol_filter=symbol_filter,
        verbose=True,
    )

    successful = sum(1 for value in results.values() if value is not None)
    failed = sum(1 for value in results.values() if value is None)

    log.info("-" * 60)
    log.info(f"Split complete: {successful} successful, {failed} failed")
    return 0 if failed == 0 else 1


def _cmd_split_pcblib(input_file: Path, output_dir: Path, args) -> int:
    from altium_monkey.altium_pcblib import AltiumPcbLib

    default_pattern = "{symbol_name}.SchLib"
    if getattr(args, "pattern", default_pattern) != default_pattern:
        log.error("--pattern is not supported for PcbLib split")
        return 1
    if getattr(args, "symbols", None):
        log.error("--symbols is not supported for PcbLib split")
        return 1

    pcblib = AltiumPcbLib.from_file(input_file)
    log.info(f"Found {len(pcblib.footprints)} footprint(s)")

    results = pcblib.split(output_dir=output_dir, verbose=True)
    log.info("-" * 60)
    log.info(f"Split complete: {len(results)} successful, 0 failed")
    return 0


def cmd_split(args) -> int:
    """
    Handle split subcommand.

    Supported inputs:
    - `.SchLib` -> individual `SchLib` files
    - `.PcbLib` -> individual `PcbLib` files
    """
    input_file = Path(args.file).resolve()
    if not input_file.exists():
        log.error(f"File not found: {input_file}")
        return 1

    output_dir = _resolve_output_dir(args.output, "split")

    log.info(f"Splitting: {input_file.name}")
    log.info(f"Output directory: {output_dir}")

    try:
        suffix = input_file.suffix.lower()
        if suffix == ".schlib":
            return _cmd_split_schlib(input_file, output_dir, args)
        if suffix == ".pcblib":
            return _cmd_split_pcblib(input_file, output_dir, args)

        log.error(f"Unsupported file type: {input_file.suffix}")
        log.info("Supported types: .SchLib, .PcbLib")
        return 1
    except Exception as exc:
        log.error(f"Error splitting {input_file.name}: {exc}")
        import traceback

        traceback.print_exc()
        return 1


def register_parser(subparsers):
    split_parser = subparsers.add_parser(
        "split",
        help="split a multi-symbol SchLib or multi-footprint PcbLib into individual files",
        description=(
            "Split a multi-symbol SchLib or multi-footprint PcbLib library file "
            "into individual library files."
        ),
        epilog=(
            "Examples:\n"
            "  altium_cruncher split library.SchLib\n"
            "  altium_cruncher split library.PcbLib\n"
            "  altium_cruncher split library.SchLib -o split_output/\n"
            "  altium_cruncher split library.SchLib --pattern \"MY_{symbol_name}.SchLib\"\n"
            "  altium_cruncher split library.SchLib --symbols \"RES1\" \"CAP1\""
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    split_parser.add_argument("file", help="multi-symbol SchLib or multi-footprint PcbLib file to split")
    split_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output directory (default: ./output/split)",
    )
    split_parser.add_argument(
        "--pattern",
        type=str,
        default="{symbol_name}.SchLib",
        help="SchLib-only output filename pattern (default: {symbol_name}.SchLib)",
    )
    split_parser.add_argument("--symbols", nargs="+", help="SchLib-only symbol filter")
    split_parser.set_defaults(handler=cmd_split)
    return split_parser
