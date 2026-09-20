"""Generated from src/tsp/altium_cruncher/outputs/toon-warning-report.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

ToonWarningReport = TypedDict("ToonWarningReport", {
    "schema": "Literal[\"toon.warning_report.a0\"]",
    "summary": "ToonWarningSummary",
    "diagnostics": "list[ToonWarningDiagnostic]",
}, closed=True)

ToonWarningSummary = TypedDict("ToonWarningSummary", {
    "unique_diagnostic_count": "int",
    "occurrence_count": "int",
    "groups": "list[ToonWarningSummaryGroup]",
}, closed=True)

ToonWarningDiagnostic = TypedDict("ToonWarningDiagnostic", {
    "key": "str",
    "code": "str",
    "severity": "Literal[\"warning\"]",
    "category": "Literal[\"missing_model\"] | Literal[\"unsupported_model\"] | Literal[\"invalid_model_geometry\"] | Literal[\"geometer_geometry\"] | Literal[\"region_resolution\"] | Literal[\"rotation_resolution\"] | Literal[\"clipping\"]",
    "producer": "str",
    "message": "str",
    "occurrence_count": "int",
    "input": NotRequired["str"],
    "board": NotRequired["str"],
    "variant": NotRequired["str"],
    "view": NotRequired["str"],
    "component_designator": NotRequired["str"],
    "body_index": NotRequired["int"],
    "model_identity": NotRequired["str"],
    "detail": NotRequired["RecordUnknown"],
}, closed=True)

ToonWarningSummaryGroup = TypedDict("ToonWarningSummaryGroup", {
    "category": "Literal[\"missing_model\"] | Literal[\"unsupported_model\"] | Literal[\"invalid_model_geometry\"] | Literal[\"geometer_geometry\"] | Literal[\"region_resolution\"] | Literal[\"rotation_resolution\"] | Literal[\"clipping\"]",
    "code": "str",
    "unique_diagnostic_count": "int",
    "occurrence_count": "int",
    "affected_component_count": "int",
    "affected_body_count": "int",
    "affected_model_count": "int",
    "sample_designators": "list[str]",
}, closed=True)

RecordUnknown = dict[str, object]
