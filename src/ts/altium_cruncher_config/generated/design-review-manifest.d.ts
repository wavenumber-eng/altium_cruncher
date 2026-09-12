/** Generated from src/tsp/altium_cruncher/outputs/design-review-manifest.tsp. Do not edit. */

export type Path = string;
export type DesignReviewManifestSchematicSvgsItem = LogicalSchematicArtifact | CompiledSchematicArtifact;
export type PositiveInteger = number;

export interface DesignReviewManifest {
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
export interface DocumentArtifact {
  file: Path;
  source: Path;
  kind: "SchDoc" | "PcbDoc";
}
export interface LogicalSchematicArtifact {
  file: Path;
  source: Path;
  page_number: PositiveInteger;
  page_count: PositiveInteger;
}
export interface CompiledSchematicArtifact {
  file: Path;
  page_occurrence_ref: string;
  artifact_key: "sch.dwg_scene";
  source: Path;
  source_sheet: Path;
  page_number: PositiveInteger;
  page_count: PositiveInteger;
}
export interface PcbArtifact {
  manifest: Path;
  board: string | null;
  layer_outputs: PcbOutput[];
  views: PcbOutput[];
}
export interface PcbOutput {
  name: string;
  file: Path;
  layers: string[];
}
