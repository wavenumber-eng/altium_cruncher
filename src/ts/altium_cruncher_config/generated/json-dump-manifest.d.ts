/** Generated from src/tsp/altium_cruncher/outputs/json-dump.tsp. Do not edit. */

export interface JsonDumpManifest {
  schema: "altium_cruncher.json_dump.manifest.a0";
  outputs: DumpOutput[];
}
export interface DumpOutput {
  source_path: string;
  output_path: string;
  kind: "SchDoc" | "SchLib" | "PcbDoc" | "PcbLib";
}
