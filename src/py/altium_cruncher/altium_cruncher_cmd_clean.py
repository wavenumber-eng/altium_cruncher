"""clean command for altium_cruncher."""

from __future__ import annotations

import argparse
import json
import logging
import shutil
from pathlib import Path

from altium_cruncher.altium_clean import (
    AltiumCleanConfig,
    apply_clean_to_schdoc,
    apply_clean_to_schlib,
    infer_clean_config_path,
)
from altium_cruncher.altium_pcblib_clean import (
    DEFAULT_PCBLIB_CLEAN_CONFIG_FILENAME,
    PcbLibCleanConfig,
    apply_clean_to_pcblib,
    infer_pcblib_clean_config_path,
)
from altium_cruncher.altium_cruncher_common import find_prjpcb_in_cwd
from altium_cruncher.config_json import load_json_config

log = logging.getLogger(__name__)

DEFAULT_SCH_CLEAN_CONFIG_FILENAME = "altium-clean.json"
_SCHEMATIC_CONFIG_SUFFIX = ".schdoc"
_PCBLIB_CONFIG_SUFFIX = ".pcblib"

_SCHEMATIC_CLEAN_COMMENTS: dict[str, tuple[str, ...]] = {
    "schema": (
        "Schematic clean config for .SchDoc, .SchLib, and .PrjPcb inputs.",
        "This file is JSONC: // comments and trailing commas are accepted.",
        "Use --init-config to write this template without cleaning an input.",
        "Use --force-config with --init-config to overwrite an existing template.",
    ),
    "enabled": (
        "Set enabled=false to leave this rule family unchanged.",
    ),
    "font_name": (
        "Altium font family name to apply.",
    ),
    "size_pt": (
        "Font size in points.",
    ),
    "bold": (
        "Whether the generated font is bold.",
    ),
    "italic": (
        "Whether the generated font is italic.",
    ),
    "color_win32": (
        "Win32/BGR integer color. The loader also accepts #RRGGBB or integer strings.",
    ),
    "normalize_pin_fonts": (
        "Pin name/designator fonts inside symbols.",
        "Set enabled=false if library pin text is already curated.",
    ),
    "normalize_pin_fonts.name_font": (
        "Style for visible pin names.",
    ),
    "normalize_pin_fonts.designator_font": (
        "Style for visible pin designators/numbers.",
    ),
    "normalize_symbol_body_rectangles": (
        "Main symbol body rectangles. Width/height thresholds avoid touching tiny graphics.",
        "line_width accepts smallest/zero, small, medium, large, or the Altium enum integer.",
    ),
    "normalize_symbol_body_rectangles.min_width_mils": (
        "Only rectangles wider than this many mils are treated as symbol bodies.",
    ),
    "normalize_symbol_body_rectangles.min_height_mils": (
        "Only rectangles taller than this many mils are treated as symbol bodies.",
    ),
    "normalize_symbol_body_rectangles.outline_color_win32": (
        "Rectangle outline color.",
    ),
    "normalize_symbol_body_rectangles.line_width": (
        "Outline width: smallest/zero, small, medium, large, or enum integer.",
    ),
    "normalize_symbol_body_rectangles.fill_color_win32": (
        "Rectangle fill color.",
    ),
    "normalize_symbol_body_rectangles.is_solid": (
        "Whether the rectangle fill is solid.",
    ),
    "normalize_symbol_body_rectangles.transparent": (
        "Whether the rectangle fill should be transparent.",
    ),
    "normalize_power_symbols": (
        "Power-port text and color normalization for schematic sheets.",
        "Colors may be Win32/BGR integers, 0xRRGGBB-style strings, or #RRGGBB.",
    ),
    "normalize_power_symbols.font": (
        "Font applied to power-port text.",
    ),
    "normalize_net_labels": (
        "Net-label text style and color normalization.",
        "Use this to make copied/vendor sheets match the project drawing standard.",
    ),
    "normalize_net_labels.font": (
        "Font applied to net-label text.",
    ),
    "normalize_component_designators": (
        "Placed component designator text, for example U1/R3/C10.",
        "Font specs use font_name, size_pt, bold, italic, and optional color_win32/color.",
    ),
    "normalize_component_designators.font": (
        "Font applied to component designator text.",
    ),
    "normalize_component_parameters": (
        "Visible component parameter text such as value or part-number fields.",
        "This does not rename parameter keys; it only normalizes displayed text style.",
    ),
    "normalize_component_parameters.font": (
        "Font applied to visible component parameter text.",
    ),
    "normalize_component_free_text": (
        "Free text owned by a component rather than board/sheet-level free text.",
        "Useful for vendor symbols with inconsistent internal notes.",
    ),
    "normalize_component_free_text.font_name": (
        "Font family applied to component-owned free text.",
    ),
    "normalize_wires": (
        "Schematic wire color normalization.",
        "This intentionally avoids net labels and power symbols; those have separate rules.",
    ),
    "normalize_no_erc": (
        "No-ERC marker appearance.",
        "symbol accepts cross, thin cross, small cross, checkbox, triangle, or enum integer.",
    ),
    "normalize_no_erc.symbol": (
        "Marker style: cross, thin cross, small cross, checkbox, triangle, or enum integer.",
    ),
    "normalize_sheet_style": (
        "Sheet border/area colors and document title-block font.",
        "PrjPcb input applies this rule to every SchDoc listed by the project.",
    ),
    "normalize_sheet_style.line_color_win32": (
        "Sheet border line color.",
    ),
    "normalize_sheet_style.area_color_win32": (
        "Sheet background/area color.",
    ),
    "normalize_sheet_style.document_font": (
        "Font applied to sheet document/title-block text.",
    ),
    "normalize_symbol_internal_graphics_monochrome": (
        "Symbol-owned internal graphics, such as lines, polygons, arcs, and fills.",
        "saturation=0 makes graphics monochrome while preserving relative intensity.",
    ),
    "normalize_symbol_internal_graphics_monochrome.saturation": (
        "Target saturation from 0.0 monochrome to 1.0 unchanged.",
    ),
}

_PCBLIB_CLEAN_COMMENTS: dict[str, tuple[str, ...]] = {
    "schema": (
        "PcbLib clean config for footprint-library cleanup.",
        "This file is JSONC: // comments and trailing commas are accepted.",
        "Use --init-config to write this template without cleaning an input.",
        "Use --force-config with --init-config to overwrite an existing template.",
        "The default profile removes vendor drafting noise while preserving 3D bodies.",
    ),
    "enabled": (
        "Set enabled=false to leave this rule family unchanged.",
    ),
    "profile": (
        "Human-readable rule profile name written to clean reports.",
        "Use separate config files for different vendor/library cleanup policies.",
    ),
    "remove_mechanical_primitives": (
        "Remove mechanical-layer tracks, arcs, fills, and similar drafting primitives.",
        "Preserve options protect component bodies, board cutouts, keepouts, and custom pads.",
    ),
    "remove_mechanical_primitives.primitive_types": (
        "Primitive collections to remove; supported values include tracks, arcs, fills, and texts.",
    ),
    "remove_mechanical_primitives.layers": (
        "Layer policy for primitive removal, for example mechanical or any.",
    ),
    "remove_mechanical_primitives.preserve_regions": (
        "Keep regions even if mechanical primitive removal is enabled.",
    ),
    "remove_mechanical_primitives.preserve_component_bodies": (
        "Keep component-body/3D-model related primitives.",
    ),
    "remove_text_strings": (
        "Remove configured PcbLib text strings, often vendor labels on mechanical layers.",
        "Match by layer, text content, or both depending on the nested rule options.",
    ),
    "remove_text_strings.layers": (
        "Layer policy for text removal, for example any or mechanical.",
    ),
    "remove_text_strings.match": (
        "Text matching mode: all, regex, contains, or exact.",
    ),
    "remove_text_strings.patterns": (
        "Text patterns used when match is regex, contains, or exact.",
    ),
    "remove_regions": (
        "Remove configured mechanical regions.",
        "Use cautiously: the rule has preservation flags for keepouts and custom-pad regions.",
    ),
    "remove_regions.layers": (
        "Layer policy for region removal, for example mechanical or any.",
    ),
    "remove_regions.preserve_component_linked": (
        "Keep regions linked to a footprint component object.",
    ),
    "remove_regions.preserve_model_associated": (
        "Keep regions associated with embedded or generated models.",
    ),
    "remove_regions.preserve_keepouts": (
        "Keep keepout regions.",
    ),
    "remove_regions.preserve_board_cutouts": (
        "Keep board-cutout regions.",
    ),
    "remove_regions.preserve_custom_pad_regions": (
        "Keep regions used to represent custom pads.",
    ),
}


def _find_input_in_cwd() -> Path | None:
    prjpcb = find_prjpcb_in_cwd()
    if prjpcb is not None:
        return prjpcb.resolve()

    candidates = sorted(
        [
            p
            for p in Path.cwd().iterdir()
            if p.is_file() and p.suffix.lower() in {".schdoc", ".schlib", ".pcblib"}
        ],
        key=lambda p: p.name.lower(),
    )
    if len(candidates) == 1:
        return candidates[0]
    return None


def _resolve_output_path(input_file: Path, output_arg: Path | None) -> Path:
    if output_arg is None:
        return input_file

    resolved = output_arg.resolve()
    if resolved.exists() and resolved.is_dir():
        return (resolved / input_file.name).resolve()
    return resolved


def _resolve_backup_path(input_file: Path, backup_path_arg: Path | None) -> Path:
    if backup_path_arg is not None:
        return backup_path_arg.resolve()
    return input_file.with_name(f"{input_file.name}.bak").resolve()


def _project_relative_path(project_file: Path, document_file: Path) -> Path:
    project_dir = project_file.parent.resolve()
    document_resolved = document_file.resolve()
    try:
        return document_resolved.relative_to(project_dir)
    except ValueError:
        return Path(document_file.name)


def _resolve_project_output_root(output_arg: Path | None) -> Path | None:
    if output_arg is None:
        return None
    output_root = output_arg.resolve()
    if output_root.exists() and output_root.is_file():
        raise ValueError(f"For .PrjPcb clean, --output must be a directory: {output_root}")
    output_root.mkdir(parents=True, exist_ok=True)
    return output_root


def _resolve_project_backup_root(backup_path_arg: Path | None) -> Path | None:
    if backup_path_arg is None:
        return None
    backup_root = backup_path_arg.resolve()
    if backup_root.exists() and backup_root.is_file():
        raise ValueError(f"For .PrjPcb clean, --backup-path must be a directory: {backup_root}")
    backup_root.mkdir(parents=True, exist_ok=True)
    return backup_root


def _write_config_template(path: Path, *, suffix: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    template = (
        PcbLibCleanConfig.template().to_dict()
        if suffix == _PCBLIB_CONFIG_SUFFIX
        else AltiumCleanConfig.template().to_dict()
    )
    comments = (
        _PCBLIB_CLEAN_COMMENTS
        if suffix == _PCBLIB_CONFIG_SUFFIX
        else _SCHEMATIC_CLEAN_COMMENTS
    )
    path.write_text(_render_jsonc_template(template, comments), encoding="utf-8")


def _render_jsonc_template(
    template: dict[str, object],
    comments: dict[str, tuple[str, ...]],
) -> str:
    """Render a JSONC config template with section guidance comments."""
    lines: list[str] = [
        "// Generated by altium-cruncher clean.",
        "// Edit enabled flags and rule values, then rerun the same command.",
        "// Use --output or --backup when trying a new rule set on real designs.",
        "{",
    ]
    lines.extend(_render_jsonc_object_fields(template, comments, path=(), indent=2))
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def _render_jsonc_object_fields(
    data: dict[str, object],
    comments: dict[str, tuple[str, ...]],
    *,
    path: tuple[str, ...],
    indent: int,
) -> list[str]:
    lines: list[str] = []
    keys = list(data)
    for index, key in enumerate(keys):
        if index:
            lines.append("")
        current_path = (*path, key)
        lines.extend(_comment_lines(comments, current_path, indent=indent))
        comma = "," if index < len(keys) - 1 else ""
        lines.extend(
            _render_jsonc_property(
                key,
                data[key],
                comments,
                path=current_path,
                indent=indent,
                comma=comma,
            )
        )
    return lines


def _render_jsonc_property(
    key: str,
    value: object,
    comments: dict[str, tuple[str, ...]],
    *,
    path: tuple[str, ...],
    indent: int,
    comma: str,
) -> list[str]:
    space = " " * indent
    if isinstance(value, dict):
        lines = [f'{space}"{key}": {{']
        lines.extend(
            _render_jsonc_object_fields(
                value,
                comments,
                path=path,
                indent=indent + 2,
            )
        )
        lines.append(f"{space}}}{comma}")
        return lines

    value_text = json.dumps(value, indent=2)
    value_lines = value_text.splitlines()
    if len(value_lines) == 1:
        return [f'{space}"{key}": {value_lines[0]}{comma}']
    lines = [f'{space}"{key}": {value_lines[0]}']
    lines.extend(f"{space}{line}" for line in value_lines[1:-1])
    lines.append(f"{space}{value_lines[-1]}{comma}")
    return lines


def _comment_lines(
    comments: dict[str, tuple[str, ...]],
    path: tuple[str, ...],
    *,
    indent: int,
) -> list[str]:
    key = ".".join(path)
    comment_text = comments.get(key)
    if comment_text is None:
        comment_text = comments.get(path[-1], ())
    space = " " * indent
    return [f"{space}// {comment}" for comment in comment_text]


def _suffix_from_config_type(config_type: str | None) -> str | None:
    if config_type is None:
        return None
    return _PCBLIB_CONFIG_SUFFIX if config_type == "pcblib" else _SCHEMATIC_CONFIG_SUFFIX


def _resolve_config_suffix(
    *,
    input_file: Path | None,
    config_type: str | None,
) -> str:
    config_suffix = _suffix_from_config_type(config_type)
    if input_file is None:
        if config_suffix is None:
            raise ValueError("--init-config without a file requires --config-type")
        return config_suffix

    input_suffix = input_file.suffix.lower()
    input_config_suffix = (
        _PCBLIB_CONFIG_SUFFIX if input_suffix == ".pcblib" else _SCHEMATIC_CONFIG_SUFFIX
    )
    if config_suffix is not None and config_suffix != input_config_suffix:
        raise ValueError(
            f"--config-type {config_type} does not match input file type {input_suffix}"
        )
    return input_config_suffix


def _resolve_config_template_path(
    args: argparse.Namespace,
    input_file: Path | None,
    *,
    suffix: str,
) -> Path:
    if args.config:
        return Path(args.config).resolve()
    if input_file is None:
        filename = (
            DEFAULT_PCBLIB_CLEAN_CONFIG_FILENAME
            if suffix == _PCBLIB_CONFIG_SUFFIX
            else DEFAULT_SCH_CLEAN_CONFIG_FILENAME
        )
        return (Path.cwd() / filename).resolve()
    if suffix == _PCBLIB_CONFIG_SUFFIX:
        return infer_pcblib_clean_config_path(input_file).resolve()
    return infer_clean_config_path(
        input_file,
        config_filename=DEFAULT_SCH_CLEAN_CONFIG_FILENAME,
    ).resolve()


def _init_clean_config(
    args: argparse.Namespace,
    input_file: Path | None,
    *,
    suffix: str,
) -> int:
    config_path = _resolve_config_template_path(args, input_file, suffix=suffix)
    if config_path.exists() and not getattr(args, "force_config", False):
        log.error(
            "Config already exists: %s. Use --force-config to overwrite.",
            config_path,
        )
        return 1
    _write_config_template(config_path, suffix=suffix)
    log.info("Created clean config template: %s", config_path)
    log.info("Edit the config, then run clean without --init-config.")
    return 0


def _resolve_clean_input(args: argparse.Namespace) -> Path | None:
    if args.file:
        input_file = Path(args.file).resolve()
        if not input_file.exists() and not getattr(args, "init_config", False):
            raise FileNotFoundError(f"File not found: {input_file}")
        return input_file

    if getattr(args, "init_config", False) and getattr(args, "config_type", None):
        return None

    detected = _find_input_in_cwd()
    if detected is None:
        raise ValueError(
            "No input specified and no unique .PrjPcb/.SchDoc/.SchLib/.PcbLib "
            "found in current directory"
        )
    log.info(f"Auto-detected input file: {detected.name}")
    return detected


def _maybe_init_clean_config(
    args: argparse.Namespace,
    input_file: Path | None,
) -> int | None:
    try:
        config_suffix = _resolve_config_suffix(
            input_file=input_file,
            config_type=getattr(args, "config_type", None),
        )
    except ValueError as exc:
        log.error(str(exc))
        return 1

    if not getattr(args, "init_config", False):
        return None
    return _init_clean_config(args, input_file, suffix=config_suffix)


def _resolve_clean_config(
    args: argparse.Namespace,
    input_file: Path,
) -> tuple[AltiumCleanConfig | PcbLibCleanConfig | None, Path | None]:
    suffix = input_file.suffix.lower()
    if args.config:
        config_path = Path(args.config).resolve()
        if not config_path.exists():
            raise ValueError(f"Config file not found: {config_path}")
    else:
        config_path = (
            infer_pcblib_clean_config_path(input_file)
            if suffix == _PCBLIB_CONFIG_SUFFIX
            else infer_clean_config_path(
                input_file,
                config_filename=DEFAULT_SCH_CLEAN_CONFIG_FILENAME,
            )
        )
        if not config_path.exists():
            _write_config_template(config_path, suffix=suffix)
            return None, config_path

    try:
        raw = load_json_config(config_path)
    except Exception as exc:
        raise ValueError(f"Invalid JSON in clean config: {config_path}: {exc}") from exc

    if suffix == _PCBLIB_CONFIG_SUFFIX:
        return PcbLibCleanConfig.from_dict(raw), config_path
    return AltiumCleanConfig.from_dict(raw), config_path


def cmd_clean(args: argparse.Namespace) -> int:
    from altium_monkey.altium_prjpcb import AltiumPrjPcb
    from altium_monkey.altium_pcblib import AltiumPcbLib
    from altium_monkey.altium_schdoc import AltiumSchDoc
    from altium_monkey.altium_schlib import AltiumSchLib

    try:
        input_file = _resolve_clean_input(args)
    except (FileNotFoundError, ValueError) as exc:
        log.error(str(exc))
        log.info(
            "Usage: altium-cruncher clean "
            "[project.PrjPcb | file.SchDoc | file.SchLib | file.PcbLib]"
        )
        return 1

    init_result = _maybe_init_clean_config(args, input_file)
    if init_result is not None:
        return init_result

    assert input_file is not None
    suffix = input_file.suffix.lower()
    if suffix not in {".prjpcb", ".schdoc", ".schlib", ".pcblib"}:
        log.error(f"Unsupported file type for clean: {suffix}")
        log.info("Supported clean types: .PrjPcb, .SchDoc, .SchLib, .PcbLib")
        return 1

    try:
        config, created_template = _resolve_clean_config(args, input_file)
    except ValueError as exc:
        log.error(str(exc))
        return 1

    if config is None and created_template is not None:
        log.info(f"Created clean config template: {created_template}")
        log.info("Edit the config, then rerun the clean command.")
        return 0

    assert config is not None

    if suffix == ".prjpcb":
        if not isinstance(config, AltiumCleanConfig):
            log.error(".PrjPcb clean requires an Altium schematic clean config")
            return 1
        try:
            project = AltiumPrjPcb(input_file)
            schdoc_files = project.get_schdoc_paths()
        except Exception as exc:
            log.error(f"Error loading project: {input_file}: {exc}")
            return 1

        if not schdoc_files:
            log.error(f"No SchDoc files found in project: {input_file}")
            return 1
        log.info(f"Found {len(schdoc_files)} SchDoc file(s) in project")

        try:
            output_root = _resolve_project_output_root(args.output)
            backup_root = _resolve_project_backup_root(args.backup_path) if args.backup else None
        except ValueError as exc:
            log.error(str(exc))
            return 1

        project_dir = input_file.parent.resolve()
        total_pins = 0
        updated_name_fonts = 0
        updated_designator_fonts = 0
        total_rectangles = 0
        matched_rectangles = 0
        updated_rectangles = 0
        total_power_symbols = 0
        updated_power_symbol_colors = 0
        updated_power_symbol_fonts = 0
        total_net_labels = 0
        updated_net_label_colors = 0
        updated_net_label_fonts = 0
        total_component_designators = 0
        updated_component_designator_colors = 0
        updated_component_designator_fonts = 0
        total_component_parameters = 0
        updated_component_parameter_colors = 0
        updated_component_parameter_fonts = 0
        total_component_free_texts = 0
        updated_component_free_text_colors = 0
        updated_component_free_text_fonts = 0
        total_wires = 0
        updated_wire_colors = 0
        total_no_ercs = 0
        updated_no_erc_colors = 0
        updated_no_erc_symbols = 0
        total_sheets = 0
        updated_sheet_line_colors = 0
        updated_sheet_area_colors = 0
        updated_sheet_document_fonts = 0
        total_symbol_internal_graphics = 0
        updated_symbol_internal_graphic_stroke_colors = 0
        updated_symbol_internal_graphic_fill_colors = 0
        success_count = 0

        for schdoc_path in schdoc_files:
            rel_path = _project_relative_path(input_file, schdoc_path)
            output_file = ((output_root / rel_path) if output_root else schdoc_path).resolve()
            output_file.parent.mkdir(parents=True, exist_ok=True)

            if args.backup:
                if backup_root is not None:
                    backup_target = (backup_root / rel_path).resolve()
                    backup_path = backup_target.with_name(f"{backup_target.name}.bak")
                else:
                    backup_path = _resolve_backup_path(schdoc_path, None)
                if backup_path == schdoc_path:
                    log.error("Backup path cannot be the same as the input file: %s", schdoc_path)
                    return 1
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(schdoc_path, backup_path)
                try:
                    backup_rel = backup_path.relative_to(project_dir)
                    log.info("Backup created: %s", backup_rel.as_posix())
                except ValueError:
                    log.info("Backup created: %s", backup_path)

            try:
                schdoc = AltiumSchDoc(schdoc_path)
                result = apply_clean_to_schdoc(schdoc, config)
                schdoc.save(output_file)
                total_pins += result.total_pins
                updated_name_fonts += result.updated_name_fonts
                updated_designator_fonts += result.updated_designator_fonts
                total_rectangles += result.total_rectangles
                matched_rectangles += result.matched_rectangles
                updated_rectangles += result.updated_rectangles
                total_power_symbols += result.total_power_symbols
                updated_power_symbol_colors += result.updated_power_symbol_colors
                updated_power_symbol_fonts += result.updated_power_symbol_fonts
                total_net_labels += result.total_net_labels
                updated_net_label_colors += result.updated_net_label_colors
                updated_net_label_fonts += result.updated_net_label_fonts
                total_component_designators += result.total_component_designators
                updated_component_designator_colors += result.updated_component_designator_colors
                updated_component_designator_fonts += result.updated_component_designator_fonts
                total_component_parameters += result.total_component_parameters
                updated_component_parameter_colors += result.updated_component_parameter_colors
                updated_component_parameter_fonts += result.updated_component_parameter_fonts
                total_component_free_texts += result.total_component_free_texts
                updated_component_free_text_colors += result.updated_component_free_text_colors
                updated_component_free_text_fonts += result.updated_component_free_text_fonts
                total_wires += result.total_wires
                updated_wire_colors += result.updated_wire_colors
                total_no_ercs += result.total_no_ercs
                updated_no_erc_colors += result.updated_no_erc_colors
                updated_no_erc_symbols += result.updated_no_erc_symbols
                total_sheets += result.total_sheets
                updated_sheet_line_colors += result.updated_sheet_line_colors
                updated_sheet_area_colors += result.updated_sheet_area_colors
                updated_sheet_document_fonts += result.updated_sheet_document_fonts
                total_symbol_internal_graphics += result.total_symbol_internal_graphics
                updated_symbol_internal_graphic_stroke_colors += result.updated_symbol_internal_graphic_stroke_colors
                updated_symbol_internal_graphic_fill_colors += result.updated_symbol_internal_graphic_fill_colors
                success_count += 1
                try:
                    in_rel = schdoc_path.resolve().relative_to(project_dir).as_posix()
                except ValueError:
                    in_rel = str(schdoc_path)
                try:
                    out_rel = output_file.resolve().relative_to(project_dir).as_posix()
                except ValueError:
                    out_rel = str(output_file)
                log.info(
                    (
                        "Cleaned %s -> %s (pins=%d, name_font_updates=%d, designator_font_updates=%d, "
                        "rectangles=%d, matched_rectangles=%d, rectangle_updates=%d, "
                        "power_symbols=%d, power_color_updates=%d, power_font_updates=%d, "
                        "net_labels=%d, net_label_color_updates=%d, net_label_font_updates=%d, "
                        "component_designators=%d, component_designator_color_updates=%d, component_designator_font_updates=%d, "
                        "component_parameters=%d, component_parameter_color_updates=%d, component_parameter_font_updates=%d, "
                        "component_free_texts=%d, component_free_text_color_updates=%d, component_free_text_font_updates=%d, "
                        "wires=%d, wire_color_updates=%d, "
                        "no_ercs=%d, no_erc_color_updates=%d, no_erc_style_updates=%d, "
                        "sheets=%d, sheet_line_color_updates=%d, sheet_area_color_updates=%d, sheet_document_font_updates=%d, "
                        "symbol_internal_graphics=%d, symbol_internal_graphic_stroke_updates=%d, "
                        "symbol_internal_graphic_fill_updates=%d)"
                    ),
                    in_rel,
                    out_rel,
                    result.total_pins,
                    result.updated_name_fonts,
                    result.updated_designator_fonts,
                    result.total_rectangles,
                    result.matched_rectangles,
                    result.updated_rectangles,
                    result.total_power_symbols,
                    result.updated_power_symbol_colors,
                    result.updated_power_symbol_fonts,
                    result.total_net_labels,
                    result.updated_net_label_colors,
                    result.updated_net_label_fonts,
                    result.total_component_designators,
                    result.updated_component_designator_colors,
                    result.updated_component_designator_fonts,
                    result.total_component_parameters,
                    result.updated_component_parameter_colors,
                    result.updated_component_parameter_fonts,
                    result.total_component_free_texts,
                    result.updated_component_free_text_colors,
                    result.updated_component_free_text_fonts,
                    result.total_wires,
                    result.updated_wire_colors,
                    result.total_no_ercs,
                    result.updated_no_erc_colors,
                    result.updated_no_erc_symbols,
                    result.total_sheets,
                    result.updated_sheet_line_colors,
                    result.updated_sheet_area_colors,
                    result.updated_sheet_document_fonts,
                    result.total_symbol_internal_graphics,
                    result.updated_symbol_internal_graphic_stroke_colors,
                    result.updated_symbol_internal_graphic_fill_colors,
                )
            except Exception as exc:
                log.error("Error cleaning %s: %s", schdoc_path, exc)

        if success_count != len(schdoc_files):
            log.warning("Clean complete with errors: cleaned=%d/%d", success_count, len(schdoc_files))
            log.info(
                (
                    "Clean summary: pins=%d, name_font_updates=%d, designator_font_updates=%d, "
                    "rectangles=%d, matched_rectangles=%d, rectangle_updates=%d, "
                    "power_symbols=%d, power_color_updates=%d, power_font_updates=%d, "
                    "net_labels=%d, net_label_color_updates=%d, net_label_font_updates=%d, "
                    "component_designators=%d, component_designator_color_updates=%d, component_designator_font_updates=%d, "
                    "component_parameters=%d, component_parameter_color_updates=%d, component_parameter_font_updates=%d, "
                    "component_free_texts=%d, component_free_text_color_updates=%d, component_free_text_font_updates=%d, "
                    "wires=%d, wire_color_updates=%d, "
                    "no_ercs=%d, no_erc_color_updates=%d, no_erc_style_updates=%d, "
                    "sheets=%d, sheet_line_color_updates=%d, sheet_area_color_updates=%d, sheet_document_font_updates=%d, "
                    "symbol_internal_graphics=%d, symbol_internal_graphic_stroke_updates=%d, "
                    "symbol_internal_graphic_fill_updates=%d"
                ),
                total_pins,
                updated_name_fonts,
                updated_designator_fonts,
                total_rectangles,
                matched_rectangles,
                updated_rectangles,
                total_power_symbols,
                updated_power_symbol_colors,
                updated_power_symbol_fonts,
                total_net_labels,
                updated_net_label_colors,
                updated_net_label_fonts,
                total_component_designators,
                updated_component_designator_colors,
                updated_component_designator_fonts,
                total_component_parameters,
                updated_component_parameter_colors,
                updated_component_parameter_fonts,
                total_component_free_texts,
                updated_component_free_text_colors,
                updated_component_free_text_fonts,
                total_wires,
                updated_wire_colors,
                total_no_ercs,
                updated_no_erc_colors,
                updated_no_erc_symbols,
                total_sheets,
                updated_sheet_line_colors,
                updated_sheet_area_colors,
                updated_sheet_document_fonts,
                total_symbol_internal_graphics,
                updated_symbol_internal_graphic_stroke_colors,
                updated_symbol_internal_graphic_fill_colors,
            )
            return 1

        log.info(
            (
                "Clean complete: schdocs=%d, pins=%d, name_font_updates=%d, designator_font_updates=%d, "
                "rectangles=%d, matched_rectangles=%d, rectangle_updates=%d, "
                "power_symbols=%d, power_color_updates=%d, power_font_updates=%d, "
                "net_labels=%d, net_label_color_updates=%d, net_label_font_updates=%d, "
                "component_designators=%d, component_designator_color_updates=%d, component_designator_font_updates=%d, "
                "component_parameters=%d, component_parameter_color_updates=%d, component_parameter_font_updates=%d, "
                "component_free_texts=%d, component_free_text_color_updates=%d, component_free_text_font_updates=%d, "
                "wires=%d, wire_color_updates=%d, "
                "no_ercs=%d, no_erc_color_updates=%d, no_erc_style_updates=%d, "
                "sheets=%d, sheet_line_color_updates=%d, sheet_area_color_updates=%d, sheet_document_font_updates=%d, "
                "symbol_internal_graphics=%d, symbol_internal_graphic_stroke_updates=%d, "
                "symbol_internal_graphic_fill_updates=%d"
            ),
            success_count,
            total_pins,
            updated_name_fonts,
            updated_designator_fonts,
            total_rectangles,
            matched_rectangles,
            updated_rectangles,
            total_power_symbols,
            updated_power_symbol_colors,
            updated_power_symbol_fonts,
            total_net_labels,
            updated_net_label_colors,
            updated_net_label_fonts,
            total_component_designators,
            updated_component_designator_colors,
            updated_component_designator_fonts,
            total_component_parameters,
            updated_component_parameter_colors,
            updated_component_parameter_fonts,
            total_component_free_texts,
            updated_component_free_text_colors,
            updated_component_free_text_fonts,
            total_wires,
            updated_wire_colors,
            total_no_ercs,
            updated_no_erc_colors,
            updated_no_erc_symbols,
            total_sheets,
            updated_sheet_line_colors,
            updated_sheet_area_colors,
            updated_sheet_document_fonts,
            total_symbol_internal_graphics,
            updated_symbol_internal_graphic_stroke_colors,
            updated_symbol_internal_graphic_fill_colors,
        )
        return 0

    output_file = _resolve_output_path(input_file, args.output)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    if args.backup:
        backup_path = _resolve_backup_path(input_file, args.backup_path)
        if backup_path == input_file:
            log.error("Backup path cannot be the same as the input file")
            return 1
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(input_file, backup_path)
        log.info(f"Backup created: {backup_path}")

    if suffix == ".pcblib":
        if not isinstance(config, PcbLibCleanConfig):
            log.error(".PcbLib clean requires a PcbLib clean config")
            return 1
        pcblib = AltiumPcbLib.from_file(input_file)
        pcblib_result = apply_clean_to_pcblib(pcblib, config)
        pcblib.save(output_file)
        log.info(
            (
                "PcbLib clean complete: footprints=%d, removed=%d, by_type=%s, "
                "by_layer=%s, output=%s"
            ),
            pcblib_result.total_footprints,
            pcblib_result.total_removed,
            pcblib_result.removed_by_collection,
            pcblib_result.removed_by_layer,
            output_file,
        )
        return 0

    if not isinstance(config, AltiumCleanConfig):
        log.error("SchDoc/SchLib clean requires an Altium schematic clean config")
        return 1
    if suffix == ".schdoc":
        schdoc = AltiumSchDoc(input_file)
        result = apply_clean_to_schdoc(schdoc, config)
        schdoc.save(output_file)
    else:
        schlib = AltiumSchLib(input_file)
        result = apply_clean_to_schlib(schlib, config)
        schlib.save(output_file, sync_pin_text_data=True)

    log.info(
        (
            "Clean complete: pins=%d, name_font_updates=%d, designator_font_updates=%d, "
            "rectangles=%d, matched_rectangles=%d, rectangle_updates=%d, "
            "power_symbols=%d, power_color_updates=%d, power_font_updates=%d, "
            "net_labels=%d, net_label_color_updates=%d, net_label_font_updates=%d, "
            "component_designators=%d, component_designator_color_updates=%d, component_designator_font_updates=%d, "
            "component_parameters=%d, component_parameter_color_updates=%d, component_parameter_font_updates=%d, "
            "component_free_texts=%d, component_free_text_color_updates=%d, component_free_text_font_updates=%d, "
            "wires=%d, wire_color_updates=%d, "
            "no_ercs=%d, no_erc_color_updates=%d, no_erc_style_updates=%d, "
            "sheets=%d, sheet_line_color_updates=%d, sheet_area_color_updates=%d, sheet_document_font_updates=%d, "
            "symbol_internal_graphics=%d, symbol_internal_graphic_stroke_updates=%d, "
            "symbol_internal_graphic_fill_updates=%d, output=%s"
        ),
        result.total_pins,
        result.updated_name_fonts,
        result.updated_designator_fonts,
        result.total_rectangles,
        result.matched_rectangles,
        result.updated_rectangles,
        result.total_power_symbols,
        result.updated_power_symbol_colors,
        result.updated_power_symbol_fonts,
        result.total_net_labels,
        result.updated_net_label_colors,
        result.updated_net_label_fonts,
        result.total_component_designators,
        result.updated_component_designator_colors,
        result.updated_component_designator_fonts,
        result.total_component_parameters,
        result.updated_component_parameter_colors,
        result.updated_component_parameter_fonts,
        result.total_component_free_texts,
        result.updated_component_free_text_colors,
        result.updated_component_free_text_fonts,
        result.total_wires,
        result.updated_wire_colors,
        result.total_no_ercs,
        result.updated_no_erc_colors,
        result.updated_no_erc_symbols,
        result.total_sheets,
        result.updated_sheet_line_colors,
        result.updated_sheet_area_colors,
        result.updated_sheet_document_fonts,
        result.total_symbol_internal_graphics,
        result.updated_symbol_internal_graphic_stroke_colors,
        result.updated_symbol_internal_graphic_fill_colors,
        output_file,
    )
    return 0


def register_parser(subparsers):
    clean_parser = subparsers.add_parser(
        "clean",
        help="normalize Altium SchDoc/SchLib/PcbLib assets using JSON/JSONC config",
        description=(
            "Normalize schematic symbol/document styles for SchDoc, SchLib, and PrjPcb files, "
            "and clean PcbLib vendor footprint mechanical drafting noise. "
            "Supports pin name/designator font normalization, symbol body rectangle normalization, "
            "schematic power symbol normalization, schematic net-label normalization, "
            "component designator/parameter font normalization, component free-text normalization, "
            "schematic wire normalization, schematic no-erc normalization, sheet-style normalization, and "
            "symbol internal-graphics monochrome normalization. For PcbLib input, supports JSON/JSONC-configured "
            "mechanical-layer primitive removal, configured text-string removal, and "
            "configured mechanical-region removal while preserving component bodies and embedded models."
        ),
        epilog=(
            "Examples:\n"
            "  altium-cruncher clean device.SchLib --init-config\n"
            "  altium-cruncher clean --init-config --config-type pcblib --config altium-pcblib-clean.json\n"
            "  altium-cruncher clean device.SchLib\n"
            "  altium-cruncher clean sheet.SchDoc --config altium-clean.json\n"
            "  altium-cruncher clean footprint.PcbLib --config altium-pcblib-clean.json\n"
            "  altium-cruncher clean project.PrjPcb --output cleaned_schdocs/\n"
            "  altium-cruncher clean device.SchLib --backup --output cleaned/Device.SchLib"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    clean_parser.add_argument(
        "file",
        nargs="?",
        help=(
            "PrjPcb, SchDoc, SchLib, or PcbLib file "
            "(optional if one is auto-detected in CWD)"
        ),
    )
    clean_parser.add_argument(
        "--config",
        type=Path,
        help=(
            "Path to clean JSON/JSONC config. "
            f"For SchDoc/SchLib/PrjPcb, omitted means {DEFAULT_SCH_CLEAN_CONFIG_FILENAME} "
            "next to input. "
            f"For PcbLib, omitted means workspace config {DEFAULT_PCBLIB_CLEAN_CONFIG_FILENAME} "
            "when available, otherwise the same filename next to input. "
            "If the resolved config is missing, creates a template and exits."
        ),
    )
    clean_parser.add_argument(
        "--init-config",
        action="store_true",
        help=(
            "Write the appropriate commented JSONC config template and exit "
            "without loading or cleaning the input file"
        ),
    )
    clean_parser.add_argument(
        "--config-type",
        choices=("schematic", "pcblib"),
        help=(
            "Config template type for --init-config when no input file is supplied; "
            "schematic covers PrjPcb, SchDoc, and SchLib inputs"
        ),
    )
    clean_parser.add_argument(
        "--force-config",
        action="store_true",
        help="Allow --init-config to overwrite an existing config file",
    )
    clean_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help=(
            "Output file path for SchDoc/SchLib/PcbLib, or output directory for PrjPcb "
            "(default: in-place overwrite)"
        ),
    )
    clean_parser.add_argument(
        "--backup",
        action="store_true",
        help="Create a backup copy of the input file before writing output",
    )
    clean_parser.add_argument(
        "--backup-path",
        type=Path,
        help=(
            "Explicit backup file path for SchDoc/SchLib/PcbLib, or backup directory for PrjPcb "
            "(default: <input>.bak when --backup is set)"
        ),
    )
    clean_parser.set_defaults(handler=cmd_clean)
    return clean_parser
