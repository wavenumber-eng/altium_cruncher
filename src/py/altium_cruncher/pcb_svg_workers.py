"""Lazy, bounded native clients owned by a single SVG render job."""

from __future__ import annotations

import argparse
from concurrent.futures import CancelledError, Future, ThreadPoolExecutor
from collections.abc import Callable
from types import TracebackType
from typing import TYPE_CHECKING, Concatenate, Self, cast
import logging
import threading

if TYPE_CHECKING:
    from geometer import GeometerClient

log = logging.getLogger(__name__)
DEFAULT_WORKERS = 4


def validate_workers(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError("SVG workers must be a positive integer")
    return value


def _worker_argument(value: str) -> int:
    try:
        return validate_workers(int(value))
    except (ValueError, TypeError) as error:
        raise argparse.ArgumentTypeError(
            "workers must be a positive integer"
        ) from error


def add_svg_worker_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--workers",
        type=_worker_argument,
        default=DEFAULT_WORKERS,
        help="maximum concurrent native STEP tessellations or component illustrations (default: 4; 1 runs serially)",
    )


class PcbSvgNativeWorkers:
    """Each executor thread owns one client; callers commit results in source order.

    Submission and close belong to the render thread. Close cancels queued work,
    drains already-running calls with their normal timeouts, then closes every
    client. No threads/processes are created until a cache miss is submitted.
    """

    def __init__(
        self,
        count: int = DEFAULT_WORKERS,
        *,
        client_factory: Callable[[], GeometerClient] | None = None,
    ) -> None:
        self.count = validate_workers(count)
        self.client_factory = client_factory
        self._executor: ThreadPoolExecutor | None = None
        self._local = threading.local()
        self._clients: list[GeometerClient] = []
        self._lock = threading.Lock()
        self._closed = False
        self._closing = False
        self.started_clients = 0

    def submit[**P, R](
        self,
        function: Callable[Concatenate[GeometerClient, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[R]:
        if self._closing:
            raise RuntimeError("SVG native workers have been closed")
        if self._executor is None:
            self._executor = ThreadPoolExecutor(
                max_workers=self.count, thread_name_prefix="pcb-svg"
            )
        return self._executor.submit(self._run, function, args, kwargs)

    def _run[R](
        self,
        function: Callable[..., R],
        args: tuple[object, ...],
        kwargs: dict[str, object],
    ) -> R:
        if self._closing:
            raise CancelledError()
        if not hasattr(self._local, "client"):
            import geometer as g

            client = (self.client_factory or g.GeometerClient)()
            with self._lock:
                self.started_clients += 1
                closing = self._closing
                if not closing:
                    self._clients.append(client)
            if closing:
                client.close()
                raise CancelledError()
            self._local.client = client
        return function(cast("GeometerClient", self._local.client), *args, **kwargs)

    def close(self) -> None:
        if self._closed:
            return
        with self._lock:
            self._closing = True
        try:
            if self._executor is not None:
                self._executor.shutdown(wait=True, cancel_futures=True)
        finally:
            # Ctrl+C during executor draining must still close registered clients.
            # In-flight factories see _closing and close their own late clients.
            for client in self._clients:
                try:
                    client.close()
                except Exception as error:
                    log.warning("Closing SVG native worker: %s", error)
            self._clients.clear()
        # An interrupted cleanup can be retried; submissions remain blocked.
        self._closed = True

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()
