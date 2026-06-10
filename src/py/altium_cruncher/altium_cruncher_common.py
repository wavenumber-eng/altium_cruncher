"""Shared file-level helpers for altium-cruncher command modules."""

from __future__ import annotations

import logging
from pathlib import Path


def find_prjpcb_in_cwd() -> Path | None:
    """
    Scan current working directory for a .PrjPcb file.

    Returns:
        Path to PrjPcb file if exactly one found, None otherwise.
    """
    prjpcb_files = list(Path.cwd().glob("*.PrjPcb"))
    if len(prjpcb_files) == 1:
        return prjpcb_files[0]
    return None


def find_prjpcbs_in_cwd() -> list[Path]:
    """Find all .PrjPcb files in current working directory (stable order)."""
    return sorted(
        [
            p
            for p in Path.cwd().iterdir()
            if p.is_file() and p.suffix.lower() == ".prjpcb"
        ],
        key=lambda p: p.name.lower(),
    )


def find_pcbdocs_in_cwd() -> list[Path]:
    """Find all .PcbDoc files in current working directory (stable order)."""
    return sorted(
        [
            p
            for p in Path.cwd().iterdir()
            if p.is_file() and p.suffix.lower() == ".pcbdoc"
        ],
        key=lambda p: p.name.lower(),
    )


def sanitize_sheet_number_parameters(design: object) -> list[tuple[str, str]]:
    """
    Clear non-numeric SheetNumber document parameters on loaded SchDocs.

    altium-monkey<=2026.6.9 AltiumDesign.to_json() raises ValueError when a
    sheet's SheetNumber document parameter is not an integer (e.g. a part
    number typed into the title block). Clearing the in-memory value makes
    sheet numbering fall back to document order, matching the behavior for
    sheets with no SheetNumber parameter. Files on disk are not modified.

    Args:
        design: AltiumDesign instance with loaded schdocs.

    Returns:
        List of (schdoc filename, offending value) pairs that were cleared.
    """
    cleared: list[tuple[str, str]] = []
    for index, schdoc in enumerate(getattr(design, "schdocs", []) or []):
        filepath = getattr(schdoc, "filepath", None)
        sheet_name = filepath.name if filepath else f"sheet{index}"
        for parameter in getattr(schdoc, "parameters", []) or []:
            if getattr(parameter, "name", "") != "SheetNumber":
                continue
            value = getattr(parameter, "text", "")
            if not value or value == "*":
                continue
            try:
                int(value)
            except ValueError:
                parameter.text = ""
                cleared.append((sheet_name, value))
    return cleared


def warn_non_numeric_sheet_numbers(log: logging.Logger, design: object) -> None:
    """Sanitize SheetNumber parameters and warn for each cleared sheet."""
    for sheet_name, value in sanitize_sheet_number_parameters(design):
        log.warning(
            "Sheet %s has non-numeric SheetNumber %r; using document order instead",
            sheet_name,
            value,
        )


def _default_output_dir(command_name: str) -> Path:
    """Return default output root for a command."""
    return (Path.cwd() / "output" / command_name).resolve()


def _resolve_output_dir(output_arg: Path | None, command_name: str) -> Path:
    """Resolve explicit output directory or command default and create it."""
    output_dir = (
        output_arg.resolve() if output_arg else _default_output_dir(command_name)
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir
