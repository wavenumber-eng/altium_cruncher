/** Generated from src/tsp/altium_cruncher/outputs/mate.tsp. Do not edit. */
import type { MateInspection } from './mate-inspection.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is MateInspection;
  errors: ConfigError[] | null;
};
export default validate;
