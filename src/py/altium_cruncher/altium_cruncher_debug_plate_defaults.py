"""Default debug-plate config payload helpers."""

from __future__ import annotations

from pathlib import Path

from altium_cruncher.altium_cruncher_mco import JsonObject


def default_mate_output_payload() -> JsonObject:
    return {
        "backend": "altium",
        "output_dir": "output/debug-plate",
        "project_name": "debug_plate",
        "origin": "preserve_source",
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
            "graphics": {"enabled": True, "layer": "MECHANICAL_1"},
            "actual_cutouts": False,
        },
    }


def default_mate_artifacts_payload() -> JsonObject:
    return {
        "pcb_layer_step": {
            "enabled": True,
            "source_layer": "bottom",
            "insert_in_output": {
                "enabled": True,
                "z_mm": 1.6,
                "layer": "MECHANICAL_13",
                "side": "TOP",
            },
            "highlights": [
                {
                    "projection": "test_points",
                    "color": "#ffcc00",
                }
            ],
        }
    }


def default_output_config_payload() -> JsonObject:
    return {
        "output_dir": "output/debug-plate",
        "project_name": "debug_plate",
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


def default_marker_payload() -> JsonObject:
    return {
        "enabled": True,
        "text": "DEBUG PLATE",
        "position_mils": [200, 200],
        "height_mils": 60,
        "layer": "TOP_OVERLAY",
    }
