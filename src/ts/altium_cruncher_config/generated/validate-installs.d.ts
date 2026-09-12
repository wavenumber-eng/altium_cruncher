/** Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit. */
import type { Installs } from './installs.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is Installs;
  errors: ConfigError[] | null;
};
export default validate;
