# PCB routing context output fields

Generated from src/tsp/altium_cruncher/outputs/pcb-routing-context.tsp. Do not edit.

Wire fields emitted by Cruncher. Validation preserves the payload without inserting defaults.

See the contract authority inventory for producer locations and delegated upstream data boundaries.

## PcbRoutingContext

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `schema` | Yes | — |  |
| `source` | Yes | — |  |
| `board` | Yes | — |  |
| `evidence` | Yes | — |  |
| `summary` | Yes | — |  |
| `net_classes` | Yes | — |  |
| `differential_pairs` | Yes | — |  |
| `differential_pair_classes` | Yes | — |  |
| `net_memberships` | Yes | — |  |
| `rules` | Yes | — |  |
| `diagnostics` | Yes | — |  |

## RoutingContextEvidence

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `authored_rules` | Yes | — | Authored PcbDoc design-rule definitions are included; this is not a compliance result. |
| `class_membership` | Yes | — | Only members stored in Classes6 are projected; display names do not imply dynamic membership. |
| `rule_applicability` | Yes | — | Cruncher preserved rule scopes but did not evaluate Altium's query language or choose effective rules. |
| `drc_run_by_cruncher` | Yes | — | False means this export operation did not run DRC; it does not describe the board's prior history. |
| `drc_violations` | Yes | — | No DRC pass/fail or violation rows are included in this artifact. |

## RoutingContextSummary

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `net_count` | Yes | — |  |
| `net_class_count` | Yes | — |  |
| `differential_pair_count` | Yes | — |  |
| `differential_pair_class_count` | Yes | — |  |
| `rule_count` | Yes | — |  |
| `enabled_rule_count` | Yes | — | Rules whose parsed enabled field is explicitly true; null is not counted as enabled. |
| `rules_by_kind` | Yes | — |  |

## NetClass

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `name` | Yes | — |  |
| `unique_id` | Yes | — |  |
| `enabled` | Yes | — |  |
| `stored_members` | Yes | — | Exact class members stored in the PcbDoc, without name-based expansion. |
| `resolved_nets` | Yes | — | Stored members that resolve uniquely to a PcbDoc net, preserving the net object's spelling. |
| `unresolved_members` | Yes | — | Stored members that do not resolve uniquely; diagnostics distinguish missing from ambiguous names. |

## DifferentialPair

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `name` | Yes | — |  |
| `unique_id` | Yes | — |  |
| `positive_net` | Yes | — | Authored positive net reference. Polarity is never inferred from a _P suffix. |
| `negative_net` | Yes | — | Authored negative net reference. Polarity is never inferred from a _N suffix. |
| `stored_classes` | Yes | — | Differential-pair classes that explicitly store this pair as a member. |

## DifferentialPairClass

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `name` | Yes | — |  |
| `unique_id` | Yes | — |  |
| `enabled` | Yes | — |  |
| `stored_members` | Yes | — |  |
| `resolved_pairs` | Yes | — |  |
| `resolved_nets` | Yes | — |  |
| `unresolved_members` | Yes | — |  |

## NetMembership

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `net` | Yes | — |  |
| `unique_id` | Yes | — |  |
| `net_classes` | Yes | — |  |
| `differential_pairs` | Yes | — | Every authored pair reference to this net; multiple rows remain visible instead of choosing one. |
| `differential_pair_classes` | Yes | — |  |

## DesignRule

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `index` | Yes | — |  |
| `unique_id` | Yes | — |  |
| `name` | Yes | — |  |
| `kind` | Yes | — |  |
| `enabled` | Yes | — |  |
| `priority` | Yes | — |  |
| `comment` | Yes | — |  |
| `defined_by_logical_document` | Yes | — |  |
| `scope` | Yes | — |  |
| `constraints` | Yes | — | Public typed rule-specific values from Altium Monkey. Values are recursively checked for finite JSON compatibility by the producer. |
| `unmodeled_fields` | Yes | — | Unconsumed source fields retained by Altium Monkey's typed rule parser. |

## RoutingContextDiagnostic

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `code` | Yes | — |  |
| `severity` | Yes | — |  |
| `message` | Yes | — |  |
| `source_collection` | Yes | — |  |
| `source_index` | No | — |  |
| `identity` | No | — |  |

## RecordCount

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## DifferentialPairMembership

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `name` | Yes | — |  |
| `polarity` | Yes | — |  |

## RuleScope

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `first` | Yes | — |  |
| `second` | Yes | — |  |
| `net_relation` | Yes | — |  |
| `layer_relation` | Yes | — |  |
| `references` | Yes | — | Conservatively extracted literal InNetClass and InDifferentialPairClass calls, in expression order. Unsupported query functions remain only in the exact expressions above. |
| `applicability` | Yes | — |  |

## RecordUnknown

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |

## RuleScopeReference

| Field | Required | Default annotation | Description |
| --- | --- | --- | --- |
| `expression` | Yes | — | Which authored binary-rule expression contains the literal reference. |
| `function` | Yes | — | Recognized Altium query function. This is a lexical reference, not an evaluated query result. |
| `kind` | Yes | — |  |
| `name` | Yes | — |  |
| `resolution` | Yes | — | Whether the literal name resolves uniquely in the corresponding exported class table. |
| `matched_name` | Yes | — |  |
| `matched_unique_id` | Yes | — |  |
