"""BOM command for altium_cruncher."""

import argparse
import csv
import json
import logging
from pathlib import Path

from altium_cruncher.altium_cruncher_common import (
    _resolve_output_dir,
    find_prjpcb_in_cwd,
)
from altium_cruncher.bom_pnp_cli_common import configured_output_root, load_or_create_bom_pnp_config, load_optional_bom_pnp_config, project_parameters_from_design, warn_for_unknown_variants, write_config_template
from altium_cruncher.bom_pnp_model import BOM_PNP_DEFAULT_CONFIG_NAME, select_variant_names

log = logging.getLogger(__name__)




from .bom_artifacts import (
    BOM_CSV_ENCODING as BOM_CSV_ENCODING,
    BOM_FIXED_COLUMNS as BOM_FIXED_COLUMNS,
    _BomDesign as _BomDesign,
    _bom_parameter_columns as _bom_parameter_columns,
    _bom_rows as _bom_rows,
    _write_bom_csv as _write_bom_csv,
    _write_named_rows_csv as _write_named_rows_csv,
    _bom_output_extension as _bom_output_extension,
    _write_bom_output as _write_bom_output,
    _configured_bom_artifacts as _configured_bom_artifacts,
    _write_configured_bom_artifact as _write_configured_bom_artifact,
    _entry_field as _entry_field,
    _pnp_entry_to_bom_dict as _pnp_entry_to_bom_dict,
    _bom_from_configured_source as _bom_from_configured_source,
    _generic_bom_payload as _generic_bom_payload,
    _write_bom_xlsx as _write_bom_xlsx,
    _legacy_bom_xlsx_row as _legacy_bom_xlsx_row,
)


def cmd_bom(args) -> int:
    """
    Handle bom subcommand - generate BOM from SchDoc/PrjPcb files.

    REQ-CLI-004: BOM generation with variant support (CSV or JSON format).

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
            log.info("Usage: altium-cruncher bom [file.SchDoc | project.PrjPcb]")
            return 1
        log.info(f"Auto-detected project: {input_file.name}")

    # Validate file type
    suffix = input_file.suffix.lower()
    if suffix == ".schdoc":
        design = AltiumDesign.from_schdoc(input_file)
    elif suffix == ".prjpcb":
        design = AltiumDesign.from_prjpcb(input_file)
    else:
        log.error(f"Unsupported file type: {suffix}")
        log.info("Supported types: .SchDoc, .PrjPcb")
        return 1

    # Show available variants
    available_variants = design.get_variants()
    if available_variants:
        log.info(f"Available variants: {', '.join(available_variants)}")
    else:
        log.info("No variants defined in project")

    requested_format_value = getattr(args, "format", None)
    requested_format = (
        requested_format_value if isinstance(requested_format_value, str) else None
    )
    if requested_format is None:
        config, config_path, created_config = load_or_create_bom_pnp_config(
            getattr(args, "config", None)
        )
        if created_config:
            log.info("Created BOM/PnP config template: %s", config_path)
        config_mode = True
    else:
        config, config_path = load_optional_bom_pnp_config(getattr(args, "config", None))
        config_mode = False
    variants_to_process = select_variant_names(
        available_variants,
        config,
        cli_variant=getattr(args, "variant", None),
        cli_all_variants=getattr(args, "all_variants", False),
    )
    warn_for_unknown_variants(log, variants_to_process, available_variants)

    project_parameters = project_parameters_from_design(design)
    output_dir = (
        configured_output_root(args.output)
        if config_mode
        else _resolve_output_dir(args.output, "bom")
    )

    files_written = 0
    for var in variants_to_process:
        bom = _bom_from_configured_source(design, config, variant=var)

        if config_mode:
            written = _configured_bom_artifacts(
                output_dir,
                bom,
                config=config,
                source=input_file,
                variant=var,
                project_parameters=project_parameters,
            )
            files_written += len(written)
            output_names = ", ".join(path.name for path in written)
        else:
            assert requested_format is not None
            base_name = input_file.stem
            ext = _bom_output_extension(requested_format)
            if var:
                output_file = output_dir / f"{base_name}_{var}_bom.{ext}"
            else:
                output_file = output_dir / f"{base_name}_bom.{ext}"

            _write_bom_output(
                output_file,
                bom,
                output_format=requested_format,
                source=input_file,
                variant=var,
            )
            files_written += 1
            output_names = output_file.name

        variant_name = var or "base"
        log.info("BOM (%s): %s components -> %s", variant_name, len(bom), output_names)

        # Count DNP components
        dnp_count = sum(1 for c in bom if c["dnp"])
        if dnp_count > 0:
            log.info(f"  DNP (Do Not Populate): {dnp_count}")

    log.info(f"Generated {files_written} BOM file(s) in {output_dir}")
    return 0


def register_parser(subparsers):
    # bom subcommand - Generate BOM from SchDoc/PrjPcb
    bom_parser = subparsers.add_parser(
        "bom",
        help="generate BOM from Altium schematic documents (CSV, JSON, or XLSX)",
        description="Generate Bill of Materials (BOM) from Altium SchDoc or PrjPcb files. "
        "CSV/XLSX formats include parameters as columns; JSON preserves nested structure. "
        "Config-driven runs can emit raw JSON, grouped tables, and JLCPCB BOM "
        "upload columns in one invocation.",
        epilog="Examples:\n"
        "  altium-cruncher bom project.PrjPcb\n"
        "  altium-cruncher bom schematic.SchDoc\n"
        "  altium-cruncher bom                               # Auto-detect PrjPcb in CWD\n"
        "  altium-cruncher bom project.PrjPcb --variant V1   # Single variant\n"
        "  altium-cruncher bom project.PrjPcb --all-variants # All variants\n"
        "  altium-cruncher bom project.PrjPcb --format json  # JSON output\n"
        "  altium-cruncher bom project.PrjPcb --format generic-json\n"
        "  altium-cruncher bom project.PrjPcb --format grouped-json\n"
        "  altium-cruncher bom project.PrjPcb --format jlc-csv\n"
        "  altium-cruncher bom project.PrjPcb --format jlc-xlsx\n"
        "  altium-cruncher bom project.PrjPcb --format xlsx  # XLSX output\n"
        "  altium-cruncher bom --write-config bom.config\n"
        "  altium-cruncher bom project.PrjPcb --config bom.config\n"
        "  altium-cruncher bom project.PrjPcb -o output_dir/",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    bom_parser.add_argument(
        "file", nargs="?", help="SchDoc or PrjPcb file (optional if PrjPcb in CWD)"
    )
    bom_parser.add_argument(
        "-o", "--output", type=Path, help="output directory (default: ./output/bom)"
    )
    bom_parser.add_argument(
        "--format",
        choices=[
            "csv",
            "json",
            "raw-json",
            "generic-json",
            "legacy-json",
            "grouped-json",
            "grouped-csv",
            "grouped-xlsx",
            "jlc-csv",
            "jlc-xlsx",
            "xlsx",
        ],
        default=None,
        help="single output format; overrides multi-output config mode",
    )
    bom_parser.add_argument(
        "--config",
        type=Path,
        help=(
            "BOM/PnP JSON/JSONC config "
            "(default: ./bom.config; created when omitted in config mode)"
        ),
    )
    bom_parser.add_argument(
        "--write-config",
        nargs="?",
        const=Path(BOM_PNP_DEFAULT_CONFIG_NAME),
        type=Path,
        metavar="PATH",
        help="write a default BOM/PnP config template",
    )
    bom_parser.add_argument(
        "--variant", type=str, help="filter by specific variant name"
    )
    bom_parser.add_argument(
        "--all-variants",
        action="store_true",
        help="generate BOM for all variants (plus base)",
    )
    bom_parser.set_defaults(handler=cmd_bom)
    return bom_parser
