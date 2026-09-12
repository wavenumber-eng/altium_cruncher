/** Generated from src/tsp/altium_cruncher/outputs/pcb-svg-component-layers.tsp. Do not edit. */
import type { PcbSvgComponentLayers } from './pcb-svg-component-layers.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is PcbSvgComponentLayers;
  errors: ConfigError[] | null;
};
export default validate;
