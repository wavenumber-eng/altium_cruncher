"""Shared JSONC-compatible config loading and rendering helpers."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import json
from pathlib import Path

import jsonc  # type: ignore[import-untyped]

JsoncCommentMap = Mapping[tuple[str, ...] | str, str | Sequence[str]]


def load_json_config(path: Path) -> object:
    """Load a user-editable JSON/JSONC config file."""
    text = path.read_text(encoding="utf-8-sig")
    return jsonc.loads(text)


def render_commented_jsonc(
    value: object,
    *,
    comments_by_path: JsoncCommentMap | None = None,
    comments_by_key: Mapping[str, str | Sequence[str]] | None = None,
    header_lines: Sequence[str] = (),
) -> str:
    """Render a JSON-compatible value with JSONC field comments.

    ``comments_by_path`` keys can be tuple paths such as
    ``("output", "mode")`` or dotted string paths such as ``"output.mode"``.
    ``comments_by_key`` is a fallback for repeated object keys.
    """
    normalized_path_comments = _normalize_comment_map(comments_by_path or {})
    text = _jsonc_dump_value(
        value,
        indent=0,
        path=(),
        comments_by_path=normalized_path_comments,
        comments_by_key=comments_by_key or {},
    )
    if not header_lines:
        return f"{text}\n"
    lines = [f"// {line}" if line else "//" for line in header_lines]
    lines.append(text)
    return "\n".join(lines) + "\n"


def enum_help(description: str, options: Sequence[str]) -> str:
    """Return standard help text for string/enum config fields."""
    return f"{description} Options: {', '.join(options)}."


def _normalize_comment_map(
    comments: JsoncCommentMap,
) -> dict[tuple[str, ...], str | Sequence[str]]:
    normalized: dict[tuple[str, ...], str | Sequence[str]] = {}
    for raw_path, comment in comments.items():
        if isinstance(raw_path, str):
            path = tuple(part for part in raw_path.split(".") if part)
        else:
            path = tuple(raw_path)
        normalized[path] = comment
    return normalized


def _jsonc_dump_value(
    value: object,
    *,
    indent: int,
    path: tuple[str, ...],
    comments_by_path: Mapping[tuple[str, ...], str | Sequence[str]],
    comments_by_key: Mapping[str, str | Sequence[str]],
) -> str:
    if isinstance(value, dict):
        return _jsonc_dump_object(
            value,
            indent=indent,
            path=path,
            comments_by_path=comments_by_path,
            comments_by_key=comments_by_key,
        )
    if isinstance(value, list):
        return _jsonc_dump_list(
            value,
            indent=indent,
            path=path,
            comments_by_path=comments_by_path,
            comments_by_key=comments_by_key,
        )
    return json.dumps(value)


def _jsonc_dump_object(
    value: Mapping[object, object],
    *,
    indent: int,
    path: tuple[str, ...],
    comments_by_path: Mapping[tuple[str, ...], str | Sequence[str]],
    comments_by_key: Mapping[str, str | Sequence[str]],
) -> str:
    if not value:
        return "{}"

    lines = ["{"]
    items = list(value.items())
    for index, (raw_key, item) in enumerate(items):
        key = str(raw_key)
        child_path = (*path, key)
        comment = _jsonc_comment_for_path(
            child_path,
            comments_by_path=comments_by_path,
            comments_by_key=comments_by_key,
        )
        if comment:
            lines.extend(_jsonc_comment_lines(comment, indent + 2))

        item_text = _jsonc_dump_value(
            item,
            indent=indent + 2,
            path=child_path,
            comments_by_path=comments_by_path,
            comments_by_key=comments_by_key,
        )
        item_lines = item_text.splitlines()
        prefix = f"{' ' * (indent + 2)}{json.dumps(key)}: "
        entry_lines = [prefix + item_lines[0]]
        entry_lines.extend(item_lines[1:])
        if index < len(items) - 1:
            entry_lines[-1] += ","
        lines.extend(entry_lines)
    lines.append(f"{' ' * indent}}}")
    return "\n".join(lines)


def _jsonc_dump_list(
    value: list[object],
    *,
    indent: int,
    path: tuple[str, ...],
    comments_by_path: Mapping[tuple[str, ...], str | Sequence[str]],
    comments_by_key: Mapping[str, str | Sequence[str]],
) -> str:
    if not value:
        return "[]"
    if all(not isinstance(item, dict | list) for item in value):
        return json.dumps(value)

    lines = ["["]
    for index, item in enumerate(value):
        item_path = path if isinstance(item, dict | list) else (*path, "*")
        item_text = _jsonc_dump_value(
            item,
            indent=indent + 2,
            path=item_path,
            comments_by_path=comments_by_path,
            comments_by_key=comments_by_key,
        )
        item_lines = item_text.splitlines()
        entry_lines = [f"{' ' * (indent + 2)}{item_lines[0]}"]
        entry_lines.extend(item_lines[1:])
        if index < len(value) - 1:
            entry_lines[-1] += ","
        lines.extend(entry_lines)
    lines.append(f"{' ' * indent}]")
    return "\n".join(lines)


def _jsonc_comment_for_path(
    path: tuple[str, ...],
    *,
    comments_by_path: Mapping[tuple[str, ...], str | Sequence[str]],
    comments_by_key: Mapping[str, str | Sequence[str]],
) -> str | Sequence[str]:
    return comments_by_path.get(path) or comments_by_key.get(path[-1], "")


def _jsonc_comment_lines(comment: str | Sequence[str], indent: int) -> list[str]:
    if isinstance(comment, str):
        comment_lines = [comment]
    else:
        comment_lines = [str(line) for line in comment]
    return [f"{' ' * indent}/* {line} */" for line in comment_lines if line]


__all__ = ["enum_help", "load_json_config", "render_commented_jsonc"]
