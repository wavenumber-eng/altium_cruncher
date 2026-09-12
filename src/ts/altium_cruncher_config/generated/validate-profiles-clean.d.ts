/** Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit. */
import type { ProfilesClean } from './profiles-clean.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is ProfilesClean;
  errors: ConfigError[] | null;
};
export default validate;
