# Changelog

## 2026.5.26

- Bootstrap standalone `altium-cruncher` public package from the prior private
  toolz application.
- Package the CLI as a normal Python application with the canonical
  `altium-cruncher` console script and `altium_cruncher` Python module entry.
- Add public command coverage for migrated Altium workflows including SVG
  export, PCB layer STEP export, extraction, BOM/PnP, netlist, cleanup, split,
  merge, megamaid, and EasyEDA placeholder commands.
- Add Rack smoke strata, release signoff checks, package build validation, and
  built-wheel install smoke coverage.
