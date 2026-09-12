import "@typespec/json-schema";
import "./creation-defaults.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Creation;

@minLength(1)
scalar NonemptyString extends string;

// Existing creation adapters use Python truthiness, not SVG's yes/no parser.
alias CreationBoolean =
  | boolean
  | string
  | float64
  | null
  | unknown[]
  | Record<unknown>;

model CustomSheetMils extends Record<unknown> {
  @doc("Custom sheet width in mils.")
  width: float64 | boolean;

  @doc("Custom sheet height in mils.")
  height: float64 | boolean;
}

model SchdocChild extends Record<unknown> {
  @doc("SchDoc file to create, relative to this config file unless absolute.")
  file: NonemptyString;

  @doc("Altium SheetStyle enum name or native integer id. Falsy input uses D.")
  sheet_style?: string | integer | boolean | null;

  @doc("Optional SchDot template file to copy settings from.")
  template?: NonemptyString | null;

  @doc("Whether to copy visual sheet settings from the template; legacy JSON truthiness is preserved. Prefer true or false.")
  apply_template_visual_sheet_settings?: CreationBoolean;

  @doc("Optional explicit sheet size in mils.")
  custom_sheet_mils?: CustomSheetMils | null;
}

model BoardOutlineMils extends Record<unknown> {
  left: float64 | boolean;
  bottom: float64 | boolean;
  right: float64 | boolean;
  top: float64 | boolean;
}

model CopperLayer extends Record<unknown> {
  @doc("Copper layer display name.")
  name: NonemptyString;

  @doc("Copper thickness in mils.")
  copper_thickness_mils?: float64 | null;

  @doc("Historical extension field; ignored by creation. Use copper_thickness_mils.")
  thickness_mils?: unknown;

  @doc("Optional native component-placement enum id.")
  component_placement?: integer | null;

  @doc("Optional native copper-orientation enum id.")
  copper_orientation?: integer | null;
}

model DielectricLayer extends Record<unknown> {
  name: NonemptyString;
  material: NonemptyString;
  thickness_mils: float64;
  dielectric_constant: float64;

  @doc("Historical extension field; ignored by creation. Use dielectric_constant.")
  dk?: unknown;

  dielectric_type?: integer | null;

  @doc("Historical extension field; ignored by creation. Use dielectric_type.")
  type_code?: unknown;

  loss_tangent?: float64 | null;
}

model RigidLayerStack extends Record<unknown> {
  @doc("Layer-stack generation mode. Omission or null uses generated_rigid.")
  mode?: "generated_rigid" | null;

  name?: string | null;

  @doc("Copper layers in top-to-bottom order.")
  @minItems(2)
  copper_layers: CopperLayer[];

  @doc("Dielectric layers between adjacent copper layers.")
  dielectrics_between: DielectricLayer[];
}

model MechanicalLayer extends Record<unknown> {
  layer: NonemptyString;
  name?: NonemptyString | null;
  enabled?: CreationBoolean;
  kind?: NonemptyString | null;
}

model MechanicalPairSide extends Record<unknown> {
  ...OmitProperties<MechanicalLayer, "kind">;
  kind: NonemptyString;
}

model GroupedMechanicalPair extends Record<unknown> {
  top: MechanicalPairSide;
  bottom: MechanicalPairSide;
}

model FlatMechanicalPair extends Record<unknown> {
  layer_1: NonemptyString;
  layer_2: NonemptyString;

  @minValue(0)
  pair_index?: integer | null;

  // The adapter chooses grouped form whenever either key is present.
  top?: never;

  bottom?: never;
}

model MechanicalKind extends Record<unknown> {
  layer: NonemptyString;
  kind: NonemptyString | integer;
}

model PcbdocChild extends Record<unknown> {
  @doc("PcbDoc file to create, relative to this config file unless absolute.")
  file: NonemptyString;

  @doc("Optional rectangular board outline in mils.")
  board_outline_mils?: BoardOutlineMils | null;

  @doc("Generated rigid stack; use only one layer-stack input.")
  layer_stack?: RigidLayerStack | null;

  @doc("Named layer-stack template; defaults to 2-layer when no stack input is supplied.")
  layer_stack_template?: string | null;

  @doc("Optional .stackupx path to import as the PcbDoc layer-stack document.")
  stackupx_file?: NonemptyString | null;

  @doc("Optional profile; case, surrounding whitespace and hyphen aliases are accepted.")
  @extension("x-acr-input", "enum")
  mechanical_layer_profile?:
    | "none"
    | ""
    | "standard_component_pairs"
    | "standard-component-pairs"
    | "v7_mechanical_53"
    | "v7-mechanical-53"
    | null;

  mechanical_layers?: MechanicalLayer[] | null;
  mechanical_layer_pairs?:
    | (GroupedMechanicalPair | FlatMechanicalPair)[]
    | null;
  mechanical_layer_kinds?: MechanicalKind[] | null;
}

model ProjectOutput extends Record<unknown> {
  @doc("PrjPcb file to create, relative to this config file unless absolute.")
  file: NonemptyString;

  @doc("Project display name; omission, null or empty derives it from the file.")
  name?: string | null;

  @doc("Project parameters; the Python adapter converts authored values to strings.")
  parameters?: Record<unknown>;
}

@jsonSchema
@id("https://github.com/wavenumber-eng/altium_cruncher/docs/contracts/schdoc_create_config.a0.schema.json")
@extension("x-acr-jsonc-comments", schdocComments)
@extension("x-acr-resolved-defaults", creationDefaults)
model SchdocCreateConfigInput extends Record<unknown> {
  @doc("SchDoc create config contract id.")
  schema: "altium_cruncher.schdoc.create.config.a0";

  ...SchdocChild;
}

@jsonSchema
@id("https://github.com/wavenumber-eng/altium_cruncher/docs/contracts/pcbdoc_create_config.a0.schema.json")
@extension("x-acr-jsonc-comments", pcbdocComments)
@extension("x-acr-jsonc-key-comments", creationKeyComments)
@extension("x-acr-resolved-defaults", creationDefaults)
model PcbdocCreateConfigInput extends Record<unknown> {
  @doc("PcbDoc create config contract id.")
  schema: "altium_cruncher.pcbdoc.create.config.a0";

  ...PcbdocChild;
}

@jsonSchema
@id("https://github.com/wavenumber-eng/altium_cruncher/docs/contracts/project_skeleton_config.a0.schema.json")
@extension("x-acr-jsonc-comments", projectComments)
@extension("x-acr-jsonc-key-comments", creationKeyComments)
@extension("x-acr-resolved-defaults", creationDefaults)
model ProjectSkeletonConfigInput extends Record<unknown> {
  @doc("Project skeleton config contract id.")
  schema: "altium_cruncher.project_skeleton.a0";

  @doc("PrjPcb output and project-level parameters.")
  project: ProjectOutput;

  @doc("SchDoc sheets to create and add to the project. Empty creates no sheets.")
  schematics: SchdocChild[];

  @doc("Optional PcbDoc output; null creates no board.")
  pcb?: PcbdocChild | null;
}
