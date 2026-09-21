"""Layer indexing must preserve V7 identity, custom dispatch and paint order."""

from types import MethodType, SimpleNamespace

import pytest
from altium_monkey.altium_board import AltiumBoard, AltiumBoardOutline
from altium_monkey.altium_pcbdoc import AltiumPcbDoc
from altium_monkey.altium_pcb_layer_ref import PcbLayerRef
from altium_monkey.altium_pcb_svg_renderer import PcbSvgRenderer, PcbSvgRenderOptions
from altium_monkey.altium_record_pcb__pad import AltiumPcbPad
from altium_monkey.altium_record_pcb__via import AltiumPcbVia
from altium_monkey.altium_record_pcb__region import AltiumPcbRegion, RegionVertex
from altium_monkey.altium_record_pcb__shapebased_region import AltiumPcbShapeBasedRegion
from altium_monkey.altium_record_pcb__track import AltiumPcbTrack
from altium_monkey.altium_record_pcb__text import AltiumPcbText
from altium_monkey.altium_record_types import PcbLayer

from altium_cruncher import pcb_svg_primitive_index as indexing
from altium_cruncher.altium_cruncher_pcb_svg_soldermask_film import SoldermaskFilmRenderer
from altium_cruncher.altium_cruncher_pcb_svg_renderer import PcbSvgCompositeRenderer
from altium_cruncher.altium_cruncher_pcb_svg_config import PcbSvgConfig
from altium_cruncher.pcb_svg_render_job import PcbSvgRenderJob


@pytest.mark.parametrize("cls", list(indexing._METHODS))
def test_v7_identity_overrides_placeholder_legacy_byte(cls):
    top, bottom, mechanical = cls(), cls(), cls()
    top.layer, bottom.layer, mechanical.layer = PcbLayer.TOP, PcbLayer.BOTTOM, PcbLayer.TOP
    ref = PcbLayerRef.parse("MECHANICAL17")
    if cls in (AltiumPcbRegion, AltiumPcbShapeBasedRegion):
        mechanical.v7_layer = ref.token
    elif cls is AltiumPcbText:
        mechanical.barcode_layer_v7 = ref.v7_saved_layer_id
    else:
        mechanical.v7_layer_id = ref.v7_saved_layer_id
    records = [top, mechanical, bottom]
    index = indexing.PrimitiveLayerIndex()
    assert index.candidates(records, PcbLayer.TOP) == (top,)
    assert index.candidates(records, PcbLayer.BOTTOM) == (bottom,)
    assert index.candidates(records, ref) == (mechanical,)
    assert index.candidates(records, None) is records


def test_layer_facts_reuse_across_subsets_without_merging_document_identities(monkeypatch):
    calls = []
    original = indexing.svg_layer_ref
    monkeypatch.setattr(indexing, "svg_layer_ref", lambda p: (calls.append(p), original(p))[1])
    top, bottom = AltiumPcbTrack(), AltiumPcbTrack()
    top.layer, bottom.layer = PcbLayer.TOP, PcbLayer.BOTTOM
    records = [top, bottom]
    index = indexing.PrimitiveLayerIndex()
    index.candidates(records, PcbLayer.TOP)
    index.candidates(records, PcbLayer.BOTTOM)
    index.candidates([bottom], PcbLayer.BOTTOM)
    assert calls == [top, bottom]
    other_board_track = AltiumPcbTrack()
    other_board_track.layer = PcbLayer.BOTTOM
    assert index.candidates([other_board_track], PcbLayer.TOP) == ()
    assert calls == [top, bottom, other_board_track]


def test_unmapped_legacy_and_multilayer_simple_records_follow_native_matching():
    unknown, multi = AltiumPcbTrack(), AltiumPcbTrack()
    unknown.layer = 0
    unknown.v7_layer_id = PcbLayerRef.parse("MECHANICAL17").v7_saved_layer_id
    multi.layer = PcbLayer.MULTI_LAYER
    records = [unknown, multi]
    index = indexing.PrimitiveLayerIndex()
    assert index.candidates(records, 0) == (unknown,)
    assert index.candidates(records, PcbLayer.TOP) == ()
    assert index.candidates(records, PcbLayer.MULTI_LAYER) == (multi,)


def scene():
    pcb = AltiumPcbDoc()
    pcb.board = AltiumBoard(outline=AltiumBoardOutline.rectangle_mils(
        left_mils=0, bottom_mils=0, right_mils=1000, top_mils=1000))
    top, bottom = AltiumPcbTrack(), AltiumPcbTrack()
    top.layer, bottom.layer = PcbLayer.TOP, PcbLayer.BOTTOM
    for track in (top, bottom):
        track.end_x, track.end_y, track.width = 1000000, 2000000, 100000
    pcb.tracks = [top, bottom]
    options = PcbSvgRenderOptions(include_metadata=False)
    baseline, indexed = PcbSvgRenderer(options), SoldermaskFilmRenderer(options)
    ctx = baseline._build_context(pcb, project_parameters=None)
    return pcb, ctx, baseline, indexed


def test_custom_renderers_pads_vias_and_instance_overrides_keep_original_order():
    pcb, ctx, baseline, indexed = scene()

    class Custom:
        layer = PcbLayer.BOTTOM
        def to_svg(self, ctx, **kwargs):
            return ['<path id="custom"/>']

    class Subclass(AltiumPcbTrack):
        def to_svg(self, ctx, **kwargs):
            return ['<path id="subclass"/>']

    overridden = AltiumPcbTrack()
    overridden.layer = PcbLayer.BOTTOM
    overridden.to_svg = MethodType(lambda self, ctx, **kwargs: ['<path id="override"/>'], overridden)
    records = [Custom(), pcb.tracks[1], AltiumPcbPad(), pcb.tracks[0],
               Subclass(), AltiumPcbVia(), overridden]
    assert indexed._primitive_index.candidates(records, PcbLayer.TOP) == tuple(
        p for p in records if p is not pcb.tracks[1])
    assert indexed._render_primitive_collection(ctx, records, PcbLayer.TOP, "red") == \
        baseline._render_primitive_collection(ctx, records, PcbLayer.TOP, "red")


def test_class_method_replacement_bypasses_existing_buckets(monkeypatch):
    pcb, ctx, baseline, indexed = scene()
    indexed._primitive_index.candidates(pcb.tracks, PcbLayer.TOP)
    monkeypatch.setattr(AltiumPcbTrack, "to_svg", lambda self, ctx, **kwargs: ['<path id="replacement"/>'])
    assert indexed._render_primitive_collection(ctx, pcb.tracks, PcbLayer.TOP, "red") == \
        baseline._render_primitive_collection(ctx, pcb.tracks, PcbLayer.TOP, "red")


def test_malformed_skipped_record_does_not_fail_during_eager_indexing():
    pcb, ctx, baseline, indexed = scene()
    bad = AltiumPcbTrack()
    bad.is_keepout = True
    bad.v7_layer_id = []
    records = [bad, *pcb.tracks]
    assert indexed._render_primitive_collection(ctx, records, PcbLayer.TOP, "red") == \
        baseline._render_primitive_collection(ctx, records, PcbLayer.TOP, "red")


def test_empty_shape_region_preserves_legacy_render_result_fallback():
    pcb, ctx, baseline, indexed = scene()
    empty = AltiumPcbShapeBasedRegion()
    empty.layer = PcbLayer.TOP
    region = AltiumPcbRegion()
    region.layer = PcbLayer.TOP
    region.outline_vertices = [RegionVertex(0, 0), RegionVertex(1000000, 0), RegionVertex(0, 1000000)]
    pcb.shapebased_regions, pcb.regions = [empty], [region]
    expected = baseline._render_regions_for_layer(ctx, pcb, PcbLayer.TOP, "red")
    assert expected
    assert indexed._render_regions_for_layer(ctx, pcb, PcbLayer.TOP, "red") == expected


def test_v7_collection_dispatch_matches_native_renderer():
    pcb, ctx, baseline, indexed = scene()
    ref = PcbLayerRef.parse("MECHANICAL17")
    pcb.tracks[0].v7_layer_id = ref.v7_saved_layer_id
    layer = SimpleNamespace(ref=ref)
    expected = baseline._render_v7_ref_primitive_collection(ctx, pcb.tracks, layer, "red")
    assert expected
    assert indexed._render_v7_ref_primitive_collection(ctx, pcb.tracks, layer, "red") == expected


def test_index_is_shared_by_job_and_isolated_between_jobs():
    job = PcbSvgRenderJob()
    first = PcbSvgCompositeRenderer(PcbSvgConfig.default(), render_job=job)
    second = PcbSvgCompositeRenderer(PcbSvgConfig.default(), render_job=job)
    film = SoldermaskFilmRenderer(primitive_index=job.primitive_index)
    assert first._primitive_index is second._primitive_index is film._primitive_index
    assert PcbSvgRenderJob().primitive_index is not job.primitive_index
