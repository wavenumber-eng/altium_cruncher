# Architecture and Rust port map

Reviewed 2026-09-12 against the standalone Python checkout. This describes
observable behavior and ownership for an ACR clone over the Altium Monkey Rust
port. It is not a request to reproduce Python's module layout or private APIs.

## Contracts and entry points

`acr`, `altium-cruncher` and `python -m altium_cruncher` converge on `_cli.main`.
`build_parser()` constructs the complete command tree without executing work.
`cli_commands.COMMAND_MODULES` preserves registration order; each command module
owns its aliases, nested actions and `handler`. The root parser owns version/help,
logging, unknown-argument errors (exit 2) and final handler exit status. Normal
progress goes through logging; JSON stdout and diagnostic stderr must stay separate.
Creation commands use `mco_cli_support` to keep incidental native stdout away from
machine-readable results. Do not homogenize command-specific failure/partial-success
policies during a port: follow the command handler and its tests.

TypeSpec under `src/tsp/altium_cruncher/{config,mco,outputs}` is the source for all
45 Cruncher-owned JSON/JSONC roots. Generated schemas, Python DTOs and TypeScript
codecs are derived artifacts. `contracts/` adapters separate authored input from
resolved domain defaults. Omission, null, extension fields and compatibility
coercions can be observable; a Rust deserializer that fills every default eagerly
would change behavior. MCO execution validates the envelope first, then reached
built-in operands; custom registry entries and skipped operations retain their
existing semantics. Native Monkey/Geometer payloads are upstream contracts.

Use [public-contract-authority.md](public-contract-authority.md) for the complete
root inventory, generator, browser vectors and owner boundaries. Do not infer an
implementation from the mere presence of a future-facing configuration field.

## Every command and its workflow boundary

All module names below are under `src/py/altium_cruncher`. Test paths are relative
to `tests`. Read the [command guide](command-inventory.md) and matching CLI HTML
for exact arguments/defaults; this table records where the behavior is owned.

| Command | Workflow modules | Input, dispatch and output behavior | Upstream boundary | Behavior evidence |
| --- | --- | --- | --- | --- |
| `bom` | bom_artifacts.py; bom_pnp_model.py | SchDoc/PrjPcb or detected project; variants, DNP and source policy before grouping; output snapshot and tables | Monkey supplies design/BOM records; Cruncher owns column selection, ordering and filenames | test_bom_outputs.py; test_bom_pnp_model.py |
| `clean` | altium_clean.py; altium_pcblib_clean.py | Explicit config init or cleanup; project fans out to SchDocs; preserve output and backup policy | Monkey parses and saves; Cruncher selects normalization/removal rules | test_schlib_clean_order.py; test_pcblib_clean_config.py |
| `design` | altium_cruncher_design_review.py | Document/project selection, review manifest, HTML/SVG/JSON and cross-artifact links | Monkey owns compiled schematic graph and native document payloads | test_notes_and_design_review.py |
| `easyeda-import` | easyeda_altium_symbol.py; easyeda_altium_footprint.py | Supplier/component identifier, download policy, library/artifact paths; model placement enabled by default when available | EasyEDA Monkey owns retrieval/source data; Altium Monkey owns library authoring | test_easyeda_import_schematic.py; test_easyeda_import_footprint.py |
| `extract` | altium_cruncher_cmd_extract.py | SchDoc/PcbDoc/PrjPcb and IntLib selection; naming and output fanout | Monkey owns extraction and library serialization | L3_public_workflows/test_L3_001_public_cli_workflows.py |
| `installs` | altium_cruncher_cmd_installs.py | Display paths found through environment, Program Files and registry | Windows installation discovery; no CAD document writes | L0_public_cli/test_L0_001_cli_entrypoint.py |
| `jlc` | bom_artifacts.py; pnp_artifacts.py | Reuse shared BOM/PnP source, variant, normalization and XLSX writers | Same Monkey boundaries as bom/pnp | L3_public_workflows/test_L3_004_bom_pnp_oracle_workflows.py |
| `json-dump` | altium_cruncher_json_dump.py | SchDoc/SchLib/PcbDoc/PcbLib; flat or by-kind output layout | Cruncher owns wrapper/layout; Monkey owns parsed record payloads | L3_public_workflows/test_L3_001_public_cli_workflows.py |
| `launch` | altium_cruncher_cmd_launch.py | Select installation, optional document, process flags and exit status | Windows process launch; separate from CAD parsing | L0_public_cli/test_L0_001_cli_entrypoint.py; support_scripts/install_test.py |
| `libraries` | altium_cruncher_mate_libraries.py; altium_cruncher_cmd_libraries.py | Scan SchLib/PcbLib files or directory roots (CWD by default), with optional recursion | Monkey owns library/project interpretation | L0_public_cli/test_L0_001_cli_entrypoint.py |
| `mate` | altium_cruncher_mate.py; mate_config_fields.py; altium_cruncher_mate_*.py | init, plan, libs, inspect, seed, parts-cache build, run; planning artifacts precede MCO execution | Cruncher owns mating geometry/policy and plans; Monkey authors CAD; Geometer supplies geometry operations | test_mate.py |
| `mco` | altium_cruncher_mco.py; altium_cruncher_mco_cad_ops.py; mco_cli_support.py | run, init, list, list-ops; preserve dry-run, operation ordering, partial results and custom registry dispatch | Cruncher owns envelope/registry/results; Monkey performs CAD operations | test_mco.py; test_mco_contract.py |
| `megamaid` | altium_cruncher_cmd_megamaid.py; bom_artifacts.py; pnp_artifacts.py | Libraries, netlist, notes, parsed JSON, assets and manifest; remove only owned stale outputs | Monkey supplies parsed/extracted data; Cruncher owns bundle layout and manifest | L3_public_workflows/test_L3_003_megamaid_workflow.py |
| `merge` | altium_cruncher_cmd_merge.py | Input discovery, conflict policy, output filename and reporting | Monkey owns merged library content and serialization | L3_public_workflows/test_L3_001_public_cli_workflows.py |
| `notes` | altium_cruncher_notes.py | Document/project selection; typed text/note records and output paths | Monkey supplies schematic records; Cruncher classifies notes and builds its envelope | test_notes_and_design_review.py |
| `outjob` | altium_cruncher_cmd_outjob.py | run or implicit run; project/job selection, temporary normalization and result reporting | Monkey OutJob runner and installed Altium perform export; Windows only | L0_public_cli/test_L0_001_cli_entrypoint.py |
| `pcb-layer-step` | altium_cruncher_pcb_layer_step.py; pcb_layer_step_options.py | Config resolves immutable options; collect board/copper/hole geometry, emit STEP and manifest | Monkey supplies PCB geometry; Geometer owns STEP/boolean operations | test_pcb_layer_step.py |
| `pcb-svg` | altium_cruncher_pcb_svg_renderer.py; pcb_svg_render_job.py; pcb_svg_artifacts.py | Project/board context; per-layer outputs and explicit views; durable SVG group updates | Monkey owns primitives/text; Cruncher owns composition, virtual layers, styles and caches; Geometer owns projection | test_pcb_svg_view_selection.py; test_pcb_svg_render_job.py |
| `pcbdoc` | project_creation.py; altium_cruncher_cmd_pcbdoc.py | create; config/CLI to pcbdoc.create, stack/mechanical profile, overwrite/dry-run policy | Monkey builds and saves the document | test_document_create_commands.py |
| `pcblib` | altium_cruncher_cmd_pcblib.py | create; initial footprint identity and output policy | Monkey builds and saves the library | test_document_create_commands.py |
| `pnp` | pnp_artifacts.py; bom_pnp_model.py | PrjPcb selection (other input suffixes rejected), coordinates/units, variant/no-BOM filters, sorting and output snapshot | Monkey supplies placements; Cruncher owns normalization and artifact formats | test_pnp_outputs.py; test_bom_pnp_model.py |
| `prjpcb` | project_creation.py; altium_cruncher_cmd_prjpcb.py | Implicit creation, create, init, add-sheet; compile config to ordered document/parameter/link MCO operations | Monkey mutates/saves documents; Cruncher owns source-relative paths and compilation | test_document_create_commands.py |
| `profiles` | altium_cruncher_cmd_profiles.py | list, clean; explicit profile targeting and dry-run; filesystem side effects | Windows ProgramData/profile state, independent of geometry | L0_public_cli/test_L0_001_cli_entrypoint.py |
| `sch-ir` | altium_cruncher_cmd_sch_ir.py; schematic_diagnostics.py | SchDoc/PrjPcb/project-directory; onscreen IR profile, naming and font diagnostics | Monkey owns gotIR and schematic interpretation | L3_public_workflows/test_L3_001_public_cli_workflows.py |
| `sch-svg` | altium_cruncher_cmd_sch_svg.py; schematic_diagnostics.py | Resolve physical/compiled pages, SVG outputs, enrichment and font diagnostics | Monkey owns compiled schematic rendering; Cruncher owns workflow/layout | L3_public_workflows/test_L3_001_public_cli_workflows.py |
| `schdoc` | altium_cruncher_cmd_schdoc.py | create; blank/template/custom sheet policy and output path | Monkey authors/saves SchDoc | test_document_create_commands.py |
| `schlib` | altium_cruncher_cmd_schlib.py | create; library and initial empty symbol operations | Monkey authors/saves SchLib | test_document_create_commands.py |
| `split` | altium_cruncher_cmd_split.py | SchLib/PcbLib discovery; filesystem-safe names while preserving internal names | Monkey owns library split/serialization | L3_public_workflows/test_L3_001_public_cli_workflows.py |
| `svg` | altium_cruncher_cmd_svg.py | Select schematic and PCB work, forwarding existing options and output policy | Delegates to sch-svg/pcb-svg workflows | L3_public_workflows/test_L3_001_public_cli_workflows.py |
| `toon` | pcb_illustration_workflow.py; pcb_illustration_config.py; pcb_svg_render_job.py | Auto-create toon.config; apply explicit choices; base/named/all variants; progress and timings; SVG only | Uses the same compositor as pcb-svg, plus Geometer models/illustration | test_toon_cli.py; L3_public_workflows/test_L3_005_pcb_illustration.py |
| `variants` | altium_cruncher_prjpcb_variants.py; altium_cruncher_cmd_variants.py | list, delete, rename, clone, toggle-dnp; preserve operation/result and write policies | Monkey owns project variant storage; Cruncher dispatches MCO changes | L0_public_cli/test_L0_003_variants_cli.py |
| `version` | _version.py | version and --version; root help also includes version | Package metadata, no CAD/native operation | L0_public_cli/test_L0_001_cli_entrypoint.py |

## PCB illustration pipeline

1. `pcb_illustration_config` overlays authored SVG settings on the generated Toon
   preset, then applies explicit CLI side/theme/assembly/board choices. First-run
   config writing belongs to the command adapter; rendering lives in
   `pcb_illustration_workflow`.
2. `altium_cruncher_pcb_workflow` loads project context, selected board documents
   and special-string parameters. Toon skips schematic parsing while retaining
   project parameters and variants. Standalone boards can discover sibling
   projects or receive pseudo-project context; `project_context=none` bypasses it.
3. `pcb_illustration_variants` creates population/parameter overlays without
   changing saved geometry or component indices. It rejects unsupported alternate
   models and output-folder collisions before rendering. Only the intersection
   of selected variants' DNP sets can be omitted from shared materialization.
4. `PcbSvgRenderJob` owns source aliases, scoped cutouts, layer-stack/context facts,
   primitive indexes, finished SVG fragments, component sessions, workers and
   timings. A geometry edit requires a fresh source/job. Parameter-only copies
   retain a source identity but get fresh parameter lookup in render contexts.
5. `IllustrationJob` resolves embedded STEP bodies and Altium extrusions. Altium
   extrusion upper elevation is MAXZ/overall height, not an extra thickness above
   standoff. Body color, opacity, relative pose and depth remain per body. Bodies
   belonging to a component stay separate meshes; there is no body union.
6. Unique STEP tessellation and posed component requests can use bounded native
   workers. All mutable result maps and diagnostics commit in source order.
   Failed/omitted bodies are retryable; partial native results keep warnings.
   Fast HLR detail plus Fast mesh shadow supply the lines, and Geometer's own
   fused-color illustration output supplies the painted surfaces.
7. `ComponentLayerSession` composes shared SVG symbols and source metadata,
   orders top surfaces by high Z and bottom surfaces by low Z, then filters each
   population. Model-less components get no invented illustration. Assembly
   labels use model outlines. Ordinary designator-only PCB SVG views can use an
   electrical-pad envelope, with locating-hole fallback if no eligible pads
   exist; a view co-composed with component illustration, including Toon, omits
   the model-less projected label. An unavailable attached model never silently
   becomes a pad-derived model.
8. The designator fitter retains autodoc's sizing/rotation/clearance rules.
   Coordinates for fitting use source Y-down millimeters; bottom-view text is
   counter-reflected for readability. Label style and SVG emission are separate
   from geometry selection and fitting. Preserve J1's electrical-pad centering.
9. The PCB SVG compositor prepares component bounds, constructs the SVG viewBox, then
   commits physical and virtual layers in the established order. Film subtracts
   authored mask primitives/text, custom pad openings, extended primitive mask
   expansions and cutouts from the board domain. NPTH bores remain open; tenting,
   filled/capped vias and outer-side selection keep their existing policies.
10. `pcb_svg_artifacts` owns durable generated-group replacement for generic SVG
    updates, including refreshing the generated scene reflection when mirroring
    or canvas width changes. Preserve user scene attributes and siblings; page
    annotations outside the scene stay in page coordinates. Toon writes its
    complete view and adds variant metadata. SVG group
    IDs, enrichment, source indices, units and file templates are public behavior.
    PNG rasterization is outside the runtime package.

## Cache and resource invariants

Keep board-scoped caches separate from persistent native model/artwork caches.
The disk cache is positive-only, checksummed JSON under a versioned identity
covering native binaries, dependencies and adapter policy source. Corrupt entries
are warnings/misses, including malformed geometry, scale and index arrays. Writes
are atomic; size-based eviction only touches owned entries. When moving native
policy to additional modules, extend `native_cache_identity()` accordingly.

An early component-artwork hit must cover every eligible authored body for that
owner. Warning provenance is part of reuse safety. Shape appearance can be shared
between instances; instance-specific warnings cannot be rebound to a different
producer. Preserve signed zero and exact pose/style key material. Do not round
keys, cache failures, union bodies or drop diagnostic ordering to improve speed.

Worker threads own their clients. Cleanup cancels queued work, drains running
requests with native timeouts, and closes clients. Timing parents include child
work; exclusive time subtracts measured children. Parallel request durations
overlap and cannot be summed as board wall time. Progress/timing output must not
change SVG metadata or deterministic rendering.

## Current seams a Rust clone should replace

Shared BOM/PnP writers now live below their CLI handlers. Project creation config
compilation is in `project_creation.py`; creation commands consume MCO rather than
calling another command's compiler. Font diagnostics and MCO terminal reporting
also have shared modules. Older Python import paths re-export moved helpers for
compatibility; the new service modules own them.

Some older orchestration remains in command modules: `svg` forwards namespaces to
its two exporters, Mate delegates optional launch, and MegaMaid/Clean still combine
several artifact/cleanup families. These are explicit dispatch seams in the table,
not reasons to copy a Namespace into a Rust domain API. Port using typed requests
and results while preserving the same order, paths, failure policy and reports.

Cruncher still calls protected Monkey helpers for primitive rendering, body
placement and owner-preserving schematic ordering. In particular, schematic body
rectangle reordering currently uses the underlying owned collection because the
public query collection is read-only; remove/add would detach identities. The Rust
port needs equivalent ownership operations, not Python private member names.

## Validation for the clone

Start with TypeSpec codecs and shared conformance vectors, then MCO ordering and
creation fixtures, then individual exporters. Use RT Super C1 first for STEP plus
extruded bodies, opposite-side body ownership, J1 without a model and variants.
Use Hydroscope for custom mask pads, and the larger corpus for geometry/cache
stress. Keep native rendering tests distinct from CLI/help and serializer tests.

Current Python entry points for evidence are `uv run --extra test rack run --all`,
the focused tests in the table, TypeSpec freshness/browser/Python checks, and the
package build/Twine/installed-console gates documented in [build.md](../build.md).
`tests/support_scripts/profile_pcb_svg.py` attributes synchronous work and verifies
repeat-view byte equality; `profile_svg_workers.py` measures whole-board parallel
runs. Neither script is a runtime API. `pcb_board_review.py` builds visual review
pages for all populations without introducing another production renderer.
