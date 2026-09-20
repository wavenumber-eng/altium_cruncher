"""Model Z-rotation candidates are selected only from authored geometry evidence."""

import math
from dataclasses import replace

import pytest
from types import SimpleNamespace
import geometer as g
from altium_monkey.altium_record_pcb__component_body import AltiumPcbComponentBody
from altium_monkey.altium_record_pcb__shapebased_region import PcbExtendedVertex

from altium_cruncher import altium_cruncher_pcb_illustration as illustration
from altium_cruncher.altium_cruncher_pcb_assembly_model_helper import (
    PcbAssemblyModelHelper,
)
from altium_cruncher.altium_cruncher_pcb_illustration import _step_matrix
from altium_cruncher.pcb_model_rotation import resolve_model_z_rotation


def test_footprint_local_candidate_fixes_the_rectangular_ic_case():
    result = resolve_model_z_rotation(
        (-4.95, -3.0, 4.95, 3.0),
        (-3.0, -4.95, -0.5, 3.0, 4.95, 1.5),
        (-4.95, -3.0, -0.5, 4.95, 3.0, 1.5),
    )

    assert result.choice == "footprint_local"
    assert result.reason == "footprint-local-native-bounds-match"


@pytest.mark.parametrize(
    "bounds",
    [
        (-2.0, -2.0, 0.0, 2.0, 2.0, 1.0),  # square quarter-turn ambiguity
        (-4.0, -2.0, 0.0, 4.0, 2.0, 1.0),  # 180-degree bounds ambiguity
    ],
)
def test_equivalent_candidates_retain_instance_space_behavior(bounds):
    target = (bounds[0], bounds[1], bounds[3], bounds[4])
    result = resolve_model_z_rotation(target, bounds, bounds)

    assert result.choice == "instance_space"


def test_neither_match_is_unresolved_instead_of_guessing():
    result = resolve_model_z_rotation(
        (0.0, 0.0, 10.0, 6.0),
        (20.0, 20.0, 0.0, 26.0, 30.0, 1.0),
        (-30.0, -20.0, 0.0, -20.0, -14.0, 1.0),
    )

    assert result.choice == "unresolved"
    assert result.reason == "neither-candidate-matches-authored-outline"


@pytest.mark.parametrize(
    ("target", "current", "alternative", "reason"),
    [
        ((0.0, 0.0, 0.0, 1.0), (0, 0, 0, 1, 1, 1), (0, 0, 0, 1, 1, 1), "invalid-authored-outline"),
        ((0.0, 0.0, 1.0, 1.0), (0, 0, 0, math.nan, 1, 1), (0, 0, 0, 1, 1, 1), "invalid-candidate-bounds"),
    ],
)
def test_invalid_geometry_is_typed_as_unresolved(target, current, alternative, reason):
    result = resolve_model_z_rotation(target, current, alternative)

    assert result.choice == "unresolved"
    assert result.reason == reason


@pytest.mark.parametrize("is_bottom", [False, True])
def test_full_affine_candidates_preserve_noncommuting_rotations_and_offsets(is_bottom):
    helper = PcbAssemblyModelHelper()
    component = SimpleNamespace(rotation="37")
    body = SimpleNamespace(
        properties={
            "MODEL.2D.X": "125mil",
            "MODEL.2D.Y": "-80mil",
            "MODEL.2D.ROTATION": "11",
            "MODEL.3D.ROTX": "23",
            "MODEL.3D.ROTY": "41",
            "MODEL.3D.ROTZ": "67",
        },
        model_3d_dz=250000,
    )

    current = _step_matrix(
        helper, body, component, (100.0, -100.0), is_bottom=is_bottom
    )
    local = _step_matrix(
        helper,
        body,
        component,
        (100.0, -100.0),
        is_bottom=is_bottom,
        rotation_mode="footprint_local",
    )

    assert current != local
    for matrix in (current, local):
        rotation = [row[:3] for row in matrix[:3]]
        determinant = (
            rotation[0][0]
            * (rotation[1][1] * rotation[2][2] - rotation[1][2] * rotation[2][1])
            - rotation[0][1]
            * (rotation[1][0] * rotation[2][2] - rotation[1][2] * rotation[2][0])
            + rotation[0][2]
            * (rotation[1][0] * rotation[2][1] - rotation[1][1] * rotation[2][0])
        )
        assert determinant == pytest.approx(1.0)
        assert matrix[0][3] == pytest.approx(25 * 0.0254)
        assert matrix[1][3] == pytest.approx(20 * 0.0254)
        assert matrix[2][3] == pytest.approx((-1 if is_bottom else 1) * 0.635)


def test_mesh_collection_uses_native_bounds_to_select_footprint_local_pose(monkeypatch):
    body = AltiumPcbComponentBody()
    body.component_index = 0
    body.model_type = 1
    body.properties = {"MODEL.NAME": "asymmetric.step", "MODEL.3D.ROTZ": "90"}
    for x_mm, y_mm in [(-5, -3), (5, -3), (5, 3), (-5, 3)]:
        vertex = PcbExtendedVertex()
        vertex.x = round(x_mm / 0.00000254)
        vertex.y = round(y_mm / 0.00000254)
        body.outline.append(vertex)
    raw = (
        g.MeshIllustrationMesh(
            id="body",
            # The first vertex is an asymmetric pin-1 direction oracle.
            positions=(
                4.0, 2.0, 0.0,
                -5.0, -3.0, 0.0,
                5.0, -3.0, 0.0,
                5.0, 3.0, 0.0,
                -5.0, 3.0, 0.0,
            ),
            indices=(0, 1, 2, 0, 2, 3, 0, 3, 4),
            materials=(g.MeshIllustrationMaterial(color=(0.5, 0.5, 0.5)),),
        ),
    )
    monkeypatch.setattr(
        illustration.IllustrationJob,
        "_body_geometry",
        lambda *args, **kwargs: (
            raw,
            illustration._rotation_z(90),
            None,
            "step",
        ),
    )
    monkeypatch.setattr(
        illustration,
        "_step_matrix",
        lambda *args, rotation_mode="instance_space", **kwargs: (
            illustration._rotation_z(90)
            if rotation_mode == "instance_space"
            else illustration._rotation_z(0)
        ),
    )
    job = illustration.IllustrationJob(None, emit_warnings=False)

    part = job._collect_mesh_body(
        body,
        0,
        SimpleNamespace(designator="IC3"),
        PcbAssemblyModelHelper(),
        {},
        {},
        (0.0, 0.0),
        (0.0, 0.0),
        "IC3",
        1.0,
        True,
    )

    assert part is not None
    assert part.bounds[:2] == pytest.approx((-5.0, -3.0))
    assert part.bounds[3:5] == pytest.approx((5.0, 3.0))
    assert part.meshes[0].positions[:2] == pytest.approx((4.0, 2.0))
    assert not job.diagnostics


def test_direct_path_retries_only_a_mismatched_current_candidate(monkeypatch):
    current_source = SimpleNamespace(name="current")
    local_source = SimpleNamespace(name="local")
    direct = illustration.DirectIllustrationSource(
        current_source,
        b"STEP",
        {"candidates": "fixture"},
        "asymmetric.step",
        local_source,
        (-5.0, -3.0, 5.0, 3.0),
    )
    part = illustration.IllustrationComponent(
        "IC3",
        (0.0, 0.0),
        (),
        (
            {
                "index": 0,
                "kind": "step",
                "lower_z_mm": 0.0,
                "upper_z_mm": 1.0,
                "color": None,
                "opacity": 1.0,
            },
        ),
        0,
        direct,
    )
    current = illustration.IllustrationSymbol(
        "<svg/>", 0, 0, 1, {}, (), (), (-3.0, -5.0, 0.0, 3.0, 5.0, 1.0)
    )
    local = illustration.IllustrationSymbol(
        "<svg/>", 0, 0, 1, {}, (), (), (-5.0, -3.0, 0.0, 5.0, 3.0, 1.0)
    )
    calls = []

    def render_source(self, source, model, side, illustrate):
        calls.append(source)
        return current if source is current_source else local

    monkeypatch.setattr(
        illustration.IllustrationJob, "_render_direct_source", render_source
    )
    job = illustration.IllustrationJob(None, emit_warnings=False)

    assert job._render_direct(part, "bottom", True) is local
    assert calls == [current_source, local_source]
    assert not job.diagnostics

    calls.clear()
    matched = illustration.DirectIllustrationSource(
        current_source,
        b"STEP",
        {"candidates": "matched"},
        "matched.step",
        local_source,
        (-3.0, -5.0, 3.0, 5.0),
    )
    matched_part = replace(part, direct=matched)
    assert job._render_direct(matched_part, "bottom", True) is current
    assert calls == [current_source]
