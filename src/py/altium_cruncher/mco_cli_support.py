"""Shared MCO execution and terminal presentation for authoring commands.

Keep native incidental output on stderr when callers request a JSON stdout
result. Business execution remains in altium_cruncher_mco, not in a CLI handler.
"""

from __future__ import annotations

import contextlib
import json
import os
from pathlib import Path
import sys
from colorama import Fore, Style, just_fix_windows_console
from .altium_cruncher_mco import (
    JsonObject,
    McoExecutionContext,
    McoExecutionResult,
    McoOperationResult,
    McoOperationInfo,
    execute_mco,
    mco_operation_catalog,
)


def execute_mco_for_cli(
    payload: JsonObject,
    context: McoExecutionContext,
    *,
    json_stdout: bool = False,
) -> McoExecutionResult:
    """Execute an MCO payload while preserving clean machine-readable stdout."""
    if json_stdout:
        sys.stdout.flush()
        sys.stderr.flush()
        saved_stdout_fd = os.dup(sys.stdout.fileno())
        try:
            os.dup2(sys.stderr.fileno(), sys.stdout.fileno())
            with contextlib.redirect_stdout(sys.stderr):
                return execute_mco(payload, context)
        finally:
            sys.stdout.flush()
            sys.stderr.flush()
            os.dup2(saved_stdout_fd, sys.stdout.fileno())
            os.close(saved_stdout_fd)
    return execute_mco(payload, context)


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
    by_group: dict[str, list[McoOperationInfo]] = {}
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
