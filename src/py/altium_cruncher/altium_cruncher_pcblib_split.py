"""PcbLib split helpers for altium_cruncher commands."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from altium_cruncher.output_path_templates import sanitize_output_name

log = logging.getLogger(__name__)


def split_pcblib_filesystem_safe(
    pcblib: Any,
    output_dir: Path,
    *,
    verbose: bool = False,
    debug: bool = False,
) -> dict[str, Path]:
    """Split a PcbLib using filenames that are safe on Windows filesystems."""
    from altium_monkey.altium_pcb_embedded_model_compose import (
        collect_pcblib_embedded_model_entries,
        copy_footprint_with_models_into_builder,
    )
    from altium_monkey.altium_pcblib_builder import PcbLibBuilder

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    footprints = list(getattr(pcblib, "footprints", []) or [])
    if verbose:
        log.info(f"Splitting PcbLib with {len(footprints)} footprints")

    results: dict[str, Path] = {}
    used_output_stems: set[str] = set()
    model_entries = collect_pcblib_embedded_model_entries(
        getattr(pcblib, "raw_models_data", None),
        getattr(pcblib, "raw_models", {}),
    )

    for footprint in footprints:
        footprint_name = str(getattr(footprint, "name", "") or "footprint")
        output_stem = _unique_output_stem(
            sanitize_output_name(footprint_name),
            used_output_stems,
        )
        output_path = output_dir / f"{output_stem}.PcbLib"

        builder = PcbLibBuilder()
        parameters = getattr(footprint, "parameters", {}) or {}
        copy_footprint_with_models_into_builder(
            builder,
            footprint,
            model_entries,
            height=parameters.get("HEIGHT", "0mil"),
            description=parameters.get("DESCRIPTION", ""),
            item_guid=parameters.get("ITEMGUID", ""),
            revision_guid=parameters.get("REVISIONGUID", ""),
            seen_model_signatures=set(),
        )
        builder.build().save(output_path, debug=debug)
        results[footprint_name] = output_path

        if verbose:
            record_order = getattr(footprint, "_record_order", None)
            total = len(record_order) if record_order else 0
            log.info(f"  Wrote {output_path.name} ({total} primitives)")

    if verbose:
        log.info(f"Split {len(results)} footprints into {output_dir}")

    return results


def _unique_output_stem(candidate: str, existing_stems: set[str]) -> str:
    """Return a unique output stem on a case-insensitive filesystem basis."""
    candidate_lower = candidate.lower()
    if candidate_lower not in existing_stems:
        existing_stems.add(candidate_lower)
        return candidate

    suffix = 2
    while True:
        alternate = f"{candidate}_{suffix}"
        alternate_lower = alternate.lower()
        if alternate_lower not in existing_stems:
            existing_stems.add(alternate_lower)
            return alternate
        suffix += 1
