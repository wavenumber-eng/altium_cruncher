"""Config helpers for PCB layer STEP fixture-alignment output."""

from __future__ import annotations

import json
from .contracts.workflows import workflow_comments, workflow_metadata

from copy import deepcopy
import re

from altium_monkey.altium_record_types import PcbLayer

from altium_cruncher.altium_cruncher_mco import JsonObject, loads_jsonc
from altium_cruncher.altium_cruncher_pcb_layer_resolve import (
    resolve_pcb_layer_ref_or_none,
)
from altium_cruncher.config_json import enum_help, render_commented_jsonc

PCB_LAYER_STEP_DEFAULT_CONFIG_TEXT = json.dumps(workflow_metadata("pcb_layer_step_config", "resolved-defaults"), indent=2)


_PCB_LAYER_STEP_HEADER_LINES = workflow_metadata("pcb_layer_step_config", "header-lines")

_PCB_LAYER_STEP_COMMENTS = workflow_comments("pcb_layer_step_config")

_PCB_LAYER_STEP_KEY_COMMENTS = workflow_metadata("pcb_layer_step_config", "jsonc-key-comments")


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
        return _layer_from_v7_selector(selector)
    return layer


def _layer_from_v7_selector(selector: str | int) -> PcbLayer:
    """Resolve V7 layer tokens; layer-step operations require a legacy layer.

    Layer-step internals index dense legacy-layer arrays (``layer.value - 1``),
    so V7-only layers (Mechanical17+, Mid31+) cannot be supported here.
    """
    ref = resolve_pcb_layer_ref_or_none(selector)
    if ref is None:
        raise ValueError(f"Unknown PCB layer selector: {selector!r}")
    if ref.legacy_layer is None:
        raise ValueError(
            f"V7-only layer {ref.token!r} is not supported for layer-step "
            "operations; choose a layer with a legacy id (Top/Bottom, "
            "Mid1-30, Mechanical1-16)."
        )
    return ref.legacy_layer


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
