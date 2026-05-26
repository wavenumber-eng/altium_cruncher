"""sch-svg command for altium_cruncher."""

import argparse
import logging
from pathlib import Path

from altium_cruncher.altium_cruncher_common import _resolve_output_dir, find_prjpcb_in_cwd

log = logging.getLogger(__name__)


def cmd_sch_svg(args) -> int:
    """
    Handle sch-svg subcommand - generate SVG from SchDoc/PrjPcb/SchLib files.
    """
    from altium_monkey.altium_prjpcb import AltiumPrjPcb
    from altium_monkey.altium_schdoc import AltiumSchDoc
    from altium_monkey.altium_schlib import AltiumSchLib

    input_file: Path | None = None
    if args.file:
        input_file = Path(args.file).resolve()
        if not input_file.exists():
            log.error(f"File not found: {input_file}")
            return 1
    else:
        input_file = find_prjpcb_in_cwd()
        if not input_file:
            log.error("No file specified and no .PrjPcb found in current directory")
            log.info("Usage: altium_cruncher sch-svg [file.SchDoc | project.PrjPcb | library.SchLib]")
            return 1
        log.info(f"Auto-detected project: {input_file.name}")

    output_dir = _resolve_output_dir(args.output, "sch-svg")
    suffix = input_file.suffix.lower()

    schdoc_files: list[Path] = []
    project_parameters: dict[str, str] = {}

    if suffix == ".schdoc":
        schdoc_files = [input_file]
    elif suffix == ".prjpcb":
        project = AltiumPrjPcb(input_file)
        schdoc_files = project.get_schdoc_paths()
        project_parameters = dict(project.parameters)
        current_variant = project.get_current_variant()
        if current_variant:
            project_parameters["VariantName"] = current_variant
        if not schdoc_files:
            log.error(f"No SchDoc files found in project: {input_file}")
            return 1
        log.info(f"Found {len(schdoc_files)} SchDoc file(s) in project")
    elif suffix == ".schlib":
        try:
            schlib = AltiumSchLib(input_file)
            log.info(f"Processing SchLib: {input_file.name}")
            log.info(f"  Symbols: {len(schlib.symbols)}")

            svg_dict = schlib.to_svg(output_dir=output_dir)

            total_svgs = 0
            for symbol_name, parts in svg_dict.items():
                for part_id in parts:
                    total_svgs += 1
                    if len(parts) > 1:
                        log.info(f"  -> {symbol_name}_part{part_id}.svg")
                    else:
                        log.info(f"  -> {symbol_name}.svg")

            log.info(f"Successfully generated {total_svgs} SVG file(s)")
            return 0
        except Exception as exc:
            log.error(f"Error processing SchLib: {exc}")
            return 1
    else:
        log.error(f"Unsupported file type: {suffix}")
        log.info("Supported schematic SVG types: .SchDoc, .PrjPcb, .SchLib")
        return 1

    success_count = 0
    for schdoc_path in schdoc_files:
        output_file = output_dir / f"{schdoc_path.stem}.svg"
        log.info(f"Processing: {schdoc_path.name}")
        try:
            schdoc = AltiumSchDoc(schdoc_path)
            svg_content = schdoc.to_svg(project_parameters=project_parameters, wrap_components=True)
            output_file.write_text(svg_content, encoding="utf-8")
            log.info(f"  -> {output_file.name}")
            success_count += 1
        except Exception as exc:
            log.error(f"Error processing {schdoc_path.name}: {exc}")

    if success_count == len(schdoc_files):
        log.info(f"Successfully generated {success_count} SVG file(s)")
        return 0

    log.warning(f"Generated {success_count}/{len(schdoc_files)} SVG file(s)")
    return 1


def register_parser(subparsers):
    sch_svg_parser = subparsers.add_parser(
        "sch-svg",
        help="generate schematic SVG from Altium SchDoc/PrjPcb/SchLib",
        description="Generate SVG files from Altium SchDoc, PrjPcb, or SchLib inputs.",
        epilog="Examples:\n"
               "  altium_cruncher sch-svg schematic.SchDoc\n"
               "  altium_cruncher sch-svg project.PrjPcb\n"
               "  altium_cruncher sch-svg library.SchLib\n"
               "  altium_cruncher sch-svg                             # Auto-detect PrjPcb in CWD\n"
               "  altium_cruncher sch-svg project.PrjPcb -o output_dir/",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sch_svg_parser.add_argument(
        "file",
        nargs="?",
        help="SchDoc, PrjPcb, or SchLib file (optional if PrjPcb in CWD)",
    )
    sch_svg_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output directory (default: ./output/sch-svg)",
    )
    sch_svg_parser.set_defaults(handler=cmd_sch_svg)
    return sch_svg_parser
