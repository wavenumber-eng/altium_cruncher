+++
type = "plan"
id = "altium-cruncher-gui-config-infrastructure"
status = "active"
created = "2026-07-16"

[[steps]]
id = "capture-current-state"
title = "Capture current research findings and planning context"
status = "done"

[[steps]]
id = "define-first-target-application"
title = "Define the first target application requirements"
status = "active"
depends_on = ["capture-current-state"]

[[steps]]
id = "settle-minimum-infrastructure"
title = "Settle the minimum daemon, contract, and generated-type infrastructure"
status = "pending"
depends_on = ["define-first-target-application"]

[[steps]]
id = "pilot-target-application"
title = "Implement the first target application against the shared infrastructure"
status = "pending"
depends_on = ["settle-minimum-infrastructure"]

[[steps]]
id = "promote-durable-docs"
title = "Promote stable outcomes into durable design docs, ADRs, and contracts"
status = "pending"
depends_on = ["pilot-target-application"]

[[steps]]
id = "design-doc-intent-audit"
title = "Audit design docs, ADRs, and requirements against implementation"
status = "pending"
depends_on = ["promote-durable-docs"]

[[steps]]
id = "test-runtime-impact-audit"
title = "Audit new test runtime impact"
status = "pending"
depends_on = ["pilot-target-application"]

[[steps]]
id = "external-review"
title = "Obtain independent external review"
status = "pending"
depends_on = ["design-doc-intent-audit", "test-runtime-impact-audit"]

[[exit_criteria]]
id = "signoff"
title = "Focused signoff passes"
status = "pending"

[[exit_criteria]]
id = "first-target-application-defined"
title = "The first target application requirements and acceptance criteria are defined"
status = "pending"

[[exit_criteria]]
id = "minimum-infrastructure-settled"
title = "The minimum daemon, API contract, config contract, and generated-type rules are settled"
status = "pending"

[[exit_criteria]]
id = "headless-cli-preserved"
title = "Saved GUI-edited configs can be consumed by headless CLI flows without GUI-only state"
status = "pending"

[[exit_criteria]]
id = "design-doc-intent-audit"
title = "Design docs, ADRs, and requirements match implementation"
status = "pending"

[[exit_criteria]]
id = "test-runtime-impact-audit"
title = "New tests are listed and runtime impact is reviewed"
status = "pending"

[[exit_criteria]]
id = "external-review"
title = "Independent external review is complete"
status = "pending"
+++

# Altium Cruncher GUI Config Infrastructure

## Purpose

This plan captures the current research and direction for adding a lightweight
GUI/server infrastructure to `altium-cruncher`. The immediate goal is not to
design one universal UI for every command. The goal is to establish the minimum
rules, contracts, and hygiene needed so future config editors and preview tools
can share a reliable process-level bridge to `altium-cruncher`.

The first target application is still pending. Current expectation is that the
pilot will be related to SVG or assembly documentation views, because those
configs are already complex and upcoming documentation-generator work needs an
interactive editor with live preview.

## Current Research Snapshot

### Lib Cruncher Cleaner Integration

`appz/lib_cruncher` currently performs library asset import and cleaning in
Python process, not by spawning the `altium-cruncher` CLI.

Important current behavior:

- Symbols and footprints pass through `altium-cruncher` Python package helpers
  in-process.
- Lib Cruncher still uses direct `altium_monkey` APIs for low-level loading,
  extraction, copying, and preview rendering.
- Symbol import has bespoke pre-clean selection/copy behavior before invoking
  the `altium-cruncher` schematic cleaner profile.
- Footprint import copies the selected footprint with `altium_monkey`, then
  applies the `altium-cruncher` PCBLib cleaner profile.
- The dependency is the installed `altium-cruncher` package, not necessarily the
  sibling checkout at `C:\eli\wn-hw\altium_cruncher`.

Interpretation: moving Lib Cruncher to a process-level dependency on
`altium-cruncher` requires more than invoking the existing `clean` command. The
CLI needs selected-asset, preview/report, and machine-readable inspection
surfaces that match the current in-process workflows.

### Altium Cruncher CLI Surface Gaps

The current CLI has useful config-driven commands, but it does not yet expose
all operations needed for Lib Cruncher-style process isolation or GUI preview.

Observed gaps:

- `clean` operates on whole projects/docs/libs and config files, but does not
  expose selected symbol/footprint extraction plus cleaning as a single
  daemon-friendly command.
- `clean` does not currently provide the full JSON report/check mode needed for
  future "run cleaner on existing library parts" workflows.
- `libraries --json` lists SchLib/PcbLib contents, but not extraction plans for
  SchDoc/PcbDoc/PrjPcb/IntLib.
- `extract` can extract assets, but there is no dry-run/list command that
  returns the same de-duplicated candidates that extraction would use.
- `sch-svg` and `pcb-svg` are document-oriented. They do not yet provide a
  stable selected-symbol or selected-footprint preview surface for viewer tabs.
- `pcb-svg` does not directly cover single `.PcbLib` footprint preview.

Likely CLI additions:

- read-only list/plan commands for extractable symbols and footprints;
- selected asset extract/clean/preview commands;
- JSON report modes for cleaner/check workflows;
- consistent config resolution for daemon calls;
- batch manifests for import flows that contain many assets.

### Altium Monkey API Gaps

Several pieces are better introduced in `altium_monkey` first because they are
CAD-file facts or renderer behavior, not `altium-cruncher` orchestration.

Already filed issues in `altium_monkey_dev`:

- https://github.com/wavenumber-eng/altium_monkey_dev/issues/17 -
  investigate pad-number overlay support in the PCB SVG renderer.
- https://github.com/wavenumber-eng/altium_monkey_dev/issues/18 - add
  read-only asset inspection APIs for extraction preview.
- https://github.com/wavenumber-eng/altium_monkey_dev/issues/19 - add
  read-only embedded PCB asset inventory APIs.

The extraction-preview issue should preserve the current extraction semantics:

- SchDoc extraction may have many placed components that share one logical
  symbol. Preview/list APIs need the same unique-symbol reduction as extract.
- PcbDoc extraction groups footprints by the existing extraction identity and
  suffixing behavior, not by a naive component count.
- PrjPcb and IntLib workflows need list/plan behavior that matches extraction
  behavior before any files are written.

The embedded-asset issue covers listing embedded 3D models and fonts before a
full extraction. Megamaid already extracts models at the orchestration layer,
but the inventory belongs in `altium_monkey` so both Python and C++ users can
inspect source files before committing to extraction.

### Pad Number Preview Current State

Lib Cruncher adds pad numbers as a bespoke post-processing overlay after SVG
generation.

Current implementation shape:

- footprint preview calls the `altium_monkey` PCB SVG renderer;
- Lib Cruncher reaches into renderer context data;
- Lib Cruncher injects a `<g class="lc-pad-number-overlay">` group by editing
  the generated SVG string.

Preferred direction:

- add pad-number rendering as a first-class `altium_monkey` PCB SVG renderer
  option;
- expose that option through `altium-cruncher` SVG/preview commands;
- keep Lib Cruncher as a caller of the stable renderer/CLI surface rather than
  maintaining SVG surgery.

### PR 18 As A Relevant Pressure Test

`altium_cruncher` PR 18 adds an `impedance-doc` command that is config-driven
and SVG-backed. It is a useful reference for the planned GUI infrastructure even
if it is not the first pilot.

Relevant properties:

- command creates and consumes a JSONC config;
- config has a schema id;
- output is visual documentation derived from PCB SVG rendering;
- a GUI would need source inventory, preview rendering, parameter editing, and
  save-config behavior.

This is the same pattern expected for assembly documentation views and future
highlight/annotation editors.

## Proposed Architecture Direction

### Process Boundary

Future Lib Cruncher and GUI integrations should treat `altium-cruncher` as a
process-level service or CLI, not as an imported Python implementation detail.
That leaves room for:

- keeping Lib Cruncher in Python while isolating tool behavior;
- replacing or accelerating internals with the C++ ports of `altium_monkey` and
  `altium_cruncher`;
- using the same headless commands from desktop apps, CI, and local web UIs.

### GUI Mode

Add an `altium-cruncher gui` mode that starts a local daemon and serves a web
application. The first version should be intentionally small.

Minimum expected shape:

- local-only HTTP server, likely FastAPI initially;
- static web UI served by the daemon;
- typed HTTP APIs for inspection, config loading/saving, validation, and
  rendering;
- WebSockets only when a use case needs streaming progress or interactive
  updates;
- generated OpenAPI and JSON Schema artifacts committed or checked in a
  reproducible way;
- frontend types generated from server/API/config schemas;
- no handwritten duplicate TypeScript interfaces for persisted configs or API
  payloads.

The daemon is primarily a filesystem and execution bridge. The client should
not need to know Altium file internals, temporary directory conventions, or
which `altium-cruncher` internals are used to render a preview.

### Config Files As Project Files

The edited config file is the durable artifact. The GUI is only an editing aid.

Rules to preserve:

- a config created or edited in the GUI can be rerun later from pure CLI;
- rendered outputs are reproducible from the saved config and source files;
- GUI-only state must either be absent or explicitly separated from the command
  config;
- config schema ids and versions are part of the compatibility contract;
- JSONC remains useful for humans, while strict JSON Schema remains the
  machine-checkable contract.

### Contract And Type Generation Pattern

Use the `toolz/data_models` pattern narrowly, not wholesale.

Reference discipline to copy:

- define canonical Python models or schema-backed contracts;
- emit JSON Schema/OpenAPI where appropriate;
- generate JavaScript/TypeScript interfaces from those contracts;
- keep generated files separate from handwritten editor logic;
- include a freshness check so generated contracts cannot drift from source;
- include runtime validation helpers where useful.

This should reduce bespoke JS/Python drift while still allowing editor-specific
operators and UI state to be written in TypeScript or JavaScript.

### Frontend Scope

Do not start with one universal config editor. Build shared infrastructure and
then one real editor.

Likely shared UI/server capabilities:

- open/load config;
- validate config and report schema errors;
- inspect source file capabilities and derived inventory;
- render preview from a config;
- save config;
- manage temporary working directories safely;
- expose progress/errors in a stable machine-readable format.

Likely editor-specific capabilities:

- controls mapped to one command's config model;
- domain-specific source inventory views;
- visual selection and override operations;
- preview interaction such as enabling/disabling overlays, moving virtual
  designator projections, or changing colors.

## Candidate First Target Application

The expected first target is an SVG or assembly documentation config editor.
The exact requirements are intentionally pending.

Known likely needs:

- source `.PcbDoc` or `.PrjPcb` selection;
- board/layer/view inventory from source files;
- preview render using the same config consumed by CLI;
- config editing for assembly views and visual overlays;
- future interactions for virtual designator projections:
  - selectively enable or disable items;
  - reposition projected labels;
  - adjust colors and style;
  - persist those edits into the config;
- save JSONC config for later headless generation.

Potential adjacent pilots:

- cleaner preview/check UI for symbols and footprints;
- selected symbol/footprint viewer with cleaner controls;
- impedance/net-class highlight documentation editor based on PR 18.

## Open Design Questions

- What exact command/config should be the first pilot?
- Should `gui` be a single command with app routes, or should each tool command
  expose a `--gui` or `preview` subcommand that starts the same daemon?
- Which contracts are Python-model-first and which are JSON-Schema-first?
- How much generated frontend code should be committed versus generated during
  development?
- What is the first stable API version prefix, for example `/api/acr/v0`?
- What authentication or local token policy is required for localhost use?
- Which file operations are allowed from the daemon, and how are project roots
  constrained?
- Which preview jobs need WebSockets or cancellation in the first slice?
- How should temporary extraction folders be named, retained, and cleaned?

## Minimum First Slice Proposal

The first implementation slice should only establish infrastructure needed by
the selected pilot.

Candidate minimum:

1. `altium-cruncher gui` starts a localhost server and serves a minimal page.
2. `/health` reports version, process id, and available feature flags.
3. `/api/acr/v0/config-kinds` lists supported config editors.
4. One pilot config kind exposes:
   - schema metadata;
   - load/validate/save endpoints;
   - source inspection endpoint;
   - render-preview endpoint.
5. OpenAPI and config schema artifacts are generated or checked for freshness.
6. Frontend TypeScript types are generated from contracts.
7. Tests cover contract freshness, schema validation, and one preview request at
   a unit or integration level.

Non-goals for the first slice:

- universal config editing UI;
- multi-user server;
- remote deployment;
- complex job queue unless the pilot requires it;
- replacing existing CLI commands.

## Documentation And Signoff Expectations

When this moves beyond planning, durable outcomes should be promoted according
to the repository documentation lifecycle:

- architecture decisions to `docs/adrs/`;
- public command behavior to `docs/design/cli/`;
- public API/interface behavior to `docs/design/api/`;
- schemas and generated contract artifacts to `docs/contracts/`;
- tests into the appropriate Rack strata and L99 signoff checks.

This plan should remain working material only. Completed decisions and stable
contracts must not remain trapped here.
