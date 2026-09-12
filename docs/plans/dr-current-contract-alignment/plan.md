+++
type = "plan"
id = "dr-current-contract-alignment"
status = "active"
created = "2026-09-12"

[[steps]]
id = "identity-joins"
title = "Fix scoped component enrichment and prove ambiguous and multipart cases"
status = "done"

[[steps]]
id = "review-evidence"
title = "Include compiler metadata and align generated review instructions"
status = "done"
depends_on = ["identity-joins"]

[[steps]]
id = "bundle-qualification"
title = "Qualify current-release bundles, schemas, and identity joins"
status = "done"
depends_on = ["review-evidence"]

[[steps]]
id = "design-doc-intent-audit"
title = "Audit design docs, ADRs, and requirements against implementation"
status = "done"
depends_on = ["bundle-qualification"]

[[steps]]
id = "test-runtime-impact-audit"
title = "Audit new test runtime impact"
status = "done"
depends_on = ["bundle-qualification"]

[[steps]]
id = "external-review"
title = "Obtain independent external review"
status = "done"
depends_on = ["bundle-qualification", "design-doc-intent-audit", "test-runtime-impact-audit"]

[[exit_criteria]]
id = "identity-correctness"
title = "No metadata crosses distinct component identities; multipart and repeated-page joins remain correct"
status = "done"

[[exit_criteria]]
id = "review-evidence"
title = "Compiler context and agent guidance describe released semantics without inventing evidence"
status = "done"

[[exit_criteria]]
id = "signoff"
title = "Focused signoff passes"
status = "pending"

[[exit_criteria]]
id = "design-doc-intent-audit"
title = "Design docs, ADRs, and requirements match implementation"
status = "done"

[[exit_criteria]]
id = "test-runtime-impact-audit"
title = "New tests are listed and runtime impact is reviewed"
status = "done"

[[exit_criteria]]
id = "external-review"
title = "Independent external review is complete"
status = "done"
+++

# DR current-release contract alignment

## Objective and boundary

Make `design` / `design-review` / `dr` a trustworthy review input against the
currently pinned Altium Monkey **2026.9.12**. Incorrect component metadata or
misread compiler evidence can produce confident false findings, so identity and
semantic guidance are acceptance requirements, not cosmetic documentation work.

This is a small Cruncher adapter and documentation change. Preserve Design b0,
compiled schematic graph a0, and the current Cruncher bundle/SVG contracts.
Do not implement anticipated b1/c0 fields, bump dependencies, modify Monkey,
export the full beta compiler model, or change rendering/variant policy.
Implementation and local qualification are complete; PR CI signoff remains.

## Confirmed baseline

- The existing DR export already uses `AltiumDesign.to_json()` and graph-scoped
  physical schematic rendering. RT Super C1 generated successfully and its
  Design JSON passed the installed generated Design b0 structural contract.
- `_annotate_compiled_schematic_graph_links()` indexes enriched components by
  designator. A probe with two distinct `R?` occurrences assigned both the
  second component's value. This is a Cruncher enrichment bug.
- `to_json()` defaults `include_compile_metadata=False`; DR currently follows
  that default. Omission is contract-valid, but loses useful review context.
- Focused existing tests: 12 passed, one external-corpus test skipped because
  its fixture was unavailable. This does not qualify the skipped repeated-page
  case; cover it explicitly below.

## Execution

1. **Repair component joins.** Resolve graph component occurrences to enriched
   Design component rows using released source identity and occurrence scope.
   Verify the mapping against installed 2026.9.12 fields before coding it.
   Do not equate raw compiler IDs with graph occurrence IDs, parse opaque IDs,
   or select an arbitrary row by designator. If no unique evidence-based match
   exists, preserve graph identity and supported labels while omitting unproven
   descriptive/variant attributes. Distinguish separate components sharing a
   label from legitimate multipart bodies belonging to one component.

2. **Expose and explain review evidence.** Explicitly request
   `include_compile_metadata=True` in DR's existing Design JSON export.
   Preserve upstream diagnostic payloads. Update the generated bundle README
   and the public `design` command guide to explain:
   - graph occurrences and full scoped drawing selectors identify objects;
     display designators and bare SVG IDs do not;
   - `classification.pin_count` is the combined compiled schematic component
     count: do not multiply by part count, divide to infer each body's count,
     or assume it proves physical package-pad completeness;
   - per-body investigation uses the source SchDoc's selected part/display mode
     and pin visibility; typed future cardinality fields are not available yet;
   - compiler diagnostics and graph resolution diagnostics describe compiler
     evidence/limitations and are not automatically electrical-design defects;
     absence of diagnostics does not certify the design;
   - aliases are non-unique search/provenance information; optional compatibility
     indexes can be absent or ambiguous. Power-tree guidance must follow scoped
     connectivity and retain intervening component evidence.
   Coordinate terminology with the Monkey documentation work rather than
   inventing a parallel diagnostic-code taxonomy or waiting for a new schema.
   A warning or unresolved relationship must not newly fail bundle generation.

3. **Qualify and review.** Add a small set of regression cases that first expose
   the identity bug, then verify duplicate labels, repeated pages, legitimate
   multipart bodies, and missing/ambiguous identity. Assert values and DNP/fitted
   attributes never cross identities. Verify compiler metadata survives export,
   and `--no-indexes` still produces usable graph-based review evidence.
   Exercise the real RT Super C1 project, validate emitted Design/manifest/SVG
   metadata contracts, and check scoped SVG links against graph targets.
   Use a reproducible repeated-page fixture if the external corpus remains
   unavailable; do not count a skipped test as coverage. Check generated README
   guidance and multipart-count examples. Run focused tests and Python hygiene,
   record their runtime, and use normal PR CI before landing the implementation.
   Obtain independent review of the joins, diagnostic guidance, and regressions;
   resolve all material findings before closeout.

## Files and contract ownership

Primary implementation: `src/py/altium_cruncher/altium_cruncher_design_review.py`.
Qualification: `tests/test_notes_and_design_review.py` and existing public-output
contract checks. Durable command guidance: `docs/design/cli/design.html` and the
generated bundle README; record the behavior fix in `CHANGELOG.md`.

Upstream TypeSpec/DTOs remain the structural authority for Design JSON. Enabling
already-optional compile sections does not require inventing a Cruncher schema
revision. If a Cruncher-owned public shape unexpectedly needs to change, revisit
that scope explicitly and update its TypeSpec authority and generated consumers;
never patch generated contracts by hand. Structural validation alone does not
prove identity joins or electrical correctness.

## Coordination and closeout

- [Monkey #57](https://github.com/wavenumber-eng/altium_monkey/issues/57): released
  compiled-component pin counts and per-body inspection guidance.
- [Monkey Dev #71](https://github.com/wavenumber-eng/altium_monkey_dev/issues/71):
  current-contract documentation first, then coordinated future-contract work.
  Keep this private coordination reference in working plans, not generated
  review bundles or public user guidance.

At closeout, audit the command docs against actual behavior and review added
test runtime. Promote useful findings into the command documentation/tests,
record independent signoff, and retire this plan under
[ADR-0004](../../adrs/ADR-0004-documentation-lifecycle-and-release-boundary.md).
This work does not authorize a formal package release.

## Execution evidence

- The released physical IR bridge validates the canonical page reference before
  matching `physical_sheet_id` and `source_unique_id`. Duplicate labels alone
  are permitted; duplicate identity candidates are not resolved arbitrarily.
- Seven focused identity regressions cover duplicate labels, repeated source
  IDs, multipart omission, and missing/ambiguous identity. The original behavior
  failed these cases before the fix. Bridge mismatch, compiler-warning
  preservation, and no-indexes coverage exercise the bundle workflow.
- Focused contract/workflow suite: 36 passed, one corpus test skipped, 11.26s.
  The skipped corpus test was then run explicitly with the correct local corpus
  root: one passed in 35.32s. Added fast cases keep the regular suite small;
  external corpus loading/rendering remains a separate qualification cost.
- RT Super C1 with `--no-indexes` and the five-page node-test-array bundle passed
  Design b0, manifest, and SVG metadata validation. All 4,442 annotated SVG graph
  links matched their scoped graph targets. Enriched values and variant flags
  matched unique identity candidates; unmatched bodies did not inherit them.
- Python hygiene: zero findings. Dev Std checks and documentation/link audit
  passed. Durable behavior is recorded in the command guide, generated README,
  regressions, and changelog; no new ADR or schema revision is needed.
- Independent reviewer `review_dr_identity_mapping` found no material issues.
  Its real repeated-page qualification caveat was satisfied by the corpus run
  and scoped link audit above.
