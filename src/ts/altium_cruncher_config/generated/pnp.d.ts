/** Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit. */

export type Count = number;

export interface Pnp {
  schema: "altium_cruncher.pnp.a0";
  source: Source;
  variant: string | null;
  units: "mm" | "mils";
  position_mode: "altium-pick-place" | "component-origin";
  placement_count: Count;
  placements: Placement[];
}
export interface Source {
  path: string;
  name: string;
  stem: string;
}
export interface Placement {
  designator: string;
  comment: string;
  layer: string;
  footprint: string;
  center_x: number;
  center_y: number;
  rotation: number;
  units: string;
  description: string;
  parameters: RecordString;
  canonical_fields: RecordString;
  field_sources: RecordString;
}
export interface RecordString {
  [k: string]: string;
}
