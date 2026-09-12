/** Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit. */

export interface McoExecution {
  /**
   * Existing execution reports reuse the input schema tag; the contract file distinguishes the result shape.
   */
  schema: "altium_cruncher.mco.a0";
  ok: boolean;
  dry_run: boolean;
  results: McoOperationResult[];
}
export interface McoOperationResult {
  op: string;
  id: string;
  status: "ok" | "fail";
  message: string;
  outputs: RecordUnknown;
  error?: string;
}
/**
 * Operation-specific results; custom registries own their output payloads.
 */
export interface RecordUnknown {
  [k: string]: unknown;
}
