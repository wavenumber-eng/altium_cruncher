import "@typespec/json-schema";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.DesignReviewManifestContract;

@extension("minLength", 1)
scalar Path extends string;

@extension("minimum", 1)
scalar PositiveInteger extends integer;

model DocumentArtifact {
  file: Path;
  source: Path;
  kind: "SchDoc" | "PcbDoc";
}

model LogicalSchematicArtifact {
  file: Path;
  source: Path;
  page_number: PositiveInteger;
  page_count: PositiveInteger;
}

model CompiledSchematicArtifact {
  file: Path;

  @extension("minLength", 1)
  page_occurrence_ref: string;

  artifact_key: "sch.dwg_scene";
  source: Path;
  source_sheet: Path;
  page_number: PositiveInteger;
  page_count: PositiveInteger;
}

model PcbOutput {
  @extension("minLength", 1)
  name: string;

  file: Path;
  layers: string[];
}

model PcbArtifact {
  manifest: Path;
  board: string | null;
  layer_outputs: PcbOutput[];
  views: PcbOutput[];

  @doc("Path to pcb/<board>__design-rules-and-classes.json, containing compact authored net classes, differential pairs/classes, and design rules for this board. New B1 producers always emit it; it is optional for additive schema compatibility.")
  design_rules_and_classes?: Path;
}

@oneOf
union DesignReviewManifestSchematicSvgsItem {
  LogicalSchematicArtifact,
  CompiledSchematicArtifact,
}

@jsonSchema
@id("https://github.com/wavenumber-eng/altium_cruncher/docs/contracts/design_review_manifest.b1.schema.json")
@extension("title", "Altium Cruncher Design Review Manifest b1")
model DesignReviewManifest {
  schema: "altium_cruncher.design_review_manifest.b1";
  input: Path;
  design_json: Path;
  document_jsons: DocumentArtifact[];
  notes_json: Path;
  schematic_svgs: DesignReviewManifestSchematicSvgsItem[];
  schematic_irs: CompiledSchematicArtifact[];
  pcb_svgs: PcbArtifact[];
  readme: Path;
}

// Frozen B0 predecessor. Keep its complete reachable artifact model separate
// so later B1 additions cannot leak into the durable historical schema.
model DocumentArtifactB0 {
  file: Path;
  source: Path;
  kind: "SchDoc" | "PcbDoc";
}

model LogicalSchematicArtifactB0 {
  file: Path;
  source: Path;
  page_number: PositiveInteger;
  page_count: PositiveInteger;
}

model CompiledSchematicArtifactB0 {
  file: Path;

  @extension("minLength", 1)
  page_occurrence_ref: string;

  artifact_key: "sch.dwg_scene";
  source: Path;
  source_sheet: Path;
  page_number: PositiveInteger;
  page_count: PositiveInteger;
}

model PcbOutputB0 {
  @extension("minLength", 1)
  name: string;

  file: Path;
  layers: string[];
}

model PcbArtifactB0 {
  manifest: Path;
  board: string | null;
  layer_outputs: PcbOutputB0[];
  views: PcbOutputB0[];
}

@oneOf
union DesignReviewManifestSchematicSvgsItemB0 {
  LogicalSchematicArtifactB0,
  CompiledSchematicArtifactB0,
}

@jsonSchema
@id("https://github.com/wavenumber-eng/altium_cruncher/docs/contracts/design_review_manifest.b0.schema.json")
@extension("title", "Altium Cruncher Design Review Manifest b0")
model DesignReviewManifestB0 {
  schema: "altium_cruncher.design_review_manifest.b0";
  input: Path;
  design_json: Path;
  document_jsons: DocumentArtifactB0[];
  notes_json: Path;
  schematic_svgs: DesignReviewManifestSchematicSvgsItemB0[];
  schematic_irs: CompiledSchematicArtifactB0[];
  pcb_svgs: PcbArtifactB0[];
  readme: Path;
}
