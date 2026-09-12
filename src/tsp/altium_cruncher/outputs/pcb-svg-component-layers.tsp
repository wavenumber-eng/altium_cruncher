import "@typespec/json-schema";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.PcbSvgComponentLayersContract;

model PcbSvgComponentLayersLayersItemInstancesItemBodiesItem
  extends Record<unknown> {
  index: integer;
  kind: "step" | "extruded";
  lower_z_mm: float64;
  upper_z_mm: float64;

  @extension("minItems", 3)
  @extension("maxItems", 3)
  color: float64[] | null;

  @extension("minimum", 0)
  @extension("maximum", 1)
  opacity: float64;
}

model PcbSvgComponentLayersLayersItemInstancesItem extends Record<unknown> {
  group_id: string;
  component_index: integer | null;
  designator: string;
  side?: "top" | "bottom";
  symbol_id?: string;

  @extension("minItems", 2)
  @extension("maxItems", 2)
  anchor_svg_mm?: float64[];

  @extension("minItems", 2)
  @extension("maxItems", 2)
  anchor_board_mm?: float64[];

  @extension("minItems", 6)
  @extension("maxItems", 6)
  bounds_local_xyz_mm?: float64[];

  bodies?: PcbSvgComponentLayersLayersItemInstancesItemBodiesItem[];

  @extension("minimum", 0)
  paint_order?: integer;

  geometry_source?: "model" | "pads";

  @extension("minItems", 2)
  @extension("maxItems", 2)
  center_view_mm?: float64[];

  @extension("exclusiveMinimum", 0)
  font_size_mm?: float64;

  rotation_degrees?: float64;
}

model PcbSvgComponentLayersLayersItem extends Record<unknown> {
  token:
    | "ILLUSTRATION_TOP"
    | "ILLUSTRATION_BOTTOM"
    | "ASSEMBLY_DESIGNATORS_TOP"
    | "ASSEMBLY_DESIGNATORS_BOTTOM";
  group_id: string;
  side: "top" | "bottom";
  instances: PcbSvgComponentLayersLayersItemInstancesItem[];

  @extension("minimum", 0)
  unique_symbols?: integer;
}

@jsonSchema
@id("pcb.svg.component-layers.a0")
@extension("title", "PCB SVG component layer metadata extension")
model PcbSvgComponentLayers extends Record<unknown> {
  schema: "pcb.svg.component-layers.a0";
  coordinate_policy: string;
  layers: PcbSvgComponentLayersLayersItem[];
}
