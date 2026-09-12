/** Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit. */
import type { McoOperations } from './mco-operations.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is McoOperations;
  errors: ConfigError[] | null;
};
export default validate;
