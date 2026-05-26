# ADR-0002: CLI Install And Dependency Discipline

Status: accepted
Date: 2026-05-26

## Context

`altium-cruncher` is a public command-line application. It should be easy for
new users to install, easy for WN workspace setup to pin, and predictable for
CI to smoke test.

Wavenumber tools also need a shared discipline around dependencies and CLI
command layout. Application packages may carry more dependencies than core
libraries, but every dependency still creates install, packaging, CI, and
support cost.

`altium-cruncher` imports `altium-monkey` for normal operation. Because
`altium-monkey` is AGPL-3.0-or-later, the `altium-cruncher` package remains
AGPL-3.0-or-later.

## Decision

The public CLI install path is:

```powershell
uv tool install altium-cruncher
uv tool update-shell
altium-cruncher --version
```

WN workspace setup/update should install pinned released tool versions with
`uv tool install --force`, then smoke test the generated executable.

Local source development may replace a released tool with an editable checkout:

```powershell
uv tool install --force --editable C:\path\to\altium_cruncher
```

The top-level CLI module should be an orchestrator. It may own global options,
root parser setup, command registration, and dispatch. Public subcommands should
own command-specific parser setup and behavior in command modules, including
simple commands.

Every new public feature or command must justify itself in the commit, PR, or
linked plan.

Every new dependency must explain:

- why the dependency is needed;
- why the standard library or existing project dependencies are not sufficient;
- expected install/package impact;
- license compatibility;
- whether the dependency is required, optional, or test-only.

## Consequences

`pipx` can remain a possible user fallback, but it is not the primary install
path documented for Wavenumber tools.

Reviewers can reject command or dependency additions that lack justification,
even when tests pass.

The existing migrated CLI already has many command modules, but first-release
cleanup should avoid adding new command behavior to the top-level CLI module.
