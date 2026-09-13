"""Parallel misses must preserve deduplication, warnings, order and cleanup."""

from concurrent.futures import CancelledError
from dataclasses import replace
import threading
from types import SimpleNamespace

import geometer as g
import pytest

from altium_cruncher.altium_cruncher_pcb_illustration import (
    IllustrationComponent,
    IllustrationJob,
    IllustrationSymbol,
    ModelGeometryError,
)
from altium_cruncher import altium_cruncher_pcb_illustration as illustration
from altium_cruncher.pcb_svg_model_cache import PcbSvgModelCache
from altium_cruncher.pcb_svg_workers import PcbSvgNativeWorkers


class Client:
    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True


def part(name, color):
    mesh = g.MeshIllustrationMesh(
        id=name,
        positions=(0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0),
        materials=(g.MeshIllustrationMaterial(color=color),),
    )
    return IllustrationComponent(name, (0.0, 0.0), (mesh,), ())


def symbol(part):
    return IllustrationSymbol(
        '<svg xmlns="http://www.w3.org/2000/svg"/>',
        0.0,
        0.0,
        1.0,
        {},
        (f"Diagnostic: {part.designator}",),
    )


def test_unique_work_overlaps_but_composition_and_warnings_stay_ordered(monkeypatch):
    barrier = threading.Barrier(2)
    clients, calls = [], []

    def factory():
        client = Client()
        clients.append(client)
        return client

    def native(self, component, **kwargs):
        calls.append((component.designator, id(self.client)))
        barrier.wait(timeout=5)
        return symbol(component)

    monkeypatch.setattr(IllustrationJob, "_render_native", native)
    first = part("U1", (1.0, 0.0, 0.0))
    repeated = replace(first, designator="U2", anchor_mm=(10.0, 10.0))
    second = part("U3", (0.0, 1.0, 0.0))
    with PcbSvgNativeWorkers(2, client_factory=factory) as workers:
        job = IllustrationJob(None)
        placed = job.render_many(
            [first, repeated, second], side="top", illustrate=True, workers=workers
        )
        assert [p.designator for p, _ in placed] == ["U1", "U2", "U3"]
        assert job.counts["illustrations"] == 2 and job.counts["illustration_hits"] == 1
        assert job.warnings == ["Diagnostic: U1", "Diagnostic: U3"]
    assert len(calls) == len(clients) == 2
    assert len({client for _, client in calls}) == 2
    assert all(client.closed for client in clients)


def test_warm_disk_cache_starts_no_workers(tmp_path, monkeypatch):
    def native(self, component, **kwargs):
        return symbol(component)

    monkeypatch.setattr(IllustrationJob, "_render_native", native)
    source = part("U1", (1.0, 0.0, 0.0))

    def cache():
        return PcbSvgModelCache(tmp_path, identity="a" * 64)

    cold = IllustrationJob(None, cache=cache()).render(source)

    def forbidden():
        pytest.fail("A fully cached render must not start native workers")

    with PcbSvgNativeWorkers(4, client_factory=forbidden) as workers:
        job = IllustrationJob(None, cache=cache())
        assert job.render_many(
            [source], side="top", illustrate=True, workers=workers
        ) == [(source, cold)]
        assert job.counts["illustration_disk_hits"] == 1
        assert job.warnings == ["Diagnostic: U1"]


def test_parallel_model_failures_preserve_other_parts_and_warn_for_repeats(monkeypatch):
    calls = []

    def native(self, component, **kwargs):
        calls.append(component.designator)
        if component.designator == "bad":
            raise g.GeometerOperationError("illustration", ())
        return symbol(component)

    monkeypatch.setattr(IllustrationJob, "_render_native", native)
    bad, good = part("bad", (1.0, 0.0, 0.0)), part("good", (0.0, 1.0, 0.0))
    with PcbSvgNativeWorkers(2, client_factory=Client) as workers:
        job = IllustrationJob(None)
        result = job.render_many(
            [bad, replace(bad, designator="repeated"), good],
            side="bottom",
            illustrate=True,
            workers=workers,
        )
    assert [p.designator for p, _ in result] == ["good"]
    assert sorted(calls) == ["bad", "good"]
    assert len(job.warnings) == 3
    assert "bad (bottom)" in job.warnings[0]
    assert "repeated (bottom)" in job.warnings[1]


def test_cancel_queued_work_and_close_every_started_client():
    entered, release = threading.Event(), threading.Event()
    clients = []

    def factory():
        client = Client()
        clients.append(client)
        return client

    def running(client):
        entered.set()
        assert release.wait(timeout=5)

    workers = PcbSvgNativeWorkers(1, client_factory=factory)
    first = workers.submit(running)
    assert entered.wait(timeout=5)
    second = workers.submit(lambda client: pytest.fail("Queued work was not cancelled"))
    closer = threading.Thread(target=workers.close)
    closer.start()
    # shutdown cancels queued futures before waiting for running requests.
    with pytest.raises(CancelledError):
        second.result(timeout=5)
    release.set()
    closer.join(timeout=5)
    assert not closer.is_alive()
    assert first.result(timeout=1) is None
    assert clients and all(c.closed for c in clients)
    workers.close()  # Idempotent cleanup.


@pytest.mark.parametrize("value", [0, -1, True, 1.5])
def test_worker_count_must_be_a_positive_integer(value):
    with pytest.raises(ValueError):
        PcbSvgNativeWorkers(value)


def test_interrupted_shutdown_still_closes_clients_and_allows_cleanup_retry():
    class InterruptedExecutor:
        def shutdown(self, **kwargs):
            raise KeyboardInterrupt()
    workers = PcbSvgNativeWorkers(2)
    client = Client()
    workers._clients.append(client)
    workers._executor = InterruptedExecutor()
    with pytest.raises(KeyboardInterrupt):
        workers.close()
    assert client.closed
    with pytest.raises(RuntimeError):
        workers.submit(lambda client: None)
    workers._executor = None
    workers.close()
    assert workers._closed


@pytest.mark.parametrize("failed_second", [False, True])
def test_step_prefetch_commits_in_body_order_and_reuses_positive_disk_results(
    tmp_path, monkeypatch, failed_second, caplog,
):
    caplog.set_level("INFO")
    barrier = threading.Barrier(2)
    second_finished = threading.Event()
    completed = []

    class TessellationClient(Client):
        def model_tessellation(self, step, options, **kwargs):
            barrier.wait(timeout=5)
            if step == b"a":
                assert second_finished.wait(timeout=5)
            completed.append(step)
            if step == b"b":
                second_finished.set()
                if failed_second:
                    raise g.GeometerError(1, "bad STEP", "model_tessellation")
            return SimpleNamespace(
                metadata=SimpleNamespace(warnings=(f"partial {step.decode()}",)),
                mesh_collection=SimpleNamespace(meshes=part("face", (1., 0., 0.)).meshes),
            )

    monkeypatch.setattr(illustration, "_body_anchor", lambda *args: (0, 0))
    bodies = [SimpleNamespace(model_type=1, component_index=i,
              properties={"model": key}, body_opacity_3d=1)
              for i, key in enumerate(("a", "b", "a"))]
    pcb = SimpleNamespace(component_bodies=bodies,
        components=[SimpleNamespace(designator=f"U{i + 1}") for i in range(3)])
    helper = SimpleNamespace(
        _component_body_is_bottom=lambda *args: False,
        _resolve_component_body_model_entry=lambda props, **kwargs:
            dict(hash=props["model"], name=props["model"] + ".step", step_bytes=props["model"].encode()),
    )

    def cache():
        return PcbSvgModelCache(tmp_path, identity="a" * 64)

    with PcbSvgNativeWorkers(2, client_factory=TessellationClient) as workers:
        job = IllustrationJob(None, cache=cache())
        job._prefetch_steps(pcb, helper, {}, {}, "top", frozenset(), workers)
        assert "Preparing top STEP models: 2 unique models" in caplog.text
        assert "a.step (U1)" in caplog.text and "b.step (U2)" in caplog.text
        assert ("Failed top STEP model" in caplog.text) == failed_second
        assert completed == [b"b", b"a"]
        assert job.counts["tessellations"] == 0 and job.warnings == []
        first = job._tessellate("a", b"a", context="U1")
        if failed_second:
            for context in ("U2", "repeat"):
                with pytest.raises(ModelGeometryError, match="bad STEP"):
                    job._tessellate("b", b"b", context=context)
        else:
            job._tessellate("b", b"b", context="U2")
        assert job._tessellate("a", b"a", context="U3") is first
        assert job.warnings == (["U1: partial a", "U3: partial a"] if failed_second
                                else ["U1: partial a", "U2: partial b", "U3: partial a"])
        assert job.counts["tessellations"] == (1 if failed_second else 2)
        assert job.counts["tessellation_hits"] == 1
        assert len(completed) == 2
    if failed_second:
        assert len(list(tmp_path.rglob("*.json.gz"))) == 1
        return

    def forbidden():
        pytest.fail("Warm STEP prefetch must not start native workers")

    with PcbSvgNativeWorkers(4, client_factory=forbidden) as workers:
        warm = IllustrationJob(None, cache=cache())
        warm._prefetch_steps(pcb, helper, {}, {}, "top", frozenset(), workers)
        for name, context in (("a", "U1"), ("b", "U2"), ("a", "U3")):
            assert warm._tessellate(name, name.encode(), context=context) == first
        assert warm.warnings == job.warnings
        assert warm.counts["tessellation_disk_hits"] == 2
        assert warm.counts["tessellation_hits"] == 1


@pytest.mark.parametrize("side", ["top", "bottom"])
def test_component_hlr_always_requests_fast_detail_and_fast_mesh_shadow(side):
    requests = []

    def hlr(mesh, options, **kwargs):
        requests.append(options)
        return SimpleNamespace(views=[SimpleNamespace(id=side,
            modes=SimpleNamespace(outline=SimpleNamespace(segments=())))])

    job = IllustrationJob(SimpleNamespace(mesh_hlr_projection=hlr))
    job._render_native(part("U1", (1., 0., 0.)), side=side, illustrate=False)
    options = requests[0]
    assert options.projection_algorithm == g.HlrProjectionAlgorithm.FAST
    assert options.outline_algorithm == g.HlrOutlineAlgorithm.FAST_MESH_SHADOW
    assert options.output_detail and options.output_outline
