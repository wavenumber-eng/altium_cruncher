"""Legacy svg shortcut command for altium_cruncher."""

import argparse
import logging
from pathlib import Path

from altium_cruncher.altium_cruncher_cmd_pcb_svg import (
    add_pcb_svg_option_arguments,
    cmd_pcb_svg,
)
from altium_cruncher.altium_cruncher_cmd_sch_svg import cmd_sch_svg
from altium_cruncher.altium_cruncher_common import (
    find_pcbdocs_in_cwd,
    find_prjpcb_in_cwd,
    find_prjpcbs_in_cwd,
)

log = logging.getLogger(__name__)


def _project_has_pcbdoc(prjpcb_path: Path) -> bool:
    """Return True when project resolves at least one PcbDoc path."""
    try:
        from altium_monkey.altium_prjpcb import AltiumPrjPcb

        project = AltiumPrjPcb(prjpcb_path)
        return bool(project.get_pcbdoc_paths())
    except Exception:
        return False


def _resolve_svg_execution_modes(input_file: Path | None) -> tuple[bool, bool]:
    """
    Return (run_sch_svg, run_pcb_svg) for legacy svg shortcut.
    """
    if input_file is not None:
        suffix = input_file.suffix.lower()
        if suffix in {".schdoc", ".schlib"}:
            return True, False
        if suffix == ".pcbdoc":
            return False, True
        if suffix == ".prjpcb":
            return True, _project_has_pcbdoc(input_file)
        return False, False

    has_schematic_input = find_prjpcb_in_cwd() is not None
    has_pcb_input = bool(find_pcbdocs_in_cwd())
    if not has_pcb_input:
        has_pcb_input = any(_project_has_pcbdoc(path) for path in find_prjpcbs_in_cwd())
    return has_schematic_input, has_pcb_input


def cmd_svg(args) -> int:
    """
    Handle svg shortcut command.

    Behavior:
    - `.SchDoc` / `.SchLib` input: run `sch-svg`
    - `.PcbDoc` input: run `pcb-svg`
    - `.PrjPcb` input: run both `sch-svg` then `pcb-svg`
    - no input: auto-detect and run whichever of `sch-svg` / `pcb-svg` has valid inputs
    """
    input_file: Path | None = None
    if args.file:
        input_file = Path(args.file).resolve()
        if not input_file.exists():
            log.error(f"File not found: {input_file}")
            return 1

    run_sch, run_pcb = _resolve_svg_execution_modes(input_file)
    if not run_sch and not run_pcb:
        if input_file is not None:
            log.error(f"Unsupported file type: {input_file.suffix.lower()}")
            log.info("Supported svg shortcut file types: .SchDoc, .SchLib, .PcbDoc, .PrjPcb")
            return 1
        log.error("No file specified and no compatible .PrjPcb/.PcbDoc found in current directory")
        log.info("Usage: altium-cruncher svg [file.SchDoc | file.SchLib | board.PcbDoc | project.PrjPcb]")
        return 1

    # Meta-command output policy:
    # - no -o: let subcommands use their own defaults (./output/sch-svg, ./output/pcb-svg)
    # - with -o <dir>: write under <dir>/sch-svg and <dir>/pcb-svg
    output_root = args.output.resolve() if args.output else None
    return_codes: list[int] = []

    if run_sch:
        log.info("svg shortcut: running sch-svg")
        sch_args = argparse.Namespace(
            file=args.file,
            output=(output_root / "sch-svg") if output_root else None,
        )
        return_codes.append(cmd_sch_svg(sch_args))

    if run_pcb:
        log.info("svg shortcut: running pcb-svg")
        pcb_args = argparse.Namespace(**vars(args))
        pcb_args.output = (output_root / "pcb-svg") if output_root else None
        return_codes.append(cmd_pcb_svg(pcb_args))

    return 0 if return_codes and all(code == 0 for code in return_codes) else 1


def register_parser(subparsers):
    svg_parser = subparsers.add_parser(
        "svg",
        help="legacy shortcut: run sch-svg and/or pcb-svg based on input",
        description="Compatibility shortcut command. Routes to sch-svg and pcb-svg based on input type.",
        epilog="Examples:\n"
               "  altium-cruncher svg schematic.SchDoc      # runs sch-svg\n"
               "  altium-cruncher svg board.PcbDoc          # runs pcb-svg\n"
               "  altium-cruncher svg project.PrjPcb        # runs sch-svg + pcb-svg\n"
               "  altium-cruncher svg                        # auto-detects and runs available commands\n"
               "  altium-cruncher svg -o output_dir project.PrjPcb",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    svg_parser.add_argument(
        "file",
        nargs="?",
        help="SchDoc, SchLib, PcbDoc, or PrjPcb file (optional if auto-detected in CWD)",
    )
    svg_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="base output directory (default: ./output; writes to ./output/sch-svg and ./output/pcb-svg)",
    )
    add_pcb_svg_option_arguments(svg_parser, include_legacy_pcb_flag=True)
    svg_parser.set_defaults(handler=cmd_svg)
    return svg_parser
