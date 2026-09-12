/** Generated from src/tsp/altium_cruncher/outputs/mate.tsp. Do not edit. */
import type { MatePartsManifest } from './mate-parts-manifest.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is MatePartsManifest;
  errors: ConfigError[] | null;
};
export default validate;
