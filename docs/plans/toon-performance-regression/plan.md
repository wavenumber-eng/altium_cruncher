+++
type = "plan"
id = "toon-performance-regression"
status = "pending"
created = "2026-09-20"

[[steps]]
id = "capture-user-reproducer"
title = "Capture the reported slow boards, exact commands, configs, cache state, and machine context"
status = "pending"

[[steps]]
id = "establish-controlled-baseline"
title = "Measure pre-clipping, first-clipping, and corrected candidates under controlled cold and warm conditions"
status = "pending"

[[steps]]
id = "test-runtime-impact-audit"
title = "Attribute wall time, native requests, data volume, memory, and SVG growth to each rendering branch"
status = "pending"
depends_on = ["establish-controlled-baseline"]

[[steps]]
id = "isolate-regression-causes"
title = "Separate Cruncher visibility planning, Geometer operations, dependency versions, and SVG composition costs"
status = "pending"
depends_on = ["test-runtime-impact-audit"]

[[steps]]
id = "implement-safe-visibility-fast-paths"
title = "Skip clipping and aperture work when 3D bounds and board topology prove it unnecessary"
status = "pending"
depends_on = ["isolate-regression-causes"]

[[steps]]
id = "reduce-native-and-serialization-work"
title = "Reuse or batch required projections and prevent redundant native payload and SVG generation"
status = "pending"
depends_on = ["implement-safe-visibility-fast-paths"]

[[steps]]
id = "validate-cache-and-determinism"
title = "Verify cold, warm, worker-count, cache identity, output determinism, and failure behavior"
status = "pending"
depends_on = ["reduce-native-and-serialization-work"]

[[steps]]
id = "requalify-rendering-correctness"
title = "Rerun every placement, through-board, overhang, cutout, reverse-mount, flex, and designator gate"
status = "pending"
depends_on = ["validate-cache-and-determinism"]

[[steps]]
id = "design-doc-intent-audit"
title = "Reconcile the optimized algorithm, public documentation, contracts, and accepted limitations"
status = "pending"
depends_on = ["requalify-rendering-correctness"]

[[steps]]
id = "accept-performance-envelope"
title = "Obtain owner acceptance of the measured runtime, memory, and output-size envelope"
status = "pending"
depends_on = ["design-doc-intent-audit"]

[[steps]]
id = "external-review"
title = "Independently audit the optimized algorithm, measurements, and correctness evidence"
status = "pending"
depends_on = ["accept-performance-envelope", "design-doc-intent-audit", "test-runtime-impact-audit"]

[[steps]]
id = "release-requalification"
title = "Run full source, contract, packaging, installed-tool, and gallery qualification"
status = "pending"
depends_on = ["external-review"]

[[exit_criteria]]
id = "reported-regression-reproduced"
title = "At least one owner-reported approximately 10x case is reproduced or its environmental cause is identified"
status = "pending"

[[exit_criteria]]
id = "pre-clipping-baseline"
title = "The last pre-clipping release and current candidate are compared with identical inputs and explicit dependency attribution"
status = "pending"

[[exit_criteria]]
id = "bounded-native-work"
title = "Native request count is proportional to physically required surface and open-space projections"
status = "pending"

[[exit_criteria]]
id = "test-runtime-impact-audit"
title = "Cold, warm, runtime, memory, and SVG-size budgets pass on synthetic and real-world boards"
status = "pending"

[[exit_criteria]]
id = "correctness-preserved"
title = "All Issue 67 rendering gates pass without disabling or approximating required clipping behavior"
status = "pending"

[[exit_criteria]]
id = "design-doc-intent-audit"
title = "Public documentation and contracts match the optimized implementation and accepted performance policy"
status = "pending"

[[exit_criteria]]
id = "external-review"
title = "Independent review has no unresolved material correctness or performance findings"
status = "pending"
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
boards. The first controlled A/B uses RT Super C1 because it contains 157
modeled occurrences, both board sides, through-board geometry, and established
profiling history without the excessive review cost of the i.MX93 fixture.

The corrected pre-clipping comparison is:

- `2026.9.18` / commit `79bb81e`, Monkey 2026.9.18, Geometer 2026.9.13;
- current corrected branch / commit `bb76253`, Monkey 2026.9.19, Geometer
  2026.9.19;
- identical RT Super project, generated 2026.9.18 A0 config, four workers,
  persistent cache disabled, one warm-up, and three measured runs.

The current branch is 1.77x slower by median complete command wall time and
2.60x slower inside the measured render job. Its two SVGs are 3.33x larger.
This proves a material regression but does not reproduce the reported 10x case.
The detailed evidence is in `baseline.md`.

An initially attempted comparison against 2026.9.19 was invalid as a
pre-clipping baseline because that release already contains the surface/open-
space projection algorithm. It is still useful attribution evidence: 2026.9.19
and the corrected branch are effectively flat on RT Super, showing that the
later Issue 67 correctness fixes did not introduce this particular slowdown.

## Measurement contract

Every reported comparison must record:

- Cruncher commit/version and exact Monkey/Geometer versions;
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

Measure three code points:

1. 2026.9.18, the last pre-clipping release;
2. 2026.9.19, the first released clipping implementation, even though the
   package was withdrawn for correctness;
3. the current corrected candidate.

Run both each revision's default config and the newest mutually accepted config.
The former captures user experience; the latter isolates implementation cost.
Because the pre-clipping release also pins older Monkey and Geometer versions,
add a dependency cross-matrix or targeted native microbenchmarks where API
compatibility permits. Do not attribute all delta to Cruncher until renderer
planning and native-kernel costs are separated.

The fixture set must include:

- RT Super C1 as the dense modeled baseline;
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

## Optimization model

The existing algorithm remains the conservative fallback. Fast paths are
allowed only when inexpensive bounds and topology tests prove that they are
semantically equivalent.

### 1. Z-interval classification

Before invoking Geometer clipping, compare transformed 3D bounds with the
resolved top or bottom surface:

- wholly on the visible side: render the surface result uncut;
- wholly behind an opaque board-material surface: omit the surface result;
- crossing the surface within tolerance: use Geometer half-space clipping;
- unresolved or incompatible regions: retain the documented conservative
  fallback.

This avoids asking the native kernel to clip ordinary SMT bodies that cannot
cross the board surface. Bounds may prove absence; they must not be used to
invent visible geometry.

### 2. Open-space candidate classification

Generate the uncut aperture projection only if the transformed conservative XY
footprint can intersect true open space for that side:

- outside the board outline;
- a routed board cutout;
- an eligible untented, unfilled, uncapped and unplugged through bore.

Precompute a side-aware spatial index of those domains. A footprint completely
inside board material and disjoint from indexed openings cannot contribute to
the aperture branch and must not receive an uncut native projection. Ambiguous
cases continue through the current exact masked composition.

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

Final budgets require the owner-reported reproducer, but implementation should
start with these release gates:

- boards whose models neither cross a surface nor intersect open space: median
  cold wall time no more than 1.25x the pre-clipping baseline;
- mixed through-hole/overhang boards: no more than 2.0x pre-clipping cold wall
  time unless the owner explicitly accepts a measured, necessary cost;
- warm-cache median no more than 1.10x the corrected candidate's established
  warm baseline, with zero native geometry requests on complete artwork hits;
- SVG size no more than 1.5x pre-clipping for boards with no visible aperture
  contribution, and every larger result explained by visible new information;
- no unbounded RSS growth; retain `--workers 1` as the low-memory path and apply
  the existing 10 percent plus 64 MiB investigation threshold;
- byte-identical outputs across repeated runs and worker counts.

These are budgets, not invitations to disable details, drop warnings, lower
quality, or silently change defaults.

## Correctness and review gates

Every optimization must be fault-injected or tested so the regression fails if
the fast-path predicate is removed or inverted. At minimum, prove:

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
