/** Generated from src/tsp/altium_cruncher/outputs/schematic-svg-enrichment.tsp. Do not edit. */

export type SchematicSvgEnrichmentViewPhysicalPageMetadata = RecordUnknown & {};

export interface SchematicSvgEnrichment {
  schema: "altium_cruncher.schematic.svg.enrichment.b0";
  source: SchematicSvgEnrichmentSource;
  view: SchematicSvgEnrichmentView;
}
export interface SchematicSvgEnrichmentSource {
  altium_schdoc_file: string;
  page_occurrence_ref: string;
  artifact_key: "sch.dwg_scene";
}
export interface SchematicSvgEnrichmentView {
  kind: "compiled_schematic_page";
  profile: "design_review";
  sheet_name: string;
  sheet_file: string;
  page_occurrence_ref: string;
  artifact_key: "sch.dwg_scene";
  physical_page_metadata: SchematicSvgEnrichmentViewPhysicalPageMetadata;
}
export interface RecordUnknown {
  [k: string]: unknown;
}
