+++
type = "plan_log"
id = "toon-performance-independent-audit"
plan_id = "toon-performance-regression"
step_id = "external-review"
created = "2026-09-20T23:30:00-04:00"
+++

# Independent implementation audit

Status: follow-up review complete; no unresolved material findings

The independent read-only audit found no request-count duplication in the
optimized projection planner, but it did identify two high, two medium, and
one low correctness risks around the optimization boundary.

## Findings and remediation

1. **Physical-open-space cache identity (high).** Projection and complete
   component-artwork keys did not identify the board-material/opening domain.
   They now include the exact opening bounds, conservative clearance, material
   topology digest, and topology-trust state. Tests change the domain in both
   cache layers and verify stable keys only for identical domains.
2. **Speculative prewarm failure boundary (high).** A recoverable model or
   Geometer operation error during opposite-side bounds prewarm could escape
   before the normal component failure path. Serial and parallel prewarm now
   absorb only those recoverable model-operation failures. The ordinary render
   retries and owns the deterministic diagnostic; service, protocol, timeout,
   and other fatal failures still propagate. Focused tests cover one and two
   workers with a failing and a healthy component.
3. **Invalid board topology (medium).** The open-space optimizer previously
   repaired an invalid polygon with `buffer(0)` and could then treat that
   invented topology as authoritative. Invalid, empty, incomplete, or
   boundary-touching topology is now explicitly untrusted and always returns
   `may intersect`, retaining exact rendering. A valid material polygon is
   eroded once when the immutable query index is built rather than once per
   occurrence.
4. **Persistent namespace coverage (medium).** The native cache namespace now
   hashes every Cruncher module that owns artwork placement, clipping,
   projection reuse/prewarm, region/open-space policy, rotation, and complete
   component-artwork caching. A test owns the explicit policy-module set and
   verifies every source exists.
5. **Aperture definition renumbering (low).** Population pruning now remaps
   both `symbol_id` and `aperture_symbol_id` metadata when definitions are
   compacted. A focused regression covers distinct surface/aperture IDs.

The audit also noted the linear scan over opening bounds. The valid-material
erosion was the avoidable repeated geometry operation and is now precomputed.
The remaining bound checks are cheap, conservative rectangle comparisons; the
Loz profile does not identify them as a material bottleneck. A spatial index
is therefore deferred until evidence shows a board with enough physical
openings for that scan to matter.

The independent follow-up re-read every remediation and ran 124 focused tests.
It found no unresolved material correctness or performance finding. The Loz
profiles continue to attribute the remaining accepted delta to required native
response volume/decoding rather than an open-space Python hot loop.

The exact release candidate still needs a frozen source identity and the
remaining release-process checks. No release is authorized by this plan log.
