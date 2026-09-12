import type { PcbSvgConfigInput } from "../../src/ts/altium_cruncher_config/index.js";
import { decodeContract } from "../../src/ts/altium_cruncher_config/index.js";

const builtinResult = decodeContract("mco_builtin_result", {} as unknown);
if (builtinResult.status === "ok" && builtinResult.op === "pcbdoc.add_via") {
  const position: number[] = builtinResult.outputs.position_mils;
  // @ts-expect-error A point cannot become an untyped nested dictionary.
  const invalidPosition: string = builtinResult.outputs.position_mils;
  void [position, invalidPosition];
}

declare const config: PcbSvgConfigInput;
const label: boolean | string | number | null | undefined = config.components?.J1?.show_designator;
const extension: unknown = config.global?.styles?.custom?.["vendor"];
const input: PcbSvgConfigInput = {
  components: { J1: { show_designator: false } },
  global: { styles: { custom: { vendor: { nested: 1 } } } },
};
// Record values must retain their type, not degrade to an empty interface/unknown.
// @ts-expect-error An array is not a component override.
const bad: PcbSvgConfigInput = { components: { J1: [] } };
void [label, extension, input, bad];

import type { ProjectSkeletonConfigInput, PcbdocCreateConfigInput } from "../../src/ts/altium_cruncher_config/index.js";
import type { FlatMechanicalPair } from "../../src/ts/altium_cruncher_config/generated/pcbdoc-create.js";
const project: ProjectSkeletonConfigInput = {
  schema: "altium_cruncher.project_skeleton.a0", project: {file: "a.PrjPcb", parameters: {Count: 2}},
  schematics: [], pcb: null, editor: {expanded: false},
};
const pcb: PcbdocCreateConfigInput = {
  schema: "altium_cruncher.pcbdoc.create.config.a0", file: "a.PcbDoc",
  mechanical_layer_kinds: [{layer: "MECHANICAL2", kind: 0}],
};
// @ts-expect-error A creation config requires a file.
const missingFile: PcbdocCreateConfigInput = {schema: "altium_cruncher.pcbdoc.create.config.a0"};
// @ts-expect-error Presence of top selects grouped form, never a flat pair.
const badPair: FlatMechanicalPair = {layer_1: "MECHANICAL10", layer_2: "MECHANICAL11", top: {}};
void [project, pcb, missingFile, badPair];

import type { BuiltinOperation, McoDocument } from "../../src/ts/altium_cruncher_config/index.js";
declare const operation: BuiltinOperation;
if (operation.op === "pcbdoc.add_text") {
  const height: number = operation.args.height_mils;
  const text: string = operation.args.text;
  void [height, text];
}
// @ts-expect-error add_text requires height_mils.
const missingHeight: BuiltinOperation = {op: "pcbdoc.add_text", args: {file: "a.PcbDoc", text: "Hi", position_mils: [0, 0]}};
// @ts-expect-error The container requires its ordered operation list.
const missingOperations: McoDocument = {schema: "altium_cruncher.mco.a0"};
void [missingHeight, missingOperations];
