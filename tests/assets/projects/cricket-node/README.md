# cricket-node fixture

This fixture is a minimized copy of the `cricket-node` corpus project used for
`pcb-layer-step` command coverage.

Only the PcbDoc required for bottom-layer STEP generation is checked in here.
Generated STEP files are intentionally not checked in because they are large and
are covered by non-empty artifact plus manifest checks.

Fixture layout:

- `input/`: source Altium design files used by tests.
- `reference_output/`: checked-in golden outputs when a stable output contract
  exists.
- `output/`: transient local output only; ignored by Git.
