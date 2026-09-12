"""Generated from src/tsp/altium_cruncher/config/bom-pnp-config.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

BomPnpConfigInput = TypedDict("BomPnpConfigInput", {
    "schema": NotRequired["Literal[\"altium_cruncher.bom.config.a0\"] | None"],
    "field_aliases": NotRequired["BomPnpConfigInputFieldAliases"],
    "variants": NotRequired["BomPnpConfigInputVariants"],
    "bom": NotRequired["BomPnpConfigInputBom"],
    "pnp": NotRequired["BomPnpConfigInputPnp"],
    "output": NotRequired["BomPnpConfigInputOutput"],
}, closed=True)

BomPnpConfigInputVariants = TypedDict("BomPnpConfigInputVariants", {
    "mode": NotRequired["Literal[\"base\"] | Literal[\"all\"] | Literal[\"named\"]"],
    "names": NotRequired["list[str]"],
    "include_base": NotRequired["bool"],
}, closed=True)

BomPnpConfigInputBom = TypedDict("BomPnpConfigInputBom", {
    "source_mode": NotRequired["Literal[\"schematic\"] | Literal[\"pcb\"] | Literal[\"merged\"]"],
    "outputs": NotRequired["list[Literal[\"raw-json\"] | Literal[\"legacy-json\"] | Literal[\"grouped-json\"] | Literal[\"grouped-csv\"] | Literal[\"grouped-xlsx\"] | Literal[\"jlc-csv\"] | Literal[\"jlc-xlsx\"]]"],
    "group_fields": NotRequired["list[str]"],
    "output_fields": NotRequired["list[str]"],
    "include_dnp": NotRequired["bool"],
    "split_dnp": NotRequired["bool"],
    "dnp_placement": NotRequired["Literal[\"inline\"] | Literal[\"end\"] | Literal[\"separate\"]"],
    "highlight_dnp_rows": NotRequired["bool"],
    "prefix_order": NotRequired["list[str]"],
    "pcb_line_item": NotRequired["BomPnpConfigInputBomPcbLineItem"],
}, closed=True)

BomPnpConfigInputPnp = TypedDict("BomPnpConfigInputPnp", {
    "outputs": NotRequired["list[Literal[\"json\"] | Literal[\"csv\"] | Literal[\"xlsx\"] | Literal[\"jlc-cpl\"] | Literal[\"jlc-cpl-xlsx\"]]"],
    "output_fields": NotRequired["list[str]"],
    "units": NotRequired["Literal[\"mm\"] | Literal[\"mils\"]"],
    "position_mode": NotRequired["Literal[\"altium-pick-place\"] | Literal[\"component-origin\"]"],
    "exclude_no_bom": NotRequired["bool"],
    "layer_order": NotRequired["list[str]"],
    "prefix_order": NotRequired["list[str]"],
}, closed=True)

BomPnpConfigInputOutput = TypedDict("BomPnpConfigInputOutput", {
    "dir_template": NotRequired["str"],
    "name_template": NotRequired["str"],
}, closed=True)

BomPnpConfigInputBomPcbLineItem = TypedDict("BomPnpConfigInputBomPcbLineItem", {
    "enabled": NotRequired["bool"],
    "designator": NotRequired["str"],
    "fields": NotRequired["BomPnpConfigInputBomPcbLineItemFields"],
}, closed=True)

BomPnpConfigInputFieldAliases = dict[str, Never]
RecordArrayString = dict[str, list[str]]
BomPnpConfigInputBomPcbLineItemFields = dict[str, Never]
RecordString = dict[str, str]
