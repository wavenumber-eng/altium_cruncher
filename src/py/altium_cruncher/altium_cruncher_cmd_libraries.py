from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

from colorama import Fore, Style, just_fix_windows_console

from altium_cruncher.altium_cruncher_mate_libraries import (
    AltiumLibraryEntry,
    AltiumLibraryScanResult,
    scan_altium_libraries,
)


def cmd_libraries(args: argparse.Namespace) -> int:
    """List symbols and footprints discoverable from Altium libraries."""
    roots = args.roots or [Path.cwd()]
    try:
        result = scan_altium_libraries(
            roots,
            recursive=not bool(args.no_recursive),
        )
    except Exception as exc:
        print(f"Failed scanning libraries: {exc}", file=sys.stderr)
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


def print_library_scan_result(
    result: AltiumLibraryScanResult,
    *,
    base_dir: Path,
    absolute: bool = False,
    color: bool = True,
) -> None:
    """Print a human-readable library scan result."""
    use_color = color and _terminal_color_enabled()
    if use_color:
        just_fix_windows_console()
    _print_section(
        "Symbols",
        result.symbols,
        base_dir=base_dir,
        absolute=absolute,
        color=use_color,
    )
    _print_section(
        "Footprints",
        result.footprints,
        base_dir=base_dir,
        absolute=absolute,
        color=use_color,
    )
    if result.warnings:
        print(_style("Warnings", Fore.YELLOW, use_color))
        for warning in result.warnings:
            print(f"  {_style(warning, Fore.YELLOW, use_color)}")


def _print_section(
    label: str,
    entries: tuple[AltiumLibraryEntry, ...],
    *,
    base_dir: Path,
    absolute: bool,
    color: bool,
) -> None:
    print(_style(f"{label} ({len(entries)})", Fore.YELLOW, color, bright=True))
    if not entries:
        print(f"  {_style('none found', Fore.WHITE, color)}")
        return
    name_width = max(len(entry.name) for entry in entries)
    for entry in entries:
        name = _style(entry.name, Fore.CYAN, color)
        path = _style(
            _display_path(entry.library_path, base_dir=base_dir, absolute=absolute),
            Fore.WHITE,
            color,
        )
        print(f"  {name:<{name_width + _ansi_padding(name, entry.name)}}  {path}")


def _display_path(path: Path, *, base_dir: Path, absolute: bool) -> str:
    resolved = path.resolve()
    if absolute:
        return str(resolved)
    try:
        return resolved.relative_to(base_dir.resolve()).as_posix()
    except ValueError:
        return str(resolved)


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


def _ansi_padding(styled: str, plain: str) -> int:
    return len(styled) - len(plain)


def register_parser(
    subparsers: argparse._SubParsersAction,
) -> argparse.ArgumentParser:
    """Register the libraries command parser."""
    parser = subparsers.add_parser(
        "libraries",
        help="list symbols and footprints in Altium libraries",
        description=(
            "Scan .SchLib and .PcbLib files under one or more roots and list "
            "the symbol and footprint names available for commands such as mate."
        ),
    )
    parser.add_argument(
        "roots",
        nargs="*",
        type=Path,
        help="library files or directories to scan (default: current directory)",
    )
    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="scan only the direct files in each directory root",
    )
    parser.add_argument(
        "--absolute",
        action="store_true",
        help="show absolute paths in human output instead of paths relative to cwd",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="disable terminal color in human output",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="write machine-readable JSON with absolute paths",
    )
    parser.set_defaults(handler=cmd_libraries)
    return parser
