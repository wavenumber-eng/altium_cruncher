/** Generated from src/tsp/altium_cruncher/outputs/pcb-routing-context.tsp. Do not edit. */

export type Path = string;
export type Count = number;

/**
 * Compact authored PCB classes, differential pairs, and design rules for review agents. It contains no DRC result.
 */
export interface PcbRoutingContext {
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
export interface RoutingContextEvidence {
  /**
   * Authored PcbDoc design-rule definitions are included; this is not a compliance result.
   */
  authored_rules: "included";
  /**
   * Only members stored in Classes6 are projected; display names do not imply dynamic membership.
   */
  class_membership: "stored_members_only";
  /**
   * Cruncher preserved rule scopes but did not evaluate Altium's query language or choose effective rules.
   */
  rule_applicability: "not_evaluated_by_cruncher";
  /**
   * False means this export operation did not run DRC; it does not describe the board's prior history.
   */
  drc_run_by_cruncher: false;
  /**
   * No DRC pass/fail or violation rows are included in this artifact.
   */
  drc_violations: "not_included";
}
export interface RoutingContextSummary {
  net_count: Count;
  net_class_count: Count;
  differential_pair_count: Count;
  differential_pair_class_count: Count;
  rule_count: Count;
  /**
   * Rules whose parsed enabled field is explicitly true; null is not counted as enabled.
   */
  enabled_rule_count: number;
  rules_by_kind: RecordCount;
}
export interface RecordCount {
  [k: string]: Count;
}
export interface NetClass {
  name: string;
  unique_id: string | null;
  enabled: boolean;
  /**
   * Exact class members stored in the PcbDoc, without name-based expansion.
   */
  stored_members: string[];
  /**
   * Stored members that resolve uniquely to a PcbDoc net, preserving the net object's spelling.
   */
  resolved_nets: string[];
  /**
   * Stored members that do not resolve uniquely; diagnostics distinguish missing from ambiguous names.
   */
  unresolved_members: string[];
}
export interface DifferentialPair {
  name: string;
  unique_id: string | null;
  /**
   * Authored positive net reference. Polarity is never inferred from a _P suffix.
   */
  positive_net: string;
  /**
   * Authored negative net reference. Polarity is never inferred from a _N suffix.
   */
  negative_net: string;
  /**
   * Differential-pair classes that explicitly store this pair as a member.
   */
  stored_classes: string[];
}
export interface DifferentialPairClass {
  name: string;
  unique_id: string | null;
  enabled: boolean;
  stored_members: string[];
  resolved_pairs: string[];
  resolved_nets: string[];
  unresolved_members: string[];
}
export interface NetMembership {
  net: string;
  unique_id: string | null;
  net_classes: string[];
  /**
   * Every authored pair reference to this net; multiple rows remain visible instead of choosing one.
   */
  differential_pairs: DifferentialPairMembership[];
  differential_pair_classes: string[];
}
export interface DifferentialPairMembership {
  name: string;
  polarity: "positive" | "negative";
}
export interface DesignRule {
  index: Count;
  unique_id: string | null;
  name: string;
  kind: string;
  enabled: boolean | null;
  priority: number | null;
  comment: string;
  defined_by_logical_document: boolean | null;
  scope: RuleScope;
  constraints: RecordUnknown;
  unmodeled_fields: RecordUnknown1;
}
export interface RuleScope {
  first: string;
  second: string;
  net_relation: string;
  layer_relation: string;
  /**
   * Conservatively extracted literal InNetClass and InDifferentialPairClass calls, in expression order. Unsupported query functions remain only in the exact expressions above.
   */
  references: RuleScopeReference[];
  applicability: "not_evaluated_by_cruncher";
}
export interface RuleScopeReference {
  /**
   * Which authored binary-rule expression contains the literal reference.
   */
  expression: "first" | "second";
  /**
   * Recognized Altium query function. This is a lexical reference, not an evaluated query result.
   */
  function: "InNetClass" | "InDifferentialPairClass";
  kind: "net_class" | "differential_pair_class";
  name: string;
  /**
   * Whether the literal name resolves uniquely in the corresponding exported class table.
   */
  resolution: "resolved" | "missing" | "ambiguous";
  matched_name: string | null;
  matched_unique_id: string | null;
}
/**
 * Public typed rule-specific values from Altium Monkey. Values are recursively checked for finite JSON compatibility by the producer.
 */
export interface RecordUnknown {
  [k: string]: unknown;
}
/**
 * Unconsumed source fields retained by Altium Monkey's typed rule parser.
 */
export interface RecordUnknown1 {
  [k: string]: unknown;
}
export interface RoutingContextDiagnostic {
  code: string;
  severity: "warning";
  message: string;
  source_collection: string;
  source_index?: Count;
  identity?: string;
}
