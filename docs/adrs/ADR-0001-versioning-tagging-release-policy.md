# ADR-0001: Versioning, Tagging, And Release Policy

Status: accepted
Date: 2026-05-25

## Context

`altium-cruncher` is moving from the private `toolz` monorepo into a standalone
public repository. It will accept public PRs and publish Python packages to
PyPI, so releases need a clear source-of-truth policy and a repeatable
automation path.

## Decision

`altium-cruncher` uses date-based PEP 440 versions:

- normal release: `YYYY.M.D`
- supplemental build release: `YYYY.M.D.N`

The Git tag for a release is `v<version>`, for example `v2026.5.25`.

Release source is the standalone public repository. There is no generated
public-export flow.

The normal publishing path is GitHub Actions with PyPI Trusted Publishing /
OIDC:

1. merge to protected `main` after CI passes;
2. create an annotated `v<version>` tag or GitHub Release from the release
   commit;
3. release workflow verifies package version metadata matches the tag;
4. release workflow verifies release notes mention the version;
5. release workflow runs tests, signoff, package build, install tests, and
   `twine check`;
6. release workflow publishes wheel and sdist to PyPI.

Local Twine upload is reserved for emergency fallback.

Public command names, command-line flags, stable JSON outputs, and config file
formats are compatibility surfaces. Breaking changes require an ADR or release
note that states the migration path.

## Consequences

- CI and `L99_signoff` must be release gates, not advisory checks.
- Release artifacts are traceable to a public source commit and annotated tag.
- Direct PRs can be accepted, but only after protected-branch CI/signoff passes.
- The same policy should be used by the planned public `easyeda-monkey`
  package unless an EasyEDA-specific ADR supersedes it.
