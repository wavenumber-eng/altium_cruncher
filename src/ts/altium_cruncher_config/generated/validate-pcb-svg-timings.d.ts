/** Generated from src/tsp/altium_cruncher/outputs/pcb-svg-timings.tsp. Do not edit. */
import type { PcbSvgTimings } from './pcb-svg-timings.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is PcbSvgTimings;
  errors: ConfigError[] | null;
};
export default validate;
