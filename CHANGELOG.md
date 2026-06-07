# Changelog

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
- Clean configured BOM/PnP/JLC output filenames so format-only outputs rely on
  the file extension while semantic stems such as `raw`, `grouped`, and
  `jlc-cpl` remain visible.
- Continue experimental `mco` and `debug-plate` development toward Cricket
  Node mating-board automation.

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
- Add experimental `json-dump`, `mco`, and `debug-plate` commands for
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
