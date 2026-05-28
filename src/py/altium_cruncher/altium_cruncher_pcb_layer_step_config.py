"""Config helpers for PCB layer STEP fixture-alignment output."""

from __future__ import annotations

import re

from altium_monkey.altium_record_types import PcbLayer

PCB_LAYER_STEP_DEFAULT_CONFIG_TEXT = """{
  /* pcb-layer-step creates compact fixture-alignment models, not full
     fabrication STEP exports. Keep only the features that help verify pogo-pin
     alignment against DUT pads. */
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
        "tracks": true,
        "arcs": true,
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
