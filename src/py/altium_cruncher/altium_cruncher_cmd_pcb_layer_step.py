"""pcb-layer-step command for altium_cruncher."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from altium_cruncher.altium_cruncher_common import (
    _resolve_output_dir,
    find_pcbdocs_in_cwd,
    find_prjpcbs_in_cwd,
)
from altium_cruncher.altium_cruncher_pcb_layer_step import (
    PCB_LAYER_STEP_CONFIG_FILENAME,
    PcbLayerStepConfig,
    PcbLayerStepOptions,
    export_pcb_layer_step,
    layer_step_output_name,
    load_pcb_layer_step_config,
    resolve_pcb_layer_selector,
    write_default_pcb_layer_step_config,
)
from altium_cruncher.altium_cruncher_pcb_workflow import (
    iter_pcb_render_inputs,
    load_design_for_pcb_input,
)

log = logging.getLogger(__name__)


def cmd_pcb_layer_step(args) -> int:
    """Generate a STEP alignment model for one selected PCB layer."""
    input_files = _resolve_input_files(args.file)
    if not input_files:
        return 1

    try:
        config_by_input, created_configs = resolve_pcb_layer_step_configs(args, input_files)
    except ValueError as exc:
        log.error(str(exc))
        return 1

    if created_configs:
        for config_path in created_configs:
            log.info("Created pcb-layer-step config template: %s", config_path)
        log.info("pcb-layer-step config template created and defaulted for this invocation.")

    output_dir = _resolve_output_dir(args.output, "pcb-layer-step")
    written = 0
    for input_file in input_files:
        config = config_by_input[input_file.resolve()]
        try:
            options = _options_from_config_and_args(config, args)
        except ValueError as exc:
            log.error(str(exc))
            return 1
        pcbdoc_selector = getattr(args, "pcbdoc", None) or config.pcbdoc
        try:
            design, _source_tag = load_design_for_pcb_input(
                input_file,
                project_context=getattr(args, "project_context", "auto"),
            )
            render_inputs = iter_pcb_render_inputs(
                design,
                pcbdoc_selector=pcbdoc_selector,
            )
        except Exception as exc:
            log.error("Failed loading PCB input %s: %s", input_file.name, exc)
            return 1

        for render_input in render_inputs:
            output_path = output_dir / layer_step_output_name(
                render_input.board_key, options.layer
            )
            try:
                result = export_pcb_layer_step(
                    render_input.pcbdoc,
                    output_path,
                    options=options,
                    board_name=render_input.board_key,
                    source_input=str(render_input.pcb_path),
                )
            except Exception as exc:
                log.error(
                    "Failed generating PCB layer STEP for %s (%s): %s",
                    render_input.board_key,
                    options.layer.to_display_name(),
                    exc,
                )
                return 1
            written += 2
            log.info(
                "PCB layer STEP (%s %s): %s, %s",
                render_input.board_key,
                options.layer.to_json_name(),
                result.output_path.name,
                result.manifest_path.name,
            )

    log.info("Generated %d PCB layer STEP artifact file(s) in %s", written, output_dir)
    return 0


def resolve_pcb_layer_step_configs(
    args,
    input_files: list[Path],
) -> tuple[dict[Path, PcbLayerStepConfig], list[Path]]:
    """Resolve one effective pcb-layer-step config per input file."""
    resolved_input_files = [path.resolve() for path in input_files]
    created_paths: list[Path] = []
    config_by_input: dict[Path, PcbLayerStepConfig] = {}
    config_cache: dict[Path, PcbLayerStepConfig] = {}

    if getattr(args, "config", None):
        explicit_config_path = Path(args.config).resolve()
        if not explicit_config_path.exists():
            write_default_pcb_layer_step_config(explicit_config_path)
            created_paths.append(explicit_config_path)
        loaded_config = load_pcb_layer_step_config(explicit_config_path)
        for input_file in resolved_input_files:
            config_by_input[input_file] = loaded_config
        return config_by_input, created_paths

    for input_file in resolved_input_files:
        auto_config_path = input_file.parent / PCB_LAYER_STEP_CONFIG_FILENAME
        if not auto_config_path.exists():
            write_default_pcb_layer_step_config(auto_config_path)
            created_paths.append(auto_config_path)

    for input_file in resolved_input_files:
        auto_config_path = input_file.parent / PCB_LAYER_STEP_CONFIG_FILENAME
        loaded = config_cache.get(auto_config_path)
        if loaded is None:
            loaded = load_pcb_layer_step_config(auto_config_path)
            config_cache[auto_config_path] = loaded
        config_by_input[input_file] = loaded

    return config_by_input, sorted(set(created_paths))


def _options_from_config_and_args(config: PcbLayerStepConfig, args) -> PcbLayerStepOptions:
    layer = resolve_pcb_layer_selector(getattr(args, "layer", None) or config.layer)
    return PcbLayerStepOptions(
        layer=layer,
        thickness_mm=float(_arg_or_config(args, "thickness_mm", config.thickness_mm)),
        z_mm=float(_arg_or_config(args, "z_mm", config.z_mm)),
        copper_color=str(_arg_or_config(args, "copper_color", config.copper_color)),
        outline_width_mm=float(
            _arg_or_config(args, "outline_width_mm", config.outline_width_mm)
        ),
        outline_color=str(_arg_or_config(args, "outline_color", config.outline_color)),
        include_copper=False
        if bool(getattr(args, "outline_only", False))
        else config.include_copper,
        include_board_outline=False
        if bool(getattr(args, "no_board_outline", False))
        else config.include_board_outline,
        include_poured_polygons=False
        if bool(getattr(args, "exclude_poured_polygons", False))
        else config.include_poured_polygons,
        cut_holes=False if bool(getattr(args, "no_hole_cuts", False)) else config.cut_holes,
        drill_hole_mode="none"
        if bool(getattr(args, "no_hole_cuts", False))
        else str(_arg_or_config(args, "drill_hole_mode", config.drill_hole_mode)),
        max_boolean_drill_cuts=int(
            _arg_or_config(
                args,
                "max_boolean_drill_cuts",
                config.max_boolean_drill_cuts,
            )
        ),
        drill_hole_color=str(
            _arg_or_config(args, "drill_hole_color", config.drill_hole_color)
        ),
        drill_overlay_thickness_mm=float(
            _arg_or_config(
                args,
                "drill_overlay_thickness_mm",
                config.drill_overlay_thickness_mm,
            )
        ),
        fuse_copper=False if bool(getattr(args, "no_fuse", False)) else config.fuse_copper,
        fuse_board_outline=False
        if bool(getattr(args, "no_fuse", False))
        else config.fuse_board_outline,
        arc_segments=int(_arg_or_config(args, "arc_segments", config.arc_segments)),
    )


def _arg_or_config(args, name: str, config_value):
    value = getattr(args, name, None)
    return config_value if value is None else value


def _resolve_input_files(file_arg: str | Path | None) -> list[Path] | None:
    if file_arg:
        input_file = Path(file_arg).resolve()
        if not input_file.exists():
            log.error("File not found: %s", input_file)
            return None
        suffix = input_file.suffix.lower()
        if suffix not in {".pcbdoc", ".prjpcb"}:
            log.error("Unsupported file type: %s", suffix)
            log.info("Supported PCB layer STEP types: .PcbDoc, .PrjPcb")
            return None
        return [input_file]

    prjpcbs = find_prjpcbs_in_cwd()
    if prjpcbs:
        log.info(
            "Auto-detected %d project file(s) for PCB layer STEP generation",
            len(prjpcbs),
        )
        return prjpcbs
    pcbdocs = find_pcbdocs_in_cwd()
    if pcbdocs:
        log.info(
            "Auto-detected %d standalone PcbDoc file(s) for PCB layer STEP generation",
            len(pcbdocs),
        )
        return pcbdocs

    log.error("No file specified and no .PrjPcb/.PcbDoc found in current directory")
    log.info("Usage: altium-cruncher pcb-layer-step [project.PrjPcb | board.PcbDoc]")
    return None


def register_parser(subparsers):
    parser = subparsers.add_parser(
        "pcb-layer-step",
        help="generate a colored STEP model for one PCB layer",
        description=(
            "Generate a STEP model for one selected Altium PCB layer. "
            "The default is a bottom-copper alignment model with drilled holes cut out "
            "and a separate board-outline body."
        ),
        epilog="Examples:\n"
        "  altium-cruncher pcb-layer-step board.PcbDoc\n"
        "  altium-cruncher pcb-layer-step project.PrjPcb --doc board.PcbDoc --layer bottom\n"
        "  altium-cruncher pcb-layer-step board.PcbDoc --exclude-poured-polygons\n"
        "  altium-cruncher pcb-layer-step board.PcbDoc --outline-only\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="PcbDoc or PrjPcb file (optional if auto-detected in CWD)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output directory (default: ./output/pcb-layer-step)",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help=(
            "path to pcb-layer-step JSON/JSONC config. "
            f"If omitted, pcb-layer-step looks for {PCB_LAYER_STEP_CONFIG_FILENAME} "
            "next to each input file; if missing, it creates a template and uses defaults."
        ),
    )
    parser.add_argument(
        "--doc",
        "--pcbdoc",
        dest="pcbdoc",
        type=str,
        help="with .PrjPcb input, select a specific PcbDoc by filename, stem, or relative path",
    )
    parser.add_argument(
        "--project-context",
        choices=["auto", "none", "schematic"],
        default="auto",
        help="project-context mode for standalone PcbDoc inputs (default: auto)",
    )
    parser.add_argument(
        "--layer",
        default=None,
        help="PCB layer selector: bottom, top, BOTTOM, TOP, layer id, or layer display name",
    )
    parser.add_argument(
        "--thickness-mm",
        type=float,
        default=None,
        help="extruded layer thickness in millimeters (default: 0.035)",
    )
    parser.add_argument(
        "--z-mm",
        type=float,
        default=None,
        help="bottom Z position in millimeters (default: 0)",
    )
    parser.add_argument(
        "--copper-color",
        default=None,
        help="STEP color for selected-layer copper, #RRGGBB or #AARRGGBB (default: #B87333)",
    )
    parser.add_argument(
        "--outline-width-mm",
        type=float,
        default=None,
        help="board-outline body width in millimeters (default: 0.2)",
    )
    parser.add_argument(
        "--outline-color",
        default=None,
        help="STEP color for board outline, #RRGGBB or #AARRGGBB (default: #111111)",
    )
    parser.add_argument(
        "--exclude-poured-polygons",
        action="store_true",
        help="exclude poured-polygon/rendered-region geometry from the selected layer",
    )
    parser.add_argument(
        "--outline-only",
        action="store_true",
        help="emit only the board outline body",
    )
    parser.add_argument(
        "--no-board-outline",
        action="store_true",
        help="do not include the board-outline body",
    )
    parser.add_argument(
        "--no-hole-cuts",
        action="store_true",
        help="do not subtract or overlay pad/via drill holes in copper geometry",
    )
    parser.add_argument(
        "--drill-hole-mode",
        choices=["auto", "cut", "overlay", "none"],
        default=None,
        help=(
            "drill-hole handling: auto cuts small boards and overlays dense boards, "
            "cut uses precise booleans, overlay uses fast visible disks, none omits them"
        ),
    )
    parser.add_argument(
        "--max-boolean-drill-cuts",
        type=int,
        default=None,
        help="auto mode uses boolean drill cuts up to this count (default: 128)",
    )
    parser.add_argument(
        "--drill-hole-color",
        default=None,
        help="STEP color for drill overlays, #RRGGBB or #AARRGGBB (default: #FFFFFF)",
    )
    parser.add_argument(
        "--drill-overlay-thickness-mm",
        type=float,
        default=None,
        help="thickness for fast drill-overlay disks in millimeters (default: 0.001)",
    )
    parser.add_argument(
        "--no-fuse",
        action="store_true",
        help="preserve primitive-level copper and board-outline regions instead of requesting Geometer 2D fusion",
    )
    parser.add_argument(
        "--arc-segments",
        type=int,
        default=None,
        help="fallback sampling resolution for non-circular curves such as elliptical pads (default: 32)",
    )
    parser.set_defaults(handler=cmd_pcb_layer_step)
    return parser
