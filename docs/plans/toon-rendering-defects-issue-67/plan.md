+++
type = "plan"
id = "toon-rendering-defects-issue-67"
status = "pending"
created = "2026-09-20"

[[steps]]
id = "capture-current-state"
title = "Record the defect buckets, fixtures, known causes, and release state"
status = "done"

[[steps]]
id = "freeze-rendering-rules"
title = "Define the side, transform, clipping, aperture, and designator invariants"
status = "done"
depends_on = ["capture-current-state"]

[[steps]]
id = "complete-single-part-corrections"
title = "Correct affine placement, board-space aperture composition, and designator ownership"
status = "done"
depends_on = ["freeze-rendering-rules"]

[[steps]]
id = "automate-single-part-matrix"
title = "Add structural and rendered assertions for all single-part permutations"
status = "done"
depends_on = ["complete-single-part-corrections"]

[[steps]]
id = "review-single-part-matrix"
title = "Generate and obtain owner sign-off on the through-hole and SMT galleries"
status = "done"
depends_on = ["automate-single-part-matrix"]

[[steps]]
id = "review-projection-test"
title = "Qualify the projection-test edge, cutout, and overhang cases"
status = "done"
depends_on = ["review-single-part-matrix"]

[[steps]]
id = "review-usb-edge"
title = "Qualify the USB edge connector and reverse-mount LED cases"
status = "done"
depends_on = ["review-projection-test"]

[[steps]]
id = "review-reporter-board"
title = "Qualify the GitHub issue 67 reporter board"
status = "done"
depends_on = ["review-usb-edge"]

[[steps]]
id = "resolve-mechanical-open-space-policy"
title = "Align through-bore component visibility with the canonical mechanical opening domain"
status = "done"
depends_on = ["review-reporter-board"]

[[steps]]
id = "requalify-open-space-gates"
title = "Rerun and obtain owner sign-off on Gates 1 through 4 after the mechanical-opening change"
status = "done"
depends_on = ["resolve-mechanical-open-space-policy"]

[[steps]]
id = "review-rigid-flex-boards"
title = "Qualify Bluetooth Sentinel Flex and Kame IMU as Gate 5"
status = "done"
depends_on = ["requalify-open-space-gates"]

[[steps]]
id = "generate-review-analytic-bodies"
title = "Generate and qualify the component-owned analytic-body matrix as Gate 6"
status = "done"
depends_on = ["review-rigid-flex-boards"]

[[steps]]
id = "generate-review-free-board-bodies"
title = "Qualify the loz-old-man board-level free STEP body as Gate 7"
status = "done"
depends_on = ["generate-review-analytic-bodies"]

[[steps]]
id = "review-real-world-smoke-boards"
title = "Qualify RT Super C1 and Bunny Brain as Gate 8"
status = "done"
depends_on = ["generate-review-free-board-bodies"]

[[steps]]
id = "review-pcb-svg-shared-path"
title = "Requalify the ordinary PCB SVG assembly compositor as Gate 9"
status = "done"
depends_on = ["review-real-world-smoke-boards"]

[[steps]]
id = "split-review-gallery-by-gate"
title = "Split the durable SVG review gallery into independently loaded gate pages"
status = "done"
depends_on = ["review-pcb-svg-shared-path"]

[[steps]]
id = "neutralize-runtime-contract-boundary"
title = "Separate versioned PCB SVG contract loading from neutral runtime rendering types"
status = "done"
depends_on = ["split-review-gallery-by-gate"]

[[steps]]
id = "draft-renderer-design"
title = "Write the durable Toon rendering algorithm and limitation document"
status = "done"
depends_on = ["neutralize-runtime-contract-boundary"]

[[steps]]
id = "test-runtime-impact-audit"
title = "Measure coverage, determinism, cache behavior, runtime, and memory impact"
status = "done"
depends_on = ["neutralize-runtime-contract-boundary"]

[[steps]]
id = "promote-public-documentation"
title = "Finalize public Toon behavior, support boundaries, and release documentation"
status = "done"
depends_on = ["draft-renderer-design"]

[[steps]]
id = "design-doc-intent-audit"
title = "Audit public documentation and contracts against the implemented behavior"
status = "done"
depends_on = ["promote-public-documentation"]

[[steps]]
id = "requalify-model-less-designators"
title = "Obtain owner sign-off on the refreshed Gate 4 no-model projected-label policy"
status = "done"
depends_on = ["promote-public-documentation"]

[[steps]]
id = "external-review"
title = "Obtain an independent correctness and performance review of the candidate"
status = "done"
depends_on = ["design-doc-intent-audit", "test-runtime-impact-audit", "requalify-model-less-designators"]

[[steps]]
id = "remediate-audit-findings"
title = "Resolve material audit findings and repeat affected qualification gates"
status = "done"
depends_on = ["external-review"]

[[steps]]
id = "reaudit-remediated-candidate"
title = "Independently re-audit the exact remediated release candidate"
status = "done"
depends_on = ["remediate-audit-findings"]

[[steps]]
id = "full-release-qualification"
title = "Run repository, contract, packaging, installed-package, and development-standard checks"
status = "done"
depends_on = ["reaudit-remediated-candidate"]

[[steps]]
id = "release-candidate-review"
title = "Regenerate the complete gallery from the exact release candidate and obtain final owner sign-off"
status = "done"
depends_on = ["full-release-qualification"]

[[steps]]
id = "publish-and-verify"
title = "Publish the replacement release, verify a clean installation, and reconcile tracked issues"
status = "pending"
depends_on = ["release-candidate-review"]

[[exit_criteria]]
id = "rendering-rules-defined"
title = "Placement, visibility, clipping, aperture, designator, and unsupported-model rules have one documented meaning"
status = "met"

[[exit_criteria]]
id = "single-part-matrix-accepted"
title = "All 16 single-part SVG cases pass automated checks and owner visual review"
status = "met"

[[exit_criteria]]
id = "stress-boards-accepted"
title = "Projection, USB edge, issue 67, rigid-flex, analytic-body, and free-board-body fixtures pass Gates 2 through 7"
status = "met"

[[exit_criteria]]
id = "automated-regressions"
title = "All regressions pass on the candidate and were proven sensitive to the captured defect or a controlled fault"
status = "met"

[[exit_criteria]]
id = "algorithm-design-document"
title = "A comprehensive public design document explains the renderer algorithm, invariants, fallbacks, and limitations"
status = "met"

[[exit_criteria]]
id = "public-toon-documentation"
title = "Public Toon documentation states what is rendered, what is ignored, and how warnings and unsupported models behave"
status = "met"

[[exit_criteria]]
id = "contract-compatibility"
title = "Any configuration changes follow TypeSpec authority and the A1-additive/B0-breaking policy"
status = "met"

[[exit_criteria]]
id = "neutral-runtime-boundary"
title = "Versioned PCB SVG inputs normalize once into neutral runtime types and rendering implementation names contain no stale contract version"
status = "met"

[[exit_criteria]]
id = "test-runtime-impact-audit"
title = "Determinism, cache, runtime, output-size, and memory evidence has an accepted disposition"
status = "met"

[[exit_criteria]]
id = "external-review"
title = "Independent review has no unresolved material correctness, maintainability, or performance findings"
status = "met"

[[exit_criteria]]
id = "design-doc-intent-audit"
title = "Public documentation and contracts match the reviewed implementation and accepted limitations"
status = "met"

[[exit_criteria]]
id = "release-qualified"
title = "The exact published candidate passes full source and clean-installed-package qualification"
status = "pending"
+++

# Toon rendering and designator defect closeout

## Objective

Close the known Toon component-rendering and projected-designator defects without
losing the reasoning behind the fixes. The work must proceed through small,
reviewable fixtures before returning to complex boards. The final implementation
must have executable regression coverage, a reproducible vector review gallery,
an independent algorithm and performance audit, and durable public documentation.

This plan treats the currently yanked release as unqualified. Existing local
fixes and apparently correct SVGs are candidates, not accepted behavior, until
they pass the ordered gates below.

## Execution checkpoint

Independent pre-execution review completed on 2026-09-20. Its seven findings
were incorporated before implementation: material-intersection rather than
full-footprint region qualification, a concrete transform contract and numeric
oracle, mandatory post-remediation re-audit, gate-specific assertions, SVG/CLI
compatibility review, reproducible performance thresholds, and unambiguous
regression-test exit wording.

Gate 1 implementation and automated qualification are complete. The board-space
mask fix keeps each `userSpaceOnUse` domain on an untransformed parent and moves
only its child `<use>`. Projected designators now always follow component
placement side, independent of prepared model fragments. The independent
noncommuting transform oracle, eight-case side-ownership test, four native
fixture matrix cases, SVG-gallery tests, and related clipping tests pass: 62
focused tests total.

The corrected 16-SVG default/assembly review is under
`temp/toon-rendering-closeout/gate1-defaults-v2/` and the durable owner-review page
is `temp/toon-rendering-closeout/review/index.html`. The repository owner
accepted Gates 1 through 9 on 2026-09-20. The durable gallery is split into
per-gate pages, and NXP FRDM i.MX93 was removed from Gates 8 and 9 because its
large SVGs added review cost without new coverage. The runtime contract-boundary
refactor and comprehensive algorithm document are complete. Preliminary cache
and determinism measurements found and fixed loss of diagnostic model identity
on warm artwork hits; the completed performance evidence is recorded in
`impact-audit.md`, and independent findings and remediation are recorded in
`independent-audit.md`.

The final independent audit found and then verified remediation of one early
whole-component cache-identity gap. That final change affects cache invalidation
only, not SVG construction; the signed gallery remains the exact cold-render
output, and the warm-cache regression proves equivalent output after reuse.
Full rack, contract, browser, packaging, isolated-install, and development-
standard qualification are green. The four-worker performance tradeoff is
owner accepted. Publication remains deliberately pending explicit owner
authorization.

## Issue-number note

GitHub number 57 is the merged pull request that released 2026.9.12. The external
rendering-defect report is issue 67, and the approved reporter fixture is stored
under `tests/assets/projects/issue67-reporter`. Therefore the reported-board
gate in this plan means issue 67. If “issue 57” referred to a different local
artifact, add that artifact as a separate gate without replacing issue 67.

## Scope and defect buckets

The work is divided by observable failure rather than by the module in which a
fix happens:

1. **Affine placement and view projection.** Model-local, authored model,
   component-placement, board-world, and top/bottom view transforms must be
   composed once and in a defined order. A bottom view must not create a second
   occurrence, double-rotate a body, or expose an untranslated copy.
2. **Board-thickness clipping.** A through-board body must be clipped in world
   space against the correct region surface. The clipped geometry, not a later
   2D approximation, supplies bounds, HLR, outlines, occlusion, shading, and SVG.
3. **Edge and cutout visibility.** Geometry over a routed void or beyond the
   board perimeter remains visible from the opposite view. Geometry hidden by
   actual board material does not. Pad and via graphics are not automatically
   treated as through-open voids because their 2D appearance alone does not
   prove a clear mechanical bore.
4. **SVG coordinate-space composition.** Board-material and open-space masks
   operate in board/view coordinates. They must not inherit a component
   occurrence translation a second time. Definitions, masks, symbols, and
   instance groups must retain stable IDs and valid references.
5. **Projected-designator ownership.** An assembly designator belongs to the
   component's authored placement side. A body or pin crossing the board does
   not make the designator visible on the other side. Disabling projected
   designators emits none. Physical top/bottom silkscreen text remains a
   separate authored-layer concern.
6. **Region-aware board presentation.** Substrate, outer copper, solder mask or
   coverlay, silkscreen clipping, board cuts, and bend-line graphics must retain
   the already accepted regional paint order while component fixes are made.
7. **Unsupported or absent component geometry.** A component with no supported
   STEP or supported Altium extruded/analytic body receives no invented body.
   Unsupported attached formats and unusable geometry omit only the affected
   body. Board-owned pads, copper, holes, and authored overlay remain physical
   board artwork, not substitute component geometry. Missing/unsupported model
   diagnostics are queued, grouped, and presented at completion.

The last bucket requires one explicit policy assertion before implementation is
frozen: projected assembly labels for a component with no renderable body are
also omitted, matching the current public Toon document and the direction to
ignore components whose appearance is unknowable. Tests and public docs must
agree; do not retain a hidden pad-envelope fallback in one code path.

## Rendering invariants to freeze first

The implementation and independent audit use the following model. Any necessary
change must be recorded before code is accepted.

### Coordinate and geometry pipeline

For every renderable body:

1. Decode or construct geometry in model-local coordinates.
2. Apply the complete authored body transform, including model origin, rotation,
   scaling, standoff, and root placement.
3. Apply the component occurrence placement and side convention to obtain one
   board-world representation.
4. Query the rigid board region/envelope applicable to the occurrence and derive
   the top or bottom visibility half-space.
5. Clip world-space triangles in Geometer before bounds, HLR, outline, shading,
   or geometry serialization. `cap_policy: none` remains the expected policy.
6. Project the accepted fragment into the selected view. Apply the bottom-view
   presentation mirror exactly once at the scene/view boundary.

The `freeze-rendering-rules` deliverable must publish the actual homogeneous
matrix contract used by the implementation, not only this prose sequence. Using
column-vector notation, begin with the symbolic form

`p_view = M_scene(view) * M_component(side, rotation, translation) * M_body(root, pose, scale, standoff) * p_model`

and replace every term with its concrete 4-by-4 definition. Record handedness,
millimetre/mil conversion boundaries, positive rotation convention, pivot for
each rotation and scale, multiplication order, bottom-placement operation,
board-world Z zero, top and bottom surface elevations, and the one location at
which the presentation mirror is applied. Resolve the layer-stack convention
for nonzero top surfaces rather than assuming that every top is Z=0.

Build an independent numeric oracle that does not call the production transform
helpers. Transform the origin and all three basis points through deliberately
noncommuting root offset, nonuniform scale, authored rotations, component
rotation/translation, standoff, and bottom placement. Exercise top and bottom
views plus a region with nondefault top and bottom elevations. A symmetric or
translation-only fixture is insufficient evidence for transform order.

### Frozen Gate 1 transform contract

Cruncher uses right-handed board coordinates, millimetres at the Geometer
boundary, 4-by-4 matrices acting on column vectors, and positive rotations by
the right-hand rule. Python composes row arrays as `left * right`; Geometer's
flat occurrence matrix is the column-major serialization of that result.

For an embedded STEP point `p_step`, Geometer preserves and first applies the
STEP root placement `M_root`. Cruncher's selected instance-space occurrence is:

`M_step = T(dx, dy, side_sign * dz) * Rz(component_rotation + model_2d_rotation) * Rx(bottom ? 180deg : 0deg) * Rz(model_3d_rotz + (bottom ? component_rotation : -component_rotation)) * Ry(model_3d_roty) * Rx(model_3d_rotx)`

where `dx` and `dy` are the authored model 2D anchor minus the component anchor,
converted from mils to millimetres, and `side_sign` is +1 for top and -1 for
bottom. The footprint-local rotation candidate uses authored `model_3d_rotz`
without the instance-space component adjustment and is selected only when its
native bounds match the authored body outline better. STEP root transforms,
including their offset/orientation/scale, remain upstream of `M_step`.

The component-local result is placed in board XY by `T(anchor_x, anchor_y)`.
Bottom-authored geometry then receives the resolved normalized board-surface Z
offset. Cruncher's board frame normalizes each valid stack envelope to top Z=0
and bottom Z=`-thickness`, even when Monkey reports a midplane or another source
Z-zero. Region lookup therefore consumes board XY plus local bounds, while the
world-space clip plane is top Z=0 or bottom Z=`-thickness`.

Bottom-surface Z placement first uses a resolved component anchor. If the anchor
is outside a board with exactly one valid rigid region, use that sole region's
thickness. Outside-origin placement inference on multi-region or rigid-flex
boards is a known limitation for this release: Cruncher warns rather than
selecting a region by nearest distance or greatest overlap. A future
implementation should intersect actual mounting-pad geometry, then the
transformed model's actual XY footprint, with board material. Bounding boxes may
accelerate candidate selection but are not placement authority because they can
cross gaps, cutouts, or untouched adjacent regions. Multiple touched regions
would be acceptable only when their physical envelopes are equivalent.

Geometer's bottom `mirror_x` corrects the handedness of its -Z projection back
into board coordinates; it is not the user-facing bottom-view mirror. The SVG
scene applies the “viewed from underneath” presentation reflection once. SVG
component `<use>` translation applies only the board XY anchor. Board-domain
masks remain on its untransformed parent.

`tests/test_pcb_model_rotation.py` freezes the noncommuting STEP occurrence with
an independent origin/three-basis-point numeric oracle for both placements; the
native root-placement test uses a deliberately asymmetric STEP root. Region
index tests use source envelopes with nonzero top/bottom elevations and assert
their normalized 0/`-thickness` board surfaces.

Plane normalization, tolerance, cap policy, full placement, board-envelope
identity, material assignment, and relevant illustration settings must
participate in deterministic result/cache identity. A completely clipped body
is a successful empty fragment, not an error and not a cache failure.

### Surface and open-space composition

A single Z half-space cannot represent the union “visible past the board edge or
through a routed cutout, or visible beyond this board surface.” Where required,
compose two disjoint presentations of the same correctly placed occurrence:

- a surface fragment clipped at the applicable top/bottom plane and restricted
  to the board-material domain; and
- an uncut fragment restricted to actual open space: outside the board outline
  plus routed board cutouts.

The board-material and open-space masks are complementary in board/view space.
Attach them to an untransformed parent or otherwise prove that occurrence
translation is not applied to mask coordinates. Do not use film openings, pad
shapes, or via/drill display circles as the mechanical open-space mask. Avoid
double painting at mask boundaries with one declared tolerance and deterministic
path construction.

Qualify the surface plane against the transformed body's intersection with the
**board-material domain**, not by requiring board material to cover the body's
complete XY bounds. A surface plane is usable when every material region
intersected by that footprint has an equivalent physical envelope. The uncut
open-space branch is generated independently of surface-plane success, including
for a body wholly inside a routed cutout or wholly outside the outline but still
inside the output bounds. If intersected material regions have incompatible
envelopes, preserve the valid open-space branch and apply the documented
conservative fallback only to the material-intersection branch; never erase the
open-space geometry merely because no single surface plane exists. Flex regions
remain flat in this release; bend-line graphics do not fold component geometry.

Automated cases must cover a partial edge overhang, a body wholly within a routed
cutout, a body wholly outside the outline but inside the output bounds, and a
body spanning incompatible envelopes plus open space.

Gate 3 exposed a separate policy question that did not invalidate its baseline
visual acceptance. The implemented policy now uses one side-aware mechanical
opening domain for substrate removal and component open-space composition: NPTH
features and applicable untented through bores are open; mere film apertures and
tented, filled, plugged, capped, blind, or buried features remain occluding.
Default `DRILLS`, `SLOTS`, and `BOARD_CUTOUTS` presentation is transparent with
outlines only. Their configurable fills, hatches, and labels remain optional
drafting annotations rather than physical occluders. Gates 1 through 4 must be
reaccepted against the regenerated outputs before more boards are added.

For Gate 3 requalification, keep two additional review-only top/bottom pairs
beside the normal default and assembly outputs. The **pure open-space** pair
disables the `BOARD_CUTOUTS`, `DRILLS`, and `SLOTS` artwork while retaining the
same physical opening masks. The **all opening overlays** pair enables those
three layers, cutout hatch, `CUTOUT` labels, and transparent drill/slot
outlines. Comparing the pairs must show that annotation changes presentation
only: component visibility and the physical board/film apertures must remain
identical.

### Designator semantics

Projected assembly designators are filtered by component placement side before
any model-fragment visibility decision:

- top-owned component: label allowed only in a top view;
- bottom-owned component: label allowed only in a bottom view;
- through-board or overhanging geometry: no change to label ownership;
- DNP component: no projected label in the active population;
- disabled assembly-designator layer: no projected label;
- no renderable body: no invented label or body;
- authored silkscreen designator: controlled only by its actual overlay layer
  and the selected physical-silkscreen style.

Label placement may use the accepted projected owning-side geometry, but model
preparation for both clipping sides must never bypass the ownership filter.

## Fixture policy

The approved fixtures are:

- `tests/assets/projects/single-throughhole/input/`: paired top- and
  bottom-mounted two-pin terminal blocks with STEP geometry;
- `tests/assets/projects/single-smt/input/`: paired top- and bottom-mounted SMT
  parts with STEP geometry;
- `tests/assets/projects/projection-test/input/projection_test.PcbDoc`: board-edge
  overhang, interior-cutout overhang, and a connector seated in a cutout;
- `tests/assets/projects/usb-edge/input/usb_edge.PcbDoc`: sanitized PcbDoc-only
  board with a straddle-mount USB connector and reverse-mount LED;
- `tests/assets/projects/issue67-reporter/input/sample.PcbDoc`: reporter-approved
  PcbDoc-only regression board for affine placement and opposite-side geometry.

Keep each `source-manifest.json` with provenance, authorization, scope, hashes,
and sanitization notes. Do not commit the reporter archive, reporter screenshot,
review screenshots, generated SVGs, galleries, proprietary logo, removed project
files, or removed schematics. Review output belongs under ignored `temp/` or
`output/` directories.

## Ordered implementation and review sequence

Do not bypass a rejected visual gate by moving to the next board. A correction
after a gate is accepted must rerun that gate and every later gate affected by
the same code path.

### Gate 1: single-part matrix

Generate the complete 16-SVG matrix:

| Fixture | Placement document | View | Toon mode |
| --- | --- | --- | --- |
| Through-hole | top, bottom | top, bottom | default, `--assembly` |
| SMT | top, bottom | top, bottom | default, `--assembly` |

Use the unmodified `acr toon` defaults. Do not apply a theme, mask, substrate,
silkscreen, opacity, or other review-only style override. The second rendering
differs only by `--assembly`: default mode retains authored physical silkscreen
designators and has no projected designator layer; assembly mode retains the
authored board and adds projected assembly designators. The additive A1 option
`assembly.hide_silkscreen_designators=true` explicitly suppresses the physical
designators when desired. This matrix
therefore reviews the behavior a user receives from the command, including
saved mask/material resolution, rather than an artificial isolation theme.

Acceptance checks:

- the top/bottom placed copies have the expected rotation and footprint
  registration in their owning views;
- the SMT body is absent from the opposite view;
- only the physically crossing portion of the through-hole model is visible in
  the opposite view, aligned with its owning-side occurrence and pads;
- there is no half-body, shifted duplicate, translated mask window, or
  opposite-side surface slice;
- in default mode, no projected designator exists and authored silkscreen
  follows its actual overlay side;
- in assembly mode, exactly one projected designator exists in the
  placement-side view and none exists in the opposite view, while authored
  silkscreen designators remain controlled by their physical overlay side;
- the opt-in `assembly.hide_silkscreen_designators=true` policy suppresses
  authored designators without changing projected-label ownership;
- top and bottom views retain the documented “looking at that side” mirror and
  readable label behavior.

Both fixture types must pass automated checks before creating the owner-review
gallery. Record owner acceptance or findings in a working review log beside this
plan. The next gate cannot start until both are accepted.

### Gate 2: projection-test

Render top and bottom views in default and `--assembly` modes. Review each
board-edge and interior-cutout overhang, the cutout-seated connector, component
rotation, board registration, mask boundaries, and top/bottom label ownership.
Inspect at high zoom in the vector gallery. Add structural or pixel assertions
for every discovered failure rather than relying solely on a whole-page golden.
Before gallery acceptance, automated checks must identify the intended edge and
cutout components and assert their visible/hidden regions on both sides.

### Gate 3: usb-edge

Render top and bottom views in default and `--assembly` modes. Review the
straddle-mount USB connector at the board plane, reverse-mount LED body visible
through the routed slot, board-side ownership, labels, copper/film/cutout paint
order, and absence of false openings at ordinary pads or vias. This board remains
PcbDoc-only; do not restore scrubbed project, schematic, or logo content.
Also review the pure-open-space and all-opening-overlays pairs defined above so
routed-cutout hatch/labels and drill/slot outlines cannot silently disappear or
alter the physical aperture policy.
Before gallery acceptance, automated checks must prove USB/LED cutout visibility
and prove that representative ordinary pad/via graphics do not act as component
apertures.

### Gate 4: issue 67 reporter board

Render top and bottom views in default and `--assembly` modes. Recheck the
reported rotations, component heights, P1-style pin alignment, correct fragments
for bodies crossing the board, absence of opposite-side body leakage, and
placement-side-only labels. Compare against the reporter's Altium intent without
committing the supplied screenshot or original attachment.
Before gallery acceptance, add reporter-specific automated orientation and
registration assertions for IC1, IC2, IC3, and P1, including IC3 pin-1 direction
and P1 pin/footprint alignment. These checks must be independent of a reviewer
recognizing the error by eye.

### Gate 5: rigid-flex corpus

After the first four gates are reaccepted, render the two owner-selected
PcbDoc-only rigid-flex fixtures:

- `bluetooth_sentinel_flex/input/Bluetooth_Sentinel.PcbDoc`: two 32.1455 mil
  rigid regions and one 3.3267 mil flex region from the public Altium example;
- `Kame_IMU/input/Kame_IMU.PcbDoc`: two 34.1479 mil rigid regions and one
  6.3391 mil flex region from the owner-supplied `Sample - Kame_IMU` project.

Render top and bottom in default and `--assembly` modes. Review the boards flat;
no flex folding is simulated. Qualify region partition coverage, local rigid and
flex thickness, substrate and film material/color selection, coverlay versus
solder-mask behavior, surface copper in every region, bend-line geometry and
style, cutouts, modeled-component placement, and placement-side designators.
Explicitly record any component whose anchor/model footprint crosses regions or
falls outside the region partition under the documented multi-region placement
limitation. Such a warning must not silently select an arbitrary nearby region.

Both fixture manifests must retain provenance, authorization, byte count, and
SHA-256 identity. Generated SVGs remain transient. Gate 5 requires separate
owner acceptance for each board before adding any further corpus cases.

The owner accepted both Gate 5 boards on 2026-09-20 after `BEND_LINES` was added
to the default top and bottom Toon view orders. The accepted rerender contains
six bend-line primitives per Bluetooth Sentinel view and three per Kame_IMU
view.

### Gate 6: generated component-owned analytic bodies

Create a focused rigid-board fixture with an Altium Monkey generator before
changing Toon behavior. The generator is the fixture source of truth:

- generator: `tests/support_scripts/generate_toon_analytic_bodies.py`;
- committed fixture directory: `tests/assets/projects/toon-analytic-bodies/`;
- generated board: `input/toon_analytic_bodies.PcbDoc`;
- generated semantic inventory: model type, owner, side, anchor, XY outline,
  Z interval, color, opacity, and intended review case for every body;
- source manifest: pinned Altium Monkey version, generation command, generated
  file byte count and SHA-256, and regeneration/authorization notes.

Use only Altium Monkey's public authoring surface. Build footprint-local bodies
in a generated PcbLib/in-memory footprint and place them with
`AltiumPcbDoc.add_component_from_pcblib(...)`; do not patch binary streams or
reach into private builders. The committed PcbDoc lets normal tests run without
regeneration. Two generator runs must produce the same semantic inventory. They
should byte-match when the writer supports deterministic container identity; if
non-semantic container bytes vary, document them and compare a normalized
semantic digest so geometry drift still fails loudly. Open the generated file
in Altium for validation without resaving it; repair the generator if Altium
rejects or repairs the document.

The board has one known rigid thickness and an asymmetric outline with a routed
interior cutout. Arrange clearly separated, silk-labeled cells with mirrored top
and bottom counterparts. Cover every Toon-supported Altium analytic model type:

| Case family | Required authored geometry |
| --- | --- |
| Extruded profiles | Convex rectangle, rotated/offset polygon, concave profile, and a multi-body composite |
| Cylinders | Surface-contained, offset, and through-board cylinders |
| Spheres | Surface-contained, offset, and board-plane-crossing spheres |
| Z interaction | Same-XY bodies that are separated, exactly touching, and overlapping at different Z intervals |
| Side ownership | Equivalent top- and bottom-authored bodies with nonzero component rotations |
| Board interaction | Owning-side only, board-thickness crossing, edge overhang, and routed-cutout overhang |
| Appearance controls | Distinct opaque body colors, one partially transparent documented-limit case, and one zero-opacity omission control |

At least one compound component must mix extrusion, cylinder, and sphere bodies
with distinct colors and overlapping XY/Z extents. This proves that body-local
materials survive batching and that HLR/paint order is determined in 3D rather
than by source-record order. At least one through-board body of each analytic
type must be visible from both sides, clipped at the correct regional surfaces,
and aligned to one board-space anchor. Surface-contained bodies must not leak to
the opposite side.

Render top and bottom in default and `--assembly` modes. Structural tests must
assert the generated semantic inventory after reparsing the PcbDoc, body-to-
component ownership, top/bottom placement, Z extents, colors, deterministic
cache identity, clipped/empty fragments, and placement-side-only designators.
The review gallery must keep case names visible in its card titles; silkscreen
cell labels are reference marks, not substitutes for structural assertions.

Do not use STEP models in Gate 6. This gate isolates Altium `MODELTYPE=0`
(extruded profile), `MODELTYPE=2` (cylinder), and `MODELTYPE=3` (sphere), plus
their multi-body composition. STEP affine behavior remains covered by Gates 1
through 5.

The owner accepted Gate 6 on 2026-09-20. The deterministic generated fixture
contains 14 component owners and 19 bodies. A3 and A4 isolate through-board
cylinder and sphere behavior. A5 deliberately stages its purple extrusion,
top-only blue cylinder, and lower/side yellow sphere so top/bottom visibility is
unambiguous without requiring a Boolean union between intersecting analytic
bodies. General intersecting/coplanar multi-body limitations belong in the
final renderer design document; Toon will not grow a CAD-kernel-style body
union for this release.

### Gate 7: loz-old-man board-level free STEP body

Gate 7 uses the existing real-world `loz-old-man/input/SB0037A.PcbDoc` rather
than adding a generated free-body matrix. It contains one unowned STEP record:
component index `65535`, body index `107`, model
`XB3-C-A1-UT-001.STEP`, model type `1`. The repository owner changed its body
opacity from `0.0` to `0.75` on 2026-09-20, so it is now Gate 7's real-world
case for visible free STEP collection. The review qualified its placement,
top/bottom visibility, material opacity, lack of assembly designator, and the
documented `partial-opacity-opaque-occlusion` diagnostic. The owner accepted the
Gate 7 rendering on 2026-09-20.

This release does not claim a general matrix for unowned analytic bodies,
opposite-side free bodies, through-board free-body clipping, edge/cutout
overhangs, Z overlap, or zero-opacity free-body permutations. Those can become
a separately scoped future fixture if a concrete workflow requires them; they
are not Gate 7 exit criteria for this plan.

The owner accepted the 75% opacity review on 2026-09-20. For a component or
free-body instance whose rendered bodies share one authored partial opacity,
Toon performs geometry clipping, HLR, shading, and open-space composition as
opaque geometry, removes the repeated polygon opacity, and applies the authored
value once to the final component-instance SVG group. This is intentionally not
transparent-aware HLR: the body still occludes as opaque and retains the
`partial-opacity-opaque-occlusion` diagnostic. Zero opacity remains an early
geometry omission. Mixed per-body opacity cannot be represented by one instance
value and remains material-local.

### Gate 8: broad real-world Toon smoke boards

Gate 8 has no new feature-specific agenda. It renders the existing
`rt_super_c1` and `bunny_brain` fixtures from both sides in the unmodified Toon
default and `--assembly` modes. This is a broad visual regression pass over two
additional real-world designs after the focused placement, aperture,
rigid-flex, analytic-body, and free-body gates. The review must use the normal
Toon color and layer defaults apart from the explicit assembly-mode comparison.

The Gate 8 SVGs were generated on 2026-09-20 for both boards, both sides,
and both modes. Rendering completed without a fatal error, and the owner
accepted the combined gallery on 2026-09-20.

### Gate 9: ordinary PCB SVG assembly compositor

Gate 9 deliberately does not use `ILLUSTRATION_TOP`, `ILLUSTRATION_BOTTOM`, or
the `toon` command. It runs the ordinary `pcb-svg` path for the two Gate 8
boards plus `loz-old-man`, using the standard top and bottom assembly view
composition: board outline, side copper, physical overlay/designators,
mechanical cutouts, colored drill/slot artwork, and
`ASSEMBLY_HLR_TOP`/`ASSEMBLY_HLR_BOTTOM`. This gate protects the shared board
aperture and hole changes without conflating them with Toon surface shading.
Only the view list and layer-output suppression are narrowed for review; the
normal PCB SVG style defaults remain authoritative. The HLR mode is `simple`
(normalized to outline-only) and the review pins `projection_algorithm: fast`
with `outline_algorithm: fast-mesh-shadow` so the intended backend is explicit.

The candidate Gate 9 SVGs were generated on 2026-09-20 for all three boards.
Structural inspection found one expected HLR layer and a simple assembly
overlay in every output, the correct side's physical overlay, drill artwork in
every output, slot artwork on boards that contain slots, and no
`ILLUSTRATION_TOP`/`ILLUSTRATION_BOTTOM` token. The owner accepted the combined
gallery on 2026-09-20.

The initially accepted combined gallery was slow because it embedded every SVG,
including the very large NXP FRDM i.MX93 review set, in one document. On
2026-09-20 the durable generator gained manifest-driven gate partitioning. The
stable root is now a lightweight gate chooser, and each self-contained gate
page loads only its own vector set. This changes review-tool packaging only;
the accepted renderer output is unchanged. The owner subsequently removed the
NXP board from Gates 8 and 9 because its unusually large review SVGs added cost
without additional qualification value; the underlying corpus fixture remains
available for other workflows.

## Durable SVG review workflow

Use `tests/support_scripts/svg_review_gallery.py` and the package-owned offline
gallery implementation. A review manifest supplies an arbitrary ordered array
of SVG path/title entries. The generated responsive gallery must preserve the
original SVG vectors, open a full-screen modal, support fit/pan/wheel/toolbar
zoom and next/previous navigation, and provide a raw-SVG link. It must not
rasterize review content or depend on a network CDN.

Large closeout manifests must set `split_by_group_pattern` and partition the
review by gate. The stable root `index.html` is a lightweight gate chooser;
each gate page embeds only that gate's vectors and retains the full offline
pan/zoom workflow. This prevents opening the durable root from parsing every
accepted real-world SVG at once.

For every gate:

- generate into a new, clearly named directory below
  `temp/toon-rendering-closeout/`;
- use deterministic card order and titles containing fixture, placement side,
  view side, and Toon mode;
- include the manifest and the exact command/config/dependency versions needed
  to reproduce the gallery;
- update the single durable owner-review page at
  `temp/toon-rendering-closeout/review/index.html`, so the same browser tab can
  be refreshed throughout the process;
- keep accepted and candidate SVGs in separate gate-specific directories even
  though the durable index is regenerated, and archive each accepted manifest
  before pointing the durable page at a later candidate;
- give the owner that stable absolute `index.html` path and, when useful,
  individual SVG paths;
- record accepted/rejected status and findings in the plan's working review log.

The final release-candidate gallery must be regenerated from the exact candidate
commit and locked dependency set, not reused from an earlier working tree.

## Automated test strategy

Prefer behavioral assertions and small fixtures over fragile whole-page byte
goldens. Full SVG byte identity is useful for determinism checks, not as the only
proof of visual correctness.

### Unit and structural coverage

Cover at least:

- the full 3D affine chain for representative top/bottom placement, authored
  model rotation, standoff, root offset, and bottom-view reflection;
- component-side classification independent of prepared model-fragment sides;
- designator inclusion/exclusion for top, bottom, DNP, disabled, missing-model,
  unsupported-model, and through-board cases;
- rigid-region board-thickness selection, tolerance boundaries, successful empty
  clips, and fallback for incompatible/spanning envelopes;
- construction of board-material versus true-open-space masks;
- masks attached in board coordinates with translated child occurrences;
- stable SVG IDs, references, metadata, Inkscape/ARIA labels, layer ordering,
  and absence of orphaned definitions;
- routed edge/cutout behavior without treating pads/vias as guaranteed voids;
- queued, grouped, deterministic nonfatal diagnostics;
- cache keys covering every geometry- or result-affecting transform, clip, mask,
  material, and policy input.

### Fixture-level rendered assertions

For focused cases, parse emitted SVG and rasterize at a fixed documented DPI for
targeted sample/region assertions. Prove presence, absence, alignment, and label
ownership in stable local regions. Keep tolerances explicit and diagnose whether
a failure is geometry, paint order, transform, or antialiasing. Avoid enormous
binary reference images when geometric/DOM assertions express the rule better.

At minimum, a regression test must fail for each known defect:

- a mask translated with its component instance exposes an offset chunk;
- a prepared opposite-side model causes a designator on the wrong side;
- an SMT body leaks to its opposite view;
- a through-hole opposite-side pin fragment is shifted from its footprint;
- an edge/cutout overhang is erased by a Z-only surface clip;
- a pad or via display opening falsely reveals an uncut component body.

### Determinism and cache coverage

For representative focused and complex boards:

- compare cold and warm results;
- compare one worker and the default worker count;
- repeat top/bottom and default/assembly modes;
- require byte-identical SVG for identical inputs and configuration;
- require deterministic diagnostic order and report contents;
- prove complete warm artwork reuse starts no unnecessary native clients;
- prove a changed transform, plane, tolerance, aperture policy, or material does
  not reuse an incompatible cache entry;
- prove expected empty fragments cache as success while failures retry.

## Performance and independent audit

The independent audit starts only after the owner accepts every selected visual
gate. The reviewer must not be the primary implementer and must review an exact
candidate commit/diff with a clean statement of dependency versions and local
generated artifacts. The audit is not satisfied by rerunning tests alone.

Before that review, collect cold-cache and warm-cache wall time, phase timings,
peak aggregate RSS, SVG size, cache hit/miss counts, and native request counts.
Use the existing profiling scripts where applicable and record the exact baseline
commit/tree, lock/dependency identity, machine, worker count, configuration, and
cache state. A defective pre-fix build may prove test sensitivity but is not a
performance baseline unless it produces the same accepted content. Select one
correctness-equivalent baseline before measurement.

For the reporter board and at least one owner-selected dense board, perform one
unmeasured warm-up followed by five measured runs per cold/warm and worker-count
condition; report median and spread. Investigate wall-time growth exceeding both
10 percent and 0.25 seconds, peak aggregate RSS growth exceeding both 10 percent
and 64 MiB, or SVG-size growth exceeding both 10 percent and 100 KiB. Repeated
geometry work or loss of the complete warm-cache bypass is always investigated.
Every threshold crossing needs a technical disposition and explicit owner
acceptance; do not hide it inside total command noise.

The independent reviewer examines:

1. affine conventions and transform order in full 3D;
2. region/thickness selection and the rigid/flex boundary;
3. Geometer half-space inputs, tolerances, empty results, materials, and cache
   identity;
4. the surface/open-space union, SVG mask coordinate systems, boundary seams,
   and bounds;
5. top/bottom occurrence and designator ownership;
6. substrate/copper/film/silk/cutout/component paint order;
7. unsupported/missing/degenerate geometry and queued warnings;
8. cache correctness, deterministic concurrency, time, memory, and SVG growth;
9. tests for plausible alternate paths, not only the exact prior failures;
10. agreement among code, contracts, CLI docs, the algorithm document, and the
    claimed limitations.

Classify findings by severity and record evidence and disposition. Any material
correctness or performance finding blocks release. After remediation, rerun the
affected automated and visual gates and obtain a follow-up independent review.
Record the audited Git commit/tree hash, `uv.lock` identity, Monkey and Geometer
versions, generated-contract state, and algorithm-document identity. The
`reaudit-remediated-candidate` step is mandatory even when the first review has
no findings: it attests the exact release candidate after all dispositions. Any
code, dependency, generated contract, algorithm document, or behavior change
after that attestation requires an impact disposition and repetition of the
affected review, audit, and visual gates.

## Neutral runtime contract boundary refactor

Complete this low-priority refactor after the visual corpus gates and before the
design, performance, and independent audits. The audited and released code must
not use a stale public contract version as the name of the active renderer or as
the shape passed throughout the rendering pipeline.

The target flow is:

`versioned JSON/JSONC -> schema dispatch and decode/migration -> neutral resolved runtime config -> renderer/workflow dispatch`

Rules for the refactor:

- Keep public schema identifiers and generated DTO names versioned. A0, A1, and
  any future B0 identity remains explicit at file/serialization boundaries.
- Put schema recognition, version-specific decoding, compatibility migration,
  presence-preserving override handling, and validation in one loader/adapter
  boundary. Reject unknown schemas there with the existing actionable error.
- Normalize every accepted contract version into one neutral Cruncher-owned
  runtime container before preset resolution, layer selection, job creation, or
  rendering. Downstream code must not branch on A0/A1 schema identity.
- Give active implementation classes and modules role-based names. Replace names
  such as `PcbSvgA0Renderer` with an unversioned, non-conflicting name such as
  `CruncherPcbSvgRenderer` or `PcbSvgCompositeRenderer`; choose the final name
  after checking the upstream Monkey `PcbSvgRenderer` import to avoid ambiguity.
- Do not rename genuinely versioned public payloads, schema files, generated
  bindings, compatibility decoders, or cache/transport contracts merely to make
  them look neutral.
- Inventory imports and determine whether any implementation class was actually
  exported as supported Python API. Preserve a documented compatibility alias
  for one release if external use is plausible; otherwise record that the rename
  is internal. Avoid two independently evolving renderer implementations.
- Keep configuration authority in TypeSpec. This refactor does not authorize a
  hand-written duplicate public DTO or a new schema version.
- Add loader-dispatch tests for each accepted schema, an unknown schema, authored
  unset/presence preservation, and semantic equivalence after normalization.
- Require byte-identical SVGs, diagnostics, metadata, and gallery manifests for
  the accepted review corpus before and after the refactor. Rerun all focused
  rendering and contract tests. Any output difference returns to the affected
  owner-review gate instead of being dismissed as a naming-only change.

The comprehensive renderer design document must show this boundary explicitly,
so a future contract version changes the adapter rather than forcing versioned
names and conditionals through the implementation.

## Contract and compatibility rules

The expected fixes are behavioral and should not require a new config shape. Do
not add a switch merely to preserve incorrect geometry. If configuration must
change, author it only in `src/tsp/altium_cruncher`, regenerate all governed
artifacts, and update the public field guide and tests. Compatible additive
fields use the A1 contract line; a breaking or replacement shape requires B0.
Presence-preserving authored overrides, preset merging, layer resolution, and
existing dry-run behavior remain intact.

Internal cache versions may change when correctness requires it. Cache entries
are disposable implementation data, but versioning must prevent old incorrect
artwork from being accepted as a valid hit.

TypeSpec is not the only compatibility surface. Before release, inventory and
record the disposition of observable SVG and CLI behavior: layer presence and
order, IDs and references, Inkscape/ARIA labels, metadata attributes, bounds,
warning codes/grouping/order, model-less component and designator omission, and
gallery behavior. Preserve stable metadata where it remains truthful. Reconcile
older pad-envelope fallback tests and documentation with the accepted no-model
policy, and release-note intentional behavior changes even when the JSON shape
does not change.

## Durable documentation deliverables

Before closeout, create or substantially revise one comprehensive document under
`docs/design/` that explains:

- coordinate systems and the complete affine transform pipeline;
- top/bottom view convention and designator ownership;
- board-region and thickness resolution;
- Geometer world-space clipping and `cap_policy: none`;
- surface versus true-open-space composition for edge/cutout overhang;
- SVG masks, definitions, occurrence reuse, bounds, and layer ordering;
- regional substrate, copper, film/coverlay, silkscreen, cutouts, bend lines,
  component art, and label composition;
- cache keys, concurrency, determinism, partial geometry, and warning handling;
- supported STEP and Altium extruded/analytic bodies;
- purposeful omissions and fallbacks.

The limitations section must plainly state at least:

- flex is rendered flat; bend lines are graphical and no folding is simulated;
- component bodies without a supported renderable model are omitted rather than
  invented from pads or courtyards;
- unsupported model formats and unusable bodies are omitted with nonfatal
  diagnostics;
- a Z half-space alone is insufficient for edge/cutout overhang, hence the
  separately masked open-space composition;
- incompatible/spanning region envelopes use the documented conservative
  fallback;
- section caps are not synthesized;
- pad/via display openings are not assumed to be mechanically open through the
  complete board;
- rendering is an illustration, not a collision, manufacturability, or complete
  photorealistic simulation.

Update `docs/design/cli/toon.html` with a concise user-facing explanation of how
Toon generally works, what models and board structures are handled, what is
purposely ignored, how top/bottom and labels behave, and where warnings appear.
Update qualification, architecture/porting, examples, generated field docs, and
release notes where affected. Durable information must not remain only in this
plan or the review galleries. Retire this working plan according to ADR-0004
only after all knowledge has been promoted.

## Release qualification and closeout

After audit remediation and documentation review:

1. regenerate all contracts if their TypeSpec authority changed and run contract,
   TypeScript, and browser freshness checks;
2. run focused Toon, gallery, model-cache, board-surface, and L3 fixture tests;
3. run `uv run --extra test rack run --all`;
4. build wheel and sdist, run Twine checks, and run the isolated install test;
5. run `uvx --from git+https://github.com/wavenumber-eng/wn-dev-std.git wn-dev-std check . --format json`;
6. install the exact artifacts in a clean environment and regenerate the final
   focused and selected-board galleries;
7. obtain final owner sign-off on those installed-package SVGs;
8. confirm that the packaged tree, lock/dependency identity, generated contracts,
   and algorithm document exactly match the re-audited identity; otherwise stop
   and repeat the affected audit and qualification gates;
9. publish a version newer than the yanked release with exact compatible Monkey
   and Geometer pins, verify package metadata and a fresh install, then attach
   release notes describing the corrected behavior and limitations;
10. reconcile issue 67 and any other tracked defects only after the published
   artifact is verified. If an issue is already closed, add the verified release
   result rather than rewriting history.

No plan step, passing unit test, or locally accepted SVG by itself authorizes
publication. The release gate is the exact packaged candidate plus owner visual
sign-off and an independent audit with no unresolved material findings.
