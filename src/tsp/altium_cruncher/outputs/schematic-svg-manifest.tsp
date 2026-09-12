import "@typespec/json-schema";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.SchematicSvgManifestContract;

model SvgArtifact {
  @extension("minLength", 1)
  file: string;

  @extension("minLength", 1)
  page_occurrence_ref: string;

  artifact_key: "sch.dwg_scene";

  @extension("minLength", 1)
  source: string;

  @extension("minLength", 1)
  source_sheet: string;

  @extension("minimum", 1)
  page_number: integer;

  @extension("minimum", 1)
  page_count: integer;
}

@jsonSchema
@id("https://github.com/wavenumber-eng/altium_cruncher/docs/contracts/schematic_svg_manifest.b0.schema.json")
@extension("title", "Altium Cruncher Schematic SVG Manifest b0")
model SchematicSvgManifest {
  schema: "altium_cruncher.schematic_svg_manifest.b0";

  @extension("minLength", 1)
  input: string;

  @extension("minLength", 1)
  design_json: string;

  design_schema: "altium_monkey.design.b0";
  compiled_schematic_graph_schema: "altium_monkey.compiled_schematic_graph.a0";

  @extension("minItems", 1)
  svgs: SvgArtifact[];
}
