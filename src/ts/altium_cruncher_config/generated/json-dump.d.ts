/** Generated from src/tsp/altium_cruncher/outputs/json-dump.tsp. Do not edit. */

export type JsonDump = SchdocDump | SchlibDump | PcbdocDump | PcblibDump;
/**
 * The full SchDoc interop payload comes from Altium Monkey to_json(). Cruncher only supplies its format tag.
 */
export type SchDoc = RecordUnknown & {
  format: "altium_monkey.schdoc.interop.a0";
};
/**
 * The full SchLib interop payload comes from Altium Monkey to_json(). Cruncher only supplies its format tag.
 */
export type SchLib = RecordUnknown & {
  format: "altium_monkey.schlib.interop.a0";
};
/**
 * Native Altium Monkey record reflection, including enum/bytes summaries, properties and depth/cycle fallbacks. Upstream record fields are not owned by Cruncher.
 */
export type NativeValue = unknown;
export type Count = number;

export interface SchdocDump {
  schema: "altium_cruncher.json_dump.a0";
  kind: "SchDoc";
  document: SchDoc;
}
export interface RecordUnknown {
  [k: string]: unknown;
}
export interface SchlibDump {
  schema: "altium_cruncher.json_dump.a0";
  kind: "SchLib";
  document: SchLib;
}
export interface PcbdocDump {
  schema: "altium_cruncher.json_dump.a0";
  kind: "PcbDoc";
  document: PcbDoc;
}
export interface PcbDoc {
  pads: unknown[];
  vias: NativeValue[];
  tracks: NativeValue[];
  arcs: NativeValue[];
  texts: NativeValue[];
  fills: NativeValue[];
  regions: NativeValue[];
  shapebased_regions: NativeValue[];
  component_bodies: NativeValue[];
  models: NativeValue[];
  format: "altium_monkey.pcbdoc.structural.a0";
  counts: RecordCount;
  raw_streams: RawStream[];
  board: NativeValue;
  union_name_records: NativeValue[];
  smart_unions: NativeValue[];
  user_unions: (UserUnion | UnionError)[];
  components: NativeValue[];
  nets: NativeValue[];
  net_classes: NativeValue[];
  differential_pairs: NativeValue[];
  polygons: NativeValue[];
  rules: NativeValue[];
  dimensions: NativeValue[];
  extended_primitive_information: NativeValue[];
  custom_shapes: NativeValue[];
  via_structures: NativeValue[];
  via_structure_links: NativeValue[];
  board_regions: NativeValue[];
  shapebased_component_bodies: NativeValue[];
  embedded_fonts: NativeValue[];
  embedded_models: NativeValue[];
}
export interface RecordCount {
  [k: string]: Count;
}
export interface RawStream {
  name: string;
  byte_count: Count;
  sha256: string;
}
export interface UserUnion {
  union_index: number;
  name: string;
  member_count: Count;
  members: UnionMember[];
}
export interface UnionMember {
  collection: string;
  object_index: number;
  union_index: number;
  object_summary: MemberSummary;
}
export interface MemberSummary {
  class?: string;
  designator?: NativeValue;
  name?: NativeValue;
  text_content?: NativeValue;
  footprint?: NativeValue;
  comment?: NativeValue;
  x_mils?: NativeValue;
  y_mils?: NativeValue;
  start_x_mils?: NativeValue;
  start_y_mils?: NativeValue;
  end_x_mils?: NativeValue;
  end_y_mils?: NativeValue;
  center_x_mils?: NativeValue;
  center_y_mils?: NativeValue;
}
export interface UnionError {
  error: string;
}
export interface PcblibDump {
  schema: "altium_cruncher.json_dump.a0";
  kind: "PcbLib";
  document: PcbLib;
}
export interface PcbLib {
  format: "altium_monkey.pcblib.structural.a0";
  footprint_count: Count;
  footprints: Footprint[];
  models_3d: NativeValue;
  raw_streams: RawStream[];
}
export interface Footprint {
  pads: NativeValue[];
  vias: NativeValue[];
  tracks: NativeValue[];
  arcs: NativeValue[];
  texts: NativeValue[];
  fills: NativeValue[];
  regions: NativeValue[];
  shapebased_regions: NativeValue[];
  component_bodies: NativeValue[];
  models: NativeValue[];
  name: string;
  counts: RecordCount;
}
