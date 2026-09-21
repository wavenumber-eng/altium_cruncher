"""Reusable SVG review gallery behavior."""

import json
from pathlib import Path
import subprocess
import sys

import pytest

from altium_cruncher.svg_review_gallery import (
    SvgReviewItem,
    write_svg_review_gallery,
)

ROOT = Path(__file__).resolve().parents[1]


def _svg(path: Path, label: str = "fixture") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">'
        f'<title>{label}</title><path d="M0 0h10v10H0z"/></svg>',
        encoding="utf-8",
    )
    return path


def test_review_gallery_embeds_vector_modal_and_offline_pan_zoom(tmp_path):
    first = _svg(tmp_path / "inputs" / "top view.svg", "top")
    second = _svg(tmp_path / "inputs" / "bottom.svg", "bottom")

    target = write_svg_review_gallery(
        tmp_path / "review",
        [
            SvgReviewItem(first, "Top", "Single part"),
            SvgReviewItem(second, "Bottom", "Single part", "Seen from underneath"),
        ],
        title="Projection review",
    )

    text = target.read_text(encoding="utf-8")
    assert target == tmp_path / "review" / "index.html"
    assert "svg-pan-zoom v3.6.2" in text
    assert "https://cdn" not in text and "unpkg.com" not in text
    assert 'id="svg-review-dialog"' in text
    assert "window.svgPanZoom(svg" in text
    assert "mouseWheelZoomEnabled: true" in text
    assert "maxZoom: 100" in text
    assert "#review=" in text
    assert "grid-template-columns: repeat(auto-fit" in text
    assert "top%20view.svg?v=" in text
    assert text.count("Open raw SVG") == 2
    assert "Seen from underneath" in text
    embedded = json.loads(
        text.split('<script id="svg-review-data" type="application/json">', 1)[1].split(
            "</script>", 1
        )[0]
    )
    assert [item["title"] for item in embedded] == ["Top", "Bottom"]
    assert all(item["svg"].startswith("<svg") for item in embedded)


def test_manifest_script_resolves_relative_paths(tmp_path):
    svg = _svg(tmp_path / "vectors" / "part.svg")
    manifest = tmp_path / "review.json"
    manifest.write_text(
        json.dumps(
            {
                "title": "Arbitrary SVGs",
                "items": [
                    {
                        "title": "Part",
                        "path": str(svg.relative_to(tmp_path)),
                        "group": "Models",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    target = tmp_path / "out" / "review.html"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tests/support_scripts/svg_review_gallery.py"),
            str(manifest),
            "--output",
            str(target),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert target.name == "review.html"
    text = target.read_text(encoding="utf-8")
    assert "Arbitrary SVGs" in text
    assert "Models" in text
    assert "Part" in text


def test_manifest_script_splits_large_review_by_group_pattern(tmp_path):
    first = _svg(tmp_path / "vectors" / "gate1-top.svg", "gate 1 top")
    second = _svg(tmp_path / "vectors" / "gate1-bottom.svg", "gate 1 bottom")
    third = _svg(tmp_path / "vectors" / "gate2.svg", "gate 2")
    manifest = tmp_path / "review.json"
    manifest.write_text(
        json.dumps(
            {
                "title": "Rendering closeout",
                "split_by_group_pattern": r"^(Gate \d+)",
                "items": [
                    {
                        "title": "Top",
                        "path": str(first.relative_to(tmp_path)),
                        "group": "Gate 1 - Single parts",
                    },
                    {
                        "title": "Bottom",
                        "path": str(second.relative_to(tmp_path)),
                        "group": "Gate 1 - Single parts",
                    },
                    {
                        "title": "Stress",
                        "path": str(third.relative_to(tmp_path)),
                        "group": "Gate 2 - Projection stress",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    output = tmp_path / "review"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tests/support_scripts/svg_review_gallery.py"),
            str(manifest),
            "--output",
            str(output),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    index = (output / "index.html").read_text(encoding="utf-8")
    gate1 = (output / "gate-1" / "index.html").read_text(encoding="utf-8")
    gate2 = (output / "gate-2" / "index.html").read_text(encoding="utf-8")
    assert '<a class="gate" href="gate-1/index.html">' in index
    assert '<a class="gate" href="gate-2/index.html">' in index
    assert "<svg" not in index
    assert "Top" in gate1 and "Bottom" in gate1 and "Stress" not in gate1
    assert "Stress" in gate2 and "gate 1 top" not in gate2
    assert 'id="svg-review-dialog"' in gate1


def test_active_svg_content_is_rejected(tmp_path):
    active = tmp_path / "active.svg"
    active.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="active element"):
        write_svg_review_gallery(tmp_path / "review", [SvgReviewItem(active, "Unsafe")])
