# Dependency Audit

Status: initial audit
Last updated: 2026-05-27

## Purpose

This audit records current private-workspace references that must be addressed
before the standalone `altium-cruncher` repo fully replaces the private
`toolz/altium_cruncher` package.

## Runtime Dependencies

- `openpyxl` is an intentional runtime dependency for BOM/PnP/JLC spreadsheet
  output. It matches the existing `bom_cruncher` spreadsheet stack and avoids
  hand-written OpenXML as the command grows support for DNP row highlighting,
  text-preserved package fields such as `0603`, freeze panes, and future review
  formatting.
- `json-with-comments` is an intentional small runtime dependency for
  user-editable command configs. It accepts normal JSON plus JSONC comments and
  trailing commas so users can temporarily disable config sections while
  comparing output. Generated artifacts and checked-in contract examples remain
  strict JSON.

## Toolz

Current private state:

- `toolz/pyproject.toml` still includes workspace member `altium_cruncher`.
- `toolz/pyproject.toml` still publishes `wn-altium-cruncher` from the private
  workspace member.
- `toolz/build_bin.py` exposes the private workspace script as
  `toolz/bin/altium-cruncher`.
- `toolz/setup.ps1` and `toolz/setup.sh` still verify that local wrapper.
- private tests and docs under `toolz/altium_cruncher` still reference the old
  package location.

Required migration:

- keep the private copy until the standalone package has been pushed and CI is
  green;
- after public release, remove `toolz/altium_cruncher` from the workspace
  members;
- update wrapper generation so `altium-cruncher` comes from the standalone
  package or from `wn-hw` installer management, not private `toolz`;
- keep native `altium_cruncher_native` under `altium_monkey` separate from the
  Python app package.

## Appz

Current private state:

- root `appz/pyproject.toml` points `wn-altium-cruncher` at
  `../toolz/altium_cruncher`;
- `appz/lib_cruncher/pyproject.toml` points `wn-altium-cruncher` at
  `../../toolz/altium_cruncher`;
- `lib_cruncher` imports `altium_cruncher.altium_clean` and
  `altium_cruncher.altium_pcblib_clean` directly.

Required migration:

- switch `appz` and `lib_cruncher` to public `altium-cruncher`;
- decide whether `lib_cruncher` should depend on application internals such as
  clean helpers or whether those helpers should move to `altium-monkey` later;
- add an app-level test after the dependency change so CAD import and PcbLib
  cleaning still work.

## wn-hw

Current private state:

- workspace docs still refer to running `altium_cruncher` from `toolz`;
- `config/workspace.json` has no standalone `altium_cruncher` repo entry;
- setup/update only adds sibling `bin` folders from existing repos.

Required migration:

- add a standalone `altium_cruncher` repo/dependency entry after the public repo
  is pushed;
- install or expose `altium-cruncher` during `setup` and `update`;
- add a workspace test that resolves `altium-cruncher` from PATH and checks
  `--version`;
- remove stale `uv run --project ... toolz/altium_cruncher` guidance once the
  workspace executable path is verified.

## EasyEDA

Current private state:

- EasyEDA command implementation still imports `easyeda_monkey` when the
  optional package is installed;
- standalone `altium-cruncher` treats EasyEDA commands as placeholders when
  `easyeda-monkey` is missing.
- `easyeda-monkey==2026.5.26` is now public on PyPI and linked through the
  `altium-cruncher[easyeda]` optional extra.

Required migration:

- add an EasyEDA-extra test lane that installs `altium-cruncher[easyeda]` and
  runs fixture-backed EasyEDA workflows;
- keep base-install placeholder behavior tested when the optional dependency is
  absent.
