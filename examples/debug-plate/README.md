# Debug-Plate Examples

Debug-plate examples are arranged as runnable workspaces. Open an example
folder, stage the local Altium inputs described by its README, then run the
working-tree `altium_cruncher` command from that folder with:

```powershell
uv run python -m altium_cruncher ...
```

Current examples:

- `cricket-node/` - first mate/debug-plate workflow using cricket-node as the
  DUT and node-test-array as the source for known mate parts.
