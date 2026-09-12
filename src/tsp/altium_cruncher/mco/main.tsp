import "./operations/file-copy.tsp";
import "./operations/mco-fail.tsp";
import "./operations/mco-message.tsp";
import "./operations/pcbdoc-add_arc.tsp";
import "./operations/pcbdoc-add_component.tsp";
import "./operations/pcbdoc-add_embedded_3d_model.tsp";
import "./operations/pcbdoc-add_fill.tsp";
import "./operations/pcbdoc-add_pad.tsp";
import "./operations/pcbdoc-add_region.tsp";
import "./operations/pcbdoc-add_text.tsp";
import "./operations/pcbdoc-add_track.tsp";
import "./operations/pcbdoc-add_via.tsp";
import "./operations/pcbdoc-arrange_designators.tsp";
import "./operations/pcbdoc-create.tsp";
import "./operations/pcbdoc-create_user_union.tsp";
import "./operations/pcbdoc-export_layer_step.tsp";
import "./operations/pcblib-add_footprint.tsp";
import "./operations/pcblib-create.tsp";
import "./operations/project-add_document.tsp";
import "./operations/project-add_parameter.tsp";
import "./operations/project-add_variant.tsp";
import "./operations/project-add_variant_dnp.tsp";
import "./operations/project-clone_variant.tsp";
import "./operations/project-create.tsp";
import "./operations/project-delete_variant.tsp";
import "./operations/project-list_variants.tsp";
import "./operations/project-rename_variant.tsp";
import "./operations/project-toggle_variant_dnp.tsp";
import "./operations/schdoc-add_component.tsp";
import "./operations/schdoc-add_net_label.tsp";
import "./operations/schdoc-add_power_port.tsp";
import "./operations/schdoc-add_wire.tsp";
import "./operations/schdoc-create.tsp";
import "./operations/schlib-add_symbol.tsp";
import "./operations/schlib-create.tsp";
import "./defaults.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

union BuiltinOperation {
  FileCopyOperation,
  McoFailOperation,
  McoMessageOperation,
  PcbdocAddArcOperation,
  PcbdocAddComponentOperation,
  PcbdocAddEmbedded3dModelOperation,
  PcbdocAddFillOperation,
  PcbdocAddPadOperation,
  PcbdocAddRegionOperation,
  PcbdocAddTextOperation,
  PcbdocAddTrackOperation,
  PcbdocAddViaOperation,
  PcbdocArrangeDesignatorsOperation,
  PcbdocCreateOperation,
  PcbdocCreateUserUnionOperation,
  PcbdocExportLayerStepOperation,
  PcblibAddFootprintOperation,
  PcblibCreateOperation,
  ProjectAddDocumentOperation,
  ProjectAddParameterOperation,
  ProjectAddVariantOperation,
  ProjectAddVariantDnpOperation,
  ProjectCloneVariantOperation,
  ProjectCreateOperation,
  ProjectDeleteVariantOperation,
  ProjectListVariantsOperation,
  ProjectRenameVariantOperation,
  ProjectToggleVariantDnpOperation,
  SchdocAddComponentOperation,
  SchdocAddNetLabelOperation,
  SchdocAddPowerPortOperation,
  SchdocAddWireOperation,
  SchdocCreateOperation,
  SchlibAddSymbolOperation,
  SchlibCreateOperation,
}

model CustomOperation extends Record<unknown> {
  ...OperationFields;

  @doc("Custom registry operation name; built-in names are excluded during generation.")
  @extension("x-acr-custom-op", true)
  `op`: McoString;

  args?: Record<unknown>;
}

model McoDocument extends Record<unknown> {
  schema?: "altium_cruncher.mco.a0" | null;
  operations: (BuiltinOperation | CustomOperation)[];
}

@jsonSchema
@id("https://github.com/wavenumber-eng/altium_cruncher/docs/contracts/mco_input.a0.schema.json")
@extension("x-acr-schema", "altium_cruncher.mco.a0")
@extension("x-acr-template", mcoTemplate)
@extension("x-acr-jsonc-key-comments", mcoKeyComments)
@extension("x-acr-jsonc-comments", mcoPathComments)
union McoInput {
  document: McoDocument,
  operations: (BuiltinOperation | CustomOperation)[],
}

model McoEnvelopeDocument extends Record<unknown> {
  schema?: "altium_cruncher.mco.a0" | null;
  operations: OpenOperation[];
}

@jsonSchema
@id("https://github.com/wavenumber-eng/altium_cruncher/docs/contracts/mco_envelope.a0.schema.json")
@extension("x-acr-schema", "altium_cruncher.mco.a0")
union McoEnvelopeInput {
  document: McoEnvelopeDocument,
  operations: OpenOperation[],
}
