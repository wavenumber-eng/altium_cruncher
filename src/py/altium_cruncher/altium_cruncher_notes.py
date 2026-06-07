"""Structured schematic note extraction for Altium projects."""

from __future__ import annotations

import json
from pathlib import Path

from altium_cruncher.altium_cruncher_common import _resolve_output_dir

NOTES_SCHEMA = "altium_cruncher.notes.a0"
NOTES_JSONC_HEADER = """/*
altium-cruncher notes artifact

Schema: altium_cruncher.notes.a0
Intent: review-focused schematic annotations for agents and humans.
Path policy: input and page file values are relative to the input SchDoc or PrjPcb
directory, not absolute machine-local paths.
Filtering: dedicated Note objects and schematic-owned text are included by
default. Text owned by sheet templates or title blocks is suppressed by default.
Use --include-sheet-template-text for raw diagnostic output. Empty annotation
categories and pages without included annotations are omitted.
*/
"""


def build_notes_payload(
    input_file: Path | str,
    *,
    include_sheet_template_text: bool = False,
) -> dict[str, object]:
    """Build structured note/text payloads for one SchDoc or PrjPcb input."""
    source = Path(input_file).resolve()
    path_base = source.parent
    schdoc_paths = _resolve_schdoc_paths(source)
    pages: list[dict[str, object]] = []
    for index, schdoc_path in enumerate(schdoc_paths):
        page = _schdoc_notes_page(
            schdoc_path,
            include_sheet_template_text=include_sheet_template_text,
            path_base=path_base,
        )
        if _page_has_annotations(page):
            pages.append(page)
    return {
        "schema": NOTES_SCHEMA,
        "input": _portable_path(source, path_base),
        "source_kind": source.suffix.lower().lstrip("."),
        "path_base": "input_directory",
        "schdoc_count": len(schdoc_paths),
        "filters": {
            "include_sheet_template_text": include_sheet_template_text,
            "default_suppression": "sheet-template/title-block owned text",
        },
        "schdocs": pages,
    }


def write_notes_payload(
    input_file: Path | str,
    *,
    output: Path | None = None,
    include_sheet_template_text: bool = False,
) -> Path:
    """Write structured notes JSONC and return the output path."""
    source = Path(input_file).resolve()
    output_dir = _resolve_output_dir(output, "notes")
    output_path = output_dir / f"{source.stem}_notes.jsonc"
    output_path.write_text(
        render_notes_jsonc(
            build_notes_payload(
                source,
                include_sheet_template_text=include_sheet_template_text,
            )
        ),
        encoding="utf-8",
    )
    return output_path


def render_notes_jsonc(payload: dict[str, object]) -> str:
    """Render a notes payload as commented JSONC."""
    return NOTES_JSONC_HEADER + json.dumps(payload, indent=2) + "\n"


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
    include_sheet_template_text: bool,
    path_base: Path,
) -> dict[str, object]:
    from altium_monkey.altium_schdoc import AltiumSchDoc

    schdoc = AltiumSchDoc(schdoc_path)
    notes = _filtered_entries(
        schdoc.notes,
        include_sheet_template_text=include_sheet_template_text,
    )
    text_frames = _filtered_entries(
        schdoc.text_frames,
        include_sheet_template_text=include_sheet_template_text,
    )
    free_text = _filtered_entries(
        schdoc.text_strings,
        include_sheet_template_text=include_sheet_template_text,
    )
    page: dict[str, object] = {
        "file": _portable_path(schdoc_path.resolve(), path_base),
    }
    _append_entries(page, "notes", notes)
    _append_entries(page, "text_frames", text_frames)
    _append_entries(page, "free_text", free_text)
    return page


def _filtered_entries(
    objects: object,
    *,
    include_sheet_template_text: bool,
) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for obj in objects:
        if (
            not include_sheet_template_text
            and _source_scope(_owner_index(obj)) == "sheet_template"
        ):
            continue
        entries.append(_object_entry(obj))
    return entries


def _append_entries(
    page: dict[str, object],
    name: str,
    entries: list[dict[str, object]],
) -> None:
    if entries:
        page[name] = entries


def _page_has_annotations(page: dict[str, object]) -> bool:
    return any(name in page for name in ("notes", "text_frames", "free_text"))


def _object_entry(obj: object) -> dict[str, object]:
    entry: dict[str, object] = {
        "text": str(getattr(obj, "text", "") or ""),
        "position_mils": _point_to_json(getattr(obj, "location", None)),
    }
    _append_optional_text(entry, "unique_id", getattr(obj, "unique_id", None))
    bounds = _bounds_to_json(obj)
    if bounds is not None:
        entry["bounds_mils"] = bounds
    _append_optional(entry, "author", getattr(obj, "author", None))
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


def _append_optional_text(
    entry: dict[str, object],
    name: str,
    value: object,
) -> None:
    text = str(value or "").strip()
    if text:
        entry[name] = text


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


def _portable_path(path: Path, base: Path) -> str:
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return path.name
