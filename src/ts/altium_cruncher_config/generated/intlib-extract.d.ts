/** Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit. */

export type Count = number;

export interface IntlibExtract {
  schema: "altium_cruncher.extract.intlib.a0";
  source: Source;
  output_dir: string;
  component_count: Count;
  component_parse_error: string | null;
  source_count: Count;
  libpkg_path: string | null;
  sources: ExtractedSource[];
}
export interface Source {
  path: string;
  name: string;
  stem: string;
}
export interface ExtractedSource {
  kind: string;
  stream_path: string;
  original_path: string;
  suggested_filename: string;
  output_path: string | null;
  output_relative_path: string | null;
}
