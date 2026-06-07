"""Design-review bundle generation for Altium projects."""

from __future__ import annotations

import html
import json
import logging
import re
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
SCHEMATIC_SVG_ENRICHMENT_SCHEMA = "altium_monkey.schematic.svg.enrichment.a0"
SCHEMATIC_SVG_ENRICHMENT_METADATA_ID = "schematic-enrichment-a0"
SCHEMATIC_REVIEW_THEME = "altium_cruncher.design_review.schematic_svg.a0"

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
    design_json_path = output_dir / "design" / f"{input_file.stem}_design.json"
    _write_json(design_json_path, design_payload)
    log.info("Design JSON: %s", _relpath(design_json_path, output_dir))

    schdoc_paths = _schdoc_paths(input_file, design)
    pcbdoc_paths = _pcbdoc_paths(input_file, design)
    source_base = input_file.resolve().parent
    sch_svgs = _write_schematic_svgs(
        schdoc_paths,
        output_dir,
        design,
        design_payload=design_payload,
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
    design_payload: dict[str, object],
    source_base: Path,
) -> list[dict[str, object]]:
    from altium_monkey.altium_schdoc import AltiumSchDoc

    schematic_dir = output_dir / "sch"
    schematic_dir.mkdir(parents=True, exist_ok=True)
    project_parameters = _project_parameters(design)
    artifacts: list[dict[str, object]] = []
    for index, schdoc_path in enumerate(schdoc_paths):
        output_path = schematic_dir / f"{schdoc_path.stem}.svg"
        svg = AltiumSchDoc(schdoc_path).to_svg(
            project_parameters=project_parameters,
            wrap_components=True,
        )
        svg = _enrich_schematic_svg(
            svg,
            design_payload=design_payload,
            schdoc_path=schdoc_path,
            source_base=source_base,
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


def _enrich_schematic_svg(
    svg: str,
    *,
    design_payload: dict[str, object],
    schdoc_path: Path,
    source_base: Path,
) -> str:
    """Embed design-review schematic SVG metadata and component lookup attrs."""
    rel_source = _source_path(schdoc_path, source_base)
    payload = _schematic_svg_enrichment_payload(
        design_payload,
        schdoc_path=schdoc_path,
        rel_source=rel_source,
    )
    root_attrs = {
        "data-enrichment-schema": SCHEMATIC_SVG_ENRICHMENT_SCHEMA,
        "data-view-kind": "schematic_sheet",
        "data-profile": "design_review",
        "data-source": rel_source,
        "data-sheet-name": schdoc_path.stem,
        "data-review-theme": SCHEMATIC_REVIEW_THEME,
    }
    svg = _inject_svg_root_attrs_and_metadata(
        svg,
        root_attrs=root_attrs,
        metadata_element=_schematic_svg_enrichment_metadata_element(payload),
    )
    return _annotate_schematic_component_groups(
        svg,
        design_payload=design_payload,
        schdoc_path=schdoc_path,
    )


def _schematic_svg_enrichment_payload(
    design_payload: dict[str, object],
    *,
    schdoc_path: Path,
    rel_source: str,
) -> dict[str, object]:
    return {
        "schema": SCHEMATIC_SVG_ENRICHMENT_SCHEMA,
        "source": {
            "altium_schdoc_file": rel_source,
        },
        "view": {
            "kind": "schematic_sheet",
            "profile": "design_review",
            "sheet_name": schdoc_path.stem,
            "sheet_file": schdoc_path.name,
        },
        "view_indexes": _schematic_svg_view_indexes(
            design_payload,
            schdoc_path=schdoc_path,
        ),
        "design": design_payload,
    }


def _schematic_svg_view_indexes(
    design_payload: dict[str, object],
    *,
    schdoc_path: Path,
) -> dict[str, object]:
    components = _schematic_components_for_sheet(design_payload, schdoc_path)
    svg_to_component = {
        str(component["svg_id"]): str(component["designator"])
        for component in components
        if component.get("svg_id") and component.get("designator")
    }
    component_to_svg = {
        designator: svg_id for svg_id, designator in svg_to_component.items()
    }
    component_to_nets = _filtered_component_to_nets(design_payload, component_to_svg)
    return {
        "svg_to_component": svg_to_component,
        "component_to_svg": component_to_svg,
        "component_to_nets": component_to_nets,
    }


def _schematic_components_for_sheet(
    design_payload: dict[str, object],
    schdoc_path: Path,
) -> list[dict[str, object]]:
    raw_components = design_payload.get("components", [])
    if not isinstance(raw_components, list):
        return []
    components = [
        component
        for component in raw_components
        if isinstance(component, dict)
    ]
    sheet_name = schdoc_path.name.lower()
    sheet_components = [
        component
        for component in components
        if _component_sheet_name(component).lower() == sheet_name
    ]
    return sheet_components or components


def _component_sheet_name(component: dict[str, object]) -> str:
    hierarchy = component.get("hierarchy")
    if isinstance(hierarchy, dict):
        return str(hierarchy.get("sheet") or "")
    return ""


def _filtered_component_to_nets(
    design_payload: dict[str, object],
    component_to_svg: dict[str, str],
) -> dict[str, object]:
    indexes = design_payload.get("indexes", {})
    if not isinstance(indexes, dict):
        return {}
    raw_component_to_nets = indexes.get("component_to_nets", {})
    if not isinstance(raw_component_to_nets, dict):
        return {}
    return {
        component: raw_component_to_nets.get(component, [])
        for component in sorted(component_to_svg)
        if component in raw_component_to_nets
    }


def _inject_svg_root_attrs_and_metadata(
    svg: str,
    *,
    root_attrs: dict[str, object],
    metadata_element: str,
) -> str:
    root_match = re.search(r"<svg\b[^>]*>", svg)
    if root_match is None:
        return svg
    root_tag = root_match.group(0)
    updated_root = root_tag
    for key, value in root_attrs.items():
        if re.search(rf"\b{re.escape(key)}\s*=", updated_root):
            continue
        updated_root = updated_root[:-1] + f' {key}="{_escape_attr(value)}">'
    enriched = svg[: root_match.start()] + updated_root + svg[root_match.end() :]
    if f'id="{SCHEMATIC_SVG_ENRICHMENT_METADATA_ID}"' in enriched:
        return enriched
    insert_at = root_match.start() + len(updated_root)
    return enriched[:insert_at] + "\n" + metadata_element + enriched[insert_at:]


def _schematic_svg_enrichment_metadata_element(payload: dict[str, object]) -> str:
    body = html.escape(json.dumps(payload, indent=2, sort_keys=True), quote=False)
    return (
        f'<metadata id="{SCHEMATIC_SVG_ENRICHMENT_METADATA_ID}" '
        f'data-schema="{SCHEMATIC_SVG_ENRICHMENT_SCHEMA}">\n'
        f"{body}\n"
        "</metadata>"
    )


def _annotate_schematic_component_groups(
    svg: str,
    *,
    design_payload: dict[str, object],
    schdoc_path: Path,
) -> str:
    for component in _schematic_components_for_sheet(design_payload, schdoc_path):
        svg_id = str(component.get("svg_id") or "").strip()
        if not svg_id:
            continue
        attrs = _schematic_component_group_attrs(component, svg_id)
        svg = _annotate_svg_group_by_id(svg, svg_id, attrs)
    return svg


def _schematic_component_group_attrs(
    component: dict[str, object],
    svg_id: str,
) -> dict[str, object]:
    attrs: dict[str, object] = {
        "data-primitive": "component",
        "data-source-kind": "schematic",
        "data-element-key": svg_id,
        "data-component-uid": svg_id,
    }
    designator = str(component.get("designator") or "").strip()
    if designator:
        attrs["data-component"] = designator
        attrs["data-designator"] = designator
    for source_key, attr_key in (
        ("library_ref", "data-symbol-library-ref"),
        ("footprint", "data-footprint"),
        ("value", "data-value"),
    ):
        value = str(component.get(source_key) or "").strip()
        if value:
            attrs[attr_key] = value
    classification = component.get("classification")
    if isinstance(classification, dict):
        component_type = str(classification.get("type") or "").strip()
        if component_type:
            attrs["data-component-type"] = component_type
    return attrs


def _annotate_svg_group_by_id(
    svg: str,
    group_id: str,
    attrs: dict[str, object],
) -> str:
    pattern = re.compile(
        rf"(<g\b(?=[^>]*\bid\s*=\s*(['\"]){re.escape(group_id)}\2)([^>]*)>)"
    )

    def replace(match: re.Match[str]) -> str:
        tag = match.group(1)
        updated = tag
        for key, value in attrs.items():
            if re.search(rf"\b{re.escape(key)}\s*=", updated):
                continue
            updated = updated[:-1] + f' {key}="{_escape_attr(value)}">'
        return updated

    return pattern.sub(replace, svg, count=1)


def _escape_attr(value: object) -> str:
    return html.escape(str(value), quote=True)


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

## Start Here

1. Read `design_review_manifest.json`; all paths in it are relative to this
   folder.
2. Read `{manifest['design_json']}` for the project-level design model.
3. Open `sch/*.svg` and `pcb/layers/*.svg` for visual context. The SVGs carry
   in-band metadata that links drawn objects back to the JSON model.
4. Use `json/schdoc/` and `json/pcbdoc/` only when you need raw Altium document
   details that are not summarized in the design JSON or SVG metadata.

## Artifact Map

- `{manifest['design_json']}`: Altium Monkey design/netlist JSON. This is the
  primary semantic model for components, nets, hierarchy, variants, PnP, and
  lookup indexes. For deeper model/API context, see the public
  [altium_monkey](https://github.com/wavenumber-eng/altium_monkey) project.
- `design_review_manifest.json`: artifact index for this bundle.
- `{manifest['notes_json']}`: JSONC dedicated notes, schematic-owned text
  frames, and schematic-owned free text by sheet. Sheet-template/title-block
  text is suppressed by default.
- `json/schdoc/` and `json/pcbdoc/`: serialized document JSON snapshots from
  `json-dump`. These are parsed-document dumps, not the high-level netlist
  summary: use them when you need exact SchDoc/PcbDoc object records, raw
  Altium fields, primitive properties, board data, or information that has not
  been promoted into the design JSON yet. SchDoc and SchLib dumps use the
  `altium_monkey.schdoc.interop.a0` and `altium_monkey.schlib.interop.a0`
  interop formats; PcbDoc payloads use the
  `altium_monkey.pcbdoc.structural.a0` document format.
- `sch/`: schematic SVGs. Each SVG root has
  `data-enrichment-schema="altium_monkey.schematic.svg.enrichment.a0"` and a
  `<metadata id="schematic-enrichment-a0">` JSON payload.
- `pcb/layers/`: PCB copper-layer SVGs with board outline, cutouts, drills, and
  slots. These use the `altium_monkey.pcb.svg.enrichment.a0` SVG contract.

## Design JSON

The design JSON is produced by `altium-monkey` and is the best starting point
for reasoning about the circuit. Important top-level areas:

- `components`: component rows with designator, value, footprint, library ref,
  hierarchy, classification, parameters, and `svg_id` where available. This is
  effectively the BOM-like part of the netlist; use it for designator, value,
  footprint, library, classification, and parameter review without needing a
  separate BOM export.
- `nets`: net rows with endpoint/component relationships.
- `indexes.svg_to_component`: maps schematic SVG group ids to component
  designators.
- `indexes.component_to_nets`: maps component designators to connected nets.
- `indexes.net_to_components`: maps a net name back to the components on it.

## Power-Tree Review Hint

For supply and power-tree analysis, it is often useful to build a derived graph
that follows nets through selected two-pin series components while still
recording the component in the explanation. Useful candidates include zero-ohm
resistors or jumpers, current-sense resistors, ferrite beads, inductors, fuses,
and other intentional power-path or ERC-link parts. This can reveal related
power nets that are separated by measurement, filtering, or configuration
elements.

Do not blindly merge every two-pin device: capacitors, LEDs, TVS parts, loads,
and protection parts have different meaning. Use component classification,
designator prefix, value text, footprint, and parameters from `components` plus
`indexes.component_to_nets` to decide which two-pin parts should be followed in
a derived power-tree view.

## Schematic SVG Links

Schematic SVG component groups are annotated when a component `svg_id` is known.
Look for attributes such as `data-component`, `data-designator`,
`data-element-key`, `data-symbol-library-ref`, `data-footprint`, and
`data-value`. To resolve a drawn component to nets:

1. Read the SVG group's `data-component` or `data-element-key`.
2. If using `data-element-key`, resolve it through
   `indexes.svg_to_component` in the design JSON or through the SVG metadata
   `view_indexes.svg_to_component`.
3. Resolve the designator through `indexes.component_to_nets`.

The embedded `schematic-enrichment-a0` metadata repeats the relevant view
indexes so a single SVG can be inspected without first loading every other
artifact.

## PCB SVG Links

PCB layer SVGs are generated from the same A0 renderer used by `pcb-svg`. The
root metadata includes board, canvas, layer, component, and net maps. Individual
drawn primitives include attributes such as `data-primitive`,
`data-layer-name`, `data-layer-role`, `data-net`, `data-net-index`,
`data-net-uid`, `data-component`, and `data-element-key` when known.

For a PCB review, start with the copper layer that matters, then use the
primitive `data-net`/`data-component` attributes to join graphical geometry back
to the design JSON. Use `json/pcbdoc/` if you need raw Altium fields for a
specific primitive or document-level board data.

## Counts

- Schematic SVGs: {schematic_count}
- PCB layer SVGs: {pcb_count}

Generated artifact paths in `design_review_manifest.json` are relative to this
bundle. Source paths are relative to the input project or document directory.
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
