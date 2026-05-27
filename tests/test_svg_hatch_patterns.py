import pytest

from altium_cruncher.svg_hatch_patterns import (
    svg_hatch_pattern_defs,
    svg_stroke_dasharray_for_style,
)


def test_svg_hatch_pattern_defs_support_configurable_spacing_and_angle() -> None:
    defs = svg_hatch_pattern_defs(
        pattern_id="test-hatch",
        stroke_color="#FF0000",
        spacing_mm=1.5,
        angle_deg=-45.0,
        line_width_mm=0.1,
        opacity=0.4,
    )
    joined = "\n".join(defs)

    assert 'id="test-hatch"' in joined
    assert 'width="1.5" height="1.5"' in joined
    assert 'patternTransform="rotate(-45)"' in joined
    assert 'stroke-width="0.1"' in joined
    assert 'opacity="0.4"' in joined


def test_svg_stroke_dasharray_for_style_supports_solid_and_dashed() -> None:
    assert svg_stroke_dasharray_for_style(outline_style="solid", dash_mm=1.0) == ""
    assert (
        svg_stroke_dasharray_for_style(outline_style="dashed", dash_mm=0.75)
        == "0.75 0.75"
    )


def test_svg_stroke_dasharray_for_style_rejects_unknown_style() -> None:
    with pytest.raises(ValueError, match="outline_style"):
        svg_stroke_dasharray_for_style(outline_style="dotted", dash_mm=1.0)
