"""JSON dump helpers for parsed Altium documents."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
from pathlib import Path

from altium_cruncher.altium_cruncher_common import (
    _resolve_output_dir,
    find_prjpcbs_in_cwd,
)

JSON_DUMP_SCHEMA = "altium_cruncher.json_dump.a0"
JSON_DUMP_MANIFEST_SCHEMA = "altium_cruncher.json_dump.manifest.a0"

_SUPPORTED_SUFFIX_TO_KIND = {
    ".schdoc": "SchDoc",
    ".schlib": "SchLib",
    ".pcbdoc": "PcbDoc",
    ".pcblib": "PcbLib",
}

_PCB_DOC_COLLECTIONS = (
    "components",
    "nets",
    "net_classes",
    "differential_pairs",
    "polygons",
    "rules",
    "dimensions",
    "extended_primitive_information",
    "custom_shapes",
    "via_structures",
    "via_structure_links",
    "pads",
    "vias",
    "tracks",
    "arcs",
    "texts",
    "fills",
    "regions",
    "board_regions",
    "shapebased_regions",
    "component_bodies",
    "shapebased_component_bodies",
    "models",
    "embedded_fonts",
    "embedded_models",
)

_PCB_FOOTPRINT_COLLECTIONS = (
    "pads",
    "vias",
    "tracks",
    "arcs",
    "texts",
    "fills",
    "regions",
    "shapebased_regions",
    "component_bodies",
    "models",
)

_NOT_JSONABLE = object()


@dataclass(frozen=True, slots=True)
class JsonDumpOutput:
    """One written json-dump document."""

    source_path: Path
    output_path: Path
    kind: str

    def to_dict(self) -> dict[str, object]:
        return {
            "source_path": self.source_path.as_posix(),
            "output_path": self.output_path.as_posix(),
            "kind": self.kind,
        }


@dataclass(frozen=True, slots=True)
class JsonDumpResult:
    """Result of writing one json-dump batch."""

    output_dir: Path
    manifest_path: Path
    outputs: tuple[JsonDumpOutput, ...]

    def to_manifest(self) -> dict[str, object]:
        return {
            "schema": JSON_DUMP_MANIFEST_SCHEMA,
            "outputs": [output.to_dict() for output in self.outputs],
        }


def build_json_dump_payload(path: Path | str) -> dict[str, object]:
    """Build a JSON dump payload for one supported Altium document."""
    source_path = Path(path).resolve()
    kind = _document_kind(source_path)
    document = _load_document_payload(source_path, kind)
    return {
        "schema": JSON_DUMP_SCHEMA,
        "kind": kind,
        "document": document,
    }


def resolve_json_dump_sources(
    inputs: list[Path],
    *,
    recursive: bool = False,
) -> list[Path]:
    """Resolve CLI inputs into supported document paths in deterministic order."""
    if not inputs:
        project_files = find_prjpcbs_in_cwd()
        if len(project_files) == 1:
            return _deduplicate_paths(_project_document_paths(project_files[0]))
        return _supported_files_in_directory(Path.cwd(), recursive=False)

    resolved: list[Path] = []
    for raw_input in inputs:
        input_path = Path(raw_input).resolve()
        if not input_path.exists():
            raise FileNotFoundError(f"Input path not found: {input_path}")
        if input_path.is_dir():
            resolved.extend(_supported_files_in_directory(input_path, recursive))
            continue
        if input_path.suffix.lower() == ".prjpcb":
            resolved.extend(_project_document_paths(input_path))
            continue
        if _is_supported_document(input_path):
            resolved.append(input_path)
            continue
        raise ValueError(f"Unsupported json-dump input type: {input_path.suffix}")
    return _deduplicate_paths(resolved)


def write_json_dumps(
    inputs: list[Path],
    *,
    output: Path | None = None,
    recursive: bool = False,
) -> JsonDumpResult:
    """Write JSON dump files and a manifest for the resolved input set."""
    sources = resolve_json_dump_sources(inputs, recursive=recursive)
    if not sources:
        raise ValueError("No supported Altium documents found for json-dump")

    output_dir = _resolve_output_dir(output, "json-dump")
    used_names: set[str] = set()
    outputs: list[JsonDumpOutput] = []
    for source in sources:
        payload = build_json_dump_payload(source)
        output_path = _output_path_for_source(source, output_dir, used_names)
        _write_json(output_path, payload)
        outputs.append(
            JsonDumpOutput(
                source_path=source,
                output_path=output_path,
                kind=str(payload["kind"]),
            )
        )

    result = JsonDumpResult(
        output_dir=output_dir,
        manifest_path=output_dir / "manifest.json",
        outputs=tuple(outputs),
    )
    _write_json(result.manifest_path, result.to_manifest())
    return result


def build_single_json_dump_payload(
    inputs: list[Path],
    *,
    recursive: bool = False,
) -> dict[str, object]:
    """Resolve one input and return its JSON dump payload for stdout mode."""
    sources = resolve_json_dump_sources(inputs, recursive=recursive)
    if len(sources) != 1:
        raise ValueError(
            f"--stdout requires exactly one resolved document; found {len(sources)}"
        )
    return build_json_dump_payload(sources[0])


def _load_document_payload(
    source_path: Path,
    kind: str,
) -> dict[str, object]:
    if kind == "SchDoc":
        from altium_monkey.altium_schdoc import AltiumSchDoc

        return AltiumSchDoc(source_path).to_json()
    if kind == "SchLib":
        from altium_monkey.altium_schlib import AltiumSchLib

        return AltiumSchLib(source_path).to_json()
    if kind == "PcbDoc":
        from altium_monkey.altium_pcbdoc import AltiumPcbDoc

        return _pcbdoc_to_json(AltiumPcbDoc.from_file(source_path))
    if kind == "PcbLib":
        from altium_monkey.altium_pcblib import AltiumPcbLib

        return _pcblib_to_json(AltiumPcbLib.from_file(source_path))
    raise ValueError(f"Unsupported json-dump document kind: {kind}")


def _pcbdoc_to_json(pcbdoc: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "format": "altium_cruncher.pcbdoc.structural.v1",
        "counts": _collection_counts(pcbdoc, _PCB_DOC_COLLECTIONS),
        "raw_streams": _raw_stream_inventory(getattr(pcbdoc, "_raw_streams", {})),
        "board": _jsonable(getattr(pcbdoc, "board", None), set()),
        "union_name_records": _jsonable(
            getattr(pcbdoc, "union_name_records", ()),
            set(),
        ),
        "smart_unions": _jsonable(getattr(pcbdoc, "smart_unions", ()), set()),
        "user_unions": _pcb_user_unions_to_json(pcbdoc),
    }
    for collection in _PCB_DOC_COLLECTIONS:
        payload[collection] = _jsonable(getattr(pcbdoc, collection, ()), set())
    return payload


def _pcblib_to_json(pcblib: object) -> dict[str, object]:
    footprints = []
    for footprint in getattr(pcblib, "footprints", ()):
        entry: dict[str, object] = {
            "name": str(getattr(footprint, "name", "")),
            "counts": _collection_counts(footprint, _PCB_FOOTPRINT_COLLECTIONS),
        }
        for collection in _PCB_FOOTPRINT_COLLECTIONS:
            entry[collection] = _jsonable(getattr(footprint, collection, ()), set())
        footprints.append(entry)
    return {
        "format": "altium_cruncher.pcblib.structural.v1",
        "footprint_count": len(footprints),
        "footprints": footprints,
        "models_3d": _jsonable(getattr(pcblib, "models_3d", {}), set()),
        "raw_streams": _raw_stream_inventory(getattr(pcblib, "_raw_streams", {})),
    }


def _pcb_user_unions_to_json(pcbdoc: object) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    try:
        user_unions = getattr(pcbdoc, "user_unions")
    except Exception as exc:
        return [{"error": str(exc)}]
    for user_union in user_unions:
        members = []
        for member in getattr(user_union, "members", ()):
            member_obj = getattr(member, "obj", None)
            members.append(
                {
                    "collection": str(getattr(member, "collection", "")),
                    "object_index": int(getattr(member, "object_index", -1)),
                    "union_index": int(getattr(member, "union_index", 0)),
                    "object_summary": _pcb_member_summary(member_obj),
                }
            )
        result.append(
            {
                "union_index": int(getattr(user_union, "union_index", 0)),
                "name": str(getattr(user_union, "name", "")),
                "member_count": int(getattr(user_union, "member_count", len(members))),
                "members": members,
            }
        )
    return result


def _pcb_member_summary(member_obj: object | None) -> dict[str, object]:
    if member_obj is None:
        return {}
    summary: dict[str, object] = {"class": type(member_obj).__name__}
    for name in ("designator", "name", "text_content", "footprint", "comment"):
        value = getattr(member_obj, name, None)
        if value is not None and value != "":
            summary[name] = _jsonable(value, set())
    for name in (
        "x_mils",
        "y_mils",
        "start_x_mils",
        "start_y_mils",
        "end_x_mils",
        "end_y_mils",
        "center_x_mils",
        "center_y_mils",
    ):
        try:
            value = getattr(member_obj, name)
        except Exception:
            continue
        if value is not None:
            summary[name] = _jsonable(value, set())
    return summary


def _jsonable(value: object, seen: set[int], *, depth: int = 0) -> object:
    simple_value = _simple_jsonable(value)
    if simple_value is not _NOT_JSONABLE:
        return simple_value
    if isinstance(value, Mapping):
        return {
            str(key): _jsonable(item, seen, depth=depth + 1)
            for key, item in value.items()
        }
    if isinstance(value, list | tuple | set | frozenset):
        return [_jsonable(item, seen, depth=depth + 1) for item in value]
    if depth > 10:
        return repr(value)

    return _complex_jsonable(value, seen, depth=depth)


def _simple_jsonable(value: object) -> object:
    if value is None or isinstance(value, str | int | float | bool):
        return value
    if isinstance(value, bytes | bytearray):
        return _bytes_summary(bytes(value))
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, Enum):
        return {"name": value.name, "value": value.value}
    return _NOT_JSONABLE


def _complex_jsonable(value: object, seen: set[int], *, depth: int) -> object:
    value_id = id(value)
    if value_id in seen:
        return {"ref": type(value).__name__}
    seen.add(value_id)
    try:
        if is_dataclass(value) and not isinstance(value, type):
            return _dataclass_to_jsonable(value, seen, depth=depth)
        if hasattr(value, "__dict__"):
            return _object_to_jsonable(value, seen, depth=depth)
        return repr(value)
    finally:
        seen.discard(value_id)


def _dataclass_to_jsonable(
    value: object,
    seen: set[int],
    *,
    depth: int,
) -> dict[str, object]:
    result: dict[str, object] = {"class": type(value).__name__}
    for field in fields(value):
        if field.name.startswith("_"):
            continue
        result[field.name] = _jsonable(getattr(value, field.name), seen, depth=depth + 1)
    properties = _public_properties(value, seen, depth=depth)
    if properties:
        result["properties"] = properties
    return result


def _object_to_jsonable(
    value: object,
    seen: set[int],
    *,
    depth: int,
) -> dict[str, object]:
    fields_payload: dict[str, object] = {}
    for name, item in vars(value).items():
        if name.startswith("_"):
            continue
        fields_payload[name] = _jsonable(item, seen, depth=depth + 1)
    result: dict[str, object] = {
        "class": type(value).__name__,
        "fields": fields_payload,
    }
    properties = _public_properties(value, seen, depth=depth)
    if properties:
        result["properties"] = properties
    return result


def _public_properties(
    value: object,
    seen: set[int],
    *,
    depth: int,
) -> dict[str, object]:
    result: dict[str, object] = {}
    for cls in reversed(type(value).mro()):
        for name, descriptor in cls.__dict__.items():
            if name.startswith("_") or not isinstance(descriptor, property):
                continue
            try:
                property_value = getattr(value, name)
            except Exception as exc:
                result[name] = {"error": str(exc)}
                continue
            result[name] = _jsonable(property_value, seen, depth=depth + 1)
    return result


def _collection_counts(value: object, collection_names: tuple[str, ...]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for name in collection_names:
        collection = getattr(value, name, ())
        try:
            counts[name] = len(collection)
        except TypeError:
            counts[name] = 0
    return counts


def _raw_stream_inventory(raw_streams: object) -> list[dict[str, object]]:
    if not isinstance(raw_streams, Mapping):
        return []
    entries = []
    for name, data in sorted(raw_streams.items(), key=lambda item: str(item[0])):
        if not isinstance(data, bytes | bytearray):
            continue
        entries.append(
            {
                "name": str(name),
                "byte_count": len(data),
                "sha256": hashlib.sha256(bytes(data)).hexdigest(),
            }
        )
    return entries


def _bytes_summary(data: bytes) -> dict[str, object]:
    return {
        "byte_count": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def _document_kind(path: Path) -> str:
    try:
        return _SUPPORTED_SUFFIX_TO_KIND[path.suffix.lower()]
    except KeyError as exc:
        raise ValueError(f"Unsupported json-dump document type: {path.suffix}") from exc


def _is_supported_document(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in _SUPPORTED_SUFFIX_TO_KIND


def _supported_files_in_directory(path: Path, recursive: bool) -> list[Path]:
    pattern = "**/*" if recursive else "*"
    return sorted(
        [
            candidate.resolve()
            for candidate in path.glob(pattern)
            if _is_supported_document(candidate)
        ],
        key=lambda candidate: candidate.as_posix().lower(),
    )


def _project_document_paths(project_path: Path) -> list[Path]:
    from altium_monkey.altium_prjpcb import AltiumPrjPcb

    project = AltiumPrjPcb(project_path)
    project_dir = project_path.resolve().parent
    documents: list[Path] = []
    for document in project.documents:
        raw_document_path = str(document.get("path", "") or "")
        document_path = Path(raw_document_path.replace("\\", "/"))
        if document_path.suffix.lower() not in _SUPPORTED_SUFFIX_TO_KIND:
            continue
        resolved = (project_dir / document_path).resolve()
        if resolved.exists():
            documents.append(resolved)
    return documents


def _deduplicate_paths(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    result: list[Path] = []
    for path in paths:
        key = path.resolve().as_posix().lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(path.resolve())
    return result


def _output_path_for_source(
    source: Path,
    output_dir: Path,
    used_names: set[str],
) -> Path:
    name = f"{source.name}.json"
    key = name.lower()
    if key in used_names:
        digest = hashlib.sha1(source.resolve().as_posix().encode("utf-8")).hexdigest()
        name = f"{source.stem}__{digest[:8]}{source.suffix}.json"
        key = name.lower()
    used_names.add(key)
    return output_dir / name


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
