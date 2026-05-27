# Altium Cruncher

`altium-cruncher` is a cross-platform command-line application for Altium file
workflows. It is intended for users who want useful Altium utilities without
writing Python.

The package consumes the public `altium-monkey` library and keeps higher-level
command behavior here: SVG export, PCB layer STEP export, extraction, BOM/PnP
output, netlist export, cleanup, project decomposition, and EasyEDA import
workflows.

## Install

Install `uv` first if it is not already available:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

On macOS or Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

The intended user install path is `uv tool install`:

```powershell
uv tool install altium-cruncher
uv tool update-shell
altium-cruncher --help
```

During local development:

```powershell
uv sync --extra test
uv run altium-cruncher --help
uv run python -m altium_cruncher version
```

EasyEDA commands are optional. Install the `easyeda` extra when those workflows
are needed:

```powershell
uv tool install --force "altium-cruncher[easyeda]"
```

The equivalent explicit form is:

```powershell
uv tool install --force --with easyeda-monkey altium-cruncher
```

During local EasyEDA development:

```powershell
uv sync --extra test --extra easyeda
uv run --extra easyeda altium-cruncher easyeda-import --help
```

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
- `jlc`
- `netlist`
- `extract`
- `easyeda-import`
- `easyeda-review`
- `easyeda-footprint-review`
- `split`
- `merge`
- `megamaid`
- `clean`

`pcb-svg` includes normal layer SVG output, top/bottom assembly SVG views with
geometer-backed HLR projection of embedded STEP models, and an optional
synthetic `BOARD_CUTOUTS` layer for board-profile cutouts. The A0 PCB SVG
config uses `pcb.svg.config` by default and fits SVGs tightly around the board
outline while metadata preserves Altium-coordinate placement and transform data.
User-editable config files may use JSONC comments and trailing commas.

Compact JSON output is a core direction for machine-consumable Altium design
data, but the first standalone milestone prioritizes command parity and
cross-platform packaging.

New commands should keep the top-level CLI as an orchestrator. Command-specific
parser setup and behavior belong in command modules, including simple commands.
New commands, features, and external dependencies need explicit justification in
the commit, PR, or linked plan. Minimize dependencies unless there is a clear
install, licensing, and maintenance case.

## Tests

Run the Rack suite:

```powershell
uv run --extra test rack run --all
```

Run the built-wheel install test after `python -m build`:

```powershell
uv run --extra test python tests\support_scripts\install_test.py
```

Rack is the primary local gate. Current public strata are
`L0_public_cli` for command registration and `L3_public_workflows` for
fixture-backed CLI workflows. `L99_signoff` runs version-contract and Python
hygiene checks. Additional command parity gates will be added as public fixtures
and release policy are finalized. Signoff policy will cover command manifests,
public command tests, PEP 257-style docstrings, architecture/design
documentation, JSON/config contracts, and package build/install tests.

## Architecture Docs

- `docs/adrs/` records accepted architecture decisions.
- `docs/design/` records durable interface, command, data-flow, and format
  design notes.
- `docs/design/index.html` is the master design-doc entry point used by humans
  and signoff tooling.
- `docs/contracts/` stores stable schemas and conformance examples for public JSON
  or config formats.

## Release Policy

Versioning, tagging, release, and traceability are defined in
`docs/adrs/ADR-0001-versioning-tagging-release-policy.md`. The intended
release workflow is GitHub Actions plus PyPI Trusted Publishing/OIDC. Local
Twine upload is fallback only.

`altium-cruncher` remains AGPL-3.0-or-later because it imports and depends on
the AGPL `altium-monkey` package for normal operation.
