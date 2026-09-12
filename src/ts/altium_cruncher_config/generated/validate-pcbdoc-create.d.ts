/** Generated from src/tsp/altium_cruncher/config/creation.tsp. Do not edit. */
import type { PcbdocCreateConfigInput } from './pcbdoc-create.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is PcbdocCreateConfigInput;
  errors: ConfigError[] | null;
};
export default validate;
