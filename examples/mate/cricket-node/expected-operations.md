# Expected Operation Sequence

After `mate.a0.jsonc` has been generated and reviewed, `mate plan` should emit
an MCO with this high-level shape:

1. `project.create-skeleton`, with a rectangular board outline expanded from
   the DUT bounds by the configured margin and an ANSI `D` schematic sheet.
2. Six `file.copy` operations for the SchLib/PcbLib files resolved from
   `mating_parts/` by `symbol_name` and `footprint_name`.
3. For each selected `TP*`: schematic component with a stable unique ID,
   pin-directed schematic wire, matching-orientation schematic net label on
   that wire, PCB pogo component linked back to that schematic ID, and one
   expanded source-pad reference outline using the effective source-layer pad
   shape. Symbols are grouped by symbol type on the schematic sheet, sorted in
   natural designator order inside each group, and written with centered-above
   schematic designators.
4. For each selected `M1-M4`: schematic component with a stable unique ID and
   PCB standoff component linked back to that schematic ID.
5. For each matching free NPTH alignment pad: schematic component, optional
   pin-directed schematic wire and matching-orientation net label, and PCB
   alignment-pin component.
6. `pcbdoc.add-track` operations projecting the DUT board outline onto the
   configured graphics layer, plus configured internal cutout outlines on
   `MECHANICAL_1`.
7. `pcbdoc.add-region` board-cutout operations for each detected DUT internal
   cutout when `board_projection.cutouts.actual_cutouts` is enabled.
8. `pcbdoc.arrange-designators` to move generated component-owned designator
   text above each mate component using the configured Arial 40 mil bold style.
9. `pcbdoc.export-layer-step` for the DUT bottom layer, including selected
   `TP*` component-pad copper, large drill overlays, board outline bodies,
   artifact-hashed output filenames, NPTH drill rings, pad-shaped plated drill
   overlays, and the configured red `test_points` pad color rule.
10. `pcbdoc.add-embedded-3d-model` to insert that STEP artifact into the output
    PcbDoc at the configured 8.5 mm Z height, using the DUT outline bounds for
    the body projection.
11. `pcbdoc.create-user-union` named `MATE_FEATURES` after PCB-side generation
    completes, so the group reflects the final generated board state.
12. Board-edge PCB net-label column headers and labels after the user union.
    These labels are grouped into one column per source projection/input type,
    use the same computed box width, and remain loose so they can be manually
    moved after generation.

The example uses Cricket Node's `M1-M4` mount designators directly. The old
node-test-array known-parts cache is no longer part of the public example; the
minimal libraries are checked in under `mating_parts/`.
