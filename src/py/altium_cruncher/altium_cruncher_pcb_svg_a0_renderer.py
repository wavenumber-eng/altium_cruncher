"""Compatibility imports for the former version-named PCB SVG renderer.

New code must import :mod:`altium_cruncher.altium_cruncher_pcb_svg_renderer`.
The aliases remain for one compatibility cycle because downstream Python tools
may have imported the implementation class even though it was not documented as
a stable public API.
"""

from __future__ import annotations

from .altium_cruncher_pcb_svg_renderer import (
    PcbSvgCompositeRenderer,
    render_pcb_svg_to_output,
    write_or_update_view_svg,
)

PcbSvgA0Renderer = PcbSvgCompositeRenderer
render_pcb_svg_a0_to_output = render_pcb_svg_to_output

__all__ = [
    "PcbSvgA0Renderer",
    "render_pcb_svg_a0_to_output",
    "write_or_update_view_svg",
]
