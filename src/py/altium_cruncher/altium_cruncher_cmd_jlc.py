"""JLCPCB manufacturing bundle command for altium_cruncher."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from altium_monkey.altium_pnp_position import (
    PNP_POSITION_MODES,
    normalize_pnp_position_mode,
)

from altium_cruncher.altium_cruncher_cmd_bom import (
    _bom_from_configured_source,
    _configured_bom_artifacts,
)
from altium_cruncher.altium_cruncher_cmd_pnp import (
    _configured_pnp_artifacts,
    _pnp_format_option_error,
)
from altium_cruncher.altium_cruncher_common import find_prjpcb_in_cwd
from altium_cruncher.bom_pnp_cli_common import (
    configured_output_root,
    load_optional_bom_pnp_config,
    project_parameters_from_design,
    warn_for_unknown_variants,
    write_config_template,
)
from altium_cruncher.bom_pnp_model import (
    BOM_PNP_DEFAULT_CONFIG_NAME,
    BomPnpConfig,
    select_variant_names,
)

log = logging.getLogger(__name__)


def _position_mode_arg(args: argparse.Namespace, config: BomPnpConfig) -> str:
    """Return the effective PnP position mode for JLC CPL output."""
    return normalize_pnp_position_mode(
        getattr(args, "position_mode", None) or config.pnp_position_mode
    )


def cmd_jlc(args: argparse.Namespace) -> int:
    """Generate JLCPCB BOM and CPL files from one project input."""
    from altium_monkey.altium_design import AltiumDesign

    write_config = getattr(args, "write_config", None)
    if write_config is not None:
        config_path = write_config_template(write_config)
        log.info("Wrote BOM/PnP config template: %s", config_path)
        if not getattr(args, "file", None):
            return 0

    input_file = _resolve_input_file(args.file)
    if input_file is None:
        return 1

    design = AltiumDesign.from_prjpcb(input_file)
    available_variants = design.get_variants()
    if available_variants:
        log.info("Available variants: %s", ", ".join(available_variants))
    else:
        log.info("No variants defined in project")

    config, _config_path = load_optional_bom_pnp_config(getattr(args, "config", None))
    units = getattr(args, "units", None) or config.pnp_units
    position_mode = _position_mode_arg(args, config)
    option_error = _pnp_format_option_error("jlc-cpl-xlsx", units)
    if option_error:
        log.error(option_error)
        return 1

    variants_to_process = select_variant_names(
        available_variants,
        config,
        cli_variant=getattr(args, "variant", None),
        cli_all_variants=getattr(args, "all_variants", False),
    )
    warn_for_unknown_variants(log, variants_to_process, available_variants)

    output_root = configured_output_root(args.output)
    project_parameters = project_parameters_from_design(design)
    exclude_no_bom = (
        getattr(args, "exclude_no_bom", False) or config.pnp_exclude_no_bom
    )

    files_written = 0
    for variant in variants_to_process:
        bom = _bom_from_configured_source(design, config, variant=variant)
        pnp = design.to_pnp(
            variant=variant,
            units=units,
            position_mode=position_mode,
            exclude_no_bom=exclude_no_bom,
        )
        bom_files = _configured_bom_artifacts(
            output_root,
            bom,
            config=config,
            source=input_file,
            variant=variant,
            project_parameters=project_parameters,
            output_kinds=("jlc-xlsx",),
            command="jlc",
        )
        pnp_files = _configured_pnp_artifacts(
            output_root,
            pnp,
            config=config,
            source=input_file,
            variant=variant,
            units=units,
            position_mode=position_mode,
            project_parameters=project_parameters,
            output_kinds=("jlc-cpl-xlsx",),
            command="jlc",
        )
        written = [*bom_files, *pnp_files]
        files_written += len(written)
        log.info(
            "JLC (%s): %s",
            variant or "base",
            ", ".join(path.name for path in written),
        )

    log.info("Generated %s JLC file(s) in %s", files_written, output_root)
    return 0


def _resolve_input_file(file_arg: str | None) -> Path | None:
    """Resolve an explicit or auto-detected project input."""
    if file_arg:
        input_file = Path(file_arg).resolve()
        if not input_file.exists():
            log.error("File not found: %s", input_file)
            return None
    else:
        input_file = find_prjpcb_in_cwd()
        if input_file is None:
            log.error("No file specified and no .PrjPcb found in current directory")
            log.info("Usage: altium-cruncher jlc [project.PrjPcb]")
            return None
        log.info("Auto-detected project: %s", input_file.name)

    if input_file.suffix.lower() != ".prjpcb":
        log.error("JLC output requires a .PrjPcb file, got: %s", input_file.suffix)
        return None
    return input_file


def register_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Register the jlc subcommand."""
    parser = subparsers.add_parser(
        "jlc",
        help="generate JLCPCB BOM and CPL outputs from an Altium project",
        description="Generate a JLCPCB BOM XLSX and CPL XLSX from one PrjPcb. "
        "The command reuses the BOM/PnP config for aliases, sorting, variants, "
        "and output naming.",
        epilog="Examples:\n"
        "  altium-cruncher jlc project.PrjPcb\n"
        "  altium-cruncher jlc project.PrjPcb --variant B4\n"
        "  altium-cruncher jlc project.PrjPcb --all-variants\n"
        "  altium-cruncher jlc project.PrjPcb --position-mode component-origin\n"
        "  altium-cruncher jlc project.PrjPcb --config bom.config\n"
        "  altium-cruncher jlc --write-config bom.config",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="PrjPcb file (optional if PrjPcb in CWD)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output root directory (default: ./output)",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="BOM/PnP JSON/JSONC config (default: ./bom.config if present)",
    )
    parser.add_argument(
        "--write-config",
        nargs="?",
        const=Path(BOM_PNP_DEFAULT_CONFIG_NAME),
        type=Path,
        metavar="PATH",
        help="write a default BOM/PnP config template",
    )
    parser.add_argument("--variant", type=str, help="filter by specific variant name")
    parser.add_argument(
        "--all-variants",
        action="store_true",
        help="generate outputs for all variants plus base",
    )
    parser.add_argument(
        "--units",
        choices=["mm", "mils"],
        default=None,
        help="coordinate units (JLC CPL requires mm)",
    )
    parser.add_argument(
        "--position-mode",
        choices=list(PNP_POSITION_MODES),
        default=None,
        help="placement position mode (default: config value or altium-pick-place)",
    )
    parser.add_argument(
        "--exclude-no-bom",
        action="store_true",
        help="exclude STANDARD_NO_BOM components from CPL generation",
    )
    parser.set_defaults(handler=cmd_jlc)
    return parser
