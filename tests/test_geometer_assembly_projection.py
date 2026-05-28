from __future__ import annotations

from pathlib import Path

from altium_cruncher.altium_cruncher_pcb_svg_assembly_projection import (
    AssemblyProjectionCache,
    AssemblyProjectionOptions,
)


ROOT = Path(__file__).resolve().parents[1]
STEP_FIXTURE = (
    ROOT
    / "tests"
    / "assets"
    / "3d"
    / "RESC1608X06N.step"
)
IDENTITY_MATRIX = [
    [1.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 1.0],
]


def test_assembly_projection_cache_uses_geometer_for_step_hlr() -> None:
    cache = AssemblyProjectionCache()
    step_bytes = STEP_FIXTURE.read_bytes()

    top_key, top_geometry = cache.project(
        model_hash="resc1608x06n",
        step_bytes=step_bytes,
        pose_signature=(0.0, 0.0, 0.0),
        transform_matrix=IDENTITY_MATRIX,
        options=AssemblyProjectionOptions(side="top", curve_mode="polyline"),
        model_label="RESC1608X06N",
    )
    assert not top_geometry.is_empty
    assert len(top_geometry.simple_line_segments) + len(top_geometry.simple_arcs) > 0
    assert len(top_geometry.detail_line_segments) + len(top_geometry.detail_arcs) > 0

    cached_key, cached_geometry = cache.project(
        model_hash="resc1608x06n",
        step_bytes=step_bytes,
        pose_signature=(0.0, 0.0, 0.0),
        transform_matrix=IDENTITY_MATRIX,
        options=AssemblyProjectionOptions(side="top", curve_mode="polyline"),
        model_label="RESC1608X06N",
    )
    assert cached_key == top_key
    assert cached_geometry is top_geometry

    _bottom_key, bottom_geometry = cache.project(
        model_hash="resc1608x06n",
        step_bytes=step_bytes,
        pose_signature=(0.0, 0.0, 0.0),
        transform_matrix=IDENTITY_MATRIX,
        options=AssemblyProjectionOptions(side="bottom", curve_mode="polyline"),
        model_label="RESC1608X06N",
    )
    assert not bottom_geometry.is_empty
    assert (
        len(bottom_geometry.simple_line_segments) + len(bottom_geometry.simple_arcs) > 0
    )
