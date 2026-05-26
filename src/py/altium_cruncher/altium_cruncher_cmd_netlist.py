"""Netlist command for altium_cruncher."""

import argparse
import logging
from pathlib import Path

from altium_cruncher.altium_cruncher_common import _resolve_output_dir, find_prjpcb_in_cwd

log = logging.getLogger(__name__)
def cmd_netlist(args) -> int:
    """
    Handle netlist subcommand - generate netlist JSON from SchDoc/PrjPcb files.

    REQ-CLI-006: Netlist JSON generation using AltiumDesign.to_json().

    Args:
        args: Parsed argparse namespace with file and output options.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    import json
    from altium_monkey.altium_design import AltiumDesign

    # Determine input file
    input_file: Path | None = None

    if args.file:
        input_file = Path(args.file).resolve()
        if not input_file.exists():
            log.error(f"File not found: {input_file}")
            return 1
    else:
        # Auto-detect PrjPcb in CWD
        input_file = find_prjpcb_in_cwd()
        if not input_file:
            log.error("No file specified and no .PrjPcb found in current directory")
            log.info("Usage: altium_cruncher netlist [file.SchDoc | project.PrjPcb]")
            return 1
        log.info(f"Auto-detected project: {input_file.name}")

    # Validate file type
    suffix = input_file.suffix.lower()
    if suffix == '.schdoc':
        design = AltiumDesign.from_schdoc(input_file)
    elif suffix == '.prjpcb':
        design = AltiumDesign.from_prjpcb(input_file)
    else:
        log.error(f"Unsupported file type: {suffix}")
        log.info("Supported types: .SchDoc, .PrjPcb")
        return 1

    # Determine output directory
    output_dir = _resolve_output_dir(args.output, "netlist")

    # Determine output filename
    output_file = output_dir / f"{input_file.stem}_netlist.json"

    # Include indexes option
    include_indexes = not getattr(args, 'no_indexes', False)

    # Serialize the design model to JSON
    design_json = design.to_json(include_indexes=include_indexes)

    # Write JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(design_json, f, indent=2)

    # Summary
    log.info(f"Netlist: {len(design_json.get('components', []))} components, "
             f"{len(design_json.get('nets', []))} nets -> {output_file.name}")

    return 0




def register_parser(subparsers):
    # netlist subcommand - Generate netlist JSON from SchDoc/PrjPcb
    netlist_parser = subparsers.add_parser(
        'netlist',
        help='generate netlist JSON from Altium schematic documents',
        description='Generate netlist JSON from Altium SchDoc or PrjPcb files. '
                    'Serializes the full AltiumDesign model including nets, components, and hierarchy.',
        epilog='Examples:\n'
               '  altium_cruncher netlist project.PrjPcb\n'
               '  altium_cruncher netlist schematic.SchDoc\n'
               '  altium_cruncher netlist                    # Auto-detect PrjPcb in CWD\n'
               '  altium_cruncher netlist project.PrjPcb --no-indexes  # Without lookup indexes\n'
               '  altium_cruncher netlist project.PrjPcb -o output_dir/',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    netlist_parser.add_argument('file', nargs='?', help='SchDoc or PrjPcb file (optional if PrjPcb in CWD)')
    netlist_parser.add_argument('-o', '--output', type=Path, help='output directory (default: ./output/netlist)')
    netlist_parser.add_argument('--no-indexes', action='store_true', help='exclude lookup indexes from JSON')
    netlist_parser.set_defaults(handler=cmd_netlist)
    return netlist_parser
