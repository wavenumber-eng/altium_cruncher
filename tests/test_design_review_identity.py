"""DR enrichment must not confuse display labels with realized identity."""

import xml.etree.ElementTree as ET

import pytest

from altium_cruncher.altium_cruncher_design_review import (
    _annotate_compiled_schematic_graph_links,
)


def component_row(uid, page="physical-a", value="10k", dnp=False, **extra):
    return dict(
        designator="R?", source_unique_id=uid, physical_sheet_id=page,
        value=value, dnp=dnp, fitted=not dnp, **extra,
    )


def enrich(rows, bodies, *, physical_page="physical-a"):
    graph = {
        "schema": "altium_monkey.compiled_schematic_graph.a0",
        "component_occurrences": [],
        "graphical_artifact_links": [],
    }
    for index, uid in enumerate(bodies):
        graph["component_occurrences"].append({
            "id": f"component-{index}", "page_occurrence_ref": "page-a",
            "physical_designator": "R?", "display_designator": "R?",
            "unit": index + 1,
            "source_identity": {"sch.source_key.source_uuid": uid},
        })
        graph["graphical_artifact_links"].append({
            "page_occurrence_ref": "page-a", "artifact_key": "sch.dwg_scene",
            "element_id": f"body-{index}", "target_type": "sch.component_occurrence",
            "target_ref": f"component-{index}",
        })
    svg = "<svg>" + "".join(f'<g id="body-{i}"></g>' for i in range(len(bodies))) + "</svg>"
    result = _annotate_compiled_schematic_graph_links(
        svg,
        design_payload={"schema": "altium_monkey.design.b0", "components": rows,
                        "compiled_schematic_graph": graph},
        schematic_page={"page_occurrence_ref": "page-a", "physical_document_id": physical_page},
    )
    return [group.attrib for group in ET.fromstring(result)]


def test_duplicate_labels_keep_distinct_values_and_variant_states():
    groups = enrich([component_row("uid-a", ambiguous_physical_designator=True), component_row("uid-b", value="100k", dnp=True)], ["uid-a", "uid-b"])
    assert [(g["data-value"], g["data-dnp"], g["data-fitted"]) for g in groups] == [
        ("10k", "false", "true"), ("100k", "true", "false"),
    ]
    assert [g["data-component-occurrence-ref"] for g in groups] == ["component-0", "component-1"]


def test_reused_source_uid_is_scoped_to_the_rendered_physical_page():
    rows = [component_row("uid-a"), component_row("uid-a", "physical-b", "100k", True)]
    first = enrich(rows, ["uid-a"])[0]
    second = enrich(rows, ["uid-a"], physical_page="physical-b")[0]
    assert (first["data-value"], first["data-dnp"]) == ("10k", "false")
    assert (second["data-value"], second["data-dnp"]) == ("100k", "true")


@pytest.mark.parametrize("rows,bodies,page", [
    ([component_row("uid-a"), component_row("uid-a", value="100k")], ["uid-a"], "physical-a"),
    ([component_row("uid-a")], [""], "physical-a"),
    ([component_row("uid-a")], ["uid-a"], ""),
    ([component_row("uid-a")], ["other-uid"], "physical-a"),
])
def test_unproven_identity_keeps_graph_evidence_without_metadata(rows, bodies, page):
    group = enrich(rows, bodies, physical_page=page)[0]
    assert group["data-component-occurrence-ref"] == "component-0"
    assert group["data-designator"] == "R?"
    assert not {"data-value", "data-dnp", "data-fitted"} & group.keys()


def test_multipart_body_without_aggregate_source_match_is_not_guessed():
    # Design b0 can expose an aggregate component row for only one source body.
    first, second = enrich([component_row("body-a")], ["body-a", "body-b"])
    assert first["data-value"] == "10k"
    assert second["data-designator"] == "R?"
    assert second["data-component-occurrence-ref"] == "component-1"
    assert "data-value" not in second
