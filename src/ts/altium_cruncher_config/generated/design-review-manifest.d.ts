/** Generated from src/tsp/altium_cruncher/outputs/design-review-manifest.tsp. Do not edit. */

export type Path = string;
export type DesignReviewManifestSchematicSvgsItem = LogicalSchematicArtifact | CompiledSchematicArtifact;
export type PositiveInteger = number;

export interface DesignReviewManifest {
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
  /**
   * Path to pcb/<board>__design-rules-and-classes.json, containing compact authored net classes, differential pairs/classes, and design rules for this board. New B1 producers always emit it; it is optional for additive schema compatibility.
   */
  design_rules_and_classes?: string;
}
export interface PcbOutput {
  name: string;
  file: Path;
  layers: string[];
}
