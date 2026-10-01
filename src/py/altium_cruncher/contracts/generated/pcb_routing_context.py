"""Generated from src/tsp/altium_cruncher/outputs/pcb-routing-context.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

PcbRoutingContext = TypedDict("PcbRoutingContext", {
    "schema": "Literal[\"altium_cruncher.pcb_routing_context.a0\"]",
    "source": "Path",
    "board": "str | None",
    "evidence": "RoutingContextEvidence",
    "summary": "RoutingContextSummary",
    "net_classes": "list[NetClass]",
    "differential_pairs": "list[DifferentialPair]",
    "differential_pair_classes": "list[DifferentialPairClass]",
    "net_memberships": "list[NetMembership]",
    "rules": "list[DesignRule]",
    "diagnostics": "list[RoutingContextDiagnostic]",
}, closed=True)

RoutingContextEvidence = TypedDict("RoutingContextEvidence", {
    "authored_rules": "Literal[\"included\"]",
    "class_membership": "Literal[\"stored_members_only\"]",
    "rule_applicability": "Literal[\"not_evaluated_by_cruncher\"]",
    "drc_run_by_cruncher": "Literal[False]",
    "drc_violations": "Literal[\"not_included\"]",
}, closed=True)

RoutingContextSummary = TypedDict("RoutingContextSummary", {
    "net_count": "Count",
    "net_class_count": "Count",
    "differential_pair_count": "Count",
    "differential_pair_class_count": "Count",
    "rule_count": "Count",
    "enabled_rule_count": "Count",
    "rules_by_kind": "RecordCount",
}, closed=True)

NetClass = TypedDict("NetClass", {
    "name": "str",
    "unique_id": "str | None",
    "enabled": "bool",
    "stored_members": "list[str]",
    "resolved_nets": "list[str]",
    "unresolved_members": "list[str]",
}, closed=True)

DifferentialPair = TypedDict("DifferentialPair", {
    "name": "str",
    "unique_id": "str | None",
    "positive_net": "str",
    "negative_net": "str",
    "stored_classes": "list[str]",
}, closed=True)

DifferentialPairClass = TypedDict("DifferentialPairClass", {
    "name": "str",
    "unique_id": "str | None",
    "enabled": "bool",
    "stored_members": "list[str]",
    "resolved_pairs": "list[str]",
    "resolved_nets": "list[str]",
    "unresolved_members": "list[str]",
}, closed=True)

NetMembership = TypedDict("NetMembership", {
    "net": "str",
    "unique_id": "str | None",
    "net_classes": "list[str]",
    "differential_pairs": "list[DifferentialPairMembership]",
    "differential_pair_classes": "list[str]",
}, closed=True)

DesignRule = TypedDict("DesignRule", {
    "index": "Count",
    "unique_id": "str | None",
    "name": "str",
    "kind": "str",
    "enabled": "bool | None",
    "priority": "int | None",
    "comment": "str",
    "defined_by_logical_document": "bool | None",
    "scope": "RuleScope",
    "constraints": "RecordUnknown",
    "unmodeled_fields": "RecordUnknown",
}, closed=True)

RoutingContextDiagnostic = TypedDict("RoutingContextDiagnostic", {
    "code": "str",
    "severity": "Literal[\"warning\"]",
    "message": "str",
    "source_collection": "str",
    "source_index": NotRequired["Count"],
    "identity": NotRequired["str"],
}, closed=True)

DifferentialPairMembership = TypedDict("DifferentialPairMembership", {
    "name": "str",
    "polarity": "Literal[\"positive\"] | Literal[\"negative\"]",
}, closed=True)

RuleScope = TypedDict("RuleScope", {
    "first": "str",
    "second": "str",
    "net_relation": "str",
    "layer_relation": "str",
    "references": "list[RuleScopeReference]",
    "applicability": "Literal[\"not_evaluated_by_cruncher\"]",
}, closed=True)

RuleScopeReference = TypedDict("RuleScopeReference", {
    "expression": "Literal[\"first\"] | Literal[\"second\"]",
    "function": "Literal[\"InNetClass\"] | Literal[\"InDifferentialPairClass\"]",
    "kind": "Literal[\"net_class\"] | Literal[\"differential_pair_class\"]",
    "name": "str",
    "resolution": "Literal[\"resolved\"] | Literal[\"missing\"] | Literal[\"ambiguous\"]",
    "matched_name": "str | None",
    "matched_unique_id": "str | None",
}, closed=True)

Path = str
Count = int
RecordCount = dict[str, Count]
RecordUnknown = dict[str, object]
