"""PCB routing-context projection tests."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

from jsonschema import Draft202012Validator

from altium_monkey import (
    AltiumPcbDifferentialPair,
    AltiumPcbDoc,
    AltiumPcbNet,
    AltiumPcbNetClass,
    PcbNetClassKind,
)
from altium_monkey.altium_pcb_rule import AltiumPcbRule
from altium_cruncher.altium_cruncher_pcb_routing_context import (
    PCB_ROUTING_CONTEXT_SCHEMA,
    build_pcb_routing_context_payload,
)


ROOT = Path(__file__).resolve().parents[1]


def _validate(payload: object) -> None:
    schema = json.loads(
        (ROOT / "docs/contracts/pcb_routing_context.a0.schema.json").read_text(
            encoding="utf-8"
        )
    )
    Draft202012Validator(schema).validate(payload)


def _net(name: str, unique_id: str) -> AltiumPcbNet:
    return AltiumPcbNet(name=name, unique_id=unique_id)


def _class(
    name: str,
    kind: PcbNetClassKind,
    members: list[str],
    *,
    enabled: bool = True,
) -> AltiumPcbNetClass:
    return AltiumPcbNetClass(
        name=name,
        kind=kind,
        member_count=len(members),
        members=members,
        enabled=enabled,
        unique_id=f"CLASS-{name}",
    )


def test_routing_context_projects_authored_classes_pairs_and_rules() -> None:
    nets = [
        _net("USB_D_P", "NET-P"),
        _net("usb_d_n", "NET-N"),
        _net("CLOCK_A", "NET-A"),
        _net("CLOCK_B", "NET-B"),
    ]
    pairs = [
        AltiumPcbDifferentialPair.create(
            name="USB_D",
            positive_net_name="USB_D_P",
            negative_net_name="USB_D_N",
        ),
        AltiumPcbDifferentialPair.create(
            name="CLOCK_LINK",
            positive_net_name="CLOCK_A",
            negative_net_name="CLOCK_B",
        ),
        AltiumPcbDifferentialPair.create(
            name="SECOND_REFERENCE",
            positive_net_name="USB_D_P",
            negative_net_name="CLOCK_B",
        ),
    ]
    classes = [
        _class("USB", PcbNetClassKind.NET, ["USB_D_P", "USB_D_N"]),
        _class(
            "Serial Pairs",
            PcbNetClassKind.DIFF_PAIR,
            ["USB_D", "CLOCK_LINK"],
        ),
        _class("Not a net class", PcbNetClassKind.COMPONENT, ["U1"]),
    ]
    rule = AltiumPcbRule.from_record(
        {
            "RULEKIND": "DiffPairsRouting",
            "NAME": "USB pair routing",
            "ENABLED": "TRUE",
            "PRIORITY": "1",
            "SCOPE1EXPRESSION": (
                "InDifferentialPairClass('Serial Pairs') And OnLayer('Top Layer')"
            ),
            "SCOPE2EXPRESSION": "All",
            "NETSCOPE": "DifferentNets",
            "LAYERKIND": "SameLayer",
            "IMPEDANCEPROFILEDRIVEN": "FALSE",
            "TOPLAYER_MINWIDTH": "4mil",
            "TOPLAYER_PREFWIDTH": "5mil",
            "TOPLAYER_MAXWIDTH": "6mil",
            "FUTUREFIELD": "preserve-me",
        },
        index=7,
    )
    unknown_enabled_rule = AltiumPcbRule.from_record(
        {
            "RULEKIND": "FutureRule",
            "NAME": "Future semantics",
            "SCOPE1EXPRESSION": "All",
            "SCOPE2EXPRESSION": "All",
            "FUTURELIMIT": "11mil",
        },
        index=8,
    )
    pcbdoc = SimpleNamespace(
        nets=nets,
        net_classes=classes,
        differential_pairs=pairs,
        rules=[rule, unknown_enabled_rule],
    )

    payload = build_pcb_routing_context_payload(
        pcbdoc,
        source="boards/controller.PcbDoc",
        board="controller",
    )

    _validate(payload)
    assert payload["schema"] == PCB_ROUTING_CONTEXT_SCHEMA
    assert payload["evidence"] == {
        "authored_rules": "included",
        "class_membership": "stored_members_only",
        "rule_applicability": "not_evaluated_by_cruncher",
        "drc_run_by_cruncher": False,
        "drc_violations": "not_included",
    }
    assert payload["summary"] == {
        "net_count": 4,
        "net_class_count": 1,
        "differential_pair_count": 3,
        "differential_pair_class_count": 1,
        "rule_count": 2,
        "enabled_rule_count": 1,
        "rules_by_kind": {"DiffPairsRouting": 1, "FutureRule": 1},
    }
    assert [row["name"] for row in payload["net_classes"]] == ["USB"]
    assert payload["net_classes"][0]["resolved_nets"] == ["USB_D_P", "usb_d_n"]
    assert [row["name"] for row in payload["differential_pair_classes"]] == [
        "Serial Pairs"
    ]
    assert payload["differential_pair_classes"][0]["resolved_nets"] == [
        "USB_D_P",
        "usb_d_n",
        "CLOCK_A",
        "CLOCK_B",
    ]

    usb_p = payload["net_memberships"][0]
    assert usb_p["net_classes"] == ["USB"]
    assert usb_p["differential_pairs"] == [
        {"name": "USB_D", "polarity": "positive"},
        {"name": "SECOND_REFERENCE", "polarity": "positive"},
    ]
    assert usb_p["differential_pair_classes"] == ["Serial Pairs"]
    clock_a = payload["net_memberships"][2]
    assert clock_a["differential_pairs"] == [
        {"name": "CLOCK_LINK", "polarity": "positive"}
    ]

    projected_rule = payload["rules"][0]
    assert projected_rule["enabled"] is True
    assert projected_rule["scope"]["first"] == (
        "InDifferentialPairClass('Serial Pairs') And OnLayer('Top Layer')"
    )
    assert projected_rule["scope"]["applicability"] == ("not_evaluated_by_cruncher")
    assert projected_rule["scope"]["references"] == [
        {
            "expression": "first",
            "function": "InDifferentialPairClass",
            "kind": "differential_pair_class",
            "name": "Serial Pairs",
            "resolution": "resolved",
            "matched_name": "Serial Pairs",
            "matched_unique_id": "CLASS-Serial Pairs",
        }
    ]
    assert projected_rule["constraints"]["impedance_profile_driven"] is False
    assert projected_rule["constraints"]["layer_metrics"]["TOPLAYER"] == {
        "minimum_width": "4mil",
        "preferred_width": "5mil",
        "maximum_width": "6mil",
        "minimum_gap": "",
        "preferred_gap": "",
        "maximum_gap": "",
    }
    assert projected_rule["unmodeled_fields"] == {"FUTUREFIELD": "preserve-me"}
    assert payload["rules"][1]["enabled"] is None
    assert payload["rules"][1]["priority"] is None
    assert payload["rules"][1]["defined_by_logical_document"] is None
    assert payload["rules"][1]["unmodeled_fields"] == {"FUTURELIMIT": "11mil"}


def test_scope_class_references_are_conservative_and_diagnostic() -> None:
    rules = [
        AltiumPcbRule(
            index=4,
            rule_kind="MatchedLengths",
            name="Resolved references",
            scope1_expression=("innetclass ( 'emmc' ) Or InNetClass('Driver''s Bus')"),
            scope2_expression="InDifferentialPairClass('Serial Pairs')",
        ),
        AltiumPcbRule(
            index=5,
            rule_kind="MatchedLengths",
            name="Unresolved references",
            scope1_expression="InNetClass('MISSING') Or InNetClass('dup')",
            scope2_expression=(
                "Name = 'InNetClass(''NOT_A_CALL'')' And InxSignalClass('XS')"
            ),
        ),
    ]
    pcbdoc = SimpleNamespace(
        nets=[],
        net_classes=[
            _class("EMMC", PcbNetClassKind.NET, []),
            _class("Driver's Bus", PcbNetClassKind.NET, []),
            _class("DUP", PcbNetClassKind.NET, []),
            _class("dup", PcbNetClassKind.NET, []),
            _class("Serial Pairs", PcbNetClassKind.DIFF_PAIR, []),
        ],
        differential_pairs=[],
        rules=rules,
    )

    payload = build_pcb_routing_context_payload(
        pcbdoc,
        source="scope-references.PcbDoc",
        board="scope-references",
    )

    _validate(payload)
    assert payload["rules"][0]["scope"]["references"] == [
        {
            "expression": "first",
            "function": "InNetClass",
            "kind": "net_class",
            "name": "emmc",
            "resolution": "resolved",
            "matched_name": "EMMC",
            "matched_unique_id": "CLASS-EMMC",
        },
        {
            "expression": "first",
            "function": "InNetClass",
            "kind": "net_class",
            "name": "Driver's Bus",
            "resolution": "resolved",
            "matched_name": "Driver's Bus",
            "matched_unique_id": "CLASS-Driver's Bus",
        },
        {
            "expression": "second",
            "function": "InDifferentialPairClass",
            "kind": "differential_pair_class",
            "name": "Serial Pairs",
            "resolution": "resolved",
            "matched_name": "Serial Pairs",
            "matched_unique_id": "CLASS-Serial Pairs",
        },
    ]
    assert payload["rules"][1]["scope"]["references"] == [
        {
            "expression": "first",
            "function": "InNetClass",
            "kind": "net_class",
            "name": "MISSING",
            "resolution": "missing",
            "matched_name": None,
            "matched_unique_id": None,
        },
        {
            "expression": "first",
            "function": "InNetClass",
            "kind": "net_class",
            "name": "dup",
            "resolution": "ambiguous",
            "matched_name": None,
            "matched_unique_id": None,
        },
    ]
    assert [row["code"] for row in payload["diagnostics"]] == [
        "missing_rule_scope_class_reference",
        "ambiguous_rule_scope_class_reference",
    ]


def test_rt_super_corpus_resolves_sdio_matched_length_class() -> None:
    board_path = ROOT / "tests/assets/projects/rt_super_c1/input/RT_SUPER_C1.PCBdoc"
    pcbdoc = AltiumPcbDoc.from_file(board_path)

    payload = build_pcb_routing_context_payload(
        pcbdoc,
        source=board_path.name,
        board=board_path.stem,
    )

    _validate(payload)
    sdio = next(row for row in payload["net_classes"] if row["name"] == "SDIO")
    assert sdio["stored_members"] == [
        "SD-D3",
        "SD-D2",
        "SD-D1",
        "SD-D0",
        "SD-CMD",
        "SD-CLK",
    ]
    assert sdio["resolved_nets"] == sdio["stored_members"]
    matched = next(row for row in payload["rules"] if row["name"] == "EMMC_MATCH")
    assert matched["scope"]["references"] == [
        {
            "expression": "first",
            "function": "InNetClass",
            "kind": "net_class",
            "name": "SDIO",
            "resolution": "resolved",
            "matched_name": "SDIO",
            "matched_unique_id": sdio["unique_id"],
        }
    ]


def test_pimx8_corpus_resolves_compound_and_pair_class_scopes() -> None:
    board_path = (
        ROOT / "tests/assets/projects/ov-tech-pimx8/input/PCB/PiMX8MP_r0.3.PcbDoc"
    )
    pcbdoc = AltiumPcbDoc.from_file(board_path)

    payload = build_pcb_routing_context_payload(
        pcbdoc,
        source=board_path.name,
        board=board_path.stem,
    )

    _validate(payload)
    compound = next(row for row in payload["rules"] if row["name"] == "MTCH_xSIG_DIFF")
    assert [
        (reference["name"], reference["resolution"])
        for reference in compound["scope"]["references"]
    ] == [("DSI1", "resolved"), ("LVDS0", "resolved")]
    pair_class = next(row for row in payload["rules"] if row["name"] == "MTCH_DIFF")
    assert pair_class["scope"]["references"] == [
        {
            "expression": "first",
            "function": "InDifferentialPairClass",
            "kind": "differential_pair_class",
            "name": "All Differential Pairs",
            "resolution": "resolved",
            "matched_name": "All Differential Pairs",
            "matched_unique_id": next(
                row["unique_id"]
                for row in payload["differential_pair_classes"]
                if row["name"] == "All Differential Pairs"
            ),
        }
    ]


def test_routing_context_keeps_ambiguous_references_and_bad_values_visible() -> None:
    bad_rule = AltiumPcbRule(
        index=2,
        rule_kind="FutureRule",
        name="Bad JSON field",
        semantic_values={"not_json": b"binary"},
    )
    pcbdoc = SimpleNamespace(
        nets=[_net("DUP", "ONE"), _net("dup", "TWO")],
        net_classes=[_class("Signals", PcbNetClassKind.NET, ["DUP", "MISSING"])],
        differential_pairs=[
            AltiumPcbDifferentialPair.create(
                name="PAIR",
                positive_net_name="DUP",
                negative_net_name="MISSING",
            )
        ],
        rules=[bad_rule],
    )

    payload = build_pcb_routing_context_payload(
        pcbdoc,
        source="ambiguous.PcbDoc",
        board=None,
    )

    _validate(payload)
    assert payload["net_classes"][0]["resolved_nets"] == []
    assert payload["net_classes"][0]["unresolved_members"] == ["DUP", "MISSING"]
    assert payload["rules"][0]["constraints"] == {}
    codes = [row["code"] for row in payload["diagnostics"]]
    assert codes == [
        "duplicate_net_name",
        "ambiguous_pair_net",
        "missing_pair_net",
        "ambiguous_net_class_member",
        "missing_net_class_member",
        "unrepresentable_rule_value",
    ]


def test_empty_routing_context_is_schema_valid_and_deterministic() -> None:
    pcbdoc = SimpleNamespace(
        nets=[],
        net_classes=[],
        differential_pairs=[],
        rules=[],
    )

    first = build_pcb_routing_context_payload(
        pcbdoc,
        source="empty.PcbDoc",
        board="empty",
    )
    second = build_pcb_routing_context_payload(
        pcbdoc,
        source="empty.PcbDoc",
        board="empty",
    )

    _validate(first)
    assert first == second
    assert first["summary"] == {
        "net_count": 0,
        "net_class_count": 0,
        "differential_pair_count": 0,
        "differential_pair_class_count": 0,
        "rule_count": 0,
        "enabled_rule_count": 0,
        "rules_by_kind": {},
    }
    assert first["diagnostics"] == []
