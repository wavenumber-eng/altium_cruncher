/** Generated from src/tsp/altium_cruncher/outputs/mco-builtins.tsp. Do not edit. */
import type { McoBuiltinResult } from './mco-builtin-result.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is McoBuiltinResult;
  errors: ConfigError[] | null;
};
export default validate;
