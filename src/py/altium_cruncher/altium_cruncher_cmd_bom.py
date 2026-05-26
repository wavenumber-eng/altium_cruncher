"""BOM command for altium_cruncher."""

import argparse
import csv
from datetime import UTC, datetime
import json
import logging
from pathlib import Path
import zipfile
from xml.sax.saxutils import escape

from altium_cruncher.altium_cruncher_common import (
    _resolve_output_dir,
    find_prjpcb_in_cwd,
)

log = logging.getLogger(__name__)

BOM_FIXED_COLUMNS = [
    "Designator",
    "Value",
    "Footprint",
    "Library Ref",
    "Description",
    "Sheet",
    "DNP",
]


def _bom_parameter_columns(bom: list[dict]) -> list[str]:
    all_params = set()
    for comp in bom:
        all_params.update(comp.get("parameters", {}).keys())
    return sorted(all_params)


def _bom_rows(
    bom: list[dict], *, param_columns: list[str] | None = None
) -> list[list[str]]:
    columns = (
        param_columns if param_columns is not None else _bom_parameter_columns(bom)
    )
    rows: list[list[str]] = []
    for comp in sorted(bom, key=lambda c: c["designator"]):
        params = comp.get("parameters", {})
        rows.append(
            [
                str(comp.get("designator", "")),
                str(comp.get("value", "")),
                str(comp.get("footprint", "")),
                str(comp.get("library_ref", "")),
                str(comp.get("description", "")),
                str(comp.get("sheet", "")),
                "Yes" if comp.get("dnp") else "No",
                *[str(params.get(param_name, "")) for param_name in columns],
            ]
        )
    return rows


def _write_bom_csv(output_file: Path, bom: list[dict]) -> None:
    param_columns = _bom_parameter_columns(bom)
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(BOM_FIXED_COLUMNS + param_columns)
        writer.writerows(_bom_rows(bom, param_columns=param_columns))


def _generic_bom_payload(
    bom: list[dict],
    *,
    source: Path,
    variant: str | None,
) -> dict:
    param_columns = _bom_parameter_columns(bom)
    rows = _bom_rows(bom, param_columns=param_columns)
    columns = BOM_FIXED_COLUMNS + param_columns
    components = [
        {column: row[index] for index, column in enumerate(columns)} for row in rows
    ]
    return {
        "schema": "wn.altium_cruncher.bom.v1",
        "source": {
            "path": str(source),
            "name": source.name,
            "stem": source.stem,
        },
        "variant": variant,
        "component_count": len(bom),
        "dnp_count": sum(1 for component in bom if component.get("dnp")),
        "columns": columns,
        "parameter_columns": param_columns,
        "components": components,
        "raw_components": bom,
    }


def _write_bom_xlsx(output_file: Path, bom: list[dict]) -> None:
    param_columns = _bom_parameter_columns(bom)
    rows = [
        BOM_FIXED_COLUMNS + param_columns,
        *_bom_rows(bom, param_columns=param_columns),
    ]
    sheet_xml = _xlsx_sheet_xml(rows)
    created = (
        datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    )

    with zipfile.ZipFile(output_file, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", _XLSX_CONTENT_TYPES)
        zf.writestr("_rels/.rels", _XLSX_ROOT_RELS)
        zf.writestr("docProps/app.xml", _XLSX_APP_PROPS)
        zf.writestr("docProps/core.xml", _xlsx_core_props(created))
        zf.writestr("xl/workbook.xml", _XLSX_WORKBOOK)
        zf.writestr("xl/_rels/workbook.xml.rels", _XLSX_WORKBOOK_RELS)
        zf.writestr("xl/styles.xml", _XLSX_STYLES)
        zf.writestr("xl/worksheets/sheet1.xml", sheet_xml)


def _xlsx_sheet_xml(rows: list[list[str]]) -> str:
    row_xml: list[str] = []
    for row_index, row in enumerate(rows, start=1):
        cells = []
        for column_index, value in enumerate(row, start=1):
            ref = f"{_xlsx_column_name(column_index)}{row_index}"
            text = escape(str(value or ""))
            cells.append(f'<c r="{ref}" t="inlineStr"><is><t>{text}</t></is></c>')
        row_xml.append(f'<row r="{row_index}">{"".join(cells)}</row>')
    dimension = f"A1:{_xlsx_column_name(max((len(row) for row in rows), default=1))}{max(len(rows), 1)}"
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f'<dimension ref="{dimension}"/>'
        '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" '
        'activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>'
        "<sheetData>"
        f"{''.join(row_xml)}"
        "</sheetData>"
        "</worksheet>"
    )


def _xlsx_column_name(index: int) -> str:
    if index < 1:
        raise ValueError("XLSX column indexes are 1-based")
    name = ""
    while index:
        index, rem = divmod(index - 1, 26)
        name = chr(65 + rem) + name
    return name


def _xlsx_core_props(created: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        "<dc:creator>altium_cruncher</dc:creator>"
        "<cp:lastModifiedBy>altium_cruncher</cp:lastModifiedBy>"
        f'<dcterms:created xsi:type="dcterms:W3CDTF">{created}</dcterms:created>'
        f'<dcterms:modified xsi:type="dcterms:W3CDTF">{created}</dcterms:modified>'
        "</cp:coreProperties>"
    )


_XLSX_CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>"""

_XLSX_ROOT_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>"""

_XLSX_WORKBOOK = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets><sheet name="BOM" sheetId="1" r:id="rId1"/></sheets>
</workbook>"""

_XLSX_WORKBOOK_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

_XLSX_STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>
<fills count="1"><fill><patternFill patternType="none"/></fill></fills>
<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>
</styleSheet>"""

_XLSX_APP_PROPS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
<Application>altium_cruncher</Application>
</Properties>"""


def cmd_bom(args) -> int:
    """
    Handle bom subcommand - generate BOM from SchDoc/PrjPcb files.

    REQ-CLI-004: BOM generation with variant support (CSV or JSON format).

    Args:
        args: Parsed argparse namespace with file and output options.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    from altium_monkey.altium_design import AltiumDesign

    # Determine input file
    input_file: Path | None = None

    if args.file:
        input_file = Path(args.file).resolve()
        if not input_file.exists():
            log.error(f"File not found: {input_file}")
            return 1
    else:
        # Auto-detect PrjPcb in CWD
        input_file = find_prjpcb_in_cwd()
        if not input_file:
            log.error("No file specified and no .PrjPcb found in current directory")
            log.info("Usage: altium-cruncher bom [file.SchDoc | project.PrjPcb]")
            return 1
        log.info(f"Auto-detected project: {input_file.name}")

    # Validate file type
    suffix = input_file.suffix.lower()
    if suffix == ".schdoc":
        design = AltiumDesign.from_schdoc(input_file)
    elif suffix == ".prjpcb":
        design = AltiumDesign.from_prjpcb(input_file)
    else:
        log.error(f"Unsupported file type: {suffix}")
        log.info("Supported types: .SchDoc, .PrjPcb")
        return 1

    # Show available variants
    available_variants = design.get_variants()
    if available_variants:
        log.info(f"Available variants: {', '.join(available_variants)}")
    else:
        log.info("No variants defined in project")

    # Determine output directory
    output_dir = _resolve_output_dir(args.output, "bom")

    # Determine which variants to process
    all_variants = getattr(args, "all_variants", False)
    variant = getattr(args, "variant", None)

    if all_variants and available_variants:
        variants_to_process = [None] + available_variants  # None = base (no variant)
    elif variant:
        if variant not in available_variants:
            log.warning(
                f"Variant '{variant}' not found in project (available: {', '.join(available_variants) or 'none'})"
            )
        variants_to_process = [variant]
    else:
        variants_to_process = [None]  # No variant filtering

    # Get output format
    output_format = getattr(args, "format", "csv")

    files_written = 0
    for var in variants_to_process:
        bom = design.to_bom(variant=var)

        # Determine output filename
        base_name = input_file.stem
        if output_format in {"json", "generic-json"}:
            ext = "json"
        elif output_format == "xlsx":
            ext = "xlsx"
        else:
            ext = "csv"
        if var:
            output_file = output_dir / f"{base_name}_{var}_bom.{ext}"
        else:
            output_file = output_dir / f"{base_name}_bom.{ext}"

        if output_format == "json":
            # Write JSON (preserves full structure with nested parameters)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(bom, f, indent=2)
        elif output_format == "generic-json":
            payload = _generic_bom_payload(bom, source=input_file, variant=var)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
        elif output_format == "xlsx":
            _write_bom_xlsx(output_file, bom)
        else:
            _write_bom_csv(output_file, bom)

        variant_name = var or "base"
        log.info(f"BOM ({variant_name}): {len(bom)} components -> {output_file.name}")
        files_written += 1

        # Count DNP components
        dnp_count = sum(1 for c in bom if c["dnp"])
        if dnp_count > 0:
            log.info(f"  DNP (Do Not Populate): {dnp_count}")

    log.info(f"Generated {files_written} BOM file(s) in {output_dir}")
    return 0


def register_parser(subparsers):
    # bom subcommand - Generate BOM from SchDoc/PrjPcb
    bom_parser = subparsers.add_parser(
        "bom",
        help="generate BOM from Altium schematic documents (CSV, JSON, or XLSX)",
        description="Generate Bill of Materials (BOM) from Altium SchDoc or PrjPcb files. "
        "CSV/XLSX formats include parameters as columns; JSON preserves nested structure.",
        epilog="Examples:\n"
        "  altium-cruncher bom project.PrjPcb\n"
        "  altium-cruncher bom schematic.SchDoc\n"
        "  altium-cruncher bom                               # Auto-detect PrjPcb in CWD\n"
        "  altium-cruncher bom project.PrjPcb --variant V1   # Single variant\n"
        "  altium-cruncher bom project.PrjPcb --all-variants # All variants\n"
        "  altium-cruncher bom project.PrjPcb --format json  # JSON output\n"
        "  altium-cruncher bom project.PrjPcb --format generic-json\n"
        "  altium-cruncher bom project.PrjPcb --format xlsx  # XLSX output\n"
        "  altium-cruncher bom project.PrjPcb -o output_dir/",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    bom_parser.add_argument(
        "file", nargs="?", help="SchDoc or PrjPcb file (optional if PrjPcb in CWD)"
    )
    bom_parser.add_argument(
        "-o", "--output", type=Path, help="output directory (default: ./output/bom)"
    )
    bom_parser.add_argument(
        "--format",
        choices=["csv", "json", "generic-json", "xlsx"],
        default="csv",
        help="output format (default: csv)",
    )
    bom_parser.add_argument(
        "--variant", type=str, help="filter by specific variant name"
    )
    bom_parser.add_argument(
        "--all-variants",
        action="store_true",
        help="generate BOM for all variants (plus base)",
    )
    bom_parser.set_defaults(handler=cmd_bom)
    return bom_parser
