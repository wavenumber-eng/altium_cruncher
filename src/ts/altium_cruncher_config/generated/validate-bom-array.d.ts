/** Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit. */
import type { BomArray } from './bom-array.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is BomArray;
  errors: ConfigError[] | null;
};
export default validate;
