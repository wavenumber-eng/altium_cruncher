/** Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit. */

export type Count = number;
/**
 * Raw rows from the Altium Monkey BOM API, with source-dependent parameter columns preserved.
 */
export type RawBomComponent = RecordUnknown & {
  designator?: string;
  value?: string;
  footprint?: string;
  library_ref?: string;
  description?: string;
  sheet?: string;
  dnp?: boolean;
  parameters?: RecordUnknown;
};
export type ImportedBomNormalized_Count = number;

export interface BomLegacy {
  schema: "altium_cruncher.bom.a0";
  source: Source;
  variant: string | null;
  component_count: Count;
  dnp_count: Count;
  columns: string[];
  parameter_columns: string[];
  components: RecordString[];
  raw_components: RawBomComponent[];
  normalized: ImportedBomNormalized;
}
export interface Source {
  path: string;
  name: string;
  stem: string;
}
export interface RecordString {
  [k: string]: string;
}
export interface RecordUnknown {
  [k: string]: unknown;
}
export interface ImportedBomNormalized {
  schema: "altium_cruncher.bom.raw.a0";
  source: ImportedBomNormalized_Source;
  variant: string | null;
  component_count: ImportedBomNormalized_Count;
  dnp_count: ImportedBomNormalized_Count;
  components: ImportedBomNormalized_NormalizedBomComponent[];
}
export interface ImportedBomNormalized_Source {
  path: string;
  name: string;
  stem: string;
}
export interface ImportedBomNormalized_NormalizedBomComponent {
  designator: string;
  value: string;
  footprint: string;
  library_ref: string;
  description: string;
  sheet: string;
  dnp: boolean;
  parameters: ImportedBomNormalized_RecordString;
  canonical_fields: ImportedBomNormalized_RecordString;
  field_sources: ImportedBomNormalized_RecordString;
}
export interface ImportedBomNormalized_RecordString {
  [k: string]: string;
}
