from __future__ import annotations

import sys
from pathlib import Path
from types import ModuleType

import pytest

from altium_cruncher.altium_cruncher_cmd_extract import _extract_schdocs_to_output

DUPLICATE_SYMBOL_NAME = "ERJ-3EKF1002V"
DUPLICATE_SYMBOL_FILE = f"{DUPLICATE_SYMBOL_NAME}.SchLib"


class FakeSchDoc:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)

    def extract_symbols(
        self,
        *,
        output_dir: Path,
        combined_schlib: bool,
        split_schlibs: bool,
        debug: bool,
    ) -> dict[str, bool]:
        del debug
        output_dir.mkdir(parents=True, exist_ok=True)
        if split_schlibs:
            (output_dir / DUPLICATE_SYMBOL_FILE).write_text(
                self.path.stem,
                encoding="utf-8",
            )
        if combined_schlib:
            (output_dir / f"{self.path.stem}.SchLib").write_text(
                f"combined:{self.path.stem}",
                encoding="utf-8",
            )
        return {DUPLICATE_SYMBOL_NAME: True}


def _install_fake_schdoc(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_module = ModuleType("altium_monkey.altium_schdoc")
    fake_module.AltiumSchDoc = FakeSchDoc
    monkeypatch.setitem(sys.modules, "altium_monkey.altium_schdoc", fake_module)


def test_project_schdoc_extract_split_outputs_are_namespaced(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_schdoc(monkeypatch)
    output_dir = tmp_path / "schlib"

    successful, failed, results = _extract_schdocs_to_output(
        [tmp_path / "case1.SchDoc", tmp_path / "Sheet1.SchDoc"],
        output_dir,
        split=True,
        combined=False,
        debug=False,
    )

    assert successful == 2
    assert failed == 0
    assert results == {
        f"case1/{DUPLICATE_SYMBOL_NAME}": True,
        f"Sheet1/{DUPLICATE_SYMBOL_NAME}": True,
    }
    assert (output_dir / "case1" / DUPLICATE_SYMBOL_FILE).read_text(
        encoding="utf-8"
    ) == "case1"
    assert (output_dir / "Sheet1" / DUPLICATE_SYMBOL_FILE).read_text(
        encoding="utf-8"
    ) == "Sheet1"
    assert not (output_dir / DUPLICATE_SYMBOL_FILE).exists()


def test_project_schdoc_extract_combined_outputs_stay_at_schlib_root(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_schdoc(monkeypatch)
    output_dir = tmp_path / "schlib"

    successful, failed, _ = _extract_schdocs_to_output(
        [tmp_path / "case1.SchDoc", tmp_path / "Sheet1.SchDoc"],
        output_dir,
        split=True,
        combined=True,
        debug=False,
    )

    assert successful == 2
    assert failed == 0
    assert (output_dir / "case1.SchLib").read_text(encoding="utf-8") == "combined:case1"
    assert (output_dir / "Sheet1.SchLib").read_text(
        encoding="utf-8"
    ) == "combined:Sheet1"
    assert not (output_dir / "case1" / "case1.SchLib").exists()
    assert not (output_dir / "Sheet1" / "Sheet1.SchLib").exists()
