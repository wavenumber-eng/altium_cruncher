"""easyeda-import command for altium_cruncher."""

from __future__ import annotations

import argparse
from collections.abc import Mapping
from dataclasses import asdict, dataclass
import json
import logging
from pathlib import Path
import urllib.error
import urllib.request

from altium_cruncher.altium_cruncher_common import _resolve_output_dir
from altium_cruncher.easyeda_altium_symbol import (
    EasyEdaSchematicImportPolicy,
    EasyEdaSchematicImportResult,
    build_altium_schlib_from_easyeda_symbol,
    load_easyeda_symbol_input,
)
from altium_cruncher.easyeda_altium_footprint import (
    build_altium_pcblib_from_easyeda_footprint,
    load_easyeda_footprint_input,
    render_easyeda_footprint_source_svg,
)
from altium_cruncher.easyeda_altium_preview import (
    _svg_document_from_content,
    render_altium_library_preview_svgs,
    render_compare_svg,
    write_easyeda_symbol_preview_artifacts,
)
from easyeda_monkey.easyeda_api import EasyEdaApiClient
from easyeda_monkey.easyeda_footprint import EasyEdaFootprint
from easyeda_monkey.easyeda_symbol import EasyEdaSymbol

log = logging.getLogger(__name__)

_EASYEDA_3D_MODEL_OBJ_URL = "https://modules.easyeda.com/3dmodel/{uuid}"
_EASYEDA_3D_MODEL_STEP_URL = "https://modules.easyeda.com/qAxj6KHrDKw4blvCG8QJPs7Y/{uuid}"


@dataclass(frozen=True)
class _EasyEda3DModelRef:
    uuid: str
    title: str
    origin: str
    z: str
    rotation: str


def cmd_easyeda_import(args: argparse.Namespace) -> int:
    """Generate Altium library artifacts from an EasyEDA/LCSC component."""

    output_dir = _resolve_output_dir(args.output, "easyeda-import")
    case_dir = output_dir / _safe_part_id(args.lcsc_id)
    case_dir.mkdir(parents=True, exist_ok=True)

    try:
        easyeda_symbol, source_data = _load_source_data(args)
        preview_dir = _preview_dir_from_args(args, case_dir)

        policy = _policy_from_args(args)
        result = build_altium_schlib_from_easyeda_symbol(
            easyeda_symbol,
            source_data=source_data,
            symbol_name=args.symbol_name,
            policy=policy,
        )
        schlib_name = args.schlib_name or f"{_safe_part_id(args.lcsc_id)}.SchLib"
        schlib_path = case_dir / schlib_name
        result.library.save(schlib_path, sync_pin_text_data=True)

        report_path = case_dir / "easyeda-import-report.json"
        result.report.write_json(report_path)

        log.info("Generated SchLib: %s", schlib_path)
        log.info(
            "Mapped %s pins, %s rectangles, %s polylines, %s polygons",
            result.report.pin_count,
            result.report.rectangle_count,
            result.report.polyline_count,
            result.report.polygon_count,
        )
        if result.report.unsupported_graphics:
            log.warning(
                "Skipped %s unsupported schematic graphic(s); see %s",
                result.report.unsupported_count,
                report_path,
            )

        if preview_dir is not None:
            _write_schematic_preview_artifacts(
                easyeda_symbol=easyeda_symbol,
                result=result,
                policy=policy,
                preview_dir=preview_dir,
            )

        if _should_write_footprint_artifacts(args):
            _write_footprint_artifacts(
                args=args,
                case_dir=case_dir,
                preview_dir=preview_dir,
                source_data=source_data,
            )
            if _should_download_3d_model_artifacts(args):
                _write_3d_model_artifacts(
                    case_dir=case_dir,
                    source_data=source_data,
                    lcsc_id=args.lcsc_id,
                )

        return 0
    except Exception as exc:
        log.exception("EasyEDA import failed: %s", exc)
        return 1


def _preview_dir_from_args(args: argparse.Namespace, case_dir: Path) -> Path | None:
    if not getattr(args, "preview", False):
        return None
    preview_dir = case_dir / "preview"
    preview_dir.mkdir(parents=True, exist_ok=True)
    return preview_dir


def _should_write_footprint_artifacts(args: argparse.Namespace) -> bool:
    return not getattr(args, "symbol_only", False)


def _should_download_3d_model_artifacts(args: argparse.Namespace) -> bool:
    return not getattr(args, "no_fetch", False) and not getattr(
        args,
        "no_3d_model_download",
        False,
    )


def _load_source_data(
    args: argparse.Namespace,
) -> tuple[EasyEdaSymbol, dict[str, object] | None]:
    if args.input_json:
        return load_easyeda_symbol_input(Path(args.input_json))

    cache_dir = Path(args.cache_dir) if args.cache_dir else None
    if args.no_fetch:
        if cache_dir is None:
            raise ValueError("--no-fetch requires --cache-dir or --input-json")
        cache_path = cache_dir / f"{_safe_part_id(args.lcsc_id)}.json"
        if not cache_path.exists():
            raise FileNotFoundError(f"Cached EasyEDA response not found: {cache_path}")
        return load_easyeda_symbol_input(cache_path)

    client = EasyEdaApiClient(cache_dir=cache_dir)
    source_data = client.fetch_component(args.lcsc_id)
    if not source_data:
        raise ValueError(f"No EasyEDA component data returned for {args.lcsc_id}")
    return EasyEdaSymbol.from_json(source_data), source_data


def _write_footprint_artifacts(
    *,
    args: argparse.Namespace,
    case_dir: Path,
    preview_dir: Path | None,
    source_data: dict[str, object] | None,
) -> None:
    easyeda_footprint, footprint_source_data = _load_footprint_data(args, source_data)
    footprint_result = build_altium_pcblib_from_easyeda_footprint(
        easyeda_footprint,
        source_data=footprint_source_data,
        footprint_name=getattr(args, "footprint_name", None),
    )

    pcblib_name = getattr(args, "pcblib_name", None) or f"{_safe_part_id(args.lcsc_id)}.PcbLib"
    pcblib_path = case_dir / pcblib_name
    footprint_result.library.save(pcblib_path)

    report_path = case_dir / "easyeda-footprint-report.json"
    footprint_result.report.write_json(report_path)

    log.info("Generated PcbLib: %s", pcblib_path)
    log.info(
        "Mapped %s footprint pad(s), %s raw graphic(s), %s unsupported footprint item(s)",
        footprint_result.report.generated_pad_count,
        (
            footprint_result.report.track_count
            + footprint_result.report.circle_count
            + footprint_result.report.arc_count
            + footprint_result.report.rectangle_count
            + footprint_result.report.region_count
        ),
        footprint_result.report.unsupported_count,
    )

    if preview_dir is None:
        return

    source_svg = render_easyeda_footprint_source_svg(
        easyeda_footprint,
        source_data=footprint_source_data,
    )
    source_svg_path = preview_dir / "easyeda-footprint-source.svg"
    source_svg_path.write_text(source_svg, encoding="utf-8")

    altium_svg = footprint_result.library.footprints[0].to_svg()
    altium_svg_path = preview_dir / "altium-footprint.svg"
    altium_svg_path.write_text(altium_svg, encoding="utf-8")

    compare_svg = render_compare_svg(
        easyeda_svg=_svg_document_from_content(source_svg),
        altium_svg=_svg_document_from_content(altium_svg),
        symbol_name=footprint_result.report.footprint_name,
    )
    compare_svg_path = preview_dir / "footprint-compare.svg"
    compare_svg_path.write_text(compare_svg, encoding="utf-8")
    log.info("Generated footprint preview SVGs: %s", preview_dir)


def _write_schematic_preview_artifacts(
    *,
    easyeda_symbol: EasyEdaSymbol,
    result: EasyEdaSchematicImportResult,
    policy: EasyEdaSchematicImportPolicy,
    preview_dir: Path,
) -> None:
    svg_dict = render_altium_library_preview_svgs(
        library=result.library,
        output_dir=preview_dir,
        background="none",
        pin_text_follows_orientation=_preview_pin_text_follows_orientation(policy),
    )
    svg_count = sum(len(parts) for parts in svg_dict.values())
    log.info("Generated %s schematic preview SVG(s): %s", svg_count, preview_dir)
    altium_svg_content = _first_svg_content(svg_dict)
    if not altium_svg_content:
        return

    preview_artifacts = write_easyeda_symbol_preview_artifacts(
        easyeda_symbol=easyeda_symbol,
        altium_svg_content=altium_svg_content,
        output_dir=preview_dir,
        symbol_name=result.report.symbol_name,
    )
    log.info("Generated EasyEDA source SVG: %s", preview_artifacts.easyeda_source_svg)
    log.info("Generated comparison SVG: %s", preview_artifacts.compare_svg)


def _write_3d_model_artifacts(
    *,
    case_dir: Path,
    source_data: dict[str, object] | None,
    lcsc_id: str,
) -> None:
    model_refs = _extract_3d_model_refs(source_data)
    if not model_refs:
        log.info("No EasyEDA 3D model reference found")
        return

    model_dir = case_dir / "3d_models"
    model_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, object] = {
        "schema": "wn.altium_cruncher.easyeda.3d_models.v1",
        "lcsc_id": _safe_part_id(lcsc_id),
        "placement_implemented": False,
        "placement_note": (
            "3D model download is implemented, but placement/attachment into "
            "the generated Altium PcbLib footprint is not implemented."
        ),
        "models": [],
    }

    for index, model_ref in enumerate(model_refs, start=1):
        stem = _safe_artifact_stem(model_ref.title or model_ref.uuid or f"model_{index}")
        files: dict[str, str] = {}
        errors: dict[str, str] = {}
        for file_kind, url_template, suffix in (
            ("obj", _EASYEDA_3D_MODEL_OBJ_URL, ".obj"),
            ("step", _EASYEDA_3D_MODEL_STEP_URL, ".step"),
        ):
            output_path = model_dir / f"{stem}{suffix}"
            try:
                payload = _download_easyeda_model_bytes(
                    url_template.format(uuid=model_ref.uuid)
                )
                output_path.write_bytes(payload)
                files[file_kind] = str(output_path.relative_to(case_dir))
                log.info("Downloaded EasyEDA 3D %s model: %s", file_kind.upper(), output_path)
            except Exception as exc:
                errors[file_kind] = str(exc)
                log.warning(
                    "Could not download EasyEDA 3D %s model for %s: %s",
                    file_kind.upper(),
                    model_ref.uuid,
                    exc,
                )

        model_entry: dict[str, object] = asdict(model_ref)
        model_entry.update(
            {
                "files": files,
                "errors": errors,
                "placement_status": "downloaded_not_attached" if files else "not_downloaded",
            }
        )
        cast_models = manifest["models"]
        if isinstance(cast_models, list):
            cast_models.append(model_entry)

    manifest_path = case_dir / "easyeda-3d-models.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def _download_easyeda_model_bytes(url: str) -> bytes:
    request = urllib.request.Request(
        url=url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:  # noqa: S310
            status = getattr(response, "status", 200)
            if status != 200:
                raise RuntimeError(f"unexpected HTTP status {status}")
            return response.read()
    except urllib.error.URLError as exc:
        raise RuntimeError(str(exc)) from exc


def _extract_3d_model_refs(
    source_data: dict[str, object] | None,
) -> list[_EasyEda3DModelRef]:
    model_refs: list[_EasyEda3DModelRef] = []
    seen: set[str] = set()
    for shape in _package_shapes(source_data):
        model_ref = _model_ref_from_shape(shape)
        if model_ref is None or model_ref.uuid in seen:
            continue
        seen.add(model_ref.uuid)
        model_refs.append(model_ref)
    return model_refs


def _package_shapes(source_data: dict[str, object] | None) -> list[object]:
    result = _mapping_child(source_data or {}, "result")
    package_detail = _mapping_child(result, "packageDetail")
    data_str = _mapping_child(package_detail, "dataStr")
    raw_shapes = data_str.get("shape", [])
    return raw_shapes if isinstance(raw_shapes, list) else []


def _mapping_child(data: Mapping[str, object], key: str) -> Mapping[str, object]:
    child = data.get(key)
    return child if isinstance(child, Mapping) else {}


def _model_ref_from_shape(shape: object) -> _EasyEda3DModelRef | None:
    if not isinstance(shape, str) or not shape.startswith("SVGNODE~"):
        return None
    try:
        node = json.loads(shape.split("~", 1)[1])
    except json.JSONDecodeError:
        return None
    attrs = node.get("attrs", {}) if isinstance(node, dict) else {}
    if not isinstance(attrs, dict):
        return None
    if str(attrs.get("c_etype", "")).strip().lower() != "outline3d":
        return None
    uuid = str(attrs.get("uuid", "")).strip()
    if not uuid:
        return None
    return _EasyEda3DModelRef(
        uuid=uuid,
        title=str(attrs.get("title", "")).strip(),
        origin=str(attrs.get("c_origin", "")).strip(),
        z=str(attrs.get("z", "")).strip(),
        rotation=str(attrs.get("c_rotation", "")).strip(),
    )


def _load_footprint_data(
    args: argparse.Namespace,
    source_data: dict[str, object] | None,
) -> tuple[EasyEdaFootprint, dict[str, object] | None]:
    if source_data is not None:
        return EasyEdaFootprint.from_json(source_data), source_data
    if args.input_json:
        return load_easyeda_footprint_input(Path(args.input_json))
    raise ValueError("Footprint import requires EasyEDA source data")


def _safe_part_id(value: str) -> str:
    text = str(value or "").strip().upper()
    if not text:
        return "EASYEDA_PART"
    if not text.startswith("C") and text[0].isdigit():
        text = f"C{text}"
    return "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in text)


def _safe_artifact_stem(value: str) -> str:
    stem = "".join(ch if ch.isalnum() or ch in {"-", "_", "."} else "_" for ch in value)
    return stem.strip("._-") or "model"


def _first_svg_content(svg_dict: dict[str, dict[int, str]]) -> str | None:
    for parts in svg_dict.values():
        for svg in parts.values():
            return svg
    return None


def _policy_from_args(args: argparse.Namespace) -> EasyEdaSchematicImportPolicy:
    return EasyEdaSchematicImportPolicy(
        hotspot_grid_mils=getattr(args, "pin_grid_mils", 100.0),
        align_hotspots_to_grid=not getattr(args, "no_align_pin_grid", False),
        use_source_pin_electrical=getattr(args, "use_source_pin_electrical", False),
        use_source_pin_ieee_symbols=getattr(args, "use_source_pin_ieee_symbols", False),
        pin_name_visibility=getattr(args, "pin_name_visibility", "source"),
        pin_designator_visibility=getattr(args, "pin_designator_visibility", "source"),
        pin_text_orientation=getattr(args, "pin_text_orientation", "default"),
        rotate_vertical_pin_text=getattr(args, "rotate_vertical_pin_text", False),
    )


def _preview_pin_text_follows_orientation(policy: EasyEdaSchematicImportPolicy) -> bool:
    return (
        policy.rotate_vertical_pin_text
        or policy.pin_text_orientation.strip().lower() in {"source", "vertical"}
    )


def register_parser(subparsers):
    easyeda_parser = subparsers.add_parser(
        "easyeda-import",
        help="EXPERIMENTAL: generate Altium SchLib, PcbLib, and downloaded 3D assets",
        description=(
            "EXPERIMENTAL: generate Altium schematic-library and PCB-library "
            "artifacts from EasyEDA/LCSC component data by default. If an "
            "EasyEDA 3D model is referenced and network fetches are enabled, "
            "the command downloads OBJ and STEP assets. 3D model placement/"
            "attachment into the generated Altium PcbLib is not implemented."
        ),
        epilog=(
            "Examples:\n"
            "  altium-cruncher easyeda-import C2040 --preview\n"
            "  altium-cruncher easyeda-import C2040 --symbol-only\n"
            "  altium-cruncher easyeda-import C2040 --input-json C2040.json -o output/easyeda-import"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    easyeda_parser.add_argument(
        "lcsc_id",
        help="LCSC part number, e.g. C2040",
    )
    easyeda_parser.add_argument(
        "--input-json",
        type=Path,
        help="saved EasyEDA API response or EasyEdaSymbol JSON file",
    )
    easyeda_parser.add_argument(
        "--cache-dir",
        type=Path,
        help="cache directory for live EasyEDA API responses",
    )
    easyeda_parser.add_argument(
        "--no-fetch",
        action="store_true",
        help=(
            "do not call the EasyEDA API or download 3D models; require "
            "--input-json or a cached response"
        ),
    )
    easyeda_parser.add_argument(
        "--symbol-name",
        help="override generated SchLib symbol name",
    )
    easyeda_parser.add_argument(
        "--schlib-name",
        help="override generated SchLib filename",
    )
    easyeda_parser.add_argument(
        "--footprint",
        action="store_true",
        help="accepted for compatibility; PcbLib footprint generation is now the default",
    )
    easyeda_parser.add_argument(
        "--full",
        action="store_true",
        help="accepted for compatibility; full output is now the default",
    )
    easyeda_parser.add_argument(
        "--symbol-only",
        action="store_true",
        help="generate only the SchLib/report outputs; skip PcbLib and 3D asset download",
    )
    easyeda_parser.add_argument(
        "--footprint-name",
        help="override generated PcbLib footprint name",
    )
    easyeda_parser.add_argument(
        "--pcblib-name",
        help="override generated PcbLib filename",
    )
    easyeda_parser.add_argument(
        "--preview",
        action="store_true",
        help="also generate SVG preview from the generated SchLib",
    )
    easyeda_parser.add_argument(
        "--no-3d-model-download",
        action="store_true",
        help=(
            "skip EasyEDA 3D model asset download; placement into PcbLib is "
            "not implemented either way"
        ),
    )
    easyeda_parser.add_argument(
        "--pin-grid-mils",
        type=float,
        default=100.0,
        help="target schematic pin hotspot grid in mils (default: 100)",
    )
    easyeda_parser.add_argument(
        "--no-align-pin-grid",
        action="store_true",
        help="do not adjust the symbol anchor to place hotspots on the target grid",
    )
    easyeda_parser.add_argument(
        "--use-source-pin-electrical",
        action="store_true",
        help="map EasyEDA pin electrical types instead of importing every pin as passive",
    )
    easyeda_parser.add_argument(
        "--use-source-pin-ieee-symbols",
        action="store_true",
        help="map EasyEDA pin dot/clock markers to Altium IEEE pin symbols",
    )
    easyeda_parser.add_argument(
        "--pin-name-visibility",
        choices=("source", "show", "hide"),
        default="source",
        help="pin name visibility policy (default: source)",
    )
    easyeda_parser.add_argument(
        "--pin-designator-visibility",
        choices=("source", "show", "hide"),
        default="source",
        help="pin designator visibility policy (default: source)",
    )
    easyeda_parser.add_argument(
        "--rotate-vertical-pin-text",
        action="store_true",
        help="alias for --pin-text-orientation vertical unless another mode is set",
    )
    easyeda_parser.add_argument(
        "--pin-text-orientation",
        choices=("default", "vertical", "source"),
        default="default",
        help=(
            "pin name/designator orientation policy: default Altium layout, "
            "vertical for 90/270 pins, or source EasyEDA text orientation "
            "(default: default)"
        ),
    )
    easyeda_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output directory (default: ./output/easyeda-import)",
    )
    easyeda_parser.set_defaults(handler=cmd_easyeda_import)
    return easyeda_parser
