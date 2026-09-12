/** Full authored MCO validation; runtime branching and custom handlers stay in Python. */
import { decodeConfig } from "./_runtime.js";
import validate from "./generated/validate-mco.js";
import type { McoInput } from "./generated/mco.js";
export type { McoInput, McoDocument, BuiltinOperation, CustomOperation } from "./generated/mco.js";

export function decodeMco(value: unknown): McoInput {
  return decodeConfig(value, validate, "MCO");
}

export function encodeMco(value: McoInput): string {
  return JSON.stringify(decodeMco(value), null, 2) + "\n";
}
