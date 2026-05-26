# Altium Cruncher

`altium-cruncher` is a cross-platform command-line application for Altium file
workflows. It is intended for users who want useful Altium utilities without
writing Python.

The package consumes the public `altium-monkey` library and keeps higher-level
command behavior here: SVG export, PCB layer STEP export, extraction, BOM/PnP
output, netlist export, cleanup, project decomposition, and EasyEDA import
workflows.

## Install

The intended user install path is `pipx`:

```powershell
pipx install altium-cruncher
altium-cruncher --help
```

During local development:

```powershell
uv sync --extra test
uv run altium-cruncher --help
uv run python -m altium_cruncher version
```

EasyEDA commands require `easyeda-monkey` to be installed in the same
environment:

```powershell
pipx inject altium-cruncher easyeda-monkey
```

Until `easyeda-monkey` is published as its own public package, local EasyEDA
testing can install the sibling source checkout explicitly. The
`altium-cruncher[easyeda]` extra should be added after `easyeda-monkey` is
available on PyPI.

## Commands

The current migrated command set includes:

- `version`
- `sch-svg`
- `pcb-svg`
- `pcb-layer-step`
- `svg`
- `pcblib-footprint-3d`
- `bom`
- `pnp`
- `netlist`
- `extract`
- `easyeda-import`
- `easyeda-review`
- `easyeda-footprint-review`
- `split`
- `merge`
- `megamaid`
- `clean`

Compact JSON output is a core direction for machine-consumable Altium design
data, but the first standalone milestone prioritizes command parity and
cross-platform packaging.

## Tests

Run package-local tests:

```powershell
uv run pytest
```

Run signoff:

```powershell
uv run python scripts\py_signoff.py --root .
```

This repository is being moved toward `wn-rack` test strata with an
`L99_signoff` lane. Signoff policy will cover command manifests, public command
tests, PEP 257-style docstrings, architecture/design documentation, JSON/config
contracts, and package build/install smoke.

## Architecture Docs

- `docs/adrs/` records accepted architecture decisions.
- `docs/design/` records durable interface, command, data-flow, and format
  design notes.
- `contracts/` stores stable schemas and conformance examples for public JSON
  or config formats.

## Release Policy

The first ADR will define versioning, tagging, release, and traceability. The
intended release workflow is GitHub Actions plus PyPI Trusted Publishing/OIDC.
Local Twine upload is fallback only.
