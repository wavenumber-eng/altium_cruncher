# Changelog

## 2026.6.22

- Consume pinned `altium-monkey==2026.6.21`, including the corrected rounded
  rectangle pad corner-ratio projection and updated PcbLib cavity-region
  authoring/readback behavior.
- Add a GitHub PR hygiene gate that requires public pull requests to link an
  existing same-repo issue and rejects emoji, AI-vendor attribution, and common
  non-factual filler in PR metadata and commit messages.
- Run the Wavenumber development-standard check in CI so public pull requests
  exercise the same repo-shape gate documented for local development.

## 2026.6.17

- Consume pinned `altium-monkey==2026.6.16`, including the public mechanical
  layer-kind authoring/readback surface and the SchLib-to-SchDoc insertion
  order fix used by generated schematic workflows.
- Add MCO-backed `schdoc create`, `schlib create`, and `pcbdoc create`
  commands for blank schematic documents, one-symbol schematic libraries, and
  generated rigid PCB documents.
- Add `prjpcb init`, `prjpcb create`, and `prjpcb add-sheet` workflows for
  JSONC-driven PrjPcb skeleton generation with project parameters, multiple
  schematic sheets, generated rigid board stacks, board outlines, and the
  standard mechanical layer-kind profile.
- Make `prjpcb create` with no config target bootstrap `prjpcb_init.jsonc` on
  the first run and use that config on later runs; bare project names passed to
  `prjpcb init` and `prjpcb create` resolve to `NAME.project.jsonc`.
- Start the new project skeleton config contract at
  `altium_cruncher.project_skeleton.a0` and expand standard mechanical
  rows in generated configs so users can edit single layers and grouped
  top/bottom layer pairs directly.
- Normalize `altium-cruncher` owned public contract identifiers to
  `altium_cruncher.*.a0`, leaving separately owned contracts such as
  `pcb.svg.config.a0`, `pcb.svg.manifest.a0`, and
  `geometry.planar_step.request.a0` unchanged.
- Improve `mate` fixture generation with free-pad selectors, destination-pad
  reference outlines, source schematic power-port projection, board-cutout
  scope controls, and cleaner single-pin schematic placement.
- Keep generated PrjPcb/PcbDoc stack authoring scoped to generated rigid
  layer stacks; `.stackup` and `.stackupx` import into new PcbDoc files is
  tracked as future Altium Monkey work.
- Preserve clean JSON stdout for MCO-backed creation commands by redirecting
  lower-level document save messages to stderr in `--json` mode.

## 2026.6.13

- Consume pinned `altium-monkey==2026.6.13`, including the SchDoc
  near-crossing netlist fix, noncanonical `SheetNumber` design-JSON fix, and
  PcbDoc/PcbLib DXP parameter-list escape handling for `PrimitiveParameters`.
- Ship the initial minimal `pcblib create` command, backed by generated
  `pcblib.create` and `pcblib.add_footprint` MCO operations, for one-footprint
  PcbLib authoring.
- Keep generated JSONC config/comment rendering and the PcbLib create command
  docs aligned for the public release boundary.

## 2026.6.11

- Consume pinned `altium-monkey==2026.6.11` and `wn-geometer==2026.6.10`
  for the OCCT V8-backed geometry stack used by assembly HLR and PCB layer
  STEP export.
- Narrow the package metadata to Python `>=3.12,<3.13`, matching the current
  public Altium Monkey dependency.
- Prefer `outline` for `pcb-svg` assembly silhouette projections while keeping
  `simple` as a legacy config alias, and read Geometer's current outline result
  key for STEP overlays.
- Update `pcb-layer-step` defaults for fixture-alignment models: explicit
  feature bodies, colors, thickness bias, selected pad highlights, scoped drill
  policies, and yellow board outline/cutout bodies.
- Align `mate` generated PCB layer STEP artifacts with the standalone
  `pcb-layer-step --init-config` defaults.
- Add `pcblib create`, backed by generated `pcblib.create` and
  `pcblib.add_footprint` MCO operations, for one-footprint PcbLib authoring.
- Route generated editable configs through the shared JSONC comment renderer
  and add ADR-0007: string/enum fields in generated config comments must list
  accepted options.

## 2026.6.9

- Consume pinned `altium-monkey==2026.6.9`.
- Add the public `variants` command for PrjPcb variant inspection and
  MCO-backed variant edits.
- Add project variant MCO operations for list, delete, rename, clone, DNP set,
  and DNP toggle workflows.
- Render variant list output with width-aware Rich tables grouped by variant
  and schematic sheet, including resolved component values for DNP rows.
- Add shared recursive CLI help coloring for command and subcommand names,
  with plain captured output and `NO_COLOR`/`TERM=dumb` behavior preserved.
- Add filesystem-safe PcbLib split filenames so footprint names containing
  Windows-invalid characters no longer fail split, extract, or megamaid.
- Normalize Altium XML-BOM oracle aliases in L3 release tests so reference
  comparisons tolerate exports that use `Comment` where older output used
  `Name`.
- Add ADR-0006 for CLI help output policy and update variant/MCO design docs.

## 2026.6.7

- Consume pinned `altium-monkey==2026.6.7`.
- Add `acr` and `ad` executable aliases for local workflows.
- Promote `easyeda-import` to a first-class public command dependency.
- Add `installs`, `launch`, and `profiles` commands for Altium install,
  launcher, and ProgramData profile diagnostics.
- Expand `design` into an agent-facing design review bundle, with
  `design-review` and `dr` aliases, serialized SchDoc/PcbDoc JSON, structured
  notes JSONC, schematic SVGs, copper-layer PCB review SVGs, manifest, and
  README output.
- Align design-review PCB SVG output with the default `pcb-svg` layer-output
  folder shape under `pcb/layers/`, limited to copper layers including inner
  copper layers, and log generated review artifacts progressively.
- Add a dedicated `notes` command for Altium Note objects, text frames, and
  free schematic text.
- Write `notes` and design-review note artifacts as sparse JSONC with relative
  paths and Altium unique ids; sheet-template/title-block owned text is
  suppressed by default, with an opt-in raw text flag for diagnostics.
- Extend `megamaid` output with serialized document JSON, combined extracted
  library JSON, and notes JSONC artifacts under the shared `json/<kind>/`
  folder convention.
- Add `outjob run` for executing project-referenced or explicit `.OutJob`
  files through the public `altium-monkey` runner.
- Change standalone `json-dump` batch output to write `schdoc/`, `pcbdoc/`,
  and related domain folders directly under `output/json-dump`, with
  `--layout flat` for single-folder dumps.
- Clean configured BOM/PnP/JLC output filenames so format-only outputs rely on
  the file extension while semantic stems such as `raw`, `grouped`, and
  `jlc-cpl` remain visible.
- Add the initial beta `mate` release for Cricket Node-style fixture and debug
  mating-board testing. The public example generates primitive MCO operations,
  resolves mate parts from local SchLib/PcbLib search roots, projects DUT
  reference graphics and cutouts, creates linked schematic/PCB components,
  emits a user union, generates loose manual net labels, and can embed a
  bottom-layer fixture-alignment STEP artifact.
- Add `mco list` as a maintained operation catalog, with message-first MCO run
  output and explicit required/optional argument groups in human catalog output.
- Add the `examples/mate/bug-brain` fixture as source material for future
  header-style mate workflows.

## 2026.5.28

- Bootstrap standalone `altium-cruncher` public package from the prior private
  toolz application.
- Package the CLI as a normal Python application with the canonical
  `altium-cruncher` console script and `altium_cruncher` Python module entry.
- Add public command coverage for migrated Altium workflows including SVG
  export, PCB layer STEP export, extraction, BOM/PnP, design JSON, cleanup,
  split, merge, megamaid, and EasyEDA import commands.
- Add Rack smoke strata, release signoff checks, package build validation, and
  built-wheel install smoke coverage.
- Document `uv tool install` as the preferred CLI install path.
- Add ADR-0002 for CLI install, command layout, AGPL licensing boundary, and
  dependency-minimization discipline.
- Add `altium-cruncher[easyeda]` as the optional public dependency path for
  EasyEDA workflows through `easyeda-monkey`.
- Add ADR-0005 and L99 checks for CLI design docs plus public dataclass and
  major-interface design/test ownership.
- Consume pinned `altium-monkey==2026.6.7` and expose explicit PnP position mode
  selection for BOM/PnP/JLC workflows.
- Add experimental `json-dump`, `mco`, and `mate` commands for
  reference inspection, generated CAD operation execution, and Cricket Node
  mating-board workflow development.
- Align BOM/PnP spreadsheet output with `bom_cruncher` by using `openpyxl`;
  XLSX cells are written as text so package values such as `0603` retain
  leading zeroes.
- Make `raw-json` a flat list of unaliased raw BOM components, write
  `bom.config.used.json` beside configured outputs, add DNP row highlight
  support for grouped XLSX, and emit JLC BOM/CPL XLSX from the `jlc` command.
- Restore `pcb-svg` assembly-view HLR coverage through `wn-geometer` and add an
  enabled-by-default synthetic `BOARD_CUTOUTS` layer with configurable hash
  density, hash direction, hash and outline stroke widths, dashed or solid
  outlines, and labels.
- Let user-editable command config files load JSONC comments and trailing
  commas, and use `pcb.svg.config` as the default PCB SVG config filename.
- Add global `--quiet`, `--verbose`, and `--log-level` CLI logging controls.
- Add public contribution guide, issue templates, pull-request template, and
  release notes for the May 28, 2026 public release.
- Add a Windows PowerShell installer wrapper around the supported
  `uv tool install` flow.
- Run CI for pull requests on Ubuntu and Windows, including Rack, package
  build, distribution check, and installed-console smoke test.
