/** Generated contract transport entry points. Do not edit. */
import { decodeConfig } from "../_runtime.js";
import type { PcbSvgConfigInput } from "./pcb-svg.js";
import PcbSvgConfigInputValidator from "./validate.js";
import type { SchdocCreateConfigInput } from "./schdoc-create.js";
import SchdocCreateConfigInputValidator from "./validate-schdoc-create.js";
import type { PcbdocCreateConfigInput } from "./pcbdoc-create.js";
import PcbdocCreateConfigInputValidator from "./validate-pcbdoc-create.js";
import type { ProjectSkeletonConfigInput } from "./project-skeleton.js";
import ProjectSkeletonConfigInputValidator from "./validate-project-skeleton.js";
import type { McoInput } from "./mco.js";
import McoInputValidator from "./validate-mco.js";
import type { McoEnvelopeInput } from "./mco-envelope.js";
import McoEnvelopeInputValidator from "./validate-mco-envelope.js";
import type { BomPnpConfigInput } from "./bom-pnp.js";
import BomPnpConfigInputValidator from "./validate-bom-pnp.js";
import type { CleanConfigInput } from "./clean.js";
import CleanConfigInputValidator from "./validate-clean.js";
import type { MateConfigInput } from "./mate.js";
import MateConfigInputValidator from "./validate-mate.js";
import type { PcbLayerStepConfigInput } from "./pcb-layer-step.js";
import PcbLayerStepConfigInputValidator from "./validate-pcb-layer-step.js";
import type { DesignReviewManifest } from "./design-review-manifest.js";
import DesignReviewManifestValidator from "./validate-design-review-manifest.js";
import type { MegamaidManifest } from "./megamaid-manifest.js";
import MegamaidManifestValidator from "./validate-megamaid-manifest.js";
import type { SchematicSvgEnrichment } from "./schematic-svg-enrichment.js";
import SchematicSvgEnrichmentValidator from "./validate-schematic-svg-enrichment.js";
import type { SchematicSvgManifest } from "./schematic-svg-manifest.js";
import SchematicSvgManifestValidator from "./validate-schematic-svg-manifest.js";
import type { PcbSvgComponentLayers } from "./pcb-svg-component-layers.js";
import PcbSvgComponentLayersValidator from "./validate-pcb-svg-component-layers.js";
import type { PcbSvgTimings } from "./pcb-svg-timings.js";
import PcbSvgTimingsValidator from "./validate-pcb-svg-timings.js";
import type { BomArray } from "./bom-array.js";
import BomArrayValidator from "./validate-bom-array.js";
import type { BomGrouped } from "./bom-grouped.js";
import BomGroupedValidator from "./validate-bom-grouped.js";
import type { BomLegacy } from "./bom-legacy.js";
import BomLegacyValidator from "./validate-bom-legacy.js";
import type { BomNormalized } from "./bom-normalized.js";
import BomNormalizedValidator from "./validate-bom-normalized.js";
import type { EasyedaFootprintReport } from "./easyeda-footprint-report.js";
import EasyedaFootprintReportValidator from "./validate-easyeda-footprint-report.js";
import type { EasyedaModels } from "./easyeda-models.js";
import EasyedaModelsValidator from "./validate-easyeda-models.js";
import type { EasyedaSymbolReport } from "./easyeda-symbol-report.js";
import EasyedaSymbolReportValidator from "./validate-easyeda-symbol-report.js";
import type { Installs } from "./installs.js";
import InstallsValidator from "./validate-installs.js";
import type { InterfaceDesignManifest } from "./interface-design-manifest.js";
import InterfaceDesignManifestValidator from "./validate-interface-design-manifest.js";
import type { IntlibExtract } from "./intlib-extract.js";
import IntlibExtractValidator from "./validate-intlib-extract.js";
import type { JsonDump } from "./json-dump.js";
import JsonDumpValidator from "./validate-json-dump.js";
import type { JsonDumpManifest } from "./json-dump-manifest.js";
import JsonDumpManifestValidator from "./validate-json-dump-manifest.js";
import type { Launch } from "./launch.js";
import LaunchValidator from "./validate-launch.js";
import type { LibrariesScan } from "./libraries-scan.js";
import LibrariesScanValidator from "./validate-libraries-scan.js";
import type { MateInspection } from "./mate-inspection.js";
import MateInspectionValidator from "./validate-mate-inspection.js";
import type { MatePartsInput } from "./mate-parts-input.js";
import MatePartsInputValidator from "./validate-mate-parts-input.js";
import type { MatePartsManifest } from "./mate-parts-manifest.js";
import MatePartsManifestValidator from "./validate-mate-parts-manifest.js";
import type { McoBuiltinResult } from "./mco-builtin-result.js";
import McoBuiltinResultValidator from "./validate-mco-builtin-result.js";
import type { McoExecution } from "./mco-execution.js";
import McoExecutionValidator from "./validate-mco-execution.js";
import type { McoOperations } from "./mco-operations.js";
import McoOperationsValidator from "./validate-mco-operations.js";
import type { Notes } from "./notes.js";
import NotesValidator from "./validate-notes.js";
import type { OutjobRun } from "./outjob-run.js";
import OutjobRunValidator from "./validate-outjob-run.js";
import type { PcbLayerStepManifest } from "./pcb-layer-step-output.js";
import PcbLayerStepManifestValidator from "./validate-pcb-layer-step-output.js";
import type { PcbSvgEnrichment } from "./pcb-svg-enrichment.js";
import PcbSvgEnrichmentValidator from "./validate-pcb-svg-enrichment.js";
import type { PcbSvgManifest } from "./pcb-svg-manifest.js";
import PcbSvgManifestValidator from "./validate-pcb-svg-manifest.js";
import type { Pnp } from "./pnp.js";
import PnpValidator from "./validate-pnp.js";
import type { Profiles } from "./profiles.js";
import ProfilesValidator from "./validate-profiles.js";
import type { ProfilesClean } from "./profiles-clean.js";
import ProfilesCleanValidator from "./validate-profiles-clean.js";
import type { VariantsList } from "./variants-list.js";
import VariantsListValidator from "./validate-variants-list.js";
export interface ContractTypes {
  "pcb_svg_config": PcbSvgConfigInput;
  "schdoc_create_config": SchdocCreateConfigInput;
  "pcbdoc_create_config": PcbdocCreateConfigInput;
  "project_skeleton_config": ProjectSkeletonConfigInput;
  "mco_input": McoInput;
  "mco_envelope": McoEnvelopeInput;
  "bom_pnp_config": BomPnpConfigInput;
  "clean_config": CleanConfigInput;
  "mate_config": MateConfigInput;
  "pcb_layer_step_config": PcbLayerStepConfigInput;
  "design_review_manifest": DesignReviewManifest;
  "megamaid_manifest": MegamaidManifest;
  "schematic_svg_enrichment": SchematicSvgEnrichment;
  "schematic_svg_manifest": SchematicSvgManifest;
  "pcb_svg_component_layers": PcbSvgComponentLayers;
  "pcb_svg_timings": PcbSvgTimings;
  "bom_array": BomArray;
  "bom_grouped": BomGrouped;
  "bom_legacy": BomLegacy;
  "bom_normalized": BomNormalized;
  "easyeda_footprint_report": EasyedaFootprintReport;
  "easyeda_models": EasyedaModels;
  "easyeda_symbol_report": EasyedaSymbolReport;
  "installs": Installs;
  "interface_design_manifest": InterfaceDesignManifest;
  "intlib_extract": IntlibExtract;
  "json_dump": JsonDump;
  "json_dump_manifest": JsonDumpManifest;
  "launch": Launch;
  "libraries_scan": LibrariesScan;
  "mate_inspection": MateInspection;
  "mate_parts_input": MatePartsInput;
  "mate_parts_manifest": MatePartsManifest;
  "mco_builtin_result": McoBuiltinResult;
  "mco_execution": McoExecution;
  "mco_operations": McoOperations;
  "notes": Notes;
  "outjob_run": OutjobRun;
  "pcb_layer_step": PcbLayerStepManifest;
  "pcb_svg_enrichment": PcbSvgEnrichment;
  "pcb_svg_manifest": PcbSvgManifest;
  "pnp": Pnp;
  "profiles": Profiles;
  "profiles_clean": ProfilesClean;
  "variants_list": VariantsList;
}
const validators = {
  "pcb_svg_config": PcbSvgConfigInputValidator,
  "schdoc_create_config": SchdocCreateConfigInputValidator,
  "pcbdoc_create_config": PcbdocCreateConfigInputValidator,
  "project_skeleton_config": ProjectSkeletonConfigInputValidator,
  "mco_input": McoInputValidator,
  "mco_envelope": McoEnvelopeInputValidator,
  "bom_pnp_config": BomPnpConfigInputValidator,
  "clean_config": CleanConfigInputValidator,
  "mate_config": MateConfigInputValidator,
  "pcb_layer_step_config": PcbLayerStepConfigInputValidator,
  "design_review_manifest": DesignReviewManifestValidator,
  "megamaid_manifest": MegamaidManifestValidator,
  "schematic_svg_enrichment": SchematicSvgEnrichmentValidator,
  "schematic_svg_manifest": SchematicSvgManifestValidator,
  "pcb_svg_component_layers": PcbSvgComponentLayersValidator,
  "pcb_svg_timings": PcbSvgTimingsValidator,
  "bom_array": BomArrayValidator,
  "bom_grouped": BomGroupedValidator,
  "bom_legacy": BomLegacyValidator,
  "bom_normalized": BomNormalizedValidator,
  "easyeda_footprint_report": EasyedaFootprintReportValidator,
  "easyeda_models": EasyedaModelsValidator,
  "easyeda_symbol_report": EasyedaSymbolReportValidator,
  "installs": InstallsValidator,
  "interface_design_manifest": InterfaceDesignManifestValidator,
  "intlib_extract": IntlibExtractValidator,
  "json_dump": JsonDumpValidator,
  "json_dump_manifest": JsonDumpManifestValidator,
  "launch": LaunchValidator,
  "libraries_scan": LibrariesScanValidator,
  "mate_inspection": MateInspectionValidator,
  "mate_parts_input": MatePartsInputValidator,
  "mate_parts_manifest": MatePartsManifestValidator,
  "mco_builtin_result": McoBuiltinResultValidator,
  "mco_execution": McoExecutionValidator,
  "mco_operations": McoOperationsValidator,
  "notes": NotesValidator,
  "outjob_run": OutjobRunValidator,
  "pcb_layer_step": PcbLayerStepManifestValidator,
  "pcb_svg_enrichment": PcbSvgEnrichmentValidator,
  "pcb_svg_manifest": PcbSvgManifestValidator,
  "pnp": PnpValidator,
  "profiles": ProfilesValidator,
  "profiles_clean": ProfilesCleanValidator,
  "variants_list": VariantsListValidator,
};
export function decodeContract<K extends keyof ContractTypes>(name: K, value: unknown): ContractTypes[K] {
  if (!Object.hasOwn(validators, name)) throw new Error(`Unknown contract: ${name}`);
  return decodeConfig<unknown>(value, validators[name], name) as ContractTypes[K];
}
export function encodeContract<K extends keyof ContractTypes>(name: K, value: ContractTypes[K]): string {
  return JSON.stringify(decodeContract(name, value), null, 2) + "\n";
}
