# Altium Cruncher

`altium-cruncher` is a cross-platform command-line application for Altium file
workflows. It is intended for users who want useful Altium utilities without
writing Python.

The package consumes the public `altium-monkey` library and keeps higher-level
command behavior here: SVG export, PCB layer STEP export, extraction, BOM/PnP
output, design JSON export, cleanup, project decomposition, and EasyEDA import
workflows.

## Install

### Windows Quick Install

For Windows users who are not already using Python tooling, the repository
includes a PowerShell installer wrapper. It installs `uv` if needed, installs
`altium-cruncher` as a `uv` tool, updates the shell PATH, and verifies the
install with `altium-cruncher version`.

From a source checkout or release source archive:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-altium-cruncher.ps1
```

To reinstall or update the tool:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-altium-cruncher.ps1 -Force
```

To include the optional experimental EasyEDA workflow:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-altium-cruncher.ps1 -IncludeEasyeda -Force
```

### Manual Install

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

The EasyEDA import command is optional and experimental. It generates SchLib,
PcbLib footprint, and downloaded 3D model assets by default, but 3D model
placement into the generated PcbLib is not implemented. Install the `easyeda`
extra when that workflow is needed:

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

Run `altium-cruncher <command> --help` for command-specific options.

| Command | Purpose | Status |
| --- | --- | --- |
| `version` | Print `altium-cruncher` and controlled dependency versions. | Public |
| `sch-svg` | Generate schematic SVG from SchDoc, PrjPcb, or SchLib inputs. | Public |
| `pcb-svg` | Generate PCB SVG views from PcbDoc or PrjPcb inputs. | Public, with beta HLR/pin-view areas |
| `pcb-layer-step` | Generate a colored STEP model for one PCB layer, intended for fixture-alignment workflows. | Public |
| `svg` | Run schematic SVG, PCB SVG, or both based on input. | Public |
| `bom` | Generate BOM output as CSV, JSON, or XLSX. | Public |
| `pnp` | Generate pick-and-place output as CSV, JSON, XLSX, or JLC CPL. | Public |
| `jlc` | Generate JLCPCB BOM and CPL outputs from an Altium project. | Public |
| `design` | Generate design JSON with nets, components, and SVG IDs. | Public |
| `extract` | Extract symbols, footprints, or IntLib sources from Altium design documents. | Public |
| `split` | Split a multi-symbol SchLib or multi-footprint PcbLib into individual files. | Public |
| `merge` | Merge multiple SchLib or PcbLib files into one library. | Public |
| `megamaid` | Decompose a PrjPcb into libraries, BOM, netlist, and embedded assets. | Public |
| `clean` | Normalize SchDoc, SchLib, or PcbLib assets using JSON/JSONC config. | Public |
| `easyeda-import` | Generate Altium SchLib, PcbLib footprint, and downloaded 3D assets from EasyEDA/LCSC data. | Optional experimental |

`pcb-svg` includes normal layer SVG output, top/bottom assembly SVG views with
geometer-backed HLR projection of embedded STEP models, and an optional
synthetic `BOARD_CUTOUTS` layer for board-profile cutouts. The A0 PCB SVG
config uses `pcb.svg.config` by default and fits SVGs tightly around the board
outline while metadata preserves Altium-coordinate placement and transform data.
User-editable config files may use JSONC comments and trailing commas.

The `pcb-svg` HLR and pin-oriented views are beta quality. Hidden-line
rendering, embedded STEP projection, pin visibility, and related details are
expected to improve, and current output may contain errors or omissions.

`easyeda-import` is experimental. Expect command behavior, generated artifacts,
config, and dependency details to change while this workflow matures.

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

GitHub Actions runs CI for pull requests and pushes to `main` on Ubuntu and
Windows. CI runs the Rack suite, builds the package, checks the distributions,
and runs the installed-console smoke test.

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

Current release notes are available in
`docs/releases/2026-05-28.md`.

`altium-cruncher` remains AGPL-3.0-or-later because it imports and depends on
the AGPL `altium-monkey` package for normal operation.
