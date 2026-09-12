"""Ordered layer candidates for immutable PCB records within one SVG job."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from heapq import merge
from altium_monkey.altium_pcb_layer_ref import PcbLayerRef
from altium_monkey.altium_record_types import PcbLayer

from altium_monkey.altium_record_pcb__arc import AltiumPcbArc
from altium_monkey.altium_record_pcb__fill import AltiumPcbFill
from altium_monkey.altium_record_pcb__region import AltiumPcbRegion
from altium_monkey.altium_record_pcb__shapebased_region import AltiumPcbShapeBasedRegion
from altium_monkey.altium_record_pcb__text import AltiumPcbText
from altium_monkey.altium_record_pcb__track import AltiumPcbTrack
from altium_monkey.altium_record_pcb__svg_support import (
    svg_layer_ref,
    svg_requested_layer_ref,
)


# Only these exact implementations reject other layers before rendering.
# Pads/vias and custom implementations may render on multiple layers.
_METHODS = {
    cls: (cls.to_svg, cls.layer_state, cls.layer_ref)
    for cls in (
        AltiumPcbArc,
        AltiumPcbFill,
        AltiumPcbRegion,
        AltiumPcbShapeBasedRegion,
        AltiumPcbText,
        AltiumPcbTrack,
    )
}


def _native_methods_unchanged() -> bool:
    return all(
        (cls.to_svg, cls.layer_state, cls.layer_ref) == methods
        and not hasattr(methods[0], "__wrapped__")
        and not hasattr(methods[0], "__signature__")
        for cls, methods in _METHODS.items()
    )


type LayerKey = tuple[str, PcbLayerRef | int | None]
type OrderedPrimitive = tuple[int, object]


@dataclass
class _CollectionLayers:
    original: Sequence[object]
    buckets: dict[LayerKey, list[OrderedPrimitive]] = field(default_factory=dict)
    passthrough: list[OrderedPrimitive] = field(default_factory=list)
    selected: dict[LayerKey, tuple[object, ...]] = field(default_factory=dict)

    def candidates(self, target: LayerKey) -> Sequence[object]:
        if not self.buckets:
            return self.original
        if target not in self.selected:
            self.selected[target] = tuple(
                p
                for _, p in merge(
                    self.buckets.get(target, ()),
                    self.passthrough,
                    key=lambda item: item[0],
                )
            )
        return self.selected[target]


class PrimitiveLayerIndex:
    """Reuse layer facts and ordered collection buckets, never rendered output.

    Record objects and collection references are retained to prevent ID reuse.
    Parameters, colors, keepout checks, mask rules and SVG IDs remain the native
    renderer's responsibility. Geometry edits require a new job/index.
    """

    def __init__(self) -> None:
        self._facts: dict[int, tuple[object, tuple[PcbLayerRef | None, int]]] = {}
        self._collections: dict[int, _CollectionLayers] = {}

    def _fact(self, primitive: object) -> tuple[PcbLayerRef | None, int] | None:
        cached = self._facts.get(id(primitive))
        if cached is not None:
            return cached[1]
        if type(primitive) not in _METHODS:
            return None
        fields = getattr(primitive, "__dict__", {})
        if any(name in fields for name in ("to_svg", "layer_state", "layer_ref")):
            return None
        try:
            fact = svg_layer_ref(primitive), int(primitive.layer)
        except ValueError, TypeError, AttributeError, OverflowError:
            # Defer malformed records to the original skip/render path, so an
            # off-layer or keepout record cannot cause a new eager failure.
            return None
        self._facts[id(primitive)] = primitive, fact
        return fact

    def candidates(
        self,
        collection: Sequence[object],
        layer: PcbLayer | PcbLayerRef | int | None,
    ) -> Sequence[object]:
        if (
            layer is None
            or not isinstance(collection, (list, tuple))
            or not _native_methods_unchanged()
        ):
            return collection
        requested = svg_requested_layer_ref(layer)
        # For a non-mappable legacy target Monkey compares raw legacy integers,
        # even when the record also carries a resolved V7 identity.
        target = ("ref", requested) if requested is not None else ("legacy", int(layer))
        key = id(collection)
        entry = self._collections.get(key)
        if entry is None:
            entry = self._index_collection(collection)
            self._collections[key] = entry
        return entry.candidates(target)

    def _index_collection(self, collection: Sequence[object]) -> _CollectionLayers:
        entry = _CollectionLayers(collection)
        for ordinal, primitive in enumerate(collection):
            fact = self._fact(primitive)
            if fact is None:
                entry.passthrough.append((ordinal, primitive))
                continue
            ref, legacy = fact
            entry.buckets.setdefault(("ref", ref), []).append((ordinal, primitive))
            entry.buckets.setdefault(("legacy", legacy), []).append(
                (ordinal, primitive)
            )
        return entry
