"""Behavior tests for the impedance-doc command."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import jsonc  # type: ignore[import-untyped]
from jsonschema import Draft202012Validator

from altium_monkey import PcbLayer

from altium_cruncher.altium_cruncher_impedance_doc import (
    CONFIG_SCHEMA,
    ImpedanceClass,
    apply_config,
    compose_page_svg,
    diff_pair_impedance,
    group_by_impedance,
    recolor_layer_svg,
    render_config_jsonc,
    single_ended_impedance,
)

CONTRACT = (
    Path(__file__).resolve().parents[1]
    / "docs" / "contracts" / "impedance_doc.config.a0.schema.json"
)


def _rule(**kw: object) -> SimpleNamespace:
    base = {
        "rule_kind": "",
        "scope1_expression": "",
        "impedance_profile_value": "",
        "minimum": "",
        "maximum": "",
        "minimum_impedance": "",
        "maximum_impedance": "",
        "favorite_impedance": "",
        "impedance_profile_driven": None,
    }
    base.update(kw)
    return SimpleNamespace(**base)


def _pcb(*rules: SimpleNamespace) -> SimpleNamespace:
    return SimpleNamespace(rules=list(rules))


# --- impedance extraction -------------------------------------------------- #

def test_diff_pair_impedance_from_routing_rule() -> None:
    pcb = _pcb(_rule(
        rule_kind="DiffPairsRouting",
        scope1_expression="InDifferentialPairClass('USB3')",
        impedance_profile_value="90",
    ))
    assert diff_pair_impedance(pcb, "USB3") == "90 ohm"


def test_diff_pair_impedance_ignores_other_classes() -> None:
    pcb = _pcb(_rule(
        rule_kind="DiffPairsRouting",
        scope1_expression="InDifferentialPairClass('OTHER')",
        impedance_profile_value="100",
    ))
    assert diff_pair_impedance(pcb, "USB3") is None


def test_single_ended_plain_width_rule_is_not_controlled_impedance() -> None:
    # A width constraint with no impedance data must not be documented.
    pcb = _pcb(_rule(rule_kind="Width", scope1_expression="InNetClass('BANK_33')"))
    assert single_ended_impedance(pcb, "BANK_33") is None


def test_single_ended_explicit_rule_impedance_wins_over_name_digits() -> None:
    # Name carries a non-impedance number (lane count) but the rule is explicit.
    pcb = _pcb(_rule(
        rule_kind="Width",
        scope1_expression="InNetClass('LANE12_SE')",
        impedance_profile_value="50",
    ))
    assert single_ended_impedance(pcb, "LANE12_SE") == "50 ohm"


def test_single_ended_name_encoded_impedance_used_when_rule_default() -> None:
    # Only a favorite (default) impedance present -> name SE_35 takes precedence.
    pcb = _pcb(_rule(
        rule_kind="Width",
        scope1_expression="InNetClass('SE_35')",
        favorite_impedance="50",
    ))
    assert single_ended_impedance(pcb, "SE_35") == "35 ohm"


# --- grouping + config round-trip ------------------------------------------ #

def _classes() -> list[ImpedanceClass]:
    top = PcbLayer(1)
    return [
        ImpedanceClass("USB3", "differential", "85 ohm", ("USB_P", "USB_N"), (top,)),
        ImpedanceClass("SE_50", "single-ended", "50 ohm", ("CLK",), (top,)),
    ]


def test_group_by_impedance_sorts_and_colors() -> None:
    groups = group_by_impedance(_classes())
    assert [g.impedance for g in groups] == ["50 ohm", "85 ohm"]
    assert all(g.color for g in groups)
    assert groups[1].kind == "differential"
    assert groups[0].kind == "single-ended"


def test_config_round_trip_overrides_title_and_color() -> None:
    groups = group_by_impedance(_classes())
    text = render_config_jsonc("board.PcbDoc", groups)
    cfg = jsonc.loads(text)
    assert cfg["schema"] == CONFIG_SCHEMA
    # Hand-edit: rename + recolor the 85 ohm group.
    for entry in cfg["groups"]:
        if entry["impedance"] == "85 ohm":
            entry["title"] = "USB 3.0 (85 ohm diff)"
            entry["color"] = "#FF8800"
    fresh = group_by_impedance(_classes())
    apply_config(fresh, cfg)
    g85 = next(g for g in fresh if g.impedance == "85 ohm")
    assert g85.title == "USB 3.0 (85 ohm diff)"
    assert g85.color == "#FF8800"


def test_generated_config_validates_against_contract() -> None:
    groups = group_by_impedance(_classes())
    payload = jsonc.loads(render_config_jsonc("board.PcbDoc", groups))
    validator = Draft202012Validator(json.loads(CONTRACT.read_text(encoding="utf-8")))
    errors = sorted(validator.iter_errors(payload), key=str)
    assert errors == [], [e.message for e in errors]


# --- compose + recolor ----------------------------------------------------- #

_LAYER_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 80" '
    'width="100" height="80">\n'
    '<path data-primitive="track" data-net="USB_P" stroke="#000000" '
    'fill="none"/>\n'
    '<path data-primitive="track" data-net="GND" stroke="#000000" fill="none"/>\n'
    '</svg>'
)


def test_recolor_highlights_impedance_net_and_greys_context() -> None:
    colored = recolor_layer_svg(_LAYER_SVG, {"USB_P": "#FF8800"}, {
        "context_copper": "#B8B8B8", "pad_via": "#000000", "drill_knockout": "#FFFFFF",
    })
    lines = colored.splitlines()
    usb = next(line for line in lines if 'data-net="USB_P"' in line)
    gnd = next(line for line in lines if 'data-net="GND"' in line)
    assert 'stroke="#FF8800"' in usb
    assert 'stroke="#B8B8B8"' in gnd  # context net dropped to grey


def test_compose_page_emits_legend_with_impedance_and_kind() -> None:
    groups = group_by_impedance(_classes())
    style = {
        "context_copper": "#B8B8B8", "pad_via": "#000000", "board_outline": "#000000",
        "drill_knockout": "#FFFFFF", "background": "#FFFFFF",
        "font_family": "Arial, sans-serif", "company": "", "watermark": "",
        "logo_path": "", "logo_width_px": 120,
    }
    page = compose_page_svg(
        _LAYER_SVG, layer_name="Top Layer", groups=groups, present={"USB_P"},
        style=style, page_title="Board - controlled-impedance routing",
    )
    assert "Controlled-impedance" in page
    assert "85 ohm  (differential)" in page
    assert "(not on this layer)" in page  # 50 ohm group has no present nets
    assert 'data-acr-layer="Top Layer"' in page
    assert page.count("<svg") == 2  # outer page + nested board
