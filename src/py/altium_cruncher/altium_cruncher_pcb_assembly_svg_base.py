"""Altium PCB surface/assembly SVG rendering helpers."""

from __future__ import annotations

from dataclasses import dataclass
import html
import math
import re

from typing import TYPE_CHECKING, Any

from altium_monkey.altium_pcb_surface import (
    PCB_SurfaceRole,
    PCB_SurfaceSide,
    pcb_surface_layers,
)
from altium_monkey.altium_pcb_svg_renderer import (
    PcbSvgRenderer,
    PcbSvgRenderOptions,
    _MIL_TO_MM,
)
from altium_monkey.altium_record_types import PcbLayer

from altium_cruncher.altium_cruncher_pcb_assembly_model_helper import (
    PcbAssemblyModelHelper,
)
from altium_cruncher.altium_cruncher_pcb_workflow import iter_pcb_render_inputs
from altium_cruncher.altium_cruncher_pcb_svg_assembly_projection import (
    AssemblyProjectionOptions,
    get_assembly_projection_cache,
)

if TYPE_CHECKING:
    from altium_monkey.altium_design import AltiumDesign
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc
    from altium_monkey.altium_pcb_svg_renderer import PcbSvgRenderContext


@dataclass
class CruncherPcbAssemblySvgRenderOptions(PcbSvgRenderOptions):
    """PCB SVG options including assembly overlay controls."""

    include_assembly_overlay: bool = False
    assembly_view_side: str | None = None
    assembly_include_simple: bool = True
    assembly_include_detail: bool = True
    assembly_curve_mode: str = "native_arcs"
    assembly_samples_per_curve: int = 24
    assembly_round_digits: int = 3
    assembly_include_visible: bool = True
    assembly_include_outline: bool = True
    assembly_union_polygons: bool = True
    assembly_overlay_color: str = "#F59E0B"


class CruncherPcbAssemblySvgRenderer(PcbSvgRenderer):
    """PCB renderer that can emit assembly overlays."""

    def _get_model_helper(self):
        if getattr(self, "_assembly_model_helper", None) is None:
            self._assembly_model_helper = PcbAssemblyModelHelper()
        return self._assembly_model_helper

    @staticmethod
    def _assembly_projection_types():
        return AssemblyProjectionOptions, get_assembly_projection_cache

    def _render_overlay_defs_scene(self, ctx, pcbdoc):
        if not self.options.include_assembly_overlay:
            return [], []
        return self._render_assembly_overlay(ctx, pcbdoc)

    @staticmethod
    def _safe_svg_token(raw: str, *, fallback: str) -> str:
        text = (raw or "").strip()
        if not text:
            return fallback
        token = re.sub(r"[^0-9A-Za-z_.-]+", "_", text).strip("._-")
        return token or fallback

    @staticmethod
    def _assembly_canonical_angle_deg(value: float) -> float:
        angle = math.fmod(float(value), 360.0)
        if angle <= -180.0:
            angle += 360.0
        elif angle > 180.0:
            angle -= 360.0
        if math.isclose(angle, -180.0, abs_tol=1e-9):
            angle = 180.0
        if math.isclose(angle, 0.0, abs_tol=1e-9):
            angle = 0.0
        return round(float(angle), 6)

    def _fmt_local_mm(self, value: float) -> str:
        return f"{float(value):.{self.options.precision}f}".rstrip("0").rstrip(".")

    def _assembly_component_anchor_mils(
        self,
        helper,
        component_obj: object | None,
        props: dict[str, object],
    ) -> tuple[float | None, float | None]:
        comp_x_mils = None
        comp_y_mils = None
        if component_obj is not None:
            comp_x_mils = helper._parse_altium_mils(
                getattr(component_obj, "x", None),
                assume_internal_units=False,
                default=None,
            )
            comp_y_mils = helper._parse_altium_mils(
                getattr(component_obj, "y", None),
                assume_internal_units=False,
                default=None,
            )
        if comp_x_mils is None or comp_y_mils is None:
            comp_x_mils = helper._parse_altium_mils(
                props.get("MODEL.2D.X"),
                assume_internal_units=False,
                default=None,
            )
            comp_y_mils = helper._parse_altium_mils(
                props.get("MODEL.2D.Y"),
                assume_internal_units=False,
                default=None,
            )
        return comp_x_mils, comp_y_mils

    def _assembly_build_instance_transform(
        self,
        ctx: PcbSvgRenderContext,
        *,
        side: str,
        instance_x_mils: float,
        instance_y_mils: float,
        component_rotation_deg: float,
    ) -> tuple[float, float, float, str]:
        tx = ctx.x_to_svg(float(instance_x_mils))
        ty = ctx.y_to_svg(float(instance_y_mils))
        instance_rotation_deg = -90.0 - float(component_rotation_deg)
        transform_value = f"translate({ctx.fmt(tx)} {ctx.fmt(ty)})"
        if not math.isclose(instance_rotation_deg, 0.0, abs_tol=1e-9):
            transform_value += f" rotate({ctx.fmt(instance_rotation_deg)})"
        if side == "bottom":
            # Keep local Y reflection as rightmost transform so it executes first.
            transform_value += " scale(1 -1)"
        return tx, ty, instance_rotation_deg, transform_value

    def _assembly_world_svg_mm_to_local_up_mm(
        self,
        *,
        side: str,
        world_x_svg_mm: float,
        world_y_svg_mm: float,
        tx_svg_mm: float,
        ty_svg_mm: float,
        instance_rotation_deg: float,
    ) -> tuple[float, float]:
        dx = float(world_x_svg_mm) - float(tx_svg_mm)
        dy = float(world_y_svg_mm) - float(ty_svg_mm)
        rot_inv_rad = math.radians(-float(instance_rotation_deg))
        cos_r = math.cos(rot_inv_rad)
        sin_r = math.sin(rot_inv_rad)
        local_svg_x = (dx * cos_r) - (dy * sin_r)
        local_svg_y = (dx * sin_r) + (dy * cos_r)
        if side == "bottom":
            local_svg_y = -local_svg_y
        # _assembly_geometry_elements_local expects local Y-up coordinates.
        return local_svg_x, -local_svg_y

    def _assembly_board_mm_to_local_up_mm(
        self,
        ctx: PcbSvgRenderContext,
        *,
        side: str,
        x_mm: float,
        y_mm: float,
        tx_svg_mm: float,
        ty_svg_mm: float,
        instance_rotation_deg: float,
    ) -> tuple[float, float]:
        x_mils = float(x_mm) / _MIL_TO_MM
        y_mils = float(y_mm) / _MIL_TO_MM
        world_x_svg_mm = ctx.x_to_svg(x_mils)
        world_y_svg_mm = ctx.y_to_svg(y_mils)
        return self._assembly_world_svg_mm_to_local_up_mm(
            side=side,
            world_x_svg_mm=world_x_svg_mm,
            world_y_svg_mm=world_y_svg_mm,
            tx_svg_mm=tx_svg_mm,
            ty_svg_mm=ty_svg_mm,
            instance_rotation_deg=instance_rotation_deg,
        )

    def _assembly_coords_to_local_segments(
        self,
        ctx: PcbSvgRenderContext,
        *,
        side: str,
        coords: list[tuple[float, float]],
        tx_svg_mm: float,
        ty_svg_mm: float,
        instance_rotation_deg: float,
    ) -> list[tuple[tuple[float, float], tuple[float, float]]]:
        if len(coords) < 2:
            return []
        local_segments: list[tuple[tuple[float, float], tuple[float, float]]] = []
        for coord_idx in range(len(coords) - 1):
            x1_mm, y1_mm = float(coords[coord_idx][0]), float(coords[coord_idx][1])
            x2_mm, y2_mm = float(coords[coord_idx + 1][0]), float(coords[coord_idx + 1][1])
            if math.isclose(x1_mm, x2_mm, abs_tol=1e-12) and math.isclose(y1_mm, y2_mm, abs_tol=1e-12):
                continue
            p1 = self._assembly_board_mm_to_local_up_mm(
                ctx,
                side=side,
                x_mm=x1_mm,
                y_mm=y1_mm,
                tx_svg_mm=tx_svg_mm,
                ty_svg_mm=ty_svg_mm,
                instance_rotation_deg=instance_rotation_deg,
            )
            p2 = self._assembly_board_mm_to_local_up_mm(
                ctx,
                side=side,
                x_mm=x2_mm,
                y_mm=y2_mm,
                tx_svg_mm=tx_svg_mm,
                ty_svg_mm=ty_svg_mm,
                instance_rotation_deg=instance_rotation_deg,
            )
            local_segments.append((p1, p2))
        return local_segments

    @staticmethod
    def _assembly_component_layer_is_bottom(component_obj: object | None) -> bool:
        if component_obj is None:
            return False
        layer_text = str(getattr(component_obj, "layer", "") or "").upper()
        if "BOTTOM" in layer_text:
            return True
        if "TOP" in layer_text:
            return False
        return False

    @staticmethod
    def _assembly_dedupe_local_segments(
        segments: list[tuple[tuple[float, float], tuple[float, float]]],
        *,
        round_digits: int,
    ) -> tuple[tuple[tuple[float, float], tuple[float, float]], ...]:
        deduped: list[tuple[tuple[float, float], tuple[float, float]]] = []
        seen: set[tuple[tuple[float, float], tuple[float, float]]] = set()
        for (x1, y1), (x2, y2) in segments:
            p1 = (round(float(x1), round_digits), round(float(y1), round_digits))
            p2 = (round(float(x2), round_digits), round(float(y2), round_digits))
            if p1 == p2:
                continue
            key = (p1, p2) if p1 <= p2 else (p2, p1)
            if key in seen:
                continue
            seen.add(key)
            deduped.append(((float(p1[0]), float(p1[1])), (float(p2[0]), float(p2[1]))))
        return tuple(deduped)

    @staticmethod
    def _assembly_segment_signature_key(
        segments: tuple[tuple[tuple[float, float], tuple[float, float]], ...],
        *,
        round_digits: int,
    ) -> tuple[float, ...]:
        signature: list[float] = []
        for (x1, y1), (x2, y2) in segments:
            signature.extend(
                [
                    round(float(x1), round_digits),
                    round(float(y1), round_digits),
                    round(float(x2), round_digits),
                    round(float(y2), round_digits),
                ]
            )
        return tuple(signature)

    def _assembly_component_copper_bbox_mils(
        self,
        pcbdoc: "AltiumPcbDoc",
        *,
        component_index: int,
    ) -> tuple[float, float, float, float] | None:
        min_x: float | None = None
        min_y: float | None = None
        max_x: float | None = None
        max_y: float | None = None

        def _update(x_val: float, y_val: float) -> None:
            nonlocal min_x, min_y, max_x, max_y
            min_x = x_val if min_x is None else min(min_x, x_val)
            min_y = y_val if min_y is None else min(min_y, y_val)
            max_x = x_val if max_x is None else max(max_x, x_val)
            max_y = y_val if max_y is None else max(max_y, y_val)

        def _update_bbox(x0: float, y0: float, x1: float, y1: float) -> None:
            _update(float(x0), float(y0))
            _update(float(x1), float(y1))

        for pad in list(getattr(pcbdoc, "pads", []) or []):
            if int(getattr(pad, "component_index", -1) or -1) != int(component_index):
                continue
            x_pad = float(getattr(pad, "x_mils", 0.0))
            y_pad = float(getattr(pad, "y_mils", 0.0))
            width_mils = max(
                float(getattr(pad, "top_width", 0.0)) / 10000.0,
                float(getattr(pad, "mid_width", 0.0)) / 10000.0,
                float(getattr(pad, "bot_width", 0.0)) / 10000.0,
                0.1,
            )
            height_mils = max(
                float(getattr(pad, "top_height", 0.0)) / 10000.0,
                float(getattr(pad, "mid_height", 0.0)) / 10000.0,
                float(getattr(pad, "bot_height", 0.0)) / 10000.0,
                0.1,
            )
            half_w = width_mils * 0.5
            half_h = height_mils * 0.5
            _update_bbox(x_pad - half_w, y_pad - half_h, x_pad + half_w, y_pad + half_h)

        for track in list(getattr(pcbdoc, "tracks", []) or []):
            if int(getattr(track, "component_index", -1) or -1) != int(component_index):
                continue
            half_width = max(float(getattr(track, "width_mils", 0.0)) * 0.5, 0.1)
            sx = float(getattr(track, "start_x_mils", 0.0))
            sy = float(getattr(track, "start_y_mils", 0.0))
            ex = float(getattr(track, "end_x_mils", 0.0))
            ey = float(getattr(track, "end_y_mils", 0.0))
            _update_bbox(sx - half_width, sy - half_width, sx + half_width, sy + half_width)
            _update_bbox(ex - half_width, ey - half_width, ex + half_width, ey + half_width)

        for arc in list(getattr(pcbdoc, "arcs", []) or []):
            if int(getattr(arc, "component_index", -1) or -1) != int(component_index):
                continue
            radius = max(
                float(getattr(arc, "radius_mils", 0.0)) + max(float(getattr(arc, "width_mils", 0.0)) * 0.5, 0.1),
                0.1,
            )
            cx = float(getattr(arc, "center_x_mils", 0.0))
            cy = float(getattr(arc, "center_y_mils", 0.0))
            _update_bbox(cx - radius, cy - radius, cx + radius, cy + radius)

        for fill in list(getattr(pcbdoc, "fills", []) or []):
            if int(getattr(fill, "component_index", -1) or -1) != int(component_index):
                continue
            x1 = float(getattr(fill, "pos1_x_mils", 0.0))
            y1 = float(getattr(fill, "pos1_y_mils", 0.0))
            x2 = float(getattr(fill, "pos2_x_mils", 0.0))
            y2 = float(getattr(fill, "pos2_y_mils", 0.0))
            _update_bbox(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))

        for region in list(getattr(pcbdoc, "regions", []) or []):
            if int(getattr(region, "component_index", -1) or -1) != int(component_index):
                continue
            for vertex in list(getattr(region, "outline_vertices", []) or []):
                _update(float(getattr(vertex, "x_mils", 0.0)), float(getattr(vertex, "y_mils", 0.0)))

        for shape_region in list(getattr(pcbdoc, "shapebased_regions", []) or []):
            if int(getattr(shape_region, "component_index", -1) or -1) != int(component_index):
                continue
            for vertex in list(getattr(shape_region, "outline", []) or []):
                _update(float(getattr(vertex, "x_mils", 0.0)), float(getattr(vertex, "y_mils", 0.0)))

        if min_x is None or min_y is None or max_x is None or max_y is None:
            return None
        return float(min_x), float(min_y), float(max_x), float(max_y)

    def _render_assembly_overlay(
        self,
        ctx: PcbSvgRenderContext,
        pcbdoc: "AltiumPcbDoc",
    ) -> tuple[list[str], list[str]]:
        side = str(self.options.assembly_view_side or "").strip().lower()
        if side not in {"top", "bottom"}:
            return [], []
        emit_simple = bool(self.options.assembly_include_simple)
        emit_detail = bool(self.options.assembly_include_detail)
        if not (emit_simple or emit_detail):
            return [], []
        available_mode_tokens: list[str] = []
        if emit_simple:
            available_mode_tokens.append("simple")
        if emit_detail:
            available_mode_tokens.append("detail")
        available_modes_text = " ".join(available_mode_tokens)
        default_mode = "detail" if emit_detail else "simple"

        curve_mode = str(self.options.assembly_curve_mode or "").strip().lower()
        if curve_mode not in {"native_arcs", "polyline"}:
            curve_mode = "native_arcs"
        samples_per_curve = max(int(self.options.assembly_samples_per_curve), 2)
        round_digits = max(int(self.options.assembly_round_digits), 0)

        AssemblyProjectionOptions, get_assembly_projection_cache = self._assembly_projection_types()
        helper = self._get_model_helper()
        projection_cache = get_assembly_projection_cache()

        model_catalog, _discovery = helper._collect_embedded_step_model_catalog(pcbdoc)

        models_by_id: dict[str, list[dict[str, object]]] = {}
        models_by_name: dict[str, list[dict[str, object]]] = {}
        for entry in model_catalog:
            model_id_norm = str(entry.get("id_norm", "") or "")
            if model_id_norm:
                models_by_id.setdefault(model_id_norm, []).append(entry)
            model_name_norm = str(entry.get("name_norm", "") or "")
            if model_name_norm:
                models_by_name.setdefault(model_name_norm, []).append(entry)

        projection_options = AssemblyProjectionOptions(
            side="bottom" if side == "bottom" else "top",
            curve_mode="polyline" if curve_mode == "polyline" else "native_arcs",
            samples_per_curve=samples_per_curve,
            round_digits=round_digits,
            include_visible=bool(self.options.assembly_include_visible),
            include_outline=bool(self.options.assembly_include_outline),
            union_polygons=bool(self.options.assembly_union_polygons),
        )

        components = list(getattr(pcbdoc, "components", []) or [])
        symbol_ids_by_key: dict[tuple[object, ...], tuple[str, str]] = {}
        defs_lines: list[str] = []
        scene_lines: list[str] = []
        instance_count = 0
        unique_projection_count = 0
        component_had_body_on_side: set[int] = set()
        component_emitted_geometry: set[int] = set()
        extruded_bodies_by_component: dict[int, list[tuple[int, object, dict[str, object]]]] = {}
        free_extruded_bodies: list[tuple[int, object, dict[str, object], float, float, float]] = []

        class _ProjectedLines:
            __slots__ = (
                "simple_line_segments",
                "simple_arcs",
                "detail_line_segments",
                "detail_arcs",
            )

            def __init__(
                self,
                *,
                simple_line_segments: tuple[tuple[tuple[float, float], tuple[float, float]], ...],
                detail_line_segments: tuple[tuple[tuple[float, float], tuple[float, float]], ...],
            ) -> None:
                self.simple_line_segments = simple_line_segments
                self.simple_arcs = tuple()
                self.detail_line_segments = detail_line_segments
                self.detail_arcs = tuple()

            @property
            def is_empty(self) -> bool:
                return (not self.simple_line_segments) and (not self.detail_line_segments)

        for body_idx, body in enumerate(list(getattr(pcbdoc, "component_bodies", []) or [])):
            props = dict(getattr(body, "properties", {}) or {})
            model_id_text = str(props.get("MODELID", "") or "").strip()
            model_name_text = str(props.get("MODEL.NAME", "") or "").strip()

            model_entry = helper._resolve_component_body_model_entry(
                props,
                models_by_id=models_by_id,
                models_by_name=models_by_name,
            ) if (model_id_text or model_name_text) else None

            comp_idx_raw = getattr(body, "component_index", -1)
            try:
                comp_idx = int(comp_idx_raw)
            except (TypeError, ValueError):
                comp_idx = -1
            component = components[comp_idx] if 0 <= comp_idx < len(components) else None
            component_rotation_deg = 0.0
            if component is not None:
                component_rotation_deg = helper._parse_altium_float(
                    getattr(component, "rotation", None),
                    default=0.0,
                )
            is_bottom = bool(helper._component_body_is_bottom(props, component))
            if side == "top" and is_bottom:
                continue
            if side == "bottom" and not is_bottom:
                continue
            if comp_idx >= 0:
                component_had_body_on_side.add(comp_idx)

            if model_entry is None:
                model_type = helper._parse_altium_int(props.get("MODEL.MODELTYPE"))
                if model_type == 0:
                    if comp_idx >= 0:
                        extruded_bodies_by_component.setdefault(comp_idx, []).append((body_idx, body, props))
                    else:
                        anchor_x, anchor_y = self._assembly_component_anchor_mils(helper, component, props)
                        if anchor_x is None or anchor_y is None:
                            body_geometry = helper._component_body_polygon_mm(body)
                            if body_geometry is not None and not body_geometry.is_empty:
                                centroid = body_geometry.centroid
                                anchor_x = float(centroid.x) / _MIL_TO_MM
                                anchor_y = float(centroid.y) / _MIL_TO_MM
                        if anchor_x is not None and anchor_y is not None:
                            free_extruded_bodies.append(
                                (
                                    body_idx,
                                    body,
                                    props,
                                    float(anchor_x),
                                    float(anchor_y),
                                    float(component_rotation_deg),
                                )
                            )
                continue

            model_anchor_x_mils = helper._parse_altium_mils(
                props.get("MODEL.2D.X"),
                assume_internal_units=False,
                default=None,
            )
            model_anchor_y_mils = helper._parse_altium_mils(
                props.get("MODEL.2D.Y"),
                assume_internal_units=False,
                default=None,
            )
            component_x_mils = None
            component_y_mils = None
            if component is not None:
                component_x_mils = helper._parse_altium_mils(
                    getattr(component, "x", None),
                    assume_internal_units=False,
                    default=None,
                )
                component_y_mils = helper._parse_altium_mils(
                    getattr(component, "y", None),
                    assume_internal_units=False,
                    default=None,
                )

            local_offset_x_mils = 0.0
            local_offset_y_mils = 0.0
            if component_x_mils is not None and component_y_mils is not None:
                # Component body MODEL.2D.X/Y can include body-local offsets relative
                # to the owning component placement. Keep instance placement anchored
                # to component origin and apply body-local offset in model space.
                instance_x_mils = float(component_x_mils)
                instance_y_mils = float(component_y_mils)
                if model_anchor_x_mils is not None and model_anchor_y_mils is not None:
                    delta_x_mils = float(model_anchor_x_mils) - float(component_x_mils)
                    delta_y_mils = float(model_anchor_y_mils) - float(component_y_mils)
                    # Imported/original-library bodies often store MODEL.2D.X/Y in
                    # board-space after component rotation. Normalize to body-local
                    # offsets so identical footprints reuse the same projection.
                    rot_rad = math.radians(float(component_rotation_deg))
                    cos_r = math.cos(rot_rad)
                    sin_r = math.sin(rot_rad)
                    local_offset_x_mils = (delta_x_mils * cos_r) + (delta_y_mils * sin_r)
                    local_offset_y_mils = (-delta_x_mils * sin_r) + (delta_y_mils * cos_r)
            elif model_anchor_x_mils is not None and model_anchor_y_mils is not None:
                instance_x_mils = float(model_anchor_x_mils)
                instance_y_mils = float(model_anchor_y_mils)
            else:
                continue

            model_2d_rotation_deg = helper._parse_altium_float(props.get("MODEL.2D.ROTATION"), default=0.0)
            model_rotx_deg = helper._parse_altium_float(props.get("MODEL.3D.ROTX"), default=0.0)
            model_roty_deg = helper._parse_altium_float(props.get("MODEL.3D.ROTY"), default=0.0)
            model_rotz_raw = props.get("MODEL.3D.ROTZ")
            model_rotz_deg = helper._parse_altium_float(model_rotz_raw, default=0.0)
            model_rotz_present = bool(str(model_rotz_raw or "").strip().strip("\x00"))
            if component is not None:
                if model_rotz_present:
                    # MODEL.3D.ROTZ is frequently instance-space in imported designs.
                    # Recover body-local Z rotation from instance-space encoding.
                    # Top and bottom assembly views use opposite composition signs.
                    if side == "bottom":
                        model_rotz_deg = float(model_rotz_deg) + float(component_rotation_deg)
                    else:
                        model_rotz_deg = float(model_rotz_deg) - float(component_rotation_deg)
                else:
                    # If ROTZ is absent, treat per-instance rotation as component-level.
                    model_rotz_deg = 0.0

            model_2d_rotation_deg = self._assembly_canonical_angle_deg(model_2d_rotation_deg)
            model_rotx_deg = self._assembly_canonical_angle_deg(model_rotx_deg)
            model_roty_deg = self._assembly_canonical_angle_deg(model_roty_deg)
            model_rotz_deg = self._assembly_canonical_angle_deg(model_rotz_deg)
            pose_signature = (
                model_2d_rotation_deg,
                model_rotx_deg,
                model_roty_deg,
                model_rotz_deg,
                round(float(local_offset_x_mils), 6),
                round(float(local_offset_y_mils), 6),
                1.0 if is_bottom else 0.0,
            )
            transform_matrix = helper._compose_step_component_transform(
                x_mm=float(local_offset_x_mils) * _MIL_TO_MM,
                y_mm=float(local_offset_y_mils) * _MIL_TO_MM,
                z_mm=0.0,
                model_2d_rotation_deg=model_2d_rotation_deg,
                model_rotx_deg=model_rotx_deg,
                model_roty_deg=model_roty_deg,
                model_rotz_deg=model_rotz_deg,
                is_bottom=is_bottom,
            )
            cache_key, projected = projection_cache.project(
                model_hash=str(model_entry.get("hash", "") or ""),
                step_bytes=bytes(model_entry.get("step_bytes", b"") or b""),
                pose_signature=pose_signature,
                transform_matrix=transform_matrix,
                options=projection_options,
                model_label=str(model_entry.get("name", "") or model_name_text or model_id_text or ""),
            )
            if projected.is_empty:
                continue

            symbol_ids = symbol_ids_by_key.get(cache_key)
            if symbol_ids is None:
                base_id = f"assembly-proj-{len(symbol_ids_by_key):04d}"
                simple_id = f"{base_id}-simple"
                detail_id = f"{base_id}-detail"
                defs_lines.extend(
                    self._build_assembly_symbol_defs(
                        simple_id=simple_id,
                        detail_id=detail_id,
                        projected=projected,
                    )
                )
                symbol_ids = (simple_id, detail_id)
                symbol_ids_by_key[cache_key] = symbol_ids
                unique_projection_count += 1

            simple_id, detail_id = symbol_ids
            designator = ""
            if component is not None:
                designator = str(getattr(component, "designator", "") or "").strip()
            if not designator and comp_idx in ctx.component_designator_by_index:
                designator = str(ctx.component_designator_by_index.get(comp_idx) or "").strip()
            token = self._safe_svg_token(designator, fallback=f"comp_{body_idx:04d}")
            comp_group_id = f"assembly-comp-{token}-{body_idx:04d}"

            tx, ty, instance_rotation_deg, transform_value = self._assembly_build_instance_transform(
                ctx,
                side=side,
                instance_x_mils=float(instance_x_mils),
                instance_y_mils=float(instance_y_mils),
                component_rotation_deg=float(component_rotation_deg),
            )
            comp_attrs = [
                f'id="{html.escape(comp_group_id)}"',
                # Local projection geometry is already converted to SVG Y-down
                # coordinates in _assembly_geometry_elements_local().
                f'transform="{transform_value}"',
            ]
            if self.options.include_metadata:
                comp_attrs.extend(
                    ctx.relationship_metadata_attrs(
                        component_index=comp_idx if comp_idx >= 0 else None,
                        include_net_classes=False,
                    )
                )
                model_hash = str(model_entry.get("hash", "") or "")
                if model_hash:
                    comp_attrs.append(f'data-assembly-model-hash="{html.escape(model_hash)}"')
                comp_attrs.append('data-assembly-source="step"')
                comp_attrs.append(f'data-assembly-available-modes="{html.escape(available_modes_text)}"')

            scene_lines.append("    " + f"<g {' '.join(comp_attrs)}>")
            if emit_simple:
                scene_lines.append(
                    "      "
                    + (
                        f'<g data-assembly-mode="simple"><use href="#{html.escape(simple_id)}"/>'
                        "</g>"
                    )
                )
            if emit_detail:
                scene_lines.append(
                    "      "
                    + (
                        f'<g data-assembly-mode="detail"><use href="#{html.escape(detail_id)}"/>'
                        "</g>"
                    )
            )
            scene_lines.append("    </g>")
            instance_count += 1
            if comp_idx >= 0:
                component_emitted_geometry.add(comp_idx)

        for comp_idx, extruded_entries in sorted(extruded_bodies_by_component.items(), key=lambda item: item[0]):
            if comp_idx < 0 or comp_idx >= len(components):
                continue
            component = components[comp_idx]
            component_rotation_deg = helper._parse_altium_float(
                getattr(component, "rotation", None),
                default=0.0,
            )
            comp_x_mils, comp_y_mils = self._assembly_component_anchor_mils(helper, component, {})
            if comp_x_mils is None or comp_y_mils is None:
                continue

            tx, ty, instance_rotation_deg, transform_value = self._assembly_build_instance_transform(
                ctx,
                side=side,
                instance_x_mils=float(comp_x_mils),
                instance_y_mils=float(comp_y_mils),
                component_rotation_deg=float(component_rotation_deg),
            )

            detail_segments_raw: list[tuple[tuple[float, float], tuple[float, float]]] = []
            simple_union_geometry = None

            for _body_idx, body, _props in extruded_entries:
                body_geometry = helper._component_body_polygon_mm(body)
                if body_geometry is None or body_geometry.is_empty:
                    continue
                polys = helper._extract_polygons(body_geometry)
                for poly in polys:
                    detail_segments_raw.extend(
                        self._assembly_coords_to_local_segments(
                            ctx,
                            side=side,
                            coords=[(float(x), float(y)) for x, y in list(poly.exterior.coords)],
                            tx_svg_mm=tx,
                            ty_svg_mm=ty,
                            instance_rotation_deg=instance_rotation_deg,
                        )
                    )
                    for interior in list(poly.interiors):
                        detail_segments_raw.extend(
                            self._assembly_coords_to_local_segments(
                                ctx,
                                side=side,
                                coords=[(float(x), float(y)) for x, y in list(interior.coords)],
                                tx_svg_mm=tx,
                                ty_svg_mm=ty,
                                instance_rotation_deg=instance_rotation_deg,
                            )
                        )
                simple_union_geometry = body_geometry if simple_union_geometry is None else simple_union_geometry.union(
                    body_geometry
                )

            simple_segments_raw: list[tuple[tuple[float, float], tuple[float, float]]] = []
            if simple_union_geometry is not None and not simple_union_geometry.is_empty:
                for poly in helper._extract_polygons(simple_union_geometry):
                    simple_segments_raw.extend(
                        self._assembly_coords_to_local_segments(
                            ctx,
                            side=side,
                            coords=[(float(x), float(y)) for x, y in list(poly.exterior.coords)],
                            tx_svg_mm=tx,
                            ty_svg_mm=ty,
                            instance_rotation_deg=instance_rotation_deg,
                        )
                    )

            detail_segments = self._assembly_dedupe_local_segments(detail_segments_raw, round_digits=round_digits)
            simple_segments = self._assembly_dedupe_local_segments(simple_segments_raw, round_digits=round_digits)
            projected = _ProjectedLines(
                simple_line_segments=simple_segments,
                detail_line_segments=detail_segments,
            )
            if projected.is_empty:
                continue

            cache_key = (
                "extruded",
                self._assembly_segment_signature_key(simple_segments, round_digits=round_digits),
                self._assembly_segment_signature_key(detail_segments, round_digits=round_digits),
                bool(side == "bottom"),
            )
            symbol_ids = symbol_ids_by_key.get(cache_key)
            if symbol_ids is None:
                base_id = f"assembly-proj-{len(symbol_ids_by_key):04d}"
                simple_id = f"{base_id}-simple"
                detail_id = f"{base_id}-detail"
                defs_lines.extend(
                    self._build_assembly_symbol_defs(
                        simple_id=simple_id,
                        detail_id=detail_id,
                        projected=projected,
                    )
                )
                symbol_ids = (simple_id, detail_id)
                symbol_ids_by_key[cache_key] = symbol_ids
                unique_projection_count += 1

            simple_id, detail_id = symbol_ids
            designator = str(getattr(component, "designator", "") or "").strip()
            token = self._safe_svg_token(designator, fallback=f"comp_{comp_idx:04d}")
            comp_group_id = f"assembly-comp-{token}-extruded-{comp_idx:04d}"
            comp_attrs = [
                f'id="{html.escape(comp_group_id)}"',
                f'transform="{transform_value}"',
            ]
            if self.options.include_metadata:
                comp_attrs.extend(
                    ctx.relationship_metadata_attrs(
                        component_index=comp_idx,
                        include_net_classes=False,
                    )
                )
                comp_attrs.append('data-assembly-source="extruded"')
                comp_attrs.append(f'data-assembly-available-modes="{html.escape(available_modes_text)}"')

            scene_lines.append("    " + f"<g {' '.join(comp_attrs)}>")
            if emit_simple:
                scene_lines.append(
                    "      "
                    + (
                        f'<g data-assembly-mode="simple"><use href="#{html.escape(simple_id)}"/>'
                        "</g>"
                    )
                )
            if emit_detail:
                scene_lines.append(
                    "      "
                    + (
                        f'<g data-assembly-mode="detail"><use href="#{html.escape(detail_id)}"/>'
                        "</g>"
                    )
                )
            scene_lines.append("    </g>")
            instance_count += 1
            component_emitted_geometry.add(comp_idx)

        for body_idx, body, props, anchor_x_mils, anchor_y_mils, component_rotation_deg in free_extruded_bodies:
            tx, ty, instance_rotation_deg, transform_value = self._assembly_build_instance_transform(
                ctx,
                side=side,
                instance_x_mils=float(anchor_x_mils),
                instance_y_mils=float(anchor_y_mils),
                component_rotation_deg=float(component_rotation_deg),
            )
            body_geometry = helper._component_body_polygon_mm(body)
            if body_geometry is None or body_geometry.is_empty:
                continue

            detail_segments_raw: list[tuple[tuple[float, float], tuple[float, float]]] = []
            for poly in helper._extract_polygons(body_geometry):
                detail_segments_raw.extend(
                    self._assembly_coords_to_local_segments(
                        ctx,
                        side=side,
                        coords=[(float(x), float(y)) for x, y in list(poly.exterior.coords)],
                        tx_svg_mm=tx,
                        ty_svg_mm=ty,
                        instance_rotation_deg=instance_rotation_deg,
                    )
                )
                for interior in list(poly.interiors):
                    detail_segments_raw.extend(
                        self._assembly_coords_to_local_segments(
                            ctx,
                            side=side,
                            coords=[(float(x), float(y)) for x, y in list(interior.coords)],
                            tx_svg_mm=tx,
                            ty_svg_mm=ty,
                            instance_rotation_deg=instance_rotation_deg,
                        )
                    )

            detail_segments = self._assembly_dedupe_local_segments(detail_segments_raw, round_digits=round_digits)
            projected = _ProjectedLines(
                simple_line_segments=detail_segments,
                detail_line_segments=detail_segments,
            )
            if projected.is_empty:
                continue

            cache_key = (
                "extruded-free",
                self._assembly_segment_signature_key(projected.simple_line_segments, round_digits=round_digits),
                bool(side == "bottom"),
            )
            symbol_ids = symbol_ids_by_key.get(cache_key)
            if symbol_ids is None:
                base_id = f"assembly-proj-{len(symbol_ids_by_key):04d}"
                simple_id = f"{base_id}-simple"
                detail_id = f"{base_id}-detail"
                defs_lines.extend(
                    self._build_assembly_symbol_defs(
                        simple_id=simple_id,
                        detail_id=detail_id,
                        projected=projected,
                    )
                )
                symbol_ids = (simple_id, detail_id)
                symbol_ids_by_key[cache_key] = symbol_ids
                unique_projection_count += 1

            simple_id, detail_id = symbol_ids
            comp_group_id = f"assembly-comp-free-extruded-{body_idx:04d}"
            comp_attrs = [
                f'id="{html.escape(comp_group_id)}"',
                f'transform="{transform_value}"',
            ]
            if self.options.include_metadata:
                comp_attrs.append('data-assembly-source="extruded"')
                comp_attrs.append(f'data-assembly-available-modes="{html.escape(available_modes_text)}"')

            scene_lines.append("    " + f"<g {' '.join(comp_attrs)}>")
            if emit_simple:
                scene_lines.append(
                    "      "
                    + (
                        f'<g data-assembly-mode="simple"><use href="#{html.escape(simple_id)}"/>'
                        "</g>"
                    )
                )
            if emit_detail:
                scene_lines.append(
                    "      "
                    + (
                        f'<g data-assembly-mode="detail"><use href="#{html.escape(detail_id)}"/>'
                        "</g>"
                    )
                )
            scene_lines.append("    </g>")
            instance_count += 1

        for comp_idx in sorted(component_had_body_on_side - component_emitted_geometry):
            if comp_idx < 0 or comp_idx >= len(components):
                continue
            component = components[comp_idx]
            if self._assembly_component_layer_is_bottom(component) != (side == "bottom"):
                continue

            bbox = self._assembly_component_copper_bbox_mils(
                pcbdoc,
                component_index=comp_idx,
            )
            if bbox is None:
                continue

            component_rotation_deg = helper._parse_altium_float(
                getattr(component, "rotation", None),
                default=0.0,
            )
            comp_x_mils, comp_y_mils = self._assembly_component_anchor_mils(helper, component, {})
            if comp_x_mils is None or comp_y_mils is None:
                comp_x_mils = (float(bbox[0]) + float(bbox[2])) * 0.5
                comp_y_mils = (float(bbox[1]) + float(bbox[3])) * 0.5

            tx, ty, instance_rotation_deg, transform_value = self._assembly_build_instance_transform(
                ctx,
                side=side,
                instance_x_mils=float(comp_x_mils),
                instance_y_mils=float(comp_y_mils),
                component_rotation_deg=float(component_rotation_deg),
            )
            min_x_mils, min_y_mils, max_x_mils, max_y_mils = bbox
            ring_mm = [
                (float(min_x_mils) * _MIL_TO_MM, float(min_y_mils) * _MIL_TO_MM),
                (float(max_x_mils) * _MIL_TO_MM, float(min_y_mils) * _MIL_TO_MM),
                (float(max_x_mils) * _MIL_TO_MM, float(max_y_mils) * _MIL_TO_MM),
                (float(min_x_mils) * _MIL_TO_MM, float(max_y_mils) * _MIL_TO_MM),
                (float(min_x_mils) * _MIL_TO_MM, float(min_y_mils) * _MIL_TO_MM),
            ]
            bbox_segments = self._assembly_dedupe_local_segments(
                self._assembly_coords_to_local_segments(
                    ctx,
                    side=side,
                    coords=ring_mm,
                    tx_svg_mm=tx,
                    ty_svg_mm=ty,
                    instance_rotation_deg=instance_rotation_deg,
                ),
                round_digits=round_digits,
            )
            projected = _ProjectedLines(
                simple_line_segments=bbox_segments,
                detail_line_segments=bbox_segments,
            )
            if projected.is_empty:
                continue

            cache_key = (
                "bbox-fallback",
                self._assembly_segment_signature_key(bbox_segments, round_digits=round_digits),
                bool(side == "bottom"),
            )
            symbol_ids = symbol_ids_by_key.get(cache_key)
            if symbol_ids is None:
                base_id = f"assembly-proj-{len(symbol_ids_by_key):04d}"
                simple_id = f"{base_id}-simple"
                detail_id = f"{base_id}-detail"
                defs_lines.extend(
                    self._build_assembly_symbol_defs(
                        simple_id=simple_id,
                        detail_id=detail_id,
                        projected=projected,
                    )
                )
                symbol_ids = (simple_id, detail_id)
                symbol_ids_by_key[cache_key] = symbol_ids
                unique_projection_count += 1

            simple_id, detail_id = symbol_ids
            designator = str(getattr(component, "designator", "") or "").strip()
            token = self._safe_svg_token(designator, fallback=f"comp_{comp_idx:04d}")
            comp_group_id = f"assembly-comp-{token}-bbox-{comp_idx:04d}"
            comp_attrs = [
                f'id="{html.escape(comp_group_id)}"',
                f'transform="{transform_value}"',
            ]
            if self.options.include_metadata:
                comp_attrs.extend(
                    ctx.relationship_metadata_attrs(
                        component_index=comp_idx,
                        include_net_classes=False,
                    )
                )
                comp_attrs.append('data-assembly-source="bbox-fallback"')
                comp_attrs.append(f'data-assembly-available-modes="{html.escape(available_modes_text)}"')

            scene_lines.append("    " + f"<g {' '.join(comp_attrs)}>")
            if emit_simple:
                scene_lines.append(
                    "      "
                    + (
                        f'<g data-assembly-mode="simple"><use href="#{html.escape(simple_id)}"/>'
                        "</g>"
                    )
                )
            if emit_detail:
                scene_lines.append(
                    "      "
                    + (
                        f'<g data-assembly-mode="detail"><use href="#{html.escape(detail_id)}"/>'
                        "</g>"
                    )
                )
            scene_lines.append("    </g>")
            instance_count += 1
            component_emitted_geometry.add(comp_idx)

        if instance_count <= 0:
            return [], []

        overlay_attrs = [
            'id="assembly-overlay"',
            f'data-assembly-side="{html.escape(side)}"',
            f'data-assembly-instance-count="{instance_count}"',
            f'data-assembly-unique-projections="{unique_projection_count}"',
            f'data-assembly-modes="{html.escape(available_modes_text)}"',
            f'data-assembly-default-mode="{html.escape(default_mode)}"',
            'fill="none"',
            f'stroke="{html.escape(str(self.options.assembly_overlay_color or "#F59E0B"))}"',
            'stroke-linecap="round"',
            'stroke-linejoin="round"',
            'vector-effect="non-scaling-stroke"',
        ]
        wrapped_scene = ["  " + f"<g {' '.join(overlay_attrs)}>"]
        wrapped_scene.extend(scene_lines)
        wrapped_scene.append("  </g>")
        return defs_lines, wrapped_scene

    def _build_assembly_symbol_defs(
        self,
        *,
        simple_id: str,
        detail_id: str,
        projected,
    ) -> list[str]:
        simple_segments = tuple(projected.simple_line_segments)
        simple_arcs = tuple(projected.simple_arcs)
        detail_segments = tuple(projected.detail_line_segments)
        detail_arcs = tuple(projected.detail_arcs)
        if (not simple_segments and not simple_arcs) and (detail_segments or detail_arcs):
            # Guarantee mode-switchable geometry even when only one mode is produced.
            simple_segments = detail_segments
            simple_arcs = detail_arcs
        if (not detail_segments and not detail_arcs) and (simple_segments or simple_arcs):
            detail_segments = simple_segments
            detail_arcs = simple_arcs

        lines: list[str] = []
        lines.append(
            "    "
            + (
                f'<g id="{html.escape(simple_id)}" data-assembly-symbol="simple" '
                'stroke-width="0.12">'
            )
        )
        lines.extend(
            self._assembly_geometry_elements_local(
                line_segments=simple_segments,
                arcs=simple_arcs,
            )
        )
        lines.append("    </g>")

        lines.append(
            "    "
            + (
                f'<g id="{html.escape(detail_id)}" data-assembly-symbol="detail" '
                'stroke-width="0.08">'
            )
        )
        lines.extend(
            self._assembly_geometry_elements_local(
                line_segments=detail_segments,
                arcs=detail_arcs,
            )
        )
        lines.append("    </g>")
        return lines

    def _assembly_geometry_elements_local(
        self,
        *,
        line_segments,
        arcs,
    ) -> list[str]:
        lines: list[str] = []
        for (x1, y1), (x2, y2) in line_segments:
            lx1 = float(x1)
            ly1 = -float(y1)
            lx2 = float(x2)
            ly2 = -float(y2)
            lines.append(
                "      "
                + (
                    f'<line x1="{self._fmt_local_mm(lx1)}" y1="{self._fmt_local_mm(ly1)}" '
                    f'x2="{self._fmt_local_mm(lx2)}" y2="{self._fmt_local_mm(ly2)}"/>'
                )
            )

        for arc in arcs:
            cx = float(arc.center[0])
            cy = -float(arc.center[1])
            radius = max(float(arc.radius), 0.0)
            if radius <= 0.0:
                continue
            if bool(arc.full_circle):
                lines.append(
                    "      "
                    + (
                        f'<circle cx="{self._fmt_local_mm(cx)}" cy="{self._fmt_local_mm(cy)}" '
                        f'r="{self._fmt_local_mm(radius)}"/>'
                    )
                )
                continue

            sx = float(arc.start[0])
            sy = -float(arc.start[1])
            ex = float(arc.end[0])
            ey = -float(arc.end[1])
            large_arc = "1" if float(arc.extent_rad) > math.pi else "0"
            sweep = "0" if bool(arc.ccw) else "1"
            d = (
                f"M {self._fmt_local_mm(sx)} {self._fmt_local_mm(sy)} "
                f"A {self._fmt_local_mm(radius)} {self._fmt_local_mm(radius)} 0 "
                f"{large_arc} {sweep} {self._fmt_local_mm(ex)} {self._fmt_local_mm(ey)}"
            )
            lines.append("      " + f'<path d="{d}"/>')
        return lines

def _surface_role_order_from_tokens(
    order_tokens: list[str] | tuple[str, ...] | None,
    *,
    include_missing_roles: bool,
) -> list[PCB_SurfaceRole]:
    ordered_roles: list[PCB_SurfaceRole] = []
    for token in list(order_tokens or []):
        normalized = str(token or "").strip().lower()
        if not normalized:
            continue
        role = PCB_SurfaceRole(normalized)
        if role not in ordered_roles:
            ordered_roles.append(role)
    if include_missing_roles:
        for role in (PCB_SurfaceRole.COPPER, PCB_SurfaceRole.SILKSCREEN):
            if role not in ordered_roles:
                ordered_roles.append(role)
    return ordered_roles


def render_pcb_assembly_svg_views(
    design: "AltiumDesign",
    *,
    pcbdoc_selector: str | None = None,
    views: set[str] | None = None,
    layer_filter: set[PcbLayer] | None = None,
    monochrome_color: str = "#000000",
    plated_drill_color: str = "#90EE90",
    non_plated_drill_color: str = "#ADD8E6",
    drill_mode: str = "overlay",
    drill_overlay_opacity: float = 1.0,
    include_metadata: bool = True,
    include_board_outline: bool = True,
    show_empty_layers: bool = False,
    include_polygon_definition_overlays: bool = False,
    polygon_overlay_color: str = "#000000",
    board_cutout_color: str = "#FF0000",
    mirror_bottom_view: bool = True,
    clip_to_outline: bool = True,
    clip_holes_from_copper: bool = True,
    assembly_enabled: bool = False,
    assembly_include_simple: bool = True,
    assembly_include_detail: bool = True,
    assembly_curve_mode: str = "native_arcs",
    assembly_samples_per_curve: int = 24,
    assembly_round_digits: int = 3,
    assembly_include_visible: bool = True,
    assembly_include_outline: bool = True,
    assembly_union_polygons: bool = True,
    assembly_overlay_color: str = "#F59E0B",
    svg_display_scale: float = 1.0,
    svg_size_unit: str = "",
    top_board_outline_color: str | None = None,
    top_board_cutout_color: str | None = None,
    top_copper_color: str | None = None,
    top_silkscreen_color: str | None = None,
    top_plated_drill_color: str | None = None,
    top_non_plated_drill_color: str | None = None,
    top_polygon_overlay_color: str | None = None,
    top_layer_order: list[str] | tuple[str, ...] | None = None,
    bottom_board_outline_color: str | None = None,
    bottom_board_cutout_color: str | None = None,
    bottom_copper_color: str | None = None,
    bottom_silkscreen_color: str | None = None,
    bottom_plated_drill_color: str | None = None,
    bottom_non_plated_drill_color: str | None = None,
    bottom_polygon_overlay_color: str | None = None,
    bottom_layer_order: list[str] | tuple[str, ...] | None = None,
    assembly_top_layer_order: list[str] | tuple[str, ...] | None = None,
    assembly_bottom_layer_order: list[str] | tuple[str, ...] | None = None,
    **_ignored: Any,
) -> dict[str, dict[str, str]]:
    del layer_filter
    normalized_views = {v.strip().lower() for v in (views or set()) if v and v.strip()}
    if not normalized_views:
        return {}
    unsupported = normalized_views - {"assembly-top", "assembly-bottom"}
    if unsupported:
        raise ValueError(
            "render_pcb_assembly_svg_views() only supports assembly surface views; "
            f"got {sorted(unsupported)}"
        )
    rendered: dict[str, dict[str, str]] = {}

    for render_input in iter_pcb_render_inputs(design, pcbdoc_selector=pcbdoc_selector):
        pcbdoc = render_input.pcbdoc
        board_key = render_input.board_key
        board_views: dict[str, str] = {}

        if "assembly-top" in normalized_views:
            top_role_order = _surface_role_order_from_tokens(
                assembly_top_layer_order or ["copper"],
                include_missing_roles=False,
            )
            top_layers_in_order = pcb_surface_layers(
                PCB_SurfaceSide.TOP,
                role_order=top_role_order,
                include_missing_roles=False,
            )
            top_renderer = CruncherPcbAssemblySvgRenderer(
                CruncherPcbAssemblySvgRenderOptions(
                    visible_layers=set(top_layers_in_order),
                    layer_render_order=top_layers_in_order,
                    layer_colors={
                        PcbLayer.TOP: top_copper_color or monochrome_color,
                        PcbLayer.TOP_OVERLAY: top_silkscreen_color or monochrome_color,
                    },
                    show_empty_layers=True,
                    include_metadata=include_metadata,
                    show_board_outline=include_board_outline,
                    board_outline_color=top_board_outline_color or monochrome_color,
                    board_cutout_color=top_board_cutout_color or board_cutout_color,
                    drill_hole_mode=drill_mode,
                    drill_hole_overlay_plated_color=top_plated_drill_color or plated_drill_color,
                    drill_hole_overlay_non_plated_color=(
                        top_non_plated_drill_color or non_plated_drill_color
                    ),
                    drill_hole_overlay_opacity=drill_overlay_opacity,
                    clip_copper_to_board_outline=clip_to_outline,
                    clip_all_layers_to_board_outline=clip_to_outline,
                    clip_holes_from_copper=clip_holes_from_copper,
                    include_assembly_overlay=assembly_enabled,
                    assembly_view_side="top",
                    assembly_include_simple=assembly_include_simple,
                    assembly_include_detail=assembly_include_detail,
                    assembly_curve_mode=assembly_curve_mode,
                    assembly_samples_per_curve=assembly_samples_per_curve,
                    assembly_round_digits=assembly_round_digits,
                    assembly_include_visible=assembly_include_visible,
                    assembly_include_outline=assembly_include_outline,
                    assembly_union_polygons=assembly_union_polygons,
                    assembly_overlay_color=assembly_overlay_color,
                    svg_display_scale=svg_display_scale,
                    svg_size_unit=svg_size_unit,
                )
            )
            board_views["assembly_top_view"] = top_renderer.render_board(
                pcbdoc,
                project_parameters=render_input.project_parameters,
            )

        if "assembly-bottom" in normalized_views:
            bottom_role_order = _surface_role_order_from_tokens(
                assembly_bottom_layer_order or ["copper"],
                include_missing_roles=False,
            )
            bottom_layers_in_order = pcb_surface_layers(
                PCB_SurfaceSide.BOTTOM,
                role_order=bottom_role_order,
                include_missing_roles=False,
            )
            bottom_renderer = CruncherPcbAssemblySvgRenderer(
                CruncherPcbAssemblySvgRenderOptions(
                    visible_layers=set(bottom_layers_in_order),
                    layer_render_order=bottom_layers_in_order,
                    layer_colors={
                        PcbLayer.BOTTOM: bottom_copper_color or monochrome_color,
                        PcbLayer.BOTTOM_OVERLAY: bottom_silkscreen_color or monochrome_color,
                    },
                    show_empty_layers=True,
                    include_metadata=include_metadata,
                    show_board_outline=include_board_outline,
                    board_outline_color=bottom_board_outline_color or monochrome_color,
                    board_cutout_color=bottom_board_cutout_color or board_cutout_color,
                    drill_hole_mode=drill_mode,
                    drill_hole_overlay_plated_color=bottom_plated_drill_color or plated_drill_color,
                    drill_hole_overlay_non_plated_color=(
                        bottom_non_plated_drill_color or non_plated_drill_color
                    ),
                    drill_hole_overlay_opacity=drill_overlay_opacity,
                    clip_copper_to_board_outline=clip_to_outline,
                    clip_all_layers_to_board_outline=clip_to_outline,
                    clip_holes_from_copper=clip_holes_from_copper,
                    include_assembly_overlay=assembly_enabled,
                    assembly_view_side="bottom",
                    assembly_include_simple=assembly_include_simple,
                    assembly_include_detail=assembly_include_detail,
                    assembly_curve_mode=assembly_curve_mode,
                    assembly_samples_per_curve=assembly_samples_per_curve,
                    assembly_round_digits=assembly_round_digits,
                    assembly_include_visible=assembly_include_visible,
                    assembly_include_outline=assembly_include_outline,
                    assembly_union_polygons=assembly_union_polygons,
                    assembly_overlay_color=assembly_overlay_color,
                    mirror_x=mirror_bottom_view,
                    svg_display_scale=svg_display_scale,
                    svg_size_unit=svg_size_unit,
                )
            )
            board_views["assembly_bottom_view"] = bottom_renderer.render_board(
                pcbdoc,
                project_parameters=render_input.project_parameters,
            )

        rendered[board_key] = board_views

    return rendered
