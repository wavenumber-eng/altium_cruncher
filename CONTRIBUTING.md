# Contributing

`altium-cruncher` accepts direct public pull requests once CI is enabled.

Use `uv` for local development and test commands. Public CLI install
documentation should prefer `uv tool install altium-cruncher`.

Before opening a PR:

1. Keep changes focused on one command, contract, or infrastructure slice.
2. Add or update tests for every public command behavior change.
3. Update docs for public interfaces, JSON output, or config formats.
4. Justify every new public feature, command, and dependency in the commit,
   PR, or linked plan.
5. Run package tests and signoff locally.

Minimize external dependencies. This is a general Wavenumber tool convention.
A new dependency must explain why the standard library and existing project
dependencies are not enough, whether it is runtime/optional/test-only, its
license compatibility, and the expected packaging impact.

The top-level CLI should stay an orchestrator. Public subcommands should keep
command-specific parser setup and behavior in command modules, including simple
commands.

Expected local checks:

```powershell
uv run pytest
uv run python scripts\py_signoff.py --root .
```

Release decisions, compatibility policy, and public contract changes should be
recorded in `docs/adrs/`.
