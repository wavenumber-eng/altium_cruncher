"""Shared CLI helpers for BOM/PnP-style commands."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import json
import logging
from pathlib import Path

from altium_cruncher.bom_pnp_model import (
    BOM_PNP_DEFAULT_CONFIG_NAME,
    BomPnpConfig,
    find_bom_pnp_config_path,
    load_bom_pnp_config,
    write_bom_pnp_config,
)
from altium_cruncher.output_path_templates import TemplateValue


def project_parameters_from_design(design: object) -> dict[str, TemplateValue]:
    """Return project parameters for output templates."""
    project = getattr(design, "project", None)
    parameters = getattr(project, "parameters", {}) if project is not None else {}
    if not isinstance(parameters, Mapping):
        return {}
    return {str(name): value for name, value in parameters.items()}


def configured_output_root(output_arg: Path | None) -> Path:
    """Resolve the root used by config-driven output templates."""
    output_root = output_arg.resolve() if output_arg else (Path.cwd() / "output")
    output_root.mkdir(parents=True, exist_ok=True)
    return output_root


def load_optional_bom_pnp_config(
    config_arg: Path | None,
) -> tuple[BomPnpConfig, Path | None]:
    """Load explicit or default BOM/PnP config, if present."""
    config_path = config_arg.resolve() if config_arg else find_bom_pnp_config_path()
    if config_path is None:
        return BomPnpConfig(), None
    return load_bom_pnp_config(config_path), config_path


def write_config_template(write_arg: Path | None) -> Path:
    """Write a default BOM/PnP config template and return its path."""
    path = (write_arg or Path(BOM_PNP_DEFAULT_CONFIG_NAME)).resolve()
    write_bom_pnp_config(path)
    return path


def write_used_config_snapshot(output_file: Path, config: BomPnpConfig) -> Path:
    """Write the effective BOM/PnP config beside one generated artifact."""
    config_path = output_file.parent / "bom.config.used.json"
    config_path.write_text(
        json.dumps(config.to_json_obj(), indent=2) + "\n",
        encoding="utf-8",
    )
    return config_path


def warn_for_unknown_variants(
    logger: logging.Logger,
    variants: Sequence[str | None],
    available_variants: Sequence[str],
) -> None:
    """Log warnings for requested variants not reported by the design."""
    available = set(available_variants)
    for variant in variants:
        if variant is not None and variant not in available:
            logger.warning(
                "Variant '%s' not found in project (available: %s)",
                variant,
                ", ".join(available_variants) or "none",
            )
