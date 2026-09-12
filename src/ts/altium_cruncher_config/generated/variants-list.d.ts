/** Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit. */

export type Count = number;

export interface VariantsList {
  schema: "altium_cruncher.variants.list.a0";
  project: string;
  current_variant: string | null;
  variant_count: Count;
  variants: Variant[];
  rows: VariantRow[];
  index_errors: string[];
}
export interface Variant {
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
export interface VariantRow {
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
