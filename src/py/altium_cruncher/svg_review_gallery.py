"""Offline, vector-native review galleries for arbitrary SVG artifacts."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import html
import json
import os
from pathlib import Path
from urllib.parse import quote
import xml.etree.ElementTree as ET

_VENDOR = Path(__file__).with_name("_vendor") / "svg_pan_zoom"
_SVG_PAN_ZOOM = _VENDOR / "svg-pan-zoom.min.js"
_DISALLOWED_SVG_ELEMENTS = {"script", "foreignObject", "iframe", "object", "embed"}
ET.register_namespace("", "http://www.w3.org/2000/svg")
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")


@dataclass(frozen=True, slots=True)
class SvgReviewItem:
    """One titled SVG in a review gallery."""

    path: Path
    title: str
    group: str = "SVG review"
    detail: str | None = None


def _artifact_url(path: Path, gallery_dir: Path) -> str:
    """Return a browser-safe, cache-busted artifact URL."""
    resolved = path.resolve()
    try:
        relative = os.path.relpath(resolved, gallery_dir.resolve())
    except ValueError:
        url = resolved.as_uri()
    else:
        url = quote(Path(relative).as_posix(), safe="/")
    return f"{url}?v={path.stat().st_mtime_ns}"


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _review_svg_markup(path: Path) -> str:
    """Read safe inline SVG markup for lossless modal inspection."""
    try:
        root = ET.fromstring(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ET.ParseError) as exc:
        raise ValueError(f"Could not read SVG review artifact {path}: {exc}") from exc
    if _local_name(root.tag) != "svg":
        raise ValueError(f"SVG review artifact does not have an <svg> root: {path}")
    for element in root.iter():
        name = _local_name(element.tag)
        if name in _DISALLOWED_SVG_ELEMENTS:
            raise ValueError(
                f"SVG review artifact contains unsupported active element <{name}>: {path}"
            )
        for attribute in element.attrib:
            if _local_name(attribute).lower().startswith("on"):
                raise ValueError(
                    f"SVG review artifact contains an event attribute {attribute!r}: {path}"
                )
    return ET.tostring(root, encoding="unicode")


def _json_for_html(value: object) -> str:
    """Serialize data without allowing markup to terminate the JSON script node."""
    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )


def _validated_review_items(items: Iterable[SvgReviewItem]) -> list[SvgReviewItem]:
    rows = list(items)
    if not rows:
        raise ValueError("SVG review gallery requires at least one item")
    for item in rows:
        if not item.path.is_file():
            raise FileNotFoundError(item.path)
        if item.path.suffix.lower() != ".svg":
            raise ValueError(f"SVG review artifact must end in .svg: {item.path}")
    return rows


def _review_payload(
    rows: list[SvgReviewItem], gallery_dir: Path
) -> list[dict[str, str]]:
    return [
        {
            "title": item.title,
            "group": item.group,
            "detail": item.detail or "",
            "url": _artifact_url(item.path, gallery_dir),
            "svg": _review_svg_markup(item.path),
        }
        for item in rows
    ]


def _review_card(index: int, item: SvgReviewItem, url_value: str) -> str:
    url = html.escape(url_value, quote=True)
    item_title = html.escape(item.title)
    detail = (
        f'<span class="detail">{html.escape(item.detail)}</span>'
        if item.detail
        else ""
    )
    return (
        '<figure class="card">'
        f'<button class="preview" type="button" data-review-index="{index}" '
        f'aria-label="Inspect {html.escape(item.title, quote=True)}">'
        f'<img loading="lazy" src="{url}" alt="{html.escape(item.title, quote=True)}">'
        '<span class="inspect-hint">Inspect SVG</span></button>'
        '<figcaption><span class="caption-copy">'
        f"<strong>{item_title}</strong>{detail}</span>"
        f'<a href="{url}" target="_blank" rel="noopener">Open raw SVG</a>'
        "</figcaption></figure>"
    )


def _review_sections(
    rows: list[SvgReviewItem], payload: list[dict[str, str]]
) -> list[str]:
    grouped: dict[str, list[tuple[int, SvgReviewItem]]] = {}
    for index, item in enumerate(rows):
        grouped.setdefault(item.group, []).append((index, item))
    sections: list[str] = []
    for group, group_rows in grouped.items():
        cards = [
            _review_card(index, item, payload[index]["url"])
            for index, item in group_rows
        ]
        sections.append(
            f'<section><h2>{html.escape(group)}</h2><div class="gallery">'
            f"{''.join(cards)}</div></section>"
        )
    return sections


def write_svg_review_gallery(
    output: Path,
    items: Iterable[SvgReviewItem],
    *,
    title: str = "SVG review gallery",
    introduction: str = (
        "Select a preview for vector-native inspection. Drag to pan and use the "
        "mouse wheel or toolbar to zoom."
    ),
) -> Path:
    """Write an offline gallery with responsive previews and an SVG pan/zoom modal."""
    rows = _validated_review_items(items)
    target = output if output.suffix.lower() == ".html" else output / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = _review_payload(rows, target.parent)
    sections = _review_sections(rows, payload)

    vendor_js = _SVG_PAN_ZOOM.read_text(encoding="utf-8")
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
button, a {{ font: inherit; }}
main {{ width: min(100%, 1800px); margin: 0 auto; padding: clamp(18px, 3vw, 40px); }}
h1 {{ margin: 0; font-size: clamp(1.65rem, 3vw, 2.5rem); }}
.intro {{ margin: 8px 0 32px; max-width: 82ch; color: #526171; line-height: 1.5; }}
section {{ margin-top: 34px; }}
h2 {{ margin: 0 0 14px; font-size: 1.12rem; font-weight: 700; }}
.gallery {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 420px), 1fr));
  gap: 22px;
  min-width: 0;
}}
.card {{ margin: 0; min-width: 0; overflow: hidden; border: 1px solid #c7ced8;
  border-radius: 12px; background: white; box-shadow: 0 8px 24px #24364a18; }}
.preview {{ position: relative; width: 100%; height: clamp(300px, 48vh, 650px);
  padding: 24px; border: 0; min-width: 0; min-height: 0; overflow: hidden;
  display: flex; align-items: center; justify-content: center; cursor: zoom-in;
  background: #f7f8fa; }}
.preview:hover, .preview:focus-visible {{ background: #eef4fb; outline: 3px solid #2563eb;
  outline-offset: -3px; }}
.preview img {{ display: block; width: auto; height: 100%; max-width: 100%; max-height: 100%;
  min-width: 0; min-height: 0; object-fit: contain; object-position: center center; }}
.inspect-hint {{ position: absolute; right: 12px; bottom: 12px; padding: 6px 9px;
  border-radius: 999px; background: #17212bd9; color: white; font-size: .78rem; }}
figcaption {{ display: flex; justify-content: space-between; align-items: center;
  flex-wrap: wrap; gap: 8px 16px; min-width: 0; padding: 13px 16px;
  border-top: 1px solid #d8dee6; }}
.caption-copy {{ display: grid; gap: 3px; }}
.detail {{ color: #657383; font-size: .84rem; }}
a {{ color: #1557a0; }}
dialog {{ width: 100vw; height: 100vh; max-width: none; max-height: none; margin: 0;
  padding: 0; border: 0; background: #111827; color: white; }}
dialog::backdrop {{ background: #111827; }}
.viewer-shell {{ display: grid; grid-template-rows: auto minmax(0, 1fr); height: 100%; }}
.viewer-toolbar {{ display: flex; align-items: center; gap: 8px; min-width: 0;
  padding: 10px 12px; background: #111827; border-bottom: 1px solid #334155; }}
.viewer-title {{ min-width: 0; margin-right: auto; overflow: hidden; text-overflow: ellipsis;
  white-space: nowrap; font-weight: 700; }}
.viewer-toolbar button, .viewer-toolbar a {{ min-width: 40px; min-height: 38px; padding: 8px 11px;
  border: 1px solid #64748b; border-radius: 7px; background: #1e293b; color: white;
  text-align: center; text-decoration: none; cursor: pointer; }}
.viewer-toolbar button:hover, .viewer-toolbar button:focus-visible,
.viewer-toolbar a:hover, .viewer-toolbar a:focus-visible {{ background: #334155; outline: 2px solid #93c5fd; }}
.viewer-stage {{ position: relative; min-width: 0; min-height: 0; overflow: hidden;
  background-color: #eef2f6;
  background-image: linear-gradient(45deg, #d9e0e7 25%, transparent 25%),
    linear-gradient(-45deg, #d9e0e7 25%, transparent 25%),
    linear-gradient(45deg, transparent 75%, #d9e0e7 75%),
    linear-gradient(-45deg, transparent 75%, #d9e0e7 75%);
  background-size: 24px 24px; background-position: 0 0, 0 12px, 12px -12px, -12px 0; }}
.viewer-stage > svg {{ display: block; width: 100% !important; height: 100% !important;
  max-width: none !important; max-height: none !important; }}
.shortcut-help {{ color: #cbd5e1; font-size: .78rem; white-space: nowrap; }}
@media (max-width: 720px) {{
  .gallery {{ grid-template-columns: minmax(0, 1fr); }}
  .preview {{ height: 54vh; min-height: 280px; padding: 12px; }}
  .shortcut-help, .raw-link {{ display: none; }}
  .viewer-toolbar {{ gap: 5px; }}
}}
</style>
</head>
<body><main>
<h1>{html.escape(title)}</h1>
<p class="intro">{html.escape(introduction)}</p>
{"".join(sections)}
</main>
<dialog id="svg-review-dialog" aria-labelledby="svg-review-title">
  <div class="viewer-shell">
    <div class="viewer-toolbar">
      <span class="viewer-title" id="svg-review-title"></span>
      <span class="shortcut-help">Drag · wheel · +/− · 0 fit · ←/→ views</span>
      <button type="button" data-action="previous" title="Previous SVG">←</button>
      <button type="button" data-action="next" title="Next SVG">→</button>
      <button type="button" data-action="zoom-out" title="Zoom out">−</button>
      <button type="button" data-action="zoom-in" title="Zoom in">+</button>
      <button type="button" data-action="fit" title="Fit SVG">Fit</button>
      <a class="raw-link" id="svg-review-raw" target="_blank" rel="noopener">Raw</a>
      <button type="button" data-action="close" title="Close viewer">Close</button>
    </div>
    <div class="viewer-stage" id="svg-review-stage"></div>
  </div>
</dialog>
<script id="svg-review-data" type="application/json">{_json_for_html(payload)}</script>
<script>{vendor_js}</script>
<script>
(() => {{
  "use strict";
  const items = JSON.parse(document.getElementById("svg-review-data").textContent);
  const dialog = document.getElementById("svg-review-dialog");
  const stage = document.getElementById("svg-review-stage");
  const title = document.getElementById("svg-review-title");
  const raw = document.getElementById("svg-review-raw");
  let current = 0;
  let viewer = null;

  function destroyViewer() {{
    if (viewer) viewer.destroy();
    viewer = null;
    stage.replaceChildren();
  }}

  function fitViewer() {{
    if (!viewer) return;
    viewer.resize();
    viewer.fit();
    viewer.center();
  }}

  function show(index, updateHash = true) {{
    current = (index + items.length) % items.length;
    const item = items[current];
    destroyViewer();
    title.textContent = `${{item.group}} · ${{item.title}}`;
    raw.href = item.url;
    stage.innerHTML = item.svg;
    const svg = stage.querySelector("svg");
    svg.setAttribute("aria-label", item.title);
    if (!dialog.open) dialog.showModal();
    viewer = window.svgPanZoom(svg, {{
      panEnabled: true,
      zoomEnabled: true,
      dblClickZoomEnabled: true,
      mouseWheelZoomEnabled: true,
      controlIconsEnabled: false,
      fit: true,
      center: true,
      minZoom: 0.02,
      maxZoom: 100,
      zoomScaleSensitivity: 0.22
    }});
    if (updateHash) history.replaceState(null, "", `#review=${{current}}`);
    requestAnimationFrame(fitViewer);
  }}

  document.querySelectorAll("[data-review-index]").forEach((button) => {{
    button.addEventListener("click", () => show(Number(button.dataset.reviewIndex)));
  }});
  document.querySelector(".viewer-toolbar").addEventListener("click", (event) => {{
    const action = event.target.closest("[data-action]")?.dataset.action;
    if (action === "close") dialog.close();
    else if (action === "previous") show(current - 1);
    else if (action === "next") show(current + 1);
    else if (action === "zoom-in") viewer?.zoomIn();
    else if (action === "zoom-out") viewer?.zoomOut();
    else if (action === "fit") fitViewer();
  }});
  dialog.addEventListener("close", () => {{
    destroyViewer();
    history.replaceState(null, "", `${{location.pathname}}${{location.search}}`);
  }});
  window.addEventListener("resize", fitViewer);
  window.addEventListener("keydown", (event) => {{
    if (!dialog.open) return;
    if (event.key === "+" || event.key === "=") viewer?.zoomIn();
    else if (event.key === "-") viewer?.zoomOut();
    else if (event.key === "0") fitViewer();
    else if (event.key === "ArrowLeft") show(current - 1);
    else if (event.key === "ArrowRight") show(current + 1);
  }});
  const initial = location.hash.match(/^#review=(\\d+)$/);
  if (initial) show(Number(initial[1]), false);
}})();
</script>
</body>
</html>
"""
    target.write_text(page, encoding="utf-8")
    return target


__all__ = ["SvgReviewItem", "write_svg_review_gallery"]
