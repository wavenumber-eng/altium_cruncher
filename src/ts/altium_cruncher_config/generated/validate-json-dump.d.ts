/** Generated from src/tsp/altium_cruncher/outputs/json-dump.tsp. Do not edit. */
import type { JsonDump } from './json-dump.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is JsonDump;
  errors: ConfigError[] | null;
};
export default validate;
