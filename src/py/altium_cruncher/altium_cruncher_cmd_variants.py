"""Inspect and edit PrjPcb project variants."""

from __future__ import annotations

import argparse
import json
import os
from collections.abc import Callable
from pathlib import Path
import sys

from rich import box
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from altium_cruncher.altium_cruncher_common import find_prjpcbs_in_cwd
from altium_cruncher.altium_cruncher_mco import (
    MCO_SCHEMA,
    McoExecutionContext,
    McoExecutionResult,
    execute_mco,
)
from altium_cruncher.bom_pnp_model import designator_sort_key


class VariantsCommandError(ValueError):
    """Raised when the variants command cannot resolve user input."""


MutationBuilder = Callable[[argparse.Namespace], tuple[str, dict[str, object]]]


def cmd_variants(args: argparse.Namespace) -> int:
    """Dispatch variants subcommands."""
    action = getattr(args, "variants_action", None)
    if action is None:
        action = "list"
    try:
        project_path = _resolve_project_path(
            getattr(args, "project_file", None),
            getattr(args, "project", None),
        )
        if action == "list":
            return _cmd_variants_list(args, project_path)
        missing = _missing_mutation_args(action, args)
        if missing:
            raise VariantsCommandError(
                _missing_mutation_args_message(action, missing, project_path)
            )
        op, op_args = _mutation_operation_for_args(action, args)
        return _cmd_variants_mutation(args, project_path, op, op_args)
    except Exception as exc:
        _print_variants_error(f"variants {action} failed: {exc}")
        return 1

    print(f"Unknown variants subcommand: {action}", file=sys.stderr)
    return 1


def _mutation_operation_for_args(
    action: str,
    args: argparse.Namespace,
) -> tuple[str, dict[str, object]]:
    builder = _MUTATION_BUILDERS.get(action)
    if builder is None:
        raise VariantsCommandError(f"Unknown variants subcommand: {action}")
    return builder(args)


def _delete_operation_args(args: argparse.Namespace) -> tuple[str, dict[str, object]]:
    return "project.delete_variant", {"name": args.name}


def _rename_operation_args(args: argparse.Namespace) -> tuple[str, dict[str, object]]:
    return "project.rename_variant", {"name": args.name, "new_name": args.new_name}


def _clone_operation_args(args: argparse.Namespace) -> tuple[str, dict[str, object]]:
    op_args: dict[str, object] = {
        "source_name": args.source_name,
        "name": args.name,
    }
    if args.unique_id:
        op_args["unique_id"] = args.unique_id
    if args.allow_fabrication is not None:
        op_args["allow_fabrication"] = bool(args.allow_fabrication)
    if args.current:
        op_args["current"] = True
    return "project.clone_variant", op_args


def _toggle_dnp_operation_args(
    args: argparse.Namespace,
) -> tuple[str, dict[str, object]]:
    op_args: dict[str, object] = {
        "variant": args.variant,
        "designator": args.designator,
    }
    if args.unique_id:
        op_args["unique_id"] = args.unique_id
    if args.alternate_part:
        op_args["alternate_part"] = args.alternate_part
    return "project.toggle_variant_dnp", op_args


_MUTATION_BUILDERS: dict[str, MutationBuilder] = {
    "delete": _delete_operation_args,
    "rename": _rename_operation_args,
    "clone": _clone_operation_args,
    "toggle-dnp": _toggle_dnp_operation_args,
}

_MUTATION_REQUIRED_ARGS: dict[str, tuple[str, ...]] = {
    "delete": ("name",),
    "rename": ("name", "new_name"),
    "clone": ("source_name", "name"),
    "toggle-dnp": ("variant", "designator"),
}

_MUTATION_USAGE: dict[str, str] = {
    "delete": "acr variants delete NAME [project.PrjPcb]",
    "rename": "acr variants rename NAME NEW_NAME [project.PrjPcb]",
    "clone": "acr variants clone SOURCE_NAME NAME [project.PrjPcb]",
    "toggle-dnp": "acr variants toggle-dnp VARIANT DESIGNATOR [project.PrjPcb]",
}


def _missing_mutation_args(action: str, args: argparse.Namespace) -> list[str]:
    return [
        name
        for name in _MUTATION_REQUIRED_ARGS.get(action, ())
        if not str(getattr(args, name, "") or "").strip()
    ]


def _missing_mutation_args_message(
    action: str,
    missing: list[str],
    project_path: Path,
) -> str:
    missing_args = ", ".join(missing)
    lines = [f"missing required argument(s): {missing_args}"]
    usage = _MUTATION_USAGE.get(action)
    if usage:
        lines.append(f"Usage: {usage}")
    variants = _available_variant_names(project_path)
    if variants:
        lines.append(f"Available variants: {', '.join(variants)}")
    else:
        lines.append("Available variants: none")
    return "\n".join(lines)


def _available_variant_names(project_path: Path) -> list[str]:
    from altium_monkey.altium_prjpcb import AltiumPrjPcb

    project = AltiumPrjPcb(project_path)
    return [str(name) for name in project.variants]


def _cmd_variants_list(args: argparse.Namespace, project_path: Path) -> int:
    result = _execute_project_operation(
        project_path,
        "project.list_variants",
        {},
        dry_run=True,
    )
    if not result.ok:
        _print_mco_errors(result)
        return 1
    payload = _single_result_outputs(result)
    if getattr(args, "json", False):
        print(json.dumps(payload, indent=2))
    else:
        print_variants_summary(
            payload,
            color=not bool(getattr(args, "no_color", False)),
        )
    return 0


def _cmd_variants_mutation(
    args: argparse.Namespace,
    project_path: Path,
    op: str,
    op_args: dict[str, object],
) -> int:
    result = _execute_project_operation(
        project_path,
        op,
        op_args,
        dry_run=bool(getattr(args, "dry_run", False)),
    )
    if getattr(args, "json", False):
        print(json.dumps(result.to_dict(), indent=2))
        return 0 if result.ok else 1
    if not result.ok:
        _print_mco_errors(result)
        return 1
    item = result.results[0]
    mode = "dry run: " if result.dry_run else ""
    print()
    print(f"{mode}{item.message}")
    print()
    return 0


def _execute_project_operation(
    project_path: Path,
    op: str,
    op_args: dict[str, object],
    *,
    dry_run: bool,
) -> McoExecutionResult:
    args = {"file": str(project_path), **op_args}
    payload = {
        "schema": MCO_SCHEMA,
        "operations": [
            {
                "op": op,
                "id": op.replace(".", "_"),
                "args": args,
            }
        ],
    }
    return execute_mco(
        payload,
        McoExecutionContext(work_dir=project_path.parent, dry_run=dry_run),
    )


def _single_result_outputs(result: McoExecutionResult) -> dict[str, object]:
    if not result.results:
        raise VariantsCommandError("MCO operation produced no result")
    return dict(result.results[0].outputs)


def _print_mco_errors(result: McoExecutionResult) -> None:
    print(file=sys.stderr)
    for item in result.results:
        if item.is_ok:
            continue
        print(item.error or item.message, file=sys.stderr)
    print(file=sys.stderr)


def _print_variants_error(message: str) -> None:
    print(file=sys.stderr)
    print(message, file=sys.stderr)
    print(file=sys.stderr)


def _resolve_project_path(
    positional: Path | str | None,
    explicit: Path | str | None,
) -> Path:
    if positional is not None and explicit is not None:
        raise VariantsCommandError("pass either a project path or --project, not both")
    if explicit is not None:
        return _validate_project_path(Path(explicit))
    if positional is not None:
        return _validate_project_path(Path(positional))
    projects = [project.resolve() for project in find_prjpcbs_in_cwd()]
    if len(projects) == 1:
        return projects[0]
    if not projects:
        raise VariantsCommandError(
            "No .PrjPcb file found in the current directory; pass a project explicitly."
        )
    project_list = "\n".join(f"  {project.name}" for project in projects)
    raise VariantsCommandError(
        "Multiple .PrjPcb files found in the current directory; pass one explicitly "
        f"or use --project:\n{project_list}"
    )


def _validate_project_path(path: Path) -> Path:
    project = path.resolve()
    if project.suffix.lower() != ".prjpcb":
        raise VariantsCommandError(f"Expected a .PrjPcb project, got: {project}")
    if not project.is_file():
        raise FileNotFoundError(f"Project not found: {project}")
    return project


def print_variants_summary(
    payload: dict[str, object],
    *,
    color: bool = True,
) -> None:
    """Print project variants in grouped table form."""
    use_color = color and _terminal_color_enabled()
    console = _rich_console(use_color=use_color)
    project = Path(str(payload.get("project", "") or ""))
    console.print()
    console.print(_text(f"Project: {project.name}", "bold white", use_color))
    console.print()
    _print_variant_summary_section(payload, console=console, use_color=use_color)
    console.print()
    _print_variant_change_sections(payload, console=console, use_color=use_color)
    _print_index_warnings(payload, console=console, use_color=use_color)
    console.print()


def _print_variant_summary_section(
    payload: dict[str, object],
    *,
    console: Console,
    use_color: bool,
) -> None:
    variants = list(payload.get("variants", []) or [])
    if not variants:
        console.print("  No variants defined.")
        return

    table = Table(
        box=_table_box(use_color),
        expand=True,
        header_style=_header_style(use_color),
        safe_box=not use_color,
    )
    table.add_column("Variant", min_width=8, overflow="fold")
    table.add_column("Current", justify="center", no_wrap=True)
    table.add_column("Fab", justify="center", no_wrap=True)
    table.add_column("DNP", justify="right", no_wrap=True)
    table.add_column("Changes", justify="right", no_wrap=True)
    for variant in variants:
        table.add_row(*_variant_summary_row(variant))
    console.print(table)


def _print_variant_change_sections(
    payload: dict[str, object],
    *,
    console: Console,
    use_color: bool,
) -> None:
    rows = list(payload.get("rows", []) or [])
    console.print(_text("Changes By Variant", "bold yellow", use_color))
    if not rows:
        console.print("  No DNP or parameter changes.")
        return

    for variant_name, variant_rows in _rows_by_variant(payload, rows).items():
        sheet_renderables: list[object] = []
        for sheet, sheet_rows in _rows_by_sheet(variant_rows).items():
            sheet_renderables.append(_text(str(sheet), "bold magenta", use_color))
            sheet_renderables.append(
                _change_table_for_sheet(sheet_rows, use_color=use_color)
            )
        console.print(
            Panel(
                Group(*sheet_renderables),
                title=f"Variant {variant_name}",
                box=_panel_box(use_color),
                expand=True,
                border_style="yellow" if use_color else "",
                safe_box=not use_color,
            )
        )


def _print_index_warnings(
    payload: dict[str, object],
    *,
    console: Console,
    use_color: bool,
) -> None:
    errors = payload.get("index_errors", []) or []
    if errors:
        console.print()
        console.print(_text("Schematic index warnings", "bold yellow", use_color))
        for error in errors:
            console.print(f"  {error}")


def _change_table_for_sheet(
    sheet_rows: list[dict[str, object]],
    *,
    use_color: bool,
) -> Table:
    table = Table(
        box=_table_box(use_color),
        expand=True,
        header_style=_header_style(use_color),
        safe_box=not use_color,
    )
    table.add_column("Designator", min_width=10, no_wrap=True)
    table.add_column("Value", min_width=8, max_width=18, overflow="fold")
    table.add_column("Op", min_width=9, no_wrap=True)
    table.add_column("Detail", ratio=1, overflow="fold")
    for row in sheet_rows:
        designator, value, operation, detail = _change_table_row(row)
        table.add_row(
            designator,
            value,
            _operation_text(operation, use_color),
            detail,
        )
    return table


def _change_table_row(row: dict[str, object]) -> list[str]:
    return [
        str(row.get("designator", "") or ""),
        str(row.get("component_value", "") or ""),
        str(row.get("operation", "") or ""),
        _pretty_detail(row),
    ]


def _pretty_detail(row: dict[str, object]) -> str:
    detail = str(row.get("detail", "") or "")
    if row.get("operation") != "DNP":
        return _strip_expression_source_notes(detail)
    alternate = str(row.get("alternate_part_resolved", "") or "")
    if alternate:
        return f"not fitted; alternate_part={alternate}"
    return "not fitted"


def _strip_expression_source_notes(detail: str) -> str:
    return detail.replace(" (from =Value)", "")


def _variant_summary_row(variant: object) -> list[str]:
    data = dict(variant if isinstance(variant, dict) else {})
    dnp = [str(item) for item in data.get("dnp", []) or []]
    changes = (
        int(data.get("variation_count", 0) or 0)
        + int(data.get("parameter_count", 0) or 0)
        + int(data.get("param_variation_count", 0) or 0)
    )
    return [
        str(data.get("name", "") or ""),
        "*" if bool(data.get("current")) else "",
        "yes" if bool(data.get("allow_fabrication")) else "no",
        str(len(dnp)),
        str(changes),
    ]


def _rows_by_variant(
    payload: dict[str, object],
    rows: list[object],
) -> dict[str, list[dict[str, object]]]:
    grouped = {name: [] for name in _variant_names_from_payload(payload)}
    for row in _sorted_variant_rows(rows):
        grouped.setdefault(_row_variant_name(row), []).append(row)
    return {name: variant_rows for name, variant_rows in grouped.items() if variant_rows}


def _variant_names_from_payload(payload: dict[str, object]) -> list[str]:
    names: list[str] = []
    for variant in payload.get("variants", []) or []:
        if isinstance(variant, dict):
            name = str(variant.get("name", "") or "")
            if name:
                names.append(name)
    return names


def _sorted_variant_rows(rows: list[object]) -> list[dict[str, object]]:
    clean_rows = [dict(row) for row in rows if isinstance(row, dict)]
    return sorted(
        clean_rows,
        key=lambda row: (
            str(row.get("variant", "") or "").lower(),
            str(row.get("sheet", "") or ""),
            designator_sort_key(str(row.get("designator", "") or "")),
            str(row.get("operation", "") or "").lower(),
        ),
    )


def _row_variant_name(row: dict[str, object]) -> str:
    return str(row.get("variant", "") or "(unknown variant)")


def _rows_by_sheet(rows: list[object]) -> dict[str, list[dict[str, object]]]:
    result: dict[str, list[dict[str, object]]] = {}
    clean_rows = [dict(row) for row in rows if isinstance(row, dict)]
    clean_rows.sort(
        key=lambda row: (
            str(row.get("sheet", "") or ""),
            designator_sort_key(str(row.get("designator", "") or "")),
            str(row.get("variant", "") or "").lower(),
        )
    )
    for row in clean_rows:
        result.setdefault(str(row.get("sheet", "") or "(unknown sheet)"), []).append(row)
    return result


def _operation_text(value: str, enabled: bool) -> Text:
    normalized = value.lower()
    if normalized == "dnp":
        return _text(value, "bold red", enabled)
    if normalized in {"parameter", "variant_parameter"}:
        return _text(value, "cyan", enabled)
    return _text(value, "yellow", enabled)


def _rich_console(*, use_color: bool) -> Console:
    return Console(
        no_color=not use_color,
        highlight=False,
        soft_wrap=False,
        force_terminal=use_color,
    )


def _table_box(use_color: bool) -> box.Box:
    return box.SIMPLE_HEAVY if use_color else box.ASCII


def _panel_box(use_color: bool) -> box.Box:
    return box.ROUNDED if use_color else box.ASCII


def _header_style(use_color: bool) -> str:
    return "reverse bold white" if use_color else "bold"


def _terminal_color_enabled() -> bool:
    if os.environ.get("NO_COLOR") is not None or os.environ.get("TERM") == "dumb":
        return False
    isatty = getattr(sys.stdout, "isatty", None)
    return bool(callable(isatty) and isatty())


def _text(text: str, style: str, enabled: bool) -> Text:
    if not enabled:
        return Text(text)
    return Text(text, style=style)


def register_parser(
    subparsers: argparse._SubParsersAction,
) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(
        "variants",
        help="inspect and edit PrjPcb project variants",
        description=(
            "Inspect and edit project variants in an Altium .PrjPcb file. "
            "With no subcommand, runs list. "
            "When no project is passed, the command auto-detects exactly one "
            ".PrjPcb in the current directory."
        ),
    )
    parser.add_argument(
        "--project",
        type=Path,
        help="explicit .PrjPcb project path",
    )
    action_subparsers = parser.add_subparsers(
        dest="variants_action",
        metavar="<variants-action>",
    )

    list_parser = action_subparsers.add_parser(
        "list",
        help="list variants and part changes",
    )
    list_parser.add_argument(
        "project_file",
        nargs="?",
        type=Path,
        help="PrjPcb file (optional if PrjPcb in CWD)",
    )
    _add_project_option(list_parser)
    list_parser.add_argument("--json", action="store_true", help="write JSON")
    list_parser.add_argument(
        "--no-color",
        action="store_true",
        help="disable terminal color in human output",
    )
    list_parser.set_defaults(handler=cmd_variants)

    delete_parser = action_subparsers.add_parser(
        "delete",
        help="delete one variant",
    )
    delete_parser.add_argument("name", nargs="?", help="variant name to delete")
    _add_optional_project_and_common_mutation_args(delete_parser)

    rename_parser = action_subparsers.add_parser(
        "rename",
        help="rename one variant",
    )
    rename_parser.add_argument("name", nargs="?", help="variant name to rename")
    rename_parser.add_argument("new_name", nargs="?", help="new variant name")
    _add_optional_project_and_common_mutation_args(rename_parser)

    clone_parser = action_subparsers.add_parser(
        "clone",
        help="clone an existing variant",
    )
    clone_parser.add_argument("source_name", nargs="?", help="variant name to clone")
    clone_parser.add_argument("name", nargs="?", help="new variant name")
    clone_parser.add_argument("--unique-id", help="explicit new variant UniqueId")
    clone_parser.add_argument(
        "--allow-fabrication",
        dest="allow_fabrication",
        action="store_true",
        default=None,
        help="set AllowFabrication=1 on the cloned variant",
    )
    clone_parser.add_argument(
        "--no-allow-fabrication",
        dest="allow_fabrication",
        action="store_false",
        help="set AllowFabrication=0 on the cloned variant",
    )
    clone_parser.add_argument(
        "--current",
        action="store_true",
        help="make the cloned variant the current project variant",
    )
    _add_optional_project_and_common_mutation_args(clone_parser)

    _add_dnp_parser(
        action_subparsers,
        "toggle-dnp",
        help_text="toggle one designator DNP in a variant",
    )

    parser.set_defaults(handler=cmd_variants)
    return parser


def _add_dnp_parser(
    action_subparsers: argparse._SubParsersAction,
    name: str,
    *,
    help_text: str,
) -> argparse.ArgumentParser:
    dnp_parser = action_subparsers.add_parser(name, help=help_text)
    dnp_parser.add_argument("variant", nargs="?", help="variant to edit")
    dnp_parser.add_argument(
        "designator",
        nargs="?",
        help="component designator to toggle DNP",
    )
    dnp_parser.add_argument(
        "--unique-id",
        help="Altium variation UniqueId; inferred for simple non-channel schematics",
    )
    dnp_parser.add_argument(
        "--alternate-part",
        default="",
        help="optional AlternatePart value for the variation row",
    )
    _add_optional_project_and_common_mutation_args(dnp_parser)
    return dnp_parser


def _add_optional_project_and_common_mutation_args(
    parser: argparse.ArgumentParser,
) -> None:
    parser.add_argument(
        "project_file",
        nargs="?",
        type=Path,
        help="PrjPcb file (optional if PrjPcb in CWD)",
    )
    _add_project_option(parser)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate and report without writing the project file",
    )
    parser.add_argument("--json", action="store_true", help="write MCO result JSON")
    parser.set_defaults(handler=cmd_variants)


def _add_project_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--project",
        type=Path,
        default=argparse.SUPPRESS,
        help="explicit .PrjPcb project path",
    )
