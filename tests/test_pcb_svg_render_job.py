"""SVG reuse must preserve populations, document identity, and text dependencies."""

from copy import copy
from dataclasses import replace
import json
from pathlib import Path
from types import SimpleNamespace
import xml.etree.ElementTree as ET

from altium_monkey.altium_board import (
    AltiumBoard,
    AltiumBoardOutline,
    BoardOutlineVertex,
)
from altium_monkey.altium_pcb_component import AltiumPcbComponent
from altium_monkey.altium_pcbdoc import AltiumPcbDoc
from altium_monkey.altium_record_pcb__component_body import AltiumPcbComponentBody
from altium_monkey.altium_record_pcb__shapebased_region import PcbExtendedVertex
from altium_monkey.altium_record_pcb__text import AltiumPcbText
from altium_monkey.altium_record_types import PcbLayer
from jsonschema import Draft202012Validator
import pytest

from altium_cruncher.altium_cruncher_pcb_svg_renderer import PcbSvgCompositeRenderer
from altium_cruncher.altium_cruncher_pcb_svg_component_layers import (
    ComponentLayerSession,
    _renumber_population_entries,
)
from altium_cruncher.altium_cruncher_pcb_svg_config import (
    PcbSvgConfig,
    PcbSvgViewConfig,
)
from altium_cruncher.pcb_svg_render_job import PcbSvgRenderJob
from altium_cruncher.pcb_svg_model_cache import PcbSvgModelCache

SVG = "http://www.w3.org/2000/svg"


def test_population_metadata_renumbers_surface_and_aperture_symbols():
    entries = [
        {
            "symbol_id": "old-surface",
            "aperture_symbol_id": "old-aperture",
            "anchor_svg_mm": [5.0, 6.0],
            "bounds_local_xyz_mm": [0.0, 0.0, 0.0, 1.0, 1.0, 1.0],
        }
    ]
    ids, _bounds = _renumber_population_entries(
        entries,
        {"token": "ILLUSTRATION_TOP"},
        SimpleNamespace(options=SimpleNamespace(mirror_x=False), width_mm=10.0),
    )

    assert entries[0]["symbol_id"] == ids["old-surface"]
    assert entries[0]["aperture_symbol_id"] == ids["old-aperture"]
    assert entries[0]["symbol_id"] != entries[0]["aperture_symbol_id"]


@pytest.mark.parametrize("fails", [False, True])
def test_render_job_prunes_model_cache_once_on_every_exit(
    tmp_path, monkeypatch, fails
):
    store = PcbSvgModelCache(tmp_path, identity="a" * 64)
    calls = 0

    def prune():
        nonlocal calls
        calls += 1

    monkeypatch.setattr(store, "prune", prune)
    if fails:
        with pytest.raises(RuntimeError, match="test failure"):
            with PcbSvgRenderJob(model_cache=store):
                raise RuntimeError("test failure")
    else:
        with PcbSvgRenderJob(model_cache=store):
            pass

    assert calls == 1


@pytest.mark.parametrize("component_side", ["top", "bottom"])
@pytest.mark.parametrize("view_side", ["top", "bottom"])
@pytest.mark.parametrize("has_model", [False, True])
def test_projected_designator_belongs_only_to_component_placement_side(
    component_side, view_side, has_model
):
    component = AltiumPcbComponent("R1", "test", component_side.upper(), "0mil", "0mil")
    renderer = PcbSvgCompositeRenderer(PcbSvgConfig.default())

    actual = ComponentLayerSession()._visible_designator(
        renderer, component, has_model, view_side
    )

    assert actual == ("R1" if component_side == view_side else None)


def test_toon_projected_designator_requires_a_renderable_model():
    component = AltiumPcbComponent("R1", "test", "TOP", "0mil", "0mil")
    renderer = PcbSvgCompositeRenderer(PcbSvgConfig.default())
    session = ComponentLayerSession()

    assert (
        session._visible_designator(
            renderer, component, False, "top", require_model=True
        )
        is None
    )
    assert session._visible_designator(
        renderer, component, True, "top", require_model=True
    ) == "R1"


@pytest.mark.parametrize("film", [False, True])
def test_primitive_dispatch_reuses_ordinary_methods_and_preserves_dynamic_callables(
    monkeypatch, film
):
    import inspect
    from types import MethodType
    from altium_monkey.altium_pcb_svg_renderer import PcbSvgRenderer
    from altium_cruncher.altium_cruncher_pcb_svg_soldermask_film import (
        SoldermaskFilmRenderer,
    )

    renderer = (
        SoldermaskFilmRenderer() if film else PcbSvgCompositeRenderer(PcbSvgConfig.default())
    )
    original = PcbSvgRenderer._to_svg_accepts_for_layer
    calls = []

    def inspect_once(method):
        calls.append(method)
        return original(method)

    monkeypatch.setattr(
        PcbSvgRenderer, "_to_svg_accepts_for_layer", staticmethod(inspect_once)
    )

    class Primitive:
        def to_svg(self, context, *, for_layer=None):
            pass

    for _ in range(10):
        assert renderer._to_svg_accepts_for_layer(Primitive().to_svg)
    assert len(calls) == 1
    Primitive.to_svg.__signature__ = inspect.Signature(
        [
            inspect.Parameter("self", inspect.Parameter.POSITIONAL_OR_KEYWORD),
        ]
    )
    assert not renderer._to_svg_accepts_for_layer(Primitive().to_svg)
    del Primitive.to_svg.__signature__
    assert renderer._to_svg_accepts_for_layer(Primitive().to_svg)

    class UnhashableCallable:
        __hash__ = None

        def __call__(self, bound, *, for_layer=None):
            pass

    custom = MethodType(UnhashableCallable(), object())
    assert renderer._to_svg_accepts_for_layer(custom) == original(custom)


def board():
    pcb = AltiumPcbDoc()
    pcb.board = AltiumBoard(
        outline=AltiumBoardOutline.rectangle_mils(
            left_mils=0, bottom_mils=0, right_mils=1000, top_mils=1000
        )
    )
    return pcb


def draw(renderer, pcb, layers, parameters=None, *, mirror=False):
    view = PcbSvgViewConfig(name="test", layers=layers)
    return renderer.render_view_svg(
        pcb,
        view,
        project_parameters=parameters,
        layers=layers,
        group_id="review",
        mirror=mirror,
        styles=renderer.config.resolved_styles_for_view(view),
    )


@pytest.mark.parametrize("side", ["top", "bottom"])
def test_population_composition_matches_fresh_render_and_keeps_cached_base(side):
    pcb = board()
    for i in range(3):
        pcb.components.append(
            AltiumPcbComponent(
                f"U{i + 1}",
                "test",
                side.upper(),
                f"{i * 250}mil",
                "0mil",
                unique_id=f"uid{i}",
            )
        )
        body = AltiumPcbComponentBody()
        body.component_index = i
        body.properties = {
            "MODEL.2D.X": "0mil",
            "MODEL.2D.Y": "0mil",
            "BODYPROJECTION": "1" if side == "bottom" else "0",
            "MODEL.EXTRUDED.MINZ": "0mil",
            "MODEL.EXTRUDED.MAXZ": "100mil",
        }
        body.model_extruded_min_z, body.model_extruded_max_z = 0, 1_000_000
        body.body_color_3d = (0x00CC33, 0x0000FF, 0x00CC33)[i]
        for x, y in [(0, 0), (100, 0), (100, 200), (0, 200)]:
            vertex = PcbExtendedVertex()
            vertex.x, vertex.y = x * 10000, y * 10000
            body.outline.append(vertex)
        pcb.component_bodies.append(body)
    config = PcbSvgConfig.default()
    layers = [
        "BOARD_OUTLINE",
        "ILLUSTRATION_" + side.upper(),
        "ASSEMBLY_DESIGNATORS_" + side.upper(),
    ]
    job = PcbSvgRenderJob()
    job.register_board(pcb)
    base_renderer = PcbSvgCompositeRenderer(config, render_job=job)
    base = draw(base_renderer, pcb, layers, mirror=side == "bottom")
    before = dict(base_renderer.component_layers.job.counts)
    variant = copy(pcb)
    variant.components = [
        replace(c, parameters={"Value": "variant"}) for c in pcb.components
    ]
    job.register_variant(variant, pcb)
    excluded = frozenset(
        {"U1", "U2"}
    )  # Removes first use of a shared symbol and an entire color.
    selected = PcbSvgCompositeRenderer(config, render_job=job, excluded_designators=excluded)
    actual = draw(selected, variant, layers, mirror=side == "bottom")
    fresh = draw(
        PcbSvgCompositeRenderer(config, excluded_designators=excluded),
        variant,
        layers,
        mirror=side == "bottom",
    )
    actual_root, fresh_root, base_root = map(ET.fromstring, (actual, fresh, base))
    illustration_id = "layer-" + ("9013" if side == "bottom" else "9012")

    def group(root, identity):
        return root.find(f".//{{{SVG}}}g[@id='{identity}']")

    assert ET.tostring(group(actual_root, illustration_id)) == ET.tostring(
        group(fresh_root, illustration_id)
    )
    label_id = f"assembly_designators_{side}-component-2"
    assert ET.tostring(group(actual_root, label_id)) == ET.tostring(
        group(base_root, label_id)
    )
    # The existing autodoc fit cache rounds geometry keys, while its solver uses
    # unrounded points. An independently fitted population can land one binary
    # search step away. Cached composition must retain the exact prepared label.
    a_text = group(actual_root, label_id).find(f"{{{SVG}}}text")
    b_text = group(fresh_root, label_id).find(f"{{{SVG}}}text")
    for attr in ("x", "y"):
        assert float(a_text.get(attr)) == pytest.approx(
            float(b_text.get(attr)), abs=1e-9, rel=0
        )
    assert float(a_text.get("font-size")) == pytest.approx(
        float(b_text.get("font-size")), abs=0.0011, rel=0
    )
    a_meta = json.loads(actual_root.find(f"{{{SVG}}}metadata").text)
    b_meta = json.loads(fresh_root.find(f"{{{SVG}}}metadata").text)
    assert (
        a_meta["virtual_component_layers"]["layers"][0]
        == b_meta["virtual_component_layers"]["layers"][0]
    )
    assert (
        a_meta["virtual_component_layers"]["layers"][1]["instances"][0][
            "rotation_degrees"
        ]
        == b_meta["virtual_component_layers"]["layers"][1]["instances"][0][
            "rotation_degrees"
        ]
    )
    a_meta.pop("virtual_component_layers")
    b_meta.pop("virtual_component_layers")
    assert a_meta == b_meta
    assert actual_root.get("viewBox") == fresh_root.get("viewBox")
    assert base_renderer.component_layers.job.counts == before
    assert draw(base_renderer, pcb, layers, mirror=side == "bottom") == base
    root = ET.fromstring(actual)
    ids = [n.get("id") for n in root.iter() if n.get("id")]
    assert len(ids) == len(set(ids))
    assert all(n.get("href")[1:] in ids for n in root.iter(f"{{{SVG}}}use"))
    metadata = json.loads(root.find(f"{{{SVG}}}metadata").text)
    assert all(
        [e["designator"] for e in layer["instances"]] == ["U3"]
        for layer in metadata["virtual_component_layers"]["layers"]
    )


def test_variant_mask_text_and_style_invalidate_fragments():
    pcb = board()
    text = AltiumPcbText()
    text.layer = PcbLayer.TOP_SOLDER
    text.text_content = ".VariantName"
    text.x = text.y = 1_000_000
    text.height = 400_000
    pcb.texts.append(text)
    config = PcbSvgConfig.default()
    job = PcbSvgRenderJob()
    renderer = PcbSvgCompositeRenderer(config, render_job=job)
    layers = ["BOARD_OUTLINE", "SOLDERMASK_FILM_TOP"]
    first = draw(renderer, pcb, layers, {"VariantName": "ABC", "unused": "A"})
    repeated = draw(renderer, pcb, layers, {"VariantName": "ABC", "unused": "B"})
    assert repeated == first
    assert all(e["cache"] == "hit" for e in job.events[-2:])
    second = draw(renderer, pcb, layers, {"VariantName": "XYZ"})
    assert second != first
    assert second == draw(PcbSvgCompositeRenderer(config), pcb, layers, {"VariantName": "XYZ"})
    config.global_options.styles["soldermask_film"]["color"] = "#EEEEEE"
    changed = draw(renderer, pcb, layers, {"VariantName": "XYZ"})
    assert changed != second
    assert changed == draw(
        PcbSvgCompositeRenderer(config), pcb, layers, {"VariantName": "XYZ"}
    )


def test_unrelated_documents_with_shared_board_do_not_share_stack(monkeypatch):
    from altium_monkey.altium_pcb_svg_renderer import PcbSvgRenderer

    a, b = board(), board()
    b.board = a.board
    calls = []

    def resolve(pcb):
        calls.append(pcb)
        return object()

    monkeypatch.setattr(
        PcbSvgRenderer, "_resolved_layer_stack_safe", staticmethod(resolve)
    )
    renderer = PcbSvgCompositeRenderer(PcbSvgConfig.default())
    first = renderer._resolved_layer_stack_safe(a)
    assert renderer._resolved_layer_stack_safe(a) is first
    assert renderer._resolved_layer_stack_safe(b) is not first
    assert calls == [a, b]


def test_region_envelope_index_reuses_source_across_variants(monkeypatch):
    from altium_cruncher.pcb_board_region_envelope_index import (
        BoardRegionEnvelopeIndex,
    )

    pcb = board()
    variant = copy(pcb)
    job = PcbSvgRenderJob()
    job.register_variant(variant, pcb)
    built = object()
    calls = []
    resolved = object()

    class Document:
        @staticmethod
        def to_resolved_layer_stack():
            return resolved

    document = Document()

    def build(source_document, source_resolved):
        calls.append((source_document, source_resolved))
        return built

    monkeypatch.setattr(job, "layer_stack_document", lambda _source: document)
    monkeypatch.setattr(
        BoardRegionEnvelopeIndex, "from_layer_stack_document", staticmethod(build)
    )

    assert job.board_region_envelopes(pcb) is built
    assert job.board_region_envelopes(variant) is built
    assert calls == [(document, resolved)]


def test_cutout_scopes_share_variant_artwork_but_keep_distinct_film():
    pcb = board()
    pcb.board.outline.cutouts = [
        [BoardOutlineVertex.line(x, y) for x, y in points]
        for points in (
            [(200, 200), (400, 200), (400, 400), (200, 400)],
            [(0, 600), (100, 600), (100, 700), (0, 700)],
        )
    ]
    pcb.components = [AltiumPcbComponent("J1", "pads", "TOP", "0mil", "0mil")]
    variant = copy(pcb)
    variant.components = [replace(pcb.components[0], parameters={"Value": "changed"})]
    job = PcbSvgRenderJob()
    job.register_board(pcb)
    job.register_variant(variant, pcb)
    interior = job.scoped_document(pcb, "interior")
    selected = job.scoped_document(variant, "interior")
    assert len(pcb.board.outline.cutouts) == 2
    assert len(interior.board.outline.cutouts) == 1
    assert selected.board is interior.board
    assert selected.components is variant.components
    assert job.geometry_source(selected) is pcb
    assert job.components(selected) is job.components(pcb)
    config = PcbSvgConfig.default()
    renderer = PcbSvgCompositeRenderer(config, render_job=job)
    layers = ["BOARD_OUTLINE", "SOLDERMASK_FILM_TOP"]
    all_svg = draw(renderer, pcb, layers)
    config.global_options.styles["board_cutouts"]["scope"] = "interior"
    interior_svg = draw(renderer, pcb, layers)
    assert all_svg != interior_svg
    assert interior_svg == draw(PcbSvgCompositeRenderer(config), pcb, layers)


def test_mixed_view_timings_and_failure_report_follow_contract(tmp_path):
    job = PcbSvgRenderJob()
    renderer = PcbSvgCompositeRenderer(PcbSvgConfig.default(), render_job=job)
    draw(renderer, board(), ["TOP", "BOTTOM", "BOARD_OUTLINE"])
    assert next(e for e in job.events if e["stage"] == "view")["side"] == "both"
    sides = {e["layer"]: e["side"] for e in job.events if e["stage"] == "layer"}
    assert sides == {"TOP": "top", "BOTTOM": "bottom", "BOARD_OUTLINE": "board"}
    with pytest.raises(RuntimeError), job.measure("job", command="test"):
        with job.measure("layer", layer="TOP", side="top"):
            raise RuntimeError("failure")
    target = tmp_path / "timings.json"
    job.write_timings(target)
    payload = json.loads(target.read_text())
    schema = json.loads(
        (
            Path(__file__).parents[1] / "docs/contracts/pcb_svg_timings.a0.schema.json"
        ).read_text()
    )
    Draft202012Validator(schema).validate(payload)
    assert payload["events"][-1]["failed"] and payload["events"][-2]["failed"]
    for event in payload["events"]:
        assert 0 <= event["exclusive_seconds"] <= event["seconds"]
        if event["parent_id"] is not None:
            assert event["parent_id"] < event["id"]


def test_context_reuse_keeps_variant_metadata_and_parameters_independent():
    pcb = board()
    pcb.components = [
        AltiumPcbComponent(
            "U1", "test", "TOP", "0mil", "0mil", parameters={"Value": "base"}
        )
    ]
    variant = copy(pcb)
    variant.components = [replace(pcb.components[0], parameters={"Value": "variant"})]
    job = PcbSvgRenderJob()
    job.register_variant(variant, pcb)
    config = PcbSvgConfig.default()
    renderer = PcbSvgCompositeRenderer(config, render_job=job)
    first = renderer._build_context(pcb, {"NAME": "base"})
    renderer.options = replace(
        renderer.options, mirror_x=True, visible_layers=[PcbLayer.BOTTOM]
    )
    second = renderer._build_context(variant, {"name": "variant"})
    assert len(job.contexts) == 1
    assert first is not second
    assert not first.options.mirror_x and second.options.mirror_x
    assert first.substitute_special_strings(".Name") == "base"
    assert second.substitute_special_strings(".Name") == "variant"
    assert second.component_data_by_index != first.component_data_by_index
    assert (
        second.component_data_by_index
        == PcbSvgCompositeRenderer(config)._build_context(variant).component_data_by_index
    )
    renderer.options = replace(renderer.options, include_metadata=False)
    renderer._build_context(pcb)
    assert len(job.contexts) == 2


def test_saved_silk_designators_survive_muted_graphics_and_reuse_fragments():
    pcb = board()
    pcb.components = [AltiumPcbComponent("U1", "test", "TOP", "100mil", "100mil")]
    for index, label in enumerate(("U1", "component-art", "board-art")):
        text = AltiumPcbText()
        text.layer = PcbLayer.TOP_OVERLAY
        text.component_index = 0 if index < 2 else None
        text.is_designator = index == 0
        text.text_content = label
        text.x, text.y, text.height = 1_000_000, (index + 1) * 1_000_000, 200_000
        pcb.texts.append(text)
    config = PcbSvgConfig.default()
    job = PcbSvgRenderJob()
    renderer = PcbSvgCompositeRenderer(config, render_job=job)
    full = draw(renderer, pcb, ["TOPOVERLAY"])
    for name in ("silkscreen_component_graphics", "silkscreen_board_graphics"):
        config.global_options.styles[name]["enabled"] = False
    muted = draw(renderer, pcb, ["TOPOVERLAY"])
    assert muted != full
    assert muted == draw(PcbSvgCompositeRenderer(config), pcb, ["TOPOVERLAY"])
    reused = [e for e in job.events if e["stage"] == "silk_chunk"][-1]
    assert reused["part"] == "silkscreen_designators_text" and reused["cache"] == "hit"
    config.global_options.styles["silkscreen_designators"]["enabled"] = False
    assert draw(renderer, pcb, ["TOPOVERLAY"]) != muted
