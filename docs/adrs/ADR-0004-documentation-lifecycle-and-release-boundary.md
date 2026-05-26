# ADR-0004: Documentation Lifecycle And Release Boundary

## Status

Accepted.

## Context

`docs/plans/` and `docs/research/` are useful while work is in progress. They
can contain local task notes, migration checklists, open questions, false
starts, source links, raw reverse-engineering observations, and coordination
details that should not become public release material.

Once a plan is complete, durable information should not remain trapped in the
plan. Decisions, useful discoveries, format details, interface rationale,
contract requirements, and reusable artifacts need to move into stable docs that
developers and users can rely on.

## Decision

`docs/plans/` and `docs/research/` are developer-only working material and are
excluded from release artifacts.

When a plan completes, any useful durable output must be promoted before the
plan is considered retired:

- architecture decisions go to `docs/adrs/`;
- canonical format descriptions go to `docs/canonical_format/`;
- interface, command, data-flow, and explanatory format docs go to
  `docs/design/`;
- machine-readable schemas and examples go to `docs/contracts/` when applicable;
- executable behavior expectations go into Rack strata and tests;
- reusable examples or fixtures go into the package's public example/test
  locations when they are intended for users or downstream consumers.

Completed plans may remain in the repository as development history, but they
are not the source of truth for released behavior.

## Consequences

Release artifacts can include stable reference docs while excluding
`docs/plans/` and `docs/research/`.

Reviewers may block a completed work package if important results only exist in
a plan and have not been promoted to ADRs, design docs, contracts, examples, or
tests.
