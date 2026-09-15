# CI and release gates

Cruncher separates source correctness from installed-artifact portability. The
full Rack suite and generated Python consumer checks run once on Linux. That
job builds one wheel and one source distribution, validates their contents,
rebuilds a wheel from the sdist, records SHA-256 identities, and tests the
installed console commands. Windows and macOS download those exact identified
artifacts and run only the platform-specific installed-console checks; Windows
also parses the PowerShell installer.

The `Change scope` job may select the documentation-only path only when every
changed path is in the reviewed documentation allowlist. For executable
changes, it separately selects generated-contract validation when TypeSpec,
TypeScript, generated Python contracts, contract tests, public examples, locks,
build metadata, or workflows change. The contract generator and check harness
sources themselves (`.tsp`, `.ts`, `.mts`, and `.mjs` files anywhere) also
select that gate. Unknown paths select that gate. Empty diffs, unknown events,
missing history, classifier failures, executable documentation assets, renames,
deletions, and fork pull requests fail closed to full validation. The
`CI policy` job always reports one stable result, rejects a missing or
malformed contract-scope output, and rejects every failed, cancelled,
unexpectedly skipped, or missing gate that the selected scope requires.

The historical operating-system check names remain present while branch
protection migrates to `CI policy`. Main-push validation remains enabled until
the stable policy is observed on the protected branch and branch protection is
updated. Documentation-only compatibility jobs use inexpensive Linux runners
and perform no build or installation.

Release publishing is a separate trusted boundary. The release workflow
requires the tag commit to equal current protected `main`, rechecks generated
contracts and version/release-note identity, runs release signoff plus the
generated Python consumer and CI/artifact policy tests, and rebuilds the
publish artifacts. It validates and installation-tests those exact files
before PyPI OIDC becomes useful, then removes the digest manifest so only the
tested wheel and sdist are handed to the publishing action. Pull-request
artifacts are not promoted into the trusted release workflow.

## Source-distribution policy

The sdist contains runtime Python, authored TypeSpec and TypeScript contract
sources, public documentation, public examples, installer scripts, and package
metadata. Tests and their large proprietary/project fixtures are CI inputs, not
published source-distribution content. The artifact policy enforces one wheel,
one sdist, an exact digest manifest, an allowlisted top-level shape, and these
budgets:

- wheel: at most 5 MiB;
- compressed sdist: at most 25 MiB; and
- unpacked sdist: at most 40 MiB.

The sdist must build a wheel in isolation from the repository. Its rebuilt
wheel must match the direct wheel's package name, version, and dependency
metadata. Changing the allowlist or budgets requires a reviewed packaging
decision rather than silently admitting new trees.
