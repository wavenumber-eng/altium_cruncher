"""SchLib authoring commands backed by MCO operations."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from altium_cruncher.altium_cruncher_cmd_mco import (
    execute_mco_for_cli,
    print_mco_execution_result,
)
from altium_cruncher.altium_cruncher_mco import (
    MCO_SCHEMA,
    JsonObject,
    McoExecutionContext,
    McoExecutionResult,
    execute_mco,
    mco_operation,
)

log = logging.getLogger(__name__)


def build_schlib_create_mco(
    output_file: Path | str,
    *,
    symbol: str | None = None,
    description: str = "",
    overwrite: bool = False,
) -> JsonObject:
    """Build the MCO payload for creating a one-symbol SchLib."""
    file_path = Path(output_file)
    symbol_name = symbol or file_path.stem
    return {
        "schema": MCO_SCHEMA,
        "operations": [
            mco_operation(
                "schlib.create",
                "create_schlib",
                "Create SchLib",
                {"file": str(file_path), "overwrite": overwrite},
            ),
            mco_operation(
                "schlib.add_symbol",
                "add_symbol",
                "Add initial symbol",
                {
                    "file": str(file_path),
                    "name": symbol_name,
                    "description": description,
                },
            ),
        ],
    }


def execute_schlib_create_mco(
    output_file: Path | str,
    *,
    symbol: str | None = None,
    description: str = "",
    overwrite: bool = False,
    dry_run: bool = False,
) -> McoExecutionResult:
    """Execute the generated SchLib-create MCO payload."""
    return execute_mco(
        build_schlib_create_mco(
            output_file,
            symbol=symbol,
            description=description,
            overwrite=overwrite,
        ),
        McoExecutionContext(work_dir=Path.cwd(), dry_run=dry_run),
    )


def cmd_schlib(args: argparse.Namespace) -> int:
    """Dispatch SchLib subcommands."""
    if getattr(args, "schlib_action", None) == "create":
        return _cmd_schlib_create(args)
    log.error("No SchLib subcommand specified")
    return 1


def _cmd_schlib_create(args: argparse.Namespace) -> int:
    try:
        payload = build_schlib_create_mco(
            args.file,
            symbol=args.symbol,
            description=args.description,
            overwrite=bool(args.force),
        )
        if args.emit_mco is not None:
            _write_json(args.emit_mco, payload, overwrite=bool(args.force))
        result = execute_mco_for_cli(
            payload,
            McoExecutionContext(work_dir=Path.cwd(), dry_run=bool(args.dry_run)),
            json_stdout=bool(args.json),
        )
    except Exception as exc:
        log.error("Failed creating SchLib: %s", exc)
        return 1

    if args.json_output is not None:
        _write_json(args.json_output, result.to_dict(), overwrite=True)
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print_mco_execution_result(
            result,
            title="schlib",
            color=not bool(args.no_color),
        )
    return 0 if result.ok else 1


def _write_json(path: Path, payload: JsonObject, *, overwrite: bool) -> Path:
    if path.exists() and not overwrite:
        raise FileExistsError(f"Output already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path.resolve()


def register_parser(
    subparsers: argparse._SubParsersAction,
) -> argparse.ArgumentParser:
    """Register the schlib command parser."""
    parser = subparsers.add_parser(
        "schlib",
        help="author schematic libraries",
        description="Create Altium .SchLib files through generated MCO operations.",
    )
    action_subparsers = parser.add_subparsers(
        dest="schlib_action",
        metavar="<schlib-action>",
    )

    create_parser = action_subparsers.add_parser(
        "create",
        help="create a new SchLib with one empty symbol",
    )
    create_parser.add_argument("file", type=Path, help="output .SchLib path")
    create_parser.add_argument(
        "--symbol",
        help="initial symbol name (default: output file stem)",
    )
    create_parser.add_argument(
        "--description",
        default="",
        help="symbol description",
    )
    create_parser.add_argument(
        "--emit-mco",
        type=Path,
        help="write the generated MCO JSON file before execution",
    )
    create_parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite an existing SchLib or emitted MCO file",
    )
    create_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate and report planned outputs without writing files",
    )
    create_parser.add_argument(
        "--json",
        action="store_true",
        help="write the MCO execution report JSON to stdout",
    )
    create_parser.add_argument(
        "--json-output",
        type=Path,
        help="write the MCO execution report JSON to this file",
    )
    create_parser.add_argument(
        "--no-color",
        action="store_true",
        help="disable terminal color in human output",
    )
    create_parser.set_defaults(handler=cmd_schlib)
    return parser
