/** Generated from src/tsp/altium_cruncher/outputs/easyeda.tsp. Do not edit. */

/**
 * @minItems 4
 * @maxItems 4
 */
export type BoundsArray = [number, number, number, number];

export interface EasyedaModels {
  schema: "altium_cruncher.easyeda.3d_models.a0";
  lcsc_id: string;
  placement_implemented: boolean;
  placement_note: string;
  models: ModelReference[];
  placement_verdict?: string;
  placement_check?: PlacementCheck;
}
export interface ModelReference {
  uuid: string;
  title: string;
  origin: string;
  z: string;
  rotation: string;
  files: RecordString;
  errors: RecordString;
  placement_status: string;
}
export interface RecordString {
  [k: string]: string;
}
export interface PlacementCheck {
  verdict?: "ok" | "needs_checking";
  checked?: boolean;
  reason?: string;
  center_distance_mils?: number;
  distance_ratio?: number;
  model_bounds_mils?: BoundsArray;
  pad_bounds_mils?: BoundsArray;
}
