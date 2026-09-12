"""PnP command for altium_cruncher."""

import argparse
import csv
import json
import logging
from pathlib import Path

from altium_monkey.altium_pnp_position import (
    PNP_POSITION_MODES,
    normalize_pnp_position_mode,
)

from altium_cruncher.altium_cruncher_common import (
    _resolve_output_dir,
    find_prjpcb_in_cwd,
)
from altium_cruncher.bom_pnp_cli_common import configured_output_root, load_optional_bom_pnp_config, project_parameters_from_design, warn_for_unknown_variants, write_config_template
from altium_cruncher.bom_pnp_model import BOM_PNP_DEFAULT_CONFIG_NAME, select_variant_names

log = logging.getLogger(__name__)





from .pnp_artifacts import (
    PNP_CSV_ENCODING as PNP_CSV_ENCODING,
    PNP_FIXED_COLUMNS as PNP_FIXED_COLUMNS,
    _write_pnp_csv as _write_pnp_csv,
    _write_jlc_cpl_csv as _write_jlc_cpl_csv,
    _write_named_rows_csv as _write_named_rows_csv,
    _pnp_output_extension as _pnp_output_extension,
    _write_pnp_xlsx as _write_pnp_xlsx,
    _configured_pnp_artifacts as _configured_pnp_artifacts,
    _write_configured_pnp_artifact as _write_configured_pnp_artifact,
    _pnp_format_option_error as _pnp_format_option_error,
    _write_legacy_pnp_output as _write_legacy_pnp_output,
)


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

    write_config = getattr(args, "write_config", None)
    if write_config is not None:
        config_path = write_config_template(write_config)
        log.info("Wrote BOM/PnP config template: %s", config_path)
        if not getattr(args, "file", None):
            return 0

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

    config, config_path = load_optional_bom_pnp_config(getattr(args, "config", None))
    config_mode = config_path is not None and getattr(args, "format", None) is None
    variants_to_process = select_variant_names(
        available_variants,
        config,
        cli_variant=getattr(args, "variant", None),
        cli_all_variants=getattr(args, "all_variants", False),
    )
    warn_for_unknown_variants(log, variants_to_process, available_variants)

    units = getattr(args, "units", None) or config.pnp_units
    position_mode = normalize_pnp_position_mode(
        getattr(args, "position_mode", None) or config.pnp_position_mode
    )
    exclude_no_bom = (
        getattr(args, "exclude_no_bom", False) or config.pnp_exclude_no_bom
    )
    output_format = getattr(args, "format", None) or "csv"
    jlc_requested = config_mode and any(
        kind in {"jlc-cpl", "jlc-cpl-xlsx"} for kind in config.pnp_outputs
    )
    checked_format = "jlc-cpl-xlsx" if jlc_requested else output_format
    option_error = _pnp_format_option_error(checked_format, units)
    if option_error:
        log.error(option_error)
        return 1
    output_dir = (
        configured_output_root(args.output)
        if config_mode
        else _resolve_output_dir(args.output, "pnp")
    )
    project_parameters = project_parameters_from_design(design)

    files_written = 0
    for var in variants_to_process:
        try:
            pnp = design.to_pnp(
                variant=var,
                units=units,
                position_mode=position_mode,
                exclude_no_bom=exclude_no_bom,
            )
        except ValueError as e:
            log.error(f"PnP generation failed: {e}")
            return 1

        if config_mode:
            written = _configured_pnp_artifacts(
                output_dir,
                pnp,
                config=config,
                source=input_file,
                variant=var,
                units=units,
                position_mode=position_mode,
                project_parameters=project_parameters,
            )
            files_written += len(written)
            output_names = ", ".join(path.name for path in written)
        else:
            output_file = _write_legacy_pnp_output(
                output_dir,
                input_file,
                pnp,
                output_format=output_format,
                variant=var,
                units=units,
                position_mode=position_mode,
            )
            files_written += 1
            output_names = output_file.name

        variant_name = var or "base"
        log.info("PnP (%s): %s placements -> %s", variant_name, len(pnp), output_names)

    log.info(f"Generated {files_written} PnP file(s) in {output_dir}")
    return 0


def register_parser(subparsers):
    # pnp subcommand - Generate Pick-and-Place from PrjPcb
    pnp_parser = subparsers.add_parser(
        "pnp",
        help="generate Pick-and-Place from Altium project (CSV, JSON, XLSX, or JLC CPL)",
        description="Generate Pick-and-Place (PnP) from Altium PrjPcb files. "
        "Requires PcbDoc in project. Includes all component parameters. "
        "Config-driven runs can emit JSON, CSV, XLSX, and JLCPCB CPL "
        "upload columns in one invocation.",
        epilog="Examples:\n"
        "  altium-cruncher pnp project.PrjPcb\n"
        "  altium-cruncher pnp                               # Auto-detect PrjPcb in CWD\n"
        "  altium-cruncher pnp project.PrjPcb --variant V1   # Single variant\n"
        "  altium-cruncher pnp project.PrjPcb --all-variants # All variants\n"
        "  altium-cruncher pnp project.PrjPcb --units mils   # Use mils instead of mm\n"
        "  altium-cruncher pnp project.PrjPcb --position-mode component-origin\n"
        "  altium-cruncher pnp project.PrjPcb --format json  # JSON output\n"
        "  altium-cruncher pnp project.PrjPcb --format xlsx\n"
        "  altium-cruncher pnp project.PrjPcb --format jlc-cpl\n"
        "  altium-cruncher pnp project.PrjPcb --format jlc-cpl-xlsx\n"
        "  altium-cruncher pnp --write-config bom.config\n"
        "  altium-cruncher pnp project.PrjPcb --config bom.config\n"
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
        choices=["csv", "json", "xlsx", "jlc-cpl", "jlc-cpl-xlsx"],
        default=None,
        help="single output format; overrides multi-output config mode",
    )
    pnp_parser.add_argument(
        "--config",
        type=Path,
        help="BOM/PnP JSON/JSONC config (default: ./bom.config if present)",
    )
    pnp_parser.add_argument(
        "--write-config",
        nargs="?",
        const=Path(BOM_PNP_DEFAULT_CONFIG_NAME),
        type=Path,
        metavar="PATH",
        help="write a default BOM/PnP config template",
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
        default=None,
        help="coordinate units (default: config value or mm)",
    )
    pnp_parser.add_argument(
        "--position-mode",
        choices=list(PNP_POSITION_MODES),
        default=None,
        help="placement position mode (default: config value or altium-pick-place)",
    )
    pnp_parser.add_argument(
        "--exclude-no-bom",
        action="store_true",
        help="exclude STANDARD_NO_BOM components",
    )
    pnp_parser.set_defaults(handler=cmd_pnp)
    return pnp_parser
