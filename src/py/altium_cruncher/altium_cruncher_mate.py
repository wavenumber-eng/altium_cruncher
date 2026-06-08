"""Mate workflow configuration and MCO generation."""

from __future__ import annotations

import fnmatch
import hashlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from pathlib import Path

from altium_cruncher.altium_cruncher_mco import (
    MCO_SCHEMA,
    JsonObject,
    McoExecutionContext,
    McoExecutionResult,
    execute_mco,
    load_jsonc_file,
    mco_operation,
)
from altium_cruncher.bom_pnp_model import designator_sort_key
from altium_cruncher.altium_cruncher_mate_parts import (
    load_mate_known_parts_manifest,
    manifest_path_for_cache_dir,
    resolve_known_part,
)
from altium_cruncher.altium_cruncher_mate_libraries import (
    MateLibraryScanResult,
    resolve_mate_footprint,
    resolve_mate_symbol,
    scan_mate_libraries,
)
from altium_cruncher.altium_cruncher_mate_graphics import (
    board_outline_geometry,
    board_origin_mils,
    board_outline_bounds_mils,
    build_pcb_board_projection_operations,
    build_pcb_reference_graphics_operations,
    component_pad_geometries,
    pad_height_mils,
    pad_width_mils,
    parse_selection_pad_geometries,
    parse_source_pad_geometries,
    single_inspection_board_origin,
    single_inspection_board_outline,
    transform_source_pad_geometries,
)
from altium_cruncher.altium_cruncher_mate_schematic import (
    schematic_designator_style,
    schematic_grouped_positions,
    schematic_net_label_operation,
    schematic_net_route,
    schematic_wire_operation,
)
from altium_cruncher.altium_cruncher_mate_artifacts import (
    build_mate_artifact_operations,
)
from altium_cruncher.altium_cruncher_mate_labels import (
    MatePcbLabelsConfig,
    PcbNetLabelRequest,
    pcb_net_label_operations,
    pcb_net_label_request,
)
from altium_cruncher.altium_cruncher_mate_defaults import (
    DEFAULT_MATE_BOARD_OUTLINE_MARGIN_MILS,
    default_known_parts_payload as _default_known_parts_payload,
    default_marker_payload as _default_marker_payload,
    default_mate_artifacts_payload as _default_mate_artifacts_payload,
    default_mate_board_projection_payload as _default_mate_board_projection_payload,
    default_mate_designators_payload as _default_mate_designators_payload,
    default_mate_label_placement_payload as _default_mate_label_placement_payload,
    default_mate_label_style_payload as _default_mate_label_style_payload,
    default_mate_output_payload as _default_mate_output_payload,
    default_output_config_payload as _default_output_config_payload,
    default_pcb_designators_payload as _default_pcb_designators_payload,
    default_pcb_labels_payload as _default_pcb_labels_payload,
    default_placement_payload as _default_placement_payload,
    mate_known_parts_payload as _mate_known_parts_payload,
)

LEGACY_MATE_CONFIG_SCHEMA = "wn.altium_cruncher.mate.v1"
MATE_CONFIG_SCHEMA = "wn.pcb_cruncher.mate_config.a0"
MATE_INSPECTION_SCHEMA = "wn.altium_cruncher.mate.inspect.v1"


@dataclass(frozen=True, slots=True)
class MateOutputConfig:
    """Output project settings for a generated mate."""

    output_dir: str
    project_name: str
    schematic_filename: str | None
    schematic_sheet_style: str | None
    board_filename: str | None
    project_filename: str | None
    layer_stack_template: str
    overwrite: bool
    board_outline_mils: JsonObject | None
    board_origin_mils: JsonObject | None


@dataclass(frozen=True, slots=True)
class MateMarkerConfig:
    """Initial marker text used by the first mate orchestration slice."""

    text: str
    position_mils: tuple[float, float]
    height_mils: float
    layer: str


@dataclass(frozen=True, slots=True)
class MateKnownPartsConfig:
    """Known fixture-part cache referenced by a mate config."""

    manifest_path: Path
    cache_dir: Path


@dataclass(frozen=True, slots=True)
class MateLibrariesConfig:
    """Library roots used to resolve mate symbols and footprints by name."""

    roots: tuple[Path, ...]
    recursive: bool


@dataclass(frozen=True, slots=True)
class MatePlacementConfig:
    """Board-side placement transform for projected DUT coordinates."""

    source_mount_side: str
    offset_mils: tuple[float, float]
    mirror_x: bool
    mirror_y: bool
    mirror_origin_mils: tuple[float, float]


@dataclass(frozen=True, slots=True)
class MatePcbDesignatorsConfig:
    """PCB-side component designator normalization settings."""

    enabled: bool
    placement: str
    offset_mils: tuple[float, float]
    width_factor: float
    style: JsonObject


@dataclass(frozen=True, slots=True)
class MateSelectionComponent:
    """Selected DUT component to project into the mate."""

    designator: str
    kind: str
    layer: str
    footprint: str
    x_mils: float
    y_mils: float
    net_name: str | None
    mate_projection_id: str | None = None
    mate_part_role: str | None = None
    mate_component: JsonObject | None = None
    mate_pcb_label: JsonObject | None = None
    mate_reference_graphics: JsonObject | None = None
    source_pad_geometries: tuple[JsonObject, ...] = ()


@dataclass(frozen=True, slots=True)
class MateSelectionPad:
    """Selected DUT free pad/NPTH to project into the mate."""

    designator: str
    kind: str
    x_mils: float
    y_mils: float
    net_name: str | None
    mate_projection_id: str | None = None
    mate_part_role: str | None = None
    mate_component: JsonObject | None = None
    mate_pcb_label: JsonObject | None = None
    mate_reference_graphics: JsonObject | None = None
    source_pad_geometries: tuple[JsonObject, ...] = ()


@dataclass(frozen=True, slots=True)
class MateSelectionBoard:
    """Selected DUT board items to project into the mate."""

    board_key: str
    pcb_path: str
    components: tuple[MateSelectionComponent, ...]
    free_pads: tuple[MateSelectionPad, ...]
    board_outline_mils: JsonObject | None = None
    board_outline: JsonObject | None = None


@dataclass(frozen=True, slots=True)
class MateSelectionConfig:
    """Selected DUT items to project into the mate."""

    boards: tuple[MateSelectionBoard, ...]


@dataclass(frozen=True, slots=True)
class MateConfig:
    """Parsed mate configuration."""

    source_dut: str | None
    output: MateOutputConfig
    marker: MateMarkerConfig | None
    known_parts: MateKnownPartsConfig | None
    libraries: MateLibrariesConfig | None
    placement: MatePlacementConfig
    pcb_labels: MatePcbLabelsConfig
    pcb_designators: MatePcbDesignatorsConfig
    selection: MateSelectionConfig
    board_projection: JsonObject
    artifacts: JsonObject


@dataclass(frozen=True, slots=True)
class _KnownPartOperations:
    placement_operations: list[JsonObject]
    pcb_label_operations: list[JsonObject]


@dataclass(frozen=True, slots=True)
class _ResolvedMatePartTarget:
    target: JsonObject
    part: JsonObject
    designator: str


@dataclass(frozen=True, slots=True)
class MateComponentCandidate:
    """DUT component candidate for mate projection."""

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
class MatePadCandidate:
    """Free pad or NPTH candidate for mate projection."""

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
class MateBoardInspection:
    """Mate source inspection for one PCB document."""

    board_key: str
    pcb_path: str
    board_outline_mils: JsonObject | None
    board_outline: JsonObject | None
    board_origin_mils: JsonObject | None
    components: tuple[MateComponentCandidate, ...]
    free_pads: tuple[MatePadCandidate, ...]

    def to_dict(self) -> JsonObject:
        payload: JsonObject = {
            "board_key": self.board_key,
            "pcb_path": self.pcb_path,
            "components": [candidate.to_dict() for candidate in self.components],
            "free_pads": [candidate.to_dict() for candidate in self.free_pads],
        }
        _add_optional(payload, "board_outline_mils", self.board_outline_mils)
        _add_optional(payload, "board_outline", self.board_outline)
        _add_optional(payload, "board_origin_mils", self.board_origin_mils)
        return payload


def load_mate_config(path: Path | str) -> MateConfig:
    """Load a mate JSONC config file."""
    input_path = Path(path).resolve()
    payload = load_jsonc_file(input_path)
    return parse_mate_config(payload, base_dir=input_path.parent)


def parse_mate_config(
    payload: object,
    *,
    base_dir: Path | str | None = None,
) -> MateConfig:
    """Parse a mate config payload."""
    root = _json_object(payload, "mate config root")
    schema = root.get("schema")
    if schema == MATE_CONFIG_SCHEMA:
        return _parse_mate_config(root, base_dir=base_dir)
    if schema not in {None, LEGACY_MATE_CONFIG_SCHEMA, MATE_CONFIG_SCHEMA}:
        raise ValueError(f"Unsupported mate config schema: {schema!r}")
    source = _section(root, "source")
    return MateConfig(
        source_dut=_optional_string(source, "dut", None),
        output=_parse_output_config(_section(root, "output")),
        marker=_parse_marker_config(_section(root, "marker")),
        known_parts=_parse_known_parts_config(
            _optional_section(root, "known_parts"),
            base_dir=base_dir,
        ),
        libraries=_parse_libraries_config(
            _optional_section(root, "libraries"),
            base_dir=base_dir,
            default_to_base_dir=False,
        ),
        placement=_parse_placement_config(_section(root, "placement")),
        pcb_labels=_parse_pcb_labels_config(_optional_section(root, "pcb_labels")),
        pcb_designators=_parse_pcb_designators_config(
            _optional_section(root, "pcb_designators"),
            default_enabled=False,
        ),
        selection=_parse_selection_config(_section(root, "selection")),
        board_projection=_optional_section(root, "board_projection") or {},
        artifacts=_section(root, "artifacts"),
    )


def _parse_mate_config(
    root: Mapping[str, object],
    *,
    base_dir: Path | str | None,
) -> MateConfig:
    source = _section(root, "source")
    source_board = _optional_string(source, "board", None)
    inspection = _mate_source_inspection(root, base_dir=base_dir)
    return MateConfig(
        source_dut=source_board,
        output=_parse_mate_output_config(_section(root, "output"), inspection),
        marker=None,
        known_parts=_parse_known_parts_config(
            _optional_section(root, "known_parts"),
            base_dir=base_dir,
        ),
        libraries=_parse_libraries_config(
            _optional_section(root, "libraries"),
            base_dir=base_dir,
            default_to_base_dir=True,
        ),
        placement=_default_mate_placement_config(),
        pcb_labels=_parse_mate_pcb_labels_config(root),
        pcb_designators=_parse_pcb_designators_config(
            _optional_section(root, "pcb_designators"),
            default_enabled=True,
        ),
        selection=_selection_from_mate_inspection(root, inspection),
        board_projection=_section(root, "board_projection"),
        artifacts=_section(root, "artifacts"),
    )


def build_mate_mco(config: MateConfig) -> JsonObject:
    """Build the executable MCO payload for a mate config."""
    operations: list[JsonObject] = _project_bootstrap_operations(config.output)
    marker = config.marker
    if marker is not None:
        operations.append(_pcb_marker_operation(config.output, marker))
    library_copy_operations = _known_part_library_copy_operations(config)
    operations.extend(library_copy_operations)
    operations.extend(_known_part_project_document_operations(config))
    known_part_operations = _known_part_operations(config)
    placement_operations = known_part_operations.placement_operations
    schdoc_operations = _operations_with_prefix(placement_operations, "schdoc.")
    pcbdoc_operations = [
        operation
        for operation in placement_operations
        if not str(operation.get("op", "")).startswith("schdoc.")
    ]
    board_projection_operations = _board_projection_operations(config)
    artifact_operations = build_mate_artifact_operations(config)
    operations.extend(schdoc_operations)
    operations.extend(pcbdoc_operations)
    operations.extend(board_projection_operations)
    operations.extend(artifact_operations)
    if placement_operations or board_projection_operations or artifact_operations:
        operations.append(_mate_user_union_operation(config.output))
    operations.extend(known_part_operations.pcb_label_operations)
    return {"schema": MCO_SCHEMA, "operations": operations}


def write_mate_config_template(
    path: Path | str,
    *,
    overwrite: bool = False,
    source_board: Path | str | None = None,
) -> Path:
    """Write an editable mate JSONC template."""
    output_path = Path(path)
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"Mate config already exists: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        _mate_template_text(source_board=source_board),
        encoding="utf-8",
    )
    return output_path.resolve()


def build_legacy_mate_seed_config(
    input_file: Path | str,
    *,
    pcbdoc_selector: Path | str | None = None,
    project_context: str | None = "auto",
) -> JsonObject:
    """Build an editable mate config seeded from DUT inspection."""
    inspection = inspect_mate_source(
        input_file,
        pcbdoc_selector=pcbdoc_selector,
        project_context=project_context,
    )
    return {
        "schema": LEGACY_MATE_CONFIG_SCHEMA,
        "source": {"dut": str(Path(input_file).resolve())},
        "output": _default_output_config_payload(),
        "known_parts": _default_known_parts_payload(),
        "placement": _default_placement_payload(),
        "pcb_labels": _default_pcb_labels_payload(),
        "pcb_designators": _default_pcb_designators_payload(),
        "marker": _default_marker_payload(),
        "selection": _selection_from_inspection(inspection),
    }


def build_mate_seed_config(
    input_file: Path | str,
    *,
    known_parts_manifest: Path | str | None = None,
    pcbdoc_selector: Path | str | None = None,
    project_context: str | None = "auto",
) -> JsonObject:
    """Build a draft mate config seeded from DUT inspection."""
    inspection = inspect_mate_source(
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
        "pcb_designators": _default_mate_designators_payload(),
        "board_projection": _default_mate_board_projection_payload(),
        "artifacts": _default_mate_artifacts_payload(),
    }


def write_legacy_mate_seed_config(
    input_file: Path | str,
    path: Path | str,
    *,
    overwrite: bool = False,
    pcbdoc_selector: Path | str | None = None,
    project_context: str | None = "auto",
) -> Path:
    """Write an editable mate config seeded from a DUT PCB input."""
    output_path = Path(path)
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"Mate config already exists: {output_path}")
    payload = build_legacy_mate_seed_config(
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


def write_mate_seed_config(
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
        raise FileExistsError(f"Mate config already exists: {output_path}")
    payload = build_mate_seed_config(
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


def write_mate_mco(
    config: MateConfig,
    path: Path | str,
    *,
    overwrite: bool = False,
) -> Path:
    """Write the generated mate MCO payload."""
    output_path = Path(path)
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"Mate MCO already exists: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(build_mate_mco(config), indent=2) + "\n",
        encoding="utf-8",
    )
    return output_path.resolve()


def execute_mate_config(
    path: Path | str,
    *,
    dry_run: bool = False,
) -> McoExecutionResult:
    """Execute a mate config through the MCO engine."""
    config_path = Path(path).resolve()
    config = load_mate_config(config_path)
    context = McoExecutionContext(work_dir=config_path.parent, dry_run=dry_run)
    return execute_mco(build_mate_mco(config), context)


def inspect_mate_source(
    input_file: Path | str,
    *,
    pcbdoc_selector: Path | str | None = None,
    project_context: str | None = "auto",
) -> JsonObject:
    """Inspect a DUT PCB input and report mate projection candidates."""
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
        inspect_pcbdoc_for_mate(
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
        "schema": MATE_INSPECTION_SCHEMA,
        "source": str(input_path),
        "source_tag": source_tag,
        "boards": [board.to_dict() for board in boards],
    }


def inspect_pcbdoc_for_mate(
    board_key: str,
    pcbdoc: object,
    pcb_path: Path | str,
) -> MateBoardInspection:
    """Inspect one loaded PcbDoc object for likely mate candidates."""
    return MateBoardInspection(
        board_key=board_key,
        pcb_path=str(Path(pcb_path)),
        board_outline_mils=board_outline_bounds_mils(pcbdoc),
        board_outline=board_outline_geometry(pcbdoc),
        board_origin_mils=board_origin_mils(pcbdoc),
        components=tuple(_component_candidates(pcbdoc)),
        free_pads=tuple(_free_pad_candidates(pcbdoc)),
    )


def _parse_output_config(raw: Mapping[str, object]) -> MateOutputConfig:
    output_dir = _optional_string(raw, "output_dir", "output/mate")
    project_name = _optional_string(raw, "project_name", "mate")
    layer_stack_template = _optional_string(raw, "layer_stack_template", "2-layer")
    return MateOutputConfig(
        output_dir=output_dir or "output/mate",
        project_name=project_name or "mate",
        schematic_filename=_optional_string(raw, "schematic_filename", None),
        schematic_sheet_style=_optional_string(raw, "schematic_sheet_style", "D"),
        board_filename=_optional_string(raw, "board_filename", None),
        project_filename=_optional_string(raw, "project_filename", None),
        layer_stack_template=layer_stack_template or "2-layer",
        overwrite=_optional_bool(raw, "overwrite", False),
        board_outline_mils=_optional_number_object(
            raw,
            "board_outline_mils",
            ("left", "bottom", "right", "top"),
        ),
        board_origin_mils=_optional_number_object(
            raw,
            "board_origin_mils",
            ("x", "y"),
        ),
    )


def _parse_mate_output_config(
    raw: Mapping[str, object],
    inspection: Mapping[str, object],
) -> MateOutputConfig:
    output = _parse_output_config(raw)
    origin = _optional_string(raw, "origin", "preserve_source")
    source_outline = single_inspection_board_outline(inspection)
    outline = output.board_outline_mils
    if outline is None and (origin == "preserve_source" or "board_outline" in raw):
        outline = _resolve_mate_output_board_outline(raw, source_outline)
    origin_mils = output.board_origin_mils
    if origin_mils is None and origin == "preserve_source":
        origin_mils = single_inspection_board_origin(inspection)
    return replace(
        output,
        board_outline_mils=outline,
        board_origin_mils=origin_mils,
    )


def _resolve_mate_output_board_outline(
    raw: Mapping[str, object],
    source_outline: JsonObject | None,
) -> JsonObject | None:
    outline_config = _optional_section(raw, "board_outline") or {}
    mode = _optional_string(
        outline_config,
        "mode",
        "source_bounds_with_margin",
    )
    if source_outline is None:
        return None
    if mode in {"source_bounds", "match_source_bounds", "match_bounds"}:
        return dict(source_outline)
    if mode in {
        "source_bounds_with_margin",
        "source_bounds_plus_margin",
        "padded_rectangle",
        "padded_source_bounds",
    }:
        return _expand_board_outline_mils(
            source_outline,
            _board_outline_margin_mils(outline_config),
        )
    if mode in {"match_shape", "source_shape"}:
        raise ValueError(
            "Mate output.board_outline.mode='match_shape' needs an "
            "arbitrary-outline project skeleton; use 'source_bounds' or "
            "'source_bounds_with_margin' for the current rectangular skeleton"
        )
    raise ValueError(
        "Mate output.board_outline.mode must be 'source_bounds' or "
        "'source_bounds_with_margin'"
    )


def _board_outline_margin_mils(
    raw: Mapping[str, object],
) -> tuple[float, float, float, float]:
    value = raw.get("margin_mils", DEFAULT_MATE_BOARD_OUTLINE_MARGIN_MILS)
    if isinstance(value, int | float) and not isinstance(value, bool):
        margin = float(value)
        if margin < 0.0:
            raise ValueError(
                "Mate output.board_outline.margin_mils must be non-negative"
            )
        return (margin, margin, margin, margin)
    if isinstance(value, dict):
        margin = (
            _optional_margin_side_mils(value, "left"),
            _optional_margin_side_mils(value, "bottom"),
            _optional_margin_side_mils(value, "right"),
            _optional_margin_side_mils(value, "top"),
        )
        if any(side < 0.0 for side in margin):
            raise ValueError(
                "Mate output.board_outline.margin_mils sides must be "
                "non-negative"
            )
        return margin
    raise ValueError(
        "Mate output.board_outline.margin_mils must be a number or an object"
    )


def _optional_margin_side_mils(raw: Mapping[str, object], name: str) -> float:
    value = raw.get(name, 0.0)
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise ValueError(
            f"Mate output.board_outline.margin_mils.{name} must be numeric"
        )
    return float(value)


def _expand_board_outline_mils(
    outline: Mapping[str, object],
    margin_mils: tuple[float, float, float, float],
) -> JsonObject:
    left_margin, bottom_margin, right_margin, top_margin = margin_mils
    return {
        "left": _number_field(
            outline,
            "source board_outline_mils",
            "left",
        )
        - left_margin,
        "bottom": _number_field(
            outline,
            "source board_outline_mils",
            "bottom",
        )
        - bottom_margin,
        "right": _number_field(
            outline,
            "source board_outline_mils",
            "right",
        )
        + right_margin,
        "top": _number_field(
            outline,
            "source board_outline_mils",
            "top",
        )
        + top_margin,
    }


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
        "board_outline_mils": _optional_dict_copy(board, "board_outline_mils"),
        "board_outline": _optional_dict_copy(board, "board_outline"),
    }


def _optional_dict_copy(payload: Mapping[str, object], name: str) -> JsonObject | None:
    value = payload.get(name)
    if isinstance(value, dict):
        return dict(value)
    return None


def _list_field(payload: Mapping[str, object], name: str) -> list[object]:
    value = payload.get(name, [])
    return list(value) if isinstance(value, list) else []


def _component_candidates(pcbdoc: object) -> list[MateComponentCandidate]:
    candidates: list[MateComponentCandidate] = []
    components = list(getattr(pcbdoc, "components", []) or [])
    for index, component in enumerate(components):
        designator = str(getattr(component, "designator", "") or "")
        kind = _component_candidate_kind(designator)
        if kind is None:
            continue
        x_mils, y_mils = _component_position_mils(pcbdoc, index, component)
        candidates.append(
            MateComponentCandidate(
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


def _free_pad_candidates(pcbdoc: object) -> list[MatePadCandidate]:
    candidates: list[MatePadCandidate] = []
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
        x_mils, y_mils = position_fn(index, origin_relative=False)
        return (float(x_mils), float(y_mils))
    except Exception:
        x_fn = getattr(component, "get_x_mils")
        y_fn = getattr(component, "get_y_mils")
        return (float(x_fn()), float(y_fn()))


def _is_free_pad(pad: object) -> bool:
    component_index = getattr(pad, "component_index", None)
    return component_index is None or int(component_index) == 0xFFFF


def _pad_candidate(pcbdoc: object, pad: object) -> MatePadCandidate:
    hole_size = _float_attr(pad, "hole_size_mils")
    plated = _bool_attr(pad, "is_plated")
    return MatePadCandidate(
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


def _parse_marker_config(raw: Mapping[str, object]) -> MateMarkerConfig | None:
    enabled = _optional_bool(raw, "enabled", True)
    if not enabled:
        return None
    marker_text = _optional_string(raw, "text", "MATE")
    marker_layer = _optional_string(raw, "layer", "TOP_OVERLAY")
    return MateMarkerConfig(
        text=marker_text or "MATE",
        position_mils=_required_point(raw, "position_mils", default=(200.0, 200.0)),
        height_mils=_optional_float(raw, "height_mils", 60.0),
        layer=marker_layer or "TOP_OVERLAY",
    )


def _parse_known_parts_config(
    raw: Mapping[str, object] | None,
    *,
    base_dir: Path | str | None,
) -> MateKnownPartsConfig | None:
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
    return MateKnownPartsConfig(
        manifest_path=manifest_path,
        cache_dir=resolved_cache_dir or manifest_path.parent,
    )


def _parse_libraries_config(
    raw: Mapping[str, object] | None,
    *,
    base_dir: Path | str | None,
    default_to_base_dir: bool,
) -> MateLibrariesConfig | None:
    base_path = Path(base_dir).resolve() if base_dir is not None else Path.cwd()
    if raw is None:
        if not default_to_base_dir:
            return None
        return MateLibrariesConfig(roots=(base_path,), recursive=True)
    recursive = _optional_bool(raw, "recursive", True)
    root_values = raw.get("roots")
    if root_values is None:
        roots = [base_path]
    elif isinstance(root_values, str):
        roots = [root_values]
    elif isinstance(root_values, list):
        roots = []
        for root_value in root_values:
            if not isinstance(root_value, str) or not root_value:
                raise ValueError(
                    "Mate libraries.roots must contain non-empty strings"
                )
            roots.append(root_value)
    else:
        raise ValueError("Mate libraries.roots must be a string or array")
    return MateLibrariesConfig(
        roots=tuple(_resolve_config_path(root, base_path) for root in roots),
        recursive=recursive,
    )


def _parse_placement_config(raw: Mapping[str, object]) -> MatePlacementConfig:
    mount_side = _optional_string(raw, "source_mount_side", "bottom")
    if mount_side not in {"bottom", "top"}:
        raise ValueError("Mate placement.source_mount_side must be bottom or top")
    return MatePlacementConfig(
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
) -> MatePcbLabelsConfig:
    if raw is None:
        raw = {}
    enabled = _optional_bool(raw, "enabled", False)
    side = _optional_string(raw, "side", "right")
    if side not in {"left", "right", "board_left", "board_right"}:
        raise ValueError(
            "Mate pcb_labels.side must be left, right, board_left, or board_right"
        )
    return MatePcbLabelsConfig(
        enabled=enabled,
        side=side,
        offset_mils=_required_point(raw, "offset_mils", default=(120.0, 0.0)),
        box_size_mils=_optional_point(raw, "box_size_mils"),
        center_box_on_target=_optional_bool(raw, "center_box_on_target", True),
        row_spacing_mils=_optional_float_or_none(raw, "row_spacing_mils"),
        column_spacing_mils=_optional_float_or_none(raw, "column_spacing_mils"),
        auto_width_padding_mils=_optional_float_or_none(
            raw,
            "auto_width_padding_mils",
        ),
        style=_section(raw, "style"),
    )


def _parse_pcb_designators_config(
    raw: Mapping[str, object] | None,
    *,
    default_enabled: bool,
) -> MatePcbDesignatorsConfig:
    if raw is None:
        raw = {}
    enabled = _optional_bool(raw, "enabled", default_enabled)
    placement = _optional_string(raw, "placement", "above_component")
    if placement != "above_component":
        raise ValueError(
            "Mate pcb_designators.placement must be above_component"
        )
    return MatePcbDesignatorsConfig(
        enabled=enabled,
        placement=placement,
        offset_mils=_required_point(raw, "offset_mils", default=(0.0, 10.0)),
        width_factor=_optional_float(raw, "width_factor", 0.6),
        style=_section(raw, "style"),
    )


def _default_mate_placement_config() -> MatePlacementConfig:
    return MatePlacementConfig(
        source_mount_side="bottom",
        offset_mils=(0.0, 0.0),
        mirror_x=False,
        mirror_y=False,
        mirror_origin_mils=(0.0, 0.0),
    )


def _parse_mate_pcb_labels_config(
    _root: Mapping[str, object],
) -> MatePcbLabelsConfig:
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
    return inspect_mate_source(
        input_file,
        pcbdoc_selector=_optional_string(source, "pcbdoc", None),
        project_context=_optional_string(source, "project_context", "auto"),
    )


def _selection_from_mate_inspection(
    root: Mapping[str, object],
    inspection: Mapping[str, object],
) -> MateSelectionConfig:
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
                "board_outline_mils": _optional_dict_copy(
                    board,
                    "board_outline_mils",
                ),
                "board_outline": _optional_dict_copy(board, "board_outline"),
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
    action = _projection_mate_component_action(projection)
    if action is None:
        return None
    part = action.get("part")
    if part is None:
        return None
    if not isinstance(part, str) or not part:
        raise ValueError("Mate projection mate_component.part must be a string")
    return part


def _projection_mate_component_action(
    projection: Mapping[str, object],
) -> JsonObject | None:
    for action in _list_field(projection, "actions"):
        if not isinstance(action, dict) or action.get("kind") != "mate_component":
            continue
        return dict(action)
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
        raw["enabled"] = _optional_bool(raw, "enabled", True)
        return raw
    if _projection_requests_mate_component(projection):
        return _default_mate_reference_graphics_payload()
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
                    "mate_component",
                    _projection_mate_component_action(projection),
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
    seen: set[tuple[object, ...]] = set()
    for projection in projections:
        pad_selector = _projection_selector(projection, "free_pads")
        if pad_selector is None:
            continue
        for pad in _list_field(board, "free_pads"):
            if not isinstance(pad, dict):
                continue
            selection_key = _free_pad_selection_key(pad)
            if selection_key in seen:
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
                    "mate_component",
                    _projection_mate_component_action(projection),
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
                seen.add(selection_key)
    return selected


def _free_pad_selection_key(pad: Mapping[str, object]) -> tuple[object, ...]:
    return (
        str(pad.get("designator", "") or "").upper(),
        _selection_key_number(pad.get("x_mils")),
        _selection_key_number(pad.get("y_mils")),
        _selection_key_number(pad.get("hole_size_mils")),
        _selection_key_number(pad.get("width_mils")),
        _selection_key_number(pad.get("height_mils")),
        pad.get("layer"),
        pad.get("plated"),
    )


def _selection_key_number(value: object) -> float | object:
    return round(float(value), 6) if isinstance(value, int | float) else value


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


def _parse_selection_config(raw: Mapping[str, object]) -> MateSelectionConfig:
    boards = raw.get("boards", [])
    if not isinstance(boards, list):
        raise ValueError("Mate selection.boards must be an array")
    return MateSelectionConfig(
        boards=tuple(
            _parse_selection_board(board)
            for board in boards
            if isinstance(board, dict)
        )
    )


def _parse_selection_board(raw: Mapping[str, object]) -> MateSelectionBoard:
    return MateSelectionBoard(
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
        board_outline_mils=_optional_number_object(
            raw,
            "board_outline_mils",
            ("left", "bottom", "right", "top"),
        ),
        board_outline=_optional_section(raw, "board_outline"),
    )


def _parse_selection_component(
    raw: Mapping[str, object],
) -> MateSelectionComponent:
    return MateSelectionComponent(
        designator=str(raw.get("designator", "") or ""),
        kind=str(raw.get("kind", "") or ""),
        layer=str(raw.get("layer", "") or ""),
        footprint=str(raw.get("footprint", "") or ""),
        x_mils=_number_like(raw, "x_mils"),
        y_mils=_number_like(raw, "y_mils"),
        net_name=_optional_string(raw, "net_name", None),
        mate_projection_id=_optional_string(raw, "mate_projection_id", None),
        mate_part_role=_optional_string(raw, "mate_part_role", None),
        mate_component=_optional_section(raw, "mate_component"),
        mate_pcb_label=_optional_section(raw, "mate_pcb_label"),
        mate_reference_graphics=_optional_section(raw, "mate_reference_graphics"),
        source_pad_geometries=parse_source_pad_geometries(raw),
    )


def _parse_selection_pad(raw: Mapping[str, object]) -> MateSelectionPad:
    return MateSelectionPad(
        designator=str(raw.get("designator", "") or ""),
        kind=str(raw.get("kind", "") or ""),
        x_mils=_number_like(raw, "x_mils"),
        y_mils=_number_like(raw, "y_mils"),
        net_name=_optional_string(raw, "net_name", None),
        mate_projection_id=_optional_string(raw, "mate_projection_id", None),
        mate_part_role=_optional_string(raw, "mate_part_role", None),
        mate_component=_optional_section(raw, "mate_component"),
        mate_pcb_label=_optional_section(raw, "mate_pcb_label"),
        mate_reference_graphics=_optional_section(raw, "mate_reference_graphics"),
        source_pad_geometries=parse_selection_pad_geometries(raw),
    )


def _project_bootstrap_operations(output: MateOutputConfig) -> list[JsonObject]:
    project_file = _output_file(output.output_dir, _project_filename(output))
    schematic_file = _output_file(output.output_dir, _schematic_filename(output))
    board_file = _output_file(output.output_dir, _board_filename(output))
    create_board_args: JsonObject = {
        "file": board_file,
        "layer_stack_template": output.layer_stack_template,
        "overwrite": output.overwrite,
    }
    _add_optional(create_board_args, "board_outline_mils", output.board_outline_mils)
    _add_optional(create_board_args, "board_origin_mils", output.board_origin_mils)
    return [
        mco_operation(
            "project.create",
            "create_mate_project",
            "Create mate project",
            {
                "file": project_file,
                "name": output.project_name,
                "overwrite": output.overwrite,
            },
        ),
        mco_operation(
            "schdoc.create",
            "create_mate_schematic",
            "Create mate schematic",
            {
                "file": schematic_file,
                "sheet_style": output.schematic_sheet_style,
                "overwrite": output.overwrite,
            },
        ),
        mco_operation(
            "pcbdoc.create",
            "create_mate_board",
            "Create mate board",
            create_board_args,
        ),
        mco_operation(
            "project.add_document",
            "add_mate_schematic_to_project",
            "Add mate schematic to project",
            {
                "file": project_file,
                "document": _schematic_filename(output),
            },
        ),
        mco_operation(
            "project.add_document",
            "add_mate_board_to_project",
            "Add mate board to project",
            {
                "file": project_file,
                "document": _board_filename(output),
            },
        ),
    ]


def _pcb_marker_operation(
    output: MateOutputConfig,
    marker: MateMarkerConfig,
) -> JsonObject:
    return mco_operation(
        "pcbdoc.add_text",
        "add_mate_marker",
        "Add mate PCB marker text",
        {
            "file": _output_file(output.output_dir, _board_filename(output)),
            "overwrite": True,
            "text": marker.text,
            "position_mils": list(marker.position_mils),
            "height_mils": marker.height_mils,
            "layer": marker.layer,
        },
    )


def _known_part_operations(config: MateConfig) -> _KnownPartOperations:
    resolved_targets = _resolved_mate_targets(config)
    if not resolved_targets:
        return _KnownPartOperations([], [])
    operations: list[JsonObject] = []
    pcb_label_requests: list[PcbNetLabelRequest] = []
    board_label_column_indices: dict[str, int] = {}
    board_label_rows: dict[str, int] = {}
    placed_designators: list[str] = []
    schematic_positions = schematic_grouped_positions(
        [_part_string(resolved.part, "symbol_name") for resolved in resolved_targets]
    )
    for resolved, schematic_position in zip(
        resolved_targets,
        schematic_positions,
        strict=True,
    ):
        target = resolved.target
        part = resolved.part
        designator = resolved.designator
        operations.append(
            _schematic_part_operation(
                config.output,
                part,
                target,
                designator,
                schematic_position,
            )
        )
        schematic_file = _output_file(config.output.output_dir, _schematic_filename(config.output))
        net_name = _target_optional_string(target, "net_name")
        net_route = schematic_net_route(
            symbol_library_path=_part_source_file(part, "symbol_library"),
            symbol_name=_part_string(part, "symbol_name"),
            signal_pin_designator=_part_optional_string(part, "signal_pad_designator"),
            component_position_mils=schematic_position,
            net_name=net_name,
        )
        if net_route is not None:
            operations.append(
                schematic_wire_operation(
                    schematic_file=schematic_file,
                    designator=designator,
                    route=net_route,
                )
            )
            operations.append(
                schematic_net_label_operation(
                    schematic_file=schematic_file,
                    designator=designator,
                    net_name=str(net_name),
                    route=net_route,
                )
            )
        operations.append(
            _pcb_part_operation(
                config.output,
                part,
                target,
                designator,
            )
        )
        placed_designators.append(designator)
        target_labels = _target_pcb_labels_config(config.pcb_labels, target)
        pcb_label_request = pcb_net_label_request(
            target_labels,
            target,
            designator,
            board_label_column_indices=board_label_column_indices,
            board_label_rows=board_label_rows,
        )
        if pcb_label_request is not None:
            pcb_label_requests.append(pcb_label_request)
        operations.extend(
            build_pcb_reference_graphics_operations(
                output_dir=config.output.output_dir,
                board_filename=_board_filename(config.output),
                target=target,
                designator=designator,
            )
        )
    designators_operation = _pcb_designator_arrangement_operation(
        config.output,
        config.pcb_designators,
        placed_designators,
    )
    if designators_operation is not None:
        operations.append(designators_operation)
    return _KnownPartOperations(
        operations,
        pcb_net_label_operations(
            board_file=_output_file(config.output.output_dir, _board_filename(config.output)),
            board_outline_mils=config.output.board_outline_mils,
            requests=pcb_label_requests,
        ),
    )


def _sort_known_part_targets_by_group_and_designator(
    resolved_targets: list[_ResolvedMatePartTarget],
) -> list[_ResolvedMatePartTarget]:
    group_order: dict[str, int] = {}
    for resolved in resolved_targets:
        group_key = _part_string(resolved.part, "symbol_name")
        group_order.setdefault(group_key, len(group_order))
    return sorted(
        resolved_targets,
        key=lambda item: (
            group_order[_part_string(item.part, "symbol_name")],
            designator_sort_key(item.designator),
        ),
    )


def _board_projection_operations(config: MateConfig) -> list[JsonObject]:
    return build_pcb_board_projection_operations(
        output_dir=config.output.output_dir,
        board_filename=_board_filename(config.output),
        board_projection=config.board_projection,
        selection=config.selection,
    )


def _known_part_project_documents(config: MateConfig) -> list[str]:
    return [
        reference["project_path"]
        for reference in _known_part_library_references(config)
    ]


def _known_part_project_document_operations(config: MateConfig) -> list[JsonObject]:
    project_file = _output_file(config.output.output_dir, _project_filename(config.output))
    return [
        mco_operation(
            "project.add_document",
            f"add_{_safe_id(project_path)}_to_project",
            f"Add mate library {Path(project_path).name} to project",
            {
                "file": project_file,
                "document": project_path,
            },
        )
        for project_path in _known_part_project_documents(config)
    ]


def _known_part_library_copy_operations(config: MateConfig) -> list[JsonObject]:
    operations: list[JsonObject] = []
    for reference in _known_part_library_references(config):
        project_path = reference["project_path"]
        source = reference["source"]
        operations.append(
            mco_operation(
                "file.copy",
                f"copy_{_safe_id(project_path)}",
                f"Copy mate library {Path(project_path).name}",
                {
                    "source": source,
                    "destination": _output_file(config.output.output_dir, project_path),
                    "overwrite": config.output.overwrite,
                },
            )
        )
    return operations


def _known_part_library_references(config: MateConfig) -> list[dict[str, str]]:
    references: dict[str, str] = {}
    for resolved in _resolved_mate_targets(config):
        part = resolved.part
        for field in ("symbol_library", "footprint_library"):
            project_path = _known_part_project_library_path(part, field)
            references[project_path] = _part_source_file(part, field)
    return [
        {"project_path": project_path, "source": references[project_path]}
        for project_path in sorted(references)
    ]


def _resolved_mate_targets(config: MateConfig) -> list[_ResolvedMatePartTarget]:
    targets = _placement_targets(config.selection, config.placement)
    if not targets:
        return []
    manifest = _loaded_known_parts_manifest(config)
    library_scan = _loaded_mate_library_scan(config)
    used_designators: set[str] = set()
    free_counts: dict[str, int] = {}
    resolved_targets: list[_ResolvedMatePartTarget] = []
    for target in targets:
        part = _resolve_mate_part(
            config,
            target,
            manifest=manifest,
            library_scan=library_scan,
        )
        designator = _projected_designator(
            target,
            part,
            manifest or {},
            used_designators=used_designators,
            free_counts=free_counts,
        )
        resolved_targets.append(
            _ResolvedMatePartTarget(
                target=target,
                part=part,
                designator=designator,
            )
        )
    return _sort_known_part_targets_by_group_and_designator(resolved_targets)


def _loaded_known_parts_manifest(config: MateConfig) -> JsonObject | None:
    known_parts = config.known_parts
    if known_parts is None:
        return None
    return load_mate_known_parts_manifest(known_parts.manifest_path)


def _loaded_mate_library_scan(config: MateConfig) -> MateLibraryScanResult | None:
    libraries = config.libraries
    if libraries is None:
        return None
    return scan_mate_libraries(libraries.roots, recursive=libraries.recursive)


def _resolve_mate_part(
    config: MateConfig,
    target: Mapping[str, object],
    *,
    manifest: Mapping[str, object] | None,
    library_scan: MateLibraryScanResult | None,
) -> JsonObject:
    action = _target_mate_component_action(target)
    if action is not None and _action_uses_named_libraries(action):
        if library_scan is None:
            raise ValueError(
                "Mate config needs libraries.roots when mate_component uses "
                "symbol_name or footprint_name"
            )
        return _resolve_named_mate_part(target, action, library_scan)
    role = _target_optional_string(target, "mate_part_role")
    if manifest is not None:
        if config.known_parts is None:
            raise ValueError("Internal mate known-parts config is missing")
        target_kind = str(target.get("kind", "") or "")
        part = dict(resolve_known_part(manifest, target_kind, role=role))
        part["symbol_source_library"] = _known_part_file(
            config.known_parts,
            part,
            "symbol_library",
        )
        part["footprint_source_library"] = _known_part_file(
            config.known_parts,
            part,
            "footprint_library",
        )
        return part
    raise ValueError(
        "Mate component action must provide symbol_name and footprint_name, "
        "or the config must reference a legacy known_parts manifest"
    )


def _target_mate_component_action(target: Mapping[str, object]) -> JsonObject | None:
    raw = target.get("mate_component")
    if raw is None:
        return None
    if not isinstance(raw, dict):
        raise ValueError("Mate target mate_component must be an object")
    return dict(raw)


def _action_uses_named_libraries(action: Mapping[str, object]) -> bool:
    return "symbol_name" in action or "footprint_name" in action


def _resolve_named_mate_part(
    target: Mapping[str, object],
    action: Mapping[str, object],
    library_scan: MateLibraryScanResult,
) -> JsonObject:
    symbol_name = _action_required_string(action, "symbol_name")
    footprint_name = _action_required_string(action, "footprint_name")
    symbol = resolve_mate_symbol(library_scan, symbol_name)
    footprint = resolve_mate_footprint(library_scan, footprint_name)
    return {
        "role": _action_optional_string(action, "role")
        or _action_optional_string(action, "part")
        or _safe_id(f"{symbol_name}_{footprint_name}"),
        "description": _action_optional_string(action, "description") or "",
        "symbol_name": symbol_name,
        "symbol_library": f"schlib/{symbol.library_path.name}",
        "symbol_source_library": symbol.library_path.as_posix(),
        "footprint_name": footprint_name,
        "footprint_library": f"pcblib/{footprint.library_path.name}",
        "footprint_source_library": footprint.library_path.as_posix(),
        "target_kinds": [str(target.get("kind", "") or "")],
        "designator_prefix": _action_optional_string(action, "designator_prefix")
        or _default_mate_designator_prefix(target),
        "signal_pad_designator": _action_optional_string(
            action,
            "signal_pad_designator",
        ),
    }


def _action_required_string(
    action: Mapping[str, object],
    name: str,
) -> str:
    value = action.get(name)
    if not isinstance(value, str) or not value:
        raise ValueError(f"Mate mate_component.{name} must be a non-empty string")
    return value


def _action_optional_string(
    action: Mapping[str, object],
    name: str,
) -> str | None:
    value = action.get(name)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"Mate mate_component.{name} must be a string")
    return value or None


def _default_mate_designator_prefix(target: Mapping[str, object]) -> str:
    kind = str(target.get("kind", "") or "").strip().lower()
    if kind == "free_npth":
        return "P"
    source = str(target.get("source_designator", "") or "").strip()
    prefix, _number = _split_designator_number(source.upper())
    return prefix or "X"


def _placement_targets(
    selection: MateSelectionConfig,
    placement: MatePlacementConfig | None = None,
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
                    "mate_component": component.mate_component,
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
                    "mate_component": pad.mate_component,
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
    placement: MatePlacementConfig | None,
) -> tuple[float, float]:
    if placement is None:
        return (x_mils, y_mils)
    mirror_origin_x, mirror_origin_y = placement.mirror_origin_mils
    transformed_x = 2.0 * mirror_origin_x - x_mils if placement.mirror_x else x_mils
    transformed_y = 2.0 * mirror_origin_y - y_mils if placement.mirror_y else y_mils
    offset_x, offset_y = placement.offset_mils
    return (transformed_x + offset_x, transformed_y + offset_y)


def _schematic_part_operation(
    output: MateOutputConfig,
    part: Mapping[str, object],
    target: Mapping[str, object],
    designator: str,
    position_mils: tuple[float, float],
) -> JsonObject:
    symbol_name = _part_string(part, "symbol_name")
    footprint_name = _part_string(part, "footprint_name")
    return mco_operation(
        "schdoc.add_component",
        f"add_{_safe_id(designator)}_symbol",
        f"Add mate schematic component {designator}",
        {
            "file": _output_file(output.output_dir, _schematic_filename(output)),
            "overwrite": True,
            "library": _copied_known_part_file(output, part, "symbol_library"),
            "symbol": symbol_name,
            "designator": designator,
            "unique_id": _component_link_unique_id(output, target, designator),
            "position_mils": list(position_mils),
            "design_item_id": symbol_name,
            "footprint_model": footprint_name,
            "footprint_library": footprint_name,
            "parameters": _mate_component_parameters(target, part),
            "designator_style": schematic_designator_style(
                designator,
                position_mils,
            ),
        },
    )


def _pcb_part_operation(
    output: MateOutputConfig,
    part: Mapping[str, object],
    target: Mapping[str, object],
    designator: str,
) -> JsonObject:
    footprint_library = _copied_known_part_file(output, part, "footprint_library")
    symbol_name = _part_string(part, "symbol_name")
    symbol_library = Path(_known_part_project_library_path(part, "symbol_library"))
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
        "source_unique_id": _component_link_unique_id(output, target, designator),
        "source_hierarchical_path": output.project_name,
        "source_component_library": symbol_library.name,
        "source_lib_reference": symbol_name,
        "source_description": _mate_part_symbol_description(part),
        "comment_text": "*",
        "component_parameters": _mate_component_parameters(target, part),
    }
    pad_nets = _mate_pad_nets(target, part)
    if pad_nets:
        args["pad_nets"] = pad_nets
    return mco_operation(
        "pcbdoc.add_component",
        f"add_{_safe_id(designator)}_footprint",
        f"Add mate PCB component {designator}",
        args,
    )


def _target_pcb_labels_config(
    default_labels: MatePcbLabelsConfig,
    target: Mapping[str, object],
) -> MatePcbLabelsConfig:
    raw = target.get("mate_pcb_label")
    if isinstance(raw, dict):
        return _parse_pcb_labels_config(raw)
    return default_labels


def _pcb_designator_arrangement_operation(
    output: MateOutputConfig,
    designators: MatePcbDesignatorsConfig,
    placed_designators: list[str],
) -> JsonObject | None:
    if not designators.enabled or not placed_designators:
        return None
    style = dict(designators.style)
    args: JsonObject = {
        "file": _output_file(output.output_dir, _board_filename(output)),
        "overwrite": True,
        "designators": list(placed_designators),
        "placement": designators.placement,
        "offset_mils": list(designators.offset_mils),
        "width_factor": designators.width_factor,
        "height_mils": _style_float(style, "height_mils", 40.0),
        "layer": _style_string_or_int(style, "layer", "TOP_OVERLAY"),
        "font_kind": _style_string(style, "font_kind", "truetype"),
        "font_name": _style_string(style, "font_name", "Arial"),
        "bold": _style_bool(style, "bold", True),
        "italic": _style_bool(style, "italic", False),
        "stroke_width_mils": _style_float(style, "stroke_width_mils", 8.0),
    }
    return mco_operation(
        "pcbdoc.arrange_designators",
        "arrange_pcb_designators",
        "Arrange mate PCB designators",
        args,
    )


def _mate_user_union_operation(output: MateOutputConfig) -> JsonObject:
    return mco_operation(
        "pcbdoc.create_user_union",
        "group_mate_features",
        "Group generated mate PCB features",
        {
            "file": _output_file(output.output_dir, _board_filename(output)),
            "overwrite": True,
            "name": "MATE_FEATURES",
        },
    )


def _mate_component_parameters(
    target: Mapping[str, object],
    part: Mapping[str, object],
) -> dict[str, str]:
    parameters = {
        "MateRole": _part_string(part, "role"),
        "MateSourceBoard": str(target.get("board_key", "") or ""),
        "MateSourceDesignator": str(target.get("source_designator", "") or ""),
        "MateSourceKind": str(target.get("kind", "") or ""),
        "MateSourceFootprint": str(target.get("source_footprint", "") or ""),
    }
    net_name = _target_optional_string(target, "net_name")
    if net_name:
        parameters["MateSourceNet"] = net_name
    return parameters


def _mate_pad_nets(
    target: Mapping[str, object],
    part: Mapping[str, object],
) -> dict[str, str] | None:
    net_name = _target_optional_string(target, "net_name")
    signal_pad = _part_optional_string(part, "signal_pad_designator")
    if not net_name or not signal_pad:
        return None
    return {signal_pad: net_name}


def _known_part_file(
    known_parts: MateKnownPartsConfig,
    part: Mapping[str, object],
    field: str,
) -> str:
    relative = _part_string(part, field)
    return (known_parts.cache_dir / relative).resolve().as_posix()


def _part_source_file(part: Mapping[str, object], field: str) -> str:
    source_field = {
        "symbol_library": "symbol_source_library",
        "footprint_library": "footprint_source_library",
    }.get(field)
    if source_field is None:
        raise ValueError(f"Unsupported mate library field: {field}")
    return _part_string(part, source_field)


def _copied_known_part_file(
    output: MateOutputConfig,
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


def _component_link_unique_id(
    output: MateOutputConfig,
    target: Mapping[str, object],
    designator: str,
) -> str:
    seed = "|".join(
        [
            output.project_name,
            designator,
            str(target.get("board_key", "") or ""),
            str(target.get("source_designator", "") or ""),
            str(target.get("kind", "") or ""),
        ]
    )
    return hashlib.sha1(seed.encode("utf-8")).hexdigest()[:8].upper()


def _mate_part_symbol_description(
    part: Mapping[str, object],
) -> str:
    try:
        from altium_monkey import AltiumSchLib

        schlib = AltiumSchLib(_part_source_file(part, "symbol_library"))
        symbol = schlib.get_symbol(_part_string(part, "symbol_name"))
        if symbol is not None:
            description = str(getattr(symbol, "description", "") or "")
            if description:
                return description
    except Exception:
        return _part_optional_string(part, "description") or ""
    return _part_optional_string(part, "description") or ""


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


def _schematic_filename(output: MateOutputConfig) -> str:
    return output.schematic_filename or f"{output.project_name}.SchDoc"


def _board_filename(output: MateOutputConfig) -> str:
    return output.board_filename or f"{output.project_name}.PcbDoc"


def _project_filename(output: MateOutputConfig) -> str:
    return output.project_filename or f"{output.project_name}.PrjPcb"


def _operations_with_prefix(
    operations: Sequence[Mapping[str, object]],
    prefix: str,
) -> list[JsonObject]:
    return [
        dict(operation)
        for operation in operations
        if str(operation.get("op", "")).startswith(prefix)
    ]


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
        raise ValueError(f"Mate config field {name!r} must be an object")
    return dict(value)


def _section(root: Mapping[str, object], name: str) -> JsonObject:
    value = root.get(name, {})
    if not isinstance(value, dict):
        raise ValueError(f"Mate config field {name!r} must be an object")
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


def _optional_float_or_none(
    args: Mapping[str, object],
    name: str,
) -> float | None:
    value = args.get(name)
    if value is None:
        return None
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
            _default_mate_reference_graphics_payload(),
            {
                "kind": "label",
                "text": "source_net",
                "placement": _default_mate_label_placement_payload(),
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
            _default_mate_reference_graphics_payload(),
        ],
    }


def _mate_seed_alignment_pins_projection(_pads: list[JsonObject]) -> JsonObject:
    return {
        "id": "alignment_pins",
        "source": {
            "object": "free_pad",
            "hole_size_mils": {"min": 75, "max": 85},
            "plated": False,
        },
        "actions": [
            {"kind": "mate_component", "part": "alignment_pin_2mm_npth"},
            _default_mate_reference_graphics_payload(),
            {
                "kind": "label",
                "text": "source_net",
                "placement": _default_mate_label_placement_payload(),
                "style": _default_mate_label_style_payload(),
            },
        ],
    }


def _default_mate_reference_graphics_payload() -> JsonObject:
    return {
        "kind": "reference_graphics",
        "shape": "source_pad_outline",
        "layer": "MECHANICAL_1",
        "style": {
            "mode": "outline",
            "outline_count": 1,
            "clearance_mils": 10,
            "stroke_width_mils": 10,
        },
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


def _mate_template_text(*, source_board: Path | str | None = None) -> str:
    payload = _mate_template_payload(source_board=source_board)
    return (
        "/*\n"
        "  altium-cruncher mate config a0\n"
        "\n"
        "  Edit source.board to the DUT .PrjPcb or .PcbDoc, place any required\n"
        "  SchLib/PcbLib files under libraries.roots, and then run:\n"
        "\n"
        "      altium-cruncher mate\n"
        "\n"
        "  mate_component actions resolve symbol_name and footprint_name by\n"
        "  scanning the configured library roots. The generated MCO is a derived\n"
        "  artifact; keep this config as the human-authored source of truth.\n"
        "*/\n"
        f"{json.dumps(payload, indent=2)}\n"
    )


def _mate_template_payload(*, source_board: Path | str | None) -> JsonObject:
    source_board_text = (
        str(source_board).replace("\\", "/")
        if source_board is not None
        else "path/to/dut.PrjPcb"
    )
    output = _default_mate_output_payload()
    output.update(
        {
            "output_dir": "output",
            "project_name": "mate",
            "board_outline": {
                "mode": "source_bounds_with_margin",
                "margin_mils": {
                    "left": 500,
                    "bottom": 500,
                    "right": 3000,
                    "top": 500,
                },
            },
            "overwrite": True,
        }
    )
    board_projection = _default_mate_board_projection_payload()
    board_projection["cutouts"]["actual_cutouts"] = True
    return {
        "schema": MATE_CONFIG_SCHEMA,
        "source": {
            "board": source_board_text,
            "project_context": "auto",
        },
        "output": output,
        "libraries": {
            "roots": ["mating_parts"],
            "recursive": True,
        },
        "validation": {
            "source_side": "infer_single_side",
            "allow_side_agnostic_through_hole": True,
            "side_agnostic_kinds": ["mount"],
        },
        "projections": [
            _named_test_point_projection(),
            _named_mount_projection(),
            _named_alignment_pin_projection(),
        ],
        "pcb_designators": _default_mate_designators_payload(),
        "board_projection": board_projection,
        "artifacts": _default_mate_artifacts_payload(),
    }


def _named_test_point_projection() -> JsonObject:
    return {
        "id": "test_points",
        "source": {
            "object": "component",
            "designators": "TP*",
        },
        "actions": [
            {
                "kind": "mate_component",
                "symbol_name": "YZ209315103P-01",
                "footprint_name": "YZ209315103P-01",
                "designator_prefix": "TP",
                "signal_pad_designator": "1",
            },
            _default_mate_reference_graphics_payload(),
            {
                "kind": "label",
                "text": "source_net",
                "placement": _default_mate_label_placement_payload(),
                "style": _default_mate_label_style_payload(),
            },
        ],
    }


def _named_mount_projection() -> JsonObject:
    return {
        "id": "mounts",
        "source": {
            "object": "component",
            "designators": "M1-4",
        },
        "actions": [
            {
                "kind": "mate_component",
                "symbol_name": "9774080360R",
                "footprint_name": "9774080360R-YIYUAN",
                "designator_prefix": "M",
            },
            _default_mate_reference_graphics_payload(),
        ],
    }


def _named_alignment_pin_projection() -> JsonObject:
    return {
        "id": "alignment_pins",
        "source": {
            "object": "free_pad",
            "hole_size_mils": {"min": 75, "max": 85},
            "plated": False,
        },
        "actions": [
            {
                "kind": "mate_component",
                "symbol_name": "H2184-05",
                "footprint_name": "H2184-05",
                "designator_prefix": "P",
                "signal_pad_designator": "1",
            },
            _default_mate_reference_graphics_payload(),
            {
                "kind": "label",
                "text": "source_net",
                "placement": _default_mate_label_placement_payload(),
                "style": _default_mate_label_style_payload(),
            },
        ],
    }
