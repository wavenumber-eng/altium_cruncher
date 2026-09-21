+++
type = "plan_log"
id = "toon-rendering-defects-issue-67-independent-audit"
plan_id = "toon-rendering-defects-issue-67"
step_id = "external-review"
created = "2026-09-20T15:00:00-04:00"
+++

# Independent Toon candidate audit

Status: follow-up audit complete; no unresolved technical findings
Initial review: 2026-09-20
Reviewer: independent `plan_review` agent; no candidate files modified

## Initial result

The independent review found the overall placement, clipping, aperture,
designator, paint-order, diagnostics, and A1 contract approach coherent, but
blocked release on the following material findings:

1. IPC-4761 plugged vias were still treated as physical open space.
2. Equal normalized board slabs could become ambiguous solely because their
   source stacks used different Z-zero conventions.
3. Mesh normals used the position matrix instead of inverse-transpose affine
   transformation under nonuniform STEP root scale.
4. Reporter, analytic-body, and fully-open/incompatible-envelope cases lacked
   the fixture-specific structural regressions required by the plan.
5. Four excluded fixture artifacts remained and the projection project
   manifest described an older file revision.
6. Region-query tolerance, clip tolerance, and cap policy were incomplete in
   illustration cache identity.
7. The four-worker cold RSS increase crossed the plan's explicit owner-review
   threshold, although the reviewer found the bounded concurrency tradeoff
   technically sound.

The reviewer also noted that the initial audit was not an exact-candidate
attestation because the implementation, generated contracts, fixtures, and
documentation were still assembled in a large dirty working tree.

## Remediation

- Cruncher now separates drill illustration policy from mechanical openness
  and excludes every IPC-4761 plugging, filling, and capping type from both
  substrate and opposite-side component apertures.
- Region equivalence now compares normalized physical slabs; source Z metadata
  no longer changes the clipping result.
- Mesh normals use the inverse transpose of the complete combined linear
  transform and are normalized. A non-axis-aligned normal under nonuniform
  root scale freezes the behavior.
- Cache identity now includes region-query tolerance and the explicit clip
  tolerance/cap policy.
- The real reporter fixture renders IC1, IC2, and IC3 through Geometer and
  checks their pad-row registration, IC3 pin-1 direction, and every P1 pin-body
  center against its footprint pad center.
- Gate 6 reparses against its committed semantic inventory, proves two
  generator runs are semantically identical, and renders through-board
  extrusion, cylinder, and sphere cases on both sides.
- Synthetic tests prove that uncut aperture geometry survives for bodies wholly
  inside a cutout, wholly outside the outline, and across incompatible slabs
  plus outside-board open space.
- The excluded reporter HTML, USB PcbLib, projection structure sidecar, and Loz
  HTML report were removed. The projection project manifest now matches the
  retained project bytes.
- Gates 4 through 6 were regenerated without persistent cache. Gate 4 default
  top and bottom SVGs are byte-identical to the owner-signed artifacts and the
  recorded performance candidate.

Focused remediation verification was 130 passing tests plus Ruff.

## Follow-up audit

The independent reviewer rechecked every original finding and the ten audit
areas required by the plan. The first follow-up pass found that the early
whole-component artwork cache included the region partition but not clipping
tolerance or cap policy, allowing a warm bundle to bypass the corrected
per-render key. The final remediation:

- gives render-level and whole-component cache keys one shared clipping-policy
  identity;
- includes the clipping-policy module in the persistent cache namespace; and
- proves with a warm-bundle regression that changing either tolerance or cap
  policy recollects every body instead of accepting stale artwork.

After that change, the reviewer reported no unresolved correctness,
maintainability, or technical performance finding. The known four-worker RSS
tradeoff remains an explicit owner-disposition gate rather than a technical
defect.

## Exact local candidate identity

The post-remediation local candidate is version 2026.9.20 and uses
`altium-monkey==2026.9.19` plus `wn-geometer==2026.9.19`.

- base Git commit: `c477f54d5feae6b71ea910f9f707269b8163afe0`;
- release-relevant changed-file manifest: 99 entries, excluding `docs/plans`
  because working plans are not packaged;
- manifest SHA-256: `757DC8FCB5B27AD2C7EBEBE190C8C43228BA245B8C59A75549150EFA942C73CE`;
- tracked binary-diff Git blob: `01b121dbeb1a2044cd3fe35ce658ed613ee87297`;
- `uv.lock` SHA-256:
  `67FDC55827F32584C7F736D0C34A2521B8EC5254921EF2657594BC7FC8471D01`;
- algorithm document SHA-256:
  `1F70343B84BE7338CF745FADF7BF5FF4618A4C340AA7815C400FFADC02314EDA`;
- wheel SHA-256:
  `8DBDF88EB3526BB5D7285069C48295CB8DDCEE062689003FE528FEDA5C77437D`;
- sdist SHA-256:
  `07B8DB7B14DB8FD6A810315B579AB7B643B334DC6CD5A4CF0BE232B3A54F4E14`.

The manifest digest is computed from sorted records containing disposition
(`F` or `D`), repository-relative path, and SHA-256 for every content-different
tracked or untracked release-relevant file. A reproducible commit/tree remains
preferable before publication; any release-relevant change after this identity
requires rebuilding and repeating affected qualification.
