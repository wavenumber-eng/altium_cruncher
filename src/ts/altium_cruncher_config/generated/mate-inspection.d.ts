/** Generated from src/tsp/altium_cruncher/outputs/mate.tsp. Do not edit. */

/**
 * @minItems 2
 * @maxItems 2
 */
export type Pair = [number, number];

export interface MateInspection {
  schema: "altium_cruncher.mate.inspect.a0";
  source: string;
  source_tag: string;
  boards: Board[];
}
export interface Board {
  board_key: string;
  pcb_path: string;
  components: Component[];
  free_pads: FreePad[];
  board_outline_mils?: Bounds;
  board_outline?: Outline;
  board_origin_mils?: Point;
}
export interface Component {
  designator: string;
  kind: string;
  layer: string;
  footprint: string;
  x_mils: number;
  y_mils: number;
  net_name?: string;
  source_power_port?: PowerPort;
  source_pad_geometries?: PadGeometry[];
}
export interface PowerPort {
  text: string;
  style: string;
  show_net_name: boolean;
}
export interface PadGeometry {
  x_mils: number;
  y_mils: number;
  width_mils: number;
  height_mils: number;
  shape: number;
  layer: number;
  rotation_degrees: number;
  corner_radius_mils?: number;
}
export interface FreePad {
  designator: string;
  kind: string;
  layer: number;
  x_mils: number;
  y_mils: number;
  width_mils: number;
  height_mils: number;
  hole_size_mils: number;
  plated: boolean;
  shape: number;
  net_name?: string;
  source_power_port?: PowerPort;
}
export interface Bounds {
  left: number;
  bottom: number;
  right: number;
  top: number;
}
export interface Outline {
  vertices: (LineVertex | ArcVertex)[];
  closed: boolean;
  cutouts?: Outline[];
}
export interface LineVertex {
  x_mils: number;
  y_mils: number;
  segment: "line";
}
export interface ArcVertex {
  x_mils: number;
  y_mils: number;
  segment: "arc";
  center_mils: Pair;
  radius_mils: number;
  start_angle_degrees: number;
  end_angle_degrees: number;
}
export interface Point {
  x: number;
  y: number;
}
