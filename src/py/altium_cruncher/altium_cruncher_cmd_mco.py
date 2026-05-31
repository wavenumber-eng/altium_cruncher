"""MCO command for altium_cruncher."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from altium_cruncher.altium_cruncher_mco import (
    available_mco_operations,
    execute_mco_file,
    write_mco_template,
)

log = logging.getLogger(__name__)


def cmd_mco(args: argparse.Namespace) -> int:
    """Dispatch MCO subcommands."""
    action = getattr(args, "mco_action", None)
    if action == "run":
        return _cmd_mco_run(args)
    if action == "init":
        return _cmd_mco_init(args)
    if action == "list-ops":
        return _cmd_mco_list_ops()
    log.error("No MCO subcommand specified")
    return 1


def _cmd_mco_run(args: argparse.Namespace) -> int:
    try:
        result = execute_mco_file(args.file, dry_run=bool(args.dry_run))
    except Exception as exc:
        log.error("Failed running MCO: %s", exc)
        return 1
    payload = result.to_dict()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if result.ok else 1


def _cmd_mco_init(args: argparse.Namespace) -> int:
    try:
        output_path = write_mco_template(args.file, overwrite=bool(args.force))
    except Exception as exc:
        log.error("Failed writing MCO template: %s", exc)
        return 1
    print(str(output_path))
    return 0


def _cmd_mco_list_ops() -> int:
    payload = {"operations": available_mco_operations()}
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def register_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(
        "mco",
        help="run Monkey Change Order automation files",
        description=(
            "Run Monkey Change Order (MCO) JSONC operation files. "
            "MCO is the execution substrate for generated workflows such as "
            "debug-plate."
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
        "list-ops",
        help="list registered MCO operation names",
    )
    list_parser.set_defaults(handler=cmd_mco)

    parser.set_defaults(handler=cmd_mco)
    return parser
