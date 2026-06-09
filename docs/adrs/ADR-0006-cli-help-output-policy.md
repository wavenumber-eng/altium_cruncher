# ADR-0006: CLI Help Output Policy

Status: accepted
Date: 2026-06-09

## Context

`altium-cruncher` has a growing public command surface. New commands often add
subcommands, aliases, JSON modes, and workflow-specific options. Help output is
the first discovery surface for terminal users, so command lists need to be
easy to scan without each command module inventing its own formatter.

## Decision

CLI help formatting is owned by the shared parser layer.

The global parser highlights command and subcommand names when help is written
to an interactive terminal. It must respect `NO_COLOR` and `TERM=dumb`, and
captured help output must stay plain text for tests, scripts, and docs.

Command modules should provide accurate `help` and `description` strings, but
should not directly embed ANSI color in help text. Compatibility aliases may be
registered with suppressed help so old invocations keep working without adding
noise to command discovery.

Help text should prefer:

- concise command descriptions that start with a verb;
- command names and important choices surfaced by argparse command lists;
- stable argument names that match MCO and config contracts where practical;
- no decorative color in non-interactive output.

## Consequences

New commands get consistent help behavior by registering with the shared
`CruncherArgumentParser` hierarchy. Tests cover parser-level color formatting
and command-specific help only needs to assert the visible command contract.
