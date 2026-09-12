"""Reusable config defaults for document creation commands."""

from __future__ import annotations

from pathlib import Path
from typing import cast

from altium_cruncher.altium_cruncher_project_profiles import (
    V7_MECHANICAL_53_LAYERS,
    generated_rigid_stack_config,
    standard_mechanical_project_config,
)
from altium_cruncher.config_json import load_json_config, render_commented_jsonc

from altium_cruncher.contracts.creation import (
    creation_comments,
    creation_key_comments,
    creation_default,
    creation_schema,
    decode_schdoc_create_config,
    decode_pcbdoc_create_config,
)

JsonObject = dict[str, object]

SCHDOC_CREATE_CONFIG_SCHEMA = creation_schema("schdoc_create_config")
PCBDOC_CREATE_CONFIG_SCHEMA = creation_schema("pcbdoc_create_config")

SCHDOC_AUTO_CONFIG_NAME = "schdoc_create.jsonc"
PCBDOC_AUTO_CONFIG_NAME = "pcbdoc_create.jsonc"


def default_schdoc_child_config(*, document_name: str) -> JsonObject:
    """Return the PrjPcb-compatible SchDoc child config shape."""
    return {
        "file": f"{document_name}.SchDoc",
        "sheet_style": creation_default("sheet_style"),
    }


def default_schdoc_create_config(*, document_name: str) -> JsonObject:
    """Return the standalone SchDoc create config shape."""
    return {
        "schema": SCHDOC_CREATE_CONFIG_SCHEMA,
        **default_schdoc_child_config(document_name=document_name),
    }


def default_pcbdoc_child_config(
    *,
    document_name: str,
    layer_count: int = 2,
) -> JsonObject:
    """Return the PrjPcb-compatible PcbDoc child config shape."""
    pcb_config: JsonObject = {
        "file": f"{document_name}.PcbDoc",
        "board_outline_mils": creation_default("board_outline_mils"),
        "layer_stack": generated_rigid_stack_config(layer_count),
    }
    pcb_config.update(standard_mechanical_project_config())
    return pcb_config


def default_pcbdoc_create_config(
    *,
    document_name: str,
    layer_count: int = 2,
) -> JsonObject:
    """Return the standalone PcbDoc create config shape."""
    return {
        "schema": PCBDOC_CREATE_CONFIG_SCHEMA,
        **default_pcbdoc_child_config(
            document_name=document_name,
            layer_count=layer_count,
        ),
    }


def render_schdoc_create_config(config: JsonObject) -> str:
    """Render a SchDoc create config as commented JSONC."""
    return render_commented_jsonc(
        config,
        comments_by_path=creation_comments("schdoc_create_config"),
        header_lines=(
            "altium-cruncher SchDoc create config.",
            "This file is JSONC: comments and trailing commas are accepted.",
        ),
    )


def render_pcbdoc_create_config(config: JsonObject) -> str:
    """Render a PcbDoc create config as commented JSONC."""
    return render_commented_jsonc(
        config,
        comments_by_path=_pcbdoc_comment_paths(prefix=()),
        comments_by_key=creation_key_comments(),
        header_lines=project_config_header_lines(
            title="altium-cruncher PcbDoc create config."
        ),
    )


def project_config_header_lines(*, title: str) -> tuple[str, ...]:
    """Return the shared document-create JSONC header."""
    return (
        title,
        "This file is JSONC: comments and trailing commas are accepted.",
        "",
        "Valid mechanical layer ids/indexes/default names:",
        *_mechanical_layer_reference_lines(),
        "",
        "Valid mechanical layer kind enum names:",
        *_mechanical_kind_reference_lines(),
    )


def _mechanical_layer_reference_lines() -> tuple[str, ...]:
    return tuple(
        f"  {layer}=index {index}: {name}"
        for index, (layer, name, _enabled) in enumerate(
            V7_MECHANICAL_53_LAYERS,
            start=1,
        )
    )


def _mechanical_kind_reference_lines() -> tuple[str, ...]:
    from altium_monkey import MechanicalLayerKind

    return tuple(f"  {kind.name}" for kind in MechanicalLayerKind)


def _pcbdoc_comment_paths(
    *,
    prefix: tuple[str, ...],
) -> dict[tuple[str, ...] | str, str]:
    return creation_comments("pcbdoc_create_config", prefix=prefix)


def project_pcbdoc_comment_paths(
    *, prefix: tuple[str, ...]
) -> dict[tuple[str, ...] | str, str]:
    """Return shared PcbDoc child comments for project configs."""
    comments = _pcbdoc_comment_paths(prefix=prefix)
    comments.pop((*prefix, "schema"), None)
    return comments


def load_object_config(path: Path | str, *, schema: str, label: str) -> JsonObject:
    """Load a JSONC object config and verify its schema field."""
    payload = load_json_config(Path(path))
    if not isinstance(payload, dict):
        raise ValueError(f"{label} config root must be an object")
    config = dict(payload)
    if config.get("schema") != schema:
        raise ValueError(f"Unsupported {label} config schema: {config.get('schema')!r}")
    if schema == SCHDOC_CREATE_CONFIG_SCHEMA:
        return cast(JsonObject, decode_schdoc_create_config(config))
    if schema == PCBDOC_CREATE_CONFIG_SCHEMA:
        return cast(JsonObject, decode_pcbdoc_create_config(config))
    return config


__all__ = [
    "PCBDOC_AUTO_CONFIG_NAME",
    "PCBDOC_CREATE_CONFIG_SCHEMA",
    "SCHDOC_AUTO_CONFIG_NAME",
    "SCHDOC_CREATE_CONFIG_SCHEMA",
    "default_pcbdoc_child_config",
    "default_pcbdoc_create_config",
    "default_schdoc_child_config",
    "default_schdoc_create_config",
    "load_object_config",
    "project_config_header_lines",
    "project_pcbdoc_comment_paths",
    "render_pcbdoc_create_config",
    "render_schdoc_create_config",
]
