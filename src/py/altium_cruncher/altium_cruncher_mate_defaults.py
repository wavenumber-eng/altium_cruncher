"""Default mate config payload helpers."""

from __future__ import annotations

from .contracts.workflows import workflow_metadata

from pathlib import Path

from altium_cruncher.altium_cruncher_mco import JsonObject
from altium_cruncher.altium_cruncher_pcb_layer_step_config import (
    default_pcb_layer_step_mate_artifact_payload,
)

DEFAULT_MATE_BOARD_OUTLINE_MARGIN_MILS = 250.0


def default_mate_output_payload() -> JsonObject:
    return workflow_metadata("mate_config", "domain-defaults")["default_mate_output_payload"]


def mate_known_parts_payload(
    known_parts_manifest: Path | str | None,
) -> JsonObject:
    if known_parts_manifest is None:
        return default_known_parts_payload()
    return {"manifest": str(known_parts_manifest)}


def default_mate_label_style_payload() -> JsonObject:
    return workflow_metadata("mate_config", "domain-defaults")["default_mate_label_style_payload"]


def default_mate_label_placement_payload() -> JsonObject:
    return workflow_metadata("mate_config", "domain-defaults")["default_mate_label_placement_payload"]


def default_mate_designators_payload() -> JsonObject:
    return workflow_metadata("mate_config", "domain-defaults")["default_mate_designators_payload"]


def default_mate_board_projection_payload() -> JsonObject:
    return workflow_metadata("mate_config", "domain-defaults")["default_mate_board_projection_payload"]


def default_mate_artifacts_payload() -> JsonObject:
    return workflow_metadata("mate_config", "domain-defaults")["default_mate_artifacts_payload"]


def default_output_config_payload() -> JsonObject:
    return workflow_metadata("mate_config", "domain-defaults")["default_output_config_payload"]


def default_known_parts_payload() -> JsonObject:
    return workflow_metadata("mate_config", "domain-defaults")["default_known_parts_payload"]


def default_placement_payload() -> JsonObject:
    return workflow_metadata("mate_config", "domain-defaults")["default_placement_payload"]


def default_pcb_labels_payload() -> JsonObject:
    return workflow_metadata("mate_config", "domain-defaults")["default_pcb_labels_payload"]


def default_pcb_designators_payload() -> JsonObject:
    return workflow_metadata("mate_config", "domain-defaults")["default_pcb_designators_payload"]


def default_marker_payload() -> JsonObject:
    return workflow_metadata("mate_config", "domain-defaults")["default_marker_payload"]
