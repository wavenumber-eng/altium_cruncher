"""Generate the Gate 6 component-owned analytic-body Toon fixture.

The PcbDoc is the committed test input. This script is its source of truth and
uses only Altium Monkey's public document, footprint, and primitive surfaces.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
from typing import Literal

from altium_monkey import (
    AltiumPcbDoc,
    AltiumPcbLib,
    PcbBodyProjection,
    PcbLayer,
    PcbRegionKind,
)


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "assets" / "projects" / "toon-analytic-bodies"
DEFAULT_OUTPUT = FIXTURE / "input" / "toon_analytic_bodies.PcbDoc"
INVENTORY_PATH = FIXTURE / "semantic-inventory.json"
MANIFEST_PATH = FIXTURE / "source-manifest.json"
IU_PER_MIL = 10_000.0


@dataclass(frozen=True)
class BodySpec:
    name: str
    kind: Literal["extrusion", "cylinder", "sphere"]
    color: str
    standoff_mils: float
    upper_or_height_mils: float
    outline_mils: tuple[tuple[float, float], ...]
    offset_mils: tuple[float, float] = (0.0, 0.0)
    radius_mils: float = 0.0
    opacity: float = 1.0


@dataclass(frozen=True)
class CaseSpec:
    designator: str
    title: str
    side: Literal["top", "bottom"]
    anchor_mils: tuple[float, float]
    rotation_degrees: float
    intent: str
    bodies: tuple[BodySpec, ...]


RECT = ((-210.0, -150.0), (210.0, -150.0), (210.0, 150.0), (-210.0, 150.0))
SMALL_RECT = ((-150.0, -110.0), (150.0, -110.0), (150.0, 110.0), (-150.0, 110.0))
CONCAVE = (
    (-250.0, -170.0),
    (250.0, -170.0),
    (250.0, -40.0),
    (60.0, -40.0),
    (60.0, 170.0),
    (-250.0, 170.0),
)
CIRCLE_HINT = ((-180.0, -180.0), (180.0, -180.0), (180.0, 180.0), (-180.0, 180.0))


CASES = (
    CaseSpec(
        "A1",
        "TOP RECT",
        "top",
        (650.0, 4050.0),
        17.0,
        "surface-contained convex extrusion with nonzero component rotation",
        (BodySpec("rect", "extrusion", "#E63946", 20.0, 150.0, RECT),),
    ),
    CaseSpec(
        "A2",
        "TOP CONCAVE",
        "top",
        (1550.0, 4050.0),
        31.0,
        "offset concave extrusion with nonzero component rotation",
        (
            BodySpec(
                "concave",
                "extrusion",
                "#F4A261",
                10.0,
                170.0,
                CONCAVE,
                offset_mils=(70.0, -35.0),
            ),
        ),
    ),
    CaseSpec(
        "A3",
        "TOP CYL THROUGH",
        "top",
        (2500.0, 4050.0),
        23.0,
        "isolated offset cylinder crossing the complete board slab",
        (
            BodySpec(
                "cylinder",
                "cylinder",
                "#2A9D8F",
                -100.0,
                220.0,
                CIRCLE_HINT,
                offset_mils=(95.0, -55.0),
                radius_mils=150.0,
            ),
        ),
    ),
    CaseSpec(
        "A4",
        "TOP SPHERE THROUGH",
        "top",
        (3400.0, 4050.0),
        13.0,
        "offset sphere crossing the complete board slab",
        (
            BodySpec(
                "sphere",
                "sphere",
                "#457B9D",
                -100.0,
                0.0,
                CIRCLE_HINT,
                offset_mils=(-70.0, 50.0),
                radius_mils=155.0,
            ),
        ),
    ),
    CaseSpec(
        "A5",
        "THROUGH MIX",
        "top",
        (4350.0, 4050.0),
        19.0,
        "staged compound: through extrusion, top-only cylinder, and lower/side sphere",
        (
            BodySpec(
                "through-extrusion", "extrusion", "#9B5DE5", -120.0, 120.0, SMALL_RECT
            ),
            BodySpec(
                "top-cylinder",
                "cylinder",
                "#00BBF9",
                -40.0,
                220.0,
                CIRCLE_HINT,
                offset_mils=(20.0, 0.0),
                radius_mils=70.0,
            ),
            BodySpec(
                "lower-sphere",
                "sphere",
                "#FEE440",
                -170.0,
                0.0,
                CIRCLE_HINT,
                offset_mils=(-170.0, 0.0),
                radius_mils=110.0,
            ),
        ),
    ),
    CaseSpec(
        "A6",
        "Z STACK",
        "top",
        (5350.0, 4050.0),
        11.0,
        "same-XY extrusion intervals include a gap, exact touch, and overlap",
        (
            BodySpec("z-low", "extrusion", "#264653", 20.0, 40.0, SMALL_RECT),
            BodySpec("z-gap", "extrusion", "#2A9D8F", 60.0, 100.0, SMALL_RECT),
            BodySpec("z-touch", "extrusion", "#E9C46A", 100.0, 140.0, SMALL_RECT),
            BodySpec("z-overlap", "extrusion", "#E76F51", 120.0, 175.0, SMALL_RECT),
        ),
    ),
    CaseSpec(
        "A7",
        "OPACITY 55%",
        "top",
        (6250.0, 4050.0),
        27.0,
        "uniform partial opacity applied once to the final component instance",
        (BodySpec("partial", "extrusion", "#8E44AD", 15.0, 160.0, RECT, opacity=0.55),),
    ),
    CaseSpec(
        "B1",
        "BOTTOM RECT",
        "bottom",
        (650.0, 850.0),
        29.0,
        "bottom-authored counterpart of the surface extrusion",
        (BodySpec("rect", "extrusion", "#E63946", 20.0, 150.0, RECT),),
    ),
    CaseSpec(
        "B2",
        "BOTTOM CYL",
        "bottom",
        (1550.0, 850.0),
        37.0,
        "bottom-authored offset surface cylinder",
        (
            BodySpec(
                "cylinder",
                "cylinder",
                "#2A9D8F",
                15.0,
                180.0,
                CIRCLE_HINT,
                offset_mils=(80.0, -45.0),
                radius_mils=150.0,
            ),
        ),
    ),
    CaseSpec(
        "B3",
        "BOTTOM SPHERE",
        "bottom",
        (2500.0, 850.0),
        41.0,
        "bottom-authored offset surface sphere",
        (
            BodySpec(
                "sphere",
                "sphere",
                "#457B9D",
                12.0,
                0.0,
                CIRCLE_HINT,
                offset_mils=(-70.0, 45.0),
                radius_mils=155.0,
            ),
        ),
    ),
    CaseSpec(
        "B4",
        "BOTTOM THROUGH",
        "bottom",
        (3400.0, 850.0),
        33.0,
        "bottom-authored extrusion crossing the complete board slab",
        (BodySpec("through", "extrusion", "#9B5DE5", -100.0, 120.0, RECT),),
    ),
    CaseSpec(
        "B5",
        "EDGE OVERHANG",
        "bottom",
        (100.0, 2450.0),
        21.0,
        "bottom-authored body extending beyond the left board edge",
        (
            BodySpec(
                "edge",
                "extrusion",
                "#FF6B6B",
                10.0,
                150.0,
                ((-380.0, -190.0), (380.0, -190.0), (380.0, 190.0), (-380.0, 190.0)),
            ),
        ),
    ),
    CaseSpec(
        "A8",
        "CUTOUT OVERHANG",
        "top",
        (5550.0, 2250.0),
        16.0,
        "top-authored body spanning the routed interior cutout",
        (
            BodySpec(
                "cutout",
                "extrusion",
                "#4CC9F0",
                10.0,
                150.0,
                ((-520.0, -330.0), (520.0, -330.0), (520.0, 330.0), (-520.0, 330.0)),
            ),
        ),
    ),
    CaseSpec(
        "A9",
        "ZERO OPACITY",
        "top",
        (6550.0, 2250.0),
        12.0,
        "zero-opacity body must be omitted before geometry and occlusion",
        (BodySpec("hidden", "extrusion", "#000000", 10.0, 150.0, RECT, opacity=0.0),),
    ),
)


def _colorref(css: str) -> int:
    red, green, blue = (int(css[index : index + 2], 16) for index in (1, 3, 5))
    return red | (green << 8) | (blue << 16)


def _iu(mils: float) -> int:
    return int(round(mils * IU_PER_MIL))


def _add_body(footprint: object, spec: BodySpec) -> None:
    shifted = [
        (x + spec.offset_mils[0], y + spec.offset_mils[1]) for x, y in spec.outline_mils
    ]
    body = footprint.add_component_body(
        outline_points_mils=shifted,
        layer=PcbLayer.MECHANICAL_1,
        overall_height_mils=(
            spec.upper_or_height_mils
            if spec.kind != "sphere"
            else spec.standoff_mils + (2 * spec.radius_mils)
        ),
        standoff_height_mils=spec.standoff_mils,
        body_projection=PcbBodyProjection.TOP,
        model_2d_mils=spec.offset_mils,
        name=spec.name,
        identifier=spec.name,
        body_color_3d=_colorref(spec.color),
        body_opacity_3d=spec.opacity,
        model_type={"extrusion": 0, "cylinder": 2, "sphere": 3}[spec.kind],
    )
    # Analytic-specific record fields are public Altium Monkey model fields.
    # The generic public component-body authoring helper creates the owning
    # primitive; these fields select and parameterize its native analytic type.
    body.model_type = {"extrusion": 0, "cylinder": 2, "sphere": 3}[spec.kind]
    body.model_extruded_min_z = _iu(spec.standoff_mils)
    body.model_extruded_max_z = _iu(spec.upper_or_height_mils)
    body.model_2d_x = _iu(spec.offset_mils[0])
    body.model_2d_y = _iu(spec.offset_mils[1])
    if spec.kind == "cylinder":
        body.model_cylinder_radius = _iu(spec.radius_mils)
        body.model_cylinder_height = _iu(spec.upper_or_height_mils)
    elif spec.kind == "sphere":
        body.model_sphere_radius = _iu(spec.radius_mils)


def _build_library() -> tuple[AltiumPcbLib, dict[str, object]]:
    library = AltiumPcbLib()
    footprints: dict[str, object] = {}
    for case in CASES:
        footprint = library.add_footprint(
            f"TOON_{case.designator}_{case.title.replace(' ', '_')}",
            description=case.intent,
        )
        for body in case.bodies:
            _add_body(footprint, body)
        footprints[case.designator] = footprint
    return library, footprints


def _add_reference_text(pcbdoc: AltiumPcbDoc) -> None:
    for case in CASES:
        x, y = case.anchor_mils
        label_y = y + 330.0 if y < 1500.0 else y - 360.0
        for layer, mirrored in (
            (PcbLayer.TOP_OVERLAY, False),
            (PcbLayer.BOTTOM_OVERLAY, True),
        ):
            pcbdoc.add_text(
                text=f"{case.designator} {case.title}",
                position_mils=(x, label_y),
                height_mils=62.0,
                stroke_width_mils=8.0,
                layer=layer,
                is_mirrored=mirrored,
            )


def build_board(output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    library, footprints = _build_library()
    pcbdoc = AltiumPcbDoc()
    pcbdoc.set_layer_stack_template("2-layer")
    pcbdoc.set_outline_vertices_mils(
        ((0.0, 0.0), (7000.0, 0.0), (7000.0, 4200.0), (6500.0, 5000.0), (0.0, 5000.0))
    )
    pcbdoc.set_origin_to_outline_lower_left()
    pcbdoc.add_region(
        outline_points_mils=[
            (5150.0, 1800.0),
            (5950.0, 1800.0),
            (5950.0, 2700.0),
            (5150.0, 2700.0),
        ],
        layer=PcbLayer.MULTI_LAYER,
        kind=PcbRegionKind.BOARD_CUTOUT,
        is_board_cutout=True,
        is_shapebased=True,
    )
    _add_reference_text(pcbdoc)
    for case in CASES:
        pcbdoc.add_component_from_pcblib(
            footprints[case.designator],
            designator=case.designator,
            position_mils=case.anchor_mils,
            layer=PcbLayer.TOP if case.side == "top" else PcbLayer.BOTTOM,
            rotation_degrees=case.rotation_degrees,
            source_pcblib=library,
            comment_text=case.title,
        )
    pcbdoc.save(output_path)
    return output_path


def _round(value: float) -> float:
    return round(value, 4)


def _component_mils(value: object) -> float:
    text = str(value).strip()
    return float(text[:-3] if text.lower().endswith("mil") else text)


def semantic_inventory(path: Path) -> dict[str, object]:
    pcbdoc = AltiumPcbDoc.from_file(path)
    components = {index: component for index, component in enumerate(pcbdoc.components)}
    intent = {case.designator: case.intent for case in CASES}
    bodies = []
    for index, body in enumerate(pcbdoc.component_bodies):
        component = components[int(body.component_index)]
        model_type = int(body.model_type)
        radius = (
            body.model_cylinder_radius
            if model_type == 2
            else body.model_sphere_radius
            if model_type == 3
            else 0
        )
        bodies.append(
            {
                "body_index": index,
                "body_name": str(body.name),
                "component_index": int(body.component_index),
                "designator": str(component.designator),
                "side": "bottom" if str(component.layer).upper() == "BOTTOM" else "top",
                "component_anchor_mils": [
                    _round(_component_mils(component.x)),
                    _round(_component_mils(component.y)),
                ],
                "component_rotation_degrees": _round(float(component.rotation)),
                "model_type": model_type,
                "kind": {0: "extrusion", 2: "cylinder", 3: "sphere"}.get(
                    model_type, "unsupported"
                ),
                "outline_mils": [
                    [_round(vertex.x / IU_PER_MIL), _round(vertex.y / IU_PER_MIL)]
                    for vertex in body.outline
                ],
                "model_offset_mils": [
                    _round(body.model_2d_x / IU_PER_MIL),
                    _round(body.model_2d_y / IU_PER_MIL),
                ],
                "standoff_mils": _round(body.standoff_height / IU_PER_MIL),
                "overall_height_mils": _round(body.overall_height / IU_PER_MIL),
                "cylinder_height_mils": _round(body.model_cylinder_height / IU_PER_MIL),
                "radius_mils": _round(radius / IU_PER_MIL),
                "colorref": f"0x{int(body.body_color_3d):06X}",
                "opacity": _round(float(body.body_opacity_3d)),
                "intent": intent[str(component.designator)],
            }
        )
    return {
        "schema": "altium-cruncher.toon-analytic-bodies.inventory.a0",
        "board": {
            "component_count": len(pcbdoc.components),
            "body_count": len(pcbdoc.component_bodies),
            "cutout_count": sum(
                1 for region in pcbdoc.regions if region.is_board_cutout
            ),
        },
        "bodies": bodies,
    }


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def generate(output_path: Path = DEFAULT_OUTPUT) -> dict[str, object]:
    build_board(output_path)
    inventory = semantic_inventory(output_path)
    _write_json(INVENTORY_PATH, inventory)
    data = output_path.read_bytes()
    manifest = {
        "schema": "altium-cruncher.test-asset-source.a0",
        "fixture": "toon-analytic-bodies",
        "authorization": "Generated repository test fixture; no third-party design content.",
        "generator": "tests/support_scripts/generate_toon_analytic_bodies.py",
        "command": "uv run python tests/support_scripts/generate_toon_analytic_bodies.py",
        "altium_monkey_version": version("altium-monkey"),
        "files": [
            {
                "path": "input/toon_analytic_bodies.PcbDoc",
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        ],
        "semantic_inventory": "semantic-inventory.json",
    }
    _write_json(MANIFEST_PATH, manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    manifest = generate(args.output.resolve())
    print(args.output.resolve())
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
