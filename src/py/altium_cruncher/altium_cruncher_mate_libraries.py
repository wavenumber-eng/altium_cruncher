"""Library discovery helpers for mate workflows."""

from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from io import StringIO
import logging
from pathlib import Path

from altium_cruncher.altium_cruncher_mco import JsonObject


@dataclass(frozen=True, slots=True)
class MateLibraryEntry:
    """One symbol or footprint discovered in an Altium library file."""

    name: str
    library_path: Path

    def to_dict(self) -> JsonObject:
        return {
            "name": self.name,
            "library": self.library_path.as_posix(),
        }


@dataclass(frozen=True, slots=True)
class MateLibraryScanResult:
    """Symbols and footprints found under configured mate library roots."""

    roots: tuple[Path, ...]
    recursive: bool
    symbols: tuple[MateLibraryEntry, ...]
    footprints: tuple[MateLibraryEntry, ...]
    warnings: tuple[str, ...]

    def to_dict(self) -> JsonObject:
        return {
            "schema": "wn.altium_cruncher.mate.library_scan.v1",
            "roots": [root.as_posix() for root in self.roots],
            "recursive": self.recursive,
            "symbols": [entry.to_dict() for entry in self.symbols],
            "footprints": [entry.to_dict() for entry in self.footprints],
            "warnings": list(self.warnings),
        }


def scan_mate_libraries(
    roots: Sequence[Path | str],
    *,
    recursive: bool = True,
) -> MateLibraryScanResult:
    """Scan Altium SchLib/PcbLib files for symbol and footprint names."""
    resolved_roots = tuple(Path(root).resolve() for root in roots)
    symbols: list[MateLibraryEntry] = []
    footprints: list[MateLibraryEntry] = []
    warnings: list[str] = []
    for library_path in _iter_library_files(resolved_roots, recursive=recursive):
        suffix = library_path.suffix.lower()
        if suffix == ".schlib":
            try:
                symbols.extend(_schlib_entries(library_path))
            except Exception as exc:
                warnings.append(f"{library_path}: {exc}")
        elif suffix == ".pcblib":
            try:
                footprints.extend(_pcblib_entries(library_path))
            except Exception as exc:
                warnings.append(f"{library_path}: {exc}")
    return MateLibraryScanResult(
        roots=resolved_roots,
        recursive=recursive,
        symbols=tuple(sorted(symbols, key=_entry_sort_key)),
        footprints=tuple(sorted(footprints, key=_entry_sort_key)),
        warnings=tuple(warnings),
    )


def resolve_mate_symbol(
    scan: MateLibraryScanResult,
    symbol_name: str,
) -> MateLibraryEntry:
    """Resolve a unique symbol name from a mate library scan."""
    return _resolve_unique(scan.symbols, symbol_name, "symbol")


def resolve_mate_footprint(
    scan: MateLibraryScanResult,
    footprint_name: str,
) -> MateLibraryEntry:
    """Resolve a unique footprint name from a mate library scan."""
    return _resolve_unique(scan.footprints, footprint_name, "footprint")


def _iter_library_files(
    roots: Iterable[Path],
    *,
    recursive: bool,
) -> Iterable[Path]:
    seen: set[Path] = set()
    for root in roots:
        if root.is_file():
            candidates = [root]
        elif root.is_dir():
            candidates = root.rglob("*") if recursive else root.glob("*")
        else:
            continue
        for candidate in candidates:
            if not candidate.is_file():
                continue
            if candidate.suffix.lower() not in {".schlib", ".pcblib"}:
                continue
            resolved = candidate.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            yield resolved


def _schlib_entries(library_path: Path) -> list[MateLibraryEntry]:
    from altium_monkey import AltiumSchLib

    with _quiet_library_loader():
        schlib = AltiumSchLib(library_path)
    return [
        MateLibraryEntry(name=name, library_path=library_path)
        for symbol in list(getattr(schlib, "symbols", []) or [])
        for name in [_object_name(symbol)]
        if name
    ]


def _pcblib_entries(library_path: Path) -> list[MateLibraryEntry]:
    from altium_monkey import AltiumPcbLib

    with _quiet_library_loader():
        pcblib = AltiumPcbLib.from_file(library_path)
    return [
        MateLibraryEntry(name=name, library_path=library_path)
        for footprint in list(getattr(pcblib, "footprints", []) or [])
        for name in [_object_name(footprint)]
        if name
    ]


def _object_name(value: object) -> str:
    return str(getattr(value, "name", "") or "").strip()


class _quiet_library_loader:
    def __enter__(self) -> None:
        self._previous_disable_level = logging.root.manager.disable
        logging.disable(logging.INFO)
        self._stdout = redirect_stdout(StringIO())
        self._stderr = redirect_stderr(StringIO())
        self._stdout.__enter__()
        self._stderr.__enter__()

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        self._stderr.__exit__(exc_type, exc, tb)
        self._stdout.__exit__(exc_type, exc, tb)
        logging.disable(self._previous_disable_level)


def _resolve_unique(
    entries: Sequence[MateLibraryEntry],
    requested_name: str,
    label: str,
) -> MateLibraryEntry:
    normalized_name = requested_name.strip().casefold()
    matches = [
        entry
        for entry in entries
        if entry.name.strip().casefold() == normalized_name
    ]
    if not matches:
        raise ValueError(f"Mate {label} not found in configured libraries: {requested_name}")
    unique_paths = {entry.library_path.resolve() for entry in matches}
    if len(unique_paths) > 1:
        paths = ", ".join(path.as_posix() for path in sorted(unique_paths))
        raise ValueError(
            f"Mate {label} {requested_name!r} is ambiguous across libraries: {paths}"
        )
    return matches[0]


def _entry_sort_key(entry: MateLibraryEntry) -> tuple[str, str]:
    return (entry.name.casefold(), entry.library_path.as_posix().casefold())
