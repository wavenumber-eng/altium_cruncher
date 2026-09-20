"""Structured diagnostics shared by the PCB illustration pipeline."""

from __future__ import annotations

from concurrent.futures import Future, as_completed
from dataclasses import asdict, dataclass
import json
import logging
from pathlib import Path
from typing import TypedDict

from altium_monkey.altium_pcb_component import AltiumPcbComponent
from altium_monkey.altium_record_pcb__component_body import AltiumPcbComponentBody
import geometer as g


log = logging.getLogger(__name__)


@dataclass(frozen=True)
class IllustrationDiagnostic:
    """Structured nonfatal condition produced while preparing component geometry."""

    code: str
    category: str
    producer: str
    message: str
    component_designator: str | None = None
    body_index: int | None = None
    model_identity: str | None = None
    detail: dict[str, object] | None = None

    def metadata(self) -> dict[str, object]:
        return {
            name: value
            for name, value in asdict(self).items()
            if name != "message" and value is not None
        }


class DiagnosticMetadata(TypedDict, total=False):
    code: str
    category: str
    producer: str
    component_designator: str | None
    body_index: int | None
    model_identity: str | None
    detail: dict[str, object] | None


type WarningEvents = list[tuple[bool, str, DiagnosticMetadata]]


def unavailable_step_reason(name: str) -> str:
    extension = Path(name.strip().strip("\x00")).suffix.lower()
    formats = {
        ".x_t": "Parasolid text",
        ".x_b": "Parasolid binary",
        ".sldprt": "SolidWorks part",
        ".sldasm": "SolidWorks assembly",
    }
    if extension and extension not in {".step", ".stp"}:
        return (
            f"unsupported model format {formats.get(extension, 'unknown')} ({extension}); "
            "Toon supports embedded STEP (.step/.stp), Altium extruded bodies, "
            "and Altium cylinder bodies"
        )
    return "embedded STEP unavailable or unreadable"


def body_model_label(body: AltiumPcbComponentBody) -> str:
    labels = {0: "extruded body", 2: "cylinder body", 3: "sphere body"}
    fallback = labels.get(body.model_type, "unnamed model")
    return str(body.properties.get("MODEL.NAME") or fallback)


def body_failure_classification(
    body: AltiumPcbComponentBody,
) -> tuple[str, str]:
    """Classify from authored fields, never by parsing a native error message."""

    if body.model_type not in {0, 1, 2, 3}:
        return "unsupported_model", "unsupported-body-type"
    if body.model_type == 1:
        extension = Path(body_model_label(body).strip().strip("\x00")).suffix.lower()
        if extension and extension not in {".step", ".stp"}:
            return "unsupported_model", "unsupported-model-format"
        return "invalid_model_geometry", "step-unavailable-or-unreadable"
    return "invalid_model_geometry", "invalid-authored-body"


def report_step_completions(
    futures: dict[
        Future[g.ModelTessellation], tuple[str, AltiumPcbComponent | None, int]
    ],
    side: str,
) -> None:
    # Observe completion without raising task errors here; source-order
    # consumption still supplies body-specific warnings/errors.
    for completed, future in enumerate(as_completed(futures), 1):
        name, component, index = futures[future]
        owner = component.designator if component is not None else f"free-body-{index}"
        failed = future.cancelled() or future.exception() is not None
        log.info(
            "%s %s STEP model %d/%d: %s (%s)",
            "Failed" if failed else "Completed",
            side,
            completed,
            len(futures),
            name,
            owner,
        )


def geometer_failure_message(
    error: g.GeometerOperationError | g.GeometerError,
) -> str:
    if isinstance(error, g.GeometerOperationError):
        details = "; ".join(f"{d.code}: {d.message}" for d in error.diagnostics)
        return f"{error.operation}: {details}" if details else str(error)
    return str(error)


class IllustrationDiagnosticsMixin:
    """Collect illustration diagnostics while retaining legacy warning strings."""

    _warning_capture: WarningEvents | None
    _suppress_collection_warnings: bool
    _diagnostic_identities: set[tuple[object, ...]]
    emit_warnings: bool
    warnings: list[str]
    diagnostics: list[IllustrationDiagnostic]

    def _initialize_diagnostics(self, emit_warnings: bool) -> None:
        self.emit_warnings = emit_warnings
        self.warnings: list[str] = []
        self.diagnostics: list[IllustrationDiagnostic] = []
        self._diagnostic_identities: set[tuple[object, ...]] = set()

    def warn(
        self,
        message: str,
        *,
        code: str = "illustration-warning",
        category: str = "invalid_model_geometry",
        producer: str = "altium-cruncher",
        component_designator: str | None = None,
        body_index: int | None = None,
        model_identity: str | None = None,
        detail: dict[str, object] | None = None,
    ) -> None:
        metadata = DiagnosticMetadata(
            code=code,
            category=category,
            producer=producer,
            component_designator=component_designator,
            body_index=body_index,
            model_identity=model_identity,
            detail=detail,
        )
        if self._warning_capture is not None:
            self._warning_capture.append((True, message, metadata))
        if self._suppress_collection_warnings:
            return
        self._record_diagnostic(message, metadata)
        if message not in self.warnings:
            self.warnings.append(message)
            if self.emit_warnings:
                log.warning(message)

    def _append_warning(
        self,
        message: str,
        *,
        code: str = "illustration-warning",
        category: str = "invalid_model_geometry",
        producer: str = "altium-cruncher",
        component_designator: str | None = None,
        body_index: int | None = None,
        model_identity: str | None = None,
        detail: dict[str, object] | None = None,
    ) -> None:
        metadata = DiagnosticMetadata(
            code=code,
            category=category,
            producer=producer,
            component_designator=component_designator,
            body_index=body_index,
            model_identity=model_identity,
            detail=detail,
        )
        if self._warning_capture is not None:
            self._warning_capture.append((False, message, metadata))
        if not self._suppress_collection_warnings:
            self._record_diagnostic(message, metadata)
            self.warnings.append(message)

    def _record_diagnostic(self, message: str, metadata: DiagnosticMetadata) -> None:
        diagnostic = IllustrationDiagnostic(
            code=metadata.get("code", "illustration-warning"),
            category=metadata.get("category", "invalid_model_geometry"),
            producer=metadata.get("producer", "altium-cruncher"),
            message=message,
            component_designator=metadata.get("component_designator"),
            body_index=metadata.get("body_index"),
            model_identity=metadata.get("model_identity"),
            detail=metadata.get("detail"),
        )
        identity = (
            diagnostic.code,
            diagnostic.category,
            diagnostic.producer,
            diagnostic.component_designator,
            diagnostic.body_index,
            diagnostic.model_identity,
            json.dumps(diagnostic.detail, sort_keys=True) if diagnostic.detail else "",
            diagnostic.message,
        )
        if identity not in self._diagnostic_identities:
            self._diagnostic_identities.add(identity)
            self.diagnostics.append(diagnostic)


__all__ = [
    "DiagnosticMetadata",
    "IllustrationDiagnostic",
    "IllustrationDiagnosticsMixin",
    "WarningEvents",
]
