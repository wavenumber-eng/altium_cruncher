# Mate Implementation Plan

Status: active, Cricket public example cleanup verified

This plan tracks the implementation slices for the `mate` mating-board
workflow in `altium_cruncher`. The stable public contracts live in the design
docs; this file is the working tracker for current implementation order,
remaining work, and release exit criteria.

## Design Sources

- `docs/design/cli/mate.html` - current command behavior.
- `docs/design/cli/mate-config.html` - portable mate config shape
  and theory of operations.
- `docs/design/api/mate-automation-interfaces.html` - public contracts
  and test obligations.
- `docs/design/cli/mco.html` - generated MCO operation contract.
- `examples/mate/cricket-node/README.md` - runnable Cricket Node
  reference workflow.
- `examples/mate/cricket-node/expected-operations.md` - example-level
  expected output behavior.

## Goals

- Make the Cricket Node mate workflow feature-complete enough to use as
  the first public example.
- Keep the human-authored config portable in concept, while generated MCO stays
  Altium-specific.
- Keep the command self-contained in public `altium_cruncher`; do not import
  private Wavenumber data-model packages.
- Preserve public interfaces while the config and generated operation contract
  are still marked experimental.
- Build the implementation in committed slices with focused tests for each
  slice and full signoff before release.

## Current State

- `mate` now owns the normal public workflow: with no config it writes an
  editable `mate.a0.jsonc`; with a config it emits the derived MCO and runs it.
- `mate plan` emits the derived MCO only, and `mate libs` lists discoverable
  SchLib symbols and PcbLib footprints from search roots.
- `mate` can create a generated Altium project with schematic, PCB, copied
  libraries, mate components, reference graphics, board cutouts, PCB labels,
  schematic wires/net labels, designator arrangement, feature union, and STEP
  artifact operations.
- The Cricket example has been manually inspected in Altium for several output
  slices.
- Public Cricket mate parts are now resolved by `symbol_name` and
  `footprint_name` from config-relative `libraries.roots`; the old generated
  known-parts manifest remains a tested compatibility path but is no longer
  part of the public example.
- The next design pressure is missing-part fallback behavior, graphics-only
  projections, and simplifying the config further after manual inspection.

## Terminology

- Source, input, DUT: the board being mated to.
- Destination, output, mate board: the generated board.
- Config: human-authored or GUI-authored source of truth.
- Plan: resolved source facts and projection decisions.
- MCO: generated Altium-specific operation script, analogous to compiled
  object code.
- Mate component: a reusable output symbol/footprint selected by a projection
  action and resolved from configured public libraries.

## Implementation Slices

| Slice | Status | Description | Exit Criteria |
| --- | --- | --- | --- |
| S0 | done | Create this active implementation tracker. | Plan exists and points to the design contracts. |
| S1 | done | Document the library-root resolver MVP. | Design docs define config fields, search paths, duplicate handling, and generated MCO expectations. |
| S2 | done | Add public-safe Altium library indexing. | `altium_cruncher` can index `.SchLib` symbol names and `.PcbLib` footprint names from configured roots without importing private packages. |
| S3 | done | Add named mate-component resolution. | Config accepts `libraries.roots` plus `mate_component.symbol_name` and `footprint_name`, while preserving the existing manifest/cache path for compatibility tests. |
| S4 | done | Resolve mate components during planning. | `mate plan` resolves symbol/footprint names to concrete libraries, reports clear errors for zero or multiple matches, and emits concrete MCO paths only in generated output. |
| S5 | pending | Keep graphics-only projection valid. | A config can intentionally generate reference graphics, outlines, labels, cutouts, and STEP artifacts without placing mate components. |
| S6 | done | Update Cricket example to the new resolver style. | The example can run from its folder using relative search paths and does not require hand-authored absolute library paths. |
| S7 | done | Stabilize config and MCO docs. | Design docs, example README, expected operations, and command help match implemented behavior. |
| S8 | pending | Release signoff. | Focused tests, full test suite, lint/type checks, and manual Altium inspection notes are complete. |

## Library Resolver Direction

The MVP allows users to specify mate parts by symbol and footprint names, plus
one or more search roots. Search roots are config-relative by default so
examples are portable and command invocation directory does not change behavior.

Recommended authored shape:

```jsonc
{
  "libraries": {
    "roots": ["mating_parts"],
    "recursive": true
  },
  "projections": [{
    "id": "test_points",
    "source": {"object": "component", "designators": "TP*"},
    "actions": [{
      "kind": "mate_component",
      "symbol_name": "YZ209315103P-01",
      "footprint_name": "YZ209315103P-01",
      "designator_prefix": "TP",
      "signal_pad_designator": "1"
    }]
  }]
}
```

Resolver behavior:

- exact one symbol and footprint match: use it;
- zero matches: fail by default; graphics-only fallback remains a deferred
  explicit policy;
- multiple matches: fail with candidate paths unless the config provides a
  root, path, or library hint;
- generated MCO stores concrete resolved paths, not unresolved search roots;
- authored config should avoid absolute paths unless the user intentionally
  chooses a machine-local setup.

The existing manifest/cache workflow remains available for compatibility tests
and older local configs. It is no longer the public Cricket example path.

## Cricket MVP Target

The Cricket Node example should demonstrate:

- source component selection with compact designator selectors;
- free NPTH/alignment pad selection;
- mate component insertion for test points, mounts, and alignment pins;
- generated schematic symbols linked to generated PCB components;
- schematic wires and net labels arranged by symbol group in natural
  designator order;
- configurable PCB designator text style and placement;
- loose board-edge net-label columns with group headers and shared label
  widths;
- source-pad reference outlines on a configurable mechanical layer, using
  effective layer pad bodies for circular, obround, rectangular/square,
  octagonal/chamfered, and rounded-rectangle pads;
- source board outline and cutout projection;
- generated board size with configurable margins around the DUT;
- bottom-layer fixture-alignment STEP artifact generation with projection-linked
  pad color rules, selected `TP*` component-pad copper, large ring-shaped NPTH
  drill overlays, pad-shaped plated drill overlays, artifact-hashed filenames,
  and 3D-body Z placement;
- a user union for generated fixture features, excluding loose labels intended
  for manual repositioning.

## Testing Strategy

Use focused tests during development and full signoff before release.

Focused lanes:

- config parsing and template generation;
- source inspection and selector expansion;
- library indexing and known-part resolution;
- MCO planning shape;
- MCO operation handlers for schematic and PCB mutations;
- Cricket example planning and run smoke tests;
- JSON read-back with `json-dump` for generated SchDoc/PcbDoc assertions.

Full signoff:

- `uv run --extra test pytest -q`;
- release signoff tests;
- lint and type checks used by the repo;
- manual Altium inspection of the Cricket example output when geometry or
  linkage behavior changes.

## Deferred Topics

- GUI config authoring and source-object selection.
- Source schematic symbol reuse as a mate symbol fallback.
- Source footprint 1:1 projection for shield/header workflows.
- Multi-pin connector mating and pin-order policies.
- Saleae-style breakout connector automation.
- Public A0 JSON reader for future CAD part/library metadata.
- Alexandria/library-facet integration outside the public package boundary.
- Generic `pcb_cruncher` and KiCad backend mapping.
- Update-in-place behavior for an existing mate board.
- Filled source-pad reference graphics using the same effective pad-shape model.

## Slice Log

- S0: Created active implementation plan and linked it to the current design
  contract docs.
- 2026-06-07: Renamed the public workflow, CLI command, examples, design docs,
  command manifest, tests, and plan folder to `mate`.
- 2026-06-07: Updated source-pad reference graphics to read effective
  source-layer pad geometry and emit shape-specific outlines for circular,
  obround, rectangular/square, octagonal/chamfered, and rounded-rectangle pads.
- 2026-06-07: Fixed `pcb-layer-step` pad/highlight shape export so unequal
  circular pad bodies, such as Cricket TP9, emit obround/capsule STEP regions
  instead of oval approximations.
- 2026-06-07: Changed mate-generated `pcb-layer-step` component highlights to
  use projection-linked pad color rules instead of duplicate explicit highlight
  bodies, so Cricket TP10 and other selected component pads are colored in
  place on the copper layer.
- 2026-06-07: Changed mate-generated `pcb-layer-step` defaults to render NPTH
  drill overlays as rings and plated drill overlays with pad-shaped geometry,
  matching the standalone `pcb-layer-step` default config.
- 2026-06-07: Added artifact hashes to mate-generated `pcb-layer-step` STEP
  filenames so Altium reloads regenerated embedded models instead of using a
  stale embedded-model cache entry with the previous filename.
- 2026-06-07: Aligned mate-generated `pcb-layer-step` defaults with the
  standalone fixture-alignment config by limiting Cricket STEP source copper to
  selected `TP*` component pads and large drill overlays. Full bottom-layer
  routing copper remains opt-in through the mate config.
- 2026-06-07: Simplified the public `mate` workflow so a bare command creates
  or runs `mate.a0.jsonc`, added `mate libs` for SchLib/PcbLib discovery,
  added name-based `mate_component` resolution from `libraries.roots`, removed
  the checked-in Cricket config and known-parts manifest, and moved the public
  Cricket example to a README-driven layout with committed DUT files and
  minimal `mating_parts/` libraries.
