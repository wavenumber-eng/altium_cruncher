/** Generated from src/tsp/altium_cruncher/outputs/schematic-svg-manifest.tsp. Do not edit. */
import type { SchematicSvgManifest } from './schematic-svg-manifest.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is SchematicSvgManifest;
  errors: ConfigError[] | null;
};
export default validate;
