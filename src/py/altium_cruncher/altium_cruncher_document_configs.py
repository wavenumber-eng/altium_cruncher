"""Reusable config defaults for document creation commands."""

from __future__ import annotations

from pathlib import Path

from altium_cruncher.altium_cruncher_project_profiles import (
    MECHANICAL_LAYER_PROFILE_CHOICES,
    V7_MECHANICAL_53_LAYERS,
    generated_rigid_stack_config,
    standard_mechanical_project_config,
)
from altium_cruncher.config_json import load_json_config, render_commented_jsonc

JsonObject = dict[str, object]

SCHDOC_CREATE_CONFIG_SCHEMA = "altium_cruncher.schdoc.create.config.a0"
PCBDOC_CREATE_CONFIG_SCHEMA = "altium_cruncher.pcbdoc.create.config.a0"

SCHDOC_AUTO_CONFIG_NAME = "schdoc_create.jsonc"
PCBDOC_AUTO_CONFIG_NAME = "pcbdoc_create.jsonc"


def default_schdoc_child_config(*, document_name: str) -> JsonObject:
    """Return the PrjPcb-compatible SchDoc child config shape."""
    return {
        "file": f"{document_name}.SchDoc",
        "sheet_style": "D",
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
        "board_outline_mils": {
            "left": 0,
            "bottom": 0,
            "right": 3000,
            "top": 2000,
        },
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
        comments_by_path={
            ("schema",): "SchDoc create config contract id.",
            (
                "file",
            ): "SchDoc file to create, relative to this config file unless absolute.",
            ("sheet_style",): (
                "Schematic sheet style. Options: Altium SheetStyle enum name or native enum id."
            ),
            ("template",): "Optional SchDot template file to copy settings from.",
            ("apply_template_visual_sheet_settings",): (
                "Whether to copy visual sheet settings from the template."
            ),
            ("custom_sheet_mils",): "Optional explicit sheet size in mils.",
            ("custom_sheet_mils", "width"): "Custom sheet width in mils.",
            ("custom_sheet_mils", "height"): "Custom sheet height in mils.",
        },
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
        comments_by_key={
            "file": "Path relative to this config file unless absolute.",
            "layer": "Mechanical layer id; see valid ids in the header.",
            "kind": "Mechanical layer kind enum name; see valid kind names in the header.",
            "enabled": "Whether this row is enabled.",
        },
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
) -> dict[tuple[str, ...], str]:
    return {
        (*prefix, "schema"): "PcbDoc create config contract id.",
        (
            *prefix,
            "file",
        ): "PcbDoc file to create, relative to this config file unless absolute.",
        (*prefix, "board_outline_mils"): "Rectangular board outline in mils.",
        (
            *prefix,
            "board_outline_mils",
            "left",
        ): "Left board outline coordinate in mils.",
        (
            *prefix,
            "board_outline_mils",
            "bottom",
        ): "Bottom board outline coordinate in mils.",
        (
            *prefix,
            "board_outline_mils",
            "right",
        ): "Right board outline coordinate in mils.",
        (*prefix, "board_outline_mils", "top"): "Top board outline coordinate in mils.",
        (*prefix, "layer_stack"): (
            "Generated rigid stack. Use stackupx_file instead for imported "
            ".stackupx layer-stack documents."
        ),
        (*prefix, "stackupx_file"): (
            "Optional .stackupx path to import as the PcbDoc layer-stack document."
        ),
        (
            *prefix,
            "layer_stack",
            "mode",
        ): "Layer-stack generation mode. Options: generated_rigid.",
        (*prefix, "layer_stack", "name"): "Layer-stack display name.",
        (
            *prefix,
            "layer_stack",
            "copper_layers",
        ): "Copper layers in top-to-bottom order.",
        (*prefix, "layer_stack", "copper_layers", "name"): "Copper layer display name.",
        (*prefix, "layer_stack", "copper_layers", "copper_thickness_mils"): (
            "Copper thickness in mils."
        ),
        (*prefix, "layer_stack", "dielectrics_between"): (
            "Dielectric layers between adjacent copper layers."
        ),
        (*prefix, "layer_stack", "dielectrics_between", "name"): (
            "Dielectric layer display name."
        ),
        (*prefix, "layer_stack", "dielectrics_between", "thickness_mils"): (
            "Dielectric thickness in mils."
        ),
        (*prefix, "layer_stack", "dielectrics_between", "dielectric_constant"): (
            "Dielectric constant."
        ),
        (*prefix, "layer_stack", "dielectrics_between", "material"): (
            "Dielectric material name."
        ),
        (*prefix, "layer_stack", "dielectrics_between", "dielectric_type"): (
            "Altium dielectric type code."
        ),
        (*prefix, "mechanical_layer_profile"): (
            "Optional shorthand. Options: "
            f"{', '.join(MECHANICAL_LAYER_PROFILE_CHOICES)}. "
            "Explicit mechanical rows override this profile."
        ),
        (
            *prefix,
            "mechanical_layers",
        ): "Editable single or unpaired mechanical layer rows.",
        (
            *prefix,
            "mechanical_layers",
            "layer",
        ): "Mechanical layer id; see valid ids in the header.",
        (*prefix, "mechanical_layers", "name"): "Mechanical layer display name.",
        (
            *prefix,
            "mechanical_layers",
            "enabled",
        ): "Whether the mechanical layer is enabled.",
        (*prefix, "mechanical_layers", "kind"): (
            "Optional mechanical layer kind enum name; see valid kind names in the header."
        ),
        (*prefix, "mechanical_layer_pairs"): (
            "Editable grouped top/bottom mechanical layer pair rows."
        ),
        (*prefix, "mechanical_layer_pairs", "top"): "Top-side mechanical layer row.",
        (*prefix, "mechanical_layer_pairs", "top", "layer"): (
            "Top-side mechanical layer id; see valid ids in the header."
        ),
        (*prefix, "mechanical_layer_pairs", "top", "name"): (
            "Top-side mechanical layer display name."
        ),
        (*prefix, "mechanical_layer_pairs", "top", "enabled"): (
            "Whether the top-side layer is enabled."
        ),
        (*prefix, "mechanical_layer_pairs", "top", "kind"): (
            "Top-side mechanical layer kind enum name; see valid kind names in the header."
        ),
        (
            *prefix,
            "mechanical_layer_pairs",
            "bottom",
        ): "Bottom-side mechanical layer row.",
        (*prefix, "mechanical_layer_pairs", "bottom", "layer"): (
            "Bottom-side mechanical layer id; see valid ids in the header."
        ),
        (*prefix, "mechanical_layer_pairs", "bottom", "name"): (
            "Bottom-side mechanical layer display name."
        ),
        (*prefix, "mechanical_layer_pairs", "bottom", "enabled"): (
            "Whether the bottom-side layer is enabled."
        ),
        (*prefix, "mechanical_layer_pairs", "bottom", "kind"): (
            "Bottom-side mechanical layer kind enum name; see valid kind names in the header."
        ),
        (*prefix, "mechanical_layer_pairs", "layer_1"): (
            "Legacy flat pair form: first mechanical layer in the pair."
        ),
        (*prefix, "mechanical_layer_pairs", "layer_2"): (
            "Legacy flat pair form: second mechanical layer in the pair."
        ),
        (*prefix, "mechanical_layer_pairs", "pair_index"): (
            "Legacy flat pair form: optional pair ordering override."
        ),
        (
            *prefix,
            "mechanical_layer_kinds",
        ): "Editable mechanical layer kind assignment rows.",
        (*prefix, "mechanical_layer_kinds", "layer"): (
            "Mechanical layer id to assign; see valid ids in the header."
        ),
        (*prefix, "mechanical_layer_kinds", "kind"): (
            "Mechanical layer kind enum name; see valid kind names in the header."
        ),
    }


def project_pcbdoc_comment_paths(
    *, prefix: tuple[str, ...]
) -> dict[tuple[str, ...], str]:
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
