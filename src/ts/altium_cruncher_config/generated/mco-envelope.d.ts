/** Generated from src/tsp/altium_cruncher/mco/main.tsp. Do not edit. */

export type McoEnvelopeInput = McoEnvelopeDocument | OpenOperation[];
export type McoEnvelopeDocument = RecordUnknown & {
  schema?: "altium_cruncher.mco.a0" | null;
  operations: OpenOperation[];
};
export type OpenOperation = RecordUnknown & {
  /**
   * Stable operation ID; omission, null or empty generates opN in source order.
   */
  id?: string | null;
  /**
   * Optional human-readable operation message.
   */
  message?: string | null;
  /**
   * Operation ID to jump to on failure. Null/omission stops on failure.
   */
  on_fail?: string | null;
  op: McoString;
  args?: RecordUnknown;
};
export type McoString = string;

export interface RecordUnknown {
  [k: string]: unknown;
}
