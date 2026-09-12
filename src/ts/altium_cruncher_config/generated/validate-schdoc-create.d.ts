/** Generated from src/tsp/altium_cruncher/config/creation.tsp. Do not edit. */
import type { SchdocCreateConfigInput } from './schdoc-create.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is SchdocCreateConfigInput;
  errors: ConfigError[] | null;
};
export default validate;
