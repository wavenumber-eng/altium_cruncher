"""mate command for altium_cruncher."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from altium_cruncher.altium_cruncher_cmd_launch import cmd_launch
from altium_cruncher.altium_cruncher_cmd_libraries import print_library_scan_result
from altium_cruncher.altium_cruncher_mate import (
    execute_mate_config,
    inspect_mate_source,
    load_mate_config,
    write_mate_config_template,
    write_mate_seed_config,
    write_mate_mco,
    write_legacy_mate_seed_config,
)
from altium_cruncher.altium_cruncher_mate_parts import (
    build_mate_known_parts_cache,
)
from altium_cruncher.altium_cruncher_mate_libraries import scan_mate_libraries

log = logging.getLogger(__name__)

DEFAULT_MATE_CONFIG = Path("mate.a0.jsonc")


def cmd_mate(args: argparse.Namespace) -> int:
    """Dispatch mate subcommands."""
    action = getattr(args, "mate_action", None)
    if action is None:
        return _cmd_mate_default(args)
    if action == "init":
        return _cmd_mate_init(args)
    if action == "plan":
        return _cmd_mate_plan(args)
    if action == "libs":
        return _cmd_mate_libraries(args)
    if action == "inspect":
        return _cmd_mate_inspect(args)
    if action == "seed":
        return _cmd_mate_seed(args)
    if action == "parts-cache":
        return _cmd_mate_parts_cache(args)
    if action == "run":
        return _cmd_mate_run(args)
    log.error("No mate subcommand specified")
    return 1


def _cmd_mate_default(args: argparse.Namespace) -> int:
    config_path = _selected_config_path(args)
    if not config_path.exists():
        return _write_default_config(args, config_path)
    run_args = argparse.Namespace(
        config=config_path,
        emit_mco=_mco_output_path_for_config(config_path),
        force=True,
        dry_run=getattr(args, "dry_run", False),
        launch=getattr(args, "launch", False),
        ad_version=getattr(args, "ad_version", None),
        altium_path=getattr(args, "altium_path", None),
    )
    return _cmd_mate_run(run_args)


def _cmd_mate_init(args: argparse.Namespace) -> int:
    return _write_default_config(args, args.config)


def _write_default_config(args: argparse.Namespace, config_path: Path) -> int:
    try:
        output_path = write_mate_config_template(
            config_path,
            overwrite=bool(getattr(args, "force", False)),
            source_board=_default_source_board_for_config(config_path),
        )
    except Exception as exc:
        log.error("Failed writing mate config template: %s", exc)
        return 1
    print(str(output_path))
    print("Created mate config. Read the JSONC comments, edit as needed, then run `altium-cruncher mate`.")
    return 0


def _cmd_mate_plan(args: argparse.Namespace) -> int:
    config_path = _selected_config_path(args)
    if not config_path.exists():
        return _write_default_config(args, config_path)
    try:
        config = load_mate_config(config_path)
        output_path = write_mate_mco(
            config,
            _mco_output_path(args),
            overwrite=bool(args.force),
        )
    except Exception as exc:
        log.error("Failed writing mate MCO: %s", exc)
        return 1
    print(str(output_path))
    return 0


def _cmd_mate_inspect(args: argparse.Namespace) -> int:
    try:
        payload = inspect_mate_source(
            args.file,
            pcbdoc_selector=args.pcbdoc,
            project_context=args.project_context,
        )
    except Exception as exc:
        log.error("Failed inspecting mate source: %s", exc)
        return 1
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def _cmd_mate_seed(args: argparse.Namespace) -> int:
    try:
        if bool(args.mate_config):
            output_path = write_mate_seed_config(
                args.file,
                args.config,
                overwrite=bool(args.force),
                known_parts_manifest=args.known_parts_manifest,
                pcbdoc_selector=args.pcbdoc,
                project_context=args.project_context,
            )
        else:
            output_path = write_legacy_mate_seed_config(
                args.file,
                args.config,
                overwrite=bool(args.force),
                pcbdoc_selector=args.pcbdoc,
                project_context=args.project_context,
            )
    except Exception as exc:
        log.error("Failed seeding mate config: %s", exc)
        return 1
    print(str(output_path))
    return 0


def _cmd_mate_parts_cache(args: argparse.Namespace) -> int:
    subaction = getattr(args, "parts_cache_action", None)
    if subaction != "build":
        log.error("No mate parts-cache subcommand specified")
        return 1
    try:
        output_path = build_mate_known_parts_cache(
            args.file,
            args.cache_dir,
            overwrite=bool(args.force),
            verbose=bool(args.debug),
        )
    except Exception as exc:
        log.error("Failed building mate known-parts cache: %s", exc)
        return 1
    print(str(output_path))
    return 0


def _cmd_mate_libraries(args: argparse.Namespace) -> int:
    roots = args.roots or [Path.cwd()]
    try:
        result = scan_mate_libraries(
            roots,
            recursive=not bool(args.no_recursive),
        )
    except Exception as exc:
        log.error("Failed scanning mate libraries: %s", exc)
        return 1
    if args.json:
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
        return 0
    print_library_scan_result(
        result,
        base_dir=Path.cwd(),
        absolute=bool(args.absolute),
        color=not bool(args.no_color),
    )
    return 0


def _cmd_mate_run(args: argparse.Namespace) -> int:
    try:
        config = load_mate_config(args.config)
        if args.emit_mco is not None:
            write_mate_mco(config, args.emit_mco, overwrite=bool(args.force))
        result = execute_mate_config(args.config, dry_run=bool(args.dry_run))
    except Exception as exc:
        log.error("Failed running mate workflow: %s", exc)
        return 1
    print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    if not result.ok:
        return 1
    if getattr(args, "launch", False) and not bool(args.dry_run):
        return _launch_mate_output(args, config)
    return 0


def _mco_output_path(args: argparse.Namespace) -> Path:
    if args.output_mco is not None:
        return args.output_mco
    return _mco_output_path_for_config(_selected_config_path(args))


def _mco_output_path_for_config(config_path: Path) -> Path:
    return Path(config_path).with_suffix(".mco.jsonc")


def _selected_config_path(args: argparse.Namespace) -> Path:
    config_path = getattr(args, "config", None)
    if config_path is not None:
        return Path(config_path)
    if DEFAULT_MATE_CONFIG.exists():
        return DEFAULT_MATE_CONFIG
    legacy_path = Path("mate.jsonc")
    if legacy_path.exists():
        return legacy_path
    return DEFAULT_MATE_CONFIG


def _default_source_board_for_config(config_path: Path) -> Path | None:
    config_dir = config_path.parent if config_path.parent != Path("") else Path.cwd()
    if not config_dir.exists():
        return None
    projects = sorted(
        (
            item
            for item in config_dir.iterdir()
            if item.is_file() and item.suffix.lower() == ".prjpcb"
        ),
        key=lambda item: item.name.lower(),
    )
    if len(projects) != 1:
        return None
    return _path_relative_to(projects[0], config_dir)


def _path_relative_to(path: Path, base_dir: Path) -> Path:
    try:
        return path.resolve().relative_to(base_dir.resolve())
    except ValueError:
        return path.resolve()


def _launch_mate_output(args: argparse.Namespace, config: object) -> int:
    output = getattr(config, "output")
    project_filename = output.project_filename or f"{output.project_name}.PrjPcb"
    project_path = Path(output.output_dir) / project_filename
    launch_args = argparse.Namespace(
        file=str(project_path),
        ad_version=getattr(args, "ad_version", None),
        altium_path=getattr(args, "altium_path", None),
        dry_run=False,
        json=False,
    )
    return cmd_launch(launch_args)


def register_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(
        "mate",
        help="generate a mating-board project from configuration",
        description=(
            "Create or run an editable mate JSONC config. With no config in "
            "the current directory, writes mate.a0.jsonc. With a config, "
            "generates the derived MCO and runs it."
        ),
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="mate JSONC config path (default: mate.a0.jsonc, then mate.jsonc)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="generate and report operations without writing supported outputs",
    )
    parser.add_argument(
        "--launch",
        action="store_true",
        help="launch the generated mate project in Altium after a successful run",
    )
    parser.add_argument(
        "--ad-version",
        "--series",
        dest="ad_version",
        help="Altium major series to launch with --launch, for example AD26",
    )
    parser.add_argument(
        "--altium-path",
        type=Path,
        help="explicit X2.exe or install root for --launch",
    )
    action_subparsers = parser.add_subparsers(
        dest="mate_action",
        help="mate commands",
    )

    init_parser = action_subparsers.add_parser(
        "init",
        help=argparse.SUPPRESS,
    )
    init_parser.add_argument("config", type=Path, help="config output path")
    init_parser.add_argument("--force", action="store_true", help="overwrite config")
    init_parser.set_defaults(handler=cmd_mate)

    plan_parser = action_subparsers.add_parser(
        "plan",
        help="generate an MCO file from a mate config",
    )
    plan_parser.add_argument(
        "config",
        nargs="?",
        type=Path,
        help="mate JSONC config (default: mate.a0.jsonc, then mate.jsonc)",
    )
    plan_parser.add_argument(
        "--output-mco",
        type=Path,
        help="MCO output path (default: config path with .mco.jsonc suffix)",
    )
    plan_parser.add_argument("--force", action="store_true", help="overwrite MCO")
    plan_parser.set_defaults(handler=cmd_mate)

    libs_parser = action_subparsers.add_parser(
        "libs",
        help="list discoverable mate symbols and footprints",
    )
    libs_parser.add_argument(
        "roots",
        nargs="*",
        type=Path,
        help="library roots to scan (default: current directory)",
    )
    libs_parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="scan only the direct files in each root",
    )
    libs_parser.add_argument(
        "--absolute",
        action="store_true",
        help="show absolute paths in human output instead of paths relative to cwd",
    )
    libs_parser.add_argument(
        "--no-color",
        action="store_true",
        help="disable terminal color in human output",
    )
    libs_parser.add_argument(
        "--json",
        action="store_true",
        help="write machine-readable JSON",
    )
    libs_parser.set_defaults(handler=cmd_mate)

    inspect_parser = action_subparsers.add_parser(
        "inspect",
        help=argparse.SUPPRESS,
    )
    inspect_parser.add_argument("file", type=Path, help="DUT .PrjPcb or .PcbDoc input")
    inspect_parser.add_argument(
        "--doc",
        "--pcbdoc",
        dest="pcbdoc",
        type=str,
        help="with .PrjPcb input, select a specific PcbDoc",
    )
    inspect_parser.add_argument(
        "--project-context",
        choices=["auto", "none", "schematic"],
        default="auto",
        help="project-context mode for standalone PcbDoc inputs (default: auto)",
    )
    inspect_parser.set_defaults(handler=cmd_mate)

    seed_parser = action_subparsers.add_parser(
        "seed",
        help=argparse.SUPPRESS,
    )
    seed_parser.add_argument("file", type=Path, help="DUT .PrjPcb or .PcbDoc input")
    seed_parser.add_argument(
        "--config",
        type=Path,
        default=Path("mate.jsonc"),
        help="config output path (default: mate.jsonc)",
    )
    seed_parser.add_argument(
        "--doc",
        "--pcbdoc",
        dest="pcbdoc",
        type=str,
        help="with .PrjPcb input, select a specific PcbDoc",
    )
    seed_parser.add_argument(
        "--project-context",
        choices=["auto", "none", "schematic"],
        default="auto",
        help="project-context mode for standalone PcbDoc inputs (default: auto)",
    )
    seed_parser.add_argument(
        "--mate-config",
        action="store_true",
        help="write the draft selector/projection mate-config schema",
    )
    seed_parser.add_argument(
        "--known-parts-manifest",
        type=Path,
        help="with --mate-config, set known_parts.manifest in the seeded config",
    )
    seed_parser.add_argument("--force", action="store_true", help="overwrite config")
    seed_parser.set_defaults(handler=cmd_mate)

    parts_cache_parser = action_subparsers.add_parser(
        "parts-cache",
        help=argparse.SUPPRESS,
    )
    parts_cache_subparsers = parts_cache_parser.add_subparsers(
        dest="parts_cache_action",
        help="parts-cache subcommands",
    )
    parts_cache_build_parser = parts_cache_subparsers.add_parser(
        "build",
        help="extract node-test-array symbols/footprints into a known-parts cache",
    )
    parts_cache_build_parser.add_argument(
        "file",
        type=Path,
        help="node-test-array .PrjPcb source",
    )
    parts_cache_build_parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path("mate-known-parts/node-test-array"),
        help=(
            "cache output directory "
            "(default: mate-known-parts/node-test-array)"
        ),
    )
    parts_cache_build_parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite an existing cache manifest",
    )
    parts_cache_build_parser.add_argument(
        "--debug",
        action="store_true",
        help="enable verbose extraction logging",
    )
    parts_cache_build_parser.set_defaults(handler=cmd_mate)
    parts_cache_parser.set_defaults(handler=cmd_mate)

    run_parser = action_subparsers.add_parser(
        "run",
        help=argparse.SUPPRESS,
    )
    run_parser.add_argument("config", type=Path, help="mate JSONC config")
    run_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="report generated operations without writing supported outputs",
    )
    run_parser.add_argument(
        "--emit-mco",
        type=Path,
        help="also write the generated MCO file before running",
    )
    run_parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite --emit-mco output when present",
    )
    run_parser.set_defaults(handler=cmd_mate)

    action_subparsers.metavar = "{plan,libs}"
    action_subparsers._choices_actions = [
        action
        for action in action_subparsers._choices_actions
        if action.help != argparse.SUPPRESS
    ]
    parser.set_defaults(handler=cmd_mate)
    return parser
