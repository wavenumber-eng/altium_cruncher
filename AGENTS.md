# AGENTS.md

## Purpose

This repository owns the standalone public `altium-cruncher` Python package and
CLI. It builds higher-level Altium workflows on top of the public
`altium-monkey` package.

## Setup

Use `uv` with Python 3.14 for local development (`.python-version` selects it):

```powershell
uv sync --all-extras
uv run rack run --all
```

Do not hand-edit `uv.lock`. Update dependency pins in `pyproject.toml`, then
regenerate the lockfile with `uv lock`.

## Boundaries

- Runtime package code lives under `src/py/altium_cruncher`.
- Public command contracts live under `docs/contracts`.
- Public design documentation lives under `docs/design`.
- Working plans live under `docs/plans` and are excluded from release
  artifacts.
- Public examples live under `examples`.
- Test-support scripts live under `tests/support_scripts`.

Do not develop new `altium-cruncher` features in the old monorepo copy under
`toolz/altium_cruncher`; that copy is stale. Use this standalone checkout.

## Public Surface

All Cruncher-owned public JSON/JSONC contracts are authored in
`src/tsp/altium_cruncher`: config structure, static defaults and help in `config`,
operation arguments in `mco`, and emitted payloads in `outputs`.
See `docs/design/public-contract-authority.md` for ownership boundaries.
Run `npm ci --ignore-scripts`, then
`npm run generate:contracts` after edits. Do not hand-edit generated schemas,
Python DTO/resources, TypeScript bindings/validator, or the generated field guide.
`npm run check:contracts`, `npm run check:typescript` and `npm run check:browser`
check freshness, complete public-schema coverage and the web consumer.
MCO operation/argument models and their ordered container live under
`src/tsp/altium_cruncher/mco`; generate their schemas, catalog metadata, defaults
and template help with the same commands. Add a Python handler registration when
adding a built-in operation. Preserve reached-operation validation, failure
branches, custom registries and existing dry-run semantics.
Keep authored overrides presence-preserving; preset merging, layer resolution,
MCO compilation, native profile/stack construction and rendering remain Python
behavior. Node is development tooling, not a CLI runtime
requirement.

Command names, CLI arguments, config schemas, generated JSON, and generated file
layouts are public contracts. Update the matching design document, command or
config manifest, and tests when changing them.

## Signoff

Fast local checks may run focused tests during development. Release-facing
changes should pass:

```powershell
uv run --extra test rack run --all
uv run --extra test python -m build
uv run --extra test twine check dist/*
uv run --extra test python tests/support_scripts/install_test.py
```

Run `uvx --from git+https://github.com/wavenumber-eng/wn-dev-std.git
wn-dev-std check . --format json` when checking alignment with the Wavenumber
development standard.
