import "@typespec/json-schema";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.MegamaidManifestContract;

model Netlist {
  @extension("minLength", 1)
  design_json: string;

  design_schema: "altium_monkey.design.b0";
  compiled_schematic_graph_schema: "altium_monkey.compiled_schematic_graph.a0";

  @extension("minimum", 0)
  component_count: integer;

  @extension("minimum", 0)
  net_count: integer;

  @extension("minimum", 0)
  page_occurrence_count: integer;

  @extension("minimum", 0)
  graphical_artifact_link_count: integer;
}

model MegamaidManifestBom extends Record<unknown> {
  output_kinds?: string[];
  outputs?: BomOutput[];
}
model BomOutput {
  variant: string;
  component_count: integer;
  artifacts: string[];
}
model PnpOutput {
  variant: string;
  placement_count: integer;
  artifacts: string[];
}

model MegamaidManifestPnp extends Record<unknown> {
  output_kinds?: string[];
  outputs?: PnpOutput[];
  skipped?: string;
}

model MegamaidManifestDocumentJsonsItem extends Record<unknown> {
  source?: string;
  kind?: string;
  json?: string;
}
model LibraryJsonEntry {
  source: string;
  kind: string;
  json: string;
  scope: "combined" | "split";
}

model MegamaidManifestLibraryJsons extends Record<unknown> {
  schlib?: LibraryJsonEntry[];
  pcblib?: LibraryJsonEntry[];
}

model MegamaidManifestNotes extends Record<unknown> {
  notes_json?: string;
}
model SchdocSplitResult {
  source_schdoc: string;
  split_results: Record<boolean>;
}

model MegamaidManifestSchlibItem extends Record<unknown> {
  source_schdocs?: string[];
  combined_schlib?: string;
  split_dir?: string;
  symbol_count?: integer;
  split_file_count?: integer;
  split_files?: string[];
  split_results_by_schdoc?: SchdocSplitResult[];
}

model MegamaidManifestPcblibItem extends Record<unknown> {
  source_pcbdoc?: string;
  combined_pcblib?: string;
  split_dir?: string;
  footprint_count?: integer;
  split_file_count?: integer;
  split_files?: string[];
}
model EmbeddedAsset {
  source_pcbdoc: string;
  source_name: string;
  output_file: string;
  deduplicated: boolean;
}
model SchematicImage {
  source_schdoc: string;
  source_name: string;
  output_file: string;
  deduplicated: boolean;
}

model MegamaidManifestEmbeddedAssets extends Record<unknown> {
  fonts?: EmbeddedAsset[];
  models?: EmbeddedAsset[];
  font_file_count?: integer;
  model_file_count?: integer;
}

model MegamaidManifestSchImages extends Record<unknown> {
  images?: SchematicImage[];
  image_file_count?: integer;
}

@jsonSchema
@id("https://github.com/wavenumber-eng/altium_cruncher/docs/contracts/megamaid_manifest.b0.schema.json")
@extension("title", "Altium Cruncher MegaMaid Manifest b0")
model MegamaidManifest {
  schema: "altium_cruncher.megamaid_manifest.b0";
  kind: "megamaid";

  @extension("minLength", 1)
  input_project: string;

  @extension("minLength", 1)
  output_root: string;

  variants: string[];
  bom_pnp_config: string | null;

  @extension("minimum", 0)
  schdoc_count: integer;

  @extension("minimum", 0)
  pcbdoc_count: integer;

  bom: MegamaidManifestBom;
  pnp: MegamaidManifestPnp;
  netlist: Netlist;
  document_jsons: MegamaidManifestDocumentJsonsItem[];
  library_jsons: MegamaidManifestLibraryJsons;
  notes: MegamaidManifestNotes;
  schlib: MegamaidManifestSchlibItem[];
  pcblib: MegamaidManifestPcblibItem[];
  embedded_assets: MegamaidManifestEmbeddedAssets;
  sch_images: MegamaidManifestSchImages;
}
