import "@typespec/json-schema";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.PcbRoutingContextContract;

@minValue(0)
scalar Count extends integer;

@extension("minLength", 1)
scalar Path extends string;

model RoutingContextEvidence {
  @doc("Authored PcbDoc design-rule definitions are included; this is not a compliance result.")
  authored_rules: "included";

  @doc("Only members stored in Classes6 are projected; display names do not imply dynamic membership.")
  class_membership: "stored_members_only";

  @doc("Cruncher preserved rule scopes but did not evaluate Altium's query language or choose effective rules.")
  rule_applicability: "not_evaluated_by_cruncher";

  @doc("False means this export operation did not run DRC; it does not describe the board's prior history.")
  drc_run_by_cruncher: false;

  @doc("No DRC pass/fail or violation rows are included in this artifact.")
  drc_violations: "not_included";
}

model RoutingContextSummary {
  net_count: Count;
  net_class_count: Count;
  differential_pair_count: Count;
  differential_pair_class_count: Count;
  rule_count: Count;

  @doc("Rules whose parsed enabled field is explicitly true; null is not counted as enabled.")
  enabled_rule_count: Count;

  rules_by_kind: Record<Count>;
}

model NetClass {
  name: string;
  unique_id: string | null;
  enabled: boolean;

  @doc("Exact class members stored in the PcbDoc, without name-based expansion.")
  stored_members: string[];

  @doc("Stored members that resolve uniquely to a PcbDoc net, preserving the net object's spelling.")
  resolved_nets: string[];

  @doc("Stored members that do not resolve uniquely; diagnostics distinguish missing from ambiguous names.")
  unresolved_members: string[];
}

model DifferentialPair {
  name: string;
  unique_id: string | null;

  @doc("Authored positive net reference. Polarity is never inferred from a _P suffix.")
  positive_net: string;

  @doc("Authored negative net reference. Polarity is never inferred from a _N suffix.")
  negative_net: string;

  @doc("Differential-pair classes that explicitly store this pair as a member.")
  stored_classes: string[];
}

model DifferentialPairClass {
  name: string;
  unique_id: string | null;
  enabled: boolean;
  stored_members: string[];
  resolved_pairs: string[];
  resolved_nets: string[];
  unresolved_members: string[];
}

model DifferentialPairMembership {
  name: string;
  polarity: "positive" | "negative";
}

model NetMembership {
  net: string;
  unique_id: string | null;
  net_classes: string[];

  @doc("Every authored pair reference to this net; multiple rows remain visible instead of choosing one.")
  differential_pairs: DifferentialPairMembership[];

  differential_pair_classes: string[];
}

model RuleScopeReference {
  @doc("Which authored binary-rule expression contains the literal reference.")
  expression: "first" | "second";

  @doc("Recognized Altium query function. This is a lexical reference, not an evaluated query result.")
  function: "InNetClass" | "InDifferentialPairClass";

  kind: "net_class" | "differential_pair_class";
  name: string;

  @doc("Whether the literal name resolves uniquely in the corresponding exported class table.")
  resolution: "resolved" | "missing" | "ambiguous";

  matched_name: string | null;
  matched_unique_id: string | null;
}

model RuleScope {
  first: string;
  second: string;
  net_relation: string;
  layer_relation: string;

  @doc("Conservatively extracted literal InNetClass and InDifferentialPairClass calls, in expression order. Unsupported query functions remain only in the exact expressions above.")
  references: RuleScopeReference[];

  applicability: "not_evaluated_by_cruncher";
}

model DesignRule {
  index: Count;
  unique_id: string | null;
  name: string;
  kind: string;
  enabled: boolean | null;
  priority: integer | null;
  comment: string;
  defined_by_logical_document: boolean | null;
  scope: RuleScope;

  @doc("Public typed rule-specific values from Altium Monkey. Values are recursively checked for finite JSON compatibility by the producer.")
  constraints: Record<unknown>;

  @doc("Unconsumed source fields retained by Altium Monkey's typed rule parser.")
  unmodeled_fields: Record<unknown>;
}

model RoutingContextDiagnostic {
  code: string;
  severity: "warning";
  message: string;
  source_collection: string;
  source_index?: Count;
  identity?: string;
}

@jsonSchema
@id("altium_cruncher.pcb_routing_context.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "pcb_routing_context",
    title: "PCB routing context",
    source: "../outputs/pcb-routing-context",
    kind: "output",
  }
)
@doc("Compact authored PCB classes, differential pairs, and design rules for review agents. It contains no DRC result.")
model PcbRoutingContext {
  schema: "altium_cruncher.pcb_routing_context.a0";
  source: Path;
  board: string | null;
  evidence: RoutingContextEvidence;
  summary: RoutingContextSummary;
  net_classes: NetClass[];
  differential_pairs: DifferentialPair[];
  differential_pair_classes: DifferentialPairClass[];
  net_memberships: NetMembership[];
  rules: DesignRule[];
  diagnostics: RoutingContextDiagnostic[];
}
