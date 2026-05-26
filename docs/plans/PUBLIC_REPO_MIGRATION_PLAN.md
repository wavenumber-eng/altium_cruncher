# Altium Cruncher Public Repo Migration Plan

Status: bootstrap in progress
Last updated: 2026-05-26

## Goal

Move `altium_cruncher` out of the private `toolz` monorepo into the public
repository at <https://github.com/wavenumber-eng/altium_cruncher>.

The standalone repo should be the public source of truth. Unlike
`altium-monkey`, it should not use a generated public-release/export flow.

The package is an application/CLI for users who want Altium utilities without
writing Python. It should consume the public `altium-monkey` package as a real
downstream dependency, ideally tracking the latest released date version.

## Product Direction

`altium_cruncher` should prioritize command parity first:

1. inventory current commands from `toolz/altium_cruncher`;
2. migrate or reimplement stable commands in the standalone repo;
3. add installable console entry points;
4. add tests and CI for each migrated command;
5. remove the private `toolz` package only after the public repo is viable.

Compact JSON output is a central product direction because exposing Altium
design data in machine-consumable form is one of the main reasons this tool
exists. However, the first migration milestone should not block on designing a
complete design-query JSON contract. Initial command migration should preserve
clean output boundaries, stable exit codes, and structured error behavior so
the richer JSON contract can be promoted later.

## Repository Contract

The standalone public repo should include:

- `pyproject.toml`;
- `src/altium_cruncher/`;
- `tests/`;
- `rack.toml` and Rack strata manifests;
- `README.md`;
- `LICENSE`;
- `CONTRIBUTING.md`;
- issue templates;
- pull-request template;
- GitHub Actions CI for Windows, macOS, and Linux.
- `docs/adrs/` for architecture decision records;
- `docs/design/` for interface, command, data-flow, and format design
  documentation;
- `contracts/` for machine-readable schemas and contract examples where a
  command exposes stable JSON or config formats.

One of the first ADRs must define versioning, tagging, release, and
traceability policy. It should align with the current Geometer-style package
discipline:

- date-versioned Python package releases;
- explicit PyPI publish flow;
- annotated Git tags for released source commits;
- release notes or changelog expectations;
- compatibility policy for public commands, JSON outputs, and config formats;
- rules for when direct PRs can be released.

The preferred release workflow should be GitHub-driven rather than a local-only
Twine ritual:

- PR and push CI run Rack tests, `L99_signoff`, package build, clean-install
  smoke, and `twine check`;
- `main` is protected and requires passing CI before merge;
- release publishing uses GitHub Actions with PyPI Trusted Publishing / OIDC
  where possible, not long-lived local PyPI tokens;
- releases are triggered from a protected tag or GitHub Release, using tags such
  as `vYYYY.M.D`;
- release jobs verify package version metadata matches the tag;
- release jobs verify release notes/changelog mention the version;
- release jobs build wheel/sdist from the tagged source and publish to PyPI;
- local Twine upload remains an emergency/manual fallback, not the normal path.

The likely package and entry-point names are:

- distribution: `altium-cruncher`;
- import package: `altium_cruncher`;
- console script: `altium-cruncher`.

The package should be easy to install with `pipx`, producing normal executable
entry points on Windows, macOS, and Linux. Nuitka or PyInstaller packaging can
be evaluated later, but the first packaging target should be a normal Python
package with console scripts.

## Workspace Installer Integration

The standalone package must also work through the WN workspace setup/update
flow, not only through direct developer commands.

`wn-hw` integration is a first-release blocker:

- add a standalone `altium_cruncher` repo/dependency entry to the workspace
  manifest when the public repo is ready to consume;
- decide whether `wn-hw` installs the released package with `pipx`, installs
  the local source checkout in editable mode, or creates workspace-local
  wrappers;
- ensure the resulting script/executable directory is on PATH after
  `setup.ps1`/`setup.sh` and after `update.ps1`/`update.sh`;
- standardize workspace workflows on the single public console name
  `altium-cruncher`; the import/module name remains `altium_cruncher`;
- add an installer smoke test that starts from the workspace shell and runs
  `altium-cruncher --version`;
- remove old `uv run --project ... toolz/altium_cruncher` assumptions from
  WN docs/scripts only after the standalone executable path is verified.

## Dependency Policy

`altium_cruncher` is an application package, so it can carry richer dependencies
than core `altium-monkey`.

Expected direct dependencies include:

- public `altium-monkey`;
- `wn-geometer` where command features need geometry support;
- other application-level libraries as needed.

The package must not import private `toolz` modules. `wn-hw` should eventually
clone/use this standalone repo as an external dependency, similar to
`geometer`.

## Test Strategy

The standalone repo should use `wn-rack` for tests and signoff.

Tests must run from the repo's own `tests/` folder. Fixtures must be
redistributable; initial candidates should come from the existing
`altium-monkey` public-release examples/assets where practical.

Initial Rack shape:

- `L0_foundation`: package import, version, CLI help, console entry point;
- `L1_command_manifest`: every registered command has docs, help, and test
  ownership;
- `L2_assets`: redistributable fixture discovery and asset-integrity checks;
- `L3_commands`: fixture-backed command smoke tests;
- `L4_outputs`: structured/golden output checks for selected stable commands;
- `L9_cross_platform`: path handling, Unicode filenames, output folders, and
  OS-specific install/runtime behavior;
- `L99_signoff`: type coverage, complexity checks, command coverage, docs
  links, PEP 257-style docstring coverage, design/contract documentation
  coverage, contract conformance tests, no private paths, no `toolz` imports,
  package build/install smoke.

The signoff model should copy the useful shape from the in-progress
`data_models` worktree:

- ADRs record architecture choices and compatibility policy;
- `docs/design/` records durable interface and data-flow design;
- `contracts/` stores stable schema/config artifacts;
- contract conformance helpers live in tests and are reused by command tests;
- L99 checks prevent new public surfaces from landing without matching docs,
  contracts, and tests.

All package functions and methods should have PEP 257-style docstrings. Public
interfaces, command output formats, JSON config files, and any stable compact
JSON payloads must have corresponding design docs and conformance tests before
they are treated as release-ready.

Before migrating commands, perform an evidence pass:

- inventory existing `toolz/altium_cruncher` commands;
- inventory private `toolz-tests` coverage for those commands;
- identify reusable public fixtures from `altium_monkey_public`;
- identify private-corpus-only tests that need replacement fixtures;
- map each command to existing coverage, missing coverage, public fixture
  availability, and dependency blockers.

## Command Coverage Guardrails

The repo should have a command manifest used by tests and CI.

Every public command should have:

- manifest entry;
- CLI help smoke test;
- docs or README coverage;
- at least one behavioral test, or an explicit waiver with rationale.

`L99_signoff` should fail when a new public command is added without the
required manifest/test/doc coverage.

## EasyEDA Commands

Some newer commands convert EasyEDA designs and currently depend on private
`toolz` `ezeda_monkey` work.

Do not allow these commands to make the public `altium_cruncher` package depend
on private modules.

The intended direction is to move `ezeda_monkey` out of `toolz` into its own
public repository at <https://github.com/wavenumber-eng/easyeda_monkey> and
publish it to PyPI as a normal dependency. That package should have the same
public-repo requirements as `altium_cruncher`:

- `pyproject.toml` and installable package metadata;
- tests that run from its own repo;
- `wn-rack` strata and `L99_signoff`;
- CI on Windows, macOS, and Linux where practical;
- GitHub Actions release automation with PyPI Trusted Publishing / OIDC where
  possible;
- contributor guide, license, issue templates, and PR template;
- no private `toolz` imports in public package code;
- direct PRs allowed only through CI/signoff.
- the same date-versioning policy used by current Wavenumber Python packages.
- the same ADR/design-doc/contract-conformance and PEP 257 docstring signoff
  expectations as `altium_cruncher`.
- an early ADR for versioning, tagging, release, and traceability policy,
  aligned with the `altium_cruncher` policy.

As part of the split, audit `toolz` and `appz` for imports and workspace
dependencies that currently reach into private `ezeda_monkey` or
`altium_cruncher` source. Public-facing packages and applications should consume
the public PyPI/GitHub versions once those repos exist.

First-release options for `altium_cruncher`:

1. defer the EasyEDA commands until public `ezeda_monkey` exists;
2. keep them documented as planned/experimental but absent from the public CLI;
3. expose them later behind an optional extra such as
   `altium-cruncher[easyeda]` once public `ezeda_monkey` is packageable.

## AI Skill / Assistant Workflow

The public `altium_monkey` PR
<https://github.com/wavenumber-eng/altium_monkey/pull/1> adds a project-local
Claude Code skill for reading Altium schematics through compact subcommands
such as `summary`, `components`, `nets`, `connections`, `bom`, `sheet`, and
`raw`.

That concept belongs in the `altium_cruncher` app layer rather than core
`altium-monkey`.

Preferred shape:

- implement the underlying design-query behavior as stable
  `altium-cruncher` commands;
- keep compact JSON as a supported machine-consumable mode;
- make any Codex/Claude skill a thin wrapper around the installed CLI;
- do not duplicate parsing logic inside the skill.

## Migration Phases

1. Design and inventory only.
   - Status: substantially complete for the first public bootstrap.
   - Create the migration plan.
   - Inventory commands, tests, fixtures, private dependencies, and command
     outputs.
   - Audit `toolz` and `appz` for private `altium_cruncher` and
     `ezeda_monkey` imports that need to become public package dependencies.

2. Bootstrap the public repo.
   - Status: initial local bootstrap complete; awaiting push/CI.
   - Add packaging, source layout, Rack tests, CI, project hygiene files, and
     a minimal CLI skeleton.
   - Add the initial versioning/tagging/release-policy ADR before the first
     package release.

3. Migrate stable commands.
   - Status: current stable command modules copied from private `toolz` and
     smoke-tested against Hydroscope for the first public slice.
   - Move commands one family at a time.
   - Add manifest entries, tests, and docs as each command lands.

4. Add command parity gates.
   - Status: initial manifest/help checks, `L3_public_workflows`, and
     `L99_signoff` are wired; stricter coverage enforcement remains.
   - Enforce manifest/test/doc coverage.
   - Add `L99_signoff` and package build/install smoke.

5. Wire into `wn-hw`.
   - Status: not started; documented as a first-release blocker.
   - Add standalone `altium_cruncher` as a cloned dependency.
   - Update workspace scripts/configuration.
   - Ensure setup/update exposes the console executable path.
   - Add a workspace installer smoke test for the public console script name.

6. Remove from `toolz`.
   - Status: blocked until public repo is pushed, CI is green, and app/workspace
     consumers are migrated.
   - Delete the private `toolz/altium_cruncher` package only after the public
     repo has equivalent command coverage for the selected public command set.
   - Leave a short tombstone pointing to the public repo if useful.

## First Slice Exit Criteria

The first migration slice is complete when:

- the public repo has installable package metadata;
- `pipx install` can expose the CLI from a built wheel;
- `wn-hw` setup/update can expose the CLI executable without a manual PATH fix;
- Rack tests run from the standalone repo;
- CI runs on Windows, macOS, and Linux;
- at least one stable command is migrated with fixture-backed coverage;
- the command inventory clearly states which commands remain private,
  deferred, or blocked.

Current local status:

- package metadata, console script, CI/release workflow, changelog, ADRs, design
  docs, and contracts are present;
- `rack run --all` passes locally with `L0_public_cli`,
  `L3_public_workflows`, and `L99_signoff`;
- built-wheel install smoke passes locally and verifies the public console
  script through PATH inside a clean venv;
- `ruff` is clean and `py_signoff` is clean; pyright remains an explicit
  backlog item rather than a hard release gate for this bootstrap slice;
- `wn-hw` setup/update integration and public GitHub CI remain the major first
  release blockers.
