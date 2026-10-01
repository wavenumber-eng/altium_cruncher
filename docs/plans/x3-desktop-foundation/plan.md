+++
type = "plan"
id = "x3-desktop-foundation"
status = "pending"
created = "2026-10-01"

[[steps]]
id = "capture-fresh-analysis"
title = "Record the newly agreed X3 direction without inheriting assumptions from the old GUI plan"
status = "done"

[[steps]]
id = "independent-plan-review"
title = "Independently review the architecture, first slice, risks and qualification gates"
status = "pending"
depends_on = ["capture-fresh-analysis"]

[[steps]]
id = "confirm-home-and-name"
title = "Confirm the implementation repository, migration handoff and public X3 executable name"
status = "pending"
depends_on = ["independent-plan-review"]

[[steps]]
id = "contract-foundation"
title = "Define the TypeSpec API, generated clients and backend capability boundary"
status = "pending"
depends_on = ["confirm-home-and-name"]

[[steps]]
id = "frontend-activity-shell"
title = "Build the Lit frontend skeleton and activity lifecycle from a copy-owned development-standard baseline"
status = "pending"
depends_on = ["contract-foundation"]

[[steps]]
id = "x3-rust-host"
title = "Build the Windows-first Rust host with secure loopback serving, sessions, jobs and SSE"
status = "pending"
depends_on = ["contract-foundation"]

[[steps]]
id = "python-worker-spike"
title = "Qualify a persistent packaged Python worker against real Altium Monkey operations"
status = "pending"
depends_on = ["contract-foundation", "x3-rust-host"]

[[steps]]
id = "paint-ir-renderer"
title = "Render saved SchPaintIR fixtures through the browser canvas activity"
status = "pending"
depends_on = ["frontend-activity-shell"]

[[steps]]
id = "schdoc-vertical-slice"
title = "Open and reload a real standalone SchDoc through X3 and display its ordered Paint IR"
status = "pending"
depends_on = ["python-worker-spike", "paint-ir-renderer"]

[[steps]]
id = "tauri-desktop-integration"
title = "Add the Tauri shell, single-instance routing, file associations and multiwindow behavior"
status = "pending"
depends_on = ["schdoc-vertical-slice"]

[[steps]]
id = "qualify-first-slice"
title = "Qualify contracts, security, packaging, lifecycle, rendering and representative Windows installations"
status = "pending"
depends_on = ["tauri-desktop-integration"]

[[steps]]
id = "promote-durable-docs"
title = "Promote accepted architecture and contracts into the destination repository documentation"
status = "pending"
depends_on = ["qualify-first-slice"]

[[steps]]
id = "design-doc-intent-audit"
title = "Audit design documents and contracts against the implemented first slice"
status = "pending"
depends_on = ["promote-durable-docs"]

[[steps]]
id = "test-runtime-impact-audit"
title = "Review conformance and workflow coverage, runtime cost and CI packaging cost"
status = "pending"
depends_on = ["qualify-first-slice"]

[[steps]]
id = "external-review"
title = "Obtain independent implementation, security and boundary review"
status = "pending"
depends_on = ["design-doc-intent-audit", "test-runtime-impact-audit"]

[[exit_criteria]]
id = "architecture-reviewed"
title = "The Rust host, Python worker, frontend, transport and repository boundaries have independent approval"
status = "pending"

[[exit_criteria]]
id = "typed-api-wall"
title = "TypeSpec governs every first-slice operation and generated consumers contain no duplicate wire DTOs"
status = "pending"

[[exit_criteria]]
id = "backend-replaceable"
title = "The frontend uses capabilities and observable contracts without knowing whether Rust or Python handled an operation"
status = "pending"

[[exit_criteria]]
id = "worker-qualified"
title = "The packaged Python worker passes startup, shutdown, cancellation, crash recovery and real Monkey operation tests"
status = "pending"

[[exit_criteria]]
id = "viewer-useful"
title = "A user can rapidly open, inspect and reload a real standalone SchDoc in the read-only canvas viewer"
status = "pending"

[[exit_criteria]]
id = "desktop-lifecycle-qualified"
title = "Single-instance, file-open and multiwindow behavior work in an installed Windows build"
status = "pending"

[[exit_criteria]]
id = "security-qualified"
title = "Loopback authentication and opaque file grants prevent untrusted browser and arbitrary filesystem access"
status = "pending"

[[exit_criteria]]
id = "migration-complete"
title = "The accepted plan and implementation authority live in the destination repository with this temporary copy retired"
status = "pending"

[[exit_criteria]]
id = "signoff"
title = "Focused tests, contract checks, Windows packaging and installation checks pass"
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

# X3 desktop foundation and first viewer

This is a fresh plan created from the October 2026 discussion. It supersedes
the removed `altium-cruncher-gui-config-infrastructure` plan. No decision or
assumption from that plan carries forward unless it is restated here.

The plan is deliberately pending. It records the recommended direction for
review and later execution; it does not start product implementation or a
release. Its temporary home is Altium Cruncher while the planned move into the
internal Altium Monkey development repository waits on that repository's test
system rework.

`X3` is the working name for the native application server and executable, a
reference to Altium's `x2.exe`. Confirm casing, package identifiers and whether
the name becomes public before freezing installers, file associations or API
documentation.

## Objective

Establish the smallest durable native-app foundation for future Altium tools:

- a Rust application server and native desktop host;
- a Lit/TypeScript frontend organized as independently loadable activities;
- a TypeSpec-managed API wall between user experience and implementations;
- a replaceable Python compatibility worker while Altium Monkey migrates to
  Rust; and
- a useful first activity: a fast, read-only standalone SchDoc viewer.

The first slice proves server mechanics, frontend/activity structure, Python
packaging, rendering and desktop file-open behavior. It must not prematurely
commit later symbol editing, footprint editing, schema cleanup or PCB workflows
to APIs designed only for the viewer.

## Ownership and migration boundary

- Keep this planning artifact in Altium Cruncher only until the destination
  repository is ready. Do not add X3 product code to Cruncher merely because
  the plan currently lives here.
- Before implementation, confirm the destination layout in
  `altium_monkey_dev`, move or reproduce this plan there, and retire this copy
  so only one plan is authoritative.
- Put the TypeSpec service, generated consumer artifacts, Rust server and
  frontend under a boundary that can ship together but remain testable as
  separate packages.
- Treat existing Python Altium Monkey and its future Rust implementation as
  providers behind X3 operations, never as frontend-visible protocols.
- Preserve standalone/headless use. The server library should compose into the
  desktop executable and support a deliberate `x3 serve --headless` mode for
  contract tests and future integrations.

## Recommended architecture

### Process model

Start with Rust for X3 rather than building a disposable Python HTTP server.
X3 owns native lifecycle, local security, window/session state, document grants,
jobs, cancellation, events and dispatch. Tauri composes the native shell around
the same Rust server library.

Run existing Python functionality in a lazy, persistent child worker. Do not
embed CPython or make PyO3 the primary bridge in the first slice. A process
boundary makes crashes, cancellation, packaging and the gradual replacement of
Python operations observable and testable.

The packaged shape should initially be:

- `x3.exe`: desktop entry point and application server;
- compiled frontend assets served by X3 on a same-origin loopback endpoint;
- a packaged Python worker and its runtime resources; and
- optional `x3 serve --headless` behavior from the same server implementation.

X3 must terminate orphan workers on normal exit and crashes, restart a failed
worker under a bounded policy, and expose a stable error rather than leaking
Python tracebacks or provider details to the client.

### Provider dispatch and migration

Define a Rust-side provider interface around domain operations. Capabilities
identify which operations and contract versions are currently available. A
provider selection can route an operation to qualified native Rust code or the
Python worker, but that selection is not part of the browser contract.

Migrate operation by operation:

1. preserve TypeSpec request, response, error and event behavior;
2. add shared vectors and provider-equivalence tests;
3. qualify the Rust provider against representative documents;
4. change internal dispatch; and
5. remove the Python implementation only after installed-build coverage passes.

This avoids a flag day and prevents the GUI from becoming coupled to the pace
of the Altium Monkey Rust port.

### Frontend and activities

Create a clean Lit/TypeScript frontend. Start from the current wn-dev-std Lit
activity system as a copy-owned baseline, then make X3's ownership explicit;
do not depend at runtime on internal development-standard source layout.

The shell owns navigation, document/window context, activity activation,
commands, common status and error presentation. Each activity owns its feature
state and view. Activities use generated clients and shared services rather
than route strings, raw fetch calls or native bindings.

Borrow narrow concepts from Appz Viz where useful:

- the animation scheduling core;
- camera, pan and zoom behavior; and
- retained canvas, hit testing, culling and level-of-detail patterns.

Do not treat the current private `@wavenumber/viz-runtime` package as a stable
dependency. Copy-own small proven primitives or first establish a deliberately
exported shared package with its own API and tests. The old gotIR-to-IR2D adapter
is useful evidence, not the rendering authority for this viewer.

### First rendering path

The first activity is a read-only viewer for a standalone SchDoc. Render the
ordered `SchPaintIR A0` display list directly into browser Canvas. Paint IR is a
better first boundary than SVG because it preserves the intended drawing order
and supports interactive navigation without a server round trip for every
view change.

Use known Paint IR fixtures before connecting the real backend. Then exercise a
real SchDoc through X3. Compare server-rendered SVG or PNG snapshots as a test
oracle and diagnostic fallback; they are not the interactive runtime contract.

Current evidence indicates that Python Altium Monkey covers more project and
library rendering paths, while Rust already has a standalone SchDoc Paint IR
planner and SVG/PNG rendering with incomplete broader parity. Provider dispatch
must therefore be capability-driven, and the first slice must validate the
actual destination-repository state before selecting its initial provider.

Retain IR2D as a candidate for PCB manufacturing and generic retained-scene
views. It is not required to mediate schematic Paint IR. A later PCB activity
can evaluate the existing `PcbManufacturingView` and initial IR2D projection
against forthcoming native Altium Monkey IR rather than committing to SVG.

## TypeSpec API wall

TypeSpec owns the complete public application protocol: methods, paths,
parameters, payloads, errors, event envelopes, media types and versioning. Add
the HTTP/REST/OpenAPI tooling needed for service definitions; the existing
JSON-schema-only setup is not enough.

Generate the TypeScript client and runtime validation used by the frontend.
Qualify the official TypeSpec JavaScript client emitter before adopting it
because its current maturity may not meet the project's stability needs. If it
does not, own a small deterministic generator rather than maintaining manual
DTOs and route strings. Generate or derive Rust request/response types and
conformance vectors from the same authority.

The first contract should express typed domain operations, approximately:

- `GET /api/v1/capabilities`;
- `POST /api/v1/documents` using a native-issued opaque file grant;
- `GET /api/v1/documents/{documentId}`;
- `GET /api/v1/documents/{documentId}/paint-ir`;
- `POST /api/v1/documents/{documentId}:reload`;
- `DELETE /api/v1/documents/{documentId}`;
- `POST /api/v1/operations/{operationId}:cancel`; and
- `GET /api/v1/events` as a server-sent event stream.

Names and shapes remain provisional until TypeSpec review. Do not expose a
generic "run operation" endpoint, CLI strings, arbitrary filesystem paths or
provider-specific responses.

Use ordinary HTTP for commands and resources, and SSE for server-to-client job,
document and capability events. HTTP cancellation keeps the first protocol
small and reconnectable. Defer WebSocket until a real activity demonstrates a
bidirectional, low-latency requirement.

### Internal Python protocol

The Rust-to-Python boundary is internal but still typed and versioned. Derive
its operation DTOs or conformance vectors from TypeSpec-owned models. Use a
length- or content-framed JSON stream over stdin/stdout and reserve stderr for
structured logs. The handshake includes protocol version, worker build,
capabilities and provider health.

Every call carries an operation identity, deadline and cancellation behavior.
Tests must cover partial frames, malformed data, worker startup failure, crash,
timeout, cancellation, large Paint IR responses and clean shutdown. Avoid
newline-delimited assumptions that fail when diagnostics or large payloads are
introduced.

## Native desktop behavior

Tauri is the recommended shell because the product needs native file-open
integration while retaining a web frontend. X3 should bind only to a random
loopback port. Bootstrap the webview with a per-process secret or equivalent
authenticated session, validate origin on every API/event connection, and do
not allow remote interfaces by default.

The native side grants documents to the web application using opaque tokens.
Only typed domain operations can use those grants. The server must not provide
a general filesystem REST API, accept arbitrary paths from untrusted browser
content or make a selected directory implicitly accessible.

Use one application instance to receive OS open events and route each document
to a suitable window. X3 owns document and job sessions across windows. Tauri
events may handle native shell notifications; frontend windows should use the
X3 API/event stream for durable domain state. Browser `BroadcastChannel` may be
used only for ephemeral presentation coordination, not as authoritative state.

Register `.SchDoc`, `.PcbDoc` and `.IntLib` associations only after installed
behavior is deliberate. The first release may render only SchDoc; unsupported
associated files must receive a clear capability message rather than silently
failing. Validate paths with spaces, Unicode and long-path behavior.

## Python packaging spike

Use PyInstaller `onedir` as the leading Windows experiment. It is easier to
inspect and usually avoids the extraction/startup penalties of `onefile`.
Bundle the resulting worker directory as Tauri sidecar/resources. Do not select
`onefile` until measurements justify it.

The spike must import and execute a real Altium Monkey schematic operation, not
only a toy Python program. Measure and test:

- package size, cold/warm startup and first-render latency;
- discovery of data files and native dependencies including Skia, Shapely,
  lxml and Pillow;
- logs and support diagnostics without a development Python installation;
- cancellation, worker restart and parent-process cleanup;
- spaces, Unicode, long paths and read-only installation locations;
- antivirus behavior and signing of all shipped executables; and
- deterministic CI output and license inventory.

Build each artifact on its target operating system. Start with Windows and a
Windows CI packaging lane. Tauri MSI production is Windows-hosted; do not make
macOS-to-Windows cross-compilation a first-slice gate. Add macOS and Linux only
after the application boundary and platform-specific packaging requirements are
stable.

## Execution sequence

### 1. Review and authority freeze

- Give this plan to a context-free reviewer.
- Reinspect current wn-dev-std activity assets, Appz Viz primitives and the
  destination Altium Monkey APIs; references are evidence, not inherited
  authority.
- Confirm X3 naming, destination layout, API versioning policy, Tauri version,
  TypeSpec emitters and licenses.
- Promote the plan to the destination repository before product code begins.

### 2. Contract and skeleton

- Author capabilities, document lifecycle, Paint IR delivery, errors, jobs,
  cancellation and event envelopes in TypeSpec.
- Generate and freshness-check OpenAPI, TypeScript client/validators, Rust
  models or adapters, and shared wire vectors.
- Stand up the Lit shell, activity registry/lifecycle and a fixture-only
  schematic viewer.
- Stand up the Rust server library with loopback bootstrap, session/grant store,
  job registry and SSE behavior.

### 3. Worker and real vertical slice

- Package the minimal persistent Python worker and exercise a real Monkey
  operation in an installed-like directory.
- Connect provider dispatch through the typed internal protocol.
- Open, plan, transfer and draw one representative standalone SchDoc.
- Add reload, progress, cancellation, error recovery and document close.
- Compare representative renders with the existing SVG/PNG oracle and record
  accepted differences.

### 4. Desktop integration

- Compose the server and frontend into Tauri.
- Implement single-instance open routing, multiple viewer windows and clean
  shutdown.
- Add provisional file associations only for explicitly handled behavior.
- Exercise installer, upgrade and uninstall flows on clean Windows machines.

### 5. Qualification and closeout

- Run generated-contract freshness and cross-provider conformance vectors.
- Test security boundaries from an unrelated browser origin and with forged
  document identifiers.
- Test worker crash/restart, late results, cancellation, window closure and
  server shutdown.
- Record startup, first-render, pan/zoom and large-document performance budgets.
- Promote accepted architecture to durable documentation, complete the required
  design/test audits, and obtain an independent final review.

## Deferred scope

- document mutation, save, undo/redo and concurrent editing;
- symbol or footprint editing;
- the schema/configuration cleaner activity;
- complete SchLib, IntLib, project and PcbDoc viewing;
- PCB manufacturing/IR2D viewer work;
- WebSocket or peer-to-peer window protocols;
- remote or multi-user service deployment;
- replacing every Python operation with Rust;
- macOS/Linux installers and cross-platform release automation; and
- a formal X3 or Altium Cruncher release from this planning change.

These are later activities or plans. The first slice should leave explicit
extension points without inventing their behavior now.

## Qualification evidence to retain

- independent plan and implementation reviews;
- TypeSpec sources, generated-artifact freshness checks and shared wire vectors;
- provider capability/equivalence reports;
- representative SchDoc fixtures and renderer-oracle comparisons;
- Python-worker packaging measurements and dependency inventory;
- security and lifecycle test results;
- installed Windows smoke-test results; and
- recorded performance budgets with hardware and document identities.

## Research references

- Tauri sidecars: <https://v2.tauri.app/develop/sidecar/>
- Tauri configuration and file associations:
  <https://v2.tauri.app/reference/config/>
- Tauri webview windows:
  <https://v2.tauri.app/reference/javascript/api/namespacewebviewwindow/>
- Tauri single-instance plugin:
  <https://v2.tauri.app/plugin/single-instance/>
- Tauri Windows installers:
  <https://v2.tauri.app/distribute/windows-installer/>
- TypeSpec HTTP operations:
  <https://typespec.io/docs/libraries/http/operations/>
- TypeSpec client emitters:
  <https://typespec.io/docs/emitters/clients/introduction/>
- PyInstaller operating modes:
  <https://pyinstaller.org/en/stable/operating-mode.html>
- PyInstaller change history:
  <https://pyinstaller.org/en/latest/CHANGES.html>
