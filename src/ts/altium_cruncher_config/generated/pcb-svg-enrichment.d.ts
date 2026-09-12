/** Generated from src/tsp/altium_cruncher/outputs/pcb-svg-enrichment.tsp. Do not edit. */

/**
 * Cruncher fields embedded in the Altium Monkey PCB SVG enrichment payload. Other base fields remain upstream-owned; this does not introduce a new wire tag.
 */
export type PcbSvgEnrichment = RecordUnknown & {
  canvas: Canvas;
  virtual_component_layers?: PCBSVGComponentLayerMetadataExtension;
};
/**
 * @minItems 4
 * @maxItems 4
 */
export type Bounds = [number, number, number, number];
/**
 * @minItems 2
 * @maxItems 2
 */
export type Pair = [number, number];
export type PCBSVGComponentLayerMetadataExtension = ImportedPcbSvgComponentLayers_RecordUnknown;

export interface RecordUnknown {
  [k: string]: unknown;
}
export interface Canvas {
  bounds_mode: "all_geometry" | "board_outline";
  bounds_mils: Bounds;
  margin_mm: number;
  altium_origin_mils: Pair;
  svg_units: "mm";
  geometry_transform: {
    x_svg_mm: string;
    y_svg_mm: string;
  };
  metadata_coordinate_policy: string;
  view_box_mm?: Bounds;
  scene_mirror_x?: boolean;
  scene_mirror_width_mm?: number;
}
export interface ImportedPcbSvgComponentLayers_RecordUnknown {
  [k: string]: unknown;
}
