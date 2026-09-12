"""Project metadata must survive Toon's schematic-free loading path."""

from pathlib import Path
from types import SimpleNamespace

import pytest
from altium_monkey.altium_design import AltiumDesign
from altium_monkey.altium_prjpcb import AltiumPrjPcb

from altium_cruncher.altium_cruncher_pcb_workflow import load_design_for_pcb_input
from altium_cruncher.pcb_illustration_variants import illustration_variants


ROOT = Path(__file__).resolve().parents[1]
RT = ROOT / "tests/assets/projects/rt_super_c1/input/RT_SUPER_C1.PrjPcb"


def test_project_metadata_and_all_variants_match_full_design(monkeypatch):
    full = AltiumDesign.from_prjpcb(RT)

    def forbidden(*args, **kwargs):
        pytest.fail("Preview context must not parse schematics or boards")

    monkeypatch.setattr(AltiumDesign, "from_prjpcb", forbidden)
    monkeypatch.setattr(AltiumDesign, "from_pcbdoc", forbidden)
    preview, tag = load_design_for_pcb_input(RT, load_schematics=False)
    assert tag == "prjpcb_input"
    assert preview.schdocs == []
    assert preview.get_pcbdoc_paths() == full.get_pcbdoc_paths()
    assert preview.get_pcb_project_parameters() == full.get_pcb_project_parameters()
    assert illustration_variants(preview, all_variants=True) == illustration_variants(full, all_variants=True)


def test_direct_board_discovers_project_without_loading_schematics(tmp_path, monkeypatch):
    board = tmp_path / "board.PcbDoc"
    board.touch()
    unrelated = tmp_path / "other.PcbDoc"
    unrelated.touch()
    for name, document in (("a-unrelated", unrelated), ("b-matching", board)):
        project = AltiumPrjPcb.create_minimal(name=name)
        project.add_document(document.name)
        project.add_document("unavailable.SchDoc")
        project.save(tmp_path / f"{name}.PrjPcb")

    def forbidden(*args, **kwargs):
        pytest.fail("Discovery must not enter full design loading")

    monkeypatch.setattr(AltiumDesign, "from_prjpcb", forbidden)
    monkeypatch.setattr(AltiumDesign, "from_pcbdoc", forbidden)
    design, tag = load_design_for_pcb_input(board, load_schematics=False)
    assert tag == "pcbdoc_with_project_context"
    assert design.project.filepath.name == "b-matching.PrjPcb"
    assert design.get_pcbdoc_paths() == [board]
    assert design.schdocs == []


def test_standalone_preview_retains_pseudo_project_document_list(tmp_path, monkeypatch):
    import altium_monkey.altium_schdoc as schdoc_module

    board = tmp_path / "board.PcbDoc"
    board.touch()
    sheet = tmp_path / "board.SchDoc"
    sheet.write_bytes(b"not a valid schematic")
    monkeypatch.setattr(AltiumDesign, "from_pcbdoc", lambda path: SimpleNamespace())
    calls = []
    monkeypatch.setattr(schdoc_module, "AltiumSchDoc", lambda path: calls.append(path))
    design, tag = load_design_for_pcb_input(board, load_schematics=False)
    assert tag == "pcbdoc_pseudo_project"
    assert design.project.get_pcbdoc_paths() == [board]
    assert design.project.get_schdoc_paths() == [sheet]
    assert design.schdocs == []
    assert design._options.sheet_parameters == {}
    assert calls == []


@pytest.mark.parametrize("context", ["auto", "schematic"])
def test_existing_full_design_default_is_preserved(tmp_path, monkeypatch, context):
    sentinel = object()
    monkeypatch.setattr(AltiumDesign, "from_prjpcb", lambda path: sentinel)
    design, tag = load_design_for_pcb_input(tmp_path / "board.PrjPcb", project_context=context)
    assert design is sentinel
    assert tag == "prjpcb_input"


def test_explicit_board_only_still_skips_project_discovery(tmp_path, monkeypatch):
    sentinel = object()
    monkeypatch.setattr(AltiumDesign, "from_pcbdoc", lambda path: sentinel)
    design, tag = load_design_for_pcb_input(
        tmp_path / "board.PcbDoc", project_context="none", load_schematics=False
    )
    assert design is sentinel
    assert tag == "pcbdoc_board_only"
