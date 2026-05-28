# Contributing

`altium-cruncher` accepts direct public pull requests once CI is enabled.

Use `uv` for local development and test commands. Public CLI install
documentation should prefer `uv tool install altium-cruncher`.

Use the GitHub issue templates for bugs and feature requests. Include the exact
command, `altium-cruncher version` output, and only reproduction files that can
be shared publicly.

## Contribution Workflow

Open an issue or GitHub Discussion before starting a public PR, unless the
change is a small documentation typo or an obviously isolated bug fix.

For any public command, config, JSON, generated artifact, API, dependency, or
workflow change, contributors should agree on the design first. That discussion
should settle the intended command behavior, config shape and defaults, expected
outputs, compatibility impact, docs updates, and required tests before a PR is
considered ready for review.

PRs that change public behavior should link the issue or discussion where the
design was agreed and include the matching design-doc, contract, and test
updates.

## Commit Messages And Human Signoff

Commit messages, PR summaries, and signoff notes should be concise, factual,
and limited to what changed, why it changed, and how it was validated. Do not
use emojis, decorative prefixes, or marketing-style language.

Every PR signoff should identify the responsible human by name or GitHub user
ID. If Claude or another AI coding agent materially assisted with the change,
include that as an implementation note, not as the accountable signoff. Keep it
to the point: mention the files or behavior changed, tests run, and any known
limitations.

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
