import "@typespec/json-schema";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.CleanConfigInputContract;

@@extension(
  CleanConfigInput,
  "x-acr-font-defaults",
  #{ bold: false, italic: false, color_win32: null }
);

@@extension(
  CleanConfigInput,
  "x-acr-templates",
  #{
    schematic: #{
      schema: "altium_cruncher.clean.config.a0",
      normalize_pin_fonts: #{
        enabled: true,
        name_font: #{
          font_name: "Arial",
          size_pt: 10,
          bold: false,
          italic: false,
          color_win32: 0,
        },
        designator_font: #{
          font_name: "Arial",
          size_pt: 10,
          bold: false,
          italic: false,
          color_win32: 0,
        },
      },
      normalize_symbol_body_rectangles: #{
        enabled: true,
        min_width_mils: 40.0,
        min_height_mils: 40.0,
        outline_color_win32: 0,
        line_width: "small",
        fill_color_win32: 16777215,
        is_solid: true,
        transparent: false,
      },
      normalize_power_symbols: #{
        enabled: true,
        color_win32: 0,
        font: #{ font_name: "Arial", size_pt: 10, bold: true, italic: false },
      },
      normalize_net_labels: #{
        enabled: true,
        color_win32: 0,
        font: #{ font_name: "Arial", size_pt: 8, bold: true, italic: false },
      },
      normalize_component_designators: #{
        enabled: true,
        font: #{
          font_name: "Arial",
          size_pt: 12,
          bold: true,
          italic: false,
          color_win32: 0,
        },
      },
      normalize_component_parameters: #{
        enabled: true,
        font: #{
          font_name: "Arial",
          size_pt: 10,
          bold: false,
          italic: false,
          color_win32: 0,
        },
      },
      normalize_component_free_text: #{
        enabled: true,
        font_name: "Arial",
        color_win32: 0,
      },
      normalize_wires: #{ enabled: true, color_win32: 4408131 },
      normalize_no_erc: #{
        enabled: true,
        color_win32: 0,
        symbol: "cross_small",
      },
      normalize_sheet_style: #{
        enabled: true,
        line_color_win32: 0,
        area_color_win32: 16777215,
        document_font: #{
          font_name: "Times New Roman",
          size_pt: 10,
          bold: false,
          italic: false,
        },
      },
      normalize_symbol_internal_graphics_monochrome: #{
        enabled: true,
        saturation: 0.0,
      },
    },
    pcblib: #{
      schema: "altium_cruncher.pcblib.clean.config.a0",
      profile: "default",
      remove_mechanical_primitives: #{
        enabled: true,
        primitive_types: #["tracks", "arcs", "fills", "texts"],
        layers: #["mechanical"],
        preserve_regions: true,
        preserve_component_bodies: true,
      },
      remove_text_strings: #{
        enabled: true,
        layers: #["any"],
        match: "regex",
        patterns: #["(?i)\\bdesignator\\b"],
      },
      remove_regions: #{
        enabled: true,
        layers: #["mechanical"],
        preserve_component_linked: true,
        preserve_model_associated: true,
        preserve_keepouts: true,
        preserve_board_cutouts: true,
        preserve_custom_pad_regions: true,
      },
    },
  }
);

@@extension(
  CleanConfigInput,
  "x-acr-resolved-defaults",
  #{
    schematic: #{
      schema: "altium_cruncher.clean.config.a0",
      normalize_pin_fonts: #{
        enabled: true,
        name_font: null,
        designator_font: null,
      },
      normalize_symbol_body_rectangles: #{
        enabled: true,
        min_width_mils: 40.0,
        min_height_mils: 40.0,
        outline_color_win32: 0,
        line_width: "small",
        fill_color_win32: 16777215,
        is_solid: true,
        transparent: false,
      },
      normalize_power_symbols: #{
        enabled: true,
        color_win32: 0,
        font: #{ font_name: "Arial", size_pt: 10, bold: true, italic: false },
      },
      normalize_net_labels: #{
        enabled: true,
        color_win32: 0,
        font: #{ font_name: "Arial", size_pt: 8, bold: true, italic: false },
      },
      normalize_component_designators: #{
        enabled: true,
        font: #{
          font_name: "Arial",
          size_pt: 12,
          bold: true,
          italic: false,
          color_win32: 0,
        },
      },
      normalize_component_parameters: #{
        enabled: true,
        font: #{
          font_name: "Arial",
          size_pt: 10,
          bold: false,
          italic: false,
          color_win32: 0,
        },
      },
      normalize_component_free_text: #{
        enabled: true,
        font_name: "Arial",
        color_win32: 0,
      },
      normalize_wires: #{ enabled: true, color_win32: 4408131 },
      normalize_no_erc: #{
        enabled: true,
        color_win32: 0,
        symbol: "cross_small",
      },
      normalize_sheet_style: #{
        enabled: true,
        line_color_win32: 0,
        area_color_win32: 16777215,
        document_font: #{
          font_name: "Times New Roman",
          size_pt: 10,
          bold: false,
          italic: false,
        },
      },
      normalize_symbol_internal_graphics_monochrome: #{
        enabled: true,
        saturation: 0.0,
      },
    },
    pcblib: #{
      schema: "altium_cruncher.pcblib.clean.config.a0",
      profile: "default",
      remove_mechanical_primitives: #{
        enabled: true,
        primitive_types: #["tracks", "arcs", "fills", "texts"],
        layers: #["mechanical"],
        preserve_regions: true,
        preserve_component_bodies: true,
      },
      remove_text_strings: #{
        enabled: true,
        layers: #["any"],
        match: "regex",
        patterns: #["(?i)\\bdesignator\\b"],
      },
      remove_regions: #{
        enabled: true,
        layers: #["mechanical"],
        preserve_component_linked: true,
        preserve_model_associated: true,
        preserve_keepouts: true,
        preserve_board_cutouts: true,
        preserve_custom_pad_regions: true,
      },
    },
  }
);

@@extension(
  CleanConfigInput,
  "x-acr-schematic-comments",
  #{
    schema: #[
      "Schematic clean config for .SchDoc, .SchLib, and .PrjPcb inputs.",
      "This file is JSONC: // comments and trailing commas are accepted.",
      "Use --init-config to write this template without cleaning an input.",
      "Use --force-config with --init-config to overwrite an existing template."
    ],
    enabled: #["Set enabled=false to leave this rule family unchanged."],
    font_name: #["Altium font family name to apply."],
    size_pt: #["Font size in points."],
    bold: #["Whether the generated font is bold."],
    italic: #["Whether the generated font is italic."],
    color_win32: #[
      "Win32/BGR integer color. The loader also accepts #RRGGBB or integer strings."
    ],
    normalize_pin_fonts: #[
      "Pin name/designator fonts inside symbols.",
      "Set enabled=false if library pin text is already curated."
    ],
    `normalize_pin_fonts.name_font`: #["Style for visible pin names."],
    `normalize_pin_fonts.designator_font`: #[
      "Style for visible pin designators/numbers."
    ],
    normalize_symbol_body_rectangles: #[
      "Main symbol body rectangles. Width/height thresholds avoid touching tiny graphics.",
      "line_width options: smallest/zero, small, medium, large, or the Altium enum integer."
    ],
    `normalize_symbol_body_rectangles.min_width_mils`: #[
      "Only rectangles wider than this many mils are treated as symbol bodies."
    ],
    `normalize_symbol_body_rectangles.min_height_mils`: #[
      "Only rectangles taller than this many mils are treated as symbol bodies."
    ],
    `normalize_symbol_body_rectangles.outline_color_win32`: #[
      "Rectangle outline color."
    ],
    `normalize_symbol_body_rectangles.line_width`: #[
      "Outline width. Options: smallest/zero, small, medium, large, or enum integer."
    ],
    `normalize_symbol_body_rectangles.fill_color_win32`: #[
      "Rectangle fill color."
    ],
    `normalize_symbol_body_rectangles.is_solid`: #[
      "Whether the rectangle fill is solid."
    ],
    `normalize_symbol_body_rectangles.transparent`: #[
      "Whether the rectangle fill should be transparent."
    ],
    normalize_power_symbols: #[
      "Power-port text and color normalization for schematic sheets.",
      "Colors may be Win32/BGR integers, 0xRRGGBB-style strings, or #RRGGBB."
    ],
    `normalize_power_symbols.font`: #["Font applied to power-port text."],
    normalize_net_labels: #[
      "Net-label text style and color normalization.",
      "Use this to make copied/vendor sheets match the project drawing standard."
    ],
    `normalize_net_labels.font`: #["Font applied to net-label text."],
    normalize_component_designators: #[
      "Placed component designator text, for example U1/R3/C10.",
      "Font specs use font_name, size_pt, bold, italic, and optional color_win32/color."
    ],
    `normalize_component_designators.font`: #[
      "Font applied to component designator text."
    ],
    normalize_component_parameters: #[
      "Visible component parameter text such as value or part-number fields.",
      "This does not rename parameter keys; it only normalizes displayed text style."
    ],
    `normalize_component_parameters.font`: #[
      "Font applied to visible component parameter text."
    ],
    normalize_component_free_text: #[
      "Free text owned by a component rather than board/sheet-level free text.",
      "Useful for vendor symbols with inconsistent internal notes."
    ],
    `normalize_component_free_text.font_name`: #[
      "Font family applied to component-owned free text."
    ],
    normalize_wires: #[
      "Schematic wire color normalization.",
      "This intentionally avoids net labels and power symbols; those have separate rules."
    ],
    normalize_no_erc: #[
      "No-ERC marker appearance.",
      "symbol options: cross, thin cross, small cross, checkbox, triangle, or enum integer."
    ],
    `normalize_no_erc.symbol`: #[
      "Marker style. Options: cross, thin cross, small cross, checkbox, triangle, or enum integer."
    ],
    normalize_sheet_style: #[
      "Sheet border/area colors and document title-block font.",
      "PrjPcb input applies this rule to every SchDoc listed by the project."
    ],
    `normalize_sheet_style.line_color_win32`: #["Sheet border line color."],
    `normalize_sheet_style.area_color_win32`: #["Sheet background/area color."],
    `normalize_sheet_style.document_font`: #[
      "Font applied to sheet document/title-block text."
    ],
    normalize_symbol_internal_graphics_monochrome: #[
      "Symbol-owned internal graphics, such as lines, polygons, arcs, and fills.",
      "saturation=0 makes graphics monochrome while preserving relative intensity."
    ],
    `normalize_symbol_internal_graphics_monochrome.saturation`: #[
      "Target saturation from 0.0 monochrome to 1.0 unchanged."
    ],
  }
);

@@extension(
  CleanConfigInput,
  "x-acr-pcblib-comments",
  #{
    schema: #[
      "PcbLib clean config for footprint-library cleanup.",
      "This file is JSONC: // comments and trailing commas are accepted.",
      "Use --init-config to write this template without cleaning an input.",
      "Use --force-config with --init-config to overwrite an existing template.",
      "The default profile removes vendor drafting noise while preserving 3D bodies."
    ],
    enabled: #["Set enabled=false to leave this rule family unchanged."],
    profile: #[
      "Human-readable rule profile name written to clean reports.",
      "Options: raw, default.",
      "Use separate config files for different vendor/library cleanup policies."
    ],
    remove_mechanical_primitives: #[
      "Remove mechanical-layer tracks, arcs, fills, and similar drafting primitives.",
      "Preserve options protect component bodies, board cutouts, keepouts, and custom pads."
    ],
    `remove_mechanical_primitives.primitive_types`: #[
      "Primitive collections to remove; supported values include tracks, arcs, fills, and texts."
    ],
    `remove_mechanical_primitives.layers`: #[
      "Layer policy for primitive removal. Options: any, mechanical, layer names, or layer ids."
    ],
    `remove_mechanical_primitives.preserve_regions`: #[
      "Keep regions even if mechanical primitive removal is enabled."
    ],
    `remove_mechanical_primitives.preserve_component_bodies`: #[
      "Keep component-body/3D-model related primitives."
    ],
    remove_text_strings: #[
      "Remove configured PcbLib text strings, often vendor labels on mechanical layers.",
      "Match by layer, text content, or both depending on the nested rule options."
    ],
    `remove_text_strings.layers`: #[
      "Layer policy for text removal. Options: any, mechanical, layer names, or layer ids."
    ],
    `remove_text_strings.match`: #[
      "Text matching mode. Options: all, regex, contains, exact."
    ],
    `remove_text_strings.patterns`: #[
      "Text patterns used when match is regex, contains, or exact."
    ],
    remove_regions: #[
      "Remove configured mechanical regions.",
      "Use cautiously: the rule has preservation flags for keepouts and custom-pad regions."
    ],
    `remove_regions.layers`: #[
      "Layer policy for region removal. Options: any, mechanical, layer names, or layer ids."
    ],
    `remove_regions.preserve_component_linked`: #[
      "Keep regions linked to a footprint component object."
    ],
    `remove_regions.preserve_model_associated`: #[
      "Keep regions associated with embedded or generated models."
    ],
    `remove_regions.preserve_keepouts`: #["Keep keepout regions."],
    `remove_regions.preserve_board_cutouts`: #["Keep board-cutout regions."],
    `remove_regions.preserve_custom_pad_regions`: #[
      "Keep regions used to represent custom pads."
    ],
  }
);

@@extension(
  CleanConfigInput,
  "x-acr-domain-model-defaults",
  #{
    PinFontNormalizationConfig: #{
      enabled: true,
      name_font: null,
      designator_font: null,
    },
    SymbolBodyRectangleNormalizationConfig: #{
      enabled: true,
      min_width_mils: 40.0,
      min_height_mils: 40.0,
      outline_color_win32: 0,
      line_width: 1,
      fill_color_win32: 16777215,
      is_solid: true,
      transparent: false,
    },
    PowerSymbolNormalizationConfig: #{
      enabled: true,
      color_win32: 0,
      font_name: "Arial",
      size_pt: 10,
      bold: true,
      italic: false,
    },
    NetLabelNormalizationConfig: #{
      enabled: true,
      color_win32: 0,
      font_name: "Arial",
      size_pt: 8,
      bold: true,
      italic: false,
    },
    ComponentDesignatorNormalizationConfig: #{ enabled: true },
    ComponentParameterNormalizationConfig: #{ enabled: true },
    SheetStyleNormalizationConfig: #{
      enabled: true,
      line_color_win32: 0,
      area_color_win32: 16777215,
    },
    ComponentFreeTextNormalizationConfig: #{
      enabled: true,
      font_name: "Arial",
      color_win32: 0,
    },
    WireNormalizationConfig: #{ enabled: true, color_win32: 4408131 },
    NoErcNormalizationConfig: #{ enabled: true, color_win32: 0, symbol: 2 },
    SymbolInternalGraphicsMonochromeConfig: #{ enabled: true, saturation: 0.0 },
    AltiumCleanConfig: #{ schema: "altium_cruncher.clean.config.a0" },
    PcbLibMechanicalPrimitiveRemovalConfig: #{
      enabled: true,
      primitive_types: #["tracks", "arcs", "fills", "texts"],
      layers: #["mechanical"],
      preserve_regions: true,
      preserve_component_bodies: true,
    },
    PcbLibTextStringRemovalConfig: #{
      enabled: true,
      layers: #["any"],
      match: "regex",
      patterns: #["(?i)\\bdesignator\\b"],
    },
    PcbLibRegionRemovalConfig: #{
      enabled: true,
      layers: #["mechanical"],
      preserve_component_linked: true,
      preserve_model_associated: true,
      preserve_keepouts: true,
      preserve_board_cutouts: true,
      preserve_custom_pad_regions: true,
    },
    PcbLibCleanConfig: #{
      schema: "altium_cruncher.pcblib.clean.config.a0",
      profile: "default",
    },
  }
);
