import "@typespec/json-schema";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.ToonWarningReportContract;

alias ToonWarningCategory =
  | "missing_model"
  | "unsupported_model"
  | "invalid_model_geometry"
  | "geometer_geometry"
  | "region_resolution"
  | "rotation_resolution"
  | "clipping";

model ToonWarningDiagnostic {
  @doc("Stable digest of the diagnostic's structured grouping identity.")
  key: string;

  code: string;
  severity: "warning";
  category: ToonWarningCategory;
  producer: string;
  message: string;

  @extension("minimum", 1)
  occurrence_count: integer;

  input?: string;
  board?: string;
  variant?: string;
  view?: string;
  component_designator?: string;

  @extension("minimum", 0)
  body_index?: integer;

  model_identity?: string;
  detail?: Record<unknown>;
}

model ToonWarningSummaryGroup {
  category: ToonWarningCategory;
  code: string;

  @extension("minimum", 1)
  unique_diagnostic_count: integer;

  @extension("minimum", 1)
  occurrence_count: integer;

  @extension("minimum", 0)
  affected_component_count: integer;

  @extension("minimum", 0)
  affected_body_count: integer;

  @extension("minimum", 0)
  affected_model_count: integer;

  sample_designators: string[];
}

model ToonWarningSummary {
  @extension("minimum", 0)
  unique_diagnostic_count: integer;

  @extension("minimum", 0)
  occurrence_count: integer;

  groups: ToonWarningSummaryGroup[];
}

@jsonSchema
@id("toon.warning_report.a0")
@extension("title", "Toon nonfatal warning report")
model ToonWarningReport {
  schema: "toon.warning_report.a0";
  summary: ToonWarningSummary;
  diagnostics: ToonWarningDiagnostic[];
}
