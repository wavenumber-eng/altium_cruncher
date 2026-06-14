"""Project skeleton commands backed by MCO operations."""

from __future__ import annotations

import argparse
import json
import logging
import os
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
from altium_cruncher.config_json import load_json_config, render_commented_jsonc

PROJECT_CONFIG_SCHEMA = "wn.altium_cruncher.project_skeleton.v1"

log = logging.getLogger(__name__)


def default_project_config(
    *,
    project_name: str = "generated_project",
    layer_count: int = 2,
) -> JsonObject:
    """Return the editable default project skeleton config."""
    return {
        "schema": PROJECT_CONFIG_SCHEMA,
        "project": {
            "file": f"{project_name}.PrjPcb",
            "name": project_name,
            "parameters": {
                "ProjectName": project_name,
            },
        },
        "schematics": [
            {
                "file": f"{project_name}.SchDoc",
                "sheet_style": "D",
            }
        ],
        "pcb": {
            "file": f"{project_name}.PcbDoc",
            "board_outline_mils": {
                "left": 0,
                "bottom": 0,
                "right": 3000,
                "top": 2000,
            },
            "layer_stack": generated_rigid_stack_config(layer_count),
            "mechanical_layer_profile": STANDARD_MECHANICAL_LAYER_PROFILE,
        },
    }


def render_project_config(config: JsonObject) -> str:
    """Render a project skeleton config as commented JSONC."""
    return render_commented_jsonc(
        config,
        comments_by_path={
            ("schema",): "Project skeleton config contract id.",
            ("project",): "PrjPcb output and project-level parameters.",
            ("schematics",): "SchDoc sheets to create and add to the project.",
            ("pcb",): "PcbDoc output, board outline, layer stack, and mechanical profile.",
            ("pcb", "layer_stack"): (
                "Generated rigid stack. stackup/stackupx import is intentionally "
                "not part of this release contract."
            ),
        },
        comments_by_key={
            "file": "Path relative to this config file unless absolute.",
            "sheet_style": "Altium SheetStyle enum name or integer. Default sheets use D.",
            "parameters": "Project-level PrjPcb parameters.",
            "mechanical_layer_profile": (
                "Options: standard_component_pairs or none. The generated MCO expands "
                "the standard profile into editable layer, pair, and kind rows."
            ),
        },
        header_lines=(
            "altium-cruncher project skeleton config.",
            "This file is JSONC: comments and trailing commas are accepted.",
        ),
    )


def write_project_config(
    path: Path | str,
    config: JsonObject,
    *,
    overwrite: bool = False,
) -> Path:
    """Write a project skeleton config file."""
    output_path = Path(path)
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"Config already exists: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_project_config(config), encoding="utf-8")
    return output_path.resolve()


def load_project_config(path: Path | str) -> JsonObject:
    """Load and validate a project skeleton config file."""
    payload = load_json_config(Path(path))
    if not isinstance(payload, dict):
        raise ValueError("Project config root must be an object")
    config = dict(payload)
    schema = config.get("schema")
    if schema != PROJECT_CONFIG_SCHEMA:
        raise ValueError(f"Unsupported project config schema: {schema!r}")
    return config


def build_project_create_mco(config: JsonObject, *, overwrite: bool = False) -> JsonObject:
    """Compile a project skeleton config to MCO operations."""
    project = _object(config.get("project"), "project")
    project_file = _string(project.get("file"), "project.file")
    document_files, document_operations = _document_create_operations(config, overwrite)
    operations = [
        _project_create_operation(project, project_file, overwrite),
        *_project_parameter_operations(project, project_file),
        *document_operations,
        *_project_document_operations(project_file, document_files),
    ]
    return {"schema": MCO_SCHEMA, "operations": operations}


def _project_create_operation(
    project: JsonObject,
    project_file: str,
    overwrite: bool,
) -> JsonObject:
    return mco_operation(
        "project.create",
        "create_project",
        "Create project",
        {
            "file": project_file,
            "name": str(project.get("name") or Path(project_file).stem),
            "overwrite": overwrite,
        },
    )


def _project_parameter_operations(
    project: JsonObject,
    project_file: str,
) -> list[JsonObject]:
    return [
        mco_operation(
            "project.add_parameter",
            f"set_project_parameter_{index}",
            f"Set project parameter {name}",
            {"file": project_file, "name": name, "value": value},
        )
        for index, (name, value) in enumerate(_parameters(project).items(), start=1)
    ]


def _document_create_operations(
    config: JsonObject,
    overwrite: bool,
) -> tuple[list[str], list[JsonObject]]:
    document_files: list[str] = []
    operations: list[JsonObject] = []
    for index, sheet in enumerate(_object_list(config.get("schematics"), "schematics")):
        sheet_file, operation = _schematic_create_operation(index, sheet, overwrite)
        document_files.append(sheet_file)
        operations.append(operation)

    pcb_file, pcb_operation = _pcb_create_operation(config.get("pcb"), overwrite)
    if pcb_file is not None and pcb_operation is not None:
        document_files.append(pcb_file)
        operations.append(pcb_operation)
    return document_files, operations


def _schematic_create_operation(
    index: int,
    sheet: JsonObject,
    overwrite: bool,
) -> tuple[str, JsonObject]:
    sheet_file = _string(sheet.get("file"), "schematics[].file")
    return sheet_file, mco_operation(
        "schdoc.create",
        f"create_schematic_{index + 1}",
        f"Create schematic {Path(sheet_file).name}",
        _schematic_create_args(sheet, sheet_file, overwrite),
    )


def _schematic_create_args(
    sheet: JsonObject,
    sheet_file: str,
    overwrite: bool,
) -> JsonObject:
    args: JsonObject = {
        "file": sheet_file,
        "sheet_style": str(sheet.get("sheet_style") or "D"),
        "overwrite": overwrite,
    }
    if sheet.get("template") is not None:
        args["template"] = _string(sheet.get("template"), "schematics[].template")
        args["apply_template_visual_sheet_settings"] = bool(
            sheet.get("apply_template_visual_sheet_settings", False)
        )
    if sheet.get("custom_sheet_mils") is not None:
        args["custom_sheet_mils"] = _object(
            sheet.get("custom_sheet_mils"),
            "schematics[].custom_sheet_mils",
        )
    return args


def _pcb_create_operation(
    raw_pcb: object,
    overwrite: bool,
) -> tuple[str | None, JsonObject | None]:
    if raw_pcb is None:
        return None, None
    pcb_obj = _object(raw_pcb, "pcb")
    pcb_file = _string(pcb_obj.get("file"), "pcb.file")
    return pcb_file, mco_operation(
        "pcbdoc.create",
        "create_board",
        f"Create board {Path(pcb_file).name}",
        _pcb_create_args(pcb_obj, pcb_file, overwrite),
    )


def _pcb_create_args(
    pcb_obj: JsonObject,
    pcb_file: str,
    overwrite: bool,
) -> JsonObject:
    pcb_args: JsonObject = {
        "file": pcb_file,
        "overwrite": overwrite,
    }
    if pcb_obj.get("board_outline_mils") is not None:
        pcb_args["board_outline_mils"] = _object(
            pcb_obj.get("board_outline_mils"),
            "pcb.board_outline_mils",
        )
    _apply_pcb_layer_stack_args(pcb_args, pcb_obj)
    _apply_pcb_mechanical_profile_args(pcb_args, pcb_obj)
    return pcb_args


def _apply_pcb_layer_stack_args(pcb_args: JsonObject, pcb_obj: JsonObject) -> None:
    layer_stack = pcb_obj.get("layer_stack")
    if layer_stack is None:
        pcb_args["layer_stack_template"] = str(
            pcb_obj.get("layer_stack_template") or "2-layer"
        )
        return
    layer_stack_obj = _object(layer_stack, "pcb.layer_stack")
    mode = str(layer_stack_obj.get("mode") or "generated_rigid")
    if mode != "generated_rigid":
        raise ValueError(
            "Only pcb.layer_stack.mode='generated_rigid' is supported in this release"
        )
    pcb_args["rigid_stack"] = layer_stack_obj


def _apply_pcb_mechanical_profile_args(
    pcb_args: JsonObject,
    pcb_obj: JsonObject,
) -> None:
    profile = str(pcb_obj.get("mechanical_layer_profile") or "none")
    normalized = profile.strip().lower().replace("-", "_")
    if normalized in {"", "none"}:
        return
    if normalized != STANDARD_MECHANICAL_LAYER_PROFILE:
        raise ValueError(f"Unsupported mechanical layer profile: {profile!r}")
    pcb_args.update(standard_mechanical_profile_args())


def _project_document_operations(
    project_file: str,
    document_files: list[str],
) -> list[JsonObject]:
    return [
        mco_operation(
            "project.add_document",
            f"add_document_{index}",
            f"Add {Path(document_file).name} to project",
            {
                "file": project_file,
                "document": _project_relative_document(project_file, document_file),
            },
        )
        for index, document_file in enumerate(document_files, start=1)
    ]


def execute_project_create_mco(
    config: JsonObject,
    *,
    config_dir: Path,
    overwrite: bool = False,
    dry_run: bool = False,
) -> McoExecutionResult:
    """Execute a project skeleton config through generated MCO operations."""
    return execute_mco(
        build_project_create_mco(config, overwrite=overwrite),
        McoExecutionContext(work_dir=config_dir, dry_run=dry_run),
    )


def cmd_project(args: argparse.Namespace) -> int:
    """Dispatch project subcommands."""
    action = getattr(args, "project_action", None)
    if action == "init":
        return _cmd_project_init(args)
    if action == "create":
        return _cmd_project_create(args)
    if action == "add-sheet":
        return _cmd_project_add_sheet(args)
    log.error("No project subcommand specified")
    return 1


def _cmd_project_init(args: argparse.Namespace) -> int:
    try:
        config = default_project_config(
            project_name=args.project_name,
            layer_count=args.layers,
        )
        output_path = write_project_config(args.config, config, overwrite=bool(args.force))
    except Exception as exc:
        log.error("Failed writing project config: %s", exc)
        return 1
    log.info("Wrote %s", output_path)
    return 0


def _cmd_project_create(args: argparse.Namespace) -> int:
    try:
        config_path = Path(args.config)
        if not config_path.exists():
            if not bool(args.defaults):
                raise FileNotFoundError(
                    f"Config not found: {config_path}. Use --defaults to create one."
                )
            write_project_config(
                config_path,
                default_project_config(
                    project_name=args.project_name,
                    layer_count=args.layers,
                ),
                overwrite=bool(args.force),
            )
        config = load_project_config(config_path)
        written_config = Path(args.write_config) if args.write_config else _config_copy_path(config_path, config)
        if written_config.resolve() == config_path.resolve():
            written_config = config_path.resolve()
        else:
            write_project_config(written_config, config, overwrite=bool(args.force))
        payload = build_project_create_mco(config, overwrite=bool(args.force))
        if args.emit_mco is not None:
            _write_json(args.emit_mco, payload, overwrite=bool(args.force))
        result = execute_mco_for_cli(
            payload,
            McoExecutionContext(work_dir=config_path.resolve().parent, dry_run=bool(args.dry_run)),
            json_stdout=bool(args.json),
        )
    except Exception as exc:
        log.error("Failed creating project: %s", exc)
        return 1

    if args.json_output is not None:
        _write_json(args.json_output, result.to_dict(), overwrite=True)
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print_mco_execution_result(
            result,
            title="project",
            color=not bool(args.no_color),
        )
        log.info("Config: %s", written_config)
    return 0 if result.ok else 1


def _cmd_project_add_sheet(args: argparse.Namespace) -> int:
    try:
        project_file = Path(args.project)
        sheet_file = Path(args.sheet)
        payload = {
            "schema": MCO_SCHEMA,
            "operations": [
                mco_operation(
                    "schdoc.create",
                    "create_schematic",
                    "Create schematic",
                    {
                        "file": str(sheet_file),
                        "sheet_style": args.sheet_style,
                        "overwrite": bool(args.force),
                    },
                ),
                mco_operation(
                    "project.add_document",
                    "add_schematic_to_project",
                    "Add schematic to project",
                    {
                        "file": str(project_file),
                        "document": _project_relative_document(
                            str(project_file),
                            str(sheet_file),
                        ),
                    },
                ),
            ],
        }
        if args.emit_mco is not None:
            _write_json(args.emit_mco, payload, overwrite=bool(args.force))
        result = execute_mco_for_cli(
            payload,
            McoExecutionContext(work_dir=Path.cwd(), dry_run=bool(args.dry_run)),
            json_stdout=bool(args.json),
        )
    except Exception as exc:
        log.error("Failed adding sheet: %s", exc)
        return 1

    if args.json_output is not None:
        _write_json(args.json_output, result.to_dict(), overwrite=True)
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print_mco_execution_result(
            result,
            title="project",
            color=not bool(args.no_color),
        )
    return 0 if result.ok else 1


def _config_copy_path(config_path: Path, config: JsonObject) -> Path:
    project = _object(config.get("project"), "project")
    project_file = Path(_string(project.get("file"), "project.file"))
    if not project_file.is_absolute():
        project_file = config_path.resolve().parent / project_file
    return project_file.with_suffix(".project.jsonc")


def _project_relative_document(project_file: str, document_file: str) -> str:
    project_path = Path(project_file)
    document_path = Path(document_file)
    if project_path.is_absolute() and document_path.is_absolute():
        return os.path.relpath(document_path, project_path.parent)
    if project_path.parent != Path(".") and document_path.parent != Path("."):
        return os.path.relpath(document_path, project_path.parent)
    return str(document_path)


def _parameters(project: JsonObject) -> dict[str, str]:
    raw = project.get("parameters", {})
    if not isinstance(raw, dict):
        raise ValueError("project.parameters must be an object")
    return {str(name): str(value) for name, value in raw.items()}


def _object(value: object, label: str) -> JsonObject:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return dict(value)


def _object_list(value: object, label: str) -> list[JsonObject]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a list")
    return [_object(item, label) for item in value]


def _string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a non-empty string")
    return value


def _write_json(path: Path, payload: JsonObject, *, overwrite: bool) -> Path:
    if path.exists() and not overwrite:
        raise FileExistsError(f"Output already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path.resolve()


def register_parser(
    subparsers: argparse._SubParsersAction,
) -> argparse.ArgumentParser:
    """Register the project command parser."""
    parser = subparsers.add_parser(
        "project",
        help="create Altium project skeletons",
        description="Create .PrjPcb project skeletons through JSONC config and MCO operations.",
    )
    action_subparsers = parser.add_subparsers(
        dest="project_action",
        metavar="<project-action>",
    )

    init_parser = action_subparsers.add_parser(
        "init",
        help="write a project skeleton JSONC config",
    )
    init_parser.add_argument("config", type=Path, help="output project config path")
    init_parser.add_argument(
        "--project-name",
        default="generated_project",
        help="default project name",
    )
    init_parser.add_argument(
        "--layers",
        type=int,
        default=2,
        help="default rigid copper layer count",
    )
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite an existing config",
    )
    init_parser.set_defaults(handler=cmd_project)

    create_parser = action_subparsers.add_parser(
        "create",
        help="create a project skeleton from JSONC config",
    )
    create_parser.add_argument("config", type=Path, help="project config path")
    create_parser.add_argument(
        "--defaults",
        action="store_true",
        help="write and use a default config if the config path does not exist",
    )
    create_parser.add_argument(
        "--project-name",
        default="generated_project",
        help="default project name used with --defaults",
    )
    create_parser.add_argument(
        "--layers",
        type=int,
        default=2,
        help="default rigid copper layer count used with --defaults",
    )
    create_parser.add_argument(
        "--write-config",
        type=Path,
        help="write the normalized config used to this path",
    )
    create_parser.add_argument(
        "--emit-mco",
        type=Path,
        help="write the generated MCO JSON file before execution",
    )
    create_parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite generated project outputs and emitted files",
    )
    create_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate and report planned outputs without writing CAD files",
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
    create_parser.set_defaults(handler=cmd_project)

    add_sheet_parser = action_subparsers.add_parser(
        "add-sheet",
        help="create a new sheet and add it to an existing PrjPcb",
    )
    add_sheet_parser.add_argument("project", type=Path, help="target .PrjPcb path")
    add_sheet_parser.add_argument("sheet", type=Path, help="new .SchDoc path")
    add_sheet_parser.add_argument(
        "--sheet-style",
        default="D",
        help="Altium SheetStyle enum name or integer (default: D)",
    )
    add_sheet_parser.add_argument(
        "--emit-mco",
        type=Path,
        help="write the generated MCO JSON file before execution",
    )
    add_sheet_parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite the SchDoc if it already exists",
    )
    add_sheet_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate and report planned outputs without writing files",
    )
    add_sheet_parser.add_argument(
        "--json",
        action="store_true",
        help="write the MCO execution report JSON to stdout",
    )
    add_sheet_parser.add_argument(
        "--json-output",
        type=Path,
        help="write the MCO execution report JSON to this file",
    )
    add_sheet_parser.add_argument(
        "--no-color",
        action="store_true",
        help="disable terminal color in human output",
    )
    add_sheet_parser.set_defaults(handler=cmd_project)
    return parser
