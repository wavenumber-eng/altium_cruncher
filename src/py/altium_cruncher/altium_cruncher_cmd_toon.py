"""The toon command: top/bottom PCB illustrations using the SVG compositor."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from .altium_cruncher_common import find_pcbdocs_in_cwd, find_prjpcbs_in_cwd
from .altium_cruncher_pcb_svg_config import PcbSvgConfig, pcb_svg_config_text
from .pcb_illustration_workflow import render_project
from .config_json import load_json_config
from .pcb_illustration_config import resolve_illustration_config
from .pcb_svg_render_job import PcbSvgRenderJob
from .pcb_svg_model_cache import add_model_cache_arguments
from .pcb_svg_workers import add_svg_worker_arguments

log = logging.getLogger(__name__)
TOON_CONFIG_FILENAME = "toon.config"


def _resolve_config(args: argparse.Namespace, input_file: Path | None = None) -> PcbSvgConfig:
    config_path = args.config
    if config_path is None and input_file is not None:
        config_path = input_file.parent / TOON_CONFIG_FILENAME
    override = _read_config(config_path)
    if config_path and not config_path.exists():
        template = resolve_illustration_config(theme=args.theme, assembly=args.assembly, pcbdoc=args.pcbdoc)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(pcb_svg_config_text(template), encoding="utf-8")
        override = template.to_dict()
        log.info("Created editable toon config: %s", config_path)
    elif config_path:
        log.info("Using toon config: %s", config_path)
    config = resolve_illustration_config(
        override, side=args.side, theme=args.theme, assembly=args.assembly, pcbdoc=args.pcbdoc,
    )
    return config



def _read_config(path: Path | None) -> dict | None:
    from .contracts.pcb_svg import decode_pcb_svg_config

    if path is None or not path.exists():
        return None
    value = load_json_config(path)
    if value is None:
        return None
    return dict(decode_pcb_svg_config(value))


def _resolve_inputs(file: str | None) -> list[Path]:
    inputs = [Path(file).resolve()] if file else find_prjpcbs_in_cwd() or find_pcbdocs_in_cwd()
    if not inputs:
        raise ValueError("Specify a PrjPcb/PcbDoc or run inside its directory")
    for input_file in inputs:
        if not input_file.is_file() or input_file.suffix.lower() not in {".prjpcb", ".pcbdoc"}:
            raise ValueError(f"Input must be an existing PrjPcb or PcbDoc: {input_file}")
    return inputs


def _cmd_toon(args: argparse.Namespace, render_job: PcbSvgRenderJob) -> str:
    """Write the requested output and return its final user-facing summary."""
    if args.write_config:
        config = _resolve_config(args)
        args.write_config.parent.mkdir(parents=True, exist_ok=True)
        args.write_config.write_text(pcb_svg_config_text(config), encoding="utf-8")
        return f"Success: wrote toon SVG config to {args.write_config.resolve()}"
    inputs = _resolve_inputs(args.file)
    output_dir = args.output.resolve()
    written = 0
    for input_file in inputs:
        config = _resolve_config(args, input_file)
        written += render_project(
            input_file, config, output_dir, render_job=render_job,
            variant_name=args.variant, all_variants=args.all_variants,
        )
    if not written:
        return "No SVG files written: no views are enabled in the selected config."
    noun = "file" if written == 1 else "files"
    return f"Success: wrote {written} SVG {noun} to {output_dir}"


def cmd_toon(args: argparse.Namespace) -> int:
    render_job = PcbSvgRenderJob.from_args(args)
    try:
        try:
            with render_job.measure("job", command="toon"):
                try:
                    summary = _cmd_toon(args, render_job)
                finally:
                    render_job.finish()
        finally:
            if getattr(args, "timings", None):
                render_job.write_timings(args.timings)
                log.info("Wrote timing report: %s", args.timings.resolve())
    except (ValueError, OSError, RuntimeError) as exc:
        log.error("toon: %s", exc)
        return 1
    log.info(summary)
    return 0


def register_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(
        "toon", help="generate top/bottom PCB illustration SVGs",
        description="Generate PCB illustrations with built-in defaults and optional pcb.svg.config.a0 overrides.",
        epilog=(
            "Examples:\n"
            "  acr toon board.PrjPcb --theme white\n"
            "  acr toon board.PrjPcb --assembly --all-variants\n"
            "  acr toon --write-config toon.jsonc"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("file", nargs="?", help="PrjPcb/PcbDoc (auto-detected in CWD when omitted)")
    parser.add_argument("-o", "--output", type=Path, default=Path("output/toon"),
                        help="output directory (default: ./output/toon)")
    parser.add_argument("--doc", "--pcbdoc", dest="pcbdoc", help="select a PCB within a PrjPcb")
    parser.add_argument("--side", choices=("top", "bottom", "both"), default="both", help="board side (default: both)")
    parser.add_argument("--assembly", action="store_true", help="add projected assembly designators (red by default)")
    variants = parser.add_mutually_exclusive_group()
    variants.add_argument("--variant", help="named PrjPcb variant; omit DNP bodies/labels and apply parameter overrides")
    variants.add_argument("--all-variants", action="store_true", help="base plus all named variants, each in its own directory")
    parser.add_argument("--theme", choices=("saved", "white", "black", "green"),
                        help="mask/silk colors (default: saved mask, white silk; explicit choice overrides config)")
    parser.add_argument("--timings", type=Path, help="write SVG job/layer/view/variant wall timings and cache outcomes as JSON")
    add_model_cache_arguments(parser)
    add_svg_worker_arguments(parser)
    parser.add_argument("--config", type=Path, help="SVG JSON/JSONC settings; default: toon.config beside input, created if missing")
    parser.add_argument("--write-config", type=Path, help="write resolved editable SVG settings and exit")
    parser.set_defaults(handler=cmd_toon)
    return parser
