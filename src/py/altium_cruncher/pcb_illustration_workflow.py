"""Project-to-SVG illustration orchestration, independent of CLI argument parsing.

One job owns geometry and layer caches across boards, variants and views. Variant
population is applied after shared artwork is built; authored documents stay intact.
"""

from __future__ import annotations

import logging
import xml.etree.ElementTree as ET
from pathlib import Path

from .altium_cruncher_pcb_svg_a0_renderer import PcbSvgA0Renderer
from .altium_cruncher_pcb_svg_config import PcbSvgConfig, resolve_config_output_path
from .altium_cruncher_pcb_workflow import (
    CruncherPcbRenderInput,
    iter_pcb_render_inputs,
    load_design_for_pcb_input,
)
from .pcb_illustration_config import illustration_view_side
from .pcb_illustration_variants import IllustrationVariant, illustration_variants
from .pcb_svg_render_job import PcbSvgRenderJob

log = logging.getLogger(__name__)


def render_project(
    input_file: Path,
    config: PcbSvgConfig,
    output_dir: Path,
    *,
    render_job: PcbSvgRenderJob,
    variant_name: str | None = None,
    all_variants: bool = False,
) -> int:
    """Resolve project metadata once, then render its selected boards/populations."""
    log.info("Loading project/board context: %s", input_file)
    with render_job.measure("project", board=str(input_file)):
        design, source = load_design_for_pcb_input(input_file, load_schematics=False)
    log.info("Loaded design context: %s", source)
    variants = illustration_variants(
        design, variant=variant_name, all_variants=all_variants
    )
    log.info("Loading selected PCB documents")
    with render_job.measure("load_boards", board=str(input_file)):
        boards = iter_pcb_render_inputs(
            design, pcbdoc_selector=config.global_options.pcbdoc
        )
    if not boards:
        raise ValueError(f"No PCB matched in {input_file}")
    common_dnp = frozenset.intersection(
        *(variant.excluded_designators for variant in variants)
    )
    variant_scoped = bool(variant_name or all_variants)
    written = 0
    for render_input in boards:
        render_job.register_board(render_input.pcbdoc, excluded_designators=common_dnp)
        for variant in variants:
            log.info(
                "Variant %s: %d DNP components",
                variant.name or "base",
                len(variant.excluded_designators),
            )
            variant_output = (
                output_dir / variant.folder if variant_scoped else output_dir
            )
            with render_job.measure(
                "variant",
                board=str(render_input.pcb_path),
                variant=variant.name or "base",
            ):
                written += render_board(
                    config,
                    render_input,
                    variant,
                    variant_output,
                    render_job=render_job,
                    variant_scoped=variant_scoped,
                )
    return written


def render_board(
    config: PcbSvgConfig,
    render_input: CruncherPcbRenderInput,
    variant: IllustrationVariant,
    output_dir: Path,
    *,
    render_job: PcbSvgRenderJob,
    variant_scoped: bool = False,
) -> int:
    renderer = PcbSvgA0Renderer(
        config, excluded_designators=variant.excluded_designators, render_job=render_job
    )
    pcbdoc = variant.board(render_input.pcbdoc)
    renderer.render_job.register_variant(pcbdoc, render_input.pcbdoc)
    written = 0
    for view in config.enabled_views():
        side = illustration_view_side(view)
        mirror = (
            view.mirror
            if view.mirror is not None
            else (config.global_options.mirror_bottom_view and side == "bottom")
        )
        log.info(
            "Rendering %s / %s / %s",
            render_input.board_key,
            variant.name or "base",
            view.name,
        )
        svg = renderer.render_view_svg(
            pcbdoc,
            view,
            project_parameters=variant.project_parameters,
            layers=view.layers,
            group_id=view.resolved_group_id(),
            mirror=mirror,
            styles=config.resolved_styles_for_view(view),
        )
        if variant.name is not None:
            root = ET.fromstring(svg)
            root.set("data-variant", variant.name)
            svg = ET.tostring(root, encoding="unicode")
        svg_path = resolve_config_output_path(
            output_dir,
            view.resolved_output_svg(),
            board=render_input.board_key,
            view=view.name,
        )
        if variant_scoped and not svg_path.resolve().is_relative_to(
            output_dir.resolve()
        ):
            raise ValueError(
                "Variant outputs must stay inside their variant directory; use relative output_svg paths"
            )
        svg_path.parent.mkdir(parents=True, exist_ok=True)
        with renderer.render_job.measure("write_svg", view=view.name, side=side):
            svg_path.write_text(svg, encoding="utf-8")
        log.info("Wrote SVG: %s", svg_path)
        written += 1
    return written
