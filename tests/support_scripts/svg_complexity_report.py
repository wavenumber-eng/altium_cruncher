"""Report deterministic structural metrics for generated SVG files.

This is a measurement tool for renderer performance work. It deliberately uses
streaming XML parsing so a large review SVG does not need to remain in memory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


PATH_COMMAND = re.compile(r"[MmLlHhVvCcSsQqTtAaZz]")
HREF = "{http://www.w3.org/1999/xlink}href"


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def inspect_svg(path: Path) -> dict[str, object]:
    """Return byte, hash, element, definition, instance, and path metrics."""
    digest = hashlib.sha256()
    byte_count = 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
            byte_count += len(chunk)

    tags: Counter[str] = Counter()
    illustration_defs: Counter[str] = Counter()
    uses: Counter[str] = Counter()
    path_metrics = [0, 0]
    for _event, element in ET.iterparse(path, events=("end",)):
        tag = _local_name(element.tag)
        tags[tag] += 1
        _count_definition(element, illustration_defs)
        _count_instance_or_path(element, tag, uses, path_metrics)
        element.clear()

    return {
        "path": str(path.resolve()),
        "bytes": byte_count,
        "sha256": digest.hexdigest().upper(),
        "elements": sum(tags.values()),
        "tags": dict(sorted(tags.items())),
        "illustration_definitions": dict(sorted(illustration_defs.items())),
        "instances": dict(sorted(uses.items())),
        "path_commands": path_metrics[0],
        "path_data_bytes": path_metrics[1],
    }


def _count_definition(element: ET.Element, counts: Counter[str]) -> None:
    element_id = element.get("id", "")
    if "-aperture-symbol-" in element_id:
        counts["aperture"] += 1
    elif "illustration_" in element_id and "-symbol-" in element_id:
        counts["surface"] += 1


def _count_instance_or_path(
    element: ET.Element,
    tag: str,
    uses: Counter[str],
    path_metrics: list[int],
) -> None:
    if tag == "use":
        _count_use(element, uses)
    elif tag == "path":
        data = element.get("d", "")
        path_metrics[0] += len(PATH_COMMAND.findall(data))
        path_metrics[1] += len(data.encode("utf-8"))


def _count_use(element: ET.Element, uses: Counter[str]) -> None:
    href = element.get("href") or element.get(HREF) or ""
    if "aperture" in href:
        uses["aperture"] += 1
    elif "illustration" in href:
        uses["surface"] += 1
    else:
        uses["other"] += 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg", nargs="+", type=Path)
    args = parser.parse_args()
    report = [inspect_svg(path) for path in args.svg]
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
