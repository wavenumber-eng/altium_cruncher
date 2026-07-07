+++
type = "requirement"
id = "public_package-req-0001"
domain = "public_package"
status = "implemented"
title = "Public CLI Release Surface Is Tested"
created = "2026-07-06"
adr_refs = ["public_package-adr-0001"]
design_refs = [
  "docs/design/cli/sch-ir.html",
  "docs/design/cli/sch-svg.html",
]

[[verification_refs]]
kind = "local_pytest"
target = "tests/test_sch_ir_command.py::test_sch_ir_writes_single_schdoc_gotir_json"
+++

# Public CLI Release Surface Is Tested

The public package release surface includes command registration, command
documentation, package version metadata, and focused behavior tests for newly
added commands.

For the `2026.7.6` release, the `sch-ir` command exports gotIR JSON through the
same onscreen schematic IR path used by schematic SVG rendering and the
interactive schematic viewer.
