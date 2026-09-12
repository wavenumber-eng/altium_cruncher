/** Generated from src/tsp/altium_cruncher/outputs/json-dump.tsp. Do not edit. */
import type { JsonDumpManifest } from './json-dump-manifest.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is JsonDumpManifest;
  errors: ConfigError[] | null;
};
export default validate;
