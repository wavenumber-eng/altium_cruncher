"""Config helpers for PCB layer STEP fixture-alignment output."""

from __future__ import annotations

from copy import deepcopy
import re

from altium_monkey.altium_record_types import PcbLayer

from altium_cruncher.altium_cruncher_mco import JsonObject, loads_jsonc
from altium_cruncher.config_json import enum_help, render_commented_jsonc

PCB_LAYER_STEP_DEFAULT_CONFIG_TEXT = """{
  /* pcb-layer-step creates compact fixture-alignment models, not full
     fabrication STEP exports. Keep only the features that help verify pogo-pin
     alignment against DUT pads.

     This file is JSONC, not strict JSON. Comments and trailing commas are
     accepted. Newly generated configs use the .jsonc extension; older
     pcb-layer-step.json files are still accepted when explicitly passed or
     already present next to a board.

     Feature bodies are extruded by Geometer from 2D regions. Normal layer
     thickness is controlled by thickness_mm. Feature-specific
     thickness_bias_mm values are symmetric: a 0.010 mm bias moves that body's
     bottom down by 0.010 mm and adds 0.020 mm to its extrusion thickness.
     This prevents z-fighting when pads, vias, polygons, and traces overlap
     but are rendered as different colored STEP bodies. */
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
       drill_selected_component_mode
       drill_other_component_mode
       drill_free_pad_mode
       drill_via_mode

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


     STRUCTURED SECTIONS

       "board_outline"
         color:        STEP color for the outer board-outline body.
         cutout_color: STEP color for interior board-cutout outline bodies.
         cutouts:      true/false, include separate cutout outline bodies.
         width_mm:     visual stroke width for outline bodies.
         fuse:         true/false, request Geometer fusion for outline bodies.

       "features"
         Each feature can be a simple true/false or an object:

           {
             "enabled": true,
             "color": "#RRGGBB",
             "step_body_name": "body_name",
             "thickness_bias_mm": 0.010
           }

         Object form both enables the feature and splits it into a named,
         independently colored STEP body. STEP body names should be stable ASCII
         ids. The tokens {component}, {pad}, and {feature} are replaced per
         source feature before sanitizing the STEP body name.

         defaults: fallback feature styling. color is the fallback copper color.
         tracks:   copper track primitives.
         arcs:     copper arc primitives.
         fills:    copper fill rectangles.
         polygons: poured-polygon primitives from tracks, arcs, fills, or regions.
         regions:  non-polygon copper region primitives.
         vias:     via copper pads.
         free_pads: pads not owned by a component.

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

           component_pads object form also accepts enabled, color,
           step_body_name, thickness_bias_mm, and highlight_rules.

         highlight_rules split matching component/free pads into named STEP
         bodies. Each rule supports:
           designators:     pattern list, such as ["TP*"].
           color:           named color or #RRGGBB.
           step_body_name:  Geometer body id/name for the matched pads.

       "drills"
         mode:                 Options: auto, cut, overlay, none.
         selected_component_mode:
                               Options: inherit, cut, overlay, none for drills on
                               selected component pads.
         other_component_mode: Options: inherit, cut, overlay, none for drills on
                               component pads not selected by component_pads.
         free_pad_mode:        Options: inherit, cut, overlay, none for drills on pads
                               not owned by a component.
         via_mode:             Options: inherit, cut, overlay, none for via holes.
         minimum_diameter_mm:  omit drills smaller than this diameter.
         shape:                Options: solid, ring.
         color:                default drill-overlay color.
         plated_color:         plated drill-overlay color.
         non_plated_color:     non-plated drill-overlay color.
         ring_width_mm:        fixed annulus width when shape is ring.
         plated_ring_shape:    annulus.
         overlay_thickness_mm: Z thickness for overlay drill bodies.

       Per-feature "thickness_bias_mm"
         tracks/arcs/fills: connecting copper defaults to 0.0 mm.
         polygons/regions:  poured or region copper defaults to 0.003 mm.
         vias:              via copper defaults to 0.006 mm.
         component_pads/free_pads: pad copper defaults to 0.010 mm.


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
         Render separate visible drill-reference bodies. Copper is still clipped
         at the same drill holes so holes do not fill with copper.

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


     CLI OVERRIDES

       CLI overrides are available for the main layer, color, outline, drill,
       fusion, and Z/thickness settings. Run:

         altium-cruncher pcb-layer-step --help

  */
  "schema": "wn.altium_cruncher.pcb_layer_step.config.v2",
  "defaults": {
    "pcbdoc": null, /* optional PcbDoc selector when a PrjPcb contains more than one board */
    "layer": "bottom", /* layer selector: bottom, top, native layer name, or layer id */
    "z_mm": 0.0,
    "thickness_mm": 0.035,
    "include_board_outline": true,
    "board_outline": {
      "color": "#FFFF00",
      "cutout_color": "#FFFF00",
      "cutouts": true,
      "width_mm": 0.2,
      "fuse": true
    }
  },
  "outputs": [
    {
      "name": "fixture_alignment", /* output id for {output}/{Output} filename tokens */
      "output_step": "{board}__fixture_alignment.step", /* supports {board}, {Board}, {layer}, {Layer}, {output}, {Output} */
      "features": {
        /* Use include_designators for component-owned pads. Examples:
           ["TP*"] or ["TP*", "J*", "U1", "U2"].
           Feature color accepts named colors or #RRGGBB.
           step_body_name is the Geometer STEP body id. */
        "defaults": {
          "color": "#B87333" /* fallback copper color for unspecified features */
        },
        "component_pads": {
          "mode": "matching_designators", /* Options: none, all, matching_designators */
          "include_designators": ["TP*", "M*"], /* case-insensitive shell patterns */
          "color": "#B87333",
          "step_body_name": "component_pads",
          "thickness_bias_mm": 0.010,
          "highlight_rules": [
            {
              "designators": ["TP*"], /* case-insensitive shell patterns */
              "color": "red",
              "step_body_name": "test_points"
            }
          ]
        },
        "free_pads": {
          "enabled": false,
          "color": "#B87333",
          "step_body_name": "free_pads",
          "thickness_bias_mm": 0.010
        },
        "tracks": {
          "enabled": false,
          "color": "#B87333",
          "step_body_name": "tracks",
          "thickness_bias_mm": 0.0
        },
        "arcs": {
          "enabled": false,
          "color": "#B87333",
          "step_body_name": "arcs",
          "thickness_bias_mm": 0.0
        },
        "fills": {
          "enabled": false,
          "color": "#B87333",
          "step_body_name": "fills",
          "thickness_bias_mm": 0.0
        },
        "polygons": {
          "enabled": false,
          "color": "#7A8F2A",
          "step_body_name": "polygons",
          "thickness_bias_mm": 0.003
        },
        "regions": {
          "enabled": false,
          "color": "#7A8F2A",
          "step_body_name": "regions",
          "thickness_bias_mm": 0.003
        },
        "vias": {
          "enabled": false,
          "color": "#C08540",
          "step_body_name": "vias",
          "thickness_bias_mm": 0.006
        }
      },
      "drills": {
        /* none omits drills, cut performs boolean holes, overlay draws a
           separate drill-reference body. Scoped modes override mode for
           selected components, unselected components, free pads, or vias. */
        "mode": "overlay", /* auto, cut, overlay, or none */
        "selected_component_mode": "cut", /* inherit, cut, overlay, or none */
        "other_component_mode": "none", /* inherit, cut, overlay, or none */
        "free_pad_mode": "overlay", /* inherit, cut, overlay, or none */
        "via_mode": "inherit", /* inherit, cut, overlay, or none */
        "minimum_diameter_mm": 0.85,
        "shape": "ring", /* Options: solid, ring */
        "color": "#666666",
        "plated_color": "#666666",
        "non_plated_color": "#00AEEF",
        "ring_width_mm": 0.12,
        "plated_ring_shape": "annulus", /* annulus */
        "overlay_thickness_mm": 0.001
      },
      "fuse_copper": false
    }
  ]
}
"""


_PCB_LAYER_STEP_HEADER_LINES = (
    "pcb-layer-step creates compact fixture-alignment models, not full fabrication STEP exports.",
    "This file is JSONC, not strict JSON. Comments and trailing commas are accepted.",
    "Feature bodies are extruded by Geometer from 2D regions.",
    "thickness_mm controls nominal layer thickness; thickness_bias_mm is symmetric and prevents z-fighting.",
    "",
    "CONFIG SHAPE",
    "defaults: shared settings copied into every output.",
    "outputs: one or more output definitions; each output overrides only what it needs.",
    "",
    "COMMON OUTPUT FIELDS",
    "name, output_step, pcbdoc, layer, z_mm, thickness_mm",
    "copper_color, include_copper, include_board_outline, include_board_cutouts",
    "include_poured_polygons, cut_holes, drill_hole_mode, max_boolean_drill_cuts",
    "drill_hole_color, drill_plated_hole_color, drill_non_plated_hole_color",
    "drill_overlay_thickness_mm, drill_minimum_diameter_mm, drill_hole_shape",
    "drill_ring_width_mm, drill_plated_ring_shape, drill_selected_component_mode",
    "drill_other_component_mode, drill_free_pad_mode, drill_via_mode",
    "fuse_copper, fuse_board_outline, arc_segments",
    "include_tracks, include_arcs, include_fills, include_regions, include_vias",
    "include_component_pads, include_free_pads, include_designators",
    "",
    "DESIGNATOR PATTERNS",
    'Patterns are case-insensitive shell-style matches, for example ["TP*"], ["TP*", "J*", "U1"], or ["M*"].',
    "",
    "COLOR VALUES",
    "Colors may be #RRGGBB values or these names: black, blue, brown, copper, gray, green, grey, orange, purple, red, white, yellow.",
    "",
    "DRILL MODES",
    "Options: none, cut, overlay, auto. Scoped modes add inherit.",
    "",
    "DRILL SHAPES",
    "Options: solid, ring. plated_ring_shape options: annulus.",
    "",
    "CLI OVERRIDES",
    "Run: altium-cruncher pcb-layer-step --help",
)

_PCB_LAYER_STEP_COMMENTS: dict[tuple[str, ...], str | tuple[str, ...]] = {
    ("schema",): "pcb-layer-step config contract id.",
    ("defaults",): "Shared settings merged into each output.",
    (
        "defaults",
        "pcbdoc",
    ): "Optional PcbDoc selector when a PrjPcb contains more than one board.",
    ("defaults", "layer"): enum_help(
        "PCB layer selector.",
        ("bottom", "top", "native layer name", "layer id"),
    ),
    ("defaults", "z_mm"): "Bottom Z plane for generated bodies.",
    ("defaults", "thickness_mm"): "Nominal extrusion thickness before feature bias.",
    ("defaults", "include_board_outline"): "Include separate board-outline body.",
    ("defaults", "board_outline"): "Board outline and cutout body styling.",
    (
        "defaults",
        "board_outline",
        "color",
    ): "STEP color for the outer board outline body.",
    (
        "defaults",
        "board_outline",
        "cutout_color",
    ): "STEP color for interior board cutout outline bodies.",
    (
        "defaults",
        "board_outline",
        "cutouts",
    ): "Include separate bodies around interior board cutouts.",
    (
        "defaults",
        "board_outline",
        "width_mm",
    ): "Outline stroke body width in millimeters.",
    (
        "defaults",
        "board_outline",
        "fuse",
    ): "Request Geometer planar fusion for outline bodies.",
    (
        "outputs",
    ): "Output definitions. Each item inherits defaults and overrides selected fields.",
    ("outputs", "name"): "Output id for filename tokens and logs.",
    (
        "outputs",
        "output_step",
    ): "Output STEP path template. Supports {board}, {Board}, {layer}, {Layer}, {output}, and {Output}.",
    (
        "outputs",
        "features",
    ): "Copper feature selection, color, body-name, and thickness-bias policy.",
    (
        "outputs",
        "features",
        "defaults",
    ): "Fallback feature styling. color is the fallback copper color.",
    (
        "outputs",
        "features",
        "component_pads",
    ): "Component-owned pad selection and styling.",
    ("outputs", "features", "component_pads", "mode"): enum_help(
        "Component pad mode.",
        ("none", "all", "matching_designators"),
    ),
    (
        "outputs",
        "features",
        "component_pads",
        "include_designators",
    ): "Case-insensitive shell patterns for component designators.",
    (
        "outputs",
        "features",
        "component_pads",
        "highlight_rules",
    ): "Rules that split matching component pads into separately colored STEP bodies.",
    (
        "outputs",
        "features",
        "component_pads",
        "highlight_rules",
        "designators",
    ): "Case-insensitive shell patterns for this highlight rule.",
    ("outputs", "features", "free_pads"): "Pads not owned by a component.",
    ("outputs", "features", "tracks"): "Copper track primitives.",
    ("outputs", "features", "arcs"): "Copper arc primitives.",
    ("outputs", "features", "fills"): "Copper fill rectangles.",
    ("outputs", "features", "polygons"): "Poured polygon copper primitives.",
    ("outputs", "features", "regions"): "Non-polygon copper region primitives.",
    ("outputs", "features", "vias"): "Via copper pad primitives.",
    ("outputs", "drills"): "Drill and slot visualization policy.",
    ("outputs", "drills", "mode"): enum_help(
        "Global drill mode.",
        ("auto", "cut", "overlay", "none"),
    ),
    ("outputs", "drills", "selected_component_mode"): enum_help(
        "Drill mode for pads selected by component_pads.",
        ("inherit", "cut", "overlay", "none"),
    ),
    ("outputs", "drills", "other_component_mode"): enum_help(
        "Drill mode for unselected component-owned pads.",
        ("inherit", "cut", "overlay", "none"),
    ),
    ("outputs", "drills", "free_pad_mode"): enum_help(
        "Drill mode for pads not owned by a component.",
        ("inherit", "cut", "overlay", "none"),
    ),
    ("outputs", "drills", "via_mode"): enum_help(
        "Drill mode for via holes.",
        ("inherit", "cut", "overlay", "none"),
    ),
    (
        "outputs",
        "drills",
        "minimum_diameter_mm",
    ): "Omit drill overlays/cuts below this diameter.",
    ("outputs", "drills", "shape"): enum_help(
        "Overlay shape.",
        ("solid", "ring"),
    ),
    ("outputs", "drills", "color"): "Default STEP color for drill overlay bodies.",
    (
        "outputs",
        "drills",
        "plated_color",
    ): "STEP color for plated drill overlay bodies.",
    (
        "outputs",
        "drills",
        "non_plated_color",
    ): "STEP color for non-plated drill overlay bodies.",
    (
        "outputs",
        "drills",
        "ring_width_mm",
    ): "Fixed annulus width when drill shape is ring.",
    ("outputs", "drills", "plated_ring_shape"): enum_help(
        "Plated drill ring policy.",
        ("annulus",),
    ),
    (
        "outputs",
        "drills",
        "overlay_thickness_mm",
    ): "Z thickness for separate drill overlay bodies.",
    ("outputs", "fuse_copper"): "Request Geometer planar fusion for copper bodies.",
}

_PCB_LAYER_STEP_KEY_COMMENTS: dict[str, str] = {
    "enabled": "Enable this feature body.",
    "color": "STEP color for this body or rule.",
    "step_body_name": "Stable Geometer STEP body id/name.",
    "thickness_bias_mm": "Symmetric Z bias that prevents overlapping colored bodies from z-fighting.",
    "designators": "Case-insensitive shell-style designator patterns.",
}


def pcb_layer_step_default_config_text() -> str:
    """Render the editable pcb-layer-step default config through the shared renderer."""
    return render_commented_jsonc(
        default_pcb_layer_step_config_payload(),
        comments_by_path=_PCB_LAYER_STEP_COMMENTS,
        comments_by_key=_PCB_LAYER_STEP_KEY_COMMENTS,
        header_lines=_PCB_LAYER_STEP_HEADER_LINES,
    )


def default_pcb_layer_step_config_payload() -> JsonObject:
    """Return the parsed generated pcb-layer-step JSONC default config."""
    payload = loads_jsonc(PCB_LAYER_STEP_DEFAULT_CONFIG_TEXT)
    if not isinstance(payload, dict):
        raise ValueError("Internal pcb-layer-step default config must be an object")
    return deepcopy(payload)


def default_pcb_layer_step_output_payload() -> JsonObject:
    """Return the first generated output with defaults applied."""
    payload = default_pcb_layer_step_config_payload()
    defaults = payload.get("defaults", {})
    outputs = payload.get("outputs", [])
    if not isinstance(defaults, dict):
        raise ValueError("Internal pcb-layer-step defaults must be an object")
    if not isinstance(outputs, list) or not outputs or not isinstance(outputs[0], dict):
        raise ValueError("Internal pcb-layer-step default output is missing")

    merged: JsonObject = deepcopy(defaults)
    merged.update(deepcopy(outputs[0]))
    return merged


def default_pcb_layer_step_mate_artifact_payload() -> JsonObject:
    """Return the mate artifact form of the generated pcb-layer-step default."""
    output = default_pcb_layer_step_output_payload()
    source_layer = output.get("layer", "bottom")
    artifact: JsonObject = {
        "enabled": True,
        "source_layer": str(source_layer or "bottom"),
    }
    for key, value in output.items():
        if key in {"name", "output_step", "pcbdoc", "layer"}:
            continue
        artifact[key] = deepcopy(value)
    artifact["insert_in_output"] = {
        "enabled": True,
        "z_mm": 8.5,
        "layer": "MECHANICAL_13",
        "side": "TOP",
    }
    artifact["highlights"] = [
        {
            "projection": "test_points",
            "color": "#FF0000",
        }
    ]
    return artifact


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
