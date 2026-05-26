"""Generate a STEP alignment model for one PCB layer."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import logging
import math
from pathlib import Path
import re
from typing import Any

from altium_monkey.altium_board import BoardOutlineVertex, resolve_outline_arc_segment
from altium_monkey.altium_pcb_enums import PadShape
from altium_monkey.altium_record_types import PcbLayer
from altium_monkey.altium_svg_arc_helpers import choose_svg_sweep_flag_for_center

log = logging.getLogger(__name__)

MIL_TO_MM = 0.0254
INTERNAL_UNITS_PER_MIL = 10000.0
DEFAULT_COPPER_COLOR = "#B87333"
DEFAULT_OUTLINE_COLOR = "#111111"
PCB_LAYER_STEP_CONFIG_FILENAME = "pcb-layer-step.json"
PCB_LAYER_STEP_CONFIG_SCHEMA = "wn.altium_cruncher.pcb_layer_step.config.v1"


@dataclass(frozen=True, slots=True)
class PcbLayerStepOptions:
    """Options for one-layer PCB STEP export."""

    layer: PcbLayer = PcbLayer.BOTTOM
    thickness_mm: float = 0.035
    z_mm: float = 0.0
    copper_color: str = DEFAULT_COPPER_COLOR
    outline_width_mm: float = 0.2
    outline_color: str = DEFAULT_OUTLINE_COLOR
    include_copper: bool = True
    include_board_outline: bool = True
    include_poured_polygons: bool = True
    cut_holes: bool = True
    fuse_copper: bool = True
    fuse_board_outline: bool = True
    arc_segments: int = 32


@dataclass(frozen=True, slots=True)
class PcbLayerStepResult:
    """Summary of a generated one-layer PCB STEP export."""

    output_path: Path
    manifest_path: Path
    board_name: str
    layer: str
    copper_body_count: int
    outline_body_count: int
    drill_cut_count: int
    source_input: str | None


def _coerce_optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _coerce_str(value: Any, default: str) -> str:
    if value is None:
        return default
    return str(value)


def _coerce_float(value: Any, default: float) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid numeric value in pcb-layer-step config: {value!r}") from exc


def _coerce_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, int | float):
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "y", "on"}:
            return True
        if normalized in {"0", "false", "no", "n", "off"}:
            return False
    raise ValueError(f"Invalid boolean value in pcb-layer-step config: {value!r}")


@dataclass(frozen=True, slots=True)
class PcbLayerStepConfig:
    """JSON config for one-layer PCB STEP export."""

    schema: str = PCB_LAYER_STEP_CONFIG_SCHEMA
    pcbdoc: str | None = None
    layer: str = "bottom"
    thickness_mm: float = 0.035
    z_mm: float = 0.0
    copper_color: str = DEFAULT_COPPER_COLOR
    outline_width_mm: float = 0.2
    outline_color: str = DEFAULT_OUTLINE_COLOR
    include_copper: bool = True
    include_board_outline: bool = True
    include_poured_polygons: bool = True
    cut_holes: bool = True
    fuse_copper: bool = True
    fuse_board_outline: bool = True
    arc_segments: int = 32

    @classmethod
    def default(cls) -> "PcbLayerStepConfig":
        return cls()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PcbLayerStepConfig":
        if not isinstance(data, dict):
            raise ValueError("pcb-layer-step config root must be a JSON object")
        options = data.get("options")
        if options is not None:
            if not isinstance(options, dict):
                raise ValueError("pcb-layer-step config field 'options' must be an object")
            merged = {**data, **options}
        else:
            merged = data
        default = cls()
        return cls(
            schema=str(merged.get("schema") or default.schema),
            pcbdoc=_coerce_optional_str(merged.get("pcbdoc")),
            layer=_coerce_str(merged.get("layer"), default.layer),
            thickness_mm=_coerce_float(merged.get("thickness_mm"), default.thickness_mm),
            z_mm=_coerce_float(merged.get("z_mm"), default.z_mm),
            copper_color=_coerce_str(merged.get("copper_color"), default.copper_color),
            outline_width_mm=_coerce_float(
                merged.get("outline_width_mm"), default.outline_width_mm
            ),
            outline_color=_coerce_str(merged.get("outline_color"), default.outline_color),
            include_copper=_coerce_bool(
                merged.get("include_copper"), default.include_copper
            ),
            include_board_outline=_coerce_bool(
                merged.get("include_board_outline"), default.include_board_outline
            ),
            include_poured_polygons=_coerce_bool(
                merged.get("include_poured_polygons"), default.include_poured_polygons
            ),
            cut_holes=_coerce_bool(merged.get("cut_holes"), default.cut_holes),
            fuse_copper=_coerce_bool(merged.get("fuse_copper"), default.fuse_copper),
            fuse_board_outline=_coerce_bool(
                merged.get("fuse_board_outline"), default.fuse_board_outline
            ),
            arc_segments=int(_coerce_float(merged.get("arc_segments"), default.arc_segments)),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "pcbdoc": self.pcbdoc,
            "layer": self.layer,
            "thickness_mm": self.thickness_mm,
            "z_mm": self.z_mm,
            "copper_color": self.copper_color,
            "outline_width_mm": self.outline_width_mm,
            "outline_color": self.outline_color,
            "include_copper": self.include_copper,
            "include_board_outline": self.include_board_outline,
            "include_poured_polygons": self.include_poured_polygons,
            "cut_holes": self.cut_holes,
            "fuse_copper": self.fuse_copper,
            "fuse_board_outline": self.fuse_board_outline,
            "arc_segments": self.arc_segments,
        }

    def to_options(self) -> PcbLayerStepOptions:
        return PcbLayerStepOptions(
            layer=resolve_pcb_layer_selector(self.layer),
            thickness_mm=self.thickness_mm,
            z_mm=self.z_mm,
            copper_color=self.copper_color,
            outline_width_mm=self.outline_width_mm,
            outline_color=self.outline_color,
            include_copper=self.include_copper,
            include_board_outline=self.include_board_outline,
            include_poured_polygons=self.include_poured_polygons,
            cut_holes=self.cut_holes,
            fuse_copper=self.fuse_copper,
            fuse_board_outline=self.fuse_board_outline,
            arc_segments=self.arc_segments,
        )


@dataclass(slots=True)
class _Segment:
    kind: str = "line"
    center: tuple[float, float] | None = None
    sweep: str | None = None

    def to_json(self) -> dict[str, Any]:
        data: dict[str, Any] = {"kind": self.kind}
        if self.center is not None:
            data["center"] = [self.center[0], self.center[1]]
        if self.sweep is not None:
            data["sweep"] = self.sweep
        return data


@dataclass(slots=True)
class _Ring:
    points: list[tuple[float, float]]
    segments: list[_Segment] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.points = _dedupe_closed_points(self.points)
        if not self.segments:
            self.segments = [_Segment() for _ in self.points]
        if len(self.segments) != len(self.points):
            raise ValueError("ring segments must match ring points")

    def to_json(self) -> dict[str, Any]:
        return {
            "points": [[x, y] for x, y in self.points],
            "segments": [segment.to_json() for segment in self.segments],
        }


@dataclass(slots=True)
class _Region:
    outer: _Ring
    holes: list[_Ring] = field(default_factory=list)

    def to_json(self) -> dict[str, Any]:
        data: dict[str, Any] = {"outer": self.outer.to_json()}
        if self.holes:
            data["holes"] = [hole.to_json() for hole in self.holes]
        return data


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

    normalized = re.sub(r"[\s_\-]+", "", text).upper()
    if normalized.startswith("L") and normalized[1:].isdigit():
        return PcbLayer(int(normalized[1:]))

    aliases = {
        "TOP": PcbLayer.TOP,
        "TOPLAYER": PcbLayer.TOP,
        "FRONT": PcbLayer.TOP,
        "BOTTOM": PcbLayer.BOTTOM,
        "BOTTOMLAYER": PcbLayer.BOTTOM,
        "BOT": PcbLayer.BOTTOM,
        "BACK": PcbLayer.BOTTOM,
        "MULTILAYER": PcbLayer.MULTI_LAYER,
    }
    if normalized in aliases:
        return aliases[normalized]

    for layer in PcbLayer:
        names = {
            re.sub(r"[\s_\-]+", "", layer.name).upper(),
            re.sub(r"[\s_\-]+", "", layer.to_json_name()).upper(),
            re.sub(r"[\s_\-]+", "", layer.to_display_name()).upper(),
        }
        if normalized in names:
            return layer

    raise ValueError(f"Unknown PCB layer selector: {selector!r}")


def write_default_pcb_layer_step_config(config_path: Path) -> None:
    """Write a default editable pcb-layer-step JSON config."""
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        json.dumps(PcbLayerStepConfig.default().to_dict(), indent=2),
        encoding="utf-8",
    )


def load_pcb_layer_step_config(config_path: Path) -> PcbLayerStepConfig:
    """Load a pcb-layer-step JSON config."""
    try:
        raw_data = json.loads(config_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"Failed to parse pcb-layer-step config '{config_path}': {exc}") from exc
    return PcbLayerStepConfig.from_dict(raw_data)


def export_pcb_layer_step(
    pcbdoc: Any,
    output_path: Path,
    *,
    options: PcbLayerStepOptions | None = None,
    board_name: str | None = None,
    source_input: str | None = None,
) -> PcbLayerStepResult:
    """Export a selected PCB layer as a colored STEP alignment model."""
    opts = options or PcbLayerStepOptions()
    if opts.thickness_mm <= 0.0:
        raise ValueError("STEP layer thickness must be positive")
    if opts.outline_width_mm < 0.0:
        raise ValueError("Board outline width must be non-negative")

    try:
        import geometer
    except Exception as exc:  # pragma: no cover - import failure depends on environment
        raise RuntimeError("PCB layer STEP export requires wn-geometer with planar_step support") from exc
    if not hasattr(geometer, "write_planar_step"):
        raise RuntimeError("PCB layer STEP export requires wn-geometer write_planar_step support")

    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    layer = opts.layer
    resolved_board_name = board_name or _board_name_from_pcbdoc(pcbdoc)

    layer_regions = _collect_layer_regions(pcbdoc, layer, opts)
    drill_cutouts = _collect_drill_cutout_regions(pcbdoc, layer, opts)
    board_cutouts = _collect_board_cutout_regions(pcbdoc)
    all_cutouts = [*drill_cutouts, *board_cutouts] if opts.cut_holes else []
    outline_regions = (
        _collect_board_outline_regions(pcbdoc, opts)
        if opts.include_board_outline and opts.outline_width_mm > 0.0
        else []
    )

    bodies: list[dict[str, Any]] = []
    if opts.include_copper and layer_regions:
        copper_body: dict[str, Any] = {
            "id": "copper",
            "name": "copper",
            "color": opts.copper_color,
            "z_mm": opts.z_mm,
            "thickness_mm": opts.thickness_mm,
            "regions": [region.to_json() for region in layer_regions],
        }
        if opts.fuse_copper:
            copper_body["fuse_regions"] = True
        if all_cutouts:
            copper_body["cutouts"] = [cutout.to_json() for cutout in all_cutouts]
        bodies.append(copper_body)

    if outline_regions:
        outline_body: dict[str, Any] = {
            "id": "board_outline",
            "name": "board_outline",
            "color": opts.outline_color,
            "z_mm": opts.z_mm,
            "thickness_mm": opts.thickness_mm,
            "regions": [region.to_json() for region in outline_regions],
        }
        if opts.fuse_board_outline:
            outline_body["fuse_regions"] = True
        bodies.append(outline_body)

    if not bodies:
        raise ValueError(f"No geometry found for layer {layer.to_display_name()}")

    request = {
        "schema": "geometry.planar_step.request.a0",
        "units": "mm",
        "name": _step_name(resolved_board_name),
        "bodies": bodies,
    }
    geometer.write_planar_step(request, output_path)

    manifest_path = output_path.with_suffix(".json")
    manifest = {
        "schema": "wn.altium_cruncher.pcb_layer_step.v1",
        "backend": "geometer.planar_step",
        "board": resolved_board_name,
        "source_input": source_input,
        "step_file": output_path.name,
        "layer": {
            "id": int(layer.value),
            "json_name": layer.to_json_name(),
            "display_name": layer.to_display_name(),
        },
        "options": {
            "thickness_mm": float(opts.thickness_mm),
            "z_mm": float(opts.z_mm),
            "copper_color": opts.copper_color,
            "outline_width_mm": float(opts.outline_width_mm),
            "outline_color": opts.outline_color,
            "include_copper": bool(opts.include_copper),
            "include_board_outline": bool(opts.include_board_outline),
            "include_poured_polygons": bool(opts.include_poured_polygons),
            "cut_holes": bool(opts.cut_holes),
            "fuse_copper": bool(opts.fuse_copper),
            "fuse_board_outline": bool(opts.fuse_board_outline),
            "arc_segments": int(opts.arc_segments),
        },
        "counts": {
            "source_layer_geometries": len(layer_regions),
            "drill_cut_geometries": len(drill_cutouts),
            "board_cutout_geometries": len(board_cutouts),
            "copper_bodies": len(layer_regions) if opts.include_copper else 0,
            "outline_bodies": len(outline_regions),
        },
        "bytes": output_path.stat().st_size,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    return PcbLayerStepResult(
        output_path=output_path,
        manifest_path=manifest_path,
        board_name=resolved_board_name,
        layer=layer.to_json_name(),
        copper_body_count=len(layer_regions) if opts.include_copper else 0,
        outline_body_count=len(outline_regions),
        drill_cut_count=len(drill_cutouts),
        source_input=source_input,
    )


def _collect_layer_regions(
    pcbdoc: Any,
    layer: PcbLayer,
    opts: PcbLayerStepOptions,
) -> list[_Region]:
    regions: list[_Region] = []

    for track in getattr(pcbdoc, "tracks", []) or []:
        if int(getattr(track, "layer", 0) or 0) != layer.value:
            continue
        if _is_poured_polygon_primitive(track) and not opts.include_poured_polygons:
            continue
        region = _track_region(track)
        if region is not None:
            regions.append(region)

    for arc in getattr(pcbdoc, "arcs", []) or []:
        if int(getattr(arc, "layer", 0) or 0) != layer.value:
            continue
        if _is_poured_polygon_primitive(arc) and not opts.include_poured_polygons:
            continue
        region = _arc_region(arc)
        if region is not None:
            regions.append(region)

    for fill in getattr(pcbdoc, "fills", []) or []:
        if int(getattr(fill, "layer", 0) or 0) != layer.value:
            continue
        if _is_poured_polygon_primitive(fill) and not opts.include_poured_polygons:
            continue
        region = _fill_region(fill)
        if region is not None:
            regions.append(region)

    if layer.is_copper():
        for pad in getattr(pcbdoc, "pads", []) or []:
            region = _pad_region(pad, layer)
            if region is not None:
                regions.append(region)
        for via in getattr(pcbdoc, "vias", []) or []:
            region = _via_region(via, layer)
            if region is not None:
                regions.append(region)

    for region in getattr(pcbdoc, "regions", []) or []:
        if int(getattr(region, "layer", 0) or 0) != layer.value:
            continue
        if bool(getattr(region, "is_board_cutout", False)) or bool(
            getattr(region, "is_keepout", False)
        ):
            continue
        if _is_poured_polygon_primitive(region) and not opts.include_poured_polygons:
            continue
        converted = _region_from_outline_vertices(region)
        if converted is not None:
            regions.append(converted)

    for region in getattr(pcbdoc, "shapebased_regions", []) or []:
        if int(getattr(region, "layer", 0) or 0) != layer.value:
            continue
        if bool(getattr(region, "is_keepout", False)):
            continue
        if _is_poured_polygon_primitive(region) and not opts.include_poured_polygons:
            continue
        converted = _shapebased_region(region)
        if converted is not None:
            regions.append(converted)

    return [region for region in regions if len(region.outer.points) >= 3]


def _collect_drill_cutout_regions(
    pcbdoc: Any,
    layer: PcbLayer,
    opts: PcbLayerStepOptions,
) -> list[_Region]:
    if not layer.is_copper():
        return []
    cutouts: list[_Region] = []
    for pad in getattr(pcbdoc, "pads", []) or []:
        if not _pad_should_render_on_layer(pad, layer):
            continue
        cutout = _pad_hole_region(pad, layer, opts.arc_segments)
        if cutout is not None:
            cutouts.append(cutout)
    for via in getattr(pcbdoc, "vias", []) or []:
        if not _via_spans_layer(via, layer):
            continue
        cutout = _via_hole_region(via)
        if cutout is not None:
            cutouts.append(cutout)
    return cutouts


def _collect_board_outline_regions(pcbdoc: Any, opts: PcbLayerStepOptions) -> list[_Region]:
    board = getattr(pcbdoc, "board", None)
    outline = getattr(board, "outline", None) if board is not None else None
    if outline is None:
        return []

    regions: list[_Region] = []
    regions.extend(_outline_stroke_regions(getattr(outline, "vertices", []) or [], opts.outline_width_mm))
    for cutout in getattr(outline, "cutouts", []) or []:
        regions.extend(_outline_stroke_regions(cutout, opts.outline_width_mm))
    return regions


def _collect_board_cutout_regions(pcbdoc: Any) -> list[_Region]:
    cutouts: list[_Region] = []
    board = getattr(pcbdoc, "board", None)
    outline = getattr(board, "outline", None) if board is not None else None
    for cutout in getattr(outline, "cutouts", []) or []:
        ring = _outline_ring(cutout)
        if ring is not None:
            cutouts.append(_Region(ring))

    for region in getattr(pcbdoc, "regions", []) or []:
        if not bool(getattr(region, "is_board_cutout", False)):
            continue
        converted = _region_from_outline_vertices(region)
        if converted is not None:
            cutouts.append(converted)
    return cutouts


def _track_region(track: Any) -> _Region | None:
    width_mm = max(_mils_to_mm(float(getattr(track, "width_mils", 0.0) or 0.0)), 0.0)
    if width_mm <= 0.0:
        return None
    start = (
        _mils_to_mm(float(getattr(track, "start_x_mils", 0.0))),
        _mils_to_mm(float(getattr(track, "start_y_mils", 0.0))),
    )
    end = (
        _mils_to_mm(float(getattr(track, "end_x_mils", 0.0))),
        _mils_to_mm(float(getattr(track, "end_y_mils", 0.0))),
    )
    return _line_capsule_region(start, end, width_mm)


def _arc_region(arc: Any) -> _Region | None:
    width_mm = max(_mils_to_mm(_iu_to_mils(getattr(arc, "width", 0))), 0.0)
    radius_mils = float(getattr(arc, "radius_mils", 0.0) or 0.0)
    if width_mm <= 0.0 or radius_mils <= 0.0:
        return None
    center_mils = (float(arc.center_x_mils), float(arc.center_y_mils))
    start_degrees = float(getattr(arc, "start_angle", 0.0) or 0.0)
    end_degrees = float(getattr(arc, "end_angle", 0.0) or 0.0)
    start_point = _arc_point_from_angle_mils(center_mils, radius_mils, start_degrees)
    end_point = _arc_point_from_angle_mils(center_mils, radius_mils, end_degrees)
    sweep = _svg_like_board_sweep_degrees(
        center_mils=center_mils,
        radius_mils=radius_mils,
        start_point_mils=start_point,
        end_point_mils=end_point,
        start_degrees=start_degrees,
        end_degrees=end_degrees,
        default_sweep_flag=1,
    )
    return _arc_stroke_region(
        center=(_mils_to_mm(center_mils[0]), _mils_to_mm(center_mils[1])),
        radius_mm=_mils_to_mm(radius_mils),
        start_degrees=math.degrees(math.atan2(start_point[1] - center_mils[1], start_point[0] - center_mils[0])),
        sweep_degrees=sweep,
        width_mm=width_mm,
    )


def _fill_region(fill: Any) -> _Region | None:
    x1 = _mils_to_mm(_iu_to_mils(getattr(fill, "pos1_x", 0)))
    y1 = _mils_to_mm(_iu_to_mils(getattr(fill, "pos1_y", 0)))
    x2 = _mils_to_mm(_iu_to_mils(getattr(fill, "pos2_x", 0)))
    y2 = _mils_to_mm(_iu_to_mils(getattr(fill, "pos2_y", 0)))
    if math.isclose(x1, x2, abs_tol=1e-9) or math.isclose(y1, y2, abs_tol=1e-9):
        return None
    cx = (x1 + x2) / 2.0
    cy = (y1 + y2) / 2.0
    return _rectangle_region(
        center=(cx, cy),
        width_mm=abs(x2 - x1),
        height_mm=abs(y2 - y1),
        rotation_degrees=float(getattr(fill, "rotation", 0.0) or 0.0),
    )


def _pad_region(pad: Any, layer: PcbLayer) -> _Region | None:
    if not _pad_should_render_on_layer(pad, layer):
        return None
    try:
        width_iu, height_iu = pad._layer_size(layer)
        shape = int(pad._layer_shape(layer))
        cx_mils, cy_mils = pad.pad_center_mils(layer)
    except Exception:
        width_iu = int(getattr(pad, "top_width", 0) or getattr(pad, "width", 0) or 0)
        height_iu = int(getattr(pad, "top_height", 0) or getattr(pad, "height", 0) or 0)
        shape = int(getattr(pad, "shape", PadShape.CIRCLE) or PadShape.CIRCLE)
        cx_mils = _iu_to_mils(getattr(pad, "x", 0))
        cy_mils = _iu_to_mils(getattr(pad, "y", 0))

    width_mm = _mils_to_mm(_iu_to_mils(width_iu))
    height_mm = _mils_to_mm(_iu_to_mils(height_iu))
    if width_mm <= 0.0 or height_mm <= 0.0:
        return None
    center = (_mils_to_mm(cx_mils), _mils_to_mm(cy_mils))
    rotation = float(getattr(pad, "rotation", 0.0) or 0.0)
    corner_pct = _pad_corner_radius_percent(pad, layer)
    region = _pad_shape_region(
        center=center,
        width_mm=width_mm,
        height_mm=height_mm,
        shape=shape,
        rotation_degrees=rotation,
        corner_radius_percent=corner_pct,
    )
    return region


def _via_region(via: Any, layer: PcbLayer) -> _Region | None:
    if not _via_spans_layer(via, layer) or _via_pad_removed_on_layer(via, layer):
        return None
    diameter_iu = _via_diameter_iu(via, layer)
    diameter_mm = _mils_to_mm(_iu_to_mils(diameter_iu))
    if diameter_mm <= 0.0:
        return None
    center = (_mils_to_mm(via.x_mils), _mils_to_mm(via.y_mils))
    return _circle_region(center, diameter_mm / 2.0)


def _region_from_outline_vertices(region: Any) -> _Region | None:
    outline = [
        (_mils_to_mm(vertex.x_mils), _mils_to_mm(vertex.y_mils))
        for vertex in (getattr(region, "outline_vertices", []) or [])
    ]
    holes = [
        _Ring([(_mils_to_mm(vertex.x_mils), _mils_to_mm(vertex.y_mils)) for vertex in hole])
        for hole in (getattr(region, "hole_vertices", []) or [])
        if len(hole) >= 3
    ]
    if len(_dedupe_closed_points(outline)) < 3:
        return None
    return _Region(_Ring(outline), holes)


def _shapebased_region(region: Any) -> _Region | None:
    outline_vertices = list(getattr(region, "outline", []) or [])
    if hasattr(region, "_outline_vertices_without_closing_duplicate"):
        outline_vertices = region._outline_vertices_without_closing_duplicate(outline_vertices)
    outer = _extended_vertices_ring(outline_vertices)
    if outer is None:
        return None
    holes = [
        _Ring([(_mils_to_mm(vertex.x_mils), _mils_to_mm(vertex.y_mils)) for vertex in hole])
        for hole in (getattr(region, "holes", []) or [])
        if len(hole) >= 3
    ]
    return _Region(outer, holes)


def _pad_hole_region(pad: Any, layer: PcbLayer, arc_segments: int) -> _Region | None:
    hole_size_mils = float(getattr(pad, "hole_size_mils", 0.0) or 0.0)
    if hole_size_mils <= 0.0:
        return None
    try:
        cx_mils, cy_mils = pad.hole_center_mils(layer)
    except Exception:
        cx_mils = _iu_to_mils(getattr(pad, "x", 0))
        cy_mils = _iu_to_mils(getattr(pad, "y", 0))
    center = (_mils_to_mm(cx_mils), _mils_to_mm(cy_mils))
    diameter_mm = _mils_to_mm(hole_size_mils)
    slot_size_mils = _iu_to_mils(getattr(pad, "slot_size", 0))
    is_slot = int(getattr(pad, "hole_shape", 0) or 0) == 2 and slot_size_mils > hole_size_mils
    if not is_slot:
        return _circle_region(center, diameter_mm / 2.0)
    slot_length_mm = _mils_to_mm(slot_size_mils)
    rotation = float(getattr(pad, "slot_rotation", 0.0) or 0.0) + float(
        getattr(pad, "rotation", 0.0) or 0.0
    )
    return _capsule_region(center, slot_length_mm, diameter_mm, rotation, arc_segments)


def _via_hole_region(via: Any) -> _Region | None:
    hole_size_mils = float(getattr(via, "hole_size_mils", 0.0) or 0.0)
    if hole_size_mils <= 0.0:
        return None
    center = (_mils_to_mm(via.x_mils), _mils_to_mm(via.y_mils))
    return _circle_region(center, _mils_to_mm(hole_size_mils) / 2.0)


def _line_capsule_region(start: tuple[float, float], end: tuple[float, float], width_mm: float) -> _Region | None:
    radius = width_mm / 2.0
    if radius <= 0.0:
        return None
    if _points_close(start, end):
        return _circle_region(start, radius)
    sx, sy = start
    ex, ey = end
    dx = ex - sx
    dy = ey - sy
    length = math.hypot(dx, dy)
    if length <= 1e-12:
        return _circle_region(start, radius)
    nx = -dy / length
    ny = dx / length
    points = [
        (sx + nx * radius, sy + ny * radius),
        (ex + nx * radius, ey + ny * radius),
        (ex - nx * radius, ey - ny * radius),
        (sx - nx * radius, sy - ny * radius),
    ]
    segments = [
        _Segment("line"),
        _Segment("arc", center=end, sweep="cw"),
        _Segment("line"),
        _Segment("arc", center=start, sweep="cw"),
    ]
    return _Region(_Ring(points, segments))


def _arc_stroke_region(
    *,
    center: tuple[float, float],
    radius_mm: float,
    start_degrees: float,
    sweep_degrees: float,
    width_mm: float,
) -> _Region | None:
    half_width = width_mm / 2.0
    outer_radius = radius_mm + half_width
    inner_radius = radius_mm - half_width
    if outer_radius <= 0.0 or inner_radius <= 0.0 or math.isclose(sweep_degrees, 0.0, abs_tol=1e-9):
        return None
    end_degrees = start_degrees + sweep_degrees
    outer_start = _arc_point_from_angle_mm(center, outer_radius, start_degrees)
    outer_end = _arc_point_from_angle_mm(center, outer_radius, end_degrees)
    inner_end = _arc_point_from_angle_mm(center, inner_radius, end_degrees)
    inner_start = _arc_point_from_angle_mm(center, inner_radius, start_degrees)
    end_center = _arc_point_from_angle_mm(center, radius_mm, end_degrees)
    start_center = _arc_point_from_angle_mm(center, radius_mm, start_degrees)
    sweep = "ccw" if sweep_degrees > 0.0 else "cw"
    opposite = "cw" if sweep == "ccw" else "ccw"
    return _Region(
        _Ring(
            [outer_start, outer_end, inner_end, inner_start],
            [
                _Segment("arc", center=center, sweep=sweep),
                _Segment("arc", center=end_center, sweep=sweep),
                _Segment("arc", center=center, sweep=opposite),
                _Segment("arc", center=start_center, sweep=sweep),
            ],
        )
    )


def _capsule_region(
    center: tuple[float, float],
    length_mm: float,
    diameter_mm: float,
    rotation_degrees: float,
    arc_segments: int,
) -> _Region | None:
    del arc_segments
    straight = max(0.0, length_mm - diameter_mm)
    dx = (straight / 2.0) * math.cos(math.radians(rotation_degrees))
    dy = (straight / 2.0) * math.sin(math.radians(rotation_degrees))
    start = (center[0] - dx, center[1] - dy)
    end = (center[0] + dx, center[1] + dy)
    return _line_capsule_region(start, end, diameter_mm)


def _circle_region(center: tuple[float, float], radius_mm: float) -> _Region:
    cx, cy = center
    points = [
        (cx + radius_mm, cy),
        (cx, cy + radius_mm),
        (cx - radius_mm, cy),
        (cx, cy - radius_mm),
    ]
    segments = [_Segment("arc", center=center, sweep="ccw") for _ in range(4)]
    return _Region(_Ring(points, segments))


def _ellipse_region(
    center: tuple[float, float],
    radius_x_mm: float,
    radius_y_mm: float,
    rotation_degrees: float,
    samples: int,
) -> _Region:
    count = max(16, int(samples))
    points = [
        _rotate_point(
            (
                center[0] + radius_x_mm * math.cos(2.0 * math.pi * idx / count),
                center[1] + radius_y_mm * math.sin(2.0 * math.pi * idx / count),
            ),
            center,
            rotation_degrees,
        )
        for idx in range(count)
    ]
    return _Region(_Ring(points))


def _rectangle_region(
    *,
    center: tuple[float, float],
    width_mm: float,
    height_mm: float,
    rotation_degrees: float,
) -> _Region:
    cx, cy = center
    half_w = width_mm / 2.0
    half_h = height_mm / 2.0
    points = [
        (cx - half_w, cy - half_h),
        (cx + half_w, cy - half_h),
        (cx + half_w, cy + half_h),
        (cx - half_w, cy + half_h),
    ]
    if not math.isclose(rotation_degrees, 0.0, abs_tol=1e-9):
        points = [_rotate_point(point, center, rotation_degrees) for point in points]
    return _Region(_Ring(points))


def _rounded_rectangle_region(
    center: tuple[float, float],
    width_mm: float,
    height_mm: float,
    radius_mm: float,
    rotation_degrees: float,
) -> _Region:
    radius = max(0.0, min(radius_mm, width_mm / 2.0, height_mm / 2.0))
    if radius <= 1e-9:
        return _rectangle_region(center=center, width_mm=width_mm, height_mm=height_mm, rotation_degrees=rotation_degrees)
    cx, cy = center
    half_w = width_mm / 2.0
    half_h = height_mm / 2.0
    centers = [
        (cx + half_w - radius, cy + half_h - radius),
        (cx - half_w + radius, cy + half_h - radius),
        (cx - half_w + radius, cy - half_h + radius),
        (cx + half_w - radius, cy - half_h + radius),
    ]
    points = [
        (cx + half_w, cy - half_h + radius),
        (cx + half_w, cy + half_h - radius),
        (cx + half_w - radius, cy + half_h),
        (cx - half_w + radius, cy + half_h),
        (cx - half_w, cy + half_h - radius),
        (cx - half_w, cy - half_h + radius),
        (cx - half_w + radius, cy - half_h),
        (cx + half_w - radius, cy - half_h),
    ]
    segments = [
        _Segment("line"),
        _Segment("arc", center=centers[0], sweep="ccw"),
        _Segment("line"),
        _Segment("arc", center=centers[1], sweep="ccw"),
        _Segment("line"),
        _Segment("arc", center=centers[2], sweep="ccw"),
        _Segment("line"),
        _Segment("arc", center=centers[3], sweep="ccw"),
    ]
    ring = _Ring(points, segments)
    if not math.isclose(rotation_degrees, 0.0, abs_tol=1e-9):
        ring = _rotate_ring(ring, center, rotation_degrees)
    return _Region(ring)


def _pad_shape_region(
    *,
    center: tuple[float, float],
    width_mm: float,
    height_mm: float,
    shape: int,
    rotation_degrees: float,
    corner_radius_percent: int,
) -> _Region:
    if shape == int(PadShape.CIRCLE):
        if math.isclose(width_mm, height_mm, rel_tol=1e-9, abs_tol=1e-9):
            return _circle_region(center, width_mm / 2.0)
        return _ellipse_region(center, width_mm / 2.0, height_mm / 2.0, rotation_degrees, 48)
    if shape == int(PadShape.OCTAGONAL):
        points = _octagon_points(center[0], center[1], width_mm / 2.0, height_mm / 2.0)
        if not math.isclose(rotation_degrees, 0.0, abs_tol=1e-9):
            points = [_rotate_point(point, center, rotation_degrees) for point in points]
        return _Region(_Ring(points))
    if shape == int(PadShape.ROUNDED_RECTANGLE):
        radius = (max(0, corner_radius_percent) / 100.0) * min(width_mm, height_mm) / 2.0
        return _rounded_rectangle_region(center, width_mm, height_mm, radius, rotation_degrees)
    return _rectangle_region(center=center, width_mm=width_mm, height_mm=height_mm, rotation_degrees=rotation_degrees)


def _outline_stroke_regions(vertices: list[BoardOutlineVertex], width_mm: float) -> list[_Region]:
    if len(vertices) < 2 or width_mm <= 0.0:
        return []
    regions: list[_Region] = []
    count = len(vertices)
    for idx, current in enumerate(vertices):
        nxt = vertices[(idx + 1) % count]
        start = (_mils_to_mm(current.x_mils), _mils_to_mm(current.y_mils))
        end = (_mils_to_mm(nxt.x_mils), _mils_to_mm(nxt.y_mils))
        if bool(getattr(current, "is_arc", False)) and float(getattr(current, "radius_mils", 0.0) or 0.0) > 0.0:
            clockwise, sweep = resolve_outline_arc_segment(current, nxt)
            start_angle = math.degrees(
                math.atan2(
                    current.y_mils - current.center_y_mils,
                    current.x_mils - current.center_x_mils,
                )
            )
            region = _arc_stroke_region(
                center=(_mils_to_mm(current.center_x_mils), _mils_to_mm(current.center_y_mils)),
                radius_mm=_mils_to_mm(current.radius_mils),
                start_degrees=start_angle,
                sweep_degrees=-sweep if clockwise else sweep,
                width_mm=width_mm,
            )
        else:
            region = _line_capsule_region(start, end, width_mm)
        if region is not None:
            regions.append(region)
    return regions


def _outline_ring(vertices: list[BoardOutlineVertex]) -> _Ring | None:
    if len(vertices) < 3:
        return None
    points: list[tuple[float, float]] = []
    segments: list[_Segment] = []
    count = len(vertices)
    for idx, current in enumerate(vertices):
        nxt = vertices[(idx + 1) % count]
        points.append((_mils_to_mm(current.x_mils), _mils_to_mm(current.y_mils)))
        if bool(getattr(current, "is_arc", False)) and float(getattr(current, "radius_mils", 0.0) or 0.0) > 0.0:
            clockwise, _sweep = resolve_outline_arc_segment(current, nxt)
            segments.append(
                _Segment(
                    "arc",
                    center=(_mils_to_mm(current.center_x_mils), _mils_to_mm(current.center_y_mils)),
                    sweep="cw" if clockwise else "ccw",
                )
            )
        else:
            segments.append(_Segment("line"))
    return _Ring(points, segments)


def _extended_vertices_ring(vertices: list[Any]) -> _Ring | None:
    if len(vertices) < 3:
        return None
    points: list[tuple[float, float]] = []
    segments: list[_Segment] = []
    count = len(vertices)
    for idx, current in enumerate(vertices):
        nxt = vertices[(idx + 1) % count]
        points.append((_mils_to_mm(float(current.x_mils)), _mils_to_mm(float(current.y_mils))))
        if bool(getattr(current, "is_round", False)) and float(getattr(current, "radius_mils", 0.0) or 0.0) > 0.0:
            raw_delta = float(getattr(current, "end_angle", 0.0) or 0.0) - float(
                getattr(current, "start_angle", 0.0) or 0.0
            )
            current_point = (float(current.x_mils), float(current.y_mils))
            next_point = (float(nxt.x_mils), float(nxt.y_mils))
            sweep = _svg_like_board_sweep_degrees(
                center_mils=(float(current.center_x_mils), float(current.center_y_mils)),
                radius_mils=float(current.radius_mils),
                start_point_mils=current_point,
                end_point_mils=next_point,
                start_degrees=float(getattr(current, "start_angle", 0.0) or 0.0),
                end_degrees=float(getattr(current, "end_angle", 0.0) or 0.0),
                default_sweep_flag=1 if raw_delta >= 0.0 else 0,
            )
            segments.append(
                _Segment(
                    "arc",
                    center=(_mils_to_mm(float(current.center_x_mils)), _mils_to_mm(float(current.center_y_mils))),
                    sweep="ccw" if sweep > 0.0 else "cw",
                )
            )
        else:
            segments.append(_Segment("line"))
    return _Ring(points, segments)


def _rotate_point(
    point: tuple[float, float],
    origin: tuple[float, float],
    rotation_degrees: float,
) -> tuple[float, float]:
    if math.isclose(rotation_degrees, 0.0, abs_tol=1e-12):
        return point
    angle = math.radians(rotation_degrees)
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    px, py = point
    ox, oy = origin
    dx = px - ox
    dy = py - oy
    return (ox + dx * cos_a - dy * sin_a, oy + dx * sin_a + dy * cos_a)


def _rotate_ring(ring: _Ring, origin: tuple[float, float], rotation_degrees: float) -> _Ring:
    segments = [
        _Segment(
            kind=segment.kind,
            center=_rotate_point(segment.center, origin, rotation_degrees)
            if segment.center is not None
            else None,
            sweep=segment.sweep,
        )
        for segment in ring.segments
    ]
    return _Ring([_rotate_point(point, origin, rotation_degrees) for point in ring.points], segments)


def _sample_arc_points_mils(
    *,
    center_mils: tuple[float, float],
    radius_mils: float,
    start_degrees: float,
    end_degrees: float,
    arc_segments: int,
) -> list[tuple[float, float]]:
    if radius_mils <= 0.0:
        return []
    raw_delta = end_degrees - start_degrees
    sweep = _normalize_signed_sweep(raw_delta)
    return _sample_arc_points_for_sweep_mils(
        center_mils=center_mils,
        radius_mils=radius_mils,
        start_degrees=start_degrees,
        sweep_degrees=sweep,
        raw_delta_degrees=raw_delta,
        arc_segments=arc_segments,
    )


def _sample_svg_arc_points_mils(
    *,
    center_mils: tuple[float, float],
    radius_mils: float,
    start_point_mils: tuple[float, float],
    end_point_mils: tuple[float, float],
    start_degrees: float,
    end_degrees: float,
    default_sweep_flag: int,
    arc_segments: int,
) -> list[tuple[float, float]]:
    if radius_mils <= 0.0:
        return []
    raw_delta = end_degrees - start_degrees
    sweep = _svg_like_board_sweep_degrees(
        center_mils=center_mils,
        radius_mils=radius_mils,
        start_point_mils=start_point_mils,
        end_point_mils=end_point_mils,
        start_degrees=start_degrees,
        end_degrees=end_degrees,
        default_sweep_flag=default_sweep_flag,
    )
    start_angle = math.degrees(
        math.atan2(
            start_point_mils[1] - center_mils[1],
            start_point_mils[0] - center_mils[0],
        )
    )
    points = _sample_arc_points_for_sweep_mils(
        center_mils=center_mils,
        radius_mils=radius_mils,
        start_degrees=start_angle,
        sweep_degrees=sweep,
        raw_delta_degrees=raw_delta,
        arc_segments=arc_segments,
    )
    if not points:
        return []
    points[0] = start_point_mils
    points[-1] = end_point_mils
    return points


def _svg_like_board_sweep_degrees(
    *,
    center_mils: tuple[float, float],
    radius_mils: float,
    start_point_mils: tuple[float, float],
    end_point_mils: tuple[float, float],
    start_degrees: float,
    end_degrees: float,
    default_sweep_flag: int,
) -> float:
    raw_delta = end_degrees - start_degrees
    sweep_ccw = (end_degrees - start_degrees) % 360.0
    if math.isclose(sweep_ccw, 0.0, abs_tol=1e-9) and not math.isclose(raw_delta, 0.0, abs_tol=1e-9):
        return 360.0 if raw_delta >= 0.0 else -360.0
    large_arc_int = 1 if sweep_ccw > 180.0 else 0

    sx, sy = start_point_mils
    ex, ey = end_point_mils
    cx, cy = center_mils
    sweep_flag = choose_svg_sweep_flag_for_center(
        sx,
        -sy,
        ex,
        -ey,
        radius_mils,
        large_arc_int,
        cx,
        -cy,
        default_sweep_flag=default_sweep_flag,
    )
    svg_sweep = _signed_svg_sweep_degrees(
        start_point=(sx, -sy),
        end_point=(ex, -ey),
        center=(cx, -cy),
        sweep_flag=sweep_flag,
    )
    return -svg_sweep


def _signed_svg_sweep_degrees(
    *,
    start_point: tuple[float, float],
    end_point: tuple[float, float],
    center: tuple[float, float],
    sweep_flag: int,
) -> float:
    sx, sy = start_point
    ex, ey = end_point
    cx, cy = center
    start = math.degrees(math.atan2(sy - cy, sx - cx))
    end = math.degrees(math.atan2(ey - cy, ex - cx))
    delta = (end - start) % 360.0
    if int(sweep_flag):
        return 360.0 if math.isclose(delta, 0.0, abs_tol=1e-9) else delta
    return -360.0 if math.isclose(delta, 0.0, abs_tol=1e-9) else delta - 360.0


def _sample_arc_points_for_sweep_mils(
    *,
    center_mils: tuple[float, float],
    radius_mils: float,
    start_degrees: float,
    sweep_degrees: float,
    raw_delta_degrees: float,
    arc_segments: int,
) -> list[tuple[float, float]]:
    sweep = sweep_degrees
    if math.isclose(sweep, 0.0, abs_tol=1e-9) and not math.isclose(raw_delta_degrees, 0.0, abs_tol=1e-9):
        sweep = 360.0 if raw_delta_degrees >= 0.0 else -360.0
    samples = max(2, int(math.ceil(max(abs(sweep), 1.0) / 360.0 * max(8, arc_segments))) + 1)
    cx, cy = center_mils
    return [
        (
            cx + radius_mils * math.cos(math.radians(start_degrees + sweep * idx / (samples - 1))),
            cy + radius_mils * math.sin(math.radians(start_degrees + sweep * idx / (samples - 1))),
        )
        for idx in range(samples)
    ]


def _normalize_signed_sweep(raw_delta: float) -> float:
    if raw_delta >= 0.0:
        return raw_delta % 360.0
    return -((-raw_delta) % 360.0)


def _arc_point_from_angle_mils(
    center_mils: tuple[float, float], radius_mils: float, angle_degrees: float
) -> tuple[float, float]:
    cx, cy = center_mils
    return (
        cx + radius_mils * math.cos(math.radians(angle_degrees)),
        cy + radius_mils * math.sin(math.radians(angle_degrees)),
    )


def _arc_point_from_angle_mm(
    center_mm: tuple[float, float], radius_mm: float, angle_degrees: float
) -> tuple[float, float]:
    cx, cy = center_mm
    return (
        cx + radius_mm * math.cos(math.radians(angle_degrees)),
        cy + radius_mm * math.sin(math.radians(angle_degrees)),
    )


def _pad_should_render_on_layer(pad: Any, layer: PcbLayer) -> bool:
    try:
        return bool(pad._should_render_on_layer(layer)) or bool(
            pad._should_force_svg_copper_render(layer)
        )
    except Exception:
        source_layer = int(getattr(pad, "layer", 0) or 0)
        if source_layer == PcbLayer.MULTI_LAYER.value and layer.is_copper():
            return True
        return source_layer == layer.value


def _via_spans_layer(via: Any, layer: PcbLayer) -> bool:
    start = int(getattr(via, "layer_start", PcbLayer.TOP.value) or PcbLayer.TOP.value)
    end = int(getattr(via, "layer_end", PcbLayer.BOTTOM.value) or PcbLayer.BOTTOM.value)
    low = min(start, end)
    high = max(start, end)
    return low <= layer.value <= high


def _via_pad_removed_on_layer(via: Any, layer: PcbLayer) -> bool:
    idx = layer.value - 1
    removed = getattr(via, "is_pad_removed", []) or []
    return 0 <= idx < len(removed) and bool(removed[idx])


def _via_diameter_iu(via: Any, layer: PcbLayer) -> int:
    idx = layer.value - 1
    diameters = getattr(via, "diameter_by_layer", []) or []
    if 0 <= idx < len(diameters) and int(diameters[idx] or 0) > 0:
        return int(diameters[idx])
    return int(getattr(via, "diameter", 0) or 0)


def _pad_corner_radius_percent(pad: Any, layer: PcbLayer) -> int:
    idx = layer.value - 1
    corner_radius = getattr(pad, "corner_radius", []) or []
    if 0 <= idx < len(corner_radius) and int(corner_radius[idx] or 0) > 0:
        return int(corner_radius[idx])
    return int(getattr(pad, "corner_radius_percentage", 0) or 0)


def _is_poured_polygon_primitive(primitive: Any) -> bool:
    if bool(getattr(primitive, "is_polygon_outline", False)):
        return True
    polygon_index = getattr(primitive, "polygon_index", None)
    try:
        polygon_index_int = int(polygon_index)
    except (TypeError, ValueError):
        return False
    return polygon_index_int not in {0, 0xFFFF}


def _octagon_points(cx: float, cy: float, half_w: float, half_h: float) -> list[tuple[float, float]]:
    chamfer = min(half_w, half_h) / 2.0
    return [
        (cx + half_w, cy - (half_h - chamfer)),
        (cx + half_w, cy + half_h - chamfer),
        (cx + half_w - chamfer, cy + half_h),
        (cx - (half_w - chamfer), cy + half_h),
        (cx - half_w, cy + half_h - chamfer),
        (cx - half_w, cy - (half_h - chamfer)),
        (cx - (half_w - chamfer), cy - half_h),
        (cx + half_w - chamfer, cy - half_h),
    ]


def _mils_to_mm(value: float) -> float:
    return float(value) * MIL_TO_MM


def _iu_to_mils(value: Any) -> float:
    return float(value or 0.0) / INTERNAL_UNITS_PER_MIL


def _points_close(a: tuple[float, float], b: tuple[float, float], tol: float = 1e-9) -> bool:
    return math.isclose(a[0], b[0], abs_tol=tol) and math.isclose(a[1], b[1], abs_tol=tol)


def _dedupe_closed_points(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    deduped: list[tuple[float, float]] = []
    for x, y in points:
        point = (float(x), float(y))
        if deduped and _points_close(deduped[-1], point):
            continue
        deduped.append(point)
    if len(deduped) > 1 and _points_close(deduped[0], deduped[-1]):
        deduped.pop()
    return deduped


def _board_name_from_pcbdoc(pcbdoc: Any) -> str:
    filepath = getattr(pcbdoc, "filepath", None)
    if filepath:
        return Path(filepath).stem
    return "board"


def _step_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]+", "_", value).strip("_") or "board"


def layer_step_output_name(board_name: str, layer: PcbLayer) -> str:
    """Return the conventional filename for one generated layer STEP artifact."""
    layer_name = re.sub(r"[^A-Za-z0-9]+", "_", layer.to_json_name().lower()).strip("_")
    return f"{_step_name(board_name)}__{layer_name}_layer.step"
