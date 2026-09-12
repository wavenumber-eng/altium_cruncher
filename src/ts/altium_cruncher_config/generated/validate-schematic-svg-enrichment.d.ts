/** Generated from src/tsp/altium_cruncher/outputs/schematic-svg-enrichment.tsp. Do not edit. */
import type { SchematicSvgEnrichment } from './schematic-svg-enrichment.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is SchematicSvgEnrichment;
  errors: ConfigError[] | null;
};
export default validate;
