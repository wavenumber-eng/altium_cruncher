"""Project/PCB creation config compilation into ordered MCO operations."""

from __future__ import annotations

from copy import deepcopy
import logging
import os
from pathlib import Path
from typing import cast

from altium_cruncher.altium_cruncher_mco import (
    MCO_SCHEMA,
    JsonObject,
    McoExecutionContext,
    McoExecutionResult,
    execute_mco,
    mco_operation,
)
from altium_cruncher.altium_cruncher_document_configs import (
    default_pcbdoc_child_config,
    default_schdoc_child_config,
    project_config_header_lines,
)
from altium_cruncher.altium_cruncher_project_profiles import (
    mechanical_profile_args,
)
from altium_cruncher.config_json import load_json_config, render_commented_jsonc

from altium_cruncher.contracts.creation import (
    creation_comments,
    creation_key_comments,
    creation_default,
    creation_integer,
    creation_schema,
    decode_project_skeleton_config,
)

PROJECT_CONFIG_SCHEMA = creation_schema("project_skeleton_config")
PROJECT_CONFIG_SUFFIX = ".project.jsonc"
PROJECT_AUTO_CONFIG_NAME = "prjpcb_init.jsonc"

log = logging.getLogger(__name__)


def default_project_config(
    *,
    project_name: str = "generated_project",
    layer_count: int = 2,
) -> JsonObject:
    """Return the editable default project skeleton config."""
    return {
        "schema": PROJECT_CONFIG_SCHEMA,
        "project": {
            "file": f"{project_name}.PrjPcb",
            "name": project_name,
            "parameters": {
                "ProjectName": project_name,
            },
        },
        "schematics": [default_schdoc_child_config(document_name=project_name)],
        "pcb": default_pcbdoc_child_config(
            document_name=project_name,
            layer_count=layer_count,
        ),
    }


def render_project_config(config: JsonObject) -> str:
    """Render a project skeleton config as commented JSONC."""
    return render_commented_jsonc(
        config,
        comments_by_path=creation_comments("project_skeleton_config"),
        comments_by_key=creation_key_comments(),
        header_lines=project_config_header_lines(
            title="altium-cruncher project skeleton config."
        ),
    )


def write_project_config(
    path: Path | str,
    config: JsonObject,
    *,
    overwrite: bool = False,
) -> Path:
    """Write a project skeleton config file."""
    output_path = Path(path)
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"Config already exists: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_project_config(config), encoding="utf-8")
    return output_path.resolve()


def load_project_config(path: Path | str) -> JsonObject:
    """Load and validate a project skeleton config file."""
    payload = load_json_config(Path(path))
    if not isinstance(payload, dict):
        raise ValueError("Project config root must be an object")
    config = dict(payload)
    schema = config.get("schema")
    if schema != PROJECT_CONFIG_SCHEMA:
        raise ValueError(f"Unsupported project config schema: {schema!r}")
    return cast(JsonObject, decode_project_skeleton_config(config))


def build_project_create_mco(
    config: JsonObject, *, overwrite: bool = False
) -> JsonObject:
    """Compile a project skeleton config to MCO operations."""
    project = _object(config.get("project"), "project")
    project_file = _string(project.get("file"), "project.file")
    document_files, document_operations = _document_create_operations(config, overwrite)
    operations = [
        _project_create_operation(project, project_file, overwrite),
        *_project_parameter_operations(project, project_file),
        *document_operations,
        *_project_document_operations(project_file, document_files),
    ]
    return {"schema": MCO_SCHEMA, "operations": operations}


def _project_create_operation(
    project: JsonObject,
    project_file: str,
    overwrite: bool,
) -> JsonObject:
    return mco_operation(
        "project.create",
        "create_project",
        "Create project",
        {
            "file": project_file,
            "name": str(project.get("name") or Path(project_file).stem),
            "overwrite": overwrite,
        },
    )


def _project_parameter_operations(
    project: JsonObject,
    project_file: str,
) -> list[JsonObject]:
    return [
        mco_operation(
            "project.add_parameter",
            f"set_project_parameter_{index}",
            f"Set project parameter {name}",
            {"file": project_file, "name": name, "value": value},
        )
        for index, (name, value) in enumerate(_parameters(project).items(), start=1)
    ]


def _document_create_operations(
    config: JsonObject,
    overwrite: bool,
) -> tuple[list[str], list[JsonObject]]:
    document_files: list[str] = []
    operations: list[JsonObject] = []
    for index, sheet in enumerate(_object_list(config.get("schematics"), "schematics")):
        sheet_file, operation = _schematic_create_operation(index, sheet, overwrite)
        document_files.append(sheet_file)
        operations.append(operation)

    pcb_file, pcb_operation = _pcb_create_operation(config.get("pcb"), overwrite)
    if pcb_file is not None and pcb_operation is not None:
        document_files.append(pcb_file)
        operations.append(pcb_operation)
    return document_files, operations


def _schematic_create_operation(
    index: int,
    sheet: JsonObject,
    overwrite: bool,
) -> tuple[str, JsonObject]:
    sheet_file = _string(sheet.get("file"), "schematics[].file")
    return sheet_file, mco_operation(
        "schdoc.create",
        f"create_schematic_{index + 1}",
        f"Create schematic {Path(sheet_file).name}",
        _schematic_create_args(sheet, sheet_file, overwrite),
    )


def _schematic_create_args(
    sheet: JsonObject,
    sheet_file: str,
    overwrite: bool,
) -> JsonObject:
    args: JsonObject = {
        "file": sheet_file,
        "sheet_style": str(
            creation_integer(sheet.get("sheet_style"))
            or creation_default("sheet_style")
        ),
        "overwrite": overwrite,
    }
    if sheet.get("template") is not None:
        args["template"] = _string(sheet.get("template"), "schematics[].template")
        args["apply_template_visual_sheet_settings"] = bool(
            sheet.get(
                "apply_template_visual_sheet_settings",
                creation_default("apply_template_visual_sheet_settings"),
            )
        )
    if sheet.get("custom_sheet_mils") is not None:
        args["custom_sheet_mils"] = _object(
            sheet.get("custom_sheet_mils"),
            "schematics[].custom_sheet_mils",
        )
    return args


def _pcb_create_operation(
    raw_pcb: object,
    overwrite: bool,
) -> tuple[str | None, JsonObject | None]:
    if raw_pcb is None:
        return None, None
    pcb_obj = _object(raw_pcb, "pcb")
    pcb_file = _string(pcb_obj.get("file"), "pcb.file")
    return pcb_file, mco_operation(
        "pcbdoc.create",
        "create_board",
        f"Create board {Path(pcb_file).name}",
        _pcb_create_args(pcb_obj, pcb_file, overwrite),
    )


def _pcb_create_args(
    pcb_obj: JsonObject,
    pcb_file: str,
    overwrite: bool,
) -> JsonObject:
    pcb_args: JsonObject = {
        "file": pcb_file,
        "overwrite": overwrite,
    }
    if pcb_obj.get("board_outline_mils") is not None:
        pcb_args["board_outline_mils"] = _object(
            pcb_obj.get("board_outline_mils"),
            "pcb.board_outline_mils",
        )
    _apply_pcb_layer_stack_args(pcb_args, pcb_obj)
    _apply_pcb_mechanical_args(pcb_args, pcb_obj)
    return pcb_args


def _apply_pcb_layer_stack_args(pcb_args: JsonObject, pcb_obj: JsonObject) -> None:
    layer_stack = pcb_obj.get("layer_stack")
    layer_stack_template = pcb_obj.get("layer_stack_template")
    stackupx_file = pcb_obj.get("stackupx_file")
    configured = [
        name
        for name, value in (
            ("layer_stack", layer_stack),
            ("layer_stack_template", layer_stack_template),
            ("stackupx_file", stackupx_file),
        )
        if value is not None
    ]
    if len(configured) > 1:
        names = ", ".join(configured)
        raise ValueError(f"Use only one pcb layer-stack input, got: {names}")
    if stackupx_file is not None:
        pcb_args["stackupx_file"] = _string(stackupx_file, "pcb.stackupx_file")
        return
    if layer_stack is None:
        pcb_args["layer_stack_template"] = str(
            layer_stack_template or creation_default("layer_stack_template")
        )
        return
    layer_stack_obj = _object(layer_stack, "pcb.layer_stack")
    mode = str(layer_stack_obj.get("mode") or creation_default("mode"))
    if mode != "generated_rigid":
        raise ValueError(
            "Only pcb.layer_stack.mode='generated_rigid' is supported in this release"
        )
    pcb_args["rigid_stack"] = _native_layer_stack_integers(layer_stack_obj)


def _native_layer_stack_integers(layer_stack_obj: JsonObject) -> JsonObject:
    # JSON has one number type; native MCO enum/id fields require Python ints.
    layer_stack_obj = deepcopy(layer_stack_obj)
    for section, keys in (
        ("copper_layers", ("component_placement", "copper_orientation")),
        ("dielectrics_between", ("dielectric_type",)),
    ):
        rows = layer_stack_obj.get(section)
        if isinstance(rows, list):
            for row in rows:
                if isinstance(row, dict):
                    for key in keys:
                        if key in row:
                            row[key] = creation_integer(row[key])
    return layer_stack_obj


def _apply_pcb_mechanical_args(
    pcb_args: JsonObject,
    pcb_obj: JsonObject,
) -> None:
    profile = str(
        pcb_obj.get("mechanical_layer_profile")
        or creation_default("mechanical_layer_profile")
    )
    normalized = profile.strip().lower().replace("-", "_")
    if normalized not in {"", "none"}:
        pcb_args.update(mechanical_profile_args(profile))
    _apply_explicit_project_mechanical_rows(pcb_args, pcb_obj)


def _apply_explicit_project_mechanical_rows(
    pcb_args: JsonObject,
    pcb_obj: JsonObject,
) -> None:
    mechanical_layers: list[JsonObject] = []
    mechanical_layer_pairs: list[JsonObject] = []
    mechanical_layer_kinds: list[JsonObject] = []

    _append_project_mechanical_layers(
        pcb_obj, mechanical_layers, mechanical_layer_kinds
    )
    _append_project_mechanical_pairs(
        pcb_obj,
        mechanical_layers,
        mechanical_layer_pairs,
        mechanical_layer_kinds,
    )

    if pcb_obj.get("mechanical_layer_kinds") is not None:
        for raw in _object_list(
            pcb_obj.get("mechanical_layer_kinds"), "pcb.mechanical_layer_kinds"
        ):
            row = dict(raw)
            if "kind" in row:
                row["kind"] = creation_integer(row["kind"])
            mechanical_layer_kinds.append(row)

    if mechanical_layers:
        pcb_args["mechanical_layers"] = mechanical_layers
    if mechanical_layer_pairs:
        pcb_args["mechanical_layer_pairs"] = mechanical_layer_pairs
    if mechanical_layer_kinds:
        pcb_args["mechanical_layer_kinds"] = mechanical_layer_kinds


def _append_project_mechanical_layers(
    pcb_obj: JsonObject,
    mechanical_layers: list[JsonObject],
    mechanical_layer_kinds: list[JsonObject],
) -> None:
    rows = pcb_obj.get("mechanical_layers")
    if rows is None:
        return
    for row in _object_list(rows, "pcb.mechanical_layers"):
        layer_row = _mechanical_layer_row(row, "pcb.mechanical_layers[]")
        mechanical_layers.append(layer_row)
        if row.get("kind") is not None:
            mechanical_layer_kinds.append(
                {
                    "layer": layer_row["layer"],
                    "kind": _string(row.get("kind"), "pcb.mechanical_layers[].kind"),
                }
            )


def _append_project_mechanical_pairs(
    pcb_obj: JsonObject,
    mechanical_layers: list[JsonObject],
    mechanical_layer_pairs: list[JsonObject],
    mechanical_layer_kinds: list[JsonObject],
) -> None:
    rows = pcb_obj.get("mechanical_layer_pairs")
    if rows is None:
        return
    for row in _object_list(rows, "pcb.mechanical_layer_pairs"):
        _append_project_mechanical_pair(
            row,
            mechanical_layers,
            mechanical_layer_pairs,
            mechanical_layer_kinds,
        )


def _append_project_mechanical_pair(
    row: JsonObject,
    mechanical_layers: list[JsonObject],
    mechanical_layer_pairs: list[JsonObject],
    mechanical_layer_kinds: list[JsonObject],
) -> None:
    if "top" not in row and "bottom" not in row:
        row = dict(row)
        if "pair_index" in row:
            row["pair_index"] = creation_integer(row["pair_index"])
        mechanical_layer_pairs.append(row)
        return

    top = _mechanical_pair_side(row.get("top"), "pcb.mechanical_layer_pairs[].top")
    bottom = _mechanical_pair_side(
        row.get("bottom"), "pcb.mechanical_layer_pairs[].bottom"
    )
    mechanical_layers.extend(
        [
            _mechanical_layer_row(top, "pcb.mechanical_layer_pairs[].top"),
            _mechanical_layer_row(bottom, "pcb.mechanical_layer_pairs[].bottom"),
        ]
    )
    mechanical_layer_pairs.append({"layer_1": top["layer"], "layer_2": bottom["layer"]})
    mechanical_layer_kinds.extend(
        [
            {"layer": top["layer"], "kind": top["kind"]},
            {"layer": bottom["layer"], "kind": bottom["kind"]},
        ]
    )


def _mechanical_pair_side(value: object, label: str) -> JsonObject:
    row = _object(value, label)
    _string(row.get("layer"), f"{label}.layer")
    _string(row.get("kind"), f"{label}.kind")
    return row


def _mechanical_layer_row(row: JsonObject, label: str) -> JsonObject:
    layer_row: JsonObject = {
        "layer": _string(row.get("layer"), f"{label}.layer"),
    }
    if row.get("name") is not None:
        layer_row["name"] = _string(row.get("name"), f"{label}.name")
    if row.get("enabled") is not None:
        layer_row["enabled"] = bool(row.get("enabled"))
    return layer_row


def _project_document_operations(
    project_file: str,
    document_files: list[str],
) -> list[JsonObject]:
    return [
        mco_operation(
            "project.add_document",
            f"add_document_{index}",
            f"Add {Path(document_file).name} to project",
            {
                "file": project_file,
                "document": _project_relative_document(project_file, document_file),
            },
        )
        for index, document_file in enumerate(document_files, start=1)
    ]


def execute_project_create_mco(
    config: JsonObject,
    *,
    config_dir: Path,
    overwrite: bool = False,
    dry_run: bool = False,
) -> McoExecutionResult:
    """Execute a project skeleton config through generated MCO operations."""
    return execute_mco(
        build_project_create_mco(config, overwrite=overwrite),
        McoExecutionContext(work_dir=config_dir, dry_run=dry_run),
    )


def _project_relative_document(project_file: str, document_file: str) -> str:
    project_path = Path(project_file)
    document_path = Path(document_file)
    if project_path.is_absolute() and document_path.is_absolute():
        return os.path.relpath(document_path, project_path.parent)
    if project_path.parent != Path(".") and document_path.parent != Path("."):
        return os.path.relpath(document_path, project_path.parent)
    return str(document_path)


def _parameters(project: JsonObject) -> dict[str, str]:
    raw = project.get("parameters", {})
    if not isinstance(raw, dict):
        raise ValueError("project.parameters must be an object")
    return {str(name): str(value) for name, value in raw.items()}


def _object(value: object, label: str) -> JsonObject:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return dict(value)


def _object_list(value: object, label: str) -> list[JsonObject]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a list")
    return [_object(item, label) for item in value]


def _string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a non-empty string")
    return value
