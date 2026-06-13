from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def test_pcblib_create_cli_writes_library_and_generated_mco(tmp_path: Path) -> None:
    output_file = tmp_path / "fixture.PcbLib"
    mco_file = tmp_path / "fixture.mco.json"

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "altium_cruncher",
            "pcblib",
            "create",
            str(output_file),
            "--footprint",
            "DBG_CONTACT_FP",
            "--height",
            "12mil",
            "--description",
            "Debug contact footprint",
            "--parameter",
            "AREA=1mil^2",
            "--primitive-parameter",
            "Value=A|B=C",
            "--emit-mco",
            str(mco_file),
            "--json",
        ],
        cwd=PACKAGE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["ok"] is True
    assert [result["op"] for result in payload["results"]] == [
        "pcblib.create",
        "pcblib.add_footprint",
    ]

    generated_mco = json.loads(mco_file.read_text(encoding="utf-8"))
    assert [operation["op"] for operation in generated_mco["operations"]] == [
        "pcblib.create",
        "pcblib.add_footprint",
    ]
    assert generated_mco["operations"][1]["args"]["primitive_parameters"] == {
        "Value": "A|B=C"
    }

    from altium_monkey import AltiumPcbLib

    pcblib = AltiumPcbLib.from_file(output_file)
    assert [footprint.name for footprint in pcblib.footprints] == ["DBG_CONTACT_FP"]
    footprint = pcblib.footprints[0]
    assert footprint.parameters["HEIGHT"] == "12mil"
    assert footprint.parameters["DESCRIPTION"] == "Debug contact footprint"
    assert footprint.parameters["AREA"] == "1mil^2"
    assert footprint.footprint_primitive_parameters["Value"] == "A|B=C"
