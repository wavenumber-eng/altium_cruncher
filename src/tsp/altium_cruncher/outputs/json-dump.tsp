import "@typespec/json-schema";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.JsonDumpContract;

@minValue(0)
scalar Count extends integer;
@doc("Native Altium Monkey record reflection, including enum/bytes summaries, properties and depth/cycle fallbacks. Upstream record fields are not owned by Cruncher.")
union NativeValue {
  unknown,
}
model RawStream {
  name: string;
  byte_count: Count;
  @pattern("^[0-9a-f]{64}$") sha256: string;
}
model MemberSummary {
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
model UnionMember {
  collection: string;
  object_index: integer;
  union_index: integer;
  object_summary: MemberSummary;
}
model UserUnion {
  union_index: integer;
  name: string;
  member_count: Count;
  members: UnionMember[];
}
model UnionError {
  error: string;
}
model FootprintCollections {
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
}
model Footprint {
  ...FootprintCollections;
  name: string;
  counts: Record<Count>;
}
model PcbDoc {
  ...FootprintCollections;
  format: "altium_monkey.pcbdoc.structural.a0";
  counts: Record<Count>;
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
model PcbLib {
  format: "altium_monkey.pcblib.structural.a0";
  footprint_count: Count;
  footprints: Footprint[];
  models_3d: NativeValue;
  raw_streams: RawStream[];
}
@doc("The full SchDoc interop payload comes from Altium Monkey to_json(). Cruncher only supplies its format tag.")
model SchDoc extends Record<unknown> {
  format: "altium_monkey.schdoc.interop.a0";
}
@doc("The full SchLib interop payload comes from Altium Monkey to_json(). Cruncher only supplies its format tag.")
model SchLib extends Record<unknown> {
  format: "altium_monkey.schlib.interop.a0";
}
model SchdocDump {
  schema: "altium_cruncher.json_dump.a0";
  kind: "SchDoc";
  document: SchDoc;
}
model SchlibDump {
  schema: "altium_cruncher.json_dump.a0";
  kind: "SchLib";
  document: SchLib;
}
model PcbdocDump {
  schema: "altium_cruncher.json_dump.a0";
  kind: "PcbDoc";
  document: PcbDoc;
}
model PcblibDump {
  schema: "altium_cruncher.json_dump.a0";
  kind: "PcbLib";
  document: PcbLib;
}
@jsonSchema
@id("altium_cruncher.json_dump.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "json_dump",
    title: "Document JSON dump",
    source: "../outputs/json-dump",
    kind: "output",
  }
)
union JsonDump {
  SchdocDump,
  SchlibDump,
  PcbdocDump,
  PcblibDump,
}
model DumpOutput {
  source_path: string;
  output_path: string;
  kind: "SchDoc" | "SchLib" | "PcbDoc" | "PcbLib";
}
@jsonSchema
@id("altium_cruncher.json_dump.manifest.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "json_dump_manifest",
    title: "JSON dump batch",
    source: "../outputs/json-dump",
    kind: "output",
  }
)
model JsonDumpManifest {
  schema: "altium_cruncher.json_dump.manifest.a0";
  outputs: DumpOutput[];
}
