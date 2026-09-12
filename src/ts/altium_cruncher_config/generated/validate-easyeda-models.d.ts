/** Generated from src/tsp/altium_cruncher/outputs/easyeda.tsp. Do not edit. */
import type { EasyedaModels } from './easyeda-models.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is EasyedaModels;
  errors: ConfigError[] | null;
};
export default validate;
