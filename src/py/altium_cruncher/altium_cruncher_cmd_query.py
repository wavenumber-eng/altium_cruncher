"""Query Altium design data as compact JSON for scripts and agents."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from altium_cruncher.altium_cruncher_common import find_prjpcbs_in_cwd

if TYPE_CHECKING:
    from altium_monkey.altium_design import AltiumDesign

QUERY_SUMMARY_SCHEMA = "altium_cruncher.query.summary.a0"
QUERY_COMPONENTS_SCHEMA = "altium_cruncher.query.components.a0"
QUERY_NETS_SCHEMA = "altium_cruncher.query.nets.a0"
QUERY_NET_DETAIL_SCHEMA = "altium_cruncher.query.net_detail.a0"
QUERY_CONNECTIONS_SCHEMA = "altium_cruncher.query.connections.a0"
QUERY_SHEET_SCHEMA = "altium_cruncher.query.sheet.a0"


class QueryCommandError(ValueError):
    """Raised when the query command cannot resolve user input."""


def cmd_query(args: argparse.Namespace) -> int:
    """Dispatch query subcommands and print one JSON payload to stdout."""
    action = getattr(args, "query_action", None)
    if action is None:
        _print_query_error("query requires a subcommand; see `query --help`")
        return 1
    _route_logging_to_stderr()
    try:
        payload = _QUERY_ACTIONS[action](args)
    except Exception as exc:
        _print_query_error(f"query {action} failed: {exc}")
        return 1
    print(json.dumps(payload, indent=2, default=str))
    return 0


def _query_summary(args: argparse.Namespace) -> dict[str, object]:
    """Build the project summary payload."""
    project_path = _resolve_project_path(args)
    design = _load_design(project_path)
    design_json = design.to_json()
    netlist_json = design.to_netlist().to_json()
    return {
        "schema": QUERY_SUMMARY_SCHEMA,
        "project_file": project_path.name,
        "current_variant": _current_variant(design),
        "variants": design.get_variants(),
        "sheets": _sheet_rows(design_json),
        "component_count": len(design_json.get("components", [])),
        "net_count": len(netlist_json.get("nets", [])),
        "component_type_counts": _component_type_counts(design_json),
        "power_and_ground_nets": _power_and_ground_nets(netlist_json),
        "pcb_documents": [path.name for path in design.get_pcbdoc_paths()],
    }


def _query_components(args: argparse.Namespace) -> dict[str, object]:
    """Build the filtered component list payload."""
    design = _load_design(_resolve_project_path(args))
    components = list(design.to_json().get("components", []))
    components = _filter_components(components, args)
    if not args.full:
        components = [_brief_component(component) for component in components]
    return {
        "schema": QUERY_COMPONENTS_SCHEMA,
        "count": len(components),
        "components": components,
    }


def _query_nets(args: argparse.Namespace) -> dict[str, object]:
    """Build the net list payload, or one net's full terminal detail."""
    design = _load_design(_resolve_project_path(args))
    nets = list(design.to_netlist().to_json().get("nets", []))
    if args.name:
        return _net_detail(nets, args.name)
    if args.contains:
        needle = args.contains.upper()
        nets = [net for net in nets if needle in str(net.get("name") or "").upper()]
    return {
        "schema": QUERY_NETS_SCHEMA,
        "count": len(nets),
        "nets": [_brief_net(net) for net in nets],
    }


def _query_connections(args: argparse.Namespace) -> dict[str, object]:
    """Build the per-pin connectivity payload for one designator."""
    design = _load_design(_resolve_project_path(args))
    design_json = design.to_json()
    netlist_json = design.to_netlist().to_json()

    comp_to_nets = design_json.get("indexes", {}).get("component_to_nets", {})
    if args.designator not in comp_to_nets:
        sample = ", ".join(sorted(comp_to_nets)[:30])
        raise QueryCommandError(
            f"designator {args.designator!r} not found; sample designators: {sample}"
        )

    component = _component_by_designator(design_json, args.designator)
    pins = _pin_connection_rows(
        netlist_json,
        net_names=comp_to_nets[args.designator],
        designator=args.designator,
        pin=args.pin,
    )
    if args.pin and not pins:
        raise QueryCommandError(f"pin {args.pin!r} not found on {args.designator}")
    return {
        "schema": QUERY_CONNECTIONS_SCHEMA,
        "designator": args.designator,
        "value": component.get("value") if component else None,
        "footprint": component.get("footprint") if component else None,
        "type": _component_type(component) if component else None,
        "sheet": _component_sheet(component) if component else None,
        "pin_count": len(pins),
        "pins": pins,
    }


def _query_sheet(args: argparse.Namespace) -> dict[str, object]:
    """Build the single-SchDoc inspection payload."""
    from altium_monkey.altium_schdoc import AltiumSchDoc

    schdoc_path = Path(args.schdoc_file)
    if not schdoc_path.is_file():
        raise FileNotFoundError(f"SchDoc not found: {schdoc_path}")
    if schdoc_path.suffix.lower() != ".schdoc":
        raise QueryCommandError(f"expected a .SchDoc file, got: {schdoc_path.name}")
    schdoc = AltiumSchDoc(str(schdoc_path))

    components = [_sheet_component_row(component) for component in schdoc.components]
    net_labels = _unique_attr_texts(schdoc.net_labels, "text")
    ports = _unique_attr_texts(schdoc.ports, "name")
    sheet_symbols = [_sheet_symbol_row(symbol) for symbol in schdoc.sheet_symbols]
    return {
        "schema": QUERY_SHEET_SCHEMA,
        "filename": schdoc_path.name,
        "component_count": len(components),
        "components": components,
        "net_label_count": len(net_labels),
        "net_labels": net_labels,
        "port_count": len(ports),
        "ports": ports,
        "sheet_symbol_count": len(sheet_symbols),
        "sheet_symbols": sheet_symbols,
    }


_QUERY_ACTIONS = {
    "summary": _query_summary,
    "components": _query_components,
    "nets": _query_nets,
    "connections": _query_connections,
    "sheet": _query_sheet,
}


def _load_design(project_path: Path) -> "AltiumDesign":
    """Load an AltiumDesign from a resolved .PrjPcb path."""
    from altium_monkey.altium_design import AltiumDesign

    return AltiumDesign.from_prjpcb(project_path)


def _resolve_project_path(args: argparse.Namespace) -> Path:
    """Resolve the target project from positional, --project, or CWD scan."""
    positional = getattr(args, "project_file", None)
    explicit = getattr(args, "project", None)
    if positional is not None and explicit is not None:
        raise QueryCommandError("pass either a project path or --project, not both")
    selected = explicit if explicit is not None else positional
    if selected is not None:
        return _validate_project_path(Path(selected))
    projects = [project.resolve() for project in find_prjpcbs_in_cwd()]
    if len(projects) == 1:
        return projects[0]
    if not projects:
        raise QueryCommandError(
            "No .PrjPcb file found in the current directory; pass a project explicitly."
        )
    project_list = "\n".join(f"  {project.name}" for project in projects)
    raise QueryCommandError(
        "Multiple .PrjPcb files found in the current directory; pass one explicitly "
        f"or use --project:\n{project_list}"
    )


def _validate_project_path(path: Path) -> Path:
    """Validate that a user-supplied project path is an existing .PrjPcb."""
    project = path.resolve()
    if project.suffix.lower() != ".prjpcb":
        raise QueryCommandError(f"Expected a .PrjPcb project, got: {project}")
    if not project.is_file():
        raise FileNotFoundError(f"Project not found: {project}")
    return project


def _current_variant(design: "AltiumDesign") -> str | None:
    """Return the project's current variant name when available."""
    project = getattr(design, "project", None)
    if project is None:
        return None
    return project.get_current_variant()


def _sheet_rows(design_json: dict[str, object]) -> list[dict[str, object]]:
    """Return sheet filename/title rows with top-level markers."""
    hierarchy_docs = design_json.get("schematic_hierarchy", {}).get("documents", [])
    top_level_by_filename = {
        doc.get("filename"): doc.get("is_top_level") for doc in hierarchy_docs
    }
    return [
        {
            "filename": sheet.get("filename"),
            "title": sheet.get("title"),
            "is_top_level": top_level_by_filename.get(sheet.get("filename")),
        }
        for sheet in design_json.get("sheets", [])
    ]


def _component_type_counts(design_json: dict[str, object]) -> dict[str, int]:
    """Return component counts grouped by classification type."""
    counts: dict[str, int] = {}
    for component in design_json.get("components", []):
        kind = _component_type(component) or "unknown"
        counts[kind] = counts.get(kind, 0) + 1
    return dict(sorted(counts.items()))


def _power_and_ground_nets(netlist_json: dict[str, object]) -> list[str]:
    """Return named nets that look like power or ground rails.

    Heuristic: a named, non-auto-named net counts when any terminal pin is
    POWER-typed or the net name contains GND or VSS.
    """
    names = {
        str(net["name"])
        for net in netlist_json.get("nets", [])
        if net.get("name")
        and not net.get("auto_named")
        and (
            any(
                terminal.get("pin_type") == "POWER"
                for terminal in net.get("terminals", [])
            )
            or any(token in str(net["name"]).upper() for token in ("GND", "VSS"))
        )
    }
    return sorted(names)


def _filter_components(
    components: list[dict[str, object]],
    args: argparse.Namespace,
) -> list[dict[str, object]]:
    """Apply designator, sheet, type, and value filters to component rows."""
    return [
        component
        for component in components
        if _component_matches_filters(component, args)
    ]


def _component_matches_filters(
    component: dict[str, object],
    args: argparse.Namespace,
) -> bool:
    """Return whether one component row passes every requested filter."""
    if args.designator and component.get("designator") != args.designator:
        return False
    if args.sheet and not _component_sheet_matches(component, args.sheet):
        return False
    if args.type and (_component_type(component) or "").lower() != args.type.lower():
        return False
    if args.value_contains:
        needle = args.value_contains.lower()
        return needle in str(component.get("value") or "").lower()
    return True


def _component_sheet_matches(component: dict[str, object], sheet: str) -> bool:
    """Match a sheet filter against the full hierarchy path or bare filename."""
    wanted = sheet.lower()
    owning_sheet = _component_sheet(component)
    return owning_sheet.lower() == wanted or Path(owning_sheet).name.lower() == wanted


def _brief_component(component: dict[str, object]) -> dict[str, object]:
    """Reduce one component row to agent-friendly summary fields."""
    classification = component.get("classification", {})
    return {
        "designator": component.get("designator"),
        "value": component.get("value"),
        "footprint": component.get("footprint"),
        "type": classification.get("type"),
        "sheet": _component_sheet(component),
        "pin_count": classification.get("pin_count"),
    }


def _component_type(component: dict[str, object]) -> str | None:
    """Return the classification type for one component row."""
    kind = component.get("classification", {}).get("type")
    return str(kind) if kind else None


def _component_sheet(component: dict[str, object]) -> str:
    """Return the owning sheet filename for one component row."""
    return str(component.get("hierarchy", {}).get("sheet", "") or "")


def _component_by_designator(
    design_json: dict[str, object],
    designator: str,
) -> dict[str, object] | None:
    """Return the component row matching a designator, if present."""
    for component in design_json.get("components", []):
        if component.get("designator") == designator:
            return component
    return None


def _net_detail(nets: list[dict[str, object]], name: str) -> dict[str, object]:
    """Return the full terminal detail payload for one named net."""
    target = name.upper()
    matches = [net for net in nets if str(net.get("name") or "").upper() == target]
    if not matches:
        raise QueryCommandError(f"no net named: {name}")
    net = matches[0]
    return {
        "schema": QUERY_NET_DETAIL_SCHEMA,
        "name": net.get("name"),
        "auto_named": net.get("auto_named"),
        "source_sheets": net.get("source_sheets"),
        "terminal_count": len(net.get("terminals", [])),
        "terminals": net.get("terminals", []),
    }


def _brief_net(net: dict[str, object]) -> dict[str, object]:
    """Reduce one net row to name, terminal count, and source sheets."""
    return {
        "name": net.get("name"),
        "auto_named": net.get("auto_named"),
        "terminal_count": len(net.get("terminals", [])),
        "source_sheets": net.get("source_sheets"),
    }


def _pin_connection_rows(
    netlist_json: dict[str, object],
    *,
    net_names: list[str],
    designator: str,
    pin: str | None,
) -> list[dict[str, object]]:
    """Return per-pin rows describing what one designator connects to."""
    nets_by_name = {net.get("name"): net for net in netlist_json.get("nets", [])}
    rows: list[dict[str, object]] = []
    for net_name in net_names:
        net = nets_by_name.get(net_name)
        if not net:
            continue
        terminals = list(net.get("terminals", []))
        own = [t for t in terminals if t.get("designator") == designator]
        others = [t for t in terminals if t.get("designator") != designator]
        for terminal in own:
            if pin is not None and str(terminal.get("pin")) != str(pin):
                continue
            rows.append(
                {
                    "pin": terminal.get("pin"),
                    "pin_name": terminal.get("pin_name"),
                    "pin_type": terminal.get("pin_type"),
                    "net": net_name,
                    "connected_to": [_terminal_row(other) for other in others],
                }
            )
    return rows


def _terminal_row(terminal: dict[str, object]) -> dict[str, object]:
    """Reduce one netlist terminal to designator/pin identification fields."""
    return {
        "designator": terminal.get("designator"),
        "pin": terminal.get("pin"),
        "pin_name": terminal.get("pin_name"),
        "pin_type": terminal.get("pin_type"),
    }


def _sheet_component_row(component: object) -> dict[str, object]:
    """Return library reference and value fields for one SchDoc component."""
    parameters: dict[str, str] = {}
    for parameter in getattr(component, "parameters", []) or []:
        name = getattr(parameter, "name", None)
        text = getattr(parameter, "text", None)
        if name and text not in (None, ""):
            parameters[str(name)] = str(text)
    return {
        "lib_reference": getattr(component, "lib_reference", None),
        "design_item_id": getattr(component, "design_item_id", None),
        "description": getattr(component, "component_description", None),
        "value": parameters.get("Value") or parameters.get("Comment"),
        "manufacturer_part": parameters.get("MP"),
    }


def _sheet_symbol_row(symbol: object) -> dict[str, object]:
    """Return filename and sheet-name fields for one sheet symbol."""
    filename = getattr(symbol, "file_name", None)
    sheet_name = getattr(symbol, "sheet_name", None)
    return {
        "filename": str(getattr(filename, "text", filename) or "") or None,
        "sheet_name": str(getattr(sheet_name, "text", sheet_name) or "") or None,
    }


def _unique_attr_texts(items: object, attribute: str) -> list[str]:
    """Return sorted unique non-empty attribute strings from parsed records."""
    return sorted(
        {
            str(value)
            for item in items or []
            if (value := getattr(item, attribute, None))
        }
    )


def _route_logging_to_stderr() -> None:
    """Move stdout log handlers to stderr so stdout stays parseable JSON."""
    for handler in logging.getLogger().handlers:
        if isinstance(handler, logging.StreamHandler) and handler.stream is sys.stdout:
            handler.setStream(sys.stderr)


def _print_query_error(message: str) -> None:
    """Print one query command error message to stderr."""
    print(message, file=sys.stderr)


def register_parser(
    subparsers: argparse._SubParsersAction,
) -> argparse.ArgumentParser:
    """Register the query command parser."""
    parser = subparsers.add_parser(
        "query",
        help="query design data as compact JSON for scripts and agents",
        description=(
            "Query Altium design data and print compact JSON to stdout. "
            "Subcommands return the smallest payload that answers a typical "
            "design question: project summary, filtered component lists, net "
            "lists, per-pin connectivity, and single-sheet inspection. "
            "When no project is passed, project subcommands auto-detect "
            "exactly one .PrjPcb in the current directory."
        ),
        epilog=(
            "Examples:\n"
            "  altium-cruncher query summary project.PrjPcb\n"
            "  altium-cruncher query components --sheet Codec.SchDoc --type ic\n"
            "  altium-cruncher query nets --contains P5V\n"
            "  altium-cruncher query nets --name SDA\n"
            "  altium-cruncher query connections U7 --pin C9\n"
            "  altium-cruncher query sheet Codec.SchDoc"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    action_subparsers = parser.add_subparsers(
        dest="query_action",
        metavar="<query-action>",
    )

    summary_parser = action_subparsers.add_parser(
        "summary",
        help="project overview: sheets, counts, variants, power nets",
    )
    _add_project_arguments(summary_parser)

    components_parser = action_subparsers.add_parser(
        "components",
        help="list and filter project components",
    )
    components_parser.add_argument(
        "--designator",
        help="exact designator match",
    )
    components_parser.add_argument(
        "--sheet",
        help="filter by owning sheet filename",
    )
    components_parser.add_argument(
        "--type",
        help="filter by classification type: ic, resistor, capacitor, connector, ...",
    )
    components_parser.add_argument(
        "--value-contains",
        help="case-insensitive substring match on component value",
    )
    components_parser.add_argument(
        "--full",
        action="store_true",
        help="include full component rows instead of brief summary fields",
    )
    _add_project_arguments(components_parser)

    nets_parser = action_subparsers.add_parser(
        "nets",
        help="list nets, or fetch one net's full terminal detail",
    )
    nets_parser.add_argument(
        "--name",
        help="exact net name (case-insensitive) for full terminal detail",
    )
    nets_parser.add_argument(
        "--contains",
        help="case-insensitive substring match on net names",
    )
    _add_project_arguments(nets_parser)

    connections_parser = action_subparsers.add_parser(
        "connections",
        help="per-pin connectivity for one designator",
    )
    connections_parser.add_argument(
        "designator",
        help="component designator, for example U7",
    )
    connections_parser.add_argument(
        "--pin",
        help="restrict output to one pin identifier, for example C9 or 1",
    )
    _add_project_arguments(connections_parser)

    sheet_parser = action_subparsers.add_parser(
        "sheet",
        help="inspect a single .SchDoc without a project",
    )
    sheet_parser.add_argument(
        "schdoc_file",
        type=Path,
        help="SchDoc file to inspect",
    )
    sheet_parser.set_defaults(handler=cmd_query)

    parser.set_defaults(handler=cmd_query)
    return parser


def _add_project_arguments(parser: argparse.ArgumentParser) -> None:
    """Add the shared optional project positional and --project option."""
    parser.add_argument(
        "project_file",
        nargs="?",
        type=Path,
        help="PrjPcb file (optional if exactly one PrjPcb in CWD)",
    )
    parser.add_argument(
        "--project",
        type=Path,
        help="explicit .PrjPcb project path",
    )
    parser.set_defaults(handler=cmd_query)
