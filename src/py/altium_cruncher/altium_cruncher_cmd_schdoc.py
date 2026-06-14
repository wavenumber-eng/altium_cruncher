"""SchDoc authoring commands backed by MCO operations."""

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


def build_schdoc_create_mco(
    output_file: Path | str,
    *,
    sheet_style: str = "D",
    template: Path | str | None = None,
    apply_template_visual_sheet_settings: bool = False,
    custom_sheet_mils: tuple[float, float] | None = None,
    overwrite: bool = False,
) -> JsonObject:
    """Build the MCO payload for creating a SchDoc."""
    args: JsonObject = {
        "file": str(Path(output_file)),
        "sheet_style": sheet_style,
        "overwrite": overwrite,
    }
    if template is not None:
        args["template"] = str(template)
        args["apply_template_visual_sheet_settings"] = (
            apply_template_visual_sheet_settings
        )
    if custom_sheet_mils is not None:
        args["custom_sheet_mils"] = {
            "width": custom_sheet_mils[0],
            "height": custom_sheet_mils[1],
        }
    return {
        "schema": MCO_SCHEMA,
        "operations": [
            mco_operation(
                "schdoc.create",
                "create_schdoc",
                "Create SchDoc",
                args,
            )
        ],
    }


def execute_schdoc_create_mco(
    output_file: Path | str,
    *,
    sheet_style: str = "D",
    template: Path | str | None = None,
    apply_template_visual_sheet_settings: bool = False,
    custom_sheet_mils: tuple[float, float] | None = None,
    overwrite: bool = False,
    dry_run: bool = False,
) -> McoExecutionResult:
    """Execute the generated SchDoc-create MCO payload."""
    return execute_mco(
        build_schdoc_create_mco(
            output_file,
            sheet_style=sheet_style,
            template=template,
            apply_template_visual_sheet_settings=apply_template_visual_sheet_settings,
            custom_sheet_mils=custom_sheet_mils,
            overwrite=overwrite,
        ),
        McoExecutionContext(work_dir=Path.cwd(), dry_run=dry_run),
    )


def cmd_schdoc(args: argparse.Namespace) -> int:
    """Dispatch SchDoc subcommands."""
    if getattr(args, "schdoc_action", None) == "create":
        return _cmd_schdoc_create(args)
    help_parser = getattr(args, "_schdoc_parser", None)
    if help_parser is not None:
        help_parser.print_help()
        return 0
    log.error("No SchDoc subcommand specified")
    return 1


def _cmd_schdoc_create(args: argparse.Namespace) -> int:
    try:
        custom_sheet_mils = None
        if args.custom_width_mils is not None or args.custom_height_mils is not None:
            if args.custom_width_mils is None or args.custom_height_mils is None:
                raise ValueError(
                    "--custom-width-mils and --custom-height-mils must be used together"
                )
            custom_sheet_mils = (args.custom_width_mils, args.custom_height_mils)
        payload = build_schdoc_create_mco(
            args.file,
            sheet_style=args.sheet_style,
            template=args.template,
            apply_template_visual_sheet_settings=bool(
                args.apply_template_visual_sheet_settings
            ),
            custom_sheet_mils=custom_sheet_mils,
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
        log.error("Failed creating SchDoc: %s", exc)
        return 1

    if args.json_output is not None:
        _write_json(args.json_output, result.to_dict(), overwrite=True)
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print_mco_execution_result(
            result,
            title="schdoc",
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
    """Register the schdoc command parser."""
    parser = subparsers.add_parser(
        "schdoc",
        help="author schematic documents",
        description="Create Altium .SchDoc files through generated MCO operations.",
    )
    action_subparsers = parser.add_subparsers(
        dest="schdoc_action",
        metavar="<schdoc-action>",
    )
    parser.set_defaults(handler=cmd_schdoc, _schdoc_parser=parser)

    create_parser = action_subparsers.add_parser(
        "create",
        help="create a new schematic document",
    )
    create_parser.add_argument("file", type=Path, help="output .SchDoc path")
    create_parser.add_argument(
        "--sheet-style",
        default="D",
        help="Altium SheetStyle enum name or integer (default: D)",
    )
    create_parser.add_argument(
        "--template",
        type=Path,
        help="optional .SchDot template to apply",
    )
    create_parser.add_argument(
        "--apply-template-visual-sheet-settings",
        action="store_true",
        help="also copy visual sheet settings from the template",
    )
    create_parser.add_argument(
        "--custom-width-mils",
        type=float,
        help="custom schematic sheet width in mils",
    )
    create_parser.add_argument(
        "--custom-height-mils",
        type=float,
        help="custom schematic sheet height in mils",
    )
    create_parser.add_argument(
        "--emit-mco",
        type=Path,
        help="write the generated MCO JSON file before execution",
    )
    create_parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite an existing SchDoc or emitted MCO file",
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
    create_parser.set_defaults(handler=cmd_schdoc)
    return parser
