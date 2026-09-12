/** Generated from src/tsp/altium_cruncher/outputs/pcb-svg-component-layers.tsp. Do not edit. */

export type PcbSvgComponentLayers = RecordUnknown & {
  schema: "pcb.svg.component-layers.a0";
  coordinate_policy: string;
  layers: PcbSvgComponentLayersLayersItem[];
};
export type PcbSvgComponentLayersLayersItem = RecordUnknown & {
  token: "ILLUSTRATION_TOP" | "ILLUSTRATION_BOTTOM" | "ASSEMBLY_DESIGNATORS_TOP" | "ASSEMBLY_DESIGNATORS_BOTTOM";
  group_id: string;
  side: "top" | "bottom";
  instances: PcbSvgComponentLayersLayersItemInstancesItem[];
  unique_symbols?: number;
};
export type PcbSvgComponentLayersLayersItemInstancesItem = RecordUnknown & {
  group_id: string;
  component_index: number | null;
  designator: string;
  side?: "top" | "bottom";
  symbol_id?: string;
  /**
   * @minItems 2
   * @maxItems 2
   */
  anchor_svg_mm?: [number, number];
  /**
   * @minItems 2
   * @maxItems 2
   */
  anchor_board_mm?: [number, number];
  /**
   * @minItems 6
   * @maxItems 6
   */
  bounds_local_xyz_mm?: [number, number, number, number, number, number];
  bodies?: PcbSvgComponentLayersLayersItemInstancesItemBodiesItem[];
  paint_order?: number;
  geometry_source?: "model" | "pads";
  /**
   * @minItems 2
   * @maxItems 2
   */
  center_view_mm?: [number, number];
  font_size_mm?: number;
  rotation_degrees?: number;
};
export type PcbSvgComponentLayersLayersItemInstancesItemBodiesItem = RecordUnknown & {
  index: number;
  kind: "step" | "extruded";
  lower_z_mm: number;
  upper_z_mm: number;
  color: number[] | null;
  opacity: number;
};

export interface RecordUnknown {
  [k: string]: unknown;
}
