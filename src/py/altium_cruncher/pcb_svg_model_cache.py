"""Versioned, content-addressed native geometry/SVG cache (JSON, never pickle)."""

from __future__ import annotations

import gzip
import argparse
from collections.abc import Callable, Iterator
import hashlib
from importlib.metadata import version
import json
import logging
import os
from pathlib import Path
import platform
import tempfile
import time
import zlib

log = logging.getLogger(__name__)
SCHEMA = "pcb.svg.model-cache.a1"
MAX_BYTES = 1024 * 1024 * 1024
MAX_ENTRY_BYTES = 256 * 1024 * 1024
_CACHE_POLICY_FILES = (
    "altium_cruncher_pcb_illustration.py",
    "altium_cruncher_pcb_svg_component_layers.py",
    "altium_cruncher_pcb_svg_substrate.py",
    "pcb_board_region_envelope_index.py",
    "pcb_component_clipping.py",
    "pcb_direct_projection_memo.py",
    "pcb_direct_projection_prewarm.py",
    "pcb_direct_projection_runtime.py",
    "pcb_illustration_model_geometry.py",
    "pcb_model_rotation.py",
    "pcb_svg_component_cache.py",
)


def cache_directory() -> Path:
    if os.name == "nt":
        root = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local"))
    elif platform.system() == "Darwin":
        root = Path.home() / "Library/Caches"
    else:
        root = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return root / "altium-cruncher" / "svg-models"


def _json_bytes(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode()


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def native_cache_identity() -> str:
    import geometer as g

    executable = g.executable_path().resolve()
    # Hash the consumed executable and adjacent dynamic libraries, including
    # custom GEOMETER_EXE builds. Package version alone misses local rebuilds.
    binaries = [
        executable,
        *sorted(executable.parent.glob("*.dll")),
        *sorted(executable.parent.glob("*.so*")),
        *sorted(executable.parent.glob("*.dylib")),
    ]
    package = Path(__file__).parent
    return _sha(
        _json_bytes(
            dict(
                schema=SCHEMA,
                geometer=version("wn-geometer"),
                monkey=version("altium-monkey"),
                platform=platform.system(),
                machine=platform.machine(),
                binaries={
                    p.name: _sha(p.read_bytes()) for p in binaries if p.is_file()
                },
                policy_sources={
                    name: _sha((package / name).read_bytes())
                    for name in _CACHE_POLICY_FILES
                },
            )
        )
    )


class PcbSvgModelCache:
    """Optional cache failures become misses; only completed positive results persist."""

    def __init__(
        self,
        directory: Path | None = None,
        *,
        identity: str | None = None,
        max_bytes: int = MAX_BYTES,
    ) -> None:
        self.directory = (
            directory if directory is not None else cache_directory()
        ) / "a1"
        self._identity = identity
        self.max_bytes = max_bytes
        self._warned: set[str] = set()
        self.counts = dict(hits=0, misses=0, writes=0, invalid=0, evictions=0)
        self.read_seconds = 0.0
        self.write_seconds = 0.0

    def _path(self, kind: str, key: str) -> Path:
        if (
            kind not in {"tessellation", "illustration", "component-artwork"}
            or len(key) != 64
            or any(c not in "0123456789abcdef" for c in key)
        ):
            raise ValueError("Invalid SVG model cache key")
        if self._identity is None:
            self._identity = native_cache_identity()
        if len(self._identity) != 64 or any(
            c not in "0123456789abcdef" for c in self._identity
        ):
            raise ValueError("Invalid SVG model cache build identity")
        return self.directory / self._identity / kind / (key + ".json.gz")

    def _warn(self, message: str) -> None:
        if message not in self._warned:
            self._warned.add(message)
            log.warning("SVG model cache: %s; rendering continues", message)

    def load[T](self, kind: str, key: str, decode: Callable[[object], T]) -> T | None:
        started = time.perf_counter()
        try:
            path = self._path(kind, key)
            if not path.is_file():
                self.counts["misses"] += 1
                return None
            with gzip.open(path, "rb") as stream:
                raw = stream.read(MAX_ENTRY_BYTES + 1)
            if len(raw) > MAX_ENTRY_BYTES:
                raise ValueError("entry exceeds size limit")
            entry = json.loads(raw)
            if (
                entry["schema"] != SCHEMA
                or entry["kind"] != kind
                or entry["key"] != key
            ):
                raise ValueError("entry identity mismatch")
            payload = entry["payload"]
            if entry["sha256"] != _sha(_json_bytes(payload)):
                raise ValueError("entry checksum mismatch")
            value = decode(payload)
            self.counts["hits"] += 1
            try:
                path.touch()  # Recently reused entries survive size-based eviction.
            except OSError:
                pass
            return value
        except (
            OSError,
            EOFError,
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            zlib.error,
        ) as error:
            self.counts["invalid"] += 1
            self.counts["misses"] += 1
            self._warn(f"cannot reuse {kind} entry ({error})")
            return None
        finally:
            self.read_seconds += time.perf_counter() - started

    def store(self, kind: str, key: str, payload: object) -> None:
        started = time.perf_counter()
        temporary = None
        try:
            path = self._path(kind, key)
            entry = dict(
                schema=SCHEMA,
                kind=kind,
                key=key,
                payload=payload,
                sha256=_sha(_json_bytes(payload)),
            )
            raw = _json_bytes(entry)
            if len(raw) > MAX_ENTRY_BYTES:
                return
            data = gzip.compress(raw, compresslevel=1, mtime=0)
            if len(data) > self.max_bytes:
                return
            path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                dir=path.parent, suffix=".tmp", delete=False
            ) as stream:
                temporary = Path(stream.name)
                stream.write(data)
            os.replace(temporary, path)
            temporary = None
            self.counts["writes"] += 1
            # A render job can write hundreds of entries.  Eviction enumerates
            # the complete cache, so doing it here makes cold population
            # O(writes * existing entries).  PcbSvgRenderJob owns the cache's
            # command lifetime and prunes once from finish(), including when
            # its context exits through an exception.
        except (OSError, ValueError, TypeError) as error:
            self._warn(f"cannot save {kind} entry ({error})")
        finally:
            if temporary is not None:
                try:
                    temporary.unlink(missing_ok=True)
                except OSError:
                    pass
            self.write_seconds += time.perf_counter() - started

    def _entries(self) -> Iterator[tuple[int, int, Path]]:
        """Enumerate only cache-owned regular files, tolerating concurrent eviction."""
        for path in self.directory.glob("*/*/*.json.gz"):
            if not _owned_entry_path(path):
                continue
            try:
                stat = path.stat()
            except OSError:
                continue
            yield stat.st_mtime_ns, stat.st_size, path

    def prune(self) -> None:
        """Bound our generated entries; never recursively delete user directories."""
        try:
            entries = list(self._entries())
            size = sum(item[1] for item in entries)
            for _, length, path in sorted(entries):
                if size <= self.max_bytes:
                    break
                path.unlink(missing_ok=True)
                size -= length
                self.counts["evictions"] += 1
        except OSError as error:
            self._warn(f"cannot trim cache ({error})")


def _owned_entry_path(path: Path) -> bool:
    if path.parent.name not in {"tessellation", "illustration", "component-artwork"}:
        return False
    if len(path.parent.parent.name) != 64 or len(path.name) != 72:
        return False
    if any(
        c not in "0123456789abcdef" for c in path.parent.parent.name + path.name[:-8]
    ):
        return False
    return not any(
        item.is_symlink() for item in (path, path.parent, path.parent.parent)
    )


def add_model_cache_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--cache-dir",
        type=Path,
        help="persistent model/SVG cache directory (default: OS user cache/altium-cruncher/svg-models)",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="disable persistent model/SVG caching; retain reuse within this command",
    )
