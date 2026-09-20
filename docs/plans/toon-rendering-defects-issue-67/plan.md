+++
type = "plan"
id = "toon-rendering-defects-issue-67"
status = "done"
created = "2026-09-19"

[[steps]]
id = "research-baseline"
title = "Reproduce and bucket the reported rendering defects"
status = "done"

[[steps]]
id = "agree-behavior"
title = "Agree rotation resolution and physical visibility behavior"
status = "done"
depends_on = ["research-baseline"]

[[steps]]
id = "establish-oracles"
title = "Add approved source fixtures, native-Altium references, and focused characterization tests"
status = "done"
depends_on = ["agree-behavior"]

[[steps]]
id = "define-board-surfaces"
title = "Implement a temporary Cruncher board-region envelope query with future Altium Monkey migration"
status = "done"
depends_on = ["establish-oracles"]

[[steps]]
id = "resolve-board-appearance"
title = "Resolve region-local substrate, solder-mask, and coverlay appearance from authored stack materials with explicit config precedence"
status = "done"
depends_on = ["define-board-surfaces"]

[[steps]]
id = "add-bend-lines"
title = "Add a BEND_LINES virtual layer from source-aware rigid-flex bend geometry"
status = "done"
depends_on = ["define-board-surfaces"]

[[steps]]
id = "clip-silkscreen"
title = "Add configurable silkscreen clipping to the physical solder-mask/coverlay film domain"
status = "done"
depends_on = ["resolve-board-appearance"]

[[steps]]
id = "aggregate-diagnostics"
title = "Collect, group, summarize, and optionally persist nonfatal Toon diagnostics"
status = "done"
depends_on = ["establish-oracles"]

[[steps]]
id = "add-native-clipping"
title = "Integrate the generic half-space clipping contract from an exact Geometer source revision"
status = "done"
depends_on = ["define-board-surfaces"]

[[steps]]
id = "implement-cross-side-visibility"
title = "Place bodies in board space and render only geometry visible beyond each board surface"
status = "done"
depends_on = ["add-native-clipping"]

[[steps]]
id = "compose-aperture-visibility"
title = "Compose opposite-side edge, cutout, slot, and drill visibility through the board-material complement"
status = "done"
depends_on = ["implement-cross-side-visibility"]

[[steps]]
id = "qualify-rotation"
title = "Resolve IC1-IC3 rotation semantics without regressing instance-space bodies"
status = "done"
depends_on = ["establish-oracles"]

[[steps]]
id = "update-public-surface"
title = "Update TypeSpec-owned metadata, design documentation, and generated artifacts where required"
status = "done"
depends_on = ["implement-cross-side-visibility", "compose-aperture-visibility", "qualify-rotation", "aggregate-diagnostics", "resolve-board-appearance", "add-bend-lines", "clip-silkscreen"]

[[steps]]
id = "focused-verification"
title = "Run focused correctness, cache, determinism, and performance verification"
status = "done"
depends_on = ["update-public-surface"]

[[steps]]
id = "design-doc-intent-audit"
title = "Audit design docs, ADRs, and requirements against implementation"
status = "done"
depends_on = ["focused-verification"]

[[steps]]
id = "test-runtime-impact-audit"
title = "Audit new test runtime impact and assign each fixture to the appropriate test level"
status = "done"
depends_on = ["focused-verification"]

[[steps]]
id = "external-review"
title = "Obtain independent review of geometry semantics, contracts, and regression coverage"
status = "done"
depends_on = ["focused-verification", "design-doc-intent-audit", "test-runtime-impact-audit"]

[[steps]]
id = "release-signoff"
title = "Run repository release signoff"
status = "done"
depends_on = ["external-review"]

[[exit_criteria]]
id = "agreed-semantics"
title = "The rotation-resolution and physical-visibility decisions are recorded"
status = "met"

[[exit_criteria]]
id = "cross-side-fidelity"
title = "J3 and RT_SUPER through-board pins render on both sides without duplicating hidden package bodies"
status = "met"

[[exit_criteria]]
id = "aperture-visibility"
title = "Approved edge, cutout, straddle, and reverse-mount fixtures reveal complete models only through non-board XY space and surface-clipped fragments over board material"
status = "met"

[[exit_criteria]]
id = "region-envelope-fidelity"
title = "Bluetooth Sentinel rigid and flex regions resolve to their own finished stack envelopes"
status = "met"

[[exit_criteria]]
id = "region-appearance-fidelity"
title = "Bluetooth Sentinel rigid, flex, coating, and exposed-substrate areas use deterministic source-aware appearance with documented config precedence"
status = "met"

[[exit_criteria]]
id = "bend-line-fidelity"
title = "Bluetooth Sentinel bend lines render as clipped, independently styled 2D board-region annotations without folding or deforming the board"
status = "met"

[[exit_criteria]]
id = "silkscreen-clipping-fidelity"
title = "Configured silkscreen clipping removes artwork outside the board and over cutouts, film openings, pads, and physical holes without changing unclipped compatibility mode"
status = "met"

[[exit_criteria]]
id = "false-positive-control"
title = "Small source-side penetrations that do not cross the board slab remain absent from the opposite view"
status = "met"

[[exit_criteria]]
id = "rotation-fidelity"
title = "IC1-IC3 match their authored body outlines and native-Altium orientation without rotating other packages"
status = "met"

[[exit_criteria]]
id = "public-contracts"
title = "Changed public output metadata and configuration are TypeSpec-authored, generated, documented, and validated"
status = "met"

[[exit_criteria]]
id = "diagnostic-reporting"
title = "Nonfatal model and geometry diagnostics are deterministic, grouped at completion, and available as a machine-readable report"
status = "met"

[[exit_criteria]]
id = "cache-and-performance"
title = "Clipping participates in cache identity and benchmarked runtime remains within the agreed budget"
status = "met"

[[exit_criteria]]
id = "signoff"
title = "Focused and repository release signoff passes"
status = "met"

[[exit_criteria]]
id = "design-doc-intent-audit"
title = "Design docs, ADRs, and requirements match implementation"
status = "met"

[[exit_criteria]]
id = "test-runtime-impact-audit"
title = "New tests are listed and runtime impact is reviewed"
status = "met"

[[exit_criteria]]
id = "external-review"
title = "Independent external review has no unresolved material findings"
status = "met"
+++

# Qualify and correct Toon component rendering defects

This completed plan covers the defects reported in [GitHub issue 67](https://github.com/wavenumber-eng/altium_cruncher/issues/67). Implementation and release qualification are complete against the published, mutually compatible Geometer and Altium Monkey 2026.9.19 packages and ordinary dependency pins.

## Scope and constraints

- Preserve the authored Altium model, placement, offsets, side, and rotations unless a native-Altium oracle demonstrates that Cruncher's transform is wrong.
- Never commit the reporter's original PcbDoc or IC3 screenshot. Repository regression coverage must use existing approved fixtures or a separately user-authored purpose-built board with explicit provenance.
- Preserve the current contract that components without an authored STEP, extrusion, or supported analytic body add no illustration. Component Height alone does not define renderable shape. Add a nonfatal diagnostic for fitted components that have no supported renderable body.
- Treat the requested top or bottom view as a camera/visibility decision, never as a new mounting side.
- Keep PCB semantics in Cruncher or Altium Monkey. If Geometer changes, expose a generic geometry-clipping capability rather than board-specific policy.
- Preserve the direct native rendering path, source materials, multi-body components, deterministic source ordering, worker batching, and memory/disk caching.
- Include source-aware local board thickness in this release. Implement the spatial region-to-envelope query temporarily in Cruncher, exercise it with Bluetooth Sentinel, and migrate to the future Altium Monkey API tracked by [altium_monkey_dev issue 95](https://github.com/wavenumber-eng/altium_monkey_dev/issues/95) in a later release.
- Include source-aware board-surface appearance in this release: rigid and flex regions may expose different substrate materials and may use solder mask, coverlay, or no coating. Preserve explicit user color overrides and define deterministic precedence between stack material colors, saved 3D-view colors, configured palettes, and fallbacks.
- Add `BEND_LINES` as a composable virtual layer. It is flat board-document annotation; this work does not attempt to render a physically folded board.
- Add configurable top/bottom silkscreen clipping to the corresponding physical film domain. Keep legacy unclipped behavior available and avoid requiring Geometer for an SVG-domain intersection already owned by Cruncher.
- Treat the supported board as a rigid or rigid-flex collection of locally planar regions with constant envelopes. A component body whose conservative XY projection intersects regions with different envelopes is not representable by one pair of Z half-spaces; retain mounting-side rendering for that body and emit a nonfatal diagnostic. Cavities, embedded components, and continuously varying thickness remain out of scope.
- Do not add a Node runtime dependency. Any public metadata or configuration change starts in `src/tsp/altium_cruncher` and is generated by the repository commands.
- Do not broaden this work into exact inter-component occlusion unless a marked issue example demonstrates that it is required.

## Research snapshot

### Reproduction inputs

- Local-only reporter sample: `sample.PcbDoc`, 7,526,400 bytes, SHA-256 `DC5AA9072D4CDBA05E3F4647365549467D90683784A36EE19ACEAC5A9490B10A`. It is a research input only and must not be committed, copied into test assets, or included in generated artifacts.
- Existing regression fixture: `tests/assets/projects/rt_super_c1/input/RT_SUPER_C1.PCBdoc`.
- Local-only Altium orientation reference for IC3 in the issue reporter's `sample.PcbDoc`: `IC3_ref.png`, 592,019 bytes, SHA-256 `7085571DCB3A2074D21E4D02D80BA384616ED6C19702791D793380708CF4CCC4`. The red arrow identifies pin 1. It must not be committed or copied into test assets.
- Committed rigid-flex fixture: `tests/assets/projects/bluetooth_sentinel_flex/input/Bluetooth_Sentinel.PcbDoc`, 17,699,328 bytes, SHA-256 `1E18C3EFA9D6C3245AA09CAB7268B2A908078E50ED2D09DC9D6DFD3BC36B95F3`. Its source and authorization are recorded in the adjacent `source-manifest.json`.
- Planned purpose-built regression fixture: a small user-authored board containing one fitted component with no model, one through-board model, one IC3-equivalent rotation case, and optionally one board-edge overhang and one overhang across an interior through-cutout. It receives a new fixture identity and provenance manifest and must contain no reporter file, screenshot, or unrelated reporter design content.
- Baseline command: `acr toon <input.PcbDoc>` with normal top and bottom outputs and no pre-existing disk cache.

The reporter sample produced 9 top-side component illustrations and 104 bottom-side component illustrations from 117 components. That disparity is not itself an assertion of expected count, but inspection confirms that bodies which physically extend through the board are selected only by their authored `BODYPROJECTION` side.

### Confirmed facts

1. **J3 is intentionally unusual, not mis-resolved.** J3 is a bottom-side `QFP32_STM32` footprint with a QFP STEP body. Its embedded-model identity resolves correctly even though other bodies reuse the filename `step_temp.STEP`. The transformed XY model envelope nearly coincides with the pad envelope. Its authored body spans both signs of its mounting-surface Z coordinate, so pins can protrude through the top. The current top view omits the component because collection is side-exclusive.
2. **RT_SUPER already contains the second cross-side oracle.** The T-pin family is mounted/projected from the bottom and has substantial signed Z extent through the board. It is suitable for checking repeated-instance transforms and both-side visibility.
3. **A sign test is insufficient.** Ordinary source-side models can have small negative standoffs without reaching the far board surface. Selecting every body whose local bounds cross zero would incorrectly expose parts such as shallow top-side packages on the bottom.
4. **Body geometry height is being retained.** For the reporter sample, rendered STEP Z bounds agree with authored standoff/overall bounds within the characterization tolerance. The reported height symptom is therefore not evidence that STEP height is discarded.
5. **Model-less sample parts are expected omissions with diagnostics.** U1, P2, J2, and FB1 have no STEP, extrusion, or other supported body. Component Height supplies only one dimension and cannot define a trustworthy package footprint, so these parts remain intentionally absent. Fitted components in this state should contribute one grouped nonfatal diagnostic rather than invented geometry.
6. **The rotation defect is localized to IC1, IC2, and IC3.** All three are bottom-side instances with component rotation 270 degrees, `MODEL.3D.ROTX=90`, and `MODEL.3D.ROTZ=90`. The current instance-space normalization produces a 6.0 by 9.9 mm vertical projection. Their authored body outlines and pads are 9.9 by 6.0 mm and horizontal, matching the reported Altium presentation.
7. **The stored Z rotation as a footprint-local candidate matches the IC oracle.** Applying the raw model Z rotation without the instance-space correction produces an exact 9.9 by 6.0 mm match to each authored body outline. This is one specific alternative transform, not an arbitrary 90-degree designator adjustment.
8. **A global removal of the correction would regress other parts.** Across 110 applicable STEP bodies in the reporter sample, the footprint-local candidate is uniquely better only for IC1 through IC3; the current instance-space candidate is better for 52 and the remaining 55 are dimensionally ambiguous. Across 150 applicable RT_SUPER bodies, the footprint-local candidate is better for none, the current candidate is better for 28, and 122 are dimensionally ambiguous.
9. **Multi-body grouping is currently preserved.** Sample components P1 and JP2 retain all body indices in one component illustration request. They remain valuable regression cases, but there is not yet evidence that grouping itself is defective.
10. **The IC direction oracle is now explicit.** In the supplied Altium presentation, IC3 is horizontal and pin 1 is the upper-right lead, next to the short vertical reference mark. This is the required 90-degree counter-clockwise correction in the bottom-side presentation; matching only the rectangular extents is insufficient.
11. **Altium Monkey already owns source-aware physical stack resolution.** `AltiumLayerStackDocument.from_pcbdoc(...)` reconciles the serialized layer representations, and `to_resolved_layer_stack()` exposes `stack_envelope_for_substack(...)` and `stack_envelope_for_board_region(...)`. Cruncher should consume these semantic models instead of summing raw V9 rows or creating a second V7 parser.
12. **The fixture envelopes are now characterized through that public API.** The reporter sample resolves to a 16.2 mil (0.41148 mm) finished envelope from +8.1 to -8.1 mil around its local midplane. RT_SUPER resolves to 40.312 mil (1.0239248 mm), from +20.156 to -20.156 mil. Both resolved envelopes include the enabled solder-mask, copper, and dielectric rows.
13. **Bluetooth Sentinel is now the committed local-thickness oracle.** Its source-aware model contains one physical stack, two substacks, and three board regions. Regions 1 and 2 use the 32.1455 mil `Rigid` envelope; Region 3 uses the 3.3267 mil `Flex` envelope. It is a shipping test asset for the temporary Cruncher region query and later Altium Monkey API parity tests.
14. **The IC3 image is a local-only research oracle.** It belongs to the reporter defect sample, not Bluetooth Sentinel, and establishes the expected IC1-through-IC3 direction without becoming a repository asset. The committed replacement test must encode the same asymmetric pin-1 direction in a user-authored body/outline that can be asserted numerically without the screenshot.
15. **Geometer 2026.9.13 has transforms but no illustration clipping contract.** Its model and mesh illustration requests accept affine placement, preparation, linework, and style options, but expose no clip plane or half-space. Exact through-board visibility therefore cannot remain on the current direct one-pass path without a generic Geometer extension.
16. **Ordinary mounting-side overhang does not require native clipping.** Component illustration layers are not clipped to the board outline, and Toon expands the SVG viewBox to include component bounds. A body extending past the board edge remains visible from its mounting side today.
17. **Current warnings are emitted during work rather than reported as a stable result.** `IllustrationJob.warn()` logs immediately while accumulating strings, some call paths append without logging, and direct-model warnings use a separate first-warning policy. Worker completion order and cache hits can therefore affect console order and visibility. Toon has no final grouped summary or full warning report.
18. **Most release work is independent of Geometer issue 40.** Fixture tests, region indexing, board-space transform composition, rotation qualification, structured diagnostic collection, public diagnostic contracts, and cache-key design can be completed while native clipping is being built.
19. **Current mask and substrate colors come from different global sources.** `soldermask_film.color = "auto"` reads the side-wide `CFG3D.TOPSOLDERMASKCOLOR` or `CFG3D.BOTSOLDERMASKCOLOR` from the saved 3D view and falls back to `#176B3A`. `BOARD_SUBSTRATE` does not use the layer stack; it uses the configured color or fixed `#B6A26B`. Neither path can represent different rigid/flex surface materials by region.
20. **Bluetooth Sentinel exposes the appearance gap.** Its saved 3D configuration requests black top and bottom solder mask and a `#D9DBCD` board-core display color. The resolved semantic stack identifies `Solder Resist`, `FR-4`, and `Polyamide`, while the Flex substack resolves to copper/Polyamide without the rigid solder-mask rows. In the installed Altium Monkey version, this file yields `materials = ()` and no semantic material color, so color must not be guessed from a material name until the native material records are characterized.
21. **Altium Monkey and the AD26 C# oracle distinguish coverlay from ordinary solder mask.** Monkey's current `StackupXLayerType` exposes distinct `SOLDER_MASK` and `BIKINI_COVERLAY` TypeIds that match the C# schema constants. The AD26 `LayerType` enum likewise has separate `SolderMask` and `Coverlay` members. The Pcb stack importer classifies a flex-enabled solder-mask-layer record as bikini coverlay when its coverlay expansion is positive or its dielectric type is film, and imports dielectric material name and coverlay expansion separately. Cruncher must use those typed semantics rather than treating every outer polymer row as solder mask.
22. **Bluetooth Sentinel contains six region-local bend lines.** They are attached to Flex Region 3 and carry angle, radius, fold index, and two endpoints. The top-level Board6 bend cache is empty in this saved file. Altium Monkey explicitly documents the region-local geometry and Board6 cache coordinate systems as non-interchangeable, so `BEND_LINES` must use the region-local source plus a verified region-to-board transform.
23. **Current physical silkscreen is not clipped to film openings by default.** Top/bottom overlay primitives are independently rendered physical layers. General board-outline clipping can constrain them to the outer profile, but it does not intersect them with the solder-mask film domain. The existing film renderer already constructs most required aperture geometry, though its private SVG mask must be factored into a shared surface-domain builder instead of coupled by generated element ID or draw order.
24. **AD26 separates authored material color from visualization fallback color.** The current Altium Monkey property table identifies `Material.Color` as `System.Windows.Media.Color`. AD26's generic stack serializer round-trips typed values through the .NET type converter, and the modern stack UI uses a typed `Color` from layer properties when one exists. By contrast, the V7 PCB importer imports dielectric material name, thickness/electrical values, and coverlay expansion but does not import a material color. Altium's `MaterialFactory` and stack editor then provide hard-coded class-display colors. Those UI colors are fallback evidence, not authored material data.
25. **The bend source transform needs a typed upstream contract.** Cruncher's temporary adapter treats `BoardRegions/Data` endpoints as offsets from the source region geometry envelope's lower-left, matching Bluetooth Sentinel and a translated semantic vector. [altium_monkey_dev issue 96](https://github.com/wavenumber-eng/altium_monkey_dev/issues/96) tracks a core region-local-to-board transform so a future Cruncher release can delete that format interpretation.
26. **The regional appearance implementation now has an end-to-end oracle.** Bluetooth Sentinel emits three substrate paths: Rigid Regions 1/2 use the saved `#D9DBCD` board-core display color and identify `FR-4`, while Flex Region 3 uses the configured amber `#D18B28` fallback and identifies `Polyamide`. Top and bottom film include only the two rigid regions because the Flex substack has no enabled solder-mask or coverlay row. A synthetic typed-bikini-coverlay vector verifies that ordinary zero-thickness overlay is not misclassified as coverlay and that WPF `#AARRGGBB` material color is normalized to SVG `#RRGGBB`.
27. **Silkscreen clipping now shares the film aperture domain.** `none` leaves authored overlay unchanged, `board` removes board cutouts and physical bores, and `film` also removes mask/coverlay apertures and every region without physical film. Raster assertions cover an SMD mask opening, an interior cutout, and unaffected artwork. General PCB-SVG defaults to `none`; newly generated Toon illustration presets select `film`.
28. **The pre-native visibility qualifier is now executable and overhang-safe.** A region-envelope query now reports whether the complete conservative XY bounds are covered by equivalent board material, including the union of adjacent equal-envelope regions. Bounds crossing an outer edge, an interior cutout, invalid region geometry, or different envelopes cannot produce one Z plane: the mounting-side illustration remains unclipped and the opposite-side illustration is omitted with a future clipping diagnostic. Fully covered bounds resolve to the exact top or bottom half-space; wholly surviving and empty fragments are detected without a native call.
29. **RT_SUPER T1 numerically requires both clipped views.** Its bottom-mount-relative transformed bounds before board-surface placement are `(-0.508, -0.504296108, -4.4069)` through `(0.508, 0.504296108, 2.5273)` mm. The owning rigid region is 40.312 mil / 1.0239248 mm thick, so the complete board-space placement translates those bounds by `-1.0239248 mm` in world Z before applying `z >= 0` for the top fragment and `z <= -1.0239248 mm` for the bottom fragment. This is a committed numeric regression oracle; Geometer B0 remains necessary to render the fragments.
30. **Geometer issue 40 is available for pre-publication integration.** Cruncher remains release-pinned to `wn-geometer==2026.9.13`, whose A0 requests have no clipping field, but local Geometer revision `ffb250b7cab66bdbfec3fc2a255dad7f8fe8902c` exposes the generated B0 model, mesh, HLR, clipping, fragment, and empty-result values. Cruncher consumes those generated types without inventing a parallel wire contract. `uv run --with-editable ..\geometer ...` selects the sibling checkout for a direct command without modifying `pyproject.toml` or `uv.lock`. Rack launches nested uv commands, so full local qualification instead uses an editable environment install with `UV_NO_SYNC=1` inherited by those subprocesses.
31. **The current Cruncher slice satisfies repository structural gates.** Illustration diagnostics, model-geometry/cache codecs, surface policy, and shared A0 helpers are separated into focused modules. The Python signoff reports no new file-size, byte-size, complexity, or `Any` regressions, and all newly public dataclasses have machine-checked interface-design entries.
32. **The post-refactor verification checkpoint is green.** The focused feature/signoff selection passes 213 tests. `rack run --all` passes all 13 subtests and 85 tests, with the existing optional native Megamaid comparison skipped. Contract freshness covers 464 generated artifacts across 46 contracts; TypeScript validation and all 124 shared browser vectors pass.
33. **Valid split-board regions form the board partition and are the reliable rigid-flex canvas oracle.** The AD26 API rebuilds split-board regions from the board outline and its split lines (`IPCB_Board.RebuildSplitBoardRegions`); the board outline owns the split lines, and each split record connects left/right board regions. Bluetooth Sentinel's three valid regions have negligible numeric overlap, one connected union, and the complete 80 by 55 mm board envelope. Its legacy outline bounding box uses arc endpoints and collapses to the roughly 80 by 5 mm flex strip, which caused region fills and film masks to be clipped while the outline stroke remained visible outside the canvas. Canvas bounds now retain the legacy outline as a compatibility baseline and expand it by the complete valid region partition; any invalid region keeps the legacy fallback.
34. **Visible copper is region-local in a rigid-flex surface view.** Bluetooth Sentinel's rigid regions expose `L1/TOP`, but the Flex substack begins at `L3/MID2`; its bottom surface is `L32/BOTTOM`. A composed top view that requests literal `TOP` therefore omits all flex copper. Rendering literal `MID2` board-wide would expose an internal rigid layer. `SURFACE_COPPER_TOP` and `SURFACE_COPPER_BOTTOM` instead resolve the first enabled copper row from each region side, group regions by physical layer, and clip that layer's artwork to only the regions where it is outer copper. Literal physical tokens retain their existing raw-layer meaning.
35. **Persisted bend-line identity is narrower than Altium's live object model.** The authoritative region-local `BENDINGLINE{N}` payload used by Bluetooth Sentinel contains angle, radius, fold index, and endpoints only. Altium's richer native object model also exposes a name, locked state, affected-region names, rotation, and computed affected width, while the optional top-level Board6 cache serialization can carry name/state/region fields. Bluetooth has no Board6 bend cache, and neither inspected interface exposes a per-line color. Cruncher may therefore group and label shipping bend lines by fold index plus region/source identity, but must not claim an authored name or color unless Altium Monkey later supplies a source-aware unified record.
36. **The green dots in the first Bluetooth review were a review-config defect.** They were all 173 plated via-hole marks from the explicit `DRILLS` virtual layer. Every Bluetooth via is tented on both sides. Toon already selects `respect_tenting=true`; the ad-hoc PCB-SVG review config inherited the general compatibility default `false`. The review config now uses the Toon tenting policy so those via-drill marks are omitted.
37. **The B0 clipping contract satisfies the rigid-board through-body requirement.** Against the exact unpublished revision above and after board-surface placement, RT_SUPER T1's top fragment has bounds `(-0.2413, -0.23954065132, -0.000001)` through `(0.2413, 0.23954065132, 1.5033752)` mm. Its bottom fragment has bounds `(-0.508, -0.504296108042, -5.4308248)` through `(0.508, 0.504296108042, -1.0239238)` mm. Full Toon top/bottom composition includes T1 on both sides, cold and warm cache outputs are byte-identical, and the generated B0 request applies `cap_policy="none"` after the complete authored transform.
38. **The unpublished dependency passes Cruncher's feature matrix.** With the exact sibling revision installed editable and uv synchronization disabled for nested Rack commands, L0 passes 30 tests and L3 passes 34 tests with one unrelated optional skip. The only L99 failure in that environment is the expected version assertion: the locked release metadata requires `wn-geometer 2026.9.13` while the deliberately substituted checkout reports `2026.9.19`. Python structural signoff has zero findings. After restoring the locked environment, L99 passes all 22 tests and the combined persisted Rack status is 13/13 subtests, 86 passed, one optional skip. Final release signoff still waits for a published Geometer version and ordinary pin update.
39. **Bottom-side board thickness belongs in the affine placement, not only the clipping plane.** The first B0 integration mirrored bottom-authored geometry about top-surface `z=0` but did not translate its mounting plane to the owning region's bottom surface. That left zero-thickness or shallow slices of bottom SMD models in top output and shortened through-board projections by one board thickness. Cruncher now resolves placement thickness from the component/body anchor, left-composes world-Z translation `Tz(-T_region)` for mesh, STEP, and analytic sources, and then performs the conservative full-footprint clipping query. RT_SUPER C10 is empty from the top while T1 remains nonempty on both sides. Reporter IC1-IC3 similarly move from `[-1.75, 0]` mm to `[-2.16148, -0.41148]` mm and are absent from the top. The placement contract and illustration identities are versioned so stale artwork cannot survive the correction.
40. **A clipped native SVG must be placed from its post-clip projected bounds.** Reporter P1's seven pin bodies have a correct affine pose: their clipped HLR centers coincide with the through-hole pad centers. The visible top fragment spans 15.874511 mm in X, while the complete source model spans 17.77950978 mm. Cruncher formerly mapped Geometer's normalized clipped SVG through the complete-model span, stretching the pin pitch by about 12 percent and making the outer pins diverge while the middle stayed near alignment. HLR now requests the projected bounding box and that post-clip box drives SVG origin, scale, and stroke normalization. Bottom-view X is converted back from the camera's reversed basis before placement, and the renderer/cache contract is versioned.
41. **Two approved fixtures now cover non-board XY visibility.** `projection-test` is a five-component, 16.2 mil purpose-built board with top-side edge/cutout/straddle placements and one bottom-side USB body. `usb-edge` is a sanitized, PcbDoc-only 31.4962 mil real-world board with top-side straddle connector J1 and bottom-side reverse-mount LED D1. The repository owner explicitly authorized both fixture copies and removed proprietary logo artwork from `usb-edge`. Project, schematic, project-structure, History, generated-output, and working-library files are excluded from that fixture.
42. **The physical board mask supplies the topology but not the final occlusion policy.** `BOARD_SUBSTRATE` already carries the outer profile, interior board cutouts, D1's non-plated slot, and drill bores. Component visibility reuses that topology through a side-aware board-occlusion domain: NPTH apertures remain open, while blind, filled/capped, and viewing-side-tented bores stay opaque. The optional `BOARD_CUTOUTS`, `DRILLS`, and `SLOTS` layers remain review annotations rather than physical occluders.
43. **Aperture visibility composes from two existing Geometer renders.** For board-occlusion domain `B`, the orthographic result is `(Project(ClipZ(M)) intersect B) union (Project(M) intersect not-B)`. The clipped and full projections retain their independent native canvas transforms. Both remain inside the existing `ILLUSTRATION_TOP/BOTTOM` layer, and the complement mask spans the expanded component canvas so edge overhang is not erased. SVG antialias coverage is not a mathematically binary partition under source-over; a possible one-pixel boundary seam and transparent-material behavior are explicit v1 limitations that require raster qualification rather than an exactness claim.
44. **Release qualification must pin one compatible geometry stack.** Cruncher release signoff requires a published Altium Monkey version and a published Geometer version whose exact dependency relationship has been qualified together. Cruncher must pin that Monkey release and the same compatible Geometer release, regenerate `uv.lock`, remove the editable Geometer override, and rerun the full signoff matrix.
45. **Independent review found no release-blocking Geometer request.** Geometer's existing full projection, B0 half-space clipping, HLR, and projected-bounds results are sufficient for perpendicular orthographic Toon. A future native multi-variant request could reduce duplicate work but is only a convenience/performance proposal.
46. **The approved stress fixtures pass the Cruncher composition.** Projection-test bottom output restores J2 and J7 only outside the board domain, including correct bottom mirroring. USB-edge top output reveals reverse-mount D1 through its 1.6 mm NPTH slot, while side-aware tests keep tented and blind bores opaque. Structural tests cover independent projection transforms and the expanded complement-mask canvas.
47. **Composite artwork is deterministic across execution modes.** Projection-test top and bottom SVGs are byte-identical across cold cache, warm cache, four native workers, and one native worker. The combined L0/L3/focused matrix passes 115 tests with one optional skip against the exact local Geometer checkout.
48. **The additive config surface advances to A1.** `pcb.svg.config.a1` is the current TypeSpec-authored target for regional substrate/film fallbacks, `SURFACE_COPPER_TOP/BOTTOM`, `BEND_LINES`, and silkscreen clipping. A0 remains accepted without rewriting an authored file during ordinary rendering, its public schema path remains generated, and resolved/new configs identify as A1. Explicit non-`auto` colors retain global-override meaning. Open root/style records and string layer arrays leave room for later material maps, per-bend policy, and synthetic layers without reinterpreting current fields. Breaking or replacement shapes start at B0.
49. **Contract and test-runtime audits are complete.** Generation produces 465 artifacts for 46 contracts; freshness, TypeScript, and browser checks pass with 126 shared vectors. The focused config/rendering/signoff selection passes 133 tests in 11.45 seconds. Fast semantic/cache tests remain in focused unit modules; native fixture workflows, including `projection-test` and the sanitized PcbDoc-only `usb-edge`, remain in L3, and the aperture stress parameterization is explicitly marked slow. Project fixtures remain excluded from release artifacts.
50. **The remaining local failures are the release dependency gate, not config regressions.** With the currently pinned Geometer 2026.9.13 restored, six B0 request tests fail because that release does not export `ModelIllustrationGeometryRequestB0` or `MeshHlrProjectionRequestB0`; 63 neighboring focused tests pass in 1.64 seconds. The exact unpublished checkout already passes the feature matrix recorded above. Do not add runtime fallback aliases or weaken the tests: update both controlled dependency pins and `uv.lock` after publication, then create the dated release note/version and run final signoff.
51. **Independent Cruncher review is closed with no unresolved material finding.** The review required the aperture-complement mask to span the expanded component canvas, side-aware treatment of tented/capped/blind bores, pad-slot topology, independent placement transforms for full and clipped projections, an explicit antialias/transparent-material limitation, and cache identity coverage. The implementation and focused/L3 tests now cover those points; Geometer needs no additional release-blocking API.
52. **Published dependency and release signoff gates are met.** `altium-monkey==2026.9.19` declares and imports with `wn-geometer==2026.9.19`; the native B0 clipping types are present. Final Rack signoff passes all 13 subtests and 88 tests with one optional native-oracle skip. Contract freshness covers 465 artifacts and 46 roots, TypeScript and 126 browser vectors pass, Pyright is clean, the wheel and sdist pass Twine, content-policy, reproducible-wheel-metadata, manifest, and clean-install checks, and the Wavenumber development-standard audit passes.

### External semantics references

- Altium's [Working with 3D Bodies](https://www.altium.com/documentation/altium-designer/pcb/3d-bodies) documentation defines Overall Height, Standoff Height, negative standoff for bodies passing through the PCB, and the body's projection side.
- Altium's [extruded, spherical, and cylindrical body](https://www.altium.com/documentation/altium-designer/pcb/3d-bodies/extruded-spherical-cylindrical?version=23) documentation gives a component pin passing through the board as a bottom-projection example.
- Altium Monkey's [PCB document guide](https://github.com/wavenumber-eng/altium_monkey/blob/main/docs/pcbdoc.md) identifies `AltiumLayerStackDocument` as the source-aware inspection model and `ResolvedLayerStack` as its read-only convenience view.
- Altium Monkey's [format contract](https://github.com/wavenumber-eng/altium_monkey/blob/main/docs/format_contracts/pcbdoc.md) distinguishes V7 saved-layer identity from V8 manager rows and V9 cache rows; those serialized identities must not be treated as interchangeable thickness sources.
- The public [flex topology report example](https://github.com/wavenumber-eng/altium_monkey/blob/main/examples/pcbdoc_flex_topology_report/pcbdoc_flex_topology_report.py) demonstrates substack and board-region envelope lookup.
- Geometer [issue 40](https://github.com/wavenumber-eng/geometer/issues/40) owns generic deterministic post-transform half-space clipping across its illustration pipelines and transports.
- The local AD26.9.1.9 decompiled C# oracle under `C:\Users\EliHughes\OneDrive - Wavenumber LLC\altium_research\ADDevelop 26.9.1.9\.net_decompiled` confirms the Layer Stack Manager layer-type enum, coverlay classification, material-name import, and coverlay-expansion import. It is research evidence, not a runtime or redistribution dependency.

## Problem buckets

### A. Through-board visibility — confirmed

**Symptom:** A physical body is mounted/projected from one side but a subset of its geometry exits the opposite board surface. Toon renders it only on its mounting side.

**Primary examples:** reporter J3; RT_SUPER T1 through T76.

**Required behavior:** each view shows only the part of the body outside that view's physical board surface. J3's protruding pins should appear on top, but the bottom QFP package body must not be duplicated on top.

### B. Rotation/pose fidelity — confirmed for IC1 through IC3

**Symptom:** the three rectangular IC models are rotated by one quarter turn relative to their pads, authored component-body outlines, and Altium presentation.

**Required behavior:** resolve the stored model Z rotation semantics from authored evidence. IC1 through IC3 must become horizontal without changing the correctly oriented passives, U4, or RT_SUPER models and without a designator-specific exception.

### C. Multi-body and clipped-fragment composition — confirmed canvas defect

**Symptom:** multi-body grouping and affine placement are correct, but a clipped illustration can be scaled through the complete source-model bounds instead of the surviving projected fragment. For a long connector such as P1 this changes visible pin pitch after clipping, so only the central pin remains approximately registered with its pad.

**Primary examples:** reporter P1 and JP2.

**Required behavior:** preserve all member bodies and their source/material order, then use the post-transform, post-clip projected bounds from the same native result for SVG canvas placement, scale, stroke normalization, bounds, and cache identity. Convert the bottom camera's reversed X basis back to board coordinates exactly once.

Exact per-pixel occlusion between separate component symbols remains outside the initial scope. It should become its own issue if a marked example proves component-level paint ordering inadequate.

### D. Components without renderable bodies — expected omission with a nonfatal diagnostic

**Examples:** reporter U1, P2, J2, and FB1.

These are not rendering defects. Component Height alone is insufficient to reconstruct package shape, so Toon should continue to omit them and should not synthesize pad-envelope boxes. Emit one structured `missing-renderable-model` diagnostic for each fitted, selected component that has no supported STEP, extrusion, or analytic body. Do not warn for a DNP component, a component excluded by selection, or a component outside the active variant population.

Keep distinct causes distinct: no authored body, an authored but unsupported body type, a missing/unreadable STEP payload, invalid body geometry, and a Geometer degeneracy must not collapse into the same message.

### E. Nonfatal warning presentation — confirmed infrastructure defect

**Symptom:** warnings are logged from multiple rendering paths as work completes. Parallel workers and cache hits can alter order; repeated views and variants can repeat the same condition; and the command has no stable end-of-run summary or complete machine-readable report.

**Required behavior:** rendering errors that prevent a requested artifact remain immediate and fatal. Recoverable model, geometry, region-resolution, rotation-resolution, and clipping conditions are collected as structured diagnostics, deterministically merged after work completes, grouped for a concise console summary, and optionally written in full to a report file. Their presence does not change a successful exit code.

### F. Visibility through the board footprint and apertures — separate qualification bucket

**Candidate examples:** a component extending beyond the outer board edge and a component extending across an interior through-cutout.

These are not the same operation as clipping geometry at the top or bottom board surface. From the opposite view, geometry may be visible wherever the orthographic ray does not intersect board material: outside the outer outline or inside a through-cutout. The exact visibility rule is the union of the full component projection over non-board XY space and the surface-clipped component fragment over board-material XY space.

Add both cases to the purpose-built fixture if they are authored, but keep their acceptance results separate from through-board Z clipping. First characterize current mounting-side and opposite-side output. Promoting opposite-side edge/cutout visibility into this release requires an explicit scope decision and an algorithm that respects the outer outline, holes, and deterministic SVG/native composition; a Z half-space alone is not an acceptable partial fix.

### G. Region-local board material appearance — confirmed

**Symptom:** one saved 3D-view solder-mask color and one configured substrate color are painted across the entire board. Rigid-flex designs can have different exposed substrate and coating materials in different board regions.

**Required behavior:** determine the visible surface material independently for each board region and side. Render authored solder mask, coverlay, exposed copper, or exposed substrate using an explicit source/override precedence. Do not recolor component models, copper artwork, or silkscreen as a side effect.

### H. Bend-line virtual layer — requested

**Primary example:** Bluetooth Sentinel Flex Region 3, which contains six authored bend lines.

**Required behavior:** expose `BEND_LINES` as a selectable synthetic SVG layer with deterministic board-space geometry, styling, metadata, cache identity, layer-output support, and top/bottom mirroring consistent with other board annotations. Preserve angle, radius, fold index, and region identity as metadata where available. This is documentation artwork, not folded-board geometry.

### I. Silkscreen-to-film clipping — requested

**Symptom:** overlay artwork may extend beyond the board, across routed cutouts or physical holes, and over pads/mask apertures where fabrication would remove or clip ink.

**Required behavior:** offer an explicit policy that intersects top/bottom silkscreen with the matching physical film domain. The domain is inside board material, outside cutouts/physical bores, and outside all resolved film openings. Preserve a compatibility mode that renders the authored overlay without this additional clipping.

## Proposed algorithms

### A. Resolve model Z-rotation semantics against the authored body outline

#### Full 3D affine model

Represent every placement as a homogeneous 4 by 4 matrix acting on STEP column vectors. Keep these frames explicit:

- `S`: STEP payload coordinates after the selected native root-placement policy;
- `L`: Altium model/body coordinates containing the authored X/Y/Z rotations and DZ;
- `P`: placed component coordinates containing component rotation, model 2D placement, and mounting-side orientation;
- `B`: physical board coordinates, later including the applicable top or bottom surface elevation;
- `V`: view/camera coordinates, applied only after the physical pose is complete.

The current render transform can be stated as:

```text
B_M_S = T(delta_x_board, delta_y_board, signed_DZ)
        * Rz(component_rotation + model_2d_rotation)
        * Side(side)
        * Rz(resolved_model_3d_rotz)
        * Ry(model_3d_roty)
        * Rx(model_3d_rotx)
        * Root(step_root_placement)

Side(top)    = I
Side(bottom) = Rx(180 degrees)
```

`delta_x_board` and `delta_y_board` must be derived once from the stored model anchor and component anchor in their documented frames; they must not be rotated a second time. The later through-board work adds the mounting-surface Z translation outside this pose. The view matrix is also outside it, so changing from top to bottom presentation cannot mutate the physical model pose.

These placement matrices must remain rigid transforms: the upper 3 by 3 block is orthonormal with determinant +1. No data-dependent scale, shear, or post-projection SVG rotation is allowed. STEP unit conversion belongs to native model loading, not to Altium placement.

Before implementation, add synthetic non-commuting rotation cases to verify Altium's Euler order rather than relying only on cardinal rotations. Cover non-zero X, Y, and Z rotations, non-zero model 2D rotation, non-zero anchor offset, both sides, and preserved STEP root placement.

Treat the existing instance-space normalization and the raw footprint-local interpretation as two documented candidates:

- **instance-space candidate:** current behavior, converting stored `MODEL.3D.ROTZ` back to body-local space using component rotation and side;
- **footprint-local candidate:** retain the stored `MODEL.3D.ROTZ` as the body-local value while preserving all other component, side, offset, and axis rotations.

Evaluate each candidate's transformed native XY bounds against the component body's authored outline in board space. Score position and extents with a scale-aware geometric tolerance, then apply these rules:

1. Select the alternative only when it is a valid outline match and is uniquely, materially better than the current candidate.
2. Retain the current instance-space candidate when both are equivalent, including square, symmetric, and 180-degree-ambiguous cases.
3. Retain current behavior and emit one actionable diagnostic when neither candidate matches; do not guess an arbitrary quarter turn.
4. Include the selected interpretation and resulting matrix in illustration cache identity.
5. Share the resolver with assembly rendering so the two public render paths cannot disagree.

The comparison must use native model bounds after the complete candidate 3D transform, including root placement and X/Y rotations, not nominal STEP axes or pad bounds. Compare the resulting `(min_x, min_y, max_x, max_y)` and center with the authored component-body outline in the same board frame. Independently validate transformed Z bounds against standoff and overall height; Z does not select between candidates that differ only about Z, but it catches an invalid composition order. The authored component-body outline is the oracle because it describes this specific Altium body; pads are only a human-readable corroboration. A preflight bounds query is preferable. If the current direct native API cannot provide a bounds-only result efficiently, compare a bounded preflight approach with rendering the current candidate and retrying only on a demonstrated mismatch before choosing the architecture.

Keep ownership separated:

- Altium Monkey should expose the documented pose candidates and authored target envelope because it owns Altium field semantics;
- Geometer should apply a supplied generic affine matrix and return exact transformed bounds because it owns native model geometry;
- Cruncher should choose among the finite candidates using the accepted policy and include the semantic choice in render/cache identity.

This discriminator is supported by the characterization set: only IC1 through IC3 select the footprint-local candidate in the reporter sample, and no RT_SUPER body selects it. Add failure messages and tests for missing, degenerate, non-finite, and ambiguous outlines.

### B. Normalize to physical board space, then clip

Use one physical Z convention for all bodies:

- top board surface: `z = 0`;
- bottom board surface: `z = -T(x, y)`, where `T` is the applicable finished board-stack thickness;
- board material occupies the slab `-T < z < 0`;
- top view keeps transformed geometry in `z >= 0`;
- bottom view keeps transformed geometry in `z <= -T`.

For a top-mounted body, map authored mounting-surface coordinates to the top surface. For a bottom-mounted body, preserve the existing side reflection but anchor it to the bottom surface rather than collapsing both mounting surfaces onto zero. Apply the full authored component/body/model transform before the visibility clip.

Use authored bounds only as a conservative prefilter. Exact clipping and final bounds must use transformed native geometry because cached or malformed metadata can disagree with the STEP payload.

The clipping operation should be a generic Geometer half-space request applied after placement. It should:

- return an empty result when no geometry survives;
- produce correct section edges/caps according to an explicitly tested illustration policy;
- preserve source colors and material grouping;
- clip every member of a multi-body component before their native composition;
- return projected bounds from the same clipped result and use those bounds—not complete-model bounds—to map any normalized SVG canvas back into board coordinates;
- include the normalized plane and tolerance in memory and disk cache identity;
- use a small geometry tolerance for coplanar noise, not a visual-distance heuristic.

If the upstream native API cannot support clipping without reconstructing meshes in Python, stop for an architecture decision. Python-side tessellation and clipping would weaken the current one-pass native path, caching, materials, and performance and should not be introduced implicitly.

#### Geometer coordination request

Geometer issue 40 tracks the following generic illustration capability while its package contracts are being revised:

- accept one or more clipping planes in millimeters, with an unambiguous equation such as `dot(normal, point) - distance_mm >= -tolerance_mm` for the kept half-space;
- define the plane in world coordinates after STEP root placement and the supplied model/occurrence affine transform;
- apply clipping after tessellation/analytic lowering but before preparation, source bounds, HLR visibility, outlines, and shaded illustration, so every returned artifact describes the same fragment;
- support both direct model/analytic illustration and composed mesh paths, either through one shared prepare option or a native mesh-clip operation whose result feeds both mesh HLR and mesh illustration;
- retain original triangle material identity, interpolate new boundary vertices and normals deterministically, remove degenerate fragments, and compact unused geometry;
- make empty output an ordinary successful result rather than an operation error, with an explicit empty indication or nullable bounds rather than fabricated six-zero bounds; Cruncher must be able to omit the fragment without letting an invisible origin-sized result affect placement or paint ordering;
- make `cap_policy: "none"` the only initially supported policy and include it in request/result identity; the exposed cut becomes an ordinary mesh boundary for HLR/outlines, and synthesized section faces remain out of scope until Geometer defines a deterministic cap-material policy;
- validate finite coefficients, nonzero normals, tolerance, maximum plane count, and work limits.

With Toon's normalized local board-region frame, the two requests are:

```text
top fragment:    normal=(0, 0,  1), distance_mm=0
bottom fragment: normal=(0, 0, -1), distance_mm=T
```

where the bottom surface is `z=-T`. Cruncher owns the board-derived plane values and includes the normalized planes, tolerance, and cap mode in its caches; Geometer owns generic geometry filtering and its deterministic result.

Cross-side fragment development may start before publication against an exact Geometer source revision that closes issue 40 across the direct model/analytic path, composed mesh illustration and HLR path, executable IPC, static SDK, and supported WASM transports. Prefer an ephemeral local editable override for workstation integration so `pyproject.toml` and `uv.lock` retain the released dependency; if repeatable CI is required before publication, use a uv source override pinned to an immutable Git commit and record that commit with the test evidence. Do not vendor or reproduce the clipper in Cruncher. Release signoff remains gated on a published Geometer package: update the exact `wn-geometer` pin in `pyproject.toml`, regenerate `uv.lock` with uv, remove any temporary source override, and rerun the complete transport and release matrices.

The current sibling-checkout development command is:

```powershell
uv run --with-editable ..\geometer pytest -q tests\L3_public_workflows\test_L3_005_pcb_illustration.py::test_rt_through_board_model_uses_clipped_fragments_on_both_sides
```

For Rack, which invokes nested uv commands, use a disposable development environment and propagate no-sync:

```powershell
uv pip install --editable ..\geometer
$env:UV_NO_SYNC = "1"
uv run rack run --all
```

Restore the locked environment with `uv sync --all-extras` after qualification.

The exact Geometer source revision must be recorded with qualification results; a moving branch name is not sufficient evidence.

#### Overhang boundary

No Geometer change is needed merely to show a component that extends beyond the board outline in its mounting-side view. Do not apply the board's 2D outline clip to component illustration layers.

Seeing that overhanging portion from the opposite board side is different. For an orthographic top/bottom view, geometry is visible when it is either outside the board material's XY footprint or beyond the near board surface. Interior through-cutouts are holes in that material footprint and follow the same ray-visibility rule. A single Z half-space cannot express this union.

The purpose-built fixture should independently characterize:

1. a body crossing the outer board outline;
2. a body crossing an interior through-cutout;
3. each body's mounting-side view;
4. each body's opposite-side view.

The new stress fixtures establish that the SVG-domain composition is sufficient
for these orthographic Toon views; no additional Geometer capability is needed.
Let `B` be the exact board-material XY domain already used by the substrate mask,
including negative cutouts, slots, and bores. For an opposite-mounted model `M`,
compose two logically disjoint images:

```text
surface fragment = Project(ClipZ(M)) intersect B
aperture fragment = Project(M) intersect complement(B)
visible result = surface fragment union aperture fragment
```

Render both terms from the same placed model and camera, retaining each native
projection's own origin and scale. Apply the board-occlusion mask to the surface
fragment and its complement to the full-model aperture fragment. The mask extent
must include the expanded illustration canvas, not only the original board
canvas. Reuse the shared board topology but resolve hole visibility per viewing
side: tented, blind, filled, and capped bores are occluders; routed cutouts,
NPTHs, and genuinely open through bores are apertures.

SVG antialias coverage means two complementary masks do not form a perfectly
binary premultiplied-alpha merge at their boundary. The initial implementation
accepts a possible one-pixel seam for opaque Toon models and treats transparent
materials as not yet exact. Do not advertise exact transparent composition until
raster tests establish an explicit merge policy.

The current `BOARD_CUTOUTS`, `DRILLS`, and `SLOTS` layers are review annotations,
not board material. Because `ILLUSTRATION_TOP/BOTTOM` paints later, an opaque
aperture fragment naturally covers their hatch/gray fill where a component is
physically present. A clean physical Toon preset may omit those annotation layers
entirely while standalone documentation exports retain them.

Use a conservative XY intersection against `complement(B)` to avoid generating a
full-model aperture projection for ordinary components. One local board envelope
may supply `ClipZ` only when every board-material region intersecting the body has
the same normalized thickness. Different-envelope intersections retain the safe
diagnostic path; the aperture-only term remains independently well-defined.

Initial acceptance covers perpendicular orthographic views. Perspective views,
oblique sight through a finite-thickness hole wall, cavities, blind/buried holes,
and inter-component occlusion remain outside this SVG composition contract.

### Board thickness authority

Use the existing Altium Monkey semantic stack and envelope path rather than parsing or summing serialized stack rows in Cruncher:

```python
stack_document = AltiumLayerStackDocument.from_pcbdoc(pcbdoc)
resolved_stack = stack_document.to_resolved_layer_stack()
envelope = resolved_stack.stack_envelope_for_board_region(region)
```

Altium Monkey remains the authority for the parsed regions, saved-stack/substack identities, resolved layer membership, and physical envelopes. Its envelope's enabled physical rows, `top_z_mils`, `bottom_z_mils`, `total_thickness_mils`, and Z-zero policy are authoritative. Cruncher temporarily owns only the missing spatial operation: determine which authored board region contains a board-space XY point and map that region's `layerstack_id` to its resolved substack envelope. Do not manually sum raw V9 cache rows and do not equate a V7 saved-layer identifier with physical thickness.

Normalize the envelope's local-midplane coordinates into Toon's proposed top-surface coordinate system by subtracting `top_z_mils`:

```text
z_toon = z_envelope - envelope.top_z_mils
top_surface = 0
bottom_surface = envelope.bottom_z_mils - envelope.top_z_mils
               = -envelope.total_thickness_mils
```

#### Temporary Cruncher region index

Build one immutable region-envelope index per input document and reuse it across components, views, variants, and workers:

1. Construct `AltiumLayerStackDocument` and `ResolvedLayerStack` once.
2. Read region outlines and hole contours from the semantic board-region records. Convert Altium internal coordinate units through one established unit helper; do not scatter a numeric conversion constant through renderer code.
3. Resolve each region's `layerstack_id` to its substack and physical envelope, retaining source region identity for diagnostics.
4. Precompute board-space bounding boxes and use them as the first query filter.
5. Run a tolerance-aware point-in-polygon test, including holes, for the remaining candidates. Treat a point on an outer or hole boundary as a boundary match rather than allowing floating-point noise to choose a side.
6. If exactly one region contains the point, return its region identity and envelope. If multiple matches have the same normalized envelope, return that envelope with a deterministic canonical region identity. If matches have different envelopes, return a typed ambiguous result; never pick by record order. Return a typed no-region result outside all authored regions and a typed invalid-region result for unsupported or malformed contours.

The initial implementation may lower already-parsed line-segment contours only if characterization confirms that these fixtures contain no unresolved arc semantics. If Altium Monkey exposes a normalized polygonal outline, use it. Otherwise preserve enough source information to diagnose an unsupported contour rather than silently approximating it.

Use the component/body anchor to obtain the initial local envelope, then conservatively qualify the whole transformed model footprint. Query every board region whose XY bounds intersect the model's transformed XY bounding rectangle. If all intersecting regions normalize to the same envelope, one pair of Z half-spaces is safe. If a different envelope intersects that conservative rectangle, retain mounting-side-only rendering for that body and emit `body-spans-board-envelopes`. This can produce a conservative false negative near a concave boundary, but cannot apply the wrong board thickness. A later exact polygon/intersection refinement may recover those cases without changing the safety contract.

Bluetooth Sentinel provides the shipping oracle:

- Region 2 `Rigid`: query point `(60605.31505151517, 40082.82176948154)` mil, expected thickness `32.1455` mil;
- Region 1 `Rigid`: query point `(60605.31313726855, 38830.56313808814)` mil, expected thickness `32.1455` mil;
- Region 3 `Flex`: query point `(60590.162861537574, 39449.11769487287)` mil, expected thickness `3.3267` mil.

Add synthetic tests for outer boundaries, hole boundaries, outside-board queries, overlapping equal-envelope regions, overlapping different-envelope regions, malformed outlines, and unit conversion. Keep the query internal rather than making the temporary duplication a public Cruncher API.

[Altium Monkey development issue 95](https://github.com/wavenumber-eng/altium_monkey_dev/issues/95) specifies the permanent source-aware board-coordinate query. This release does not wait for it. When that API is released, replace the temporary spatial index, run the same Bluetooth and synthetic cases as parity tests, and delete the duplicate Cruncher implementation rather than maintain two PCB-semantic authorities.

The resolved fixture envelopes include solder mask. Use those finished outer surfaces initially, because they are the public physical envelope, but capture one native-Altium fixture to confirm that STEP standoff zero is referenced to that outer finished surface rather than the adjacent copper surface. Do not silently drop mask rows to obtain a preferred nominal thickness.

### Region-local board appearance

Build a `BoardSurfaceAppearanceIndex` beside the region-envelope index. For each `(region, side)`, walk the enabled resolved substack from the requested outer surface inward and record the first physically visible surface class and its source identity:

- solder mask;
- coverlay/bikini coverlay;
- surface finish or exposed copper;
- exposed dielectric/substrate;
- unsupported or unresolved surface.

Record the first enabled copper row independently from the visible polymer or substrate class. A composed surface view uses `SURFACE_COPPER_TOP` or `SURFACE_COPPER_BOTTOM`: group valid regions by resolved physical copper layer, render each raw layer once, and clip it to the union of regions for which it is the outer conductor. If regional stack data is invalid or unavailable, fall back to literal `TOP` or `BOTTOM`; never render every candidate layer without regional clipping. Individual raw physical-layer exports remain literal and unchanged.

Use the AD26 C# `LayerType` and bikini-coverlay classification as the semantic oracle, cross-checked against Altium Monkey's public enums and source-aware layers. Do not infer coverlay solely from a material-name substring. In particular, a flex-enabled solder-mask record with film dielectric type or positive coverlay expansion is distinct from ordinary solder mask, and coverlay aperture/expansion behavior must be characterized before reusing solder-mask opening rules.

The installed Altium Monkey model retains material names but does not expose an authored material color for Bluetooth Sentinel. Research the V7/StackupX material records and `Material.Color` representation against the C# material-library and serializer paths. Normalize a valid authored color to sRGB plus alpha without treating WPF/ARGB text, Win32 `COLORREF`, and CSS hex as interchangeable. Entity references that require an unavailable external material library resolve as unavailable, not as an invented color.

If Altium Monkey does not yet expose the required typed material appearance, file a separate upstream issue and implement only the smallest temporary Cruncher reader that can consume source-preserved material records without hard-coded binary offsets. Gate that reader with fixture vectors and typed failure results, and replace it with the future Monkey API. Do not expand issue 95's region-envelope contract into an unrelated color API after the fact.

Recommended color precedence, highest first:

1. explicit region/side/material override from Toon config;
2. existing explicit `soldermask_film.color` or `board_substrate.color` override when applicable;
3. authored stack/material color attached to the resolved visible row;
4. saved 3D-view color for the matching global display class, such as top/bottom solder mask or board core;
5. configured material-class palette;
6. the documented Cruncher fallback.

An explicit global style color preserves today's single-color behavior. `auto` enables regional source resolution. The initial TypeSpec-owned surface consists of `board_substrate.color`, `rigid_color`, and `flex_color`, plus `soldermask_film.color` and `coverlay_color`. This deliberately avoids a general material/region rule language until an authored-color corpus demonstrates that its extra matching and ambiguity semantics are needed. Stable region/substack and material identity remain SVG metadata for later policy expansion.

The built-in material-class palette includes separate `flex_substrate` and `coverlay` amber/polyimide-family color defaults because exposed polyimide substrate and coverlay are distinct surface classes. The initial contract keeps the existing common film opacity; a separate coverlay-opacity control is deferred until a committed coverlay fixture provides an optical oracle. These values are explicitly `cruncher_fallback`, never `authored_material`, and must not be selected merely because a free-form material name contains `Polyimide` or `Kapton`; selection follows the resolved surface class and rigid/flex substack semantics.

Render substrate and surface film as deterministic region paths, not one board-wide fill. Clip each path to its authored region, board outline, holes, and cutouts. Apply solder-mask apertures only to regions that actually use solder mask; apply separately characterized coverlay openings to coverlay regions; emit no coating path where the selected substack has none. Retain copper and substrate below the film in the existing draw order. Include appearance source, normalized color/alpha, region identity, and policy in cache identity and optional SVG metadata.

Bluetooth Sentinel acceptance must demonstrate more than two arbitrary configured colors: it must identify which rows are visible on each side of Rigid Regions 1/2 and Flex Region 3, distinguish `Solder Resist`, `FR-4`, and `Polyamide`, and record whether the saved file contains an authored coverlay color or only a fallback/display color. A native-Altium screenshot may be used locally as an oracle but is not a committed fixture requirement.

### Bend-line virtual layer

Add the synthetic token `BEND_LINES` and a `bend_lines` style with at least `enabled`, `color`, `opacity`, `line_width_mm`, `line_style`, `dash_length_mm`, `dash_gap_mm`, and nonnegative `extension_mm`. Support solid and dashed presentation without changing the source bend definition. A zero extension terminates at the owning region outline. A positive extension first intersects the normalized infinite bend axis with the owning region polygon, selects the chord containing or nearest the authored segment, and extends both chord endpoints by the configured absolute distance. Expand the SVG viewBox by the overrun plus half the stroke width and do not board-clip that overrun. Invalid or degenerate intersections retain the authored, region-clipped fallback. Keep the layer available to explicit views and `layer_outputs.include_special_layers`; decide separately whether the default Toon rigid-flex preset includes it.

Use `fold_index` as the stable authored grouping key available in the region payload. Preserve region index/name, source index, fold index, angle, and radius as SVG metadata. Optional labels may derive from fold index/angle or from an explicit Cruncher config override, but must not be described as an Altium-authored bend name. Per-fold color/label overrides should match `(region selector, fold_index)` so paired lines belonging to one fold receive the same presentation. Do not match by array position alone. Defer automatic authored-name import until Altium Monkey exposes a source-aware record that works even when the optional Board6 cache is absent.

Read bend geometry from each `AltiumStackRegion.bending_lines`, not from the Board6 cache. Convert endpoints from the documented region-local internal-unit frame into board coordinates using an explicit source region transform. Bluetooth Sentinel suggests a translation by the region source origin, but that observation is only a fixture characterization; do not generalize `min(outline)` into the format contract without confirming it against the Altium Monkey parser and AD26 behavior. If the current semantic model omits the required origin/transform, add a narrow temporary adapter and request the missing typed field upstream.

Canonicalize and deduplicate lines by region identity, source order/fold identity, transformed endpoints, angle, and radius. Preserve source direction for metadata but render coincident duplicates once. Clip the painted stroke to the associated flat board region/domain so an authored line can span the flex region without painting beyond its physical extent. Reject non-finite or incomplete endpoints with a structured diagnostic. Emit SVG metadata for region, fold index, angle degrees, radius mils, and source identity. Bottom views follow the existing whole-view mirror policy; do not independently reverse bend geometry.

`BEND_LINES` is annotation only. It must not rotate or deform region paths, layer artwork, holes, components, or model geometry, and it must not participate in board/component bounds except as an explicitly requested visible SVG layer.

Bluetooth Sentinel must render six valid Region 3 lines at their expected board coordinates, retain the two `-90` degree, two `-25` degree, and two `-145` degree records and their radii/fold indices, and render no invented lines for Regions 1 and 2. Absence of the optional Board6 cache must not suppress the layer.

### Silkscreen surface clipping

Factor the current solder-mask aperture construction into a shared, side-aware `SurfaceFilmDomain` builder. It returns reusable SVG mask geometry describing where physical surface film exists after board outline, region topology, cutouts, bores, saved mask/coverlay apertures, rule expansions, tenting, and regional coating classification. The film painter and silkscreen clipper consume the same immutable domain; they must not depend on one another's SVG element IDs, output order, or whether the film layer is itself requested.

Add a TypeSpec-owned per-view/global option such as `styles.silkscreen_surface.clip_mode` with:

- `none`: preserve authored overlay behavior;
- `board`: clip only to board material footprint, including cutouts and physical holes;
- `film`: intersect painted silkscreen with the matching top/bottom physical film domain, thereby removing it over film apertures, exposed pads, routed openings, and cutouts.

Use `none` as the compatibility default unless the release decision explicitly promotes `film` for Toon presets. Apply the SVG mask to the completed physical `TOPOVERLAY` or `BOTTOMOVERLAY` group so tracks, arcs, regions, fills, strings, component-owned graphics, and board-owned graphics follow one rule. SVG masking operates on painted strokes/text and therefore avoids separately polygonizing every silk primitive. Generate view-unique deterministic IDs and include the film-domain identity and clip mode in fragment caches.

`film` respects tenting: a tented via remains film and therefore does not automatically erase silk, while pad/via apertures and physical cutouts do. When a region has no surface film, the `film` policy clips silk from that region; users wanting ink on bare substrate select `board`. Unsupported aperture rules produce the existing structured nonfatal diagnostic and omit only unresolved aperture geometry, matching the film renderer's fail-safe contract.

Keep this SVG composition in Cruncher. Geometer is unnecessary for flat Toon/PCB-SVG output and should not receive board-specific mask semantics. If a later true-3D board renderer needs physical ink clipping, define a generic profile intersection or scene-surface contract separately.

### Structured diagnostic aggregation

Replace render-time warning strings with a stable internal record. The exact Python name is implementation detail, but the record needs at least:

- stable `code`, `severity`, `category`, and `producer` fields;
- input/board identity, variant, view when view-specific, component designator, body index, and model identity when known;
- a human-readable message and optional structured detail;
- a stable deduplication key and occurrence count.

Initial categories cover `missing_model`, `unsupported_model`, `invalid_model_geometry`, `geometer_geometry`, `region_resolution`, `rotation_resolution`, and `clipping`. Model-less warnings are component-scoped and side-independent. A Geometer warning should retain `producer = "geometer"`; until Geometer supplies stable codes, use a generic code plus the exact upstream message as the grouping signature rather than heuristically parsing its prose.

`PcbSvgRenderJob` owns the collector. Workers return diagnostics beside their artifacts, and the parent merges them in stable source order after all requested work completes. Cache entries must replay the same structured diagnostics as cold execution. Deduplicate by structured identity, not formatted text, so top/bottom views, variants, retries, and cache paths do not change counts accidentally.

At command completion:

- default console behavior is a concise `Nonfatal warnings` summary grouped by category and code, with counts of affected components/bodies/models and a bounded sample of designators;
- `--warnings summary|all|none` controls console presentation, with `summary` as the default;
- `--warning-report PATH` writes the complete deterministic JSON report regardless of console mode;
- nonfatal diagnostics do not change a successful exit status; fatal input, contract, and artifact failures remain immediate errors.

The report is a public emitted payload and must be authored under `src/tsp/altium_cruncher/outputs` with a versioned discriminator such as `toon.warning_report.a0`; the CLI options and help/defaults must likewise begin in the owning TypeSpec manifests. Document deterministic ordering, path collision/overwrite behavior, and whether an empty report is written when explicitly requested. Do not hand-edit generated DTOs, schemas, bindings, validators, or field guides.

## Decision ledger

1. **Rotation resolver — decided:** select between the two supported affine candidates against the authored component-body outline; never use a global formula change or designator exception. Final directional qualification still requires the purpose-built asymmetric fixture.
2. **Bounds architecture — decided:** mesh-backed bodies compare already available placed bounds; the direct native path retries only when the current candidate fails the outline check. The alternative result and diagnostics participate in normal cache behavior.
3. **Purpose-built fixture acceptance:** after the new board is authored, confirm that it is safe to commit and identify which optional edge-overhang and interior-cutout cases it contains. The reporter PcbDoc and screenshot are explicitly prohibited repository content.
4. **Overhang release scope — decided and implemented:** orthographic Toon includes opposite-side visibility outside the outer outline and through true open apertures using Cruncher-owned SVG-domain composition. Perspective/oblique wall occlusion remains out of scope.
5. **Mounting-surface reference:** confirm with a native-Altium fixture whether body standoff zero uses the resolved outer finished surface, including solder mask, or a different layer reference.
6. **Cross-region fallback — decided:** equal-envelope partial coverage reuses one Z plane and the SVG board domain; unlike or invalid envelopes retain the conservative surface fallback while the full projection may still appear through the exact open-space complement. Per-region Z composition is a later refinement.
7. **Diagnostic UX — decided:** use `--warnings summary|all|none` with `summary` as the default plus optional full JSON `--warning-report PATH`; missing-model diagnostics are limited to fitted components selected for the active variant.
8. **Appearance compatibility default — decided:** amber `flex_substrate` and `coverlay` fallbacks are `#D18B28`; new Toon configs use regional `auto`, while existing explicit colors remain global overrides.
9. **Bend-line preset — decided:** `BEND_LINES` is a selectable, opt-in virtual layer rather than an implicit member of every Toon view. The Bluetooth qualification requests it explicitly; rendering remains flat 2D annotation without folding.
10. **Silkscreen clipping default — decided:** `none|board|film` is implemented; compatibility is `none` for general PCB-SVG configs and `film` in newly generated Toon illustration presets.
11. **Bend-line metadata and overrun — decided:** angle, radius, fold index, and endpoints are authoritative for Bluetooth; per-line color is not authored and name is unavailable when the optional Board6 cache is absent. Use fold index for deterministic grouping and config-authored labels/colors. `extension_mm=0` ends at the owning region boundary; the default 1 mm extends each end by the same absolute distance and expands the SVG viewBox accordingly.

## Execution detail

Work packages 1 through 7 can start before Geometer releases clipping. Work package 8 can complete through request construction, cache identity, and mocked/contract testing, then pause at the real native call. Geometer is on the critical path only for end-to-end clipped-fragment rendering and its performance qualification.

### 1. Establish fixtures and characterization tests

- Keep the reporter PcbDoc and IC3 screenshot outside the repository. They may be inspected locally during research but must not be copied, transformed into generated repository artifacts, or referenced by machine-specific paths in committed tests.
- Create a small user-authored regression board with one case per behavior: fitted/no-model, through-board, and asymmetric IC3-equivalent rotation. If provided, add separate outer-edge-overhang and interior-through-cutout-overhang cases.
- Give the purpose-built board its own fixture name and source manifest. Record its authoring origin, explicit commit authorization, import date, byte size, SHA-256, expected designators, stack thickness, and case-to-requirement mapping.
- Make the rotation case asymmetric enough to assert pin-1 direction numerically from pads/body outline/model geometry; the committed test must not depend on the local screenshot.
- Retain the committed Bluetooth Sentinel fixture and source manifest as the production rigid-flex region-query oracle. Verify its byte size and SHA-256 before tests consume it.
- Add a focused characterization asserting the authored horizontal outline, current quarter-turned result, footprint-local candidate, and directional marker for the purpose-built IC case. Retain the reporter's 9.9 by 6.0 mm measurements only as research evidence in this plan.
- Add tables covering the candidate-selection counts for the reporter sample and RT_SUPER.
- Assert that the purpose-built no-model component remains omitted and produces the expected grouped diagnostic. U1, P2, J2, and FB1 remain local research evidence only.
- Characterize any authored edge-overhang and cutout-overhang parts separately on both views; do not treat a half-space-only result as success for opposite-side aperture visibility.

### 2. Implement the temporary board-region envelope index

- Construct and cache the semantic stack document, resolved stack, region bounds, containment contours, substack joins, and normalized envelopes once per PCB.
- Implement typed success, no-region, ambiguous-region, and invalid-region outcomes with deterministic equal-envelope tie handling.
- Verify the three Bluetooth region points and exact 32.1455/3.3267 mil envelopes, then add synthetic boundary, hole, overlap, malformed-outline, and unit-conversion tests.
- Use the union envelope of a complete valid region partition when computing the board-outline canvas. Retain the legacy outline bounds as a compatibility baseline and fall back to them if any region is invalid; assert Bluetooth's 82 by 57 mm view box including the configured 1 mm margin.
- Add the conservative transformed-body-bounds qualification. A body touching different envelopes uses mounting-side-only rendering and contributes one structured diagnostic.
- Keep this implementation internal and link its removal gate to Altium Monkey development issue 95.

### 3. Characterize and implement region-local board appearance

- Record Bluetooth's saved 3D `COLORREF` values, resolved visible rows, material names, substack membership, and any source-preserved material records for each side/region.
- Verify V7/StackupX layer-type, material, color, coverlay, and expansion meanings against Altium Monkey enums and the specified AD26 C# reference. Add small serialization vectors rather than depending only on the large fixture.
- File a focused Altium Monkey issue if typed material color or region-to-surface classification is not public. Implement a temporary Cruncher reader only for source-preserved records with established structure; do not use binary offsets or guessed name-to-color mappings.
- Add the regional surface-appearance index, config precedence, ambiguity handling, diagnostics, cache identity, and region-path rendering for substrate and surface film.
- Verify explicit single-color compatibility, `auto` regional behavior, unavailable external material references, invalid colors, alpha normalization, separate amber flex-substrate/coverlay fallbacks, no-film flex regions, and distinct coverlay aperture behavior.

### 4. Add the BEND_LINES virtual layer

- Verify and document the region-local-to-board transform with Bluetooth and a small synthetic translated-region vector.
- Add the synthetic token, stable layer id, renderer, style model/defaults/help, per-layer output integration, SVG metadata, fragment/cache keys, and mirror behavior.
- Add independent dash/gap sizing and region-boundary extension. Expansion must be geometric in board millimetres, grow the output canvas when necessary, and preserve the zero-extension clipped behavior.
- Add optional fold-index-derived labels and `(region selector, fold_index)` presentation overrides without claiming the labels or colors are authored in Altium.
- Test six Bluetooth Region 3 lines, paired fold indices, empty rigid regions, invalid endpoints, duplicate records, concave/multi-chord region intersections, holes, zero/positive extension, canvas growth, line/dash/gap styling, global and per-fold color/opacity/width, optional labels, standalone layer output, top/bottom compositions, and the absence of any board/component deformation.

### 5. Add configurable silkscreen surface clipping

- Extract one shared side-aware surface-film-domain builder from the existing solder-mask film renderer.
- Add `silkscreen_surface.clip_mode = none|board|film` through TypeSpec and apply the resulting SVG mask to completed overlay groups.
- Verify all supported silk primitive types, strings, component/board ownership, board edges, routed cutouts, plated and non-plated holes, SMD/THT pads, tented/untented vias, positive/negative expansions, region-local no-film/coverlay areas, standalone overlay outputs, and deterministic mask IDs.
- Compare SVG size and render time before enabling `film` in a preset; share cached aperture geometry rather than rebuilding it per silk category.

### 6. Implement and verify rotation resolution

- Add a shared transform resolver that can evaluate both supported Z-rotation interpretations against an authored component-body outline.
- Prefer a native bounds-only preflight if it preserves the direct source path and model cache efficiency; otherwise document and benchmark the bounded retry design before implementation.
- Keep current behavior for ambiguous or invalid outlines and issue a deduplicated diagnostic only when no candidate matches.
- Use the resolved transform in both Toon and assembly rendering and in their cache identities.
- Verify IC1 through IC3, representative passives, U4, repeated RT_SUPER models, top-side bodies, bottom-side bodies, square models, 180-degree ambiguity, non-zero offsets, and multi-body components.
- Check pin-1 direction against the native Altium oracle rather than accepting extent agreement alone.

### 7. Implement structured end-of-run diagnostics

- Introduce the structured diagnostic record and collector; adapt existing `IllustrationJob.warn()`, append-only warning paths, and direct-model/Geometer warning paths without losing information.
- Return diagnostics from workers and caches, merge in deterministic source order, and deduplicate across views, variants, retries, and cache hits by structured identity.
- Add fitted-component `missing-renderable-model` diagnostics and separate unsupported, unreadable, invalid, and degenerate geometry codes.
- Add the concise end summary, console verbosity option, and optional full versioned JSON report through the TypeSpec-owned public surface.
- Test cold/warm cache, one/multiple workers, repeated variants/views, `summary|all|none`, explicitly requested empty reports, report-path failures, and unchanged successful exit codes.

### 8. Introduce the later surface and clipping contracts

- Consume the already-built region-envelope index; do not add a second thickness parser or index in the clipping layer.
- Assert 16.2 mil for the reporter fixture and 40.312 mil for RT_SUPER, including the resolved physical-row membership and top/bottom elevations.
- Normalize each selected local envelope from its declared Z-zero policy to Toon's top-surface-zero board frame.
- Verify that Bluetooth Sentinel bodies wholly contained in rigid or flex regions receive the appropriate local clipping planes; bodies conservatively spanning unlike envelopes retain mounting-side rendering and warn.
- Validate solder-mask inclusion and the STEP mounting-surface reference against a native Altium rendering.
- Integrate first against the exact unpublished Geometer revision using an ephemeral local editable override; record the revision and exercise every supported transport without committing a machine-local path.
- If pre-publication CI must reproduce the integration, use a temporary uv source override pinned to an immutable Git commit rather than a branch or floating tag.
- Before Cruncher release signoff, consume the published Geometer package, update the exact dependency pin, regenerate the lockfile with uv, and remove the temporary override.
- Request `cap_policy: "none"` and test that the section boundary participates consistently in HLR/outlines without a synthesized filled cap.
- Version cache serialization if the request shape or renderer semantics change.
- Define empty-fragment warnings and metadata without turning an expected invisible fragment into an error.

### 9. Update through-board collection and rendering

- Replace side-exclusive body eligibility with conservative physical visibility eligibility.
- Construct one board-space transform per authored body and derive both views from it.
- Submit only candidate fragments to native clipping; discard empty results.
- Compose surviving bodies per component in original source/material order.
- Sort component symbols using clipped visible bounds, not unclipped source-side extrema.
- Preserve deterministic output under different worker counts and cache hit patterns.

### 10. Contracts, documentation, and signoff

- Update `docs/design/cli/pcb-svg.html`, `docs/design/cli/toon.html`, and the relevant API design sections for accepted rotation resolution, local board thickness/appearance, bend lines, silkscreen clipping, cross-side behavior, and grouped diagnostics. Retain bodyless omission while documenting its nonfatal diagnostic.
- Author public metadata/config changes in `src/tsp/altium_cruncher`; run `npm ci --ignore-scripts`, `npm run generate:contracts`, `npm run check:contracts`, `npm run check:typescript`, and `npm run check:browser` when applicable.
- Run focused illustration, component-layer, cache, worker-determinism, RT_SUPER, Bluetooth Sentinel, and purpose-built regression tests. Keep reporter-sample checks local and manual only.
- Benchmark cold/warm cache and one/multiple worker configurations before accepting the native clipping path.
- Run `uv run --extra test rack run --all`, build, Twine check, install test, and `wn-dev-std check . --format json` for release signoff.

## Verification matrix

| Case | Expected top view | Expected bottom view | Protects |
| --- | --- | --- | --- |
| Local-only reporter J3 | Only pins beyond the top surface | Authored bottom package and pins outside the bottom surface | Manual qualification only; no reporter artifact committed |
| Purpose-built through-board part | Only geometry beyond the top surface | Authored bottom package and geometry outside the bottom surface | Shipping regression for no whole-model duplication and retained offset |
| RT_SUPER T1 and rotated peer | Top protruding pin fragment | Bottom protruding pin/body fragment | Repeated instance transforms and cross-side clipping |
| Reporter physical stack | 16.2 mil total; +8.1/-8.1 mil source envelope normalized to 0/-16.2 mil | Same physical envelope | Source-aware finished thickness; no raw-row summation |
| RT_SUPER physical stack | 40.312 mil total; +20.156/-20.156 mil source envelope normalized to 0/-40.312 mil | Same physical envelope | Masks, copper, and dielectrics retained |
| Bluetooth Region 1/2 rigid query | 32.1455 mil local envelope | Same local envelope | Region/substack join and rigid thickness |
| Bluetooth Region 3 flex query | 3.3267 mil local envelope | Same local envelope | Local flex thickness and unit conversion |
| Equal-envelope boundary/overlap | Deterministic canonical region and common envelope | Same result | No source-order dependence |
| Different-envelope boundary/overlap | Typed ambiguity; no cross-side fragment | Mounting-side behavior plus one diagnostic | No guessed local thickness |
| Body wholly inside one Bluetooth region | Clip against that region's local surfaces | Clip against that region's local surfaces | Shipping rigid-flex/local-thickness behavior |
| Body conservatively spanning rigid and flex regions | Mounting-side behavior only | Mounting-side behavior plus one grouped diagnostic | Safe initial cross-region fallback |
| Shallow top package with small negative standoff | Normal top body | Nothing unless it reaches the physical bottom surface | Board-thickness false-positive control |
| Local-only IC1/IC2/IC3 | Not applicable: bottom-side bodies | Horizontal 9.9 by 6.0 mm body; IC3 pin 1 at upper right beside the vertical reference mark | Manual qualification only; no screenshot or reporter PcbDoc committed |
| Purpose-built asymmetric IC part | As authored | Correct horizontal bounds and numeric pin-1/reference-marker direction | Shipping mixed-Z-rotation regression without reporter content |
| Bluetooth Sentinel committed fixture | Region 1/2 map to Rigid and Region 3 maps to Flex | Same semantic mapping | One physical stack, two substacks, three regions, and future Monkey parity |
| Bluetooth rigid Regions 1/2 appearance | Resolve the first visible top row and its color provenance | Resolve the first visible bottom row and its color provenance | Region-local stack traversal and source attribution |
| Bluetooth flex Region 3 appearance | Resolve exposed Polyamide/copper/coating state without borrowing the rigid solder resist | Same independent bottom-side resolution | No global solder-mask assumption across rigid-flex regions |
| Explicit global substrate/mask color | Preserve the configured single-color result | Preserve the configured single-color result | Backward-compatible override precedence |
| Invalid or unavailable authored material color | Deterministic fallback plus one structured diagnostic | Same policy and normalized report entry | No guessed name-to-color mapping or parser crash |
| Distinct solder-mask and coverlay vector | Apply solder-mask aperture semantics only to solder mask | Apply separately characterized coverlay expansion/opening semantics | AD26/Monkey enum fidelity |
| Bluetooth Region 3 bend lines | Six deterministic board-space lines with angle, radius, fold, and region metadata | Mirrored presentation of the same six physical annotations | Region-local bend source and coordinate transform |
| Bluetooth Regions 1/2 bend lines | No bend-line geometry | No bend-line geometry | No leakage from flex region or top-level cache |
| Standalone `BEND_LINES` output | Stable layer ID, bounds, metadata, and cache bytes | Same contract under bottom-view mirroring | Virtual-layer composability |
| Silkscreen `clip_mode=none` | Authored overlay remains unchanged | Authored overlay remains unchanged | Compatibility mode |
| Silkscreen `clip_mode=board` | Remove ink outside the board, in routed cutouts, and in physical bores | Same side-aware board-domain rule | Board topology clipping independent of film |
| Silkscreen `clip_mode=film` | Also remove ink over resolved top-film apertures, exposed pads, and untented vias | Use bottom-film apertures and bottom tenting | Shared side-aware film domain |
| Silkscreen over no-film flex region | Remove ink in `film`; retain it in `board` | Same policy on bottom side | Explicit distinction between bare substrate and coated surface |
| Silkscreen over coverlay region | Use characterized coverlay openings, not solder-mask expansion by assumption | Same policy on bottom side | Coverlay-specific aperture semantics |
| Representative passives and U4 | Not applicable: bottom-side bodies | Remain aligned with their authored outlines | No global-formula regression |
| Purpose-built fitted part with no renderable body | No illustration; one side-independent diagnostic | No duplicate diagnostic | No invented geometry; useful omission reporting |
| Purpose-built outer-edge overhang, mounting side | Complete authored overhang remains visible | View depends on authored mounting side | No accidental board-outline clipping |
| Purpose-built outer-edge overhang, opposite side | Non-board-footprint portion visible | Board-material portion follows surface clipping | SVG board-domain/complement composition |
| Purpose-built interior-cutout overhang, opposite side | Portion visible through the through-cutout | Board-material portion follows surface clipping | Cutout topology and ray visibility |
| `projection-test` J1/J2/J7 | Complete mounting-side models across the outer edge | Full models only in non-board XY plus any surface-clipped board-domain fragment | Edge/straddle visibility without board overpaint |
| `projection-test` J4 | Surface-clipped top fragment plus full geometry visible through the interior cutout | Complete bottom mounting-side model | Interior-cutout complement mask |
| `usb-edge` J1 | Complete top mounting-side straddle connector | Full connector outside the board profile plus bottom-surface fragment over board material | Real-world edge/bid-plane straddle placement |
| `usb-edge` D1 | Full lens visible through the 1.6 mm NPTH slot plus only the top-surface fragment over board material | Complete bottom mounting-side LED | Recessed reverse-mount aperture visibility |
| Geometer degenerate-geometry warnings | No streaming warning during workers | One deterministic grouped end summary and full report entries | Stable nonfatal reporting |
| Cold/warm cache and 1/N workers | Identical diagnostic groups, ordering, and counts | Identical report bytes | Cache and concurrency determinism |
| P1 and JP2 | All visible member-body fragments in source order and registered to pads from post-clip bounds | Same rule with the bottom camera X basis converted once | Multi-body composition, material preservation, and clipped-canvas scale |
| Asymmetric top and bottom pose fixtures | Pin-1/reference feature matches Altium | Mirrored camera view matches Altium without changing physical pose | Rotation and side semantics |

## Risks and stop conditions

- **Temporary semantic duplication:** Cruncher temporarily owns point-to-region containment while Altium Monkey owns region and stack semantics. Keep the implementation narrow, test against issue 95, and delete it after the upstream API is released.
- **Coordinate-unit drift:** region outlines use Altium internal units while public envelopes and model transforms use physical units. Centralize conversion and verify known interior and boundary points before renderer integration.
- **Cross-region body:** one Z half-space pair cannot represent a body over unlike local envelopes. Preserve mounting-side-only rendering and warn; do not choose the anchor region for the entire body.
- **Serialized-model drift:** do not fall back to manual V7/V8/V9 row summation if source-aware resolution fails; surface the Altium Monkey diagnostic and keep mounting-side-only rendering.
- **Material-source ambiguity:** a material name, saved 3D display color, inline stack color, and external material-library entity are different sources. Preserve provenance, normalize only characterized encodings, and diagnose unavailable references rather than inventing a color.
- **Coverlay misclassification:** Altium Monkey exposes distinct `SOLDER_MASK` and `BIKINI_COVERLAY` TypeIds matching the AD26 importer. Stop if a source cannot be classified from typed fields; never infer coverlay only from `Polyamide`, `film`, or another material-name substring.
- **Region appearance seams:** independently filled region paths can expose gaps or double-paint boundaries. Use canonical shared topology/tolerance and add raster/SVG seam checks at rigid-flex boundaries before enabling regional `auto` color by default.
- **Bend coordinate-frame drift:** Board6 cached bend coordinates and region-local bend coordinates are not interchangeable. Use region-local records and a characterized region-to-board transform; stop rather than deriving an origin from outline minima as a general format rule.
- **Silkscreen-domain coupling:** the overlay clipper and film painter must consume the same immutable domain description but remain independent of output order and generated SVG IDs. Reject implementations that scrape or reference another rendered layer's private mask.
- **SVG mask cost:** large aperture sets can inflate SVGs and rasterization time. Measure representative boards, share deterministic definitions within one document where safe, and retain `none`/`board` modes without weakening correctness of `film`.
- **Mounting datum ambiguity:** do not adjust away solder mask or another physical row until a native-Altium oracle establishes the 3D-body standoff datum.
- **Native API gap:** stop for an architecture decision if clipping requires Python mesh reconstruction or loses STEP material identity.
- **Reporter-content boundary:** the issue attachment and screenshot are prohibited repository content. Do not treat minimization as permission to commit copied reporter data; use a separately user-authored fixture with explicit provenance and authorization.
- **Directional regression:** do not accept a bounds-only match that places IC3 pin 1 anywhere except the upper-right lead shown by the supplied Altium reference.
- **Ambiguous outline:** preserve current behavior when both rotation candidates match equally; do not infer semantics from pads or designator names.
- **Public behavior expansion:** do not hand-edit generated contracts if rotation diagnostics or provenance affect emitted metadata.
- **Warning-volume regression:** do not stream recoverable geometry warnings or repeat them per view/cache hit. Keep console samples bounded while preserving every structured occurrence in the requested report.
- **Performance regression:** do not accept unconditional two-side rendering of every body; use conservative bounds to avoid unnecessary native work and measure cold/warm paths.
