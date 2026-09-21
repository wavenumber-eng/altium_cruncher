"""Runtime reuse decisions for direct-model illustration projections."""

from __future__ import annotations

from dataclasses import asdict
from typing import TYPE_CHECKING

import geometer as g

from .pcb_component_clipping import (
    ComponentVisibilityAction,
    ComponentVisibilityResolution,
)
from .pcb_direct_projection_memo import direct_source_key
from .pcb_illustration_model_geometry import (
    IllustrationSymbol,
    ModelGeometryError,
    digest,
    empty_illustration_symbol,
)
from .pcb_model_rotation import RotationResolution, resolve_model_z_rotation

if TYPE_CHECKING:
    from .altium_cruncher_pcb_illustration import (
        DirectIllustrationSource,
        IllustrationComponent,
        IllustrationJob,
        Side,
    )


def render_direct(
    job: IllustrationJob,
    component: IllustrationComponent,
    side: Side,
    illustrate: bool,
) -> IllustrationSymbol:
    direct = component.direct
    if direct is None:
        raise ModelGeometryError("direct illustration source is unavailable")
    current_identity = (direct.identity, "instance_space")
    known_current = job._direct_projection_memo.opposite_uncut(
        direct_source_key(direct.source, direct.model), side
    )
    if known_current is not None:
        known = render_from_opposite_fact(
            job,
            component,
            direct,
            current_identity,
            direct.source,
            known_current,
            side,
            illustrate,
        )
        if known is not None:
            return known
    return _render_fresh_direct(
        job, component, direct, current_identity, side, illustrate
    )


def _render_fresh_direct(
    job: IllustrationJob,
    component: IllustrationComponent,
    direct: DirectIllustrationSource,
    current_identity: object,
    side: Side,
    illustrate: bool,
) -> IllustrationSymbol:
    current = job._render_direct_source_cached(
        current_identity, direct.source, direct.model, side, illustrate
    )
    alternative_source = direct.footprint_local_source
    target = direct.authored_outline_bounds_mm
    if alternative_source is None:
        return _apply_current(job, component, direct, current_identity, current, side, illustrate)
    body_index = component.bodies[0]["index"] if len(component.bodies) == 1 else None
    if target is None or current.source_bounds_mm is None:
        job.warn(
            f"{component.designator}: authored outline cannot resolve model Z rotation; retaining current placement",
            code="rotation-outline-unavailable",
            category="rotation_resolution",
            component_designator=component.designator,
            body_index=body_index,
            model_identity=direct.label,
        )
        return _apply_current(job, component, direct, current_identity, current, side, illustrate)
    current_check = resolve_model_z_rotation(
        target, current.source_bounds_mm, current.source_bounds_mm
    )
    if current_check.choice == "instance_space":
        return _apply_current(job, component, direct, current_identity, current, side, illustrate)
    return _render_rotation_alternative(
        job,
        component,
        direct,
        current_identity,
        current,
        alternative_source,
        target,
        body_index,
        side,
        illustrate,
    )


def _render_rotation_alternative(
    job: IllustrationJob,
    component: IllustrationComponent,
    direct: DirectIllustrationSource,
    current_identity: object,
    current: IllustrationSymbol,
    alternative_source: g.ModelIllustrationSourceA0,
    target: tuple[float, float, float, float],
    body_index: int | None,
    side: Side,
    illustrate: bool,
) -> IllustrationSymbol:
    assert current.source_bounds_mm is not None
    alternative_identity = (direct.identity, "footprint_local")
    alternative = job._render_direct_source_cached(
        alternative_identity, alternative_source, direct.model, side, illustrate
    )
    if alternative.source_bounds_mm is None:
        job._queue_discarded_symbol_warnings(component, alternative, side, direct)
        job.warn(
            f"{component.designator}: alternative model Z rotation returned no native bounds; retaining current placement",
            code="rotation-bounds-unavailable",
            category="rotation_resolution",
            producer="geometer",
            component_designator=component.designator,
            body_index=body_index,
            model_identity=direct.label,
        )
        return _apply_current(job, component, direct, current_identity, current, side, illustrate)
    resolution = resolve_model_z_rotation(
        target, current.source_bounds_mm, alternative.source_bounds_mm
    )
    if resolution.choice == "footprint_local":
        job._queue_discarded_symbol_warnings(component, current, side, direct)
        return job._apply_direct_visibility(
            component,
            alternative_source,
            alternative,
            side,
            illustrate,
            projection_identity=alternative_identity,
        )
    job._queue_discarded_symbol_warnings(component, alternative, side, direct)
    if resolution.choice == "unresolved":
        _warn_unresolved_rotation(job, component, direct, body_index, resolution)
    return _apply_current(job, component, direct, current_identity, current, side, illustrate)


def _apply_current(
    job: IllustrationJob,
    component: IllustrationComponent,
    direct: DirectIllustrationSource,
    identity: object,
    current: IllustrationSymbol,
    side: Side,
    illustrate: bool,
) -> IllustrationSymbol:
    return job._apply_direct_visibility(
        component,
        direct.source,
        current,
        side,
        illustrate,
        projection_identity=identity,
    )


def _warn_unresolved_rotation(
    job: IllustrationJob,
    component: IllustrationComponent,
    direct: DirectIllustrationSource,
    body_index: int | None,
    resolution: RotationResolution,
) -> None:
    job.warn(
        f"{component.designator}: neither supported model Z-rotation interpretation matches the authored outline; retaining current placement",
        code="rotation-unresolved",
        category="rotation_resolution",
        component_designator=component.designator,
        body_index=body_index,
        model_identity=direct.label,
        detail={
            "reason": resolution.reason,
            "instance_space_score": resolution.current_score,
            "footprint_local_score": resolution.footprint_local_score,
        },
    )


def render_from_opposite_fact(
    job: IllustrationJob,
    component: IllustrationComponent,
    direct: DirectIllustrationSource,
    current_identity: object,
    current_source: g.ModelIllustrationSourceA0,
    known_current: IllustrationSymbol,
    side: Side,
    illustrate: bool,
) -> IllustrationSymbol | None:
    """Skip a cross-side projection only when prior bounds prove it invisible."""

    selected = _selected_opposite_fact(
        job, direct, current_identity, current_source, known_current, side
    )
    if selected is None:
        return None
    selected_source, selected_identity, selected_symbol = selected
    resolution = job._component_visibility(
        component, selected_symbol.source_bounds_mm, side
    )
    if _is_hidden_interior(job, component, selected_symbol, resolution):
        assert resolution is not None
        job._warn_unsafe_opposite_visibility(component, resolution)
        return empty_illustration_symbol()
    uncut = job._render_direct_source_cached(
        selected_identity,
        selected_source,
        direct.model,
        side,
        illustrate,
    )
    return job._apply_direct_visibility(
        component,
        selected_source,
        uncut,
        side,
        illustrate,
        projection_identity=selected_identity,
    )


def _selected_opposite_fact(
    job: IllustrationJob,
    direct: DirectIllustrationSource,
    current_identity: object,
    current_source: g.ModelIllustrationSourceA0,
    known_current: IllustrationSymbol,
    side: Side,
) -> tuple[g.ModelIllustrationSourceA0, object, IllustrationSymbol] | None:
    alternative_source = direct.footprint_local_source
    target = direct.authored_outline_bounds_mm
    if alternative_source is None or target is None:
        return current_source, current_identity, known_current
    if known_current.source_bounds_mm is None:
        return None
    current_check = resolve_model_z_rotation(
        target, known_current.source_bounds_mm, known_current.source_bounds_mm
    )
    if current_check.choice == "instance_space":
        return current_source, current_identity, known_current
    alternative = job._direct_projection_memo.opposite_uncut(
        direct_source_key(alternative_source, direct.model), side
    )
    if alternative is None or alternative.source_bounds_mm is None:
        return None
    resolution = resolve_model_z_rotation(
        target, known_current.source_bounds_mm, alternative.source_bounds_mm
    )
    if resolution.choice == "footprint_local":
        return alternative_source, (direct.identity, "footprint_local"), alternative
    return current_source, current_identity, known_current


def _is_hidden_interior(
    job: IllustrationJob,
    component: IllustrationComponent,
    symbol: IllustrationSymbol,
    resolution: ComponentVisibilityResolution | None,
) -> bool:
    return bool(
        resolution is not None
        and resolution.action is ComponentVisibilityAction.OMIT
        and not job._may_intersect_open_space(component, symbol.source_bounds_mm)
    )


def render_source_cached(
    job: IllustrationJob,
    source: g.ModelIllustrationSourceA0,
    model: bytes | None,
    side: Side,
    illustrate: bool,
    *,
    clipping: g.IllustrationClipping | None,
) -> IllustrationSymbol:
    source_key = direct_source_key(source, model)
    key = digest(
        {
            "renderer_contract": "geometer-b0-direct-projection-singleflight-v1",
            "source_key": source_key,
            "line_width_mm": job.line_width_mm,
            "side": side,
            "illustrate": illustrate,
            "clipping": None if clipping is None else asdict(clipping),
        }
    )

    def render() -> IllustrationSymbol:
        return job._render_direct_source(
            source,
            model,
            side,
            illustrate,
            **({} if clipping is None else {"clipping": clipping}),
        )

    result = job._direct_projection_memo.get(key, render)
    if clipping is None:
        job._direct_projection_memo.remember_uncut(source_key, side, result)
    return result
