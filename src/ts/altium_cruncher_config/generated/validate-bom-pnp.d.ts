/** Generated from src/tsp/altium_cruncher/config/bom-pnp-config.tsp. Do not edit. */
import type { BomPnpConfigInput } from './bom-pnp.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is BomPnpConfigInput;
  errors: ConfigError[] | null;
};
export default validate;
