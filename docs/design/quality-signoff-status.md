# Quality Signoff Status

Status: initial bootstrap audit
Last updated: 2026-05-25

## Passing Gates

- `ruff check .` passes.
- `scripts/py_signoff.py --root . --baseline scripts/py_signoff_baseline.json`
  passes with zero findings.
- `pytest` passes locally.
- `rack run --all` passes locally.
- build, `twine check`, and built-wheel install smoke pass locally.

## Pyright Backlog

`pyright` is installed in the test extra, but it is not yet a release-blocking
gate for the first bootstrap slice.

The current local run reports 169 errors and 2 warnings. The main categories
are:

- dynamic baseline parsing in `scripts/py_signoff.py`;
- optional `easyeda_monkey` imports before `easyeda-monkey` is public;
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
