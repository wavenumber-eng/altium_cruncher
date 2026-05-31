"""Debug-plate workflow configuration and MCO generation."""

from __future__ import annotations

import fnmatch
import json
from collections.abc import Mapping
from dataclasses import dataclass, replace
from pathlib import Path

from altium_cruncher.altium_cruncher_mco import (
    MCO_SCHEMA,
    JsonObject,
    McoExecutionContext,
    McoExecutionResult,
    execute_mco,
    load_jsonc_file,
)
from altium_cruncher.altium_cruncher_debug_plate_parts import (
    load_debug_plate_known_parts_manifest,
    manifest_path_for_cache_dir,
    resolve_known_part,
)
from altium_cruncher.altium_cruncher_debug_plate_graphics import (
    board_outline_bounds_mils,
    build_pcb_reference_graphics_operations,
    component_pad_geometries,
    pad_height_mils,
    pad_width_mils,
    parse_selection_pad_geometries,
    parse_source_pad_geometries,
    single_inspection_board_outline,
    transform_source_pad_geometries,
)
from altium_cruncher.altium_cruncher_debug_plate_artifacts import (
    build_debug_plate_artifact_operations,
)

DEBUG_PLATE_CONFIG_SCHEMA = "wn.altium_cruncher.debug_plate.v1"
MATE_CONFIG_SCHEMA = "wn.pcb_cruncher.mate_config.a0"
DEBUG_PLATE_INSPECTION_SCHEMA = "wn.altium_cruncher.debug_plate.inspect.v1"

_PCB_LABEL_STYLE_PASSTHROUGH_KEYS = (
    "rotation_degrees",
    "stroke_font_type",
    "italic",
    "is_comment",
    "is_designator",
    "is_mirrored",
    "barcode_kind",
    "barcode_render_mode",
    "barcode_full_size_mils",
    "barcode_margin_mils",
    "barcode_min_width_mils",
    "barcode_show_text",
    "barcode_inverted",
)


@dataclass(frozen=True, slots=True)
class DebugPlateOutputConfig:
    """Output project settings for a generated debug plate."""

    output_dir: str
    project_name: str
    schematic_filename: str | None
    board_filename: str | None
    project_filename: str | None
    layer_stack_template: str
    overwrite: bool
    board_outline_mils: JsonObject | None


@dataclass(frozen=True, slots=True)
class DebugPlateMarkerConfig:
    """Initial marker text used by the first debug-plate orchestration slice."""

    text: str
    position_mils: tuple[float, float]
    height_mils: float
    layer: str


@dataclass(frozen=True, slots=True)
class DebugPlateKnownPartsConfig:
    """Known fixture-part cache referenced by a debug-plate config."""

    manifest_path: Path
    cache_dir: Path


@dataclass(frozen=True, slots=True)
class DebugPlatePlacementConfig:
    """Board-side placement transform for projected DUT coordinates."""

    source_mount_side: str
    offset_mils: tuple[float, float]
    mirror_x: bool
    mirror_y: bool
    mirror_origin_mils: tuple[float, float]


@dataclass(frozen=True, slots=True)
class DebugPlatePcbLabelsConfig:
    """PCB-side net-label generation settings for projected DUT targets."""

    enabled: bool
    side: str
    offset_mils: tuple[float, float]
    box_size_mils: tuple[float, float] | None
    center_box_on_target: bool
    style: JsonObject


@dataclass(frozen=True, slots=True)
class DebugPlateSelectionComponent:
    """Selected DUT component to project into the debug plate."""

    designator: str
    kind: str
    layer: str
    footprint: str
    x_mils: float
    y_mils: float
    net_name: str | None
    mate_projection_id: str | None = None
    mate_part_role: str | None = None
    mate_pcb_label: JsonObject | None = None
    mate_reference_graphics: JsonObject | None = None
    source_pad_geometries: tuple[JsonObject, ...] = ()


@dataclass(frozen=True, slots=True)
class DebugPlateSelectionPad:
    """Selected DUT free pad/NPTH to project into the debug plate."""

    designator: str
    kind: str
    x_mils: float
    y_mils: float
    net_name: str | None
    mate_projection_id: str | None = None
    mate_part_role: str | None = None
    mate_pcb_label: JsonObject | None = None
    mate_reference_graphics: JsonObject | None = None
    source_pad_geometries: tuple[JsonObject, ...] = ()


@dataclass(frozen=True, slots=True)
class DebugPlateSelectionBoard:
    """Selected DUT board items to project into the debug plate."""

    board_key: str
    pcb_path: str
    components: tuple[DebugPlateSelectionComponent, ...]
    free_pads: tuple[DebugPlateSelectionPad, ...]


@dataclass(frozen=True, slots=True)
class DebugPlateSelectionConfig:
    """Selected DUT items to project into the debug plate."""

    boards: tuple[DebugPlateSelectionBoard, ...]


@dataclass(frozen=True, slots=True)
class DebugPlateConfig:
    """Parsed debug-plate configuration."""

    source_dut: str | None
    output: DebugPlateOutputConfig
    marker: DebugPlateMarkerConfig | None
    known_parts: DebugPlateKnownPartsConfig | None
    placement: DebugPlatePlacementConfig
    pcb_labels: DebugPlatePcbLabelsConfig
    selection: DebugPlateSelectionConfig
    artifacts: JsonObject


@dataclass(frozen=True, slots=True)
class DebugPlateComponentCandidate:
    """DUT component candidate for debug-plate projection."""

    designator: str
    kind: str
    layer: str
    footprint: str
    x_mils: float
    y_mils: float
    net_name: str | None
    pad_geometries: tuple[JsonObject, ...] = ()

    def to_dict(self) -> JsonObject:
        payload: JsonObject = {
            "designator": self.designator,
            "kind": self.kind,
            "layer": self.layer,
            "footprint": self.footprint,
            "x_mils": self.x_mils,
            "y_mils": self.y_mils,
        }
        _add_optional(payload, "net_name", self.net_name)
        if self.pad_geometries:
            payload["source_pad_geometries"] = [
                dict(geometry) for geometry in self.pad_geometries
            ]
        return payload


@dataclass(frozen=True, slots=True)
class DebugPlatePadCandidate:
    """Free pad or NPTH candidate for debug-plate projection."""

    designator: str
    kind: str
    layer: int
    x_mils: float
    y_mils: float
    width_mils: float
    height_mils: float
    hole_size_mils: float
    plated: bool
    shape: int
    net_name: str | None

    def to_dict(self) -> JsonObject:
        payload: JsonObject = {
            "designator": self.designator,
            "kind": self.kind,
            "layer": self.layer,
            "x_mils": self.x_mils,
            "y_mils": self.y_mils,
            "width_mils": self.width_mils,
            "height_mils": self.height_mils,
            "hole_size_mils": self.hole_size_mils,
            "plated": self.plated,
            "shape": self.shape,
        }
        _add_optional(payload, "net_name", self.net_name)
        return payload


@dataclass(frozen=True, slots=True)
class DebugPlateBoardInspection:
    """Debug-plate source inspection for one PCB document."""

    board_key: str
    pcb_path: str
    board_outline_mils: JsonObject | None
    components: tuple[DebugPlateComponentCandidate, ...]
    free_pads: tuple[DebugPlatePadCandidate, ...]

    def to_dict(self) -> JsonObject:
        payload: JsonObject = {
            "board_key": self.board_key,
            "pcb_path": self.pcb_path,
            "components": [candidate.to_dict() for candidate in self.components],
            "free_pads": [candidate.to_dict() for candidate in self.free_pads],
        }
        _add_optional(payload, "board_outline_mils", self.board_outline_mils)
        return payload


def load_debug_plate_config(path: Path | str) -> DebugPlateConfig:
    """Load a debug-plate JSONC config file."""
    input_path = Path(path).resolve()
    payload = load_jsonc_file(input_path)
    return parse_debug_plate_config(payload, base_dir=input_path.parent)


def parse_debug_plate_config(
    payload: object,
    *,
    base_dir: Path | str | None = None,
) -> DebugPlateConfig:
    """Parse a debug-plate config payload."""
    root = _json_object(payload, "debug-plate config root")
    schema = root.get("schema")
    if schema == MATE_CONFIG_SCHEMA:
        return _parse_mate_config(root, base_dir=base_dir)
    if schema not in {None, DEBUG_PLATE_CONFIG_SCHEMA}:
        raise ValueError(f"Unsupported debug-plate config schema: {schema!r}")
    source = _section(root, "source")
    return DebugPlateConfig(
        source_dut=_optional_string(source, "dut", None),
        output=_parse_output_config(_section(root, "output")),
        marker=_parse_marker_config(_section(root, "marker")),
        known_parts=_parse_known_parts_config(
            _optional_section(root, "known_parts"),
            base_dir=base_dir,
        ),
        placement=_parse_placement_config(_section(root, "placement")),
        pcb_labels=_parse_pcb_labels_config(_optional_section(root, "pcb_labels")),
        selection=_parse_selection_config(_section(root, "selection")),
        artifacts=_section(root, "artifacts"),
    )


def _parse_mate_config(
    root: Mapping[str, object],
    *,
    base_dir: Path | str | None,
) -> DebugPlateConfig:
    source = _section(root, "source")
    source_board = _optional_string(source, "board", None)
    inspection = _mate_source_inspection(root, base_dir=base_dir)
    return DebugPlateConfig(
        source_dut=source_board,
        output=_parse_mate_output_config(_section(root, "output"), inspection),
        marker=None,
        known_parts=_parse_known_parts_config(
            _optional_section(root, "known_parts"),
            base_dir=base_dir,
        ),
        placement=_default_mate_placement_config(),
        pcb_labels=_parse_mate_pcb_labels_config(root),
        selection=_selection_from_mate_inspection(root, inspection),
        artifacts=_section(root, "artifacts"),
    )


def build_debug_plate_mco(config: DebugPlateConfig) -> JsonObject:
    """Build the executable MCO payload for a debug-plate config."""
    operations: list[JsonObject] = [
        _project_create_operation(
            config.output,
            documents=_known_part_project_documents(config),
        )
    ]
    marker = config.marker
    if marker is not None:
        operations.append(_pcb_marker_operation(config.output, marker))
    operations.extend(_known_part_library_copy_operations(config))
    operations.extend(_known_part_placement_operations(config))
    operations.extend(build_debug_plate_artifact_operations(config))
    return {"schema": MCO_SCHEMA, "operations": operations}


def write_debug_plate_config_template(
    path: Path | str,
    *,
    overwrite: bool = False,
) -> Path:
    """Write an editable debug-plate JSONC template."""
    output_path = Path(path)
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"Debug-plate config already exists: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(_debug_plate_template_text(), encoding="utf-8")
    return output_path.resolve()


def build_debug_plate_seed_config(
    input_file: Path | str,
    *,
    pcbdoc_selector: Path | str | None = None,
    project_context: str | None = "auto",
) -> JsonObject:
    """Build an editable debug-plate config seeded from DUT inspection."""
    inspection = inspect_debug_plate_source(
        input_file,
        pcbdoc_selector=pcbdoc_selector,
        project_context=project_context,
    )
    return {
        "schema": DEBUG_PLATE_CONFIG_SCHEMA,
        "source": {"dut": str(Path(input_file).resolve())},
        "output": _default_output_config_payload(),
        "known_parts": _default_known_parts_payload(),
        "placement": _default_placement_payload(),
        "pcb_labels": _default_pcb_labels_payload(),
        "marker": _default_marker_payload(),
        "selection": _selection_from_inspection(inspection),
    }


def build_debug_plate_mate_seed_config(
    input_file: Path | str,
    *,
    known_parts_manifest: Path | str | None = None,
    pcbdoc_selector: Path | str | None = None,
    project_context: str | None = "auto",
) -> JsonObject:
    """Build a draft mate config seeded from DUT inspection."""
    inspection = inspect_debug_plate_source(
        input_file,
        pcbdoc_selector=pcbdoc_selector,
        project_context=project_context,
    )
    source: JsonObject = {"board": str(Path(input_file).resolve())}
    if pcbdoc_selector is not None:
        source["pcbdoc"] = str(pcbdoc_selector)
    if project_context is not None:
        source["project_context"] = project_context
    return {
        "schema": MATE_CONFIG_SCHEMA,
        "source": source,
        "output": _default_mate_output_payload(),
        "known_parts": _mate_known_parts_payload(known_parts_manifest),
        "validation": {
            "source_side": "infer_single_side",
            "allow_side_agnostic_through_hole": True,
            "side_agnostic_kinds": ["mount"],
        },
        "projections": _mate_seed_projections(inspection),
        "board_projection": _default_mate_board_projection_payload(),
        "artifacts": _default_mate_artifacts_payload(),
    }


def write_debug_plate_seed_config(
    input_file: Path | str,
    path: Path | str,
    *,
    overwrite: bool = False,
    pcbdoc_selector: Path | str | None = None,
    project_context: str | None = "auto",
) -> Path:
    """Write an editable debug-plate config seeded from a DUT PCB input."""
    output_path = Path(path)
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"Debug-plate config already exists: {output_path}")
    payload = build_debug_plate_seed_config(
        input_file,
        pcbdoc_selector=pcbdoc_selector,
        project_context=project_context,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output_path.resolve()


def write_debug_plate_mate_seed_config(
    input_file: Path | str,
    path: Path | str,
    *,
    overwrite: bool = False,
    known_parts_manifest: Path | str | None = None,
    pcbdoc_selector: Path | str | None = None,
    project_context: str | None = "auto",
) -> Path:
    """Write a draft mate config seeded from a DUT PCB input."""
    output_path = Path(path)
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"Debug-plate mate config already exists: {output_path}")
    payload = build_debug_plate_mate_seed_config(
        input_file,
        known_parts_manifest=known_parts_manifest,
        pcbdoc_selector=pcbdoc_selector,
        project_context=project_context,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    return output_path.resolve()


def write_debug_plate_mco(
    config: DebugPlateConfig,
    path: Path | str,
    *,
    overwrite: bool = False,
) -> Path:
    """Write the generated debug-plate MCO payload."""
    output_path = Path(path)
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"Debug-plate MCO already exists: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(build_debug_plate_mco(config), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output_path.resolve()


def execute_debug_plate_config(
    path: Path | str,
    *,
    dry_run: bool = False,
) -> McoExecutionResult:
    """Execute a debug-plate config through the MCO engine."""
    config_path = Path(path).resolve()
    config = load_debug_plate_config(config_path)
    context = McoExecutionContext(work_dir=config_path.parent, dry_run=dry_run)
    return execute_mco(build_debug_plate_mco(config), context)


def inspect_debug_plate_source(
    input_file: Path | str,
    *,
    pcbdoc_selector: Path | str | None = None,
    project_context: str | None = "auto",
) -> JsonObject:
    """Inspect a DUT PCB input and report debug-plate projection candidates."""
    from altium_cruncher.altium_cruncher_pcb_workflow import (
        iter_pcb_render_inputs,
        load_design_for_pcb_input,
    )

    input_path = Path(input_file).resolve()
    design, source_tag = load_design_for_pcb_input(
        input_path,
        project_context=project_context,
    )
    boards = [
        inspect_pcbdoc_for_debug_plate(
            render_input.board_key,
            render_input.pcbdoc,
            render_input.pcb_path,
        )
        for render_input in iter_pcb_render_inputs(
            design,
            pcbdoc_selector=pcbdoc_selector,
        )
    ]
    return {
        "schema": DEBUG_PLATE_INSPECTION_SCHEMA,
        "source": str(input_path),
        "source_tag": source_tag,
        "boards": [board.to_dict() for board in boards],
    }


def inspect_pcbdoc_for_debug_plate(
    board_key: str,
    pcbdoc: object,
    pcb_path: Path | str,
) -> DebugPlateBoardInspection:
    """Inspect one loaded PcbDoc object for likely debug-plate candidates."""
    return DebugPlateBoardInspection(
        board_key=board_key,
        pcb_path=str(Path(pcb_path)),
        board_outline_mils=board_outline_bounds_mils(pcbdoc),
        components=tuple(_component_candidates(pcbdoc)),
        free_pads=tuple(_free_pad_candidates(pcbdoc)),
    )


def _parse_output_config(raw: Mapping[str, object]) -> DebugPlateOutputConfig:
    project_name = _optional_string(raw, "project_name", "debug_plate")
    return DebugPlateOutputConfig(
        output_dir=_optional_string(raw, "output_dir", "output/debug-plate"),
        project_name=project_name,
        schematic_filename=_optional_string(raw, "schematic_filename", None),
        board_filename=_optional_string(raw, "board_filename", None),
        project_filename=_optional_string(raw, "project_filename", None),
        layer_stack_template=_optional_string(raw, "layer_stack_template", "2-layer"),
        overwrite=_optional_bool(raw, "overwrite", False),
        board_outline_mils=_optional_number_object(
            raw,
            "board_outline_mils",
            ("left", "bottom", "right", "top"),
        ),
    )


def _parse_mate_output_config(
    raw: Mapping[str, object],
    inspection: Mapping[str, object],
) -> DebugPlateOutputConfig:
    output = _parse_output_config(raw)
    if output.board_outline_mils is not None:
        return output
    origin = _optional_string(raw, "origin", "preserve_source")
    if origin != "preserve_source":
        return output
    outline = single_inspection_board_outline(inspection)
    if outline is None:
        return output
    return replace(output, board_outline_mils=outline)

def _selection_from_inspection(inspection: Mapping[str, object]) -> JsonObject:
    boards = inspection.get("boards", [])
    if not isinstance(boards, list):
        boards = []
    return {
        "boards": [
            _selection_board(board)
            for board in boards
            if isinstance(board, dict)
        ]
    }


def _selection_board(board: Mapping[str, object]) -> JsonObject:
    return {
        "board_key": str(board.get("board_key", "") or ""),
        "pcb_path": str(board.get("pcb_path", "") or ""),
        "components": list(_list_field(board, "components")),
        "free_pads": list(_list_field(board, "free_pads")),
    }


def _list_field(payload: Mapping[str, object], name: str) -> list[object]:
    value = payload.get(name, [])
    return list(value) if isinstance(value, list) else []


def _component_candidates(pcbdoc: object) -> list[DebugPlateComponentCandidate]:
    candidates: list[DebugPlateComponentCandidate] = []
    components = list(getattr(pcbdoc, "components", []) or [])
    for index, component in enumerate(components):
        designator = str(getattr(component, "designator", "") or "")
        kind = _component_candidate_kind(designator)
        if kind is None:
            continue
        x_mils, y_mils = _component_position_mils(pcbdoc, index, component)
        candidates.append(
            DebugPlateComponentCandidate(
                designator=designator,
                kind=kind,
                layer=str(getattr(component, "layer", "") or ""),
                footprint=str(getattr(component, "footprint", "") or ""),
                x_mils=x_mils,
                y_mils=y_mils,
                net_name=_component_net_name(pcbdoc, index),
                pad_geometries=component_pad_geometries(pcbdoc, index),
            )
        )
    return candidates


def _free_pad_candidates(pcbdoc: object) -> list[DebugPlatePadCandidate]:
    candidates: list[DebugPlatePadCandidate] = []
    for pad in list(getattr(pcbdoc, "pads", []) or []):
        if not _is_free_pad(pad):
            continue
        candidates.append(_pad_candidate(pcbdoc, pad))
    return candidates


def _component_candidate_kind(designator: str) -> str | None:
    normalized = designator.strip().upper()
    if normalized.startswith(("TP", "DP")):
        return "test_point"
    if normalized.startswith(("MH", "MOUNT", "M")):
        return "mount"
    return None


def _component_position_mils(
    pcbdoc: object,
    index: int,
    component: object,
) -> tuple[float, float]:
    try:
        position_fn = getattr(pcbdoc, "get_component_pnp_position_mils")
        x_mils, y_mils = position_fn(index)
        return (float(x_mils), float(y_mils))
    except Exception:
        x_fn = getattr(component, "get_x_mils")
        y_fn = getattr(component, "get_y_mils")
        return (float(x_fn()), float(y_fn()))


def _is_free_pad(pad: object) -> bool:
    component_index = getattr(pad, "component_index", None)
    return component_index is None or int(component_index) == 0xFFFF


def _pad_candidate(pcbdoc: object, pad: object) -> DebugPlatePadCandidate:
    hole_size = _float_attr(pad, "hole_size_mils")
    plated = _bool_attr(pad, "is_plated")
    return DebugPlatePadCandidate(
        designator=_str_attr(pad, "designator"),
        kind="free_npth" if hole_size > 0.0 and not plated else "free_pad",
        layer=_int_attr(pad, "layer"),
        x_mils=_float_attr(pad, "x_mils"),
        y_mils=_float_attr(pad, "y_mils"),
        width_mils=pad_width_mils(pad),
        height_mils=pad_height_mils(pad),
        hole_size_mils=hole_size,
        plated=plated,
        shape=_int_attr(pad, "shape"),
        net_name=_pad_net_name(pcbdoc, pad),
    )


def _component_net_name(pcbdoc: object, component_index: int) -> str | None:
    net_names: set[str] = set()
    try:
        primitives = getattr(pcbdoc, "get_component_primitives")(component_index)
    except Exception:
        primitives = {}
    pads = primitives.get("pads", []) if isinstance(primitives, dict) else []
    for pad in pads:
        net_name = _pad_net_name(pcbdoc, pad)
        if net_name:
            net_names.add(net_name)
    if len(net_names) == 1:
        return next(iter(net_names))
    return None


def _pad_net_name(pcbdoc: object, pad: object) -> str | None:
    net_index = getattr(pad, "net_index", None)
    if net_index is None:
        return None
    nets = list(getattr(pcbdoc, "nets", []) or [])
    index = int(net_index)
    if 0 <= index < len(nets):
        name = str(getattr(nets[index], "name", "") or "").strip()
        return name or None
    return None


def _str_attr(obj: object, name: str) -> str:
    value = getattr(obj, name, "")
    return "" if value is None else str(value)


def _float_attr(obj: object, name: str) -> float:
    value = getattr(obj, name, 0.0)
    return 0.0 if value is None else float(value)


def _int_attr(obj: object, name: str) -> int:
    value = getattr(obj, name, 0)
    return 0 if value is None else int(value)


def _bool_attr(obj: object, name: str) -> bool:
    value = getattr(obj, name, False)
    return False if value is None else bool(value)


def _parse_marker_config(raw: Mapping[str, object]) -> DebugPlateMarkerConfig | None:
    enabled = _optional_bool(raw, "enabled", True)
    if not enabled:
        return None
    return DebugPlateMarkerConfig(
        text=_optional_string(raw, "text", "DEBUG PLATE"),
        position_mils=_required_point(raw, "position_mils", default=(200.0, 200.0)),
        height_mils=_optional_float(raw, "height_mils", 60.0),
        layer=_optional_string(raw, "layer", "TOP_OVERLAY"),
    )


def _parse_known_parts_config(
    raw: Mapping[str, object] | None,
    *,
    base_dir: Path | str | None,
) -> DebugPlateKnownPartsConfig | None:
    if raw is None:
        return None
    manifest = _optional_string(raw, "manifest", None)
    cache_dir = _optional_string(raw, "cache_dir", None)
    if not manifest and not cache_dir:
        return None

    base_path = Path(base_dir).resolve() if base_dir is not None else Path.cwd()
    resolved_cache_dir = (
        _resolve_config_path(cache_dir, base_path) if cache_dir else None
    )
    manifest_path = (
        _resolve_config_path(manifest, base_path)
        if manifest
        else manifest_path_for_cache_dir(resolved_cache_dir or base_path)
    )
    return DebugPlateKnownPartsConfig(
        manifest_path=manifest_path,
        cache_dir=resolved_cache_dir or manifest_path.parent,
    )


def _parse_placement_config(raw: Mapping[str, object]) -> DebugPlatePlacementConfig:
    mount_side = _optional_string(raw, "source_mount_side", "bottom")
    if mount_side not in {"bottom", "top"}:
        raise ValueError("Debug-plate placement.source_mount_side must be bottom or top")
    return DebugPlatePlacementConfig(
        source_mount_side=mount_side,
        offset_mils=_required_point(raw, "offset_mils", default=(0.0, 0.0)),
        mirror_x=_optional_bool(raw, "mirror_x", False),
        mirror_y=_optional_bool(raw, "mirror_y", False),
        mirror_origin_mils=_required_point(
            raw,
            "mirror_origin_mils",
            default=(0.0, 0.0),
        ),
    )


def _parse_pcb_labels_config(
    raw: Mapping[str, object] | None,
) -> DebugPlatePcbLabelsConfig:
    if raw is None:
        raw = {}
    enabled = _optional_bool(raw, "enabled", False)
    side = _optional_string(raw, "side", "right")
    if side not in {"left", "right"}:
        raise ValueError("Debug-plate pcb_labels.side must be left or right")
    return DebugPlatePcbLabelsConfig(
        enabled=enabled,
        side=side,
        offset_mils=_required_point(raw, "offset_mils", default=(120.0, 0.0)),
        box_size_mils=_optional_point(raw, "box_size_mils"),
        center_box_on_target=_optional_bool(raw, "center_box_on_target", True),
        style=_section(raw, "style"),
    )


def _default_mate_placement_config() -> DebugPlatePlacementConfig:
    return DebugPlatePlacementConfig(
        source_mount_side="bottom",
        offset_mils=(0.0, 0.0),
        mirror_x=False,
        mirror_y=False,
        mirror_origin_mils=(0.0, 0.0),
    )


def _parse_mate_pcb_labels_config(
    _root: Mapping[str, object],
) -> DebugPlatePcbLabelsConfig:
    return _parse_pcb_labels_config({"enabled": False})


def _mate_source_inspection(
    root: Mapping[str, object],
    *,
    base_dir: Path | str | None,
) -> JsonObject:
    source = _section(root, "source")
    source_board = _optional_string(source, "board", None)
    if not source_board:
        raise ValueError("Mate config source.board must be a non-empty string")
    base_path = Path(base_dir).resolve() if base_dir is not None else Path.cwd()
    input_file = _resolve_config_path(source_board, base_path)
    return inspect_debug_plate_source(
        input_file,
        pcbdoc_selector=_optional_string(source, "pcbdoc", None),
        project_context=_optional_string(source, "project_context", "auto"),
    )


def _selection_from_mate_inspection(
    root: Mapping[str, object],
    inspection: Mapping[str, object],
) -> DebugPlateSelectionConfig:
    projection_items = [
        projection
        for projection in _mate_projection_items(root)
        if _projection_requests_mate_component(projection)
    ]
    boards: list[JsonObject] = []
    for board in _list_field(inspection, "boards"):
        if not isinstance(board, dict):
            continue
        components = _selected_mate_components(board, projection_items)
        free_pads = _selected_mate_free_pads(board, projection_items)
        if not components and not free_pads:
            continue
        boards.append(
            {
                "board_key": str(board.get("board_key", "") or ""),
                "pcb_path": str(board.get("pcb_path", "") or ""),
                "components": components,
                "free_pads": free_pads,
            }
        )
    _validate_mate_source_sides(root, boards)
    return _parse_selection_config({"boards": boards})


def _mate_projection_items(root: Mapping[str, object]) -> list[JsonObject]:
    projections = root.get("projections", [])
    if not isinstance(projections, list):
        raise ValueError("Mate config projections must be an array")
    return [dict(projection) for projection in projections if isinstance(projection, dict)]


def _validate_mate_source_sides(
    root: Mapping[str, object],
    boards: list[JsonObject],
) -> None:
    validation = _section(root, "validation")
    source_side = _optional_string(validation, "source_side", "infer_single_side")
    if source_side in {None, "any", "none"}:
        return
    side_agnostic_kinds = _mate_side_agnostic_kinds(validation)
    selected_sides = {
        side
        for board in boards
        for component in _list_field(board, "components")
        if isinstance(component, dict)
        and not _is_side_agnostic_component(component, side_agnostic_kinds)
        for side in [_component_side(component)]
        if side is not None
    }
    if source_side == "infer_single_side":
        if len(selected_sides) > 1:
            raise ValueError(
                "Mate config selection mixes top and bottom source components"
            )
        return
    if source_side in {"top", "bottom"}:
        unexpected = selected_sides - {source_side}
        if unexpected:
            raise ValueError(
                f"Mate config expected {source_side} source components, "
                f"found {', '.join(sorted(unexpected))}"
            )
        return
    raise ValueError(
        "Mate config validation.source_side must be infer_single_side, any, "
        "none, top, or bottom"
    )


def _component_side(component: Mapping[str, object]) -> str | None:
    layer = str(component.get("layer", "") or "").strip().lower()
    if "bottom" in layer:
        return "bottom"
    if "top" in layer:
        return "top"
    return None


def _mate_side_agnostic_kinds(validation: Mapping[str, object]) -> set[str]:
    value = validation.get("side_agnostic_kinds")
    if value is None:
        return {"mount"}
    if not isinstance(value, list):
        raise ValueError("Mate config validation.side_agnostic_kinds must be an array")
    result: set[str] = set()
    for item in value:
        if not isinstance(item, str) or not item:
            raise ValueError(
                "Mate config validation.side_agnostic_kinds must contain strings"
            )
        result.add(item.strip().lower())
    return result


def _is_side_agnostic_component(
    component: Mapping[str, object],
    side_agnostic_kinds: set[str],
) -> bool:
    kind = str(component.get("kind", "") or "").strip().lower()
    return kind in side_agnostic_kinds


def _projection_requests_mate_component(projection: Mapping[str, object]) -> bool:
    for action in _list_field(projection, "actions"):
        if isinstance(action, dict) and action.get("kind") == "mate_component":
            return True
    return False


def _projection_id(projection: Mapping[str, object]) -> str | None:
    projection_id = projection.get("id")
    if projection_id is None:
        return None
    if not isinstance(projection_id, str) or not projection_id:
        raise ValueError("Mate projection id must be a non-empty string")
    return projection_id


def _projection_mate_part_role(projection: Mapping[str, object]) -> str | None:
    for action in _list_field(projection, "actions"):
        if not isinstance(action, dict) or action.get("kind") != "mate_component":
            continue
        part = action.get("part")
        if part is None:
            return None
        if not isinstance(part, str) or not part:
            raise ValueError("Mate projection mate_component.part must be a string")
        return part
    return None


def _projection_pcb_label_config(
    projection: Mapping[str, object],
) -> JsonObject | None:
    for action in _list_field(projection, "actions"):
        if not isinstance(action, dict) or action.get("kind") != "label":
            continue
        raw: JsonObject = {"enabled": True}
        placement = action.get("placement")
        if placement is not None:
            if not isinstance(placement, dict):
                raise ValueError("Mate projection label.placement must be an object")
            raw.update(dict(placement))
        style = action.get("style")
        if style is not None:
            if not isinstance(style, dict):
                raise ValueError("Mate projection label.style must be an object")
            raw["style"] = dict(style)
        return raw
    return None


def _projection_reference_graphics_config(
    projection: Mapping[str, object],
) -> JsonObject | None:
    for action in _list_field(projection, "actions"):
        if not isinstance(action, dict) or action.get("kind") != "reference_graphics":
            continue
        raw = dict(action)
        raw["enabled"] = True
        return raw
    return None


def _selected_mate_components(
    board: Mapping[str, object],
    projections: list[JsonObject],
) -> list[JsonObject]:
    selected: list[JsonObject] = []
    seen: set[str] = set()
    for projection in projections:
        component_selector = _projection_selector(projection, "components")
        if component_selector is None:
            continue
        for component in _list_field(board, "components"):
            if not isinstance(component, dict):
                continue
            designator = str(component.get("designator", "") or "")
            if designator.upper() in seen:
                continue
            if _component_matches_selector(component, component_selector):
                selected_component = dict(component)
                _add_optional(
                    selected_component,
                    "mate_projection_id",
                    _projection_id(projection),
                )
                _add_optional(
                    selected_component,
                    "mate_part_role",
                    _projection_mate_part_role(projection),
                )
                _add_optional(
                    selected_component,
                    "mate_pcb_label",
                    _projection_pcb_label_config(projection),
                )
                _add_optional(
                    selected_component,
                    "mate_reference_graphics",
                    _projection_reference_graphics_config(projection),
                )
                selected.append(selected_component)
                seen.add(designator.upper())
    return selected


def _selected_mate_free_pads(
    board: Mapping[str, object],
    projections: list[JsonObject],
) -> list[JsonObject]:
    selected: list[JsonObject] = []
    seen: set[str] = set()
    for projection in projections:
        pad_selector = _projection_selector(projection, "free_pads")
        if pad_selector is None:
            continue
        for pad in _list_field(board, "free_pads"):
            if not isinstance(pad, dict):
                continue
            designator = str(pad.get("designator", "") or "")
            if designator.upper() in seen:
                continue
            if _free_pad_matches_selector(pad, pad_selector):
                selected_pad = dict(pad)
                _add_optional(
                    selected_pad,
                    "mate_projection_id",
                    _projection_id(projection),
                )
                _add_optional(
                    selected_pad,
                    "mate_part_role",
                    _projection_mate_part_role(projection),
                )
                _add_optional(
                    selected_pad,
                    "mate_pcb_label",
                    _projection_pcb_label_config(projection),
                )
                _add_optional(
                    selected_pad,
                    "mate_reference_graphics",
                    _projection_reference_graphics_config(projection),
                )
                selected.append(selected_pad)
                seen.add(designator.upper())
    return selected


def _projection_selector(
    projection: Mapping[str, object],
    name: str,
) -> JsonObject | None:
    source_selector = projection.get("source")
    if source_selector is not None:
        if not isinstance(source_selector, dict):
            raise ValueError("Mate projection source must be an object")
        source = dict(source_selector)
        object_kind = str(source.pop("object", source.pop("type", "")) or "")
        if _source_object_matches_selector(object_kind, name):
            return source
        return None

    select = projection.get("select", {})
    if not isinstance(select, dict):
        raise ValueError("Mate projection select must be an object")
    selector = select.get(name)
    if selector is None:
        return None
    if not isinstance(selector, dict):
        raise ValueError(f"Mate projection select.{name} must be an object")
    return dict(selector)


def _source_object_matches_selector(object_kind: str, selector_name: str) -> bool:
    normalized = object_kind.strip().lower().replace("-", "_")
    if selector_name == "components":
        return normalized in {"component", "components"}
    if selector_name == "free_pads":
        return normalized in {
            "free_pad",
            "free_pads",
            "pad",
            "pads",
            "drill",
            "drills",
        }
    return False


def _component_matches_selector(
    component: Mapping[str, object],
    selector: Mapping[str, object],
) -> bool:
    designator = str(component.get("designator", "") or "")
    kind = str(component.get("kind", "") or "")
    return _designator_matches_selector(designator, selector) and _kind_matches_selector(
        kind,
        selector,
    )


def _free_pad_matches_selector(
    pad: Mapping[str, object],
    selector: Mapping[str, object],
) -> bool:
    designator = str(pad.get("designator", "") or "")
    kind = str(pad.get("kind", "") or "")
    return (
        _designator_matches_selector(designator, selector)
        and _kind_matches_selector(kind, selector)
        and _optional_bool_matches(pad, selector, "plated")
        and _optional_range_matches(pad, selector, "hole_size_mils")
    )


def _designator_matches_selector(
    designator: str,
    selector: Mapping[str, object],
) -> bool:
    patterns = _optional_selector_strings(selector, "designators")
    if not patterns:
        return True
    return any(_designator_matches_pattern(designator, pattern) for pattern in patterns)


def _designator_matches_pattern(designator: str, pattern: str) -> bool:
    normalized = designator.upper()
    candidate = pattern.upper()
    if "*" in candidate or "?" in candidate:
        return fnmatch.fnmatchcase(normalized, candidate)
    expanded = _expand_designator_range(candidate)
    if expanded is not None:
        return normalized in expanded
    return normalized == candidate


def _expand_designator_range(pattern: str) -> set[str] | None:
    if "-" not in pattern:
        return None
    start, end = pattern.split("-", 1)
    start_prefix, start_number = _split_designator_number(start)
    end_prefix, end_number = _split_designator_number(end)
    if not end_prefix and start_prefix:
        end_prefix = start_prefix
    if (
        not start_prefix
        or start_prefix != end_prefix
        or start_number is None
        or end_number is None
        or end_number < start_number
    ):
        return None
    return {
        f"{start_prefix}{number}"
        for number in range(start_number, end_number + 1)
    }


def _split_designator_number(value: str) -> tuple[str, int | None]:
    index = len(value)
    while index > 0 and value[index - 1].isdigit():
        index -= 1
    prefix = value[:index]
    suffix = value[index:]
    return (prefix, int(suffix) if suffix else None)


def _kind_matches_selector(kind: str, selector: Mapping[str, object]) -> bool:
    kinds = [
        *(_optional_selector_strings(selector, "kinds")),
        *(_optional_selector_strings(selector, "kind")),
    ]
    normalized = kind.strip().lower()
    return not kinds or normalized in {item.strip().lower() for item in kinds}


def _optional_bool_matches(
    item: Mapping[str, object],
    selector: Mapping[str, object],
    name: str,
) -> bool:
    expected = selector.get(name)
    if expected is None:
        return True
    if not isinstance(expected, bool):
        raise ValueError(f"Mate selector field {name!r} must be a boolean")
    return bool(item.get(name)) is expected


def _optional_range_matches(
    item: Mapping[str, object],
    selector: Mapping[str, object],
    name: str,
) -> bool:
    raw_range = selector.get(name)
    if raw_range is None:
        return True
    if not isinstance(raw_range, dict):
        raise ValueError(f"Mate selector field {name!r} must be an object")
    if name not in item:
        return False
    value = _number_like(item, name)
    minimum = raw_range.get("min")
    maximum = raw_range.get("max")
    if minimum is not None and value < _range_number(minimum, f"{name}.min"):
        return False
    if maximum is not None and value > _range_number(maximum, f"{name}.max"):
        return False
    return True


def _range_number(value: object, name: str) -> float:
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise ValueError(f"Mate selector field {name!r} must be numeric")
    return float(value)


def _optional_selector_strings(
    args: Mapping[str, object],
    name: str,
) -> list[str]:
    value = args.get(name)
    if value is None:
        return []
    if isinstance(value, str):
        return _split_selector_string(value, name)
    if not isinstance(value, list):
        raise ValueError(f"Mate selector field {name!r} must be a string or array")
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item:
            raise ValueError(
                f"Mate selector field {name!r} must contain non-empty strings"
            )
        result.extend(_split_selector_string(item, name))
    return result


def _split_selector_string(value: str, name: str) -> list[str]:
    result = [item.strip() for item in value.split(",") if item.strip()]
    if not result:
        raise ValueError(f"Mate selector field {name!r} must be non-empty")
    return result


def _parse_selection_config(raw: Mapping[str, object]) -> DebugPlateSelectionConfig:
    boards = raw.get("boards", [])
    if not isinstance(boards, list):
        raise ValueError("Debug-plate selection.boards must be an array")
    return DebugPlateSelectionConfig(
        boards=tuple(
            _parse_selection_board(board)
            for board in boards
            if isinstance(board, dict)
        )
    )


def _parse_selection_board(raw: Mapping[str, object]) -> DebugPlateSelectionBoard:
    return DebugPlateSelectionBoard(
        board_key=str(raw.get("board_key", "") or ""),
        pcb_path=str(raw.get("pcb_path", "") or ""),
        components=tuple(
            _parse_selection_component(component)
            for component in _list_field(raw, "components")
            if isinstance(component, dict)
        ),
        free_pads=tuple(
            _parse_selection_pad(pad)
            for pad in _list_field(raw, "free_pads")
            if isinstance(pad, dict)
        ),
    )


def _parse_selection_component(
    raw: Mapping[str, object],
) -> DebugPlateSelectionComponent:
    return DebugPlateSelectionComponent(
        designator=str(raw.get("designator", "") or ""),
        kind=str(raw.get("kind", "") or ""),
        layer=str(raw.get("layer", "") or ""),
        footprint=str(raw.get("footprint", "") or ""),
        x_mils=_number_like(raw, "x_mils"),
        y_mils=_number_like(raw, "y_mils"),
        net_name=_optional_string(raw, "net_name", None),
        mate_projection_id=_optional_string(raw, "mate_projection_id", None),
        mate_part_role=_optional_string(raw, "mate_part_role", None),
        mate_pcb_label=_optional_section(raw, "mate_pcb_label"),
        mate_reference_graphics=_optional_section(raw, "mate_reference_graphics"),
        source_pad_geometries=parse_source_pad_geometries(raw),
    )


def _parse_selection_pad(raw: Mapping[str, object]) -> DebugPlateSelectionPad:
    return DebugPlateSelectionPad(
        designator=str(raw.get("designator", "") or ""),
        kind=str(raw.get("kind", "") or ""),
        x_mils=_number_like(raw, "x_mils"),
        y_mils=_number_like(raw, "y_mils"),
        net_name=_optional_string(raw, "net_name", None),
        mate_projection_id=_optional_string(raw, "mate_projection_id", None),
        mate_part_role=_optional_string(raw, "mate_part_role", None),
        mate_pcb_label=_optional_section(raw, "mate_pcb_label"),
        mate_reference_graphics=_optional_section(raw, "mate_reference_graphics"),
        source_pad_geometries=parse_selection_pad_geometries(raw),
    )


def _project_create_operation(
    output: DebugPlateOutputConfig,
    *,
    documents: list[str] | None = None,
) -> JsonObject:
    args: JsonObject = {
        "output_dir": output.output_dir,
        "project_name": output.project_name,
        "layer_stack_template": output.layer_stack_template,
        "overwrite": output.overwrite,
    }
    _add_optional(args, "schematic_filename", output.schematic_filename)
    _add_optional(args, "board_filename", output.board_filename)
    _add_optional(args, "project_filename", output.project_filename)
    _add_optional(args, "board_outline_mils", output.board_outline_mils)
    if documents:
        args["documents"] = documents
    return {
        "id": "create_debug_plate_project",
        "op": "project.create-skeleton",
        "message": "Create debug-plate project skeleton",
        "args": args,
    }


def _pcb_marker_operation(
    output: DebugPlateOutputConfig,
    marker: DebugPlateMarkerConfig,
) -> JsonObject:
    return {
        "id": "add_debug_plate_marker",
        "op": "pcbdoc.add-text",
        "message": "Add debug-plate PCB marker text",
        "args": {
            "file": _output_file(output.output_dir, _board_filename(output)),
            "overwrite": True,
            "text": marker.text,
            "position_mils": list(marker.position_mils),
            "height_mils": marker.height_mils,
            "layer": marker.layer,
        },
    }


def _known_part_placement_operations(config: DebugPlateConfig) -> list[JsonObject]:
    known_parts = config.known_parts
    if known_parts is None:
        return []
    targets = _placement_targets(config.selection, config.placement)
    if not targets:
        return []

    manifest = load_debug_plate_known_parts_manifest(known_parts.manifest_path)
    operations: list[JsonObject] = []
    used_designators: set[str] = set()
    free_counts: dict[str, int] = {}
    for index, target in enumerate(targets, start=1):
        target_kind = str(target.get("kind", "") or "")
        part = resolve_known_part(
            manifest,
            target_kind,
            role=_target_optional_string(target, "mate_part_role"),
        )
        designator = _projected_designator(
            target,
            part,
            manifest,
            used_designators=used_designators,
            free_counts=free_counts,
        )
        operations.append(
            _schematic_part_operation(
                config.output,
                part,
                target,
                designator,
                index,
            )
        )
        net_label_operation = _schematic_net_label_operation(
            config.output,
            target,
            designator,
            index,
        )
        if net_label_operation is not None:
            operations.append(net_label_operation)
        operations.append(
            _pcb_part_operation(
                config.output,
                part,
                target,
                designator,
            )
        )
        target_labels = _target_pcb_labels_config(config.pcb_labels, target)
        pcb_label_operation = _pcb_net_label_operation(
            config.output,
            target_labels,
            target,
            designator,
        )
        if pcb_label_operation is not None:
            operations.append(pcb_label_operation)
        operations.extend(
            build_pcb_reference_graphics_operations(
                output_dir=config.output.output_dir,
                board_filename=_board_filename(config.output),
                target=target,
                designator=designator,
            )
        )
    operations.append(_debug_plate_user_union_operation(config.output))
    return operations


def _known_part_project_documents(config: DebugPlateConfig) -> list[str]:
    return [
        reference["project_path"]
        for reference in _known_part_library_references(config)
    ]


def _known_part_library_copy_operations(config: DebugPlateConfig) -> list[JsonObject]:
    operations: list[JsonObject] = []
    for reference in _known_part_library_references(config):
        project_path = reference["project_path"]
        source = reference["source"]
        operations.append(
            {
                "id": f"copy_{_safe_id(project_path)}",
                "op": "file.copy",
                "message": f"Copy debug-plate library {Path(project_path).name}",
                "args": {
                    "source": source,
                    "destination": _output_file(config.output.output_dir, project_path),
                    "overwrite": config.output.overwrite,
                },
            }
        )
    return operations


def _known_part_library_references(config: DebugPlateConfig) -> list[dict[str, str]]:
    known_parts = config.known_parts
    if known_parts is None:
        return []
    targets = _placement_targets(config.selection, config.placement)
    if not targets:
        return []

    manifest = load_debug_plate_known_parts_manifest(known_parts.manifest_path)
    references: dict[str, str] = {}
    for target in targets:
        target_kind = str(target.get("kind", "") or "")
        part = resolve_known_part(
            manifest,
            target_kind,
            role=_target_optional_string(target, "mate_part_role"),
        )
        for field in ("symbol_library", "footprint_library"):
            project_path = _known_part_project_library_path(part, field)
            references[project_path] = _known_part_file(known_parts, part, field)
    return [
        {"project_path": project_path, "source": references[project_path]}
        for project_path in sorted(references)
    ]


def _placement_targets(
    selection: DebugPlateSelectionConfig,
    placement: DebugPlatePlacementConfig | None = None,
) -> list[JsonObject]:
    targets: list[JsonObject] = []
    for board in selection.boards:
        for component in board.components:
            x_mils, y_mils = _transform_placement(
                component.x_mils,
                component.y_mils,
                placement,
            )
            targets.append(
                {
                    "board_key": board.board_key,
                    "source_designator": component.designator,
                    "kind": component.kind,
                    "source_footprint": component.footprint,
                    "source_x_mils": component.x_mils,
                    "source_y_mils": component.y_mils,
                    "net_name": component.net_name,
                    "mate_projection_id": component.mate_projection_id,
                    "mate_part_role": component.mate_part_role,
                    "mate_pcb_label": component.mate_pcb_label,
                    "mate_reference_graphics": component.mate_reference_graphics,
                    "source_pad_geometries": transform_source_pad_geometries(
                        component.source_pad_geometries,
                        placement,
                    ),
                    "x_mils": x_mils,
                    "y_mils": y_mils,
                }
            )
        for pad in board.free_pads:
            x_mils, y_mils = _transform_placement(
                pad.x_mils,
                pad.y_mils,
                placement,
            )
            targets.append(
                {
                    "board_key": board.board_key,
                    "source_designator": pad.designator,
                    "kind": pad.kind,
                    "source_footprint": "",
                    "source_x_mils": pad.x_mils,
                    "source_y_mils": pad.y_mils,
                    "net_name": pad.net_name,
                    "mate_projection_id": pad.mate_projection_id,
                    "mate_part_role": pad.mate_part_role,
                    "mate_pcb_label": pad.mate_pcb_label,
                    "mate_reference_graphics": pad.mate_reference_graphics,
                    "source_pad_geometries": transform_source_pad_geometries(
                        pad.source_pad_geometries,
                        placement,
                    ),
                    "x_mils": x_mils,
                    "y_mils": y_mils,
                }
            )
    return targets

def _transform_placement(
    x_mils: float,
    y_mils: float,
    placement: DebugPlatePlacementConfig | None,
) -> tuple[float, float]:
    if placement is None:
        return (x_mils, y_mils)
    mirror_origin_x, mirror_origin_y = placement.mirror_origin_mils
    transformed_x = 2.0 * mirror_origin_x - x_mils if placement.mirror_x else x_mils
    transformed_y = 2.0 * mirror_origin_y - y_mils if placement.mirror_y else y_mils
    offset_x, offset_y = placement.offset_mils
    return (transformed_x + offset_x, transformed_y + offset_y)


def _schematic_part_operation(
    output: DebugPlateOutputConfig,
    part: Mapping[str, object],
    target: Mapping[str, object],
    designator: str,
    index: int,
) -> JsonObject:
    symbol_name = _part_string(part, "symbol_name")
    footprint_name = _part_string(part, "footprint_name")
    return {
        "id": f"add_{_safe_id(designator)}_symbol",
        "op": "schdoc.add-component",
        "message": f"Add debug-plate schematic component {designator}",
        "args": {
            "file": _output_file(output.output_dir, _schematic_filename(output)),
            "overwrite": True,
            "library": _copied_known_part_file(output, part, "symbol_library"),
            "symbol": symbol_name,
            "designator": designator,
            "position_mils": list(_schematic_position(index)),
            "design_item_id": symbol_name,
            "footprint_model": footprint_name,
            "footprint_library": footprint_name,
            "parameters": _debug_plate_component_parameters(target, part),
        },
    }


def _schematic_net_label_operation(
    output: DebugPlateOutputConfig,
    target: Mapping[str, object],
    designator: str,
    index: int,
) -> JsonObject | None:
    net_name = _target_optional_string(target, "net_name")
    if not net_name:
        return None
    return {
        "id": f"label_{_safe_id(designator)}_net",
        "op": "schdoc.add-net-label",
        "message": f"Add debug-plate schematic net label for {designator}",
        "args": {
            "file": _output_file(output.output_dir, _schematic_filename(output)),
            "overwrite": True,
            "text": net_name,
            "location_mils": list(_schematic_net_label_position(index)),
        },
    }


def _pcb_part_operation(
    output: DebugPlateOutputConfig,
    part: Mapping[str, object],
    target: Mapping[str, object],
    designator: str,
) -> JsonObject:
    footprint_library = _copied_known_part_file(output, part, "footprint_library")
    args: JsonObject = {
        "file": _output_file(output.output_dir, _board_filename(output)),
        "overwrite": True,
        "library": footprint_library,
        "footprint": _part_string(part, "footprint_name"),
        "designator": designator,
        "position_mils": [
            _target_float(target, "x_mils"),
            _target_float(target, "y_mils"),
        ],
        "layer": "TOP",
        "source_footprint_library": Path(footprint_library).name,
        "comment_text": _part_string(part, "role"),
        "component_parameters": _debug_plate_component_parameters(target, part),
    }
    pad_nets = _debug_plate_pad_nets(target, part)
    if pad_nets:
        args["pad_nets"] = pad_nets
    return {
        "id": f"add_{_safe_id(designator)}_footprint",
        "op": "pcbdoc.add-component",
        "message": f"Add debug-plate PCB component {designator}",
        "args": args,
    }


def _target_pcb_labels_config(
    default_labels: DebugPlatePcbLabelsConfig,
    target: Mapping[str, object],
) -> DebugPlatePcbLabelsConfig:
    raw = target.get("mate_pcb_label")
    if isinstance(raw, dict):
        return _parse_pcb_labels_config(raw)
    return default_labels


def _pcb_net_label_operation(
    output: DebugPlateOutputConfig,
    labels: DebugPlatePcbLabelsConfig,
    target: Mapping[str, object],
    designator: str,
) -> JsonObject | None:
    net_name = _target_optional_string(target, "net_name")
    if not labels.enabled or not net_name:
        return None
    args: JsonObject = {
        "file": _output_file(output.output_dir, _board_filename(output)),
        "overwrite": True,
        "text": net_name,
        "position_mils": list(_pcb_net_label_position(target, labels)),
        **_pcb_net_label_style_args(labels),
    }
    return {
        "id": f"label_{_safe_id(designator)}_pcb_net",
        "op": "pcbdoc.add-text",
        "message": f"Add debug-plate PCB net label for {designator}",
        "args": args,
    }


def _pcb_net_label_position(
    target: Mapping[str, object],
    labels: DebugPlatePcbLabelsConfig,
) -> tuple[float, float]:
    x_mils = _target_float(target, "x_mils")
    y_mils = _target_float(target, "y_mils")
    offset_x, offset_y = labels.offset_mils
    box_width = labels.box_size_mils[0] if labels.box_size_mils is not None else 0.0
    if labels.side == "left":
        x_mils = x_mils - offset_x - box_width
    else:
        x_mils = x_mils + offset_x
    y_mils = y_mils + offset_y
    if labels.center_box_on_target and labels.box_size_mils is not None:
        y_mils -= labels.box_size_mils[1] / 2.0
    return (x_mils, y_mils)


def _pcb_net_label_style_args(labels: DebugPlatePcbLabelsConfig) -> JsonObject:
    style = dict(labels.style)
    use_box = labels.box_size_mils is not None
    args: JsonObject = {
        "height_mils": _style_float(style, "height_mils", 65.0),
        "layer": _style_string_or_int(style, "layer", "TOP_OVERLAY"),
        "font_kind": _style_string(style, "font_kind", "truetype"),
        "font_name": _style_string(style, "font_name", "Arial"),
        "bold": _style_bool(style, "bold", True),
        "stroke_width_mils": _style_float(style, "stroke_width_mils", 10.0),
        "is_inverted": _style_bool(style, "is_inverted", use_box),
        "inverted_margin_mils": _style_float(style, "inverted_margin_mils", 10.0),
        "use_inverted_rectangle": _style_bool(
            style,
            "use_inverted_rectangle",
            use_box,
        ),
        "is_frame": _style_bool(style, "is_frame", use_box),
        "text_justification": _style_string_or_int(
            style,
            "text_justification",
            _default_pcb_label_justification(labels.side),
        ),
    }
    if labels.box_size_mils is not None:
        box_size = list(labels.box_size_mils)
        if args["use_inverted_rectangle"]:
            args["inverted_rectangle_size_mils"] = box_size
        if args["is_frame"]:
            args["frame_size_mils"] = box_size
    for key in _PCB_LABEL_STYLE_PASSTHROUGH_KEYS:
        if key not in args and key in style:
            args[key] = style[key]
    return args


def _default_pcb_label_justification(side: str) -> str:
    return "LEFT_TOP" if side == "left" else "RIGHT_TOP"


def _debug_plate_user_union_operation(output: DebugPlateOutputConfig) -> JsonObject:
    return {
        "id": "group_debug_plate_features",
        "op": "pcbdoc.create-user-union",
        "message": "Group generated debug-plate PCB features",
        "args": {
            "file": _output_file(output.output_dir, _board_filename(output)),
            "overwrite": True,
            "name": "DEBUG_PLATE_FEATURES",
        },
    }


def _debug_plate_component_parameters(
    target: Mapping[str, object],
    part: Mapping[str, object],
) -> dict[str, str]:
    parameters = {
        "DebugPlateRole": _part_string(part, "role"),
        "DebugPlateSourceBoard": str(target.get("board_key", "") or ""),
        "DebugPlateSourceDesignator": str(target.get("source_designator", "") or ""),
        "DebugPlateSourceKind": str(target.get("kind", "") or ""),
        "DebugPlateSourceFootprint": str(target.get("source_footprint", "") or ""),
    }
    net_name = _target_optional_string(target, "net_name")
    if net_name:
        parameters["DebugPlateSourceNet"] = net_name
    return parameters


def _debug_plate_pad_nets(
    target: Mapping[str, object],
    part: Mapping[str, object],
) -> dict[str, str] | None:
    net_name = _target_optional_string(target, "net_name")
    signal_pad = _part_optional_string(part, "signal_pad_designator")
    if not net_name or not signal_pad:
        return None
    return {signal_pad: net_name}


def _known_part_file(
    known_parts: DebugPlateKnownPartsConfig,
    part: Mapping[str, object],
    field: str,
) -> str:
    relative = _part_string(part, field)
    return (known_parts.cache_dir / relative).resolve().as_posix()


def _copied_known_part_file(
    output: DebugPlateOutputConfig,
    part: Mapping[str, object],
    field: str,
) -> str:
    return _output_file(
        output.output_dir,
        _known_part_project_library_path(part, field),
    )


def _known_part_project_library_path(
    part: Mapping[str, object],
    field: str,
) -> str:
    return (Path("libraries") / Path(_part_string(part, field))).as_posix()


def _projected_designator(
    target: Mapping[str, object],
    part: Mapping[str, object],
    manifest: Mapping[str, object],
    *,
    used_designators: set[str],
    free_counts: dict[str, int],
) -> str:
    kind = str(target.get("kind", "") or "")
    source = str(target.get("source_designator", "") or "")
    prefix = _part_string(part, "designator_prefix")
    if kind == "free_npth":
        base = _next_prefixed_designator(prefix, free_counts)
    else:
        base = _normalized_designator(source, kind, manifest) or (
            _next_prefixed_designator(prefix, free_counts)
        )
    result = base
    suffix = 2
    while result.upper() in used_designators:
        result = f"{base}_{suffix}"
        suffix += 1
    used_designators.add(result.upper())
    return result


def _normalized_designator(
    designator: str,
    kind: str,
    manifest: Mapping[str, object],
) -> str:
    normalized = manifest.get("designator_normalization", {})
    if not isinstance(normalized, dict):
        return designator
    by_kind = normalized.get(kind, {})
    if not isinstance(by_kind, dict):
        return designator
    upper_designator = designator.upper()
    for raw_key, raw_value in by_kind.items():
        key = str(raw_key).upper()
        value = str(raw_value)
        if upper_designator == key:
            return value
        if upper_designator.startswith(f"{key}_"):
            return f"{value}{designator[len(key):]}"
    return designator


def _next_prefixed_designator(prefix: str, counters: dict[str, int]) -> str:
    current = counters.get(prefix, 0) + 1
    counters[prefix] = current
    return f"{prefix}{current}"


def _schematic_position(index: int) -> tuple[float, float]:
    column = (index - 1) % 4
    row = (index - 1) // 4
    return (1200.0 + column * 900.0, 1200.0 + row * 500.0)


def _schematic_net_label_position(index: int) -> tuple[float, float]:
    x_mils, y_mils = _schematic_position(index)
    return (x_mils + 350.0, y_mils)


def _schematic_filename(output: DebugPlateOutputConfig) -> str:
    return output.schematic_filename or f"{output.project_name}.SchDoc"


def _board_filename(output: DebugPlateOutputConfig) -> str:
    return output.board_filename or f"{output.project_name}.PcbDoc"


def _output_file(output_dir: str, filename: str) -> str:
    return (Path(output_dir) / filename).as_posix()


def _add_optional(payload: JsonObject, name: str, value: object | None) -> None:
    if value is not None:
        payload[name] = value


def _optional_section(
    root: Mapping[str, object],
    name: str,
) -> JsonObject | None:
    value = root.get(name)
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError(f"Debug-plate config field {name!r} must be an object")
    return dict(value)


def _section(root: Mapping[str, object], name: str) -> JsonObject:
    value = root.get(name, {})
    if not isinstance(value, dict):
        raise ValueError(f"Debug-plate config field {name!r} must be an object")
    return dict(value)


def _json_object(value: object, label: str) -> JsonObject:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return dict(value)


def _optional_string(
    args: Mapping[str, object],
    name: str,
    default: str | None,
) -> str | None:
    value = args.get(name)
    if value is None:
        return default
    if not isinstance(value, str):
        raise ValueError(f"Field {name!r} must be a string")
    return value


def _number_like(args: Mapping[str, object], name: str) -> float:
    value = args.get(name, 0.0)
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise ValueError(f"Field {name!r} must be numeric")
    return float(value)


def _target_float(args: Mapping[str, object], name: str) -> float:
    value = args.get(name)
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise ValueError(f"Field {name!r} must be numeric")
    return float(value)


def _target_optional_string(args: Mapping[str, object], name: str) -> str | None:
    value = args.get(name)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"Field {name!r} must be a string")
    return value or None


def _style_string(args: Mapping[str, object], name: str, default: str) -> str:
    value = args.get(name)
    if value is None:
        return default
    if not isinstance(value, str):
        raise ValueError(f"Field pcb_labels.style.{name} must be a string")
    return value


def _style_string_or_int(
    args: Mapping[str, object],
    name: str,
    default: str | int,
) -> str | int:
    value = args.get(name)
    if value is None:
        return default
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value
    raise ValueError(f"Field pcb_labels.style.{name} must be a string or integer")


def _style_bool(args: Mapping[str, object], name: str, default: bool) -> bool:
    value = args.get(name)
    if value is None:
        return default
    if not isinstance(value, bool):
        raise ValueError(f"Field pcb_labels.style.{name} must be a boolean")
    return value


def _style_float(args: Mapping[str, object], name: str, default: float) -> float:
    value = args.get(name)
    if value is None:
        return default
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise ValueError(f"Field pcb_labels.style.{name} must be numeric")
    return float(value)


def _part_string(part: Mapping[str, object], field: str) -> str:
    value = part.get(field)
    if not isinstance(value, str) or not value:
        raise ValueError(
            f"Known-part manifest field {field!r} must be a non-empty string"
        )
    return value


def _part_optional_string(part: Mapping[str, object], field: str) -> str | None:
    value = part.get(field)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"Known-part manifest field {field!r} must be a string")
    return value or None


def _safe_id(value: str) -> str:
    result = "".join(char.lower() if char.isalnum() else "_" for char in value)
    return result.strip("_") or "part"


def _resolve_config_path(value: str, base_dir: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (base_dir / path).resolve()


def _optional_bool(args: Mapping[str, object], name: str, default: bool) -> bool:
    value = args.get(name)
    if value is None:
        return default
    if not isinstance(value, bool):
        raise ValueError(f"Field {name!r} must be a boolean")
    return value


def _optional_float(
    args: Mapping[str, object],
    name: str,
    default: float,
) -> float:
    value = args.get(name)
    if value is None:
        return default
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise ValueError(f"Field {name!r} must be numeric")
    return float(value)


def _required_point(
    args: Mapping[str, object],
    name: str,
    *,
    default: tuple[float, float],
) -> tuple[float, float]:
    value = args.get(name)
    if value is None:
        return default
    if not isinstance(value, list | tuple) or len(value) != 2:
        raise ValueError(f"Field {name!r} must be a two-number array")
    return (_point_number(value[0], name), _point_number(value[1], name))


def _optional_point(
    args: Mapping[str, object],
    name: str,
) -> tuple[float, float] | None:
    value = args.get(name)
    if value is None:
        return None
    if not isinstance(value, list | tuple) or len(value) != 2:
        raise ValueError(f"Field {name!r} must be a two-number array")
    return (_point_number(value[0], name), _point_number(value[1], name))


def _point_number(value: object, name: str) -> float:
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise ValueError(f"Field {name!r} point values must be numeric")
    return float(value)


def _optional_number_object(
    args: Mapping[str, object],
    name: str,
    fields: tuple[str, ...],
) -> JsonObject | None:
    value = args.get(name)
    if value is None:
        return None
    raw = _json_object(value, name)
    return {field: _number_field(raw, name, field) for field in fields}


def _number_field(args: Mapping[str, object], name: str, field: str) -> float:
    value = args.get(field)
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise ValueError(f"Field {name}.{field} must be numeric")
    return float(value)


def _mate_seed_projections(inspection: Mapping[str, object]) -> list[JsonObject]:
    projections: list[JsonObject] = []
    test_points = _mate_seed_component_designators(inspection, "test_point")
    if test_points:
        projections.append(_mate_seed_test_points_projection(test_points))
    mounts = _mate_seed_component_designators(inspection, "mount")
    if mounts:
        projections.append(_mate_seed_mounts_projection(mounts))
    free_npths = _mate_seed_alignment_pads(inspection)
    if free_npths:
        projections.append(_mate_seed_alignment_pins_projection(free_npths))
    return projections


def _mate_seed_component_designators(
    inspection: Mapping[str, object],
    kind: str,
) -> list[str]:
    designators = [
        str(component.get("designator", "") or "")
        for board in _list_field(inspection, "boards")
        if isinstance(board, dict)
        for component in _list_field(board, "components")
        if isinstance(component, dict) and component.get("kind") == kind
    ]
    return sorted(set(designators), key=_designator_sort_key)


def _designator_sort_key(designator: str) -> tuple[str, int, str]:
    prefix, number = _split_designator_number(designator.strip().upper())
    return (prefix, number if number is not None else -1, designator.upper())


def _mate_seed_alignment_pads(inspection: Mapping[str, object]) -> list[JsonObject]:
    return [
        dict(pad)
        for board in _list_field(inspection, "boards")
        if isinstance(board, dict)
        for pad in _list_field(board, "free_pads")
        if isinstance(pad, dict)
        and pad.get("kind") == "free_npth"
        and _is_mate_seed_alignment_hole(pad)
    ]


def _is_mate_seed_alignment_hole(pad: Mapping[str, object]) -> bool:
    hole_size = pad.get("hole_size_mils")
    return (
        isinstance(hole_size, int | float)
        and not isinstance(hole_size, bool)
        and 75.0 <= float(hole_size) <= 85.0
    )


def _mate_seed_test_points_projection(designators: list[str]) -> JsonObject:
    return {
        "id": "test_points",
        "source": {
            "object": "component",
            "designators": _designator_expression(designators),
        },
        "actions": [
            {"kind": "mate_component", "part": "test_point_pogo"},
            {
                "kind": "reference_graphics",
                "shape": "source_pad_outline",
                "layer": "MECHANICAL_1",
                "style": {"mode": "double_ring", "clearance_mils": 10},
            },
            {
                "kind": "label",
                "text": "source_net",
                "placement": {
                    "side": "right",
                    "offset_mils": [120, 0],
                    "box_size_mils": [450, 70],
                    "center_box_on_target": True,
                },
                "style": _default_mate_label_style_payload(),
            },
        ],
    }


def _mate_seed_mounts_projection(designators: list[str]) -> JsonObject:
    return {
        "id": "mounts",
        "source": {
            "object": "component",
            "designators": _designator_expression(designators),
        },
        "actions": [
            {"kind": "mate_component", "part": "m25_smt_standoff"},
        ],
    }


def _mate_seed_alignment_pins_projection(_pads: list[JsonObject]) -> JsonObject:
    return {
        "id": "alignment_pins",
        "source": {
            "object": "free_pad",
            "kind": "free_npth",
            "hole_size_mils": {"min": 75, "max": 85},
            "plated": False,
        },
        "actions": [
            {"kind": "mate_component", "part": "alignment_pin_2mm_npth"},
            {"kind": "label", "text": "source_net"},
        ],
    }


def _designator_expression(designators: list[str]) -> str:
    sorted_designators = sorted(set(designators), key=_designator_sort_key)
    tokens: list[str] = []
    run_prefix: str | None = None
    run_start: int | None = None
    run_end: int | None = None
    for designator in sorted_designators:
        prefix, number = _split_designator_number(designator.strip().upper())
        if number is None:
            _append_designator_run(tokens, run_prefix, run_start, run_end)
            tokens.append(designator)
            run_prefix = None
            run_start = None
            run_end = None
            continue
        if run_prefix == prefix and run_end is not None and number == run_end + 1:
            run_end = number
            continue
        _append_designator_run(tokens, run_prefix, run_start, run_end)
        run_prefix = prefix
        run_start = number
        run_end = number
    _append_designator_run(tokens, run_prefix, run_start, run_end)
    return ", ".join(tokens)


def _append_designator_run(
    tokens: list[str],
    prefix: str | None,
    start: int | None,
    end: int | None,
) -> None:
    if prefix is None or start is None or end is None:
        return
    if start == end:
        tokens.append(f"{prefix}{start}")
    else:
        tokens.append(f"{prefix}{start}-{end}")


def _default_mate_output_payload() -> JsonObject:
    return {
        "backend": "altium",
        "output_dir": "output/debug-plate",
        "project_name": "debug_plate",
        "origin": "preserve_source",
        "overwrite": False,
        "layer_stack_template": "2-layer",
    }


def _mate_known_parts_payload(
    known_parts_manifest: Path | str | None,
) -> JsonObject:
    if known_parts_manifest is None:
        return _default_known_parts_payload()
    return {"manifest": str(known_parts_manifest)}


def _default_mate_label_style_payload() -> JsonObject:
    return {
        "height_mils": 65,
        "layer": "TOP_OVERLAY",
        "font_kind": "truetype",
        "font_name": "Arial",
        "bold": True,
        "stroke_width_mils": 10,
        "text_justification": "RIGHT_TOP",
    }


def _default_mate_board_projection_payload() -> JsonObject:
    return {
        "outline": {"graphics": {"enabled": True, "layer": "MECHANICAL_1"}},
        "cutouts": {
            "graphics": {"enabled": True, "layer": "MECHANICAL_1"},
            "actual_cutouts": False,
        },
    }


def _default_mate_artifacts_payload() -> JsonObject:
    return {
        "pcb_layer_step": {
            "enabled": True,
            "source_layer": "bottom",
            "highlights": [
                {
                    "projection": "test_points",
                    "color": "#ffcc00",
                }
            ],
        }
    }


def _default_output_config_payload() -> JsonObject:
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


def _default_known_parts_payload() -> JsonObject:
    return {
        "manifest": "",
    }


def _default_placement_payload() -> JsonObject:
    return {
        "source_mount_side": "bottom",
        "offset_mils": [0, 0],
        "mirror_x": False,
        "mirror_y": False,
        "mirror_origin_mils": [0, 0],
    }


def _default_pcb_labels_payload() -> JsonObject:
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


def _default_marker_payload() -> JsonObject:
    return {
        "enabled": True,
        "text": "DEBUG PLATE",
        "position_mils": [200, 200],
        "height_mils": 60,
        "layer": "TOP_OVERLAY",
    }


def _debug_plate_template_text() -> str:
    return (
        "{\n"
        f'  "schema": "{DEBUG_PLATE_CONFIG_SCHEMA}",\n'
        '  "source": {\n'
        '    "dut": ""\n'
        "  },\n"
        '  "output": {\n'
        '    "output_dir": "output/debug-plate",\n'
        '    "project_name": "debug_plate",\n'
        '    "overwrite": false,\n'
        '    "layer_stack_template": "2-layer",\n'
        '    "board_outline_mils": {\n'
        '      "left": 0,\n'
        '      "bottom": 0,\n'
        '      "right": 3000,\n'
        '      "top": 2000\n'
        "    }\n"
        "  },\n"
        '  "known_parts": {\n'
        '    "manifest": ""\n'
        "  },\n"
        '  "placement": {\n'
        '    "source_mount_side": "bottom",\n'
        '    "offset_mils": [0, 0],\n'
        '    "mirror_x": false,\n'
        '    "mirror_y": false,\n'
        '    "mirror_origin_mils": [0, 0]\n'
        "  },\n"
        '  "pcb_labels": {\n'
        '    "enabled": false,\n'
        '    "side": "right",\n'
        '    "offset_mils": [120, 0],\n'
        '    "box_size_mils": [450, 70],\n'
        '    "center_box_on_target": true,\n'
        '    "style": {\n'
        '      "height_mils": 65,\n'
        '      "layer": "TOP_OVERLAY",\n'
        '      "font_kind": "truetype",\n'
        '      "font_name": "Arial",\n'
        '      "bold": true,\n'
        '      "stroke_width_mils": 10,\n'
        '      "is_inverted": true,\n'
        '      "inverted_margin_mils": 10,\n'
        '      "use_inverted_rectangle": true,\n'
        '      "is_frame": true,\n'
        '      "text_justification": "RIGHT_TOP"\n'
        "    }\n"
        "  },\n"
        '  "marker": {\n'
        '    "enabled": true,\n'
        '    "text": "DEBUG PLATE",\n'
        '    "position_mils": [200, 200],\n'
        '    "height_mils": 60,\n'
        '    "layer": "TOP_OVERLAY"\n'
        "  },\n"
        '  "selection": {\n'
        '    "boards": []\n'
        "  }\n"
        "}\n"
    )
