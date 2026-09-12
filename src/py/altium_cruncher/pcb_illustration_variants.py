"""Read-only project variant selection for illustrated board outputs."""

from __future__ import annotations

from copy import copy
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from altium_monkey.altium_design import AltiumDesign
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc

from .output_path_templates import sanitize_output_name


@dataclass(frozen=True)
class IllustrationVariant:
    name: str | None
    excluded_designators: frozenset[str]
    project_parameters: dict[str, str]
    component_parameters: dict[str, dict[str, str]]

    @property
    def folder(self) -> str:
        return sanitize_output_name(self.name or "base")

    def board(self, pcbdoc: AltiumPcbDoc) -> AltiumPcbDoc:
        """Keep saved geometry and component indices; copy overridden parameters."""
        if not self.component_parameters:
            return pcbdoc
        result = copy(pcbdoc)
        result.components = [
            replace(
                component,
                parameters={
                    **(component.parameters or {}),
                    **self.component_parameters[component.designator],
                },
            )
            if component.designator in self.component_parameters
            else component
            for component in pcbdoc.components
        ]
        return result


def illustration_variants(
    design: AltiumDesign,
    *,
    variant: str | None = None,
    all_variants: bool = False,
) -> list[IllustrationVariant]:
    available = design.get_variants()
    if variant is not None and variant not in available:
        raise ValueError(
            f"Unknown variant '{variant}'. Available: {', '.join(available) or 'none'}"
        )
    names = [None, *available] if all_variants else [variant]
    results = [_resolve_variant(design, name) for name in names]
    folders = [item.folder.casefold() for item in results]
    if len(folders) != len(set(folders)):
        raise ValueError(
            "Selected variant names collide as output folders; render them separately with -o"
        )
    return results


def _resolve_variant(design: AltiumDesign, name: str | None) -> IllustrationVariant:
    data = design.project.variants[name] if name is not None else {}
    _reject_alternate_models(data.get("variations", []), name)
    parameters = dict(design.get_pcb_project_parameters())
    parameters["VariantName"] = name or ""
    for row in data.get("parameters", []):
        key = row.get("ParameterName") or row.get("Name")
        if key:
            parameters[key] = row.get("VariantValue", row.get("Value", ""))
    dnp = frozenset(
        row["Designator"]
        for row in data.get("variations", [])
        if str(row.get("Kind")) == "1" and row.get("Designator")
    )
    return IllustrationVariant(
        name,
        dnp,
        parameters,
        design.get_variant_parameter_overrides(name) if name is not None else {},
    )


def _reject_alternate_models(rows: list[dict[str, str]], name: str | None) -> None:
    alternates = [
        row.get("Designator", "?")
        for row in rows
        if str(row.get("Kind", "0")) not in {"0", "1"}
    ]
    if alternates:
        raise ValueError(
            f"Variant '{name}' contains alternate-part substitutions for {', '.join(alternates)}; "
            "alternate 3D model resolution is not supported yet"
        )
