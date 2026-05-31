"""json-dump command for altium_cruncher."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from altium_cruncher.altium_cruncher_json_dump import (
    build_single_json_dump_payload,
    write_json_dumps,
)

log = logging.getLogger(__name__)


def cmd_json_dump(args: argparse.Namespace) -> int:
    """Handle the json-dump command."""
    inputs = list(args.inputs or [])
    try:
        if args.stdout:
            payload = build_single_json_dump_payload(
                inputs,
                recursive=bool(args.recursive),
            )
            print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
            return 0

        result = write_json_dumps(
            inputs,
            output=args.output,
            recursive=bool(args.recursive),
        )
    except Exception as exc:
        log.error("Failed dumping Altium JSON: %s", exc)
        return 1

    print(str(result.manifest_path))
    return 0


def register_parser(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(
        "json-dump",
        help="dump parsed Altium documents to developer JSON",
        description=(
            "Dump parsed SchDoc, SchLib, PcbDoc, and PcbLib documents to JSON. "
            "PrjPcb inputs expand to supported project documents."
        ),
        epilog=(
            "Examples:\n"
            "  altium_cruncher json-dump board.PcbDoc\n"
            "  altium_cruncher json-dump project.PrjPcb -o output/json-dump\n"
            "  altium_cruncher json-dump . --recursive\n"
            "  altium_cruncher json-dump board.PcbDoc --stdout"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        type=Path,
        help=(
            "files or directories to dump; if omitted, auto-detect one PrjPcb "
            "or supported documents in the current directory"
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output directory (default: ./output/json-dump)",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="recurse through directory inputs",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="print one resolved document to stdout instead of writing files",
    )
    parser.set_defaults(handler=cmd_json_dump)
    return parser
