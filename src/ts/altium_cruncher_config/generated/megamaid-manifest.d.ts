/** Generated from src/tsp/altium_cruncher/outputs/megamaid-manifest.tsp. Do not edit. */

export type MegamaidManifestBom = RecordUnknown & {
  output_kinds?: string[];
  outputs?: BomOutput[];
};
export type MegamaidManifestPnp = RecordUnknown & {
  output_kinds?: string[];
  outputs?: PnpOutput[];
  skipped?: string;
};
export type MegamaidManifestDocumentJsonsItem = RecordUnknown & {
  source?: string;
  kind?: string;
  json?: string;
};
export type MegamaidManifestLibraryJsons = RecordUnknown & {
  schlib?: LibraryJsonEntry[];
  pcblib?: LibraryJsonEntry[];
};
export type MegamaidManifestNotes = RecordUnknown & {
  notes_json?: string;
};
export type MegamaidManifestSchlibItem = RecordUnknown & {
  source_schdocs?: string[];
  combined_schlib?: string;
  split_dir?: string;
  symbol_count?: number;
  split_file_count?: number;
  split_files?: string[];
  split_results_by_schdoc?: SchdocSplitResult[];
};
export type MegamaidManifestPcblibItem = RecordUnknown & {
  source_pcbdoc?: string;
  combined_pcblib?: string;
  split_dir?: string;
  footprint_count?: number;
  split_file_count?: number;
  split_files?: string[];
};
export type MegamaidManifestEmbeddedAssets = RecordUnknown & {
  fonts?: EmbeddedAsset[];
  models?: EmbeddedAsset[];
  font_file_count?: number;
  model_file_count?: number;
};
export type MegamaidManifestSchImages = RecordUnknown & {
  images?: SchematicImage[];
  image_file_count?: number;
};

export interface MegamaidManifest {
  schema: "altium_cruncher.megamaid_manifest.b0";
  kind: "megamaid";
  input_project: string;
  output_root: string;
  variants: string[];
  bom_pnp_config: string | null;
  schdoc_count: number;
  pcbdoc_count: number;
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
export interface RecordUnknown {
  [k: string]: unknown;
}
export interface BomOutput {
  variant: string;
  component_count: number;
  artifacts: string[];
}
export interface PnpOutput {
  variant: string;
  placement_count: number;
  artifacts: string[];
}
export interface Netlist {
  design_json: string;
  design_schema: "altium_monkey.design.b0";
  compiled_schematic_graph_schema: "altium_monkey.compiled_schematic_graph.a0";
  component_count: number;
  net_count: number;
  page_occurrence_count: number;
  graphical_artifact_link_count: number;
}
export interface LibraryJsonEntry {
  source: string;
  kind: string;
  json: string;
  scope: "combined" | "split";
}
export interface SchdocSplitResult {
  source_schdoc: string;
  split_results: RecordBoolean;
}
export interface RecordBoolean {
  [k: string]: boolean;
}
export interface EmbeddedAsset {
  source_pcbdoc: string;
  source_name: string;
  output_file: string;
  deduplicated: boolean;
}
export interface SchematicImage {
  source_schdoc: string;
  source_name: string;
  output_file: string;
  deduplicated: boolean;
}
