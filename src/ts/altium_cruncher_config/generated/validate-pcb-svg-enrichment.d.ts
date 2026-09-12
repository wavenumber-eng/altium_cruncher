/** Generated from src/tsp/altium_cruncher/outputs/pcb-svg-enrichment.tsp. Do not edit. */
import type { PcbSvgEnrichment } from './pcb-svg-enrichment.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is PcbSvgEnrichment;
  errors: ConfigError[] | null;
};
export default validate;
