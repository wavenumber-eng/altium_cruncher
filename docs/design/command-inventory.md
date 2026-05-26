# Command Inventory

Status: initial migration inventory
Last updated: 2026-05-25

This inventory records the command set migrated from the private
`toolz/altium_cruncher` package into the standalone public repo.

| Command | Initial status | Notes |
| --- | --- | --- |
| `version` | public | Package/CLI version reporting. |
| `sch-svg` | public | Schematic SVG export. |
| `pcb-svg` | public | PCB SVG export and board-view generation. |
| `pcb-layer-step` | public | Layer-to-STEP export using `wn-geometer`. |
| `svg` | public | Combined schematic/project SVG wrapper. |
| `pcblib-footprint-3d` | public | Footprint 3D preview helper. |
| `bom` | public | BOM CSV/JSON/XLSX output. |
| `pnp` | public | Pick-and-place output. |
| `netlist` | public | Netlist JSON output. |
| `extract` | public | SchDoc/PcbDoc extraction workflows. |
| `easyeda-import` | planned-public | Requires `easyeda-monkey`; optional extra until that package is public. |
| `easyeda-review` | planned-public | Requires `easyeda-monkey`; optional extra until that package is public. |
| `easyeda-footprint-review` | planned-public | Requires `easyeda-monkey`; optional extra until that package is public. |
| `split` | public | SchLib/PcbLib split workflows. |
| `merge` | public | SchLib/PcbLib merge workflows. |
| `megamaid` | public | Project decomposition workflow. |
| `clean` | public | SchDoc/SchLib/PcbLib cleanup workflows. |

The command manifest lives at `contracts/command_manifest.v0.json`. `L99` should
eventually enforce that every manifest command has help, docs, and behavioral
test ownership.
