from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest

from altium_cruncher import altium_cruncher_cmd_megamaid as megamaid
import altium_monkey.altium_schdoc as schdoc_module
from altium_monkey.altium_schdoc import AltiumSchDoc as RealAltiumSchDoc
from altium_monkey.altium_sch_image_payload import decode_sch_embedded_image_payload


PNG_BYTES = b"\x89PNG\r\n\x1a\nembedded-png"
PACKAGE_ROOT = Path(__file__).resolve().parents[2]
HYDROSCOPE_PROJECT = (
    PACKAGE_ROOT
    / "tests"
    / "assets"
    / "projects"
    / "hydroscope"
    / "input"
    / "Hydroscope.PrjPcb"
)


def _minimal_bmp_preview() -> bytes:
    header = bytearray(54)
    header[0:2] = b"BM"
    header[2:6] = (54).to_bytes(4, "little")
    header[10:14] = (54).to_bytes(4, "little")
    header[14:18] = (40).to_bytes(4, "little")
    header[18:22] = (1).to_bytes(4, "little", signed=True)
    header[22:26] = (1).to_bytes(4, "little", signed=True)
    header[26:28] = (1).to_bytes(2, "little")
    header[28:30] = (24).to_bytes(2, "little")
    return bytes(header)


def _wrapped_png_payload() -> bytes:
    class_name = b"TdxPNGImage"
    return _minimal_bmp_preview() + bytes([len(class_name)]) + class_name + PNG_BYTES


def test_megamaid_schematic_image_extract_writes_preferred_payload(
    tmp_path: Path,
    monkeypatch,
) -> None:
    class FakeSchDoc:
        @staticmethod
        def _embedded_image_payload_for_output(data: bytes) -> tuple[bytes, str | None]:
            payload = decode_sch_embedded_image_payload(data)
            extension = RealAltiumSchDoc._embedded_image_extension_from_format(
                payload.preferred_format
            )
            return payload.preferred_data, extension

        def __init__(self, path: Path) -> None:
            self.path = path
            self.images = [
                SimpleNamespace(filename="logo.dat", image_data=_wrapped_png_payload()),
                SimpleNamespace(filename="logo.png", image_data=PNG_BYTES),
            ]

    monkeypatch.setattr(schdoc_module, "AltiumSchDoc", FakeSchDoc)

    entries = megamaid._extract_project_schematic_images(
        schdoc_paths=[tmp_path / "CPU.SchDoc"],
        output_root=tmp_path / "out",
        debug=False,
    )

    assert len(entries) == 2
    assert entries[0]["deduplicated"] is False
    assert entries[1]["deduplicated"] is True

    output_file = Path(str(entries[0]["output_file"]))
    assert output_file.name == "logo.png"
    assert output_file.read_bytes() == PNG_BYTES
    assert entries[1]["output_file"] == str(output_file)


def test_megamaid_hydroscope_extracts_images_and_models(tmp_path: Path) -> None:
    output_dir = tmp_path / "megamaid"

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "megamaid",
            str(HYDROSCOPE_PROJECT),
            "-o",
            str(output_dir),
        ],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    combined_output = completed.stdout + completed.stderr
    assert completed.returncode == 0, combined_output
    assert "Traceback" not in combined_output
    assert "Logging error" not in combined_output

    manifest = json.loads((output_dir / "megamaid_manifest.json").read_text())
    assert manifest["embedded_assets"]["model_file_count"] == 29
    assert manifest["sch_images"]["image_file_count"] == 7

    png_paths = sorted((output_dir / "sch_images").glob("*.png"))
    assert len(png_paths) == 7
    for png_path in png_paths:
        data = png_path.read_bytes()
        assert data.startswith(b"\x89PNG\r\n\x1a\n"), png_path.name
        assert not data.startswith(b"BM"), png_path.name


def _run_megamaid_command(command: list[str], output_dir: Path) -> str:
    completed = subprocess.run(
        [*command, str(HYDROSCOPE_PROJECT), "-o", str(output_dir)],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    combined_output = completed.stdout + completed.stderr
    assert completed.returncode == 0, combined_output
    return combined_output


def _relative_file_map(root: Path, subdir: str) -> dict[str, bytes]:
    base = root / subdir
    return {
        str(path.relative_to(base)).replace("\\", "/"): path.read_bytes()
        for path in sorted(base.rglob("*"))
        if path.is_file()
    }


def test_native_megamaid_matches_python_for_hydroscope_assets(tmp_path: Path) -> None:
    native_exe = os.environ.get("ALTIUM_CRUNCHER_NATIVE_EXE")
    if not native_exe:
        pytest.skip("ALTIUM_CRUNCHER_NATIVE_EXE is not set")

    python_output_dir = tmp_path / "python"
    native_output_dir = tmp_path / "native"

    python_log = _run_megamaid_command(
        [sys.executable, "-m", "altium_cruncher", "megamaid"],
        python_output_dir,
    )
    native_log = _run_megamaid_command([native_exe, "megamaid"], native_output_dir)

    assert "Traceback" not in python_log + native_log
    assert "Logging error" not in python_log + native_log

    for subdir in ("sch_images", "embedded_models"):
        assert _relative_file_map(native_output_dir, subdir) == _relative_file_map(
            python_output_dir,
            subdir,
        )
