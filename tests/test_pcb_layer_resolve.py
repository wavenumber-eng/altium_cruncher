from __future__ import annotations

import pytest

from altium_monkey.altium_record_types import PcbLayer

from altium_cruncher.altium_cruncher_pcb_layer_resolve import (
    canonical_pcb_layer_token,
    legacy_pcb_layer_or_none,
    pcb_layer_ref_is_copper,
    pcb_layer_ref_sort_key,
    resolve_pcb_layer_ref,
    resolve_pcb_layer_ref_or_none,
)


def test_resolve_pcb_layer_ref_accepts_legacy_and_v7_forms() -> None:
    assert resolve_pcb_layer_ref(PcbLayer.TOP).legacy_layer == PcbLayer.TOP
    assert resolve_pcb_layer_ref("TOP").legacy_layer == PcbLayer.TOP
    assert resolve_pcb_layer_ref(1).legacy_layer == PcbLayer.TOP
    assert resolve_pcb_layer_ref("MECHANICAL_16").legacy_layer == PcbLayer.MECHANICAL_16

    mech17 = resolve_pcb_layer_ref("Mechanical 17")
    assert mech17.token == "MECHANICAL17"
    assert mech17.legacy_layer is None
    assert mech17.v7_saved_layer_id == 0x01020011

    mid31 = resolve_pcb_layer_ref("mid_31")
    assert mid31.token == "MID31"
    assert mid31.legacy_layer is None
    assert mid31.v7_saved_layer_id == 0x01000020


def test_resolve_pcb_layer_ref_rejects_unknown_values() -> None:
    with pytest.raises(ValueError, match="Unknown PCB layer"):
        resolve_pcb_layer_ref("not-a-layer")
    assert resolve_pcb_layer_ref_or_none("not-a-layer") is None
    assert resolve_pcb_layer_ref_or_none(None) is None


def test_legacy_layer_and_token_helpers_classify_v7_layers() -> None:
    assert legacy_pcb_layer_or_none("BOTTOM") == PcbLayer.BOTTOM
    assert legacy_pcb_layer_or_none("MECHANICAL17") is None
    assert legacy_pcb_layer_or_none("garbage") is None
    assert canonical_pcb_layer_token("Mechanical 17") == "MECHANICAL17"
    assert canonical_pcb_layer_token(PcbLayer.TOP_OVERLAY) == "TOPOVERLAY"
    with pytest.raises(ValueError, match="Unknown PCB layer"):
        canonical_pcb_layer_token("garbage")


def test_copper_classification_covers_v7_mid_layers() -> None:
    assert pcb_layer_ref_is_copper(resolve_pcb_layer_ref("TOP"))
    assert pcb_layer_ref_is_copper(resolve_pcb_layer_ref("MID31"))
    assert pcb_layer_ref_is_copper(resolve_pcb_layer_ref("PLANE1"))
    assert not pcb_layer_ref_is_copper(resolve_pcb_layer_ref("MECHANICAL17"))
    assert not pcb_layer_ref_is_copper(resolve_pcb_layer_ref("TOPOVERLAY"))


def test_sort_key_orders_legacy_before_v7_only_layers() -> None:
    refs = [
        resolve_pcb_layer_ref("MID31"),
        resolve_pcb_layer_ref("MECHANICAL17"),
        resolve_pcb_layer_ref("BOTTOM"),
        resolve_pcb_layer_ref("TOP"),
    ]
    ordered = sorted(refs, key=pcb_layer_ref_sort_key)
    assert [ref.token for ref in ordered] == ["TOP", "BOTTOM", "MID31", "MECHANICAL17"]
