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
}

@oneOf
union DesignReviewManifestSchematicSvgsItem {
  LogicalSchematicArtifact,
  CompiledSchematicArtifact,
}

@jsonSchema
@id("https://github.com/wavenumber-eng/altium_cruncher/docs/contracts/design_review_manifest.b0.schema.json")
@extension("title", "Altium Cruncher Design Review Manifest b0")
model DesignReviewManifest {
  schema: "altium_cruncher.design_review_manifest.b0";
  input: Path;
  design_json: Path;
  document_jsons: DocumentArtifact[];
  notes_json: Path;
  schematic_svgs: DesignReviewManifestSchematicSvgsItem[];
  schematic_irs: CompiledSchematicArtifact[];
  pcb_svgs: PcbArtifact[];
  readme: Path;
}
