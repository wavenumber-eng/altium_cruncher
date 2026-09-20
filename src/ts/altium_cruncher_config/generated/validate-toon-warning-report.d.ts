/** Generated from src/tsp/altium_cruncher/outputs/toon-warning-report.tsp. Do not edit. */
import type { ToonWarningReport } from './toon-warning-report.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is ToonWarningReport;
  errors: ConfigError[] | null;
};
export default validate;
