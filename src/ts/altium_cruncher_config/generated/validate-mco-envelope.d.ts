/** Generated from src/tsp/altium_cruncher/mco/main.tsp. Do not edit. */
import type { McoEnvelopeInput } from './mco-envelope.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is McoEnvelopeInput;
  errors: ConfigError[] | null;
};
export default validate;
