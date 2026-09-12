"""Positive component artwork reuse before tessellation or mesh placement.

The side key covers exact authored recipes and diagnostic identities. Successful
placements share symbols, but retain per-body warning events and instance data.
Omitted/failed bodies are never represented as reusable negative results.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc
    from altium_monkey.altium_pcb_component import AltiumPcbComponent
    from altium_monkey.altium_record_pcb__component_body import AltiumPcbComponentBody
import logging
import math

from .altium_cruncher_pcb_assembly_model_helper import PcbAssemblyModelHelper
from .altium_cruncher_pcb_illustration import (
    CachedComponentPlacement,
    ComponentPlacement,
    IllustrationSymbol,
    IllustrationJob,
    BodyMetadata,
    WarningEvents,
    CachedBodies,
    PlacedIllustrations,
    Side,
    RenderKeys,
    model_catalog_context,
    _finite_vector,
    ModelGeometryError,
    _body_anchor,
    _body_opacity,
    _colorref,
    _decode_cached_symbol,
    _digest,
    _extrusion_request,
    _owning_component,
    _step_matrix,
)

log = logging.getLogger(__name__)


def _hash_key(value: object) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(c not in "0123456789abcdef" for c in value)
    ):
        raise ValueError("invalid cached appearance key")
    return value


type ArtworkEntry = tuple[
    CachedComponentPlacement, RenderKeys, dict[int, WarningEvents]
]
type Artwork = tuple[dict[str, IllustrationSymbol], list[ArtworkEntry]]


def _decode_placement(value: dict) -> CachedComponentPlacement:
    part = CachedComponentPlacement(
        value["designator"],
        _finite_vector(value["anchor_mm"], 2),
        tuple(value["bodies"]),
        value["component_index"],
        _finite_vector(value["bounds"], 6),
    )
    if (
        not isinstance(part.designator, str)
        or not part.bodies
        or (
            part.component_index is not None
            and (type(part.component_index) is not int or part.component_index < 0)
        )
        or any(part.bounds[i] > part.bounds[i + 3] for i in range(3))
    ):
        raise ValueError("invalid cached component placement")
    return part


def _validate_body(body: BodyMetadata, seen: set[int]) -> int:
    index = body["index"]
    if type(index) is not int or index < 0 or index in seen:
        raise ValueError("invalid cached body identity")
    if body["kind"] not in {"step", "extruded"}:
        raise ValueError("invalid cached body kind")
    lower, upper, opacity = _finite_vector(
        (body["lower_z_mm"], body["upper_z_mm"], body["opacity"]), 3
    )
    if lower > upper or not 0 < opacity <= 1:
        raise ValueError("invalid cached body extents or opacity")
    if body["color"] is not None:
        if any(not 0 <= channel <= 1 for channel in _finite_vector(body["color"], 3)):
            raise ValueError("invalid cached body color")
    if body["color"] is not None:
        body["color"] = tuple(body["color"])
    seen.add(index)
    return index


def _decode_warning_events(value: list) -> WarningEvents:
    if any(
        not isinstance(event, (list, tuple))
        or len(event) != 2
        or type(event[0]) is not bool
        or not isinstance(event[1], str)
        for event in value
    ):
        raise ValueError("invalid cached warning events")
    return [(deduplicate, message) for deduplicate, message in value]


def _decode_artwork(payload: object) -> Artwork:
    data = cast(dict, payload)
    symbols = {
        _hash_key(key): _decode_cached_symbol(value, allow_warnings=True)
        for key, value in data["symbols"].items()
    }
    entries = []
    seen: set[int] = set()
    for entry in data["entries"]:
        part = _decode_placement(entry["placement"])
        keys = tuple(_hash_key(k) for k in entry["keys"])
        if len(keys) != 2 or keys[0] not in symbols:
            raise ValueError("missing cached component symbol")
        events = {}
        for body in part.bodies:
            index = _validate_body(body, seen)
            events[index] = _decode_warning_events(entry["body_warnings"][str(index)])
        entries.append((part, keys, events))
    return symbols, entries


class ComponentArtworkCache:
    def __init__(
        self,
        job: IllustrationJob,
        pcbdoc: AltiumPcbDoc,
        side: Side,
        illustrate: bool,
        excluded: frozenset[str],
    ) -> None:
        self.job, self.side, self.illustrate = job, side, illustrate
        self.catalog_context = model_catalog_context(pcbdoc)
        helper, by_id, by_name = self.catalog_context
        self.recipes = {}
        unusable = set()
        signature = []
        for index, body in enumerate(pcbdoc.component_bodies):
            component = _owning_component(pcbdoc, body)
            owner = body.component_index if component is not None else -index - 1
            if component is not None and component.designator in excluded:
                continue
            try:
                recipe = self._body_recipe(body, index, component, owner)
                if recipe is None:
                    continue
                signature.append(_digest(recipe))
                self.recipes.setdefault(owner, []).append(recipe)
            except ModelGeometryError, ValueError, TypeError, AttributeError:
                # The original collector still validates/reports this body.
                # Never reuse a component with an unrepresented authored body.
                unusable.add(owner)
                signature.append(dict(uncacheable_body=index, owner=owner))
        for owner in unusable:
            self.recipes.pop(owner, None)
        self.key = _digest(
            dict(
                recipes=signature,
                side=side,
                illustrate=illustrate,
                line_width_mm=job.line_width_mm,
            )
        )
        self.hit_owners = set()

    def _body_recipe(
        self,
        body: AltiumPcbComponentBody,
        index: int,
        component: AltiumPcbComponent | None,
        owner: int,
    ) -> dict | None:
        helper, by_id, by_name = self.catalog_context
        side = self.side
        if helper._component_body_is_bottom(body.properties, component) != (
            side == "bottom"
        ):
            return None
        opacity = _body_opacity(body)
        if opacity == 0:
            return None
        anchor = _body_anchor(helper, body, component)
        if anchor is None:
            raise ModelGeometryError("missing anchor")
        designator = (
            str(component.designator) if component is not None else f"free-body-{index}"
        )
        color = _colorref(body.body_color_3d)
        anchor_mm = tuple(v * 0.0254 for v in anchor)
        if body.model_type == 0:
            source = _extrusion_request(body, anchor_mm, is_bottom=side == "bottom")
        elif body.model_type == 1:
            entry = helper._resolve_component_body_model_entry(
                body.properties, models_by_id=by_id, models_by_name=by_name
            )
            if entry is None:
                raise ModelGeometryError("unavailable STEP")
            source = dict(
                model=entry["hash"],
                name=entry["name"],
                matrix=_step_matrix(
                    helper, body, component, anchor, is_bottom=side == "bottom"
                ),
            )
            color = color if body.body_override_color else None
        else:
            raise ModelGeometryError("unsupported body")
        recipe = dict(
            index=index,
            owner=owner,
            designator=designator,
            anchor_mm=anchor_mm,
            kind=body.model_type,
            source=source,
            color=color,
            opacity=opacity,
        )
        return recipe

    @staticmethod
    def _owner(part: ComponentPlacement) -> int:
        return (
            part.component_index
            if part.component_index is not None
            else -part.bodies[0]["index"] - 1
        )

    @staticmethod
    def _matches_recipe(
        part: CachedComponentPlacement, recipes: list[dict] | None
    ) -> bool:
        return bool(
            recipes
            and [b["index"] for b in part.bodies] == [r["index"] for r in recipes]
            and part.designator == recipes[0]["designator"]
            and part.anchor_mm == recipes[0]["anchor_mm"]
        )

    def load(self) -> CachedBodies:
        artifact = self.job.cache.load("component-artwork", self.key, _decode_artwork)
        cached_bodies = {}
        if artifact is None:
            return cached_bodies
        symbols, entries = artifact
        unsafe = set()
        for part, keys, events in entries:
            owner = self._owner(part)
            recipes = self.recipes.get(owner)
            if not self._matches_recipe(part, recipes):
                if symbols[keys[0]].warnings:
                    unsafe.add(keys[0])
                continue
            if keys[0] in unsafe:
                continue
            self.hit_owners.add(owner)
            self.job._early_components[id(part)] = (
                part,
                keys,
                symbols[keys[0]],
                self.side,
                self.job.line_width_mm,
                self.illustrate,
            )
            for ordinal, body in enumerate(part.bodies):
                index = body["index"]
                cached_bodies[index] = (part if ordinal == 0 else None, events[index])
        log.info(
            "Reusing illustrations for %d %s components",
            len(self.hit_owners),
            self.side,
        )
        return cached_bodies

    @staticmethod
    def _complete_bodies(part: ComponentPlacement, recipes: list[dict] | None) -> bool:
        return bool(
            recipes
            and [b["index"] for b in part.bodies] == [r["index"] for r in recipes]
        )

    def store(self, placed: PlacedIllustrations) -> None:
        entries, symbols = [], {}
        seen, unsafe = set(), set()
        changed = False
        for part, symbol in placed:
            owner = self._owner(part)
            recipes = self.recipes.get(owner)
            # All eligible bodies must have succeeded. Partial *tessellation*
            # warnings are fine; an entirely omitted body must retry next time.
            keys = self.job._render_keys(part, self.side, self.illustrate)
            complete = self._complete_bodies(part, recipes)
            if keys[0] not in seen and not complete and symbol.warnings:
                # Do not persist a consumer's borrowed diagnostics when their
                # original producer is incomplete and must retry next run.
                unsafe.add(keys[0])
            seen.add(keys[0])
            if not complete or keys[0] in unsafe:
                continue
            changed |= owner not in self.hit_owners
            if keys[0] not in symbols:
                symbols[keys[0]] = asdict(symbol)
            entries.append(self._encode_entry(part, keys))
        if entries and changed:
            self.job.cache.store(
                "component-artwork", self.key, dict(entries=entries, symbols=symbols)
            )

    def _encode_entry(self, part: ComponentPlacement, keys: RenderKeys) -> dict:
        placement = dict(
            designator=part.designator,
            anchor_mm=part.anchor_mm,
            bodies=part.bodies,
            component_index=part.component_index,
            bounds=part.bounds,
        )
        return dict(
            placement=placement,
            keys=keys,
            body_warnings={
                str(body["index"]): self.job._body_warning_events[body["index"]]
                for body in part.bodies
            },
        )
