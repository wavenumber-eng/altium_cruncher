"""Build top/bottom previews with copper, film, silkscreen and native illustrations.

uv run --no-sync python tests/support_scripts/pcb_board_review.py
uv run --no-sync python tests/support_scripts/pcb_board_review.py --projects bunny_brain goomba hydroscope --theme green
Updates the fixed illustration-review/index.html. Repeated component SVGs use defs/use.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
import time
import xml.etree.ElementTree as ET

from dataclasses import replace
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc
    from altium_cruncher.altium_cruncher_pcb_workflow import CruncherPcbRenderInput
    from altium_cruncher.pcb_illustration_variants import IllustrationVariant
    from altium_cruncher.altium_cruncher_pcb_svg_config import PcbSvgViewConfig
from altium_cruncher.altium_cruncher_pcb_svg_renderer import PcbSvgCompositeRenderer
from altium_cruncher.altium_cruncher_pcb_svg_config import PcbSvgConfig
from altium_cruncher.altium_cruncher_pcb_workflow import (
    iter_pcb_render_inputs,
    load_design_for_pcb_input,
)
from altium_cruncher.pcb_illustration_variants import illustration_variants
from altium_cruncher.pcb_svg_render_job import PcbSvgRenderJob
from altium_cruncher.pcb_svg_model_cache import (
    PcbSvgModelCache,
    add_model_cache_arguments,
)
from altium_cruncher.pcb_svg_workers import DEFAULT_WORKERS, add_svg_worker_arguments
from pcb_review_page import OUTPUT, write_review_page, write_standalone_review_page

ROOT = Path(__file__).resolve().parents[2]
SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)


def _review_config(theme: str) -> PcbSvgConfig:
    config_data = json.loads(
        (ROOT / "examples/pcb-svg/board-preview.config.json").read_text()
    )
    if theme in ("black", "white"):
        config_data["views"] = [
            view for view in config_data["views"] if view["name"].endswith("_green")
        ]
        for view in config_data["views"]:
            view["name"] = view["name"].replace("_green", "_" + theme)
            view["group_id"] = view["group_id"].replace("-green", "-" + theme)
            view["styles"]["soldermask_film"]["color"] = (
                "#000000" if theme == "black" else "#EEEEEE"
            )
            if theme == "white":
                for style in (
                    "silkscreen_component_graphics",
                    "silkscreen_designators",
                    "silkscreen_board_graphics",
                ):
                    view["styles"][style]["color"] = "#000000"
    config = PcbSvgConfig.from_dict(config_data)
    config.global_options.styles["assembly_designators"].update(
        stroke_color="#FFFFFF",
        stroke_width_mm=0.1,
    )
    return config


def _review_source(project_dir: Path, source: Path | None) -> Path:
    if source is None:
        sources = [
            p
            for p in (project_dir / "input").iterdir()
            if p.suffix.lower() == ".pcbdoc"
        ]
        if len(sources) != 1:
            raise ValueError(
                f"Expected one PCB in {project_dir / 'input'}, found {len(sources)}"
            )
        source = sources[0]
    return source


def render_board(
    project: str,
    theme: str | None,
    *,
    source: Path | None = None,
    output: Path | None = None,
    pcbdoc_selector: Path | None = None,
    cache_dir: Path | None = None,
    no_cache: bool = False,
    workers: int = DEFAULT_WORKERS,
) -> Path:
    started = time.perf_counter()
    if theme is None:
        theme = {
            "rt_super_c1": "white",
            "bunny_brain": "white",
            "goomba": "black",
            "hydroscope": "black",
        }.get(project, "all")
    project_dir = ROOT / "tests/assets/projects" / project
    source = _review_source(project_dir, source)
    if output is None:
        output = project_dir / "output/pcb-svg/illustration-review"
    output.mkdir(parents=True, exist_ok=True)
    print(f"{project}: reading {source.name}", flush=True)
    design, context_source = load_design_for_pcb_input(source)
    if source.suffix.lower() == ".pcbdoc":
        pcbdoc_selector = source
    inputs = iter_pcb_render_inputs(design, pcbdoc_selector=pcbdoc_selector)
    if len(inputs) != 1:
        raise ValueError("Expected one project PCB; use --pcbdoc to select the board")
    render_input = inputs[0]
    pcb = render_input.pcbdoc
    config = _review_config(theme)
    common_report = {
        "source": render_input.pcb_path.name,
        "project": project,
        "project_file": str(design.project.filepath) if design.project else None,
        "project_context": context_source,
        "theme": theme,
        "composition": "SVG virtual layers with reusable component symbols and assembly designators",
    }
    variants = illustration_variants(design, all_variants=True)
    render_job = PcbSvgRenderJob(
        model_cache=None if no_cache else PcbSvgModelCache(cache_dir), workers=workers
    )
    render_job.register_board(
        pcb,
        excluded_designators=frozenset.intersection(
            *(v.excluded_designators for v in variants)
        ),
    )
    print(
        f"{project}: rendering base and {len(variants) - 1} named variants", flush=True
    )
    reports = []
    try:
        for variant in variants:
            directory = (
                output if variant.name is None else output / "variants" / variant.folder
            )
            with render_job.measure(
                "variant",
                board=str(render_input.pcb_path),
                variant=variant.name or "base",
            ):
                report = _render_variant(
                    config,
                    variant,
                    pcb,
                    directory,
                    common_report,
                    render_job=render_job,
                )
            report["directory"] = directory.relative_to(output).as_posix()
            reports.append(report)
        report = {
            **reports[0],
            "variants": reports,
            "seconds": time.perf_counter() - started,
        }
        (output / "board-report.json").write_text(
            json.dumps(report, indent=2), encoding="utf-8"
        )
    finally:
        render_job.finish()
        render_job.write_timings(output / "svg-timings.json")
    print(
        f"{project}: finished {len(variants)} populations in {report['seconds']:.1f}s",
        flush=True,
    )
    return output


def _render_variant(
    config: PcbSvgConfig,
    variant: IllustrationVariant,
    saved_pcb: AltiumPcbDoc,
    output: Path,
    common_report: dict,
    *,
    render_job: PcbSvgRenderJob | None = None,
) -> dict:
    started = time.perf_counter()
    output.mkdir(parents=True, exist_ok=True)
    pcb = variant.board(saved_pcb)
    project_parameters = variant.project_parameters
    renderer = PcbSvgCompositeRenderer(
        config, excluded_designators=variant.excluded_designators, render_job=render_job
    )
    renderer.render_job.register_variant(pcb, saved_pcb)
    project, theme = common_report["project"], common_report["theme"]
    label = f"{project} / {variant.name or 'base'}"
    report = {
        **common_report,
        "variant": variant.name,
        "component_population": "variant" if variant.name is not None else "saved PCB",
        "excluded_designators": sorted(variant.excluded_designators),
        "sides": {},
    }
    report["mask_texts"] = _mask_text_report(renderer, pcb, project_parameters)
    for side in ("top", "bottom"):
        side_started = time.perf_counter()
        print(f"{label} {side}: rendering virtual layers", flush=True)
        for view in config.views:
            if not view.name.startswith(side + "_"):
                continue
            if theme != "all" and not view.name.endswith("_" + theme):
                continue
            _render_review_views(renderer, pcb, config, view, variant, side, output)
        report["sides"][side] = _side_report(
            renderer,
            pcb,
            side,
            variant.excluded_designators,
            time.perf_counter() - side_started,
        )
        print(
            f"{label} {side}: finished in {time.perf_counter() - side_started:.1f}s",
            flush=True,
        )
    session = renderer.component_layers
    report.update(
        status="complete",
        counts=session.job.counts if session.job else {},
        warnings=session.job.warnings if session.job else [],
        layer_cache_hits=session.layer_hits,
        designator_fits=session.fit_session.telemetry.as_dict(),
        seconds=time.perf_counter() - started,
    )
    (output / "board-report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(f"{label}: complete ({report['seconds']:.1f}s)", flush=True)
    return report


def _side_report(
    renderer: PcbSvgCompositeRenderer,
    pcb: AltiumPcbDoc,
    side: str,
    excluded: frozenset[str],
    seconds: float,
) -> dict[str, object]:
    session = renderer.component_layers
    source = renderer.render_job.source(pcb)
    parts = [
        part
        for part in session._parts.get(
            (id(source.components), id(source.component_bodies), side), []
        )
        if part.designator not in excluded
    ]
    return {
        "components": len(parts),
        "bodies": sum(len(part.bodies) for part in parts),
        "illustration_rendered": True,
        "designators": [part.designator for part in parts],
        "seconds": seconds,
    }


def _mask_text_report(
    renderer: PcbSvgCompositeRenderer,
    pcb: AltiumPcbDoc,
    project_parameters: dict[str, str],
) -> list[dict[str, object]]:
    text_context = renderer._build_context(pcb, project_parameters=project_parameters)
    return [
        {
            "layer": int(text.layer),
            "source": text.text_content,
            "resolved": text_context.substitute_special_strings(text.text_content),
            "barcode": text.font_type == 2,
        }
        for text in pcb.texts
        if int(text.layer) in (37, 38)
    ]


def _render_review_views(
    renderer: PcbSvgCompositeRenderer,
    pcb: AltiumPcbDoc,
    config: PcbSvgConfig,
    view: PcbSvgViewConfig,
    variant: IllustrationVariant,
    side: str,
    output: Path,
) -> None:
    project_parameters = variant.project_parameters
    for assembly in (False, True):
        active = replace(view, layers=list(view.layers), styles=dict(view.styles))
        if assembly:
            active.name = view.name.replace("_board_", "_assembly_")
            active.group_id = view.group_id.replace("-board-", "-assembly-")
            active.layers.append("ASSEMBLY_DESIGNATORS_" + side.upper())
            active.styles["silkscreen_designators"] = {"enabled": False}
        svg = renderer.render_view_svg(
            pcb,
            active,
            project_parameters=project_parameters,
            layers=active.layers,
            group_id=active.group_id,
            mirror=side == "bottom",
            styles=config.resolved_styles_for_view(active),
        )
        if variant.name is not None:
            root = ET.fromstring(svg)
            root.set("data-variant", variant.name)
            svg = ET.tostring(root, encoding="unicode")
        target_name = active.name.replace("_", "-")
        (output / f"{target_name}.svg").write_text(svg, encoding="utf-8")


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    parser = argparse.ArgumentParser(description=__doc__)
    sources = parser.add_mutually_exclusive_group()
    sources.add_argument("--projects", nargs="+")
    sources.add_argument(
        "--pcbdoc", type=Path, help="External board for a separate review page"
    )
    parser.add_argument(
        "--prjpcb", type=Path, help="Project context; --pcbdoc can select its board"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Required review directory for an external board/project",
    )
    parser.add_argument(
        "--theme", choices=("all", "saved", "green", "black", "white"), default=None
    )
    add_model_cache_arguments(parser)
    add_svg_worker_arguments(parser)
    args = parser.parse_args()
    if args.prjpcb is not None and args.projects:
        parser.error("--prjpcb cannot be combined with --projects")
    if args.pcbdoc is not None or args.prjpcb is not None:
        if args.output is None:
            parser.error("--pcbdoc/--prjpcb requires --output")
        source = args.prjpcb or args.pcbdoc
        output = render_board(
            source.stem,
            args.theme,
            source=source,
            output=args.output,
            pcbdoc_selector=args.pcbdoc,
            cache_dir=args.cache_dir,
            no_cache=args.no_cache,
            workers=args.workers,
        )
        print(write_standalone_review_page(output), flush=True)
        return
    if args.output is not None:
        parser.error("--output requires --pcbdoc or --prjpcb")
    for project in args.projects or ["rt_super_c1"]:
        render_board(
            project,
            args.theme,
            cache_dir=args.cache_dir,
            no_cache=args.no_cache,
            workers=args.workers,
        )
        print(write_review_page(OUTPUT), flush=True)


if __name__ == "__main__":
    main()
