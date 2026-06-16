"""Config contract signoff tests for public CLI commands."""

from __future__ import annotations

from collections.abc import Iterator
from html.parser import HTMLParser
import json
from pathlib import Path
from typing import Any

import jsonc  # type: ignore[import-untyped]
from jsonschema import Draft202012Validator, validators

from altium_cruncher.altium_clean import AltiumCleanConfig
from altium_cruncher.altium_cruncher_cmd_clean import (
    _PCBLIB_CLEAN_COMMENTS,
    _SCHEMATIC_CLEAN_COMMENTS,
    _render_jsonc_template,
)
from altium_cruncher.altium_cruncher_mate_templates import mate_template_text
from altium_cruncher.altium_cruncher_mco import _mco_template_text
from altium_cruncher.altium_cruncher_pcb_layer_step_config import (
    pcb_layer_step_default_config_text,
)
from altium_cruncher.altium_cruncher_pcb_svg_config import (
    PcbSvgConfig,
    pcb_svg_config_text,
)
from altium_cruncher.altium_pcblib_clean import PcbLibCleanConfig
from altium_cruncher.bom_pnp_model import bom_pnp_config_text


def _project_root() -> Path:
    """Find the repository root from this test file."""
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Could not locate repository root")


PACKAGE_ROOT = _project_root()
CONTRACTS_ROOT = PACKAGE_ROOT / "docs" / "contracts"
DESIGN_ROOT = PACKAGE_ROOT / "docs" / "design"
CLI_DESIGN_ROOT = DESIGN_ROOT / "cli"
COMMAND_MANIFEST = CONTRACTS_ROOT / "command_manifest.v0.json"


class _DataAttrParser(HTMLParser):
    """Collect HTML elements carrying data attributes."""

    def __init__(self) -> None:
        super().__init__()
        self.elements: list[tuple[str, dict[str, str]]] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        data = {key: value or "" for key, value in attrs if key.startswith("data-")}
        if data:
            self.elements.append((tag, data))


def _manifest_commands() -> list[str]:
    payload = json.loads(COMMAND_MANIFEST.read_text(encoding="utf-8"))
    assert payload["schema"] == "altium_cruncher.command_manifest.v0"
    commands = payload["commands"]
    assert isinstance(commands, list)
    return [str(command["name"]) for command in commands]


def _data_elements(path: Path) -> list[tuple[str, dict[str, str]]]:
    parser = _DataAttrParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.elements


def _cli_index_contracts() -> dict[str, str]:
    rows: dict[str, str] = {}
    for tag, attrs in _data_elements(CLI_DESIGN_ROOT / "index.html"):
        if tag == "tr" and "data-command" in attrs:
            rows[attrs["data-command"]] = attrs.get("data-config-contract", "")
    return rows


def _cli_doc_body_attrs(command: str) -> dict[str, str]:
    doc_path = CLI_DESIGN_ROOT / f"{command}.html"
    for tag, attrs in _data_elements(doc_path):
        if tag == "body":
            return attrs
    raise AssertionError(f"{doc_path}: missing body element with data attributes")


def _schema_paths() -> Iterator[Path]:
    yield from sorted(CONTRACTS_ROOT.glob("*.schema.json"))


def _schema_validator(schema_name: str) -> Draft202012Validator:
    schema = json.loads((CONTRACTS_ROOT / schema_name).read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def _validation_failures(
    case_name: str,
    validator: Draft202012Validator,
    payload: Any,
) -> list[str]:
    failures: list[str] = []
    for error in sorted(validator.iter_errors(payload), key=str):
        path = ".".join(str(part) for part in error.absolute_path) or "<root>"
        failures.append(f"{case_name}: {path}: {error.message}")
    return failures


def _config_cases() -> list[tuple[str, str, Any]]:
    return [
        (
            "bom/pnp generated default",
            "bom_pnp_config.v1.schema.json",
            jsonc.loads(bom_pnp_config_text()),
        ),
        (
            "pcb-svg generated default",
            "pcb_svg_config.a0.schema.json",
            jsonc.loads(pcb_svg_config_text(PcbSvgConfig.default())),
        ),
        (
            "pcb-layer-step generated template",
            "pcb_layer_step_config.v2.schema.json",
            jsonc.loads(pcb_layer_step_default_config_text()),
        ),
        (
            "mate generated template",
            "mate_config.a0.schema.json",
            jsonc.loads(mate_template_text(schema="wn.pcb_cruncher.mate_config.a0")),
        ),
        (
            "schematic clean generated template",
            "clean_config.v1.schema.json",
            AltiumCleanConfig.template().to_dict(),
        ),
        (
            "PcbLib clean generated template",
            "clean_config.v1.schema.json",
            PcbLibCleanConfig.template().to_dict(),
        ),
    ]


def _generated_template_comment_cases() -> list[tuple[str, str, list[str]]]:
    return [
        (
            "bom/pnp",
            bom_pnp_config_text(),
            [
                "/* Variant mode. Options: all, base, named. */",
                "/* BOM source mode. Options: merged, pcb, schematic. */",
                "/* Output coordinate units. Options: mils, mm. */",
            ],
        ),
        (
            "pcb-svg",
            pcb_svg_config_text(PcbSvgConfig.default()),
            [
                "/* Canvas bounds mode. Options: all_geometry, board_outline. */",
                "/* Projection mode for fitted components. Options: bounding_box, detail, none, outline, simple. */",
                "/* HLR curve serialization mode. Options: native_arcs, polyline. */",
            ],
        ),
        (
            "pcb-layer-step",
            pcb_layer_step_default_config_text(),
            [
                "/* Global drill mode. Options: auto, cut, overlay, none. */",
                "/* Overlay shape. Options: solid, ring. */",
                "/* Component pad mode. Options: none, all, matching_designators. */",
            ],
        ),
        (
            "mate",
            mate_template_text(schema="wn.pcb_cruncher.mate_config.a0"),
            [
                (
                    "/* Project loading mode. auto/schematic loads source SchDocs "
                    "for power-port detection. Options: auto, none, schematic. */"
                ),
                "/* Source object kind. Options: component, free_pad. */",
                "/* Free-pad hole-size filter in mils. */",
                "/* Free-pad plating filter. */",
                "/* Reference graphics shape mode. Options: source_pad_outline, destination_pad_outline. */",
                "/* Board-cutout projection filter. Options: all, interior. */",
                "/* Create actual board cutouts when true; otherwise graphics only. */",
                "/* Overlay shape. Options: solid, ring. */",
            ],
        ),
        (
            "schematic clean",
            _render_jsonc_template(
                AltiumCleanConfig.template().to_dict(),
                _SCHEMATIC_CLEAN_COMMENTS,
            ),
            [
                "/* Outline width. Options: smallest/zero, small, medium, large, or enum integer. */",
                "/* Marker style. Options: cross, thin cross, small cross, checkbox, triangle, or enum integer. */",
            ],
        ),
        (
            "PcbLib clean",
            _render_jsonc_template(
                PcbLibCleanConfig.template().to_dict(),
                _PCBLIB_CLEAN_COMMENTS,
            ),
            [
                "/* Human-readable rule profile name written to clean reports. */",
                "/* Options: raw, default. */",
                "/* Text matching mode. Options: all, regex, contains, exact. */",
            ],
        ),
        (
            "mco",
            _mco_template_text(),
            [
                "/* MCO operation name. Options: */",
                "project.create",
                "/* Schematic sheet style. Options: Altium SheetStyle enum name or native enum id. */",
            ],
        ),
    ]


def test_cli_config_contract_links_are_release_ready() -> None:
    """Every public CLI design doc must resolve its declared config contract."""
    index_contracts = _cli_index_contracts()
    failures: list[str] = []

    for command in _manifest_commands():
        index_contract = index_contracts.get(command)
        body_attrs = _cli_doc_body_attrs(command)
        doc_contract = body_attrs.get("data-config-contract", "")
        if not index_contract:
            failures.append(f"{command}: missing CLI index config contract")
            continue
        if index_contract != doc_contract:
            failures.append(
                f"{command}: CLI index contract {index_contract!r} does not "
                f"match design doc contract {doc_contract!r}"
            )

        if doc_contract == "pending":
            failures.append(f"{command}: config contract is still pending")
            continue
        if doc_contract == "none":
            continue
        if not doc_contract.startswith("docs/contracts/"):
            failures.append(
                f"{command}: config contract must live under docs/contracts"
            )
            continue
        if not doc_contract.endswith(".schema.json"):
            failures.append(f"{command}: config contract is not a JSON schema")
            continue
        contract_path = PACKAGE_ROOT / doc_contract
        if not contract_path.exists():
            failures.append(f"{command}: missing config contract {doc_contract}")

    pending_docs = [
        path.relative_to(PACKAGE_ROOT).as_posix()
        for path in DESIGN_ROOT.rglob("*.html")
        if 'data-config-contract="pending"' in path.read_text(encoding="utf-8")
    ]
    failures.extend(
        f"{path}: contains pending config contract" for path in pending_docs
    )

    assert failures == [], "Config contract link signoff gaps:\n" + "\n".join(failures)


def test_config_contract_schemas_are_valid_json_schema() -> None:
    """All checked-in config schemas must be valid Draft 2020-12 schemas."""
    failures: list[str] = []

    for path in _schema_paths():
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
            validator_class = validators.validator_for(schema)
            validator_class.check_schema(schema)
        except Exception as exc:  # pragma: no cover - failure path is diagnostic
            rel_path = path.relative_to(PACKAGE_ROOT).as_posix()
            failures.append(f"{rel_path}: {exc}")

    assert failures == [], "Invalid config schemas:\n" + "\n".join(failures)


def test_generated_config_defaults_validate_against_contracts() -> None:
    """Generated public config templates must conform to their schemas."""
    validators_by_schema: dict[str, Draft202012Validator] = {}
    failures: list[str] = []

    for case_name, schema_name, payload in _config_cases():
        validator = validators_by_schema.setdefault(
            schema_name,
            _schema_validator(schema_name),
        )
        failures.extend(_validation_failures(case_name, validator, payload))

    assert failures == [], "Generated config contract drift:\n" + "\n".join(failures)


def test_generated_editable_configs_document_enum_options() -> None:
    """Generated editable JSONC configs must list options for string/enum fields."""
    failures: list[str] = []

    for case_name, text, expected_comments in _generated_template_comment_cases():
        jsonc.loads(text)
        if "Options:" not in text:
            failures.append(f"{case_name}: no Options comments found")
        for expected in expected_comments:
            if expected not in text:
                failures.append(f"{case_name}: missing {expected}")

    assert failures == [], "Generated JSONC comment policy drift:\n" + "\n".join(
        failures
    )
