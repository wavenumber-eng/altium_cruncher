"""
Altium Cruncher - High-level CLI for Altium file operations.

Output policy:
    - Every command accepts -o/--output as an output directory.
    - If omitted, artifacts are written under ./output/<command>/.
    - pcb-svg is config-driven: uses pcb.svg.config (or --config) for view/options policy.
    - pcb-svg emits contract SVG geometry/metadata only; presentation labels live in HTML/report layers.
    - clean normalizes SchDoc/SchLib style attributes using JSON config; PrjPcb inputs apply to all project SchDocs.
"""

import argparse
import logging
import os
import re
import sys
from pathlib import Path
from typing import cast

# Support direct script execution: `python -m altium_cruncher`.
if __package__ in {None, ""}:
    this_dir = Path(__file__).resolve().parent
    if sys.path and Path(sys.path[0]).resolve() == this_dir:
        sys.path.pop(0)
    sys.path.insert(0, str(this_dir.parent))

from colorama import Fore, Style

from altium_cruncher.logging_utils import setup_cli_logging
from altium_cruncher._version import cli_version_report, cli_version_text

from altium_cruncher.altium_cruncher_cmd_bom import (
    register_parser as register_bom_parser,
)
from altium_cruncher.altium_cruncher_cmd_clean import (
    register_parser as register_clean_parser,
)
from altium_cruncher.altium_cruncher_cmd_design import (
    register_parser as register_design_parser,
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
from altium_cruncher.altium_cruncher_cmd_pcb_svg import (
    register_parser as register_pcb_svg_parser,
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

LOG_LEVEL_BY_NAME = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


def _help_color_enabled(stream: object | None = None) -> bool:
    """Return whether help text should include ANSI color escapes."""
    if os.environ.get("NO_COLOR") is not None or os.environ.get("TERM") == "dumb":
        return False
    output_stream = sys.stdout if stream is None else stream
    isatty = getattr(output_stream, "isatty", None)
    return bool(callable(isatty) and isatty())


def _color_command_names_in_help(help_text: str, command_names: tuple[str, ...]) -> str:
    """Color command names in the root argparse command list."""
    if not command_names:
        return help_text
    command_pattern = "|".join(re.escape(command) for command in command_names)
    line_pattern = re.compile(
        rf"^(?P<indent>\s{{4}})(?P<command>{command_pattern})(?P<rest>(?:\s{{2,}}.*)?)$",
        re.MULTILINE,
    )

    def replace(match: re.Match[str]) -> str:
        command = match.group("command")
        color = f"{Style.BRIGHT}{Fore.YELLOW}"
        return f"{match.group('indent')}{color}{command}{Style.RESET_ALL}{match.group('rest')}"

    return line_pattern.sub(replace, help_text)


def _format_parser_error_line(prog: str, message: str, *, color: bool) -> str:
    """Format the argparse error line, optionally with terminal color."""
    error_text = f"{prog}: error: {message}"
    if color:
        error_text = f"{Style.BRIGHT}{Fore.RED}{error_text}{Style.RESET_ALL}"
    return f"{error_text}\n"


class CruncherArgumentParser(argparse.ArgumentParser):
    """Argument parser that prints the package version in help output."""

    command_names_for_help_color: tuple[str, ...] = ()

    def format_help(self) -> str:
        """Return help text with a visible version line at the top."""
        help_text = super().format_help().rstrip()
        if _help_color_enabled():
            help_text = _color_command_names_in_help(
                help_text,
                self.command_names_for_help_color,
            )
        return f"{cli_version_text()}\n\n{help_text}\n"

    def error(self, message: str) -> None:
        """Print parser errors with red highlighting on interactive terminals."""
        self.print_usage(sys.stderr)
        self.exit(
            2,
            _format_parser_error_line(
                self.prog,
                message,
                color=_help_color_enabled(sys.stderr),
            ),
        )


class VersionReportAction(argparse.Action):
    """Print the full version report without argparse whitespace normalization."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | list[str] | None,
        option_string: str | None = None,
    ) -> None:
        del namespace, values, option_string
        print(cli_version_report())
        parser.exit(0)


def _configure_root_help_color(
    parser: CruncherArgumentParser,
    subparsers: argparse._SubParsersAction,
) -> None:
    """Attach root command names used for colorized terminal help."""
    parser.command_names_for_help_color = tuple(str(command) for command in subparsers.choices)


def _cmd_version(_args: argparse.Namespace) -> int:
    print(cli_version_report())
    return 0


def _cli_log_level(args: argparse.Namespace) -> int:
    """Return the requested root CLI logging threshold."""
    if bool(getattr(args, "quiet", False)):
        return logging.WARNING
    if bool(getattr(args, "verbose", False)):
        return logging.DEBUG
    log_level = getattr(args, "log_level", None)
    if log_level:
        return LOG_LEVEL_BY_NAME[str(log_level)]
    return logging.INFO


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
    parser = subparsers.add_parser(command, help=help_text, description=help_text)
    parser.set_defaults(handler=_cmd_missing_easyeda)


def _register_easyeda_parsers(subparsers: argparse._SubParsersAction) -> None:
    """Register EasyEDA commands when their optional runtime dependency is installed."""
    try:
        from altium_cruncher.altium_cruncher_cmd_easyeda_import import (
            register_parser as register_easyeda_import_parser,
        )
    except ModuleNotFoundError as exc:
        if exc.name is None or not exc.name.startswith("easyeda_monkey"):
            raise
        _register_missing_easyeda_parser(
            subparsers,
            "easyeda-import",
            "EXPERIMENTAL: import EasyEDA symbols/footprints (requires easyeda-monkey)",
        )
        return

    register_easyeda_import_parser(subparsers)


def main() -> None:
    """Main entry point for the altium-cruncher CLI tool."""
    parser = CruncherArgumentParser(
        prog="altium-cruncher",
        description="High-level CLI for Altium file operations",
        epilog="Run `altium-cruncher <command> --help` for command-specific options.",
    )
    parser.add_argument(
        "--version",
        nargs=0,
        action=VersionReportAction,
        help="Print version information and exit",
    )
    logging_group = parser.add_mutually_exclusive_group()
    logging_group.add_argument(
        "--quiet",
        action="store_true",
        help="Only print warnings and errors from command logging",
    )
    logging_group.add_argument(
        "--verbose",
        action="store_true",
        help="Print debug-level command and parser logging",
    )
    logging_group.add_argument(
        "--log-level",
        choices=tuple(LOG_LEVEL_BY_NAME),
        help="Set command logging level explicitly",
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
    register_design_parser(command_subparsers)
    _register_easyeda_parsers(command_subparsers)
    register_extract_parser(command_subparsers)
    register_jlc_parser(command_subparsers)
    register_megamaid_parser(command_subparsers)
    register_merge_parser(command_subparsers)
    register_pcb_layer_step_parser(command_subparsers)
    register_pcb_svg_parser(command_subparsers)
    register_pnp_parser(command_subparsers)
    register_sch_svg_parser(command_subparsers)
    register_split_parser(command_subparsers)
    register_svg_parser(command_subparsers)

    version_parser = subparsers.add_parser("version", help="Print version information")
    version_parser.set_defaults(handler=_cmd_version)
    _configure_root_help_color(parser, subparsers)

    args, unknown_args = parser.parse_known_args()
    if unknown_args:
        parser.error(f"unrecognized arguments: {' '.join(unknown_args)}")

    setup_cli_logging(_cli_log_level(args))

    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return
    sys.exit(handler(args))


if __name__ == "__main__":
    main()
