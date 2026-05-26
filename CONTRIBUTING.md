# Contributing

`altium-cruncher` accepts direct public pull requests once CI is enabled.

Use `uv` for local development and test commands. Public CLI install
documentation should prefer `uv tool install altium-cruncher`.

Before opening a PR:

1. Keep changes focused on one command, contract, or infrastructure slice.
2. Add or update tests for every public command behavior change.
3. Update docs for public commands, interfaces, JSON output, or config formats.
4. Justify every new public feature, command, and dependency in the commit,
   PR, or linked plan.
5. Run package tests and signoff locally.

Minimize external dependencies. A new dependency must explain why the standard
library and existing project dependencies are not enough, whether it is
runtime/optional/test-only, its license compatibility, and the expected
packaging impact.

The top-level CLI should stay an orchestrator. Public subcommands should keep
command-specific parser setup and behavior in command modules, including simple
commands.

Design documentation is release-signoff material:

- every command in `docs/contracts/command_manifest.v0.json` needs
  `docs/design/cli/<command>.html`;
- command docs must cover usage patterns, invocations, arguments, output, and
  tests;
- commands with config files or stable machine-readable output need a contract
  under `docs/contracts/` plus conformance tests;
- every public dataclass and listed major interface needs an API design section
  under `docs/design/api/` with rationale, purpose, test requirements, working
  definition, and Rack test ownership.

Expected local checks:

```powershell
uv run --extra test rack run --all
```

Rack is the primary local gate. Additional release artifact tests should
also run before publishing.

Release decisions, compatibility policy, and public contract changes should be
recorded in `docs/adrs/`.
