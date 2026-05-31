"""Known fixture-part cache support for debug-plate workflows."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from altium_cruncher.altium_cruncher_mco import JsonObject, load_jsonc_file

DEBUG_PLATE_PARTS_CACHE_SCHEMA = "wn.altium_cruncher.debug_plate.parts_cache.v1"
DEBUG_PLATE_PARTS_CACHE_FILENAME = "debug-plate-known-parts.json"


@dataclass(frozen=True, slots=True)
class DebugPlateKnownPartTemplate:
    """One debug-plate fixture part expected in a generated cache."""

    role: str
    description: str
    symbol_name: str
    footprint_name: str
    symbol_library: str
    footprint_library: str
    target_kinds: tuple[str, ...]
    designator_prefix: str
    signal_pad_designator: str | None = None


NODE_TEST_ARRAY_PART_TEMPLATES: tuple[DebugPlateKnownPartTemplate, ...] = (
    DebugPlateKnownPartTemplate(
        role="test_point_pogo",
        description="Pogo fixture contact aligned to cricket-node 2 mm test pads.",
        symbol_name="YZ209315103P-01",
        footprint_name="YZ209315103P-01",
        symbol_library="schlib/YZ209315103P-01.SchLib",
        footprint_library="pcblib/split/YZ209315103P-01.PcbLib",
        target_kinds=("test_point",),
        designator_prefix="TP",
        signal_pad_designator="1",
    ),
    DebugPlateKnownPartTemplate(
        role="m25_smt_standoff",
        description=(
            "M2.5 SMT standoff aligned to cricket-node M1-M4 mounting features."
        ),
        symbol_name="9774080360R",
        footprint_name="9774080360R-YIYUAN",
        symbol_library="schlib/9774080360R.SchLib",
        footprint_library="pcblib/split/9774080360R-YIYUAN.PcbLib",
        target_kinds=("mount",),
        designator_prefix="M",
    ),
    DebugPlateKnownPartTemplate(
        role="alignment_pin_2mm_npth",
        description="2 mm alignment pin associated with cricket-node free NPTH holes.",
        symbol_name="H2184-05",
        footprint_name="H2184-05",
        symbol_library="schlib/H2184-05.SchLib",
        footprint_library="pcblib/split/H2184-05.PcbLib",
        target_kinds=("free_npth",),
        designator_prefix="P",
        signal_pad_designator="1",
    ),
)


def build_debug_plate_known_parts_cache(
    source_project: Path | str,
    cache_dir: Path | str,
    *,
    overwrite: bool = False,
    verbose: bool = False,
) -> Path:
    """Extract node-test-array libraries and write a debug-plate parts manifest."""
    source_path = Path(source_project).resolve()
    output_dir = Path(cache_dir).resolve()
    manifest_path = output_dir / DEBUG_PLATE_PARTS_CACHE_FILENAME
    if manifest_path.exists() and not overwrite:
        raise FileExistsError(f"Debug-plate known-parts cache already exists: {manifest_path}")

    _extract_project_assets(source_path, output_dir, verbose=verbose)
    payload = build_node_test_array_parts_manifest(source_path, output_dir)
    write_debug_plate_known_parts_manifest(payload, manifest_path)
    return manifest_path


def build_node_test_array_parts_manifest(
    source_project: Path | str,
    cache_dir: Path | str,
) -> JsonObject:
    """Build the manifest for node-test-array derived debug-plate fixture parts."""
    source_path = Path(source_project).resolve()
    output_dir = Path(cache_dir).resolve()
    _validate_part_template_outputs(output_dir, NODE_TEST_ARRAY_PART_TEMPLATES)
    return {
        "schema": DEBUG_PLATE_PARTS_CACHE_SCHEMA,
        "source": {
            "kind": "node_test_array",
            "project": str(source_path),
        },
        "parts": [
            _part_template_payload(template)
            for template in NODE_TEST_ARRAY_PART_TEMPLATES
        ],
        "designator_normalization": {
            "mount": {
                "M5": "M1",
                "M6": "M2",
                "M7": "M3",
                "M8": "M4",
            }
        },
    }


def write_debug_plate_known_parts_manifest(
    payload: Mapping[str, object],
    path: Path | str,
) -> Path:
    """Write a debug-plate known-parts cache manifest."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_path.resolve()


def load_debug_plate_known_parts_manifest(path: Path | str) -> JsonObject:
    """Load and validate a debug-plate known-parts manifest."""
    payload = load_jsonc_file(path)
    root = _json_object(payload, "debug-plate known-parts manifest")
    schema = root.get("schema")
    if schema != DEBUG_PLATE_PARTS_CACHE_SCHEMA:
        raise ValueError(f"Unsupported debug-plate parts-cache schema: {schema!r}")
    parts = root.get("parts")
    if not isinstance(parts, list):
        raise ValueError("Debug-plate parts-cache manifest must contain a parts array")
    return root


def resolve_known_part(
    manifest: Mapping[str, object],
    target_kind: str,
    *,
    role: str | None = None,
) -> JsonObject:
    """Return the first known-part manifest entry matching a target kind."""
    parts = _known_part_entries(manifest)
    if role:
        return _resolve_known_part_by_role(parts, target_kind, role)
    return _resolve_known_part_by_kind(parts, target_kind)


def _known_part_entries(manifest: Mapping[str, object]) -> list[JsonObject]:
    parts = manifest.get("parts")
    if not isinstance(parts, list):
        raise ValueError("Debug-plate parts-cache manifest must contain a parts array")
    return [_json_object(part, "debug-plate known part") for part in parts]


def _resolve_known_part_by_kind(
    parts: list[JsonObject],
    target_kind: str,
) -> JsonObject:
    for part in parts:
        if _known_part_targets_kind(part, target_kind):
            return part
    raise ValueError(f"No debug-plate known part matches target kind: {target_kind}")


def _resolve_known_part_by_role(
    parts: list[JsonObject],
    target_kind: str,
    role: str,
) -> JsonObject:
    role_matches = [
        part
        for part in parts
        if str(part.get("role", "") or "") == role
    ]
    if not role_matches:
        raise ValueError(f"No debug-plate known part matches role: {role}")
    for part in role_matches:
        if _known_part_targets_kind(part, target_kind):
            return part
    raise ValueError(
        f"Debug-plate known part role {role!r} does not target kind: {target_kind}"
    )


def _known_part_targets_kind(
    part: Mapping[str, object],
    target_kind: str,
) -> bool:
    target_kinds = part.get("target_kinds", [])
    if not isinstance(target_kinds, list):
        return False
    normalized_kind = target_kind.strip().lower()
    return normalized_kind in {
        str(item).strip().lower()
        for item in target_kinds
        if isinstance(item, str)
    }


def manifest_path_for_cache_dir(cache_dir: Path | str) -> Path:
    """Return the default manifest path inside a known-parts cache directory."""
    path = Path(cache_dir)
    if path.suffix.lower() == ".json":
        return path
    return path / DEBUG_PLATE_PARTS_CACHE_FILENAME


def _extract_project_assets(
    source_project: Path,
    output_dir: Path,
    *,
    verbose: bool,
) -> None:
    if source_project.suffix.lower() != ".prjpcb":
        raise ValueError("Debug-plate known-parts cache builds require a .PrjPcb input")

    from altium_cruncher.altium_cruncher_cmd_extract import (
        _extract_pcbdocs_to_output,
        _extract_schdocs_to_output,
    )
    from altium_monkey.altium_prjpcb import AltiumPrjPcb

    project = AltiumPrjPcb(source_project)
    schdoc_files = project.get_schdoc_paths()
    pcbdoc_files = project.get_pcbdoc_paths()
    if not schdoc_files:
        raise ValueError(f"No SchDoc files found in project: {source_project}")
    if not pcbdoc_files:
        raise ValueError(f"No PcbDoc files found in project: {source_project}")

    sch_output_dir = output_dir / "schlib"
    pcb_output_dir = output_dir / "pcblib"
    sch_output_dir.mkdir(parents=True, exist_ok=True)
    pcb_output_dir.mkdir(parents=True, exist_ok=True)

    successful, failed, _ = _extract_schdocs_to_output(
        schdoc_files,
        sch_output_dir,
        split=True,
        combined=True,
        debug=verbose,
    )
    if failed or not successful:
        raise RuntimeError(f"SchLib extraction failed for {failed} symbol(s)")

    successful, failed = _extract_pcbdocs_to_output(
        pcbdoc_files,
        pcb_output_dir,
        split=True,
        combined=True,
        verbose=verbose,
    )
    if failed or not successful:
        raise RuntimeError(f"PcbLib extraction failed for {failed} board(s)")


def _part_template_payload(template: DebugPlateKnownPartTemplate) -> JsonObject:
    return {
        "role": template.role,
        "description": template.description,
        "symbol_name": template.symbol_name,
        "symbol_library": template.symbol_library,
        "footprint_name": template.footprint_name,
        "footprint_library": template.footprint_library,
        "target_kinds": list(template.target_kinds),
        "designator_prefix": template.designator_prefix,
        "signal_pad_designator": template.signal_pad_designator,
    }


def _validate_part_template_outputs(
    output_dir: Path,
    templates: Sequence[DebugPlateKnownPartTemplate],
) -> None:
    missing: list[Path] = []
    for template in templates:
        for relative_path in (template.symbol_library, template.footprint_library):
            candidate = output_dir / relative_path
            if not candidate.exists():
                missing.append(candidate)
    if missing:
        missing_text = ", ".join(str(path) for path in missing)
        raise FileNotFoundError(f"Missing extracted debug-plate known-part files: {missing_text}")


def _json_object(value: object, label: str) -> JsonObject:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return dict(value)
