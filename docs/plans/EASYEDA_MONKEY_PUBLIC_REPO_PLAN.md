# EasyEDA Monkey Public Repo Plan

Status: planned prerequisite
Last updated: 2026-05-26

## Goal

Stand up `easyeda-monkey` as its own public package before finalizing the
EasyEDA commands in `altium-cruncher`.

Repository target:

- GitHub: <https://github.com/wavenumber-eng/easyeda_monkey>
- Distribution: `easyeda-monkey`
- Import package: `easyeda_monkey`

`altium-cruncher` should not carry private EasyEDA implementation dependencies.
It should become a CLI/application consumer of the public `easyeda-monkey`
package once that package has the same quality and release shape as this repo.

## Release Blocker

The first official `altium-cruncher` release should not treat EasyEDA import
commands as complete until `easyeda-monkey` has a public package with passing
signoff and redistributable fixtures.

Allowed interim behavior in `altium-cruncher`:

- keep EasyEDA commands as missing-dependency placeholders;
- keep `altium-cruncher` tests that verify the placeholders fail clearly;
- keep direct EasyEDA behavioral tests out of the required release lane until
  they can consume public `easyeda-monkey`.

## CI/CD Proving Ground

`easyeda-monkey` should also be the simpler proving ground for the public
GitHub CI/CD flow before we depend on the same flow for a larger
`altium-cruncher` release.

Reasoning:

- the package surface is smaller than `altium-cruncher`;
- the dependency graph should be lighter;
- the command/API surface is easier to audit;
- CI failures should be easier to interpret;
- PyPI Trusted Publishing can be configured and verified with less release
  risk;
- the resulting workflow can become the template for `altium-cruncher` and
  future public Wavenumber packages.

The first `easyeda-monkey` release should prove:

- GitHub Actions runs the full required test/signoff/build/install lane;
- release tags match package versions;
- changelog/release notes are enforced;
- PyPI Trusted Publishing works from the intended workflow and environment;
- a clean install from PyPI works with `pip`, and `pipx` if a CLI is exposed;
- the published source commit, tag, GitHub release, and PyPI artifact are
  traceable to each other.

Once that flow works, mirror the corrected release automation back into
`altium-cruncher`.

## Repository Contract

`easyeda-monkey` should use the same public repo structure as
`altium-cruncher`:

- `pyproject.toml`;
- `src/py/easyeda_monkey/`;
- `tests/`;
- `rack.toml` plus Rack stratum manifests;
- `README.md`;
- `CHANGELOG.md`;
- `LICENSE`;
- `CONTRIBUTING.md`;
- issue templates and pull request template;
- GitHub Actions CI;
- GitHub Actions release workflow using PyPI Trusted Publishing/OIDC where
  possible;
- `docs/adrs/` for architecture decisions;
- `docs/design/` for interface, data-flow, command/API, and format design;
- `contracts/` for stable JSON/config schemas and conformance examples.

The first ADR should define versioning, tagging, release, and compatibility
policy. It should match the date-based Wavenumber package policy:

- normal release: `YYYY.M.D`;
- supplemental build release: `YYYY.M.D.N`;
- annotated release tags: `v<version>`;
- changelog entry required for each release;
- public APIs, CLI flags, config formats, and JSON output formats are
  compatibility surfaces.

## Signoff And Quality Gates

`easyeda-monkey` should meet the same signoff expectations as
`altium-cruncher`, not a reduced subset.

Required local and CI gates:

- `pytest` for the full test suite;
- `wn-rack` strata with `rack run --all`;
- `ruff check .`;
- Python signoff script with zero unwaived findings;
- package build via `python -m build`;
- `twine check dist/*`;
- clean-venv install smoke;
- optional `pipx` smoke when available;
- release workflow that reruns tests, Rack, signoff, build, `twine check`, and
  install smoke before publishing.

Required signoff policy:

- every public function and method has a PEP 257-style docstring;
- public interfaces have design docs under `docs/design/`;
- stable JSON/config formats have schemas or contract examples under
  `contracts/`;
- contract conformance tests exercise those schemas/examples;
- no imports from private `toolz`, private worktrees, or machine-local paths;
- no checked-in machine-local fixture paths;
- redistributable fixtures only;
- no command/API surface without matching docs and tests;
- any type-checking backlog is documented and ratcheted rather than ignored.

Initial Rack shape:

- `L0_foundation`: package import, version, basic parser/API smoke;
- `L1_contracts`: schemas, config examples, and fixture integrity;
- `L2_parsers`: EasyEDA JSON/input parsing with redistributable fixtures;
- `L3_converters`: Altium symbol/footprint conversion behavior;
- `L4_outputs`: stable output/golden checks for selected conversions;
- `L9_cross_platform`: path handling, Unicode filenames, and install/runtime
  behavior on supported OSes;
- `L99_signoff`: version contract, changelog, docs/contracts coverage,
  docstring coverage, no private imports, build/install smoke, and Python
  quality gates.

## Fixture Strategy

Fixtures must be public and redistributable.

First pass:

- inventory current private `toolz` EasyEDA fixtures and tests;
- classify fixtures as redistributable, replaceable, or private-only;
- move only redistributable fixtures into `easyeda-monkey`;
- create synthetic fixtures where private examples cannot be redistributed;
- document fixture provenance and intended coverage.

Fixture tests should cover:

- symbol parsing;
- footprint parsing;
- source preview/render helpers if kept public;
- Altium SchLib conversion;
- Altium PcbLib conversion;
- malformed input and clear error reporting.

## Altium Cruncher Integration

After `easyeda-monkey` is public and passing signoff:

1. add `easyeda-monkey` as an optional dependency of `altium-cruncher`;
2. expose an optional extra such as `altium-cruncher[easyeda]`;
3. keep `altium-cruncher` EasyEDA commands as thin CLI adapters over
   `easyeda-monkey`;
4. add two `altium-cruncher` test modes:
   - base install: EasyEDA commands report the missing dependency clearly;
   - EasyEDA extra installed: command workflows run against public fixtures;
5. document install guidance:
   - `pipx install altium-cruncher`;
   - `pipx inject altium-cruncher easyeda-monkey` or equivalent extra flow.

`altium-cruncher` should not duplicate EasyEDA parsing/conversion logic once the
public package exists.

## Migration Phases

1. Inventory and design.
   - Audit current `toolz` EasyEDA code, tests, fixtures, and private imports.
   - Write versioning/release ADR.
   - Write design docs for core input formats and conversion interfaces.

2. Bootstrap public repo.
   - Add packaging, source layout, README, license, contributing docs,
     templates, CI, release workflow, Rack, and signoff.
   - Add minimal import/version/build/install tests.

3. Move core EasyEDA package code.
   - Port parser and model code first.
   - Remove private `toolz` assumptions.
   - Add parser and contract fixtures.

4. Move conversion behavior.
   - Add symbol conversion tests.
   - Add footprint conversion tests.
   - Add stable output checks where practical.

5. Publish `easyeda-monkey`.
   - Run local and GitHub signoff.
   - Configure PyPI Trusted Publishing.
   - Use this release to validate the GitHub/PyPI CI/CD path end to end before
     relying on the same path for `altium-cruncher`.
   - Publish a date-versioned release.

6. Link into `altium-cruncher`.
   - Replace placeholders with optional dependency-backed command behavior.
   - Add base-install and extra-install test lanes.
   - Update command inventory, README, and release notes.

## Open Questions

- Which existing EasyEDA fixtures can be redistributed?
- Should `easyeda-monkey` expose only library APIs, or also a small standalone
  diagnostic CLI?
- Which output contracts should be stable in the first release versus marked
  experimental?
- Should Altium conversion helpers live entirely in `easyeda-monkey`, or should
  some reusable Altium writing helpers move down into `altium-monkey` later?
