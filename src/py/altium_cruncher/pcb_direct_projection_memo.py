"""Command-local coordination for exact native direct-model projections."""

from __future__ import annotations

from concurrent.futures import Future
from collections.abc import Callable
from dataclasses import asdict, is_dataclass
import hashlib
from threading import Lock
from typing import Literal

import geometer as g

from .pcb_illustration_model_geometry import IllustrationSymbol, digest


type Side = Literal["top", "bottom"]


class DirectProjectionMemo:
    """Single-flight projection cache plus cross-side uncut geometry facts."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._futures: dict[str, Future[IllustrationSymbol]] = {}
        self._uncut_facts: dict[tuple[str, Side], IllustrationSymbol] = {}

    def get(
        self, key: str, render: Callable[[], IllustrationSymbol]
    ) -> IllustrationSymbol:
        with self._lock:
            future = self._futures.get(key)
            owner = future is None
            if future is None:
                future = Future()
                self._futures[key] = future
        if not owner:
            return future.result()
        try:
            result = render()
        except BaseException as error:
            future.set_exception(error)
            raise
        future.set_result(result)
        return result

    def remember_uncut(
        self, source_key: str, side: Side, symbol: IllustrationSymbol
    ) -> None:
        with self._lock:
            self._uncut_facts.setdefault((source_key, side), symbol)

    def opposite_uncut(
        self, source_key: str, side: Side
    ) -> IllustrationSymbol | None:
        opposite: Side = "bottom" if side == "top" else "top"
        with self._lock:
            return self._uncut_facts.get((source_key, opposite))


def direct_source_key(
    source: g.ModelIllustrationSourceA0, model: bytes | None
) -> str:
    """Hash the native source and optional model attachment, independent of view."""

    return digest(
        {
            "source": asdict(source) if is_dataclass(source) else repr(source),
            "model_sha256": (
                None if model is None else hashlib.sha256(model).hexdigest()
            ),
        }
    )
