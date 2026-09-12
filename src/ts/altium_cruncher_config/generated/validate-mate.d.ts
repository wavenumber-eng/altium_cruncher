/** Generated from src/tsp/altium_cruncher/config/mate-config.tsp. Do not edit. */
import type { MateConfigInput } from './mate.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is MateConfigInput;
  errors: ConfigError[] | null;
};
export default validate;
