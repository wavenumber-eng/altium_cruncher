/** Generated from src/tsp/altium_cruncher/config/pcb-svg.tsp. Do not edit. */
import type { PcbSvgConfigInput } from './pcb-svg.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is PcbSvgConfigInput;
  errors: ConfigError[] | null;
};
export default validate;
