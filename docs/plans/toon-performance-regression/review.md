+++
type = "plan_log"
id = "toon-performance-regression-review"
plan_id = "toon-performance-regression"
step_id = "isolate-regression-causes"
created = "2026-09-20T21:30:00-04:00"
+++

# Independent plan review

Status: reviewed; findings incorporated before behavioral implementation

The independent review agreed with the RT Super/Loz Old Man fixture hierarchy
but found that the first draft over-attributed the cross-release delta to the
clipping algorithm. The 2026.9.18 and 2026.9.19 candidates change Cruncher,
Monkey, Geometer, and their dependency locks. Frozen worktrees, executable and
environment identities, native request replay, and a same-code factorial are
now mandatory before implementation.

The review also found that the mesh path already has trusted transformed bounds,
while direct STEP bounds are currently learned only after an expensive uncut
illustration. The plan therefore defines a trusted-bounds requirement rather
than assuming that a new Z test is free.

Additional incorporated gates define:

- exact native request-count expectations per unique render key;
- tolerance-aware open-space rejection, including edge and cutout boundaries;
- attribution-only controls that cannot be accepted as correct output;
- focused correctness and performance checks after each optimization class;
- stricter no-aperture SVG structure and dependency-aware performance budgets.

The safest first implementation sequence is measurement-only: freeze both
environments, census current SVG structure, instrument native requests, run the
factorial controls and native replay, and operate the open-space predicate in
dry-run mode. A production fast path is permitted only after that evidence
proves which work is redundant.
