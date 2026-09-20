# Contracts

This folder stores schemas, examples, and contract fixtures for stable public
JSON outputs and configuration formats.

Contract artifacts should be paired with conformance tests before the related
public interface is considered release-ready.

All Cruncher-owned public JSON/JSONC configs and output contracts are authored in
`src/tsp/altium_cruncher`. Every `*.schema.json` here is generated; use
`npm run generate:contracts`, not hand edits.
See the [authoring/consumer guide](../design/pcb-svg-config-authority.md) for
Python/browser codecs, partial-config semantics and the numeric-string validator
extension, and the [creation guide](../design/creation-config-authority.md) for
shared document sections and MCO semantics. The complete
[authority inventory](../design/public-contract-authority.md) covers every root,
producer, consumer and upstream exception. MCO operation models and containers are generated
from `src/tsp/altium_cruncher/mco`; see the
[MCO contract guide](../design/mco-contract-authority.md).

Current contracts:

- `command_manifest.a0.json`: public CLI command inventory.
- `interface_design_manifest.a0.json`: major non-dataclass interface inventory.
- `design_review_manifest.b0.schema.json`: breaking Design b0 review-bundle
  artifact manifest with canonical page-occurrence references.
- `megamaid_manifest.b0.schema.json`: MegaMaid artifact manifest, including
  the authoritative Design b0 graph output and graph-count summary.
- `schematic_svg_enrichment.b0.schema.json`: embedded metadata for compiled
  SchDoc/PrjPcb schematic SVGs linked to the Design b0 graph.
- `schematic_svg_manifest.b0.schema.json`: self-contained SchDoc/PrjPcb
  `sch-svg` bundle manifest pointing to Design b0 and graph-scoped SVG pages.
- `bom_pnp_config.a0.schema.json`: shared BOM, PnP, and JLC config schema.
- `clean_config.a0.schema.json`: shared schematic, schematic-library, and
  PCB-library clean config schema.
- `mate_config.a0.schema.json`: mating-board workflow config schema.
- `mco_input.a0.schema.json`: authored MCO document/raw-array contract with
  operation-specific built-in arguments and custom-registry extension names.
- `mco_envelope.a0.schema.json`: execution container/operation fields; argument
  checking is deferred so failure branches and custom handlers retain control.
- `schdoc_create_config.a0.schema.json`: standalone SchDoc create config schema.
- `pcbdoc_create_config.a0.schema.json`: standalone PcbDoc create config schema.
- `pcb_layer_step_config.a0.schema.json`: fixture-alignment PCB layer STEP
  config schema.
- `pcb_svg_config.a1.schema.json`: current additive PCB SVG/Toon config schema,
  including regional surface appearance, bend lines and silkscreen clipping.
- `pcb_svg_config.a0.schema.json`: accepted additive predecessor retained at its
  durable public path for existing configs.
- `pcb_svg_component_layers.a0.schema.json`: illustrated component metadata.
- `pcb_svg_timings.a0.schema.json`: per-job/layer/view/variant timing reports.
- `toon_warning_report.a0.schema.json`: deterministic grouped nonfatal Toon
  diagnostics and their structured occurrences.
- `project_skeleton_config.a0.schema.json`: JSONC PrjPcb skeleton creation
  config schema.
