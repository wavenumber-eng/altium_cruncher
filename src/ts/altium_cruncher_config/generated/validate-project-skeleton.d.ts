/** Generated from src/tsp/altium_cruncher/config/creation.tsp. Do not edit. */
import type { ProjectSkeletonConfigInput } from './project-skeleton.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is ProjectSkeletonConfigInput;
  errors: ConfigError[] | null;
};
export default validate;
