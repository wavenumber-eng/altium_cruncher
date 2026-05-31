# Cricket Node Debug-Plate Example

This example is a runnable workspace for the first cricket-node debug-plate
workflow: use a node-test-array known-parts cache, select cricket-node DUT
features, emit an MCO, then run it to create a new fixture/debug-plate project
and bottom-layer STEP alignment artifact.

The actual Altium source projects and extracted SchLib/PcbLib cache files are
not committed here. Stage them locally under `input/` and `known-parts/` before
running the workflow.

## Inputs

- `debug-plate.mate.a0.jsonc` is the primary selector/projection config for
  this example. It selects `TP1-27`, `M1-4`, matching free NPTH alignment pads,
  reference graphics, labels, a user union, and the bottom-layer STEP artifact.
- `debug-plate.jsonc` is the older reviewed config shape kept for comparison.
- `known-parts/debug-plate-known-parts.json` records the node-test-array cache
  layout expected by the config.
- `input/` is the ignored local staging area for cricket-node and
  node-test-array source projects.
- `output/` is the ignored generated output area.

## Commands

Run commands from this folder. To use the working-tree package instead of an
installed `altium-cruncher`, prefix commands with
`uv run python -m altium_cruncher`.

Stage local corpus inputs, if `WN_TEST_CORPUS` points at your real local corpus
mirror:

```powershell
New-Item -ItemType Directory -Force input\cricket-node, input\node-test-array
Copy-Item "$env:WN_TEST_CORPUS\altium\common\real_world_pcbdoc\cricket-node\input\*" input\cricket-node\ -Recurse -Force
Copy-Item "$env:WN_TEST_CORPUS\altium\common\real_world_pcbdoc\node_test_array\input\*" input\node-test-array\ -Recurse -Force
```

Build or refresh the known-parts cache from node-test-array:

```powershell
uv run python -m altium_cruncher debug-plate parts-cache build input\node-test-array\11-10077__node-test-array__B4.PrjPcb `
  --cache-dir known-parts `
  --force
```

Plan the mate workflow:

```powershell
uv run python -m altium_cruncher debug-plate plan debug-plate.mate.a0.jsonc `
  --output-mco debug-plate.mate.a0.mco.jsonc `
  --force
```

Run the mate workflow and keep an emitted MCO copy under `output/`:

```powershell
uv run python -m altium_cruncher debug-plate run debug-plate.mate.a0.jsonc `
  --emit-mco output\debug-plate.mate.a0.mco.jsonc `
  --force
```

You can also execute the root-level MCO directly:

```powershell
uv run python -m altium_cruncher mco run debug-plate.mate.a0.mco.jsonc
```

Open the generated project in Altium:

```powershell
output\cricket-node-debug-plate\cricket_node_debug_plate.PrjPcb
```

Inspect the STEP artifact at:

```text
output\cricket-node-debug-plate\artifacts\pcb-layer-step\cricket_node_hw__b__bottom.step
```
