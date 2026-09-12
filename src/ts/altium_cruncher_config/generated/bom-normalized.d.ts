/** Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit. */

export type Count = number;

export interface BomNormalized {
  schema: "altium_cruncher.bom.raw.a0";
  source: Source;
  variant: string | null;
  component_count: Count;
  dnp_count: Count;
  components: NormalizedBomComponent[];
}
export interface Source {
  path: string;
  name: string;
  stem: string;
}
export interface NormalizedBomComponent {
  designator: string;
  value: string;
  footprint: string;
  library_ref: string;
  description: string;
  sheet: string;
  dnp: boolean;
  parameters: RecordString;
  canonical_fields: RecordString;
  field_sources: RecordString;
}
export interface RecordString {
  [k: string]: string;
}
