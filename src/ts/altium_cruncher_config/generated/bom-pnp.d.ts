/** Generated from src/tsp/altium_cruncher/config/bom-pnp-config.tsp. Do not edit. */

export type BomPnpConfigInputFieldAliases = RecordArrayString & {};
export type BomPnpConfigInputBomPcbLineItemFields = RecordString & {};

export interface BomPnpConfigInput {
  schema?: "altium_cruncher.bom.config.a0" | null;
  field_aliases?: BomPnpConfigInputFieldAliases;
  variants?: BomPnpConfigInputVariants;
  bom?: BomPnpConfigInputBom;
  pnp?: BomPnpConfigInputPnp;
  output?: BomPnpConfigInputOutput;
}
export interface RecordArrayString {
  [k: string]: string[];
}
export interface BomPnpConfigInputVariants {
  mode?: "base" | "all" | "named";
  names?: string[];
  include_base?: boolean;
}
export interface BomPnpConfigInputBom {
  source_mode?: "schematic" | "pcb" | "merged";
  outputs?: ("raw-json" | "legacy-json" | "grouped-json" | "grouped-csv" | "grouped-xlsx" | "jlc-csv" | "jlc-xlsx")[];
  group_fields?: string[];
  output_fields?: string[];
  include_dnp?: boolean;
  split_dnp?: boolean;
  dnp_placement?: "inline" | "end" | "separate";
  highlight_dnp_rows?: boolean;
  prefix_order?: string[];
  pcb_line_item?: BomPnpConfigInputBomPcbLineItem;
}
export interface BomPnpConfigInputBomPcbLineItem {
  enabled?: boolean;
  designator?: string;
  fields?: BomPnpConfigInputBomPcbLineItemFields;
}
export interface RecordString {
  [k: string]: string;
}
export interface BomPnpConfigInputPnp {
  outputs?: ("json" | "csv" | "xlsx" | "jlc-cpl" | "jlc-cpl-xlsx")[];
  output_fields?: string[];
  units?: "mm" | "mils";
  position_mode?: "altium-pick-place" | "component-origin";
  exclude_no_bom?: boolean;
  layer_order?: string[];
  prefix_order?: string[];
}
export interface BomPnpConfigInputOutput {
  dir_template?: string;
  name_template?: string;
}
