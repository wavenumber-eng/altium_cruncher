/** Generated from src/tsp/altium_cruncher/config/pcb-layer-step-config.tsp. Do not edit. */
import type { PcbLayerStepConfigInput } from './pcb-layer-step.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is PcbLayerStepConfigInput;
  errors: ConfigError[] | null;
};
export default validate;
