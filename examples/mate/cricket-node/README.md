# Cricket Node Mate Example

This example is a runnable mate workflow for the Cricket Node DUT. It creates a
new mating-board project with pogo-pin test points, mounting/alignment parts,
source-board reference graphics, board cutouts, arranged designators, manual
net-label columns, and an embedded bottom-copper STEP alignment artifact.

The repo intentionally does not commit a generated `mate.a0.jsonc` config. The
first command writes that editable JSONC file from the example defaults; read
the comments in the generated file before running the workflow.

## Files

- `11-10028__cricket-node-hw__B.PrjPcb` is the DUT project.
- `cricket-node-hw__B.PcbDoc` and `cricket-node-hw--top-level_B.SchDoc` are the
  DUT PCB and schematic inputs.
- `mating_parts/` contains the minimal SchLib/PcbLib files used by the default
  mate config:
  - `YZ209315103P-01` for test-point pogo contacts;
  - `9774080360R` / `9774080360R-YIYUAN` for M2.5 SMT standoffs;
  - `H2184-05` for 2 mm alignment pins.
- `mate.a0.jsonc`, `*.mco.jsonc`, and `output/` are generated locally and
  ignored by git.

## Commands

Run commands from this folder. To use the working-tree package instead of an
installed `altium-cruncher`, prefix commands with
`uv run python -m altium_cruncher`.

Create the editable config:

```powershell
uv run python -m altium_cruncher mate
```

Inspect the discovered mating libraries:

```powershell
uv run python -m altium_cruncher libraries mating_parts
```

After reviewing `mate.a0.jsonc`, generate the debug MCO without executing it:

```powershell
uv run python -m altium_cruncher mate plan
```

Run the workflow:

```powershell
uv run python -m altium_cruncher mate
```

Run and open the generated project in Altium:

```powershell
uv run python -m altium_cruncher mate --launch
```

The generated project is written to:

```text
output\mate.PrjPcb
```

The generated STEP artifact is written under:

```text
output\artifacts\pcb-layer-step\
```

The same STEP is embedded in the generated output PcbDoc at the configured
`artifacts.pcb_layer_step.insert_in_output.z_mm` height. The default artifact
config follows the standalone `pcb-layer-step` fixture defaults: selected `TP*`
component pads are rendered, large drill overlays are rings, general routing
copper is omitted, and the STEP filename includes a short content hash so
Altium reloads regenerated models.

## Default Config Behavior

The generated config selects `TP*`, `M1-4`, and free NPTH alignment holes near
2 mm. Each `mate_component` action names the desired schematic symbol and PCB
footprint; `altium-cruncher` resolves those names by scanning `mating_parts/`
recursively.

Reference graphics trace the actual source pad shapes on `MECHANICAL_1`,
including round, obround, rectangular, octagonal/chamfered, and rounded-rect
pads. Net-label columns are generated outside the user union so they can be
manually moved after project creation.

## Expected Operation Sequence

After `mate.a0.jsonc` has been generated and reviewed, `mate plan` should emit
an MCO with this high-level shape:

1. `project.create`, `schdoc.create`, and `pcbdoc.create`, with a rectangular
   board outline expanded from the DUT bounds by the configured margin and an
   ANSI `D` schematic sheet.
2. `project.add_document` for the generated schematic and board.
3. Six `file.copy` operations for the SchLib/PcbLib files resolved from
   `mating_parts/` by `symbol_name` and `footprint_name`.
4. `project.add_document` for each copied SchLib/PcbLib, preserving relative
   project paths.
5. For each selected `TP*`: schematic component with a stable unique ID,
   pin-directed schematic wire, matching-orientation schematic net label on
   that wire, PCB pogo component linked back to that schematic ID, and one
   expanded source-pad reference outline using the effective source-layer pad
   shape. Symbols are grouped by symbol type on the schematic sheet, sorted in
   natural designator order inside each group, and written with centered-above
   schematic designators.
6. For each selected `M1-M4`: schematic component with a stable unique ID and
   PCB standoff component linked back to that schematic ID.
7. For each matching free NPTH alignment pad: schematic component, optional
   pin-directed schematic wire and matching-orientation net label, and PCB
   alignment-pin component.
8. `pcbdoc.add_track` operations projecting the DUT board outline onto the
   configured graphics layer, plus configured internal cutout outlines on
   `MECHANICAL_1`.
9. `pcbdoc.add_region` board-cutout operations for each detected DUT internal
   cutout when `board_projection.cutouts.actual_cutouts` is enabled.
10. `pcbdoc.arrange_designators` to move generated component-owned designator
    text above each mate component using the configured Arial 40 mil bold style.
11. `pcbdoc.export_layer_step` for the DUT bottom layer, including selected
    `TP*` component-pad copper, large drill overlays, board outline bodies,
    artifact-hashed output filenames, NPTH drill rings, pad-shaped plated drill
    overlays, and the configured red `test_points` pad color rule.
12. `pcbdoc.add_embedded_3d_model` to insert that STEP artifact into the output
    PcbDoc at the configured 8.5 mm Z height, using the DUT outline bounds for
    the body projection.
13. `pcbdoc.create_user_union` named `MATE_FEATURES` after PCB-side generation
    completes, so the group reflects the final generated board state.
14. Board-edge PCB net-label column headers and labels after the user union.
    These labels are grouped into one column per source projection/input type,
    use the same computed box width, and remain loose so they can be manually
    moved after generation.

The example uses Cricket Node's `M1-M4` mount designators directly. The old
node-test-array known-parts cache is no longer part of the public example; the
minimal libraries are checked in under `mating_parts/`.
