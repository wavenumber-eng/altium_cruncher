import "@typespec/json-schema";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.SchematicSvgEnrichmentContract;

model SchematicSvgEnrichmentSource {
  @extension("minLength", 1)
  altium_schdoc_file: string;

  @extension("minLength", 1)
  page_occurrence_ref: string;

  artifact_key: "sch.dwg_scene";
}

model SchematicSvgEnrichmentViewPhysicalPageMetadata extends Record<unknown> {}

model SchematicSvgEnrichmentView {
  kind: "compiled_schematic_page";
  profile: "design_review";
  sheet_name: string;

  @extension("minLength", 1)
  sheet_file: string;

  @extension("minLength", 1)
  page_occurrence_ref: string;

  artifact_key: "sch.dwg_scene";
  physical_page_metadata: SchematicSvgEnrichmentViewPhysicalPageMetadata;
}

@jsonSchema
@id("https://github.com/wavenumber-eng/altium_cruncher/docs/contracts/schematic_svg_enrichment.b0.schema.json")
@extension("title", "Compiled Schematic SVG Enrichment b0")
model SchematicSvgEnrichment {
  schema: "altium_cruncher.schematic.svg.enrichment.b0";
  source: SchematicSvgEnrichmentSource;
  view: SchematicSvgEnrichmentView;
}
