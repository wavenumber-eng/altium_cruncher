import "@typespec/json-schema";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.BomPnpConfigInputContract;

@@extension(
  BomPnpConfigInput,
  "x-acr-resolved-defaults",
  #{
    schema: "altium_cruncher.bom.config.a0",
    field_aliases: #{
      description: #["Description", "Desc"],
      footprint: #["Footprint", "Pattern", "Package"],
      jlcpcb_part_number: #[
        "JLCPCB Part #",
        "JLCPCB Part Number",
        "JLC Part #",
        "JLC Part Number",
        "LCSC Part #",
        "LCSC Part Number",
        "LCSC"
      ],
      manufacturer: #[
        "Manufacturer",
        "Mfr",
        "MFG",
        "Manufacturer Name",
        "Mfr Name"
      ],
      manufacturer_part_number: #[
        "Manufacturer Part Number",
        "MPN",
        "Mfr Part Number",
        "Mfr PN",
        "MFG PN",
        "Part Number"
      ],
      value: #["Value", "Comment"],
    },
    variants: #{ mode: "all", names: #[], include_base: true },
    bom: #{
      source_mode: "schematic",
      outputs: #["raw-json", "grouped-xlsx"],
      group_fields: #["mfg", "mpn", "description"],
      output_fields: #["mfg", "mpn", "description", "quantity", "designators"],
      include_dnp: true,
      split_dnp: true,
      dnp_placement: "inline",
      highlight_dnp_rows: true,
      prefix_order: #[],
      pcb_line_item: #{ enabled: false, designator: "PCB", fields: #{} },
    },
    pnp: #{
      outputs: #["json", "csv"],
      output_fields: #[
        "designator",
        "comment",
        "layer",
        "footprint",
        "center_x",
        "center_y",
        "rotation",
        "description"
      ],
      units: "mm",
      position_mode: "altium-pick-place",
      exclude_no_bom: false,
      layer_order: #["top", "bottom"],
      prefix_order: #[],
    },
    output: #{
      dir_template: "{Command}",
      name_template: "{SourceStem}_{VariantName}{OutputKindSuffix}",
    },
  }
);

@@extension(
  BomPnpConfigInput,
  "x-acr-jsonc-comments",
  #{
    schema: "BOM/PnP config contract id.",
    field_aliases: #[
      "Canonical BOM field aliases used to normalize project parameters.",
      "Each key is a canonical output field; each value lists accepted source names."
    ],
    variants: "Variant selection policy for BOM and PnP outputs.",
    `variants.mode`: "Variant mode. Options: all, base, named.",
    `variants.names`: "Variant names used when mode is named.",
    `variants.include_base`: "Include the base/no-variant output alongside named variants.",
    bom: "BOM normalization and artifact output settings.",
    `bom.source_mode`: "BOM source mode. Options: merged, pcb, schematic.",
    `bom.outputs`: "BOM artifacts to generate. Options: grouped-csv, grouped-json, grouped-xlsx, jlc-csv, jlc-xlsx, legacy-json, raw-json.",
    `bom.group_fields`: "Canonical fields used to group fitted parts into BOM rows.",
    `bom.output_fields`: "Columns emitted in grouped BOM table outputs.",
    `bom.include_dnp`: "Include do-not-populate components in normalized BOM data.",
    `bom.split_dnp`: "Keep fitted and DNP components in separate grouped BOM lines.",
    `bom.dnp_placement`: "Placement for DNP rows in grouped outputs. Options: end, inline, separate.",
    `bom.highlight_dnp_rows`: "Apply DNP row highlighting in spreadsheet outputs.",
    `bom.prefix_order`: "Designator prefix ordering for grouped BOM row designators.",
    `bom.pcb_line_item`: "Optional synthetic PCB line item added to BOM outputs.",
    `bom.pcb_line_item.enabled`: "Enable the synthetic PCB line item.",
    `bom.pcb_line_item.designator`: "Designator text for the synthetic PCB line item.",
    `bom.pcb_line_item.fields`: "Field templates for the synthetic PCB line item.",
    pnp: "Pick-and-place normalization and artifact output settings.",
    `pnp.outputs`: "PnP artifacts to generate. Options: csv, jlc-cpl, jlc-cpl-xlsx, json, xlsx.",
    `pnp.output_fields`: "Columns emitted in PnP table outputs.",
    `pnp.units`: "Output coordinate units. Options: mils, mm.",
    `pnp.position_mode`: "How component centers are derived. Options: altium-pick-place, component-origin.",
    `pnp.exclude_no_bom`: "Exclude placements for components marked no-BOM.",
    `pnp.layer_order`: "Layer ordering for PnP rows. Common values: top, bottom.",
    `pnp.prefix_order`: "Designator prefix ordering for PnP rows.",
    output: "Output path template settings shared by BOM and PnP artifacts.",
    `output.dir_template`: "Output directory template. Supported tokens include {Command}, {SourceName}, {SourceStem}, {VariantName}, {OutputKind}, {OutputKindStem}, and {OutputKindSuffix}.",
    `output.name_template`: "Output filename stem template. Supported tokens include {Command}, {SourceName}, {SourceStem}, {VariantName}, {OutputKind}, {OutputKindStem}, and {OutputKindSuffix}.",
  }
);

@@extension(
  BomPnpConfigInput,
  "x-acr-domain-model-defaults",
  #{
    FieldAliasConfig: #{
      canonical_fields: #{
        manufacturer: #[
          "Manufacturer",
          "Mfr",
          "MFG",
          "Manufacturer Name",
          "Mfr Name"
        ],
        manufacturer_part_number: #[
          "Manufacturer Part Number",
          "MPN",
          "Mfr Part Number",
          "Mfr PN",
          "MFG PN",
          "Part Number"
        ],
        jlcpcb_part_number: #[
          "JLCPCB Part #",
          "JLCPCB Part Number",
          "JLC Part #",
          "JLC Part Number",
          "LCSC Part #",
          "LCSC Part Number",
          "LCSC"
        ],
        value: #["Value", "Comment"],
        description: #["Description", "Desc"],
        footprint: #["Footprint", "Pattern", "Package"],
      },
    },
    BomPnpConfig: #{
      schema: "altium_cruncher.bom.config.a0",
      variant_mode: "all",
      variant_names: #[],
      include_base_variant: true,
      bom_source_mode: "schematic",
      bom_outputs: #["raw-json", "grouped-xlsx"],
      bom_group_fields: #["mfg", "mpn", "description"],
      bom_output_fields: #[
        "mfg",
        "mpn",
        "description",
        "quantity",
        "designators"
      ],
      include_dnp: true,
      split_dnp: true,
      dnp_placement: "inline",
      highlight_dnp_rows: true,
      pcb_line_item_enabled: false,
      pcb_line_item_designator: "PCB",
      pcb_line_item_fields: #{},
      pnp_outputs: #["json", "csv"],
      pnp_output_fields: #[
        "designator",
        "comment",
        "layer",
        "footprint",
        "center_x",
        "center_y",
        "rotation",
        "description"
      ],
      pnp_units: "mm",
      pnp_position_mode: "altium-pick-place",
      pnp_exclude_no_bom: false,
      layer_order: #["top", "bottom"],
      prefix_order: #[],
      output_dir_template: "{Command}",
      output_name_template: "{SourceStem}_{VariantName}{OutputKindSuffix}",
    },
  }
);
