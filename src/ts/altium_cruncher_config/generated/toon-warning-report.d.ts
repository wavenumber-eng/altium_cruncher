/** Generated from src/tsp/altium_cruncher/outputs/toon-warning-report.tsp. Do not edit. */

export interface ToonWarningReport {
  schema: "toon.warning_report.a0";
  summary: ToonWarningSummary;
  diagnostics: ToonWarningDiagnostic[];
}
export interface ToonWarningSummary {
  unique_diagnostic_count: number;
  occurrence_count: number;
  groups: ToonWarningSummaryGroup[];
}
export interface ToonWarningSummaryGroup {
  category:
    | "missing_model"
    | "unsupported_model"
    | "invalid_model_geometry"
    | "geometer_geometry"
    | "region_resolution"
    | "rotation_resolution"
    | "clipping";
  code: string;
  unique_diagnostic_count: number;
  occurrence_count: number;
  affected_component_count: number;
  affected_body_count: number;
  affected_model_count: number;
  sample_designators: string[];
}
export interface ToonWarningDiagnostic {
  /**
   * Stable digest of the diagnostic's structured grouping identity.
   */
  key: string;
  code: string;
  severity: "warning";
  category:
    | "missing_model"
    | "unsupported_model"
    | "invalid_model_geometry"
    | "geometer_geometry"
    | "region_resolution"
    | "rotation_resolution"
    | "clipping";
  producer: string;
  message: string;
  occurrence_count: number;
  input?: string;
  board?: string;
  variant?: string;
  view?: string;
  component_designator?: string;
  body_index?: number;
  model_identity?: string;
  detail?: RecordUnknown;
}
export interface RecordUnknown {
  [k: string]: unknown;
}
