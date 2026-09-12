/** Generated from src/tsp/altium_cruncher/config/mate-config.tsp. Do not edit. */

export type MatePartsInput = RecordUnknown & {
  schema: "altium_cruncher.mate.parts_cache.a0";
  parts: AuthoredKnownPart[];
  source?: PartSource;
  designator_normalization?: RecordRecordString;
};
export type AuthoredKnownPart = RecordUnknown & {
  role?: string;
  description?: string | null;
  symbol_name?: string;
  symbol_library?: string;
  footprint_name?: string;
  footprint_library?: string;
  target_kinds?: string | StringArray | null;
  designator_prefix?: string;
  signal_pad_designator?: string | null;
};
export type StringArray = string[];

export interface RecordUnknown {
  [k: string]: unknown;
}
export interface PartSource {
  kind: string;
  project: string;
}
export interface RecordRecordString {
  [k: string]: RecordString;
}
export interface RecordString {
  [k: string]: string;
}
