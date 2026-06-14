"""PcbDoc authoring commands backed by MCO operations."""

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
from altium_cruncher.altium_cruncher_project_profiles import (
    STANDARD_MECHANICAL_LAYER_PROFILE,
    generated_rigid_stack_config,
    standard_mechanical_profile_args,
)

log = logging.getLogger(__name__)


def build_pcbdoc_create_mco(
    output_file: Path | str,
    *,
    layers: int = 2,
    layer_stack_template: str | None = None,
    width_mils: float = 3000.0,
    height_mils: float = 2000.0,
    mechanical_layer_profile: str | None = None,
    overwrite: bool = False,
) -> JsonObject:
    """Build the MCO payload for creating a PcbDoc."""
    args: JsonObject = {
        "file": str(Path(output_file)),
        "overwrite": overwrite,
        "board_outline_mils": {
            "left": 0,
            "bottom": 0,
            "right": width_mils,
            "top": height_mils,
        },
    }
    if layer_stack_template:
        args["layer_stack_template"] = layer_stack_template
    else:
        args["rigid_stack"] = generated_rigid_stack_config(layers)
    if mechanical_layer_profile:
        _merge_mechanical_profile_args(args, mechanical_layer_profile)
    return {
        "schema": MCO_SCHEMA,
        "operations": [
            mco_operation(
                "pcbdoc.create",
                "create_pcbdoc",
                "Create PcbDoc",
                args,
            )
        ],
    }


def execute_pcbdoc_create_mco(
    output_file: Path | str,
    *,
    layers: int = 2,
    layer_stack_template: str | None = None,
    width_mils: float = 3000.0,
    height_mils: float = 2000.0,
    mechanical_layer_profile: str | None = None,
    overwrite: bool = False,
    dry_run: bool = False,
) -> McoExecutionResult:
    """Execute the generated PcbDoc-create MCO payload."""
    return execute_mco(
        build_pcbdoc_create_mco(
            output_file,
            layers=layers,
            layer_stack_template=layer_stack_template,
            width_mils=width_mils,
            height_mils=height_mils,
            mechanical_layer_profile=mechanical_layer_profile,
            overwrite=overwrite,
        ),
        McoExecutionContext(work_dir=Path.cwd(), dry_run=dry_run),
    )


def cmd_pcbdoc(args: argparse.Namespace) -> int:
    """Dispatch PcbDoc subcommands."""
    if getattr(args, "pcbdoc_action", None) == "create":
        return _cmd_pcbdoc_create(args)
    log.error("No PcbDoc subcommand specified")
    return 1


def _cmd_pcbdoc_create(args: argparse.Namespace) -> int:
    try:
        profile = (
            None
            if args.mechanical_layer_profile == "none"
            else args.mechanical_layer_profile
        )
        payload = build_pcbdoc_create_mco(
            args.file,
            layers=args.layers,
            layer_stack_template=args.layer_stack_template,
            width_mils=args.width_mils,
            height_mils=args.height_mils,
            mechanical_layer_profile=profile,
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
        log.error("Failed creating PcbDoc: %s", exc)
        return 1

    if args.json_output is not None:
        _write_json(args.json_output, result.to_dict(), overwrite=True)
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print_mco_execution_result(
            result,
            title="pcbdoc",
            color=not bool(args.no_color),
        )
    return 0 if result.ok else 1


def _merge_mechanical_profile_args(args: JsonObject, profile: str) -> None:
    normalized = profile.strip().lower().replace("-", "_")
    if normalized != STANDARD_MECHANICAL_LAYER_PROFILE:
        raise ValueError(f"Unsupported mechanical layer profile: {profile!r}")
    args.update(standard_mechanical_profile_args())


def _write_json(path: Path, payload: JsonObject, *, overwrite: bool) -> Path:
    if path.exists() and not overwrite:
        raise FileExistsError(f"Output already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path.resolve()


def register_parser(
    subparsers: argparse._SubParsersAction,
) -> argparse.ArgumentParser:
    """Register the pcbdoc command parser."""
    parser = subparsers.add_parser(
        "pcbdoc",
        help="author PCB documents",
        description="Create Altium .PcbDoc files through generated MCO operations.",
    )
    action_subparsers = parser.add_subparsers(
        dest="pcbdoc_action",
        metavar="<pcbdoc-action>",
    )

    create_parser = action_subparsers.add_parser(
        "create",
        help="create a new PCB document",
    )
    create_parser.add_argument("file", type=Path, help="output .PcbDoc path")
    create_parser.add_argument(
        "--layers",
        type=int,
        default=2,
        help="generated rigid copper layer count (default: 2)",
    )
    create_parser.add_argument(
        "--layer-stack-template",
        help="use an Altium Monkey layer-stack template instead of generated rigid rows",
    )
    create_parser.add_argument(
        "--width-mils",
        type=float,
        default=3000.0,
        help="rectangular board width in mils (default: 3000)",
    )
    create_parser.add_argument(
        "--height-mils",
        type=float,
        default=2000.0,
        help="rectangular board height in mils (default: 2000)",
    )
    create_parser.add_argument(
        "--mechanical-layer-profile",
        choices=("none", STANDARD_MECHANICAL_LAYER_PROFILE),
        default="none",
        help="optional mechanical layer/kind initialization profile",
    )
    create_parser.add_argument(
        "--emit-mco",
        type=Path,
        help="write the generated MCO JSON file before execution",
    )
    create_parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite an existing PcbDoc or emitted MCO file",
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
    create_parser.set_defaults(handler=cmd_pcbdoc)
    return parser
