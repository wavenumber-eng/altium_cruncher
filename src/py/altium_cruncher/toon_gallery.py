"""Self-contained HTML gallery for Toon SVG output."""

from __future__ import annotations

from dataclasses import dataclass
import html
import os
from pathlib import Path
from urllib.parse import quote


@dataclass(frozen=True, slots=True)
class _ToonGalleryArtifact:
    """Describe one SVG emitted by the current Toon render."""

    path: Path
    project: str
    board: str
    variant: str | None
    view: str
    side: str


def _artifact_url(path: Path, gallery_dir: Path) -> str:
    """Return a browser-safe URL relative to the gallery when possible."""
    resolved = path.resolve()
    try:
        relative = os.path.relpath(resolved, gallery_dir.resolve())
    except ValueError:
        url = resolved.as_uri()
    else:
        url = quote(Path(relative).as_posix(), safe="/")
    return f"{url}?v={path.stat().st_mtime_ns}"


def write_toon_gallery(
    output_dir: Path,
    artifacts: list[_ToonGalleryArtifact],
) -> Path:
    """Write a centered, responsive gallery for the current Toon render."""
    output_dir.mkdir(parents=True, exist_ok=True)
    groups: dict[tuple[str, str, str | None], list[_ToonGalleryArtifact]] = {}
    for artifact in artifacts:
        groups.setdefault(
            (artifact.project, artifact.board, artifact.variant), []
        ).append(artifact)

    sections: list[str] = []
    for (project, board, variant), rows in groups.items():
        variant_label = variant or "Base"
        cards: list[str] = []
        for artifact in rows:
            url = html.escape(_artifact_url(artifact.path, output_dir), quote=True)
            caption = html.escape(f"{artifact.view} · {artifact.side.title()}")
            alt = html.escape(
                f"{project} / {board} / {variant_label} / {artifact.view}",
                quote=True,
            )
            cards.append(
                '<figure class="card">'
                f'<div class="preview"><img src="{url}" alt="{alt}"></div>'
                "<figcaption>"
                f'<span>{caption}</span><a href="{url}" target="_blank" '
                'rel="noopener">Open raw SVG</a>'
                "</figcaption></figure>"
            )
        heading = html.escape(f"{project} · {board} · {variant_label}")
        sections.append(
            f'<section><h2>{heading}</h2><div class="gallery">'
            f"{''.join(cards)}</div></section>"
        )

    body = "".join(sections)
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Toon SVG gallery</title>
<style>
:root {{ color-scheme: light; font-family: system-ui, sans-serif; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: #e9edf2; color: #17212b; }}
main {{ width: min(100%, 1600px); margin: 0 auto; padding: 32px; }}
h1 {{ margin: 0; font-size: clamp(1.6rem, 3vw, 2.4rem); }}
.intro {{ margin: 8px 0 32px; color: #526171; }}
section {{ margin-top: 34px; }}
h2 {{ margin: 0 0 14px; font-size: 1.1rem; font-weight: 650; }}
.gallery {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(520px, 1fr));
  gap: 22px;
  min-width: 0;
}}
.card {{ margin: 0; min-width: 0; overflow: hidden; border: 1px solid #c7ced8;
  border-radius: 12px; background: white; box-shadow: 0 8px 24px #24364a18; }}
.preview {{ height: clamp(360px, 62vh, 760px); padding: 28px;
  min-width: 0; min-height: 0; overflow: hidden; display: flex;
  align-items: center; justify-content: center;
  background: #f7f8fa; }}
.preview img {{ display: block; width: auto; height: 100%; max-width: 100%; max-height: 100%;
  min-width: 0; min-height: 0;
  object-fit: contain; object-position: center center; }}
figcaption {{ display: flex; justify-content: space-between; align-items: center;
  flex-wrap: wrap; gap: 8px 16px; min-width: 0; padding: 13px 16px;
  border-top: 1px solid #d8dee6; }}
a {{ color: #1557a0; }}
@media (max-width: 640px) {{
  main {{ padding: 18px; }}
  .gallery {{ grid-template-columns: minmax(0, 1fr); }}
  .preview {{ height: 58vh; min-height: 300px; padding: 14px; }}
}}
</style>
</head>
<body><main>
<h1>Toon SVG gallery</h1>
<p class="intro">Rendered views are centered and scaled to fit. Use browser zoom for closer inspection.</p>
{body}
</main></body>
</html>
"""
    target = output_dir / "index.html"
    target.write_text(page, encoding="utf-8")
    return target


__all__ = ["write_toon_gallery"]
