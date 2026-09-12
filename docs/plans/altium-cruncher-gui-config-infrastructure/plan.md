+++
type = "plan"
id = "altium-cruncher-gui-config-infrastructure"
status = "pending"
created = "2026-07-16"

[[steps]]
id = "capture-current-state"
title = "Record the revised browser/server direction and current reference work"
status = "done"

[[steps]]
id = "define-first-target-application"
title = "Confirm the first viewer and inspect reusable Viz and Lib Cruncher boundaries"
status = "pending"
depends_on = ["capture-current-state"]

[[steps]]
id = "settle-minimum-infrastructure"
title = "Agree contract ownership, frontend rules, hosting and asynchronous operation behavior"
status = "pending"
depends_on = ["define-first-target-application"]

[[steps]]
id = "plan-external-review"
title = "Review the concrete execution plan before implementation"
status = "pending"
depends_on = ["settle-minimum-infrastructure"]

[[steps]]
id = "api-contract-authority"
title = "Author the first TypeSpec service contract and generate shared language artifacts"
status = "pending"
depends_on = ["plan-external-review"]

[[steps]]
id = "pilot-target-application"
title = "Implement one browser workflow through the governed server boundary"
status = "pending"
depends_on = ["api-contract-authority"]

[[steps]]
id = "promote-durable-docs"
title = "Promote accepted architecture, protocol and workflow behavior into public documentation"
status = "pending"
depends_on = ["pilot-target-application"]

[[steps]]
id = "design-doc-intent-audit"
title = "Audit design docs, ADRs and contracts against the implemented first slice"
status = "pending"
depends_on = ["promote-durable-docs"]

[[steps]]
id = "test-runtime-impact-audit"
title = "Review conformance and workflow coverage and its runtime cost"
status = "pending"
depends_on = ["pilot-target-application"]

[[steps]]
id = "external-review"
title = "Obtain independent implementation and boundary review"
status = "pending"
depends_on = ["design-doc-intent-audit", "test-runtime-impact-audit"]

[[exit_criteria]]
id = "first-target-application-defined"
title = "The selected first workflow and its reusable renderer boundary are explicit"
status = "pending"

[[exit_criteria]]
id = "minimum-infrastructure-settled"
title = "Frontend, transport, domain and local-effect ownership are documented"
status = "pending"

[[exit_criteria]]
id = "backend-neutral-contract"
title = "API generation and shared vectors establish a Python/Rust-independent frontend boundary"
status = "pending"

[[exit_criteria]]
id = "headless-cli-preserved"
title = "Server and CLI share workflow behavior and saved configs remain usable headlessly"
status = "pending"

[[exit_criteria]]
id = "signoff"
title = "The installed first workflow and its focused contract and behavior checks pass"
status = "pending"

[[exit_criteria]]
id = "design-doc-intent-audit"
title = "Public documentation matches accepted and implemented behavior"
status = "pending"

[[exit_criteria]]
id = "test-runtime-impact-audit"
title = "Test coverage and runtime impact have been reviewed"
status = "pending"

[[exit_criteria]]
id = "external-review"
title = "Independent review has no unresolved material findings"
status = "pending"
+++

# ACR browser tools and server boundary

Rewritten 2026-09-12 after the Toon, TypeSpec and cleanup work.
**Parked for a later discussion.** This records direction and candidate scope;
it does not authorize starting server or frontend implementation. Reconfirm the
open choices and inspect the in-flight references before execution.

## Objective

Build web tools that let users view designs, edit complex configurations and see
results without manually rerunning CLI commands. Establish clear rules for how
frontend code, APIs, server adapters and workflow implementations fit together.
The first feature should be small enough to prove these rules with a useful GUI.

The frontend should remain unchanged when the Python backend is replaced by
Rust. ACR is expected eventually to move inside the Altium Monkey repository;
repository layout must not become part of the browser protocol.

## Agreed direction

- Use a clean TypeScript frontend and Lit for reusable web components, following
  the direction of Lib Cruncher's frontend modernization.
- Separate components, feature state/actions and API access. Centralize transport
  behavior so feature code does not scatter route strings, raw requests or
  backend-specific handling throughout the UI.
- Use HTTP as the application interface. Consider a standardized SSE or
  WebSocket mechanism for asynchronous status and progress.
- The server provides access to the local filesystem, opens documents, performs
  requested modifications and returns results. The browser does not depend on
  Python implementation details or invoke native CAD code directly.
- TypeSpec should govern the API operations themselves as well as existing
  config and output structures.
- Python can implement the initial server. Rust is the future direction; Axum
  is a likely framework, not a finalized choice.
- Saved configuration files remain useful through the CLI. A GUI is an editor
  and viewer for those workflows, not the sole way to execute them.
- Establish a repeatable structure for later tools. Defer Git/diff functionality
  until the framework and viewer can display its results.

## First feature candidates

The leading candidate is a **read-only schematic viewer matching Viz's existing
schematic experience**: render all schematic pages on one large canvas surface,
using gotIR and the existing viewer/navigation approach. Reuse its presentation
and rendering behavior rather than introducing a different page-by-page viewer.

A small initial workflow could open a schematic/project, load the applicable
pages, display their combined surface, support existing pan/zoom/navigation,
reload the source and report progress or errors. Confirm exact input scope and
required interactions when this plan resumes.

Other candidates remain available:

- a symbol viewer;
- a symbol editor, which would also require agreed mutation, undo/redo and save
  semantics;
- a PCB viewer, after confirming the available PCB drawing/canvas contract;
- a GUI for creating and editing PCB SVG configuration files with live previews.

The viewer is the current preference, not an irrevocable pilot selection. The
first slice does not need to implement all these applications. Schematic gotIR
support does not establish that PCB rendering uses an identical payload/API.

## Current foundation

ACR already has TypeSpec authority for 45 public JSON/JSONC roots, generated
Python and TypeScript bindings, browser validators, defaults/help metadata and
freshness/conformance checks. API operation contracts are the new work; do not
restart config authority or introduce handwritten duplicate transport DTOs.

See [public contract authority](../../design/public-contract-authority.md),
[PCB SVG config consumption](../../design/pcb-svg-config-authority.md) and the
[architecture/Rust port guide](../../design/architecture-porting-guide.md).

The cleanup extracted shared workflow services and render-job/cache boundaries.
HTTP adapters should consume appropriate typed services shared with the CLI.
Inspect the remaining argparse-oriented seams before selecting an entry point;
frontend calls must not depend on CLI argument namespaces or scraped log text.

`sch-ir` already exports schematic gotIR. Appz Viz contains the retained
schematic IR canvas runtime and its asset/font bundling. Inspect its reusable
entry points and packaging before proposing a new viewer implementation.
Existing gotIR/drawing contracts retain their upstream ownership; ACR's API
should describe their delivery without inventing a competing geometry format.

For a later SVG editor, preserve authored overrides separately from resolved
render settings. Unset/inherit, explicit values, array replacement, JSONC
comments and save behavior need deliberate treatment. Generated types alone do
not define the editing workflow or guarantee comment-preserving round trips.

## In-flight references

Lib Cruncher is a work-in-progress model, not a finished implementation to copy
wholesale. A substantial TypeScript/Lit frontend migration is already stood up;
Python remains its backend for now, with Rust planned later.

Reference checkout: `C:/eli/wn-hw-workspace/appz/lib_cruncher`.
Reference branch: `feature/lib-cruncher-frontend-api-a0`.
The user supplied reviewed plan checkpoint `43b3678ff`; recheck current state
when resuming because another agent is implementing it.

Relevant plan, relative to that checkout:
`docs/plans/active/lib-cruncher-browser-api-a0-cutover/plan.md`.

Relevant principles:

- TypeSpec owns complete browser operations, request/response/error contracts
  and transport behavior.
- Python, TypeScript, Rust and C# artifacts derive from shared contracts where
  those languages are actual consumers.
- One compiled frontend targets the API regardless of backend language.
- JSON, streams, binary responses, headers, security and error behavior receive
  contract coverage.
- Panel Monkey and KiCad protocols retain independent ownership/versioning.
- GUI/workflow redesign is separate from the API cutover.

Do not copy ALX's route names, its 44-route migration inventory or its coordinated
Panel Monkey deployment into ACR's scope. Some current clients still contain
handwritten routes; the reviewed cutover intends to replace them with generated
operations. Follow the intended boundary rather than preserving those gaps.

Viz reference: `C:/eli/wn-hw-workspace/appz/viz`. Start with the schematic gotIR
canvas entry points and `src/py/viz/ir_canvas_runtime_manifest.py`; determine the
supported reuse boundary rather than copying its internal asset list into ACR.

## Rules to settle before implementation

1. **Ownership and hosting.** Decide which infrastructure is shared across apps,
   where ACR operations and TypeSpec sources live, and how the server launches,
   serves frontend assets and exposes connection information. Do not assume that
   this requires either a universal daemon or a permanent `acr gui` command.
2. **Frontend dependencies.** Components use feature state/actions and typed
   clients. A controlled transport layer owns HTTP, streaming, session handling,
   serialization and errors. Generate operation definitions so route literals
   have one authority. Keep renderer integration behind a clear component API.
3. **API authority.** Define versioned operations, methods, paths, parameters,
   request/response types, media types, statuses, errors and stream envelopes in
   TypeSpec. Generate OpenAPI and transport metadata where OpenAPI alone is
   insufficient. Reuse existing configuration and upstream drawing contracts.
4. **Backend equivalence.** Generate Python/TypeScript artifacts and appropriate
   Rust contract bindings/vectors. Require equivalent observable behavior;
   matching type names alone is insufficient. Implementing the Rust backend and
   generating C# bindings are not prerequisites without an actual first-slice need.
5. **Shared workflow behavior.** Keep HTTP handlers thin. CLI and server call
   domain services; filesystem and native-process effects stay behind explicit
   backend interfaces. Avoid one generic endpoint that executes arbitrary CLI
   argument strings or parses human-oriented output.
6. **Local document lifecycle.** Specify document identity, opening/reloading,
   supported file access, resource lifetime, and results/assets returned to the
   browser. Define local-session access policy and mutation/revision semantics
   where needed. Do not recreate the removed eager source-provenance snapshots.
7. **Asynchronous work.** Define status, progress, warnings, completion, failure
   and cancellation consistently. Decide reconnect/disconnect behavior and how
   obsolete requests are superseded. A late preview must not replace a newer
   selection. Keep pan/zoom and other presentation-only interactions local.
8. **Saved artifacts.** Define result media types and resource URLs, cache and
   cleanup behavior, and config load/save semantics. Keep generated previews
   distinct from source-document modifications.

The initial analysis recommends HTTP operations plus SSE for one-way job
progress, with cancellation through HTTP. WebSockets remain an option for an
actual bidirectional requirement. This recommendation has not yet been selected
as the final transport policy. Axum supports either approach.

## Resume sequence

1. Revisit the current Lib Cruncher API work and Viz renderer entry points.
2. Confirm the first user workflow, likely the combined-surface schematic viewer.
3. Record the minimal architecture rules, API ownership and transport choices;
   obtain independent review of the concrete execution slice.
4. Author the smallest complete TypeSpec service contract for that workflow and
   generate language artifacts, operation metadata and shared vectors.
5. Implement a Python server adapter and TypeScript/Lit client around reused
   rendering/workflow services. Exercise the real document-to-canvas path.
6. Qualify the installed workflow and boundary behavior before expanding to
   config editing, symbol editing or Git/diff views.

## Qualification and closeout expectations

- Generated artifacts are fresh and every implemented operation has an owner.
- Registered routes and accepted HTTP/stream behavior match the contract.
- Shared vectors cover success, errors, status/progress and relevant binary
  responses; generated clients exercise the actual serialization rules.
- The frontend contains no backend-language switch or duplicate transport DTOs.
- Viewer/operation tests cover the selected user workflow, late results,
  cancellation and resource lifetime where applicable. Keep tests focused on
  behavior rather than transient implementation structure.
- The installed frontend includes the needed canvas/runtime/font assets and uses
  the same API as development. No frontend build tools are required by end users.
- Existing CLI behavior remains qualified. Applicable saved configs can still be
  consumed headlessly; any save transformations are explicit and tested.
- Promote durable decisions to design docs, ADRs and contracts; run the required
  design-document, test-runtime and independent-review audits before closeout.

## Deferred scope

The generic server's exact packaging/ownership, first API namespace, Python
framework, authentication/bootstrap details and final SSE/WebSocket choice are
open decisions for resumption. No server launch command or endpoint is public yet.

Full symbol editing, Git history/diff/merge, a universal config editor, multi-user
or remote service deployment, and the Rust backend implementation are outside
the initial viewer slice unless separately selected. The old July Lib Cruncher
integration snapshot, upstream issue statuses and Python-model-first contract
proposal have been superseded by this direction.
