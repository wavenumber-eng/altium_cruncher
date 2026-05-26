from altium_cruncher.altium_clean import AltiumCleanConfig, apply_clean_to_schlib
from altium_monkey.altium_record_types import LineWidth
from altium_monkey.altium_record_sch__pin import AltiumSchPin
from altium_monkey.altium_schlib import AltiumSchLib


def _record_types(symbol) -> list[str]:
    return [str(record.get("RECORD")) for record in symbol.raw_records]


def test_schlib_clean_moves_body_rectangle_behind_pins(tmp_path):
    source_path = tmp_path / "body_after_pins.SchLib"
    output_path = tmp_path / "cleaned.SchLib"

    schlib = AltiumSchLib()
    symbol = schlib.add_symbol("BODY_AFTER_PINS")
    symbol.add_pin(AltiumSchPin("1", "A", -100, 0, orientation=2, length=100))
    symbol.add_pin(AltiumSchPin("2", "B", 100, 0, orientation=0, length=100))
    symbol.add_rectangle(-50, -50, 50, 50, is_solid=False, transparent=True)
    schlib.save(source_path, sync_pin_text_data=True)

    loaded = AltiumSchLib(source_path)
    before_types = _record_types(loaded.symbols[0])
    assert before_types.index("2") < before_types.index("14")

    result = apply_clean_to_schlib(loaded, AltiumCleanConfig.template())

    cleaned_symbol = loaded.symbols[0]
    object_types = [type(obj).__name__ for obj in cleaned_symbol.objects]
    raw_types = _record_types(cleaned_symbol)
    assert result.reordered_rectangles == 1
    assert object_types.index("AltiumSchRectangle") < object_types.index("AltiumSchPin")
    assert raw_types.index("14") < raw_types.index("2")

    loaded.save(output_path, sync_pin_text_data=True)
    reloaded_types = _record_types(AltiumSchLib(output_path).symbols[0])
    assert reloaded_types.index("14") < reloaded_types.index("2")


def test_schlib_clean_keeps_body_rectangle_behind_internal_graphics(tmp_path):
    source_path = tmp_path / "body_after_graphics.SchLib"
    output_path = tmp_path / "cleaned.SchLib"

    schlib = AltiumSchLib()
    symbol = schlib.add_symbol("INTERNAL_GRAPHICS")
    symbol.add_ellipse(0, 0, 30, 30, area_color=0xFF0000, is_solid=True)
    symbol.add_pin(AltiumSchPin("1", "A", -120, 0, orientation=2, length=100))
    symbol.add_rectangle(-100, -100, 100, 100, is_solid=False, transparent=True)
    symbol.add_rectangle(
        -30,
        -30,
        30,
        30,
        color=0xFF0000,
        area_color=0xFF0000,
        line_width=LineWidth.SMALLEST,
        is_solid=True,
    )
    schlib.save(source_path, sync_pin_text_data=True)

    loaded = AltiumSchLib(source_path)
    result = apply_clean_to_schlib(loaded, AltiumCleanConfig.template())
    cleaned_symbol = loaded.symbols[0]

    rectangles = cleaned_symbol.rectangles
    body_rectangle = next(
        rect for rect in rectangles if abs(rect.corner.x_mils - rect.location.x_mils) == 200
    )
    marker_rectangle = next(
        rect for rect in rectangles if abs(rect.corner.x_mils - rect.location.x_mils) == 60
    )
    ellipse = cleaned_symbol.ellipses[0]
    pin = cleaned_symbol.pins[0]

    assert result.matched_rectangles == 1
    assert result.reordered_rectangles == 1
    assert marker_rectangle.area_color == 0xFF0000
    assert marker_rectangle.line_width == LineWidth.SMALLEST
    assert cleaned_symbol.objects.index(body_rectangle) < cleaned_symbol.objects.index(ellipse)
    assert cleaned_symbol.objects.index(ellipse) < cleaned_symbol.objects.index(pin)

    loaded.save(output_path, sync_pin_text_data=True)
    reloaded = AltiumSchLib(output_path).symbols[0]
    reloaded_body = next(
        rect for rect in reloaded.rectangles if abs(rect.corner.x_mils - rect.location.x_mils) == 200
    )
    reloaded_marker = next(
        rect for rect in reloaded.rectangles if abs(rect.corner.x_mils - rect.location.x_mils) == 60
    )
    assert reloaded_marker.area_color == 0xFF0000
    assert reloaded.objects.index(reloaded_body) < reloaded.objects.index(reloaded.ellipses[0])


def test_schlib_clean_prefers_backmost_body_rectangle_over_larger_front_rectangle(tmp_path):
    source_path = tmp_path / "backmost_body.SchLib"

    schlib = AltiumSchLib()
    symbol = schlib.add_symbol("BACKMOST_BODY")
    symbol.add_rectangle(-50, -50, 50, 50, is_solid=False, transparent=True)
    symbol.add_ellipse(0, 0, 20, 20, area_color=0xFF0000, is_solid=True)
    symbol.add_rectangle(
        -120,
        -120,
        120,
        120,
        color=0xFF0000,
        area_color=0xFF0000,
        line_width=LineWidth.SMALLEST,
        is_solid=True,
    )
    schlib.save(source_path, sync_pin_text_data=True)

    loaded = AltiumSchLib(source_path)
    result = apply_clean_to_schlib(loaded, AltiumCleanConfig.template())
    rectangles = loaded.symbols[0].rectangles
    body_rectangle = next(
        rect for rect in rectangles if abs(rect.corner.x_mils - rect.location.x_mils) == 100
    )
    front_rectangle = next(
        rect for rect in rectangles if abs(rect.corner.x_mils - rect.location.x_mils) == 240
    )

    assert result.matched_rectangles == 1
    assert body_rectangle.is_solid is True
    assert body_rectangle.transparent is False
    assert front_rectangle.area_color == 0xFF0000
    assert front_rectangle.line_width == LineWidth.SMALLEST
