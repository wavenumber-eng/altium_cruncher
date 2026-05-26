# Contributing

`altium-cruncher` accepts direct public pull requests once CI is enabled.

Before opening a PR:

1. Keep changes focused on one command, contract, or infrastructure slice.
2. Add or update tests for every public command behavior change.
3. Update docs for public interfaces, JSON output, or config formats.
4. Run package tests and signoff locally.

Expected local checks:

```powershell
uv run pytest
uv run python scripts\py_signoff.py --root .
```

Release decisions, compatibility policy, and public contract changes should be
recorded in `docs/adrs/`.
