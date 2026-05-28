"""Config helpers for PCB layer STEP fixture-alignment output."""

from __future__ import annotations

import re

from altium_monkey.altium_record_types import PcbLayer

PCB_LAYER_STEP_DEFAULT_CONFIG_TEXT = """{
  /* pcb-layer-step creates compact fixture-alignment models, not full
     fabrication STEP exports. Keep only the features that help verify pogo-pin
     alignment against DUT pads. */
  /*

     CONFIG SHAPE

       "defaults"
         Shared settings copied into every output.

       "outputs"
         One or more output definitions. Each output accepts the same fields as
         defaults and overrides only what it needs.


     COORDINATES

       Geometer receives XY geometry relative to the Altium board placement
       origin: (absolute source mils - Board.ORIGINX/Y) converted to mm.

       "z_mm" controls the bottom Z plane of each body.
       "thickness_mm" controls extrusion thickness.


     COMMON OUTPUT FIELDS

       name
       output_step
       pcbdoc
       layer
       z_mm
       thickness_mm

       copper_color
       include_copper
       include_board_outline
       include_board_cutouts
       include_poured_polygons
       cut_holes

       drill_hole_mode
       max_boolean_drill_cuts
       drill_hole_color
       drill_plated_hole_color
       drill_non_plated_hole_color
       drill_overlay_thickness_mm
       drill_minimum_diameter_mm
       drill_hole_shape
       drill_ring_width_mm
       drill_plated_ring_shape

       fuse_copper
       fuse_board_outline
       arc_segments

       include_tracks
       include_arcs
       include_fills
       include_regions
       include_vias
       include_component_pads
       include_free_pads
       include_designators
       pad_color_rules


     STRUCTURED SECTIONS

       "board_outline"
         color:        STEP color for the outer board-outline body.
         cutout_color: STEP color for interior board-cutout outline bodies.
         cutouts:      true/false, include separate cutout outline bodies.
         width_mm:     visual stroke width for outline bodies.
         fuse:         true/false, request Geometer fusion for outline bodies.

       "features"
         tracks:   true/false, include copper tracks.
         arcs:     true/false, include copper arcs.
         fills:    true/false, include fill rectangles.
         polygons: true/false, include poured-polygon primitives.
         regions:  true/false, include copper region primitives.
         vias:     true/false, include via copper.
         free_pads: true/false, include pads not owned by a component.

         component_pads can be a boolean or an object:

           false
             omit all component-owned pads.

           true
             include component-owned pads. If include_designators is empty or
             omitted, all component-owned pads are included.

           {"mode": "none"}
             omit all component-owned pads.

           {"mode": "all"}
             include component-owned pads. Leave include_designators empty for
             all component-owned pads.

           {"mode": "matching_designators", "include_designators": [...]}
             include component-owned pads whose component designator matches at
             least one pattern.

       "colors"
         default_copper: STEP color for copper that no pad rule captures.
         pad_rules:      list of per-designator color/body rules.

         Each pad rule supports:
           designators: pattern list, such as ["TP*"].
           color:       named color or #RRGGBB.
           body:        Geometer body id/name for the matched pads.

       "drills"
         mode:                 auto, cut, overlay, or none.
         minimum_diameter_mm:  omit drills smaller than this diameter.
         shape:                solid or ring.
         color:                default drill-overlay color.
         plated_color:         plated drill-overlay color.
         non_plated_color:     non-plated drill-overlay color.
         ring_width_mm:        fixed annulus width when shape is ring.
         plated_ring_shape:    annulus or pad.
         overlay_thickness_mm: Z thickness for overlay drill bodies.


     DESIGNATOR PATTERNS

       Patterns are case-insensitive shell-style matches.

       Examples:
         ["TP*"]
         ["TP*", "J*", "U1", "U2"]
         ["M*"]


     COLOR VALUES

       Colors may be #RRGGBB values or one of these names:

         black, blue, brown, copper, gray, green, grey, orange, purple,
         red, white, yellow.


     LAYER VALUES

       Common selectors are bottom, top, BOTTOM, TOP, layer id numbers, or
       native/display layer names accepted by altium-cruncher.


     DRILL MODES

       none
         Omit drill visualization.

       cut
         Subtract drill holes from copper bodies.

       overlay
         Render separate visible drill-reference bodies.

       auto
         Cut small drill sets. Switch to overlays when the board has more than
         max_boolean_drill_cuts drill features.


     DRILL SHAPES

       solid
         Render drill disks or slotted capsules.

       ring
         Render rings with the drill hole removed.

       plated_ring_shape "annulus"
         Use a fixed-width ring around plated holes.

       plated_ring_shape "pad"
         Use the full plated pad outline as the ring. This is useful for
         mounting-hole pads such as M1.


     CLI OVERRIDES

       CLI overrides are available for the main layer, color, outline, drill,
       fusion, and Z/thickness settings. Run:

         altium-cruncher pcb-layer-step --help

  */
  "schema": "wn.altium_cruncher.pcb_layer_step.config.v2",
  "defaults": {
    "pcbdoc": null,
    "layer": "bottom",
    "z_mm": 0.0,
    "thickness_mm": 0.035,
    "include_board_outline": true,
    "board_outline": {
      "color": "#111111",
      "cutout_color": "#FF0000",
      "cutouts": true,
      "width_mm": 0.2,
      "fuse": true
    }
  },
  "outputs": [
    {
      "name": "fixture_alignment",
      "output_step": "{board}__fixture_alignment.step",
      "features": {
        /* Use include_designators for component-owned pads. Examples:
           ["TP*"] or ["TP*", "J*", "U1", "U2"]. */
        "component_pads": {
          "mode": "matching_designators",
          "include_designators": ["TP*"]
        },
        "free_pads": false,
        "tracks": false,
        "arcs": false,
        "fills": false,
        "polygons": false,
        "regions": false,
        "vias": false
      },
      "colors": {
        "default_copper": "#B87333",
        "pad_rules": [
          {
            "designators": ["TP*"],
            "color": "red",
            "body": "test_points"
          }
        ]
      },
      "drills": {
        /* none omits drills, cut performs boolean holes, overlay draws a
           separate drill-reference body. */
        "mode": "overlay",
        "minimum_diameter_mm": 0.85,
        "shape": "ring",
        "color": "#666666",
        "plated_color": "#666666",
        "non_plated_color": "#00AEEF",
        "ring_width_mm": 0.12,
        "plated_ring_shape": "pad",
        "overlay_thickness_mm": 0.001
      },
      "fuse_copper": false
    }
  ]
}
"""


def resolve_pcb_layer_selector(selector: str | int | PcbLayer | None) -> PcbLayer:
    """Resolve CLI/user layer selectors to a native Altium PCB layer enum."""
    if selector is None:
        return PcbLayer.BOTTOM
    if isinstance(selector, PcbLayer):
        return selector
    if isinstance(selector, int):
        return PcbLayer(selector)

    text = str(selector).strip()
    if not text:
        return PcbLayer.BOTTOM
    if text.isdigit():
        return PcbLayer(int(text))

    normalized = _normalize_layer_selector(text)
    if normalized.startswith("L") and normalized[1:].isdigit():
        return PcbLayer(int(normalized[1:]))

    layer = _layer_aliases().get(normalized) or _layer_by_native_name(normalized)
    if layer is None:
        raise ValueError(f"Unknown PCB layer selector: {selector!r}")
    return layer


def _normalize_layer_selector(value: str) -> str:
    return re.sub(r"[\s_\-]+", "", value).upper()


def _layer_aliases() -> dict[str, PcbLayer]:
    return {
        "TOP": PcbLayer.TOP,
        "TOPLAYER": PcbLayer.TOP,
        "FRONT": PcbLayer.TOP,
        "BOTTOM": PcbLayer.BOTTOM,
        "BOTTOMLAYER": PcbLayer.BOTTOM,
        "BOT": PcbLayer.BOTTOM,
        "BACK": PcbLayer.BOTTOM,
        "MULTILAYER": PcbLayer.MULTI_LAYER,
    }


def _layer_by_native_name(normalized: str) -> PcbLayer | None:
    for layer in PcbLayer:
        names = {
            _normalize_layer_selector(layer.name),
            _normalize_layer_selector(layer.to_json_name()),
            _normalize_layer_selector(layer.to_display_name()),
        }
        if normalized in names:
            return layer
    return None
