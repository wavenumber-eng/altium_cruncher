# Changelog

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
- Consume pinned `altium-monkey==2026.5.26` and expose explicit PnP position mode
  selection for BOM/PnP/JLC workflows.
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
