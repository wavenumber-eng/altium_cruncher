/** Generated from src/tsp/altium_cruncher/config/mate-config.tsp. Do not edit. */
import type { MatePartsInput } from './mate-parts-input.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is MatePartsInput;
  errors: ConfigError[] | null;
};
export default validate;
