/** Generated from src/tsp/altium_cruncher/outputs/mate.tsp. Do not edit. */

export interface MatePartsManifest {
  schema: "altium_cruncher.mate.parts_cache.a0";
  source: PartSource;
  parts: KnownPart[];
  designator_normalization: RecordRecordString;
}
export interface PartSource {
  kind: string;
  project: string;
}
export interface KnownPart {
  role: string;
  description: string;
  symbol_name: string;
  symbol_library: string;
  footprint_name: string;
  footprint_library: string;
  target_kinds: string[];
  designator_prefix: string;
  signal_pad_designator: string | null;
}
export interface RecordRecordString {
  [k: string]: RecordString;
}
export interface RecordString {
  [k: string]: string;
}
