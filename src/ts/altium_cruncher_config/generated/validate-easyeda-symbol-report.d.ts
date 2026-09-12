/** Generated from src/tsp/altium_cruncher/outputs/easyeda.tsp. Do not edit. */
import type { EasyedaSymbolReport } from './easyeda-symbol-report.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is EasyedaSymbolReport;
  errors: ConfigError[] | null;
};
export default validate;
