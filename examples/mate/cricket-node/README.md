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
