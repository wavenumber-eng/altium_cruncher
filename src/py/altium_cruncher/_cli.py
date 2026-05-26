"""
Altium Cruncher - High-level CLI for Altium file operations.

Output policy:
    - Every command accepts -o/--output as an output directory.
    - If omitted, artifacts are written under ./output/<command>/.
    - pcb-svg is config-driven: uses pcb-svg.json (or --config) for view/options policy.
    - pcb-svg emits contract SVG geometry/metadata only; presentation labels live in HTML/report layers.
    - clean normalizes SchDoc/SchLib style attributes using JSON config; PrjPcb inputs apply to all project SchDocs.
"""

import argparse
import sys
from pathlib import Path
from typing import cast

# Support direct script execution: `python -m altium_cruncher`.
if __package__ in {None, ""}:
    this_dir = Path(__file__).resolve().parent
    if sys.path and Path(sys.path[0]).resolve() == this_dir:
        sys.path.pop(0)
    sys.path.insert(0, str(this_dir.parent))

from altium_cruncher.logging_utils import setup_cli_logging
from altium_cruncher._version import cli_version_text

from altium_cruncher.altium_cruncher_cmd_bom import (
    register_parser as register_bom_parser,
)
from altium_cruncher.altium_cruncher_cmd_clean import (
    register_parser as register_clean_parser,
)
from altium_cruncher.altium_cruncher_cmd_extract import (
    register_parser as register_extract_parser,
)
from altium_cruncher.altium_cruncher_cmd_jlc import (
    register_parser as register_jlc_parser,
)
from altium_cruncher.altium_cruncher_cmd_merge import (
    register_parser as register_merge_parser,
)
from altium_cruncher.altium_cruncher_cmd_megamaid import (
    register_parser as register_megamaid_parser,
)
from altium_cruncher.altium_cruncher_cmd_netlist import (
    register_parser as register_netlist_parser,
)
from altium_cruncher.altium_cruncher_cmd_pcb_svg import (
    register_parser as register_pcb_svg_parser,
)
from altium_cruncher.altium_cruncher_cmd_pcblib_footprint_3d import (
    register_parser as register_pcblib_footprint_3d_parser,
)
from altium_cruncher.altium_cruncher_cmd_pcb_layer_step import (
    register_parser as register_pcb_layer_step_parser,
)
from altium_cruncher.altium_cruncher_cmd_pnp import (
    register_parser as register_pnp_parser,
)
from altium_cruncher.altium_cruncher_cmd_sch_svg import (
    register_parser as register_sch_svg_parser,
)
from altium_cruncher.altium_cruncher_cmd_split import (
    register_parser as register_split_parser,
)
from altium_cruncher.altium_cruncher_cmd_svg import (
    register_parser as register_svg_parser,
)


class CruncherArgumentParser(argparse.ArgumentParser):
    """Argument parser that prints the package version in help output."""

    def format_help(self) -> str:
        """Return help text with a visible version line at the top."""
        help_text = super().format_help().rstrip()
        return f"{cli_version_text()}\n\n{help_text}\n"


def _cmd_version(_args: argparse.Namespace) -> int:
    print(cli_version_text())
    return 0


def _cmd_missing_easyeda(_args: argparse.Namespace) -> int:
    """Report that an EasyEDA command needs the optional dependency extra."""
    print(
        "EasyEDA commands require the optional easyeda dependency: "
        "install altium-cruncher[easyeda] or install easyeda-monkey "
        "alongside altium-cruncher.",
        file=sys.stderr,
    )
    return 2


def _register_missing_easyeda_parser(
    subparsers: argparse._SubParsersAction,
    command: str,
    help_text: str,
) -> None:
    """Register an EasyEDA command placeholder when the optional extra is absent."""
    parser = subparsers.add_parser(command, help=help_text)
    parser.set_defaults(handler=_cmd_missing_easyeda)


def _register_easyeda_parsers(subparsers: argparse._SubParsersAction) -> None:
    """Register EasyEDA commands when their optional runtime dependency is installed."""
    try:
        from altium_cruncher.altium_cruncher_cmd_easyeda_footprint_review import (
            register_parser as register_easyeda_footprint_review_parser,
        )
        from altium_cruncher.altium_cruncher_cmd_easyeda_import import (
            register_parser as register_easyeda_import_parser,
        )
        from altium_cruncher.altium_cruncher_cmd_easyeda_review import (
            register_parser as register_easyeda_review_parser,
        )
    except ModuleNotFoundError as exc:
        if exc.name is None or not exc.name.startswith("easyeda_monkey"):
            raise
        _register_missing_easyeda_parser(
            subparsers,
            "easyeda-footprint-review",
            "Review EasyEDA footprint imports (requires easyeda-monkey)",
        )
        _register_missing_easyeda_parser(
            subparsers,
            "easyeda-import",
            "Import EasyEDA symbols/footprints (requires easyeda-monkey)",
        )
        _register_missing_easyeda_parser(
            subparsers,
            "easyeda-review",
            "Review EasyEDA schematic imports (requires easyeda-monkey)",
        )
        return

    register_easyeda_footprint_review_parser(subparsers)
    register_easyeda_import_parser(subparsers)
    register_easyeda_review_parser(subparsers)


def main() -> None:
    """Main entry point for the altium-cruncher CLI tool."""
    setup_cli_logging()

    parser = CruncherArgumentParser(
        prog="altium-cruncher",
        description="High-level CLI for Altium file operations",
        epilog="Run `altium-cruncher <command> --help` for command-specific options.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=cli_version_text(),
        help="Print version information and exit",
    )
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        metavar="<command>",
        parser_class=CruncherArgumentParser,
    )
    command_subparsers = cast(
        "argparse._SubParsersAction[argparse.ArgumentParser]",
        subparsers,
    )

    register_bom_parser(command_subparsers)
    register_clean_parser(command_subparsers)
    _register_easyeda_parsers(command_subparsers)
    register_extract_parser(command_subparsers)
    register_jlc_parser(command_subparsers)
    register_megamaid_parser(command_subparsers)
    register_merge_parser(command_subparsers)
    register_netlist_parser(command_subparsers)
    register_pcb_layer_step_parser(command_subparsers)
    register_pcb_svg_parser(command_subparsers)
    register_pcblib_footprint_3d_parser(command_subparsers)
    register_pnp_parser(command_subparsers)
    register_sch_svg_parser(command_subparsers)
    register_split_parser(command_subparsers)
    register_svg_parser(command_subparsers)

    version_parser = subparsers.add_parser("version", help="Print version information")
    version_parser.set_defaults(handler=_cmd_version)

    args, unknown_args = parser.parse_known_args()
    if unknown_args:
        parser.error(f"unrecognized arguments: {' '.join(unknown_args)}")

    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return
    sys.exit(handler(args))


if __name__ == "__main__":
    main()
