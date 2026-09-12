"""MCO command for altium_cruncher."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path


from altium_cruncher.altium_cruncher_mco import execute_mco_file, mco_operation_catalog, write_mco_template

from .mco_cli_support import (
    _mco_operations_jsonc_text as _mco_operations_jsonc_text,
    _print_mco_operation_result as _print_mco_operation_result,
    _style as _style,
    _terminal_color_enabled as _terminal_color_enabled,
    _write_mco_execution_json as _write_mco_execution_json,
    execute_mco_for_cli as execute_mco_for_cli,
    print_mco_execution_result as print_mco_execution_result,
    print_mco_operation_catalog as print_mco_operation_catalog,
)

log = logging.getLogger(__name__)


def cmd_mco(args: argparse.Namespace) -> int:
    """Dispatch MCO subcommands."""
    action = getattr(args, "mco_action", None)
    if action == "run":
        return _cmd_mco_run(args)
    if action == "init":
        return _cmd_mco_init(args)
    if action in {"list", "list-ops"}:
        return _cmd_mco_list(args)
    log.error("No MCO subcommand specified")
    return 1


def _cmd_mco_run(args: argparse.Namespace) -> int:
    try:
        result = execute_mco_file(args.file, dry_run=bool(args.dry_run))
    except Exception as exc:
        log.error("Failed running MCO: %s", exc)
        return 1
    if args.json_output is not None:
        _write_mco_execution_json(result, args.json_output)
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print_mco_execution_result(
            result,
            title=f"MCO {Path(args.file).name}",
            color=not bool(args.no_color),
        )
    return 0 if result.ok else 1


def _cmd_mco_init(args: argparse.Namespace) -> int:
    try:
        output_path = write_mco_template(args.file, overwrite=bool(args.force))
    except Exception as exc:
        log.error("Failed writing MCO template: %s", exc)
        return 1
    print(str(output_path))
    return 0


def _cmd_mco_list(args: argparse.Namespace) -> int:
    payload = {
        "schema": "altium_cruncher.mco.operations.a0",
        "operations": [info.to_dict() for info in mco_operation_catalog()],
    }
    if getattr(args, "output", None) is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            _mco_operations_jsonc_text(payload),
            encoding="utf-8",
        )
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print_mco_operation_catalog(color=not bool(args.no_color))
    return 0


def register_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(
        "mco",
        help="run Monkey Change Order automation files",
        description=(
            "Run Monkey Change Order (MCO) JSONC operation files. "
            "MCO is the execution substrate for generated workflows such as "
            "mate."
        ),
    )
    action_subparsers = parser.add_subparsers(
        dest="mco_action",
        help="MCO subcommands",
    )

    run_parser = action_subparsers.add_parser(
        "run",
        help="execute an MCO JSONC file",
    )
    run_parser.add_argument("file", type=Path, help="MCO JSONC file")
    run_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate and report planned outputs without writing supported operations",
    )
    run_parser.add_argument(
        "--json",
        action="store_true",
        help="write the execution report JSON to stdout",
    )
    run_parser.add_argument(
        "--json-output",
        type=Path,
        help="write the execution report JSON to this file",
    )
    run_parser.add_argument(
        "--no-color",
        action="store_true",
        help="disable terminal color in human output",
    )
    run_parser.set_defaults(handler=cmd_mco)

    init_parser = action_subparsers.add_parser(
        "init",
        help="write an editable MCO JSONC template",
    )
    init_parser.add_argument("file", type=Path, help="template output path")
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite an existing template",
    )
    init_parser.set_defaults(handler=cmd_mco)

    list_parser = action_subparsers.add_parser(
        "list",
        help="list supported MCO operations",
    )
    list_parser.add_argument(
        "--json",
        action="store_true",
        help="write machine-readable operation metadata",
    )
    list_parser.add_argument(
        "--output",
        type=Path,
        help="write JSONC operation metadata to a file",
    )
    list_parser.add_argument(
        "--no-color",
        action="store_true",
        help="disable terminal color in human output",
    )
    list_parser.set_defaults(handler=cmd_mco)

    legacy_list_parser = action_subparsers.add_parser(
        "list-ops",
        help=argparse.SUPPRESS,
    )
    legacy_list_parser.add_argument("--json", action="store_true", default=True)
    legacy_list_parser.add_argument("--output", type=Path)
    legacy_list_parser.add_argument("--no-color", action="store_true")
    legacy_list_parser.set_defaults(handler=cmd_mco)

    parser.set_defaults(handler=cmd_mco)
    return parser
