"""Minimal PCB assembly model helpers used by SVG HLR overlays."""

from __future__ import annotations

import hashlib
import math
from typing import Any
import zlib

from altium_monkey.altium_embedded_files import classify_embedded_model_format

_MIL_TO_MM = 0.0254


def _identity_matrix() -> list[list[float]]:
    return [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]


def _multiply_matrix(left: list[list[float]], right: list[list[float]]) -> list[list[float]]:
    return [
        [
            sum(float(left[row][k]) * float(right[k][col]) for k in range(4))
            for col in range(4)
        ]
        for row in range(4)
    ]


def _translation_matrix(x: float, y: float, z: float) -> list[list[float]]:
    matrix = _identity_matrix()
    matrix[0][3] = float(x)
    matrix[1][3] = float(y)
    matrix[2][3] = float(z)
    return matrix


def _rotation_matrix(angle_rad: float, axis: tuple[float, float, float]) -> list[list[float]]:
    x, y, z = axis
    length = math.sqrt((x * x) + (y * y) + (z * z))
    if length <= 0.0:
        return _identity_matrix()
    x /= length
    y /= length
    z /= length
    c = math.cos(angle_rad)
    s = math.sin(angle_rad)
    t = 1.0 - c
    return [
        [t * x * x + c, t * x * y - s * z, t * x * z + s * y, 0.0],
        [t * x * y + s * z, t * y * y + c, t * y * z - s * x, 0.0],
        [t * x * z - s * y, t * y * z + s * x, t * z * z + c, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]


def _concatenate_matrices(*matrices: list[list[float]]) -> list[list[float]]:
    result = _identity_matrix()
    for matrix in matrices:
        result = _multiply_matrix(result, matrix)
    return result


def _ring_points_to_mm(points_mils: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(x * _MIL_TO_MM, y * _MIL_TO_MM) for x, y in points_mils]


class PcbAssemblyModelHelper:
    """Small subset of former GLTF helper behavior needed for assembly SVG."""

    def _collect_embedded_step_model_catalog(
        self,
        pcbdoc: Any,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        discovery: dict[str, Any] = {
            "model_record_count": 0,
            "model_stream_count": 0,
            "embedded_with_stream_count": 0,
            "step_candidate_count": 0,
            "classifications": {},
            "models": [],
        }
        model_records = list(getattr(pcbdoc, "models", []) or [])
        if not model_records:
            return [], discovery
        discovery["model_record_count"] = len(model_records)

        get_entries = getattr(pcbdoc, "get_embedded_model_entries", None)
        embedded_entries = list(get_entries() or []) if callable(get_entries) else []
        unused_entry_indices = list(range(len(embedded_entries)))
        embedded_entry_cursor = 0

        def model_entry_signature(model: Any) -> tuple[str, str, int | None]:
            return (
                self._normalize_model_id(getattr(model, "id", None)),
                self._normalize_model_name(getattr(model, "name", None)),
                self._parse_altium_int(getattr(model, "checksum", None)),
            )

        catalog: list[dict[str, Any]] = []
        for model_index, model in enumerate(model_records):
            is_embedded = bool(getattr(model, "is_embedded", False))
            model_name = str(getattr(model, "name", "") or "").strip().strip("\x00")
            model_format = classify_embedded_model_format(model_name)
            model_stream: bytes | None = None

            if is_embedded and unused_entry_indices:
                target_signature = model_entry_signature(model)
                matched_entry_index: int | None = None
                for entry_index in unused_entry_indices:
                    entry_model, _entry_payload = embedded_entries[entry_index]
                    if model_entry_signature(entry_model) == target_signature:
                        matched_entry_index = entry_index
                        break
                if matched_entry_index is None:
                    while (
                        embedded_entry_cursor < len(embedded_entries)
                        and embedded_entry_cursor not in unused_entry_indices
                    ):
                        embedded_entry_cursor += 1
                    if embedded_entry_cursor < len(embedded_entries):
                        matched_entry_index = embedded_entry_cursor
                if matched_entry_index is not None:
                    unused_entry_indices.remove(matched_entry_index)
                    embedded_entry_cursor = max(embedded_entry_cursor, matched_entry_index + 1)
                    _entry_model, entry_payload = embedded_entries[matched_entry_index]
                    if isinstance(entry_payload, bytes | bytearray):
                        model_stream = bytes(entry_payload)

            has_stream = isinstance(model_stream, bytes | bytearray)
            if has_stream:
                discovery["model_stream_count"] += 1
            if is_embedded and has_stream:
                discovery["embedded_with_stream_count"] += 1
                by_fmt = dict(discovery.get("classifications", {}) or {})
                by_fmt[model_format] = int(by_fmt.get(model_format, 0)) + 1
                discovery["classifications"] = by_fmt

            discovery["models"].append(
                {
                    "index": int(model_index),
                    "name": model_name,
                    "format": model_format,
                    "embedded": bool(is_embedded),
                    "has_stream": bool(has_stream),
                }
            )
            if not has_stream or not is_embedded:
                continue

            step_bytes = self._decompress_model_stream(bytes(model_stream))
            if not step_bytes or not self._is_step_payload(step_bytes, model_name=model_name):
                continue

            discovery["step_candidate_count"] += 1
            model_id_raw = str(getattr(model, "id", "") or "").strip().upper().strip("\x00")
            catalog.append(
                {
                    "index": model_index,
                    "id_raw": model_id_raw,
                    "id_norm": self._normalize_model_id(model_id_raw),
                    "name": model_name,
                    "name_norm": self._normalize_model_name(model_name),
                    "checksum": self._parse_altium_int(getattr(model, "checksum", None)),
                    "hash": hashlib.sha256(step_bytes).hexdigest(),
                    "step_bytes": step_bytes,
                }
            )

        return catalog, discovery

    def _resolve_component_body_model_entry(
        self,
        props: dict[str, Any],
        *,
        models_by_id: dict[str, list[dict[str, Any]]],
        models_by_name: dict[str, list[dict[str, Any]]],
    ) -> dict[str, Any] | None:
        model_id_norm = self._normalize_model_id(props.get("MODELID"))
        model_name_norm = self._normalize_model_name(props.get("MODEL.NAME"))
        body_checksum = self._parse_altium_int(props.get("MODEL.CHECKSUM"))

        candidates: list[dict[str, Any]] = []
        if model_id_norm:
            candidates = list(models_by_id.get(model_id_norm, []))
        if not candidates and model_name_norm:
            candidates = list(models_by_name.get(model_name_norm, []))
        if not candidates:
            return None

        if body_checksum is not None:
            for candidate in candidates:
                if candidate.get("checksum") == body_checksum:
                    return candidate
        if model_name_norm:
            for candidate in candidates:
                if candidate.get("name_norm") == model_name_norm:
                    return candidate
        return candidates[0]

    def _compose_step_component_transform(
        self,
        *,
        x_mm: float,
        y_mm: float,
        z_mm: float,
        model_2d_rotation_deg: float,
        model_rotx_deg: float,
        model_roty_deg: float,
        model_rotz_deg: float,
        is_bottom: bool,
    ) -> list[list[float]]:
        bottom_orientation = _identity_matrix()
        if is_bottom:
            bottom_orientation = _rotation_matrix(math.pi, (1.0, 0.0, 0.0))
        return _concatenate_matrices(
            _translation_matrix(x_mm, y_mm, z_mm),
            _rotation_matrix(math.radians(model_2d_rotation_deg), (0.0, 0.0, 1.0)),
            bottom_orientation,
            _rotation_matrix(math.radians(model_rotz_deg), (0.0, 0.0, 1.0)),
            _rotation_matrix(math.radians(model_roty_deg), (0.0, 1.0, 0.0)),
            _rotation_matrix(math.radians(model_rotx_deg), (1.0, 0.0, 0.0)),
        )

    def _component_body_is_bottom(self, props: dict[str, Any], component: Any | None) -> bool:
        projection_value = self._parse_altium_int(props.get("BODYPROJECTION"))
        if projection_value == 0:
            return False
        if projection_value == 1:
            return True
        if component is not None:
            layer = str(getattr(component, "layer", "") or "").upper()
            if "BOTTOM" in layer:
                return True
            if "TOP" in layer:
                return False
        return False

    def _component_body_polygon_mm(self, body: Any):
        try:
            from shapely.geometry import Polygon
            from shapely.ops import unary_union
        except Exception:
            return None

        outline = list(getattr(body, "outline", []) or [])
        if len(outline) < 3:
            return None

        shell = _ring_points_to_mm(
            self._dedupe_ring(
                [
                    (
                        float(getattr(vertex, "x_mils", 0.0) or 0.0),
                        float(getattr(vertex, "y_mils", 0.0) or 0.0),
                    )
                    for vertex in outline
                ]
            )
        )
        if len(shell) < 3:
            return None

        holes: list[list[tuple[float, float]]] = []
        for hole in list(getattr(body, "holes", []) or []):
            hole_ring = _ring_points_to_mm(
                self._dedupe_ring(
                    [
                        (
                            float(getattr(vertex, "x_mils", 0.0) or 0.0),
                            float(getattr(vertex, "y_mils", 0.0) or 0.0),
                        )
                        for vertex in hole
                    ]
                )
            )
            if len(hole_ring) >= 3:
                holes.append(hole_ring)

        poly = Polygon(shell, holes)
        if not poly.is_valid:
            poly = poly.buffer(0)
        if poly.is_empty:
            return None
        extracted = self._extract_polygons(poly)
        if not extracted:
            return None
        return extracted[0] if len(extracted) == 1 else unary_union(extracted)

    def _extract_polygons(self, geometry: Any) -> list[Any]:
        if geometry is None or geometry.is_empty:
            return []
        geom_type = geometry.geom_type
        if geom_type == "Polygon":
            return [geometry]
        if geom_type == "MultiPolygon":
            return [poly for poly in geometry.geoms if not poly.is_empty]
        extracted: list[Any] = []
        for geom in getattr(geometry, "geoms", []):
            extracted.extend(self._extract_polygons(geom))
        return extracted

    def _normalize_model_id(self, value: Any) -> str:
        return str(value or "").strip().upper().strip("\x00")

    def _normalize_model_name(self, value: Any) -> str:
        text = str(value or "").strip().strip("\x00")
        if not text:
            return ""
        return text.replace("\\", "/").split("/")[-1].lower()

    def _decompress_model_stream(self, data: bytes) -> bytes:
        if len(data) >= 2 and data[0] == 0x78:
            try:
                return zlib.decompress(data)
            except Exception:
                pass
        return data

    def _is_step_payload(self, data: bytes, *, model_name: str) -> bool:
        head = data.lstrip()[:32]
        if head.startswith(b"ISO-10303-21;"):
            return True
        lower_name = (model_name or "").lower()
        return lower_name.endswith(".step") or lower_name.endswith(".stp")

    def _parse_altium_int(self, value: Any) -> int | None:
        if value is None:
            return None
        try:
            text = str(value).strip().strip("\x00")
            if not text:
                return None
            return int(float(text))
        except Exception:
            return None

    def _parse_altium_float(self, value: Any, *, default: float) -> float:
        if value is None:
            return float(default)
        try:
            text = str(value).strip().strip("\x00")
            if not text:
                return float(default)
            return float(text)
        except Exception:
            return float(default)

    def _parse_altium_mils(
        self,
        value: Any,
        *,
        assume_internal_units: bool,
        default: float | None = None,
    ) -> float | None:
        if value is None:
            return default
        try:
            text = str(value).strip().strip("\x00")
            if not text:
                return default
            lower = text.lower()
            if lower.endswith("mil"):
                return float(lower[:-3].strip())
            parsed = float(text)
            if assume_internal_units and abs(parsed) >= 1000.0:
                return parsed / 10000.0
            return parsed
        except Exception:
            return default

    def _dedupe_ring(
        self,
        points: list[tuple[float, float]],
        tol: float = 1e-6,
    ) -> list[tuple[float, float]]:
        deduped: list[tuple[float, float]] = []
        for x, y in points:
            if not deduped:
                deduped.append((x, y))
                continue
            px, py = deduped[-1]
            if abs(px - x) <= tol and abs(py - y) <= tol:
                continue
            deduped.append((x, y))

        if len(deduped) >= 2:
            fx, fy = deduped[0]
            lx, ly = deduped[-1]
            if abs(fx - lx) <= tol and abs(fy - ly) <= tol:
                deduped.pop()
        return deduped
