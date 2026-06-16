"""Mate config template and seed projection helpers."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from altium_cruncher.altium_cruncher_mco import JsonObject
from altium_cruncher.altium_cruncher_mate_defaults import (
    default_mate_artifacts_payload,
    default_mate_board_projection_payload,
    default_mate_designators_payload,
    default_mate_label_placement_payload,
    default_mate_label_style_payload,
    default_mate_output_payload,
)
from altium_cruncher.config_json import enum_help, render_commented_jsonc

_MATE_CONFIG_COMMENT_BY_PATH = {
    ("schema",): "Mate config contract id.",
    ("source",): "DUT source board input and load policy.",
    ("source", "board"): "Path to the DUT .PrjPcb or .PcbDoc.",
    ("source", "project_context"): enum_help(
        "Project loading mode.",
        ("auto", "none", "schematic"),
    ),
    ("output",): "Generated mate project output settings.",
    ("output", "backend"): enum_help(
        "Output backend.",
        ("altium",),
    ),
    ("output", "output_dir"): "Directory for generated project and artifacts.",
    ("output", "project_name"): "Base name for generated project documents.",
    ("output", "schematic_sheet_style"): (
        "Generated schematic sheet size/style, such as D."
    ),
    ("output", "origin"): "How generated output coordinates are initialized.",
    ("output", "board_outline"): "Generated output-board outline policy.",
    ("output", "board_outline", "mode"): enum_help(
        "Generated board-outline mode.",
        (
            "source_bounds",
            "match_source_bounds",
            "match_bounds",
            "source_bounds_with_margin",
            "source_bounds_plus_margin",
            "padded_rectangle",
            "padded_source_bounds",
        ),
    ),
    ("output", "board_outline", "margin_mils"): (
        "Board-outline expansion around source bounds in mils."
    ),
    ("output", "overwrite"): "Allow replacing existing generated output files.",
    ("output", "layer_stack_template"): (
        "Layer stack template id. Options are supplied by altium-monkey; "
        "the generated default uses 2-layer."
    ),
    ("libraries",): "Library roots used to resolve mate symbols and footprints.",
    ("libraries", "roots"): "Directories scanned for SchLib/PcbLib files.",
    ("libraries", "recursive"): "Scan library roots recursively when true.",
    ("validation",): "Source-side validation and ambiguity handling.",
    ("validation", "source_side"): enum_help(
        "How the source mount side is inferred.",
        ("infer_single_side", "any", "none", "top", "bottom"),
    ),
    ("validation", "allow_side_agnostic_through_hole"): (
        "Allow through-hole mate targets to be used across source sides."
    ),
    ("validation", "side_agnostic_kinds"): (
        "Projection kinds allowed to ignore source side."
    ),
    ("projections",): "Named DUT feature groups projected into the mate output.",
    ("projections", "id"): "Stable projection id referenced by actions/artifacts.",
    ("projections", "source"): "DUT source selector for this projection.",
    ("projections", "source", "object"): enum_help(
        "Source object kind.",
        ("component", "free_pad"),
    ),
    ("projections", "source", "designators"): (
        "Designator wildcard/range expression, such as TP* or M1-4."
    ),
    ("projections", "source", "hole_size_mils"): ("Free-pad hole-size filter in mils."),
    ("projections", "source", "hole_size_mils", "min"): (
        "Minimum accepted hole size in mils."
    ),
    ("projections", "source", "hole_size_mils", "max"): (
        "Maximum accepted hole size in mils."
    ),
    ("projections", "source", "plated"): "Free-pad plating filter.",
    ("projections", "actions"): "Actions applied to each matched source object.",
    ("projections", "actions", "kind"): enum_help(
        "Action kind.",
        ("mate_component", "reference_graphics", "label"),
    ),
    ("projections", "actions", "part"): (
        "Known-parts manifest id for seeded mate_component actions."
    ),
    ("projections", "actions", "symbol_name"): (
        "Schematic symbol name for explicit mate_component actions."
    ),
    ("projections", "actions", "footprint_name"): (
        "PCB footprint name for explicit mate_component actions."
    ),
    ("projections", "actions", "designator_prefix"): (
        "Generated mate component designator prefix."
    ),
    ("projections", "actions", "signal_pad_designator"): (
        "Pad designator used for generated signal routing."
    ),
    ("projections", "actions", "shape"): enum_help(
        "Reference graphics shape mode.",
        ("source_pad_outline", "destination_pad_outline"),
    ),
    ("projections", "actions", "layer"): "Target Altium layer for this action.",
    ("projections", "actions", "style"): "Action-specific display/text style.",
    ("projections", "actions", "text"): "Label text source, such as source_net.",
    ("projections", "actions", "placement"): "Label placement policy object.",
    ("pcb_designators",): "PCB-side component designator normalization settings.",
    ("pcb_designators", "enabled"): "Enable generated designator normalization.",
    ("pcb_designators", "placement"): enum_help(
        "Designator placement mode.",
        ("above_component",),
    ),
    ("pcb_designators", "offset_mils"): "Designator placement offset in mils.",
    ("pcb_designators", "width_factor"): "Text width scaling factor.",
    ("pcb_designators", "style"): "Generated designator text style.",
    ("board_projection",): "Reference graphics copied from the DUT board.",
    ("board_projection", "outline"): "DUT board-outline reference graphics.",
    ("board_projection", "outline", "graphics"): (
        "Board-outline drawing operation settings."
    ),
    ("board_projection", "cutouts"): "DUT board-cutout reference behavior.",
    ("board_projection", "cutouts", "graphics"): (
        "Board-cutout drawing operation settings."
    ),
    ("board_projection", "cutouts", "scope"): enum_help(
        "Board-cutout projection filter.",
        ("all", "interior"),
    ),
    ("board_projection", "cutouts", "actual_cutouts"): (
        "Create actual board cutouts when true; otherwise graphics only."
    ),
    ("artifacts",): "Optional generated artifacts produced by mate planning/runs.",
    ("artifacts", "pcb_layer_step"): (
        "PCB layer STEP artifact generated with the same defaults as "
        "pcb-layer-step --init-config."
    ),
    ("artifacts", "pcb_layer_step", "enabled"): (
        "Enable a local STEP model of the selected DUT PCB layer."
    ),
    ("artifacts", "pcb_layer_step", "source_layer"): enum_help(
        "DUT PCB layer selector passed to pcb-layer-step.",
        ("bottom", "top", "native layer name", "layer id"),
    ),
    ("artifacts", "pcb_layer_step", "z_mm"): (
        "Bottom Z plane for the exported local STEP bodies."
    ),
    ("artifacts", "pcb_layer_step", "thickness_mm"): (
        "Nominal extrusion thickness for selected copper features."
    ),
    ("artifacts", "pcb_layer_step", "include_board_outline"): (
        "Include separate board-outline bodies for visual registration."
    ),
    ("artifacts", "pcb_layer_step", "board_outline"): (
        "Board outline and cutout body styling."
    ),
    ("artifacts", "pcb_layer_step", "board_outline", "color"): (
        "STEP color for the outer board outline body."
    ),
    ("artifacts", "pcb_layer_step", "board_outline", "cutout_color"): (
        "STEP color for interior board cutout outline bodies."
    ),
    ("artifacts", "pcb_layer_step", "board_outline", "cutouts"): (
        "Include separate outline bodies around interior board cutouts."
    ),
    ("artifacts", "pcb_layer_step", "board_outline", "width_mm"): (
        "Outline stroke body width in millimeters."
    ),
    ("artifacts", "pcb_layer_step", "board_outline", "fuse"): (
        "Request planar fusion for board-outline bodies."
    ),
    ("artifacts", "pcb_layer_step", "features"): (
        "Copper feature selection, color, body-name, and thickness-bias policy."
    ),
    ("artifacts", "pcb_layer_step", "features", "defaults"): (
        "Fallback feature styling when a feature does not override it."
    ),
    ("artifacts", "pcb_layer_step", "features", "component_pads"): (
        "Component-owned pad selection and styling."
    ),
    ("artifacts", "pcb_layer_step", "features", "free_pads"): (
        "Pads not owned by a PCB component."
    ),
    ("artifacts", "pcb_layer_step", "features", "tracks"): ("Copper track primitives."),
    ("artifacts", "pcb_layer_step", "features", "arcs"): ("Copper arc primitives."),
    ("artifacts", "pcb_layer_step", "features", "fills"): ("Copper fill primitives."),
    ("artifacts", "pcb_layer_step", "features", "polygons"): (
        "Poured polygon copper primitives."
    ),
    ("artifacts", "pcb_layer_step", "features", "regions"): (
        "Non-polygon copper region primitives."
    ),
    ("artifacts", "pcb_layer_step", "features", "vias"): ("Via copper pad primitives."),
    ("artifacts", "pcb_layer_step", "features", "component_pads", "mode"): enum_help(
        "Component pad mode.",
        ("none", "all", "matching_designators"),
    ),
    (
        "artifacts",
        "pcb_layer_step",
        "features",
        "component_pads",
        "include_designators",
    ): ("Case-insensitive shell-style component designator patterns to include."),
    ("artifacts", "pcb_layer_step", "features", "component_pads", "highlight_rules"): (
        "Rules that split matching pads into separately colored STEP bodies."
    ),
    (
        "artifacts",
        "pcb_layer_step",
        "features",
        "component_pads",
        "highlight_rules",
        "designators",
    ): ("Case-insensitive shell-style designator patterns for this highlight."),
    ("artifacts", "pcb_layer_step", "drills"): ("Drill and slot visualization policy."),
    ("artifacts", "pcb_layer_step", "drills", "mode"): enum_help(
        "Global drill mode.",
        ("auto", "cut", "overlay", "none"),
    ),
    ("artifacts", "pcb_layer_step", "drills", "selected_component_mode"): enum_help(
        "Drill mode for pads selected by component_pads.",
        ("inherit", "cut", "overlay", "none"),
    ),
    ("artifacts", "pcb_layer_step", "drills", "other_component_mode"): enum_help(
        "Drill mode for unselected component-owned pads.",
        ("inherit", "cut", "overlay", "none"),
    ),
    ("artifacts", "pcb_layer_step", "drills", "free_pad_mode"): enum_help(
        "Drill mode for pads not owned by a component.",
        ("inherit", "cut", "overlay", "none"),
    ),
    ("artifacts", "pcb_layer_step", "drills", "via_mode"): enum_help(
        "Drill mode for via holes.",
        ("inherit", "cut", "overlay", "none"),
    ),
    ("artifacts", "pcb_layer_step", "drills", "minimum_diameter_mm"): (
        "Omit drill overlays/cuts below this diameter."
    ),
    ("artifacts", "pcb_layer_step", "drills", "shape"): enum_help(
        "Overlay shape.",
        ("solid", "ring"),
    ),
    ("artifacts", "pcb_layer_step", "drills", "color"): (
        "Default STEP color for drill overlay bodies."
    ),
    ("artifacts", "pcb_layer_step", "drills", "plated_color"): (
        "STEP color for plated drill overlay bodies."
    ),
    ("artifacts", "pcb_layer_step", "drills", "non_plated_color"): (
        "STEP color for non-plated drill overlay bodies."
    ),
    ("artifacts", "pcb_layer_step", "drills", "ring_width_mm"): (
        "Fixed annulus width when drill shape is ring."
    ),
    ("artifacts", "pcb_layer_step", "drills", "plated_ring_shape"): enum_help(
        "Plated drill ring policy.",
        ("annulus",),
    ),
    ("artifacts", "pcb_layer_step", "drills", "overlay_thickness_mm"): (
        "Z thickness for separate drill overlay bodies."
    ),
    ("artifacts", "pcb_layer_step", "fuse_copper"): (
        "Request Geometer planar fusion for copper bodies."
    ),
    ("artifacts", "pcb_layer_step", "insert_in_output"): (
        "Insert the generated STEP artifact into the mate output PcbDoc."
    ),
    ("artifacts", "pcb_layer_step", "insert_in_output", "enabled"): (
        "Enable embedding the STEP model in the generated output board."
    ),
    ("artifacts", "pcb_layer_step", "insert_in_output", "z_mm"): (
        "Model placement Z in the generated output board."
    ),
    ("artifacts", "pcb_layer_step", "insert_in_output", "layer"): enum_help(
        "Altium layer used for the embedded STEP model.",
        ("native layer name", "layer id"),
    ),
    ("artifacts", "pcb_layer_step", "insert_in_output", "side"): enum_help(
        "Board side used for the embedded STEP model.",
        ("TOP", "BOTTOM", "native projection enum id"),
    ),
    ("artifacts", "pcb_layer_step", "highlights"): (
        "Projection-driven extra highlight geometries added to the artifact."
    ),
    ("artifacts", "pcb_layer_step", "highlights", "projection"): (
        "Projection id whose source pad geometries should be highlighted."
    ),
    ("artifacts", "pcb_layer_step", "highlights", "color"): (
        "STEP color for this projection highlight."
    ),
}

_MATE_CONFIG_COMMENT_BY_KEY = {
    "enabled": "Enable this feature body.",
    "color": "STEP color for this body or rule.",
    "step_body_name": "Stable Geometer STEP body id/name.",
    "thickness_bias_mm": (
        "Symmetric Z bias that prevents overlapping colored bodies from z-fighting."
    ),
    "designators": "Case-insensitive shell-style designator patterns.",
    "side": enum_help(
        "Board side selector.",
        ("top", "bottom", "left", "right", "board_left", "board_right"),
    ),
    "layer": enum_help(
        "Altium layer selector.",
        ("native layer name", "layer id"),
    ),
    "style": "Rendering or text style object.",
    "graphics": "Graphics output settings.",
    "height_mils": "Text height in mils.",
    "font_kind": enum_help(
        "Text font kind.",
        ("truetype", "stroke", "barcode"),
    ),
    "font_name": "Free-form text font face name.",
    "bold": "Render text in bold when true.",
    "stroke_width_mils": "Stroke width in mils.",
    "text_justification": enum_help(
        "Altium text justification.",
        ("Altium text justification enum name", "native enum id"),
    ),
    "mode": "Mode selector for this object; see the field-specific comment for options.",
    "offset_mils": "XY offset in mils.",
    "box_size_mils": "Label box width and height in mils.",
    "row_spacing_mils": "Vertical spacing between generated label rows.",
    "column_spacing_mils": "Horizontal spacing between generated label columns.",
    "auto_width_padding_mils": "Extra padding added to auto-sized label boxes.",
}


def mate_seed_projections(inspection: Mapping[str, object]) -> list[JsonObject]:
    """Build default mate projections from inspection output."""
    projections: list[JsonObject] = []
    test_points = _mate_seed_component_designators(inspection, "test_point")
    if test_points:
        projections.append(_mate_seed_test_points_projection(test_points))
    mounts = _mate_seed_component_designators(inspection, "mount")
    if mounts:
        projections.append(_mate_seed_mounts_projection(mounts))
    free_npths = _mate_seed_alignment_pads(inspection)
    if free_npths:
        projections.append(_mate_seed_alignment_pins_projection(free_npths))
    return projections


def mate_template_text(
    *,
    schema: str,
    source_board: Path | str | None = None,
) -> str:
    """Return the editable default mate JSONC template text."""
    payload = _mate_template_payload(schema=schema, source_board=source_board)
    payload_text = mate_config_payload_text(payload)
    return (
        "/*\n"
        "  altium-cruncher mate config a0\n"
        "\n"
        "  Edit source.board to the DUT .PrjPcb or .PcbDoc, place any required\n"
        "  SchLib/PcbLib files under libraries.roots, and then run:\n"
        "\n"
        "      altium-cruncher mate\n"
        "\n"
        "  mate_component actions resolve symbol_name and footprint_name by\n"
        "  scanning the configured library roots. The generated MCO is a derived\n"
        "  artifact; keep this config as the human-authored source of truth.\n"
        "\n"
        "  Generated mate config sections are JSONC-commented from the config\n"
        "  help registry. artifacts.pcb_layer_step is generated from the same\n"
        "  default payload as pcb-layer-step --init-config.\n"
        "*/\n"
        f"{payload_text}\n"
    )


def mate_config_payload_text(payload: JsonObject) -> str:
    """Render a mate config payload as commented JSONC."""
    return render_commented_jsonc(
        payload,
        comments_by_path=_MATE_CONFIG_COMMENT_BY_PATH,
        comments_by_key=_MATE_CONFIG_COMMENT_BY_KEY,
    ).rstrip()


def _mate_config_comment_maps() -> tuple[
    Mapping[tuple[str, ...] | str, str | tuple[str, ...]],
    Mapping[str, str | tuple[str, ...]],
]:
    return (
        _MATE_CONFIG_COMMENT_BY_PATH,
        _MATE_CONFIG_COMMENT_BY_KEY,
    )


def _mate_seed_component_designators(
    inspection: Mapping[str, object],
    kind: str,
) -> list[str]:
    designators = [
        str(component.get("designator", "") or "")
        for board in _list_field(inspection, "boards")
        if isinstance(board, dict)
        for component in _list_field(board, "components")
        if isinstance(component, dict) and component.get("kind") == kind
    ]
    return sorted(set(designators), key=_designator_sort_key)


def _mate_seed_alignment_pads(inspection: Mapping[str, object]) -> list[JsonObject]:
    return [
        dict(pad)
        for board in _list_field(inspection, "boards")
        if isinstance(board, dict)
        for pad in _list_field(board, "free_pads")
        if isinstance(pad, dict)
        and pad.get("kind") == "free_npth"
        and _is_mate_seed_alignment_hole(pad)
    ]


def _is_mate_seed_alignment_hole(pad: Mapping[str, object]) -> bool:
    hole_size = pad.get("hole_size_mils")
    return (
        isinstance(hole_size, int | float)
        and not isinstance(hole_size, bool)
        and 75.0 <= float(hole_size) <= 85.0
    )


def _mate_seed_test_points_projection(designators: list[str]) -> JsonObject:
    return {
        "id": "test_points",
        "source": {
            "object": "component",
            "designators": _designator_expression(designators),
        },
        "actions": [
            {"kind": "mate_component", "part": "test_point_pogo"},
            default_mate_reference_graphics_payload(),
            {
                "kind": "label",
                "text": "source_net",
                "placement": default_mate_label_placement_payload(),
                "style": default_mate_label_style_payload(),
            },
        ],
    }


def _mate_seed_mounts_projection(designators: list[str]) -> JsonObject:
    return {
        "id": "mounts",
        "source": {
            "object": "component",
            "designators": _designator_expression(designators),
        },
        "actions": [
            {"kind": "mate_component", "part": "m25_smt_standoff"},
            default_mate_reference_graphics_payload(),
        ],
    }


def _mate_seed_alignment_pins_projection(_pads: list[JsonObject]) -> JsonObject:
    return {
        "id": "alignment_pins",
        "source": {
            "object": "free_pad",
            "hole_size_mils": {"min": 75, "max": 85},
            "plated": False,
        },
        "actions": [
            {"kind": "mate_component", "part": "alignment_pin_2mm_npth"},
            default_mate_reference_graphics_payload(),
            {
                "kind": "label",
                "text": "source_net",
                "placement": default_mate_label_placement_payload(),
                "style": default_mate_label_style_payload(),
            },
        ],
    }


def default_mate_reference_graphics_payload() -> JsonObject:
    return {
        "kind": "reference_graphics",
        "shape": "source_pad_outline",
        "layer": "MECHANICAL_1",
        "style": {
            "mode": "outline",
            "outline_count": 1,
            "clearance_mils": 10,
            "stroke_width_mils": 10,
        },
    }


def _mate_template_payload(
    *,
    schema: str,
    source_board: Path | str | None,
) -> JsonObject:
    source_board_text = (
        str(source_board).replace("\\", "/")
        if source_board is not None
        else "path/to/dut.PrjPcb"
    )
    output = default_mate_output_payload()
    output.update(
        {
            "output_dir": "output",
            "project_name": "mate",
            "board_outline": {
                "mode": "source_bounds_with_margin",
                "margin_mils": {
                    "left": 500,
                    "bottom": 500,
                    "right": 3000,
                    "top": 500,
                },
            },
            "overwrite": True,
        }
    )
    board_projection = default_mate_board_projection_payload()
    board_projection["cutouts"]["actual_cutouts"] = True
    return {
        "schema": schema,
        "source": {
            "board": source_board_text,
            "project_context": "auto",
        },
        "output": output,
        "libraries": {
            "roots": ["mating_parts"],
            "recursive": True,
        },
        "validation": {
            "source_side": "infer_single_side",
            "allow_side_agnostic_through_hole": True,
            "side_agnostic_kinds": ["mount"],
        },
        "projections": [
            _named_test_point_projection(),
            _named_mount_projection(),
            _named_alignment_pin_projection(),
        ],
        "pcb_designators": default_mate_designators_payload(),
        "board_projection": board_projection,
        "artifacts": default_mate_artifacts_payload(),
    }


def _named_test_point_projection() -> JsonObject:
    return {
        "id": "test_points",
        "source": {
            "object": "component",
            "designators": "TP*",
        },
        "actions": [
            {
                "kind": "mate_component",
                "symbol_name": "YZ209315103P-01",
                "footprint_name": "YZ209315103P-01",
                "designator_prefix": "TP",
                "signal_pad_designator": "1",
            },
            default_mate_reference_graphics_payload(),
            {
                "kind": "label",
                "text": "source_net",
                "placement": default_mate_label_placement_payload(),
                "style": default_mate_label_style_payload(),
            },
        ],
    }


def _named_mount_projection() -> JsonObject:
    return {
        "id": "mounts",
        "source": {
            "object": "component",
            "designators": "M1-4",
        },
        "actions": [
            {
                "kind": "mate_component",
                "symbol_name": "9774080360R",
                "footprint_name": "9774080360R-YIYUAN",
                "designator_prefix": "M",
            },
            default_mate_reference_graphics_payload(),
        ],
    }


def _named_alignment_pin_projection() -> JsonObject:
    return {
        "id": "alignment_pins",
        "source": {
            "object": "free_pad",
            "hole_size_mils": {"min": 75, "max": 85},
            "plated": False,
        },
        "actions": [
            {
                "kind": "mate_component",
                "symbol_name": "H2184-05",
                "footprint_name": "H2184-05",
                "designator_prefix": "P",
                "signal_pad_designator": "1",
            },
            default_mate_reference_graphics_payload(),
            {
                "kind": "label",
                "text": "source_net",
                "placement": default_mate_label_placement_payload(),
                "style": default_mate_label_style_payload(),
            },
        ],
    }


def _designator_expression(designators: list[str]) -> str:
    sorted_designators = sorted(set(designators), key=_designator_sort_key)
    tokens: list[str] = []
    run_prefix: str | None = None
    run_start: int | None = None
    run_end: int | None = None
    for designator in sorted_designators:
        prefix, number = _split_designator_number(designator.strip().upper())
        if number is None:
            _append_designator_run(tokens, run_prefix, run_start, run_end)
            tokens.append(designator)
            run_prefix = None
            run_start = None
            run_end = None
            continue
        if run_prefix == prefix and run_end is not None and number == run_end + 1:
            run_end = number
            continue
        _append_designator_run(tokens, run_prefix, run_start, run_end)
        run_prefix = prefix
        run_start = number
        run_end = number
    _append_designator_run(tokens, run_prefix, run_start, run_end)
    return ", ".join(tokens)


def _append_designator_run(
    tokens: list[str],
    prefix: str | None,
    start: int | None,
    end: int | None,
) -> None:
    if prefix is None or start is None or end is None:
        return
    if start == end:
        tokens.append(f"{prefix}{start}")
    else:
        tokens.append(f"{prefix}{start}-{end}")


def _designator_sort_key(designator: str) -> tuple[str, int, str]:
    prefix, number = _split_designator_number(designator.strip().upper())
    return (prefix, number if number is not None else -1, designator.upper())


def _split_designator_number(value: str) -> tuple[str, int | None]:
    index = len(value)
    while index > 0 and value[index - 1].isdigit():
        index -= 1
    prefix = value[:index].upper()
    suffix = value[index:]
    return (prefix, int(suffix) if suffix else None)


def _list_field(payload: Mapping[str, object], name: str) -> list[object]:
    value = payload.get(name)
    if isinstance(value, list):
        return value
    return []
