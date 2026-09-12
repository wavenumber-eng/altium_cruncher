/** Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit. */

export type Count = number;

export interface BomGrouped {
  schema: "altium_cruncher.bom.grouped.a0";
  source: Source;
  variant: string | null;
  line_count: Count;
  component_count: Count;
  dnp_line_count: Count;
  lines: GroupedBomLine[];
}
export interface Source {
  path: string;
  name: string;
  stem: string;
}
export interface GroupedBomLine {
  item: number;
  quantity: Count;
  designators: string[];
  dnp: boolean;
  fields: RecordString;
}
export interface RecordString {
  [k: string]: string;
}
