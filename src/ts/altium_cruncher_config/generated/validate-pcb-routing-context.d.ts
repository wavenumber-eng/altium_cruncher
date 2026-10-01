/** Generated from src/tsp/altium_cruncher/outputs/pcb-routing-context.tsp. Do not edit. */
import type { PcbRoutingContext } from './pcb-routing-context.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is PcbRoutingContext;
  errors: ConfigError[] | null;
};
export default validate;
