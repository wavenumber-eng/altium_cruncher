# Debug Plate / Mate Implementation Plan

Status: active

This plan tracks the implementation slices for the `debug-plate` mating-board
workflow in `altium_cruncher`. The stable public contracts live in the design
docs; this file is the working tracker for current implementation order,
remaining work, and release exit criteria.

## Design Sources

- `docs/design/cli/debug-plate.html` - current command behavior.
- `docs/design/cli/debug-plate-mate-config.html` - portable mate config shape
  and theory of operations.
- `docs/design/api/debug-plate-automation-interfaces.html` - public contracts
  and test obligations.
- `docs/design/cli/mco.html` - generated MCO operation contract.
- `examples/debug-plate/cricket-node/README.md` - runnable Cricket Node
  reference workflow.
- `examples/debug-plate/cricket-node/expected-operations.md` - example-level
  expected output behavior.

## Goals

- Make the Cricket Node debug plate workflow feature-complete enough to use as
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

- `debug-plate plan` can compile a Cricket Node config into an MCO.
- `debug-plate run` can create a generated Altium project with schematic, PCB,
  copied libraries, mate components, reference graphics, board cutouts, PCB
  labels, schematic wires/net labels, designator arrangement, feature union,
  and STEP artifact operations.
- The Cricket example has been manually inspected in Altium for several output
  slices.
- Known parts are currently driven by a generated manifest/cache seeded from
  node-test-array assets.
- The next design pressure is how users specify and resolve mate symbols and
  footprints without relying on private library infrastructure.

## Terminology

- Source, input, DUT: the board being mated to.
- Destination, output, mate board: the generated board.
- Config: human-authored or GUI-authored source of truth.
- Plan: resolved source facts and projection decisions.
- MCO: generated Altium-specific operation script, analogous to compiled
  object code.
- Known part: a reusable mate symbol/footprint definition selected by a
  projection action.

## Implementation Slices

| Slice | Status | Description | Exit Criteria |
| --- | --- | --- | --- |
| S0 | done | Create this active implementation tracker. | Plan exists and points to the design contracts. |
| S1 | pending | Document the known-parts resolver MVP. | Design docs define config fields, search paths, duplicate handling, missing-part policy, and generated MCO expectations. |
| S2 | pending | Add public-safe Altium library indexing. | `altium_cruncher` can index `.SchLib` symbol names and `.PcbLib` footprint names from configured roots without importing private packages. |
| S3 | pending | Extend `known_parts` config. | Config accepts inline part definitions, search roots, optional root/path hints, and missing-part policy while preserving the existing manifest/cache path. |
| S4 | pending | Resolve known parts during planning. | `debug-plate plan` resolves symbol/footprint names to concrete libraries, reports clear errors for zero or multiple matches, and emits concrete MCO paths only in generated output. |
| S5 | pending | Keep graphics-only projection valid. | A config can intentionally generate reference graphics, outlines, labels, cutouts, and STEP artifacts without placing mate components. |
| S6 | pending | Update Cricket example to the new resolver style. | The example can run from its folder using relative search paths and does not require hand-authored absolute library paths. |
| S7 | pending | Stabilize config and MCO docs. | Design docs, example README, expected operations, and command help match implemented behavior. |
| S8 | pending | Release signoff. | Focused tests, full test suite, lint/type checks, and manual Altium inspection notes are complete. |

## Known-Parts Resolver Direction

The MVP should allow users to specify mate parts by symbol and footprint names,
plus one or more search roots. Search roots should be config-relative by
default so examples are portable and command invocation directory does not
change behavior.

Recommended authored shape:

```jsonc
{
  "known_parts": {
    "search_paths": [
      ".",
      "known-parts",
      "local_library"
    ],
    "on_missing": "error",
    "parts": [
      {
        "role": "test_point_pogo",
        "target_kinds": ["test_point"],
        "designator_prefix": "TP",
        "signal_pad_designator": "1",
        "symbol": "YZ209315103P-01",
        "footprint": "YZ209315103P-01"
      }
    ]
  }
}
```

Resolver behavior:

- exact one symbol and footprint match: use it;
- zero matches: fail by default, or skip only when the config explicitly allows
  a graphics-only fallback;
- multiple matches: fail with candidate paths unless the config provides a
  root, path, or library hint;
- generated MCO stores concrete resolved paths, not unresolved search roots;
- authored config should avoid absolute paths unless the user intentionally
  chooses a machine-local setup.

The existing manifest/cache workflow remains useful for generated examples and
should stay compatible during the transition.

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
- source-pad reference outlines on a configurable mechanical layer;
- source board outline and cutout projection;
- generated board size with configurable margins around the DUT;
- bottom-layer STEP artifact generation with explicit pad highlights, track
  settings, polygon settings, and 3D-body Z placement;
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

## Slice Log

- S0: Created active implementation plan and linked it to the current design
  contract docs.
