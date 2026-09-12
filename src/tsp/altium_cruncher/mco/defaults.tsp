namespace Wavenumber.AltiumCruncher.Mco;

const mcoTemplate = #{
  schema: "altium_cruncher.mco.a0",
  operations: #[
    #{
      `op`: "project.create",
      id: "create_project",
      message: "Create a blank Altium project",
      args: #{
        file: "output/mate/mate.PrjPcb",
        name: "mate",
        overwrite: false,
      },
    },
    #{
      `op`: "schdoc.create",
      id: "create_schematic",
      message: "Create a blank schematic",
      args: #{
        file: "output/mate/mate.SchDoc",
        sheet_style: "D",
        overwrite: false,
      },
    },
    #{
      `op`: "pcbdoc.create",
      id: "create_board",
      message: "Create a blank board",
      args: #{
        file: "output/mate/mate.PcbDoc",
        layer_stack_template: "2-layer",
        overwrite: false,
        board_outline_mils: #{ left: 0, bottom: 0, right: 3000, top: 2000 },
      },
    },
    #{
      `op`: "project.add_document",
      id: "add_schematic_to_project",
      message: "Add schematic to project",
      args: #{ file: "output/mate/mate.PrjPcb", document: "mate.SchDoc" },
    },
    #{
      `op`: "project.add_document",
      id: "add_board_to_project",
      message: "Add board to project",
      args: #{ file: "output/mate/mate.PrjPcb", document: "mate.PcbDoc" },
    }
  ],
};

const mcoKeyComments = #{
  id: "Stable operation id used by logs and on_fail jumps.",
  message: "Free-form human-readable operation message.",
  file: "Path to the target Altium document or project file.",
  name: "Free-form generated object or project name.",
  overwrite: "Allow replacing an existing output object/file.",
  document: "Project-relative document path to add to a .PrjPcb.",
  footprint: "PcbLib footprint pattern name.",
  height: "Footprint height string, for example \"0mil\".",
  description: "Human-readable footprint description.",
  primitive_parameters: "Footprint PrimitiveParameters side-stream values.",
  sheet_style: "Schematic sheet style. Options: Altium SheetStyle enum name or native enum id.",
  custom_sheet_mils: "Custom schematic sheet size object with width and height in mils.",
  template: "Optional .SchDot template path for SchDoc creation.",
  layer_stack_template: "Layer stack template id. Options are supplied by altium-monkey; the generated default uses 2-layer.",
  rigid_stack: "Generated rigid layer-stack object for new PcbDoc creation.",
  stackupx_file: "Path to a .stackupx file to import as the PcbDoc layer-stack document.",
  mechanical_layer_profile: "Mechanical layer profile. Options: standard_component_pairs, v7_mechanical_53.",
  mechanical_layers: "Editable mechanical layer display-name/enabled rows.",
  mechanical_layer_pairs: "Editable mechanical layer top/bottom pair rows.",
  mechanical_layer_kinds: "Editable mechanical layer kind assignment rows.",
  layer: "PCB layer selector. Legacy PcbLayer names/ids remain supported; with a V7-aware altium-monkey, primitive ops also accept semantic tokens such as MECHANICAL33. Raw serialized V7 saved-layer ids are diagnostics, not layer selectors.",
  layer_start: "Start layer selector for legacy pad/via span operations.",
  layer_end: "End layer selector for legacy pad/via span operations.",
  left: "Rectangle left coordinate in mils.",
  bottom: "Rectangle bottom coordinate in mils.",
  right: "Rectangle right coordinate in mils.",
  top: "Rectangle top coordinate in mils.",
};

const mcoPathComments = #{
  schema: "MCO config contract id.",
  operations: "Operations execute in order. Use on_fail to jump to another operation id.",
  `operations.args`: "Operation-specific arguments. Use altium-cruncher mco ops to inspect each contract.",
  `operations.args.board_outline_mils`: "Board outline rectangle in mils.",
};
