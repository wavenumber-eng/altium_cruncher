# Contracts

This folder stores schemas, examples, and contract fixtures for stable public
JSON outputs and configuration formats.

Contract artifacts should be paired with conformance tests before the related
public interface is considered release-ready.

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
- `schdoc_create_config.a0.schema.json`: standalone SchDoc create config schema.
- `pcbdoc_create_config.a0.schema.json`: standalone PcbDoc create config schema.
- `pcb_layer_step_config.a0.schema.json`: fixture-alignment PCB layer STEP
  config schema.
- `pcb_svg_config.a0.schema.json`: experimental explicit PCB SVG config schema.
- `project_skeleton_config.a0.schema.json`: JSONC PrjPcb skeleton creation
  config schema.
