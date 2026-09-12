"""Command-scoped SVG reuse and wall timings for immutable PCB snapshots.

Only register parameter-only variant copies as aliases. Geometry edits require
a new snapshot/job. Cached fragments are immutable strings, never live XML nodes.
"""

from __future__ import annotations

import argparse
from collections.abc import Iterable, Iterator, Mapping
from contextlib import contextmanager
from copy import copy
from dataclasses import dataclass
import json
import logging
from pathlib import Path
import time
from types import TracebackType
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc
    from altium_monkey.altium_resolved_layer_stack import ResolvedLayerStack
    from altium_monkey.altium_pcb_svg_renderer import PcbSvgRenderContext

from .altium_cruncher_pcb_svg_component_layers import ComponentLayerSession
from .altium_cruncher_pcb_svg_cutout_layer import _pcbdoc_with_cutout_scope
from .pcb_svg_model_cache import PcbSvgModelCache
from .pcb_svg_primitive_index import PrimitiveLayerIndex
from .pcb_svg_workers import DEFAULT_WORKERS, PcbSvgNativeWorkers

log = logging.getLogger(__name__)


@dataclass
class _TimingFrame:
    row: dict[str, object]
    context: dict[str, object]
    children_seconds: float = 0.0


class PcbSvgRenderJob:
    """Own snapshot aliases, reusable render state, native clients and timings."""

    def __init__(
        self, *, model_cache: PcbSvgModelCache | None = None, workers: int = 1
    ) -> None:
        self.model_cache = model_cache
        self.primitive_index = PrimitiveLayerIndex()
        self.native_workers = PcbSvgNativeWorkers(workers)
        self.events: list[dict[str, object]] = []
        self._frames: list[_TimingFrame] = []
        self._records: dict[int, object] = {}
        self._sources: dict[int, AltiumPcbDoc] = {}
        self._geometry_sources: dict[int, AltiumPcbDoc] = {}
        self._scoped: dict[tuple[int, str], AltiumPcbDoc] = {}
        self._sessions: dict[int, ComponentLayerSession] = {}
        self._excluded: dict[int, frozenset[str]] = {}
        self.stacks: dict[int, ResolvedLayerStack] = {}
        self.contexts: dict[tuple[int, str, str], PcbSvgRenderContext] = {}
        self.component_metadata: dict[
            int, tuple[dict[int, str], dict[int, str], dict[int, dict[str, object]]]
        ] = {}
        self.fragments: dict[tuple[object, ...], tuple[str, ...]] = {}

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> Self:
        return cls(
            model_cache=None
            if getattr(args, "no_cache", False)
            else PcbSvgModelCache(getattr(args, "cache_dir", None)),
            workers=getattr(args, "workers", DEFAULT_WORKERS),
        )

    def finish(self) -> None:
        self.native_workers.close()
        log.info(
            "SVG native workers: limit %d, started %d clients",
            self.native_workers.count,
            self.native_workers.started_clients,
        )
        if self.model_cache is not None:
            self.model_cache.prune()
            log.info("SVG disk cache: %s", self.model_cache.counts)

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.finish()

    def identity(self, value: object) -> int:
        self._records[id(value)] = value
        return id(value)

    def register_board(
        self,
        pcbdoc: AltiumPcbDoc,
        *,
        excluded_designators: frozenset[str] = frozenset(),
    ) -> None:
        """Prepare the union of selected populations, skipping DNP in all of them."""
        key = self.identity(pcbdoc)
        if key in self._excluded and self._excluded[key] != excluded_designators:
            raise ValueError("Cannot change prepared SVG population within a job")
        self._excluded[key] = excluded_designators

    def register_variant(self, pcbdoc: AltiumPcbDoc, source: AltiumPcbDoc) -> None:
        """The caller guarantees only component parameters differ from source."""
        if pcbdoc is not source:
            self._sources[self.identity(pcbdoc)] = self.source(source)

    def source(self, pcbdoc: AltiumPcbDoc) -> AltiumPcbDoc:
        return self._sources.get(self.identity(pcbdoc), pcbdoc)

    def geometry_source(self, pcbdoc: AltiumPcbDoc) -> AltiumPcbDoc:
        source = self.source(pcbdoc)
        return self._geometry_sources.get(self.identity(source), source)

    def scoped_document(self, pcbdoc: AltiumPcbDoc, scope: str) -> AltiumPcbDoc:
        key = self.identity(pcbdoc), scope
        if key not in self._scoped:
            source = self.source(pcbdoc)
            if source is pcbdoc:
                scoped = _pcbdoc_with_cutout_scope(pcbdoc, scope)
                if scoped is not pcbdoc:
                    self._geometry_sources[self.identity(scoped)] = (
                        self.geometry_source(pcbdoc)
                    )
            else:
                base = self.scoped_document(source, scope)
                scoped = pcbdoc if base is source else copy(pcbdoc)
                if scoped is not pcbdoc:
                    scoped.board = base.board
                self.register_variant(scoped, base)
            self._scoped[key] = scoped
        return self._scoped[key]

    def components(self, pcbdoc: AltiumPcbDoc) -> ComponentLayerSession:
        # Cutout scoping changes the board outline, not component geometry.
        source = self.geometry_source(pcbdoc)
        key = self.identity(source)
        if key not in self._sessions:
            excluded = self._excluded.get(key, frozenset())
            self._sessions[key] = ComponentLayerSession(
                excluded, cache=self.model_cache, workers=self.native_workers
            )
        return self._sessions[key]

    @contextmanager
    def measure(self, stage: str, **labels: object) -> Iterator[dict[str, object]]:
        parent = self._frames[-1] if self._frames else None
        context = {**(parent.context if parent else {}), **labels}
        row = {
            "id": len(self.events),
            "parent_id": parent.row["id"] if parent else None,
            "stage": stage,
            **context,
            "cache": "none",
            "failed": False,
        }
        self.events.append(row)
        frame = _TimingFrame(row, context)
        self._frames.append(frame)
        started = time.perf_counter()
        try:
            yield row
        except BaseException:
            row["failed"] = True
            raise
        finally:
            elapsed = time.perf_counter() - started
            self._frames.pop()
            if parent:
                parent.children_seconds += elapsed
            row.update(
                seconds=elapsed,
                exclusive_seconds=max(0, elapsed - frame.children_seconds),
            )
            if stage in {"layer", "view", "variant"}:
                label = " / ".join(
                    str(context[k])
                    for k in ("board", "variant", "view", "layer")
                    if context.get(k) is not None
                )
                log.info(
                    "Render timing %s: %s %.3fs (%s)",
                    stage,
                    label,
                    elapsed,
                    row["cache"],
                )

    def write_timings(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "schema": "pcb.svg.timings.a0",
                    "clock": "wall",
                    "workers": self.native_workers.count,
                    "notes": "Parent times include children; exclusive_seconds subtracts measured children. Native waits are included. Variant/job totals include SVG file writing. Board/layer caches last one job; model_cache describes optional persistent geometry/SVG reuse.",
                    "events": self.events,
                    "model_cache": None
                    if self.model_cache is None
                    else {
                        "directory": str(self.model_cache.directory),
                        "counts": self.model_cache.counts,
                        "read_seconds": self.model_cache.read_seconds,
                        "write_seconds": self.model_cache.write_seconds,
                    },
                },
                indent=2,
            ),
            encoding="utf-8",
        )


def layer_side(token: str) -> str:
    for side in ("top", "bottom"):
        if token.startswith(side.upper()) or token.endswith("_" + side.upper()):
            return side
    return "board"


def view_side(tokens: Iterable[str]) -> str:
    sides = {layer_side(token) for token in tokens} - {"board"}
    return "both" if len(sides) > 1 else next(iter(sides), "board")


def layer_style_key(token: str, styles: Mapping[str, object]) -> str:
    """Keep unrelated annotation styles from invalidating manufacturing layers."""
    categories = {
        "BOARD_OUTLINE": ("board_outline",),
        "BOARD_CUTOUTS": ("board_cutouts",),
        "DRILLS": ("drills",),
        "SLOTS": ("slots",),
        "BOARD_SUBSTRATE": ("board_substrate",),
        "SOLDERMASK_FILM_TOP": ("soldermask_film",),
        "SOLDERMASK_FILM_BOTTOM": ("soldermask_film",),
        "TOP": (
            "copper_traces",
            "copper_polygons",
            "vias",
            "smd_pads",
            "through_hole_pads",
        ),
        "BOTTOM": (
            "copper_traces",
            "copper_polygons",
            "vias",
            "smd_pads",
            "through_hole_pads",
        ),
        "TOPOVERLAY": (
            "silkscreen_component_graphics",
            "silkscreen_board_graphics",
            "silkscreen_designators",
        ),
        "BOTTOMOVERLAY": (
            "silkscreen_component_graphics",
            "silkscreen_board_graphics",
            "silkscreen_designators",
        ),
    }.get(token)
    return json.dumps(
        styles if categories is None else {k: styles.get(k, {}) for k in categories},
        sort_keys=True,
    )


def layer_text_key(
    ctx: PcbSvgRenderContext, pcbdoc: AltiumPcbDoc, token: str
) -> tuple[tuple[str, ...], tuple[str, ...]] | tuple[()]:
    """Use the same substitution as primitive rendering, including mask/barcodes.

    Include all texts conservatively; variant parameters unused by any text do
    not invalidate layers. Component parameter changes are conservatively kept
    for text-bearing layers even where the current Monkey resolver is project-only.
    """
    if token in {
        "BOARD_OUTLINE",
        "BOARD_CUTOUTS",
        "DRILLS",
        "SLOTS",
        "BOARD_SUBSTRATE",
    }:
        return ()
    texts = tuple(
        ctx.substitute_special_strings(t.text_content or "") for t in pcbdoc.texts
    )
    parameters = tuple(
        json.dumps(c.parameters or {}, sort_keys=True) for c in pcbdoc.components
    )
    return texts, parameters
