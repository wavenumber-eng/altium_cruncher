"""Generated contract transport entry points. Do not edit."""
from typing import Literal, overload
from .._runtime import decode_config
from .pcb_svg_config import PcbSvgConfigInput
from .schdoc_create_config import SchdocCreateConfigInput
from .pcbdoc_create_config import PcbdocCreateConfigInput
from .project_skeleton_config import ProjectSkeletonConfigInput
from .mco_input import McoInput
from .mco_envelope import McoEnvelopeInput
from .bom_pnp_config import BomPnpConfigInput
from .clean_config import CleanConfigInput
from .mate_config import MateConfigInput
from .pcb_layer_step_config import PcbLayerStepConfigInput
from .design_review_manifest import DesignReviewManifest
from .megamaid_manifest import MegamaidManifest
from .schematic_svg_enrichment import SchematicSvgEnrichment
from .schematic_svg_manifest import SchematicSvgManifest
from .pcb_svg_component_layers import PcbSvgComponentLayers
from .pcb_svg_timings import PcbSvgTimings
from .bom_array import BomArray
from .bom_grouped import BomGrouped
from .bom_legacy import BomLegacy
from .bom_normalized import BomNormalized
from .easyeda_footprint_report import EasyedaFootprintReport
from .easyeda_models import EasyedaModels
from .easyeda_symbol_report import EasyedaSymbolReport
from .installs import Installs
from .interface_design_manifest import InterfaceDesignManifest
from .intlib_extract import IntlibExtract
from .json_dump import JsonDump
from .json_dump_manifest import JsonDumpManifest
from .launch import Launch
from .libraries_scan import LibrariesScan
from .mate_inspection import MateInspection
from .mate_parts_input import MatePartsInput
from .mate_parts_manifest import MatePartsManifest
from .mco_builtin_result import McoBuiltinResult
from .mco_execution import McoExecution
from .mco_operations import McoOperations
from .notes import Notes
from .outjob_run import OutjobRun
from .pcb_layer_step import PcbLayerStepManifest
from .pcb_svg_enrichment import PcbSvgEnrichment
from .pcb_svg_manifest import PcbSvgManifest
from .pnp import Pnp
from .profiles import Profiles
from .profiles_clean import ProfilesClean
from .variants_list import VariantsList

@overload
def decode_contract(name: Literal["pcb_svg_config"], value: object) -> PcbSvgConfigInput: ...

@overload
def decode_contract(name: Literal["schdoc_create_config"], value: object) -> SchdocCreateConfigInput: ...

@overload
def decode_contract(name: Literal["pcbdoc_create_config"], value: object) -> PcbdocCreateConfigInput: ...

@overload
def decode_contract(name: Literal["project_skeleton_config"], value: object) -> ProjectSkeletonConfigInput: ...

@overload
def decode_contract(name: Literal["mco_input"], value: object) -> McoInput: ...

@overload
def decode_contract(name: Literal["mco_envelope"], value: object) -> McoEnvelopeInput: ...

@overload
def decode_contract(name: Literal["bom_pnp_config"], value: object) -> BomPnpConfigInput: ...

@overload
def decode_contract(name: Literal["clean_config"], value: object) -> CleanConfigInput: ...

@overload
def decode_contract(name: Literal["mate_config"], value: object) -> MateConfigInput: ...

@overload
def decode_contract(name: Literal["pcb_layer_step_config"], value: object) -> PcbLayerStepConfigInput: ...

@overload
def decode_contract(name: Literal["design_review_manifest"], value: object) -> DesignReviewManifest: ...

@overload
def decode_contract(name: Literal["megamaid_manifest"], value: object) -> MegamaidManifest: ...

@overload
def decode_contract(name: Literal["schematic_svg_enrichment"], value: object) -> SchematicSvgEnrichment: ...

@overload
def decode_contract(name: Literal["schematic_svg_manifest"], value: object) -> SchematicSvgManifest: ...

@overload
def decode_contract(name: Literal["pcb_svg_component_layers"], value: object) -> PcbSvgComponentLayers: ...

@overload
def decode_contract(name: Literal["pcb_svg_timings"], value: object) -> PcbSvgTimings: ...

@overload
def decode_contract(name: Literal["bom_array"], value: object) -> BomArray: ...

@overload
def decode_contract(name: Literal["bom_grouped"], value: object) -> BomGrouped: ...

@overload
def decode_contract(name: Literal["bom_legacy"], value: object) -> BomLegacy: ...

@overload
def decode_contract(name: Literal["bom_normalized"], value: object) -> BomNormalized: ...

@overload
def decode_contract(name: Literal["easyeda_footprint_report"], value: object) -> EasyedaFootprintReport: ...

@overload
def decode_contract(name: Literal["easyeda_models"], value: object) -> EasyedaModels: ...

@overload
def decode_contract(name: Literal["easyeda_symbol_report"], value: object) -> EasyedaSymbolReport: ...

@overload
def decode_contract(name: Literal["installs"], value: object) -> Installs: ...

@overload
def decode_contract(name: Literal["interface_design_manifest"], value: object) -> InterfaceDesignManifest: ...

@overload
def decode_contract(name: Literal["intlib_extract"], value: object) -> IntlibExtract: ...

@overload
def decode_contract(name: Literal["json_dump"], value: object) -> JsonDump: ...

@overload
def decode_contract(name: Literal["json_dump_manifest"], value: object) -> JsonDumpManifest: ...

@overload
def decode_contract(name: Literal["launch"], value: object) -> Launch: ...

@overload
def decode_contract(name: Literal["libraries_scan"], value: object) -> LibrariesScan: ...

@overload
def decode_contract(name: Literal["mate_inspection"], value: object) -> MateInspection: ...

@overload
def decode_contract(name: Literal["mate_parts_input"], value: object) -> MatePartsInput: ...

@overload
def decode_contract(name: Literal["mate_parts_manifest"], value: object) -> MatePartsManifest: ...

@overload
def decode_contract(name: Literal["mco_builtin_result"], value: object) -> McoBuiltinResult: ...

@overload
def decode_contract(name: Literal["mco_execution"], value: object) -> McoExecution: ...

@overload
def decode_contract(name: Literal["mco_operations"], value: object) -> McoOperations: ...

@overload
def decode_contract(name: Literal["notes"], value: object) -> Notes: ...

@overload
def decode_contract(name: Literal["outjob_run"], value: object) -> OutjobRun: ...

@overload
def decode_contract(name: Literal["pcb_layer_step"], value: object) -> PcbLayerStepManifest: ...

@overload
def decode_contract(name: Literal["pcb_svg_enrichment"], value: object) -> PcbSvgEnrichment: ...

@overload
def decode_contract(name: Literal["pcb_svg_manifest"], value: object) -> PcbSvgManifest: ...

@overload
def decode_contract(name: Literal["pnp"], value: object) -> Pnp: ...

@overload
def decode_contract(name: Literal["profiles"], value: object) -> Profiles: ...

@overload
def decode_contract(name: Literal["profiles_clean"], value: object) -> ProfilesClean: ...

@overload
def decode_contract(name: Literal["variants_list"], value: object) -> VariantsList: ...

def decode_contract(name: str, value: object) -> object:
    """Validate and copy authored JSON without applying defaults."""
    if name not in ["pcb_svg_config","schdoc_create_config","pcbdoc_create_config","project_skeleton_config","mco_input","mco_envelope","bom_pnp_config","clean_config","mate_config","pcb_layer_step_config","design_review_manifest","megamaid_manifest","schematic_svg_enrichment","schematic_svg_manifest","pcb_svg_component_layers","pcb_svg_timings","bom_array","bom_grouped","bom_legacy","bom_normalized","easyeda_footprint_report","easyeda_models","easyeda_symbol_report","installs","interface_design_manifest","intlib_extract","json_dump","json_dump_manifest","launch","libraries_scan","mate_inspection","mate_parts_input","mate_parts_manifest","mco_builtin_result","mco_execution","mco_operations","notes","outjob_run","pcb_layer_step","pcb_svg_enrichment","pcb_svg_manifest","pnp","profiles","profiles_clean","variants_list"]:
        raise ValueError(f"Unknown contract: {name}")
    return decode_config(value, name, name)
