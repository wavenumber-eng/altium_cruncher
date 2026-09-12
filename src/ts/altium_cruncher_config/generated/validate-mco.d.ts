/** Generated from src/tsp/altium_cruncher/mco/main.tsp. Do not edit. */
import type { McoInput } from './mco.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is McoInput;
  errors: ConfigError[] | null;
};
export default validate;
