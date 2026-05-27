"""BOM command for altium_cruncher."""

import argparse
from collections.abc import Mapping, Sequence
import csv
from datetime import UTC, datetime
import json
import logging
from pathlib import Path
from typing import Protocol
import zipfile
from xml.sax.saxutils import escape

from altium_cruncher.altium_cruncher_common import (
    _resolve_output_dir,
    find_prjpcb_in_cwd,
)
from altium_cruncher.bom_pnp_cli_common import (
    configured_output_root,
    load_optional_bom_pnp_config,
    project_parameters_from_design,
    warn_for_unknown_variants,
    write_config_template,
    write_used_config_snapshot,
)
from altium_cruncher.bom_pnp_model import (
    BOM_GROUPED_DEFAULT_COLUMNS,
    BOM_PNP_DEFAULT_CONFIG_NAME,
    BomPnpConfig,
    GroupedBomLine,
    JLC_BOM_COLUMNS,
    NormalizedBomComponent,
    bom_raw_payload,
    configured_output_file,
    designator_sort_key,
    filter_bom_components,
    flat_raw_bom_payload,
    group_bom_components,
    grouped_bom_table_rows,
    grouped_bom_payload,
    jlc_bom_rows,
    make_pcb_line_item,
    normalize_bom_components,
    ordered_bom_lines,
    select_variant_names,
)
from altium_cruncher.output_path_templates import TemplateValue
from altium_cruncher.simple_xlsx import write_xlsx_table

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


class _BomDesign(Protocol):
    """Protocol for the AltiumDesign methods used by configured BOM output."""

    def to_bom(self, variant: str | None = None) -> list[dict]:
        """Return schematic-sourced BOM dictionaries."""
        ...

    def to_pnp(
        self,
        variant: str | None = None,
        units: str = "mm",
        exclude_no_bom: bool = False,
        position_mode: str = "altium-pick-place",
    ) -> Sequence[object]:
        """Return PCB-sourced placement entries."""
        ...


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
    for comp in sorted(
        bom,
        key=lambda c: designator_sort_key(str(c.get("designator", ""))),
    ):
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


def _write_named_rows_csv(
    output_file: Path,
    columns: Sequence[str],
    rows: Sequence[Mapping[str, str]],
) -> None:
    """Write named rows to CSV using a fixed column order."""
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _bom_output_extension(output_format: str) -> str:
    """Return the file extension for a BOM output format."""
    json_formats = {
        "json",
        "raw-json",
        "generic-json",
        "legacy-json",
        "grouped-json",
    }
    if output_format in json_formats:
        return "json"
    if output_format in {"xlsx", "grouped-xlsx", "jlc-xlsx"}:
        return "xlsx"
    return "csv"


def _write_bom_output(
    output_file: Path,
    bom: list[dict],
    *,
    output_format: str,
    source: Path,
    variant: str | None,
) -> None:
    """Write one BOM output artifact for the selected format."""
    if output_format == "json":
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(bom, f, indent=2)
        return
    if output_format == "raw-json":
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(flat_raw_bom_payload(bom), f, indent=2)
        return
    if output_format in {"generic-json", "legacy-json"}:
        payload = _generic_bom_payload(bom, source=source, variant=variant)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        return
    if output_format == "grouped-json":
        normalized = normalize_bom_components(bom)
        lines = group_bom_components(normalized)
        payload = grouped_bom_payload(lines, source=source, variant=variant)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        return
    if output_format == "grouped-csv":
        normalized = normalize_bom_components(bom)
        lines = group_bom_components(normalized)
        rows = grouped_bom_table_rows(lines)
        _write_named_rows_csv(output_file, BOM_GROUPED_DEFAULT_COLUMNS, rows)
        return
    if output_format == "grouped-xlsx":
        normalized = normalize_bom_components(bom)
        lines = group_bom_components(normalized)
        rows = grouped_bom_table_rows(lines)
        write_xlsx_table(
            output_file,
            columns=BOM_GROUPED_DEFAULT_COLUMNS,
            rows=rows,
            sheet_name="BOM",
        )
        return
    if output_format == "jlc-csv":
        normalized = normalize_bom_components(bom)
        lines = group_bom_components(normalized)
        rows = jlc_bom_rows(lines)
        _write_named_rows_csv(output_file, JLC_BOM_COLUMNS, rows)
        return
    if output_format == "jlc-xlsx":
        normalized = normalize_bom_components(bom)
        lines = group_bom_components(normalized)
        rows = jlc_bom_rows(lines)
        write_xlsx_table(
            output_file,
            columns=JLC_BOM_COLUMNS,
            rows=rows,
            sheet_name="JLC BOM",
        )
        return
    if output_format == "xlsx":
        _write_bom_xlsx(output_file, bom)
        return
    _write_bom_csv(output_file, bom)


def _configured_bom_artifacts(
    output_root: Path,
    raw_bom: list[dict],
    *,
    config: BomPnpConfig,
    source: Path,
    variant: str | None,
    project_parameters: Mapping[str, TemplateValue],
    output_kinds: Sequence[str] | None = None,
    command: str = "bom",
) -> list[Path]:
    """Write all configured BOM artifacts and return their paths."""
    kinds = tuple(output_kinds or config.bom_outputs)
    components = normalize_bom_components(raw_bom, config.field_aliases)
    components = filter_bom_components(components, include_dnp=config.include_dnp)
    pcb_line = make_pcb_line_item(
        config,
        project_parameters,
        variant_name=variant,
    )
    if pcb_line is not None:
        components.append(pcb_line)
    lines = group_bom_components(
        components,
        group_fields=config.bom_group_fields,
        split_dnp=config.split_dnp,
        prefix_order=config.prefix_order,
    )
    written: list[Path] = []
    for output_kind in kinds:
        output_file = configured_output_file(
            output_root,
            config,
            source=source,
            command=command,
            output_kind=output_kind,
            extension=_bom_output_extension(output_kind),
            project_parameters=project_parameters,
            variant_name=variant,
        )
        _write_configured_bom_artifact(
            output_file,
            output_kind,
            raw_bom=raw_bom,
            components=components,
            lines=lines,
            config=config,
            source=source,
            variant=variant,
        )
        write_used_config_snapshot(output_file, config)
        written.append(output_file)
    return written


def _write_configured_bom_artifact(
    output_file: Path,
    output_kind: str,
    *,
    raw_bom: list[dict],
    components: Sequence[NormalizedBomComponent],
    lines: Sequence[GroupedBomLine],
    config: BomPnpConfig,
    source: Path,
    variant: str | None,
) -> None:
    """Write one configured BOM artifact."""
    if output_kind == "raw-json":
        output_file.write_text(
            json.dumps(flat_raw_bom_payload(raw_bom), indent=2),
            encoding="utf-8",
        )
        return
    if output_kind == "legacy-json":
        payload = _generic_bom_payload(raw_bom, source=source, variant=variant)
        output_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return
    if output_kind == "grouped-json":
        payload = grouped_bom_payload(
            ordered_bom_lines(lines, dnp_placement=config.dnp_placement),
            source=source,
            variant=variant,
        )
        output_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return
    if output_kind == "grouped-csv":
        ordered_lines = ordered_bom_lines(
            lines,
            dnp_placement=config.dnp_placement,
        )
        rows = grouped_bom_table_rows(
            ordered_lines,
            fields=config.bom_output_fields,
            dnp_placement=None,
        )
        _write_named_rows_csv(output_file, config.bom_output_fields, rows)
        return
    if output_kind == "grouped-xlsx":
        ordered_lines = ordered_bom_lines(
            lines,
            dnp_placement=config.dnp_placement,
        )
        rows = grouped_bom_table_rows(
            ordered_lines,
            fields=config.bom_output_fields,
            dnp_placement=None,
        )
        write_xlsx_table(
            output_file,
            columns=config.bom_output_fields,
            rows=rows,
            sheet_name="BOM",
            highlighted_rows=[line.dnp for line in ordered_lines]
            if config.highlight_dnp_rows
            else (),
        )
        return
    if output_kind == "jlc-csv":
        rows = jlc_bom_rows(
            ordered_bom_lines(lines, dnp_placement=config.dnp_placement),
            include_dnp=config.include_dnp,
        )
        _write_named_rows_csv(output_file, JLC_BOM_COLUMNS, rows)
        return
    if output_kind == "jlc-xlsx":
        rows = jlc_bom_rows(
            ordered_bom_lines(lines, dnp_placement=config.dnp_placement),
            include_dnp=config.include_dnp,
        )
        write_xlsx_table(
            output_file,
            columns=JLC_BOM_COLUMNS,
            rows=rows,
            sheet_name="JLC BOM",
        )
        return
    raise ValueError(f"Unsupported configured BOM output: {output_kind}")


def _entry_field(entry: object, name: str) -> object:
    """Read one field from a mapping or object-like entry."""
    if isinstance(entry, Mapping):
        return entry.get(name)
    return getattr(entry, name, None)


def _pnp_entry_to_bom_dict(entry: object) -> dict[str, object]:
    """Convert a placement entry into PCB-sourced BOM-like component data."""
    parameters = _entry_field(entry, "parameters")
    if not isinstance(parameters, Mapping):
        parameters = {}
    return {
        "designator": str(_entry_field(entry, "designator") or ""),
        "value": str(_entry_field(entry, "comment") or ""),
        "footprint": str(_entry_field(entry, "footprint") or ""),
        "library_ref": "",
        "description": str(_entry_field(entry, "description") or ""),
        "sheet": "",
        "parameters": {str(key): str(value) for key, value in parameters.items()},
        "dnp": False,
    }


def _bom_from_configured_source(
    design: _BomDesign,
    config: BomPnpConfig,
    *,
    variant: str | None,
) -> list[dict]:
    """Return BOM rows from the selected configured data source."""
    if config.bom_source_mode == "pcb":
        pnp_entries = design.to_pnp(
            variant=variant,
            units="mm",
            position_mode=config.pnp_position_mode,
            exclude_no_bom=True,
        )
        return [_pnp_entry_to_bom_dict(entry) for entry in pnp_entries]
    return design.to_bom(variant=variant)


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
    normalized_components = normalize_bom_components(bom)
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
        "normalized": bom_raw_payload(
            normalized_components,
            source=source,
            variant=variant,
        ),
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

    write_config = getattr(args, "write_config", None)
    if write_config is not None:
        config_path = write_config_template(write_config)
        log.info("Wrote BOM/PnP config template: %s", config_path)
        if not getattr(args, "file", None):
            return 0

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

    config, config_path = load_optional_bom_pnp_config(getattr(args, "config", None))
    config_mode = config_path is not None and getattr(args, "format", None) is None
    variants_to_process = select_variant_names(
        available_variants,
        config,
        cli_variant=getattr(args, "variant", None),
        cli_all_variants=getattr(args, "all_variants", False),
    )
    warn_for_unknown_variants(log, variants_to_process, available_variants)

    output_format = getattr(args, "format", None) or "csv"
    project_parameters = project_parameters_from_design(design)
    output_dir = (
        configured_output_root(args.output)
        if config_mode
        else _resolve_output_dir(args.output, "bom")
    )

    files_written = 0
    for var in variants_to_process:
        bom = _bom_from_configured_source(design, config, variant=var)

        if config_mode:
            written = _configured_bom_artifacts(
                output_dir,
                bom,
                config=config,
                source=input_file,
                variant=var,
                project_parameters=project_parameters,
            )
            files_written += len(written)
            output_names = ", ".join(path.name for path in written)
        else:
            base_name = input_file.stem
            ext = _bom_output_extension(output_format)
            if var:
                output_file = output_dir / f"{base_name}_{var}_bom.{ext}"
            else:
                output_file = output_dir / f"{base_name}_bom.{ext}"

            _write_bom_output(
                output_file,
                bom,
                output_format=output_format,
                source=input_file,
                variant=var,
            )
            files_written += 1
            output_names = output_file.name

        variant_name = var or "base"
        log.info("BOM (%s): %s components -> %s", variant_name, len(bom), output_names)

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
        "CSV/XLSX formats include parameters as columns; JSON preserves nested structure. "
        "Config-driven runs can emit raw JSON, grouped tables, and JLCPCB BOM "
        "upload columns in one invocation.",
        epilog="Examples:\n"
        "  altium-cruncher bom project.PrjPcb\n"
        "  altium-cruncher bom schematic.SchDoc\n"
        "  altium-cruncher bom                               # Auto-detect PrjPcb in CWD\n"
        "  altium-cruncher bom project.PrjPcb --variant V1   # Single variant\n"
        "  altium-cruncher bom project.PrjPcb --all-variants # All variants\n"
        "  altium-cruncher bom project.PrjPcb --format json  # JSON output\n"
        "  altium-cruncher bom project.PrjPcb --format generic-json\n"
        "  altium-cruncher bom project.PrjPcb --format grouped-json\n"
        "  altium-cruncher bom project.PrjPcb --format jlc-csv\n"
        "  altium-cruncher bom project.PrjPcb --format jlc-xlsx\n"
        "  altium-cruncher bom project.PrjPcb --format xlsx  # XLSX output\n"
        "  altium-cruncher bom --write-config bom.config\n"
        "  altium-cruncher bom project.PrjPcb --config bom.config\n"
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
        choices=[
            "csv",
            "json",
            "raw-json",
            "generic-json",
            "legacy-json",
            "grouped-json",
            "grouped-csv",
            "grouped-xlsx",
            "jlc-csv",
            "jlc-xlsx",
            "xlsx",
        ],
        default=None,
        help="single output format; overrides multi-output config mode",
    )
    bom_parser.add_argument(
        "--config",
        type=Path,
        help="BOM/PnP JSON config (default: ./bom.config if present)",
    )
    bom_parser.add_argument(
        "--write-config",
        nargs="?",
        const=Path(BOM_PNP_DEFAULT_CONFIG_NAME),
        type=Path,
        metavar="PATH",
        help="write a default BOM/PnP config template",
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
