"""Generate an offline SVG review gallery from a small JSON manifest.

Manifest shape::

    {
      "title": "Projection review",
      "split_by_group_pattern": "^(Gate \\d+)",
      "items": [
        {"title": "Top", "path": "output/board__top.svg", "group": "Board"}
      ]
    }

Item paths are resolved relative to the manifest. The output may be either an
HTML filename or a directory, in which case ``index.html`` is written. When
``split_by_group_pattern`` is present, the main page is a lightweight index and
each regex match is written as a separate subgallery.
"""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
import re

from altium_cruncher.svg_review_gallery import SvgReviewItem, write_svg_review_gallery


def _manifest_item(
    manifest_path: Path, index: int, raw: object
) -> SvgReviewItem:
    if not isinstance(raw, dict):
        raise ValueError(f"Review manifest item {index} must be an object")
    title = raw.get("title")
    path = raw.get("path")
    if not isinstance(title, str) or not title.strip():
        raise ValueError(f"Review manifest item {index} needs a title")
    if not isinstance(path, str) or not path.strip():
        raise ValueError(f"Review manifest item {index} needs a path")
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = manifest_path.parent / candidate
    return SvgReviewItem(
        path=candidate,
        title=title,
        group=str(raw.get("group") or "SVG review"),
        detail=str(raw["detail"]) if raw.get("detail") is not None else None,
    )


def _manifest_items(manifest_path: Path, raw_items: object) -> list[SvgReviewItem]:
    """Resolve and validate the ordered SVG items from one manifest."""
    if not isinstance(raw_items, list) or not raw_items:
        raise ValueError("Review manifest 'items' must be a non-empty array")
    return [
        _manifest_item(manifest_path, index, raw)
        for index, raw in enumerate(raw_items)
    ]


def _slug(value: str) -> str:
    """Return a stable directory name for a matched gallery partition."""
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")
    if not slug:
        raise ValueError(f"Could not derive a gallery directory from {value!r}")
    return slug


def _write_split_index(
    target: Path,
    *,
    title: str,
    introduction: str,
    partitions: list[tuple[str, Path, list[SvgReviewItem]]],
) -> Path:
    """Write a lightweight landing page that does not embed any SVG markup."""
    cards: list[str] = []
    for label, gallery_path, items in partitions:
        relative_url = gallery_path.relative_to(target.parent).as_posix()
        groups = list(dict.fromkeys(item.group for item in items))
        svg_bytes = sum(item.path.stat().st_size for item in items)
        size_mb = svg_bytes / (1024 * 1024)
        cards.append(
            '<a class="gate" href="'
            + html.escape(relative_url, quote=True)
            + '"><strong>'
            + html.escape(label)
            + '</strong><span>'
            + f"{len(items)} SVG{'s' if len(items) != 1 else ''} · {size_mb:.1f} MiB source"
            + '</span><small>'
            + html.escape(" · ".join(groups))
            + "</small></a>"
        )
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>
:root {{ color-scheme: light; font-family: Inter, ui-sans-serif, system-ui, sans-serif; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: #e9edf2; color: #17212b; }}
main {{ width: min(100%, 1100px); margin: 0 auto; padding: clamp(18px, 4vw, 48px); }}
h1 {{ margin: 0; font-size: clamp(1.65rem, 3vw, 2.5rem); }}
.intro {{ margin: 8px 0 28px; max-width: 82ch; color: #526171; line-height: 1.5; }}
.gates {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr)); gap: 16px; }}
.gate {{ display: grid; gap: 7px; min-width: 0; padding: 18px; border: 1px solid #c7ced8;
  border-radius: 12px; background: white; color: #17212b; text-decoration: none;
  box-shadow: 0 8px 24px #24364a18; }}
.gate:hover, .gate:focus-visible {{ outline: 3px solid #2563eb; background: #f6f9fd; }}
.gate strong {{ font-size: 1.15rem; }}
.gate span {{ color: #1557a0; }}
.gate small {{ color: #657383; line-height: 1.4; }}
</style>
</head>
<body><main>
<h1>{html.escape(title)}</h1>
<p class="intro">{html.escape(introduction)} Each gate opens as a separate offline vector gallery, so large SVGs are parsed only when that gate is selected.</p>
<div class="gates">{"".join(cards)}</div>
</main></body>
</html>
"""
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page, encoding="utf-8")
    return target


def _write_split_galleries(
    output: Path,
    items: list[SvgReviewItem],
    *,
    pattern_text: str,
    title: str,
    introduction: str,
) -> Path:
    """Partition items by a group-label regex and write one gallery per match."""
    try:
        pattern = re.compile(pattern_text)
    except re.error as exc:
        raise ValueError(f"Invalid split_by_group_pattern: {exc}") from exc
    partitioned: dict[str, list[SvgReviewItem]] = {}
    for item in items:
        match = pattern.search(item.group)
        if match is None:
            raise ValueError(
                f"Review group {item.group!r} does not match split_by_group_pattern"
            )
        label = match.group(1) if match.lastindex else match.group(0)
        partitioned.setdefault(label, []).append(item)

    target = output if output.suffix.lower() == ".html" else output / "index.html"
    target = target.resolve()
    partitions: list[tuple[str, Path, list[SvgReviewItem]]] = []
    used_slugs: set[str] = set()
    for label, partition_items in partitioned.items():
        slug = _slug(label)
        if slug in used_slugs:
            raise ValueError(f"Duplicate split gallery directory {slug!r}")
        used_slugs.add(slug)
        gallery_path = write_svg_review_gallery(
            target.parent / slug / "index.html",
            partition_items,
            title=f"{title} · {label}",
            introduction=f"{introduction} This page contains only {label}.",
        )
        partitions.append((label, gallery_path, partition_items))
    return _write_split_index(
        target,
        title=title,
        introduction=introduction,
        partitions=partitions,
    )


def write_manifest_gallery(manifest_path: Path, output: Path) -> Path:
    """Load a review manifest and write its single or partitioned gallery."""
    manifest_path = manifest_path.resolve()
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    items = _manifest_items(manifest_path, payload.get("items"))
    title = str(payload.get("title") or "SVG review gallery")
    introduction = str(
        payload.get("introduction")
        or "Select a preview for vector-native pan and zoom inspection."
    )
    split_pattern = payload.get("split_by_group_pattern")
    if split_pattern is not None:
        if not isinstance(split_pattern, str) or not split_pattern:
            raise ValueError("split_by_group_pattern must be a non-empty string")
        return _write_split_galleries(
            output,
            items,
            pattern_text=split_pattern,
            title=title,
            introduction=introduction,
        )
    return write_svg_review_gallery(
        output.resolve(),
        items,
        title=title,
        introduction=introduction,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="JSON manifest of titled SVGs")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        required=True,
        help="output HTML path or directory",
    )
    args = parser.parse_args()
    print(write_manifest_gallery(args.manifest, args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
