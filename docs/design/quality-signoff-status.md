# Quality Signoff Status

Status: initial bootstrap audit
Last updated: 2026-05-26

## Passing Gates

- `ruff check .` passes.
- `tests/support_scripts/py_signoff.py --root . --baseline
  tests/support_scripts/py_signoff_baseline.json` passes with zero findings.
- `pytest` passes locally.
- `rack run --all` passes locally.
- build, `twine check`, and built-wheel install tests pass locally.
- Direct `uv tool install` testing is not yet a hard local gate; the venv
  install test verifies equivalent generated console scripts through PATH.
- GitHub CI is blocking on Windows and Ubuntu for the first public release.
  macOS GitHub-hosted CI is deferred because `wn-geometer==2026.5.25` currently
  publishes a `macosx_26_0_arm64` wheel while GitHub `macos-latest` resolves to
  macOS 15 arm64. Manual macOS pip/uv-tool testing is still required until that
  wheel tag or runner mismatch is resolved.

## Active Design-Doc Gate

`L99_signoff` now includes hard checks for command design docs, config contract
links, config schema validation, generated-template conformance, and public
dataclass / major-interface design ownership.

Current known gaps:

- keep command design docs, config contracts, and public API/interface sections
  synchronized as commands move into the release boundary.

## Pyright Backlog

`pyright` is installed in the test extra, but it is not yet a release-blocking
gate for the first bootstrap slice.

The current local run reports 169 errors and 2 warnings. The main categories
are:

- dynamic baseline parsing in `tests/support_scripts/py_signoff.py`;
- optional `easyeda_monkey` imports behind the `altium-cruncher[easyeda]`
  extra;
- broad `object`/union typing in `altium_cruncher_cmd_megamaid.py`;
- broad renderer option unions in PCB assembly/SVG helpers;
- a small set of optional-value narrowing issues in EasyEDA and PCB geometry
  helpers.

Before making pyright a CI hard gate, decide whether to:

- add a pyright baseline/waiver file and ratchet it down;
- move optional EasyEDA implementation behind a public optional dependency;
- narrow PCB/megamaid config and manifest dataclasses;
- exclude migration scripts from strict package typing and keep them covered by
  `py_signoff`.
