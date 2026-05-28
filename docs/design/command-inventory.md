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
| `bom` | public | `L3_public_workflows` | Key BOM command. Keep and expand toward self-contained `bom_cruncher`-style JLC, flat raw JSON, grouped JSON, and grouped XLSX output with config-driven aliases, variants, DNP policy/highlighting, and source selection. |
| `pnp` | public | `L3_public_workflows` | Keep. Expand toward self-contained PnP/CPL output with shared BOM/PnP normalization, CSV/JSON/XLSX formats, JLC CPL CSV/XLSX, units, variant/no-BOM filtering, and configurable sorting. |
| `jlc` | public | `L3_public_workflows` | Meta command that generates both JLC BOM XLSX and JLC CPL XLSX through the shared BOM/PnP implementation paths. |
| `netlist` | public | `L3_public_workflows` | Key command. Keep current netlist JSON behavior for Altium schematic/project documents. |
| `extract` | public | `L3_public_workflows` | Keep. SchDoc/PcbDoc/PrjPcb extraction workflows plus IntLib source extraction must be tested against the same fixture surfaces and semantic checks as the underlying Altium Monkey extraction APIs. |
| `easyeda-import` | optional-public | placeholder plus extra lane | Work in progress. Requires `altium-cruncher[easyeda]` or side-installed `easyeda-monkey`; audit and fixture-backed tests are required before release ownership. |
| `easyeda-review` | optional-public | placeholder plus extra lane | Development review command. Audit before deciding whether to keep public, move behind a dev namespace, or defer. |
| `easyeda-footprint-review` | optional-public | placeholder plus extra lane | Development review command. Audit before deciding whether to keep public, move behind a dev namespace, or defer. |
| `split` | public | `L3_public_workflows` | Keep. SchLib/PcbLib split workflows should be tested against provided reference split outputs without complex interop/native parity requirements. |
| `merge` | public | `L3_public_workflows` | Keep. SchLib/PcbLib merge workflows should use the same reference-output semantic test shape as split. |
| `megamaid` | public | `L3_public_workflows` | Keep. Showcase project decomposition command; should have end-to-end fixture coverage for libs, BOM, netlist, manifest, and embedded assets. |
| `clean` | public | `L3_public_workflows` | Keep. Needs detailed config documentation plus fixture-backed CLI tests for template creation, actual clean application, output/backup behavior, and PcbLib removal rules. |

The command manifest lives at `docs/contracts/command_manifest.v0.json`. `L99` should
eventually enforce that every manifest command has help, docs, and behavioral
test ownership.

Shared help requirements for every command:

- top-level and command-specific help should print the package version;
- command lists should be alphabetical;
- help output should include readable spacing between version, usage, commands,
  and options;
- top-level help should explicitly show how to request command-specific help.
- root-level logging controls are `--quiet`, `--verbose`, and `--log-level`;
  normal command progress is INFO, while parser internals should stay DEBUG.

Shared output naming requirements:

- output-producing commands should use one filename-template resolver rather
  than command-local naming rules;
- the shared resolver applies to `svg`, `sch-svg`, `pcb-svg`, `netlist`, `bom`,
  `pnp`, and the `jlc` command;
- filename and output-folder templates should support stable placeholders,
  fixed string fragments, `PrjPcb` project parameters, and the runtime
  `VariantName` token for the current processed variant;
- the resolver should return safe relative paths by default and reject path
  traversal;
- missing parameter behavior, filename/path sanitization, cross-platform
  separator normalization, and manifest reporting of resolved output names must
  be documented and tested.

SVG command family notes:

- `sch-svg`, `pcb-svg`, and `svg` all stay in the first public command set;
- `svg` is a convenience command that runs schematic output, PCB output, or both
  depending on the input type;
- `svg` help describes that routing behavior and avoids presenting the command
  as a separate renderer;
- `pcb-svg` has fixture-backed assembly-view coverage with HLR/geometer using
  Hydroscope embedded STEP models, while the normal layer-output test remains
  in place so HLR work cannot regress layer SVG output;
- `pcb-svg` uses `pcb.svg.config`; user config files may contain JSONC
  comments and trailing commas, while contracts remain strict JSON. Individual
  layer outputs are separate
  from composed views, and composed views have explicit layer tokens, durable
  group ids, and output SVG paths;
- synthetic layer tokens include `BOARD_OUTLINE`, `BOARD_CUTOUTS`, `DRILLS`,
  `SLOTS`, `ASSEMBLY_HLR_TOP`, and `ASSEMBLY_HLR_BOTTOM`;
- `ASSEMBLY_HLR_TOP`/`ASSEMBLY_HLR_BOTTOM` and `PIN1_TOP`/`PIN1_BOTTOM`
  have initial A0 rendering implementations;
- `ASSEMBLY_DESIGNATORS_TOP`/`ASSEMBLY_DESIGNATORS_BOTTOM`, DNP visual
  treatment, diode line art/cathode overlays, and richer project-level SVG
  metadata are planned but not implemented yet;
- `BOARD_CUTOUTS` supports configurable hash spacing/direction/line width,
  configurable outline line width, and solid or dashed outlines. A0 deliberately
  omits generated cutout text labels;
- board cutout hash rendering is implemented through reusable SVG pattern
  helpers so future synthetic layers can fill arbitrary closed paths the same
  way.

PCB layer STEP notes:

- `pcb-layer-step` stays in the first public command set;
- first fixture-backed command test uses a minimized `cricket-node` PcbDoc and
  generates bottom-layer copper through the command handler;
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
- default grouped XLSX BOM review output puts DNP status first, omits the
  line-number `item` column unless explicitly configured, keeps text cells
  spreadsheet-safe, uses inverse knockout headers, and does not enable Excel
  filter dropdowns;
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

PnP notes:

- `pnp` stays in the first public command set;
- current CSV/JSON behavior from `.PrjPcb` should be preserved while adding
  XLSX, JLC CPL, and richer sorting controls;
- implementation should share normalized component/placement records with
  `bom` so PCB-derived BOM JSON and PnP JSON do not diverge;
- sorting needs natural designator order, top/bottom grouping, and configurable
  designator-prefix ordering;
- test against `node_test_array`, including variant `B4`, because it exercises
  hierarchical sheet instances and resolved designators;
- tests should mirror core `AltiumDesign.to_pnp(...)` coverage for required
  fields, numeric positions, `top`/`bottom` layers, mm/mils conversion, and
  no-BOM filtering;
- use the older `bom_cruncher` placement, JLC CPL, and natural designator
  sorting code as reference material, but keep `altium-cruncher` self-contained.

JLC notes:

- `jlc` generates JLC BOM plus JLC CPL from one project/config
  invocation;
- default `jlc` output writes the paired BOM and CPL XLSX files as siblings in
  the same output folder;
- tests should prove meta-command output matches the equivalent independent
  `bom` and `pnp` JLC modes.

Netlist notes:

- `netlist` stays in the first public command set;
- preserve current JSON model output from `.SchDoc` and `.PrjPcb` inputs;
- keep `--no-indexes`;
- treat the command as a first-class machine-consumable output surface in
  design docs and L99 command coverage.

Extract notes:

- `extract` stays in the first public command set;
- tests should mirror the Altium Monkey extraction tests rather than only
  checking that files exist;
- SchDoc extraction should cover split and combined `SchLib` output from
  cleared `extract_symbols` fixtures;
- PcbDoc extraction should cover split and combined `PcbLib` output from
  cleared PcbDoc extraction fixtures;
- `.PrjPcb` extraction should prove both `schlib/` and `pcblib/` fanout when a
  project contains both source types;
- `.IntLib` extraction should expose the existing `AltiumIntLib.extract_sources`
  behavior from the command line, writing individual source libraries, a
  manifest, and the generated `.LibPkg`;
- IntLib tests should use public fixtures such as `RT_SUPER_C1.IntLib` or
  `loz-old-man.IntLib` and verify the extracted `SchLib`/`PcbLib` files reparse;
- fixtures copied from `C:\eli\wn_test_corpus` require proprietary-information
  review before check-in.

EasyEDA command notes:

- `easyeda-import`, `easyeda-review`, and `easyeda-footprint-review` remain
  work in progress until audited;
- `easyeda-import` is the likely public command, but it needs tests proving
  saved JSON input, optional API/cache behavior, generated `SchLib`, generated
  `PcbLib` when requested, reports, and preview artifacts;
- the review commands were built for development review and may need to become
  dev-only or deferred if they are not stable enough for public CLI support;
- no EasyEDA command should be release-owned until the `easyeda-monkey` optional
  extra lane runs fixture-backed command tests.

Split notes:

- `split` stays in the first public command set;
- tests should run the public CLI and compare generated split output against
  checked-in reference outputs from cleared test projects;
- SchLib coverage should include file-set matching, reparsing generated
  `SchLib` files, output filename pattern behavior, and symbol filtering;
- PcbLib coverage should include file-set matching and reparsing generated
  `PcbLib` files;
- heavy AD25/native/interop parity is not required for the public CLI split
  test; stable semantic matching is enough.

Merge notes:

- `merge` stays in the first public command set;
- tests should run the public CLI and compare generated merged libraries
  against checked-in reference outputs from cleared test projects;
- SchLib coverage should include reparse checks, symbol-name set matching,
  selected primitive/stream counts, and conflict policies;
- PcbLib coverage should include reparse checks, footprint-name set matching,
  and rename-only conflict behavior;
- heavy AD25/native/interop parity is not required for the public CLI merge
  test; stable semantic matching is enough.

Megamaid notes:

- `megamaid` stays in the first public command set as a showcase command;
- tests should run the public CLI against a representative project fixture;
- required output coverage includes `schlib/`, `pcblib/`, `bom/`, `netlist/`,
  `embedded_models/`, `embedded_fonts/`, `sch_images/`, and
  `megamaid_manifest.json`;
- generated combined libraries should reparse, BOM CSV and netlist JSON should
  exist, and manifest counts/paths should be validated;
- rerun behavior should clear megamaid-owned stale artifacts while preserving
  unrelated files under the output root.

Clean notes:

- `clean` stays in the first public command set;
- release docs must explain both config schemas:
  `wn.altium.clean.config.v1` for `SchDoc`/`SchLib`/`PrjPcb`, and
  `wn.altium.pcblib.clean.config.v1` for `PcbLib`;
- docs must cover config auto-generation, output path behavior, backup
  behavior, color/font/line-width/no-ERC value formats, every schematic
  normalization section, and every PcbLib removal section;
- current tests are not enough: they cover SchDoc template generation, a few
  SchLib helper-ordering cases, and PcbLib config-path discovery;
- add CLI tests for actual SchLib/SchDoc clean application, project fanout when
  cleared fixtures exist, PcbLib mechanical/text/region removal, generated
  config contract conformance, and backup/output semantics;
- before/after preview or GUI-assisted rule development is useful but should be
  tracked as a post-release issue, not a first-release blocker.

Deferred command notes:

- `pcblib-footprint-3d` should not be treated as public for the first release.
