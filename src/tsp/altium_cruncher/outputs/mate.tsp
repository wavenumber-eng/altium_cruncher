import "@typespec/json-schema";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.MateGeometry;

@minItems(2)
@maxItems(2)
model Pair is float64[];
model Point {
  x: float64;
  y: float64;
}
model Bounds {
  left: float64;
  bottom: float64;
  right: float64;
  top: float64;
}
model LineVertex {
  x_mils: float64;
  y_mils: float64;
  segment: "line";
}
model ArcVertex {
  x_mils: float64;
  y_mils: float64;
  segment: "arc";
  center_mils: Pair;
  radius_mils: float64;
  start_angle_degrees: float64;
  end_angle_degrees: float64;
}
alias Vertex = LineVertex | ArcVertex;
model Outline {
  vertices: Vertex[];
  closed: boolean;
  cutouts?: Outline[];
}
model PowerPort {
  text: string;
  style: string;
  show_net_name: boolean;
}
model PadGeometry {
  x_mils: float64;
  y_mils: float64;
  width_mils: float64;
  height_mils: float64;
  shape: integer;
  layer: integer;
  rotation_degrees: float64;
  corner_radius_mils?: float64;
}
model Component {
  designator: string;
  kind: string;
  layer: string;
  footprint: string;
  x_mils: float64;
  y_mils: float64;
  net_name?: string;
  source_power_port?: PowerPort;
  source_pad_geometries?: PadGeometry[];
}
model FreePad {
  designator: string;
  kind: string;
  layer: integer;
  x_mils: float64;
  y_mils: float64;
  width_mils: float64;
  height_mils: float64;
  hole_size_mils: float64;
  plated: boolean;
  shape: integer;
  net_name?: string;
  source_power_port?: PowerPort;
}
model Board {
  board_key: string;
  pcb_path: string;
  components: Component[];
  free_pads: FreePad[];
  board_outline_mils?: Bounds;
  board_outline?: Outline;
  board_origin_mils?: Point;
}
@jsonSchema
@id("altium_cruncher.mate.inspect.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "mate_inspection",
    title: "Mate inspection",
    source: "../outputs/mate",
    kind: "output",
  }
)
model MateInspection {
  schema: "altium_cruncher.mate.inspect.a0";
  source: string;
  source_tag: string;
  boards: Board[];
}
model KnownPart {
  role: string;
  description: string;
  symbol_name: string;
  symbol_library: string;
  footprint_name: string;
  footprint_library: string;
  target_kinds: string[];
  designator_prefix: string;
  signal_pad_designator: string | null;
}
model PartSource {
  kind: string;
  project: string;
}
@jsonSchema
@id("altium_cruncher.mate.parts_cache.output.a0")
@extension(
  "x-acr-contract",
  #{
    stem: "mate_parts_manifest",
    title: "Generated mate parts manifest",
    source: "../outputs/mate",
    kind: "output",
  }
)
model MatePartsManifest {
  schema: "altium_cruncher.mate.parts_cache.a0";
  source: PartSource;
  parts: KnownPart[];
  designator_normalization: Record<Record<string>>;
}
