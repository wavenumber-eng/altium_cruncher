"""Launch Altium Designer from altium-cruncher."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from altium_cruncher._version import cli_version_report
from altium_cruncher.altium_environment import (
    AltiumInstall,
    discover_altium_installs,
    launch_altium,
    select_altium_install,
)
from altium_cruncher.logging_utils import setup_cli_logging


def cmd_launch(args: argparse.Namespace) -> int:
    """Launch Altium Designer, optionally with one document."""
    install = _resolve_launch_install(args)
    if install is None:
        requested = args.altium_path or args.ad_version or "latest"
        print(f"Altium Designer install not found for: {requested}", file=sys.stderr)
        return 1

    try:
        file_path = _resolve_launch_file(args)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    try:
        command = launch_altium(
            install,
            file_path=file_path,
            dry_run=bool(getattr(args, "dry_run", False)),
        )
    except Exception as exc:
        print(f"Failed to launch Altium Designer: {exc}", file=sys.stderr)
        return 1

    _print_launch_result(args, install, file_path, command)
    return 0


def _resolve_launch_install(args: argparse.Namespace) -> AltiumInstall | None:
    altium_path = Path(args.altium_path).resolve() if args.altium_path else None
    return select_altium_install(
        discover_altium_installs(),
        version=getattr(args, "ad_version", None),
        altium_path=altium_path,
    )


def _resolve_launch_file(args: argparse.Namespace) -> Path | None:
    if not args.file:
        return None
    file_path = Path(args.file).resolve()
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return file_path


def _print_launch_result(
    args: argparse.Namespace,
    install: AltiumInstall,
    file_path: Path | None,
    command: list[str],
) -> None:
    if getattr(args, "json", False):
        print(
            json.dumps(
                {
                    "schema": "altium_cruncher.launch.a0",
                    "install": install.to_dict(),
                    "file": str(file_path) if file_path else None,
                    "command": command,
                    "dry_run": bool(getattr(args, "dry_run", False)),
                },
                indent=2,
            )
        )
        return
    action = "Would launch" if getattr(args, "dry_run", False) else "Launched"
    target = f" {file_path}" if file_path else ""
    print(f"{action} {install.label}:{target}")


def add_launch_arguments(parser: argparse.ArgumentParser) -> None:
    """Add shared launch/ad entrypoint arguments."""
    parser.add_argument(
        "file",
        nargs="?",
        help="optional Altium document or project to open",
    )
    parser.add_argument(
        "--ad-version",
        "--series",
        dest="ad_version",
        help="Altium major series to launch, for example AD25, AD26, 25, or 26",
    )
    parser.add_argument(
        "--altium-path",
        type=Path,
        help="explicit path to X2.exe or its install root",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="select and print the launch command without starting Altium",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="write machine-readable launch JSON",
    )


def register_parser(
    subparsers: argparse._SubParsersAction,
) -> argparse.ArgumentParser:
    """Register the launch command parser."""
    parser = subparsers.add_parser(
        "launch",
        help="launch Altium Designer, optionally opening a file",
        description=(
            "Launch Altium Designer using altium-monkey's launcher path. By "
            "default the newest discovered AD install is selected; --ad-version "
            "selects a major series such as AD25 or AD26."
        ),
    )
    add_launch_arguments(parser)
    parser.set_defaults(handler=cmd_launch)
    return parser


def main_ad() -> None:
    """Console-script entrypoint for the short `ad` launcher alias."""
    if any(arg in {"--version", "version"} for arg in sys.argv[1:]):
        print(cli_version_report())
        return
    parser = argparse.ArgumentParser(
        prog="ad",
        description="Launch Altium Designer, optionally opening a file.",
    )
    add_launch_arguments(parser)
    args = parser.parse_args()
    setup_cli_logging(20)
    raise SystemExit(cmd_launch(args))
