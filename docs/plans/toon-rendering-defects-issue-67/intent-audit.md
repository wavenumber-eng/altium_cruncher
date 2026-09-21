+++
type = "plan_log"
id = "toon-rendering-defects-issue-67-intent-audit"
plan_id = "toon-rendering-defects-issue-67"
step_id = "design-doc-intent-audit"
created = "2026-09-20T14:00:00-04:00"
+++

# Toon contract and documentation intent audit

Status: complete; refreshed after independent-audit remediation
Recorded: 2026-09-20

This internal audit compares the current Issue 67 candidate's public TypeSpec
contract, generated consumers, CLI documentation, durable algorithm document,
runtime adapter, renderer, and focused tests. It precedes and does not replace
the plan-required independent review.

## Result

No unresolved contract or documentation mismatch was found.

- `pcb.svg.config.a1` contains only additive optional fields and tokens; A0
  remains accepted through the versioned decoder/adapter boundary and unknown
  schema families are rejected.
- Active workflow and compositor code consume neutral `PcbSvgConfig` runtime
  objects. The A0-named renderer module is a compatibility import shim, while
  the implementation is `PcbSvgCompositeRenderer` in the neutral module.
- TypeSpec remains the authority for regional substrate/film fallbacks, bend
  lines, silkscreen clipping, physical-opening presentation, component
  opacity, and assembly-designator policy.
- The Toon and PCB SVG command documents agree with the implementation on
  supported STEP/extrusion/cylinder/sphere bodies, missing-model omission,
  placement-side projected labels, flat rigid-flex handling, region-envelope
  fallback, world-space clipping, mechanical open space, physical openings,
  film/silk composition, bounded workers, queued warnings, and cache behavior.
- The algorithm document records the actual transform convention, clipping
  planes, two-branch surface/open-space union, opacity approximation, analytic
  body limitations, and config-version policy rather than claiming CAD-kernel
  behavior.
- Emitted public schema IDs remain versioned where required. Compatibility
  aliases preserve existing Python imports without leaking the stale suffix
  into active implementation names.

## Verification

- `npm run check:contracts`: 465 generated artifacts for 46 contracts current.
- `npm run check:typescript`: passed.
- `npm run check:browser`: 126 shared vectors passed; no external imports.
- Focused config/cache/job/view/CLI/gallery/public-workflow suite: 213 passed.
- Search of active runtime/workflow modules found no A0/A1 dispatch below the
  config decoder/adapter boundary.

The independent audit subsequently found implementation and test gaps rather
than a conflicting public-contract shape. Its remediations are recorded in
`independent-audit.md`; the durable algorithm document now explicitly states
inverse-transpose normal handling, normalized slab equivalence, and the full
clipping-policy cache identity.

The tree is intentionally dirty while the release candidate is assembled.
Therefore exact tree, lock, generated-contract, and design-document identities
must be captured again for the independent re-audit and publication
attestation. Any later semantic change invalidates this audit under the plan's
candidate-identity rule.
