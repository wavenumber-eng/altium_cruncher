"""Bad component models must not prevent a board preview from completing."""

from contextlib import nullcontext
from dataclasses import replace
from types import SimpleNamespace

import geometer as g
import pytest
from altium_monkey.altium_pcb_component import AltiumPcbComponent
from altium_monkey.altium_record_pcb__component_body import AltiumPcbComponentBody

from altium_cruncher.altium_cruncher_pcb_assembly_model_helper import PcbAssemblyModelHelper
from altium_cruncher.altium_cruncher_pcb_illustration import (
    IllustrationComponent, IllustrationJob, IllustrationSymbol,
)
from altium_cruncher.altium_cruncher_pcb_svg_component_layers import ComponentLayerSession


def _failure(operation="geometry.model_tessellation.a0"):
    return g.GeometerOperationError(operation, (SimpleNamespace(
        code="geometer.operation.tessellation_failed",
        message="STEP tessellation did not complete cleanly; partial meshes are not returned.",
    ),))


def _mesh(color=(.5, .5, .5)):
    return g.MeshIllustrationMesh(
        id="body", positions=(0., 0., 0., 1., 0., 0., 0., 1., 1.),
        materials=(g.MeshIllustrationMaterial(color=color),),
    )


def test_failed_and_unsupported_bodies_warn_and_preserve_other_bodies(monkeypatch, caplog):
    entries = [dict(id_norm=name, name_norm=name, name=name, hash=name, step_bytes=name.encode())
               for name in ("bad.step", "good.step")]
    monkeypatch.setattr(PcbAssemblyModelHelper, "_collect_embedded_step_model_catalog",
                        lambda self, pcb: (entries, {}))
    bodies = []
    for index, name in enumerate(("bad.step", "bad.step", "good.step", "part.x_t", "cylinder")):
        body = AltiumPcbComponentBody()
        body.component_index = 0 if index == 2 else index
        body.model_type = 2 if name == "cylinder" else 1
        body.properties = {"BODYPROJECTION": "0", "MODEL.NAME": name}
        bodies.append(body)
    pcb = SimpleNamespace(
        components=[AltiumPcbComponent(f"J{i+1}", "test", "TOP", "0mil", "0mil", rotation="0") for i in range(5)],
        component_bodies=bodies,
    )
    calls = []
    def tessellate(payload, *args, **kwargs):
        calls.append(payload)
        if payload == b"bad.step":
            raise _failure()
        return SimpleNamespace(metadata=SimpleNamespace(warnings=()),
                               mesh_collection=SimpleNamespace(meshes=(_mesh(),)))
    job = IllustrationJob(SimpleNamespace(model_tessellation=tessellate))
    for _ in range(2):
        parts = job.collect_top(pcb)
        assert [part.designator for part in parts] == ["J1"]
        assert [body["index"] for body in parts[0].bodies] == [2]
    assert calls == [b"bad.step", b"good.step"]
    assert len(job.warnings) == 4  # Once per affected body, including repeated instances.
    assert "J1 body 0 (bad.step)" in job.warnings[0]
    assert "partial meshes are not returned" in job.warnings[0]
    assert "J2 body 1 (bad.step)" in job.warnings[1]
    assert "part.x_t" in job.warnings[2] and "unsupported" in job.warnings[2]
    assert "Parasolid text (.x_t)" in job.warnings[2]
    assert "cylinder requires positive finite radius and height" in job.warnings[3]
    assert all(warning in caplog.text for warning in job.warnings)


@pytest.mark.parametrize("error", [
    g.GeometerIpcProcessError("native process stopped"),
    g.GeometerIpcProtocolError("invalid response"),
    g.GeometerIpcTimeoutError("response"),
])
def test_native_service_failures_remain_errors(error):
    def tessellate(*args, **kwargs):
        raise error
    job = IllustrationJob(SimpleNamespace(model_tessellation=tessellate))
    with pytest.raises(type(error)):
        job._tessellate("model", b"STEP")
    assert not job._tessellation_failures


def test_partial_meshes_are_cached_and_warnings_identify_the_model(caplog):
    mesh = _mesh()
    calls = []
    def tessellate(*args, **kwargs):
        calls.append(args)
        return SimpleNamespace(
            metadata=SimpleNamespace(warnings=("Partial STEP tessellation: omitted 1 face.",)),
            mesh_collection=SimpleNamespace(meshes=(mesh,)),
        )
    job = IllustrationJob(SimpleNamespace(model_tessellation=tessellate))
    first = job._tessellate("connector", b"STEP", context="J2 (connector.step)")
    assert first == (mesh,)
    assert job._tessellate("connector", b"STEP", context="J3 (connector.step)") is first
    assert len(calls) == 1
    assert job.warnings == [
        f"{ref} (connector.step): Partial STEP tessellation: omitted 1 face."
        for ref in ("J2", "J3")
    ]
    assert all(warning in caplog.text for warning in job.warnings)


def test_component_render_failure_is_cached_and_other_components_render(monkeypatch, caplog):
    bad = IllustrationComponent("J1", (0, 0), (_mesh(),), ({"index": 0},))
    repeated = replace(bad, designator="J2", anchor_mm=(10, 10))
    good = replace(bad, designator="U1", meshes=(_mesh((1., 0., 0.)),))
    calls = []
    symbol = IllustrationSymbol("<svg/>", 0, 0, 1, {}, ())
    def render_native(self, part, **kwargs):
        calls.append(part.designator)
        if part.designator.startswith("J"):
            raise _failure("geometry.mesh_illustration.a0")
        return symbol
    monkeypatch.setattr(IllustrationJob, "_render_native", render_native)
    monkeypatch.setattr(IllustrationJob, "collect", lambda *args, **kwargs: [bad, repeated, good])
    monkeypatch.setattr(g, "GeometerClient", lambda: nullcontext(SimpleNamespace()))
    session = ComponentLayerSession()
    pcb = SimpleNamespace(components=[], component_bodies=[])
    for _ in range(2):
        assert session._materialize(pcb, "top", .025, True) == [(good, symbol)]
    assert calls == ["J1", "U1"]
    assert len(session.job.warnings) == 2
    assert "J1 (top)" in caplog.text and "J2 (top)" in caplog.text
