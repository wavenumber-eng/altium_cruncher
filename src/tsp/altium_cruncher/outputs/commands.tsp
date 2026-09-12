import "@typespec/json-schema";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.CommandOutputs;

@jsonSchema
@id("altium_cruncher.interface_design_manifest.a0")
@extension("x-acr-contract", #{stem: "interface_design_manifest", title: "Interface design inventory", source: "../outputs/commands", kind: "output"})
@doc("Cruncher-owned interface inventory consumed by documentation signoff; command_manifest remains wn-dev-std-owned.")
model InterfaceDesignManifest {
  schema: "altium_cruncher.interface_design_manifest.a0";
  major_interfaces: (string | NamedInterface)[];
}
model NamedInterface extends Record<unknown> { name: string; }

@minValue(0)
scalar Count extends integer;
model Source {
  path: string;
  name: string;
  stem: string;
}
model Point {
  x: float64;
  y: float64;
}
model Bounds {
  x_min: float64;
  y_min: float64;
  x_max: float64;
  y_max: float64;
}

model Note {
  text: string;
  position_mils: Point | null;
  unique_id?: string;
  bounds_mils?: Bounds;
  author?: string | float64 | boolean;
}
model NotesPage {
  file: string;
  notes?: Note[];
  text_frames?: Note[];
  free_text?: Note[];
}
model NoteFilters {
  include_sheet_template_text: boolean;
  default_suppression: string;
}
@jsonSchema
@id("altium_cruncher.notes.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "notes",
    title: "Schematic notes",
    source: "../outputs/commands",
    kind: "output",
  }
)
model Notes {
  schema: "altium_cruncher.notes.a0";
  input: string;
  source_kind: "schdoc" | "prjpcb";
  path_base: "input_directory";
  schdoc_count: Count;
  filters: NoteFilters;
  schdocs: NotesPage[];
}

model VariantRow {
  variant: string;
  sheet: string;
  designator: string;
  operation: string;
  detail: string;
  component_value: string;
  parameter_name: string;
  value: string;
  unique_id: string;
  alternate_part?: string;
  alternate_part_resolved?: string;
}
model Variant {
  name: string;
  unique_id: string;
  allow_fabrication: boolean;
  current: boolean;
  dnp: string[];
  variation_count: Count;
  parameter_count: Count;
  param_variation_count: Count;
  rows: VariantRow[];
}
@jsonSchema
@id("altium_cruncher.variants.list.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "variants_list",
    title: "Project variant listing",
    source: "../outputs/commands",
    kind: "output",
  }
)
model VariantsList {
  schema: "altium_cruncher.variants.list.a0";
  project: string;
  current_variant: string | null;
  variant_count: Count;
  variants: Variant[];
  rows: VariantRow[];
  index_errors: string[];
}

model ExtractedSource {
  kind: string;
  stream_path: string;
  original_path: string;
  suggested_filename: string;
  output_path: string | null;
  output_relative_path: string | null;
}
@jsonSchema
@id("altium_cruncher.extract.intlib.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "intlib_extract",
    title: "IntLib extraction",
    source: "../outputs/commands",
    kind: "output",
  }
)
model IntlibExtract {
  schema: "altium_cruncher.extract.intlib.a0";
  source: Source;
  output_dir: string;
  component_count: Count;
  component_parse_error: string | null;
  source_count: Count;
  libpkg_path: string | null;
  sources: ExtractedSource[];
}

model OutjobResult {
  project: string;
  outjob: string;
  success: boolean;
  launch_code: integer;
  timed_out: boolean;
  error_count: integer;
  marker_text: string;
  normalized_changed: boolean;
  rebound_document_paths: integer;
  marker_path: string;
  log_path: string;
}
@jsonSchema
@id("altium_cruncher.outjob.run.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "outjob_run",
    title: "OutJob execution",
    source: "../outputs/commands",
    kind: "output",
  }
)
model OutjobRun {
  schema: "altium_cruncher.outjob.run.a0";
  project: string;
  success: boolean;
  results: OutjobResult[];
}

model Install {
  name: string;
  label: string;
  major: integer | null;
  root: string;
  x2_path: string;
  runtime_tfm: string | null;
  registry_version: string | null;
  unique_id: string | null;
  source: string;
}
@jsonSchema
@id("altium_cruncher.installs.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "installs",
    title: "Altium install discovery",
    source: "../outputs/commands",
    kind: "output",
  }
)
model Installs {
  schema: "altium_cruncher.installs.a0";
  installs: Install[];
}
@jsonSchema
@id("altium_cruncher.launch.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "launch",
    title: "Altium launch",
    source: "../outputs/commands",
    kind: "output",
  }
)
model Launch {
  schema: "altium_cruncher.launch.a0";
  install: Install;
  file: string | null;
  command: string[];
  dry_run: boolean;
}

model Profile {
  name: string;
  guid: string;
  path: string;
  extensions_root: string;
  registry_path: string;
  registry_exists: boolean;
  module_name: string;
  module_dir: string;
  module_dir_exists: boolean;
  registered: boolean;
  registry_version: string | null;
  dll_path: string;
  dll_exists: boolean;
  last_write_time_utc: string | null;
}
model ProfileCleanAction {
  profile_guid: string;
  profile_name: string;
  profile_path: string;
  module_name: string;
  module_dir: string;
  removed_module_dir: boolean;
  removed_registry_item: boolean;
  dry_run: boolean;
}
@jsonSchema
@id("altium_cruncher.profiles.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "profiles",
    title: "Altium profiles",
    source: "../outputs/commands",
    kind: "output",
  }
)
model Profiles {
  schema: "altium_cruncher.profiles.a0";
  profiles: Profile[];
}
@jsonSchema
@id("altium_cruncher.profiles.clean.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "profiles_clean",
    title: "Profile cleanup report",
    source: "../outputs/commands",
    kind: "output",
  }
)
model ProfilesClean {
  schema: "altium_cruncher.profiles.clean.a0";
  actions: ProfileCleanAction[];
}

model LibraryEntry {
  name: string;
  library: string;
}
@jsonSchema
@id("altium_cruncher.libraries.scan.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "libraries_scan",
    title: "Library scan",
    source: "../outputs/commands",
    kind: "output",
  }
)
model LibrariesScan {
  schema: "altium_cruncher.libraries.scan.a0";
  roots: string[];
  recursive: boolean;
  symbols: LibraryEntry[];
  footprints: LibraryEntry[];
  warnings: string[];
}

model McoOperationResult {
  `op`: string;
  id: string;
  status: "ok" | "fail";
  message: string;

  @doc("Operation-specific results; custom registries own their output payloads.")
  outputs: Record<unknown>;

  error?: string;
}
@jsonSchema
@id("altium_cruncher.mco.execution.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "mco_execution",
    title: "MCO execution result",
    source: "../outputs/commands",
    kind: "output",
  }
)
model McoExecution {
  @doc("Existing execution reports reuse the input schema tag; the contract file distinguishes the result shape.")
  schema: "altium_cruncher.mco.a0";

  ok: boolean;
  dry_run: boolean;
  results: McoOperationResult[];
}
model McoCatalogEntry {
  `op`: string;
  group: string;
  summary: string;
  required_args: string[];
  optional_args: string[];
  aliases?: string[];
}
@jsonSchema
@id("altium_cruncher.mco.operations.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "mco_operations",
    title: "MCO operation catalog",
    source: "../outputs/commands",
    kind: "output",
  }
)
model McoOperations {
  schema: "altium_cruncher.mco.operations.a0";
  operations: McoCatalogEntry[];
}

model NormalizedBomComponent {
  designator: string;
  value: string;
  footprint: string;
  library_ref: string;
  description: string;
  sheet: string;
  dnp: boolean;
  parameters: Record<string>;
  canonical_fields: Record<string>;
  field_sources: Record<string>;
}
model GroupedBomLine {
  item: integer;
  quantity: Count;
  designators: string[];
  dnp: boolean;
  fields: Record<string>;
}
model Placement {
  designator: string;
  comment: string;
  layer: string;
  footprint: string;
  center_x: float64;
  center_y: float64;
  rotation: float64;
  units: string;
  description: string;
  parameters: Record<string>;
  canonical_fields: Record<string>;
  field_sources: Record<string>;
}
@jsonSchema
@id("altium_cruncher.bom.raw.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "bom_normalized",
    title: "Normalized BOM",
    source: "../outputs/commands",
    kind: "output",
  }
)
model BomNormalized {
  schema: "altium_cruncher.bom.raw.a0";
  source: Source;
  variant: string | null;
  component_count: Count;
  dnp_count: Count;
  components: NormalizedBomComponent[];
}
@jsonSchema
@id("altium_cruncher.bom.grouped.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "bom_grouped",
    title: "Grouped BOM",
    source: "../outputs/commands",
    kind: "output",
  }
)
model BomGrouped {
  schema: "altium_cruncher.bom.grouped.a0";
  source: Source;
  variant: string | null;
  line_count: Count;
  component_count: Count;
  dnp_line_count: Count;
  lines: GroupedBomLine[];
}
@jsonSchema
@id("altium_cruncher.pnp.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "pnp",
    title: "Pick and place",
    source: "../outputs/commands",
    kind: "output",
  }
)
model Pnp {
  schema: "altium_cruncher.pnp.a0";
  source: Source;
  variant: string | null;
  units: "mm" | "mils";
  position_mode: "altium-pick-place" | "component-origin";
  placement_count: Count;
  placements: Placement[];
}
@doc("Raw rows from the Altium Monkey BOM API, with source-dependent parameter columns preserved.")
model RawBomComponent extends Record<unknown> {
  designator?: string;
  value?: string;
  footprint?: string;
  library_ref?: string;
  description?: string;
  sheet?: string;
  dnp?: boolean;
  parameters?: Record<unknown>;
}
@jsonSchema
@id("altium_cruncher.bom.array.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "bom_array",
    title: "Raw BOM array (unwrapped wire format)",
    source: "../outputs/commands",
    kind: "output",
  }
)
model BomArray is RawBomComponent[];
@jsonSchema
@id("altium_cruncher.bom.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "bom_legacy",
    title: "Generic / legacy BOM",
    source: "../outputs/commands",
    kind: "output",
  }
)
model BomLegacy {
  schema: "altium_cruncher.bom.a0";
  source: Source;
  variant: string | null;
  component_count: Count;
  dnp_count: Count;
  columns: string[];
  parameter_columns: string[];
  components: Record<string>[];
  raw_components: RawBomComponent[];
  normalized: BomNormalized;
}

model SvgLayerOutput {
  file: string;
  layers: string[];
  group_id: string;
}
model SvgViewOutput {
  file: string;
  group_id: string;
  layers: string[];
  mirrored: boolean;
  assembly_hlr_mode: string;
}
@jsonSchema
@id("pcb.svg.manifest.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "pcb_svg_manifest",
    title: "PCB SVG outputs",
    source: "../outputs/commands",
    kind: "output",
  }
)
model PcbSvgManifest {
  schema: "pcb.svg.manifest.a0";
  board: string;
  source_input: string;
  layer_outputs: Record<SvgLayerOutput>;
  views: Record<SvgViewOutput>;
}
