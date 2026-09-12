# Current command capabilities

Reviewed 2026-09-12. This is the standalone public package, not the stale monorepo
copy. The [command manifest](../contracts/command_manifest.a0.json) owns public
status and command documentation links. Parser registration is centralized in
`src/py/altium_cruncher/cli_commands.py`; `version` is registered by `_cli.py`.

See the [architecture and Rust port map](architecture-porting-guide.md) for
workflow boundaries, native dependencies, compatibility rules and test ownership.

| Command | Capability |
| --- | --- |
| [`bom`](cli/bom.html) | BOM normalization and CSV/JSON/XLSX output. |
| [`clean`](cli/clean.html) | Config-driven schematic/library cleanup. |
| [`design`](cli/design.html) | Design-review bundle (aliases: design-review, dr). |
| [`easyeda-import`](cli/easyeda-import.html) | EasyEDA symbol, footprint and 3D import. |
| [`extract`](cli/extract.html) | Extract document and library assets. |
| [`installs`](cli/installs.html) | Discover Altium installations. |
| [`jlc`](cli/jlc.html) | JLC BOM and CPL bundle. |
| [`json-dump`](cli/json-dump.html) | Parsed document/library inspection JSON. |
| [`launch`](cli/launch.html) | Launch installed Altium (ad shortcut). |
| [`libraries`](cli/libraries.html) | Scan symbol/footprint libraries. |
| [`mate`](cli/mate.html) | Mating-board planning and generation. |
| [`mco`](cli/mco.html) | Ordered change-order execution. |
| [`megamaid`](cli/megamaid.html) | Project decomposition bundle. |
| [`merge`](cli/merge.html) | Merge SchLib/PcbLib files. |
| [`notes`](cli/notes.html) | Extract schematic note content. |
| [`outjob`](cli/outjob.html) | Run Altium output jobs. |
| [`pcb-layer-step`](cli/pcb-layer-step.html) | Generate a layer alignment STEP model. |
| [`pcb-svg`](cli/pcb-svg.html) | Configurable physical/virtual SVG compositor. |
| [`pcbdoc`](cli/pcbdoc.html) | Create a PCB through MCO. |
| [`pcblib`](cli/pcblib.html) | Create a footprint library through MCO. |
| [`pnp`](cli/pnp.html) | Placement CSV/JSON/XLSX/CPL output. |
| [`prjpcb`](cli/prjpcb.html) | Create/init projects and add sheets. |
| [`profiles`](cli/profiles.html) | Inspect/clean Altium profile state. |
| [`sch-ir`](cli/sch-ir.html) | Export schematic gotIR. |
| [`sch-svg`](cli/sch-svg.html) | Export schematic SVG. |
| [`schdoc`](cli/schdoc.html) | Create a schematic through MCO. |
| [`schlib`](cli/schlib.html) | Create a symbol library through MCO. |
| [`split`](cli/split.html) | Split libraries into individual entries. |
| [`svg`](cli/svg.html) | Combined schematic/PCB export wrapper. |
| [`toon`](cli/toon.html) | Top/bottom illustrated PCB SVG presets. |
| [`variants`](cli/variants.html) | Inspect and mutate project variants. |
| [`version`](cli/version.html) | Report package and controlled dependency versions. |

`design-review` and `dr` alias `design`. `ad` is the launch console shortcut.
The EasyEDA review modules are development helpers, intentionally unregistered.
Command-specific guides and `--help` describe arguments and defaults; output
policies differ between exports, document creation, environment tools and mutation.

Toon and PCB SVG share substrate, solder-mask film, illustration, designator,
cutout and drill/slot virtual layers. Fast HLR detail and Fast mesh shadow are the
default projection paths. Assembly labels honor `show_designator=false`; project
variants omit DNP bodies/labels and apply parameter overrides. Alternative-part
model substitutions remain unsupported. Diode line art/cathode overlays and the
older general DNP styling config are not implemented merely because fields exist.

All Cruncher-owned JSON roots now have TypeSpec authority; native Monkey/Geometer
payloads retain their upstream owners. See [contract authority](public-contract-authority.md).
Release gates enforce command/help/docs coverage, contract consistency, Python
hygiene and package build/install behavior. Existing baseline allowances remain
visible; a clean incremental gate does not imply every legacy module is small.
