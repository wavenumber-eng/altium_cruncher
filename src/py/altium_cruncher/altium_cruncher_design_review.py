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
    from altium_monkey.altium_pcb_layer_ref import PcbLayerRef
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc

DESIGN_REVIEW_MANIFEST_SCHEMA = "altium_cruncher.design_review_manifest.b0"
SCHEMATIC_SVG_ENRICHMENT_SCHEMA = "altium_monkey.schematic.svg.enrichment.a0"
SCHEMATIC_SVG_ENRICHMENT_METADATA_ID = "schematic-enrichment-a0"
COMPILED_SCHEMATIC_SVG_ENRICHMENT_SCHEMA = "altium_cruncher.schematic.svg.enrichment.b0"
COMPILED_SCHEMATIC_SVG_ENRICHMENT_METADATA_ID = "schematic-enrichment-b0"
SCHEMATIC_REVIEW_THEME = "altium_cruncher.design_review.schematic_svg.a0"
DESIGN_SCHEMA = "altium_monkey.design.b0"
COMPILED_GRAPH_SCHEMA = "altium_monkey.compiled_schematic_graph.a0"
SCHEMATIC_ARTIFACT_KEY = "sch.dwg_scene"

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
    sch_svgs, sch_irs = _write_project_schematic_artifacts(
        output_dir,
        design,
        design_payload=design_payload,
        source_base=source_base,
    )
    if not sch_svgs:
        raise ValueError(
            "Design b0 did not produce compiled schematic SVG pages; "
            "SchDoc and PrjPcb review inputs require graph-scoped artifacts"
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
        sch_irs=sch_irs,
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


def _compiled_schematic_graph(
    design_payload: dict[str, object],
) -> dict[str, object]:
    schema = design_payload.get("schema")
    if schema != DESIGN_SCHEMA:
        raise ValueError(
            f"unsupported Altium design schema {schema!r}; regenerate with "
            f"Altium Monkey Design b0 ({DESIGN_SCHEMA})"
        )
    graph = design_payload.get("compiled_schematic_graph")
    if not isinstance(graph, dict):
        raise ValueError(
            "malformed Design b0 payload: compiled_schematic_graph is required"
        )
    graph_schema = graph.get("schema")
    if graph_schema != COMPILED_GRAPH_SCHEMA:
        raise ValueError(
            "unsupported compiled schematic graph schema "
            f"{graph_schema!r}; expected {COMPILED_GRAPH_SCHEMA}"
        )
    return graph


def _compiled_schematic_pages(
    design_payload: dict[str, object],
) -> list[dict[str, object]]:
    """Return realized graph pages with narrow Altium presentation metadata."""
    graph = _compiled_schematic_graph(design_payload)
    raw_definitions, raw_pages, raw_metadata = _compiled_page_collections(
        graph,
        design_payload,
    )
    definitions = _page_definitions_by_id(raw_definitions)
    metadata_by_page = _physical_page_metadata_by_ref(raw_metadata)
    return [
        _resolved_compiled_schematic_page(
            raw_page,
            definitions=definitions,
            metadata_by_page=metadata_by_page,
        )
        for raw_page in raw_pages
    ]


def _compiled_page_collections(
    graph: dict[str, object],
    design_payload: dict[str, object],
) -> tuple[list[object], list[object], list[object]]:
    raw_definitions = graph.get("page_definitions")
    raw_pages = graph.get("page_occurrences")
    raw_metadata = design_payload.get("physical_page_metadata")
    if not isinstance(raw_definitions, list) or not isinstance(raw_pages, list):
        raise ValueError(
            "malformed compiled schematic graph: page collections are required"
        )
    if not isinstance(raw_metadata, list):
        raise ValueError(
            "malformed Design b0 payload: physical_page_metadata is required"
        )
    return raw_definitions, raw_pages, raw_metadata


def _page_definitions_by_id(
    rows: list[object],
) -> dict[str, dict[str, object]]:
    return {
        str(row.get("id") or ""): row
        for row in rows
        if isinstance(row, dict) and row.get("id")
    }


def _physical_page_metadata_by_ref(
    rows: list[object],
) -> dict[str, dict[str, object]]:
    metadata_by_page: dict[str, dict[str, object]] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("malformed physical_page_metadata row")
        page_ref = str(row.get("page_occurrence_ref") or "")
        if not page_ref or page_ref in metadata_by_page:
            raise ValueError(
                "physical_page_metadata must have one unique row per page occurrence"
            )
        metadata_by_page[page_ref] = row
    return metadata_by_page


def _resolved_compiled_schematic_page(
    raw_page: object,
    *,
    definitions: dict[str, dict[str, object]],
    metadata_by_page: dict[str, dict[str, object]],
) -> dict[str, object]:
    if not isinstance(raw_page, dict):
        raise ValueError("malformed compiled schematic graph page occurrence")
    page_ref = str(raw_page.get("id") or "")
    definition_ref = str(raw_page.get("page_definition_ref") or "")
    definition = definitions.get(definition_ref)
    metadata = metadata_by_page.get(page_ref)
    if not page_ref or definition is None or metadata is None:
        raise ValueError(
            "compiled page occurrence must resolve its definition and page metadata"
        )
    source_path = _page_definition_source_path(definition)
    source_sheet = _page_definition_source_sheet(definition, source_path)
    return {
        **raw_page,
        "page_occurrence_ref": page_ref,
        "artifact_key": SCHEMATIC_ARTIFACT_KEY,
        "source_path": source_path,
        "source_sheet": source_sheet,
        "physical_page_metadata": dict(metadata),
    }


def _page_definition_source_path(definition: dict[str, object]) -> str:
    source_identity = definition.get("source_identity")
    if not isinstance(source_identity, dict):
        return ""
    return str(source_identity.get("sch.source_key.source_path") or "")


def _page_definition_source_sheet(
    definition: dict[str, object],
    source_path: str,
) -> str:
    filename = source_path.replace("\\", "/").rsplit("/", 1)[-1]
    return filename or str(definition.get("display_name") or "sheet")


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


def _write_project_schematic_artifacts(
    output_dir: Path,
    design: object,
    *,
    design_payload: dict[str, object],
    source_base: Path,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Write resolved compiled schematic SVG and IR artifacts for a project."""
    to_physical_ir = getattr(design, "to_physical_ir", None)
    if not callable(to_physical_ir):
        log.warning("Compiled schematic rendering API is unavailable")
        return [], []

    pages = _compiled_schematic_pages(design_payload)
    if not pages:
        return [], []

    svg_dir = output_dir / "sch"
    ir_dir = output_dir / "sch-ir"
    svg_dir.mkdir(parents=True, exist_ok=True)
    ir_dir.mkdir(parents=True, exist_ok=True)
    project_parameters = _project_parameters(design)
    svg_artifacts: list[dict[str, object]] = []
    ir_artifacts: list[dict[str, object]] = []
    render_options = _physical_schematic_render_options()
    for index, page in enumerate(pages, start=1):
        page_id = str(page.get("page_occurrence_ref") or "").strip()
        if not page_id:
            continue
        source_sheet = str(page.get("source_sheet") or "sheet")
        stem = _safe_artifact_stem(f"{index:03d}_{Path(source_sheet).stem}_{page_id}")

        svg_path = svg_dir / f"{stem}.svg"
        ir_document = to_physical_ir(
            page_id,
            project_parameters=project_parameters,
            profile="onscreen",
            render_options=render_options,
        )
        ir_path = ir_dir / f"{stem}.gotir.json"
        ir_path.write_text(
            json.dumps(ir_document.to_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        log.info("Schematic IR: %s", _relpath(ir_path, output_dir))
        ir_artifacts.append(
            {
                "file": _relpath(ir_path, output_dir),
                "page_occurrence_ref": page_id,
                "artifact_key": SCHEMATIC_ARTIFACT_KEY,
                "source": _compiled_page_source(page, source_base),
                "source_sheet": source_sheet,
                "page_number": index,
                "page_count": len(pages),
            }
        )

        svg = _render_physical_ir_svg(ir_document, render_options=render_options)
        svg = _enrich_project_schematic_svg(
            svg,
            design_payload=design_payload,
            schematic_page=page,
            source_base=source_base,
        )
        svg_path.write_text(svg, encoding="utf-8")
        log.info("Schematic SVG: %s", _relpath(svg_path, output_dir))
        svg_artifacts.append(
            {
                "file": _relpath(svg_path, output_dir),
                "page_occurrence_ref": page_id,
                "artifact_key": SCHEMATIC_ARTIFACT_KEY,
                "source": _compiled_page_source(page, source_base),
                "source_sheet": source_sheet,
                "page_number": index,
                "page_count": len(pages),
            }
        )

    return svg_artifacts, ir_artifacts


def _physical_schematic_render_options() -> object:
    from altium_monkey.altium_sch_svg_renderer import SchSvgRenderOptions

    return SchSvgRenderOptions()


def _render_physical_ir_svg(
    ir_document: object,
    *,
    render_options: object,
) -> str:
    from altium_monkey.altium_sch_geometry_renderer import (
        SchGeometrySvgRenderOptions,
        SchGeometrySvgRenderer,
    )

    return SchGeometrySvgRenderer(
        SchGeometrySvgRenderOptions(
            include_workspace_background=True,
            text_mode=(
                "native_svg_export"
                if getattr(render_options, "truncate_font_size_for_baseline", False)
                else "onscreen"
            ),
            compile_mask_render_mode=getattr(
                render_options,
                "compile_mask_render_mode",
                None,
            ),
            text_as_polygons=bool(getattr(render_options, "text_as_polygons", False)),
            polygon_text_tolerance=float(
                getattr(render_options, "polygon_text_tolerance", 0.5)
            ),
            include_view_box=bool(getattr(render_options, "include_view_box", True)),
        )
    ).render(ir_document)


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
        metadata_id=SCHEMATIC_SVG_ENRICHMENT_METADATA_ID,
    )
    return _annotate_schematic_component_groups(
        svg,
        design_payload=design_payload,
        schdoc_path=schdoc_path,
    )


def _enrich_project_schematic_svg(
    svg: str,
    *,
    design_payload: dict[str, object],
    schematic_page: dict[str, object],
    source_base: Path,
) -> str:
    """Embed design-review metadata for one compiled schematic page."""
    rel_source = _compiled_page_source(schematic_page, source_base)
    page_id = str(schematic_page.get("page_occurrence_ref") or "")
    page_metadata = schematic_page.get("physical_page_metadata")
    if not isinstance(page_metadata, dict):
        page_metadata = {}
    payload = {
        "schema": COMPILED_SCHEMATIC_SVG_ENRICHMENT_SCHEMA,
        "source": {
            "altium_schdoc_file": rel_source,
            "page_occurrence_ref": page_id,
            "artifact_key": SCHEMATIC_ARTIFACT_KEY,
        },
        "view": {
            "kind": "compiled_schematic_page",
            "profile": "design_review",
            "sheet_name": Path(str(schematic_page.get("source_sheet") or "")).stem,
            "sheet_file": str(schematic_page.get("source_sheet") or ""),
            "page_occurrence_ref": page_id,
            "artifact_key": SCHEMATIC_ARTIFACT_KEY,
            "physical_page_metadata": page_metadata,
        },
    }
    root_attrs = {
        "data-enrichment-schema": COMPILED_SCHEMATIC_SVG_ENRICHMENT_SCHEMA,
        "data-view-kind": "compiled_schematic_page",
        "data-profile": "design_review",
        "data-source": rel_source,
        "data-sheet-name": Path(str(schematic_page.get("source_sheet") or "")).stem,
        "data-page-occurrence-ref": page_id,
        "data-artifact-key": SCHEMATIC_ARTIFACT_KEY,
        "data-review-theme": SCHEMATIC_REVIEW_THEME,
    }
    svg = _inject_svg_root_attrs_and_metadata(
        svg,
        root_attrs=root_attrs,
        metadata_element=_schematic_svg_enrichment_metadata_element(
            payload,
            schema=COMPILED_SCHEMATIC_SVG_ENRICHMENT_SCHEMA,
            metadata_id=COMPILED_SCHEMATIC_SVG_ENRICHMENT_METADATA_ID,
        ),
        metadata_id=COMPILED_SCHEMATIC_SVG_ENRICHMENT_METADATA_ID,
    )
    return _annotate_compiled_schematic_graph_links(
        svg,
        design_payload=design_payload,
        schematic_page=schematic_page,
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
        component for component in raw_components if isinstance(component, dict)
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
    metadata_id: str,
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
    if f'id="{metadata_id}"' in enriched:
        return enriched
    insert_at = root_match.start() + len(updated_root)
    return enriched[:insert_at] + "\n" + metadata_element + enriched[insert_at:]


def _schematic_svg_enrichment_metadata_element(
    payload: dict[str, object],
    *,
    schema: str = SCHEMATIC_SVG_ENRICHMENT_SCHEMA,
    metadata_id: str = SCHEMATIC_SVG_ENRICHMENT_METADATA_ID,
) -> str:
    body = html.escape(json.dumps(payload, indent=2, sort_keys=True), quote=False)
    return f'<metadata id="{metadata_id}" data-schema="{schema}">\n{body}\n</metadata>'


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


def _annotate_compiled_schematic_graph_links(
    svg: str,
    *,
    design_payload: dict[str, object],
    schematic_page: dict[str, object],
) -> str:
    graph = _compiled_schematic_graph(design_payload)
    page_ref = str(schematic_page.get("page_occurrence_ref") or "")
    components = _rows_by_id(graph.get("component_occurrences"))
    design_components = _rows_by_key(design_payload.get("components"), "designator")
    for link in _scoped_graphical_artifact_links(graph, page_ref):
        element_id = str(link["element_id"])
        attrs = _graphical_link_attrs(link, page_ref)
        attrs.update(
            _component_graphical_link_attrs(
                link,
                element_id=element_id,
                components=components,
                design_components=design_components,
            )
        )
        svg = _annotate_svg_group_by_id(svg, element_id, attrs)
    return svg


def _rows_by_id(value: object) -> dict[str, dict[str, object]]:
    return _rows_by_key(value, "id")


def _rows_by_key(value: object, key: str) -> dict[str, dict[str, object]]:
    if not isinstance(value, list):
        return {}
    return {
        str(row.get(key) or ""): row
        for row in value
        if isinstance(row, dict) and row.get(key)
    }


def _scoped_graphical_artifact_links(
    graph: dict[str, object],
    page_ref: str,
) -> list[dict[str, object]]:
    value = graph.get("graphical_artifact_links")
    if not isinstance(value, list):
        return []
    return [
        link
        for link in value
        if isinstance(link, dict)
        and str(link.get("page_occurrence_ref") or "") == page_ref
        and str(link.get("artifact_key") or "") == SCHEMATIC_ARTIFACT_KEY
        and str(link.get("element_id") or "").strip()
    ]


def _graphical_link_attrs(
    link: dict[str, object],
    page_ref: str,
) -> dict[str, object]:
    return {
        "data-page-occurrence-ref": page_ref,
        "data-artifact-key": SCHEMATIC_ARTIFACT_KEY,
        "data-element-id": str(link["element_id"]),
        "data-graph-target-type": str(link.get("target_type") or ""),
        "data-graph-target-ref": str(link.get("target_ref") or ""),
    }


def _component_graphical_link_attrs(
    link: dict[str, object],
    *,
    element_id: str,
    components: dict[str, dict[str, object]],
    design_components: dict[str, dict[str, object]],
) -> dict[str, object]:
    if link.get("target_type") != "sch.component_occurrence":
        return {}
    component_ref = str(link.get("target_ref") or "")
    component = components.get(component_ref)
    if component is None:
        return {}
    physical_designator = str(
        component.get("physical_designator")
        or component.get("display_designator")
        or ""
    )
    attrs = _schematic_component_group_attrs(
        design_components.get(physical_designator, component),
        element_id,
    )
    attrs["data-component-occurrence-ref"] = component_ref
    return attrs


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
    attrs.update(_component_identity_attrs(component))
    attrs.update(_component_variant_attrs(component))
    attrs.update(_component_descriptive_attrs(component))
    attrs.update(_component_classification_attrs(component))
    return attrs


def _component_identity_attrs(component: dict[str, object]) -> dict[str, object]:
    designator = str(component.get("designator") or "").strip()
    if not designator:
        return {}
    return {
        "data-component": designator,
        "data-designator": designator,
    }


def _component_variant_attrs(component: dict[str, object]) -> dict[str, object]:
    attrs: dict[str, object] = {}
    if "dnp" in component:
        attrs["data-dnp"] = "true" if bool(component.get("dnp")) else "false"
    if "fitted" in component:
        attrs["data-fitted"] = "true" if bool(component.get("fitted")) else "false"
    return attrs


def _component_descriptive_attrs(component: dict[str, object]) -> dict[str, object]:
    attrs: dict[str, object] = {}
    for source_key, attr_key in (
        ("library_ref", "data-symbol-library-ref"),
        ("footprint", "data-footprint"),
        ("value", "data-value"),
    ):
        value = str(component.get(source_key) or "").strip()
        if value:
            attrs[attr_key] = value
    return attrs


def _component_classification_attrs(
    component: dict[str, object],
) -> dict[str, object]:
    classification = component.get("classification")
    if not isinstance(classification, dict):
        return {}
    component_type = str(classification.get("type") or "").strip()
    if not component_type:
        return {}
    return {"data-component-type": component_type}


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
            root_subdir="json",
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
    from altium_cruncher.altium_cruncher_pcb_layer_resolve import (
        pcb_layer_ref_sort_key,
    )
    from altium_cruncher.altium_cruncher_pcb_svg_a0_renderer import PcbSvgA0Renderer

    renderer = PcbSvgA0Renderer(config)
    # _collect_visible_layers yields V7-aware render layers since
    # altium-monkey 2026.8.1; keep the refs so Mechanical17+/Mid31+ content
    # classifies correctly.
    refs = {
        layer.ref
        for layer in renderer._collect_visible_layers(pcbdoc)  # noqa: SLF001
        if layer.is_copper()
    }
    refs.update(_pcb_review_primitive_copper_layers(pcbdoc))
    tokens = [ref.token for ref in sorted(refs, key=pcb_layer_ref_sort_key)]
    return tokens or [PcbLayer.TOP.to_json_name(), PcbLayer.BOTTOM.to_json_name()]


def _pcb_review_primitive_copper_layers(
    pcbdoc: "AltiumPcbDoc",
) -> set["PcbLayerRef"]:
    from altium_monkey.altium_record_types import PcbLayer
    from altium_cruncher.altium_cruncher_pcb_layer_resolve import (
        pcb_layer_ref_is_copper,
        resolve_pcb_layer_ref,
    )

    multilayer_token = PcbLayer.MULTI_LAYER.to_json_name()
    layers: set["PcbLayerRef"] = set()
    saw_multilayer = False
    for layer_value in _iter_pcb_review_layer_values(pcbdoc):
        ref = _pcb_layer_ref_from_value(layer_value)
        if ref is None:
            continue
        if ref.token == multilayer_token:
            saw_multilayer = True
            continue
        if pcb_layer_ref_is_copper(ref):
            layers.add(ref)
    if saw_multilayer and not layers:
        layers.update(
            {
                resolve_pcb_layer_ref(PcbLayer.TOP),
                resolve_pcb_layer_ref(PcbLayer.BOTTOM),
            }
        )
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


def _pcb_layer_ref_from_value(value: object) -> "PcbLayerRef | None":
    from altium_cruncher.altium_cruncher_pcb_layer_resolve import (
        resolve_pcb_layer_ref_or_none,
    )

    return resolve_pcb_layer_ref_or_none(value)


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
    sch_irs: list[dict[str, object]],
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
        "schematic_irs": sch_irs,
        "pcb_svgs": pcb_artifacts,
        "readme": _relpath(readme_path, output_dir),
    }


def _readme_text(
    input_file: Path,
    output_dir: Path,
    manifest: dict[str, object],
) -> str:
    schematic_count = len(manifest.get("schematic_svgs", []))
    schematic_ir_count = len(manifest.get("schematic_irs", []))
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
2. Read `{manifest["design_json"]}` for the project-level design model.
3. Open `sch/*.svg` for schematic context. SchDoc and PrjPcb inputs both emit
   compiled, resolved schematic pages. Open `pcb/layers/*.svg` for PCB context. The SVGs
   carry in-band metadata that links drawn objects back to the JSON model.
4. Use `json/schdoc/` and `json/pcbdoc/` only when you need raw Altium document
   details that are not summarized in the design JSON or SVG metadata.

## Instructions for Review Agents

- Treat the bundled Design b0 `compiled_schematic_graph` as the authoritative
  schematic topology. Do not reconstruct connectivity from SVG geometry,
  repeated net names, page proximity, or the legacy convenience indexes.
- Select a schematic page by canonical `page_occurrence_ref`. Reused sheets can
  share source drawings, labels, and element ids, so an `element_id` alone is
  never a globally unique selector.
- Join SVG evidence to semantics only with the full scoped selector
  `page_occurrence_ref + artifact_key + element_id`, then verify the group's
  `data-graph-target-type` and `data-graph-target-ref` against the matching
  `graphical_artifact_links` row.
- Traverse hierarchy through graph terminals and
  `hierarchy_terminal_bindings`; traverse within a page through
  `local_net_occurrences`. Do not merge same-named local nets across pages
  unless the graph supplies the boundary relationship.
- Apply DNP, fitted, and design-variant facts from the top-level Design rows.
  The compiled graph is intentionally variant-neutral and represents the
  complete source schematic.
- If a scoped SVG selector, graph target, page reference, or hierarchy binding
  cannot be resolved, report that as missing evidence. Do not silently infer a
  replacement from a similar designator or net name.
- Use raw SchDoc/PcbDoc JSON to inspect source records and properties, not as a
  competing compiled connectivity model.

## Artifact Map

- `{manifest["design_json"]}`: Altium Monkey design/netlist JSON. This is the
  primary semantic model for components, nets, hierarchy, variants, PnP, and
  lookup indexes. Design b0 embeds the authoritative
  variant-neutral compiled schematic graph. Repeated sheets and channels use
  canonical page, hierarchy, component, local-net, terminal, binding, and
  drawing-link occurrences. For deeper model/API context, see the public
  [altium_monkey](https://github.com/wavenumber-eng/altium_monkey) project.
- `design_review_manifest.json`: artifact index for this bundle.
- `{manifest["notes_json"]}`: JSONC dedicated notes, schematic-owned text
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
- `sch/`: schematic SVGs. For SchDoc and PrjPcb inputs these are compiled schematic
  pages with resolved channel/repeated-sheet designators. Each SVG root has
  `data-enrichment-schema="altium_cruncher.schematic.svg.enrichment.b0"` and a
  `<metadata id="schematic-enrichment-b0">` JSON payload.
- `sch-ir/`: schematic IR JSON for SchDoc and PrjPcb inputs. These use
  `AltiumDesign.to_physical_ir()` so repeated/channel component designators are
  resolved before IR emission.
- `pcb/layers/`: PCB copper-layer SVGs with board outline, cutouts, drills, and
  slots. These use the `altium_monkey.pcb.svg.enrichment.a0` SVG contract.

## Design JSON

The design JSON is produced by `altium-monkey` and is the best starting point
for reasoning about the circuit. Important top-level areas:

- `components`: component rows with designator, value, footprint, library ref,
  hierarchy, classification, parameters, and `svg_id` where available. For
  project inputs these designators are physical/resolved when the compiled
  model can resolve repeated sheets or channels. This is effectively the
  BOM-like part of the netlist; use it for designator, value, footprint,
  library, classification, and parameter review without needing a separate BOM
  export.
- `nets`: net rows with endpoint/component relationships. When available,
  `aliases` and `name_sources` describe additional labels, ports, power names,
  and other discovered names that did not win Altium's net-name selection.
- `compiled_schematic_graph`: the required source-neutral graph. Select pages
  from `page_occurrences`; use `component_occurrences`,
  `local_net_occurrences`, `terminal_occurrences`, and
  `hierarchy_terminal_bindings` for schematic semantics.
- `physical_page_metadata`: Altium channel, room, path, and document
  presentation facts keyed by canonical `page_occurrence_ref`. It does not
  repeat components or nets.
- `compiled_schematic_graph.graphical_artifact_links`: maps the scoped drawing
  selector `page_occurrence_ref + artifact_key + element_id` to its semantic
  graph target. Current schematic review artifacts use
  `artifact_key="sch.dwg_scene"`.
- `indexes.svg_to_component`: legacy scalar mapping from schematic SVG group ids
  to component designators. It is populated only when a logical SVG id maps
  unambiguously to one physical component.
- `indexes.svg_to_components`: maps a logical schematic SVG group id to every
  physical designator represented by that source object.
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
For SchDoc and PrjPcb inputs, the `sch/*.svg` files are compiled physical pages and each
root carries `data-page-occurrence-ref` and
`data-artifact-key="sch.dwg_scene"`. Linked source groups carry the same scoped
selector, and component groups also carry `data-component-occurrence-ref`.
Look for attributes such as `data-component`, `data-designator`, `data-element-key`,
`data-symbol-library-ref`, `data-footprint`, and `data-value`. To resolve a
drawn component to nets:

1. Read the SVG root `data-page-occurrence-ref` and `data-artifact-key`, plus
   the source group's `data-element-id`.
2. Resolve that tuple through graph `graphical_artifact_links`.
3. Follow the graph target ref to a component, terminal, local net, or page.
4. For a component target, use its physical designator with the top-level
   Design component and variant rows; optional compatibility indexes may then
   provide convenient net-name lookups.

The embedded `schematic-enrichment-b0` metadata records artifact identity and
page presentation only. It does not duplicate the semantic graph; load the
bundle's Design JSON sidecar for semantic traversal.

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
- Schematic IRs: {schematic_ir_count}
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


def _compiled_page_source(page: dict[str, object], source_base: Path) -> str:
    source_path = str(page.get("source_path") or "").strip()
    if source_path:
        path = Path(source_path)
        if path.is_absolute():
            return _source_path(path, source_base)
        return source_path.replace("\\", "/")
    return str(page.get("source_sheet") or "")


def _safe_artifact_stem(value: str) -> str:
    stem = re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("._")
    return stem or "artifact"
