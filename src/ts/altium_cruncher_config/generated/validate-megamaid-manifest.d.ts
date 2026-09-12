/** Generated from src/tsp/altium_cruncher/outputs/megamaid-manifest.tsp. Do not edit. */
import type { MegamaidManifest } from './megamaid-manifest.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is MegamaidManifest;
  errors: ConfigError[] | null;
};
export default validate;
