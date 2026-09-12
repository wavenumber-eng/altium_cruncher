import "@typespec/json-schema";
import "./pcb-svg-component-layers.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.PcbSvgEnrichmentContract;

@minItems(2)
@maxItems(2)
model Pair is float64[];
@minItems(4)
@maxItems(4)
model Bounds is float64[];
model Canvas {
  bounds_mode: "all_geometry" | "board_outline";
  bounds_mils: Bounds;
  margin_mm: float64;
  altium_origin_mils: Pair;
  svg_units: "mm";
  geometry_transform: {
    x_svg_mm: string;
    y_svg_mm: string;
  };
  metadata_coordinate_policy: string;
  view_box_mm?: Bounds;
  scene_mirror_x?: boolean;
  scene_mirror_width_mm?: float64;
}
@jsonSchema
@id("altium_cruncher.pcb_svg.enrichment_extension.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "pcb_svg_enrichment",
    title: "Cruncher PCB SVG metadata extensions",
    source: "../outputs/pcb-svg-enrichment",
    kind: "output",
  }
)
@doc("Cruncher fields embedded in the Altium Monkey PCB SVG enrichment payload. Other base fields remain upstream-owned; this does not introduce a new wire tag.")
model PcbSvgEnrichment extends Record<unknown> {
  canvas: Canvas;
  virtual_component_layers?: Wavenumber.AltiumCruncher.PcbSvgComponentLayersContract.PcbSvgComponentLayers;
}
