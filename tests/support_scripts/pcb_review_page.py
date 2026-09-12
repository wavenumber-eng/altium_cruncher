"""Write the single refreshable PCB review page from the current SVG artifacts."""

from __future__ import annotations

from datetime import datetime
import html
import json
import os
from pathlib import Path

OUTPUT = (
    Path(__file__).resolve().parents[2]
    / "tests/assets/projects/rt_super_c1/output/pcb-svg/illustration-review"
)


def _variant_boards(report: dict, board_output: Path, gallery_output: Path, themes: tuple[str, ...]) -> str:
    """Build only the populations listed in the latest completed review report."""
    variants = report.get("variants") or [{"variant": None, "directory": "."}]
    sections = []
    for variant in variants:
        name = variant.get("variant")
        label = str(name) if name is not None else "Base (no variant)"
        directory = board_output / variant["directory"]
        cards = []
        for theme in themes:
            for mode, mode_label in (("board", "Illustration"), ("assembly", "Illustrated assembly")):
                for side in ("top", "bottom"):
                    path = directory / f"{side}-{mode}-{theme}.svg"
                    if not path.exists():
                        continue
                    relative = Path(os.path.relpath(path, gallery_output)).as_posix()
                    url = html.escape(f"{relative}?v={path.stat().st_mtime_ns}")
                    caption = html.escape(f"{mode_label} / {side.title()}")
                    cards.append(f'<figure><a href="{url}"><img loading="lazy" src="{url}" alt="{html.escape(label)} / {caption}"></a>'
                                 f'<figcaption>{caption}</figcaption></figure>')
        sections.append(f'<article data-variant="{html.escape(label)}"><h3>{html.escape(label)}</h3>'
                        f'<div class="boards">{"".join(cards)}</div></article>')
    return "".join(sections)


def write_review_page(output: Path = OUTPUT) -> Path:
    """Show only complete board previews in the fixed internal review gallery."""
    projects = Path(__file__).resolve().parents[2] / "tests/assets/projects"
    reports = sorted(projects.glob("*/output/pcb-svg/illustration-review/board-report.json"))
    reports.sort(key=lambda p: p.parent.resolve() != output.resolve())
    navigation = []
    sections = []
    for report_path in reports:
        report = json.loads(report_path.read_text(encoding="utf-8"))
        project = report_path.parents[3].name
        title = "RT_SUPER_C1" if project == "rt_super_c1" else project.replace("_", " ").title()
        anchor = "board-" + project
        navigation.append(f'<a href="#{html.escape(anchor)}">{html.escape(title)}</a>')
        theme = report.get("theme", "green")
        if theme == "all":
            theme = "saved" if project == "rt_super_c1" else "green"
        boards = _variant_boards(report, report_path.parent, output, (theme,))
        sections.append(f'<section id="{html.escape(anchor)}"><h2>{html.escape(title)}</h2>'
                        f'{boards}</section>')
    updated = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    page = f'''<!doctype html><html lang="en"><meta charset="utf-8"><title>PCB board review</title>
<style>body{{font:16px system-ui;background:#edf0f3;color:#172536;margin:28px}}h1{{font-size:25px}}h2{{font-size:20px}}
.boards{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}figure{{margin:0;background:#d3d9de;padding:20px;border-radius:8px}}
img{{width:100%;height:540px;object-fit:contain}}figcaption{{line-height:1.5;margin-top:10px}}a{{color:#144b93}}
.updated{{color:#526171;font-size:14px}}section{{margin-top:32px}}nav{{display:flex;gap:20px;flex-wrap:wrap}}</style>
<h1>PCB board review</h1><p>Refresh for the latest views. Click a board to open its SVG. Bottom views are seen from underneath.</p>
<nav>{"".join(navigation)}</nav><p class="updated">Updated {html.escape(updated)}</p>
{"".join(sections)}</html>'''
    target = output / "index.html"
    target.write_text(page, encoding="utf-8")
    redirect = '<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=index.html"><a href="index.html">PCB review</a>'
    for filename in ("film-review.html", "holes-review.html"):
        old = output / filename
        if old.exists():
            old.write_text(redirect, encoding="utf-8")
    return target


def write_standalone_review_page(output: Path) -> Path:
    """Keep an external board in its own refreshable review page."""
    report = json.loads((output / "board-report.json").read_text(encoding="utf-8"))
    title = html.escape(Path(report["source"]).stem)
    themes = ("saved", "green") if report["theme"] == "all" else (report["theme"],)
    boards = _variant_boards(report, output, output, tuple(themes))
    omitted = [warning for warning in report["warnings"] if "omitted" in warning]
    notes = "<p>" + html.escape(" ".join(omitted)) + "</p>" if omitted else ""
    notes += "".join(f"<p>{html.escape(note)}</p>" for note in report.get("review_notes", []))
    for side, result in report["sides"].items():
        if result.get("error"):
            notes += f'<p><strong>{side.capitalize()} illustration incomplete:</strong> {html.escape(result["error"])}</p>'
    updated = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    page = f'''<!doctype html><html lang="en"><meta charset="utf-8"><title>{title} preview review</title>
<style>body{{font:16px system-ui;background:#edf0f3;color:#172536;margin:28px}}h1{{font-size:25px}}p{{line-height:1.5}}
.boards{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}figure{{margin:0;background:#d3d9de;padding:20px;border-radius:8px}}
img{{width:100%;height:700px;object-fit:contain}}figcaption{{line-height:1.5;margin-top:10px}}a{{color:#144b93}}.updated{{color:#526171;font-size:14px}}</style>
<h1>{title} preview review</h1><p>Keep this page open and refresh for the latest render. Click either view to open its SVG.</p>
<p class="updated">Updated {html.escape(updated)}</p>{boards}
{notes}<p><a href="board-report.json">Render report</a></p></html>'''
    target = output / "index.html"
    target.write_text(page, encoding="utf-8")
    return target


if __name__ == "__main__":
    print(write_review_page())
