+++
type = "build_doc"
id = "altium-cruncher-build"
title = "Altium Cruncher Build And Release"
status = "accepted"
+++

# Altium Cruncher Build And Release

## Tools And Setup

Use `uv` with Python 3.14. The repository's `.python-version` selects this
interpreter, matching the package requirement and CI. The normal setup command is:

```bash
uv sync --extra test
```

The project uses Hatchling through `pyproject.toml`, and `uv.lock` is the
checked-in dependency lock for local and CI runs.

All public JSON contract generation uses Node 24 and the
checked-in npm lockfile:

```powershell
npm ci --ignore-scripts
npm run check:contracts
npm run check:typescript
npm run check:browser
```

After editing any source under `src/tsp/altium_cruncher`,
run `npm run generate:contracts`.
The [SVG config guide](design/pcb-svg-config-authority.md) and
[creation config guide](design/creation-config-authority.md) and
[MCO guide](design/mco-contract-authority.md) document generated
resources and compatibility boundaries. CI and release publishing check
these artifacts before packaging. Installed Python CLI users do not need Node.
The [complete authority inventory](design/public-contract-authority.md) includes
remaining workflow configs, output contracts and explicit upstream boundaries.

## Commands And Invocation

Invoke the package through `uv run` during development:

```bash
uv run altium-cruncher --help
uv run python -m altium_cruncher version
```

Build commands should run from the repository root so package metadata,
contracts, examples, and tests are resolved consistently.

## Outputs And Artifacts

Release builds write Python package artifacts under `dist/`:

```bash
uv run --extra test python -m build
uv run --extra test twine check dist/*
```

The expected distribution outputs are a wheel and source distribution for the
current date-based package version.

## Validation And Signoff

The release signoff path is:

```bash
uv run --extra test rack run --all
uv run --extra test python -m build
uv run --extra test twine check dist/*
uv run --extra test python tests/support_scripts/install_test.py
```

GitHub Actions reruns the same Rack, package build, distribution check, and
installed-console smoke tests before a published release can upload to PyPI.

## Documentation-Only CI

Documentation-only edits bypass test/build CI, including edits to generated
documentation. This applies to the root `README.md`, `CONTRIBUTING.md`,
`CHANGELOG.md`, `AGENTS.md`, and documentation under `docs/`: Markdown, HTML,
reStructuredText, text, CSS, SVG, PNG, JPEG, GIF, WebP, ICO, and PDF files.
There are no dependency installations, documentation checks, contract checks,
tests, or builds on this path.

Machine-readable contracts (including JSON schemas), governance TOML, source,
tests, workflows, and other files still run full CI. Mixed changes also run full
CI. Updating a documentation generator runs full CI; updating only its Markdown
or HTML output does not. The classifier examines the complete Git diff,
including both paths of renames. Missing history, empty diffs, and manual
workflow dispatches use full CI.

GitHub still starts a minimal workflow to detect the changed files and report
the existing required statuses. For documentation-only changes, the matrix
statuses use short Ubuntu jobs, skipping checkout and all validation steps.
Existing PR metadata checks still apply. A failed scope check explicitly fails
the required jobs. The workflow itself is never filtered out, which avoids
leaving required checks pending. Release publishing always runs full validation.
The policy lives in `tests/support_scripts/ci_scope.py` and
`.github/workflows/ci.yml`.
