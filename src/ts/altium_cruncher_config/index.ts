/** Authored PCB SVG/Toon config transport. Preset resolution belongs to the CLI. */
import { decodeConfig } from "./_runtime.js";
import validate from "./generated/validate.js";
import type { PcbSvgConfigInput } from "./generated/pcb-svg.js";

export type * from "./generated/pcb-svg.js";
export { validate };

export function decodePcbSvgConfig(value: unknown): PcbSvgConfigInput {
  return decodeConfig(value, validate, "PCB SVG");
}

export function encodePcbSvgConfig(value: PcbSvgConfigInput): string {
  return JSON.stringify(decodePcbSvgConfig(value), null, 2) + "\n";
}

export * from "./creation.js";
export * from "./mco.js";
export * from "./generated/public.js";
