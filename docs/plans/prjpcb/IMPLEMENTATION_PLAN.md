# PrjPcb Skeleton Implementation Plan

Status: active for the 2026.6.17 document/project skeleton release slice

This plan tracks the `prjpcb` project-skeleton workflow in `altium_cruncher`.
The stable public contracts live in `docs/contracts` and `docs/design`; this
file is the working tracker for current implementation order, remaining review,
and release exit criteria.

## Design Sources

- `docs/design/cli/prjpcb.html` - current command behavior.
- `docs/design/cli/mco.html` - generated MCO operation contract.
- `docs/design/cli/pcb-layer-step.html` - Geometer boundary for
  `geometry.planar_step.request.a0`.
- `docs/contracts/project_skeleton_config.a0.schema.json` - project skeleton
  config contract.
- `docs/contracts/schdoc_create_config.a0.schema.json` - standalone SchDoc
  create config contract.
- `docs/contracts/pcbdoc_create_config.a0.schema.json` - standalone PcbDoc
  create config contract.
- `docs/contracts/command_manifest.a0.json` - public CLI command inventory.

## Goals

- Create project skeletons through MCO operations rather than command-specific
  direct writers.
- Make `acr prjpcb create` useful from a blank folder: first run writes a
  commented `prjpcb_init.jsonc` config, later runs consume that config.
- Make `acr schdoc create` and `acr pcbdoc create` follow the same config-first
  pattern with child-object contracts that match the `prjpcb` config children.
- Keep `schlib` and `pcblib` as command groups with a simple direct `create`
  subcommand and no standalone config contract for now.
- Keep generated project configs editable, especially schematic sheets, project
  parameters, rigid layer stack fields, and mechanical layer kind rows.
- Normalize `altium_cruncher`-owned public contract ids to
  `altium_cruncher.*.a0`, while preserving external or separately owned schema
  ids such as `pcb.svg.config.a0`, `pcb.svg.manifest.a0`, and
  `geometry.planar_step.request.a0`.

## Current State

- Package version is locally bumped to `2026.6.17` for release testing.
- `prjpcb`, `prjpcb init`, `prjpcb create`, and `prjpcb add-sheet` are backed by
  MCO operations.
- `schdoc create` and `pcbdoc create` now support no-target config-first flows:
  `schdoc_create.jsonc` and `pcbdoc_create.jsonc`.
- `schlib create` and `pcblib create` remain direct library-seed commands under
  parent command groups. A blank SchLib creates one empty symbol, and a blank
  PcbLib creates one empty footprint.
- Bare `prjpcb` is a command group/help entry point; the config-first workflow
  lives under `prjpcb create`.
- Generated project configs use `altium_cruncher.project_skeleton.a0`.
- No-target `prjpcb create` first-run output writes `prjpcb_init.jsonc` with a
  blank line before the message and an explicit edit/rerun instruction.
- Generated mechanical kind config is explicit:
  `pcb.mechanical_layers` contains single/unpaired rows, and
  `pcb.mechanical_layer_pairs` contains grouped `top`/`bottom` rows.
- Generated JSONC headers document valid mechanical layer ids, indexes, default
  names, and mechanical layer kind enum values.
- The generated config does not emit `pair_index`; the legacy flat pair form
  remains accepted for compatibility.
- Contract filenames under `docs/contracts` use `.a0` versions. The active list
  is maintained in `docs/contracts/README.md`.
- Latest published `wn-geometer` on the configured index is `2026.6.10`, which
  matches the local pin. The Python planar-step interface accepts an opaque
  request mapping and exposes no newer request schema literal, so
  `geometry.planar_step.request.a0` remains unchanged.

## Implementation Slices

| Slice | Status | Description | Exit Criteria |
| --- | --- | --- | --- |
| S0 | done | Add project skeleton commands and MCO operations. | `prjpcb` creates PrjPcb, SchDoc, PcbDoc, project parameters, and project document links through MCO. |
| S1 | done | Improve no-target create workflow. | First `prjpcb create` run writes `prjpcb_init.jsonc`; later no-target runs create from that config. |
| S2 | done | Make generated configs editable. | JSONC output contains explicit sheet, project parameter, rigid stack, and mechanical layer kind fields. |
| S3 | done | Group mechanical layer pairs. | Generated config presents paired mechanical layers as `top`/`bottom` objects without `pair_index`. |
| S4 | done | Normalize public contract ids. | `altium_cruncher`-owned schemas use `altium_cruncher.*.a0`; PCB SVG and Geometer boundary exceptions are preserved. |
| S5 | done | Add standalone document create configs. | `schdoc create` and `pcbdoc create` write/read config templates whose child shapes match `prjpcb`. |
| S6 | active | Review the large public-contract diff. | Eli confirms public names and generated config shape before commit/release. |
| S6a | done | Confirm simple library create shape. | `schlib` and `pcblib` expose `create` subcommands for future expansion, but do not add create config files. |
| S7 | pending | Release signoff. | Focused tests remain clean, full release checks run when Eli asks to release. |

## Validation Snapshot

Focused checks passed before the final release-date bump:

```powershell
uv run --extra test pytest tests\test_command_manifest.py tests\test_bom_pnp_model.py tests\test_bom_outputs.py tests\test_pcblib_clean_config.py tests\test_pcb_layer_step.py tests\test_mco.py tests\test_prjpcb_command.py tests\test_mate.py tests\test_pcb_svg_view_selection.py tests\L99_signoff\test_L99_001_release_signoff.py tests\L99_signoff\test_L99_002_design_docs.py tests\L99_signoff\test_L99_004_interface_design_docs.py tests\L99_signoff\test_L99_005_config_contracts.py
uv run --extra test ruff check src\py\altium_cruncher\altium_clean.py src\py\altium_cruncher\altium_cruncher_cmd_bom.py src\py\altium_cruncher\altium_cruncher_cmd_easyeda_import.py src\py\altium_cruncher\altium_cruncher_cmd_extract.py src\py\altium_cruncher\altium_cruncher_cmd_prjpcb.py src\py\altium_cruncher\altium_cruncher_mate.py src\py\altium_cruncher\altium_cruncher_mate_parts.py src\py\altium_cruncher\altium_cruncher_mco.py src\py\altium_cruncher\altium_cruncher_pcb_layer_step.py src\py\altium_cruncher\altium_cruncher_pcb_layer_step_config.py src\py\altium_cruncher\altium_cruncher_project_profiles.py src\py\altium_cruncher\altium_pcblib_clean.py src\py\altium_cruncher\bom_pnp_model.py tests\test_bom_outputs.py tests\test_bom_pnp_model.py tests\test_command_manifest.py tests\test_mate.py tests\test_mco.py tests\test_pcb_layer_step.py tests\test_pcb_svg_view_selection.py tests\test_pcblib_clean_config.py tests\test_prjpcb_command.py tests\L99_signoff\test_L99_001_release_signoff.py tests\L99_signoff\test_L99_002_design_docs.py tests\L99_signoff\test_L99_004_interface_design_docs.py tests\L99_signoff\test_L99_005_config_contracts.py
```

Result: `149 passed`; ruff clean.

## Open Items

- Review generated `prjpcb` config wording and mechanical layer defaults before
  commit.
- Keep unrelated scratch files under `tests/assets/projects` out of commits
  unless Eli explicitly promotes them.
- Run full release signoff only when the release path resumes.
