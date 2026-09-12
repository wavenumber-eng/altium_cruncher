/** Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit. */
import type { LibrariesScan } from './libraries-scan.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is LibrariesScan;
  errors: ConfigError[] | null;
};
export default validate;
