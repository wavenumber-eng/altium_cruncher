"""Shared PNP source normalization and artifact writers for CLI workflows."""

from collections.abc import Mapping, Sequence
import csv
import json
import logging
from pathlib import Path


from altium_cruncher.bom_pnp_cli_common import write_used_config_snapshot
from altium_cruncher.bom_pnp_model import BomPnpConfig, JLC_CPL_COLUMNS, NormalizedPlacement, configured_output_file, jlc_cpl_rows, normalize_pnp_entries, pnp_table_rows, pnp_payload, sort_placements
from altium_cruncher.output_path_templates import TemplateValue
from altium_cruncher.simple_xlsx import write_xlsx_table

log = logging.getLogger(__name__)

PNP_CSV_ENCODING = "utf-8-sig"


PNP_FIXED_COLUMNS = [
    "Designator",
    "Comment",
    "Layer",
    "Footprint",
    "Center-X({units})",
    "Center-Y({units})",
    "Rotation",
    "Description",
]


def _write_pnp_csv(
    output_file: Path,
    placements: Sequence[object],
    *,
    units: str,
) -> None:
    """Write normalized PnP rows with parameters flattened into columns."""
    normalized = normalize_pnp_entries(placements, units=units)
    param_columns = sorted(
        {param_name for entry in normalized for param_name in entry.parameters}
    )
    fixed_columns = [column.format(units=units) for column in PNP_FIXED_COLUMNS]

    with open(output_file, "w", newline="", encoding=PNP_CSV_ENCODING) as f:
        writer = csv.writer(f)
        writer.writerow(fixed_columns + param_columns)
        for entry in sort_placements(normalized):
            row = [
                entry.designator,
                entry.comment,
                entry.layer,
                entry.footprint,
                f"{entry.center_x:.4f}",
                f"{entry.center_y:.4f}",
                f"{entry.rotation:.2f}",
                entry.description,
            ]
            row.extend(
                entry.parameters.get(param_name, "") for param_name in param_columns
            )
            writer.writerow(row)


def _write_jlc_cpl_csv(
    output_file: Path,
    placements: Sequence[object],
    *,
    units: str,
) -> None:
    """Write normalized placements in JLCPCB CPL upload format."""
    normalized = normalize_pnp_entries(placements, units=units)
    rows = jlc_cpl_rows(normalized)
    with open(output_file, "w", newline="", encoding=PNP_CSV_ENCODING) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=list(JLC_CPL_COLUMNS),
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows)


def _write_named_rows_csv(
    output_file: Path,
    columns: Sequence[str],
    rows: Sequence[Mapping[str, str]],
) -> None:
    """Write named rows to CSV using a fixed column order."""
    with open(output_file, "w", newline="", encoding=PNP_CSV_ENCODING) as f:
        writer = csv.DictWriter(f, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _pnp_output_extension(output_format: str) -> str:
    """Return the file extension for a PnP output format."""
    if output_format in {"json"}:
        return "json"
    if output_format in {"xlsx", "jlc-cpl-xlsx"}:
        return "xlsx"
    return "csv"


def _write_pnp_xlsx(
    output_file: Path,
    placements: Sequence[object],
    *,
    units: str,
) -> None:
    """Write normalized PnP rows as a single-sheet XLSX workbook."""
    normalized = normalize_pnp_entries(placements, units=units)
    param_columns = sorted(
        {param_name for entry in normalized for param_name in entry.parameters}
    )
    columns = [column.format(units=units) for column in PNP_FIXED_COLUMNS]
    rows = []
    for entry in sort_placements(normalized):
        row: dict[str, str] = {
            columns[0]: entry.designator,
            columns[1]: entry.comment,
            columns[2]: entry.layer,
            columns[3]: entry.footprint,
            columns[4]: f"{entry.center_x:.4f}",
            columns[5]: f"{entry.center_y:.4f}",
            columns[6]: f"{entry.rotation:.2f}",
            columns[7]: entry.description,
        }
        row.update(
            {
                param_name: entry.parameters.get(param_name, "")
                for param_name in param_columns
            }
        )
        rows.append(row)
    write_xlsx_table(
        output_file,
        columns=(*columns, *param_columns),
        rows=rows,
        sheet_name="PnP",
    )


def _configured_pnp_artifacts(
    output_root: Path,
    placements: Sequence[object],
    *,
    config: BomPnpConfig,
    source: Path,
    variant: str | None,
    units: str,
    position_mode: str,
    project_parameters: Mapping[str, TemplateValue],
    output_kinds: Sequence[str] | None = None,
    command: str = "pnp",
) -> list[Path]:
    """Write all configured PnP artifacts and return their paths."""
    kinds = tuple(output_kinds or config.pnp_outputs)
    normalized = normalize_pnp_entries(
        placements,
        units=units,
        aliases=config.field_aliases,
    )
    written: list[Path] = []
    for output_kind in kinds:
        output_file = configured_output_file(
            output_root,
            config,
            source=source,
            command=command,
            output_kind=output_kind,
            extension=_pnp_output_extension(output_kind),
            project_parameters=project_parameters,
            variant_name=variant,
        )
        _write_configured_pnp_artifact(
            output_file,
            output_kind,
            normalized=normalized,
            config=config,
            source=source,
            variant=variant,
            units=units,
            position_mode=position_mode,
        )
        write_used_config_snapshot(output_file, config)
        written.append(output_file)
    return written


def _write_configured_pnp_artifact(
    output_file: Path,
    output_kind: str,
    *,
    normalized: Sequence[NormalizedPlacement],
    config: BomPnpConfig,
    source: Path,
    variant: str | None,
    units: str,
    position_mode: str,
) -> None:
    """Write one configured PnP artifact."""
    if output_kind == "json":
        payload = pnp_payload(
            normalized,
            source=source,
            variant=variant,
            units=units,
            position_mode=position_mode,
            layer_order=config.layer_order,
            prefix_order=config.prefix_order,
        )
        output_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return
    if output_kind == "csv":
        rows = pnp_table_rows(
            normalized,
            fields=config.pnp_output_fields,
            layer_order=config.layer_order,
            prefix_order=config.prefix_order,
        )
        _write_named_rows_csv(output_file, config.pnp_output_fields, rows)
        return
    if output_kind == "xlsx":
        rows = pnp_table_rows(
            normalized,
            fields=config.pnp_output_fields,
            layer_order=config.layer_order,
            prefix_order=config.prefix_order,
        )
        write_xlsx_table(
            output_file,
            columns=config.pnp_output_fields,
            rows=rows,
            sheet_name="PnP",
        )
        return
    if output_kind == "jlc-cpl":
        rows = jlc_cpl_rows(
            normalized,
            layer_order=config.layer_order,
            prefix_order=config.prefix_order,
        )
        _write_named_rows_csv(output_file, JLC_CPL_COLUMNS, rows)
        return
    if output_kind == "jlc-cpl-xlsx":
        rows = jlc_cpl_rows(
            normalized,
            layer_order=config.layer_order,
            prefix_order=config.prefix_order,
        )
        write_xlsx_table(
            output_file,
            columns=JLC_CPL_COLUMNS,
            rows=rows,
            sheet_name="JLC CPL",
        )
        return
    raise ValueError(f"Unsupported configured PnP output: {output_kind}")


def _pnp_format_option_error(output_format: str, units: str) -> str:
    """Return an option error message for incompatible PnP options."""
    if output_format in {"jlc-cpl", "jlc-cpl-xlsx"} and units != "mm":
        return "JLC CPL output requires --units mm because JLCPCB CPL uses mm"
    return ""


def _write_legacy_pnp_output(
    output_dir: Path,
    input_file: Path,
    placements: Sequence[object],
    *,
    output_format: str,
    variant: str | None,
    units: str,
    position_mode: str,
) -> Path:
    """Write one legacy single-format PnP output and return its path."""
    ext = _pnp_output_extension(output_format)
    variant_part = f"_{variant}" if variant else ""
    output_file = output_dir / f"{input_file.stem}{variant_part}_pnp.{ext}"

    if output_format == "json":
        normalized = normalize_pnp_entries(placements, units=units)
        output_data = pnp_payload(
            normalized,
            source=input_file,
            variant=variant,
            units=units,
            position_mode=position_mode,
        )
        output_file.write_text(json.dumps(output_data, indent=2), encoding="utf-8")
        return output_file
    if output_format == "jlc-cpl":
        _write_jlc_cpl_csv(output_file, placements, units=units)
        return output_file
    if output_format == "jlc-cpl-xlsx":
        normalized = normalize_pnp_entries(placements, units=units)
        rows = jlc_cpl_rows(normalized)
        write_xlsx_table(
            output_file,
            columns=JLC_CPL_COLUMNS,
            rows=rows,
            sheet_name="JLC CPL",
        )
        return output_file
    if output_format == "xlsx":
        _write_pnp_xlsx(output_file, placements, units=units)
        return output_file
    _write_pnp_csv(output_file, placements, units=units)
    return output_file
