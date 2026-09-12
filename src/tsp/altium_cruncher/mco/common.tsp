import "@typespec/json-schema";
import "../config/creation.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

@minLength(1)
scalar McoString extends string;

@minItems(2)
@maxItems(2)
model PointMils is float64[];

@minItems(2)
model WirePoints is PointMils[];

@minItems(3)
model RegionPoints is PointMils[];

@minItems(4)
@maxItems(4)
model BoundsArray is float64[];

model BoundsObject extends Record<unknown> {
  left: float64;
  bottom: float64;
  right: float64;
  top: float64;
}

// Numeric enum IDs are represented as JSON integers; native names remain semantic.
alias NativeEnum = string | integer;

model OperationFields {
  @doc("Stable operation ID; omission, null or empty generates opN in source order.")
  id?: string | null;

  @doc("Optional human-readable operation message.")
  message?: string | null;

  @doc("Operation ID to jump to on failure. Null/omission stops on failure.")
  on_fail?: string | null;
}

model OpenOperation extends Record<unknown> {
  ...OperationFields;
  `op`: McoString;
  args?: Record<unknown>;
}

model MutationArgs {
  @doc("Input Altium document path, relative to the MCO file directory.")
  file: McoString;

  @doc("Optional output document; otherwise overwrite=true is required.")
  output_file?: string | null;

  @doc("Allow overwriting the input or existing output document.")
  overwrite?: boolean | null = false;
}

model SchematicTextStyle extends Record<unknown> {
  position_mils?: PointMils | null;
  font_name?: string | null = "Arial";
  font_size?: float64 | null = 12;

  @doc("Default is true for designator style and false for comment style.")
  bold?: boolean | null;

  justification?: NativeEnum | null;

  @doc("Explicit hidden takes precedence over visible.")
  hidden?: boolean | null;

  visible?: boolean | null;
}

model McoMechanicalLayer extends Record<unknown> {
  layer: McoString;
  name?: string | null;
  enabled?: boolean | null = true;
}

model McoMechanicalPair extends Record<unknown> {
  layer_1: McoString;
  layer_2: McoString;

  @doc("Defaults to the row's zero-based source index.")
  pair_index?: integer | null;
}

model McoMechanicalKind extends Record<unknown> {
  layer: McoString;
  kind: NativeEnum | boolean;
}

model OriginMils extends Record<unknown> {
  x: float64 | boolean;
  y: float64 | boolean;
}

model SheetFrameMils extends Record<unknown> {
  x: float64 | boolean;
  y: float64 | boolean;
  width: float64 | boolean;
  height: float64 | boolean;
}

model LayerStepHighlight extends Record<unknown> {
  id: McoString;
  name?: string | null;
  color: McoString;

  @doc("Geometry records consumed by the existing STEP exporter; non-object entries are ignored.")
  pad_geometries?: unknown[];

  z_offset_mm?: float64 | null = 0.001;
  thickness_mm?: float64 | null = 0.01;
}
