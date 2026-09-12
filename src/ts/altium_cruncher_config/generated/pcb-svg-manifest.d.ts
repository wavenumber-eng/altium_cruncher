/** Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit. */

export interface PcbSvgManifest {
  schema: "pcb.svg.manifest.a0";
  board: string;
  source_input: string;
  layer_outputs: RecordSvgLayerOutput;
  views: RecordSvgViewOutput;
}
export interface RecordSvgLayerOutput {
  [k: string]: SvgLayerOutput;
}
export interface SvgLayerOutput {
  file: string;
  layers: string[];
  group_id: string;
}
export interface RecordSvgViewOutput {
  [k: string]: SvgViewOutput;
}
export interface SvgViewOutput {
  file: string;
  group_id: string;
  layers: string[];
  mirrored: boolean;
  assembly_hlr_mode: string;
}
