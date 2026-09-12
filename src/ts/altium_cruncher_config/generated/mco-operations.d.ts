/** Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit. */

export interface McoOperations {
  schema: "altium_cruncher.mco.operations.a0";
  operations: McoCatalogEntry[];
}
export interface McoCatalogEntry {
  op: string;
  group: string;
  summary: string;
  required_args: string[];
  optional_args: string[];
  aliases?: string[];
}
