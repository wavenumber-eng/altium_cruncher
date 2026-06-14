"""PcbLib authoring commands backed by MCO operations."""

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


def cmd_pcblib(args: argparse.Namespace) -> int:
    """Dispatch PcbLib subcommands."""
    action = getattr(args, "pcblib_action", None)
    if action == "create":
        return _cmd_pcblib_create(args)
    log.error("No PcbLib subcommand specified")
    return 1


def build_pcblib_create_mco(
    output_file: Path | str,
    *,
    footprint: str | None = None,
    height: str = "0mil",
    description: str = "",
    parameters: dict[str, str] | None = None,
    primitive_parameters: dict[str, str] | None = None,
    overwrite: bool = False,
) -> JsonObject:
    """Build the MCO payload for creating a single-footprint PcbLib."""
    file_path = Path(output_file)
    footprint_name = footprint or file_path.stem
    add_footprint_args: JsonObject = {
        "file": str(file_path),
        "name": footprint_name,
        "height": height,
        "description": description,
        "overwrite": True,
    }
    if parameters:
        add_footprint_args["parameters"] = dict(parameters)
    if primitive_parameters:
        add_footprint_args["primitive_parameters"] = dict(primitive_parameters)
    return {
        "schema": MCO_SCHEMA,
        "operations": [
            mco_operation(
                "pcblib.create",
                "create_pcblib",
                "Create PcbLib",
                {
                    "file": str(file_path),
                    "overwrite": overwrite,
                },
            ),
            mco_operation(
                "pcblib.add_footprint",
                "add_footprint",
                "Add initial footprint",
                add_footprint_args,
            ),
        ],
    }


def execute_pcblib_create_mco(
    output_file: Path | str,
    *,
    footprint: str | None = None,
    height: str = "0mil",
    description: str = "",
    parameters: dict[str, str] | None = None,
    primitive_parameters: dict[str, str] | None = None,
    overwrite: bool = False,
    dry_run: bool = False,
) -> McoExecutionResult:
    """Execute the generated PcbLib-create MCO payload."""
    payload = build_pcblib_create_mco(
        output_file,
        footprint=footprint,
        height=height,
        description=description,
        parameters=parameters,
        primitive_parameters=primitive_parameters,
        overwrite=overwrite,
    )
    return execute_mco(
        payload,
        McoExecutionContext(work_dir=Path.cwd(), dry_run=dry_run),
    )


def _cmd_pcblib_create(args: argparse.Namespace) -> int:
    try:
        parameters = _parse_key_value_items(args.parameter)
        primitive_parameters = _parse_key_value_items(args.primitive_parameter)
        payload = build_pcblib_create_mco(
            args.file,
            footprint=args.footprint,
            height=args.height,
            description=args.description,
            parameters=parameters,
            primitive_parameters=primitive_parameters,
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
        log.error("Failed creating PcbLib: %s", exc)
        return 1

    if args.json_output is not None:
        _write_json(args.json_output, result.to_dict(), overwrite=True)
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print_mco_execution_result(
            result,
            title="pcblib",
            color=not bool(args.no_color),
        )
    return 0 if result.ok else 1


def _parse_key_value_items(items: list[str] | None) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in items or []:
        name, separator, value = item.partition("=")
        if not separator or not name.strip():
            raise ValueError(f"Expected NAME=VALUE, got {item!r}")
        result[name.strip()] = value
    return result


def _write_json(path: Path, payload: JsonObject, *, overwrite: bool) -> Path:
    if path.exists() and not overwrite:
        raise FileExistsError(f"Output already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path.resolve()


def register_parser(
    subparsers: argparse._SubParsersAction,
) -> argparse.ArgumentParser:
    """Register the pcblib command parser."""
    parser = subparsers.add_parser(
        "pcblib",
        help="author PCB footprint libraries",
        description=(
            "Create and mutate Altium .PcbLib files through generated MCO "
            "operations. The initial create workflow composes a library from "
            "pcblib.create plus pcblib.add_footprint so future footprint "
            "primitive operators can extend the same path."
        ),
    )
    action_subparsers = parser.add_subparsers(
        dest="pcblib_action",
        metavar="<pcblib-action>",
    )

    create_parser = action_subparsers.add_parser(
        "create",
        help="create a new PcbLib with one initial footprint",
    )
    create_parser.add_argument("file", type=Path, help="output .PcbLib path")
    create_parser.add_argument(
        "--footprint",
        help="initial footprint name (default: output file stem)",
    )
    create_parser.add_argument(
        "--height",
        default="0mil",
        help="footprint height string (default: 0mil)",
    )
    create_parser.add_argument(
        "--description",
        default="",
        help="footprint description",
    )
    create_parser.add_argument(
        "--parameter",
        action="append",
        help="set one footprint Parameters value as NAME=VALUE",
    )
    create_parser.add_argument(
        "--primitive-parameter",
        action="append",
        help="set one footprint PrimitiveParameters value as NAME=VALUE",
    )
    create_parser.add_argument(
        "--emit-mco",
        type=Path,
        help="write the generated MCO JSON file before execution",
    )
    create_parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite an existing PcbLib or emitted MCO file",
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
    create_parser.set_defaults(handler=cmd_pcblib)
    return parser
