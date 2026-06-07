"""Structured schematic note extraction for Altium projects."""

from __future__ import annotations

import json
from pathlib import Path

from altium_cruncher.altium_cruncher_common import _resolve_output_dir

NOTES_SCHEMA = "altium_cruncher.notes.a0"


def build_notes_payload(
    input_file: Path | str,
    *,
    include_sheet_template_text: bool = False,
) -> dict[str, object]:
    """Build structured note/text payloads for one SchDoc or PrjPcb input."""
    source = Path(input_file).resolve()
    schdoc_paths = _resolve_schdoc_paths(source)
    pages = [
        _schdoc_notes_page(
            schdoc_path,
            page_number=index + 1,
            page_count=len(schdoc_paths),
            include_sheet_template_text=include_sheet_template_text,
        )
        for index, schdoc_path in enumerate(schdoc_paths)
    ]
    counts = _payload_counts(pages)
    suppressed_counts = _payload_counts(pages, field="suppressed_counts")
    return {
        "schema": NOTES_SCHEMA,
        "input": str(source),
        "source_kind": source.suffix.lower().lstrip("."),
        "schdoc_count": len(schdoc_paths),
        "filters": {
            "include_sheet_template_text": include_sheet_template_text,
            "default_suppression": "sheet-template/title-block owned text",
        },
        "counts": counts,
        "suppressed_counts": suppressed_counts,
        "schdocs": pages,
    }


def write_notes_payload(
    input_file: Path | str,
    *,
    output: Path | None = None,
    include_sheet_template_text: bool = False,
) -> Path:
    """Write structured notes JSON and return the output path."""
    source = Path(input_file).resolve()
    output_dir = _resolve_output_dir(output, "notes")
    output_path = output_dir / f"{source.stem}_notes.json"
    output_path.write_text(
        json.dumps(
            build_notes_payload(
                source,
                include_sheet_template_text=include_sheet_template_text,
            ),
            indent=2,
        ),
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
    include_sheet_template_text: bool,
) -> dict[str, object]:
    from altium_monkey.altium_schdoc import AltiumSchDoc

    schdoc = AltiumSchDoc(schdoc_path)
    notes, suppressed_notes = _filtered_entries(
        "note",
        schdoc.notes,
        include_sheet_template_text=include_sheet_template_text,
    )
    text_frames, suppressed_text_frames = _filtered_entries(
        "text_frame",
        schdoc.text_frames,
        include_sheet_template_text=include_sheet_template_text,
    )
    free_text, suppressed_free_text = _filtered_entries(
        "free_text",
        schdoc.text_strings,
        include_sheet_template_text=include_sheet_template_text,
    )
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
        "suppressed_counts": _counts_dict(
            notes=suppressed_notes,
            text_frames=suppressed_text_frames,
            free_text=suppressed_free_text,
        ),
    }


def _filtered_entries(
    kind: str,
    objects: object,
    *,
    include_sheet_template_text: bool,
) -> tuple[list[dict[str, object]], int]:
    entries: list[dict[str, object]] = []
    suppressed_count = 0
    for obj in objects:
        entry = _object_entry(kind, obj)
        if (
            not include_sheet_template_text
            and entry["source_scope"] == "sheet_template"
        ):
            suppressed_count += 1
            continue
        entries.append(entry)
    return entries, suppressed_count


def _object_entry(kind: str, obj: object) -> dict[str, object]:
    owner_index = _owner_index(obj)
    entry: dict[str, object] = {
        "kind": kind,
        "object_type": type(obj).__name__,
        "text": str(getattr(obj, "text", "") or ""),
        "position_mils": _point_to_json(getattr(obj, "location", None)),
        "is_hidden": bool(getattr(obj, "is_hidden", False)),
        "owner_index": owner_index,
        "source_scope": _source_scope(owner_index),
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


def _owner_index(obj: object) -> int | None:
    value = getattr(obj, "_owner_index", None)
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _source_scope(owner_index: int | None) -> str:
    if owner_index in (None, 0):
        return "schematic"
    return "sheet_template"


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


def _payload_counts(
    pages: list[dict[str, object]],
    *,
    field: str = "counts",
) -> dict[str, int]:
    totals = _counts_dict(notes=0, text_frames=0, free_text=0)
    for page in pages:
        counts = page.get(field, {})
        if not isinstance(counts, dict):
            continue
        totals["notes"] += int(counts.get("notes", 0))
        totals["text_frames"] += int(counts.get("text_frames", 0))
        totals["free_text"] += int(counts.get("free_text", 0))
    totals["all_text_annotations"] = (
        totals["notes"] + totals["text_frames"] + totals["free_text"]
    )
    return totals


def _counts_dict(
    *,
    notes: int,
    text_frames: int,
    free_text: int,
) -> dict[str, int]:
    return {
        "notes": notes,
        "text_frames": text_frames,
        "free_text": free_text,
        "all_text_annotations": notes + text_frames + free_text,
    }
