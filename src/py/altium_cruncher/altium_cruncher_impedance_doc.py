"""Controlled-impedance routing documentation (the ``impedance-doc`` command).

Renders per-copper-layer review pages that show where each controlled-impedance
class routes, with the target impedance and single-ended / differential kind
labeled. Built on the public altium-monkey PCB SVG renderer and its
``data-net`` / ``data-primitive`` enrichment attributes -- no Altium, no
Draftsman IR.

For each copper layer one composed SVG page is written, drawing:

* that layer's copper in light-gray context (true pad shapes + track widths),
* every controlled-impedance class routed on the layer in its own color,
* a legend mapping color -> target impedance and single-ended / differential,
* the board outline.

Differential-pair classes take their impedance from the ``DiffPairsRouting``
rule; single-ended net classes from a controlled-impedance ``Width`` rule, or
the value encoded in the class name (e.g. ``SE_35`` -> 35 ohm).

The command autogenerates a commented ``impedance-doc.config`` (JSONC) next to
each input the first time it runs. Edit it by hand -- titles, colors, output
formats, page style, watermark, logo -- and subsequent runs honor it, so
headless / CI regeneration is reproducible from the config alone. Pretty titles
and colors are decoupled from the raw net-class names.
"""

from __future__ import annotations

import html
import io
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from altium_monkey import PcbLayer, PcbSvgRenderOptions
from altium_monkey.altium_pcb_drawing_geometry import discover_pcb_routed_class_views

if TYPE_CHECKING:
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc

from altium_cruncher.config_json import (
    JsoncCommentMap,
    load_json_config,
    render_commented_jsonc,
)

log = logging.getLogger(__name__)

CONFIG_SCHEMA = "altium_cruncher.impedance_doc.config.a0"
CONFIG_FILENAME = "impedance-doc.config"

# Distinct, print-friendly colors cycled across impedance groups.
PALETTE = ["#D00000", "#0070C0", "#00B050", "#7030A0", "#ED7D31",
           "#C00000", "#1F7A1F", "#7A4F00", "#005B9A", "#9A0059"]

# Single-ended Width rules often carry a default favorite_impedance (50); the
# real target is usually encoded in the class name (SE_35 -> 35 ohm). Anchor to
# a delimiter so generation / lane / bank counts (LANE12_, BANK_33) are not
# mistaken for an impedance value.
_NAME_OHM_RE = re.compile(r"(?:^|[_\-])(\d{2,3})(?:$|[_\-Oo])")

DEFAULT_FORMATS = ("svg", "html")
DEFAULT_SCALE = 10.0
DEFAULT_MIN_ROUTING_LENGTH_MILS = 10.0
DEFAULT_PNG_ZOOM = 2.0


# --------------------------------------------------------------------------- #
# Impedance extraction (pure PCB-doc logic, no rendering)                      #
# --------------------------------------------------------------------------- #

def _fmt_ohm(value: object) -> str | None:
    if value in (None, ""):
        return None
    try:
        return f"{float(str(value)):g} ohm"
    except (TypeError, ValueError):
        return f"{value} ohm"


def _name_ohm(name: str) -> str | None:
    """Impedance encoded in a class name (delimited 2-3 digit run), or None."""
    m = _NAME_OHM_RE.search(name or "")
    return f"{m.group(1)} ohm" if m else None


def diff_pair_impedance(pcbdoc: object, class_name: str) -> str | None:
    """Target impedance for a differential-pair class, from its routing rule."""
    needle = f"InDifferentialPairClass('{class_name}')"
    z = None
    for rule in getattr(pcbdoc, "rules", []) or []:
        if needle not in (getattr(rule, "scope1_expression", "") or ""):
            continue
        kind = getattr(rule, "rule_kind", "")
        if kind == "DiffPairsRouting" and getattr(rule, "impedance_profile_value", ""):
            z = rule.impedance_profile_value
        elif kind == "MaxMinImpedance":
            z = getattr(rule, "maximum", "") or getattr(rule, "minimum", "") or z
    return _fmt_ohm(z)


def single_ended_impedance(pcbdoc: object, class_name: str) -> str | None:
    """Target impedance for a single-ended net class.

    An explicit controlled-impedance value on the ``Width`` rule wins; otherwise
    the value encoded in the class name (``SE_35`` -> 35 ohm); the rule's
    ``favorite_impedance`` (often a meaningless default like 50) is the last
    resort. Returns ``None`` when the class carries no controlled-impedance
    ``Width`` rule at all -- a plain width constraint with no impedance data does
    not count, so an ordinary class like ``BANK_33`` is not mis-documented as a
    33-ohm controlled-impedance class.
    """
    needle = f"InNetClass('{class_name}')"
    has_impedance_rule = False
    explicit_z = None
    favorite_z = None
    for rule in getattr(pcbdoc, "rules", []) or []:
        if getattr(rule, "rule_kind", "") != "Width":
            continue
        if needle not in (getattr(rule, "scope1_expression", "") or ""):
            continue
        explicit = (getattr(rule, "impedance_profile_value", "")
                    or getattr(rule, "minimum_impedance", "")
                    or getattr(rule, "maximum_impedance", ""))
        favorite = getattr(rule, "favorite_impedance", "")
        if not (explicit or favorite or getattr(rule, "impedance_profile_driven", None)):
            continue  # plain width constraint, not controlled-impedance
        has_impedance_rule = True
        explicit_z = explicit or explicit_z
        favorite_z = favorite or favorite_z
    if not has_impedance_rule:
        return None
    return (_fmt_ohm(explicit_z)
            or _name_ohm(class_name)
            or _fmt_ohm(favorite_z)
            or "impedance n/a")


@dataclass
class ImpedanceClass:
    name: str
    kind: str          # "differential" | "single-ended"
    impedance: str     # e.g. "85 ohm"
    nets: tuple[str, ...]
    layers: tuple[PcbLayer, ...]


@dataclass
class ImpedanceGroup:
    impedance: str
    title: str
    color: str
    classes: list[ImpedanceClass] = field(default_factory=list)

    @property
    def kind(self) -> str:
        kinds = {c.kind for c in self.classes}
        if kinds == {"differential"}:
            return "differential"
        if kinds == {"single-ended"}:
            return "single-ended"
        return "diff + single-ended"

    @property
    def nets(self) -> set[str]:
        out: set[str] = set()
        for c in self.classes:
            out.update(c.nets)
        return out

    @property
    def layers(self) -> set[PcbLayer]:
        out: set[PcbLayer] = set()
        for c in self.classes:
            out.update(c.layers)
        return out


def _impedance_sort_key(z_text: str) -> tuple[int, float]:
    m = re.match(r"\s*([\d.]+)", z_text or "")
    return (0, float(m.group(1))) if m else (1, 0.0)


def discover_impedance_classes(
    pcbdoc: object, min_routing_length_mils: float
) -> list[ImpedanceClass]:
    """All controlled-impedance routed classes on the board, diff + single-ended."""
    out: list[ImpedanceClass] = []
    for view in discover_pcb_routed_class_views(
        pcbdoc, min_routing_length_mils=min_routing_length_mils
    ):
        if view.kind == "differential_pair_class":
            z = diff_pair_impedance(pcbdoc, view.name)
            kind = "differential"
        else:
            z = single_ended_impedance(pcbdoc, view.name)
            kind = "single-ended"
        if not z:
            continue  # not a controlled-impedance class
        out.append(ImpedanceClass(
            name=view.name, kind=kind, impedance=z,
            nets=tuple(view.nets), layers=tuple(view.layers),
        ))
    return out


def group_by_impedance(classes: list[ImpedanceClass]) -> list[ImpedanceGroup]:
    buckets: dict[str, ImpedanceGroup] = {}
    for c in classes:
        g = buckets.get(c.impedance)
        if g is None:
            g = buckets[c.impedance] = ImpedanceGroup(
                impedance=c.impedance, title=c.impedance, color="",
            )
        g.classes.append(c)
    groups = [buckets[z] for z in sorted(buckets, key=_impedance_sort_key)]
    for idx, g in enumerate(groups):
        g.color = PALETTE[idx % len(PALETTE)]
    return groups


# --------------------------------------------------------------------------- #
# JSONC config (the escape hatch)                                             #
# --------------------------------------------------------------------------- #

def default_style() -> dict:
    return {
        "context_copper": "#B8B8B8",
        "pad_via": "#000000",
        "board_outline": "#000000",
        "drill_knockout": "#FFFFFF",
        "background": "#FFFFFF",
        "font_family": "Arial, Helvetica, sans-serif",
        "title": "",          # blank -> derived from board file name
        "company": "",
        "watermark": "",
        "watermark_color": "#0000000F",
        "logo_path": "",      # optional PNG/SVG drawn top-right
        "logo_width_px": 120,
    }


def build_config_dict(
    pcbdoc_file: str, groups: list[ImpedanceGroup]
) -> dict:
    """Assemble the config dict that is serialized to the JSONC template."""
    return {
        "schema": CONFIG_SCHEMA,
        "source_pcbdoc": pcbdoc_file,
        "output": {"formats": list(DEFAULT_FORMATS)},
        "view": {
            "scale": DEFAULT_SCALE,
            "min_routing_length_mils": DEFAULT_MIN_ROUTING_LENGTH_MILS,
            "png_zoom": DEFAULT_PNG_ZOOM,
        },
        "style": default_style(),
        "groups": [
            {
                "impedance": g.impedance,
                "title": g.title,
                "color": g.color,
                "kind": g.kind,
                "classes": [c.name for c in g.classes],
            }
            for g in groups
        ],
    }


_CONFIG_COMMENTS: JsoncCommentMap = {
    "schema": "Config contract identifier; do not edit.",
    "source_pcbdoc": "Board this config was generated from (informational).",
    "output.formats": (
        "Output formats. svg is primary; html/png/pdf are derived from it. "
        "png/pdf are rasterized with resvg-py; pdf also needs Pillow. Missing "
        "deps are skipped with a warning (svg/html still emit)."
    ),
    "view.scale": "SVG display scale of the rendered board.",
    "view.min_routing_length_mils": (
        "Ignore routing shorter than this when deciding which layers a class is "
        "on (filters stubs/fanout)."
    ),
    "view.png_zoom": "Raster (png/pdf) zoom factor over the SVG's natural size.",
    "style": "Page style, branding, watermark, and logo.",
    "groups": (
        "One entry per target impedance. title/color are decoupled from the raw "
        "net-class names so you can pretty-print the legend. kind is "
        "informational; classes membership is re-derived from the board each run."
    ),
}

_CONFIG_HEADER = (
    "altium-cruncher impedance-doc configuration.",
    "Autogenerated -- safe to hand-edit. Re-running honors every value below.",
    "Delete this file to regenerate defaults from the board.",
)


def render_config_jsonc(pcbdoc_file: str, groups: list[ImpedanceGroup]) -> str:
    return render_commented_jsonc(
        build_config_dict(pcbdoc_file, groups),
        comments_by_path=_CONFIG_COMMENTS,
        header_lines=_CONFIG_HEADER,
    )


def load_config(path: Path) -> dict:
    raw = load_json_config(path)
    if not isinstance(raw, dict):
        raise ValueError(f"impedance-doc config must be a JSON object: {path}")
    return raw


def apply_config(groups: list[ImpedanceGroup], config: dict) -> None:
    """Override title/color on detected groups from the config (matched by ohm)."""
    by_imp = {str(g.get("impedance")): g for g in config.get("groups", [])}
    for g in groups:
        cfg = by_imp.get(g.impedance)
        if not cfg:
            continue
        g.title = str(cfg.get("title") or g.title)
        g.color = str(cfg.get("color") or g.color)


# --------------------------------------------------------------------------- #
# SVG helpers (recolor + compose)                                            #
# --------------------------------------------------------------------------- #

def _split_rgba_hex(color: str) -> tuple[str, str | None]:
    """Split an 8-digit #RRGGBBAA color into (#RRGGBB, opacity). resvg/legacy
    renderers do not parse packed alpha, so emit the alpha as a separate
    opacity. Non-8-digit colors pass through unchanged."""
    m = re.fullmatch(r"#([0-9a-fA-F]{6})([0-9a-fA-F]{2})", color or "")
    if not m:
        return color, None
    return f"#{m.group(1)}", f"{int(m.group(2), 16) / 255:.3f}"


def _svg_attr(element: str, name: str) -> str | None:
    m = re.search(rf'\b{re.escape(name)}="([^"]*)"', element)
    return html.unescape(m.group(1)) if m else None


def _replace_attr(element: str, name: str, value: str) -> str:
    return re.sub(rf'\b{re.escape(name)}="[^"]*"',
                  f'{name}="{html.escape(value, quote=True)}"', element)


def _set_colors(element: str, *, stroke: str | None = None,
                fill: str | None = None) -> str:
    out = element
    if stroke is not None and _svg_attr(out, "stroke") is not None:
        out = _replace_attr(out, "stroke", stroke)
    if fill is not None and _svg_attr(out, "fill") is not None:
        out = _replace_attr(out, "fill", fill)
    if _svg_attr(out, "data-color") is not None:
        c = fill or stroke
        if c is not None:
            out = _replace_attr(out, "data-color", c)
    return out


def recolor_layer_svg(svg: str, net_color: dict[str, str], style: dict) -> str:
    """Recolor each primitive: impedance nets in their group color, everything
    else in gray context; pads/vias black; drills knockout."""
    grey = style["context_copper"]
    black = style["pad_via"]
    knock = style["drill_knockout"]
    out: list[str] = []
    for line in svg.splitlines():
        prim = _svg_attr(line, "data-primitive")
        if prim is None:
            out.append(line)
            continue
        if prim in {"track", "arc"}:
            net = _svg_attr(line, "data-net")
            out.append(_set_colors(line, stroke=net_color.get(net or "", grey)))
        elif prim in {"fill", "region", "shapebased-region", "polygon-outline"}:
            out.append(_set_colors(line, stroke=grey, fill=grey))
        elif prim in {"pad", "via"}:
            out.append(_set_colors(line, stroke=black, fill=black))
        elif prim in {"pad-hole", "via-hole"}:
            out.append(_set_colors(line, stroke=knock, fill=knock))
        else:
            out.append(line)
    return "\n".join(out)


def _nets_present(svg: str) -> set[str]:
    nets: set[str] = set()
    for line in svg.splitlines():
        if _svg_attr(line, "data-primitive") in {"track", "arc"}:
            n = _svg_attr(line, "data-net")
            if n:
                nets.add(n)
    return nets


def _root_svg_dims(svg: str) -> tuple[float, float]:
    m = re.search(r"<svg\b[^>]*>", svg)
    head = m.group(0) if m else ""
    vb = _svg_attr(head, "viewBox")
    if vb:
        parts = vb.replace(",", " ").split()
        if len(parts) == 4:
            return float(parts[2]), float(parts[3])

    def num(s: str) -> float:
        m2 = re.match(r"[\d.]+", s or "")
        return float(m2.group(0)) if m2 else 1000.0

    return num(_svg_attr(head, "width") or "1000"), num(_svg_attr(head, "height") or "1000")


def _inner_svg(svg: str) -> str:
    """Strip XML prolog so the document can be nested inside another <svg>."""
    svg = re.sub(r"^\s*<\?xml[^>]*\?>\s*", "", svg)
    svg = re.sub(r"<!DOCTYPE[^>]*>\s*", "", svg)
    return svg.strip()


def _strip_size_attrs(attrs: str) -> str:
    return re.sub(r'\s(width|height|x|y)="[^"]*"', "", attrs)


def _estimate_label_px(text: str, font_size: float) -> float:
    return len(text) * font_size * 0.62


def compose_page_svg(layer_svg: str, *, layer_name: str,
                     groups: list[ImpedanceGroup], present: set[str],
                     style: dict, page_title: str) -> str:
    """Wrap a rendered layer SVG with a header (title/company/logo), a legend
    (impedance + single-ended/differential), and an optional watermark."""
    inner_w, inner_h = _root_svg_dims(layer_svg)
    header_h = 70.0
    pad = 16.0
    scale = max(min(900.0 / inner_w, 1200.0 / inner_h), 0.05) if inner_w and inner_h else 1.0
    view_w = inner_w * scale
    view_h = inner_h * scale
    font = style["font_family"]
    bg = style["background"]

    # Size the legend column to the longest rendered label so config-editable
    # titles never clip at the page's right edge.
    legend_labels = [
        f"{g.title}  ({g.kind})" + ("" if g.nets & present else "  (not on this layer)")
        for g in groups
    ]
    longest = max([_estimate_label_px(s, 12.0) for s in legend_labels]
                  + [_estimate_label_px("Controlled-impedance", 14.0)], default=200.0)
    legend_w = max(230.0, longest + 28.0)
    page_w = view_w + legend_w + pad * 3
    page_h = max(view_h, 60.0 + len(groups) * 26.0) + header_h + pad * 2

    nested = _inner_svg(layer_svg)
    nested = re.sub(
        r"<svg\b([^>]*?)>",
        lambda m: f'<svg{_strip_size_attrs(m.group(1))} '
                  f'x="{pad:.1f}" y="{header_h + pad:.1f}" '
                  f'width="{view_w:.1f}" height="{view_h:.1f}" '
                  f'preserveAspectRatio="xMidYMid meet">',
        nested, count=1,
    )

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{page_w:.1f}" height="{page_h:.1f}" '
        f'viewBox="0 0 {page_w:.1f} {page_h:.1f}" '
        f'data-acr-layer="{html.escape(layer_name)}">',
        f'<rect x="0" y="0" width="{page_w:.1f}" height="{page_h:.1f}" fill="{bg}"/>',
        f'<text x="{pad:.1f}" y="28" font-family="{font}" font-size="20" '
        f'font-weight="bold" fill="#202020">{html.escape(page_title)}</text>',
        f'<text x="{pad:.1f}" y="50" font-family="{font}" font-size="14" '
        f'fill="#404040">Layer: {html.escape(layer_name)}</text>',
    ]
    logo_w = float(style.get("logo_width_px") or 120) if style.get("logo_path") else 0.0
    if style.get("company"):
        company_x = page_w - pad - (logo_w + 8 if logo_w else 0)
        parts.append(
            f'<text x="{company_x:.1f}" y="28" text-anchor="end" '
            f'font-family="{font}" font-size="13" fill="#606060">'
            f'{html.escape(style["company"])}</text>'
        )
    if style.get("logo_path"):
        parts.append(
            f'<image x="{page_w - pad - logo_w:.1f}" y="20" width="{logo_w:.1f}" '
            f'href="{html.escape(style["logo_path"], quote=True)}"/>'
        )

    parts.append(nested)

    if style.get("watermark"):
        cx = pad + view_w / 2.0
        cy = header_h + pad + view_h / 2.0
        wm_fill, wm_opacity = _split_rgba_hex(style.get("watermark_color", "#0000000F"))
        opacity_attr = f' fill-opacity="{wm_opacity}"' if wm_opacity else ""
        parts.append(
            f'<text x="{cx:.1f}" y="{cy:.1f}" text-anchor="middle" '
            f'font-family="{font}" font-size="{view_w / 10:.0f}" '
            f'fill="{wm_fill}"{opacity_attr} '
            f'transform="rotate(-30 {cx:.1f} {cy:.1f})">'
            f'{html.escape(style["watermark"])}</text>'
        )

    lx = view_w + pad * 2
    ly = header_h + pad + 8
    parts.append(
        f'<text x="{lx:.1f}" y="{ly:.1f}" font-family="{font}" font-size="14" '
        f'font-weight="bold" fill="#202020">Controlled-impedance</text>'
    )
    y = ly + 26
    for g, label in zip(groups, legend_labels):
        on = bool(g.nets & present)
        swatch = g.color if on else "#CCCCCC"
        text_col = "#202020" if on else "#999999"
        parts.append(
            f'<rect x="{lx:.1f}" y="{y - 12:.1f}" width="16" height="16" fill="{swatch}"/>'
        )
        parts.append(
            f'<text x="{lx + 24:.1f}" y="{y:.1f}" font-family="{font}" '
            f'font-size="12" fill="{text_col}">{html.escape(label)}</text>'
        )
        y += 26
    parts.append("</svg>")
    return "\n".join(parts)


# --------------------------------------------------------------------------- #
# Rendering pipeline                                                          #
# --------------------------------------------------------------------------- #

def _safe(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name.strip()).strip("_").lower() or "item"


def _copper_context_colors(grey: str) -> dict[PcbLayer, str]:
    return {layer: grey for layer in PcbLayer if layer.is_copper()}


@dataclass
class ImpedanceDocResult:
    groups: list[ImpedanceGroup]
    svg_pages: list[Path]
    html_page: Path | None
    png_pages: list[Path]
    pdf_page: Path | None


def render_impedance_doc(
    pcbdoc: "AltiumPcbDoc",
    project_parameters: dict[str, str],
    groups: list[ImpedanceGroup],
    config: dict,
    out_dir: Path,
    page_title: str,
) -> ImpedanceDocResult:
    style = {**default_style(), **(config.get("style") or {})}
    view = config.get("view", {})
    scale = float(view.get("scale", DEFAULT_SCALE))
    png_zoom = float(view.get("png_zoom", DEFAULT_PNG_ZOOM))
    background = style["background"]
    formats = [f.lower() for f in (config.get("output", {}).get("formats") or DEFAULT_FORMATS)]

    net_color: dict[str, str] = {}
    for g in groups:
        for net in g.nets:
            net_color[net] = g.color

    all_layers = sorted({layer for g in groups for layer in g.layers},
                        key=lambda layer: layer.value)
    options = PcbSvgRenderOptions(
        visible_layers=set(all_layers),
        svg_display_scale=scale,
        layer_colors=_copper_context_colors(style["context_copper"]),
        polygon_overlay_color=style["context_copper"],
        board_outline_color=style["board_outline"],
        board_cutout_color=style["board_outline"],
        drill_hole_mode="knockout",
        # Interleave drill holes into each copper-layer SVG (instead of the
        # separate synthetic "DRILLS" group) so the pad-hole/via-hole knockout
        # recolor fires on each page.
        drill_holes_as_layer_group=False,
    )
    layer_svgs = pcbdoc.to_layer_svgs(options=options, project_parameters=project_parameters)

    svg_dir = out_dir / "svg"
    svg_dir.mkdir(parents=True, exist_ok=True)
    pages: list[dict] = []
    for layer in all_layers:
        raw = layer_svgs.get(layer.to_json_name())
        if raw is None:
            continue
        present = _nets_present(raw)
        colored = recolor_layer_svg(raw, net_color, style)
        page = compose_page_svg(
            colored, layer_name=layer.to_display_name(), groups=groups,
            present=present, style=style, page_title=page_title,
        )
        path = svg_dir / f"layer_{layer.value:02d}_{_safe(layer.to_json_name())}.svg"
        path.write_text(page, encoding="utf-8")
        pages.append({"layer": layer.to_display_name(), "svg": path})
        log.info("Layer page: %s", path)

    html_page = _write_html(pages, out_dir, page_title, style) if "html" in formats else None
    png_pages = (_write_png(pages, out_dir, background=background, zoom=png_zoom)
                 if "png" in formats else [])
    pdf_page = (_write_pdf(pages, out_dir, page_title, background=background, zoom=png_zoom)
                if "pdf" in formats else None)
    return ImpedanceDocResult(
        groups=groups,
        svg_pages=[p["svg"] for p in pages],
        html_page=html_page,
        png_pages=png_pages,
        pdf_page=pdf_page,
    )


def _write_html(pages: list[dict], out_dir: Path, title: str, style: dict) -> Path:
    sections = []
    for p in pages:
        svg_text = p["svg"].read_text(encoding="utf-8")
        sections.append(
            f'<section class="page"><h2>{html.escape(p["layer"])}</h2>'
            f'<div class="frame">{svg_text}</div></section>'
        )
    doc = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        f"<title>{html.escape(title)}</title><style>"
        f"body{{font-family:{style['font_family']};margin:24px;background:#f7f7f4;color:#202020}}"
        "h1{margin:0 0 16px}.page{margin:0 0 28px;padding:12px;background:#fff;border:1px solid #d8d8d0}"
        ".frame{overflow:auto}svg{display:block;max-width:none}</style></head><body>"
        f"<h1>{html.escape(title)}</h1>" + "".join(sections) + "</body></html>"
    )
    path = out_dir / "index.html"
    path.write_text(doc, encoding="utf-8")
    log.info("HTML: %s", path)
    return path


def _rasterize_png(svg_path: Path, *, background: str, zoom: float) -> bytes | None:
    """Render an SVG file to PNG bytes via resvg (pure-Rust; no native cairo).
    Returns None when resvg is not installed."""
    try:
        import resvg_py  # type: ignore
    except Exception:
        return None
    raw: Any = resvg_py.svg_to_bytes(svg_path=str(svg_path), background=background, zoom=zoom)  # type: ignore[arg-type]  # noqa: E501
    return bytes(raw)


def _write_png(pages: list[dict], out_dir: Path, *, background: str,
               zoom: float) -> list[Path]:
    png_dir = out_dir / "png"
    written: list[Path] = []
    for p in pages:
        data = _rasterize_png(p["svg"], background=background, zoom=zoom)
        if data is None:
            log.warning("png skipped: install resvg-py for PNG output "
                        "(SVG/HTML still generated).")
            return written
        png_dir.mkdir(parents=True, exist_ok=True)
        path = png_dir / (p["svg"].stem + ".png")
        path.write_bytes(data)
        written.append(path)
        log.info("PNG: %s", path)
    return written


def _write_pdf(pages: list[dict], out_dir: Path, title: str, *,
               background: str, zoom: float) -> Path | None:
    """Rasterize each layer SVG via resvg, then assemble a multi-page PDF with
    Pillow. Avoids the native-cairo dependency that cairosvg needs on Windows."""
    try:
        from PIL import Image  # type: ignore
    except Exception:
        log.warning("pdf skipped: install Pillow for PDF output "
                    "(SVG/HTML still generated).")
        return None
    frames = []
    for p in pages:
        data = _rasterize_png(p["svg"], background=background, zoom=zoom)
        if data is None:
            log.warning("pdf skipped: install resvg-py for PDF output "
                        "(SVG/HTML still generated).")
            return None
        frames.append(Image.open(io.BytesIO(data)).convert("RGB"))
    if not frames:
        return None
    pdf_path = out_dir / f"{_safe(title)}.pdf"
    frames[0].save(pdf_path, "PDF", save_all=True, append_images=frames[1:])
    log.info("PDF: %s", pdf_path)
    return pdf_path


__all__ = [
    "CONFIG_FILENAME",
    "CONFIG_SCHEMA",
    "ImpedanceClass",
    "ImpedanceDocResult",
    "ImpedanceGroup",
    "apply_config",
    "build_config_dict",
    "diff_pair_impedance",
    "discover_impedance_classes",
    "group_by_impedance",
    "load_config",
    "render_config_jsonc",
    "render_impedance_doc",
    "single_ended_impedance",
]
