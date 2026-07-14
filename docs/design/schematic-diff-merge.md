# Schematic Diff And Merge Design

Status: research/design seed
Implementation issue: https://github.com/wavenumber-eng/altium_cruncher/issues/28
Originating cleanup issue: https://github.com/wavenumber-eng/appz/issues/60

## Purpose

`altium-cruncher` should eventually provide a semantic review workflow for
Altium schematic changes. Git sees `.SchDoc` files as binary documents, so a
normal text merge conflict cannot tell the user whether a change is meaningful
schematic intent, harmless Altium save churn, or an electrical conflict.

The immediate goal is not to expose a public command. This document preserves
the useful planning work from the removed `appz/altium_diff` prototype and
places future implementation ownership in the standalone `altium-cruncher`
repo.

## Ownership

This workflow belongs in `altium-cruncher` because it is a higher-level Altium
document workflow built on public `altium-monkey` APIs. It should not live in
`appz` as a separate application package.

The first implementation should use only declared public `altium-monkey` APIs.
If the analyzer needs new parser or mutation support, capture that as an
explicit `altium-monkey` follow-up instead of importing private internals.

## Initial Scope

Start with one `.SchDoc` at a time.

Initial goals:

- read two or three `.SchDoc` files through public `altium-monkey` APIs;
- normalize away non-semantic Altium save churn;
- identify standalone records and bounded owner groups;
- classify changes as topology, component metadata, directive, hierarchy,
  visual-only, or storage-sensitive;
- emit a machine-readable analysis bundle;
- render SVG or HTML review artifacts that connect list entries to schematic
  objects;
- emit a decision manifest that can later be applied to produce a merged
  `.SchDoc`.

Out of scope for the first implementation:

- complete `.PrjPcb` merge;
- direct Git history browser;
- automatic writeback without a reviewed manifest;
- private `altium-monkey` internals;
- a PyQt desktop shell.

Complete project workflows should compose the single-sheet engine rather than
bypassing it.

## Expected Flow

```text
base/ours/theirs SchDoc files
  -> semantic analysis bundle
  -> static HTML/SVG or CLI review
  -> decision manifest
  -> manifest applier
  -> merged SchDoc
```

For an active Git conflict, a future wrapper can consume Git mergetool inputs
`$BASE`, `$LOCAL`, `$REMOTE`, and `$MERGED`. The engine should not need to run
Git itself to resolve an already materialized conflict.

Two-way diff should be implemented before three-way merge. Writeback and
automatic merge should come after the analyzer is trustworthy.

## Existing Surfaces To Reuse

Prefer existing `altium-cruncher` and `altium-monkey` surfaces before adding a
new model:

- `json-dump` already serializes parsed SchDoc documents.
- `sch-ir` already emits gotIR JSON suitable for schematic review and object
  rendering metadata.
- `sch-svg` already renders schematic SVG output.
- `design` already creates a review bundle with design JSON, serialized
  document JSON, notes, schematic SVGs, and a manifest.
- `AltiumSchDoc` exposes parsed object collections, typed query views,
  `to_json()`, `to_ir()`, normal mutation flows, and save/writeback support.

The semantic diff engine can start as a library module consumed by tests. A CLI
command should be added only after its command name, output layout, manifest
schema, and docs are ready to become public or explicitly experimental
contracts.

Potential command names to decide later:

- `sch-diff`: focused, avoids overloading existing library `merge`;
- `diff`: broader name, only if it will eventually dispatch across document
  kinds;
- `sch-merge`: only after three-way analysis and manifest apply are working.

## Non-Semantic Churn To Normalize

Initial normalization should ignore or demote:

- object parse order when the semantic object did not change;
- `IndexInSheet`;
- `OwnerIndex`;
- generated header counters;
- field casing differences;
- numeric string representation differences;
- default values added by Altium on open/save.

Z-order may become a visual warning later, but it should not block the first
semantic diff unless rendered output actually changes.

## Object Identity Strategy

Primary identity:

- sheet or session id;
- schematic record type;
- `UniqueID`.

Fallback identity should be type-specific:

- components: designator, library reference, design item id, and location;
- pins: parent component plus pin designator, name, and location;
- parameters: owner plus parameter name;
- wires and buses: normalized point list, optionally reversed, plus nearby net
  context;
- ports, power ports, and net labels: text/name, type, and location;
- sheet entries: parent sheet symbol plus entry name;
- graphics: record type, owner, geometry, and bounding box.

Fallback matches should carry a confidence score. Low-confidence matches belong
in an `identity_uncertain` bucket and should not be silently merged.

## Change Classification

Each change should be classified into one or more categories:

- `topology`: wires, buses, net labels, ports, power ports, pins, sheet entries;
- `component_metadata`: designator, value, footprint, library reference,
  parameters;
- `hierarchy`: sheet symbols, sheet names, file names, harnesses;
- `directive`: compile masks, no-ERC, blankets, parameter sets, differential
  pairs;
- `visual`: colors, line widths, fonts, free graphics, notes;
- `storage`: binary/image/storage details that need preservation or special
  handling.

Review output should sort topology and component changes above visual-only
changes.

## Analysis Bundle Boundary

The analyzer should emit an analysis bundle containing normalized semantic data,
rendered review artifacts, and enough metadata for UI or CLI review layers to
display changes.

The UI or reviewer writes a decision manifest. The manifest applier is the only
layer that writes a merged `.SchDoc`. Review surfaces must not directly mutate
`AltiumSchDoc` objects.

Initial bundle shape:

```text
session/
  inputs/
    base.SchDoc
    ours.SchDoc
    theirs.SchDoc
  analysis.json
  base.svg
  ours.svg
  theirs.svg
  diff.html
  decisions.json
```

Two-way diff sessions may omit `base.SchDoc`.

Initial decision manifest shape:

```json
{
  "schema": "altium_cruncher.sch_diff.decisions.a0",
  "session_id": "example",
  "resolutions": [
    {
      "change_id": "change-001",
      "decision": "ours",
      "notes": ""
    }
  ]
}
```

Before this becomes a public command, add JSON schema contracts under
`docs/contracts/` and conformance tests.

## Milestones

1. Two-way semantic diff library
   - snapshot model;
   - canonical object record normalization;
   - identity matching by `UniqueID`;
   - standalone object added/deleted/modified detection;
   - JSON analysis output.

2. Review bundle
   - render each side to SVG;
   - build a static HTML report;
   - layer toggles for left/right or ours/theirs;
   - list item to SVG object highlighting;
   - change filters by classification.

3. Three-way analysis
   - base/ours/theirs session model;
   - auto-clean change detection;
   - conflict classification;
   - decision manifest schema.

4. Manifest apply and writeback
   - manifest applier;
   - merged `.SchDoc` output;
   - reparse-and-compare verification;
   - rendered merged preview.

5. Git workflow integration
   - Git mergetool wrapper using `$BASE`, `$LOCAL`, `$REMOTE`, and `$MERGED`;
   - helper to extract Git index stages for conflicted files;
   - optional commit-chain/history diff view over one schematic.

## First Tests To Write

- Save-only `.SchDoc` pair produces minimal or no semantic diff.
- Added object, deleted object, and simple modified object are reported
  correctly.
- Objects with unchanged `UniqueID` but changed non-semantic fields are
  normalized.
- Same-field different-value edits in ours/theirs are reported as conflicts.
- Delete-vs-modify is reported as a conflict.
- Decision manifests round-trip through schema validation.
- A reviewed manifest can synthesize a merged `.SchDoc`, then save/reopen
  yields the expected semantic snapshot.

## Open Questions

- Which command name should become public first: `sch-diff`, `diff`, or a
  subcommand under an existing schematic command?
- Should first review output build directly on `design` bundles or use a
  smaller dedicated session layout?
- Which fields need to be considered semantic for the first release, and which
  should be classified as visual warnings?
- Are additional public `altium-monkey` helpers needed for stable owner-group
  traversal or mutation-safe writeback?
