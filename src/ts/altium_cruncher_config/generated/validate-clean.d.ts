/** Generated from src/tsp/altium_cruncher/config/clean-config.tsp. Do not edit. */
import type { CleanConfigInput } from './clean.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is CleanConfigInput;
  errors: ConfigError[] | null;
};
export default validate;
