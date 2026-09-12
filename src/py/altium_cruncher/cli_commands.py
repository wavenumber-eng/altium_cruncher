"""Ordered command registration; aliases and nested actions belong to each parser.

Review-only EasyEDA modules intentionally do not appear here. Version is supplied
by the root parser. Imports are deferred until parser construction.
"""

from __future__ import annotations

import argparse
from importlib import import_module

COMMAND_MODULES = (
    "bom",
    "clean",
    "design",
    "easyeda_import",
    "extract",
    "installs",
    "jlc",
    "json_dump",
    "launch",
    "libraries",
    "mate",
    "mco",
    "megamaid",
    "merge",
    "notes",
    "outjob",
    "pcb_layer_step",
    "pcb_svg",
    "pcbdoc",
    "pcblib",
    "pnp",
    "prjpcb",
    "profiles",
    "sch_ir",
    "sch_svg",
    "schdoc",
    "schlib",
    "split",
    "svg",
    "toon",
    "variants",
)


def register_commands(subparsers: argparse._SubParsersAction) -> None:
    """Register each public command exactly once, in established help order."""
    for name in COMMAND_MODULES:
        module = import_module(f"altium_cruncher.altium_cruncher_cmd_{name}")
        module.register_parser(subparsers)
