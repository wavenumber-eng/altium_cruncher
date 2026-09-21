"""Persistent results must preserve appearance, warning context, and rebuildability."""

from dataclasses import asdict, replace
from types import SimpleNamespace

import geometer as g
import pytest

from altium_cruncher.altium_cruncher_pcb_illustration import (
    IllustrationComponent,
    IllustrationJob,
    IllustrationSymbol,
    ModelGeometryError,
)
from altium_cruncher.pcb_illustration_model_geometry import IllustrationProjection
from altium_cruncher.altium_cruncher_pcb_svg_component_layers import (
    _illustration_instance_opacity,
)
from altium_cruncher.pcb_svg_model_cache import PcbSvgModelCache
from altium_cruncher import altium_cruncher_pcb_illustration as illustration


def cache(path, identity="a" * 64, **kwargs):
    return PcbSvgModelCache(path, identity=identity, **kwargs)


def mesh():
    return g.MeshIllustrationMesh(
        id="native-body",
        positions=(0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0),
        indices=(0, 1, 2),
        triangle_material_indices=(0,),
        materials=(g.MeshIllustrationMaterial(color=(0.5, 0.2, 0.3), opacity=0.8),),
    )


def test_projection_can_defer_authored_opacity_to_the_component_instance():
    projection = IllustrationProjection(
        """<svg xmlns="http://www.w3.org/2000/svg">
        <style>.paint { fill: #123456; opacity: 0.75; }</style>
        <path class="paint" d="M0 0L1 0L0 1Z"/>
        <path class="paint" d="M1 1L1 0L0 1Z"/>
        </svg>""",
        0,
        0,
        1,
    )

    symbol = projection.group("part", opaque_paint=True)
    paths = tuple(symbol.iter("{http://www.w3.org/2000/svg}path"))

    assert len(paths) == 2
    assert all(path.get("fill") == "#123456" for path in paths)
    assert all("opacity" not in path.attrib for path in paths)


def test_instance_opacity_requires_one_value_for_every_body():
    assert (
        _illustration_instance_opacity(
            SimpleNamespace(bodies=({"opacity": 0.75}, {"opacity": 0.75}))
        )
        == 0.75
    )
    assert (
        _illustration_instance_opacity(
            SimpleNamespace(bodies=({"opacity": 0.75}, {"opacity": 0.5}))
        )
        == 1.0
    )


def test_placed_geometry_reuses_arrays_but_preserves_instance_face_ids(monkeypatch):
    job = IllustrationJob(None)
    raw = (
        mesh(),
        replace(
            mesh(),
            id="invisible",
            materials=(g.MeshIllustrationMaterial(color=(1, 0, 0), opacity=0),),
        ),
        replace(mesh(), id="last"),
    )
    matrix = illustration._translation(0, 0, 2.54)
    calls = []
    original = illustration._placed_meshes

    def counted(*args):
        calls.append(1)
        return original(*args)

    monkeypatch.setattr(illustration, "_placed_meshes", counted)
    first = job._place_body(raw, matrix, None, 1, 3)
    second = job._place_body(raw, matrix, None, 1, 4)
    assert len(calls) == 1
    assert second == original(raw, matrix, None, 1, 4)
    assert [m.id for m in second] == ["body-4-face-0", "body-4-face-2"]
    assert all(a.positions is b.positions for a, b in zip(first, second))
    assert all(a.normals is b.normals for a, b in zip(first, second))
    for index, meshes in enumerate((first, second)):
        part = IllustrationComponent(f"U{index}", (index * 10, 20), meshes, ())
        appearance = [asdict(m) for m in meshes]
        for value in appearance:
            value.pop("id")
        expected = illustration._digest(
            dict(
                renderer_contract="geometer-b0-half-space-v5-scoped-apertures",
                meshes=appearance,
                line_width_mm=0.025,
                side="top",
                illustrate=True,
                clipping=None,
            )
        )
        key, warning_key = job._render_keys(part, "top", True)
        assert key == expected
        assert warning_key == illustration._digest(
            dict(appearance=expected, mesh_ids=[m.id for m in meshes])
        )
    assert len(job._appearance_keys) == 1


@pytest.mark.parametrize(
    "change",
    ["offset", "rotation", "mirror", "color", "opacity", "model", "source_matrix"],
)
def test_placed_geometry_cache_separates_changed_body_inputs(change):
    job = IllustrationJob(None)
    raw = (replace(mesh(), normals=(0.0, 0.0, 1.0) * 3),)
    matrix = illustration._translation(0, 0)
    job._place_body(raw, matrix, None, 1, 0)
    color, opacity = None, 1
    if change == "offset":
        matrix[2][3] = 2.54
    elif change == "rotation":
        matrix[0][:3], matrix[1][:3] = [0, -1, 0], [1, 0, 0]
    elif change == "mirror":
        matrix[0][0] = -1
    elif change == "color":
        color = (1.0, 0.0, 0.0)
    elif change == "opacity":
        opacity = 0.5
    elif change == "model":
        raw = (replace(raw[0], positions=tuple(v * 2 for v in raw[0].positions)),)
    elif change == "source_matrix":
        raw = (
            replace(raw[0], matrix=(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 3, 1)),
        )
    actual = job._place_body(raw, matrix, color, opacity, 7)
    assert actual == illustration._placed_meshes(raw, matrix, color, opacity, 7)
    assert len(job._placements) == 2


def test_appearance_keys_keep_body_order_side_width_and_line_only_mode():
    job = IllustrationJob(None)
    raw = (mesh(),)
    low = job._place_body(raw, illustration._translation(0, 0), None, 1, 0)
    high = job._place_body(raw, illustration._translation(0, 0, 3), (1, 0, 0), 1, 1)
    part = IllustrationComponent("D3", (0, 0), low + high, ())
    keys = {
        job._render_keys(part, "top", True)[0],
        job._render_keys(part, "bottom", True)[0],
        job._render_keys(part, "top", False)[0],
        job._render_keys(replace(part, meshes=high + low), "top", True)[0],
    }
    job.line_width_mm = 0.05
    keys.add(job._render_keys(part, "top", True)[0])
    assert len(keys) == 5


def test_clipping_policy_and_region_tolerance_participate_in_cache_identity(
    monkeypatch,
):
    region = SimpleNamespace(
        source_index=0,
        name="Rigid",
        outline_mils=((0.0, 0.0), (100.0, 0.0), (100.0, 100.0)),
        holes_mils=(),
        total_thickness_mils=40.0,
    )

    def render_key(*, query_tolerance=1e-6):
        region_index = SimpleNamespace(
            regions=(region,), invalid_regions=(), tolerance_mils=query_tolerance
        )
        job = IllustrationJob(None, region_index=region_index)
        part = IllustrationComponent("U1", (10.0, 20.0), (mesh(),), ())
        return job._render_keys(part, "top", True)[0]

    baseline = render_key()
    assert render_key(query_tolerance=2e-6) != baseline

    monkeypatch.setattr(illustration, "COMPONENT_CLIP_TOLERANCE_MM", 2e-6)
    tolerance_key = render_key()
    assert tolerance_key != baseline

    monkeypatch.setattr(illustration, "COMPONENT_CLIP_CAP_POLICY", "future-cap")
    assert render_key() != tolerance_key


def test_disk_reuse_preserves_meshes_svg_and_rebinds_partial_warnings(
    tmp_path, monkeypatch
):
    calls = []

    def tessellate(*args, **kwargs):
        calls.append("mesh")
        return SimpleNamespace(
            metadata=SimpleNamespace(warnings=("Partial: omitted 1 face",)),
            mesh_collection=SimpleNamespace(meshes=(mesh(),)),
        )

    symbol = IllustrationSymbol(
        '<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0L1 1"/></svg>',
        -1.0,
        2.0,
        0.0001,
        {"triangles": 1},
        (),
        (((0.0, 0.0), (1.0, 1.0)),),
    )

    def native(self, *args, **kwargs):
        calls.append("svg")
        return symbol

    monkeypatch.setattr(IllustrationJob, "_render_native", native)
    for designator in ("U1", "U2"):
        job = IllustrationJob(
            SimpleNamespace(model_tessellation=tessellate), cache=cache(tmp_path)
        )
        meshes = job._tessellate("content-hash", b"STEP", context=designator)
        assert meshes == (mesh(),)
        part = IllustrationComponent(designator, (10.0, 20.0), meshes, ())
        assert job.render(part, side="top") == symbol
        assert job.warnings == [f"{designator}: Partial: omitted 1 face"]
    assert calls == ["mesh", "svg"]
    assert (
        job.counts["tessellation_disk_hits"]
        == job.counts["illustration_disk_hits"]
        == 1
    )


def test_appearance_and_build_changes_miss_but_instance_names_reuse(
    tmp_path, monkeypatch
):
    calls = []

    def native(self, component, **kwargs):
        calls.append(component)
        return IllustrationSymbol(
            '<svg xmlns="http://www.w3.org/2000/svg"/>', 0.0, 0.0, 1.0, {}, ()
        )

    monkeypatch.setattr(IllustrationJob, "_render_native", native)
    base = IllustrationComponent("U1", (0.0, 0.0), (mesh(),), ())

    def draw(part=base, side="top", width=0.025, identity="a" * 64):
        return IllustrationJob(
            None, cache=cache(tmp_path, identity), line_width_mm=width
        ).render(part, side=side)

    draw()
    draw(
        replace(
            base,
            designator="U2",
            anchor_mm=(20.0, 20.0),
            meshes=(replace(mesh(), id="new-id"),),
        )
    )
    assert len(calls) == 1
    draw(side="bottom")
    draw(width=0.05)
    draw(identity="b" * 64)
    draw(
        replace(
            base,
            meshes=(
                replace(
                    mesh(), positions=(0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0)
                ),
            ),
        )
    )
    draw(
        replace(
            base,
            meshes=(
                replace(
                    mesh(),
                    materials=(g.MeshIllustrationMaterial(color=(1.0, 0.0, 0.0)),),
                ),
            ),
        )
    )
    assert len(calls) == 6


def test_corrupt_and_unwritable_cache_are_misses(tmp_path, caplog):
    store = cache(tmp_path)
    key = "c" * 64
    store.store("tessellation", key, {"result": [1, 2]})
    assert store.load("tessellation", key, lambda p: p) == {"result": [1, 2]}
    store._path("tessellation", key).write_bytes(b"truncated gzip")
    assert store.load("tessellation", key, lambda p: p) is None
    store.store("tessellation", key, {"result": [3]})
    assert store.load("tessellation", key, lambda p: p) == {"result": [3]}
    blocked = tmp_path / "file"
    blocked.write_text("user data")
    cache(blocked).store("illustration", key, {})
    assert blocked.read_text() == "user data"
    assert "rendering continues" in caplog.text
    assert not list(tmp_path.rglob("*.tmp"))


@pytest.mark.parametrize("kind", ["illustration", "component-artwork"])
def test_eviction_is_bounded_and_only_removes_generated_entries(tmp_path, kind):
    store = cache(tmp_path)
    sentinel = tmp_path / "keep.json.gz"
    sentinel.write_bytes(b"user data")
    nested = store.directory / ("a" * 64) / "foreign" / ("f" * 64 + ".json.gz")
    nested.parent.mkdir(parents=True)
    nested.write_bytes(b"foreign nested data")
    for digit in "123":
        store.store(kind, digit * 64, {"result": digit * 100})
    last = store._path(kind, "3" * 64)
    store.max_bytes = last.stat().st_size
    store.prune()
    assert last.exists()
    assert len(list(store.directory.rglob("*.json.gz"))) == 2
    assert sentinel.read_bytes() == b"user data"
    assert nested.read_bytes() == b"foreign nested data"


def test_native_failures_are_not_saved_across_jobs(tmp_path, monkeypatch):
    def fail(*args, **kwargs):
        raise g.GeometerOperationError("test", ())

    monkeypatch.setattr(IllustrationJob, "_render_native", fail)
    job = IllustrationJob(None, cache=cache(tmp_path))
    with pytest.raises(ModelGeometryError):
        job.render(IllustrationComponent("U1", (0.0, 0.0), (mesh(),), ()), side="top")
    assert not list(tmp_path.rglob("*.json.gz"))


def test_warning_bearing_artwork_reuses_only_matching_request_ids(
    tmp_path, monkeypatch
):
    calls = []

    def native(self, part, **kwargs):
        calls.append(part.meshes[0].id)
        return IllustrationSymbol(
            '<svg xmlns="http://www.w3.org/2000/svg"/>',
            0.0,
            0.0,
            1.0,
            {},
            (f"Skipped triangle in {part.meshes[0].id}",),
        )

    monkeypatch.setattr(IllustrationJob, "_render_native", native)
    for mesh_id in ("body-1", "body-1", "body-2", "body-2"):
        job = IllustrationJob(None, cache=cache(tmp_path))
        part = IllustrationComponent(
            "U1", (0.0, 0.0), (replace(mesh(), id=mesh_id),), ()
        )
        symbol = job.render(part, side="top")
        assert symbol.warnings == (f"Skipped triangle in {mesh_id}",)
        assert job.warnings == list(symbol.warnings)
    assert calls == ["body-1", "body-2"]


@pytest.mark.parametrize(
    "field,value", [("mm_per_unit", "bad"), ("mm_per_unit", 0), ("x_mm", True)]
)
def test_invalid_cached_symbol_geometry_is_a_rebuildable_miss(tmp_path, field, value):
    disk = cache(tmp_path)
    payload = asdict(
        IllustrationSymbol('<svg xmlns="http://www.w3.org/2000/svg"/>', 0, 0, 1, {}, ())
    )
    payload[field] = value
    key = "b" * 64
    disk.store("illustration", key, payload)
    assert disk.load("illustration", key, illustration._decode_cached_symbol) is None
    assert disk.counts["invalid"] == 1


@pytest.mark.parametrize(
    "field,value",
    [
        ("indices", [0, 1, 999]),
        ("indices", [0, True, 2]),
        ("triangle_material_indices", [3]),
        ("normals", [0, 0, 1]),
    ],
)
def test_invalid_cached_mesh_geometry_is_a_rebuildable_miss(tmp_path, field, value):
    disk = cache(tmp_path)
    payload = asdict(mesh())
    payload[field] = value
    key = "c" * 64
    disk.store("tessellation", key, dict(meshes=[payload], warnings=[]))
    assert (
        disk.load("tessellation", key, illustration._decode_cached_tessellation) is None
    )
    assert disk.counts["invalid"] == 1
