"""PrjPcb skeleton commands backed by MCO operations."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from altium_cruncher.mco_cli_support import (
    execute_mco_for_cli,
    print_mco_execution_result,
)
from altium_cruncher.altium_cruncher_mco import MCO_SCHEMA, JsonObject, McoExecutionContext, mco_operation

from altium_cruncher.contracts.creation import creation_default, creation_schema


log = logging.getLogger(__name__)


from .project_creation import (
    PROJECT_AUTO_CONFIG_NAME as PROJECT_AUTO_CONFIG_NAME,
    PROJECT_CONFIG_SCHEMA as PROJECT_CONFIG_SCHEMA,
    PROJECT_CONFIG_SUFFIX as PROJECT_CONFIG_SUFFIX,
    default_project_config as default_project_config,
    render_project_config as render_project_config,
    write_project_config as write_project_config,
    load_project_config as load_project_config,
    build_project_create_mco as build_project_create_mco,
    _project_create_operation as _project_create_operation,
    _project_parameter_operations as _project_parameter_operations,
    _document_create_operations as _document_create_operations,
    _schematic_create_operation as _schematic_create_operation,
    _schematic_create_args as _schematic_create_args,
    _pcb_create_operation as _pcb_create_operation,
    _pcb_create_args as _pcb_create_args,
    _apply_pcb_layer_stack_args as _apply_pcb_layer_stack_args,
    _native_layer_stack_integers as _native_layer_stack_integers,
    _apply_pcb_mechanical_args as _apply_pcb_mechanical_args,
    _apply_explicit_project_mechanical_rows as _apply_explicit_project_mechanical_rows,
    _append_project_mechanical_layers as _append_project_mechanical_layers,
    _append_project_mechanical_pairs as _append_project_mechanical_pairs,
    _append_project_mechanical_pair as _append_project_mechanical_pair,
    _mechanical_pair_side as _mechanical_pair_side,
    _mechanical_layer_row as _mechanical_layer_row,
    _project_document_operations as _project_document_operations,
    execute_project_create_mco as execute_project_create_mco,
    _project_relative_document as _project_relative_document,
    _parameters as _parameters,
    _object as _object,
    _object_list as _object_list,
    _string as _string,
)


def cmd_prjpcb(args: argparse.Namespace) -> int:
    """Dispatch PrjPcb subcommands."""
    action = getattr(args, "prjpcb_action", None)
    if action == "init":
        return _cmd_prjpcb_init(args)
    if action == "create":
        return _cmd_prjpcb_create(args)
    if action == "add-sheet":
        return _cmd_prjpcb_add_sheet(args)
    help_parser = getattr(args, "_prjpcb_parser", None)
    if help_parser is not None:
        help_parser.print_help()
        return 0
    log.error("No prjpcb subcommand specified")
    return 1


def _cmd_prjpcb_auto_create(args: argparse.Namespace) -> int:
    try:
        cwd = Path.cwd()
        config_path = _auto_config_path(cwd)
        if not config_path.exists():
            project_name = _default_project_name_from_cwd(cwd)
            output_path = write_project_config(
                config_path,
                default_project_config(project_name=project_name),
                overwrite=False,
            )
            log.info("")
            log.info("Writing project init config template: %s", output_path)
            log.info(
                "Please edit it, then rerun `acr prjpcb create` to create "
                "the project skeleton."
            )
            return 0

        config = load_project_config(config_path)
        log.info("")
        log.info("Using project init config: %s", config_path.resolve())
        result = execute_project_create_mco(
            config,
            config_dir=config_path.resolve().parent,
            overwrite=bool(args.force),
            dry_run=bool(args.dry_run),
        )
    except Exception as exc:
        log.error("Failed running default PrjPcb workflow: %s", exc)
        return 1

    if args.json_output is not None:
        _write_json(args.json_output, result.to_dict(), overwrite=True)
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
        return 0 if result.ok else 1
    print_mco_execution_result(
        result,
        title="prjpcb",
        color=not bool(args.no_color),
    )
    log.info("Config: %s", config_path.resolve())
    return 0 if result.ok else 1


def _cmd_prjpcb_init(args: argparse.Namespace) -> int:
    try:
        config_path, project_name = _resolve_config_path_and_project_name(
            args.config,
            project_name=args.project_name,
        )
        config = default_project_config(
            project_name=project_name,
            layer_count=args.layers,
        )
        output_path = write_project_config(
            config_path, config, overwrite=bool(args.force)
        )
    except Exception as exc:
        log.error("Failed writing project config: %s", exc)
        return 1
    log.info("Wrote %s", output_path)
    return 0


def _cmd_prjpcb_create(args: argparse.Namespace) -> int:
    try:
        if args.config is None:
            return _cmd_prjpcb_auto_create(args)
        config_path, written_config, payload = _prepare_project_create_payload(args)
        if args.emit_mco is not None:
            _write_json(args.emit_mco, payload, overwrite=bool(args.force))
        result = execute_mco_for_cli(
            payload,
            McoExecutionContext(
                work_dir=config_path.resolve().parent, dry_run=bool(args.dry_run)
            ),
            json_stdout=bool(args.json),
        )
    except Exception as exc:
        log.error("Failed creating PrjPcb project: %s", exc)
        return 1

    if args.json_output is not None:
        _write_json(args.json_output, result.to_dict(), overwrite=True)
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print_mco_execution_result(
            result,
            title="prjpcb",
            color=not bool(args.no_color),
        )
        log.info("Config: %s", written_config)
    return 0 if result.ok else 1


def _prepare_project_create_payload(
    args: argparse.Namespace,
) -> tuple[Path, Path, JsonObject]:
    config_path, project_name = _resolve_config_path_and_project_name(
        args.config,
        project_name=args.project_name,
    )
    if not config_path.exists():
        _write_default_project_config_for_create(args, config_path, project_name)
    config = load_project_config(config_path)
    written_config = _resolved_written_config_path(
        args, config_path, config, project_name
    )
    if written_config.resolve() == config_path.resolve():
        written_config = config_path.resolve()
    else:
        write_project_config(written_config, config, overwrite=bool(args.force))
    return (
        config_path,
        written_config,
        build_project_create_mco(
            config,
            overwrite=bool(args.force),
        ),
    )


def _write_default_project_config_for_create(
    args: argparse.Namespace,
    config_path: Path,
    project_name: str,
) -> None:
    if not bool(args.defaults):
        raise FileNotFoundError(
            f"Config not found: {config_path}. Use --defaults to create one."
        )
    write_project_config(
        config_path,
        default_project_config(
            project_name=project_name,
            layer_count=args.layers,
        ),
        overwrite=bool(args.force),
    )


def _resolved_written_config_path(
    args: argparse.Namespace,
    config_path: Path,
    config: JsonObject,
    project_name: str,
) -> Path:
    if args.write_config:
        written_config, _unused_name = _resolve_config_path_and_project_name(
            args.write_config,
            project_name=project_name,
        )
        return written_config
    return _config_copy_path(config_path, config)


def _cmd_prjpcb_add_sheet(args: argparse.Namespace) -> int:
    try:
        project_file = Path(args.prjpcb)
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
        log.error("Failed adding sheet to PrjPcb: %s", exc)
        return 1

    if args.json_output is not None:
        _write_json(args.json_output, result.to_dict(), overwrite=True)
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print_mco_execution_result(
            result,
            title="prjpcb",
            color=not bool(args.no_color),
        )
    return 0 if result.ok else 1


def _resolve_config_path_and_project_name(
    config_arg: Path | str,
    *,
    project_name: str | None,
) -> tuple[Path, str]:
    config_path = Path(config_arg)
    resolved_project_name = project_name or _infer_project_name_from_config_arg(
        config_path
    )
    if config_path.suffix:
        return config_path, resolved_project_name
    return (
        config_path.with_name(f"{config_path.name}{PROJECT_CONFIG_SUFFIX}"),
        resolved_project_name,
    )


def _infer_project_name_from_config_arg(config_path: Path) -> str:
    name = config_path.stem if config_path.suffix else config_path.name
    suffix_stem = PROJECT_CONFIG_SUFFIX.removesuffix(".jsonc")
    if name.endswith(suffix_stem):
        name = name[: -len(suffix_stem)]
    if not name or name in {".", ".."}:
        raise ValueError(
            "Could not infer a project name; pass a config filename or --project-name"
        )
    return name


def _auto_config_path(cwd: Path) -> Path:
    preferred = cwd / PROJECT_AUTO_CONFIG_NAME
    if preferred.exists():
        return preferred

    existing_configs = sorted(cwd.glob(f"*{PROJECT_CONFIG_SUFFIX}"))
    if len(existing_configs) == 1:
        return existing_configs[0]
    if len(existing_configs) > 1:
        names = ", ".join(path.name for path in existing_configs)
        raise ValueError(
            f"Multiple project config files found; pass `prjpcb create CONFIG`: {names}"
        )
    return preferred


def _default_project_name_from_cwd(cwd: Path) -> str:
    return cwd.name or "generated_project"


def _config_copy_path(config_path: Path, config: JsonObject) -> Path:
    project = _object(config.get("project"), "project")
    project_file = Path(_string(project.get("file"), "project.file"))
    if not project_file.is_absolute():
        project_file = config_path.resolve().parent / project_file
    return project_file.with_suffix(".project.jsonc")


def _write_json(path: Path, payload: JsonObject, *, overwrite: bool) -> Path:
    if path.exists() and not overwrite:
        raise FileExistsError(f"Output already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path.resolve()


def register_parser(
    subparsers: argparse._SubParsersAction,
) -> argparse.ArgumentParser:
    """Register the prjpcb command parser."""
    parser = subparsers.add_parser(
        "prjpcb",
        help="create Altium PrjPcb skeletons",
        description=(
            "Create .PrjPcb project skeletons through JSONC config and MCO "
            "operations. The create subcommand writes a sample config when none "
            "exists, or runs the existing config when one is present."
        ),
    )
    action_subparsers = parser.add_subparsers(
        dest="prjpcb_action",
        metavar="<prjpcb-action>",
    )
    parser.set_defaults(handler=cmd_prjpcb, _prjpcb_parser=parser)

    create_parser = action_subparsers.add_parser(
        "create",
        help="create a project skeleton from JSONC config",
    )
    create_parser.add_argument(
        "config",
        type=Path,
        nargs="?",
        help="project config path or bare project name",
    )
    create_parser.add_argument(
        "--defaults",
        action="store_true",
        help="write and use a default config if the config path does not exist",
    )
    create_parser.add_argument(
        "--project-name",
        default=None,
        help=(
            "default project name used with --defaults "
            "(default: infer from config path or bare name)"
        ),
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
    create_parser.set_defaults(handler=cmd_prjpcb)

    init_parser = action_subparsers.add_parser(
        "init",
        help="write a project skeleton JSONC config",
    )
    init_parser.add_argument(
        "config",
        type=Path,
        help=(
            "output project config path or bare project name; bare names write "
            "NAME.project.jsonc"
        ),
    )
    init_parser.add_argument(
        "--project-name",
        default=None,
        help="default project name (default: infer from config path or bare name)",
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
    init_parser.set_defaults(handler=cmd_prjpcb)

    add_sheet_parser = action_subparsers.add_parser(
        "add-sheet",
        help="create a new sheet and add it to an existing PrjPcb",
    )
    add_sheet_parser.add_argument("prjpcb", type=Path, help="target .PrjPcb path")
    add_sheet_parser.add_argument("sheet", type=Path, help="new .SchDoc path")
    add_sheet_parser.add_argument(
        "--sheet-style",
        default=creation_default("sheet_style"),
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
    add_sheet_parser.set_defaults(handler=cmd_prjpcb)
    return parser
