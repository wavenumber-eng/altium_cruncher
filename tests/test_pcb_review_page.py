"""The review gallery lists the generated project populations explicitly."""

import importlib.util
from pathlib import Path


def test_review_lists_only_svg_for_base_and_all_reported_variants(tmp_path):
    script = Path(__file__).parent / "support_scripts/pcb_review_page.py"
    spec = importlib.util.spec_from_file_location("pcb_review_page", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    report = {"variants": [
        {"variant": None, "directory": "."},
        {"variant": "A & B", "directory": "variants/A_B"},
    ]}
    for entry in report["variants"]:
        directory = tmp_path / entry["directory"]
        directory.mkdir(parents=True, exist_ok=True)
        for side in ("top", "bottom"):
            for mode in ("board", "assembly"):
                path = directory / f"{side}-{mode}-white.svg"
                path.write_text("<svg/>")
                path.with_suffix(".png").write_bytes(b"test-link")
    page = module._variant_boards(report, tmp_path, tmp_path, ("white",))
    assert page.count("<figure>") == 8
    assert ".png" not in page
    assert "Base (no variant)" in page
    assert 'data-variant="A &amp; B"' in page
    assert 'variants/A_B/bottom-assembly-white.svg?' in page
