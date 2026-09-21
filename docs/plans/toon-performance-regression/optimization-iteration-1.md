+++
type = "plan_log"
id = "toon-performance-optimization-iteration-1"
plan_id = "toon-performance-regression"
step_id = "validate-visibility-fast-paths"
created = "2026-09-20T18:00:00-04:00"
+++

# Exact projection reuse and open-space pruning

Status: implementation, five-run RT Super/Loz performance matrix, cache and
determinism validation, gallery requalification, and owner envelope acceptance
complete; independent-audit remediation is being requalified.

## Implemented changes

The command-local renderer now:

1. single-flights native direct-model projections by the exact native source,
   model bytes, view, style and clipping plane rather than by occurrence;
2. retains independent occurrence placement, board-region resolution,
   clipping-plane selection, metadata and SVG masks;
3. deduplicates SVG definitions by exact projection content and paint policy;
4. builds a conservative open-space index from the physical board outline,
   routed cutouts, eligible pad bores and eligible via bores;
5. omits the aperture branch only for a fully hidden body whose conservative
   XY bounds are strictly inside board material and disjoint from every
   eligible opening;
6. when both surface views are configured, prewarms the mounting-side
   projection so its trusted native bounds can suppress a needless hidden-side
   request. The later mounting-side render reuses that exact projection.

Surface-crossing bodies deliberately keep their uncut aperture branch even
when the conservative index finds no opening. An experiment removing that
branch changed a tiny antialiased boundary fragment on RT Super U6; retaining
the conservative branch restored exact pixels.

The implementation remains command-local and changes no public contract. Its
policy inputs are included in the disposable persistent-cache namespace, and
the exact physical board/open-space domain participates in projection and
whole-component artwork keys.

## Native request census

Cache-disabled four-worker call probes measured:

| Board | Corrected model calls | Exact reuse | Final optimized | Final uncut | Final clipped |
| --- | ---: | ---: | ---: | ---: | ---: |
| RT Super C1 | 466 | 78 | 42 | 38 | 4 |
| Loz Old Man | 547 | 226 | 138 | 104 | 34 |

The pre-clipping releases made 36 and 93 model-illustration calls respectively.
The remaining increase is bounded visible clipping/open-space work rather than
one surface-plus-aperture pair for every occurrence.

## Triage wall-time result

These measurements use the same input, generated 2026.9.18 config, four
workers, disabled persistent cache, and one process per run. They are three-run
development evidence, not the required five-run release matrix.

| Board | Pre-clipping median | Corrected median | Optimized runs | Optimized median | Versus pre-clipping |
| --- | ---: | ---: | --- | ---: | ---: |
| RT Super C1 | 3.481 s | 6.167 s | 3.178, 3.366, 3.203 s | 3.203 s | 0.92x |
| Loz Old Man | 8.149 s | 21.204 s | 13.394, 13.247, 13.142 s | 13.247 s | 1.63x |

RT Super is now faster than the last pre-clipping release in this sample. Loz
is 37.5 percent faster than the corrected candidate and is within the
provisional 2.0x mixed-board budget.

## SVG structure and equivalence

| Board | Corrected bytes | Optimized bytes | Pre-clipping bytes |
| --- | ---: | ---: | ---: |
| RT Super C1 | 12,550,726 | 4,077,663 | 3,766,900 |
| Loz Old Man | 50,759,064 | 32,605,317 | 18,354,023 |

RT Super's optimized output is 1.08x the pre-clipping size and meets the 1.25x
ordinary-board target. Loz retains necessary clipping/open-space artwork and
the large board-level model, so its remaining structural delta is carried into
the final audit rather than hidden by lowering detail.

Both boards passed raster comparisons against the corrected qualified output:

- RT Super top and bottom: zero differing pixels at 2000-pixel width;
- Loz top and bottom: zero differing pixels at 1600-pixel width.

Worker scheduling/refactoring outputs are byte-identical to the qualified
optimized files. RT Super also remained byte-identical after the source split
required by the Python signoff size and complexity limits.

One-worker rerenders of both boards are also byte-identical to the qualified
four-worker outputs. RT Super's one-worker command took 4.346 seconds. Loz's
one-worker job timing was 30.487 seconds versus the 13.247-second four-worker
median, demonstrating useful bounded parallelism without changing output.

## Persistent-cache correction

The first empty-cache/finally-warm RT Super probe exposed a scheduling defect:
the warm run loaded all 233 occurrence artworks but still made 36 native direct
model calls. Opposite-side bounds prewarming ran before exact occurrence
artwork hits were materialized.

The prewarm candidate pass now primes an exact cached symbol before scheduling
any prerequisite direct projection. A focused regression test fails if a warm
opposite-side artwork hit starts a worker. A fresh post-fix cache generation
then measured:

| Condition | Native calls | Instrumented wall | Cache result |
| --- | ---: | ---: | --- |
| empty cache | 46 | 5.924 s | 0 hits, 318 writes |
| fully warm | 0 | 2.289 s | 85 hits, 0 misses, 0 writes |

Cold and warm top/bottom files are byte-identical. These are diagnostic runs;
the five-repetition cache matrix remains pending as release evidence.

## Memory probe

The production worker profiler samples aggregate parent/child RSS every 250
ms. Its wrapper was updated for the region/open-space/prewarm arguments before
measurement. RT Super diagnostics report:

| Candidate | Workers | Peak aggregate RSS | Instrumented wall |
| --- | ---: | ---: | ---: |
| 2026.9.18 pre-clipping | 1 | 204,746,752 bytes | 3.142 s |
| optimized | 1 | 215,105,536 bytes | 4.060 s |
| 2026.9.18 pre-clipping | 4 | 269,393,920 bytes | 2.637 s |
| optimized | 4 | 281,919,488 bytes | 3.274 s |

The optimized peak is 5.1 percent higher at one worker and 4.6 percent higher
at four workers, below the existing 10 percent plus 64 MiB investigation
threshold. The one-worker path saves about 66.8 MB versus four workers in the
optimized candidate. RSS sums shared pages and is therefore conservative.

### Loz Old Man scale profile

The mandatory larger-board pass compared the frozen 2026.9.18 worktree with
the optimized candidate using the identical PcbDoc/config and disabled cache.
The profiler adds instrumentation overhead, so these walls are attribution
measurements rather than replacements for the production five-run matrix.

| Candidate | Workers | Wall | Render job | Peak aggregate RSS | SVG bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2026.9.18 | 1 | 15.088 s | 14.300 s | 390.8 MB | 18.35 MB |
| optimized | 1 | 34.164 s | 33.371 s | 461.6 MB | 32.61 MB |
| 2026.9.18 | 4 | 10.122 s | 9.011 s | 452.8 MB | 18.35 MB |
| optimized | 4 | 17.720 s | 16.805 s | 552.7 MB | 32.61 MB |

The threshold-triggered investigation attributes most of the added peak to the
Python process retaining the richer SVG document (about 436 MB versus 347 MB
at four workers); native Geometer peak-sum rises from about 249 MB to 307 MB.
SVG elements increase from 63,518 to 133,989 because the corrected renderer
retains required surface and open-space fragments.

Native tracing records 96 total Geometer calls in 2026.9.18 and 143 in the
optimized candidate. Model illustration accounts for 93 A0 calls before
clipping and 138 B0 calls now: 104 reusable uncut projections plus 34 required
clipped projections. Serial `cProfile` likewise attributes the dominant delta
to native response volume/decoding rather than a new Python hot loop. This is
the expected correctness cost accepted by the owner, not an unbounded
per-occurrence surface/aperture duplication. Raw profiles are under
`C:\eli\wn-hw\altium_cruncher\temp\toon-performance-frozen\loz-detailed`.

## Focused validation

- 96 focused clipping, worker, rotation, model-cache and substrate tests pass;
- all 43 applicable L3 public workflow tests pass, with one unrelated native
  parity test skipped;
- the through-board, Issue 67 reporter, Gate 6 analytic, projection-test,
  USB-edge, single-through-hole and single-SMT workflow tests pass;
- Ruff, Pyright and the Python structural signoff pass after separating direct
  projection memo, prewarm and runtime policy into neutral internal modules.

The optimized warning totals are lower because hidden opposite-side
projections are no longer executed. Warnings from every native operation that
still executes remain grouped and reported; no rendered geometry warning is
filtered after the fact.

## Five-run release matrix

Each condition used one unmeasured warm-up followed by five measured runs.
Empty-cache repetitions used distinct new cache roots; warm repetitions used
a fully populated cache. All output hashes were identical across worker counts,
cache states and repetitions.

| Board / condition | Median | Range |
| --- | ---: | ---: |
| RT Super, no cache, 1 worker | 3.766 s | 3.741-3.858 s |
| RT Super, no cache, 4 workers | 3.143 s | 3.137-3.213 s |
| RT Super, empty cache, 4 workers | 6.416 s | 6.368-6.531 s |
| RT Super, warm cache, 4 workers | 2.804 s | 2.766-2.817 s |
| Loz, no cache, 1 worker | 29.588 s | 29.373-31.226 s |
| Loz, no cache, 4 workers | 12.919 s | 12.873-13.236 s |
| Loz, empty cache, 4 workers | 19.772 s | 19.613-20.021 s |
| Loz, warm cache, 4 workers | 4.224 s | 4.204-4.238 s |

RT Super's four-worker no-cache median is 0.90x the 3.481-second pre-clipping
median. Loz is 1.59x its 8.149-second pre-clipping median, inside the 2.0x
mixed-board budget.

The frozen corrected candidate's five-run warm medians are 2.816 seconds for
RT Super and 4.376 seconds for Loz. The optimized warm results are therefore
1.00x and 0.97x those baselines, within the 1.10x budget. A traced warm RT run
made zero native geometry requests.

## Populated-cache maintenance regression

The split-gallery requalification reproduced the owner's approximately 10x
experience through a separate cache-maintenance path. The default operating-
system cache contained 8,557 owned entries (222,812,539 bytes). A cold RT Super
style key wrote 318 entries, and `PcbSvgModelCache.store()` enumerated, stated,
summed and sorted the complete cache after every write. The render job already
performed the same bounded eviction once from `finish()`, including exception
exits, so the per-entry scan was redundant and made population proportional to
`writes * existing entries`.

The cold gallery run measured 165.645 seconds in the render job, of which
163.052 seconds was attributed to 318 cache writes. After deferring eviction
to the existing command-finalization boundary, a fresh illustration style key
against the same populated default cache measured:

| Condition | Complete wall | Render job | Cache writes | Cache write time |
| --- | ---: | ---: | ---: | ---: |
| per-entry full-cache prune | ~166.7 s | 165.645 s | 318 | 163.052 s |
| command-final full-cache prune | 4.245 s | 3.168 s | 316 | 0.403 s |

The corrected run retained 942 misses, two reusable hits, atomic entry writes,
the 1 GiB final bound and the owned-entry-only eviction policy. A focused test
now asserts that repeated stores perform no full-cache enumeration and one
explicit command prune performs exactly one enumeration. Render-job tests also
cover the single final prune on both successful and exceptional context exits.
The exact post-fix command was:

```text
uv run acr toon tests/assets/projects/rt_super_c1/input/RT_SUPER_C1.PrjPcb --output temp/toon-performance-frozen/populated-cache-prune/after --config temp/toon-performance-frozen/populated-cache-prune/line-width-0026.jsonc --workers 4 --timings temp/toon-performance-frozen/populated-cache-prune/after/timings.json --warnings none
```

Five additional cold illustration-style keys against the populated default
cache confirm that result:

| Metric | Median | Range |
| --- | ---: | ---: |
| complete command wall | 4.199 s | 4.073-4.565 s |
| render job | 3.119 s | 3.024-3.401 s |
| 316 cache writes | 0.431 s | 0.401-0.491 s |

Every repetition recorded two reusable hits, 942 misses, 316 writes and zero
evictions. The median render-job time is 2.6 percent faster than the isolated
empty-cache median and 98.1 percent faster than the reproduced populated-cache
failure. This closes the cold populated-cache performance audit without using
a warm-cache result as a substitute.

## Remaining gates

- owner-authorized commit/push of the frozen candidate;
- package-build and installed-tool qualification in repository CI.

The 60-SVG split gallery was regenerated across Gates 1 through 9. Every
manifest path resolves, and the reusable gallery tests pass. The exact index is
`C:\eli\wn-hw\altium_cruncher\temp\toon-rendering-closeout\review\index.html`.
The optimized algorithm, conservative fallback, definition reuse, cache
lifecycle and deliberate limitations are reconciled in
`docs/design/toon-rendering-algorithm.md` and the public Toon/PCB-SVG command
documentation.

Raw profiles and outputs remain ignored under
`C:\eli\wn-hw\altium_cruncher\temp\toon-performance-frozen`.
