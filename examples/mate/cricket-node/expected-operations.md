# Expected Operation Sequence

`mate plan mate.a0.jsonc` should emit an MCO with this
high-level shape after local inputs and the known-parts cache exist:

1. `project.create-skeleton`, with a rectangular board outline expanded from
   the DUT bounds by the configured margin and an ANSI `D` schematic sheet
2. Six `file.copy` operations for the selected SchLib/PcbLib cache files
3. For each selected `TP1-27`: schematic component with a stable unique ID,
   pin-directed schematic wire, matching-orientation schematic net label on
   that wire, PCB component linked back to that schematic ID, and one expanded
   source-pad reference outline. Symbols are grouped by symbol type on the
   schematic sheet, sorted in natural designator order inside each group, and
   written with centered-above schematic designators.
4. For each selected `M1-M4`: schematic component with a stable unique ID and
   PCB standoff component linked back to that schematic ID
5. For each matching free NPTH alignment pad: schematic component, optional
   pin-directed schematic wire and matching-orientation net label, and PCB
   alignment-pin component
6. `pcbdoc.add-track` operations projecting the DUT board outline onto the
   configured graphics layer, plus configured internal cutout outlines on
   `MECHANICAL_1`
7. `pcbdoc.add-region` board-cutout operations for each detected DUT internal
   cutout when `board_projection.cutouts.actual_cutouts` is enabled
8. `pcbdoc.arrange-designators` to move generated component-owned designator
   text above each mate component using the configured Arial 40 mil bold style
9. `pcbdoc.export-layer-step` for the DUT bottom layer, including explicit
   track/polygon feature settings, copper, drill cutouts, board outline bodies,
   and the configured red `test_points` highlight
10. `pcbdoc.add-embedded-3d-model` to insert that STEP artifact into the output
   PcbDoc at the configured 8.5 mm Z height, using the DUT outline bounds for
   the body projection
11. `pcbdoc.create-user-union` named `MATE_FEATURES` after PCB-side
    generation completes, so the group reflects the final generated board state
12. Board-edge PCB net-label column headers and labels after the user union.
    These labels are grouped into one column per source projection/input type,
    use the same computed box width, and remain loose so they can be manually
    moved after generation.

The example config uses cricket-node's `M1-M4` mount designators directly. The
known-parts manifest still documents the old node-test-array `M5-M8` to
`M1-M4` normalization for reference.
