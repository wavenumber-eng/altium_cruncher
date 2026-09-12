from __future__ import annotations

from pathlib import Path
from dataclasses import replace

import geometer
import pytest

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


@pytest.mark.parametrize("algorithm", [None, "exact", "poly"])
def test_projection_backend_selection_preserves_legacy_override(monkeypatch, algorithm):
    original = geometer.project_step_hlr
    calls = []

    def capture(*args, **kwargs):
        calls.append(kwargs["options"])
        return original(*args, **kwargs)

    monkeypatch.setattr(geometer, "project_step_hlr", capture)
    geometry = AssemblyProjectionCache().project(
        model_hash="resistor", step_bytes=STEP_FIXTURE.read_bytes(),
        pose_signature=(), transform_matrix=IDENTITY_MATRIX,
        options=AssemblyProjectionOptions(side="top", projection_algorithm=algorithm),
    )[1]
    assert not geometry.is_empty
    assert calls[0]["projection_algorithm"] == (algorithm or "fast")
    if algorithm is None:
        assert calls[0]["outline_algorithm"] == "fast-mesh-shadow"
        assert calls[0]["curve_mode"] == "polyline"
        assert not geometry.simple_arcs and not geometry.detail_arcs
    else:
        assert "outline_algorithm" not in calls[0]
        assert calls[0]["curve_mode"] == "native_arcs"


def test_outline_algorithm_invalidates_cached_projection():
    cache = AssemblyProjectionCache()
    options = AssemblyProjectionOptions(side="top")
    kwargs = dict(model_hash="resistor", pose_signature=(0.0,))
    assert cache.build_cache_key(**kwargs, options=options) != cache.build_cache_key(
        **kwargs, options=replace(options, outline_algorithm="mesh-shadow")
    )


def test_fast_candidate_controls_and_legacy_controls_are_not_silently_ignored():
    cache = AssemblyProjectionCache()
    kwargs = dict(model_hash="resistor", step_bytes=STEP_FIXTURE.read_bytes(),
                  pose_signature=(), transform_matrix=IDENTITY_MATRIX)
    with pytest.raises(ValueError, match="Fast HLR uses"):
        cache.project(**kwargs, options=AssemblyProjectionOptions(side="top", include_visible=False))
    visible = cache.project(**kwargs, options=AssemblyProjectionOptions(side="top", fast={"include_hidden": False}))[1]
    hidden = cache.project(**kwargs, options=AssemblyProjectionOptions(side="top", fast={"include_hidden": True}))[1]
    assert len(hidden.detail_line_segments) > len(visible.detail_line_segments)
    empty = cache.project(**kwargs, options=AssemblyProjectionOptions(side="top", fast={
        "include_boundaries": False, "include_creases": False, "include_silhouettes": False,
    }))[1]
    assert not empty.detail_line_segments
    assert empty.simple_line_segments
