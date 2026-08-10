import argparse
import json

from altium_cruncher.altium_cruncher_cmd_sch_svg import (
    _write_project_schematic_svgs,
    cmd_sch_svg,
)
from altium_monkey.altium_record_sch__pin import AltiumSchPin
from altium_monkey.altium_record_sch__rectangle import AltiumSchRectangle
from altium_monkey.altium_record_types import CoordPoint
from altium_monkey.altium_schdoc import AltiumSchDoc


def _add_mode_children(doc: AltiumSchDoc, component, mode: int) -> None:
    rectangle = AltiumSchRectangle()
    rectangle.unique_id = f"CLI_DM{mode}_RECT"
    rectangle.location = CoordPoint.from_mils(-50, -50 + (mode * 200))
    rectangle.corner = CoordPoint.from_mils(50, 50 + (mode * 200))
    rectangle.owner_part_id = 1
    rectangle.owner_part_display_mode = mode
    doc.add_object(rectangle, owner=component)

    pin = AltiumSchPin(
        str(mode + 1),
        f"MODE_{mode}",
        -150,
        mode * 200,
        orientation=2,
        length=100,
        owner_part_id=1,
        owner_part_display_mode=mode,
    )
    pin.unique_id = f"CLI_DM{mode}_PIN"
    doc.add_object(pin, owner=component)


def test_sch_svg_command_filters_component_display_modes(tmp_path) -> None:
    schdoc_path = tmp_path / "display_modes.SchDoc"
    output_dir = tmp_path / "svg"

    doc = AltiumSchDoc()
    component = doc.add_component(
        "ALT_MODE_SYMBOL",
        "J1",
        x=1000,
        y=1000,
        display_mode=1,
        display_mode_count=2,
    )
    _add_mode_children(doc, component, 0)
    _add_mode_children(doc, component, 1)
    assert doc.save(schdoc_path)

    result = cmd_sch_svg(argparse.Namespace(file=str(schdoc_path), output=output_dir))

    assert result == 0
    manifest = json.loads(
        (output_dir / "schematic_svg_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["schema"] == "altium_cruncher.schematic_svg_manifest.b0"
    assert len(manifest["svgs"]) == 1
    svg = (output_dir / manifest["svgs"][0]["file"]).read_text(encoding="utf-8")
    assert 'data-enrichment-schema="altium_cruncher.schematic.svg.enrichment.b0"' in svg
    assert (output_dir / manifest["design_json"]).exists()
    assert "CLI_DM0_RECT" not in svg
    assert "MODE_0" not in svg
    assert "CLI_DM1_RECT" in svg
    assert "MODE_1" in svg


def test_sch_svg_project_writer_emits_compiled_page_svgs(tmp_path) -> None:
    class FakeDesign:
        def to_json(self, *, include_indexes: bool) -> dict[str, object]:
            assert include_indexes is True
            return {
                "schema": "altium_monkey.design.b0",
                "compiled_schematic_graph": {
                    "schema": "altium_monkey.compiled_schematic_graph.a0",
                    "type": "sch.compiled_schematic_graph",
                    "identity_namespace": "sch.compiled_schematic_graph.a0",
                    "unit_definitions": [],
                    "page_definitions": [
                        {
                            "id": "PDEF",
                            "display_name": "Leaf.SchDoc",
                            "source_identity": {
                                "sch.source_key.source_path": "Leaf.SchDoc"
                            },
                        }
                    ],
                    "unit_occurrences": [],
                    "page_occurrences": [
                        {"id": "PAGE_A", "page_definition_ref": "PDEF"},
                        {"id": "PAGE_B", "page_definition_ref": "PDEF"},
                    ],
                    "hierarchy_occurrences": [],
                    "component_occurrences": [],
                    "local_net_occurrences": [],
                    "terminal_occurrences": [],
                    "hierarchy_terminal_bindings": [],
                    "graphical_artifact_links": [],
                },
                "physical_page_metadata": [
                    {
                        "page_occurrence_ref": "PAGE_A",
                        "physical_instance_path": "Leaf/A",
                        "room_name": "Leaf_A",
                    },
                    {
                        "page_occurrence_ref": "PAGE_B",
                        "physical_instance_path": "Leaf/B",
                        "room_name": "Leaf_B",
                    },
                ],
            }

        def to_physical_svg(self, page_id: str, **kwargs: object) -> str:
            assert kwargs["project_parameters"] == {"VariantName": "Base"}
            assert kwargs["wrap_components"] is True
            designator = {"PAGE_A": "R1.1", "PAGE_B": "R1.2"}[page_id]
            return f'<svg data-doc-id="{page_id}"><text>{designator}</text></svg>'

    count = _write_project_schematic_svgs(
        FakeDesign(),
        tmp_path,
        project_parameters={"VariantName": "Base"},
    )

    assert count == 2
    outputs = sorted(path.name for path in tmp_path.glob("*.svg"))
    assert outputs == ["001_Leaf_Leaf_A.svg", "002_Leaf_Leaf_B.svg"]
    assert "R1.1" in (tmp_path / outputs[0]).read_text(encoding="utf-8")
    assert "R1.2" in (tmp_path / outputs[1]).read_text(encoding="utf-8")
