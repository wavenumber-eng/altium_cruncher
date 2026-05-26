import argparse

from altium_cruncher.altium_cruncher_cmd_sch_svg import cmd_sch_svg
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
    svg = (output_dir / "display_modes.svg").read_text(encoding="utf-8")
    assert "CLI_DM0_RECT" not in svg
    assert "MODE_0" not in svg
    assert "CLI_DM1_RECT" in svg
    assert "MODE_1" in svg
