"""Altium Designer install discovery command."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from altium_cruncher.altium_environment import discover_altium_installs


def cmd_installs(args: argparse.Namespace) -> int:
    """Print discovered Altium Designer installs."""
    roots = [Path(path).resolve() for path in getattr(args, "install_root", [])]
    installs = discover_altium_installs(install_roots=roots or None)
    if getattr(args, "json", False):
        print(
            json.dumps(
                {
                    "schema": "altium_cruncher.installs.a0",
                    "installs": [install.to_dict() for install in installs],
                },
                indent=2,
            )
        )
        return 0

    if not installs:
        print("No Altium Designer installs found.")
        return 0
    for install in installs:
        version = install.registry_version or install.runtime_tfm or ""
        suffix = f" ({version})" if version else ""
        print(f"{install.label:<12} {install.x2_path}{suffix}")
    return 0


def register_parser(
    subparsers: argparse._SubParsersAction,
) -> argparse.ArgumentParser:
    """Register the installs command parser."""
    parser = subparsers.add_parser(
        "installs",
        help="list discovered Altium Designer installs",
        description=(
            "List Altium Designer install roots where X2.exe exists. The command "
            "scans Program Files, ALTIUM_AD*_ROOT environment overrides, and "
            "Windows Altium build registry rows when available."
        ),
    )
    parser.add_argument(
        "--install-root",
        action="append",
        default=[],
        help="additional Altium parent install root to scan",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="write machine-readable discovery JSON",
    )
    parser.set_defaults(handler=cmd_installs)
    return parser
