"""debug-plate command for altium_cruncher."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from altium_cruncher.altium_cruncher_debug_plate import (
    execute_debug_plate_config,
    inspect_debug_plate_source,
    load_debug_plate_config,
    write_debug_plate_config_template,
    write_debug_plate_mate_seed_config,
    write_debug_plate_mco,
    write_debug_plate_seed_config,
)
from altium_cruncher.altium_cruncher_debug_plate_parts import (
    build_debug_plate_known_parts_cache,
)

log = logging.getLogger(__name__)


def cmd_debug_plate(args: argparse.Namespace) -> int:
    """Dispatch debug-plate subcommands."""
    action = getattr(args, "debug_plate_action", None)
    if action == "init":
        return _cmd_debug_plate_init(args)
    if action == "plan":
        return _cmd_debug_plate_plan(args)
    if action == "inspect":
        return _cmd_debug_plate_inspect(args)
    if action == "seed":
        return _cmd_debug_plate_seed(args)
    if action == "parts-cache":
        return _cmd_debug_plate_parts_cache(args)
    if action == "run":
        return _cmd_debug_plate_run(args)
    log.error("No debug-plate subcommand specified")
    return 1


def _cmd_debug_plate_init(args: argparse.Namespace) -> int:
    try:
        output_path = write_debug_plate_config_template(
            args.config,
            overwrite=bool(args.force),
        )
    except Exception as exc:
        log.error("Failed writing debug-plate config template: %s", exc)
        return 1
    print(str(output_path))
    return 0


def _cmd_debug_plate_plan(args: argparse.Namespace) -> int:
    try:
        config = load_debug_plate_config(args.config)
        output_path = write_debug_plate_mco(
            config,
            _mco_output_path(args),
            overwrite=bool(args.force),
        )
    except Exception as exc:
        log.error("Failed writing debug-plate MCO: %s", exc)
        return 1
    print(str(output_path))
    return 0


def _cmd_debug_plate_inspect(args: argparse.Namespace) -> int:
    try:
        payload = inspect_debug_plate_source(
            args.file,
            pcbdoc_selector=args.pcbdoc,
            project_context=args.project_context,
        )
    except Exception as exc:
        log.error("Failed inspecting debug-plate source: %s", exc)
        return 1
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def _cmd_debug_plate_seed(args: argparse.Namespace) -> int:
    try:
        if bool(args.mate_config):
            output_path = write_debug_plate_mate_seed_config(
                args.file,
                args.config,
                overwrite=bool(args.force),
                known_parts_manifest=args.known_parts_manifest,
                pcbdoc_selector=args.pcbdoc,
                project_context=args.project_context,
            )
        else:
            output_path = write_debug_plate_seed_config(
                args.file,
                args.config,
                overwrite=bool(args.force),
                pcbdoc_selector=args.pcbdoc,
                project_context=args.project_context,
            )
    except Exception as exc:
        log.error("Failed seeding debug-plate config: %s", exc)
        return 1
    print(str(output_path))
    return 0


def _cmd_debug_plate_parts_cache(args: argparse.Namespace) -> int:
    subaction = getattr(args, "parts_cache_action", None)
    if subaction != "build":
        log.error("No debug-plate parts-cache subcommand specified")
        return 1
    try:
        output_path = build_debug_plate_known_parts_cache(
            args.file,
            args.cache_dir,
            overwrite=bool(args.force),
            verbose=bool(args.debug),
        )
    except Exception as exc:
        log.error("Failed building debug-plate known-parts cache: %s", exc)
        return 1
    print(str(output_path))
    return 0


def _cmd_debug_plate_run(args: argparse.Namespace) -> int:
    try:
        config = load_debug_plate_config(args.config)
        if args.emit_mco is not None:
            write_debug_plate_mco(config, args.emit_mco, overwrite=bool(args.force))
        result = execute_debug_plate_config(args.config, dry_run=bool(args.dry_run))
    except Exception as exc:
        log.error("Failed running debug-plate workflow: %s", exc)
        return 1
    print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    return 0 if result.ok else 1


def _mco_output_path(args: argparse.Namespace) -> Path:
    if args.output_mco is not None:
        return args.output_mco
    return Path(args.config).with_suffix(".mco.jsonc")


def register_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(
        "debug-plate",
        help="generate a mating/debug fixture project from configuration",
        description=(
            "Inspect DUT PCB inputs, seed editable JSONC config, build known "
            "fixture-part caches, and generate or run MCO automation for a new "
            "debug-plate project."
        ),
    )
    action_subparsers = parser.add_subparsers(
        dest="debug_plate_action",
        help="debug-plate subcommands",
    )

    init_parser = action_subparsers.add_parser(
        "init",
        help="write an editable debug-plate JSONC config template",
    )
    init_parser.add_argument("config", type=Path, help="config output path")
    init_parser.add_argument("--force", action="store_true", help="overwrite config")
    init_parser.set_defaults(handler=cmd_debug_plate)

    plan_parser = action_subparsers.add_parser(
        "plan",
        help="generate an MCO file from a debug-plate config",
    )
    plan_parser.add_argument("config", type=Path, help="debug-plate JSONC config")
    plan_parser.add_argument(
        "--output-mco",
        type=Path,
        help="MCO output path (default: config path with .mco.jsonc suffix)",
    )
    plan_parser.add_argument("--force", action="store_true", help="overwrite MCO")
    plan_parser.set_defaults(handler=cmd_debug_plate)

    inspect_parser = action_subparsers.add_parser(
        "inspect",
        help="inspect a DUT PCB input for debug-plate candidates",
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
    inspect_parser.set_defaults(handler=cmd_debug_plate)

    seed_parser = action_subparsers.add_parser(
        "seed",
        help="seed an editable debug-plate config from a DUT PCB input",
    )
    seed_parser.add_argument("file", type=Path, help="DUT .PrjPcb or .PcbDoc input")
    seed_parser.add_argument(
        "--config",
        type=Path,
        default=Path("debug-plate.jsonc"),
        help="config output path (default: debug-plate.jsonc)",
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
    seed_parser.set_defaults(handler=cmd_debug_plate)

    parts_cache_parser = action_subparsers.add_parser(
        "parts-cache",
        help="build or inspect a debug-plate known-parts cache",
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
        default=Path("debug-plate-known-parts/node-test-array"),
        help=(
            "cache output directory "
            "(default: debug-plate-known-parts/node-test-array)"
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
    parts_cache_build_parser.set_defaults(handler=cmd_debug_plate)
    parts_cache_parser.set_defaults(handler=cmd_debug_plate)

    run_parser = action_subparsers.add_parser(
        "run",
        help="run a debug-plate config through the MCO executor",
    )
    run_parser.add_argument("config", type=Path, help="debug-plate JSONC config")
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
    run_parser.set_defaults(handler=cmd_debug_plate)

    parser.set_defaults(handler=cmd_debug_plate)
    return parser
