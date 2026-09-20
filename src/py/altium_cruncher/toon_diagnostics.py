"""Deterministic collection and presentation of nonfatal Toon diagnostics."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Literal


ToonWarningCategory = Literal[
    "missing_model",
    "unsupported_model",
    "invalid_model_geometry",
    "geometer_geometry",
    "region_resolution",
    "rotation_resolution",
    "clipping",
]


@dataclass(frozen=True)
class ToonDiagnostic:
    """One grouped warning and its stable structured identity."""

    key: str
    code: str
    severity: Literal["warning"]
    category: ToonWarningCategory
    producer: str
    message: str
    occurrence_count: int
    input: str | None = None
    board: str | None = None
    variant: str | None = None
    view: str | None = None
    component_designator: str | None = None
    body_index: int | None = None
    model_identity: str | None = None
    detail: dict[str, object] | None = None

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "key": self.key,
            "code": self.code,
            "severity": self.severity,
            "category": self.category,
            "producer": self.producer,
            "message": self.message,
            "occurrence_count": self.occurrence_count,
        }
        for name in (
            "input",
            "board",
            "variant",
            "view",
            "component_designator",
            "body_index",
            "model_identity",
            "detail",
        ):
            value = getattr(self, name)
            if value is not None:
                result[name] = value
        return result


@dataclass
class _CollectedDiagnostic:
    diagnostic: ToonDiagnostic
    occurrence_keys: set[str] = field(default_factory=set)


class ToonDiagnosticCollector:
    """Merge warnings by structured identity, independent of completion order."""

    def __init__(self) -> None:
        self._items: dict[str, _CollectedDiagnostic] = {}

    def add(
        self,
        *,
        code: str,
        category: ToonWarningCategory,
        producer: str,
        message: str,
        input: str | None = None,
        board: str | None = None,
        variant: str | None = None,
        view: str | None = None,
        component_designator: str | None = None,
        body_index: int | None = None,
        model_identity: str | None = None,
        detail: Mapping[str, object] | None = None,
        occurrence_key: str | None = None,
    ) -> ToonDiagnostic:
        normalized_detail = (
            None
            if detail is None
            else json.loads(
                json.dumps(dict(detail), sort_keys=True, allow_nan=False)
            )
        )
        identity = {
            "code": str(code),
            "severity": "warning",
            "category": category,
            "producer": str(producer),
            "message": str(message),
            "input": input,
            "board": board,
            "variant": variant,
            "view": view,
            "component_designator": component_designator,
            "body_index": body_index,
            "model_identity": model_identity,
            "detail": normalized_detail,
        }
        encoded = json.dumps(
            identity, sort_keys=True, separators=(",", ":"), allow_nan=False
        )
        key = "toon-warning:" + hashlib.sha256(encoded.encode()).hexdigest()
        item = self._items.get(key)
        occurrence = occurrence_key or key
        if item is None:
            diagnostic = ToonDiagnostic(
                key=key,
                code=str(code),
                severity="warning",
                category=category,
                producer=str(producer),
                message=str(message),
                occurrence_count=1,
                input=input,
                board=board,
                variant=variant,
                view=view,
                component_designator=component_designator,
                body_index=body_index,
                model_identity=model_identity,
                detail=normalized_detail,
            )
            item = _CollectedDiagnostic(diagnostic, {occurrence})
            self._items[key] = item
        elif occurrence not in item.occurrence_keys:
            item.occurrence_keys.add(occurrence)
            item.diagnostic = ToonDiagnostic(
                **{
                    **item.diagnostic.__dict__,
                    "occurrence_count": len(item.occurrence_keys),
                }
            )
        return item.diagnostic

    @property
    def diagnostics(self) -> tuple[ToonDiagnostic, ...]:
        return tuple(
            sorted(
                (item.diagnostic for item in self._items.values()),
                key=_diagnostic_sort_key,
            )
        )

    def report(self) -> dict[str, object]:
        diagnostics = self.diagnostics
        grouped: dict[tuple[str, str], list[ToonDiagnostic]] = defaultdict(list)
        for diagnostic in diagnostics:
            grouped[(diagnostic.category, diagnostic.code)].append(diagnostic)
        groups: list[dict[str, object]] = []
        for (category, code), items in sorted(grouped.items()):
            designators = sorted(
                {
                    item.component_designator
                    for item in items
                    if item.component_designator
                }
            )
            bodies = {
                (item.component_designator, item.body_index)
                for item in items
                if item.body_index is not None
            }
            models = {item.model_identity for item in items if item.model_identity}
            groups.append(
                {
                    "category": category,
                    "code": code,
                    "unique_diagnostic_count": len(items),
                    "occurrence_count": sum(
                        item.occurrence_count for item in items
                    ),
                    "affected_component_count": len(designators),
                    "affected_body_count": len(bodies),
                    "affected_model_count": len(models),
                    "sample_designators": designators[:8],
                }
            )
        return {
            "schema": "toon.warning_report.a0",
            "summary": {
                "unique_diagnostic_count": len(diagnostics),
                "occurrence_count": sum(
                    item.occurrence_count for item in diagnostics
                ),
                "groups": groups,
            },
            "diagnostics": [item.to_dict() for item in diagnostics],
        }

    def write(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.report(), indent=2, sort_keys=False) + "\n",
            encoding="utf-8",
        )

    def summary_lines(self) -> tuple[str, ...]:
        report = self.report()
        summary = report["summary"]
        assert isinstance(summary, dict)
        unique = int(summary["unique_diagnostic_count"])
        occurrences = int(summary["occurrence_count"])
        if unique == 0:
            return ()
        lines = [
            f"Nonfatal warnings: {unique} unique, {occurrences} occurrence"
            f"{'s' if occurrences != 1 else ''}"
        ]
        groups = summary["groups"]
        assert isinstance(groups, list)
        for group in groups:
            assert isinstance(group, dict)
            sample = group["sample_designators"]
            assert isinstance(sample, list)
            suffix = f"; examples: {', '.join(str(item) for item in sample)}" if sample else ""
            lines.append(
                f"  {group['category']} / {group['code']}: "
                f"{group['unique_diagnostic_count']} unique, "
                f"{group['occurrence_count']} occurrence"
                f"{'s' if group['occurrence_count'] != 1 else ''}{suffix}"
            )
        return tuple(lines)

    def all_lines(self) -> tuple[str, ...]:
        lines = list(self.summary_lines())
        for item in self.diagnostics:
            context = "/".join(
                str(value)
                for value in (
                    item.board,
                    item.variant,
                    item.view,
                    item.component_designator,
                )
                if value
            )
            lines.append(f"  {context + ': ' if context else ''}{item.message}")
        return tuple(lines)


def _diagnostic_sort_key(item: ToonDiagnostic) -> tuple[object, ...]:
    return (
        item.category,
        item.code,
        item.producer,
        item.input or "",
        item.board or "",
        item.variant or "",
        item.view or "",
        item.component_designator or "",
        -1 if item.body_index is None else item.body_index,
        item.model_identity or "",
        item.message,
        item.key,
    )


__all__ = [
    "ToonDiagnostic",
    "ToonDiagnosticCollector",
    "ToonWarningCategory",
]
