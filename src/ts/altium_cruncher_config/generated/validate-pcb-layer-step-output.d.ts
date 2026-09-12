/** Generated from src/tsp/altium_cruncher/outputs/pcb-layer-step.tsp. Do not edit. */
import type { PcbLayerStepManifest } from './pcb-layer-step-output.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is PcbLayerStepManifest;
  errors: ConfigError[] | null;
};
export default validate;
