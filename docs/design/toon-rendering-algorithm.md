# Toon rendering algorithm

## Purpose and scope

This document defines how `acr toon` turns Altium board data and attached 3D
models into deterministic top and bottom SVG illustrations. It is the design
authority for placement, board-thickness clipping, open-space visibility,
regional board presentation, composition, caching, diagnostics, and known
limitations. The public command reference remains
[`cli/toon.html`](cli/toon.html); the editable config contract is described in
[`pcb-svg-config-authority.md`](pcb-svg-config-authority.md).

Toon is an illustration renderer, not a solid-modeling kernel. It projects the
authored bodies that Cruncher can interpret and composes them with the physical
board artwork. It does not infer the appearance of a component that has no
supported authored 3D body.

## Contract and runtime boundary

The public config payload is versioned at the wire boundary. TypeSpec under
`src/tsp/altium_cruncher/config` owns the A0/A1 schema, defaults, help, and
generated bindings. Loading follows one direction:

```text
versioned JSON/JSONC
  -> generated presence-preserving decoder
  -> compatibility/default/semantic resolution
  -> neutral PcbSvgConfig runtime model
  -> compositor and Toon workflow
```

The renderer does not branch on A0 versus A1. A0 and A1 inputs with equivalent
authored values produce the same neutral runtime model. A1 is the current
additive family; an incompatible root shape or semantic change starts a B0
family. Version identifiers remain in serialized schemas and emitted payloads,
where they are contractually meaningful, but not in active implementation role
names.

## Coordinate systems and affine placement

Cruncher uses right-handed board coordinates and converts Altium mils to
millimetres before the Geometer boundary. The normalized board frame places the
top board surface at `z = 0` and the local bottom surface at
`z = -region_thickness`. Matrices act on column vectors. Their conceptual order
is:

```text
p_view = M_scene(view)
       * M_board_anchor
       * M_component_and_side
       * M_authored_body
       * M_root
       * p_model
```

`M_root` is the STEP root placement retained by Geometer. The authored body
transform contains the Altium model offset, tilt, Z rotation, scale, and
standoff. Component placement contains the footprint rotation, top/bottom
convention, and board-space anchor. The bottom-view presentation reflection is
applied once at the SVG scene boundary; it is not part of component placement.

For embedded STEP, Cruncher delegates the exact Altium occurrence composition
to Altium Monkey's placement helper. In the normalized frame, the selected
instance-space transform is equivalent to:

```text
T(dx, dy, side_sign * dz)
* Rz(component_rotation + model_2d_rotation)
* Rx(bottom ? 180 degrees : 0)
* Rz(model_3d_rotz + (bottom ? component_rotation : -component_rotation))
* Ry(model_3d_roty)
* Rx(model_3d_rotx)
```

The result is then translated by the board-space component anchor. STEP root
placement remains upstream of this matrix. Bottom-authored geometry receives
the resolved local bottom-surface offset.

Positions use the complete affine matrix. Normals use the inverse transpose of
its combined linear 3-by-3 part and are normalized afterward. This distinction
is required for STEP root placements containing nonuniform scale; applying the
position matrix directly to normals produces incorrect Toon lighting. A
singular transform with authored normals is rejected because its normal field
is undefined.

Some Altium files encode STEP Z rotation in footprint-local rather than
instance space. Cruncher evaluates both interpretations against the authored
body outline. It selects footprint-local only when its fit is uniquely better;
otherwise it retains the native instance-space interpretation and records a
diagnostic for an ambiguous correction. The transform tests use asymmetric,
noncommuting rotations and transformed basis points so a visually symmetric
fixture cannot conceal a multiplication-order error.

## Board regions and thickness

Altium Monkey parses the V7 layer-stack document and resolves each board region
to a physical stack envelope. Until the planned Monkey board-coordinate query
is public, Cruncher's `BoardRegionEnvelopeIndex` performs the spatial join. It
retains region polygons and holes, rejects invalid envelopes, and normalizes
every valid envelope to top `0` and bottom `-thickness`.

Region equivalence is evaluated in that normalized physical frame. Source
stack Z-zero choices and source top/bottom coordinates remain diagnostic
metadata, but equal thicknesses cannot become ambiguous merely because their
source stacks use different Z conventions.

The query uses the placed body's conservative XY bounds. A plane is usable when
every intersected valid region has the same physical envelope. Full coverage of
the bounding rectangle is not required because the SVG material/open-space
composition handles edge and cutout voids separately. Unlike envelopes are
ambiguous and cannot be represented by one Z plane.

For a placement anchor outside all regions, a board with exactly one valid
rigid region may use that sole thickness. Multi-region outside anchors do not
select a nearest or largest-overlap region. The authored side is rendered
conservatively and unsafe opposite-side material is omitted with a warning.
Flat rigid-flex is supported; bending or deforming geometry is not.

## World-space clipping

Clipping happens after the complete root, body, occurrence, and board placement
transforms. The same clipped world-space fragment supplies bounds, hidden-line
removal, outlines, shading, SVG paths, and any geometry output. Projected masks
or post-projection triangle hiding are not substitutes because they allow
opposite-side geometry to affect bounds, silhouettes, and occlusion.

The current half-spaces are:

| Requested view | Kept world-space half-space |
| --- | --- |
| Top | `z >= 0`, plane normal `(0, 0, 1)`, distance `0` |
| Bottom | `z <= -T`, plane normal `(0, 0, -1)`, distance `T` |

`T` is the resolved local region thickness. The default tolerance is
`1e-6 mm`. The cap policy is `none`: the cut boundary participates as an
ordinary outline boundary, but no synthetic filled section face or material is
created. A completely removed body is a successful empty fragment and is
omitted without an error.

Before a native call, conservative Z bounds classify a body as entirely
visible, entirely absent, or crossing the plane. Only the crossing case needs a
clipped native result. If the XY region query is invalid, outside, or ambiguous,
the mounting-side surface branch remains visible without guessed clipping and
the unsafe opposite-side surface branch is omitted.

## Surface and mechanical-open-space composition

A Z half-space alone cannot express the union of geometry visible at a board
surface and geometry visible through or beyond the board. Toon therefore
prepares up to two projections for one occurrence:

1. The **surface branch** is clipped to the requested board surface and masked
   to the board-material domain.
2. The **open-space branch** is uncut in Z and masked to the complement of the
   board-material domain.

The open-space domain includes the exterior of the board outline, routed board
cutouts, applicable untented through pad bores, and applicable untented
through-vias. Blind/buried vias and tented, filled, plugged, or capped bores do
not reveal opposite-side component geometry. Film openings and copper pad
shapes are not mechanical openings.

Both masks use `userSpaceOnUse` in board/view coordinates. The board-space mask
is attached to an untransformed parent; only the child symbol `<use>` receives
the component occurrence translation. This prevents the placement translation
from being applied to a mask twice. The material and complement branches are
disjoint, so the same occurrence is not double-painted at ordinary board
material boundaries.

Physical substrate holes remain transparent. `DRILLS`, `SLOTS`, and
`BOARD_CUTOUTS` can add fills, outlines, hatches, and labels for illustration,
but those virtual overlays do not close a physical opening or change component
visibility.

## Component body sources

Toon currently accepts these Altium component-body forms:

- embedded or otherwise resolvable STEP models (`model_type = 1`);
- extruded polygon profiles (`model_type = 0`);
- analytic cylinders (`model_type = 2`); and
- analytic spheres (`model_type = 3`).

Colors and material identity remain attached to their geometry. New vertices
created by clipping use the native interpolation rules. A zero-opacity body is
removed before geometry work. If every body in an instance shares one partial
opacity, Toon computes clipping, HLR, shading, and occlusion as opaque and
applies the authored opacity once to the final instance group. This avoids
cumulative darkening where projected polygons overlap. Mixed per-body opacity
remains material-local.

Unsupported formats, missing STEP payloads, unusable bodies, and components
with no supported model are omitted rather than replaced by pad envelopes or a
guessed package. Board-owned copper, pads, holes, and silkscreen remain because
they are authored board artwork, not substitutes for missing component bodies.

## Board presentation pipeline

Each view has an explicit draw-ordered layer list. Toon presets compose, in
broad order, the substrate, region-selected outer copper, regional solder mask
or coverlay, physical layers and silkscreen, opening annotations and outline,
bend-line annotations, and component illustration. The exact order is a config
contract and can be inspected in the generated A1 defaults.

### Regional substrate, copper, and film

The same resolved region partition drives all three surface systems:

- substrate uses authored material color when available, then the saved rigid
  board-core display color, then rigid/flex fallbacks;
- surface copper selects each substack's actual outer copper layer, so a flex
  outer layer need not have the legacy `TOP`/`BOTTOM` identity; and
- film is present only where the substack authors solder mask or coverlay.

The default rigid substrate fallback is `#B6A26B`; flex substrate and coverlay
fallback to amber `#D18B28`. Explicit non-`auto` colors remain global
compatibility overrides.

Physical silkscreen can be preserved as-authored (`none`), clipped to the board
material domain (`board`), or clipped to the actual film domain and film
openings (`film`). Toon defaults to `film`; the general PCB SVG config retains
its compatibility default.

### Bend lines

`BEND_LINES` is a virtual documentation layer. It draws flat annotations across
their owning region and never folds the board. Defaults are a `0.15 mm` line,
`#D97706` at opacity `0.8`, `0.5 mm` dash, `0.3 mm` gap, and an absolute
`1 mm` extension at each end. Config can change these values. Per-bend naming
or styling is not inferred unless the source exposes stable metadata.

## Designators and view ownership

Projected assembly designators belong to a component's authored placement
side, independent of pins or other geometry crossing the board:

- a top component can receive a projected label only in the top view;
- a bottom component can receive a projected label only in the bottom view;
- DNP parts in the selected population receive no projected label;
- a component with no renderable body receives no invented projected label;
- a disabled projected-designator layer emits no projected labels.

Authored top/bottom overlay text is separate physical silkscreen. `--assembly`
adds projected labels and preserves authored silkscreen designators by default.
`assembly.hide_silkscreen_designators=true` is the explicit assembly-only
suppression policy.

## SVG structure, bounds, and opacity

Reusable component artwork is emitted into SVG definitions, while occurrence
groups retain stable source-order placement and metadata. Surface and open-space
branches reference separate symbols when both exist. Unused definitions are
pruned after population and variant selection. Canvas bounds include accepted
component fragments and board artwork; an empty opposite-side fragment does not
expand them.

Uniform component opacity is set once on the final occurrence group after the
surface/open-space union. HLR remains opaque, so this is an illustration
approximation rather than transparent-aware hidden-line removal. Toon reports
`partial-opacity-opaque-occlusion` for that limitation.

## Ordinary assembly HLR versus Toon illustration

`ASSEMBLY_HLR_TOP/BOTTOM` in `pcb-svg` is distinct from Toon's shaded
`ILLUSTRATION_TOP/BOTTOM` layer. The ordinary assembly modes map as follows:

| Config mode | Behavior |
| --- | --- |
| `detail` | Geometer Fast HLR detail using Fast mesh-shadow outlines by default |
| `outline` | Outline-only projection; `simple` is its legacy alias |
| `bounding_box` | Component pad-bounds rectangle; no Geometer call |
| `none` | No assembly projection |

Explicit `projection_algorithm: exact` or `poly` selects the corresponding
legacy backend. Fast is otherwise the default. Toon component illustrations
use the mesh illustration/HLR path that also supplies shaded geometry and the
surface/open-space pair described above.

## Determinism, concurrency, and caching

Native work is bounded by `--workers` (default four). Each worker owns a native
Geometer process. Unique cache misses may finish out of order, but results,
warnings, symbols, and occurrence groups are committed in source order. A
serial run and a parallel run must therefore produce the same SVG bytes for the
same inputs, dependencies, config, and cache state.

Cache identity includes model content, root/body/occurrence transforms,
materials, requested side, region/envelope identity, normalized clipping
planes, region-query tolerance, clip tolerance, cap policy, and relevant
illustration settings. The
surface/open-space composition policy is also versioned internally. Successful
empty fragments are cacheable. Failed or incomplete bodies are not persisted as
successful component artwork and are retried on a later invocation. Cache files
are disposable implementation artifacts, not public interchange contracts.

## Diagnostics and failure policy

Recoverable body and geometry conditions are queued during rendering. At the
end of the command, `--warnings summary|all|none` controls console presentation;
`--warning-report` writes the complete deterministic
`toon.warning_report.a0` payload. Worker completion order does not change
diagnostic order. Common nonfatal conditions include:

- no renderable model;
- unsupported or unavailable model data;
- partial native tessellation or degenerate geometry warnings;
- ambiguous region or rotation fallback; and
- opaque-occlusion handling for partially transparent instances.

Invalid command/config input, native process/protocol failure, timeout, and
output-write failure remain fatal. A warning mode never changes report content
or converts a failed command into success.

## Deliberate limitations

- Boards are rendered flat. Rigid-flex bend lines do not deform board or
  component geometry.
- One component surface branch uses one equivalent stack envelope. A body
  spanning unlike envelopes cannot be clipped correctly by one Z plane and
  uses the documented conservative fallback.
- Bounding boxes are a conservative region-query acceleration, not exact
  mounting-pad or model-footprint authority. Irregular footprints can touch a
  region that their actual geometry does not.
- Intersecting analytic bodies are projected independently. Toon does not
  perform general solid booleans, so complex sphere/cylinder/extrusion unions
  can expose internal boundaries or imperfect occlusion.
- `cap_policy: none` leaves cut boundaries unfilled.
- Partial opacity is applied after opaque HLR and is not physically correct
  transparent rendering.
- Unsupported non-STEP attachment formats are not converted.
- Free board-level bodies are supported where placement is resolvable, but
  unusual ownership/placement encodings can fall back or warn.
- Silkscreen clipping is a 2D film-domain policy; it is not fabrication-rule
  verification.

These limitations must be preserved in public release notes unless the
underlying algorithm and qualification fixtures are changed.

## Qualification strategy

The Issue 67 closeout uses ordered visual and automated gates: single
through-hole and SMT placements, edge/cutout overhangs, a reverse-mount LED and
straddle connector, the reporter board, two rigid-flex boards, generated
analytic bodies, a board-level free STEP body, selected real-world boards, and
the ordinary PCB SVG path. The durable review gallery is generated by
`tests/support_scripts/svg_review_gallery.py` and split into per-gate pages so
large SVGs are loaded only when reviewed.

Tests should prefer structural invariants and deliberately asymmetric geometry
over whole-file goldens. Release qualification adds deterministic serial versus
parallel output checks, cache cold/warm behavior, runtime and output-size
evidence, contract checks, packaging/install checks, an independent algorithm
audit, and final owner review of SVGs generated by the exact candidate.
