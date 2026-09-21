"""Schedule mounting-side projections before opposite-side visibility tests."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, cast

import geometer as g

from .pcb_direct_projection_memo import DirectProjectionMemo, direct_source_key
from .pcb_illustration_model_geometry import ModelGeometryError, digest
from .pcb_model_rotation import resolve_model_z_rotation

if TYPE_CHECKING:
    from .altium_cruncher_pcb_illustration import (
        ComponentPlacement,
        IllustrationComponent,
        IllustrationJob,
        Side,
    )
    from .pcb_svg_workers import PcbSvgNativeWorkers


def prewarm_opposite_direct(
    job: IllustrationJob,
    components: Sequence[ComponentPlacement],
    side: Side,
    illustrate: bool,
    workers: PcbSvgNativeWorkers | None,
) -> None:
    candidates = _prewarm_candidates(job, components, side, illustrate)
    if not candidates:
        return
    authored_side: Side = "bottom" if side == "top" else "top"
    if workers is None or workers.count == 1:
        for component in candidates:
            try:
                prewarm_direct_bounds(job, component, authored_side, illustrate)
            except (g.GeometerOperationError, ModelGeometryError):
                # Speculative bounds work follows the normal per-component
                # failure path later; it must not make a recoverable model
                # failure fatal to the whole render.
                continue
        return
    futures = [
        workers.submit(
            _prewarm_direct_with_client,
            component,
            job.line_width_mm,
            authored_side,
            illustrate,
            job._direct_projection_memo,
        )
        for component in candidates
    ]
    for future in futures:
        try:
            future.result()
        except (g.GeometerOperationError, ModelGeometryError):
            continue


def _prewarm_candidates(
    job: IllustrationJob,
    components: Sequence[ComponentPlacement],
    side: Side,
    illustrate: bool,
) -> tuple[IllustrationComponent, ...]:
    candidates: dict[str, IllustrationComponent] = {}
    for component in components:
        direct = getattr(component, "direct", None)
        if direct is None or getattr(component, "authored_side", side) == side:
            continue
        if job._prime_cached_symbol(component, side, illustrate):
            continue
        identity = digest(
            {
                "current": direct_source_key(direct.source, direct.model),
                "alternative": (
                    None
                    if direct.footprint_local_source is None
                    else direct_source_key(direct.footprint_local_source, direct.model)
                ),
                "target": direct.authored_outline_bounds_mm,
            }
        )
        candidates.setdefault(identity, cast("IllustrationComponent", component))
    return tuple(candidates.values())


def prewarm_direct_bounds(
    job: IllustrationJob,
    component: IllustrationComponent,
    side: Side,
    illustrate: bool,
) -> None:
    direct = component.direct
    if direct is None:
        return
    current = job._render_direct_source_cached(
        (direct.identity, "instance_space"),
        direct.source,
        direct.model,
        side,
        illustrate,
    )
    alternative = direct.footprint_local_source
    target = direct.authored_outline_bounds_mm
    if alternative is None or target is None or current.source_bounds_mm is None:
        return
    resolution = resolve_model_z_rotation(
        target, current.source_bounds_mm, current.source_bounds_mm
    )
    if resolution.choice != "instance_space":
        job._render_direct_source_cached(
            (direct.identity, "footprint_local"),
            alternative,
            direct.model,
            side,
            illustrate,
        )


def _prewarm_direct_with_client(
    client: g.GeometerClient,
    component: IllustrationComponent,
    line_width: float,
    side: Side,
    illustrate: bool,
    direct_projection_memo: DirectProjectionMemo,
) -> None:
    from .altium_cruncher_pcb_illustration import IllustrationJob

    job = IllustrationJob(
        client,
        line_width_mm=line_width,
        direct_projection_memo=direct_projection_memo,
    )
    prewarm_direct_bounds(job, component, side, illustrate)
