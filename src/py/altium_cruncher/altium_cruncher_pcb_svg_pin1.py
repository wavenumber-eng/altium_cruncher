"""Pin-1 pad selection helpers for PCB SVG virtual layers."""

from __future__ import annotations

import re

_GRID_PAD_RE = re.compile(r"^([A-Za-z]+)(\d+)$")


def grid_row_index(row: str) -> int:
    """Convert a BGA/LGA row label such as A, B, or AA into a sortable index."""
    value = 0
    for char in row.strip().upper():
        if not ("A" <= char <= "Z"):
            return 10**9
        value = value * 26 + (ord(char) - ord("A") + 1)
    return value


def is_grid_pad_designator(designator: str) -> bool:
    """Return true when a pad designator uses BGA/LGA letter-number syntax."""
    return _GRID_PAD_RE.match(designator.strip()) is not None


def choose_pin1_pad_designator(
    pad_designators: list[str] | tuple[str, ...],
    *,
    override: str | None = None,
) -> str | None:
    """Choose a pin-1 pad name from component-owned pad designators.

    Selection order is explicit override, numeric ``1``, ``A1``, then BGA/LGA
    style letter-number pads sorted by numeric column first and row second.
    """
    original_by_upper = {
        designator.strip().upper(): designator.strip()
        for designator in pad_designators
        if designator.strip()
    }
    if override:
        overridden = original_by_upper.get(override.strip().upper())
        if overridden is not None:
            return overridden

    for preferred in ("1", "A1"):
        if preferred in original_by_upper:
            return original_by_upper[preferred]

    grid_candidates: list[tuple[int, int, str, str]] = []
    for normalized, original in original_by_upper.items():
        match = _GRID_PAD_RE.match(normalized)
        if match is None:
            continue
        row, column_text = match.groups()
        grid_candidates.append((int(column_text), grid_row_index(row), normalized, original))
    if not grid_candidates:
        return None
    return min(grid_candidates)[3]


__all__ = ["choose_pin1_pad_designator", "grid_row_index", "is_grid_pad_designator"]
