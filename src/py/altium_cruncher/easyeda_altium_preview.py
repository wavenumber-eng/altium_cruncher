"""Preview SVG helpers for EasyEDA to Altium import review."""

from __future__ import annotations

import base64
import html
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from easyeda_monkey.easyeda_symbol import EasyEdaSymbol


_PATH_TOKEN_RE = re.compile(
    r"[AaCcHhLlMmQqSsTtVvZz]|[-+]?(?:\d+\.\d+|\d+|\.\d+)(?:[eE][-+]?\d+)?"
)
_SVG_DIM_RE = re.compile(r"<svg\b[^>]*?(?:width=\"([0-9.]+)\"[^>]*height=\"([0-9.]+)\")", re.I)
_SVG_VIEWBOX_RE = re.compile(r"<svg\b[^>]*?viewBox=\"([^\"]+)\"", re.I)

_FOOTPRINT_LAYER_MAPPINGS: tuple[tuple[str, str, str, str], ...] = (
    ("1", "Top copper", "TOP", "Pads and top copper graphics"),
    ("2", "Bottom copper", "BOTTOM", "Bottom copper pads/graphics"),
    ("3", "Top silkscreen", "TOPOVERLAY", "Visible top overlay/silkscreen"),
    ("4", "Bottom silkscreen", "BOTTOMOVERLAY", "Visible bottom overlay/silkscreen"),
    ("5", "Top paste", "TOPPASTE", "Paste openings and source paste regions"),
    ("6", "Bottom paste", "BOTTOMPASTE", "Bottom paste openings"),
    ("7", "Top solder mask", "TOPSOLDER", "Top solder-mask openings"),
    ("8", "Bottom solder mask", "BOTTOMSOLDER", "Bottom solder-mask openings"),
    ("10", "Board outline", "MECHANICAL1", "Outline/document geometry"),
    ("11", "Multi-layer pads", "MULTILAYER", "Through-hole and multi-layer pad source"),
    ("12", "Document", "MECHANICAL1", "Non-fabrication reference geometry"),
    ("13", "Component shape", "MECHANICAL13", "Body/courtyard style source regions"),
    ("14", "Lead shape", "MECHANICAL14", "Lead/contact reference regions"),
    ("15", "Polarity", "MECHANICAL1", "Polarity/reference graphics"),
    ("99", "Board outline", "MECHANICAL13", "EasyEDA board-outline solid regions"),
    ("100", "Component shape", "MECHANICAL14", "EasyEDA component-shape solid regions"),
    ("101", "Top silkscreen", "TOPOVERLAY", "Alternate EasyEDA top-silk layer"),
    ("DRILLS", "Drills", "DRILLS", "Synthetic review-only drill layer"),
)
_FOOTPRINT_LAYER_MAPPING_BY_SOURCE = {
    source_id: (source_name, altium_name)
    for source_id, source_name, altium_name, _notes in _FOOTPRINT_LAYER_MAPPINGS
}


@dataclass(frozen=True)
class EasyEdaPreviewArtifacts:
    """Preview files emitted by `easyeda-import --preview`."""

    easyeda_source_svg: Path
    compare_svg: Path


@dataclass(frozen=True)
class EasyEdaReviewRow:
    """One row in the batch EasyEDA/Altium schematic review."""

    part_id: str
    symbol_name: str
    source_name: str
    easyeda_svg: "_SvgDocument"
    altium_svg: "_SvgDocument"
    pin_count: int = 0
    rectangle_count: int = 0
    circle_count: int = 0
    ellipse_count: int = 0
    polyline_count: int = 0
    polygon_count: int = 0
    unsupported_count: int = 0
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class EasyEdaFootprintReviewRow:
    """One row in the batch EasyEDA/Altium footprint review."""

    part_id: str
    footprint_name: str
    source_name: str
    easyeda_svg: "_SvgDocument"
    altium_svg: "_SvgDocument"
    source_pad_count: int = 0
    generated_pad_count: int = 0
    generated_hole_pad_count: int = 0
    custom_pad_count: int = 0
    slotted_pad_count: int = 0
    track_segment_count: int = 0
    circle_count: int = 0
    arc_count: int = 0
    region_count: int = 0
    unsupported_count: int = 0
    warnings: tuple[str, ...] = ()
    source_layers: tuple[tuple[str, int], ...] = ()


@dataclass(frozen=True)
class EasyEdaReviewArtifacts:
    """Batch review files emitted by `easyeda-review`."""

    html: Path
    svg: Path


@dataclass(frozen=True)
class _SvgDocument:
    content: str
    width: float
    height: float


def write_easyeda_symbol_preview_artifacts(
    *,
    easyeda_symbol: EasyEdaSymbol,
    altium_svg_content: str,
    output_dir: Path,
    symbol_name: str,
) -> EasyEdaPreviewArtifacts:
    """Write EasyEDA source and side-by-side/overlay comparison SVGs."""

    output_dir.mkdir(parents=True, exist_ok=True)
    easyeda_svg = render_easyeda_symbol_svg(easyeda_symbol)
    easyeda_path = output_dir / "easyeda-source.svg"
    easyeda_path.write_text(easyeda_svg.content, encoding="utf-8")

    altium_svg = _svg_document_from_content(altium_svg_content)
    compare_svg = render_compare_svg(
        easyeda_svg=easyeda_svg,
        altium_svg=altium_svg,
        symbol_name=symbol_name,
    )
    compare_path = output_dir / "compare.svg"
    compare_path.write_text(compare_svg, encoding="utf-8")

    return EasyEdaPreviewArtifacts(
        easyeda_source_svg=easyeda_path,
        compare_svg=compare_path,
    )


def render_altium_library_preview_svgs(
    *,
    library: Any,
    output_dir: Path,
    background: str = "none",
    pin_text_follows_orientation: bool = False,
) -> dict[str, dict[int, str]]:
    """Render SchLib preview SVGs, optionally honoring custom pin text orientation."""

    output_dir.mkdir(parents=True, exist_ok=True)
    results: dict[str, dict[int, str]] = {}
    for symbol in library.symbols:
        part_count = getattr(symbol, "part_count", 1) or 1
        results[symbol.name] = {}
        for part_id in range(1, part_count + 1):
            svg = library.symbol_to_svg(
                symbol.name,
                background=background,
                part_id=part_id if part_count > 1 else None,
                pin_text_follows_orientation=pin_text_follows_orientation,
            )
            results[symbol.name][part_id] = svg
            suffix = f"_part{part_id}" if part_count > 1 else ""
            (output_dir / f"{symbol.name}{suffix}_ir.svg").write_text(
                svg,
                encoding="utf-8",
            )
    return results


def make_easyeda_review_row(
    *,
    part_id: str,
    easyeda_symbol: EasyEdaSymbol,
    altium_svg_content: str,
    symbol_name: str,
    source_name: str,
    report: Any | None = None,
) -> EasyEdaReviewRow:
    """Create one row of source/generated schematic review content."""

    report_dict = report.to_dict() if hasattr(report, "to_dict") else {}
    return EasyEdaReviewRow(
        part_id=part_id,
        symbol_name=symbol_name,
        source_name=source_name,
        easyeda_svg=render_easyeda_symbol_svg(easyeda_symbol),
        altium_svg=_svg_document_from_content(altium_svg_content),
        pin_count=int(report_dict.get("pin_count") or 0),
        rectangle_count=int(report_dict.get("rectangle_count") or 0),
        circle_count=int(report_dict.get("circle_count") or 0),
        ellipse_count=int(report_dict.get("ellipse_count") or 0),
        polyline_count=int(report_dict.get("polyline_count") or 0),
        polygon_count=int(report_dict.get("polygon_count") or 0),
        unsupported_count=int(report_dict.get("unsupported_count") or 0),
        warnings=tuple(str(item) for item in report_dict.get("warnings", [])),
    )


def make_easyeda_footprint_review_row(
    *,
    part_id: str,
    easyeda_svg_content: str,
    altium_svg_content: str,
    footprint_name: str,
    source_name: str,
    report: Any | None = None,
) -> EasyEdaFootprintReviewRow:
    """Create one row of source/generated footprint review content."""

    report_dict = report.to_dict() if hasattr(report, "to_dict") else {}
    return EasyEdaFootprintReviewRow(
        part_id=part_id,
        footprint_name=footprint_name,
        source_name=source_name,
        easyeda_svg=_svg_document_from_content(easyeda_svg_content),
        altium_svg=_svg_document_from_content(altium_svg_content),
        source_pad_count=int(report_dict.get("source_pad_count") or 0),
        generated_pad_count=int(report_dict.get("generated_pad_count") or 0),
        generated_hole_pad_count=int(report_dict.get("generated_hole_pad_count") or 0),
        custom_pad_count=int(report_dict.get("custom_pad_count") or 0),
        slotted_pad_count=int(report_dict.get("slotted_pad_count") or 0),
        track_segment_count=int(report_dict.get("track_segment_count") or 0),
        circle_count=int(report_dict.get("circle_count") or 0),
        arc_count=int(report_dict.get("arc_count") or 0),
        region_count=int(report_dict.get("region_count") or 0),
        unsupported_count=int(report_dict.get("unsupported_count") or 0),
        warnings=tuple(str(item) for item in report_dict.get("warnings", [])),
        source_layers=tuple(
            (str(key), int(value))
            for key, value in sorted(
                (report_dict.get("layers") or {}).items(),
                key=lambda item: _source_layer_sort_key(str(item[0])),
            )
        ),
    )


def write_easyeda_review_artifacts(
    *,
    rows: list[EasyEdaReviewRow],
    output_dir: Path,
    title: str = "EasyEDA to Altium Schematic Review",
) -> EasyEdaReviewArtifacts:
    """Write self-contained batch review HTML and SVG files."""

    output_dir.mkdir(parents=True, exist_ok=True)
    svg_path = output_dir / "review.svg"
    html_path = output_dir / "review.html"
    svg_path.write_text(
        render_easyeda_review_svg(rows=rows, title=title),
        encoding="utf-8",
    )
    html_path.write_text(
        render_easyeda_review_html(rows=rows, title=title),
        encoding="utf-8",
    )
    return EasyEdaReviewArtifacts(html=html_path, svg=svg_path)


def write_easyeda_footprint_review_artifacts(
    *,
    rows: list[EasyEdaFootprintReviewRow],
    output_dir: Path,
    title: str = "EasyEDA to Altium Footprint Review",
) -> EasyEdaReviewArtifacts:
    """Write self-contained batch footprint review HTML and SVG files."""

    output_dir.mkdir(parents=True, exist_ok=True)
    svg_path = output_dir / "review.svg"
    html_path = output_dir / "review.html"
    svg_path.write_text(
        render_easyeda_footprint_review_svg(rows=rows, title=title),
        encoding="utf-8",
    )
    html_path.write_text(
        render_easyeda_footprint_review_html(rows=rows, title=title),
        encoding="utf-8",
    )
    return EasyEdaReviewArtifacts(html=html_path, svg=svg_path)


def render_easyeda_review_svg(
    *,
    rows: list[EasyEdaReviewRow],
    title: str = "EasyEDA to Altium Schematic Review",
) -> str:
    """Render one long SVG with EasyEDA left and Altium right per row."""

    page_w = 1240.0
    margin = 24.0
    header_h = 56.0
    row_h = 360.0
    row_gap = 14.0
    panel_gap = 18.0
    panel_w = (page_w - (margin * 2) - panel_gap) / 2.0
    image_w = panel_w - 24.0
    image_h = 266.0
    total_h = header_h + margin + (len(rows) * row_h) + max(len(rows) - 1, 0) * row_gap

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{_fmt(page_w)}" height="{_fmt(total_h)}" '
            f'viewBox="0 0 {_fmt(page_w)} {_fmt(total_h)}" '
            'data-doc-id="easyeda-altium-review">'
        ),
        '<rect x="0" y="0" width="100%" height="100%" fill="#F5F6F8"/>',
        (
            f'<text x="{_fmt(margin)}" y="35" font-family="Arial, sans-serif" '
            f'font-size="22" font-weight="700" fill="#101828">{_text(title)}</text>'
        ),
        (
            f'<text x="{_fmt(page_w - margin)}" y="35" text-anchor="end" '
            'font-family="Arial, sans-serif" font-size="13" fill="#475467">'
            f'{len(rows)} cases</text>'
        ),
    ]

    y = header_h
    for index, row in enumerate(rows, start=1):
        lines.append(
            _review_svg_row(
                row=row,
                index=index,
                x=margin,
                y=y,
                row_w=page_w - (margin * 2),
                row_h=row_h,
                panel_w=panel_w,
                panel_gap=panel_gap,
                image_w=image_w,
                image_h=image_h,
            )
        )
        y += row_h + row_gap

    lines.append("</svg>")
    return "\n".join(lines)


def render_easyeda_footprint_review_svg(
    *,
    rows: list[EasyEdaFootprintReviewRow],
    title: str = "EasyEDA to Altium Footprint Review",
) -> str:
    """Render one long SVG with EasyEDA footprint source and Altium output."""

    page_w = 1240.0
    margin = 24.0
    header_h = 56.0
    row_h = 360.0
    row_gap = 14.0
    panel_gap = 18.0
    panel_w = (page_w - (margin * 2) - panel_gap) / 2.0
    image_w = panel_w - 24.0
    image_h = 266.0
    total_h = header_h + margin + (len(rows) * row_h) + max(len(rows) - 1, 0) * row_gap

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{_fmt(page_w)}" height="{_fmt(total_h)}" '
            f'viewBox="0 0 {_fmt(page_w)} {_fmt(total_h)}" '
            'data-doc-id="easyeda-altium-footprint-review">'
        ),
        '<rect x="0" y="0" width="100%" height="100%" fill="#F5F6F8"/>',
        (
            f'<text x="{_fmt(margin)}" y="35" font-family="Arial, sans-serif" '
            f'font-size="22" font-weight="700" fill="#101828">{_text(title)}</text>'
        ),
        (
            f'<text x="{_fmt(page_w - margin)}" y="35" text-anchor="end" '
            'font-family="Arial, sans-serif" font-size="13" fill="#475467">'
            f'{len(rows)} cases</text>'
        ),
    ]

    y = header_h
    for index, row in enumerate(rows, start=1):
        lines.append(
            _footprint_review_svg_row(
                row=row,
                index=index,
                x=margin,
                y=y,
                row_w=page_w - (margin * 2),
                row_h=row_h,
                panel_w=panel_w,
                panel_gap=panel_gap,
                image_w=image_w,
                image_h=image_h,
            )
        )
        y += row_h + row_gap

    lines.append("</svg>")
    return "\n".join(lines)


def render_easyeda_review_html(
    *,
    rows: list[EasyEdaReviewRow],
    title: str = "EasyEDA to Altium Schematic Review",
) -> str:
    """Render a self-contained HTML table for schematic visual review."""

    row_markup = "\n".join(_review_html_row(index, row) for index, row in enumerate(rows, start=1))
    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f"<title>{_text(title)}</title>",
            "<style>",
            "body{margin:0;background:#f5f6f8;color:#101828;font-family:Arial,sans-serif;}",
            "header{position:sticky;top:0;z-index:2;background:#fff;border-bottom:1px solid #d0d5dd;padding:14px 18px;}",
            "h1{font-size:20px;line-height:1.2;margin:0 0 4px 0;}",
            ".meta{font-size:13px;color:#667085;}",
            "main{padding:18px;}",
            ".row{background:#fff;border:1px solid #d0d5dd;border-radius:6px;margin:0 0 14px 0;overflow:hidden;}",
            ".row-head{display:flex;gap:12px;align-items:baseline;padding:10px 12px;border-bottom:1px solid #eaecf0;}",
            ".row-head strong{font-size:15px;}",
            ".row-head span{font-size:12px;color:#667085;}",
            ".panels{display:grid;grid-template-columns:1fr 1fr;gap:0;border-bottom:1px solid #eaecf0;}",
            ".panel{padding:10px 12px;border-right:1px solid #eaecf0;}",
            ".panel:last-child{border-right:0;}",
            ".panel-title{font-size:12px;color:#475467;margin:0 0 8px 0;}",
            ".viewport{height:300px;border:1px solid #eaecf0;background:#fff;display:flex;align-items:center;justify-content:center;}",
            ".viewport img{max-width:100%;max-height:100%;object-fit:contain;}",
            ".summary{font-size:12px;color:#475467;padding:8px 12px;}",
            ".warn{color:#b42318;}",
            "@media(max-width:800px){.panels{grid-template-columns:1fr}.panel{border-right:0;border-bottom:1px solid #eaecf0}.viewport{height:240px}}",
            "</style>",
            "</head>",
            "<body>",
            "<header>",
            f"<h1>{_text(title)}</h1>",
            f'<div class="meta">{len(rows)} cases, EasyEDA source on left, generated Altium on right</div>',
            "</header>",
            "<main>",
            row_markup,
            "</main>",
            "</body>",
            "</html>",
        ]
    )


def render_easyeda_footprint_review_html(
    *,
    rows: list[EasyEdaFootprintReviewRow],
    title: str = "EasyEDA to Altium Footprint Review",
) -> str:
    """Render a self-contained HTML table for footprint visual review."""

    row_markup = "\n".join(
        _footprint_review_html_row(index, row) for index, row in enumerate(rows, start=1)
    )
    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f"<title>{_text(title)}</title>",
            "<style>",
            _footprint_review_css(),
            "</style>",
            "</head>",
            "<body>",
            "<header>",
            f"<h1>{_text(title)}</h1>",
            f'<div class="meta">{len(rows)} cases, EasyEDA source on left, generated Altium on right</div>',
            _footprint_layer_key_html(),
            _footprint_layer_mapping_html(),
            '<div class="global-layer-controls" data-global-layer-controls></div>',
            "</header>",
            "<main>",
            row_markup,
            "</main>",
            _footprint_review_script(),
            "</body>",
            "</html>",
        ]
    )


def _footprint_review_css() -> str:
    return "\n".join(
        [
            "body{margin:0;background:#f5f6f8;color:#101828;font-family:Arial,sans-serif;}",
            "header{position:sticky;top:0;z-index:2;background:#fff;border-bottom:1px solid #d0d5dd;padding:14px 18px;}",
            "h1{font-size:20px;line-height:1.2;margin:0 0 4px 0;}",
            ".meta{font-size:13px;color:#667085;}",
            ".layer-key{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center;margin-top:10px;font-size:12px;color:#475467;}",
            ".key-title{font-weight:700;color:#344054;}",
            ".key-item{display:inline-flex;align-items:center;gap:5px;white-space:nowrap;}",
            ".swatch{display:inline-block;width:11px;height:11px;border:1px solid #98a2b3;border-radius:2px;}",
            "details.mapping{margin-top:10px;font-size:12px;color:#344054;}",
            "details.mapping summary{cursor:pointer;font-weight:700;}",
            ".mapping-table{border-collapse:collapse;margin-top:8px;max-width:980px;background:#fff;}",
            ".mapping-table th,.mapping-table td{border:1px solid #d0d5dd;padding:5px 7px;text-align:left;vertical-align:top;}",
            ".mapping-table th{background:#f2f4f7;color:#344054;}",
            ".global-layer-controls{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px;padding-top:10px;border-top:1px solid #eaecf0;}",
            ".global-layer-controls:empty{display:none;}",
            "main{padding:18px;}",
            ".row{background:#fff;border:1px solid #d0d5dd;border-radius:6px;margin:0 0 14px 0;overflow:hidden;}",
            ".row-head{display:flex;gap:12px;align-items:baseline;padding:10px 12px;border-bottom:1px solid #eaecf0;}",
            ".row-head strong{font-size:15px;}",
            ".row-head span{font-size:12px;color:#667085;}",
            ".panels{display:grid;grid-template-columns:1fr 1fr;gap:0;border-bottom:1px solid #eaecf0;}",
            ".panel{padding:10px 12px;border-right:1px solid #eaecf0;min-width:0;}",
            ".panel:last-child{border-right:0;}",
            ".panel-title{font-size:12px;color:#475467;margin:0 0 8px 0;}",
            ".viewer-toolbar{display:flex;align-items:center;gap:6px;margin-bottom:6px;}",
            ".viewer-toolbar button{border:1px solid #d0d5dd;background:#fff;border-radius:4px;color:#344054;font-size:12px;line-height:1;padding:5px 8px;cursor:pointer;}",
            ".viewer-toolbar button:hover{background:#f2f4f7;}",
            ".viewer-toolbar .scale{margin-left:auto;font-size:12px;color:#667085;font-variant-numeric:tabular-nums;}",
            ".viewport{height:420px;border:1px solid #eaecf0;background:#fff;display:flex;align-items:center;justify-content:center;}",
            ".svg-viewport{overflow:hidden;touch-action:none;position:relative;cursor:grab;}",
            ".svg-viewport.dragging{cursor:grabbing;}",
            ".svg-host{width:100%;height:100%;display:flex;align-items:center;justify-content:center;transform-origin:center center;will-change:transform;}",
            ".svg-host svg{width:100%;height:100%;display:block;max-width:none;max-height:none;}",
            ".layer-controls{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;max-height:84px;overflow:auto;}",
            ".layer-chip{display:inline-flex;align-items:center;gap:5px;border:1px solid #d0d5dd;border-radius:4px;padding:3px 6px;font-size:11px;color:#344054;background:#fff;}",
            ".layer-chip input{margin:0;}",
            ".layer-chip .count{color:#98a2b3;}",
            ".summary{font-size:12px;color:#475467;padding:8px 12px;}",
            ".mapping-line{font-size:12px;color:#475467;padding:0 12px 10px 12px;}",
            ".mapping-line strong{color:#344054;}",
            ".mapping-pill{display:inline-block;border:1px solid #d0d5dd;border-radius:4px;background:#fff;padding:2px 5px;margin:2px 3px 2px 0;}",
            ".warn{color:#b42318;}",
            "@media(max-width:900px){.panels{grid-template-columns:1fr}.panel{border-right:0;border-bottom:1px solid #eaecf0}.viewport{height:320px}}",
        ]
    )


def _footprint_layer_key_html() -> str:
    items = [
        ("#C87932", "EasyEDA copper / SMD pads"),
        ("#D8D8D8", "EasyEDA multi-layer pads"),
        ("#F3D547", "EasyEDA source graphics"),
        ("#FF0000", "Altium top copper"),
        ("#FFFF00", "Altium overlay / silk"),
        ("#808080", "Altium paste / mechanical"),
        ("#800080", "Altium solder mask"),
        ("#FF8000", "Altium mechanical"),
        ("#FFFFFF", "Drills / holes"),
    ]
    lines = ['<div class="layer-key">', '<span class="key-title">Color key</span>']
    for color, label in items:
        border = "border-color:#667085;" if color == "#FFFFFF" else ""
        lines.append(
            '<span class="key-item">'
            f'<span class="swatch" style="background:{_attr(color)};{border}"></span>'
            f'{_text(label)}</span>'
        )
    lines.append("</div>")
    return "\n".join(lines)


def _footprint_layer_mapping_html() -> str:
    lines = [
        '<details class="mapping" open>',
        "<summary>Import layer mapping</summary>",
        '<table class="mapping-table">',
        "<thead><tr><th>EasyEDA source</th><th>Altium output</th><th>Notes</th></tr></thead>",
        "<tbody>",
    ]
    for source_id, source_name, altium_name, notes in _FOOTPRINT_LAYER_MAPPINGS:
        lines.append(
            "<tr>"
            f"<td>{_text(source_id)} - {_text(source_name)}</td>"
            f"<td>{_text(altium_name)}</td>"
            f"<td>{_text(notes)}</td>"
            "</tr>"
        )
    lines.extend(["</tbody>", "</table>", "</details>"])
    return "\n".join(lines)


def _footprint_review_script() -> str:
    return r"""<script>
(function () {
  var layerRegistry = new Map();
  var globalLayerState = new Map();

  function decodeBase64Utf8(value) {
    var binary = atob(value || "");
    var bytes = new Uint8Array(binary.length);
    for (var index = 0; index < binary.length; index += 1) {
      bytes[index] = binary.charCodeAt(index);
    }
    if (window.TextDecoder) {
      return new TextDecoder("utf-8").decode(bytes);
    }
    var text = "";
    for (var byteIndex = 0; byteIndex < bytes.length; byteIndex += 1) {
      text += String.fromCharCode(bytes[byteIndex]);
    }
    return decodeURIComponent(escape(text));
  }

  function paintColor(element) {
    var color = element.getAttribute("data-color") ||
      element.getAttribute("fill") ||
      element.getAttribute("stroke");
    if (color && color !== "none") {
      return color;
    }
    var painted = element.querySelector("[data-color],[fill],[stroke]");
    if (!painted) {
      return "#98A2B3";
    }
    return painted.getAttribute("data-color") ||
      painted.getAttribute("fill") ||
      painted.getAttribute("stroke") ||
      "#98A2B3";
  }

  function layerElements(svg, layerName) {
    return Array.prototype.filter.call(
      layerNodes(svg),
      function (element) {
        return element.getAttribute("data-layer-name") === layerName;
      }
    );
  }

  function layerNodes(svg) {
    var scene = svg.querySelector("#scene");
    if (scene) {
      return Array.prototype.filter.call(scene.children, function (element) {
        return element.hasAttribute("data-layer-name");
      });
    }
    return svg.querySelectorAll("[data-layer-name]");
  }

  function collectLayers(svg) {
    var layers = new Map();
    Array.prototype.forEach.call(layerNodes(svg), function (element) {
      var name = element.getAttribute("data-layer-name");
      if (!name) {
        return;
      }
      var entry = layers.get(name);
      if (!entry) {
        entry = {
          name: name,
          display: element.getAttribute("data-layer-display-name") || name,
          color: paintColor(element),
          count: 0
        };
        layers.set(name, entry);
      }
      var primitiveCount = Number(element.getAttribute("data-primitive-count") || 0);
      if (primitiveCount) {
        entry.count = Math.max(entry.count, primitiveCount);
      } else if (!element.querySelector("[data-layer-name]")) {
        entry.count += 1;
      }
    });
    return Array.from(layers.values()).sort(function (left, right) {
      return left.display.localeCompare(right.display);
    });
  }

  function renderLayerControls(viewer, svg) {
    var controls = viewer.querySelector("[data-layer-controls]");
    var layers = collectLayers(svg);
    if (!controls || !layers.length) {
      return;
    }
    layers.forEach(function (layer) {
      registerGlobalLayer(layer);
      var label = document.createElement("label");
      label.className = "layer-chip";

      var input = document.createElement("input");
      input.type = "checkbox";
      input.setAttribute("data-layer-toggle", layer.name);
      input.checked = true;
      input.addEventListener("change", function () {
        layerElements(svg, layer.name).forEach(function (element) {
          element.style.display = input.checked ? "" : "none";
        });
      });
      if (globalLayerState.has(layer.name)) {
        input.checked = globalLayerState.get(layer.name);
        layerElements(svg, layer.name).forEach(function (element) {
          element.style.display = input.checked ? "" : "none";
        });
      }

      var swatch = document.createElement("span");
      swatch.className = "swatch";
      swatch.style.background = layer.color || "#98A2B3";
      if ((layer.color || "").toUpperCase() === "#FFFFFF") {
        swatch.style.borderColor = "#667085";
      }

      var text = document.createElement("span");
      text.textContent = layer.display;

      label.appendChild(input);
      label.appendChild(swatch);
      label.appendChild(text);
      if (layer.count) {
        var count = document.createElement("span");
        count.className = "count";
        count.textContent = String(layer.count);
        label.appendChild(count);
      }
      controls.appendChild(label);
    });
  }

  function registerGlobalLayer(layer) {
    var existing = layerRegistry.get(layer.name);
    if (existing) {
      existing.count += layer.count || 0;
      return;
    }
    layerRegistry.set(layer.name, {
      name: layer.name,
      display: layer.display,
      color: layer.color,
      count: layer.count || 0
    });
    if (!globalLayerState.has(layer.name)) {
      globalLayerState.set(layer.name, true);
    }
  }

  function setLayerVisible(layerName, visible) {
    globalLayerState.set(layerName, visible);
    document.querySelectorAll("[data-svg-viewer]").forEach(function (viewer) {
      var svg = viewer.querySelector(".svg-host svg");
      if (!svg) {
        return;
      }
      layerElements(svg, layerName).forEach(function (element) {
        element.style.display = visible ? "" : "none";
      });
      viewer.querySelectorAll("input[data-layer-toggle]").forEach(function (input) {
        if (input.getAttribute("data-layer-toggle") !== layerName) {
          return;
        }
        input.checked = visible;
      });
    });
  }

  function renderGlobalLayerControls() {
    var container = document.querySelector("[data-global-layer-controls]");
    if (!container) {
      return;
    }
    container.innerHTML = "";
    var title = document.createElement("span");
    title.className = "key-title";
    title.textContent = "Global layers";
    container.appendChild(title);

    Array.from(layerRegistry.values()).sort(function (left, right) {
      return left.display.localeCompare(right.display);
    }).forEach(function (layer) {
      var label = document.createElement("label");
      label.className = "layer-chip";

      var input = document.createElement("input");
      input.type = "checkbox";
      input.checked = globalLayerState.get(layer.name) !== false;
      input.addEventListener("change", function () {
        setLayerVisible(layer.name, input.checked);
      });

      var swatch = document.createElement("span");
      swatch.className = "swatch";
      swatch.style.background = layer.color || "#98A2B3";
      if ((layer.color || "").toUpperCase() === "#FFFFFF") {
        swatch.style.borderColor = "#667085";
      }

      var text = document.createElement("span");
      text.textContent = layer.display;

      label.appendChild(input);
      label.appendChild(swatch);
      label.appendChild(text);
      if (layer.count) {
        var count = document.createElement("span");
        count.className = "count";
        count.textContent = String(layer.count);
        label.appendChild(count);
      }
      container.appendChild(label);
    });
  }

  function initViewer(viewer) {
    var host = viewer.querySelector(".svg-host");
    var viewport = viewer.querySelector(".svg-viewport");
    var scaleLabel = viewer.querySelector("[data-scale]");
    if (!host || !viewport) {
      return;
    }
    host.innerHTML = decodeBase64Utf8(host.getAttribute("data-svg-b64"));
    var svg = host.querySelector("svg");
    if (!svg) {
      return;
    }
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", "100%");
    svg.setAttribute("preserveAspectRatio", "xMidYMid meet");

    var state = {scale: 1, x: 0, y: 0};
    var dragging = false;
    var dragStart = {x: 0, y: 0, tx: 0, ty: 0};

    function applyTransform() {
      host.style.transform = "translate(" + state.x + "px," + state.y + "px) scale(" + state.scale + ")";
      if (scaleLabel) {
        scaleLabel.textContent = Math.round(state.scale * 100) + "%";
      }
    }

    function zoom(multiplier) {
      state.scale = Math.min(24, Math.max(0.1, state.scale * multiplier));
      applyTransform();
    }

    viewer.querySelector('[data-action="zoom-in"]').addEventListener("click", function () {
      zoom(1.25);
    });
    viewer.querySelector('[data-action="zoom-out"]').addEventListener("click", function () {
      zoom(0.8);
    });
    viewer.querySelector('[data-action="fit"]').addEventListener("click", function () {
      state = {scale: 1, x: 0, y: 0};
      applyTransform();
    });
    viewport.addEventListener("wheel", function (event) {
      event.preventDefault();
      zoom(event.deltaY < 0 ? 1.12 : 0.89);
    }, {passive: false});
    viewport.addEventListener("pointerdown", function (event) {
      dragging = true;
      viewport.classList.add("dragging");
      viewport.setPointerCapture(event.pointerId);
      dragStart = {x: event.clientX, y: event.clientY, tx: state.x, ty: state.y};
    });
    viewport.addEventListener("pointermove", function (event) {
      if (!dragging) {
        return;
      }
      state.x = dragStart.tx + event.clientX - dragStart.x;
      state.y = dragStart.ty + event.clientY - dragStart.y;
      applyTransform();
    });
    viewport.addEventListener("pointerup", function (event) {
      dragging = false;
      viewport.classList.remove("dragging");
      viewport.releasePointerCapture(event.pointerId);
    });
    viewport.addEventListener("pointercancel", function () {
      dragging = false;
      viewport.classList.remove("dragging");
    });
    viewport.addEventListener("dblclick", function () {
      state = {scale: 1, x: 0, y: 0};
      applyTransform();
    });

    renderLayerControls(viewer, svg);
    applyTransform();
  }

  document.querySelectorAll("[data-svg-viewer]").forEach(initViewer);
  renderGlobalLayerControls();
}());
</script>"""


def render_easyeda_symbol_svg(easyeda_symbol: EasyEdaSymbol) -> _SvgDocument:
    """Render a lightweight EasyEDA source symbol SVG from parsed fixture data."""

    min_x, min_y, max_x, max_y = _source_bounds(easyeda_symbol)
    padding = 30.0
    view_x = min_x - padding
    view_y = min_y - padding
    width = max(max_x - min_x + (padding * 2), 80.0)
    height = max(max_y - min_y + (padding * 2), 80.0)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" '
            f'width="{_fmt(width)}" height="{_fmt(height)}" '
            f'viewBox="{_fmt(view_x)} {_fmt(view_y)} {_fmt(width)} {_fmt(height)}" '
            'stroke-linecap="round" stroke-linejoin="round" fill="none" '
            f'data-doc-id="easyeda-source-{_attr(easyeda_symbol.info.lcsc_id or easyeda_symbol.info.name)}">'
        ),
        '<g id="easyeda-source" font-family="Tahoma, Arial, sans-serif">',
    ]

    for rect in easyeda_symbol.rectangles:
        lines.append(
            '<rect '
            f'x="{_fmt(rect.x)}" y="{_fmt(rect.y)}" '
            f'width="{_fmt(rect.width)}" height="{_fmt(rect.height)}" '
            f'stroke="{_attr(_svg_color(rect.stroke_color, "#880000"))}" '
            f'stroke-width="{_fmt(rect.stroke_width or 1)}" '
            f'fill="{_attr(_svg_fill(rect.fill_color))}"/>'
        )

    for circle in easyeda_symbol.circles:
        lines.append(
            '<circle '
            f'cx="{_fmt(circle.cx)}" cy="{_fmt(circle.cy)}" r="{_fmt(circle.radius)}" '
            f'stroke="{_attr(_svg_color(circle.stroke_color, "#880000"))}" '
            f'stroke-width="{_fmt(circle.stroke_width or 1)}" '
            f'fill="{_attr(_svg_fill(circle.fill_color))}"/>'
        )

    for ellipse in easyeda_symbol.ellipses:
        lines.append(
            '<ellipse '
            f'cx="{_fmt(ellipse.cx)}" cy="{_fmt(ellipse.cy)}" '
            f'rx="{_fmt(ellipse.rx)}" ry="{_fmt(ellipse.ry)}" '
            f'stroke="{_attr(_svg_color(ellipse.stroke_color, "#880000"))}" '
            f'stroke-width="{_fmt(ellipse.stroke_width or 1)}" '
            f'fill="{_attr(_svg_fill(ellipse.fill_color))}"/>'
        )

    for polyline in easyeda_symbol.polylines:
        if len(polyline.points) >= 2:
            lines.append(
                '<polyline '
                f'points="{_attr(_points(polyline.points))}" '
                f'stroke="{_attr(_svg_color(polyline.stroke_color, "#A00000"))}" '
                f'stroke-width="{_fmt(polyline.stroke_width or 1)}" '
                f'fill="{_attr(_svg_fill(polyline.fill_color))}"/>'
            )

    for polygon in easyeda_symbol.polygons:
        if len(polygon.points) >= 3:
            lines.append(
                '<polygon '
                f'points="{_attr(_points(polygon.points))}" '
                f'stroke="{_attr(_svg_color(polygon.stroke_color, "#A00000"))}" '
                f'stroke-width="{_fmt(polygon.stroke_width or 1)}" '
                f'fill="{_attr(_svg_fill(polygon.fill_color))}"/>'
            )

    for path in easyeda_symbol.paths:
        if path.path_string:
            lines.append(
                '<path '
                f'd="{_attr(path.path_string)}" '
                f'stroke="{_attr(_svg_color(path.stroke_color, "#880000"))}" '
                f'stroke-width="{_fmt(path.stroke_width or 1)}" '
                f'fill="{_attr(_svg_fill(path.fill_color))}"/>'
            )

    for arc in easyeda_symbol.arcs:
        if arc.path_string:
            lines.append(
                '<path '
                f'd="{_attr(arc.path_string)}" '
                f'stroke="{_attr(_svg_color(arc.stroke_color, "#880000"))}" '
                f'stroke-width="{_fmt(arc.stroke_width or 1)}" '
                f'fill="{_attr(_svg_fill(arc.fill_color))}"/>'
            )

    for pin in easyeda_symbol.pins:
        if pin.path_string:
            lines.append(
                '<path '
                f'd="{_attr(pin.path_string)}" '
                f'stroke="{_attr(_svg_color(pin.path_color, "#880000"))}" '
                'stroke-width="1" fill="none"/>'
            )
        if pin.dot_visible:
            lines.append(
                '<circle '
                f'cx="{_fmt(pin.dot_circle_x)}" cy="{_fmt(pin.dot_circle_y)}" '
                'r="2" stroke="#880000" stroke-width="1" fill="#FFFFFF"/>'
            )
        if pin.clock_visible and pin.clock_path:
            lines.append(
                '<path '
                f'd="{_attr(pin.clock_path)}" '
                'stroke="#880000" stroke-width="1" fill="none"/>'
            )
        if pin.name_visible and pin.name:
            lines.append(
                _text_element(
                    pin.name,
                    pin.name_x,
                    pin.name_y,
                    pin.name_rotation,
                    pin.name_anchor,
                    pin.name_font_size,
                    "#0000FF",
                )
            )
        if pin.number_visible and pin.number:
            lines.append(
                _text_element(
                    pin.number,
                    pin.number_x,
                    pin.number_y,
                    pin.number_rotation,
                    pin.number_anchor,
                    pin.number_font_size,
                    "#0000FF",
                )
            )

    lines.extend(["</g>", "</svg>"])
    return _SvgDocument(content="\n".join(lines), width=width, height=height)


def render_compare_svg(
    *,
    easyeda_svg: _SvgDocument,
    altium_svg: _SvgDocument,
    symbol_name: str,
) -> str:
    """Render a single SVG with EasyEDA, Altium, and opacity overlay panels."""

    content_w = max(280.0, easyeda_svg.width, altium_svg.width)
    content_h = max(220.0, easyeda_svg.height, altium_svg.height)
    gap = 24.0
    margin = 18.0
    label_h = 34.0
    panel_w = content_w + 24.0
    panel_h = content_h + label_h + 24.0
    total_w = (margin * 2) + (panel_w * 3) + (gap * 2)
    total_h = (margin * 2) + panel_h

    easyeda_image = _data_uri(easyeda_svg.content)
    altium_image = _data_uri(altium_svg.content)

    panels = [
        _panel_svg(
            title="EasyEDA Source",
            x=margin,
            y=margin,
            panel_w=panel_w,
            panel_h=panel_h,
            content_w=content_w,
            content_h=content_h,
            images=[(easyeda_image, easyeda_svg.width, easyeda_svg.height, 1.0)],
        ),
        _panel_svg(
            title="Altium Generated",
            x=margin + panel_w + gap,
            y=margin,
            panel_w=panel_w,
            panel_h=panel_h,
            content_w=content_w,
            content_h=content_h,
            images=[(altium_image, altium_svg.width, altium_svg.height, 1.0)],
        ),
        _panel_svg(
            title="Overlay",
            x=margin + ((panel_w + gap) * 2),
            y=margin,
            panel_w=panel_w,
            panel_h=panel_h,
            content_w=content_w,
            content_h=content_h,
            images=[
                (easyeda_image, easyeda_svg.width, easyeda_svg.height, 0.55),
                (altium_image, altium_svg.width, altium_svg.height, 0.55),
            ],
        ),
    ]

    return "\n".join(
        [
            '<?xml version="1.0" encoding="UTF-8"?>',
            (
                '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" '
                'xmlns:xlink="http://www.w3.org/1999/xlink" '
                f'width="{_fmt(total_w)}" height="{_fmt(total_h)}" '
                f'viewBox="0 0 {_fmt(total_w)} {_fmt(total_h)}" '
                'data-doc-id="easyeda-altium-compare">'
            ),
            '<rect x="0" y="0" width="100%" height="100%" fill="#F6F7F9"/>',
            (
                f'<text x="{_fmt(margin)}" y="14" font-family="Arial, sans-serif" '
                f'font-size="10" fill="#667085">{_text(symbol_name)}</text>'
            ),
            *panels,
            "</svg>",
        ]
    )


def _panel_svg(
    *,
    title: str,
    x: float,
    y: float,
    panel_w: float,
    panel_h: float,
    content_w: float,
    content_h: float,
    images: list[tuple[str, float, float, float]],
) -> str:
    content_x = x + 12.0
    content_y = y + 38.0
    body_lines = [
        (
            f'<g id="{_attr(title.lower().replace(" ", "-"))}">'
            f'<rect x="{_fmt(x)}" y="{_fmt(y)}" width="{_fmt(panel_w)}" '
            f'height="{_fmt(panel_h)}" rx="4" fill="#FFFFFF" stroke="#D0D5DD"/>'
        ),
        (
            f'<text x="{_fmt(x + 12)}" y="{_fmt(y + 23)}" '
            'font-family="Arial, sans-serif" font-size="13" '
            f'fill="#101828">{_text(title)}</text>'
        ),
        (
            f'<rect x="{_fmt(content_x)}" y="{_fmt(content_y)}" '
            f'width="{_fmt(content_w)}" height="{_fmt(content_h)}" '
            'fill="#FFFFFF" stroke="#EAECF0"/>'
        ),
    ]
    for href, source_w, source_h, opacity in images:
        fit = _fit_rect(source_w, source_h, content_w, content_h)
        body_lines.append(
            '<image '
            f'x="{_fmt(content_x + fit[0])}" y="{_fmt(content_y + fit[1])}" '
            f'width="{_fmt(fit[2])}" height="{_fmt(fit[3])}" '
            f'opacity="{_fmt(opacity)}" preserveAspectRatio="xMidYMid meet" '
            f'href="{href}" xlink:href="{href}"/>'
        )
    body_lines.append("</g>")
    return "\n".join(body_lines)


def _review_svg_row(
    *,
    row: EasyEdaReviewRow,
    index: int,
    x: float,
    y: float,
    row_w: float,
    row_h: float,
    panel_w: float,
    panel_gap: float,
    image_w: float,
    image_h: float,
) -> str:
    title = f"{index}. {row.part_id}  {row.symbol_name}"
    summary = _row_summary(row)
    warning_text = ""
    if row.unsupported_count or row.warnings:
        warning_text = f" unsupported={row.unsupported_count} warnings={len(row.warnings)}"

    lines = [
        (
            f'<g id="review-row-{index}">'
            f'<rect x="{_fmt(x)}" y="{_fmt(y)}" width="{_fmt(row_w)}" '
            f'height="{_fmt(row_h)}" rx="6" fill="#FFFFFF" stroke="#D0D5DD"/>'
        ),
        (
            f'<text x="{_fmt(x + 12)}" y="{_fmt(y + 24)}" '
            'font-family="Arial, sans-serif" font-size="14" font-weight="700" '
            f'fill="#101828">{_text(title)}</text>'
        ),
        (
            f'<text x="{_fmt(x + 12)}" y="{_fmt(y + 43)}" '
            'font-family="Arial, sans-serif" font-size="11" '
            f'fill="#667085">{_text(row.source_name)} | {_text(summary)}</text>'
        ),
    ]
    if warning_text:
        lines.append(
            f'<text x="{_fmt(x + row_w - 12)}" y="{_fmt(y + 24)}" '
            'text-anchor="end" font-family="Arial, sans-serif" font-size="11" '
            f'fill="#B42318">{_text(warning_text.strip())}</text>'
        )

    panel_y = y + 58.0
    panel_h = row_h - 70.0
    lines.append(
        _review_svg_panel(
            title="EasyEDA Source",
            svg=row.easyeda_svg,
            x=x + 12.0,
            y=panel_y,
            panel_w=panel_w - 12.0,
            panel_h=panel_h,
            image_w=image_w,
            image_h=image_h,
        )
    )
    lines.append(
        _review_svg_panel(
            title="Altium Generated",
            svg=row.altium_svg,
            x=x + panel_w + panel_gap,
            y=panel_y,
            panel_w=panel_w - 12.0,
            panel_h=panel_h,
            image_w=image_w,
            image_h=image_h,
        )
    )
    lines.append("</g>")
    return "\n".join(lines)


def _footprint_review_svg_row(
    *,
    row: EasyEdaFootprintReviewRow,
    index: int,
    x: float,
    y: float,
    row_w: float,
    row_h: float,
    panel_w: float,
    panel_gap: float,
    image_w: float,
    image_h: float,
) -> str:
    title = f"{index}. {row.part_id}  {row.footprint_name}"
    summary = _footprint_row_summary(row)
    warning_text = ""
    if row.unsupported_count or row.warnings:
        warning_text = f" unsupported={row.unsupported_count} warnings={len(row.warnings)}"

    lines = [
        (
            f'<g id="footprint-review-row-{index}">'
            f'<rect x="{_fmt(x)}" y="{_fmt(y)}" width="{_fmt(row_w)}" '
            f'height="{_fmt(row_h)}" rx="6" fill="#FFFFFF" stroke="#D0D5DD"/>'
        ),
        (
            f'<text x="{_fmt(x + 12)}" y="{_fmt(y + 24)}" '
            'font-family="Arial, sans-serif" font-size="14" font-weight="700" '
            f'fill="#101828">{_text(title)}</text>'
        ),
        (
            f'<text x="{_fmt(x + 12)}" y="{_fmt(y + 43)}" '
            'font-family="Arial, sans-serif" font-size="11" '
            f'fill="#667085">{_text(row.source_name)} | {_text(summary)}</text>'
        ),
    ]
    if warning_text:
        lines.append(
            f'<text x="{_fmt(x + row_w - 12)}" y="{_fmt(y + 24)}" '
            'text-anchor="end" font-family="Arial, sans-serif" font-size="11" '
            f'fill="#B42318">{_text(warning_text.strip())}</text>'
        )

    panel_y = y + 58.0
    panel_h = row_h - 70.0
    lines.append(
        _review_svg_panel(
            title="EasyEDA Source",
            svg=row.easyeda_svg,
            x=x + 12.0,
            y=panel_y,
            panel_w=panel_w - 12.0,
            panel_h=panel_h,
            image_w=image_w,
            image_h=image_h,
        )
    )
    lines.append(
        _review_svg_panel(
            title="Altium Generated",
            svg=row.altium_svg,
            x=x + panel_w + panel_gap,
            y=panel_y,
            panel_w=panel_w - 12.0,
            panel_h=panel_h,
            image_w=image_w,
            image_h=image_h,
        )
    )
    lines.append("</g>")
    return "\n".join(lines)


def _review_svg_panel(
    *,
    title: str,
    svg: _SvgDocument,
    x: float,
    y: float,
    panel_w: float,
    panel_h: float,
    image_w: float,
    image_h: float,
) -> str:
    image_x = x + 10.0
    image_y = y + 32.0
    fit = _fit_rect(svg.width, svg.height, image_w, image_h)
    href = _data_uri(svg.content)
    return "\n".join(
        [
            (
                f'<g><rect x="{_fmt(x)}" y="{_fmt(y)}" width="{_fmt(panel_w)}" '
                f'height="{_fmt(panel_h)}" rx="4" fill="#FFFFFF" stroke="#EAECF0"/>'
            ),
            (
                f'<text x="{_fmt(x + 10)}" y="{_fmt(y + 21)}" '
                'font-family="Arial, sans-serif" font-size="12" '
                f'fill="#475467">{_text(title)}</text>'
            ),
            (
                f'<rect x="{_fmt(image_x)}" y="{_fmt(image_y)}" '
                f'width="{_fmt(image_w)}" height="{_fmt(image_h)}" '
                'fill="#FFFFFF" stroke="#F2F4F7"/>'
            ),
            (
                f'<image x="{_fmt(image_x + fit[0])}" y="{_fmt(image_y + fit[1])}" '
                f'width="{_fmt(fit[2])}" height="{_fmt(fit[3])}" '
                'preserveAspectRatio="xMidYMid meet" '
                f'href="{href}" xlink:href="{href}"/>'
            ),
            "</g>",
        ]
    )


def _review_html_row(index: int, row: EasyEdaReviewRow) -> str:
    warning_bits: list[str] = []
    if row.unsupported_count:
        warning_bits.append(f"unsupported={row.unsupported_count}")
    if row.warnings:
        warning_bits.append(f"warnings={len(row.warnings)}")
    warning_html = ""
    if warning_bits:
        warning_html = f' <span class="warn">{" ".join(_text(bit) for bit in warning_bits)}</span>'

    return "\n".join(
        [
            '<section class="row">',
            '<div class="row-head">',
            f"<strong>{index}. {_text(row.part_id)} {_text(row.symbol_name)}</strong>",
            f"<span>{_text(row.source_name)}</span>",
            "</div>",
            '<div class="panels">',
            _review_html_panel("EasyEDA Source", row.easyeda_svg),
            _review_html_panel("Altium Generated", row.altium_svg),
            "</div>",
            f'<div class="summary">{_text(_row_summary(row))}{warning_html}</div>',
            "</section>",
        ]
    )


def _footprint_review_html_row(index: int, row: EasyEdaFootprintReviewRow) -> str:
    warning_bits: list[str] = []
    if row.unsupported_count:
        warning_bits.append(f"unsupported={row.unsupported_count}")
    if row.warnings:
        warning_bits.append(f"warnings={len(row.warnings)}")
    warning_html = ""
    if warning_bits:
        warning_html = f' <span class="warn">{" ".join(_text(bit) for bit in warning_bits)}</span>'

    return "\n".join(
        [
            '<section class="row">',
            '<div class="row-head">',
            f"<strong>{index}. {_text(row.part_id)} {_text(row.footprint_name)}</strong>",
            f"<span>{_text(row.source_name)}</span>",
            "</div>",
            '<div class="panels">',
            _footprint_review_html_panel("EasyEDA Source", row.easyeda_svg),
            _footprint_review_html_panel("Altium Generated", row.altium_svg),
            "</div>",
            f'<div class="summary">{_text(_footprint_row_summary(row))}{warning_html}</div>',
            _footprint_row_mapping_html(row),
            "</section>",
        ]
    )


def _footprint_review_html_panel(title: str, svg: _SvgDocument) -> str:
    return "\n".join(
        [
            '<div class="panel">',
            f'<div class="panel-title">{_text(title)}</div>',
            '<div class="svg-viewer" data-svg-viewer>',
            '<div class="viewer-toolbar">',
            '<button type="button" data-action="zoom-out">-</button>',
            '<button type="button" data-action="zoom-in">+</button>',
            '<button type="button" data-action="fit">Fit</button>',
            '<span class="scale" data-scale>100%</span>',
            "</div>",
            '<div class="viewport svg-viewport">',
            f'<div class="svg-host" data-svg-b64="{_attr(_svg_base64(svg.content))}"></div>',
            "</div>",
            '<div class="layer-controls" data-layer-controls></div>',
            "</div>",
            "</div>",
        ]
    )


def _footprint_row_mapping_html(row: EasyEdaFootprintReviewRow) -> str:
    if not row.source_layers:
        return ""
    pills = []
    for source_id, count in row.source_layers:
        source_name, altium_name = _footprint_layer_mapping_for_source(source_id)
        pills.append(
            '<span class="mapping-pill">'
            f'{_text(source_id)} {_text(source_name)} -> {_text(altium_name)}'
            f' <span class="count">{int(count)}</span>'
            "</span>"
        )
    return (
        '<div class="mapping-line"><strong>Source layers used</strong> '
        + " ".join(pills)
        + "</div>"
    )


def _review_html_panel(title: str, svg: _SvgDocument) -> str:
    return "\n".join(
        [
            '<div class="panel">',
            f'<div class="panel-title">{_text(title)}</div>',
            '<div class="viewport">',
            f'<img alt="{_attr(title)}" src="{_data_uri(svg.content)}">',
            "</div>",
            "</div>",
        ]
    )


def _row_summary(row: EasyEdaReviewRow) -> str:
    return (
        f"pins={row.pin_count}, rect={row.rectangle_count}, circles={row.circle_count}, "
        f"ellipses={row.ellipse_count}, polylines={row.polyline_count}, "
        f"polygons={row.polygon_count}"
    )


def _footprint_row_summary(row: EasyEdaFootprintReviewRow) -> str:
    return (
        f"pads={row.generated_pad_count}/{row.source_pad_count}, "
        f"holes={row.generated_hole_pad_count}, slots={row.slotted_pad_count}, "
        f"custom={row.custom_pad_count}, tracks={row.track_segment_count}, "
        f"circles={row.circle_count}, arcs={row.arc_count}, regions={row.region_count}"
    )


def _footprint_layer_mapping_for_source(source_id: str) -> tuple[str, str]:
    normalized = str(source_id or "").strip() or "<empty>"
    return _FOOTPRINT_LAYER_MAPPING_BY_SOURCE.get(
        normalized,
        (f"Layer {normalized}", "UNMAPPED"),
    )


def _source_layer_sort_key(source_id: str) -> tuple[int, int | str]:
    normalized = str(source_id or "").strip()
    if normalized.isdigit():
        return 0, int(normalized)
    return 1, normalized


def _fit_rect(source_w: float, source_h: float, target_w: float, target_h: float) -> tuple[float, float, float, float]:
    if source_w <= 0 or source_h <= 0:
        return 0.0, 0.0, target_w, target_h
    scale = min(target_w / source_w, target_h / source_h)
    width = source_w * scale
    height = source_h * scale
    return (target_w - width) / 2.0, (target_h - height) / 2.0, width, height


def _svg_document_from_content(content: str) -> _SvgDocument:
    width = 800.0
    height = 600.0
    dim_match = _SVG_DIM_RE.search(content)
    if dim_match:
        width = float(dim_match.group(1))
        height = float(dim_match.group(2))
    else:
        viewbox_match = _SVG_VIEWBOX_RE.search(content)
        if viewbox_match:
            parts = viewbox_match.group(1).replace(",", " ").split()
            if len(parts) == 4:
                width = float(parts[2])
                height = float(parts[3])
    return _SvgDocument(content=content, width=width, height=height)


def _source_bounds(easyeda_symbol: EasyEdaSymbol) -> tuple[float, float, float, float]:
    xs: list[float] = []
    ys: list[float] = []

    def add_point(x: float, y: float) -> None:
        xs.append(x)
        ys.append(y)

    for rect in easyeda_symbol.rectangles:
        add_point(rect.x, rect.y)
        add_point(rect.x + rect.width, rect.y + rect.height)
    for circle in easyeda_symbol.circles:
        add_point(circle.cx - circle.radius, circle.cy - circle.radius)
        add_point(circle.cx + circle.radius, circle.cy + circle.radius)
    for ellipse in easyeda_symbol.ellipses:
        add_point(ellipse.cx - ellipse.rx, ellipse.cy - ellipse.ry)
        add_point(ellipse.cx + ellipse.rx, ellipse.cy + ellipse.ry)
    for polyline in easyeda_symbol.polylines:
        for x, y in polyline.points:
            add_point(x, y)
    for polygon in easyeda_symbol.polygons:
        for x, y in polygon.points:
            add_point(x, y)
    for path in easyeda_symbol.paths:
        for x, y in _path_points_for_bounds(path.path_string):
            add_point(x, y)
    for arc in easyeda_symbol.arcs:
        for x, y in _path_points_for_bounds(arc.path_string):
            add_point(x, y)

    for pin in easyeda_symbol.pins:
        add_point(pin.dot_x, pin.dot_y)
        add_point(pin.x, pin.y)
        add_point(pin.name_x, pin.name_y)
        add_point(pin.number_x, pin.number_y)
        for x, y in _path_points_for_bounds(pin.path_string):
            add_point(x, y)
        for x, y in _path_points_for_bounds(pin.clock_path):
            add_point(x, y)

    if not xs or not ys:
        return 0.0, 0.0, 80.0, 80.0
    return min(xs), min(ys), max(xs), max(ys)


def _path_points_for_bounds(path_string: str) -> list[tuple[float, float]]:
    tokens = _PATH_TOKEN_RE.findall(path_string or "")
    points: list[tuple[float, float]] = []
    index = 0
    command = ""
    current_x = 0.0
    current_y = 0.0

    try:
        while index < len(tokens):
            token = tokens[index]
            if _is_path_command(token):
                command = token
                index += 1
            if command in "MmLl":
                x = float(tokens[index])
                y = float(tokens[index + 1])
                index += 2
                if command.islower():
                    current_x += x
                    current_y += y
                else:
                    current_x = x
                    current_y = y
                points.append((current_x, current_y))
            elif command in "Hh":
                x = float(tokens[index])
                index += 1
                current_x = current_x + x if command == "h" else x
                points.append((current_x, current_y))
            elif command in "Vv":
                y = float(tokens[index])
                index += 1
                current_y = current_y + y if command == "v" else y
                points.append((current_x, current_y))
            else:
                break
    except (IndexError, ValueError):
        return points
    return points


def _text_element(
    value: str,
    x: float,
    y: float,
    rotation: float,
    anchor: str,
    font_size: str,
    color: str,
) -> str:
    transform = ""
    if rotation:
        transform = f' transform="rotate({_fmt(rotation)} {_fmt(x)} {_fmt(y)})"'
    size = font_size or "6pt"
    return (
        '<text '
        f'x="{_fmt(x)}" y="{_fmt(y)}" '
        f'text-anchor="{_attr(_text_anchor(anchor))}" '
        f'font-size="{_attr(size)}" fill="{_attr(color)}"{transform}>'
        f'{_text(value)}</text>'
    )


def _text_anchor(value: str) -> str:
    return {"start": "start", "middle": "middle", "end": "end"}.get(
        (value or "").strip().lower(),
        "start",
    )


def _svg_color(value: str, default: str) -> str:
    text = (value or "").strip()
    if text in {"", "none"}:
        return default
    if text.startswith("#") and len(text) == 4:
        return "#" + "".join(ch * 2 for ch in text[1:])
    return text


def _svg_fill(value: str) -> str:
    text = (value or "").strip()
    if text == "" or text.lower() in {"none", "transparent"}:
        return "none"
    return _svg_color(text, "none")


def _points(points: list[tuple[float, float]]) -> str:
    return " ".join(f"{_fmt(x)},{_fmt(y)}" for x, y in points)


def _data_uri(svg_content: str) -> str:
    return f"data:image/svg+xml;base64,{_svg_base64(svg_content)}"


def _svg_base64(svg_content: str) -> str:
    return base64.b64encode(svg_content.encode("utf-8")).decode("ascii")


def _is_path_command(token: str) -> bool:
    return len(token) == 1 and token.isalpha()


def _fmt(value: float) -> str:
    if abs(value - round(value)) < 1e-6:
        return str(int(round(value)))
    return f"{value:.4f}".rstrip("0").rstrip(".")


def _attr(value: str) -> str:
    return html.escape(str(value), quote=True)


def _text(value: str) -> str:
    return html.escape(str(value), quote=False)
