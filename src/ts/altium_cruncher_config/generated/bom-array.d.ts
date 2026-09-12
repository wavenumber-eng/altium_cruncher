/** Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit. */

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
export type BomArray = RawBomComponent[];

export interface RecordUnknown {
  [k: string]: unknown;
}
