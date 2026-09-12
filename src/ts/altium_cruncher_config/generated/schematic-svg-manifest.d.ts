/** Generated from src/tsp/altium_cruncher/outputs/schematic-svg-manifest.tsp. Do not edit. */

export interface SchematicSvgManifest {
  schema: "altium_cruncher.schematic_svg_manifest.b0";
  input: string;
  design_json: string;
  design_schema: "altium_monkey.design.b0";
  compiled_schematic_graph_schema: "altium_monkey.compiled_schematic_graph.a0";
  /**
   * @minItems 1
   */
  svgs: [SvgArtifact, ...SvgArtifact[]];
}
export interface SvgArtifact {
  file: string;
  page_occurrence_ref: string;
  artifact_key: "sch.dwg_scene";
  source: string;
  source_sheet: string;
  page_number: number;
  page_count: number;
}
