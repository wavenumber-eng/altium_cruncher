/** Generated from src/tsp/altium_cruncher/outputs/design-review-manifest.tsp. Do not edit. */
import type { DesignReviewManifest } from './design-review-manifest.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is DesignReviewManifest;
  errors: ConfigError[] | null;
};
export default validate;
