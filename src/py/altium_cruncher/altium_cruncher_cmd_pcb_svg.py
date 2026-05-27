"""pcb-svg command for explicit A0 PCB SVG views."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from altium_cruncher.altium_cruncher_common import (
    _resolve_output_dir,
    find_pcbdocs_in_cwd,
    find_prjpcbs_in_cwd,
)
from altium_cruncher.altium_cruncher_pcb_svg_a0_renderer import (
    render_pcb_svg_a0_to_output,
)
from altium_cruncher.altium_cruncher_pcb_svg_config import (
    PCB_DEFAULT_SVG_SCALE,
    PCB_SVG_CONFIG_FILENAME,
    PCB_SVG_CONFIG_SCHEMA,
    PcbSvgConfig,
    PcbSvgGlobalConfig,
    PcbSvgViewConfig,
    parse_pcb_layer_selector,
)
from altium_cruncher.config_json import load_json_config

log = logging.getLogger(__name__)

_VIEW_ALIASES = {
    "top": "top_view",
    "top-view": "top_view",
    "bottom": "bottom_view",
    "bottom-view": "bottom_view",
    "cutout": "board_cutouts",
    "cutouts": "board_cutouts",
    "board-cutouts": "board_cutouts",
    "board_cutouts": "board_cutouts",
}


def _default_pcb_svg_config_text() -> str:
    """Return the JSONC text used for auto-created PCB SVG configs."""
    payload = json.dumps(PcbSvgConfig.default().to_dict(), indent=2)
    return (
        "// altium-cruncher pcb-svg configuration\n"
        "// This file is JSONC: // comments, /* block comments */, and trailing commas are accepted.\n"
        "// Schema: pcb.svg.config.a0\n"
        "// Common physical layer tokens: TOP, BOTTOM, TOPOVERLAY, BOTTOMOVERLAY, TOPPASTE,\n"
        "//   BOTTOMPASTE, TOPSOLDER, BOTTOMSOLDER, and MECHANICAL_1..MECHANICAL_32.\n"
        "// Synthetic layer tokens: BOARD_OUTLINE, BOARD_CUTOUTS, DRILLS, SLOTS,\n"
        "//   ASSEMBLY_HLR_TOP, ASSEMBLY_HLR_BOTTOM.\n"
        "// In each view, the layers array is the draw order. HLR renders last, and\n"
        "//   DRILLS/SLOTS render immediately before HLR.\n"
        "// With .PrjPcb input, add global.pcbdoc to select one specific board.\n"
        "// Set layer_outputs.enabled=false if you only want composed views.\n"
        f"{payload}\n"
    )


def _write_default_pcb_svg_config(config_path: Path) -> None:
    """Write an editable A0 pcb-svg config template."""
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        _default_pcb_svg_config_text(),
        encoding="utf-8",
    )


def _load_pcb_svg_config(config_path: Path) -> PcbSvgConfig:
    try:
        raw_data = load_json_config(config_path)
    except Exception as exc:
        raise ValueError(f"Failed to parse pcb-svg config '{config_path}': {exc}") from exc
    return PcbSvgConfig.from_dict(raw_data)


def _parse_pcb_views(raw_views: str | None) -> set[str] | None:
    if raw_views is None:
        return None
    values = [token.strip().lower() for token in raw_views.split(",") if token.strip()]
    if not values:
        return None
    selected: set[str] = set()
    for value in values:
        normalized = value.replace("_", "-")
        if normalized == "all":
            return {"all"}
        if normalized == "none":
            selected.add("none")
            continue
        if normalized in {"layers", "layer", "layer-outputs"}:
            selected.add("layers")
            continue
        selected.add(_VIEW_ALIASES.get(normalized, value.replace("-", "_")))
    return selected


def _apply_pcb_view_selection(
    config: PcbSvgConfig,
    raw_views: str | None,
) -> PcbSvgConfig:
    """Apply CLI view filtering to an A0 config."""
    selected = _parse_pcb_views(raw_views)
    if selected is None or "all" in selected:
        return config
    if "none" in selected and len(selected) == 1:
        config.layer_outputs["enabled"] = False
        for view in config.views:
            view.enabled = False
        return config

    config.layer_outputs["enabled"] = "layers" in selected
    known_names = {view.name for view in config.views}
    requested_views = selected - {"layers", "none"}
    unknown = requested_views - known_names
    if unknown:
        raise ValueError(
            "Unknown --views token(s): "
            + ", ".join(sorted(unknown))
            + ". Use a configured view name, layers, all, or none."
        )
    for view in config.views:
        view.enabled = view.name in requested_views
    return config


def _apply_pcb_layer_selection(
    config: PcbSvgConfig,
    raw_layers: str | None,
) -> PcbSvgConfig:
    """Apply CLI layer filtering to A0 layer outputs."""
    selected_layers = parse_pcb_layer_selector(raw_layers)
    if selected_layers is not None:
        config.layer_outputs["layers"] = selected_layers
    return config


def _resolve_view_render_settings(
    global_options: PcbSvgGlobalConfig,
    view: PcbSvgViewConfig,
    *,
    default_svg_scale: float | None = None,
    default_svg_size_unit: str | None = None,
) -> dict[str, object]:
    """Return the effective A0 render settings for one view."""
    config = PcbSvgConfig(global_options=global_options, views=[view])
    styles = config.resolved_styles_for_view(view)
    cutout_style = styles.get("board_cutouts", {})
    outline_style = str(cutout_style.get("outline_style", "solid")).lower()
    if outline_style not in {"solid", "dashed"}:
        raise ValueError(
            f"Invalid board_cutouts.outline_style '{outline_style}' for view '{view.name}'"
        )
    for field_name in (
        "hatch_spacing_mm",
        "hatch_line_width_mm",
        "outline_dash_mm",
        "outline_width_mm",
    ):
        value = cutout_style.get(field_name, 0.01)
        if not isinstance(value, (int, float, str)) or float(value) <= 0:
            raise ValueError(
                f"Invalid board_cutouts.{field_name} for view '{view.name}'"
            )
    svg_scale = (
        global_options.svg_scale if default_svg_scale is None else default_svg_scale
    )
    svg_size_unit = (
        global_options.svg_size_unit
        if default_svg_size_unit is None
        else default_svg_size_unit
    )
    return {
        "layers": list(view.layers),
        "mirror": view.mirror,
        "assembly_hlr_mode": view.assembly_hlr_mode,
        "styles": styles,
        "svg_scale": float(svg_scale),
        "svg_size_unit": str(svg_size_unit or ""),
    }


def _resolve_pcb_svg_configs(
    args: object,
    input_files: list[Path],
) -> tuple[dict[Path, PcbSvgConfig], list[Path]]:
    """Resolve one A0 pcb-svg config per input file."""
    resolved_input_files = [path.resolve() for path in input_files]
    created_paths: list[Path] = []
    config_by_input: dict[Path, PcbSvgConfig] = {}
    config_cache: dict[Path, PcbSvgConfig] = {}

    raw_config = getattr(args, "config", None)
    if raw_config:
        explicit_config_path = Path(raw_config).resolve()
        if not explicit_config_path.exists():
            _write_default_pcb_svg_config(explicit_config_path)
            created_paths.append(explicit_config_path)
        loaded_config = _load_pcb_svg_config(explicit_config_path)
        _apply_cli_overrides(loaded_config, args)
        for input_file in resolved_input_files:
            config_by_input[input_file] = loaded_config
        return config_by_input, created_paths

    for input_file in resolved_input_files:
        auto_config_path = input_file.parent / PCB_SVG_CONFIG_FILENAME
        if not auto_config_path.exists():
            _write_default_pcb_svg_config(auto_config_path)
            created_paths.append(auto_config_path)

    for input_file in resolved_input_files:
        auto_config_path = input_file.parent / PCB_SVG_CONFIG_FILENAME
        loaded = config_cache.get(auto_config_path)
        if loaded is None:
            loaded = _load_pcb_svg_config(auto_config_path)
            _apply_cli_overrides(loaded, args)
            config_cache[auto_config_path] = loaded
        config_by_input[input_file] = loaded

    return config_by_input, sorted(set(created_paths))


def _apply_cli_overrides(config: PcbSvgConfig, args: object) -> None:
    pcbdoc = getattr(args, "pcbdoc", None)
    if pcbdoc:
        config.global_options.pcbdoc = str(pcbdoc)
    _apply_pcb_view_selection(config, getattr(args, "pcb_views", None))
    _apply_pcb_layer_selection(config, getattr(args, "pcb_layers", None))
    svg_scale = getattr(args, "pcb_svg_scale", None)
    if svg_scale is not None:
        config.global_options.svg_scale = float(svg_scale)
    svg_size_unit = getattr(args, "pcb_svg_size_unit", None)
    if svg_size_unit is not None:
        config.global_options.svg_size_unit = str(svg_size_unit)
    if getattr(args, "pcb_clean_output", False):
        config.global_options.clean_output = True


def resolve_pcb_svg_configs(
    args: object,
    input_files: list[Path],
) -> tuple[dict[Path, PcbSvgConfig], list[Path]]:
    """Public wrapper for resolving A0 pcb-svg configs."""
    return _resolve_pcb_svg_configs(args, input_files)


def render_pcb_views_from_inputs(
    args: object,
    input_files: list[Path],
    output_dir: Path,
    config_by_input: dict[Path, PcbSvgConfig],
) -> int:
    """Render PCB SVG A0 outputs from resolved inputs/config."""
    return render_pcb_svg_a0_to_output(args, input_files, output_dir, config_by_input)


def cmd_pcb_svg(args: object) -> int:
    """Handle pcb-svg subcommand."""
    input_files: list[Path]
    raw_file = getattr(args, "file", None)
    if raw_file:
        input_file = Path(raw_file).resolve()
        if not input_file.exists():
            log.error("File not found: %s", input_file)
            return 1
        suffix = input_file.suffix.lower()
        if suffix not in {".pcbdoc", ".prjpcb"}:
            log.error("Unsupported file type: %s", suffix)
            log.info("Supported PCB SVG types: .PcbDoc, .PrjPcb")
            return 1
        input_files = [input_file]
    else:
        prjpcbs = find_prjpcbs_in_cwd()
        if prjpcbs:
            input_files = prjpcbs
            log.info("Auto-detected %s project file(s)", len(prjpcbs))
        else:
            pcbdocs = find_pcbdocs_in_cwd()
            if not pcbdocs:
                log.error(
                    "No file specified and no .PrjPcb/.PcbDoc found in current directory"
                )
                log.info("Usage: altium-cruncher pcb-svg [project.PrjPcb | board.PcbDoc]")
                return 1
            input_files = pcbdocs
            log.info("Auto-detected %s standalone PcbDoc file(s)", len(pcbdocs))

    try:
        config_by_input, created_configs = resolve_pcb_svg_configs(args, input_files)
    except ValueError as exc:
        log.error(str(exc))
        return 1

    if created_configs:
        for config_path in created_configs:
            log.info("Created pcb-svg config template: %s", config_path)
        log.info("pcb-svg config template created and defaulted for this invocation.")

    output_dir = _resolve_output_dir(getattr(args, "output", None), "pcb-svg")
    return render_pcb_views_from_inputs(args, input_files, output_dir, config_by_input)


def add_pcb_svg_option_arguments(
    parser: argparse.ArgumentParser,
    *,
    include_legacy_pcb_flag: bool = False,
) -> None:
    """Add shared PCB SVG flags to pcb-svg and the combined svg command."""
    if include_legacy_pcb_flag:
        parser.add_argument(
            "--pcb",
            action="store_true",
            help="legacy compatibility flag for svg shortcut (no-op for pcb-svg)",
        )
    parser.add_argument(
        "--config",
        type=Path,
        help=(
            f"path to {PCB_SVG_CONFIG_SCHEMA} JSON/JSONC config. If omitted, pcb-svg "
            f"uses {PCB_SVG_CONFIG_FILENAME} next to each input file, creating "
            "a template when missing."
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
        "--views",
        "--pcb-views",
        dest="pcb_views",
        type=str,
        help="comma-separated view names plus layers, all, or none",
    )
    parser.add_argument(
        "--layers",
        "--pcb-layers",
        dest="pcb_layers",
        type=str,
        help="comma-separated physical PCB layers for layer outputs",
    )
    parser.add_argument(
        "--scale",
        dest="pcb_svg_scale",
        type=float,
        default=None,
        help=f"display scale multiplier for SVG width/height attrs (default: {PCB_DEFAULT_SVG_SCALE})",
    )
    parser.add_argument(
        "--svg-size-unit",
        "--pcb-svg-size-unit",
        dest="pcb_svg_size_unit",
        type=str,
        default=None,
        help="optional size unit suffix for SVG width/height attrs (for example mm or px)",
    )
    parser.add_argument(
        "--clean-output",
        "--pcb-clean-output",
        dest="pcb_clean_output",
        action="store_true",
        help="reserved for A0 output cleanup; current renderer overwrites configured outputs",
    )
    parser.add_argument(
        "--export",
        "--pcb-export",
        dest="pcb_export",
        choices=["board", "layers", "bundle", "outline"],
        default="board",
        help="legacy compatibility option; A0 output selection is config-driven",
    )


def register_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    pcb_svg_parser = subparsers.add_parser(
        "pcb-svg",
        help="generate PCB SVG views from Altium PcbDoc/PrjPcb",
        description=(
            "Generate config-driven PCB SVG layer outputs and explicit composed "
            f"views using {PCB_SVG_CONFIG_SCHEMA}."
        ),
        epilog=(
            "Examples:\n"
            "  altium-cruncher pcb-svg board.PcbDoc\n"
            f"  altium-cruncher pcb-svg project.PrjPcb --config {PCB_SVG_CONFIG_FILENAME}\n"
            "  altium-cruncher pcb-svg board.PcbDoc --views top,bottom,layers\n"
            "  altium-cruncher pcb-svg -o output_dir/"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    pcb_svg_parser.add_argument(
        "file",
        nargs="?",
        help="PcbDoc or PrjPcb file (optional if auto-detected in CWD)",
    )
    pcb_svg_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output directory (default: ./output/pcb-svg)",
    )
    add_pcb_svg_option_arguments(pcb_svg_parser)
    pcb_svg_parser.set_defaults(handler=cmd_pcb_svg)
    return pcb_svg_parser


__all__ = [
    "PCB_SVG_CONFIG_FILENAME",
    "PCB_SVG_CONFIG_SCHEMA",
    "PcbSvgConfig",
    "PcbSvgGlobalConfig",
    "PcbSvgViewConfig",
    "_apply_pcb_layer_selection",
    "_apply_pcb_view_selection",
    "_resolve_view_render_settings",
    "add_pcb_svg_option_arguments",
    "cmd_pcb_svg",
    "render_pcb_views_from_inputs",
    "resolve_pcb_svg_configs",
]
