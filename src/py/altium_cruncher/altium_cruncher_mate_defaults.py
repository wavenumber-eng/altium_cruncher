"""Default mate config payload helpers."""

from __future__ import annotations

from pathlib import Path

from altium_cruncher.altium_cruncher_mco import JsonObject
from altium_cruncher.altium_cruncher_pcb_layer_step_config import (
    default_pcb_layer_step_mate_artifact_payload,
)

DEFAULT_MATE_BOARD_OUTLINE_MARGIN_MILS = 250.0


def default_mate_output_payload() -> JsonObject:
    return {
        "backend": "altium",
        "output_dir": "output/mate",
        "project_name": "mate",
        "schematic_sheet_style": "D",
        "origin": "preserve_source",
        "board_outline": {
            "mode": "source_bounds_with_margin",
            "margin_mils": DEFAULT_MATE_BOARD_OUTLINE_MARGIN_MILS,
        },
        "overwrite": False,
        "layer_stack_template": "2-layer",
    }


def mate_known_parts_payload(
    known_parts_manifest: Path | str | None,
) -> JsonObject:
    if known_parts_manifest is None:
        return default_known_parts_payload()
    return {"manifest": str(known_parts_manifest)}


def default_mate_label_style_payload() -> JsonObject:
    return {
        "height_mils": 65,
        "layer": "TOP_OVERLAY",
        "font_kind": "truetype",
        "font_name": "Arial",
        "bold": True,
        "stroke_width_mils": 10,
        "text_justification": "RIGHT_TOP",
    }


def default_mate_label_placement_payload() -> JsonObject:
    return {
        "side": "board_right",
        "offset_mils": [250, 250],
        "box_size_mils": [450, 70],
        "row_spacing_mils": 90,
        "column_spacing_mils": 80,
        "auto_width_padding_mils": 80,
    }


def default_mate_designators_payload() -> JsonObject:
    return {
        "enabled": True,
        "placement": "above_component",
        "offset_mils": [0, 10],
        "width_factor": 0.6,
        "style": {
            "height_mils": 40,
            "layer": "TOP_OVERLAY",
            "font_kind": "truetype",
            "font_name": "Arial",
            "bold": True,
            "stroke_width_mils": 8,
        },
    }


def default_mate_board_projection_payload() -> JsonObject:
    return {
        "outline": {
            "graphics": {
                "enabled": True,
                "layer": "TOP_OVERLAY",
                "stroke_width_mils": 8,
            }
        },
        "cutouts": {
            "graphics": {
                "enabled": True,
                "layer": "MECHANICAL_1",
                "stroke_width_mils": 8,
            },
            "scope": "all",
            "actual_cutouts": False,
        },
    }


def default_mate_artifacts_payload() -> JsonObject:
    return {"pcb_layer_step": default_pcb_layer_step_mate_artifact_payload()}


def default_output_config_payload() -> JsonObject:
    return {
        "output_dir": "output/mate",
        "project_name": "mate",
        "schematic_sheet_style": "D",
        "overwrite": False,
        "layer_stack_template": "2-layer",
        "board_outline_mils": {
            "left": 0,
            "bottom": 0,
            "right": 3000,
            "top": 2000,
        },
    }


def default_known_parts_payload() -> JsonObject:
    return {
        "manifest": "",
    }


def default_placement_payload() -> JsonObject:
    return {
        "source_mount_side": "bottom",
        "offset_mils": [0, 0],
        "mirror_x": False,
        "mirror_y": False,
        "mirror_origin_mils": [0, 0],
    }


def default_pcb_labels_payload() -> JsonObject:
    return {
        "enabled": False,
        "side": "right",
        "offset_mils": [120, 0],
        "box_size_mils": [450, 70],
        "center_box_on_target": True,
        "row_spacing_mils": 90,
        "column_spacing_mils": 80,
        "auto_width_padding_mils": 80,
        "style": {
            "height_mils": 65,
            "layer": "TOP_OVERLAY",
            "font_kind": "truetype",
            "font_name": "Arial",
            "bold": True,
            "stroke_width_mils": 10,
            "is_inverted": True,
            "inverted_margin_mils": 10,
            "use_inverted_rectangle": True,
            "is_frame": True,
            "text_justification": "RIGHT_TOP",
        },
    }


def default_pcb_designators_payload() -> JsonObject:
    payload = default_mate_designators_payload()
    payload["enabled"] = False
    return payload


def default_marker_payload() -> JsonObject:
    return {
        "enabled": True,
        "text": "MATE",
        "position_mils": [200, 200],
        "height_mils": 60,
        "layer": "TOP_OVERLAY",
    }
