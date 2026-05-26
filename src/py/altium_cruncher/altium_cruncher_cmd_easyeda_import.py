"""easyeda-import command for altium_cruncher."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Any

from altium_cruncher.altium_cruncher_common import _resolve_output_dir
from altium_cruncher.easyeda_altium_symbol import (
    EasyEdaSchematicImportPolicy,
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


def cmd_easyeda_import(args: argparse.Namespace) -> int:
    """Generate Altium library artifacts from an EasyEDA/LCSC component."""

    output_dir = _resolve_output_dir(args.output, "easyeda-import")
    case_dir = output_dir / _safe_part_id(args.lcsc_id)
    case_dir.mkdir(parents=True, exist_ok=True)

    try:
        easyeda_symbol, source_data = _load_source_data(args)
        preview_dir = case_dir / "preview" if getattr(args, "preview", False) else None
        if preview_dir is not None:
            preview_dir.mkdir(parents=True, exist_ok=True)

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
            svg_dict = render_altium_library_preview_svgs(
                library=result.library,
                output_dir=preview_dir,
                background="none",
                pin_text_follows_orientation=_preview_pin_text_follows_orientation(policy),
            )
            svg_count = sum(len(parts) for parts in svg_dict.values())
            log.info("Generated %s schematic preview SVG(s): %s", svg_count, preview_dir)
            altium_svg_content = _first_svg_content(svg_dict)
            if altium_svg_content:
                preview_artifacts = write_easyeda_symbol_preview_artifacts(
                    easyeda_symbol=easyeda_symbol,
                    altium_svg_content=altium_svg_content,
                    output_dir=preview_dir,
                    symbol_name=result.report.symbol_name,
                )
                log.info("Generated EasyEDA source SVG: %s", preview_artifacts.easyeda_source_svg)
                log.info("Generated comparison SVG: %s", preview_artifacts.compare_svg)

        if getattr(args, "footprint", False) or getattr(args, "full", False):
            _write_footprint_artifacts(
                args=args,
                case_dir=case_dir,
                preview_dir=preview_dir,
                source_data=source_data,
            )

        return 0
    except Exception as exc:
        log.exception("EasyEDA import failed: %s", exc)
        return 1


def _load_source_data(args: argparse.Namespace) -> tuple[EasyEdaSymbol, dict[str, Any] | None]:
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
    source_data: dict[str, Any] | None,
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


def _load_footprint_data(
    args: argparse.Namespace,
    source_data: dict[str, Any] | None,
) -> tuple[EasyEdaFootprint, dict[str, Any] | None]:
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
        help="generate Altium library artifacts from EasyEDA/LCSC component data",
        description="Generate an Altium schematic library from EasyEDA/LCSC component data.",
        epilog=(
            "Examples:\n"
            "  altium-cruncher easyeda-import C2040 --preview\n"
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
        help="do not call the EasyEDA API; require --input-json or a cached response",
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
        help="also generate an Altium PcbLib footprint",
    )
    easyeda_parser.add_argument(
        "--full",
        action="store_true",
        help="generate all currently supported artifacts; equivalent to --footprint",
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
