"""Shared V7-aware PCB layer resolution.

altium-monkey 2026.8.1 introduced ``PcbLayerRef`` for the V7 layer space
(Mechanical17-53, Mid31-126) alongside the legacy ``PcbLayer`` enum. All
altium_cruncher layer-name parsing routes through these helpers so V7
tokens resolve consistently everywhere. ``PcbLayerRef.token`` equals the
legacy ``PcbLayer.to_json_name()`` string for every legacy layer, so
tokens produced here are a strict superset of the legacy names.
"""

from __future__ import annotations

from altium_monkey.altium_pcb_layer_ref import (
    PcbLayerFamily,
    PcbLayerRef,
    PcbLayerResolutionError,
    coerce_pcb_layer_ref,
)
from altium_monkey.altium_record_types import PcbLayer


def resolve_pcb_layer_ref(value: object) -> PcbLayerRef:
    """Resolve a layer value to a ``PcbLayerRef``.

    Accepts ``PcbLayerRef``, ``PcbLayer``, legacy int layer ids, legacy
    JSON names, legacy enum member names, and V7 tokens (any case,
    ``_``/space separated). Raises ``ValueError`` for unknown values.
    """
    try:
        return coerce_pcb_layer_ref(value)
    except PcbLayerResolutionError as exc:
        raise ValueError(f"Unknown PCB layer: {value!r}") from exc


def resolve_pcb_layer_ref_or_none(value: object) -> PcbLayerRef | None:
    """Like :func:`resolve_pcb_layer_ref` but returns ``None`` on failure."""
    if value is None:
        return None
    try:
        return resolve_pcb_layer_ref(value)
    except (ValueError, TypeError):
        return None


def legacy_pcb_layer_or_none(value: object) -> PcbLayer | None:
    """Resolve to the legacy ``PcbLayer`` enum, or ``None`` when the value
    is unknown or names a V7-only layer with no legacy equivalent."""
    ref = resolve_pcb_layer_ref_or_none(value)
    return None if ref is None else ref.legacy_layer


def canonical_pcb_layer_token(value: object) -> str:
    """Resolve to the canonical layer token (legacy JSON name or V7 token).

    Raises ``ValueError`` for unknown values.
    """
    return resolve_pcb_layer_ref(value).token


def pcb_layer_ref_is_copper(ref: PcbLayerRef) -> bool:
    """True for signal and internal-plane layers, including V7 mids."""
    return ref.family in {PcbLayerFamily.SIGNAL, PcbLayerFamily.INTERNAL_PLANE}


def pcb_layer_ref_sort_key(ref: PcbLayerRef) -> tuple[int, int, str]:
    """Deterministic ordering: legacy layers by legacy id first, then
    V7-only layers by saved id."""
    if ref.legacy_layer_id is not None:
        return (0, int(ref.legacy_layer_id), ref.token)
    saved_id = ref.v7_saved_layer_id or ref.runtime_v7_layer_id or 0
    return (1, int(saved_id), ref.token)
