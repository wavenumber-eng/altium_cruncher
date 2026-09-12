import "@typespec/json-schema";
import "./bom-pnp-config-defaults.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.BomPnpConfigInputContract;

model BomPnpConfigInputFieldAliases extends Record<string[]> {}

model BomPnpConfigInputVariants {
  mode?: "base" | "all" | "named";
  names?: string[];
  include_base?: boolean;
}

model BomPnpConfigInputBomPcbLineItemFields extends Record<string> {}

model BomPnpConfigInputBomPcbLineItem {
  enabled?: boolean;
  designator?: string;
  fields?: BomPnpConfigInputBomPcbLineItemFields;
}

model BomPnpConfigInputBom {
  source_mode?: "schematic" | "pcb" | "merged";
  outputs?: (
    | "raw-json"
    | "legacy-json"
    | "grouped-json"
    | "grouped-csv"
    | "grouped-xlsx"
    | "jlc-csv"
    | "jlc-xlsx")[];
  group_fields?: string[];
  output_fields?: string[];
  include_dnp?: boolean;
  split_dnp?: boolean;
  dnp_placement?: "inline" | "end" | "separate";
  highlight_dnp_rows?: boolean;
  prefix_order?: string[];
  pcb_line_item?: BomPnpConfigInputBomPcbLineItem;
}

model BomPnpConfigInputPnp {
  outputs?: ("json" | "csv" | "xlsx" | "jlc-cpl" | "jlc-cpl-xlsx")[];
  output_fields?: string[];
  units?: "mm" | "mils";
  position_mode?: "altium-pick-place" | "component-origin";
  exclude_no_bom?: boolean;
  layer_order?: string[];
  prefix_order?: string[];
}

model BomPnpConfigInputOutput {
  dir_template?: string;
  name_template?: string;
}

@jsonSchema
@id("https://github.com/wavenumber-eng/altium_cruncher/docs/contracts/bom_pnp_config.a0.schema.json")
@extension("title", "Altium Cruncher BOM/PnP Config")
model BomPnpConfigInput {
  schema?: "altium_cruncher.bom.config.a0" | null;
  field_aliases?: BomPnpConfigInputFieldAliases;
  variants?: BomPnpConfigInputVariants;
  bom?: BomPnpConfigInputBom;
  pnp?: BomPnpConfigInputPnp;
  output?: BomPnpConfigInputOutput;
}
