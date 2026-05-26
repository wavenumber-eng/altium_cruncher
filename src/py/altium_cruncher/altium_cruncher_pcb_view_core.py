"""
Shared PCB view render core for altium-cruncher commands.

This module provides a stable, command-agnostic interface for:
- loading/resolving pcb-svg configuration payloads
- executing PCB SVG/HTML view rendering
"""

from pathlib import Path

from altium_cruncher.altium_cruncher_cmd_pcb_svg import (
    PcbSvgConfig,
    PcbSvgViewConfig,
    render_pcb_views_from_inputs,
    resolve_pcb_svg_configs,
)

__all__ = [
    "PcbSvgConfig",
    "PcbSvgViewConfig",
    "resolve_pcb_svg_configs",
    "render_pcb_views_from_inputs",
]


def resolve_configs(
    args,
    input_files: list[Path],
) -> tuple[dict[Path, PcbSvgConfig], list[Path]]:
    """
    Resolve effective pcb-svg config for each input file.
    """
    return resolve_pcb_svg_configs(args, input_files)


def render_views(
    args,
    input_files: list[Path],
    output_dir: Path,
    config_by_input: dict[Path, PcbSvgConfig],
) -> int:
    """
    Render PCB views using the shared core pipeline.
    """
    return render_pcb_views_from_inputs(args, input_files, output_dir, config_by_input)
