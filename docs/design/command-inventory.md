# Command Inventory

Status: initial migration inventory
Last updated: 2026-05-26

This inventory records the command set migrated from the private
`toolz/altium_cruncher` package into the standalone public repo.

| Command | Initial status | Public test coverage | Notes |
| --- | --- | --- | --- |
| `version` | public | `L0_public_cli` | Package/CLI version reporting. |
| `sch-svg` | public | `L3_public_workflows` | Schematic SVG export. |
| `pcb-svg` | public | `L3_public_workflows` | PCB SVG export and board-view generation. |
| `pcb-layer-step` | public | unit/synthetic | Layer-to-STEP export using `wn-geometer`; Hydroscope CLI output is too large for the default fast lane. |
| `svg` | public | help only | Combined schematic/project SVG wrapper. |
| `pcblib-footprint-3d` | public | help only | Footprint 3D preview helper; needs a curated redistributable PcbLib+STEP fixture. |
| `bom` | public | `L3_public_workflows` | BOM CSV/JSON/XLSX output. |
| `pnp` | public | `L3_public_workflows` | Pick-and-place output. |
| `netlist` | public | `L3_public_workflows` | Netlist JSON output. |
| `extract` | public | `L3_public_workflows` | SchDoc/PcbDoc extraction workflows. |
| `easyeda-import` | optional-public | placeholder plus extra lane | Requires `altium-cruncher[easyeda]` or side-installed `easyeda-monkey`. |
| `easyeda-review` | optional-public | placeholder plus extra lane | Requires `altium-cruncher[easyeda]` or side-installed `easyeda-monkey`. |
| `easyeda-footprint-review` | optional-public | placeholder plus extra lane | Requires `altium-cruncher[easyeda]` or side-installed `easyeda-monkey`. |
| `split` | public | `L3_public_workflows` | SchLib/PcbLib split workflows. |
| `merge` | public | `L3_public_workflows` | SchLib/PcbLib merge workflows. |
| `megamaid` | public | pytest | Project decomposition workflow, including Hydroscope embedded images/models. |
| `clean` | public | `L3_public_workflows` | SchDoc/SchLib/PcbLib cleanup workflows. |

The command manifest lives at `contracts/command_manifest.v0.json`. `L99` should
eventually enforce that every manifest command has help, docs, and behavioral
test ownership.
