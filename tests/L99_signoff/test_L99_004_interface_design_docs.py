"""Design documentation signoff for dataclasses and major interfaces."""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass
from pathlib import Path


def _project_root() -> Path:
    """Find the repository root from this test file."""
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Could not locate repository root")


@dataclass(frozen=True)
class InterfaceDoc:
    """Machine-readable interface documentation metadata."""

    name: str
    doc_path: Path
    section_text: str
    rack_stratum: str
    test_file: Path
    test_target: str


PACKAGE_ROOT = _project_root()
SOURCE_ROOT = PACKAGE_ROOT / "src" / "py" / "altium_cruncher"
DESIGN_ROOT = PACKAGE_ROOT / "docs" / "design"
INTERFACE_MANIFEST = (
    PACKAGE_ROOT / "docs" / "contracts" / "interface_design_manifest.v0.json"
)


def _is_dataclass_decorator(decorator: ast.expr) -> bool:
    """Return whether an AST decorator represents dataclass usage."""
    if isinstance(decorator, ast.Name):
        return decorator.id == "dataclass"
    if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
        return decorator.func.id == "dataclass"
    return False


def _public_dataclasses() -> set[str]:
    """Return package dataclass names that require design docs."""
    dataclasses: set[str] = set()
    for source_path in SOURCE_ROOT.glob("*.py"):
        tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            if node.name.startswith("_"):
                continue
            if any(
                _is_dataclass_decorator(decorator) for decorator in node.decorator_list
            ):
                dataclasses.add(node.name)
    return dataclasses


def _major_interfaces() -> set[str]:
    """Return explicitly listed major interfaces that require design docs."""
    payload = json.loads(INTERFACE_MANIFEST.read_text(encoding="utf-8"))
    assert payload["schema"] == "altium_cruncher.interface_design_manifest.v0"
    entries = payload["major_interfaces"]
    assert isinstance(entries, list)
    names: set[str] = set()
    for entry in entries:
        if isinstance(entry, str):
            names.add(entry)
        else:
            names.add(str(entry["name"]))
    return names


def _interface_docs() -> dict[str, InterfaceDoc]:
    """Collect interface design-doc sections from HTML design docs."""
    docs: dict[str, InterfaceDoc] = {}
    section_pattern = re.compile(
        r"<section\b(?P<attrs>[^>]*)data-interface=\"(?P<name>[^\"]+)\"(?P<attrs2>[^>]*)>"
        r"(?P<body>.*?)</section>",
        re.DOTALL,
    )
    attr_pattern = re.compile(r"(?P<name>data-[a-z-]+)=\"(?P<value>[^\"]+)\"")

    for doc_path in DESIGN_ROOT.rglob("*.html"):
        text = doc_path.read_text(encoding="utf-8")
        for match in section_pattern.finditer(text):
            attrs = dict(attr_pattern.findall(match.group("attrs") + match.group("attrs2")))
            name = match.group("name")
            docs[name] = InterfaceDoc(
                name=name,
                doc_path=doc_path,
                section_text=match.group("body"),
                rack_stratum=attrs.get("data-rack-stratum", ""),
                test_file=PACKAGE_ROOT / attrs.get("data-test-file", ""),
                test_target=attrs.get("data-test-target", ""),
            )
    return docs


def _required_interfaces() -> set[str]:
    """Return the full set of interfaces governed by design-doc signoff."""
    return _public_dataclasses() | _major_interfaces()


def test_dataclasses_and_major_interfaces_have_design_docs() -> None:
    """Verify design-doc coverage for data classes and major interfaces."""
    required = _required_interfaces()
    docs = _interface_docs()

    missing = sorted(required - set(docs))
    assert missing == [], "Missing interface design docs:\n" + "\n".join(missing)


def test_interface_design_docs_define_rationale_tests_and_working_state() -> None:
    """Verify each interface doc section records design and test expectations."""
    docs = _interface_docs()
    failures: list[str] = []

    for name in sorted(_required_interfaces() & set(docs)):
        doc = docs[name]
        for required_text in (
            "Rationale",
            "Purpose",
            "Test Requirements",
            "Working Definition",
        ):
            if required_text not in doc.section_text:
                failures.append(f"{name}: missing {required_text} in {doc.doc_path}")

    assert failures == [], "Interface design content gaps:\n" + "\n".join(failures)


def test_interface_design_docs_point_to_rack_exercising_tests() -> None:
    """Verify interface docs point to an exercising Rack stratum and test target."""
    docs = _interface_docs()
    failures: list[str] = []

    for name in sorted(_required_interfaces() & set(docs)):
        doc = docs[name]
        stratum = PACKAGE_ROOT / "tests" / doc.rack_stratum / "STRATUM.toml"
        if not stratum.exists():
            failures.append(f"{name}: missing Rack stratum {doc.rack_stratum}")
        if not doc.test_file.exists():
            failures.append(f"{name}: missing test file {doc.test_file}")
            continue

        test_text = doc.test_file.read_text(encoding="utf-8")
        if doc.test_target not in test_text:
            failures.append(f"{name}: test target not found: {doc.test_target}")

    assert failures == [], "Interface test ownership gaps:\n" + "\n".join(failures)
