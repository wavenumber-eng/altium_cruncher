+++
type = "plan_log"
id = "toon-rendering-defects-issue-67-impact-audit"
plan_id = "toon-rendering-defects-issue-67"
step_id = "test-runtime-impact-audit"
created = "2026-09-20T14:00:00-04:00"
+++

# Toon closeout impact audit

Status: complete; default-worker RSS tradeoff accepted by the owner
Recorded: 2026-09-20

This working report records deterministic-output, cache, runtime, and output-size
evidence before the independent release-candidate audit. It is intentionally
under `docs/plans`; durable behavior belongs in
`docs/design/toon-rendering-algorithm.md`.

## Environment

- repository HEAD before the dirty candidate: `c477f54d5feae6b71ea910f9f707269b8163afe0`;
- `uv.lock` Git object: `5f2ffcba8cf876a348f4e0a416ba5368e70f3279`;
- Python 3.14.1;
- altium-cruncher 2026.9.19 editable checkout;
- altium-monkey 2026.9.19;
- wn-geometer 2026.9.19;
- Windows 11 Pro 10.0.26200;
- AMD Ryzen 9 9950X, 61.6 GiB physical RAM;
- four native workers unless a serial comparison is named.

The tree is intentionally dirty while the Issue 67 candidate is assembled, so
these are development measurements rather than final release attestation.

## Neutral-boundary output check

The single-through-hole top fixture was rendered from the same resolved config
with persistent cache disabled and one versus four workers. Top SVG, bottom SVG,
and the warning report were byte-identical:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| top SVG | 344,102 | `E321D36546ABAB7C81813EFBD5C6D10D4B2A69845E3E20943FA59E602D35E784` |
| bottom SVG | 206,031 | `D9155FC1FC4121E0F9895B48832B9BBB4E8B6F0CEF7A8A5A406A194B03A6BBE4` |
| warning report | 169 | `EFDD73083A1A4E911E4806DC6193962144E76E9FAAC0FD4530C4720605990A15` |

Artifacts are under `temp/toon-rendering-closeout/closeout-audit/serial` and
`parallel`. The active renderer rename and config adapter therefore introduce no
worker-dependent output.

The corresponding previously accepted Gate 1 default SVGs differ by one
metadata line: the current component-instance payload contains `opacity: 1.0`.
That accepted uniform-opacity feature predates the neutral naming refactor. The
rendered geometry and all other lines match. It is not evidence of a refactor
output change.

## Reporter-board cold/warm check

The issue 67 reporter board was rendered top and bottom with a new empty cache,
then rerendered from that cache. The fixed candidate produced byte-identical SVG
and warning-report bytes across cold and warm runs:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| top SVG | 14,550,042 | `BF4AA7DCB81BF1252380E2996C9002530DACE5C9682A003BFFAFC811580920E3` |
| bottom SVG | 24,030,468 | `225DCCFB782733EACEBAE0C615A8C9D1F38F0F3039BDD6A53402E753B877F176` |
| warning report | 1,060,238 | `900F644E69AE0B78B23EC3CFA1DE67481EECE34C2BF0890D3039B2E439B950F7` |

The cold run took 13.939 s and recorded 458 cache misses and 232 writes. The
warm run took 2.489 s, recorded two complete artwork hits, zero misses, and zero
writes: a 5.60x wall-time improvement in this sample. Timings and artifacts are
under `reporter-cold-v2` and `reporter-warm-v2`.

The first cold/warm experiment exposed a defect: warm component-artwork hits
lost the model label attached to cached native diagnostics. SVG bytes matched,
but warning keys/messages and the affected-model group count did not. The
candidate now stores and validates `illustration_label` in
`CachedComponentPlacement`, includes the policy in the artwork cache namespace,
and has a focused regression. The repeated `v2` experiment above proves the
warning report is now byte-identical.

## Final measured matrix

RT Super C1 is the selected dense board. NXP FRDM i.MX93 remains excluded
because its very large SVG adds review and measurement cost without additional
Issue 67 coverage. Bunny Brain was considered, but its resolved Toon set has
only 47 modeled component occurrences versus RT Super's 157, so its unmeasured
warm-up was discarded before the measured dense-board matrix.

Each condition received one unmeasured warm-up followed by five measured runs.
Cold runs used `--no-cache`; warm runs reused a condition-local cache populated
by the unmeasured prime. RSS is aggregate parent/child resident memory sampled
at 250 ms intervals and therefore intentionally includes shared pages.

| Board | Workers | Cache | Wall median (range), s | Peak RSS median (range), MiB | Native illustration requests/run | SVG bytes |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| Reporter | 1 | cold | 43.857 (40.771-45.257) | 379.1 (378.1-380.8) | 226 | 38,580,510 |
| Reporter | 1 | warm | 3.637 (3.588-3.726) | 349.3 (346.5-360.6) | 0 | 38,580,510 |
| Reporter | 4 | cold | 20.991 (16.936-23.745) | 470.1 (456.8-477.3) | 226 | 38,580,510 |
| Reporter | 4 | warm | 3.842 (3.741-4.597) | 347.3 (346.6-349.2) | 0 | 38,580,510 |
| RT Super C1 | 1 | cold | 11.828 (11.580-17.522) | 241.1 (240.2-243.9) | 314 | 12,561,539 |
| RT Super C1 | 1 | warm | 3.322 (2.901-3.677) | 234.1 (233.8-236.6) | 0 | 12,561,539 |
| RT Super C1 | 4 | cold | 8.638 (8.478-9.630) | 308.8 (308.1-309.3) | 314 | 12,561,539 |
| RT Super C1 | 4 | warm | 3.330 (3.281-3.626) | 234.6 (233.4-236.5) | 0 | 12,561,539 |

The one-worker conditions are the correctness-equivalent baseline for the
default four-worker conditions: inputs, configuration, code, dependencies, and
emitted bytes are identical. Four workers reduce cold median wall time by 52.1%
on the reporter and 27.0% on RT Super. Cold peak RSS rises by 91.0 MiB and
67.7 MiB respectively, crossing the 64 MiB investigation threshold. This is an
expected bounded concurrency cost: up to four independent native requests hold
their input and result geometry concurrently. It is not retained after a full
artwork-cache hit; warm four-worker RSS is within 2 MiB of warm serial RSS on
both boards. Worker count is already explicit and bounded, and `--workers 1`
remains the low-memory option. No unbounded growth or repeated warm geometry
work was observed.

The repository owner accepted this bounded tradeoff on 2026-09-20 and retained
four as the default. Worker count remains any positive integer; `--workers 1`
is the documented low-memory/serial choice.

Every measured run emitted byte-identical top/bottom SVGs for its board across
cold/warm and one/four-worker conditions. Each board also had one deterministic
ordered warning signature across all 20 measured runs. Every warm timing report
recorded two full artwork hits, zero misses, and zero writes; profiler hooks
recorded zero native illustration requests. Output size therefore has zero
growth between conditions.

Raw reports are under
`temp/toon-rendering-closeout/closeout-audit/performance`, grouped by board and
worker count. The final exact-candidate tree and dependency identities remain a
release-attestation item after audit remediation; changing them invalidates
these measurements under the plan's candidate-identity rule.
