+++
type = "plan"
id = "library-authoring-mco"
status = "blocked"
created = "2026-09-26"

[[steps]]
id = "capture-analysis"
title = "Record the MCO, TypeSpec, altium-monkey and corpus analysis that motivates this plan"
status = "done"

[[steps]]
id = "plan-review"
title = "Independently review this plan and fold material findings into it"
status = "done"
depends_on = ["capture-analysis"]

[[steps]]
id = "confirm-decisions"
title = "Confirm strictness, versioning, granularity, mutation, ownership and upstream-issue decisions"
status = "pending"
depends_on = ["plan-review"]

[[steps]]
id = "contract-freshness-crlf"
title = "Make generated-contract freshness checking tolerant of Windows line endings"
status = "pending"

[[steps]]
id = "file-monkey-issues"
title = "File each reviewed altium-monkey defect or missing API on altium_monkey_dev without fixing it"
status = "done"
depends_on = ["plan-review"]

[[steps]]
id = "promote-reference-fixtures"
title = "Promote the GUI-authored pin-parameter and footprint-parameter files into governed test assets"
status = "pending"
depends_on = ["confirm-decisions"]

[[steps]]
id = "survey-easyeda-footprint"
title = "Inventory the EasyEDA footprint builder's monkey calls, including private-internal use"
status = "pending"

[[steps]]
id = "easyeda-baseline"
title = "Snapshot current EasyEDA symbol and footprint output structurally through altium-monkey"
status = "pending"

[[steps]]
id = "mco-validation-coverage"
title = "Validate built-in args on dry runs and for aliased built-in handlers before removing hand checks"
status = "pending"
depends_on = ["confirm-decisions"]

[[steps]]
id = "mco-strict-models"
title = "Close built-in operation and argument models, type delegated STEP fields and version the wire tag"
status = "pending"
depends_on = ["confirm-decisions", "mco-validation-coverage", "contract-freshness-crlf"]

[[steps]]
id = "mco-field-docs"
title = "Document every field of every built-in operation and shared model with purpose, units and allowed values"
status = "pending"
depends_on = ["confirm-decisions"]

[[steps]]
id = "mco-check-command"
title = "Add an mco check command for full structural preflight with design doc and manifest updates"
status = "pending"
depends_on = ["mco-strict-models"]

[[steps]]
id = "mco-runtime-fixes"
title = "Align library create semantics, flush libraries before cross-document reads and sync SchLib pin text"
status = "pending"
depends_on = ["confirm-decisions"]

[[steps]]
id = "schlib-operations"
title = "Add symbol metadata, pin, body-graphic, parameter and footprint-link SchLib operations with multi-part support"
status = "pending"
depends_on = ["mco-strict-models", "mco-runtime-fixes", "promote-reference-fixtures"]

[[steps]]
id = "pcblib-operations"
title = "Add the common PcbLib footprint primitive operations and footprint-parameter editing"
status = "pending"
depends_on = ["mco-strict-models", "mco-runtime-fixes", "survey-easyeda-footprint"]

[[steps]]
id = "easyeda-on-mco"
title = "Reimplement EasyEDA symbol and footprint generation as an MCO producer meeting the equivalence criteria"
status = "pending"
depends_on = ["schlib-operations", "pcblib-operations", "easyeda-baseline", "file-monkey-issues"]

[[steps]]
id = "llm-authoring-guide"
title = "Publish a symbol and footprint library authoring guide with CI-executed worked examples"
status = "pending"
depends_on = ["schlib-operations", "pcblib-operations", "mco-check-command", "mco-field-docs"]

[[steps]]
id = "promote-durable-docs"
title = "Promote accepted decisions into ADRs, design docs, command docs, contracts and the changelog"
status = "pending"
depends_on = ["easyeda-on-mco", "llm-authoring-guide"]

[[steps]]
id = "design-doc-intent-audit"
title = "Audit design docs, ADRs and generated contracts against the implemented operations"
status = "pending"
depends_on = ["promote-durable-docs"]

[[steps]]
id = "test-runtime-impact-audit"
title = "Review conformance, execution, Mate regression and EasyEDA equivalence coverage and its runtime cost"
status = "pending"
depends_on = ["easyeda-on-mco"]

[[steps]]
id = "external-review"
title = "Obtain independent review of contracts, handlers, guide and filed upstream issues"
status = "pending"
depends_on = ["design-doc-intent-audit", "test-runtime-impact-audit"]

[[exit_criteria]]
id = "contracts-strict-and-complete"
title = "Every built-in MCO operation and argument is TypeSpec-typed, documented and rejects unknown keys under the new wire version"
status = "pending"

[[exit_criteria]]
id = "mate-compatible"
title = "Every Mate-generated MCO payload passes strict decoding and Mate workflows still pass"
status = "pending"

[[exit_criteria]]
id = "mco-check-preflight"
title = "mco check rejects unknown keys, bad enum names and malformed args from the CLI"
status = "pending"

[[exit_criteria]]
id = "build-and-place-one-run"
title = "A SchLib and a PcbLib can be created, populated and placed from within one MCO run"
status = "pending"

[[exit_criteria]]
id = "schlib-authoring-surface"
title = "A multi-part symbol with pins, shared objects, body graphics, parameters and a footprint link can be authored and placed per part"
status = "pending"

[[exit_criteria]]
id = "pin-parameters"
title = "Pin parameters can be authored through MCO on the pinned altium-monkey release named in the log"
status = "pending"

[[exit_criteria]]
id = "pcblib-authoring-surface"
title = "A footprint with the common primitives and footprint parameters can be authored and placed through MCO"
status = "pending"

[[exit_criteria]]
id = "easyeda-equivalence"
title = "EasyEDA import produces its libraries through MCO and matches the recorded baseline except listed accepted differences"
status = "pending"

[[exit_criteria]]
id = "monkey-issues-filed"
title = "Every altium-monkey defect found is filed upstream and no Cruncher code relies on private monkey internals"
status = "pending"

[[exit_criteria]]
id = "llm-guide-published"
title = "The library authoring guide is published and its worked examples run as a named Rack task"
status = "pending"

[[exit_criteria]]
id = "release-signoff"
title = "The AGENTS.md release signoff commands and contract generation checks pass"
status = "pending"

[[exit_criteria]]
id = "design-doc-intent-audit"
title = "Public documentation matches accepted and implemented behavior"
status = "pending"

[[exit_criteria]]
id = "test-runtime-impact-audit"
title = "Test coverage and runtime impact have been reviewed"
status = "pending"

[[exit_criteria]]
id = "external-review"
title = "Independent review has no unresolved material findings"
status = "pending"
+++

# Symbol and footprint library authoring through MCO

Created 2026-09-26; revised the same day after an independent plan review (see
"Plan review disposition"). Status **blocked**, 2026-09-26: work is parked until
`wavenumber-eng/altium_monkey_dev` #115–#119 are resolved in a pinned
altium-monkey release. When the work resumes, confirm the decisions below
(including the versioning model in decision 2) before implementation.

## Objective

Make MCO a complete, strictly typed surface for authoring Altium schematic
symbol libraries (SchLib) and the common subset of PCB footprint libraries
(PcbLib), so people, scripts and LLMs can generate libraries reliably. EasyEDA
import is the acceptance case: once its symbol and footprint generation runs
through MCO and matches its recorded baseline, the surface is sufficient.

Tighten every existing MCO contract at the same time. MCO was introduced for
Mate, whose generated files never contained authoring mistakes; LLM-authored
files will.

## Non-goals and fixed constraints

- **Do not fix altium-monkey.** Defects and missing APIs are filed on the
  internal `wavenumber-eng/altium_monkey_dev` GitHub repository after review and
  consumed through a later pinned release. Cruncher code must not rely on
  private monkey attributes (leading underscore). Work blocked upstream waits or
  ships the unblocked subset with the gap documented.
- **No pad or other primitive-level PCB parameters.** Altium Designer 26.9 has no
  GUI for them (Pad Properties documentation, decompiled managed interfaces,
  native UI strings, a user GUI attempt, and corpus scans of 2,521 PcbLibs and
  636 PcbDocs parsed through altium-monkey). Only footprint and component
  parameters are authorable. Withdrawn 2026-09-26.
- **Display modes are optional.** Include `display_mode` support only if it is
  cheap on the public API (it may be; see upstream item 7); never block on it.
- Full PcbLib parity is out of scope; only the common footprint primitives.
- Tests and probes parse Altium files through altium-monkey, never hand-rolled
  record parsing.

## Analysis baseline (2026-09-26)

### Current MCO state

- 35 built-in operations, one TypeSpec file each under
  `src/tsp/altium_cruncher/mco/operations`, composed in `main.tsp`, results in
  `outputs/mco-builtins.tsp`. Handlers live in `altium_cruncher_mco.py` and
  `altium_cruncher_mco_cad_ops.py`; the handler map is checked against the
  generated catalog at import.
- Execution validates the envelope up front; reached built-ins validate args
  inside the failure boundary (ADR-0009), but only when not a dry run and only
  when the handler is the default one registered under its canonical name
  (`altium_cruncher_mco.py:593`).
- SchLib: `schlib.create` and `schlib.add_symbol` only. PcbLib: `pcblib.create`
  and `pcblib.add_footprint` only. `pcbdoc.add_*` operations reject PcbLib
  targets, so nothing can be drawn inside a footprint through MCO.
- `schdoc.add_component` already accepts `part_id` and `display_mode`.
- Mate never generates symbols; it copies libraries and places them.
- EasyEDA symbol import calls altium-monkey directly through public API. The
  EasyEDA footprint builder also uses **private monkey internals**
  (`easyeda_altium_footprint.py:238-239` `_authoring_builder` /
  `_sync_from_authored_library`; `:880-883` private region header fields;
  `:910` `_require_authoring_builder()._append_primitive`) and embeds in-memory
  STEP bytes (`:422`), which the `add_embedded_3d_model` operation cannot accept
  (file path only).

### Contract audit findings

1. **Unknown keys are silently ignored at both levels.** Every Args *and*
   Operation model extends `Record<unknown>`. `pcbdoc.add_track` with
   `layr:"BOTTOM"` passes and draws on `TOP`; an operation with `on_fial` passes
   `decode_mco` and the envelope check and silently loses its failure branch.
2. **Enumerated values are not enumerated.** `NativeEnum = string | integer`;
   unknown names pass structural validation.
3. **Almost no field documentation.** 33 of 35 operation files have no `@doc`.
4. **Imprecise types.** `schdoc.add_component.part_id`/`display_mode` are
   `float64`.
5. **Validation gaps hidden by hand checks.** Dry runs and built-in handlers
   registered under custom aliases skip contract validation and rely only on
   handler hand checks, which duplicate the contract elsewhere.
6. **No CLI preflight.** `decode_mco` exists only as an API.
7. **Inconsistent library semantics.** `schlib.add_symbol` edits in place
   without `MutationArgs`; `pcblib.add_footprint` uses them. `schlib.create`
   writes to disk and does not seed the session; `pcblib.create` seeds the
   session and writes nothing until flush.
8. **Delegated STEP fields are untyped.** Mate emits `board_outline`, `drills`,
   `features`, `fuse_copper`, `include_board_outline`, `thickness_mm`, `z_mm` in
   `pcbdoc.export_layer_step`, none declared in its TypeSpec model; the handler
   forwards unknown keys to `PcbLayerStepConfig`. `pad_geometries` is
   `unknown[]`.
9. **Misleading names.** In `pcblib.add_footprint`, `parameters` writes internal
   footprint metadata; `primitive_parameters` writes GUI footprint parameters.
10. **Windows freshness check.** `npm run check:contracts` fails on
    `core.autocrlf=true` checkouts (byte comparison against CRLF files).
11. Result contracts (`mco_builtin_result`) are complete and test-validated
    today; keep that for new operations.

### MCO runtime findings

- **Libraries built in a run cannot be placed later in that run.** Placement
  reads libraries from disk (`altium_cruncher_mco_cad_ops.py:152`, `:387`)
  without flushing the session; reproduced with `pcblib.create` →
  `pcblib.add_footprint` → `pcbdoc.add_component` ("PcbLib file not found").
- **SchLib sessions save without `sync_pin_text_data=True`**
  (`altium_cruncher_mco.py:1226`); Clean, EasyEDA import and MegaMaid pass it.
- **Session reuse ignores `file`.** `open_for_mutation` returns a cached output
  document regardless of the operation's input path (`altium_cruncher_mco.py:57`).
- **Footprints created in a run are invisible until save.** In altium-monkey,
  `AltiumPcbLib.footprints` stays empty until `save()` (#119). This breaks
  `pcblib.add_footprint`'s duplicate check and any later lookup of a footprint
  created earlier in the same run. Cruncher must not call the private builder
  sync. Until #119 is resolved, either track created footprint names in the
  session or flush and reload the library.
- Whether footprint parameters reach a component placed by
  `pcbdoc.add_component` is unverified; a probe read back empty component
  parameters.

### altium-monkey findings (filed, not fixed)

Verified against altium-monkey 2026.9.22; reviewed claims corrected. Filed on
2026-09-26 as `wavenumber-eng/altium_monkey_dev` #115 (findings 1, 2, 3 and
the helper part of 7), #116 (5, 6), #117 (8 and the stale-record part of 7),
#118 (4, 11) and #119 (9, 10, plus footprints invisible before save). Links and
refinements are in the `file-monkey-issues` log. Record the resolving release
there before closing dependent steps.

1. `belongs_to_part` keeps only `owner_part_id == -1` or the requested part, so
   part-0 objects (treated as shared by rendering and bounds) are dropped when
   a part is placed.
2. Helper ownership defaults are wrong or inconsistent: graphic helpers
   (`add_rectangle`, `add_line`, `add_arc`, …) turn the documented shared value
   `-1` into part 1; `add_label`, `add_parameter`, `add_designator`, `add_image`
   turn it into `None`, saved as 0 and then dropped by finding 1. Setting the
   public `owner_part_id = -1` after the helper call persists correctly.
3. SchDoc placement copies children of every display mode, not the selected one.
4. `add_arc`, `add_ellipse` and rounded-rectangle radii truncate to whole
   10-mil units; docstrings say 10-mil units while code uses mils.
5. **No pin-scoped parameter API.** `pin.pin_parameters` is a load-time view;
   appended entries are dropped on save. The public
   `AltiumSymbol.add_parameter(..., owner_index=..., index_in_sheet=...)` route
   works when `owner_index` is the pin's record index from the public
   `synthesize_raw_records()`, but the index shifts whenever an object is
   inserted before the pin. File as an ergonomics/robustness issue, not a hard
   blocker.
6. `pin.hidden_net_name`, `pin_package_length`, `propagation_delay` are lost on
   save; Altium stores `HiddenNetName` as a pin-owned parameter record.
7. Display-mode ergonomics: `AltiumSchPin` accepts `owner_part_display_mode` and
   `display_mode_count` is a plain attribute used at synthesis, but graphic
   helpers lack a display-mode keyword and symbols with an existing
   `component_record` do not pick up later changes. Narrow before filing.
8. Component kind and other component-record fields are only settable by
   overriding the raw `component_record`, which then goes stale.
9. New footprints receive only the `Footprint` primitive-parameter group;
   Altium writes `Footprint`, `System` and a blank group. Altium acceptance is
   unverified.
10. EasyEDA footprint needs that the public API does not cover (from the
    survey): region/arc authoring requiring private region fields and builder
    access, and embedding in-memory STEP data.
11. Bundled wheel docs referenced by package metadata are absent.

### Reference evidence

- GUI-authored project (temporary; promote before use):
  `C:\eli\temp\pin_pad_params\` with `pin_pad_params.SchLib` (two-part symbol;
  pin 1 one parameter, pin 2 two, pin 3 three; footprint link),
  `pin_pad_params.PcbLib` (three-pad footprint), and the placed SchDoc/PcbDoc.
- Pin parameter encoding: `RECORD=41` after the pin, `OwnerIndex` = pin record
  index in the symbol, `IndexInSheet` 0,1,2 per pin (omitted for 0), hidden, at
  the pin. Placement copies them and Altium appends `PinUniqueId`.
- Footprint parameters: corpus `common/pcblib_synthesized/fp140_footprint_parameters`
  (Altium-saved, `=`/`|` escapes); altium-monkey round-trips it exactly.
- Corpus pin-parameter use: `Bank` (FPGA SchDocs) and `HiddenNetName`; no corpus
  SchLib has pin parameters.

## Decisions to confirm (step `confirm-decisions`)

Recommended defaults; each was challenged in the plan review.

1. **Strictness.** Built-in Operation and Args models reject unknown keys.
   Custom operations (`OpenOperation`/`CustomOperation`) stay open; reserved
   built-in names already cannot fall into them. Amend ADR-0009: its rationale
   against a strict decoder was about *timing* (skipped rows, `on_fail`, custom
   handlers), which is preserved because reached-operation validation timing
   does not change; `mco check`/`decode_mco` will now reject files carrying keys
   read only by replacement handlers.
2. **Versioning: container and operation are separate concepts.**
   - *Container version* (`schema` tag): document shape, the operation-entry
     fields (`op`, `id`, `message`, `on_fail`, `args`, op-version field),
     execution rules and strictness of operation-entry keys.
   - *Operation version*: each operation's argument contract evolves
     independently using the ADR-0008 scheme (additive → next `a` revision,
     breaking → `b0`). Strict unknown-argument rejection belongs to the
     operation version; new operations are strict from their first version.
   - Proposed link: an optional per-operation field (name to decide, e.g.
     `op_version`). Each container version pins a frozen default table of
     operation versions for entries that omit it. `a0` documents resolve all
     operations to `a0`, preserving today's behavior. A newer container
     resolves to the operation versions current at its release. Older
     operation versions are handled by argument upgrade adapters feeding one
     handler. `mco list` shows supported versions, and results report the
     resolved version.
   - Open: the field name; whether omitted operation versions resolve through
     the container table (recommended) or always to the oldest version; the
     rollout (additive container `a1` introducing the field, then a strict
     container `b0`); schema publication and the release-note text.
3. **Enums.** New fields use TypeSpec literal unions with an explicit literal →
   monkey enum mapping table and a test against the installed monkey. A field
   shared by one handler has one contract: pad shape either closes everywhere
   (breaking, under `b0`) or stays open with documented names; layer selectors
   stay open because of V7 semantic tokens and aliases, with documented names.
4. **Granularity.** One operation per primitive kind, plus batched
   `schlib.add_pins`. Batch operations validate and resolve every entry before
   mutating anything (all-or-nothing), so `on_fail` never sees a half-built
   symbol.
5. **Library mutation semantics.** Decide with these facts: `MutationArgs`
   requires `output_file` or `overwrite:true` on every operation (a 60-operation
   symbol repeats it 60 times); the session already reuses cached documents.
   Recommended: a document created earlier in the same run is mutable in place
   without `overwrite`; editing a pre-existing file still requires
   `output_file` or `overwrite:true`. Decide whether `schlib.add_symbol` moves to
   this model (breaking under `b0`) or stays documented as an exception.
6. **Units and colors.** Mils everywhere; colors `"#RRGGBB"`.
7. **Multi-part ownership.** `part` is an integer ≥ 1 or omitted; omitted means
   shared and handlers set the public `owner_part_id = -1` after every helper
   call (graphics and text alike). Tests cover shared text as well as graphics
   surviving per-part placement.
8. **Draw order.** Body graphics must precede pins. No automatic reordering (it
   would shift pin record indexes used for pin parameters and there is no public
   ordered insert). Handlers reject, or warn on, a body graphic added to a
   symbol that already has pins; the guide documents "body first, pins second"
   and `clean` repairs existing libraries.
9. **Designators.** Normalized form matches `^[A-Za-z][A-Za-z_]*\?$`. Input is
   trimmed; a trailing `?` is kept; trailing digits are stripped
   (`R1`, `R12` → `R?`); multi-letter prefixes are preserved (`SW3` → `SW?`);
   anything else (empty, whitespace, no leading letter) becomes `U?`. Results
   report supplied and normalized values.
10. **Footprint parameter naming.** Canonical `footprint_parameters`;
    `primitive_parameters` stays as a deprecated alias under `a0` and is
    removed in `b0`; document that `parameters` is internal metadata.
11. **Pin-parameter route.** Decide whether the public `add_parameter(owner_index=…)`
    route may be used before a pin-scoped monkey API ships (it is public, but
    index-fragile). Recommended: use it only inside `schlib.add_pins`, computing
    indexes after the batch is appended and with draw order enforced by
    decision 8, and switch when upstream ships a pin-scoped API.

## Work plan

### `contract-freshness-crlf`

Independent tooling fix; land first. Compare generated content with normalized
line endings (or add `.gitattributes` `eol=lf` for generated artifacts).

### `file-monkey-issues`

Open one issue per reviewed finding on `wavenumber-eng/altium_monkey_dev` with
a minimal public-API reproduction and reference files where relevant. Nothing
is posted before the list is reviewed with the user. Record links and the
eventual pinned release in a plan log (`docs/plans/library-authoring-mco/logs/`).

### `promote-reference-fixtures`

Move the GUI-authored files from `C:\eli\temp` into the governed corpus (or
`tests/assets`), with a README describing how each was made.

### `survey-easyeda-footprint` and `easyeda-baseline`

Survey the footprint builder the same way as the symbol builder, listing every
private-internal use as an upstream issue (finding 10). Before any builder is
rewritten, snapshot current output for the offline fixtures in
`tests/assets/easyeda/api_responses`: per-type object counts, pin attributes,
parameter sets, pad/track/region geometry within tolerance, parsed through
altium-monkey. Store the snapshot as a test fixture.

### `mco-validation-coverage`

Validate built-in args on dry runs and for built-in handlers registered under
custom aliases (look up the canonical contract name). Only afterwards remove
hand checks that the contract guarantees; keep semantic checks.

### `mco-strict-models`

- Close built-in Operation and Args models under `b0` (decisions 1–2); keep
  lenient `a0` decoding as decided.
- Type delegated `pcbdoc.export_layer_step` fields by reusing the
  `pcb_layer_step_config` TypeSpec model; type `pad_geometries`.
- Fix integer types; apply decision 10.
- Add vectors (unknown arg key, unknown operation key, bad enum) to
  `tests/fixtures/mco-contract-vectors.json`.
- Add a permanent test that strictly decodes every Mate-generated payload
  (all `build_mate_mco` outputs exercised by `tests/test_mate.py`, including
  `--emit-mco`).
- Regenerate; run `check:contracts`, `check:typescript`, `check:browser`
  (generated TypedDict/TypeScript shapes change).

### `mco-field-docs`

`@doc` on every field of all existing operations and `common.tsp` models:
purpose, units, allowed values. Can proceed in parallel with the strict-model
work.

### `mco-check-command`

`altium-cruncher mco check <file>` runs full structural validation with the
existing colorized output and `--json`. Update `docs/design/cli/mco.html`
(ADR-0005 sections), the command manifest and `mco list` output tests.

### `mco-runtime-fixes`

- Make `schlib.create` and `pcblib.create` behave the same (both seed the
  session).
- Flush a library path from the session before any operation reads it from disk.
- Honor the operation's input path when reusing cached documents, or document
  and test the intended semantics.
- Save SchLib sessions with `sync_pin_text_data=True`.
- Tests: create, populate and place from a SchLib and a PcbLib in one run.

### `schlib-operations`

Draft set (names settle in implementation; all `b0`):

- `schlib.add_symbol` (extended) or `schlib.set_symbol`: `designator`, `comment`,
  `description`, `part_count`, `component_kind`; optional `display_mode_count`.
- `schlib.add_pins`: batch; per pin `designator`, `name`, `position_mils`,
  `orientation`, `length_mils`, `electrical_type`, `hidden`, `name_visible`,
  `designator_visible`, IEEE edge symbols, `description`, `part`, `parameters`
  (per decision 11).
- Body graphics: `add_rectangle`, `add_rounded_rectangle`, `add_line`,
  `add_polyline`, `add_polygon`, `add_arc`, `add_ellipse`, `add_text`; optional
  `part`, colors, line width, fill.
- `schlib.add_parameter`; `schlib.add_footprint` (implementation link, multiple
  allowed, current flag).
- Possibly `schlib.remove_symbol` / `schlib.rename_symbol`.
- Result contracts and failure paths (missing symbol, invalid part, draw-order
  violation, batch rollback).
- Tests: save/reload through altium-monkey; multi-part symbol placed per part
  with shared graphics and text; comparison with the GUI reference; per-part
  SVG previews.

### `pcblib-operations`

- Footprint primitives for the surveyed subset. Prefer generalizing existing
  `pcbdoc.add_*` handlers with a PcbLib target plus `footprint` selector; shared
  handlers share field contracts (decision 3).
- `pcblib.add_footprint_parameter` (or `set_`) for existing footprints.
- Verify footprint parameters on placed components against an Altium-placed
  reference; file upstream if placement drops them.
- Tests: save/reload, create-and-place in one run, previews.

### `easyeda-on-mco`

EasyEDA import builds and executes an MCO document (optional `--emit-mco`).
STEP data is written as a sidecar file referenced by the emitted MCO (a
temporary directory for in-process runs). Equivalence = the `easyeda-baseline`
comparison plus an explicit list of accepted differences (for example arc
regions blocked on finding 10). Add symbol → footprint links. Update the
`easyeda-import` CLI design doc and manifest for any new flag, and keep
`easyeda_symbol_report`/`easyeda_footprint_report` contracts current.

### `llm-authoring-guide`

A design document plus `mco list` metadata: grid and pin conventions, pin
orientation, body-before-pins, designator rules, multi-part and shared objects,
parameters and footprint links, footprint primitives and parameters, the
`mco check` → `mco run` → `sch-svg`/`pcb-svg` loop, common mistakes. Worked
examples (a dual op-amp; a small MCU with footprint) under `examples/` run as a
named Rack task.

## Risks

- Upstream dependency for pin-parameter robustness, part-0 placement and
  EasyEDA regions.
- `b0` strictness breaks third-party files relying on ignored keys; mitigated
  by the `a0` window, release notes and `mco check`.
- Enum drift; mitigated by the mapping-table test.
- Altium acceptance of monkey-authored footprints unverified without opening
  generated files in Altium.

## Open questions

- Is placed-pin (SchDoc) parameter editing needed, or only library pins?
- Should the guide also ship as an installed resource (`mco guide`)?

## Plan review disposition (2026-09-26)

An independent review verified the core findings and raised 13 material items;
all are folded in above: Mate STEP-field regression (strict-models step and
Mate decode test), EasyEDA private-internal use and STEP bytes (finding 10,
sidecar files, dependency on filed issues), wire versioning (decision 2),
operation-level unknown keys (finding 1, decision 1), validation gaps before
removing hand checks (`mco-validation-coverage`), pin-parameter public route
(finding 5, decision 11), `-1`→`None`→0 ownership (finding 2, decision 7),
display-mode overstatement (finding 7), mutation/session semantics (decision 5,
runtime fixes), batch atomicity (decision 4), shared-handler enum consistency
(decision 3), equivalence baseline (`easyeda-baseline`), and step splitting and
exit criteria. Minor items (designator regex, enum mapping table, plan log,
docstring mismatch, Rack task, TypeScript/browser checks) are also applied.
