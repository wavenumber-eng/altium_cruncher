# AGENTS.md

## Purpose

This repository owns the standalone public `altium-cruncher` Python package and
CLI. It builds higher-level Altium workflows on top of the public
`altium-monkey` package.

## Setup

Use `uv` for local development:

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
