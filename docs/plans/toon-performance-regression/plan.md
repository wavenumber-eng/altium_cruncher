+++
type = "plan"
id = "toon-performance-regression"
status = "pending"
created = "2026-09-20"

[[steps]]
id = "capture-user-reproducer"
title = "Capture the reported slow boards, exact commands, configs, cache state, and machine context"
status = "done"

[[steps]]
id = "freeze-benchmark-environments"
title = "Reproduce each candidate from its committed lock and record executable, dependency, and machine identities"
status = "done"

[[steps]]
id = "establish-controlled-baseline"
title = "Measure pre-clipping, first-clipping, and corrected candidates under controlled cold and warm conditions"
status = "done"
depends_on = ["freeze-benchmark-environments"]

[[steps]]
id = "test-runtime-impact-audit"
title = "Attribute wall time, native requests, data volume, memory, and SVG growth to each rendering branch"
status = "done"
depends_on = ["establish-controlled-baseline"]

[[steps]]
id = "isolate-regression-causes"
title = "Separate Cruncher visibility planning, Geometer operations, dependency versions, and SVG composition costs"
status = "done"
depends_on = ["test-runtime-impact-audit"]

[[steps]]
id = "implement-safe-visibility-fast-paths"
title = "Skip clipping and aperture work when 3D bounds and board topology prove it unnecessary"
status = "done"
depends_on = ["isolate-regression-causes"]

[[steps]]
id = "reduce-native-and-serialization-work"
title = "Reuse or batch required projections and prevent redundant native payload and SVG generation"
status = "done"
depends_on = ["validate-visibility-fast-paths"]

[[steps]]
id = "validate-visibility-fast-paths"
title = "Verify exact request counts, output equivalence, boundary cases, and RT Super/Loz performance after visibility changes"
status = "done"
depends_on = ["implement-safe-visibility-fast-paths"]

[[steps]]
id = "validate-native-and-serialization-work"
title = "Verify exact request counts, output structure, correctness, and RT Super/Loz performance after native or SVG changes"
status = "done"
depends_on = ["reduce-native-and-serialization-work"]

[[steps]]
id = "validate-cache-and-determinism"
title = "Verify cold, warm, worker-count, cache identity, output determinism, and failure behavior"
status = "done"
depends_on = ["validate-native-and-serialization-work"]

[[steps]]
id = "requalify-rendering-correctness"
title = "Rerun every placement, through-board, overhang, cutout, reverse-mount, flex, and designator gate"
status = "done"
depends_on = ["validate-cache-and-determinism"]

[[steps]]
id = "design-doc-intent-audit"
title = "Reconcile the optimized algorithm, public documentation, contracts, and accepted limitations"
status = "done"
depends_on = ["requalify-rendering-correctness"]

[[steps]]
id = "accept-performance-envelope"
title = "Obtain owner acceptance of the measured runtime, memory, and output-size envelope"
status = "done"
depends_on = ["design-doc-intent-audit"]

[[steps]]
id = "external-review"
title = "Independently audit the optimized algorithm, measurements, and correctness evidence"
status = "done"
depends_on = ["accept-performance-envelope", "design-doc-intent-audit", "test-runtime-impact-audit"]

[[steps]]
id = "release-requalification"
title = "Run full source, contract, packaging, installed-tool, and gallery qualification"
status = "pending"
depends_on = ["external-review"]

[[exit_criteria]]
id = "reported-regression-reproduced"
title = "At least one owner-reported approximately 10x case is reproduced or its environmental cause is identified"
status = "met"

[[exit_criteria]]
id = "pre-clipping-baseline"
title = "The last pre-clipping release and current candidate are compared with identical inputs and explicit dependency attribution"
status = "met"

[[exit_criteria]]
id = "bounded-native-work"
title = "Native request count is proportional to physically required surface and open-space projections"
status = "met"

[[exit_criteria]]
id = "test-runtime-impact-audit"
title = "Cold, warm, runtime, memory, and SVG-size budgets pass on synthetic and real-world boards"
status = "met"

[[exit_criteria]]
id = "correctness-preserved"
title = "All Issue 67 rendering gates pass without disabling or approximating required clipping behavior"
status = "met"

[[exit_criteria]]
id = "design-doc-intent-audit"
title = "Public documentation and contracts match the optimized implementation and accepted performance policy"
status = "met"

[[exit_criteria]]
id = "external-review"
title = "Independent review has no unresolved material correctness or performance findings"
status = "met"
+++

# Toon performance regression

## Objective

Restore practical Toon generation performance after the board-thickness,
surface-clipping, and open-space composition work without regressing the
placement and cross-side visibility behavior qualified under Issue 67.

The release remains blocked. Performance is a correctness property for this
workflow: a geometrically accurate renderer that makes ordinary boards
impractical to process is not release-ready. Cache hits may improve repeated
runs, but persistent caching is not an acceptable substitute for bounded cold
work.

## Trigger and first controlled result

The owner reports approximately 10x slower overall execution on existing
boards. RT Super C1 is the primary optimization loop because it contains 157
modeled occurrences, both board sides, through-board geometry, and established
profiling history while completing quickly enough for repeated instrumentation
and fault-injection runs. Loz Old Man is the secondary scale gate: its larger
board-level free STEP model, much larger SVGs, and heavier layer composition can
expose serialization, native-geometry, and document-complexity costs that the
RT Super inner loop may hide.

The initial cross-release comparison is:

- `2026.9.18` / commit `79bb81e`, Monkey 2026.9.18, Geometer 2026.9.13;
- current corrected branch / commit `bb76253`, Monkey 2026.9.19, Geometer
  2026.9.19;
- identical RT Super project, generated 2026.9.18 A0 config, four workers,
  persistent cache disabled, one warm-up, and three measured runs.

The current branch is 1.77x slower by median complete command wall time and
2.60x slower inside the measured render job. Its two SVGs are 3.33x larger.
This proves a material regression across the combined 2026.9.18-to-2026.9.19
release interval, but it neither isolates clipping nor reproduces the reported
10x case. Cruncher, Monkey, Geometer, and their committed dependency locks all
changed across that interval. The detailed evidence is in `baseline.md`.

The same three-run triage on Loz Old Man measures 8.149 seconds before clipping
and 21.204 seconds on the corrected branch: 2.60x slower overall and 3.08x
slower inside the render job. SVG bytes grow from 18.35 MB to 50.76 MB
(2.77x). Loz therefore remains in every milestone measurement, but RT Super is
the default development target until an optimization passes its focused tests.

An initially attempted comparison against 2026.9.19 was invalid as a
pre-clipping baseline because that release already contains the surface/open-
space projection algorithm. It is still useful attribution evidence: 2026.9.19
and the corrected branch are effectively flat on RT Super, showing that the
later Issue 67 correctness fixes did not introduce this particular slowdown.

## Measurement contract

Every reported comparison must record:

- Cruncher commit/version, committed `uv.lock` hash, `uv` version, complete
  environment freeze, and exact Monkey/Geometer versions;
- Python executable hash and Geometer executable/library hashes;
- board bytes or source-manifest hash, config bytes, selected views/variants,
  worker count, cache directory/state, and command line;
- machine, OS, Python, available cores and memory;
- complete process wall time plus Cruncher's internal stage timings;
- aggregate peak RSS and worker/client count;
- native operation name, count, duration, input bytes, result bytes, component,
  side, visibility action, and surface/aperture branch;
- cache hits, misses, writes and bytes;
- SVG count, bytes, definitions, instances, paths/segments and DOM nodes;
- deterministic hashes for equivalent repeated outputs.

The run manifest is durable plan evidence and contains the exact argv, working
directory, input/config hashes, launcher identity, cache identity, machine/OS,
Python, logical-core count, and physical memory. Raw SVGs, traces, and profiles
remain ignored under `temp/`.

Use one unmeasured warm-up followed by at least five measured repetitions for
release evidence. Three repetitions are sufficient only for initial triage.
Report medians and ranges; do not compare a cold run from one revision with a
warm run from another. Measure these conditions separately:

1. cache disabled, one worker;
2. cache disabled, default four workers;
3. empty persistent cache, four workers;
4. fully warm persistent cache, four workers;
5. SVG generation alone versus gallery/browser loading when the complaint
   includes review responsiveness.

## Baseline matrix

Measure three code points from detached worktrees synchronized with their
committed locks by `uv sync --frozen`:

1. 2026.9.18, the last pre-clipping release;
2. 2026.9.19, the first released clipping implementation, even though the
   package was withdrawn for correctness;
3. the current corrected candidate.

Run both each revision's default config and the newest mutually accepted config.
The former captures user experience; the latter isolates implementation cost.
Because the pre-clipping release also pins older Monkey and Geometer versions,
dependency isolation is mandatory before implementation. Replay identical
representative uncut native requests against Geometer 2026.9.13 and 2026.9.19,
then compare uncut and clipped requests on Geometer 2026.9.19. Where the Python
API is compatible, also run the current Cruncher code against frozen alternate
dependency sets. Do not attribute the cross-release delta to clipping or
Cruncher until renderer planning and native-kernel costs are separated.

The fixture set must include:

- RT Super C1 as the primary dense modeled inner loop for profiling and rapid
  optimization iteration;
- Loz Old Man as the secondary large-board/free-model scale and SVG-complexity
  gate;
- the Issue 67 reporter board;
- single-SMT and single-through-hole controls;
- projection-test and USB-edge for actual overhang/open-space work;
- Gate 6 analytic bodies;
- Bluetooth Sentinel or Kame IMU for rigid-flex regional cost;
- at least one owner-reported approximately 10x board, kept private if needed,
  with a scrubbed structural surrogate added when feasible.

## Attribution experiments

Instrumentation must distinguish useful work from conservative fallback work.
For every component, record:

- authored side and requested side;
- model type and mesh/triangle counts;
- resolved region/slab and visibility action;
- whether the model Z interval is fully visible, fully hidden, or crosses the
  requested surface;
- whether its projected conservative footprint can intersect board exterior,
  routed cutouts, or eligible physical bores;
- whether surface and aperture projections were requested, returned empty, or
  contributed visible SVG;
- rotation-resolution alternatives and discarded native results.

Use controlled experiments to price these independently:

- board-region and opening-domain construction;
- STEP tessellation and affine placement;
- unclipped versus clipped HLR;
- unclipped versus clipped shaded illustration;
- the second uncut aperture projection;
- solder-mask/coverlay and silkscreen clipping;
- SVG serialization, deduplication, file writing, and browser parsing.

Development-only experiment flags may bypass one stage for attribution, but
they are not public behavior and their outputs must never be presented as
correctness candidates.

Run the following same-code factorial controls on both RT Super and Loz Old Man:

1. normal corrected behavior;
2. perform all native aperture work but omit aperture SVG definitions and
   instances, isolating serialization/DOM cost;
3. suppress aperture native requests while retaining surface work, producing
   deliberately invalid output only for attribution;
4. replace clipped-plus-uncut work with one uncut projection, again producing
   deliberately invalid output only to price the clipped call;
5. instrumentation enabled with no behavioral bypass, pricing profiler
   overhead.

Attribution-only outputs are never correctness or visual-review candidates.

## Current request graph

Document the direct-STEP and mesh request graphs before optimizing them. The
mesh path already has transformed bounds before projection. The direct-STEP
path currently learns bounds from a full uncut native illustration and only
then applies visibility; therefore a bounds-based direct fast path is useful
only if its trusted bounds come from a reused cross-side result, cached model
bounds, or a measured cheaper native bounds operation. Bounds acquisition must
cost less than the illustration it avoids. Do not restore unconditional STEP
tessellation merely to obtain bounds.

## Optimization model

The existing algorithm remains the conservative fallback. Fast paths are
allowed only when inexpensive bounds and topology tests prove that they are
semantically equivalent.

### 1. Early Z-interval classification

Where trusted transformed bounds exist before an expensive projection, compare
their Z interval with the resolved top or bottom surface:

- wholly on the visible side: render the surface result uncut;
- wholly behind an opaque board-material surface: omit the surface result;
- crossing the surface within tolerance: use Geometer half-space clipping;
- unresolved or incompatible regions: retain the documented conservative
  fallback.

This avoids asking the native kernel to clip ordinary SMT bodies that cannot
cross the board surface. Bounds may prove absence; they must not be used to
invent visible geometry. If bounds are learned only by performing the expensive
uncut illustration, retain the existing path until a cheaper trusted source is
measured.

### 2. Open-space candidate classification

Generate the uncut aperture projection only if the transformed conservative XY
footprint can intersect true open space for that side:

- outside the board outline;
- a routed board cutout;
- an eligible untented, unfilled, uncapped and unplugged through bore.

Precompute a side-aware spatial index of those domains. A safe skip requires
the transformed conservative footprint to be strictly inside board material
eroded by the policy tolerance and disjoint from cutouts and eligible bores
expanded by that tolerance. Touching, invalid, outside-board, incompatible-
region, or otherwise ambiguous cases continue through the current exact masked
composition. Cover edge/cutout/slot epsilon boundaries, rotations, non-uniform
scale, equivalent and incompatible region envelopes, and every via policy.

The optimization must preserve the distinction between graphical drill marks,
film openings and physical open space.

### 3. Reuse and batching

After eliminating unnecessary branches, examine the remaining native work:

- reuse an already correct uncut projection as the surface or aperture result;
- share source preparation and immutable meshes across sides and variants;
- batch top/bottom or clipped/unclipped requests only if Geometer can return
  independent deterministic fragments without changing materials, bounds,
  diagnostics or cache identity;
- avoid repeated rotation-resolution probes once a body/model placement is
  resolved and cached;
- keep worker concurrency bounded and commit results in source order.

For each unique render key, request planning must satisfy this census:

- zero projections when the model is fully hidden and cannot contribute through
  open space;
- one uncut projection when it alone supplies the visible surface or aperture;
- one clipped plus one uncut projection only when the body crosses the surface
  and can also contribute through open space;
- placement-resolution probes accounted separately and reused across repeated
  occurrences whenever their identity permits.

Tests assert planned and actual operation counts and bytes, not only final SVG
appearance.

If the remaining dominant cost requires a Geometer API change, document the
exact convenience/batch request and measured expected benefit before requesting
it. Do not grow a CAD kernel inside Cruncher.

### 4. SVG complexity

Native speed alone is insufficient when output grows several-fold. Preserve
one definition per unique projection and use lightweight instances. Do not emit
an aperture definition or masked branch that cannot contribute pixels. Measure
path/segment and DOM-node growth, not only compressed file bytes. Any change to
IDs, metadata or layer order receives an explicit compatibility disposition.

## Provisional budgets

Final budgets require the owner-reported reproducer. Each optimization is
compared both with 2026.9.18 user experience and with a current-dependency,
feature-disabled control so dependency cost is not mistaken for algorithm cost.
Implementation starts with these release gates:

- boards whose models neither cross a surface nor intersect open space: median
  cold wall time no more than 1.25x the pre-clipping baseline;
- mixed through-hole/overhang boards: no more than 2.0x pre-clipping cold wall
  time unless the owner explicitly accepts a measured, necessary cost;
- warm-cache median no more than 1.10x the corrected candidate's established
  warm baseline, with zero native geometry requests on complete artwork hits;
- boards with no aperture contribution emit zero unused aperture definitions or
  instances; their SVG size target is no more than 1.25x pre-clipping, and every
  larger result must be explained by visible new information;
- no unbounded RSS growth; retain `--workers 1` as the low-memory path and apply
  the existing 10 percent plus 64 MiB investigation threshold;
- byte-identical outputs across repeated runs and worker counts;
- medians must improve by more than the observed run-to-run noise and measured
  ranges must not materially overlap before an optimization is credited;
- the owner-reported reproducer receives an explicit absolute wall-time target
  once captured, and gallery/browser budgets are added if review responsiveness
  is part of that report.

These are budgets, not invitations to disable details, drop warnings, lower
quality, or silently change defaults.

## Correctness and review gates

Every optimization class receives its focused correctness, request-count, RT
Super, and Loz Old Man gate before the next class begins. Every optimization
must be fault-injected or tested so the regression fails if the fast-path
predicate is removed or inverted. At minimum, prove:

- top and bottom SMT bodies skip unnecessary opposite-side native work;
- through-board pins retain both required surface fragments;
- edge and cutout overhang remains visible from the opposite side;
- USB straddle and reverse-mount LED cases retain open-space contribution;
- eligible through bores remain transparent while tented, plugged, filled,
  capped, blind and buried vias remain opaque;
- incompatible rigid/flex envelopes keep their conservative behavior;
- warm caches cannot reuse results across changed visibility policy.

Rerun the split SVG gallery and obtain owner review on every affected gate.
Then perform an independent audit of algorithmic complexity, native request
counts, cache identity, determinism, memory, SVG structure, and the complete
correctness corpus.

## Release policy

Do not publish the prepared 2026.9.20 candidate while this plan is open. A
performance fix that changes code, dependencies, cache identity, output, or the
algorithm document invalidates the prior exact-candidate attestation and
requires a new version decision, independent re-audit, full qualification, and
explicit release authorization.
