"""Early artwork hits must preserve diagnostics and retry omitted geometry."""

from contextlib import nullcontext
from types import SimpleNamespace

import geometer as g
import pytest

from altium_cruncher import altium_cruncher_pcb_illustration as illustration
from altium_cruncher import pcb_svg_component_cache as artwork
from altium_cruncher.altium_cruncher_pcb_svg_component_layers import ComponentLayerSession
from altium_cruncher.pcb_svg_model_cache import PcbSvgModelCache


@pytest.fixture
def scene(monkeypatch, tmp_path):
    bodies = [SimpleNamespace(component_index=owner, model_type=0,
              properties={"index": i}, body_color_3d=255, body_opacity_3d=.5)
              for i, owner in enumerate((0, 1, 0, 2))]
    pcb = SimpleNamespace(component_bodies=bodies,
                          components=[SimpleNamespace(designator=f"U{i}") for i in range(3)])
    helper = SimpleNamespace(_collect_embedded_step_model_catalog=lambda pcb: ([], []),
                             _component_body_is_bottom=lambda *args: False)
    monkeypatch.setattr(illustration, "PcbAssemblyModelHelper", lambda: helper)
    for module in (illustration, artwork):
        monkeypatch.setattr(module, "_body_anchor", lambda helper, body, component: (0., 0.))
    monkeypatch.setattr(
        illustration.IllustrationJob, "_collect_direct_body", lambda *args, **kwargs: None
    )
    monkeypatch.setattr(
        illustration.IllustrationJob,
        "_collect_direct_analytic_group",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(artwork, "_extrusion_request", lambda body, *args, **kwargs: body.properties)
    monkeypatch.setattr(g, "GeometerClient", lambda: nullcontext(None))
    raw = (g.MeshIllustrationMesh(id="face", positions=(0., 0., 0., 1., 0., 0., 0., 1., 1.),
           indices=(0, 1, 2), materials=(g.MeshIllustrationMaterial(color=(1., 0., 0.)),)),)
    calls = []

    def geometry(self, body, *args):
        index = body.properties["index"]
        calls.append(index)
        self.warn("shared diagnostic")
        if index == 3:
            raise illustration.ModelGeometryError("retry this missing body")
        return raw, illustration._translation(0, 0, index), (1., 0., 0.), "extruded"

    def native(self, part, *, side, illustrate):
        return illustration.IllustrationSymbol(
            '<svg xmlns="http://www.w3.org/2000/svg"/>', 0., 0., 1.,
            dict(painted=illustrate), (f"native {part.meshes[0].id}",),
            (((0., 0.), (1., 1.)),))

    monkeypatch.setattr(illustration.IllustrationJob, "_body_geometry", geometry)
    monkeypatch.setattr(illustration.IllustrationJob, "_render_native", native)
    def cache():
        return PcbSvgModelCache(tmp_path, identity="a" * 64)

    return pcb, cache, calls


def snapshot(placed):
    return [(p.designator, p.anchor_mm, p.component_index, p.bounds, s)
            for p, s in placed]


def test_warm_artwork_skips_positive_geometry_preserves_body_order_and_retries_failures(scene):
    pcb, cache, calls = scene
    cold = ComponentLayerSession(cache=cache())
    expected = snapshot(cold._materialize(pcb, "top", .025, True))
    assert calls == [0, 1, 2, 3]
    calls.clear()
    warm = ComponentLayerSession(cache=cache())
    actual = warm._materialize(pcb, "top", .025, True)
    assert snapshot(actual) == expected
    assert calls == [3]
    assert warm.job.warnings == cold.job.warnings
    assert [b["index"] for p, _ in actual for b in p.bodies] == [1, 0, 2]
    assert all(not hasattr(p, "meshes") for p, _ in actual)


def test_style_changes_recollect_without_duplicating_geometry_warnings(scene):
    pcb, cache, calls = scene
    baseline = ComponentLayerSession()
    styles = [("top", .025, False), ("top", .025, True), ("top", .05, True)]
    expected = [snapshot(baseline._materialize(pcb, *style)) for style in styles]
    for _ in range(2):  # Empty and then populated artwork cache.
        session = ComponentLayerSession(cache=cache())
        assert [snapshot(session._materialize(pcb, *style)) for style in styles] == expected
        assert session.job.warnings == baseline.job.warnings
        assert session.job._suppress_collection_warnings is False


def test_incomplete_warning_producer_and_its_consumers_retry_together(scene, monkeypatch):
    pcb, cache, calls = scene
    raw = (g.MeshIllustrationMesh(id="face", positions=(0., 0., 0., 1., 0., 0., 0., 1., 1.),
           materials=(g.MeshIllustrationMaterial(color=(1., 0., 0.)),)),)

    def geometry(self, body, *args):
        index = body.properties["index"]
        calls.append(index)
        if index == 2:
            raise illustration.ModelGeometryError("second body failed")
        # U0 is incomplete but lends its diagnostic-bearing symbol to U1.
        return raw, illustration._translation(0, 0, 0 if index < 2 else 3), None, "extruded"

    monkeypatch.setattr(illustration.IllustrationJob, "_body_geometry", geometry)
    cold = ComponentLayerSession(cache=cache())
    original = cold._materialize(pcb, "top", .025, True)
    assert original[0][1] is original[1][1]
    bundle = artwork.ComponentArtworkCache(cold.job, pcb, "top", True, frozenset())
    payload = cold.cache.load("component-artwork", bundle.key, lambda value: value)
    assert [entry["placement"]["designator"] for entry in payload["entries"]] == ["U2"]
    calls.clear()
    warm = ComponentLayerSession(cache=cache())
    actual = warm._materialize(pcb, "top", .025, True)
    assert snapshot(actual) == snapshot(original)
    assert actual[0][1] is actual[1][1]
    assert calls == [0, 1, 2]
    assert warm.job.warnings == cold.job.warnings


@pytest.mark.parametrize("change", ["color", "opacity", "recipe", "designator", "width", "side", "mode"])
def test_exact_recipe_or_style_changes_do_not_reuse_old_placements(scene, change):
    pcb, cache, calls = scene
    session = ComponentLayerSession(cache=cache())
    session._materialize(pcb, "top", .025, True)
    side, width, mode = "top", .025, True
    if change == "color":
        pcb.component_bodies[0].body_color_3d = 65535
    elif change == "opacity":
        pcb.component_bodies[0].body_opacity_3d = .75
    elif change == "recipe":
        pcb.component_bodies[0].properties["height"] = 2.54
    elif change == "designator":
        pcb.components[0].designator = "renamed"
    elif change == "width":
        width = .05
    elif change == "side":
        side = "bottom"
    else:
        mode = False
    job = illustration.IllustrationJob(None, cache=cache(), line_width_mm=width)
    assert artwork.ComponentArtworkCache(job, pcb, side, mode, frozenset()).load() == {}


@pytest.mark.parametrize("damage", ["owner", "kind", "z", "color", "opacity", "transform", "outline", "huge_coordinate"])
def test_malformed_artwork_becomes_a_cache_miss(scene, damage):
    pcb, cache, calls = scene
    session = ComponentLayerSession(cache=cache())
    session._materialize(pcb, "top", .025, True)
    store = cache()
    key = artwork.ComponentArtworkCache(session.job, pcb, "top", True, frozenset()).key
    payload = store.load("component-artwork", key, lambda value: value)
    placement = payload["entries"][0]["placement"]
    body = placement["bodies"][0]
    symbol = next(iter(payload["symbols"].values()))
    if damage == "owner":
        placement["component_index"] = []
    elif damage == "kind":
        del body["kind"]
    elif damage == "z":
        body["lower_z_mm"] = "bad"
    elif damage == "color":
        body["color"] = [1]
    elif damage == "opacity":
        body["opacity"] = -1
    elif damage == "transform":
        symbol["mm_per_unit"] = 0
    elif damage == "outline":
        symbol["outline_segments_mm"] = [[[0, 1]]]
    else:
        placement["anchor_mm"][0] = 10 ** 400
    store.store("component-artwork", key, payload)
    job = illustration.IllustrationJob(None, cache=store)
    assert artwork.ComponentArtworkCache(job, pcb, "top", True, frozenset()).load() == {}
    assert not job._early_components
