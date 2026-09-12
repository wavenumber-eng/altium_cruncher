"""Durable SVG group replacement and artifact writing.

Preserve consumer-authored siblings while replacing the generated view and its
metadata. Legacy generated siblings are removed; unusable files are replaced.
"""
from __future__ import annotations

import logging
from pathlib import Path
import xml.etree.ElementTree as ET
from altium_monkey.altium_pcb_svg_renderer import SVG_ENRICHMENT_METADATA_ID

_SVG_NS = "http://www.w3.org/2000/svg"
log = logging.getLogger(__name__)


def _extract_svg_group(svg_text: str, group_id: str) -> ET.Element:
    root = ET.fromstring(svg_text)
    result = _find_element_by_id(root, group_id)
    if result is None:
        raise ValueError(
            f"Generated SVG does not contain expected group id {group_id!r}"
        )
    return result


def _find_element_by_id(root: ET.Element, group_id: str) -> ET.Element | None:
    for elem in root.iter():
        if elem.attrib.get("id") == group_id:
            return elem
    return None


def _is_svg_group(elem: ET.Element) -> bool:
    return elem.tag in {"g", f"{{{_SVG_NS}}}g"}


def _is_legacy_generated_view_artifact(elem: ET.Element) -> bool:
    if elem.attrib.get("data-feature") == "board-cutout-label":
        return True
    if not _is_svg_group(elem):
        return False
    return (
        elem.attrib.get("data-layer-key") is not None
        or elem.attrib.get("id") == "board-outline"
    )


def _remove_legacy_generated_view_artifacts(
    root: ET.Element, protected_group_id: str
) -> None:
    protected_group = _find_element_by_id(root, protected_group_id)
    protected_descendant_ids = (
        {id(elem) for elem in protected_group.iter()}
        if protected_group is not None
        else set()
    )
    parent_map = {child: parent for parent in root.iter() for child in parent}
    removals: list[tuple[ET.Element, ET.Element]] = []
    for elem in root.iter():
        if id(elem) in protected_descendant_ids:
            continue
        if _is_legacy_generated_view_artifact(elem):
            parent = parent_map.get(elem)
            if parent is not None:
                removals.append((parent, elem))
    for parent, elem in removals:
        try:
            parent.remove(elem)
        except ValueError:
            continue


def _replace_generated_metadata(
    existing_root: ET.Element, new_root: ET.Element
) -> None:
    new_metadata = _find_element_by_id(new_root, SVG_ENRICHMENT_METADATA_ID)
    old_metadata = _find_element_by_id(existing_root, SVG_ENRICHMENT_METADATA_ID)
    parent_map = {child: parent for parent in existing_root.iter() for child in parent}
    if new_metadata is None:
        if old_metadata is not None:
            parent = parent_map.get(old_metadata)
            if parent is not None:
                parent.remove(old_metadata)
        return
    if old_metadata is None:
        existing_root.insert(0, new_metadata)
        return
    parent = parent_map.get(old_metadata)
    if parent is None:
        return
    index = list(parent).index(old_metadata)
    parent.remove(old_metadata)
    parent.insert(index, new_metadata)


def _containing_scene(root: ET.Element, group: ET.Element) -> ET.Element | None:
    scene = _find_element_by_id(root, "scene")
    if scene is not None and _is_svg_group(scene) and group in scene.iter():
        return scene
    return None


def _refresh_scene_transform(
    existing_root: ET.Element,
    new_root: ET.Element,
    old_group: ET.Element,
    new_group: ET.Element,
) -> ET.Element:
    """Refresh the generated transform; preserve user attributes and siblings."""
    old_scene = _containing_scene(existing_root, old_group)
    new_scene = _containing_scene(new_root, new_group)
    if old_scene is not None:
        old_scene.attrib.pop("transform", None)
        if new_scene is not None and "transform" in new_scene.attrib:
            old_scene.set("transform", new_scene.attrib["transform"])
    elif new_scene is not None:
        # Legacy files may have the durable group directly under the SVG root.
        # Wrap only its replacement so page-space annotations stay outside.
        wrapper = ET.Element(new_scene.tag, dict(new_scene.attrib))
        wrapper.append(new_group)
        return wrapper
    return new_group


def _replace_group_in_svg(existing_svg: str, new_svg: str, group_id: str) -> str:
    ET.register_namespace("", _SVG_NS)
    existing_root = ET.fromstring(existing_svg)
    new_root = ET.fromstring(new_svg)
    new_group = _find_element_by_id(new_root, group_id)
    if new_group is None:
        raise ValueError(
            f"Generated SVG does not contain expected group id {group_id!r}"
        )
    old_group = _find_element_by_id(existing_root, group_id)
    if old_group is None:
        raise ValueError(f"Existing SVG does not contain durable group {group_id!r}")
    else:
        existing_root.attrib.clear()
        existing_root.attrib.update(new_root.attrib)
        _replace_generated_metadata(existing_root, new_root)
        _remove_legacy_generated_view_artifacts(existing_root, group_id)
        parent_map = {
            child: parent for parent in existing_root.iter() for child in parent
        }
        parent = parent_map.get(old_group)
        if parent is None:
            raise ValueError(f"Existing SVG group {group_id!r} has no parent")
        replacement = _refresh_scene_transform(
            existing_root, new_root, old_group, new_group
        )
        index = list(parent).index(old_group)
        parent.remove(old_group)
        parent.insert(index, replacement)
    return ET.tostring(existing_root, encoding="unicode")


def write_or_update_view_svg(path: Path, svg_text: str, *, group_id: str) -> None:
    """Write a new SVG or replace an existing durable view group."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        try:
            updated = _replace_group_in_svg(
                path.read_text(encoding="utf-8"), svg_text, group_id
            )
            path.write_text(updated, encoding="utf-8")
            return
        except Exception as exc:
            log.warning(
                "Replacing whole SVG after group update failed for %s: %s", path, exc
            )
    path.write_text(svg_text, encoding="utf-8")
