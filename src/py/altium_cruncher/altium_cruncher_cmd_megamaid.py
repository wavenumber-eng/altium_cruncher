"""Megamaid project decomposition command for altium_cruncher."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import logging
from pathlib import Path, PureWindowsPath
import re
import shutil
import zlib

from altium_cruncher.altium_cruncher_common import (
    _resolve_output_dir,
    find_prjpcb_in_cwd,
)

log = logging.getLogger(__name__)


def _relative_to_root(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except Exception:
        return str(path)


def _prepare_megamaid_output_root(output_dir: Path) -> None:
    """Clear megamaid-owned outputs so regenerated trees do not retain stale artifacts."""
    owned_dirs = [
        output_dir / "schlib",
        output_dir / "pcblib",
        output_dir / "bom",
        output_dir / "netlist",
        output_dir / "embedded_models",
        output_dir / "embedded_fonts",
        output_dir / "sch_images",
    ]
    owned_files = [
        output_dir / "megamaid_manifest.json",
    ]
    for directory in owned_dirs:
        if directory.exists():
            shutil.rmtree(directory)
    for file_path in owned_files:
        if file_path.exists():
            file_path.unlink()
    output_dir.mkdir(parents=True, exist_ok=True)


def _write_bom_csv(bom: list[dict], output_file: Path) -> None:
    """Write BOM rows to CSV using the standard cruncher column contract."""
    all_params = set()
    for comp in bom:
        all_params.update(comp.get("parameters", {}).keys())
    param_columns = sorted(all_params)
    fixed_columns = [
        "Designator",
        "Value",
        "Footprint",
        "Library Ref",
        "Description",
        "Sheet",
        "DNP",
    ]

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle)
        writer.writerow(fixed_columns + param_columns)
        for comp in sorted(bom, key=lambda c: c.get("designator", "")):
            row = [
                comp.get("designator", ""),
                comp.get("value", ""),
                comp.get("footprint", ""),
                comp.get("library_ref", ""),
                comp.get("description", ""),
                comp.get("sheet", ""),
                "Yes" if comp.get("dnp") else "No",
            ]
            params = comp.get("parameters", {})
            for param_name in param_columns:
                row.append(params.get(param_name, ""))
            writer.writerow(row)


def _sanitize_asset_name(name: str, fallback: str) -> str:
    """Sanitize embedded asset names for filesystem output."""
    text = str(name or "").replace("\x00", "").strip()
    if not text:
        text = fallback
    text = re.sub(r'[<>:"/\\|?*]+', "_", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text or fallback


def _choose_asset_output_path(
    *,
    output_dir: Path,
    desired_name: str,
    payload: bytes,
    registry: dict[str, list[dict[str, object]]],
    used_names: set[str],
) -> tuple[Path | None, bool]:
    """
    Choose a flattened output path for an embedded asset.

    Returns:
        (path, created)
        - path is None when an identical existing asset should be deduplicated
        - created indicates whether a new file should be written
    """
    key = desired_name.lower()
    payload_hash = hashlib.sha256(payload).hexdigest()
    entries = registry.setdefault(key, [])
    for entry in entries:
        if entry["hash"] == payload_hash:
            return None, False

    candidate_name = desired_name
    if candidate_name.lower() in used_names:
        stem = Path(desired_name).stem
        suffix = Path(desired_name).suffix
        index = 1
        while True:
            candidate_name = f"{stem}__{index:02d}{suffix}"
            if candidate_name.lower() not in used_names:
                break
            index += 1

    used_names.add(candidate_name.lower())
    output_path = output_dir / candidate_name
    entries.append({"hash": payload_hash, "path": output_path})
    return output_path, True


def _extract_project_embedded_assets(
    *,
    pcbdoc_paths: list[Path],
    output_root: Path,
    debug: bool,
) -> dict[str, list[dict[str, object]]]:
    """Flatten embedded font/model extraction across all boards in the project."""
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc

    fonts_root = output_root / "embedded_fonts"
    models_root = output_root / "embedded_models"
    fonts_root.mkdir(parents=True, exist_ok=True)
    models_root.mkdir(parents=True, exist_ok=True)

    font_registry: dict[str, list[dict[str, object]]] = {}
    model_registry: dict[str, list[dict[str, object]]] = {}
    used_font_names: set[str] = set()
    used_model_names: set[str] = set()

    font_entries: list[dict[str, object]] = []
    model_entries: list[dict[str, object]] = []

    for pcbdoc_path in pcbdoc_paths:
        pcbdoc = AltiumPcbDoc.from_file(pcbdoc_path)

        for font in pcbdoc.embedded_fonts:
            payload = font.decompress()
            if not payload:
                continue
            desired_name = _sanitize_asset_name(font.filename, "EmbeddedFont.ttf")
            output_path, created = _choose_asset_output_path(
                output_dir=fonts_root,
                desired_name=desired_name,
                payload=payload,
                registry=font_registry,
                used_names=used_font_names,
            )
            record = {
                "source_pcbdoc": str(pcbdoc_path),
                "source_name": desired_name,
            }
            if output_path is None:
                existing_path = next(
                    Path(entry["path"])
                    for entry in font_registry[desired_name.lower()]
                    if entry["hash"] == hashlib.sha256(payload).hexdigest()
                )
                record["output_file"] = str(existing_path)
                record["deduplicated"] = True
                if debug:
                    log.info("Deduplicated embedded font: %s", desired_name)
            else:
                output_path.write_bytes(payload)
                record["output_file"] = str(output_path)
                record["deduplicated"] = False
                if created and debug:
                    log.info("Extracted embedded font: %s", output_path.name)
            font_entries.append(record)

        for model, compressed_payload in pcbdoc.get_embedded_model_entries():
            try:
                payload = zlib.decompress(compressed_payload)
            except Exception:
                payload = b""
            if not payload:
                continue
            desired_name = _sanitize_asset_name(
                str(getattr(model, "name", "") or ""),
                f"model_{len(model_entries):03d}.bin",
            )
            output_path, created = _choose_asset_output_path(
                output_dir=models_root,
                desired_name=desired_name,
                payload=payload,
                registry=model_registry,
                used_names=used_model_names,
            )
            record = {
                "source_pcbdoc": str(pcbdoc_path),
                "source_name": desired_name,
            }
            if output_path is None:
                existing_path = next(
                    Path(entry["path"])
                    for entry in model_registry[desired_name.lower()]
                    if entry["hash"] == hashlib.sha256(payload).hexdigest()
                )
                record["output_file"] = str(existing_path)
                record["deduplicated"] = True
                if debug:
                    log.info("Deduplicated embedded model: %s", desired_name)
            else:
                output_path.write_bytes(payload)
                record["output_file"] = str(output_path)
                record["deduplicated"] = False
                if created and debug:
                    log.info("Extracted embedded model: %s", output_path.name)
            model_entries.append(record)

    return {
        "fonts": font_entries,
        "models": model_entries,
    }


def _extract_project_schematic_images(
    *,
    schdoc_paths: list[Path],
    output_root: Path,
    debug: bool,
) -> list[dict[str, object]]:
    """Flatten schematic IMAGE record payload extraction across all schdocs in the project."""
    from altium_monkey.altium_schdoc import AltiumSchDoc

    images_root = output_root / "sch_images"
    images_root.mkdir(parents=True, exist_ok=True)

    image_registry: dict[str, list[dict[str, object]]] = {}
    used_names: set[str] = set()
    image_entries: list[dict[str, object]] = []
    seq = 0

    for schdoc_path in schdoc_paths:
        schdoc = AltiumSchDoc(schdoc_path)
        for image in schdoc.images:
            payload = image.image_data
            if not payload:
                continue
            seq += 1
            # Strip Windows path components from the IMAGE record filename,
            # use stem for output name, detect extension from payload bytes.
            source_name = PureWindowsPath(str(image.filename or "")).name
            stem = Path(source_name).stem if source_name else f"image_{seq:03d}"
            stem = _sanitize_asset_name(stem, f"image_{seq:03d}")
            output_data, extension = AltiumSchDoc._embedded_image_payload_for_output(
                payload
            )
            if extension is None and source_name:
                original_ext = Path(source_name).suffix.lower()
                if original_ext in {
                    ".bmp",
                    ".gif",
                    ".jpg",
                    ".jpeg",
                    ".png",
                    ".svg",
                    ".webp",
                }:
                    extension = ".jpg" if original_ext == ".jpeg" else original_ext
            extension = extension or ".bin"
            desired_name = f"{stem}{extension}"

            output_path, created = _choose_asset_output_path(
                output_dir=images_root,
                desired_name=desired_name,
                payload=output_data,
                registry=image_registry,
                used_names=used_names,
            )
            record: dict[str, object] = {
                "source_schdoc": str(schdoc_path),
                "source_name": str(image.filename or ""),
            }
            if output_path is None:
                existing_path = next(
                    Path(entry["path"])
                    for entry in image_registry[desired_name.lower()]
                    if entry["hash"] == hashlib.sha256(output_data).hexdigest()
                )
                record["output_file"] = str(existing_path)
                record["deduplicated"] = True
                if debug:
                    log.info("Deduplicated embedded sch image: %s", desired_name)
            else:
                output_path.write_bytes(output_data)
                record["output_file"] = str(output_path)
                record["deduplicated"] = False
                if created and debug:
                    log.info("Extracted embedded sch image: %s", output_path.name)
            image_entries.append(record)

    return image_entries


def _extract_schlibs_for_project(
    *,
    schdoc_paths: list[Path],
    output_root: Path,
    debug: bool,
) -> list[dict]:
    from altium_monkey.altium_schdoc import AltiumSchDoc
    from altium_monkey.altium_schlib import AltiumSchLib
    from altium_monkey.altium_schlib_merger import merge_directory

    combined_root = output_root / "combined"
    split_root = output_root / "split"
    combined_root.mkdir(parents=True, exist_ok=True)
    split_root.mkdir(parents=True, exist_ok=True)

    manifest_entries: list[dict] = []
    multi_schematic = len(schdoc_paths) > 1
    for schdoc_path in schdoc_paths:
        schdoc = AltiumSchDoc(schdoc_path)
        split_dir = split_root / schdoc_path.stem if multi_schematic else split_root
        split_dir.mkdir(parents=True, exist_ok=True)
        results = schdoc.extract_symbols(
            output_dir=split_dir,
            combined_schlib=False,
            split_schlibs=True,
            debug=debug,
        )
        successful = sum(1 for ok in results.values() if ok)

        combined_path = combined_root / f"{schdoc_path.stem}.SchLib"
        if successful == 0:
            AltiumSchLib().save(combined_path, sync_pin_text_data=True)
        else:
            success = merge_directory(
                split_dir,
                combined_path,
                pattern="*.SchLib",
                handle_conflicts="skip",
                verbose=debug,
            )
            if not success:
                raise RuntimeError(
                    f"Failed to create combined SchLib for {schdoc_path.name}"
                )

        manifest_entries.append(
            {
                "source_schdoc": str(schdoc_path),
                "combined_schlib": str(combined_path),
                "split_dir": str(split_dir),
                "split_symbol_count": successful,
                "split_results": dict(sorted(results.items())),
            }
        )
    return manifest_entries


def _extract_pcblibs_for_project(
    *,
    pcbdoc_paths: list[Path],
    output_root: Path,
    debug: bool,
) -> list[dict]:
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc

    combined_root = output_root / "combined"
    split_root = output_root / "split"
    combined_root.mkdir(parents=True, exist_ok=True)
    split_root.mkdir(parents=True, exist_ok=True)

    manifest_entries: list[dict] = []
    multi_board = len(pcbdoc_paths) > 1
    for pcbdoc_path in pcbdoc_paths:
        pcbdoc = AltiumPcbDoc.from_file(pcbdoc_path)
        pcblib = pcbdoc.extract_pcblib(verbose=debug)

        combined_path = combined_root / f"{pcbdoc_path.stem}.PcbLib"
        split_dir = split_root / pcbdoc_path.stem if multi_board else split_root

        pcblib.save(combined_path)
        split_results = pcblib.split(split_dir, verbose=debug)

        manifest_entries.append(
            {
                "source_pcbdoc": str(pcbdoc_path),
                "combined_pcblib": str(combined_path),
                "split_dir": str(split_dir),
                "footprint_count": len(pcblib.footprints),
                "split_file_count": len(split_results),
            }
        )
    return manifest_entries


def cmd_megamaid(args) -> int:
    """Decompose a PrjPcb into library, BOM, netlist, and embedded-asset outputs."""
    from altium_monkey.altium_design import AltiumDesign

    if args.file:
        input_file = Path(args.file).resolve()
        if not input_file.exists():
            log.error(f"File not found: {input_file}")
            return 1
    else:
        input_file = find_prjpcb_in_cwd()
        if input_file is None:
            log.error("No file specified and no .PrjPcb found in current directory")
            log.info("Usage: altium-cruncher megamaid [project.PrjPcb]")
            return 1
        log.info(f"Auto-detected project: {input_file.name}")

    if input_file.suffix.lower() != ".prjpcb":
        log.error(f"Unsupported file type: {input_file.suffix}")
        log.info("Supported type: .PrjPcb")
        return 1

    output_dir = _resolve_output_dir(args.output, "megamaid")
    debug = bool(getattr(args, "debug", False))
    _prepare_megamaid_output_root(output_dir)
    log.info("Output directory: %s", output_dir)

    try:
        design = AltiumDesign.from_prjpcb(input_file)
        schdoc_paths = design.project.get_schdoc_paths() if design.project else []
        pcbdoc_paths = design.get_pcbdoc_paths()
        if not schdoc_paths and not pcbdoc_paths:
            log.error("No SchDoc or PcbDoc files found in project: %s", input_file)
            return 1

        sch_manifest = _extract_schlibs_for_project(
            schdoc_paths=schdoc_paths,
            output_root=output_dir / "schlib",
            debug=debug,
        )
        pcb_manifest = _extract_pcblibs_for_project(
            pcbdoc_paths=pcbdoc_paths,
            output_root=output_dir / "pcblib",
            debug=debug,
        )
        asset_manifest = _extract_project_embedded_assets(
            pcbdoc_paths=pcbdoc_paths,
            output_root=output_dir,
            debug=debug,
        )
        sch_image_manifest = _extract_project_schematic_images(
            schdoc_paths=schdoc_paths,
            output_root=output_dir,
            debug=debug,
        )

        base_bom = design.to_bom()
        bom_path = output_dir / "bom" / f"{input_file.stem}_bom.csv"
        _write_bom_csv(base_bom, bom_path)

        netlist_payload = design.to_json(include_indexes=True)
        netlist_path = output_dir / "netlist" / f"{input_file.stem}_netlist.json"
        netlist_path.parent.mkdir(parents=True, exist_ok=True)
        netlist_path.write_text(json.dumps(netlist_payload, indent=2), encoding="utf-8")

        manifest = {
            "kind": "megamaid",
            "input_project": str(input_file),
            "output_root": str(output_dir),
            "variants": design.get_variants(),
            "schdoc_count": len(schdoc_paths),
            "pcbdoc_count": len(pcbdoc_paths),
            "bom": {
                "base_csv": _relative_to_root(bom_path, output_dir),
                "component_count": len(base_bom),
            },
            "netlist": {
                "design_json": _relative_to_root(netlist_path, output_dir),
                "component_count": len(netlist_payload.get("components", [])),
                "net_count": len(netlist_payload.get("nets", [])),
            },
            "schlib": [
                {
                    **entry,
                    "combined_schlib": _relative_to_root(
                        Path(entry["combined_schlib"]), output_dir
                    ),
                    "split_dir": _relative_to_root(
                        Path(entry["split_dir"]), output_dir
                    ),
                }
                for entry in sch_manifest
            ],
            "pcblib": [
                {
                    **entry,
                    "combined_pcblib": _relative_to_root(
                        Path(entry["combined_pcblib"]), output_dir
                    ),
                    "split_dir": _relative_to_root(
                        Path(entry["split_dir"]), output_dir
                    ),
                }
                for entry in pcb_manifest
            ],
            "embedded_assets": {
                "fonts": [
                    {
                        **entry,
                        "output_file": _relative_to_root(
                            Path(entry["output_file"]), output_dir
                        ),
                    }
                    for entry in asset_manifest["fonts"]
                ],
                "models": [
                    {
                        **entry,
                        "output_file": _relative_to_root(
                            Path(entry["output_file"]), output_dir
                        ),
                    }
                    for entry in asset_manifest["models"]
                ],
                "font_file_count": len(
                    {entry["output_file"] for entry in asset_manifest["fonts"]}
                ),
                "model_file_count": len(
                    {entry["output_file"] for entry in asset_manifest["models"]}
                ),
            },
            "sch_images": {
                "images": [
                    {
                        **entry,
                        "output_file": _relative_to_root(
                            Path(entry["output_file"]), output_dir
                        ),
                    }
                    for entry in sch_image_manifest
                ],
                "image_file_count": len(
                    {entry["output_file"] for entry in sch_image_manifest}
                ),
            },
        }
        manifest_path = output_dir / "megamaid_manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        log.info("SchLib outputs: %d document(s)", len(sch_manifest))
        log.info("PcbLib outputs: %d document(s)", len(pcb_manifest))
        log.info("BOM: %s", bom_path.name)
        log.info("Netlist: %s", netlist_path.name)
        log.info("Manifest: %s", manifest_path.name)
        return 0
    except Exception as exc:
        log.error("Megamaid failed for %s: %s", input_file.name, exc)
        return 1


def register_parser(subparsers):
    megamaid_parser = subparsers.add_parser(
        "megamaid",
        help="decompose a PrjPcb into libs, BOM, netlist, and embedded assets",
        description=(
            "Decompose an Altium project into extracted SchLib/PcbLib outputs, "
            "BOM, netlist/design JSON, and embedded PCB assets."
        ),
        epilog=(
            "Examples:\n"
            "  altium-cruncher megamaid project.PrjPcb\n"
            "  altium-cruncher megamaid                 # Auto-detect PrjPcb in CWD\n"
            "  altium-cruncher megamaid project.PrjPcb -o output/megamaid\n"
            "\n"
            "Output tree:\n"
            "  schlib/combined, schlib/split\n"
            "  pcblib/combined, pcblib/split\n"
            "  bom, netlist\n"
            "  embedded_models, embedded_fonts\n"
            "  sch_images\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    megamaid_parser.add_argument(
        "file",
        nargs="?",
        help="PrjPcb file (optional if auto-detected in CWD)",
    )
    megamaid_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output directory (default: ./output/megamaid)",
    )
    megamaid_parser.add_argument(
        "--debug",
        action="store_true",
        help="enable debug output",
    )
    megamaid_parser.set_defaults(handler=cmd_megamaid)
    return megamaid_parser
