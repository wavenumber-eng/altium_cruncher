from pathlib import Path
import xml.etree.ElementTree as ET

import pytest

from altium_cruncher.pcb_svg_artifacts import write_or_update_view_svg


NS = "{http://www.w3.org/2000/svg}"
GROUP_ID = "pcb-svg-view-bottom"


@pytest.mark.parametrize(
    ("old_transform", "new_transform", "width"),
    [
        (None, "translate(20 0) scale(-1 1)", 20),
        ("translate(20 0) scale(-1 1)", None, 20),
        ("translate(20 0) scale(-1 1)", "translate(40 0) scale(-1 1)", 40),
        ("translate(20 0) scale(-1 1)", "translate(20 0) scale(-1 1)", 20),
    ],
    ids=["enable-mirror", "disable-mirror", "resize-mirrored-canvas", "same-view"],
)
def test_update_refreshes_scene_transform_and_preserves_user_content(
    tmp_path: Path, old_transform: str | None, new_transform: str | None, width: int
) -> None:
    old_root = ET.fromstring(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 10">'
        '<text id="page-note">page</text>'
        '<g id="scene" data-user-tag="keep">'
        '<path id="scene-note" d="M 1 2 L 3 4"/>'
        '<g id="user-wrapper" transform="translate(1 2)">'
        f'<g id="{GROUP_ID}"><path id="old"/></g>'
        '</g></g></svg>'
    )
    scene = old_root.find(f"{NS}g")
    assert scene is not None
    if old_transform is not None:
        scene.set("transform", old_transform)
    target = tmp_path / "view.svg"
    target.write_text(ET.tostring(old_root, encoding="unicode"), encoding="utf-8")
    new_root = ET.fromstring(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 10">'
        f'<g id="scene"><g id="{GROUP_ID}"><path id="new"/></g></g></svg>'
    )
    new_scene = new_root.find(f"{NS}g")
    assert new_scene is not None
    if new_transform is not None:
        new_scene.set("transform", new_transform)

    write_or_update_view_svg(
        target, ET.tostring(new_root, encoding="unicode"), group_id=GROUP_ID
    )

    updated = ET.fromstring(target.read_text(encoding="utf-8"))
    by_id = {element.get("id"): element for element in updated.iter()}
    assert updated.get("viewBox") == f"0 0 {width} 10"
    assert by_id["scene"].get("transform") == new_transform
    assert by_id["scene"].get("data-user-tag") == "keep"
    assert by_id["page-note"].text == "page"
    assert by_id["scene-note"].get("d") == "M 1 2 L 3 4"
    assert by_id["user-wrapper"].get("transform") == "translate(1 2)"
    assert list(by_id["user-wrapper"]) == [by_id[GROUP_ID]]
    assert "new" in by_id and "old" not in by_id


def test_legacy_group_without_scene_gets_generated_mirror_wrapper(tmp_path: Path) -> None:
    target = tmp_path / "view.svg"
    target.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg">'
        '<text id="page-note">keep</text>'
        f'<g id="{GROUP_ID}"><path id="old"/></g></svg>',
        encoding="utf-8",
    )
    replacement = (
        '<svg xmlns="http://www.w3.org/2000/svg">'
        '<g id="scene" transform="translate(20 0) scale(-1 1)">'
        f'<g id="{GROUP_ID}"><path id="new"/></g></g></svg>'
    )

    write_or_update_view_svg(target, replacement, group_id=GROUP_ID)

    updated = ET.fromstring(target.read_text(encoding="utf-8"))
    scene = updated.find(f"{NS}g[@id='scene']")
    assert scene is not None
    assert scene.get("transform") == "translate(20 0) scale(-1 1)"
    assert scene.find(f"{NS}g[@id='{GROUP_ID}']/{NS}path[@id='new']") is not None
    assert updated.find(f"{NS}text[@id='page-note']") is not None
