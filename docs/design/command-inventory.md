# Command Inventory

Status: initial migration inventory
Last updated: 2026-05-26

This inventory records the command set migrated from the private
`toolz/altium_cruncher` package into the standalone public repo.

| Command | Initial status | Public test coverage | Notes |
| --- | --- | --- | --- |
| `version` | public | `L0_public_cli` | Package/CLI version reporting. |
| `sch-svg` | public | `L3_public_workflows` | Schematic SVG export. |
| `pcb-svg` | public | `L3_public_workflows` | PCB SVG export and board-view generation. |
| `pcb-layer-step` | public | unit/synthetic | Layer-to-STEP export using `wn-geometer`; Hydroscope CLI output is too large for the default fast lane. |
| `svg` | public | help only | Combined schematic/project SVG wrapper. |
| `pcblib-footprint-3d` | deferred | none | Broken; do not migrate into first public release. Remove or hide from public CLI/manifest before release. |
| `bom` | public | `L3_public_workflows` | Key BOM command. Keep and expand toward self-contained `bom_cruncher`-style JLC, raw JSON, grouped JSON, and grouped XLSX output with config-driven aliases, variants, DNP policy, and source selection. |
| `pnp` | public | `L3_public_workflows` | Pick-and-place output. |
| `netlist` | public | `L3_public_workflows` | Key command. Keep current netlist JSON behavior for Altium schematic/project documents. |
| `extract` | public | `L3_public_workflows` | SchDoc/PcbDoc extraction workflows. |
| `easyeda-import` | optional-public | placeholder plus extra lane | Requires `altium-cruncher[easyeda]` or side-installed `easyeda-monkey`. |
| `easyeda-review` | optional-public | placeholder plus extra lane | Requires `altium-cruncher[easyeda]` or side-installed `easyeda-monkey`. |
| `easyeda-footprint-review` | optional-public | placeholder plus extra lane | Requires `altium-cruncher[easyeda]` or side-installed `easyeda-monkey`. |
| `split` | public | `L3_public_workflows` | SchLib/PcbLib split workflows. |
| `merge` | public | `L3_public_workflows` | SchLib/PcbLib merge workflows. |
| `megamaid` | public | pytest | Project decomposition workflow, including Hydroscope embedded images/models. |
| `clean` | public | `L3_public_workflows` | SchDoc/SchLib/PcbLib cleanup workflows. |

The command manifest lives at `contracts/command_manifest.v0.json`. `L99` should
eventually enforce that every manifest command has help, docs, and behavioral
test ownership.

Shared help requirements for every command:

- top-level and command-specific help should print the package version;
- command lists should be alphabetical;
- help output should include readable spacing between version, usage, commands,
  and options;
- top-level help should explicitly show how to request command-specific help.

SVG command family notes:

- `sch-svg`, `pcb-svg`, and `svg` all stay in the first public command set;
- `svg` is a convenience command that runs schematic output, PCB output, or both
  depending on the input type;
- `svg` help should describe that routing behavior clearly;
- `pcb-svg` needs fixture-backed assembly-view coverage with HLR/geometer and a
  redistributable project that proves SVG artifacts are created.

PCB layer STEP notes:

- `pcb-layer-step` stays in the first public command set;
- first fixture-backed command test should use `cricket-node` and generate
  bottom-layer copper;
- the documented example colors are copper `#3D85C6` and board outline
  `#CCCCCC`;
- command fixtures should use `input/`, `reference_output/`, and transient
  `output/` folders.

BOM notes:

- `bom` stays in the first public command set;
- first-release target is a self-contained version of the old
  `bom_cruncher` behavior, not only the current flat CSV/JSON/XLSX command;
- required outputs are raw JSON every run, JLC BOM, grouped JSON BOM, and
  grouped XLSX BOM;
- BOM config should be JSON with a schema/type field, auto-generated as
  `bom.config`, overridable with `--config`, and covered by a machine-readable
  contract;
- config owns output fields, canonical parameter names, aliases, grouping
  keys, source mode, variant selection, DNP handling, component-kind filtering,
  and optional PCB-as-line-item behavior;
- alias behavior should adapt the `wn-hw` library-policy concepts while keeping
  the public package self-contained;
- `node_test_array` is the required hierarchical design fixture for validating
  resolved designators against Altium-generated BOM CSV reference output.

Netlist notes:

- `netlist` stays in the first public command set;
- preserve current JSON model output from `.SchDoc` and `.PrjPcb` inputs;
- keep `--no-indexes`;
- treat the command as a first-class machine-consumable output surface in
  design docs and L99 command coverage.

Deferred command notes:

- `pcblib-footprint-3d` should not be treated as public for the first release.
