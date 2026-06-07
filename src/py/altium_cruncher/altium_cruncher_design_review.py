"""Design-review bundle generation for Altium projects."""

from __future__ import annotations

import json
import logging
from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING

from altium_cruncher.altium_cruncher_json_dump import (
    build_json_dump_payload,
    document_json_output_path,
)
from altium_cruncher.altium_cruncher_notes import build_notes_payload
from altium_cruncher.altium_cruncher_notes import render_notes_jsonc

if TYPE_CHECKING:
    from altium_cruncher.altium_cruncher_pcb_svg_config import PcbSvgConfig
    from altium_monkey.altium_record_types import PcbLayer
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc

DESIGN_REVIEW_MANIFEST_SCHEMA = "altium_cruncher.design_review_manifest.a0"

log = logging.getLogger(__name__)


def write_design_review_bundle(
    input_file: Path,
    output_dir: Path,
    *,
    include_indexes: bool,
) -> dict[str, object]:
    """Write the full design-review bundle for a SchDoc or PrjPcb."""
    design = _load_design(input_file)
    design_payload = design.to_json(include_indexes=include_indexes)
    design_json_path = output_dir / f"{input_file.stem}_design.json"
    _write_json(design_json_path, design_payload)
    log.info("Design JSON: %s", _relpath(design_json_path, output_dir))

    schdoc_paths = _schdoc_paths(input_file, design)
    pcbdoc_paths = _pcbdoc_paths(input_file, design)
    source_base = input_file.resolve().parent
    sch_svgs = _write_schematic_svgs(
        schdoc_paths,
        output_dir,
        design,
        source_base=source_base,
    )
    doc_jsons = _write_document_jsons(
        [*schdoc_paths, *pcbdoc_paths],
        output_dir,
        source_base=source_base,
    )
    notes_path = _write_notes_json(input_file, output_dir)
    pcb_artifacts = _write_pcb_review_svgs(input_file, output_dir, design, pcbdoc_paths)

    manifest_path = output_dir / "design_review_manifest.json"
    readme_path = output_dir / "README.md"
    manifest = _manifest_payload(
        input_file,
        output_dir,
        design_json_path=design_json_path,
        doc_jsons=doc_jsons,
        notes_path=notes_path,
        sch_svgs=sch_svgs,
        pcb_artifacts=pcb_artifacts,
        readme_path=readme_path,
    )
    _write_json(manifest_path, manifest)
    readme_path.write_text(
        _readme_text(input_file, output_dir, manifest),
        encoding="utf-8",
    )
    log.info("Design review README: %s", _relpath(readme_path, output_dir))
    log.info("Design review manifest: %s", _relpath(manifest_path, output_dir))
    return manifest


def _load_design(input_file: Path) -> object:
    from altium_monkey.altium_design import AltiumDesign

    suffix = input_file.suffix.lower()
    if suffix == ".schdoc":
        return AltiumDesign.from_schdoc(input_file)
    if suffix == ".prjpcb":
        return AltiumDesign.from_prjpcb(input_file)
    raise ValueError(f"Unsupported design input type: {input_file.suffix}")


def _schdoc_paths(input_file: Path, design: object) -> list[Path]:
    if input_file.suffix.lower() == ".schdoc":
        return [input_file]
    project = getattr(design, "project", None)
    if project is None:
        return []
    return list(project.get_schdoc_paths())


def _pcbdoc_paths(input_file: Path, design: object) -> list[Path]:
    if input_file.suffix.lower() == ".schdoc":
        return []
    return list(getattr(design, "get_pcbdoc_paths")())


def _project_parameters(design: object) -> dict[str, str]:
    project = getattr(design, "project", None)
    if project is None:
        return {}
    parameters = dict(getattr(project, "parameters", {}))
    current_variant = project.get_current_variant()
    if current_variant:
        parameters["VariantName"] = current_variant
    return parameters


def _write_schematic_svgs(
    schdoc_paths: list[Path],
    output_dir: Path,
    design: object,
    *,
    source_base: Path,
) -> list[dict[str, object]]:
    from altium_monkey.altium_schdoc import AltiumSchDoc

    schematic_dir = output_dir / "schematics"
    schematic_dir.mkdir(parents=True, exist_ok=True)
    project_parameters = _project_parameters(design)
    artifacts: list[dict[str, object]] = []
    for index, schdoc_path in enumerate(schdoc_paths):
        output_path = schematic_dir / f"{schdoc_path.stem}.svg"
        svg = AltiumSchDoc(schdoc_path).to_svg(
            project_parameters=project_parameters,
            wrap_components=True,
        )
        output_path.write_text(svg, encoding="utf-8")
        log.info("Schematic SVG: %s", _relpath(output_path, output_dir))
        artifacts.append(
            {
                "file": _relpath(output_path, output_dir),
                "source": _source_path(schdoc_path, source_base),
                "page_number": index + 1,
                "page_count": len(schdoc_paths),
            }
        )
    return artifacts


def _write_document_jsons(
    source_paths: list[Path],
    output_dir: Path,
    *,
    source_base: Path,
) -> list[dict[str, object]]:
    artifacts: list[dict[str, object]] = []
    used_names: set[str] = set()
    for source_path in source_paths:
        payload = build_json_dump_payload(source_path)
        kind = str(payload["kind"])
        output_path = document_json_output_path(
            source_path,
            output_dir,
            kind,
            used_names,
        )
        _write_json(output_path, payload)
        log.info("Document JSON: %s", _relpath(output_path, output_dir))
        artifacts.append(
            {
                "file": _relpath(output_path, output_dir),
                "source": _source_path(source_path, source_base),
                "kind": kind,
            }
        )
    return artifacts


def _write_notes_json(input_file: Path, output_dir: Path) -> Path:
    output_path = output_dir / "notes" / f"{input_file.stem}_notes.jsonc"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_notes_jsonc(build_notes_payload(input_file)),
        encoding="utf-8",
    )
    log.info("Notes JSON: %s", _relpath(output_path, output_dir))
    return output_path


def _write_pcb_review_svgs(
    input_file: Path,
    output_dir: Path,
    design: object,
    pcbdoc_paths: list[Path],
) -> list[dict[str, object]]:
    if not pcbdoc_paths:
        return []
    from altium_cruncher.altium_cruncher_pcb_svg_a0_renderer import (
        _render_a0_board_outputs,
    )
    from altium_cruncher.altium_cruncher_pcb_svg_config import PcbSvgConfig
    from altium_cruncher.altium_cruncher_pcb_workflow import CruncherPcbRenderInput
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc

    pcb_dir = output_dir / "pcb"
    project_parameters = _project_parameters(design)
    for pcbdoc_path in pcbdoc_paths:
        pcbdoc = AltiumPcbDoc.from_file(pcbdoc_path)
        config = _pcb_review_svg_config(pcbdoc, PcbSvgConfig.default())
        render_input = CruncherPcbRenderInput(
            board_key=pcbdoc_path.stem,
            pcb_path=pcbdoc_path,
            pcbdoc=pcbdoc,
            project_parameters=project_parameters,
        )
        _render_a0_board_outputs(
            config,
            render_input,
            input_file=pcbdoc_path,
            output_dir=pcb_dir,
        )
        _log_pcb_svg_manifest_outputs(
            pcb_dir / f"{pcbdoc_path.stem}__views.json",
            pcb_dir=pcb_dir,
            output_dir=output_dir,
        )
    return _collect_pcb_svg_manifests(pcb_dir, output_dir)


def _pcb_review_svg_config(
    pcbdoc: "AltiumPcbDoc",
    config: "PcbSvgConfig",
) -> "PcbSvgConfig":
    config.views = []
    config.layer_outputs["enabled"] = True
    config.layer_outputs["layers"] = _pcb_review_copper_layer_tokens(pcbdoc, config)
    return config


def _pcb_review_copper_layer_tokens(
    pcbdoc: "AltiumPcbDoc",
    config: "PcbSvgConfig",
) -> list[str]:
    from altium_monkey.altium_record_types import PcbLayer
    from altium_cruncher.altium_cruncher_pcb_svg_a0_renderer import PcbSvgA0Renderer

    renderer = PcbSvgA0Renderer(config)
    layers = {
        layer
        for layer in renderer._collect_visible_layers(pcbdoc)  # noqa: SLF001
        if layer.is_copper()
    }
    layers.update(_pcb_review_primitive_copper_layers(pcbdoc))
    tokens = [layer.to_json_name() for layer in sorted(layers, key=int)]
    return tokens or [PcbLayer.TOP.to_json_name(), PcbLayer.BOTTOM.to_json_name()]


def _pcb_review_primitive_copper_layers(pcbdoc: "AltiumPcbDoc") -> set["PcbLayer"]:
    from altium_monkey.altium_record_types import PcbLayer

    layers: set[PcbLayer] = set()
    saw_multilayer = False
    for layer_value in _iter_pcb_review_layer_values(pcbdoc):
        layer = _pcb_layer_from_value(layer_value)
        if layer is None:
            continue
        if layer == PcbLayer.MULTI_LAYER:
            saw_multilayer = True
            continue
        if layer.is_copper():
            layers.add(layer)
    if saw_multilayer and not layers:
        layers.update({PcbLayer.TOP, PcbLayer.BOTTOM})
    return layers


def _iter_pcb_review_layer_values(pcbdoc: "AltiumPcbDoc") -> Iterator[object]:
    for collection_name in (
        "tracks",
        "arcs",
        "fills",
        "regions",
        "shapebased_regions",
        "polygons",
        "pads",
        "vias",
        "texts",
    ):
        for primitive in getattr(pcbdoc, collection_name, ()):
            yield getattr(primitive, "layer", None)
            if collection_name == "vias":
                yield getattr(primitive, "layer_start", None)
                yield getattr(primitive, "layer_end", None)


def _pcb_layer_from_value(value: object) -> "PcbLayer | None":
    from altium_monkey.altium_record_types import PcbLayer

    if value is None:
        return None
    if isinstance(value, PcbLayer):
        return value
    if isinstance(value, str):
        try:
            return PcbLayer.from_json_name(value)
        except ValueError:
            try:
                return PcbLayer[value]
            except KeyError:
                return None
    try:
        return PcbLayer(int(value))
    except (TypeError, ValueError):
        return None


def _log_pcb_svg_manifest_outputs(
    manifest_path: Path,
    *,
    pcb_dir: Path,
    output_dir: Path,
) -> None:
    if not manifest_path.exists():
        return
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    raw_layer_outputs = payload.get("layer_outputs", {})
    if not isinstance(raw_layer_outputs, dict):
        return
    for entry in raw_layer_outputs.values():
        if not isinstance(entry, dict):
            continue
        file_value = str(entry.get("file") or "")
        if file_value:
            log.info("PCB SVG: %s", _relpath(pcb_dir / file_value, output_dir))


def _collect_pcb_svg_manifests(
    pcb_dir: Path,
    output_dir: Path,
) -> list[dict[str, object]]:
    artifacts: list[dict[str, object]] = []
    for manifest_path in sorted(pcb_dir.glob("*__views.json")):
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        artifacts.append(
            {
                "manifest": _relpath(manifest_path, output_dir),
                "board": payload.get("board"),
                "layer_outputs": _manifest_output_files(
                    payload.get("layer_outputs", {}),
                    pcb_dir,
                    output_dir,
                ),
                "views": _manifest_output_files(
                    payload.get("views", {}),
                    pcb_dir,
                    output_dir,
                ),
            }
        )
    return artifacts


def _manifest_output_files(
    raw_entries: object,
    base_dir: Path,
    output_dir: Path,
) -> list[dict[str, object]]:
    if not isinstance(raw_entries, dict):
        return []
    artifacts: list[dict[str, object]] = []
    for name, raw_entry in sorted(raw_entries.items()):
        if not isinstance(raw_entry, dict):
            continue
        file_value = str(raw_entry.get("file") or "")
        artifacts.append(
            {
                "name": str(name),
                "file": _relpath(base_dir / file_value, output_dir),
                "layers": raw_entry.get("layers", []),
            }
        )
    return artifacts


def _manifest_payload(
    input_file: Path,
    output_dir: Path,
    *,
    design_json_path: Path,
    doc_jsons: list[dict[str, object]],
    notes_path: Path,
    sch_svgs: list[dict[str, object]],
    pcb_artifacts: list[dict[str, object]],
    readme_path: Path,
) -> dict[str, object]:
    return {
        "schema": DESIGN_REVIEW_MANIFEST_SCHEMA,
        "input": _source_path(input_file, input_file.resolve().parent),
        "design_json": _relpath(design_json_path, output_dir),
        "document_jsons": doc_jsons,
        "notes_json": _relpath(notes_path, output_dir),
        "schematic_svgs": sch_svgs,
        "pcb_svgs": pcb_artifacts,
        "readme": _relpath(readme_path, output_dir),
    }


def _readme_text(
    input_file: Path,
    output_dir: Path,
    manifest: dict[str, object],
) -> str:
    schematic_count = len(manifest.get("schematic_svgs", []))
    pcb_count = sum(
        len(item.get("layer_outputs", []))
        for item in manifest.get("pcb_svgs", [])
        if isinstance(item, dict)
    )
    return f"""# Altium Design Review Bundle

Input: `{_source_path(input_file, input_file.resolve().parent)}`

This folder is generated by `altium-cruncher design`, `design-review`, or `dr`.
It is intended for review agents that need a machine-readable design model plus
visual schematic and PCB context.

## Files

- `{manifest['design_json']}`: Altium design JSON from `altium-monkey`.
- `design_review_manifest.json`: artifact index for this bundle.
- `{manifest['notes_json']}`: JSONC dedicated notes, schematic-owned text frames, and schematic-owned free text by sheet. Sheet-template/title-block text is suppressed by default.
- `json/schdoc/` and `json/pcbdoc/`: serialized document JSON snapshots from `json-dump`.
- `schematics/`: schematic SVGs with component wrapping where available.
- `pcb/layers/`: PCB copper-layer SVGs with board outline, cutouts, drills, and slots.

## Counts

- Schematic SVGs: {schematic_count}
- PCB layer SVGs: {pcb_count}

Generated artifact paths in `design_review_manifest.json` are relative to this bundle. Source paths are relative to the input project or document directory.
"""


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _relpath(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _source_path(path: Path, source_base: Path) -> str:
    try:
        return path.resolve().relative_to(source_base.resolve()).as_posix()
    except ValueError:
        return path.name
