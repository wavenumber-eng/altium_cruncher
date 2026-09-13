# Toon isometric-view feasibility — 2026-09-13

## Status

Deferred. The current priority remains the core two-dimensional Toon and SVG
pipeline. This note preserves the feasibility analysis and a likely ownership
boundary if isometric views are resumed.

## Question

Can Toon add orthographic `iso-top` and `iso-bottom` views while retaining the
existing composable PCB SVG layers, cached component illustrations, metadata,
and editor-friendly groups? Which work belongs in Altium Cruncher and which
belongs in Geometer?

## Conclusion

The feature is feasible with a hybrid renderer:

- Altium Cruncher can reuse existing planar PCB SVG artwork and project each
  fixed-Z layer with an SVG affine matrix.
- Geometer should render the geometry that is actually three-dimensional:
  STEP models, analytic component bodies, the board substrate and their
  shading and internal visibility.
- Cruncher should compose the projected layers, place cached component
  symbols, preserve metadata, and calculate the final canvas.

This avoids rebuilding copper, solder-mask, silkscreen, text, drill and SVG
metadata behavior inside Geometer.

The principal limitation is visibility between independently rendered
components. A first implementation can use component-level depth ordering. An
exact result for intersecting projected depth ranges would require a native
whole-scene illustration operation.

## Why planar SVG projection works

An isometric view is an orthographic projection. For a point on a fixed plane
`z = constant`, projection onto the camera's right and up axes is affine in the
point's original `x` and `y` coordinates:

```text
projected_x = dot([x, y, z], camera_right)
projected_y = dot([x, y, z], camera_up)
```

For a fixed `z`, these equations reduce to a two-dimensional linear transform
plus translation. Each completed PCB layer group can therefore be wrapped in
an SVG `matrix(a b c d e f)` transform. Layers on different physical Z planes
share the linear part and receive different translations.

This is exact for orthographic projection. It preserves the existing vector
paths, masks, clip paths, polygons, arcs, text, special-string resolution,
metadata and Inkscape layer grouping. There is no need to reconstruct raw
Altium primitives after the ordinary PCB SVG layer has been rendered.

A planar transform cannot create board thickness, board-edge walls, cutout
walls, hole walls, component depth or three-dimensional occlusion. Perspective
projection would also be outside this technique because an SVG affine matrix
does not express perspective.

## Existing implementation foundations

Altium Cruncher already has the relevant composition seams:

- `PcbSvgA0Renderer` materializes and composes individual physical and virtual
  SVG layer fragments.
- `PcbSvgRenderJob` caches board contexts, resolved layer stacks, fragments,
  component sessions and native workers.
- Component illustrations are stored as reusable SVG symbols and placed with
  `<use>` translations.
- The resolved Altium layer-stack API supplies total thickness and local
  top/bottom Z envelopes.

Geometer already has the projection and rendering foundation:

- The HLR and illustration demos define top and bottom isometric camera poses.
- Illustration preparation normalizes the requested direction/up vectors and
  derives the orthographic right/up basis.
- `geometry.mesh_illustration.geometry.a0` returns target-independent projected
  geometry rather than requiring SVG output.
- Fast detail, Fast Mesh Shadow, material shading, surface ordering and
  same-color surface fusion operate in native code.

## Component reuse

Under orthographic projection, translating a three-dimensional occurrence
produces a two-dimensional translation of its projected result. Cruncher can
therefore render and cache component artwork by the properties that change its
appearance:

- model identity;
- complete local three-dimensional pose and side;
- material/style;
- selected ISO camera and illustration settings.

Absolute board X/Y placement does not need to be baked into the symbol. The
component anchor, including its Z coordinate, can be projected at composition
time and used as the `<use>` translation.

A rendered ISO symbol generally cannot be rotated in two dimensions to stand
in for another component rotation. Rotating a 3D model before projection
changes visible surfaces, depth and shading. Separate cached symbols are needed
for distinct poses. Common occurrences should still collapse to a small number
of model/pose combinations.

## Board body and surface artwork

The lowest-cost prototype could show a flat projected board, but the useful
production design should expose board thickness:

1. Cruncher resolves the board outline, eligible cutouts and stack thickness.
2. The planned analytic Geometer model boundary receives that outline as an
   extrusion between the resolved bottom and top Z values.
3. Geometer returns shaded board-body geometry with visible side walls.
4. Cruncher places the ordinary top or bottom SVG artwork on the corresponding
   surface Z plane using the shared camera frame.

Thousands of drill bores should not automatically become analytic wall
geometry. Existing surface masks can continue to show drills. Visible bore
walls can be added later if visual review shows enough benefit to justify the
additional geometry.

## Visibility and paint order

Rendering each component independently gives exact visibility among the bodies
inside that component, but not between different components. Projected
components overlap more often in an ISO view than in a top-down view.

A practical first implementation can:

1. project the occurrence bounds and depth interval;
2. sort components whose intervals establish an unambiguous order;
3. use a stable component-level painter order for remaining overlaps;
4. record or count ambiguous overlaps for visual qualification.

If this produces unacceptable artifacts, the precise solution is a Geometer
scene boundary with model definitions and occurrence transforms. Native code
would then perform visibility across the complete board scene. That is a larger
API and performance project and is not required to prove or initially ship ISO
views.

## Proposed ownership

### Altium Cruncher

- Project, variant, population and side selection.
- Toon view configuration and ISO camera-preset selection.
- Existing PCB physical and virtual layer rendering.
- Assignment of artwork to physical Z planes.
- SVG affine transforms for planar layers.
- Projected occurrence-anchor placement and symbol caching.
- Component-level paint ordering and ambiguity diagnostics.
- Final projected bounds/viewBox, SVG metadata and editor group names.

### Geometer

- STEP/model ingestion and tessellation.
- Analytic extrusion, cylinder and sphere handling.
- Camera normalization and orthographic projection.
- Fast detail, Fast Mesh Shadow, shading and same-color fusion.
- Visibility and ordering within a requested model or analytic scene.
- Shaded analytic board-substrate extrusion.
- A future whole-scene visibility operation if component-level ordering proves
  insufficient.

## Useful addition to the planned model-illustration boundary

The future result should expose enough projection data for Cruncher to align
native illustrations with ordinary SVG layers without independently recreating
camera rules:

- resolved normalized `right`, `up` and `direction` vectors;
- handedness or resolved `mirror_x`;
- projected two-dimensional bounds;
- source three-dimensional bounds;
- projected depth interval;
- explicit length units.

These fields can be added to the new model-illustration result without changing
the existing mesh-illustration A0 contract.

## Possible configuration direction

Projection belongs to a view rather than being represented as separate ISO
layer kinds. One possible additive shape is:

```jsonc
{
  "name": "iso-top",
  "projection": {
    "kind": "orthographic",
    "preset": "iso_top"
  },
  "layers": [
    "BOARD_SUBSTRATE",
    "TOP",
    "SOLDERMASK_FILM_TOP",
    "TOPOVERLAY",
    "BOARD_OUTLINE",
    "ILLUSTRATION_TOP"
  ]
}
```

The contract could later allow explicit `direction` and `up` vectors while the
generated Toon configuration uses stable `iso_top` and `iso_bottom` presets.
The existing `mirror` setting should not carry the camera semantics by itself.

## Suggested implementation slices if resumed

1. Add the resolved projection frame and bounds to the planned Geometer
   model-illustration result.
2. Prototype transformed planar groups and ISO component symbols without board
   thickness.
3. Add the analytic board extrusion using resolved stack thickness.
4. Add projected canvas bounds, occurrence caching and component-level depth
   ordering.
5. Visually qualify top and bottom views on a small mixed-model board and at
   least one dense board.
6. Measure ambiguous component overlaps before deciding whether a native
   whole-scene operation is warranted.

## Resume criteria

Resume this work after the core 2D Toon/model-illustration boundary is stable,
or when a concrete application needs ISO thumbnails. Treat exact whole-board
occlusion as a separate decision driven by visual failures, not as a prerequisite
for the initial ISO feature.
