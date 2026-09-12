/** Authored creation configs; document generation and MCO compilation stay in Python. */
import { decodeConfig } from "./_runtime.js";
import validateSchdocCreate from "./generated/validate-schdoc-create.js";
import type { SchdocCreateConfigInput } from "./generated/schdoc-create.js";
export type { SchdocCreateConfigInput } from "./generated/schdoc-create.js";
import validatePcbdocCreate from "./generated/validate-pcbdoc-create.js";
import type { PcbdocCreateConfigInput } from "./generated/pcbdoc-create.js";
export type { PcbdocCreateConfigInput } from "./generated/pcbdoc-create.js";
import validateProjectSkeleton from "./generated/validate-project-skeleton.js";
import type { ProjectSkeletonConfigInput } from "./generated/project-skeleton.js";
export type { ProjectSkeletonConfigInput } from "./generated/project-skeleton.js";

export function decodeSchdocCreateConfig(value: unknown): SchdocCreateConfigInput {
  return decodeConfig(value, validateSchdocCreate, "schdoc-create");
}
export function encodeSchdocCreateConfig(value: SchdocCreateConfigInput): string {
  return JSON.stringify(decodeSchdocCreateConfig(value), null, 2) + "\n";
}

export function decodePcbdocCreateConfig(value: unknown): PcbdocCreateConfigInput {
  return decodeConfig(value, validatePcbdocCreate, "pcbdoc-create");
}
export function encodePcbdocCreateConfig(value: PcbdocCreateConfigInput): string {
  return JSON.stringify(decodePcbdocCreateConfig(value), null, 2) + "\n";
}

export function decodeProjectSkeletonConfig(value: unknown): ProjectSkeletonConfigInput {
  return decodeConfig(value, validateProjectSkeleton, "project-skeleton");
}
export function encodeProjectSkeletonConfig(value: ProjectSkeletonConfigInput): string {
  return JSON.stringify(decodeProjectSkeletonConfig(value), null, 2) + "\n";
}
