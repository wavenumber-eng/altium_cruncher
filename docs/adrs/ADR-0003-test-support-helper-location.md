# ADR-0003: Test Support Helper Location

## Status

Accepted.

## Context

Some helper scripts exist only to support Rack strata, L99 signoff, release
artifact tests, or test reporting. Keeping those helpers in a top-level
`scripts/` folder makes them look like general project tooling instead of part
of the test contract.

## Decision

Scripts whose primary purpose is to support tests, Rack strata, L99 signoff, or
release artifact testing live under the test tree.

The preferred shared location is:

```text
tests/support_scripts/
```

A stratum may also keep tightly scoped helpers under:

```text
tests/Lxx_name/support_scripts/
```

Use the shared folder when more than one stratum, workflow, or release step may
call the helper.

## Consequences

CI, release workflows, docs, and tests should call test-support helpers through
their `tests/...` paths.

Top-level `scripts/` is reserved for non-test project automation. If a helper
becomes part of signoff or test execution, move it into the test tree and
update references in the same change.
