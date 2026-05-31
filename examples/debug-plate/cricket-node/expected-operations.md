# Expected Operation Sequence

`debug-plate plan debug-plate.mate.a0.jsonc` should emit an MCO with this
high-level shape after local inputs and the known-parts cache exist:

1. `project.create-skeleton`
2. Six `file.copy` operations for the selected SchLib/PcbLib cache files
3. For each selected `TP1-27`: schematic component, schematic net label, PCB
   component, PCB net label, and two mechanical reference rings
4. For each selected `M1-M4`: schematic component and PCB standoff component
5. For each matching free NPTH alignment pad: schematic component, optional
   schematic net label, PCB alignment-pin component, and optional PCB label
6. `pcbdoc.create-user-union` named `DEBUG_PLATE_FEATURES`
7. `pcbdoc.export-layer-step` for the DUT bottom layer, including copper, drill
   cutouts, board outline bodies, and the configured `test_points` highlight

The example config uses cricket-node's `M1-M4` mount designators directly. The
known-parts manifest still documents the old node-test-array `M5-M8` to
`M1-M4` normalization for reference.
