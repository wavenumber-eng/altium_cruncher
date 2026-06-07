"""Structured schematic note extraction for Altium projects."""

from __future__ import annotations

import json
from pathlib import Path

from altium_cruncher.altium_cruncher_common import _resolve_output_dir

NOTES_SCHEMA = "altium_cruncher.notes.a0"


def build_notes_payload(input_file: Path | str) -> dict[str, object]:
    """Build structured note/text payloads for one SchDoc or PrjPcb input."""
    source = Path(input_file).resolve()
    schdoc_paths = _resolve_schdoc_paths(source)
    pages = [
        _schdoc_notes_page(
            schdoc_path,
            page_number=index + 1,
            page_count=len(schdoc_paths),
        )
        for index, schdoc_path in enumerate(schdoc_paths)
    ]
    counts = _payload_counts(pages)
    return {
        "schema": NOTES_SCHEMA,
        "input": str(source),
        "source_kind": source.suffix.lower().lstrip("."),
        "schdoc_count": len(schdoc_paths),
        "counts": counts,
        "schdocs": pages,
    }


def write_notes_payload(
    input_file: Path | str,
    *,
    output: Path | None = None,
) -> Path:
    """Write structured notes JSON and return the output path."""
    source = Path(input_file).resolve()
    output_dir = _resolve_output_dir(output, "notes")
    output_path = output_dir / f"{source.stem}_notes.json"
    output_path.write_text(
        json.dumps(build_notes_payload(source), indent=2),
        encoding="utf-8",
    )
    return output_path


def _resolve_schdoc_paths(source: Path) -> list[Path]:
    suffix = source.suffix.lower()
    if suffix == ".schdoc":
        return [source]
    if suffix == ".prjpcb":
        from altium_monkey.altium_prjpcb import AltiumPrjPcb

        return AltiumPrjPcb(source).get_schdoc_paths()
    raise ValueError(f"Unsupported notes input type: {source.suffix}")


def _schdoc_notes_page(
    schdoc_path: Path,
    *,
    page_number: int,
    page_count: int,
) -> dict[str, object]:
    from altium_monkey.altium_schdoc import AltiumSchDoc

    schdoc = AltiumSchDoc(schdoc_path)
    notes = [_object_entry("note", obj) for obj in schdoc.notes]
    text_frames = [_object_entry("text_frame", obj) for obj in schdoc.text_frames]
    free_text = [_object_entry("free_text", obj) for obj in schdoc.text_strings]
    return {
        "file": str(schdoc_path.resolve()),
        "page_number": page_number,
        "page_count": page_count,
        "page_name": schdoc_path.stem,
        "notes": notes,
        "text_frames": text_frames,
        "free_text": free_text,
        "counts": {
            "notes": len(notes),
            "text_frames": len(text_frames),
            "free_text": len(free_text),
        },
    }


def _object_entry(kind: str, obj: object) -> dict[str, object]:
    entry: dict[str, object] = {
        "kind": kind,
        "object_type": type(obj).__name__,
        "text": str(getattr(obj, "text", "") or ""),
        "position_mils": _point_to_json(getattr(obj, "location", None)),
        "is_hidden": bool(getattr(obj, "is_hidden", False)),
    }
    bounds = _bounds_to_json(obj)
    if bounds is not None:
        entry["bounds_mils"] = bounds
    _append_optional(entry, "author", getattr(obj, "author", None))
    _append_optional(entry, "collapsed", getattr(obj, "collapsed", None))
    _append_optional(entry, "alignment", getattr(obj, "alignment", None))
    _append_enum_or_value(entry, "orientation", getattr(obj, "orientation", None))
    _append_enum_or_value(entry, "justification", getattr(obj, "justification", None))
    return entry


def _append_optional(
    entry: dict[str, object],
    name: str,
    value: object,
) -> None:
    if value is not None:
        entry[name] = _jsonable_value(value)


def _append_enum_or_value(
    entry: dict[str, object],
    name: str,
    value: object,
) -> None:
    if value is None:
        return
    enum_name = getattr(value, "name", None)
    if enum_name:
        entry[name] = str(enum_name)
    else:
        entry[name] = _jsonable_value(value)


def _jsonable_value(value: object) -> object:
    if isinstance(value, str | int | float | bool):
        return value
    return str(value)


def _point_to_json(point: object) -> dict[str, float] | None:
    if point is None:
        return None
    return {
        "x": float(getattr(point, "x_mils", 0.0)),
        "y": float(getattr(point, "y_mils", 0.0)),
    }


def _bounds_to_json(obj: object) -> dict[str, float] | None:
    p1 = getattr(obj, "location", None)
    p2 = getattr(obj, "corner", None)
    if p1 is None or p2 is None:
        return None
    x1 = float(getattr(p1, "x_mils", 0.0))
    y1 = float(getattr(p1, "y_mils", 0.0))
    x2 = float(getattr(p2, "x_mils", 0.0))
    y2 = float(getattr(p2, "y_mils", 0.0))
    return {
        "x_min": min(x1, x2),
        "y_min": min(y1, y2),
        "x_max": max(x1, x2),
        "y_max": max(y1, y2),
    }


def _payload_counts(pages: list[dict[str, object]]) -> dict[str, int]:
    totals = {"notes": 0, "text_frames": 0, "free_text": 0}
    for page in pages:
        counts = page.get("counts", {})
        if not isinstance(counts, dict):
            continue
        totals["notes"] += int(counts.get("notes", 0))
        totals["text_frames"] += int(counts.get("text_frames", 0))
        totals["free_text"] += int(counts.get("free_text", 0))
    totals["all_text_annotations"] = sum(totals.values())
    return totals
