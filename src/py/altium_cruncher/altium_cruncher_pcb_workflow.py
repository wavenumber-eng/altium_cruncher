"""Local helpers for Altium-backed PCB command workflows."""

from __future__ import annotations

from dataclasses import dataclass
import logging
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from altium_monkey.altium_design import AltiumDesign
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class CruncherPcbRenderInput:
    """Resolved PCB render context for one board in a command workflow."""

    board_key: str
    pcb_path: Path
    pcbdoc: AltiumPcbDoc
    project_parameters: dict[str, str]


def _path_matches_pcbdoc(candidate: Path, target: Path) -> bool:
    candidate_name = str(getattr(candidate, "name", "") or "").strip().lower()
    target_name = str(getattr(target, "name", "") or "").strip().lower()
    if candidate_name and target_name and candidate_name == target_name:
        return True

    candidate_stem = str(getattr(candidate, "stem", "") or "").strip().lower()
    target_stem = str(getattr(target, "stem", "") or "").strip().lower()
    if candidate_stem and target_stem and candidate_stem == target_stem:
        return True

    try:
        return candidate.resolve() == target.resolve()
    except Exception:
        return False


PCB_PROJECT_CONTEXT_MODES = ("auto", "none", "schematic")


def _normalize_pcb_project_context(value: str | None) -> str:
    raw = str(value or "auto").strip().lower().replace("_", "-")
    aliases = {
        "": "auto",
        "default": "auto",
        "legacy": "auto",
        "project": "schematic",
        "full": "schematic",
        "full-project": "schematic",
        "sch": "schematic",
        "schdocs": "schematic",
        "board": "none",
        "board-only": "none",
        "pcbdoc": "none",
        "off": "none",
        "false": "none",
    }
    mode = aliases.get(raw, raw)
    if mode not in PCB_PROJECT_CONTEXT_MODES:
        raise ValueError(
            "project_context must be one of: " + ", ".join(PCB_PROJECT_CONTEXT_MODES)
        )
    return mode


def load_design_for_pcb_input(
    input_file: Path,
    *,
    project_context: str | None = "auto",
) -> tuple["AltiumDesign", str]:
    """
    Load an AltiumDesign from a PcbDoc/PrjPcb input.

    Returns ``(design, source_tag)`` where source_tag records whether the input
    was a project, a board-only document, or a PcbDoc with discovered project
    context.
    """
    from altium_monkey.altium_design import AltiumDesign

    resolved_input = Path(input_file).resolve()
    context_mode = _normalize_pcb_project_context(project_context)
    suffix = resolved_input.suffix.lower()
    if suffix == ".prjpcb":
        return _load_design_from_prjpcb(resolved_input, context_mode)
    if suffix != ".pcbdoc":
        raise ValueError(f"Unsupported PCB design input type: {suffix}")

    if context_mode == "none":
        return AltiumDesign.from_pcbdoc(resolved_input), "pcbdoc_board_only"

    sibling_projects = sorted(
        [
            p
            for p in resolved_input.parent.iterdir()
            if p.is_file() and p.suffix.lower() == ".prjpcb"
        ],
        key=lambda p: p.name.lower(),
    )
    for prjpcb in sibling_projects:
        try:
            design = AltiumDesign.from_prjpcb(prjpcb)
            pcb_paths = design.get_pcbdoc_paths()
        except Exception as exc:
            log.debug(
                "Skipping project context probe for %s via %s: %s",
                resolved_input.name,
                prjpcb.name,
                exc,
            )
            continue

        for candidate in pcb_paths:
            if _path_matches_pcbdoc(candidate, resolved_input):
                log.info(
                    "Resolved project context for %s via %s",
                    resolved_input.name,
                    prjpcb.name,
                )
                return design, "pcbdoc_with_project_context"

    from altium_monkey.altium_netlist_options import NetlistOptions
    from altium_monkey.altium_prjpcb import AltiumPrjPcb
    from altium_monkey.altium_schdoc import AltiumSchDoc

    pseudo_prj_path = resolved_input.parent / f"{resolved_input.stem}__pseudo.PrjPcb"
    pseudo_project = AltiumPrjPcb.create_minimal(name=resolved_input.stem)
    pseudo_project.filepath = pseudo_prj_path
    pseudo_project.add_document(resolved_input.name)

    schdocs = []
    for schdoc_path in sorted(
        [
            p
            for p in resolved_input.parent.iterdir()
            if p.is_file() and p.suffix.lower() == ".schdoc"
        ],
        key=lambda p: p.name.lower(),
    ):
        pseudo_project.add_document(schdoc_path.name)
        try:
            schdocs.append(AltiumSchDoc(schdoc_path))
        except Exception as exc:
            log.warning(
                "Skipping pseudo-project SchDoc load for %s: %s", schdoc_path.name, exc
            )

    design = AltiumDesign.from_pcbdoc(resolved_input)
    design.project = pseudo_project
    design.schdocs = schdocs
    options = NetlistOptions.from_prjpcb(pseudo_project)
    sheet_params: dict[str, str] = {}
    for schdoc in schdocs:
        try:
            sheet_params.update(schdoc.get_parameter_dict())
        except Exception:
            continue
    options.sheet_parameters = sheet_params
    design._options = options

    log.info(
        "Using pseudo project context for %s (schdocs=%d)",
        resolved_input.name,
        len(schdocs),
    )
    return design, "pcbdoc_pseudo_project"


def _load_design_from_prjpcb(
    input_file: Path,
    context_mode: str,
) -> tuple["AltiumDesign", str]:
    from altium_monkey.altium_design import AltiumDesign

    if context_mode == "none":
        return _load_prjpcb_board_only_design(input_file), "prjpcb_board_only"
    return AltiumDesign.from_prjpcb(input_file), "prjpcb_input"


def _load_prjpcb_board_only_design(input_file: Path) -> "AltiumDesign":
    """Load a project file without parsing schematic documents."""
    from altium_monkey.altium_design import AltiumDesign
    from altium_monkey.altium_netlist_options import NetlistOptions
    from altium_monkey.altium_prjpcb import AltiumPrjPcb

    project = AltiumPrjPcb(input_file)
    return AltiumDesign(
        project=project,
        schdocs=[],
        _options=NetlistOptions.from_prjpcb(project),
    )


def iter_pcb_render_inputs(
    design,
    *,
    pcbdoc_selector: Path | str | None = None,
) -> list[CruncherPcbRenderInput]:
    """Resolve board render inputs from an AltiumDesign."""
    pcb_paths = design.get_pcbdoc_paths(selector=pcbdoc_selector)
    if not pcb_paths:
        if design.project:
            raise ValueError(f"No PcbDoc found in project: {design.project.filepath}")
        raise ValueError("No standalone PcbDoc is loaded in this design")

    project_parameters = design.get_pcb_project_parameters()
    return [
        CruncherPcbRenderInput(
            board_key=pcb_path.stem,
            pcb_path=pcb_path,
            pcbdoc=design.load_pcbdoc(selector=pcb_path),
            project_parameters=dict(project_parameters),
        )
        for pcb_path in pcb_paths
    ]
