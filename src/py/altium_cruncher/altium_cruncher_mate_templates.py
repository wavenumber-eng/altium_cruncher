"""Mate config template and seed projection helpers."""

from __future__ import annotations

import json
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
        "*/\n"
        f"{json.dumps(payload, indent=2)}\n"
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
