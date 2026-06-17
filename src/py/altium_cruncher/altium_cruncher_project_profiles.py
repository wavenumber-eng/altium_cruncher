"""Reusable project skeleton defaults for generated Altium documents."""

from __future__ import annotations

from collections.abc import Sequence

JsonObject = dict[str, object]

STANDARD_MECHANICAL_LAYER_PROFILE = "standard_component_pairs"

STANDARD_MECHANICAL_LAYERS: tuple[tuple[str, str, bool], ...] = (
    ("MECHANICAL1", "Mechanical 1", True),
    ("MECHANICAL2", "Board Shape", True),
    ("MECHANICAL3", "Route Tool Path", True),
    ("MECHANICAL4", "V Cut", True),
    ("MECHANICAL5", "Fab Notes", True),
    ("MECHANICAL6", "Sheet", True),
    ("MECHANICAL7", "Board", True),
    ("MECHANICAL8", "Dimensions", True),
    ("MECHANICAL9", "Assembly Notes", True),
    ("MECHANICAL10", "Top 3D Body", True),
    ("MECHANICAL11", "Bottom 3D Body", True),
    ("MECHANICAL12", "Top Assembly", True),
    ("MECHANICAL13", "Bottom Assembly", True),
    ("MECHANICAL14", "Top Coating", True),
    ("MECHANICAL15", "Bottom Coating", True),
    ("MECHANICAL16", "Top Component Center", True),
    ("MECHANICAL17", "Bottom Component Center", True),
    ("MECHANICAL18", "Top Glue Points", True),
    ("MECHANICAL19", "Bottom Glue Points", True),
    ("MECHANICAL20", "Top Courtyard", True),
    ("MECHANICAL21", "Bottom Courtyard", True),
    ("MECHANICAL22", "Top Component Outline", True),
    ("MECHANICAL23", "Bottom Component Outline", True),
    ("MECHANICAL24", "Top Designator", True),
    ("MECHANICAL25", "Bottom Designator", True),
    ("MECHANICAL26", "Top Dimensions", True),
    ("MECHANICAL27", "Bottom Dimensions", True),
    ("MECHANICAL28", "Top Gold Plating", True),
    ("MECHANICAL29", "Bottom Gold Plating", True),
    ("MECHANICAL30", "Top Value", True),
    ("MECHANICAL31", "Bottom Value", True),
    ("MECHANICAL32", "Mechanical 32", False),
)

STANDARD_MECHANICAL_LAYER_KINDS: tuple[tuple[str, str], ...] = (
    ("MECHANICAL2", "BOARD_SHAPE"),
    ("MECHANICAL3", "ROUTE_TOOL_PATH"),
    ("MECHANICAL4", "VCUT"),
    ("MECHANICAL5", "FAB_NOTES"),
    ("MECHANICAL6", "SHEET"),
    ("MECHANICAL7", "BOARD"),
    ("MECHANICAL8", "DIMENSIONS"),
    ("MECHANICAL9", "ASSEMBLY_NOTES"),
    ("MECHANICAL10", "BODY_3D_TOP"),
    ("MECHANICAL11", "BODY_3D_BOTTOM"),
    ("MECHANICAL12", "ASSEMBLY_TOP"),
    ("MECHANICAL13", "ASSEMBLY_BOTTOM"),
    ("MECHANICAL14", "COATING_TOP"),
    ("MECHANICAL15", "COATING_BOTTOM"),
    ("MECHANICAL16", "COMPONENT_CENTER_TOP"),
    ("MECHANICAL17", "COMPONENT_CENTER_BOTTOM"),
    ("MECHANICAL18", "GLUE_POINTS_TOP"),
    ("MECHANICAL19", "GLUE_POINTS_BOTTOM"),
    ("MECHANICAL20", "COURTYARD_TOP"),
    ("MECHANICAL21", "COURTYARD_BOTTOM"),
    ("MECHANICAL22", "COMPONENT_OUTLINE_TOP"),
    ("MECHANICAL23", "COMPONENT_OUTLINE_BOTTOM"),
    ("MECHANICAL24", "DESIGNATOR_TOP"),
    ("MECHANICAL25", "DESIGNATOR_BOTTOM"),
    ("MECHANICAL26", "DIMENSIONS_TOP"),
    ("MECHANICAL27", "DIMENSIONS_BOTTOM"),
    ("MECHANICAL28", "GOLD_PLATING_TOP"),
    ("MECHANICAL29", "GOLD_PLATING_BOTTOM"),
    ("MECHANICAL30", "VALUE_TOP"),
    ("MECHANICAL31", "VALUE_BOTTOM"),
)

STANDARD_MECHANICAL_LAYER_PAIRS: tuple[tuple[str, str], ...] = (
    ("MECHANICAL10", "MECHANICAL11"),
    ("MECHANICAL12", "MECHANICAL13"),
    ("MECHANICAL14", "MECHANICAL15"),
    ("MECHANICAL16", "MECHANICAL17"),
    ("MECHANICAL18", "MECHANICAL19"),
    ("MECHANICAL20", "MECHANICAL21"),
    ("MECHANICAL22", "MECHANICAL23"),
    ("MECHANICAL24", "MECHANICAL25"),
    ("MECHANICAL26", "MECHANICAL27"),
    ("MECHANICAL28", "MECHANICAL29"),
    ("MECHANICAL30", "MECHANICAL31"),
)


def standard_mechanical_profile_args() -> JsonObject:
    """Return editable MCO args for the standard mechanical layer profile."""
    return {
        "mechanical_layers": [
            {"layer": layer, "name": name, "enabled": enabled}
            for layer, name, enabled in STANDARD_MECHANICAL_LAYERS
        ],
        "mechanical_layer_pairs": [
            {"layer_1": layer_1, "layer_2": layer_2}
            for layer_1, layer_2 in STANDARD_MECHANICAL_LAYER_PAIRS
        ],
        "mechanical_layer_kinds": [
            {"layer": layer, "kind": kind}
            for layer, kind in STANDARD_MECHANICAL_LAYER_KINDS
        ],
    }


def standard_mechanical_project_config() -> JsonObject:
    """Return grouped project-config rows for standard mechanical layers."""
    layers_by_id = {
        layer: {"layer": layer, "name": name, "enabled": enabled}
        for layer, name, enabled in STANDARD_MECHANICAL_LAYERS
    }
    kinds_by_id = dict(STANDARD_MECHANICAL_LAYER_KINDS)
    paired_layers = {
        layer
        for layer_pair in STANDARD_MECHANICAL_LAYER_PAIRS
        for layer in layer_pair
    }
    single_rows: list[JsonObject] = []
    for layer, row in layers_by_id.items():
        if layer in paired_layers:
            continue
        row = dict(row)
        if layer in kinds_by_id:
            row["kind"] = kinds_by_id[layer]
        single_rows.append(row)

    pair_rows: list[JsonObject] = []
    for top_layer, bottom_layer in STANDARD_MECHANICAL_LAYER_PAIRS:
        top = dict(layers_by_id[top_layer])
        bottom = dict(layers_by_id[bottom_layer])
        top["kind"] = kinds_by_id[top_layer]
        bottom["kind"] = kinds_by_id[bottom_layer]
        pair_rows.append({"top": top, "bottom": bottom})

    return {
        "mechanical_layers": single_rows,
        "mechanical_layer_pairs": pair_rows,
    }


def generated_rigid_stack_config(
    layer_count: int,
    *,
    name: str = "",
    total_dielectric_thickness_mils: float = 58.9,
) -> JsonObject:
    """Return a simple generated rigid-stack config for a copper layer count."""
    if layer_count < 2:
        raise ValueError("Rigid board layer count must be at least 2")
    if layer_count > 32:
        raise ValueError("Rigid board layer count must be at most 32")
    copper_names = _default_copper_names(layer_count)
    dielectric_count = layer_count - 1
    dielectric_thickness = total_dielectric_thickness_mils / dielectric_count
    return {
        "mode": "generated_rigid",
        "name": name or f"{layer_count}-layer-rigid",
        "copper_layers": [
            {
                "name": copper_name,
                "copper_thickness_mils": 1.4,
            }
            for copper_name in copper_names
        ],
        "dielectrics_between": [
            {
                "name": f"Dielectric {index}",
                "thickness_mils": round(dielectric_thickness, 4),
                "dielectric_constant": 4.8,
                "material": "FR-4",
                "dielectric_type": 0,
            }
            for index in range(1, dielectric_count + 1)
        ],
    }


def _default_copper_names(layer_count: int) -> Sequence[str]:
    if layer_count == 2:
        return ("Top Layer", "Bottom Layer")
    return (
        "Top Layer",
        *(f"Mid-Layer {index}" for index in range(1, layer_count - 1)),
        "Bottom Layer",
    )
