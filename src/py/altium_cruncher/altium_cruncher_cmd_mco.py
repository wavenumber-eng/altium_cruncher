"""MCO command for altium_cruncher."""

from __future__ import annotations

import argparse
import json
import logging
import os
from pathlib import Path
import sys

from colorama import Fore, Style, just_fix_windows_console

from altium_cruncher.altium_cruncher_mco import (
    McoExecutionResult,
    McoOperationResult,
    execute_mco_file,
    mco_operation_catalog,
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


def print_mco_execution_result(
    result: McoExecutionResult,
    *,
    title: str = "MCO",
    color: bool = True,
) -> None:
    """Print a concise human-readable MCO execution report."""
    use_color = color and _terminal_color_enabled()
    if use_color:
        just_fix_windows_console()
    failures = [item for item in result.results if not item.is_ok]
    status = "ok" if result.ok else "failed"
    status_color = Fore.GREEN if result.ok else Fore.RED
    mode = "dry run" if result.dry_run else "run"
    print(
        _style(
            f"{title}: {status} ({len(result.results)} operations, "
            f"{len(failures)} errors, {mode})",
            status_color,
            use_color,
            bright=True,
        )
    )
    for item in result.results:
        _print_mco_operation_result(item, use_color=use_color)
    print(
        _style(
            f"{title} complete: {status}, {len(result.results)} operations, "
            f"{len(failures)} errors",
            status_color,
            use_color,
            bright=True,
        )
    )


def _print_mco_operation_result(
    item: McoOperationResult,
    *,
    use_color: bool,
) -> None:
    label = "OK" if item.is_ok else "FAIL"
    label_color = Fore.GREEN if item.is_ok else Fore.RED
    op = _style(item.op, Fore.CYAN, use_color)
    operation_id = _style(item.operation_id, Fore.WHITE, use_color)
    styled_label = _style(label, label_color, use_color, bright=True)
    message = item.message or f"{item.op} {item.operation_id}"
    print(f"  {styled_label:<4} {message}")
    print(f"       {op} {operation_id}")
    if item.error and not item.is_ok:
        print(f"       {_style(item.error, Fore.RED, use_color)}")


def print_mco_operation_catalog(*, color: bool = True) -> None:
    """Print MCO operation metadata grouped by functional area."""
    use_color = color and _terminal_color_enabled()
    if use_color:
        just_fix_windows_console()
    by_group: dict[str, list[object]] = {}
    for info in mco_operation_catalog():
        by_group.setdefault(info.group, []).append(info)
    for group in sorted(by_group):
        print(_style(group, Fore.YELLOW, use_color, bright=True))
        for info in by_group[group]:
            op = _style(info.name, Fore.CYAN, use_color)
            print(f"  {op}")
            print(f"    {info.summary}")
            if info.required_args:
                print(f"    required: {', '.join(info.required_args)}")
            if info.optional_args:
                print(f"    optional: {', '.join(info.optional_args)}")


def _write_mco_execution_json(result: McoExecutionResult, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result.to_dict(), indent=2) + "\n",
        encoding="utf-8",
    )


def _mco_operations_jsonc_text(payload: dict[str, object]) -> str:
    return (
        "// Supported MCO operation catalog for this altium-cruncher version.\n"
        "// Each operation lists required_args and optional_args separately.\n"
        + json.dumps(payload, indent=2, sort_keys=True)
        + "\n"
    )


def _terminal_color_enabled() -> bool:
    if os.environ.get("NO_COLOR") is not None or os.environ.get("TERM") == "dumb":
        return False
    isatty = getattr(sys.stdout, "isatty", None)
    return bool(callable(isatty) and isatty())


def _style(text: str, color: str, enabled: bool, *, bright: bool = False) -> str:
    if not enabled:
        return text
    prefix = f"{Style.BRIGHT if bright else ''}{color}"
    return f"{prefix}{text}{Style.RESET_ALL}"


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
