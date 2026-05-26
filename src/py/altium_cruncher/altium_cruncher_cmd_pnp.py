"""PnP command for altium_cruncher."""

import argparse
from collections.abc import Sequence
import csv
import json
import logging
from pathlib import Path

from altium_cruncher.altium_cruncher_common import (
    _resolve_output_dir,
    find_prjpcb_in_cwd,
)
from altium_cruncher.bom_pnp_model import (
    JLC_CPL_COLUMNS,
    jlc_cpl_rows,
    normalize_pnp_entries,
    pnp_payload,
    sort_placements,
)

log = logging.getLogger(__name__)


PNP_FIXED_COLUMNS = [
    "Designator",
    "Comment",
    "Layer",
    "Footprint",
    "Center-X({units})",
    "Center-Y({units})",
    "Rotation",
    "Description",
]


def _write_pnp_csv(
    output_file: Path,
    placements: Sequence[object],
    *,
    units: str,
) -> None:
    """Write normalized PnP rows with parameters flattened into columns."""
    normalized = normalize_pnp_entries(placements, units=units)
    param_columns = sorted(
        {param_name for entry in normalized for param_name in entry.parameters}
    )
    fixed_columns = [column.format(units=units) for column in PNP_FIXED_COLUMNS]

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(fixed_columns + param_columns)
        for entry in sort_placements(normalized):
            row = [
                entry.designator,
                entry.comment,
                entry.layer,
                entry.footprint,
                f"{entry.center_x:.4f}",
                f"{entry.center_y:.4f}",
                f"{entry.rotation:.2f}",
                entry.description,
            ]
            row.extend(
                entry.parameters.get(param_name, "") for param_name in param_columns
            )
            writer.writerow(row)


def _write_jlc_cpl_csv(
    output_file: Path,
    placements: Sequence[object],
    *,
    units: str,
) -> None:
    """Write normalized placements in JLCPCB CPL upload format."""
    normalized = normalize_pnp_entries(placements, units=units)
    rows = jlc_cpl_rows(normalized)
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=list(JLC_CPL_COLUMNS),
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows)


def _pnp_format_option_error(output_format: str, units: str) -> str:
    """Return an option error message for incompatible PnP options."""
    if output_format == "jlc-cpl" and units != "mm":
        return "jlc-cpl output requires --units mm because JLCPCB CPL uses mm"
    return ""


def cmd_pnp(args) -> int:
    """
    Handle pnp subcommand - generate Pick-and-Place from PrjPcb files.

    REQ-CLI-005: PnP generation with variant support (CSV or JSON format).

    Args:
        args: Parsed argparse namespace with file and output options.

    Returns:
        Exit code (0 for success, 1 for error).
    """
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
            log.info("Usage: altium-cruncher pnp [project.PrjPcb]")
            return 1
        log.info(f"Auto-detected project: {input_file.name}")

    # PnP requires PrjPcb (needs PcbDoc)
    suffix = input_file.suffix.lower()
    if suffix != ".prjpcb":
        log.error(f"PnP generation requires a .PrjPcb file, got: {suffix}")
        log.info("Supported types: .PrjPcb")
        return 1

    design = AltiumDesign.from_prjpcb(input_file)

    # Show available variants
    available_variants = design.get_variants()
    if available_variants:
        log.info(f"Available variants: {', '.join(available_variants)}")
    else:
        log.info("No variants defined in project")

    # Determine output directory
    output_dir = _resolve_output_dir(args.output, "pnp")

    # Get units
    units = getattr(args, "units", "mm")

    # Determine exclude_no_bom setting
    exclude_no_bom = getattr(args, "exclude_no_bom", False)

    # Determine which variants to process
    all_variants = getattr(args, "all_variants", False)
    variant = getattr(args, "variant", None)

    if all_variants and available_variants:
        variants_to_process = [None] + available_variants  # None = base (no variant)
    elif variant:
        if variant not in available_variants:
            log.warning(
                f"Variant '{variant}' not found in project "
                f"(available: {', '.join(available_variants) or 'none'})"
            )
        variants_to_process = [variant]
    else:
        variants_to_process = [None]  # No variant filtering

    # Get output format
    output_format = getattr(args, "format", "csv")
    option_error = _pnp_format_option_error(output_format, units)
    if option_error:
        log.error(option_error)
        return 1

    files_written = 0
    for var in variants_to_process:
        try:
            pnp = design.to_pnp(variant=var, units=units, exclude_no_bom=exclude_no_bom)
        except ValueError as e:
            log.error(f"PnP generation failed: {e}")
            return 1

        # Determine output filename
        base_name = input_file.stem
        ext = "json" if output_format == "json" else "csv"
        if var:
            output_file = output_dir / f"{base_name}_{var}_pnp.{ext}"
        else:
            output_file = output_dir / f"{base_name}_pnp.{ext}"

        if output_format == "json":
            normalized = normalize_pnp_entries(pnp, units=units)
            output_data = pnp_payload(
                normalized,
                source=input_file,
                variant=var,
                units=units,
            )
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2)
        elif output_format == "jlc-cpl":
            _write_jlc_cpl_csv(output_file, pnp, units=units)
        else:
            _write_pnp_csv(output_file, pnp, units=units)

        variant_name = var or "base"
        log.info(f"PnP ({variant_name}): {len(pnp)} placements -> {output_file.name}")
        files_written += 1

    log.info(f"Generated {files_written} PnP file(s) in {output_dir}")
    return 0


def register_parser(subparsers):
    # pnp subcommand - Generate Pick-and-Place from PrjPcb
    pnp_parser = subparsers.add_parser(
        "pnp",
        help="generate Pick-and-Place from Altium project (CSV, JSON, or JLC CPL)",
        description="Generate Pick-and-Place (PnP) from Altium PrjPcb files. "
        "Requires PcbDoc in project. Includes all component parameters. "
        "jlc-cpl writes JLCPCB CPL upload columns.",
        epilog="Examples:\n"
        "  altium-cruncher pnp project.PrjPcb\n"
        "  altium-cruncher pnp                               # Auto-detect PrjPcb in CWD\n"
        "  altium-cruncher pnp project.PrjPcb --variant V1   # Single variant\n"
        "  altium-cruncher pnp project.PrjPcb --all-variants # All variants\n"
        "  altium-cruncher pnp project.PrjPcb --units mils   # Use mils instead of mm\n"
        "  altium-cruncher pnp project.PrjPcb --format json  # JSON output\n"
        "  altium-cruncher pnp project.PrjPcb --format jlc-cpl\n"
        "  altium-cruncher pnp project.PrjPcb -o output_dir/",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    pnp_parser.add_argument(
        "file",
        nargs="?",
        help="PrjPcb file (optional if PrjPcb in CWD)",
    )
    pnp_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output directory (default: ./output/pnp)",
    )
    pnp_parser.add_argument(
        "--format",
        choices=["csv", "json", "jlc-cpl"],
        default="csv",
        help="output format (default: csv)",
    )
    pnp_parser.add_argument(
        "--variant",
        type=str,
        help="filter by specific variant name",
    )
    pnp_parser.add_argument(
        "--all-variants",
        action="store_true",
        help="generate PnP for all variants (plus base)",
    )
    pnp_parser.add_argument(
        "--units",
        choices=["mm", "mils"],
        default="mm",
        help="coordinate units (default: mm)",
    )
    pnp_parser.add_argument(
        "--exclude-no-bom",
        action="store_true",
        help="exclude STANDARD_NO_BOM components",
    )
    pnp_parser.set_defaults(handler=cmd_pnp)
    return pnp_parser
