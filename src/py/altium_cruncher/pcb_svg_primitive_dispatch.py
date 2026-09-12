"""Reuse ordinary primitive method signatures within one SVG renderer."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from types import FunctionType, MethodType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from altium_monkey.altium_pcb_svg_renderer import (
        PcbSvgRenderContext,
        _PcbSvgRenderLayer,
    )
    from altium_monkey.altium_record_types import PcbLayer

from .pcb_svg_primitive_index import PrimitiveLayerIndex


class PrimitiveDispatchCacheMixin:
    def __init__(
        self,
        *args: object,
        primitive_index: PrimitiveLayerIndex | None = None,
        **kwargs: object,
    ) -> None:
        self._primitive_dispatch = {}
        self._primitive_index = (
            primitive_index if primitive_index is not None else PrimitiveLayerIndex()
        )
        super().__init__(*args, **kwargs)

    def _render_primitive_collection(
        self,
        ctx: PcbSvgRenderContext,
        collection: Sequence[object],
        layer: PcbLayer,
        layer_color: str,
        **kwargs: object,
    ) -> list[str]:
        return super()._render_primitive_collection(
            ctx,
            self._primitive_index.candidates(collection, layer),
            layer,
            layer_color,
            **kwargs,
        )

    def _render_region_collection(
        self,
        ctx: PcbSvgRenderContext,
        collection: Sequence[object],
        layer: PcbLayer,
        layer_color: str,
    ) -> list[str]:
        return super()._render_region_collection(
            ctx, self._primitive_index.candidates(collection, layer), layer, layer_color
        )

    def _render_v7_ref_primitive_collection(
        self,
        ctx: PcbSvgRenderContext,
        collection: Sequence[object],
        layer: _PcbSvgRenderLayer,
        layer_color: str,
    ) -> list[str]:
        return super()._render_v7_ref_primitive_collection(
            ctx,
            self._primitive_index.candidates(collection, layer.ref),
            layer,
            layer_color,
        )

    def _to_svg_accepts_for_layer(self, to_svg: Callable[..., object]) -> bool:
        # Instance data does not change an ordinary bound function's signature.
        # Preserve dynamic inspection for wrappers and custom callable objects.
        if isinstance(to_svg, MethodType) and isinstance(to_svg.__func__, FunctionType):
            function = to_svg.__func__
            if not hasattr(function, "__wrapped__") and not hasattr(
                function, "__signature__"
            ):
                if function not in self._primitive_dispatch:
                    self._primitive_dispatch[function] = (
                        super()._to_svg_accepts_for_layer(to_svg)
                    )
                return self._primitive_dispatch[function]
        return super()._to_svg_accepts_for_layer(to_svg)
