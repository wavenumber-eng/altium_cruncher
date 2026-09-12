/** Generated from src/tsp/altium_cruncher/outputs/easyeda.tsp. Do not edit. */
import type { EasyedaFootprintReport } from './easyeda-footprint-report.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is EasyedaFootprintReport;
  errors: ConfigError[] | null;
};
export default validate;
